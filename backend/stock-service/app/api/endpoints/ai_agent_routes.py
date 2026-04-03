# -*- coding: utf-8 -*-
"""多Agent分析接口

提供多Agent股票分析的API端点，支持普通响应和SSE流式响应。
"""

from fastapi import APIRouter, HTTPException
from sse_starlette.sse import EventSourceResponse
import json

from app.models.ai_models import AgentAnalyzeRequest, AgentAnalyzeResponse
from app.services.ai.agent_orchestrator import AgentOrchestrator
from app.services.ai.llm_adapter import get_default_llm_adapter

router = APIRouter()


@router.post("/analyze", response_model=AgentAnalyzeResponse)
async def analyze(request: AgentAnalyzeRequest):
    """多Agent分析 - 返回完整分析结果

    Args:
        request: 分析请求，包含股票代码、查询问题、分析模式等

    Returns:
        AgentAnalyzeResponse: 分析响应，包含综合信号、置信度、各Agent观点等

    Raises:
        HTTPException: 分析过程失败时抛出500错误
    """
    # 获取默认LLM配置
    default_llm = get_default_llm_adapter()
    model_name = default_llm.config.model

    orchestrator = AgentOrchestrator(
        mode=request.mode,
        model=model_name,
    )

    try:
        result = await orchestrator.run(
            stock_code=request.stock_code,
            query=request.query or "",
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"多Agent分析失败: {str(e)}")


@router.post("/analyze/stream")
async def analyze_stream(request: AgentAnalyzeRequest):
    """多Agent分析流式响应 - 返回分析进度和结果

    通过Server-Sent Events返回分析进度和最终结果，适用于需要实时展示分析过程的场景。

    Args:
        request: 分析请求，包含股票代码、查询问题、分析模式等

    Returns:
        EventSourceResponse: SSE流式响应，包含进度事件和结果事件
    """

    async def generate():
        """生成SSE事件流"""
        # 获取默认LLM配置
        default_llm = get_default_llm_adapter()
        model_name = default_llm.config.model

        orchestrator = AgentOrchestrator(mode=request.mode, model=model_name)
        progress_messages = []

        def progress_callback(msg: str):
            """进度回调函数，收集进度消息"""
            progress_messages.append(msg)

        try:
            # 发送开始事件
            yield {"data": json.dumps({"type": "start", "message": "开始分析..."})}

            # 执行分析
            result = await orchestrator.run(
                stock_code=request.stock_code,
                query=request.query or "",
                progress_callback=progress_callback,
            )

            # 发送进度事件
            for msg in progress_messages:
                yield {"data": json.dumps({"type": "progress", "message": msg})}

            # 发送结果事件
            yield {
                "data": json.dumps(
                    {
                        "type": "result",
                        "data": result.model_dump(),
                    }
                )
            }

        except Exception as e:
            yield {"data": json.dumps({"type": "error", "message": str(e)})}

    return EventSourceResponse(generate())