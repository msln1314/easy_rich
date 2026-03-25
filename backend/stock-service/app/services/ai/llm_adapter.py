# -*- coding: utf-8 -*-
"""LLM适配器模块

提供统一的LLM调用接口，支持多种模型提供商。
支持OpenAI兼容API、流式响应和Function Calling。
"""

import os
import json
import logging
from typing import Any, Dict, List, Optional, AsyncGenerator, Callable
from dataclasses import dataclass, field
import httpx

logger = logging.getLogger(__name__)


@dataclass
class LLMConfig:
    """LLM配置类

    Attributes:
        provider: 模型提供商 (openai, deepseek, aliyun等)
        model: 模型名称
        api_key: API密钥
        api_base: API基础URL
        max_tokens: 最大生成token数
        temperature: 温度参数
        timeout: 请求超时时间(秒)
    """

    provider: str = "openai"
    model: str = "gpt-4"
    api_key: str = ""
    api_base: str = ""
    max_tokens: int = 4000
    temperature: float = 0.7
    timeout: int = 120

    def __init__(
        self,
        provider: str = "openai",
        model: str = "gpt-4",
        api_key: str = "",
        api_base: str = "",
        max_tokens: int = 4000,
        temperature: float = 0.7,
        timeout: int = 120,
    ):
        """初始化LLM配置

        Args:
            provider: 模型提供商
            model: 模型名称
            api_key: API密钥，默认从环境变量OPENAI_API_KEY获取
            api_base: API基础URL，默认从环境变量OPENAI_API_BASE获取
            max_tokens: 最大生成token数
            temperature: 温度参数，控制生成随机性
            timeout: 请求超时时间(秒)
        """
        self.provider = provider
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.api_base = api_base or os.getenv(
            "OPENAI_API_BASE", "https://api.openai.com/v1"
        )
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.timeout = timeout


