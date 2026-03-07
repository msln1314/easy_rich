from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class GlobalFinanceNews(BaseModel):
    """全球财经快讯模型"""
    title: str = Field(..., description="标题")
    summary: str = Field(..., description="摘要")
    publish_time: str = Field(..., description="发布时间")
    link: str = Field(..., description="链接")
    update_time: datetime = Field(default_factory=datetime.now, description="更新时间")

class InteractiveQuestion(BaseModel):
    """互动易提问模型"""
    stock_code: str = Field(..., description="股票代码")
    stock_name: str = Field(..., description="公司简称")
    industry: Optional[str] = Field(None, description="行业")
    industry_code: Optional[str] = Field(None, description="行业代码")
    question: str = Field(..., description="问题")
    questioner: str = Field(..., description="提问者")
    source: str = Field(..., description="来源")
    question_time: datetime = Field(..., description="提问时间")
    update_time: datetime = Field(..., description="更新时间")
    questioner_id: Optional[str] = Field(None, description="提问者编号")
    question_id: Optional[str] = Field(None, description="问题编号")
    answer_id: Optional[str] = Field(None, description="回答ID")
    answer_content: Optional[str] = Field(None, description="回答内容")
    answerer: Optional[str] = Field(None, description="回答者")

class CLSTelegraph(BaseModel):
    """财联社电报模型"""
    title: str = Field(..., description="标题")
    content: str = Field(..., description="内容")
    publish_date: str = Field(..., description="发布日期")
    publish_time: str = Field(..., description="发布时间")
    update_time: datetime = Field(default_factory=datetime.now, description="更新时间")