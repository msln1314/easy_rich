# -*- coding: utf-8 -*-
"""决策Agent

综合各专业分析师的观点，给出最终投资建议。
"""

import re
import logging
from typing import Optional, List, Dict, Any

from app.services.ai.agents.base_agent import BaseAgent
from app.services.ai.context import AgentContext
from app.models.ai_models import AgentOpinion, Signal

logger = logging.getLogger(__name__)


class DecisionAgent(BaseAgent):
    """决策Agent

    综合各专业分析师的观点，给出最终投资建议。
    主要职责包括：
    - 汇总技术面、基本面、消息面的分析结果
    - 评估风险因素
    - 给出综合投资建议
    - 提供操作策略

    Attributes:
        agent_name: Agent名称标识
        agent_type: Agent类型
        tool_names: 可用工具名称列表（决策Agent不需要调用工具）
    """

    agent_name: str = "decision"
    agent_type: str = "decision"
    tool_names: Optional[List[str]] = None  # 决策Agent不需要调用工具
    max_steps: int = 3  # 决策Agent不需要多次调用

    SYSTEM_PROMPT = """你是投资决策顾问，负责综合各专业分析师的观点，给出最终投资建议。

你需要汇总并分析以下专业意见：

## 1. 技术面分析
- K线形态和趋势判断
- 均线系统信号
- 技术指标信号
- 支撑压力位

## 2. 基本面分析
- 财务指标评估
- 成长性判断
- 估值水平
- 行业地位

## 3. 消息面分析
- 重大新闻事件
- 公告解读
- 市场情绪
- 政策影响

## 4. 风险评估
- 风险等级
- 主要风险点
- 仓位建议
- 止损位

## 决策原则
1. 多维度综合判断，不偏信单一信号
2. 风险优先原则，在高风险下倾向保守
3. 置信度加权，高置信度分析权重更大
4. 矛盾信号时，以风险控制为导向

## 最终判断标准
- 强烈买入：多维度看多，风险可控，高置信度
- 买入：整体看多，风险可控
- 持有：信号不明朗或存在较大分歧
- 卖出：整体看空或风险较高
- 强烈卖出：多维度看空或存在重大风险

## 输出格式要求
请按照以下格式输出分析结果：

**最终判断**：[强烈买入/买入/持有/卖出/强烈卖出]

**置信度**：[0-100]%

**目标价**：[价格区间]（如可估算）

**止损位**：[建议止损价格/比例]

**仓位建议**：[建议仓位比例]

**持有周期**：[短期/中期/长期]

**综合分析**：

### 技术面观点汇总
[技术面分析的要点和信号]

### 基本面观点汇总
[基本面分析的要点和信号]

### 消息面观点汇总
[消息面分析的要点和信号]

### 风险评估汇总
[风险评估的要点]

### 决策依据
[综合决策的逻辑和依据]

**操作建议**：
[具体的操作策略，包括建仓/减仓时机、止盈止损设置等]

**风险提示**：
[需要特别关注的风险点]"""

    def system_prompt(self, ctx: AgentContext) -> str:
        """返回系统提示词

        Args:
            ctx: Agent上下文

        Returns:
            系统提示词字符串
        """
        base_prompt = self.SYSTEM_PROMPT

        # 添加股票基本信息
        if ctx.stock_code and ctx.stock_name:
            base_prompt += f"\n\n## 分析对象\n股票代码：{ctx.stock_code}\n股票名称：{ctx.stock_name}"

        # 添加其他Agent的观点汇总
        opinions_summary = self._build_opinions_summary(ctx)
        if opinions_summary:
            base_prompt += f"\n\n## 各专业分析师观点\n{opinions_summary}"

        return base_prompt

    def build_user_message(self, ctx: AgentContext) -> str:
        """构建用户消息

        Args:
            ctx: Agent上下文

        Returns:
            用户消息字符串
        """
        message_parts = []

        # 添加用户查询
        if ctx.query:
            message_parts.append(f"用户问题：{ctx.query}\n")

        message_parts.append("请综合以上各专业分析师的观点，给出最终的投资决策建议。")

        return "\n".join(message_parts)

    def post_process(
        self, ctx: AgentContext, raw_text: str
    ) -> Optional[AgentOpinion]:
        """解析LLM输出

        从LLM输出的文本中提取关键信息，生成AgentOpinion对象。

        Args:
            ctx: Agent上下文
            raw_text: LLM输出的原始文本

        Returns:
            AgentOpinion对象，如果无法解析则返回None
        """
        if not raw_text:
            return None

        opinion = AgentOpinion(
            agent_name=self.agent_name,
            agent_type=self.agent_type,
        )

        # 解析最终判断
        opinion.signal = self._parse_signal(raw_text)

        # 解析置信度
        opinion.confidence = self._parse_confidence(raw_text)

        # 提取决策相关数据
        supporting_data = self._extract_decision_data(raw_text)
        opinion.supporting_data = supporting_data

        # 完整分析作为推理过程
        opinion.reasoning = raw_text

        return opinion

    def _build_opinions_summary(self, ctx: AgentContext) -> str:
        """构建观点汇总

        Args:
            ctx: Agent上下文

        Returns:
            观点汇总文本
        """
        if not ctx.opinions:
            return ""

        summary_parts = []

        for op in ctx.opinions:
            agent_type = getattr(op, "agent_type", getattr(op, "agent_name", "未知"))
            signal = getattr(op, "signal", Signal.HOLD)
            confidence = getattr(op, "confidence", 0)
            reasoning = getattr(op, "reasoning", "")

            # 获取信号的中文名称
            signal_names = {
                Signal.STRONG_BUY: "强烈买入",
                Signal.BUY: "买入",
                Signal.HOLD: "持有",
                Signal.SELL: "卖出",
                Signal.STRONG_SELL: "强烈卖出",
            }
            signal_name = signal_names.get(signal, "持有")

            summary_parts.append(f"""
### {agent_type}分析
- 判断：{signal_name}
- 置信度：{confidence * 100:.0f}%
- 分析要点：{reasoning[:200] if reasoning else '无'}...
""")

        return "\n".join(summary_parts)

    def _parse_signal(self, text: str) -> Signal:
        """解析信号

        Args:
            text: LLM输出文本

        Returns:
            Signal枚举值
        """
        # 检查明确判断
        if "最终判断" in text:
            judgment_text = text.split("最终判断")[1].split("\n")[0][:30]

            if "强烈买入" in judgment_text:
                return Signal.STRONG_BUY
            elif "买入" in judgment_text:
                return Signal.BUY
            elif "强烈卖出" in judgment_text:
                return Signal.STRONG_SELL
            elif "卖出" in judgment_text:
                return Signal.SELL
            elif "持有" in judgment_text:
                return Signal.HOLD

        # 根据关键词判断
        if "强烈买入" in text:
            return Signal.STRONG_BUY
        elif "强烈卖出" in text:
            return Signal.STRONG_SELL
        elif "买入" in text and "强烈" not in text:
            return Signal.BUY
        elif "卖出" in text and "强烈" not in text:
            return Signal.SELL

        return Signal.HOLD

    def _parse_confidence(self, text: str) -> float:
        """解析置信度

        Args:
            text: LLM输出文本

        Returns:
            置信度值（0-1）
        """
        patterns = [
            r"置信度[：:]\s*(\d+)\s*%?",
            r"置信度\s*(\d+)\s*%?",
            r"信心[：:]\s*(\d+)\s*%?",
            r"把握[：:]\s*(\d+)\s*%?",
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                confidence = int(match.group(1))
                return min(max(confidence / 100, 0.0), 1.0)

        return 0.6

    def _extract_decision_data(self, text: str) -> Dict[str, Any]:
        """提取决策相关数据

        Args:
            text: LLM输出文本

        Returns:
            包含决策数据的字典
        """
        supporting_data = {
            "target_price": None,
            "stop_loss": None,
            "position_advice": None,
            "holding_period": None,
        }

        # 提取目标价
        target_match = re.search(r"目标价[：:]\s*(\d+\.?\d*)\s*[-~至]\s*(\d+\.?\d*)", text)
        if target_match:
            supporting_data["target_price"] = {
                "low": float(target_match.group(1)),
                "high": float(target_match.group(2))
            }
        else:
            single_target = re.search(r"目标价[：:]\s*(\d+\.?\d*)", text)
            if single_target:
                supporting_data["target_price"] = float(single_target.group(1))

        # 提取止损位
        stop_loss_match = re.search(r"止损位[：:]\s*(\d+\.?\d*)", text)
        if stop_loss_match:
            supporting_data["stop_loss"] = float(stop_loss_match.group(1))

        # 提取仓位建议
        position_match = re.search(r"仓位建议[：:]\s*(\d+%?)", text)
        if position_match:
            supporting_data["position_advice"] = position_match.group(1)

        # 提取持有周期
        if "持有周期" in text:
            period_match = re.search(r"持有周期[：:]\s*(\S+)", text)
            if period_match:
                supporting_data["holding_period"] = period_match.group(1)

        return supporting_data