class LLMToolAdapter:
    """LLM工具适配器

    提供统一的LLM调用接口，支持:
    - OpenAI兼容API
    - 流式响应 (SSE)
    - Function Calling (tools)
    """

    def __init__(self, config: LLMConfig):
        """初始化LLM适配器

        Args:
            config: LLM配置对象
        """
        self.config = config
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        """获取或创建HTTP客户端

        Returns:
            httpx.AsyncClient: 异步HTTP客户端
        """
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                timeout=httpx.Timeout(self.config.timeout),
                headers={
                    "Authorization": f"Bearer {self.config.api_key}",
                    "Content-Type": "application/json",
                },
            )
        return self._client

    async def close(self) -> None:
        """关闭HTTP客户端"""
        if self._client and not self._client.is_closed:
            await self._client.aclose()
            self._client = None

    def _build_request_body(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_choice: Optional[str] = None,
        stream: bool = False,
    ) -> Dict[str, Any]:
        """构建请求体

        Args:
            messages: 对话消息列表
            tools: 工具定义列表 (Function Calling)
            tool_choice: 工具选择策略
            stream: 是否启用流式响应

        Returns:
            Dict: 请求体字典
        """
        body: Dict[str, Any] = {
            "model": self.config.model,
            "messages": messages,
            "max_tokens": self.config.max_tokens,
            "temperature": self.config.temperature,
            "stream": stream,
        }

        if tools:
            body["tools"] = tools
            if tool_choice:
                body["tool_choice"] = tool_choice

        return body

    async def chat(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_choice: Optional[str] = None,
    ) -> Dict[str, Any]:
        """发送对话请求

        Args:
            messages: 对话消息列表，格式: [{"role": "user", "content": "..."}]
            tools: 工具定义列表 (Function Calling)
            tool_choice: 工具选择策略 ("auto", "none", 或具体工具)

        Returns:
            Dict: 响应结果，包含:
                - content: 文本内容
                - tool_calls: 工具调用列表(如果有)
                - raw_response: 原始响应

        Raises:
            httpx.HTTPError: HTTP请求错误
            ValueError: API返回错误
        """
        client = await self._get_client()
        body = self._build_request_body(
            messages=messages, tools=tools, tool_choice=tool_choice, stream=False
        )

        try:
            response = await client.post(
                f"{self.config.api_base}/chat/completions", json=body
            )
            response.raise_for_status()
            result = response.json()

            # 解析响应
            choice = result.get("choices", [{}])[0]
            message = choice.get("message", {})

            return {
                "content": message.get("content", ""),
                "tool_calls": message.get("tool_calls"),
                "finish_reason": choice.get("finish_reason"),
                "usage": result.get("usage", {}),
                "raw_response": result,
            }

        except httpx.HTTPStatusError as e:
            error_detail = ""
            try:
                error_detail = e.response.json()
            except Exception:
                error_detail = e.response.text
            logger.error(f"LLM API HTTP错误: {e.response.status_code} - {error_detail}")
            raise ValueError(f"LLM API错误: {e.response.status_code} - {error_detail}")
        except httpx.RequestError as e:
            logger.error(f"LLM API请求错误: {str(e)}")
            raise

    async def chat_stream(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_choice: Optional[str] = None,
        on_tool_call: Optional[Callable[[Dict[str, Any]], None]] = None,
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """流式对话请求 (SSE)

        Args:
            messages: 对话消息列表
            tools: 工具定义列表 (Function Calling)
            tool_choice: 工具选择策略
            on_tool_call: 工具调用回调函数

        Yields:
            Dict: 流式响应块，包含:
                - content: 文本内容增量
                - tool_calls: 工具调用(完整时)
                - finish_reason: 结束原因

        Raises:
            httpx.HTTPError: HTTP请求错误
            ValueError: API返回错误
        """
        client = await self._get_client()
        body = self._build_request_body(
            messages=messages, tools=tools, tool_choice=tool_choice, stream=True
        )

        try:
            async with client.stream(
                "POST",
                f"{self.config.api_base}/chat/completions",
                json=body,
            ) as response:
                response.raise_for_status()

                current_tool_calls: Dict[int, Dict[str, Any]] = {}

                async for line in response.aiter_lines():
                    if not line or line == "data: [DONE]":
                        continue

                    if line.startswith("data: "):
                        try:
                            data = json.loads(line[6:])
                        except json.JSONDecodeError:
                            continue

                        delta = data.get("choices", [{}])[0].get("delta", {})
                        finish_reason = data.get("choices", [{}])[0].get(
                            "finish_reason"
                        )

                        result: Dict[str, Any] = {
                            "content": "",
                            "tool_calls": None,
                            "finish_reason": finish_reason,
                        }

                        # 处理文本内容
                        if "content" in delta:
                            result["content"] = delta["content"]

                        # 处理工具调用
                        if "tool_calls" in delta:
                            for tool_call_delta in delta["tool_calls"]:
                                idx = tool_call_delta.get("index", 0)

                                if idx not in current_tool_calls:
                                    current_tool_calls[idx] = {
                                        "id": tool_call_delta.get("id", ""),
                                        "type": tool_call_delta.get("type", "function"),
                                        "function": {
                                            "name": "",
                                            "arguments": "",
                                        },
                                    }

                                # 更新工具调用信息
                                if tool_call_delta.get("id"):
                                    current_tool_calls[idx]["id"] = tool_call_delta["id"]

                                function_delta = tool_call_delta.get("function", {})
                                if "name" in function_delta:
                                    current_tool_calls[idx]["function"]["name"] = (
                                        function_delta["name"]
                                    )
                                if "arguments" in function_delta:
                                    current_tool_calls[idx]["function"]["arguments"] += (
                                        function_delta["arguments"]
                                    )

                        # 流结束时检查是否有完整的工具调用
                        if finish_reason:
                            if current_tool_calls:
                                result["tool_calls"] = list(current_tool_calls.values())
                                if on_tool_call:
                                    for tc in current_tool_calls.values():
                                        on_tool_call(tc)
                            current_tool_calls = {}

                        if result["content"] or result["tool_calls"] or finish_reason:
                            yield result

        except httpx.HTTPStatusError as e:
            error_detail = ""
            try:
                error_detail = e.response.json()
            except Exception:
                error_detail = e.response.text
            logger.error(f"LLM API HTTP错误: {e.response.status_code} - {error_detail}")
            raise ValueError(f"LLM API错误: {e.response.status_code} - {error_detail}")
        except httpx.RequestError as e:
            logger.error(f"LLM API请求错误: {str(e)}")
            raise

    async def __aenter__(self) -> "LLMToolAdapter":
        """异步上下文管理器入口"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """异步上下文管理器出口"""
        await self.close()


# 预设模型配置
MODEL_CONFIGS: Dict[str, LLMConfig] = {
    "gpt-4": LLMConfig(provider="openai", model="gpt-4"),
    "gpt-4-turbo": LLMConfig(provider="openai", model="gpt-4-turbo-preview"),
    "gpt-3.5-turbo": LLMConfig(provider="openai", model="gpt-3.5-turbo"),
    "deepseek-chat": LLMConfig(
        provider="deepseek",
        model="deepseek-chat",
        api_base="https://api.deepseek.com/v1",
    ),
    "deepseek-coder": LLMConfig(
        provider="deepseek",
        model="deepseek-coder",
        api_base="https://api.deepseek.com/v1",
    ),
    "qwen-max": LLMConfig(
        provider="aliyun",
        model="qwen-max",
        api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
    ),
    "qwen-plus": LLMConfig(
        provider="aliyun",
        model="qwen-plus",
        api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
    ),
    "qwen-turbo": LLMConfig(
        provider="aliyun",
        model="qwen-turbo",
        api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
    ),
}


def get_llm_adapter(model: str = "gpt-4") -> LLMToolAdapter:
    """获取LLM适配器

    根据模型名称获取预设配置的LLM适配器实例。

    Args:
        model: 模型名称，支持预设模型或自定义模型名称

    Returns:
        LLMToolAdapter: LLM适配器实例

    Example:
        >>> adapter = get_llm_adapter("gpt-4")
        >>> response = await adapter.chat([
        ...     {"role": "user", "content": "Hello!"}
        ... ])

        >>> # 使用DeepSeek模型
        >>> adapter = get_llm_adapter("deepseek-chat")
        >>> response = await adapter.chat([
        ...     {"role": "user", "content": "你好!"}
        ... ])
    """
    config = MODEL_CONFIGS.get(model, LLMConfig(model=model))
    return LLMToolAdapter(config)


def get_llm_adapter_with_config(config: LLMConfig) -> LLMToolAdapter:
    """使用自定义配置获取LLM适配器

    Args:
        config: 自定义LLM配置

    Returns:
        LLMToolAdapter: LLM适配器实例
    """
    return LLMToolAdapter(config)