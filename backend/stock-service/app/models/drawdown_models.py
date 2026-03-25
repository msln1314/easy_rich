# backend/stock-service/app/models/drawdown_models.py
# -*- coding: utf-8 -*-
"""
回撤分析数据模型
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date


class DrawdownPoint(BaseModel):
    """单次回撤记录"""
    peak_date: date = Field(..., description="峰值日期")
    peak_price: float = Field(..., description="峰值价格")
    trough_date: date = Field(..., description="谷值日期")
    trough_price: float = Field(..., description="谷值价格")
    drawdown_percent: float = Field(..., description="回撤幅度(%)")
    duration_days: int = Field(..., description="回撤持续天数")
    recovery_date: Optional[date] = Field(None, description="恢复日期")
    recovery_days: Optional[int] = Field(None, description="恢复天数")


class DrawdownAnalysisResult(BaseModel):
    """回撤分析结果"""
    stock_code: str = Field(..., description="股票代码")
    stock_name: str = Field(..., description="股票名称")
    analysis_period: str = Field(..., description="分析周期")

    # 核心指标
    max_drawdown: float = Field(..., description="最大回撤(%)")
    max_drawdown_duration: int = Field(..., description="最大回撤持续天数")
    avg_drawdown: float = Field(..., description="平均回撤(%)")
    avg_recovery_days: float = Field(..., description="平均恢复天数")

    # 回撤次数统计
    drawdown_5p_count: int = Field(0, description="5%以上回撤次数")
    drawdown_10p_count: int = Field(0, description="10%以上回撤次数")
    drawdown_20p_count: int = Field(0, description="20%以上回撤次数")
    drawdown_30p_count: int = Field(0, description="30%以上回撤次数")

    # 详细回撤记录
    drawdown_points: List[DrawdownPoint] = Field(default_factory=list, description="回撤点列表")


class PullbackSignal(BaseModel):
    """回调买入信号"""
    signal_date: date = Field(..., description="信号日期")
    signal_type: str = Field(..., description="信号类型: support/volume/pattern")
    signal_strength: float = Field(..., ge=0, le=100, description="信号强度0-100")
    current_drawdown: float = Field(..., description="当前回调幅度(%)")
    support_price: float = Field(..., description="支撑位价格")
    stop_loss_price: float = Field(..., description="建议止损价")
    reasoning: str = Field(..., description="信号理由")


class PositionMonitor(BaseModel):
    """持仓监控"""
    stock_code: str = Field(..., description="股票代码")
    cost_price: float = Field(..., description="成本价")
    current_price: float = Field(..., description="当前价格")
    highest_price: float = Field(..., description="持仓期间最高价")
    profit_percent: float = Field(..., description="当前盈利(%)")
    drawdown_from_high: float = Field(..., description="从最高点回撤(%)")
    drawdown_from_cost: float = Field(..., description="从成本回撤(%)")
    suggested_stop_profit: float = Field(..., description="建议止盈价")
    alert_level: str = Field(..., description="警告级别: 正常/注意/警告")


class DrawdownHistoryData(BaseModel):
    """历史回撤图表数据"""
    dates: List[str] = Field(default_factory=list, description="日期列表")
    prices: List[float] = Field(default_factory=list, description="价格列表")
    drawdown_areas: List[dict] = Field(default_factory=list, description="回撤区域")


# 请求模型
class DrawdownAnalyzeRequest(BaseModel):
    """回撤分析请求"""
    stock_code: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class PositionMonitorRequest(BaseModel):
    """持仓监控请求"""
    stock_code: str
    cost_price: float
    position_date: date