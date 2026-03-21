# Portfolio Management Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 构建一个综合型投资组合管理模块，支持持仓管理、交易记录、业绩分析和风控预警功能。

**Architecture:** 采用前后端分离架构，后端基于FastAPI+SQLAlchemy提供REST API，前端使用Vue3+Element Plus实现组合概览、持仓管理和分析报告页面。

**Tech Stack:** FastAPI, SQLAlchemy 2.0, MySQL, Vue 3, Element Plus, TypeScript, ECharts

---

## Phase 1: 数据模型与基础API（2天）

### Task 1.1: 创建后端模块目录结构

**Files:**
- Create: `backend/apps/admin/portfolio/__init__.py`
- Create: `backend/apps/admin/portfolio/models/__init__.py`
- Create: `backend/apps/admin/portfolio/schemas/__init__.py`
- Create: `backend/apps/admin/portfolio/params/__init__.py`
- Create: `backend/apps/admin/portfolio/crud/__init__.py`
- Create: `backend/apps/admin/portfolio/services/__init__.py`

**Step 1: 创建目录**

```bash
mkdir -p backend/apps/admin/portfolio/models
mkdir -p backend/apps/admin/portfolio/schemas
mkdir -p backend/apps/admin/portfolio/params
mkdir -p backend/apps/admin/portfolio/crud
mkdir -p backend/apps/admin/portfolio/services
```

**Step 2: 创建初始化文件**

创建空的 `__init__.py` 文件在每个目录下。

**Step 3: 提交**

```bash
git add backend/apps/admin/portfolio/
git commit -m "feat(portfolio): init module directory structure"
```

---

### Task 1.2: 创建投资组合数据模型

**Files:**
- Create: `backend/apps/admin/portfolio/models/portfolio.py`

**Step 1: 编写数据模型**

```python
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Float, SmallInteger
from db.db_base import BaseModel


class Portfolio(BaseModel):
    __tablename__ = "portfolio"
    
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="用户ID")
    name: Mapped[str] = mapped_column(String(100), nullable=False, comment="组合名称")
    description: Mapped[str | None] = mapped_column(Text, nullable=True, comment="组合描述")
    
    target_allocation: Mapped[str | None] = mapped_column(Text, nullable=True, comment="目标资产配置JSON")
    
    max_single_position: Mapped[float] = mapped_column(Float, default=20.00, comment="单只股票最大仓位(%)")
    max_sector_position: Mapped[float] = mapped_column(Float, default=40.00, comment="单个行业最大仓位(%)")
    max_drawdown: Mapped[float] = mapped_column(Float, default=15.00, comment="最大回撤预警线(%)")
    rebalance_threshold: Mapped[float] = mapped_column(Float, default=5.00, comment="再平衡触发阈值(%)")
    rebalance_period: Mapped[str] = mapped_column(String(20), default='monthly', comment="再平衡周期")
    
    total_value: Mapped[float | None] = mapped_column(Float, nullable=True, comment="组合总市值")
    total_cost: Mapped[float | None] = mapped_column(Float, nullable=True, comment="组合总成本")
    total_profit: Mapped[float | None] = mapped_column(Float, nullable=True, comment="总盈亏")
    profit_rate: Mapped[float | None] = mapped_column(Float, nullable=True, comment="收益率")
    annual_return: Mapped[float | None] = mapped_column(Float, nullable=True, comment="年化收益率")
    
    benchmark_index: Mapped[str] = mapped_column(String(20), default='000300', comment="基准指数代码")
    is_default: Mapped[int] = mapped_column(SmallInteger, default=0, comment="是否默认组合")
    is_active: Mapped[int] = mapped_column(SmallInteger, default=1, comment="是否启用")
```

**Step 2: 更新 models/__init__.py**

```python
from .portfolio import Portfolio

__all__ = ['Portfolio']
```

**Step 3: 提交**

```bash
git add backend/apps/admin/portfolio/models/
git commit -m "feat(portfolio): add Portfolio model"
```

---

### Task 1.3: 创建持仓和交易数据模型

**Files:**
- Create: `backend/apps/admin/portfolio/models/portfolio_position.py`
- Create: `backend/apps/admin/portfolio/models/portfolio_trade.py`

