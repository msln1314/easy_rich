# -*- coding: utf-8 -*-
"""多Agent协调器

提供多Agent协作的编排和执行能力，支持不同分析模式。
"""

import logging
from typing import List, Dict, Any, Optional, Callable
from datetime import datetime

from app.services.ai.context import AgentContext
from app.services.ai.tool_registry import ToolRegistry
from app.services.ai.llm_adapter import LLMToolAdapter, get_llm_adapter
from app.services.ai.agents.base_agent import BaseAgent
from app.models.ai_models import (
    AgentOpinion,
    StageResult,
    StageStatus,
    SynthesisResult,
    AgentAnalyzeResponse,
    Signal,
)

logger = logging.getLogger(__name__)

VALID_MODES = ("quick", "standard", "full", "specialist")


class AgentOrchestrator:
    """多Agent协调器

    负责编排和执行多个Agent的分析流程，支持不同的分析模式。

    分析模式:
        - quick: 快速分析，TechnicalAgent + DecisionAgent
        - standard: 标准分析，TechnicalAgent + NewsAgent + DecisionAgent
        - full: 深度分析，TechnicalAgent + FundamentalAgent + NewsAgent + RiskAgent + DecisionAgent
        - specialist: 专家模式，可自定义Agent组合

    Attributes:
        mode: 分析模式
        model: 使用的LLM模型
        config: 配置字典
        tool_registry: 工具注册中心
        llm_adapter: LLM适配器
    """

    def __init__(
        self,
        mode: str = "standard",
        model: str = "gpt-4",
        config: Dict = None,
    ):
        """初始化协调器

        Args:
            mode: 分析模式，可选 quick/standard/full/specialist
            model: LLM模型名称
            config: 配置字典
        """
        self.mode = mode if mode in VALID_MODES else "standard"
        self.model = model
        self.config = config or {}

        self.tool_registry = ToolRegistry()
        self.llm_adapter = get_llm_adapter(model)

        # 注册默认工具（占位，实际工具在tools模块中注册）
        self._register_default_tools()

    def _register_default_tools(self) -> None:
        """注册默认工具

        子类或外部模块可以通过tool_registry.register()添加更多工具。
        """
        # 默认工具将在tools模块中注册
        # 这里只是占位，实际实现需要导入tools模块
        pass

    def _build_agent_chain(self) -> List[BaseAgent]:
        """构建Agent链

        根据分析模式构建对应的Agent执行链。

        Returns:
            Agent列表
        """
        # 具体的Agent实现将在各自的模块中完成
        # 这里返回空列表作为占位
        agents: List[BaseAgent] = []

        # 注意：实际的Agent导入将在子类或具体实现中完成
        # 避免循环导入问题
        #
        # 示例实现（仅供参考）:
        # if self.mode == "quick":
        #     from app.services.ai.agents.technical_agent import TechnicalAgent
        #     from app.services.ai.agents.decision_agent import DecisionAgent
        #     agents = [
        #         TechnicalAgent(self.tool_registry, self.llm_adapter),
        #         DecisionAgent(self.tool_registry, self.llm_adapter),
        #     ]
        # elif self.mode == "standard":
        #     from app.services.ai.agents.technical_agent import TechnicalAgent
        #     from app.services.ai.agents.news_agent import NewsAgent
        #     from app.services.ai.agents.decision_agent import DecisionAgent
        #     agents = [
        #         TechnicalAgent(self.tool_registry, self.llm_adapter),
        #         NewsAgent(self.tool_registry, self.llm_adapter),
        #         DecisionAgent(self.tool_registry, self.llm_adapter),
        #     ]
        # elif self.mode == "full":
        #     from app.services.ai.agents.technical_agent import TechnicalAgent
        #     from app.services.ai.agents.fundamental_agent import FundamentalAgent
        #     from app.services.ai.agents.news_agent import NewsAgent
        #     from app.services.ai.agents.risk_agent import RiskAgent
        #     from app.services.ai.agents.decision_agent import DecisionAgent
        #     agents = [
        #         TechnicalAgent(self.tool_registry, self.llm_adapter),
        #         FundamentalAgent(self.tool_registry, self.llm_adapter),
        #         NewsAgent(self.tool_registry, self.llm_adapter),
        #         RiskAgent(self.tool_registry, self.llm_adapter),
        #         DecisionAgent(self.tool_registry, self.llm_adapter),
        #     ]

        return agents

    async def run(
        self,
        stock_code: str,
        query: str = "",
        progress_callback: Callable[[str], None] = None,
    ) -> AgentAnalyzeResponse:
        """执行分析

        执行完整的多Agent分析流程:
        1. 创建上下文
        2. 预取数据
        3. 执行Agent链
        4. 生成综合研判
        5. 返回结果

        Args:
            stock_code: 股票代码
            query: 用户查询问题
            progress_callback: 进度回调函数

        Returns:
            AgentAnalyzeResponse: 分析响应结果
        """
        # 1. 创建上下文
        ctx = AgentContext.create(stock_code=stock_code, query=query)
        ctx.meta["mode"] = self.mode
        ctx.meta["model"] = self.model

        if progress_callback:
            progress_callback(f"开始分析股票 {stock_code}，模式: {self.mode}")

        # 2. 预取数据
        await self._prefetch_data(ctx, progress_callback)

        # 3. 执行Agent链
        agents = self._build_agent_chain()
        stage_results: List[StageResult] = []

        for agent in agents:
            if progress_callback:
                progress_callback(f"执行 {agent.agent_name} 分析...")

            result = await agent.run(ctx, progress_callback)
            stage_results.append(result)

            if result.status == StageStatus.FAILED:
                logger.error(f"Agent {agent.agent_name} 执行失败: {result.error}")
                # 继续执行其他Agent，不中断流程

        # 4. 生成综合研判
        synthesis = self._synthesize(ctx)

        if progress_callback:
            progress_callback("分析完成")

        # 5. 返回结果
        return AgentAnalyzeResponse(
            stock_code=stock_code,
            stock_name=ctx.stock_name,
            analysis_time=datetime.now(),
            signal=synthesis.signal,
            confidence=synthesis.confidence,
            summary=synthesis.summary,
            agent_opinions=[
                {
                    "agent_name": op.agent_name if hasattr(op, "agent_name") else "unknown",
                    "signal": op.signal.value if hasattr(op.signal, "value") else str(op.signal),
                    "confidence": op.confidence if hasattr(op, "confidence") else 0.0,
                    "reasoning": op.reasoning if hasattr(op, "reasoning") else "",
                }
                for op in ctx.opinions
            ],
            risks=synthesis.risks if synthesis.risks else None,
        )

    async def _prefetch_data(
        self, ctx: AgentContext, progress_callback=None
    ) -> None:
        """预取数据

        预先获取股票基本信息、实时行情、K线数据等。

        Args:
            ctx: Agent上下文
            progress_callback: 进度回调函数
        """
        if progress_callback:
            progress_callback("正在预取数据...")

        # TODO: 实际的数据预取实现
        # 这里是占位实现，实际需要调用股票服务获取数据
        #
        # 示例实现:
        # try:
        #     # 获取股票基本信息
        #     stock_info = await self._get_stock_info(ctx.stock_code)
        #     ctx.stock_name = stock_info.get("name", "")
        #     ctx.set_data("stock_info", stock_info)
        #
        #     # 获取实时行情
        #     quote = await self._get_realtime_quote(ctx.stock_code)
        #     ctx.set_data("realtime_quote", quote)
        #
        #     # 获取K线数据
        #     klines = await self._get_klines(ctx.stock_code, period="daily", count=60)
        #     ctx.set_data("klines", klines)
        #
        #     if progress_callback:
        #         progress_callback("数据预取完成")
        # except Exception as e:
        #     logger.error(f"预取数据失败: {e}")
        #     if progress_callback:
        #         progress_callback(f"预取数据失败: {e}")

        # 占位实现：设置模拟数据
        ctx.stock_name = ctx.stock_code
        ctx.set_data("prefetch_status", "completed")

        if progress_callback:
            progress_callback("数据预取完成（占位实现）")

    def _generate_debate(self, ctx: AgentContext) -> List[Dict[str, Any]]:
        """生成辩论记录

        当多个Agent有不同观点时，生成辩论风格的对话记录。

        Args:
            ctx: Agent上下文

        Returns:
            辩论记录列表
        """
        debates = []

        if len(ctx.opinions) < 2:
            return debates

        # 收集不同信号的观点
        signals = {}
        for opinion in ctx.opinions:
            signal_value = (
                opinion.signal.value if hasattr(opinion.signal, "value") else str(opinion.signal)
            )
            if signal_value not in signals:
                signals[signal_value] = []
            signals[signal_value].append(opinion)

        # 如果只有一种信号，没有辩论
        if len(signals) <= 1:
            return debates

        # 生成辩论记录
        for signal, opinions in signals.items():
            for opinion in opinions:
                agent_name = (
                    opinion.agent_name if hasattr(opinion, "agent_name") else "unknown"
                )
                reasoning = (
                    opinion.reasoning if hasattr(opinion, "reasoning") else ""
                )
                debates.append(
                    {
                        "agent": agent_name,
                        "stance": signal,
                        "argument": reasoning,
                    }
                )

        return debates

    def _synthesize(self, ctx: AgentContext) -> SynthesisResult:
        """综合研判

        综合所有Agent的观点，生成最终研判结果。

        Args:
            ctx: Agent上下文

        Returns:
            SynthesisResult: 综合研判结果
        """
        if not ctx.opinions:
            return SynthesisResult(
                stock_code=ctx.stock_code,
                signal=Signal.HOLD,
                confidence=0.0,
                summary="无有效分析观点",
                key_factors=[],
                risks=["未能获取任何分析观点"],
                agent_opinions=[],
            )

        # 统计信号投票
        signal_votes: Dict[Signal, float] = {}
        total_confidence = 0.0

        for opinion in ctx.opinions:
            signal = opinion.signal if hasattr(opinion, "signal") else Signal.HOLD
            confidence = (
                opinion.confidence if hasattr(opinion, "confidence") else 0.5
            )

            if signal not in signal_votes:
                signal_votes[signal] = 0.0
            signal_votes[signal] += confidence
            total_confidence += confidence

        # 选择得票最高的信号
        if signal_votes:
            final_signal = max(signal_votes, key=signal_votes.get)
            final_confidence = (
                signal_votes[final_signal] / total_confidence
                if total_confidence > 0
                else 0.5
            )
        else:
            final_signal = Signal.HOLD
            final_confidence = 0.0

        # 生成摘要
        summaries = []
        for opinion in ctx.opinions:
            agent_name = (
                opinion.agent_name if hasattr(opinion, "agent_name") else "unknown"
            )
            reasoning = (
                opinion.reasoning if hasattr(opinion, "reasoning") else ""
            )
            summaries.append(f"【{agent_name}】{reasoning}")

        summary = "\n".join(summaries) if summaries else "无分析结果"

        # 收集关键因素
        key_factors = []
        for opinion in ctx.opinions:
            supporting_data = (
                opinion.supporting_data
                if hasattr(opinion, "supporting_data")
                else {}
            )
            if isinstance(supporting_data, dict):
                for key in ["trend", "momentum", "volume", "pattern"]:
                    if key in supporting_data:
                        key_factors.append(f"{key}: {supporting_data[key]}")

        # 收集风险
        risks = [flag["description"] for flag in ctx.risk_flags]

        # 生成操作建议
        operation_advice = self._generate_operation_advice(
            final_signal.value, ctx
        )

        return SynthesisResult(
            stock_code=ctx.stock_code,
            signal=final_signal,
            confidence=final_confidence,
            summary=summary,
            key_factors=key_factors[:5],  # 最多5个关键因素
            risks=risks,
            agent_opinions=ctx.opinions,
            supporting_data={"operation_advice": operation_advice},
        )

    def _generate_operation_advice(self, conclusion: str, ctx: AgentContext) -> str:
        """生成操作建议

        根据分析结论生成具体的操作建议。

        Args:
            conclusion: 分析结论信号
            ctx: Agent上下文

        Returns:
            操作建议字符串
        """
        advice_templates = {
            "strong_buy": "强烈建议买入。多维度分析显示该股票具有显著的上涨潜力，可考虑逐步建仓。",
            "buy": "建议买入。分析显示该股票具有一定上涨空间，可适度参与。",
            "hold": "建议持有观望。当前信号不明确，建议等待更好的交易机会。",
            "sell": "建议减仓或卖出。分析显示存在一定风险，可考虑止盈或止损。",
            "strong_sell": "强烈建议卖出。多维度分析显示该股票风险较高，建议及时离场。",
        }

        advice = advice_templates.get(conclusion, "建议谨慎决策。")

        # 添加风险提示
        if ctx.has_high_risk:
            advice += "\n\n警告：检测到高风险信号，请特别注意风险控制。"

        if ctx.has_risk_flags:
            risk_count = len(ctx.risk_flags)
            advice += f"\n\n风险提示：共检测到 {risk_count} 个风险点，请仔细评估。"

        return advice

    def set_agents(self, agents: List[BaseAgent]) -> None:
        """设置自定义Agent列表

        用于specialist模式，允许自定义Agent组合。

        Args:
            agents: Agent列表
        """
        self._custom_agents = agents