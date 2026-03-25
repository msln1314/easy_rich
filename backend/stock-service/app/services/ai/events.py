# -*- coding: utf-8 -*-
"""
统一流式事件系统
参考 valuecell StreamResponseEvent 设计
"""
import time
import json
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class StreamEventType(str, Enum):
    """流式事件类型"""
    # 会话事件
    SESSION_STARTED = "session_started"
    SESSION_COMPLETED = "session_completed"
    SESSION_ERROR = "session_error"

    # Agent事件
    AGENT_STARTED = "agent_started"
    AGENT_COMPLETED = "agent_completed"
    AGENT_FAILED = "agent_failed"

    # 消息事件
    MESSAGE_CHUNK = "message_chunk"
    MESSAGE_COMPLETE = "message_complete"

    # 工具事件
    TOOL_CALL_STARTED = "tool_call_started"
    TOOL_CALL_COMPLETED = "tool_call_completed"

    # 推理事件 (支持思维链模型)
    REASONING_STARTED = "reasoning_started"
    REASONING_CHUNK = "reasoning_chunk"
    REASONING_COMPLETED = "reasoning_completed"

    # 辩论事件
    DEBATE_STARTED = "debate_started"
    DEBATE_ROUND = "debate_round"
    DEBATE_COMPLETED = "debate_completed"

    # 进度事件
    PROGRESS = "progress"
    DATA_FETCH = "data_fetch"

    # 结果事件
    OPINION = "opinion"
    SYNTHESIS = "synthesis"


class BaseStreamEvent(BaseModel):
    """流式事件基类"""
    event: StreamEventType
    timestamp: float = Field(default_factory=time.time)
    data: Dict[str, Any] = Field(default_factory=dict)

    def to_sse(self) -> str:
        """转换为SSE格式"""
        return f"data: {self.model_dump_json()}\n\n"

    def to_json(self) -> str:
        """转换为JSON字符串"""
        return self.model_dump_json()


class SessionStartedEvent(BaseStreamEvent):
    """会话开始事件"""
    event: StreamEventType = StreamEventType.SESSION_STARTED

    def __init__(self, session_id: str, stock_code: str = "", query: str = "", **kwargs):
        super().__init__(
            data={
                "session_id": session_id,
                "stock_code": stock_code,
                "query": query,
            }
        )


class SessionCompletedEvent(BaseStreamEvent):
    """会话完成事件"""
    event: StreamEventType = StreamEventType.SESSION_COMPLETED

    def __init__(self, session_id: str, duration_s: float = 0, tokens_used: int = 0, **kwargs):
        super().__init__(
            data={
                "session_id": session_id,
                "duration_s": duration_s,
                "tokens_used": tokens_used,
            }
        )


class SessionErrorEvent(BaseStreamEvent):
    """会话错误事件"""
    event: StreamEventType = StreamEventType.SESSION_ERROR

    def __init__(self, session_id: str, error: str, **kwargs):
        super().__init__(
            data={
                "session_id": session_id,
                "error": error,
            }
        )


class AgentStartedEvent(BaseStreamEvent):
    """Agent开始事件"""
    event: StreamEventType = StreamEventType.AGENT_STARTED

    def __init__(self, agent_name: str, agent_type: str = "", **kwargs):
        super().__init__(
            data={
                "agent_name": agent_name,
                "agent_type": agent_type,
            }
        )


class AgentCompletedEvent(BaseStreamEvent):
    """Agent完成事件"""
    event: StreamEventType = StreamEventType.AGENT_COMPLETED

    def __init__(self, agent_name: str, signal: str = "", confidence: float = 0, **kwargs):
        super().__init__(
            data={
                "agent_name": agent_name,
                "signal": signal,
                "confidence": confidence,
            }
        )


class AgentFailedEvent(BaseStreamEvent):
    """Agent失败事件"""
    event: StreamEventType = StreamEventType.AGENT_FAILED

    def __init__(self, agent_name: str, error: str, **kwargs):
        super().__init__(
            data={
                "agent_name": agent_name,
                "error": error,
            }
        )


class MessageChunkEvent(BaseStreamEvent):
    """消息块事件"""
    event: StreamEventType = StreamEventType.MESSAGE_CHUNK

    def __init__(self, content: str, agent_name: str = "", **kwargs):
        super().__init__(
            data={
                "content": content,
                "agent_name": agent_name,
            }
        )


class MessageCompleteEvent(BaseStreamEvent):
    """消息完成事件"""
    event: StreamEventType = StreamEventType.MESSAGE_COMPLETE

    def __init__(self, content: str, agent_name: str = "", **kwargs):
        super().__init__(
            data={
                "content": content,
                "agent_name": agent_name,
            }
        )


class ToolCallStartedEvent(BaseStreamEvent):
    """工具调用开始事件"""
    event: StreamEventType = StreamEventType.TOOL_CALL_STARTED

    def __init__(self, tool_name: str, arguments: Dict[str, Any] = None, agent_name: str = "", **kwargs):
        super().__init__(
            data={
                "tool_name": tool_name,
                "arguments": arguments or {},
                "agent_name": agent_name,
            }
        )


class ToolCallCompletedEvent(BaseStreamEvent):
    """工具调用完成事件"""
    event: StreamEventType = StreamEventType.TOOL_CALL_COMPLETED

    def __init__(self, tool_name: str, result: Any = None, agent_name: str = "", **kwargs):
        super().__init__(
            data={
                "tool_name": tool_name,
                "result": result,
                "agent_name": agent_name,
            }
        )