**Step 1: 编写持仓模型**

```python
from datetime import date
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Float, SmallInteger, Date
from db.db_base import BaseModel


class PortfolioPosition(BaseModel):
    __tablename__ = "portfolio_position"
    __table_args__ = (
        UniqueConstraint('portfolio_id', 'stock_code', name='uk_portfolio_stock'),
        {'comment': '持仓表'}
    )
    
    portfolio_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="组合ID")
    stock_code: Mapped[str] = mapped_column(String(20), nullable=False, comment="股票代码")
    stock_name: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="股票名称")
    
    shares: Mapped[int] = mapped_column(Integer, nullable=False, comment="持仓股数")
    available_shares: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="可用股数")
    cost_price: Mapped[float] = mapped_column(Float, nullable=False, comment="成本价")
    current_price: Mapped[float | None] = mapped_column(Float, nullable=True, comment="现价")
    market_value: Mapped[float | None] = mapped_column(Float, nullable=True, comment="市值")
    
    profit: Mapped[float | None] = mapped_column(Float, nullable=True, comment="盈亏金额")
    profit_rate: Mapped[float | None] = mapped_column(Float, nullable=True, comment="盈亏比例")
    position_ratio: Mapped[float | None] = mapped_column(Float, nullable=True, comment="仓位占比(%)")
    target_ratio: Mapped[float | None] = mapped_column(Float, nullable=True, comment="目标仓位占比(%)")
    
    dividend_received: Mapped[float] = mapped_column(Float, default=0, comment="已收分红")
    first_buy_date: Mapped[date | None] = mapped_column(Date, nullable=True, comment="首次买入日期")
    last_trade_date: Mapped[date | None] = mapped_column(Date, nullable=True, comment="最近交易日期")
```

**Step 2: 编写交易记录模型**

```python
from datetime import date
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Float, Text, Date
from db.db_base import BaseModel


class PortfolioTrade(BaseModel):
    __tablename__ = "portfolio_trade"
    
    portfolio_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="组合ID")
    stock_code: Mapped[str] = mapped_column(String(20), nullable=False, comment="股票代码")
    stock_name: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="股票名称")
    
    trade_type: Mapped[str] = mapped_column(String(10), nullable=False, comment="交易类型: buy/sell/dividend")
    trade_date: Mapped[date] = mapped_column(Date, nullable=False, comment="交易日期")
    shares: Mapped[int] = mapped_column(Integer, nullable=False, comment="交易股数")
    price: Mapped[float] = mapped_column(Float, nullable=False, comment="交易价格")
    amount: Mapped[float] = mapped_column(Float, nullable=False, comment="交易金额")
    commission: Mapped[float] = mapped_column(Float, default=0, comment="手续费")
    stamp_duty: Mapped[float] = mapped_column(Float, default=0, comment="印花税")
    
    position_before: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="交易前持仓")
    position_after: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="交易后持仓")
    cost_price_before: Mapped[float | None] = mapped_column(Float, nullable=True, comment="交易前成本")
    cost_price_after: Mapped[float | None] = mapped_column(Float, nullable=True, comment="交易后成本")
    
    source: Mapped[str] = mapped_column(String(20), default='manual', comment="来源")
    remark: Mapped[str | None] = mapped_column(Text, nullable=True, comment="备注")
```

**Step 3: 更新 models/__init__.py**

```python
from .portfolio import Portfolio
from .portfolio_position import PortfolioPosition
from .portfolio_trade import PortfolioTrade

__all__ = ['Portfolio', 'PortfolioPosition', 'PortfolioTrade']
```

**Step 4: 提交**

```bash
git add backend/apps/admin/portfolio/models/
git commit -m "feat(portfolio): add Position and Trade models"
```

---

### Task 1.4: 创建风控预警和快照数据模型

**Files:**
- Create: `backend/apps/admin/portfolio/models/portfolio_risk_alert.py`
- Create: `backend/apps/admin/portfolio/models/portfolio_snapshot.py`

**Step 1: 编写风控预警模型**

