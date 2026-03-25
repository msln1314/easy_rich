# -*- coding: utf-8 -*-
"""基本面分析Agent

专注于公司财务和估值分析，包括财务指标、成长性、行业地位和估值水平分析。
"""

import re
import logging
from typing import Optional, List, Dict, Any

from app.services.ai.agents.base_agent import BaseAgent
from app.services.ai.context import AgentContext
from app.models.ai_models import AgentOpinion, Signal

logger = logging.getLogger(__name__)


class FundamentalAgent(BaseAgent):
    """基本面分析Agent

    专注于公司财务和估值分析。
    主要分析维度包括：
    - 财务指标（PE、PB、ROE、毛利率等）
    - 成长性分析（营收增长、利润增长）
    - 行业地位和竞争优势
    - 估值水平判断

    Attributes:
        agent_name: Agent名称标识
        agent_type: Agent类型
        tool_names: 可用工具名称列表
    """

    agent_name: str = "fundamental"
    agent_type: str = "fundamental"
    tool_names: Optional[List[str]] = ["get_stock_info", "get_financial_data"]
    max_steps: int = 6

    SYSTEM_PROMPT = """你是一位资深基本面分析师，专注于公司财务和估值分析。

请基于提供的数据进行基本面分析，关注以下维度：

## 1. 财务指标分析
- 估值指标：PE（市盈率）、PB（市净率）、PS（市销率）
- 盈利能力：ROE（净资产收益率）、ROA（总资产收益率）、毛利率、净利率
- 偿债能力：资产负债率、流动比率、速动比率
- 运营效率：存货周转率、应收账款周转率

## 2. 成长性分析
- 营收增长率：分析营收的同比和环比增长
- 利润增长率：分析净利润的同比和环比增长
- 行业成长性对比
- 未来增长预期

## 3. 行业地位分析
- 市场份额
- 行业竞争格局
- 公司竞争优势
- 护城河分析

## 4. 估值水平判断
- 绝对估值：DCF模型参考
- 相对估值：同行业对比
- 历史估值分位
- 安全边际评估

## 输出格式要求
请按照以下格式输出分析结果：

**判断**：[低估/合理/高估]

**置信度**：[0-100]%

**关键指标**：
- PE：[数值]（行业平均：[数值]）
- PB：[数值]（行业平均：[数值]）
- ROE：[数值]%
- 营收增长：[数值]%
- 净利增长：[数值]%

**估值分析**：
- 绝对估值评估：[描述]
- 相对估值评估：[描述]
- 历史分位：[描述]

**投资建议**：
[基于基本面的投资建议，包含持有周期建议]

**详细分析**：
[各维度的具体分析内容，包含数据支撑和逻辑推理]

**风险提示**：
[基本面方面的主要风险点]"""

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

        message_parts.append("请对该股票进行基本面分析，给出你的判断和理由。")

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

        # 提取关键财务指标
        supporting_data = self._extract_financial_metrics(raw_text)
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
        # 检查明确判断
        if "判断" in text:
            if "低估" in text:
                return Signal.BUY
            elif "高估" in text:
                return Signal.SELL
            elif "合理" in text:
                return Signal.HOLD

        # 根据关键词判断
        bullish_keywords = ["低估", "买入", "价值投资", "安全边际高", "成长性好"]
        bearish_keywords = ["高估", "卖出", "泡沫", "估值过高", "成长性差"]

        bullish_count = sum(1 for kw in bullish_keywords if kw in text)
        bearish_count = sum(1 for kw in bearish_keywords if kw in text)

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

    def _extract_financial_metrics(self, text: str) -> Dict[str, Any]:
        """提取关键财务指标

        Args:
            text: LLM输出文本

        Returns:
            包含财务指标的字典
        """
        supporting_data = {}

        # 提取PE
        pe_match = re.search(r"PE[：:]\s*(\d+\.?\d*)", text)
        if pe_match:
            supporting_data["pe"] = float(pe_match.group(1))

        # 提取PB
        pb_match = re.search(r"PB[：:]\s*(\d+\.?\d*)", text)
        if pb_match:
            supporting_data["pb"] = float(pb_match.group(1))

        # 提取ROE
        roe_match = re.search(r"ROE[：:]\s*(\d+\.?\d*)\s*%?", text)
        if roe_match:
            supporting_data["roe"] = float(roe_match.group(1))

        # 提取营收增长
        revenue_match = re.search(r"营收增长[率]?[：:]\s*(\d+\.?\d*)\s*%?", text)
        if revenue_match:
            supporting_data["revenue_growth"] = float(revenue_match.group(1))

        # 提取净利增长
        profit_match = re.search(r"净利增长[率]?[：:]\s*(\d+\.?\d*)\s*%?", text)
        if profit_match:
            supporting_data["profit_growth"] = float(profit_match.group(1))

        return supporting_data