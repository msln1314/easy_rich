# -*- coding: utf-8 -*-
"""Agent基类

提供Agent的基础抽象类，定义Agent的标准接口和执行流程。
"""

import time
import json
import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Optional, List, Callable, Dict, Any

from app.services.ai.context import AgentContext
from app.services.ai.tool_registry import ToolRegistry
from app.services.ai.llm_adapter import LLMToolAdapter
from app.models.ai_models import AgentOpinion, StageResult, StageStatus

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Agent基类

    所有Agent的抽象基类，定义了Agent的标准接口和执行流程。
    子类需要实现system_prompt和build_user_message方法。

    Attributes:
        agent_name: Agent名称，用于标识
        agent_type: Agent类型
        tool_names: 可用工具名称列表，None表示使用所有工具
        max_steps: 最大执行步骤数
    """

    agent_name: str = "base"
    agent_type: str = "base"
    tool_names: Optional[List[str]] = None
    max_steps: int = 6

    def __init__(
        self,
        tool_registry: ToolRegistry,
        llm_adapter: LLMToolAdapter,
        skill_instructions: str = "",
    ):
        """初始化Agent

        Args:
            tool_registry: 工具注册中心
            llm_adapter: LLM适配器
            skill_instructions: 技能说明，用于增强Agent能力
        """
        self.tool_registry = tool_registry
        self.llm_adapter = llm_adapter
        self.skill_instructions = skill_instructions

    @abstractmethod
    def system_prompt(self, ctx: AgentContext) -> str:
        """返回系统提示词

        Args:
            ctx: Agent上下文

        Returns:
            系统提示词字符串
        """
        pass

    @abstractmethod
    def build_user_message(self, ctx: AgentContext) -> str:
        """构建用户消息

        Args:
            ctx: Agent上下文

        Returns:
            用户消息字符串
        """
        pass

    def post_process(
        self, ctx: AgentContext, raw_text: str
    ) -> Optional[AgentOpinion]:
        """后处理LLM输出

        子类可以重写此方法来解析LLM输出并生成AgentOpinion。

        Args:
            ctx: Agent上下文
            raw_text: LLM输出的原始文本

        Returns:
            AgentOpinion对象，如果无法解析则返回None
        """
        return None

    async def run(
        self,
        ctx: AgentContext,
        progress_callback: Callable[[str], None] = None,
    ) -> StageResult:
        """执行Agent分析

        执行流程:
        1. 构建消息
        2. 获取工具
        3. 调用LLM
        4. 处理工具调用
        5. 后处理
        6. 返回结果

        Args:
            ctx: Agent上下文
            progress_callback: 进度回调函数

        Returns:
            StageResult: 阶段执行结果
        """
        started_at = time.time()
        stage_name = f"{self.agent_name}_analysis"

        try:
            if progress_callback:
                progress_callback(f"[{self.agent_name}] 开始分析...")

            # 1. 构建消息
            messages = self._build_messages(ctx)

            # 2. 获取工具
            tools = self._get_tools()

            # 3. 调用LLM并处理工具调用
            final_content = ""
            tool_calls_count = 0

            for step in range(self.max_steps):
                if progress_callback:
                    progress_callback(
                        f"[{self.agent_name}] 执行步骤 {step + 1}/{self.max_steps}"
                    )

                # 调用LLM
                response = await self.llm_adapter.chat(
                    messages=messages,
                    tools=tools if tools else None,
                    tool_choice="auto" if tools else None,
                )

                content = response.get("content", "")
                tool_calls = response.get("tool_calls")
                finish_reason = response.get("finish_reason")

                # 如果有内容输出，保存
                if content:
                    final_content = content

                # 如果没有工具调用或已完成，结束循环
                if not tool_calls or finish_reason == "stop":
                    break

                # 4. 处理工具调用
                if tool_calls:
                    # 将助手消息添加到对话历史
                    messages.append(
                        {
                            "role": "assistant",
                            "content": content,
                            "tool_calls": tool_calls,
                        }
                    )

                    for tool_call in tool_calls:
                        tool_calls_count += 1
                        tool_id = tool_call.get("id", "")
                        function = tool_call.get("function", {})
                        tool_name = function.get("name", "")
                        arguments_str = function.get("arguments", "{}")

                        try:
                            arguments = json.loads(arguments_str)
                        except json.JSONDecodeError:
                            arguments = {}

                        if progress_callback:
                            progress_callback(
                                f"[{self.agent_name}] 调用工具: {tool_name}"
                            )

                        # 执行工具
                        try:
                            if tool_name in self.tool_registry:
                                result = self.tool_registry.execute(
                                    tool_name, **arguments
                                )
                            else:
                                result = {"error": f"工具 '{tool_name}' 不存在"}

                            result_str = json.dumps(
                                result, ensure_ascii=False, default=str
                            )
                        except Exception as e:
                            logger.error(f"工具执行错误: {tool_name} - {e}")
                            result_str = json.dumps(
                                {"error": str(e)}, ensure_ascii=False
                            )

                        # 添加工具结果到对话历史
                        messages.append(
                            {
                                "role": "tool",
                                "tool_call_id": tool_id,
                                "name": tool_name,
                                "content": result_str,
                            }
                        )

            # 5. 后处理
            opinion = self.post_process(ctx, final_content)

            # 将观点添加到上下文
            if opinion:
                ctx.add_opinion(opinion)

            duration_ms = int((time.time() - started_at) * 1000)

            if progress_callback:
                progress_callback(f"[{self.agent_name}] 分析完成")

            return StageResult(
                stage_name=stage_name,
                status=StageStatus.COMPLETED,
                output={
                    "content": final_content,
                    "tool_calls_count": tool_calls_count,
                    "opinion": opinion.__dict__ if opinion else None,
                },
                duration_ms=duration_ms,
            )

        except Exception as e:
            logger.error(f"Agent执行错误: {self.agent_name} - {e}")
            duration_ms = int((time.time() - started_at) * 1000)

            return StageResult(
                stage_name=stage_name,
                status=StageStatus.FAILED,
                error=str(e),
                duration_ms=duration_ms,
            )

    def _build_messages(self, ctx: AgentContext) -> List[Dict[str, str]]:
        """构建消息列表

        Args:
            ctx: Agent上下文

        Returns:
            消息列表
        """
        messages = []

        # 系统提示词
        system_prompt = self.system_prompt(ctx)

        # 注入缓存数据到系统提示词
        cached_data = self._inject_cached_data(ctx)
        if cached_data:
            system_prompt = f"{system_prompt}\n\n以下是已获取的数据，可直接使用:\n{cached_data}"

        messages.append({"role": "system", "content": system_prompt})

        # 技能说明
        if self.skill_instructions:
            messages.append({"role": "system", "content": self.skill_instructions})

        # 用户消息
        user_message = self.build_user_message(ctx)
        messages.append({"role": "user", "content": user_message})

        return messages

    def _inject_cached_data(self, ctx: AgentContext) -> str:
        """注入缓存数据

        将上下文中已缓存的数据格式化为可读文本。

        Args:
            ctx: Agent上下文

        Returns:
            格式化的缓存数据字符串
        """
        if not ctx.data:
            return ""

        parts = []
        for key, value in ctx.data.items():
            if value is not None:
                if isinstance(value, dict):
                    value_str = json.dumps(value, ensure_ascii=False, indent=2)
                elif isinstance(value, list):
                    value_str = json.dumps(value, ensure_ascii=False, indent=2)
                else:
                    value_str = str(value)
                parts.append(f"## {key}\n{value_str}")

        return "\n\n".join(parts)

    def _get_tools(self) -> List[Dict[str, Any]]:
        """获取可用工具

        Returns:
            OpenAI工具格式列表
        """
        if self.tool_names is None:
            # 使用所有工具
            return self.tool_registry.to_openai_tools()

        # 使用指定的工具
        tools = []
        for name in self.tool_names:
            tool_def = self.tool_registry.get(name)
            if tool_def:
                tools.append(tool_def.to_openai_tool())

        return tools