```python
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Float, SmallInteger, Text, DateTime
from db.db_base import BaseModel


class PortfolioRiskAlert(BaseModel):
    __tablename__ = "portfolio_risk_alert"
    
    portfolio_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="组合ID")
    alert_type: Mapped[str] = mapped_column(String(50), nullable=False, comment="预警类型")
    alert_level: Mapped[str] = mapped_column(String(20), nullable=False, comment="预警级别")
    
    title: Mapped[str] = mapped_column(String(200), nullable=False, comment="预警标题")
    content: Mapped[str | None] = mapped_column(Text, nullable=True, comment="预警详情")
    
    related_stock_code: Mapped[str | None] = mapped_column(String(20), nullable=True, comment="关联股票代码")
    related_value: Mapped[float | None] = mapped_column(Float, nullable=True, comment="相关数值")
    threshold_value: Mapped[float | None] = mapped_column(Float, nullable=True, comment="阈值")
    
    is_read: Mapped[int] = mapped_column(SmallInteger, default=0, comment="是否已读")
    is_handled: Mapped[int] = mapped_column(SmallInteger, default=0, comment="是否处理")
    handle_note: Mapped[str | None] = mapped_column(Text, nullable=True, comment="处理备注")
    handled_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, comment="处理时间")
```

**Step 2: 编写快照模型**

```python
from datetime import date
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Float, Text, Date
from db.db_base import BaseModel


class PortfolioSnapshot(BaseModel):
    __tablename__ = "portfolio_snapshot"
    __table_args__ = (
        UniqueConstraint('portfolio_id', 'snapshot_date', name='uk_portfolio_date'),
        {'comment': '组合快照表'}
    )
    
    portfolio_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="组合ID")
    snapshot_date: Mapped[date] = mapped_column(Date, nullable=False, comment="快照日期")
    
    total_value: Mapped[float | None] = mapped_column(Float, nullable=True, comment="组合总市值")
    total_cost: Mapped[float | None] = mapped_column(Float, nullable=True, comment="组合总成本")
    profit_rate: Mapped[float | None] = mapped_column(Float, nullable=True, comment="收益率")
    
    sector_allocation: Mapped[str | None] = mapped_column(Text, nullable=True, comment="行业分布JSON")
    top_holdings: Mapped[str | None] = mapped_column(Text, nullable=True, comment="前十大持仓JSON")
    
    volatility: Mapped[float | None] = mapped_column(Float, nullable=True, comment="波动率")
    beta: Mapped[float | None] = mapped_column(Float, nullable=True, comment="Beta值")
```

**Step 3: 更新 models/__init__.py**

```python
from .portfolio import Portfolio
from .portfolio_position import PortfolioPosition
from .portfolio_trade import PortfolioTrade
from .portfolio_risk_alert import PortfolioRiskAlert
from .portfolio_snapshot import PortfolioSnapshot

__all__ = [
    'Portfolio', 
    'PortfolioPosition', 
    'PortfolioTrade',
    'PortfolioRiskAlert',
    'PortfolioSnapshot'
]
```

**Step 4: 提交**

```bash
git add backend/apps/admin/portfolio/models/
git commit -m "feat(portfolio): add RiskAlert and Snapshot models"
```

---

### Task 1.5: 创建Pydantic Schema定义

**Files:**
- Create: `backend/apps/admin/portfolio/schemas/portfolio.py`
- Create: `backend/apps/admin/portfolio/schemas/position.py`
- Create: `backend/apps/admin/portfolio/schemas/trade.py`

**Step 1: 编写组合Schema**

