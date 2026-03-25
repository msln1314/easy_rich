# -*- coding: utf-8 -*-
"""
Agent状态管理
参考 TradingAgents-CN TypedDict 状态设计
"""
from typing import TypedDict, Annotated, List, Dict, Any, Optional
from dataclasses import dataclass, field
import time


class AgentDebateState(TypedDict):
    """
    Agent辩论状态

    用于多空辩论场景，跟踪辩论历史和最终判断。

    Attributes:
        bull_history: 多头观点历史
        bear_history: 空头观点历史
        judge_decision: 最终判断
        debate_round: 当前辩论轮次
        max_rounds: 最大轮次
    """
    bull_history: Annotated[str, "多头对话历史"]
    bear_history: Annotated[str, "空头对话历史"]
    judge_decision: Annotated[str, "最终法官判断"]
    debate_round: Annotated[int, "当前辩论轮次"]
    max_rounds: Annotated[int, "最大辩论轮次"]


class AgentReportState(TypedDict):
    """
    Agent分析报告状态

    存储各Agent产生的报告数据。
    """
    technical_report: Annotated[str, "技术分析报告"]
    fundamental_report: Annotated[str, "基本面分析报告"]
    news_report: Annotated[str, "新闻分析报告"]
    risk_report: Annotated[str, "风险评估报告"]
    final_decision: Annotated[str, "最终决策"]


class MultiAgentState(TypedDict):
    """
    多Agent工作流状态

    集成所有Agent的状态，用于LangGraph等框架的状态管理。

    Attributes:
        stock_code: 股票代码
        stock_name: 股票名称
        query: 用户查询
        reports: 各Agent报告
        debate_state: 辩论状态
        opinions: Agent观点列表
        synthesis: 综合研判结果
    """
    stock_code: Annotated[str, "股票代码"]
    stock_name: Annotated[str, "股票名称"]
    query: Annotated[str, "用户查询"]
    reports: Annotated[AgentReportState, "Agent报告"]
    debate_state: Annotated[AgentDebateState, "辩论状态"]
    opinions: Annotated[List[Dict[str, Any]], "Agent观点列表"]
    synthesis: Annotated[Dict[str, Any], "综合研判结果"]


@dataclass
class DebateRecord:
    """辩论记录"""
    round_num: int = 0
    bull_view: str = ""
    bear_view: str = ""
    bull_confidence: float = 0.0
    bear_confidence: float = 0.0
    timestamp: float = field(default_factory=time.time)


@dataclass
class DebateResult:
    """辩论结果"""
    topic: str = ""
    rounds: List[DebateRecord] = field(default_factory=list)
    final_decision: str = ""
    decision_reasoning: str = ""
    winner: str = ""  # "bull", "bear", "neutral"
    confidence: float = 0.0
    duration_s: float = 0.0


