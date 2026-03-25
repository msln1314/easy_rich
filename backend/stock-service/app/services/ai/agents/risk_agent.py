# -*- coding: utf-8 -*-
"""风控Agent

专注于风险评估和控制，分析价格波动、流动性、市场和个股风险。
"""

import re
import logging
from typing import Optional, List, Dict, Any

from app.services.ai.agents.base_agent import BaseAgent
from app.services.ai.context import AgentContext
from app.models.ai_models import AgentOpinion, Signal

logger = logging.getLogger(__name__)


class RiskAgent(BaseAgent):
    """风控Agent

    专注于风险评估和控制。
    主要分析维度包括：
    - 价格波动风险
    - 流动性风险
    - 市场风险
    - 个股特有风险

    Attributes:
        agent_name: Agent名称标识
        agent_type: Agent类型
        tool_names: 可用工具名称列表
    """

    agent_name: str = "risk"
    agent_type: str = "risk"
    tool_names: Optional[List[str]] = ["get_realtime_quote", "get_daily_kline"]
    max_steps: int = 6

    SYSTEM_PROMPT = """你是一位资深风险控制专家，专注于风险评估和控制。

请基于提供的数据进行风险评估，关注以下维度：

## 1. 价格波动风险
- 历史波动率分析
- 涨跌幅分布
- 极端行情表现
- VaR（风险价值）估算

## 2. 流动性风险
- 日均成交额
- 换手率水平
- 买卖价差
- 大额交易冲击成本

## 3. 市场风险
- 大盘趋势判断
- 行业周期位置
- 系统性风险评估
- 市场情绪指标

## 4. 个股特有风险
- 经营风险
- 财务风险
- 治理风险
- 合规风险

## 风险等级定义
- 高风险：存在重大风险因素，可能导致较大损失
- 中风险：存在一定风险因素，需要密切关注
- 低风险：风险因素较少，整体风险可控

## 输出格式要求
请按照以下格式输出分析结果：

**风险等级**：[高/中/低]

**置信度**：[0-100]%

**风险评分**：[0-100分]

**主要风险点**：
1. [风险类型]：[具体描述] - [风险程度]
2. [风险类型]：[具体描述] - [风险程度]
...

**仓位建议**：
- 建议仓位：[仓位比例]
- 加仓条件：[描述]
- 减仓条件：[描述]

**止损建议**：
- 止损位：[价格/比例]
- 止损逻辑：[描述]

**风控措施**：
[具体的风险控制措施建议]

**详细分析**：
[各风险维度的具体分析]

**风险警示**：
[需要特别关注的风险信号]"""

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

        message_parts.append("请对该股票进行风险评估，给出风险等级和控制建议。")

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

        # 解析风险等级并转换为信号
        opinion.signal = self._parse_signal(raw_text)

        # 解析置信度
        opinion.confidence = self._parse_confidence(raw_text)

        # 提取风险相关数据
        supporting_data = self._extract_risk_data(raw_text)
        opinion.supporting_data = supporting_data

        # 完整分析作为推理过程
        opinion.reasoning = raw_text

        # 添加风险标记到上下文
        self._add_risk_flags(ctx, raw_text, supporting_data)

        return opinion

    def _parse_signal(self, text: str) -> Signal:
        """解析信号

        根据风险等级转换为交易信号。
        高风险 -> 卖出
        中风险 -> 持有
        低风险 -> 买入

        Args:
            text: LLM输出文本

        Returns:
            Signal枚举值
        """
        # 检查风险等级
        if "风险等级" in text:
            if "高" in text.split("风险等级")[1].split("\n")[0][:20]:
                return Signal.SELL
            elif "低" in text.split("风险等级")[1].split("\n")[0][:20]:
                return Signal.BUY
            else:
                return Signal.HOLD

        # 根据关键词判断
        high_risk_keywords = ["高风险", "重大风险", "严重", "警示"]
        low_risk_keywords = ["低风险", "风险可控", "安全"]

        if any(kw in text for kw in high_risk_keywords):
            return Signal.SELL
        elif any(kw in text for kw in low_risk_keywords):
            return Signal.BUY
        else:
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
            r"风险评分[：:]\s*(\d+)\s*分?",
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                confidence = int(match.group(1))
                # 风险评分是风险程度，需要反转
                if "风险评分" in pattern:
                    return min(max((100 - confidence) / 100, 0.0), 1.0)
                return min(max(confidence / 100, 0.0), 1.0)

        return 0.6

    def _extract_risk_data(self, text: str) -> Dict[str, Any]:
        """提取风险相关数据

        Args:
            text: LLM输出文本

        Returns:
            包含风险数据的字典
        """
        supporting_data = {
            "risk_level": "中",
            "risk_score": 50,
            "position_advice": "30%",
            "stop_loss": None
        }

        # 提取风险等级
        level_match = re.search(r"风险等级[：:]\s*[高 中 低]+", text)
        if level_match:
            level_text = level_match.group()
            if "高" in level_text:
                supporting_data["risk_level"] = "高"
            elif "低" in level_text:
                supporting_data["risk_level"] = "低"

        # 提取风险评分
        score_match = re.search(r"风险评分[：:]\s*(\d+)", text)
        if score_match:
            supporting_data["risk_score"] = int(score_match.group(1))

        # 提取仓位建议
        position_match = re.search(r"建议仓位[：:]\s*(\d+%?)", text)
        if position_match:
            supporting_data["position_advice"] = position_match.group(1)

        # 提取止损位
        stop_loss_match = re.search(r"止损位[：:]\s*(\d+\.?\d*)", text)
        if stop_loss_match:
            supporting_data["stop_loss"] = float(stop_loss_match.group(1))

        return supporting_data

    def _add_risk_flags(
        self, ctx: AgentContext, text: str, risk_data: Dict[str, Any]
    ) -> None:
        """添加风险标记到上下文

        Args:
            ctx: Agent上下文
            text: LLM输出文本
            risk_data: 提取的风险数据
        """
        risk_level = risk_data.get("risk_level", "中")

        # 根据风险等级添加风险标记
        if risk_level == "高":
            ctx.add_risk_flag(
                category="风险评估",
                description=f"高风险股票，风险评分：{risk_data.get('risk_score', 'N/A')}",
                severity="high"
            )
        elif risk_level == "中":
            ctx.add_risk_flag(
                category="风险评估",
                description=f"中等风险股票，风险评分：{risk_data.get('risk_score', 'N/A')}",
                severity="medium"
            )

        # 检查特定风险关键词
        specific_risks = {
            "流动性风险": ["成交额低", "流动性差", "交易清淡"],
            "波动风险": ["波动大", "振幅高", "剧烈波动"],
            "财务风险": ["财务风险", "负债率高", "现金流问题"]
        }

        for risk_type, keywords in specific_risks.items():
            if any(kw in text for kw in keywords):
                ctx.add_risk_flag(
                    category=risk_type,
                    description=f"检测到{risk_type}因素",
                    severity="medium"
                )