```python
from datetime import date
from typing import Optional, List, Any
from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr


class PortfolioCreate(BaseModel):
    name: str = Field(..., description="组合名称")
    description: Optional[str] = Field(None, description="组合描述")
    target_allocation: Optional[List[dict]] = Field(None, description="目标资产配置")
    max_single_position: float = Field(default=20.0, description="单只股票最大仓位")
    max_sector_position: float = Field(default=40.0, description="单个行业最大仓位")
    max_drawdown: float = Field(default=15.0, description="最大回撤预警线")
    rebalance_threshold: float = Field(default=5.0, description="再平衡触发阈值")
    rebalance_period: str = Field(default='monthly', description="再平衡周期")
    benchmark_index: str = Field(default='000300', description="基准指数代码")


class PortfolioUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    target_allocation: Optional[List[dict]] = None
    max_single_position: Optional[float] = None
    max_sector_position: Optional[float] = None
    max_drawdown: Optional[float] = None
    rebalance_threshold: Optional[float] = None
    rebalance_period: Optional[str] = None
    benchmark_index: Optional[str] = None
    is_active: Optional[int] = None


class PortfolioOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int
    name: str
    description: Optional[str] = None
    target_allocation: Optional[Any] = None
    max_single_position: float
    max_sector_position: float
    max_drawdown: float
    rebalance_threshold: float
    rebalance_period: str
    benchmark_index: str
    total_value: Optional[float] = None
    total_cost: Optional[float] = None
    total_profit: Optional[float] = None
    profit_rate: Optional[float] = None
    annual_return: Optional[float] = None
    is_default: int
    is_active: int
    created_at: DatetimeStr
    updated_at: DatetimeStr


class PortfolioListOut(BaseModel):
    total: int
    items: List[PortfolioOut]
```

**Step 2: 编写持仓Schema**

```python
from datetime import date
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr


class PositionCreate(BaseModel):
    stock_code: str = Field(..., description="股票代码")
    stock_name: Optional[str] = Field(None, description="股票名称")
    shares: int = Field(..., description="持仓股数")
    cost_price: float = Field(..., description="成本价")
    target_ratio: Optional[float] = Field(None, description="目标仓位占比")


class PositionUpdate(BaseModel):
    shares: Optional[int] = None
    cost_price: Optional[float] = None
    target_ratio: Optional[float] = None


class PositionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    portfolio_id: int
    stock_code: str
    stock_name: Optional[str] = None
    shares: int
    available_shares: Optional[int] = None
    cost_price: float
    current_price: Optional[float] = None
    market_value: Optional[float] = None
    profit: Optional[float] = None
    profit_rate: Optional[float] = None
    position_ratio: Optional[float] = None
    target_ratio: Optional[float] = None
    dividend_received: float
    first_buy_date: Optional[date] = None
    last_trade_date: Optional[date] = None
    created_at: DatetimeStr
    updated_at: DatetimeStr


class PositionListOut(BaseModel):
    total: int
    items: List[PositionOut]
```

**Step 3: 编写交易Schema**

```python
from datetime import date
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr


class TradeBuy(BaseModel):
    stock_code: str = Field(..., description="股票代码")
    stock_name: Optional[str] = Field(None, description="股票名称")
    shares: int = Field(..., ge=1, description="买入股数")
    price: float = Field(..., gt=0, description="买入价格")
    trade_date: date = Field(..., description="交易日期")
    commission: float = Field(default=0, description="手续费")
    remark: Optional[str] = Field(None, description="备注")


class TradeSell(BaseModel):
    stock_code: str = Field(..., description="股票代码")
    shares: int = Field(..., ge=1, description="卖出股数")
    price: float = Field(..., gt=0, description="卖出价格")
    trade_date: date = Field(..., description="交易日期")
    commission: float = Field(default=0, description="手续费")
    stamp_duty: float = Field(default=0, description="印花税")
    remark: Optional[str] = Field(None, description="备注")


class TradeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    portfolio_id: int
    stock_code: str
    stock_name: Optional[str] = None
    trade_type: str
    trade_date: date
    shares: int
    price: float
    amount: float
    commission: float
    stamp_duty: float
    position_before: Optional[int] = None
    position_after: Optional[int] = None
    cost_price_before: Optional[float] = None
    cost_price_after: Optional[float] = None
    source: str
    remark: Optional[str] = None
    created_at: DatetimeStr


class TradeListOut(BaseModel):
    total: int
    items: List[TradeOut]
```

**Step 4: 更新 schemas/__init__.py**

