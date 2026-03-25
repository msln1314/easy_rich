# -*- coding: utf-8 -*-
"""消息面分析Agent

专注于新闻和公告解读，分析市场情绪和事件影响。
"""

import re
import logging
from typing import Optional, List, Dict, Any

from app.services.ai.agents.base_agent import BaseAgent
from app.services.ai.context import AgentContext
from app.models.ai_models import AgentOpinion, Signal

logger = logging.getLogger(__name__)


class NewsAgent(BaseAgent):
    """消息面分析Agent

    专注于新闻和公告解读。
    主要分析维度包括：
    - 近期重要新闻和事件
    - 公司公告解读
    - 行业政策影响
    - 市场情绪判断

    Attributes:
        agent_name: Agent名称标识
        agent_type: Agent类型
        tool_names: 可用工具名称列表
    """

    agent_name: str = "news"
    agent_type: str = "news"
    tool_names: Optional[List[str]] = ["get_stock_news", "get_announcements"]
    max_steps: int = 6

    SYSTEM_PROMPT = """你是一位资深消息面分析师，专注于新闻和公告解读。

请基于提供的新闻和公告进行分析，关注以下维度：

## 1. 近期重要新闻
- 公司重大事件
- 业绩预告/快报
- 资产重组/并购
- 重大合同/订单
- 高管变动

## 2. 公司公告解读
- 定期报告解读（年报、季报）
- 临时公告分析
- 股东大会决议
- 股权变动公告

## 3. 行业政策影响
- 国家政策导向
- 行业监管变化
- 税收政策调整
- 补贴政策影响

## 4. 市场情绪判断
- 舆论热度分析
- 机构观点汇总
- 市场预期判断
- 风险偏好评估

## 消息影响程度评估标准
- 重大利好：影响公司基本面，预期带来显著业绩增长
- 一般利好：短期提振市场情绪，对业绩有一定帮助
- 中性：影响有限或已充分预期
- 一般利空：短期对股价有压力，但影响可控
- 重大利空：严重影响公司基本面或经营状况

## 输出格式要求
请按照以下格式输出分析结果：

**判断**：[利好/利空/中性]

**置信度**：[0-100]%

**影响程度**：[重大/一般/轻微]

**关键事件**：
1. [事件标题] - [影响分析]
2. [事件标题] - [影响分析]
...

**情绪分析**：
- 舆论热度：[高/中/低]
- 市场预期：[乐观/中性/悲观]
- 机构观点：[看多/中性/看空]

**详细分析**：
[各消息面的具体分析，包含事件背景、影响逻辑、持续性判断]

**风险提示**：
[消息面方面的主要风险点]"""

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

        message_parts.append("请对该股票进行消息面分析，分析近期新闻和公告的影响。")

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

        # 提取关键事件
        supporting_data = self._extract_key_events(raw_text)
        opinion.supporting_data = supporting_data

        # 完整分析作为推理过程
        opinion.reasoning = raw_text

        # 如果发现重大利空，添加风险标记
        if self._has_major_risk(raw_text):
            ctx.add_risk_flag(
                category="消息面风险",
                description="发现重大利空消息",
                severity="high" if "重大利空" in raw_text else "medium"
            )

        return opinion

    def _parse_signal(self, text: str) -> Signal:
        """解析信号

        Args:
            text: LLM输出文本

        Returns:
            Signal枚举值
        """
        # 检查明确判断
        if "判断" in text:
            if "利好" in text:
                if "重大利好" in text:
                    return Signal.STRONG_BUY
                return Signal.BUY
            elif "利空" in text:
                if "重大利空" in text:
                    return Signal.STRONG_SELL
                return Signal.SELL
            elif "中性" in text:
                return Signal.HOLD

        # 根据关键词判断
        bullish_keywords = ["利好", "正面", "积极", "乐观", "增长", "突破"]
        bearish_keywords = ["利空", "负面", "消极", "悲观", "下滑", "风险"]

        bullish_count = sum(1 for kw in bullish_keywords if kw in text)
        bearish_count = sum(1 for kw in bearish_keywords if kw in text)

        if bullish_count > bearish_count + 2:
            return Signal.BUY
        elif bearish_count > bullish_count + 2:
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

    def _extract_key_events(self, text: str) -> Dict[str, Any]:
        """提取关键事件

        Args:
            text: LLM输出文本

        Returns:
            包含关键事件的字典
        """
        supporting_data = {
            "events": [],
            "sentiment": "中性",
            "impact_level": "一般"
        }

        # 提取情绪判断
        if "乐观" in text:
            supporting_data["sentiment"] = "乐观"
        elif "悲观" in text:
            supporting_data["sentiment"] = "悲观"

        # 提取影响程度
        if "重大" in text:
            supporting_data["impact_level"] = "重大"
        elif "轻微" in text:
            supporting_data["impact_level"] = "轻微"

        # 尝试提取关键事件（简单匹配编号列表）
        event_pattern = r"\d+\.\s*([^-]+)\s*-\s*([^\n]+)"
        events = re.findall(event_pattern, text)
        if events:
            supporting_data["events"] = [
                {"title": e[0].strip(), "impact": e[1].strip()}
                for e in events[:5]  # 最多5个事件
            ]

        return supporting_data

    def _has_major_risk(self, text: str) -> bool:
        """判断是否存在重大风险

        Args:
            text: LLM输出文本

        Returns:
            是否存在重大风险
        """
        risk_keywords = ["重大利空", "严重", "违规", "被调查", "退市风险"]
        return any(kw in text for kw in risk_keywords)