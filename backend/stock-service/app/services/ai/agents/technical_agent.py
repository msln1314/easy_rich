# -*- coding: utf-8 -*-
"""技术分析Agent

专注于股票技术面分析，包括K线形态、均线系统、技术指标、成交量和支撑压力位分析。
"""

import re
import logging
from typing import Optional, List, Dict, Any

from app.services.ai.agents.base_agent import BaseAgent
from app.services.ai.context import AgentContext
from app.models.ai_models import AgentOpinion, Signal

logger = logging.getLogger(__name__)


class TechnicalAgent(BaseAgent):
    """技术分析Agent

    专注于A股技术面分析，拥有20年技术分析经验。
    主要分析维度包括：
    - K线形态分析
    - 均线系统（MA5, MA10, MA20, MA60）
    - 技术指标（MACD, KDJ, RSI）
    - 成交量分析
    - 支撑位和压力位

    Attributes:
        agent_name: Agent名称标识
        agent_type: Agent类型
        tool_names: 可用工具名称列表
    """

    agent_name: str = "technical"
    agent_type: str = "technical"
    tool_names: Optional[List[str]] = ["get_realtime_quote", "get_daily_kline", "analyze_trend"]
    max_steps: int = 8

    SYSTEM_PROMPT = """你是一位资深技术分析师，拥有20年A股技术分析经验。

请基于提供的数据进行技术面分析，关注以下维度：

## 1. K线形态分析
- 识别常见的K线形态：锤子线、流星线、十字星、吞没形态等
- 分析K线实体和影线的比例关系
- 判断多空力量对比

## 2. 均线系统分析
- 分析MA5、MA10、MA20、MA60的排列状态
- 判断均线多头/空头排列
- 关注均线金叉、死叉信号
- 分析均线支撑和压力作用

## 3. 技术指标分析
- MACD：分析DIF和DEA的关系、柱状图变化、金叉死叉
- KDJ：分析K、D、J线的位置和交叉、超买超卖区域
- RSI：分析相对强弱、超买超卖状态

## 4. 成交量分析
- 量价配合关系
- 放量、缩量的意义判断
- 量能趋势分析

## 5. 支撑位和压力位
- 识别关键支撑位和压力位
- 分析突破和回踩的有效性

## 输出格式要求
请按照以下格式输出分析结果：

**判断**：[看多/看空/中性]

**置信度**：[0-100]%

**关键点位**：
- 支撑位：[价格]
- 压力位：[价格]

**技术信号**：
- 均线信号：[描述]
- MACD信号：[描述]
- KDJ信号：[描述]
- 成交量信号：[描述]

**详细分析**：
[各维度的具体分析内容，包含数据支撑和逻辑推理]"""

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

        message_parts.append("请对该股票进行技术面分析，给出你的判断和理由。")

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

        # 解析信号/判断
        opinion.signal = self._parse_signal(raw_text)

        # 解析置信度
        opinion.confidence = self._parse_confidence(raw_text)

        # 提取关键点位
        supporting_data = self._extract_key_levels(raw_text)
        opinion.supporting_data = supporting_data

        # 完整分析作为推理过程
        opinion.reasoning = raw_text

        return opinion

    def _parse_signal(self, text: str) -> Signal:
        """解析信号

        Args:
            text: LLM输出文本

        Returns:
            Signal枚举值
        """
        text_lower = text.lower()

        # 看多信号关键词
        bullish_keywords = ["看多", "买入", "上涨", "多头", "突破", "金叉", "超卖反弹"]
        # 看空信号关键词
        bearish_keywords = ["看空", "卖出", "下跌", "空头", "跌破", "死叉", "超买回落"]

        bullish_count = sum(1 for kw in bullish_keywords if kw in text)
        bearish_count = sum(1 for kw in bearish_keywords if kw in text)

        # 检查明确判断
        if "判断" in text:
            if "看多" in text:
                return Signal.BUY
            elif "看空" in text:
                return Signal.SELL
            elif "中性" in text:
                return Signal.HOLD

        # 根据关键词计数判断
        if bullish_count > bearish_count + 1:
            return Signal.BUY
        elif bearish_count > bullish_count + 1:
            return Signal.SELL
        else:
            return Signal.HOLD

    def _parse_confidence(self, text: str) -> float:
        """解析置信度

        Args:
            text: LLM输出文本

        Returns:
            置信度值（0-1）
        """
        # 尝试匹配置信度格式
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

        # 默认置信度
        return 0.6

    def _extract_key_levels(self, text: str) -> Dict[str, Any]:
        """提取关键点位

        Args:
            text: LLM输出文本

        Returns:
            包含支撑位和压力位的字典
        """
        supporting_data = {}

        # 提取支撑位
        support_patterns = [
            r"支撑位[：:]\s*(\d+\.?\d*)",
            r"支撑[：:]\s*(\d+\.?\d*)",
        ]
        for pattern in support_patterns:
            match = re.search(pattern, text)
            if match:
                supporting_data["support_level"] = float(match.group(1))
                break

        # 提取压力位
        resistance_patterns = [
            r"压力位[：:]\s*(\d+\.?\d*)",
            r"阻力位[：:]\s*(\d+\.?\d*)",
            r"压力[：:]\s*(\d+\.?\d*)",
        ]
        for pattern in resistance_patterns:
            match = re.search(pattern, text)
            if match:
                supporting_data["resistance_level"] = float(match.group(1))
                break

        return supporting_data