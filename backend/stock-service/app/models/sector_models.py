from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ConceptBoard(BaseModel):
    """概念板块模型"""

    rank: int = Field(..., description="排名")
    name: str = Field(..., description="板块名称")
    code: str = Field(..., description="板块代码")
    price: float = Field(..., description="最新价")
    change: float = Field(..., description="涨跌额")
    change_percent: float = Field(..., description="涨跌幅(%)")
    market_value: Optional[int] = Field(None, description="总市值")
    turnover_rate: float = Field(..., description="换手率(%)")
    up_count: int = Field(..., description="上涨家数")
    down_count: int = Field(..., description="下跌家数")
    leading_stock: str = Field(..., description="领涨股票")
    leading_stock_change_percent: float = Field(..., description="领涨股票涨跌幅(%)")
    update_time: datetime = Field(default_factory=datetime.now, description="更新时间")


class IndustryBoard(BaseModel):
    """行业板块模型"""

    rank: int = Field(..., description="排名")
    name: str = Field(..., description="板块名称")
    code: str = Field(..., description="板块代码")
    price: float = Field(..., description="最新价")
    change: float = Field(..., description="涨跌额")
    change_percent: float = Field(..., description="涨跌幅(%)")
    market_value: Optional[int] = Field(None, description="总市值")
    turnover_rate: float = Field(..., description="换手率(%)")
    up_count: int = Field(..., description="上涨家数")
    down_count: int = Field(..., description="下跌家数")
    leading_stock: str = Field(..., description="领涨股票")
    leading_stock_change_percent: float = Field(..., description="领涨股票涨跌幅(%)")
    update_time: datetime = Field(default_factory=datetime.now, description="更新时间")


class BoardSpot(BaseModel):
    """通用板块实时行情详情模型"""

    name: str = Field(..., description="板块名称")
    price: float = Field(..., description="最新价")
    high: float = Field(..., description="最高价")
    low: float = Field(..., description="最低价")
    open: float = Field(..., description="开盘价")
    volume: float = Field(..., description="成交量")
    amount: float = Field(..., description="成交额")
    turnover_rate: float = Field(..., description="换手率(%)")
    change: float = Field(..., description="涨跌额")
    change_percent: float = Field(..., description="涨跌幅(%)")
    amplitude: float = Field(..., description="振幅(%)")
    update_time: datetime = Field(default_factory=datetime.now, description="更新时间")


class ConceptBoardSpot(BoardSpot):
    """概念板块实时行情详情模型"""

    pass


class IndustryBoardSpot(BoardSpot):
    """行业板块实时行情详情模型"""

    pass


class ConceptBoardConstituent(BaseModel):
    """概念板块成份股模型"""

    rank: int = Field(..., description="序号")
    code: str = Field(..., description="股票代码")
    name: str = Field(..., description="股票名称")
    price: float = Field(..., description="最新价")
    change_percent: float = Field(..., description="涨跌幅(%)")
    change: float = Field(..., description="涨跌额")
    volume: float = Field(..., description="成交量(手)")
    amount: float = Field(..., description="成交额")
    amplitude: float = Field(..., description="振幅(%)")
    high: float = Field(..., description="最高价")
    low: float = Field(..., description="最低价")
    open: float = Field(..., description="今开")
    pre_close: float = Field(..., description="昨收")
    turnover_rate: float = Field(..., description="换手率(%)")
    pe_ratio: Optional[float] = Field(None, description="市盈率-动态")
    pb_ratio: Optional[float] = Field(None, description="市净率")
    update_time: datetime = Field(default_factory=datetime.now, description="更新时间")