```python
from .portfolio import PortfolioCreate, PortfolioUpdate, PortfolioOut, PortfolioListOut
from .position import PositionCreate, PositionUpdate, PositionOut, PositionListOut
from .trade import TradeBuy, TradeSell, TradeOut, TradeListOut

__all__ = [
    'PortfolioCreate', 'PortfolioUpdate', 'PortfolioOut', 'PortfolioListOut',
    'PositionCreate', 'PositionUpdate', 'PositionOut', 'PositionListOut',
    'TradeBuy', 'TradeSell', 'TradeOut', 'TradeListOut'
]
```

**Step 5: 提交**

```bash
git add backend/apps/admin/portfolio/schemas/
git commit -m "feat(portfolio): add Pydantic schemas"
```

---

### Task 1.6: 创建CRUD操作

**Files:**
- Create: `backend/apps/admin/portfolio/crud/portfolio_crud.py`
- Create: `backend/apps/admin/portfolio/crud/position_crud.py`

**Step 1: 编写组合CRUD**

```python
from typing import List, Tuple, Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from core.crud import DalBase
from apps.admin.portfolio import models, schemas


class PortfolioDal(DalBase):
    
    def __init__(self, db: AsyncSession):
        super().__init__()
        self.db = db
        self.model = models.Portfolio
        self.schema = schemas.PortfolioOut

    async def get_list_by_user(self, user_id: int) -> List[models.Portfolio]:
        sql = select(self.model).where(
            and_(
                self.model.user_id == user_id,
                self.model.is_delete == False
            )
        ).order_by(self.model.is_default.desc(), self.model.created_at.desc())
        
        result = await self.db.scalars(sql)
        return result.all()

    async def get_default_portfolio(self, user_id: int) -> Optional[models.Portfolio]:
        sql = select(self.model).where(
            and_(
                self.model.user_id == user_id,
                self.model.is_default == 1,
                self.model.is_delete == False
            )
        )
        result = await self.db.scalars(sql)
        return result.first()

    async def create_portfolio(self, data: schemas.PortfolioCreate, user_id: int) -> models.Portfolio:
        obj = self.model(user_id=user_id, **data.model_dump())
        self.db.add(obj)
        await self.db.flush()
        return obj

    async def set_default(self, portfolio_id: int, user_id: int):
        # 先取消其他默认
        portfolios = await self.get_list_by_user(user_id)
        for p in portfolios:
            p.is_default = 0
        
        # 设置当前默认
        portfolio = await self.get_data(portfolio_id)
        if portfolio:
            portfolio.is_default = 1
        await self.db.flush()
```

**Step 2: 编写持仓CRUD**

```python
from typing import List, Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from core.crud import DalBase
from apps.admin.portfolio import models, schemas


class PositionDal(DalBase):
    
    def __init__(self, db: AsyncSession):
        super().__init__()
        self.db = db
        self.model = models.PortfolioPosition
        self.schema = schemas.PositionOut

    async def get_by_portfolio(self, portfolio_id: int) -> List[models.PortfolioPosition]:
        sql = select(self.model).where(
            and_(
                self.model.portfolio_id == portfolio_id,
                self.model.is_delete == False
            )
        ).order_by(self.model.market_value.desc())
        
        result = await self.db.scalars(sql)
        return result.all()

    async def get_by_stock(self, portfolio_id: int, stock_code: str) -> Optional[models.PortfolioPosition]:
        sql = select(self.model).where(
            and_(
                self.model.portfolio_id == portfolio_id,
                self.model.stock_code == stock_code,
                self.model.is_delete == False
            )
        )
        result = await self.db.scalars(sql)
        return result.first()

    async def add_position(self, portfolio_id: int, data: schemas.PositionCreate) -> models.PortfolioPosition:
        obj = self.model(portfolio_id=portfolio_id, **data.model_dump())
        self.db.add(obj)
        await self.db.flush()
        return obj

    async def update_position(self, position: models.PortfolioPosition, shares: int, cost_price: float):
        old_shares = position.shares
        old_cost = position.cost_price
        
        # 更新持仓和成本
        total_cost = old_shares * old_cost + shares * cost_price
        total_shares = old_shares + shares
        
        position.shares = total_shares
        position.cost_price = total_cost / total_shares
        await self.db.flush()
```

**Step 3: 更新 crud/__init__.py**

