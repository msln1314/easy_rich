import json
import logging
import os
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from ..models.stock_calendar_event import StockCalendarEvent

logger = logging.getLogger(__name__)

AI_ANALYSIS_PROMPT = """你是一位专业的投资分析师。请分析以下事件对股票的潜在影响：

事件信息：
- 股票：{stock_name}({stock_code})
- 事件类型：{event_type}
- 事件标题：{event_title}
- 事件日期：{event_date}

请从以下维度分析：
1. 事件影响评分（-5到5分，负分利空，正分利好）
2. 情感判断（利好/中性/利空）
3. 具体影响分析（200字内）
4. 操作建议（100字内）

请以JSON格式返回：
{{
    "impact_score": 2.5,
    "sentiment": "利好",
    "analysis": "...",
    "suggestion": "..."
}}
"""


class AIAnalysisService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.api_key = os.getenv("AI_API_KEY", "")
        self.api_base = os.getenv("AI_API_BASE", "https://api.openai.com/v1")
        self.model = os.getenv("AI_MODEL", "gpt-3.5-turbo")

    async def analyze_event(self, event: StockCalendarEvent) -> dict:
        if not self.api_key:
            return {
                "impact_score": 0,
                "sentiment": "中性",
                "analysis": "AI分析服务未配置，请设置环境变量 AI_API_KEY",
                "suggestion": "请配置AI服务后重试",
            }

        prompt = AI_ANALYSIS_PROMPT.format(
            stock_name=event.stock_name or event.stock_code,
            stock_code=event.stock_code,
            event_type=event.event_type,
            event_title=event.title,
            event_date=str(event.event_date),
        )

        try:
            result = await self._call_ai_api(prompt)

            if result:
                event.ai_impact_score = result.get("impact_score", 0)
                sentiment_map = {"利好": 1, "中性": 2, "利空": 3}
                event.ai_sentiment = sentiment_map.get(
                    result.get("sentiment", "中性"), 2
                )
                event.ai_analysis = result.get("analysis", "")
                event.ai_suggestion = result.get("suggestion", "")
                await self.db.commit()

            return result or {"error": "AI分析返回空结果"}

        except Exception as e:
            logger.error(f"AI分析失败: {e}")
            return {"error": str(e)}

    async def _call_ai_api(self, prompt: str) -> Optional[dict]:
        try:
            import httpx

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.api_base}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": self.model,
                        "messages": [
                            {
                                "role": "system",
                                "content": "你是一位专业的投资分析师，请用JSON格式回复。",
                            },
                            {"role": "user", "content": prompt},
                        ],
                        "temperature": 0.7,
                        "max_tokens": 500,
                    },
                )

                if response.status_code == 200:
                    data = response.json()
                    content = data["choices"][0]["message"]["content"]
                    return json.loads(content)
                else:
                    logger.error(
                        f"AI API调用失败: {response.status_code} - {response.text}"
                    )
                    return None

        except Exception as e:
            logger.error(f"调用AI API失败: {e}")
            return None