class DebateManager:
    """
    辩论管理器

    管理多空辩论流程，支持多轮辩论和最终判断。
    """

    def __init__(self, max_rounds: int = 3):
        self.max_rounds = max_rounds
        self.state: AgentDebateState = {
            "bull_history": "",
            "bear_history": "",
            "judge_decision": "",
            "debate_round": 0,
            "max_rounds": max_rounds,
        }
        self.records: List[DebateRecord] = []

    def start_debate(self, topic: str = "") -> None:
        """开始辩论"""
        self.state["debate_round"] = 0
        self.state["bull_history"] = ""
        self.state["bear_history"] = ""
        self.state["judge_decision"] = ""
        self.records = []

    def add_bull_view(self, view: str, confidence: float = 0.0) -> None:
        """添加多头观点"""
        self.state["bull_history"] += f"\n[Round {self.state['debate_round'] + 1}] {view}"
        if self.records and self.records[-1].round_num == self.state["debate_round"] + 1:
            self.records[-1].bull_view = view
            self.records[-1].bull_confidence = confidence
        else:
            record = DebateRecord(
                round_num=self.state["debate_round"] + 1,
                bull_view=view,
                bull_confidence=confidence,
            )
            self.records.append(record)

    def add_bear_view(self, view: str, confidence: float = 0.0) -> None:
        """添加空头观点"""
        self.state["bear_history"] += f"\n[Round {self.state['debate_round'] + 1}] {view}"
        if self.records and self.records[-1].round_num == self.state["debate_round"] + 1:
            self.records[-1].bear_view = view
            self.records[-1].bear_confidence = confidence
        else:
            record = DebateRecord(
                round_num=self.state["debate_round"] + 1,
                bear_view=view,
                bear_confidence=confidence,
            )
            self.records.append(record)

    def advance_round(self) -> bool:
        """
        推进辩论轮次

        Returns:
            bool: 是否还有剩余轮次
        """
        self.state["debate_round"] += 1
        return self.state["debate_round"] < self.max_rounds

    def should_continue(self) -> bool:
        """判断是否应该继续辩论"""
        return self.state["debate_round"] < self.max_rounds

    def set_judge_decision(self, decision: str) -> None:
        """设置法官判断"""
        self.state["judge_decision"] = decision

    def get_debate_context_for_bull(self) -> str:
        """获取多头的辩论上下文"""
        return f"""
你是一位多头研究员，负责从看多角度分析股票。

之前的辩论历史：
多头观点历史：
{self.state['bull_history']}

空头观点历史：
{self.state['bear_history']}

请基于以上信息，给出你的多头观点，反驳空头的论据。
"""

    def get_debate_context_for_bear(self) -> str:
        """获取空头的辩论上下文"""
        return f"""
你是一位空头研究员，负责从看空角度分析股票。

之前的辩论历史：
多头观点历史：
{self.state['bull_history']}

空头观点历史：
{self.state['bear_history']}

请基于以上信息，给出你的空头观点，反驳多头的论据。
"""

    def get_judge_context(self) -> str:
        """获取法官的辩论上下文"""
        return f"""
你是一位公正的法官，负责根据多空辩论做出最终判断。

多头观点历史：
{self.state['bull_history']}

空头观点历史：
{self.state['bear_history']}

辩论轮次：{self.state['debate_round']}/{self.state['max_rounds']}

请综合多空双方观点，给出你的最终判断和理由。
"""

    def get_result(self, decision: str = "", reasoning: str = "") -> DebateResult:
        """获取辩论结果"""
        # 简单判断胜者
        decision_lower = decision.lower()
        if "多" in decision_lower or "buy" in decision_lower or "看涨" in decision_lower:
            winner = "bull"
        elif "空" in decision_lower or "sell" in decision_lower or "看跌" in decision_lower:
            winner = "bear"
        else:
            winner = "neutral"

        return DebateResult(
            topic="股票分析辩论",
            rounds=self.records,
            final_decision=decision,
            decision_reasoning=reasoning,
            winner=winner,
            confidence=self._calculate_confidence(),
        )

    def _calculate_confidence(self) -> float:
        """计算综合置信度"""
        if not self.records:
            return 0.5

        total_bull = sum(r.bull_confidence for r in self.records)
        total_bear = sum(r.bear_confidence for r in self.records)

        if total_bull == 0 and total_bear == 0:
            return 0.5

        # 归一化
        total = total_bull + total_bear
        return max(total_bull, total_bear) / total if total > 0 else 0.5


def create_debate_state(max_rounds: int = 3) -> AgentDebateState:
    """创建辩论状态"""
    return {
        "bull_history": "",
        "bear_history": "",
        "judge_decision": "",
        "debate_round": 0,
        "max_rounds": max_rounds,
    }


def create_multi_agent_state(
    stock_code: str,
    stock_name: str = "",
    query: str = "",
) -> MultiAgentState:
    """创建多Agent状态"""
    return {
        "stock_code": stock_code,
        "stock_name": stock_name,
        "query": query,
        "reports": {
            "technical_report": "",
            "fundamental_report": "",
            "news_report": "",
            "risk_report": "",
            "final_decision": "",
        },
        "debate_state": create_debate_state(),
        "opinions": [],
        "synthesis": {},
    }