```python
from .portfolio_crud import PortfolioDal
from .position_crud import PositionDal

__all__ = ['PortfolioDal', 'PositionDal']
```

**Step 4: 提交**

```bash
git add backend/apps/admin/portfolio/crud/
git commit -m "feat(portfolio): add CRUD operations"
```

---

### Task 1.7: 创建API视图

**Files:**
- Create: `backend/apps/admin/portfolio/views.py`

**Step 1: 编写API视图**

```python
from typing import Optional
from fastapi import APIRouter, Depends, Query
from utils.response import SuccessResponse, ErrorResponse
from apps.admin.auth.utils.current import AllUserAuth, Auth
from . import schemas, crud

router = APIRouter()


# ==================== 组合管理 ====================

@router.get("", summary="获取用户组合列表")
async def get_portfolios(auth: Auth = Depends(AllUserAuth())):
    dal = crud.PortfolioDal(auth.db)
    items = await dal.get_list_by_user(auth.user.id)
    datas = [schemas.PortfolioOut.model_validate(i).model_dump() for i in items]
    return SuccessResponse(datas, count=len(datas))


@router.get("/{portfolio_id}", summary="获取组合详情")
async def get_portfolio(portfolio_id: int, auth: Auth = Depends(AllUserAuth())):
    dal = crud.PortfolioDal(auth.db)
    portfolio = await dal.get_data(portfolio_id)
    if not portfolio:
        return ErrorResponse("组合不存在")
    return SuccessResponse(schemas.PortfolioOut.model_validate(portfolio).model_dump())


@router.post("", summary="创建组合")
async def create_portfolio(data: schemas.PortfolioCreate, auth: Auth = Depends(AllUserAuth())):
    dal = crud.PortfolioDal(auth.db)
    portfolio = await dal.create_portfolio(data, auth.user.id)
    return SuccessResponse(schemas.PortfolioOut.model_validate(portfolio).model_dump())


@router.put("/{portfolio_id}", summary="更新组合")
async def update_portfolio(portfolio_id: int, data: schemas.PortfolioUpdate, auth: Auth = Depends(AllUserAuth())):
    dal = crud.PortfolioDal(auth.db)
    portfolio = await dal.put_data(portfolio_id, data)
    return SuccessResponse(schemas.PortfolioOut.model_validate(portfolio).model_dump())


@router.delete("/{portfolio_id}", summary="删除组合")
async def delete_portfolio(portfolio_id: int, auth: Auth = Depends(AllUserAuth())):
    dal = crud.PortfolioDal(auth.db)
    await dal.delete_datas([portfolio_id], v_soft=False)
    return SuccessResponse("删除成功")


@router.put("/{portfolio_id}/default", summary="设置为默认组合")
async def set_default_portfolio(portfolio_id: int, auth: Auth = Depends(AllUserAuth())):
    dal = crud.PortfolioDal(auth.db)
    await dal.set_default(portfolio_id, auth.user.id)
    return SuccessResponse("设置成功")


# ==================== 持仓管理 ====================

@router.get("/position/{portfolio_id}", summary="获取持仓列表")
async def get_positions(portfolio_id: int, auth: Auth = Depends(AllUserAuth())):
    dal = crud.PositionDal(auth.db)
    items = await dal.get_by_portfolio(portfolio_id)
    datas = [schemas.PositionOut.model_validate(i).model_dump() for i in items]
    return SuccessResponse(datas, count=len(datas))


@router.post("/position/{portfolio_id}", summary="添加持仓")
async def add_position(portfolio_id: int, data: schemas.PositionCreate, auth: Auth = Depends(AllUserAuth())):
    dal = crud.PositionDal(auth.db)
    position = await dal.add_position(portfolio_id, data)
    return SuccessResponse(schemas.PositionOut.model_validate(position).model_dump())


@router.delete("/position/{portfolio_id}/{stock_code}", summary="删除持仓")
async def delete_position(portfolio_id: int, stock_code: str, auth: Auth = Depends(AllUserAuth())):
    dal = crud.PositionDal(auth.db)
    position = await dal.get_by_stock(portfolio_id, stock_code)
    if position:
        await dal.delete_datas([position.id], v_soft=False)
    return SuccessResponse("删除成功")


# ==================== 交易记录 ====================

@router.post("/trade/{portfolio_id}/buy", summary="记录买入")
async def record_buy(portfolio_id: int, data: schemas.TradeBuy, auth: Auth = Depends(AllUserAuth())):
    # TODO: 实现买入记录逻辑
    pass


@router.post("/trade/{portfolio_id}/sell", summary="记录卖出")
async def record_sell(portfolio_id: int, data: schemas.TradeSell, auth: Auth = Depends(AllUserAuth())):
    # TODO: 实现卖出记录逻辑
    pass
```

