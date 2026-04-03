# -*- coding: utf-8 -*-
"""AI对话接口

提供AI对话相关的API端点，支持普通响应和SSE流式响应。
"""

from datetime import datetime
from typing import Optional
from fastapi import APIRouter, HTTPException
from sse_starlette.sse import EventSourceResponse
import json
import uuid

from app.models.ai_models import ChatRequest, ChatResponse
from app.services.ai.llm_adapter import get_default_llm_adapter, get_llm_adapter, get_llm_adapter_from_config_id

router = APIRouter()


def _get_llm_for_request(model: Optional[str]) -> "LLMToolAdapter":
    """根据请求参数获取LLM适配器

    Args:
        model: 模型参数，可以是配置ID(数字字符串)或模型名称

    Returns:
        LLMToolAdapter: LLM适配器实例
    """
    if model:
        # 尝试解析为配置ID
        try:
            config_id = int(model)
            llm = get_llm_adapter_from_config_id(config_id)
            if llm:
                return llm
        except ValueError:
            pass
        # 作为模型名称使用
        return get_llm_adapter(model)
    # 使用默认配置
    return get_default_llm_adapter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """AI对话 - 返回完整响应

    Args:
        request: 对话请求，包含股票代码、用户消息等

    Returns:
        ChatResponse: 对话响应，包含AI回复消息

    Raises:
        HTTPException: 调用LLM服务失败时抛出500错误
    """
    llm = _get_llm_for_request(request.model)

    messages = [
        {
            "role": "system",
            "content": "你是一位专业的股票分析师，请基于数据给出客观、专业的分析建议。",
        },
        {
            "role": "user",
            "content": f"股票代码: {request.stock_code}\n问题: {request.message}",
        },
    ]

    try:
        response = await llm.chat(messages)
        return ChatResponse(
            conversation_id=request.conversation_id or str(uuid.uuid4()),
            message=response.get("content", ""),
            created_at=datetime.now(),
            model=llm.config.model,
            tokens_used=response.get("usage", {}).get("total_tokens", 0),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI对话失败: {str(e)}")


@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """AI对话流式响应 - SSE

    通过Server-Sent Events返回流式响应，适用于需要实时输出的场景。

    Args:
        request: 对话请求，包含股票代码、用户消息等

    Returns:
        EventSourceResponse: SSE流式响应
    """

    async def generate():
        """生成SSE事件流"""
        llm = _get_llm_for_request(request.model)

        messages = [
            {
                "role": "system",
                "content": "你是一位专业的股票分析师，请基于数据给出客观、专业的分析建议。",
            },
            {
                "role": "user",
                "content": f"股票代码: {request.stock_code}\n问题: {request.message}",
            },
        ]

        try:
            async for chunk in llm.chat_stream(messages):
                content = chunk.get("content", "")
                if content:
                    yield {"data": json.dumps({"content": content})}
            yield {"data": "[DONE]"}
        except Exception as e:
            yield {"data": json.dumps({"error": str(e)})}

    return EventSourceResponse(generate())