class ReasoningStartedEvent(BaseStreamEvent):
    """推理开始事件"""
    event: StreamEventType = StreamEventType.REASONING_STARTED

    def __init__(self, agent_name: str = "", **kwargs):
        super().__init__(
            data={
                "agent_name": agent_name,
            }
        )


class ReasoningChunkEvent(BaseStreamEvent):
    """推理块事件"""
    event: StreamEventType = StreamEventType.REASONING_CHUNK

    def __init__(self, content: str, agent_name: str = "", **kwargs):
        super().__init__(
            data={
                "content": content,
                "agent_name": agent_name,
            }
        )


class ReasoningCompletedEvent(BaseStreamEvent):
    """推理完成事件"""
    event: StreamEventType = StreamEventType.REASONING_COMPLETED

    def __init__(self, agent_name: str = "", **kwargs):
        super().__init__(
            data={
                "agent_name": agent_name,
            }
        )


class DebateStartedEvent(BaseStreamEvent):
    """辩论开始事件"""
    event: StreamEventType = StreamEventType.DEBATE_STARTED

    def __init__(self, topic: str = "", **kwargs):
        super().__init__(
            data={
                "topic": topic,
            }
        )


class DebateRoundEvent(BaseStreamEvent):
    """辩论轮次事件"""
    event: StreamEventType = StreamEventType.DEBATE_ROUND

    def __init__(self, round_num: int, bull_view: str = "", bear_view: str = "", **kwargs):
        super().__init__(
            data={
                "round": round_num,
                "bull_view": bull_view,
                "bear_view": bear_view,
            }
        )


class DebateCompletedEvent(BaseStreamEvent):
    """辩论完成事件"""
    event: StreamEventType = StreamEventType.DEBATE_COMPLETED

    def __init__(self, decision: str = "", reasoning: str = "", **kwargs):
        super().__init__(
            data={
                "decision": decision,
                "reasoning": reasoning,
            }
        )


class ProgressEvent(BaseStreamEvent):
    """进度事件"""
    event: StreamEventType = StreamEventType.PROGRESS

    def __init__(self, message: str, progress: float = 0, **kwargs):
        super().__init__(
            data={
                "message": message,
                "progress": progress,
            }
        )


class DataFetchEvent(BaseStreamEvent):
    """数据获取事件"""
    event: StreamEventType = StreamEventType.DATA_FETCH

    def __init__(self, data_type: str, status: str = "started", **kwargs):
        super().__init__(
            data={
                "data_type": data_type,
                "status": status,
            }
        )


class OpinionEvent(BaseStreamEvent):
    """观点事件"""
    event: StreamEventType = StreamEventType.OPINION

    def __init__(
        self,
        agent_name: str,
        agent_type: str,
        signal: str,
        confidence: float,
        reasoning: str,
        key_points: List[str] = None,
        key_levels: Dict[str, float] = None,
        **kwargs,
    ):
        super().__init__(
            data={
                "agent_name": agent_name,
                "agent_type": agent_type,
                "signal": signal,
                "confidence": confidence,
                "reasoning": reasoning,
                "key_points": key_points or [],
                "key_levels": key_levels or {},
            }
        )


class SynthesisEvent(BaseStreamEvent):
    """综合研判事件"""
    event: StreamEventType = StreamEventType.SYNTHESIS

    def __init__(
        self,
        conclusion: str,
        confidence: float,
        target_price: Optional[float],
        stop_loss: Optional[float],
        risk_level: str,
        operation_advice: str,
        key_factors: List[str] = None,
        **kwargs,
    ):
        super().__init__(
            data={
                "conclusion": conclusion,
                "confidence": confidence,
                "target_price": target_price,
                "stop_loss": stop_loss,
                "risk_level": risk_level,
                "operation_advice": operation_advice,
                "key_factors": key_factors or [],
            }
        )


# 事件工厂函数
def create_event(event_type: StreamEventType, **kwargs) -> BaseStreamEvent:
    """创建流式事件"""
    event_classes = {
        StreamEventType.SESSION_STARTED: SessionStartedEvent,
        StreamEventType.SESSION_COMPLETED: SessionCompletedEvent,
        StreamEventType.SESSION_ERROR: SessionErrorEvent,
        StreamEventType.AGENT_STARTED: AgentStartedEvent,
        StreamEventType.AGENT_COMPLETED: AgentCompletedEvent,
        StreamEventType.AGENT_FAILED: AgentFailedEvent,
        StreamEventType.MESSAGE_CHUNK: MessageChunkEvent,
        StreamEventType.MESSAGE_COMPLETE: MessageCompleteEvent,
        StreamEventType.TOOL_CALL_STARTED: ToolCallStartedEvent,
        StreamEventType.TOOL_CALL_COMPLETED: ToolCallCompletedEvent,
        StreamEventType.REASONING_STARTED: ReasoningStartedEvent,
        StreamEventType.REASONING_CHUNK: ReasoningChunkEvent,
        StreamEventType.REASONING_COMPLETED: ReasoningCompletedEvent,
        StreamEventType.DEBATE_STARTED: DebateStartedEvent,
        StreamEventType.DEBATE_ROUND: DebateRoundEvent,
        StreamEventType.DEBATE_COMPLETED: DebateCompletedEvent,
        StreamEventType.PROGRESS: ProgressEvent,
        StreamEventType.DATA_FETCH: DataFetchEvent,
        StreamEventType.OPINION: OpinionEvent,
        StreamEventType.SYNTHESIS: SynthesisEvent,
    }

    event_class = event_classes.get(event_type, BaseStreamEvent)
    return event_class(**kwargs)