**Step 2: 更新 portfolio/__init__.py**

```python
from . import models, schemas, crud
from .views import router

__all__ = ['models', 'schemas', 'crud', 'router']
```

**Step 3: 注册路由到 stock/api.py**

在 `backend/apps/admin/stock/api.py` 中添加：

```python
from apps.admin.portfolio import router as portfolio_router
# ...
router.include_router(portfolio_router, prefix="/portfolio", tags=["投资组合"])
```

**Step 4: 提交**

```bash
git add backend/apps/admin/portfolio/
git commit -m "feat(portfolio): add API views and register routes"
```

---

## Phase 2-7: 后续任务概要

### Phase 2: 持仓服务与交易服务（2天）

- Task 2.1: 创建持仓服务 `services/position_service.py`
- Task 2.2: 创建交易服务 `services/trade_service.py`
- Task 2.3: 完善买入/卖出API端点

### Phase 3: 分析服务（2天）

- Task 3.1: 创建分析服务 `services/analysis_service.py`
- Task 3.2: 添加业绩指标计算
- Task 3.3: 添加归因分析
- Task 3.4: 添加基准对比

### Phase 4: 风控服务（2天）

- Task 4.1: 创建风控服务 `services/risk_service.py`
- Task 4.2: 实现仓位检查
- Task 4.3: 实现回撤预警
- Task 4.4: 实现再平衡建议

### Phase 5: 前端页面开发（3天）

- Task 5.1: 创建前端目录结构
- Task 5.2: 创建主页面 Portfolio.vue
- Task 5.3: 创建持仓表格组件
- Task 5.4: 创建交易弹窗组件
- Task 5.5: 创建分析面板组件

### Phase 6: 模块联动（1天）

- Task 6.1: 实现与自选股联动
- Task 6.2: 实现与投资日历联动
- Task 6.3: 实现与AI分析联动

### Phase 7: 测试与优化（1天）

- Task 7.1: 编写后端单元测试
- Task 7.2: 性能优化
- Task 7.3: 文档完善

---

## 文件清单汇总

### 后端文件
```
backend/apps/admin/portfolio/
├── __init__.py
├── views.py
├── models/
│   ├── __init__.py
│   ├── portfolio.py
│   ├── portfolio_position.py
│   ├── portfolio_trade.py
│   ├── portfolio_risk_alert.py
│   └── portfolio_snapshot.py
├── schemas/
│   ├── __init__.py
│   ├── portfolio.py
│   ├── position.py
│   └── trade.py
├── params/
│   └── __init__.py
├── crud/
│   ├── __init__.py
│   ├── portfolio_crud.py
│   └── position_crud.py
└── services/
    ├── __init__.py
    ├── position_service.py
    ├── trade_service.py
    ├── analysis_service.py
    └── risk_service.py
```

### 前端文件
```
frontend/src/views/Vadmin/Stock/Portfolio/
├── Portfolio.vue
├── components/
│   ├── PortfolioCard.vue
│   ├── PositionTable.vue
│   ├── TradeRecord.vue
│   ├── TradeDialog.vue
│   ├── AnalysisPanel.vue
│   ├── RiskAlertPanel.vue
│   └── SettingsDialog.vue
├── composables/
│   ├── usePortfolio.ts
│   ├── usePosition.ts
│   └── useAnalysis.ts
└── types/
    └── portfolio.ts

frontend/src/api/
└── portfolio.ts
```

---

**文档版本**: v1.0
**创建日期**: 2026-03-22
**预估工期**: 13个工作日