class IndustryBoardConstituent(BaseModel):
    """行业板块成份股模型"""

    rank: int = Field(..., description="序号")
    code: str = Field(..., description="股票代码")
    name: str = Field(..., description="股票名称")
    price: float = Field(..., description="最新价")
    change_percent: float = Field(..., description="涨跌幅(%)")
    change: float = Field(..., description="涨跌额")
    volume: float = Field(..., description="成交量(手)")
    amount: float = Field(..., description="成交额")
    amplitude: float = Field(..., description="振幅(%)")
    high: float = Field(..., description="最高价")
    low: float = Field(..., description="最低价")
    open: float = Field(..., description="今开")
    pre_close: float = Field(..., description="昨收")
    turnover_rate: float = Field(..., description="换手率(%)")
    pe_ratio: Optional[float] = Field(None, description="市盈率-动态")
    pb_ratio: Optional[float] = Field(None, description="市净率")
    update_time: datetime = Field(default_factory=datetime.now, description="更新时间")


# ============ 板块轮动增强模型 ============


class LeaderStock(BaseModel):
    """龙头股信息模型"""

    code: str = Field(..., description="股票代码")
    name: str = Field(..., description="股票名称")
    price: float = Field(default=0, description="最新价")
    change_percent: float = Field(default=0, description="涨跌幅(%)")
    change: float = Field(default=0, description="涨跌额")
    volume: float = Field(default=0, description="成交量(手)")
    amount: float = Field(default=0, description="成交额")
    turnover_rate: float = Field(default=0, description="换手率(%)")
    score: float = Field(default=0, description="龙头评分(0-100)")
    is_limit_up: bool = Field(default=False, description="是否涨停")
    update_time: datetime = Field(default_factory=datetime.now, description="更新时间")


class SectorLeader(BaseModel):
    """板块龙头股模型"""

    sector_code: str = Field(..., description="板块代码")
    sector_name: str = Field(..., description="板块名称")
    sector_type: str = Field(
        default="industry", description="板块类型: industry/concept"
    )
    leader_stock: Optional[LeaderStock] = Field(None, description="龙头股信息")
    second_leader: Optional[LeaderStock] = Field(None, description="二龙头信息")
    third_leader: Optional[LeaderStock] = Field(None, description="三龙头信息")
    change_percent: float = Field(default=0, description="板块涨跌幅(%)")
    up_count: int = Field(default=0, description="上涨家数")
    down_count: int = Field(default=0, description="下跌家数")
    limit_up_count: int = Field(default=0, description="涨停家数")
    limit_down_count: int = Field(default=0, description="跌停家数")
    active_stocks: int = Field(default=0, description="活跃股数量(涨幅>3%)")
    fund_inflow: float = Field(default=0, description="资金净流入(万)")
    total_amount: float = Field(default=0, description="总成交额(万)")
    activity_score: float = Field(default=0, description="板块活跃度评分(0-100)")
    update_time: datetime = Field(default_factory=datetime.now, description="更新时间")


class SectorLeaderRanking(BaseModel):
    """板块龙头股排行模型"""

    rank: int = Field(..., description="排名")
    sector_code: str = Field(..., description="板块代码")
    sector_name: str = Field(..., description="板块名称")
    sector_type: str = Field(default="industry", description="板块类型")
    leader_stock: Optional[LeaderStock] = Field(None, description="龙头股信息")
    sector_change_percent: float = Field(default=0, description="板块涨跌幅(%)")
    activity_score: float = Field(default=0, description="板块活跃度评分")
    leader_score: float = Field(default=0, description="龙头股评分")
    update_time: datetime = Field(default_factory=datetime.now, description="更新时间")


class SectorRealtimeStatus(BaseModel):
    """板块实时状态模型（用于监控）"""

    sector_code: str = Field(..., description="板块代码")
    sector_name: str = Field(..., description="板块名称")
    sector_type: str = Field(default="industry", description="板块类型")
    change_percent: float = Field(default=0, description="涨跌幅(%)")
    change: float = Field(default=0, description="涨跌额")
    price: float = Field(default=0, description="最新价")
    high: float = Field(default=0, description="最高价")
    low: float = Field(default=0, description="最低价")
    open: float = Field(default=0, description="开盘价")
    volume: float = Field(default=0, description="成交量")
    amount: float = Field(default=0, description="成交额")
    turnover_rate: float = Field(default=0, description="换手率(%)")
    up_count: int = Field(default=0, description="上涨家数")
    down_count: int = Field(default=0, description="下跌家数")
    leading_stock: str = Field(default="", description="领涨股票")
    leading_stock_change_percent: float = Field(default=0, description="领涨股票涨跌幅")
    update_time: datetime = Field(default_factory=datetime.now, description="更新时间")


