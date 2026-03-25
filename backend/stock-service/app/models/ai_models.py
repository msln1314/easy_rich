"""AI分析相关数据模型"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# ============== 枚举类 ==============

class Signal(str, Enum):
    """交易信号"""
    STRONG_BUY = "strong_buy"
    BUY = "buy"
    HOLD = "hold"
    SELL = "sell"
    STRONG_SELL = "strong_sell"


class StageStatus(str, Enum):
    """阶段状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


# ============== 请求模型 ==============

class ChatRequest(BaseModel):
    """对话请求"""
    stock_code: str = Field(..., description="股票代码")
    message: str = Field(..., description="用户消息")
    conversation_id: Optional[str] = Field(None, description="会话ID，用于多轮对话")
    model: Optional[str] = Field(None, description="指定使用的模型")


class AgentAnalyzeRequest(BaseModel):
    """多Agent分析请求"""
    stock_code: str = Field(..., description="股票代码")
    query: Optional[str] = Field(None, description="用户查询问题")
    mode: str = Field(default="standard", description="分析模式：standard/deep/quick")
    agents: List[str] = Field(default_factory=list, description="指定使用的Agent列表")


class ReportGenerateRequest(BaseModel):
    """研报生成请求"""
    stock_code: str = Field(..., description="股票代码")
    report_type: str = Field(default="comprehensive", description="研报类型：comprehensive/technical/fundamental")
    include_sections: Optional[List[str]] = Field(None, description="包含的章节")


class MarketInterpretRequest(BaseModel):
    """市场解读请求"""
    date: Optional[str] = Field(None, description="解读日期，默认今天")
    focus_sectors: Optional[List[str]] = Field(None, description="关注板块")
    include_individual_stocks: bool = Field(default=True, description="是否包含个股分析")


class DailyReviewRequest(BaseModel):
    """每日复盘请求"""
    date: Optional[str] = Field(None, description="复盘日期，默认今天")
    portfolio_codes: Optional[List[str]] = Field(None, description="持仓股票代码列表")
    watchlist_codes: Optional[List[str]] = Field(None, description="自选股代码列表")


class ScheduleCreateRequest(BaseModel):
    """创建定时任务请求"""
    task_type: str = Field(..., description="任务类型：daily_review/market_interpret/custom")
    cron_expression: str = Field(..., description="Cron表达式")
    enabled: bool = Field(default=True, description="是否启用")
    params: Optional[Dict[str, Any]] = Field(None, description="任务参数")


# ============== 响应模型 ==============

class ChatResponse(BaseModel):
    """对话响应"""
    conversation_id: str = Field(..., description="会话ID")
    message: str = Field(..., description="AI回复消息")
    created_at: datetime = Field(..., description="创建时间")
    model: Optional[str] = Field(None, description="使用的模型")
    tokens_used: Optional[int] = Field(None, description="使用的token数量")


class AgentAnalyzeResponse(BaseModel):
    """多Agent分析响应"""
    stock_code: str = Field(..., description="股票代码")
    stock_name: Optional[str] = Field(None, description="股票名称")
    analysis_time: datetime = Field(..., description="分析时间")
    signal: Signal = Field(..., description="综合交易信号")
    confidence: float = Field(..., description="置信度(0-1)")
    summary: str = Field(..., description="分析摘要")
    agent_opinions: List[Dict[str, Any]] = Field(default_factory=list, description="各Agent观点")
    risks: Optional[List[str]] = Field(None, description="风险提示")


class ReportResponse(BaseModel):
    """研报响应"""
    report_id: str = Field(..., description="研报ID")
    stock_code: str = Field(..., description="股票代码")
    stock_name: Optional[str] = Field(None, description="股票名称")
    title: str = Field(..., description="研报标题")
    content: str = Field(..., description="研报内容(Markdown格式)")
    created_at: datetime = Field(..., description="创建时间")
    report_type: str = Field(..., description="研报类型")


class MarketOverviewResponse(BaseModel):
    """市场概览响应"""
    date: str = Field(..., description="日期")
    market_sentiment: str = Field(..., description="市场情绪：bullish/bearish/neutral")
    index_summary: Dict[str, Any] = Field(..., description="指数概况")
    hot_sectors: List[Dict[str, Any]] = Field(default_factory=list, description="热门板块")
    cold_sectors: List[Dict[str, Any]] = Field(default_factory=list, description="冷门板块")
    key_events: Optional[List[str]] = Field(None, description="重要事件")
    interpretation: str = Field(..., description="市场解读")


class DailyReviewResponse(BaseModel):
    """每日复盘响应"""
    date: str = Field(..., description="复盘日期")
    market_summary: str = Field(..., description="市场总结")
    portfolio_review: Optional[List[Dict[str, Any]]] = Field(None, description="持仓复盘")
    watchlist_review: Optional[List[Dict[str, Any]]] = Field(None, description="自选股复盘")
    opportunities: List[str] = Field(default_factory=list, description="潜在机会")
    risks: List[str] = Field(default_factory=list, description="风险提示")
    suggestions: Optional[str] = Field(None, description="操作建议")


# ============== 数据类 ==============

@dataclass
class AgentOpinion:
    """Agent观点"""
    agent_name: str
    agent_type: str = ""
    signal: Signal = Signal.HOLD
    confidence: float = 0.5
    reasoning: str = ""
    supporting_data: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class StageResult:
    """阶段执行结果"""
    stage_name: str
    status: StageStatus
    output: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    duration_ms: Optional[int] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


@dataclass
class AgentContext:
    """Agent上下文"""
    stock_code: str
    stock_name: str
    current_price: float
    historical_data: List[Dict[str, Any]] = field(default_factory=list)
    technical_indicators: Dict[str, Any] = field(default_factory=dict)
    fundamental_data: Dict[str, Any] = field(default_factory=dict)
    news_data: List[Dict[str, Any]] = field(default_factory=list)
    market_context: Dict[str, Any] = field(default_factory=dict)
    additional_context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SynthesisResult:
    """综合研判结果"""
    stock_code: str
    signal: Signal
    confidence: float
    summary: str
    key_factors: List[str] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)
    agent_opinions: List[AgentOpinion] = field(default_factory=list)
    supporting_data: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)