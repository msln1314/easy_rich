# -*- coding: utf-8 -*-
"""AI服务模块

提供完整的AI分析能力，包括：
- 多Agent协调器
- 模型工厂（支持Provider回退）
- 三层配置系统
- 统一流式事件
- 辩论状态管理
"""

from app.services.ai.context import AgentContext
from app.services.ai.tool_registry import ToolRegistry, tool, get_default_registry
from app.services.ai.llm_adapter import LLMToolAdapter, LLMConfig, get_llm_adapter
from app.services.ai.agent_orchestrator import AgentOrchestrator
from app.services.ai.model_factory import ModelFactory, get_model_factory, create_model_for_agent
from app.services.ai.events import (
    BaseStreamEvent,
    StreamEventType,
    create_event,
    SessionStartedEvent,
    SessionCompletedEvent,
    AgentStartedEvent,
    AgentCompletedEvent,
    MessageChunkEvent,
    ToolCallStartedEvent,
    ProgressEvent,
    OpinionEvent,
    SynthesisEvent,
)
from app.services.ai.states import (
    AgentDebateState,
    MultiAgentState,
    DebateManager,
    DebateResult,
    create_debate_state,
    create_multi_agent_state,
)
from app.services.ai.config import ConfigManager, get_config_manager

__all__ = [
    # 核心模块
    "AgentContext",
    "ToolRegistry",
    "tool",
    "get_default_registry",
    "LLMToolAdapter",
    "LLMConfig",
    "get_llm_adapter",
    "AgentOrchestrator",

    # 模型工厂
    "ModelFactory",
    "get_model_factory",
    "create_model_for_agent",

    # 流式事件
    "BaseStreamEvent",
    "StreamEventType",
    "create_event",
    "SessionStartedEvent",
    "SessionCompletedEvent",
    "AgentStartedEvent",
    "AgentCompletedEvent",
    "MessageChunkEvent",
    "ToolCallStartedEvent",
    "ProgressEvent",
    "OpinionEvent",
    "SynthesisEvent",

    # 状态管理
    "AgentDebateState",
    "MultiAgentState",
    "DebateManager",
    "DebateResult",
    "create_debate_state",
    "create_multi_agent_state",

    # 配置
    "ConfigManager",
    "get_config_manager",
]