class SectorRotationHistory(BaseModel):
    """板块轮动历史数据模型"""

    date: str = Field(..., description="日期")
    sector_code: str = Field(..., description="板块代码")
    sector_name: str = Field(..., description="板块名称")
    sector_type: str = Field(default="industry", description="板块类型")
    open: float = Field(default=0, description="开盘价")
    close: float = Field(default=0, description="收盘价")
    high: float = Field(default=0, description="最高价")
    low: float = Field(default=0, description="最低价")
    volume: float = Field(default=0, description="成交量")
    amount: float = Field(default=0, description="成交额")
    change_percent: float = Field(default=0, description="涨跌幅(%)")
    amplitude: float = Field(default=0, description="振幅(%)")
    turnover_rate: float = Field(default=0, description="换手率(%)")
    update_time: datetime = Field(default_factory=datetime.now, description="更新时间")


class RotationPattern(BaseModel):
    """板块轮动规律模型"""

    pattern_id: str = Field(..., description="规律ID")
    pattern_name: str = Field(..., description="规律名称")
    trigger_condition: str = Field(default="", description="触发条件描述")
    current_sector: str = Field(default="", description="当前板块")
    next_sectors: List[str] = Field(
        default_factory=list, description="预测下一轮动板块"
    )
    confidence: float = Field(default=0, description="置信度(0-100)")
    historical_accuracy: float = Field(default=0, description="历史准确率(%)")
    occurrence_count: int = Field(default=0, description="历史出现次数")
    avg_rotation_days: float = Field(default=0, description="平均轮动天数")
    update_time: datetime = Field(default_factory=datetime.now, description="更新时间")


class RotationPrediction(BaseModel):
    """板块轮动预测模型"""

    prediction_id: str = Field(..., description="预测ID")
    prediction_time: datetime = Field(
        default_factory=datetime.now, description="预测时间"
    )
    target_date: str = Field(default="", description="预测目标日期")
    predictions: List[dict] = Field(default_factory=list, description="预测结果列表")
    model_version: str = Field(default="1.0", description="模型版本")
    confidence: float = Field(default=0, description="整体置信度")
    update_time: datetime = Field(default_factory=datetime.now, description="更新时间")


class SectorFactor(BaseModel):
    """板块多因子数据模型"""

    sector_code: str = Field(..., description="板块代码")
    sector_name: str = Field(..., description="板块名称")
    sector_type: str = Field(default="industry", description="板块类型")
    # 资金流因子
    fund_flow_score: float = Field(default=0, description="资金流因子得分")
    main_net_inflow: float = Field(default=0, description="主力净流入")
    super_net_inflow: float = Field(default=0, description="超大单净流入")
    big_net_inflow: float = Field(default=0, description="大单净流入")
    # 情绪因子
    sentiment_score: float = Field(default=0, description="情绪因子得分")
    limit_up_count: int = Field(default=0, description="涨停家数")
    up_count: int = Field(default=0, description="上涨家数")
    # 技术因子
    technical_score: float = Field(default=0, description="技术因子得分")
    ma5: float = Field(default=0, description="5日均线")
    ma10: float = Field(default=0, description="10日均线")
    ma20: float = Field(default=0, description="20日均线")
    macd: float = Field(default=0, description="MACD")
    rsi: float = Field(default=0, description="RSI")
    # 模式因子
    pattern_score: float = Field(default=0, description="模式因子得分")
    # 综合得分
    total_score: float = Field(default=0, description="综合得分")
    update_time: datetime = Field(default_factory=datetime.now, description="更新时间")
