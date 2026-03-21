# 投资日历功能实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 构建一个综合规划型投资日历模块，支持个股事件管理、AI分析、智能提醒和模块联动。

**Architecture:** 采用前后端分离架构，后端基于FastAPI+SQLAlchemy提供REST API，数据通过AkShare定时采集，AI分析调用用户提供的模型API，前端使用Vue3+Element Plus实现多视图日历展示。

**Tech Stack:** FastAPI, SQLAlchemy 2.0, MySQL, AkShare, Vue 3, Element Plus, TypeScript, ECharts

---

## Phase 1: 数据模型与基础API（2天）

### Task 1.1: 创建后端模块目录结构

**Files:**
- Create: `backend/apps/admin/stock_calendar/__init__.py`
- Create: `backend/apps/admin/stock_calendar/models/__init__.py`
- Create: `backend/apps/admin/stock_calendar/schemas/__init__.py`
- Create: `backend/apps/admin/stock_calendar/params/__init__.py`
- Create: `backend/apps/admin/stock_calendar/crud/__init__.py`
- Create: `backend/apps/admin/stock_calendar/services/__init__.py`

**Step 1: 创建目录和初始化文件**

```bash
mkdir -p backend/apps/admin/stock_calendar/models
mkdir -p backend/apps/admin/stock_calendar/schemas
mkdir -p backend/apps/admin/stock_calendar/params
mkdir -p backend/apps/admin/stock_calendar/crud
mkdir -p backend/apps/admin/stock_calendar/services
touch backend/apps/admin/stock_calendar/__init__.py
touch backend/apps/admin/stock_calendar/models/__init__.py
touch backend/apps/admin/stock_calendar/schemas/__init__.py
touch backend/apps/admin/stock_calendar/params/__init__.py
touch backend/apps/admin/stock_calendar/crud/__init__.py
touch backend/apps/admin/stock_calendar/services/__init__.py
```

**Step 2: 验证目录结构**

Run: `ls -la backend/apps/admin/stock_calendar/`
Expected: 看到 models, schemas, params, crud, services 目录

**Step 3: Commit**

```bash
git add backend/apps/admin/stock_calendar/
git commit -m "feat(stock_calendar): init module directory structure"
```

---

### Task 1.2: 创建个股事件数据模型

**Files:**
- Create: `backend/apps/admin/stock_calendar/models/stock_calendar_event.py`

**Step 1: 编写数据模型**

```python
# backend/apps/admin/stock_calendar/models/stock_calendar_event.py
from sqlalchemy import Column, BigInteger, String, Date, Time, Text, JSON, DECIMAL, SmallInteger, DateTime, Index
from sqlalchemy.sql import func
from application.db.models_base import Base


class StockCalendarEvent(Base):
    """个股日历事件表"""
    __tablename__ = 'stock_calendar_event'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='主键ID')
    
    # 股票信息
    stock_code = Column(String(20), nullable=False, index=True, comment='股票代码')
    stock_name = Column(String(100), comment='股票名称')
    
    # 事件信息
    event_type = Column(String(50), nullable=False, index=True, comment='事件类型')
    event_date = Column(Date, nullable=False, index=True, comment='事件日期')
    event_time = Column(Time, comment='事件时间')
    title = Column(String(500), nullable=False, comment='事件标题')
    content = Column(Text, comment='事件详情')
    
    # 事件影响数据
    impact_data = Column(JSON, comment='事件影响数据JSON')
    
    # AI分析结果
    ai_impact_score = Column(DECIMAL(5, 2), comment='影响评分 -5~5')
    ai_sentiment = Column(SmallInteger, comment='情感: 1-利好 2-中性 3-利空')
    ai_analysis = Column(Text, comment='AI影响分析')
    ai_suggestion = Column(Text, comment='AI操作建议')
    
    # 辅助字段
    is_in_watchlist = Column(SmallInteger, default=0, index=True, comment='是否在用户自选股中')
    data_source = Column(String(50), default='akshare', comment='数据来源')
    source_url = Column(String(500), comment='来源链接')
    
    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')
    
    __table_args__ = (
        Index('idx_date_type', 'event_date', 'event_type'),
        {'comment': '个股日历事件表'}
    )
```

**Step 2: 在 models/__init__.py 中导出**

```python
# backend/apps/admin/stock_calendar/models/__init__.py
from .stock_calendar_event import StockCalendarEvent

__all__ = ['StockCalendarEvent']
```

**Step 3: Commit**

```bash
git add backend/apps/admin/stock_calendar/models/
git commit -m "feat(stock_calendar): add StockCalendarEvent model"
```

---

### Task 1.3: 创建用户提醒数据模型

**Files:**
- Create: `backend/apps/admin/stock_calendar/models/stock_event_reminder.py`

**Step 1: 编写数据模型**

```python
# backend/apps/admin/stock_calendar/models/stock_event_reminder.py
from sqlalchemy import Column, BigInteger, String, SmallInteger, Integer, Time, DateTime, UniqueConstraint, Index
from sqlalchemy.sql import func
from application.db.models_base import Base


class StockEventReminder(Base):
    """用户事件提醒表"""
    __tablename__ = 'stock_event_reminder'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='主键ID')
    user_id = Column(BigInteger, nullable=False, index=True, comment='用户ID')
    stock_code = Column(String(20), nullable=False, comment='股票代码')
    event_id = Column(BigInteger, nullable=False, comment='事件ID')
    
    remind_days = Column(Integer, default=1, comment='提前几天提醒: 1-7')
    remind_time = Column(Time, default='09:00:00', comment='提醒时间')
    remind_type = Column(String(20), default='system', comment='提醒方式: system/email')
    is_active = Column(SmallInteger, default=1, index=True, comment='是否启用')
    
    last_remind_at = Column(DateTime, comment='上次提醒时间')
    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')
    
    __table_args__ = (
        UniqueConstraint('user_id', 'stock_code', 'event_id', name='uk_user_stock_event'),
        Index('idx_user_active', 'user_id', 'is_active'),
        {'comment': '用户事件提醒表'}
    )
```

**Step 2: 更新 models/__init__.py**

```python
# backend/apps/admin/stock_calendar/models/__init__.py
from .stock_calendar_event import StockCalendarEvent
from .stock_event_reminder import StockEventReminder

__all__ = ['StockCalendarEvent', 'StockEventReminder']
```

**Step 3: Commit**

```bash
git add backend/apps/admin/stock_calendar/models/
git commit -m "feat(stock_calendar): add StockEventReminder model"
```

---

### Task 1.4: 创建宏观事件和板块机会数据模型

**Files:**
- Create: `backend/apps/admin/stock_calendar/models/invest_calendar_event.py`
- Create: `backend/apps/admin/stock_calendar/models/sector_rotation_opportunity.py`

**Step 1: 编写宏观事件模型**

```python
# backend/apps/admin/stock_calendar/models/invest_calendar_event.py
from sqlalchemy import Column, BigInteger, String, Date, Time, Text, JSON, SmallInteger, DateTime, Index
from sqlalchemy.sql import func
from application.db.models_base import Base


class InvestCalendarEvent(Base):
    """投资日历宏观事件表"""
    __tablename__ = 'invest_calendar_event'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    
    event_type = Column(String(50), nullable=False, index=True, comment='事件类型: macro/policy/meeting')
    title = Column(String(500), nullable=False, comment='事件标题')
    content = Column(Text, comment='事件详情')
    
    event_date = Column(Date, nullable=False, index=True, comment='事件日期')
    event_time = Column(Time, comment='事件时间')
    importance = Column(SmallInteger, default=2, index=True, comment='重要程度: 1-低 2-中 3-高')
    
    related_stocks = Column(JSON, comment='关联股票代码列表')
    related_sectors = Column(JSON, comment='关联板块列表')
    
    ai_analysis = Column(Text, comment='AI分析的事件影响')
    ai_sentiment = Column(SmallInteger, comment='AI情感: 1-利好 2-中性 3-利空')
    ai_suggestion = Column(Text, comment='AI投资建议')
    
    data_source = Column(String(50), default='akshare')
    source_url = Column(String(500))
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        Index('idx_date_type', 'event_date', 'event_type'),
        {'comment': '投资日历宏观事件表'}
    )
```

**Step 2: 编写板块机会模型**

```python
# backend/apps/admin/stock_calendar/models/sector_rotation_opportunity.py
from sqlalchemy import Column, BigInteger, String, Date, Text, JSON, SmallInteger, DECIMAL, DateTime
from sqlalchemy.sql import func
from application.db.models_base import Base


class SectorRotationOpportunity(Base):
    """板块轮动机会表"""
    __tablename__ = 'sector_rotation_opportunity'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    
    sector_name = Column(String(100), nullable=False, comment='板块名称')
    sector_code = Column(String(50), comment='板块代码')
    
    opportunity_type = Column(String(50), comment='机会类型: seasonal/policy/event')
    start_date = Column(Date, comment='机会开始日期')
    end_date = Column(Date, comment='机会结束日期')
    
    confidence_score = Column(DECIMAL(5, 2), comment='AI置信度评分 0-100')
    historical_return = Column(DECIMAL(10, 4), comment='历史平均收益率')
    win_rate = Column(DECIMAL(5, 2), comment='历史胜率')
    
    description = Column(Text, comment='机会描述')
    ai_analysis = Column(Text, comment='AI详细分析')
    related_stocks = Column(JSON, comment='相关个股列表')
    
    is_active = Column(SmallInteger, default=1, comment='是否有效')
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    __table_args__ = {'comment': '板块轮动机会表'}
```

**Step 3: 更新 models/__init__.py**

```python
# backend/apps/admin/stock_calendar/models/__init__.py
from .stock_calendar_event import StockCalendarEvent
from .stock_event_reminder import StockEventReminder
from .invest_calendar_event import InvestCalendarEvent
from .sector_rotation_opportunity import SectorRotationOpportunity

__all__ = [
    'StockCalendarEvent',
    'StockEventReminder', 
    'InvestCalendarEvent',
    'SectorRotationOpportunity'
]
```

**Step 4: Commit**

```bash
git add backend/apps/admin/stock_calendar/models/
git commit -m "feat(stock_calendar): add InvestCalendarEvent and SectorRotationOpportunity models"
```

---

### Task 1.5: 创建Pydantic Schema定义

**Files:**
- Create: `backend/apps/admin/stock_calendar/schemas/event.py`
- Create: `backend/apps/admin/stock_calendar/schemas/reminder.py`

**Step 1: 编写事件Schema**

```python
# backend/apps/admin/stock_calendar/schemas/event.py
from datetime import date, time, datetime
from typing import Optional, List, Any
from pydantic import BaseModel, Field


class StockCalendarEventBase(BaseModel):
    stock_code: str = Field(..., description='股票代码')
    stock_name: Optional[str] = Field(None, description='股票名称')
    event_type: str = Field(..., description='事件类型')
    event_date: date = Field(..., description='事件日期')
    event_time: Optional[time] = Field(None, description='事件时间')
    title: str = Field(..., description='事件标题')
    content: Optional[str] = Field(None, description='事件详情')
    impact_data: Optional[dict] = Field(None, description='事件影响数据')


class StockCalendarEventCreate(StockCalendarEventBase):
    data_source: str = Field(default='manual', description='数据来源')


class StockCalendarEventUpdate(BaseModel):
    stock_name: Optional[str] = None
    event_time: Optional[time] = None
    title: Optional[str] = None
    content: Optional[str] = None
    impact_data: Optional[dict] = None
    ai_impact_score: Optional[float] = None
    ai_sentiment: Optional[int] = None
    ai_analysis: Optional[str] = None
    ai_suggestion: Optional[str] = None


class StockCalendarEventOut(StockCalendarEventBase):
    id: int
    ai_impact_score: Optional[float] = None
    ai_sentiment: Optional[int] = None
    ai_analysis: Optional[str] = None
    ai_suggestion: Optional[str] = None
    is_in_watchlist: int = 0
    data_source: str
    source_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class StockCalendarEventListOut(BaseModel):
    total: int
    items: List[StockCalendarEventOut]
```

**Step 2: 编写提醒Schema**

```python
# backend/apps/admin/stock_calendar/schemas/reminder.py
from datetime import time, datetime
from typing import Optional
from pydantic import BaseModel, Field


class StockEventReminderBase(BaseModel):
    stock_code: str = Field(..., description='股票代码')
    event_id: int = Field(..., description='事件ID')
    remind_days: int = Field(default=1, ge=1, le=7, description='提前几天提醒')
    remind_time: time = Field(default=time(9, 0), description='提醒时间')
    remind_type: str = Field(default='system', description='提醒方式')


class StockEventReminderCreate(StockEventReminderBase):
    user_id: int = Field(..., description='用户ID')


class StockEventReminderUpdate(BaseModel):
    remind_days: Optional[int] = Field(None, ge=1, le=7)
    remind_time: Optional[time] = None
    remind_type: Optional[str] = None
    is_active: Optional[int] = None


class StockEventReminderOut(StockEventReminderBase):
    id: int
    user_id: int
    stock_name: Optional[str] = None
    event_title: Optional[str] = None
    event_date: Optional[str] = None
    is_active: int
    last_remind_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class StockEventReminderListOut(BaseModel):
    total: int
    items: list[StockEventReminderOut]
```

**Step 3: 更新 schemas/__init__.py**

```python
# backend/apps/admin/stock_calendar/schemas/__init__.py
from .event import (
    StockCalendarEventCreate,
    StockCalendarEventUpdate,
    StockCalendarEventOut,
    StockCalendarEventListOut
)
from .reminder import (
    StockEventReminderCreate,
    StockEventReminderUpdate,
    StockEventReminderOut,
    StockEventReminderListOut
)

__all__ = [
    'StockCalendarEventCreate',
    'StockCalendarEventUpdate',
    'StockCalendarEventOut',
    'StockCalendarEventListOut',
    'StockEventReminderCreate',
    'StockEventReminderUpdate',
    'StockEventReminderOut',
    'StockEventReminderListOut'
]
```

**Step 4: Commit**

```bash
git add backend/apps/admin/stock_calendar/schemas/
git commit -m "feat(stock_calendar): add Pydantic schemas for event and reminder"
```

---

### Task 1.6: 创建查询参数定义

**Files:**
- Create: `backend/apps/admin/stock_calendar/params/event_params.py`

**Step 1: 编写查询参数**

```python
# backend/apps/admin/stock_calendar/params/event_params.py
from datetime import date
from typing import Optional
from pydantic import BaseModel, Field


class StockCalendarEventParams(BaseModel):
    """事件查询参数"""
    start_date: Optional[date] = Field(None, description='开始日期')
    end_date: Optional[date] = Field(None, description='结束日期')
    stock_code: Optional[str] = Field(None, description='股票代码')
    event_type: Optional[str] = Field(None, description='事件类型')
    is_watchlist: Optional[int] = Field(None, description='是否仅自选股')
    page: int = Field(default=1, ge=1, description='页码')
    page_size: int = Field(default=20, ge=1, le=100, description='每页数量')


class InvestCalendarEventParams(BaseModel):
    """宏观事件查询参数"""
    start_date: Optional[date] = Field(None, description='开始日期')
    end_date: Optional[date] = Field(None, description='结束日期')
    event_type: Optional[str] = Field(None, description='事件类型')
    importance: Optional[int] = Field(None, ge=1, le=3, description='重要程度')
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
```

**Step 2: 更新 params/__init__.py**

```python
# backend/apps/admin/stock_calendar/params/__init__.py
from .event_params import StockCalendarEventParams, InvestCalendarEventParams

__all__ = ['StockCalendarEventParams', 'InvestCalendarEventParams']
```

**Step 3: Commit**

```bash
git add backend/apps/admin/stock_calendar/params/
git commit -m "feat(stock_calendar): add query params"
```

---

### Task 1.7: 创建CRUD操作

**Files:**
- Create: `backend/apps/admin/stock_calendar/crud/event_crud.py`
- Create: `backend/apps/admin/stock_calendar/crud/reminder_crud.py`

**Step 1: 编写事件CRUD**

```python
# backend/apps/admin/stock_calendar/crud/event_crud.py
from datetime import date, timedelta
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from ..models.stock_calendar_event import StockCalendarEvent
from ..params.event_params import StockCalendarEventParams
from ..schemas.event import StockCalendarEventCreate, StockCalendarEventUpdate


class EventCRUD:
    """事件CRUD操作"""
    
    @staticmethod
    def get_list(db: Session, params: StockCalendarEventParams) -> tuple[int, List[StockCalendarEvent]]:
        """获取事件列表"""
        query = db.query(StockCalendarEvent)
        
        if params.start_date:
            query = query.filter(StockCalendarEvent.event_date >= params.start_date)
        if params.end_date:
            query = query.filter(StockCalendarEvent.event_date <= params.end_date)
        if params.stock_code:
            query = query.filter(StockCalendarEvent.stock_code == params.stock_code)
        if params.event_type:
            query = query.filter(StockCalendarEvent.event_type == params.event_type)
        if params.is_watchlist:
            query = query.filter(StockCalendarEvent.is_in_watchlist == 1)
        
        total = query.count()
        items = query.order_by(StockCalendarEvent.event_date.asc()) \
            .offset((params.page - 1) * params.page_size) \
            .limit(params.page_size) \
            .all()
        
        return total, items
    
    @staticmethod
    def get_by_stock(db: Session, stock_code: str, days: int = 90) -> List[StockCalendarEvent]:
        """获取某股票的事件"""
        start_date = date.today()
        end_date = start_date + timedelta(days=days)
        
        return db.query(StockCalendarEvent).filter(
            and_(
                StockCalendarEvent.stock_code == stock_code,
                StockCalendarEvent.event_date >= start_date,
                StockCalendarEvent.event_date <= end_date
            )
        ).order_by(StockCalendarEvent.event_date.asc()).all()
    
    @staticmethod
    def get_by_date(db: Session, event_date: date) -> List[StockCalendarEvent]:
        """获取某日期的事件"""
        return db.query(StockCalendarEvent).filter(
            StockCalendarEvent.event_date == event_date
        ).order_by(StockCalendarEvent.event_time.asc()).all()
    
    @staticmethod
    def get_by_id(db: Session, event_id: int) -> Optional[StockCalendarEvent]:
        """获取单个事件"""
        return db.query(StockCalendarEvent).filter(StockCalendarEvent.id == event_id).first()
    
    @staticmethod
    def create(db: Session, event: StockCalendarEventCreate) -> StockCalendarEvent:
        """创建事件"""
        db_event = StockCalendarEvent(**event.model_dump())
        db.add(db_event)
        db.commit()
        db.refresh(db_event)
        return db_event
    
    @staticmethod
    def update(db: Session, event_id: int, event: StockCalendarEventUpdate) -> Optional[StockCalendarEvent]:
        """更新事件"""
        db_event = EventCRUD.get_by_id(db, event_id)
        if db_event:
            update_data = event.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_event, key, value)
            db.commit()
            db.refresh(db_event)
        return db_event
    
    @staticmethod
    def delete(db: Session, event_id: int) -> bool:
        """删除事件"""
        db_event = EventCRUD.get_by_id(db, event_id)
        if db_event:
            db.delete(db_event)
            db.commit()
            return True
        return False
```

**Step 2: 编写提醒CRUD**

```python
# backend/apps/admin/stock_calendar/crud/reminder_crud.py
from typing import List, Optional
from sqlalchemy.orm import Session
from ..models.stock_event_reminder import StockEventReminder
from ..schemas.reminder import StockEventReminderCreate, StockEventReminderUpdate


class ReminderCRUD:
    """提醒CRUD操作"""
    
    @staticmethod
    def get_list(db: Session, user_id: int, is_active: Optional[int] = None) -> List[StockEventReminder]:
        """获取用户提醒列表"""
        query = db.query(StockEventReminder).filter(StockEventReminder.user_id == user_id)
        if is_active is not None:
            query = query.filter(StockEventReminder.is_active == is_active)
        return query.order_by(StockEventReminder.created_at.desc()).all()
    
    @staticmethod
    def get_by_id(db: Session, reminder_id: int) -> Optional[StockEventReminder]:
        """获取单个提醒"""
        return db.query(StockEventReminder).filter(StockEventReminder.id == reminder_id).first()
    
    @staticmethod
    def create(db: Session, reminder: StockEventReminderCreate) -> StockEventReminder:
        """创建提醒"""
        db_reminder = StockEventReminder(**reminder.model_dump())
        db.add(db_reminder)
        db.commit()
        db.refresh(db_reminder)
        return db_reminder
    
    @staticmethod
    def update(db: Session, reminder_id: int, reminder: StockEventReminderUpdate) -> Optional[StockEventReminder]:
        """更新提醒"""
        db_reminder = ReminderCRUD.get_by_id(db, reminder_id)
        if db_reminder:
            update_data = reminder.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_reminder, key, value)
            db.commit()
            db.refresh(db_reminder)
        return db_reminder
    
    @staticmethod
    def delete(db: Session, reminder_id: int) -> bool:
        """删除提醒"""
        db_reminder = ReminderCRUD.get_by_id(db, reminder_id)
        if db_reminder:
            db.delete(db_reminder)
            db.commit()
            return True
        return False
    
    @staticmethod
    def get_active_reminders(db: Session) -> List[StockEventReminder]:
        """获取所有启用的提醒"""
        return db.query(StockEventReminder).filter(
            StockEventReminder.is_active == 1
        ).all()
```

**Step 3: 更新 crud/__init__.py**

```python
# backend/apps/admin/stock_calendar/crud/__init__.py
from .event_crud import EventCRUD
from .reminder_crud import ReminderCRUD

__all__ = ['EventCRUD', 'ReminderCRUD']
```

**Step 4: Commit**

```bash
git add backend/apps/admin/stock_calendar/crud/
git commit -m "feat(stock_calendar): add CRUD operations"
```

---

### Task 1.8: 创建API视图

**Files:**
- Create: `backend/apps/admin/stock_calendar/views.py`

**Step 1: 编写API视图**

```python
# backend/apps/admin/stock_calendar/views.py
from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from application.db.session import get_db
from . import models, schemas, params, crud

router = APIRouter(prefix='/stock_calendar', tags=['投资日历'])


# ==================== 事件管理 ====================

@router.get('/events', response_model=schemas.StockCalendarEventListOut)
async def get_events(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    stock_code: Optional[str] = None,
    event_type: Optional[str] = None,
    is_watchlist: Optional[int] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """获取事件列表"""
    query_params = params.StockCalendarEventParams(
        start_date=start_date,
        end_date=end_date,
        stock_code=stock_code,
        event_type=event_type,
        is_watchlist=is_watchlist,
        page=page,
        page_size=page_size
    )
    total, items = crud.EventCRUD.get_list(db, query_params)
    return {'total': total, 'items': items}


@router.get('/events/{event_id}', response_model=schemas.StockCalendarEventOut)
async def get_event(event_id: int, db: Session = Depends(get_db)):
    """获取事件详情"""
    event = crud.EventCRUD.get_by_id(db, event_id)
    if not event:
        return {'code': 404, 'message': '事件不存在'}
    return event


@router.get('/events/by_stock/{stock_code}', response_model=schemas.StockCalendarEventListOut)
async def get_events_by_stock(
    stock_code: str,
    days: int = Query(90, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """获取某股票的所有事件"""
    items = crud.EventCRUD.get_by_stock(db, stock_code, days)
    return {'total': len(items), 'items': items}


@router.get('/events/by_date/{event_date}', response_model=schemas.StockCalendarEventListOut)
async def get_events_by_date(event_date: date, db: Session = Depends(get_db)):
    """获取某日期的所有事件"""
    items = crud.EventCRUD.get_by_date(db, event_date)
    return {'total': len(items), 'items': items}


@router.post('/events', response_model=schemas.StockCalendarEventOut)
async def create_event(event: schemas.StockCalendarEventCreate, db: Session = Depends(get_db)):
    """添加自定义事件"""
    return crud.EventCRUD.create(db, event)


# ==================== 提醒管理 ====================

@router.get('/reminders', response_model=schemas.StockEventReminderListOut)
async def get_reminders(
    user_id: int = Query(..., description='用户ID'),
    is_active: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """获取用户提醒列表"""
    items = crud.ReminderCRUD.get_list(db, user_id, is_active)
    return {'total': len(items), 'items': items}


@router.post('/reminders', response_model=schemas.StockEventReminderOut)
async def create_reminder(reminder: schemas.StockEventReminderCreate, db: Session = Depends(get_db)):
    """创建提醒"""
    return crud.ReminderCRUD.create(db, reminder)


@router.put('/reminders/{reminder_id}', response_model=schemas.StockEventReminderOut)
async def update_reminder(
    reminder_id: int,
    reminder: schemas.StockEventReminderUpdate,
    db: Session = Depends(get_db)
):
    """更新提醒"""
    result = crud.ReminderCRUD.update(db, reminder_id, reminder)
    if not result:
        return {'code': 404, 'message': '提醒不存在'}
    return result


@router.delete('/reminders/{reminder_id}')
async def delete_reminder(reminder_id: int, db: Session = Depends(get_db)):
    """删除提醒"""
    success = crud.ReminderCRUD.delete(db, reminder_id)
    if not success:
        return {'code': 404, 'message': '提醒不存在'}
    return {'code': 200, 'message': '删除成功'}
```

**Step 2: Commit**

```bash
git add backend/apps/admin/stock_calendar/views.py
git commit -m "feat(stock_calendar): add API views"
```

---

### Task 1.9: 注册路由和模型

**Files:**
- Modify: `backend/apps/admin/__init__.py` (注册路由)
- Modify: `backend/application/db/models.py` (导入模型)

**Step 1: 注册路由**

在 `backend/apps/admin/__init__.py` 中添加：

```python
# 在 router 列表中添加
from .stock_calendar.views import router as stock_calendar_router
# ...
app.include_router(stock_calendar_router, prefix='/api')
```

**Step 2: 导入模型**

在 `backend/application/db/models.py` 中添加：

```python
# 导入新模型
from apps.admin.stock_calendar.models import (
    StockCalendarEvent,
    StockEventReminder,
    InvestCalendarEvent,
    SectorRotationOpportunity
)
```

**Step 3: 执行数据库迁移**

```bash
cd backend
uv run python main.py migrate
```

**Step 4: Commit**

```bash
git add backend/apps/admin/__init__.py backend/application/db/models.py
git commit -m "feat(stock_calendar): register routes and models"
```

---

## Phase 2: 数据采集服务（2天）

### Task 2.1: 创建数据同步服务

**Files:**
- Create: `backend/apps/admin/stock_calendar/services/data_sync_service.py`

**Step 1: 编写数据同步服务**

```python
# backend/apps/admin/stock_calendar/services/data_sync_service.py
import logging
from datetime import datetime, timedelta
from typing import List, Optional
import akshare as ak
from sqlalchemy.orm import Session
from ..models.stock_calendar_event import StockCalendarEvent

logger = logging.getLogger(__name__)


class CalendarDataSyncService:
    """投资日历数据同步服务"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def sync_earnings_calendar(self, days: int = 90) -> int:
        """同步财报日历
        
        Args:
            days: 同步未来多少天的数据
            
        Returns:
            同步的事件数量
        """
        try:
            start_date = datetime.now().strftime('%Y%m%d')
            end_date = (datetime.now() + timedelta(days=days)).strftime('%Y%m%d')
            
            logger.info(f"开始同步财报日历: {start_date} - {end_date}")
            
            df = ak.stock_financial_report_calendar(
                start_date=start_date,
                end_date=end_date
            )
            
            if df.empty:
                logger.warning("财报日历数据为空")
                return 0
            
            count = 0
            for _, row in df.iterrows():
                try:
                    # 解析数据
                    stock_code = str(row.get('股票代码', '')).zfill(6)
                    stock_name = row.get('股票简称', '')
                    report_date = row.get('实际公告日期') or row.get('预约公告日期')
                    report_period = row.get('报告期', '')
                    
                    if not stock_code or not report_date:
                        continue
                    
                    # 检查是否已存在
                    existing = self.db.query(StockCalendarEvent).filter(
                        StockCalendarEvent.stock_code == stock_code,
                        StockCalendarEvent.event_type == 'earnings_report',
                        StockCalendarEvent.event_date == report_date
                    ).first()
                    
                    if existing:
                        continue
                    
                    # 创建事件
                    event = StockCalendarEvent(
                        stock_code=stock_code,
                        stock_name=stock_name,
                        event_type='earnings_report',
                        event_date=report_date,
                        title=f"{stock_name} {report_period}财报发布",
                        content=f"报告期: {report_period}",
                        impact_data={'report_period': report_period},
                        data_source='akshare'
                    )
                    self.db.add(event)
                    count += 1
                    
                except Exception as e:
                    logger.error(f"处理财报事件失败: {e}")
                    continue
            
            self.db.commit()
            logger.info(f"财报日历同步完成，新增 {count} 条记录")
            return count
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"同步财报日历失败: {e}")
            raise
    
    def sync_dividend_calendar(self) -> int:
        """同步分红除权日历"""
        # TODO: 实现分红数据同步
        pass
    
    def sync_unlock_calendar(self) -> int:
        """同步解禁日历"""
        # TODO: 实现解禁数据同步
        pass
    
    def sync_all(self) -> dict:
        """全量同步"""
        results = {}
        try:
            results['earnings'] = self.sync_earnings_calendar()
        except Exception as e:
            results['earnings_error'] = str(e)
        
        return results
```

**Step 2: 更新 services/__init__.py**

```python
# backend/apps/admin/stock_calendar/services/__init__.py
from .data_sync_service import CalendarDataSyncService

__all__ = ['CalendarDataSyncService']
```

**Step 3: Commit**

```bash
git add backend/apps/admin/stock_calendar/services/
git commit -m "feat(stock_calendar): add data sync service"
```

---

### Task 2.2: 创建数据同步API

**Files:**
- Modify: `backend/apps/admin/stock_calendar/views.py`

**Step 1: 添加同步API**

在 `views.py` 中添加：

```python
from .services import CalendarDataSyncService

# ==================== 数据同步 ====================

@router.post('/sync/earnings')
async def sync_earnings(db: Session = Depends(get_db)):
    """同步财报日历"""
    service = CalendarDataSyncService(db)
    count = service.sync_earnings_calendar()
    return {'code': 200, 'message': f'同步成功，新增 {count} 条记录'}


@router.post('/sync/dividends')
async def sync_dividends(db: Session = Depends(get_db)):
    """同步分红除权"""
    service = CalendarDataSyncService(db)
    count = service.sync_dividend_calendar()
    return {'code': 200, 'message': f'同步成功，新增 {count} 条记录'}


@router.post('/sync/unlocks')
async def sync_unlocks(db: Session = Depends(get_db)):
    """同步解禁日"""
    service = CalendarDataSyncService(db)
    count = service.sync_unlock_calendar()
    return {'code': 200, 'message': f'同步成功，新增 {count} 条记录'}


@router.post('/sync/all')
async def sync_all(db: Session = Depends(get_db)):
    """全量同步"""
    service = CalendarDataSyncService(db)
    results = service.sync_all()
    return {'code': 200, 'data': results}
```

**Step 2: Commit**

```bash
git add backend/apps/admin/stock_calendar/views.py
git commit -m "feat(stock_calendar): add sync API endpoints"
```

---

## Phase 3: 前端页面开发（3天）

### Task 3.1: 创建前端目录结构

**Files:**
- Create: `frontend/src/views/Vadmin/Stock/InvestCalendar/InvestCalendar.vue`
- Create: `frontend/src/api/stockCalendar.ts`
- Create: `frontend/src/views/Vadmin/Stock/InvestCalendar/types/calendar.ts`

**Step 1: 创建目录**

```bash
mkdir -p frontend/src/views/Vadmin/Stock/InvestCalendar/components
mkdir -p frontend/src/views/Vadmin/Stock/InvestCalendar/composables
mkdir -p frontend/src/views/Vadmin/Stock/InvestCalendar/types
```

**Step 2: 创建类型定义**

```typescript
// frontend/src/views/Vadmin/Stock/InvestCalendar/types/calendar.ts

/** 事件类型 */
export type EventType = 
  | 'earnings_report'
  | 'earnings_forecast'
  | 'dividend'
  | 'unlock'
  | 'shareholders_mtg'
  | 'ipo_listing'
  | 'rating_change'
  | 'block_trade'
  | 'repurchase'
  | 'major_news'

/** AI情感 */
export type AISentiment = 1 | 2 | 3 // 1-利好 2-中性 3-利空

/** 事件信息 */
export interface CalendarEvent {
  id: number
  stock_code: string
  stock_name: string | null
  event_type: EventType
  event_date: string
  event_time: string | null
  title: string
  content: string | null
  impact_data: Record<string, any> | null
  ai_impact_score: number | null
  ai_sentiment: AISentiment | null
  ai_analysis: string | null
  ai_suggestion: string | null
  is_in_watchlist: number
  data_source: string
  source_url: string | null
  created_at: string
  updated_at: string
}

/** 提醒信息 */
export interface EventReminder {
  id: number
  user_id: number
  stock_code: string
  event_id: number
  stock_name?: string
  event_title?: string
  event_date?: string
  remind_days: number
  remind_time: string
  remind_type: 'system' | 'email'
  is_active: number
  created_at: string
}

/** 事件类型映射 */
export const EVENT_TYPE_MAP: Record<EventType, { label: string; color: string }> = {
  earnings_report: { label: '财报发布', color: '#409EFF' },
  earnings_forecast: { label: '业绩预告', color: '#67C23A' },
  dividend: { label: '分红除权', color: '#E6A23C' },
  unlock: { label: '解禁日', color: '#F56C6C' },
  shareholders_mtg: { label: '股东大会', color: '#909399' },
  ipo_listing: { label: '新股上市', color: '#409EFF' },
  rating_change: { label: '评级变动', color: '#E6A23C' },
  block_trade: { label: '大宗交易', color: '#909399' },
  repurchase: { label: '股票回购', color: '#67C23A' },
  major_news: { label: '重要公告', color: '#F56C6C' }
}

/** AI情感映射 */
export const AI_SENTIMENT_MAP: Record<AISentiment, { label: string; color: string; icon: string }> = {
  1: { label: '利好', color: '#67C23A', icon: '↑' },
  2: { label: '中性', color: '#909399', icon: '→' },
  3: { label: '利空', color: '#F56C6C', icon: '↓' }
}
```

**Step 3: 创建API文件**

```typescript
// frontend/src/api/stockCalendar.ts
import request from '@/utils/request'

const API_PREFIX = '/stock_calendar'

/** 获取事件列表 */
export function getEventList(params: {
  start_date?: string
  end_date?: string
  stock_code?: string
  event_type?: string
  is_watchlist?: number
  page?: number
  page_size?: number
}) {
  return request.get(`${API_PREFIX}/events`, { params })
}

/** 获取事件详情 */
export function getEventDetail(eventId: number) {
  return request.get(`${API_PREFIX}/events/${eventId}`)
}

/** 获取某股票的事件 */
export function getEventsByStock(stockCode: string, days = 90) {
  return request.get(`${API_PREFIX}/events/by_stock/${stockCode}`, { params: { days } })
}

/** 获取某日期的事件 */
export function getEventsByDate(date: string) {
  return request.get(`${API_PREFIX}/events/by_date/${date}`)
}

/** 创建事件 */
export function createEvent(data: any) {
  return request.post(`${API_PREFIX}/events`, data)
}

/** 获取提醒列表 */
export function getReminderList(userId: number, isActive?: number) {
  return request.get(`${API_PREFIX}/reminders`, { params: { user_id: userId, is_active: isActive } })
}

/** 创建提醒 */
export function createReminder(data: {
  user_id: number
  stock_code: string
  event_id: number
  remind_days?: number
  remind_time?: string
  remind_type?: string
}) {
  return request.post(`${API_PREFIX}/reminders`, data)
}

/** 更新提醒 */
export function updateReminder(reminderId: number, data: any) {
  return request.put(`${API_PREFIX}/reminders/${reminderId}`, data)
}

/** 删除提醒 */
export function deleteReminder(reminderId: number) {
  return request.delete(`${API_PREFIX}/reminders/${reminderId}`)
}

/** 同步财报日历 */
export function syncEarnings() {
  return request.post(`${API_PREFIX}/sync/earnings`)
}

/** 全量同步 */
export function syncAll() {
  return request.post(`${API_PREFIX}/sync/all`)
}
```

**Step 4: Commit**

```bash
git add frontend/src/views/Vadmin/Stock/InvestCalendar/
git add frontend/src/api/stockCalendar.ts
git commit -m "feat(frontend): init invest calendar frontend structure"
```

---

### Task 3.2: 创建主页面组件

**Files:**
- Create: `frontend/src/views/Vadmin/Stock/InvestCalendar/InvestCalendar.vue`

**Step 1: 编写主页面**

```vue
<!-- frontend/src/views/Vadmin/Stock/InvestCalendar/InvestCalendar.vue -->
<template>
  <div class="invest-calendar">
    <!-- 顶部操作栏 -->
    <div class="calendar-header">
      <div class="header-left">
        <el-radio-group v-model="viewType" size="large">
          <el-radio-button label="month">月历</el-radio-button>
          <el-radio-button label="week">周历</el-radio-button>
          <el-radio-button label="timeline">时间线</el-radio-button>
        </el-radio-group>
        
        <div class="date-nav">
          <el-button @click="navigateDate(-1)" :icon="ArrowLeft" circle />
          <span class="current-date">{{ currentDateDisplay }}</span>
          <el-button @click="navigateDate(1)" :icon="ArrowRight" circle />
          <el-button @click="goToToday" type="primary" size="small">今天</el-button>
        </div>
      </div>
      
      <div class="header-right">
        <el-checkbox v-model="showWatchlistOnly">仅显示自选股</el-checkbox>
        <el-select v-model="selectedEventType" placeholder="事件类型" clearable style="width: 150px">
          <el-option
            v-for="(info, type) in EVENT_TYPE_MAP"
            :key="type"
            :label="info.label"
            :value="type"
          />
        </el-select>
        <el-button type="primary" @click="handleSync" :loading="syncing">
          同步数据
        </el-button>
      </div>
    </div>
    
    <!-- 主内容区 -->
    <div class="calendar-content">
      <!-- 月历视图 -->
      <CalendarMonth
        v-if="viewType === 'month'"
        :current-date="currentDate"
        :events="events"
        @date-click="handleDateClick"
        @event-click="handleEventClick"
      />
      
      <!-- 周历视图 -->
      <CalendarWeek
        v-else-if="viewType === 'week'"
        :current-date="currentDate"
        :events="events"
        @event-click="handleEventClick"
      />
      
      <!-- 时间线视图 -->
      <TimelineView
        v-else
        :current-date="currentDate"
        :events="events"
        @event-click="handleEventClick"
      />
    </div>
    
    <!-- 事件详情弹窗 -->
    <EventDetailDialog
      v-model="showEventDetail"
      :event="selectedEvent"
      @set-reminder="handleSetReminder"
    />
    
    <!-- 提醒设置弹窗 -->
    <ReminderDialog
      v-model="showReminderDialog"
      :event="selectedEvent"
      @success="handleReminderSuccess"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { ArrowLeft, ArrowRight } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { getEventList, syncEarnings } from '@/api/stockCalendar'
import { EVENT_TYPE_MAP } from './types/calendar'
import type { CalendarEvent } from './types/calendar'
import CalendarMonth from './components/CalendarMonth.vue'
import CalendarWeek from './components/CalendarWeek.vue'
import TimelineView from './components/TimelineView.vue'
import EventDetailDialog from './components/EventDetailDialog.vue'
import ReminderDialog from './components/ReminderDialog.vue'

// 视图类型
const viewType = ref<'month' | 'week' | 'timeline'>('month')

// 当前日期
const currentDate = ref(new Date())

// 事件列表
const events = ref<CalendarEvent[]>([])
const loading = ref(false)

// 筛选条件
const showWatchlistOnly = ref(false)
const selectedEventType = ref('')

// 同步状态
const syncing = ref(false)

// 选中事件
const selectedEvent = ref<CalendarEvent | null>(null)
const showEventDetail = ref(false)
const showReminderDialog = ref(false)

// 日期显示
const currentDateDisplay = computed(() => {
  const year = currentDate.value.getFullYear()
  const month = currentDate.value.getMonth() + 1
  if (viewType.value === 'month') {
    return `${year}年${month}月`
  } else if (viewType.value === 'week') {
    return `${year}年${month}月 第${getWeekNumber(currentDate.value)}周`
  }
  return `${year}年${month}月`
})

// 获取周数
function getWeekNumber(date: Date): number {
  const firstDay = new Date(date.getFullYear(), 0, 1)
  const days = Math.floor((date.getTime() - firstDay.getTime()) / (24 * 60 * 60 * 1000))
  return Math.ceil((days + firstDay.getDay() + 1) / 7)
}

// 导航日期
function navigateDate(direction: number) {
  const newDate = new Date(currentDate.value)
  if (viewType.value === 'month') {
    newDate.setMonth(newDate.getMonth() + direction)
  } else if (viewType.value === 'week') {
    newDate.setDate(newDate.getDate() + direction * 7)
  } else {
    newDate.setMonth(newDate.getMonth() + direction)
  }
  currentDate.value = newDate
}

// 回到今天
function goToToday() {
  currentDate.value = new Date()
}

// 加载事件
async function loadEvents() {
  loading.value = true
  try {
    const startDate = getStartDate()
    const endDate = getEndDate()
    
    const { data } = await getEventList({
      start_date: startDate,
      end_date: endDate,
      is_watchlist: showWatchlistOnly.value ? 1 : undefined,
      event_type: selectedEventType.value || undefined,
      page: 1,
      page_size: 500
    })
    
    events.value = data.items || []
  } catch (error) {
    console.error('加载事件失败:', error)
    ElMessage.error('加载事件失败')
  } finally {
    loading.value = false
  }
}

// 获取开始日期
function getStartDate(): string {
  const date = new Date(currentDate.value)
  if (viewType.value === 'month') {
    date.setDate(1)
  } else if (viewType.value === 'week') {
    const day = date.getDay()
    date.setDate(date.getDate() - day)
  }
  return formatDate(date)
}

// 获取结束日期
function getEndDate(): string {
  const date = new Date(currentDate.value)
  if (viewType.value === 'month') {
    date.setMonth(date.getMonth() + 1)
    date.setDate(0)
  } else if (viewType.value === 'week') {
    const day = date.getDay()
    date.setDate(date.getDate() + (6 - day))
  }
  return formatDate(date)
}

// 格式化日期
function formatDate(date: Date): string {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

// 处理日期点击
function handleDateClick(date: Date) {
  currentDate.value = date
  viewType.value = 'week'
}

// 处理事件点击
function handleEventClick(event: CalendarEvent) {
  selectedEvent.value = event
  showEventDetail.value = true
}

// 处理设置提醒
function handleSetReminder(event: CalendarEvent) {
  selectedEvent.value = event
  showEventDetail.value = false
  showReminderDialog.value = true
}

// 提醒设置成功
function handleReminderSuccess() {
  ElMessage.success('提醒设置成功')
  showReminderDialog.value = false
}

// 同步数据
async function handleSync() {
  syncing.value = true
  try {
    await syncEarnings()
    ElMessage.success('同步成功')
    await loadEvents()
  } catch (error) {
    console.error('同步失败:', error)
    ElMessage.error('同步失败')
  } finally {
    syncing.value = false
  }
}

// 监听筛选条件变化
watch([showWatchlistOnly, selectedEventType, currentDate], () => {
  loadEvents()
})

// 初始化
onMounted(() => {
  loadEvents()
})
</script>

<style scoped lang="scss">
.invest-calendar {
  height: 100%;
  display: flex;
  flex-direction: column;
  
  .calendar-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px;
    background: var(--el-bg-color);
    border-bottom: 1px solid var(--el-border-color);
    
    .header-left {
      display: flex;
      align-items: center;
      gap: 20px;
      
      .date-nav {
        display: flex;
        align-items: center;
        gap: 8px;
        
        .current-date {
          font-size: 16px;
          font-weight: 500;
          min-width: 150px;
          text-align: center;
        }
      }
    }
    
    .header-right {
      display: flex;
      align-items: center;
      gap: 12px;
    }
  }
  
  .calendar-content {
    flex: 1;
    overflow: auto;
  }
}
</style>
```

**Step 2: Commit**

```bash
git add frontend/src/views/Vadmin/Stock/InvestCalendar/InvestCalendar.vue
git commit -m "feat(frontend): add main calendar page component"
```

---

### Task 3.3: 创建月历视图组件

**Files:**
- Create: `frontend/src/views/Vadmin/Stock/InvestCalendar/components/CalendarMonth.vue`

**Step 1: 编写月历组件**

```vue
<!-- frontend/src/views/Vadmin/Stock/InvestCalendar/components/CalendarMonth.vue -->
<template>
  <div class="calendar-month">
    <!-- 星期头 -->
    <div class="weekday-header">
      <div v-for="day in weekdays" :key="day" class="weekday-cell">{{ day }}</div>
    </div>
    
    <!-- 日期网格 -->
    <div class="date-grid">
      <div
        v-for="(cell, index) in calendarCells"
        :key="index"
        class="date-cell"
        :class="{
          'other-month': !cell.isCurrentMonth,
          'is-today': cell.isToday,
          'has-events': cell.events.length > 0
        }"
        @click="handleCellClick(cell)"
      >
        <div class="date-number">{{ cell.date }}</div>
        <div class="event-dots">
          <span
            v-for="(event, i) in cell.events.slice(0, 3)"
            :key="i"
            class="event-dot"
            :style="{ backgroundColor: getEventColor(event.event_type) }"
          />
          <span v-if="cell.events.length > 3" class="more-dots">+{{ cell.events.length - 3 }}</span>
        </div>
        <div class="event-list" v-if="cell.events.length > 0">
          <div
            v-for="event in cell.events.slice(0, 2)"
            :key="event.id"
            class="event-item"
            :style="{ borderLeftColor: getEventColor(event.event_type) }"
            @click.stop="handleEventClick(event)"
          >
            <span class="event-title">{{ event.title }}</span>
          </div>
          <div v-if="cell.events.length > 2" class="more-events" @click.stop="handleCellClick(cell)">
            还有 {{ cell.events.length - 2 }} 个事件
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, defineProps, defineEmits } from 'vue'
import type { CalendarEvent, EventType } from '../types/calendar'
import { EVENT_TYPE_MAP } from '../types/calendar'

const props = defineProps<{
  currentDate: Date
  events: CalendarEvent[]
}>()

const emit = defineEmits<{
  (e: 'date-click', date: Date): void
  (e: 'event-click', event: CalendarEvent): void
}>()

const weekdays = ['日', '一', '二', '三', '四', '五', '六']

interface CalendarCell {
  date: number
  fullDate: Date
  isCurrentMonth: boolean
  isToday: boolean
  events: CalendarEvent[]
}

// 计算日历格子
const calendarCells = computed(() => {
  const year = props.currentDate.getFullYear()
  const month = props.currentDate.getMonth()
  
  const firstDay = new Date(year, month, 1)
  const lastDay = new Date(year, month + 1, 0)
  
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  
  const cells: CalendarCell[] = []
  
  // 上个月的日期
  const firstDayWeek = firstDay.getDay()
  for (let i = firstDayWeek - 1; i >= 0; i--) {
    const date = new Date(year, month, -i)
    cells.push({
      date: date.getDate(),
      fullDate: date,
      isCurrentMonth: false,
      isToday: date.getTime() === today.getTime(),
      events: getEventsForDate(date)
    })
  }
  
  // 本月的日期
  for (let i = 1; i <= lastDay.getDate(); i++) {
    const date = new Date(year, month, i)
    cells.push({
      date: i,
      fullDate: date,
      isCurrentMonth: true,
      isToday: date.getTime() === today.getTime(),
      events: getEventsForDate(date)
    })
  }
  
  // 下个月的日期（补齐6行）
  const remaining = 42 - cells.length
  for (let i = 1; i <= remaining; i++) {
    const date = new Date(year, month + 1, i)
    cells.push({
      date: i,
      fullDate: date,
      isCurrentMonth: false,
      isToday: date.getTime() === today.getTime(),
      events: getEventsForDate(date)
    })
  }
  
  return cells
})

// 获取某日期的事件
function getEventsForDate(date: Date): CalendarEvent[] {
  const dateStr = formatDate(date)
  return props.events.filter(event => event.event_date === dateStr)
}

// 格式化日期
function formatDate(date: Date): string {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

// 获取事件颜色
function getEventColor(type: EventType): string {
  return EVENT_TYPE_MAP[type]?.color || '#909399'
}

// 处理单元格点击
function handleCellClick(cell: CalendarCell) {
  emit('date-click', cell.fullDate)
}

// 处理事件点击
function handleEventClick(event: CalendarEvent) {
  emit('event-click', event)
}
</script>

<style scoped lang="scss">
.calendar-month {
  height: 100%;
  display: flex;
  flex-direction: column;
  
  .weekday-header {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    background: var(--el-fill-color-light);
    border-bottom: 1px solid var(--el-border-color);
    
    .weekday-cell {
      padding: 12px;
      text-align: center;
      font-weight: 500;
      color: var(--el-text-color-secondary);
    }
  }
  
  .date-grid {
    flex: 1;
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    grid-template-rows: repeat(6, 1fr);
    
    .date-cell {
      min-height: 100px;
      padding: 8px;
      border-right: 1px solid var(--el-border-color-lighter);
      border-bottom: 1px solid var(--el-border-color-lighter);
      cursor: pointer;
      transition: background-color 0.2s;
      
      &:hover {
        background-color: var(--el-fill-color-light);
      }
      
      &.other-month {
        background-color: var(--el-fill-color-lighter);
        .date-number {
          color: var(--el-text-color-placeholder);
        }
      }
      
      &.is-today {
        background-color: var(--el-color-primary-light-9);
        .date-number {
          background-color: var(--el-color-primary);
          color: white;
          border-radius: 50%;
          width: 28px;
          height: 28px;
          display: flex;
          align-items: center;
          justify-content: center;
        }
      }
      
      .date-number {
        font-size: 14px;
        font-weight: 500;
        margin-bottom: 4px;
      }
      
      .event-dots {
        display: flex;
        gap: 4px;
        margin-bottom: 4px;
        
        .event-dot {
          width: 6px;
          height: 6px;
          border-radius: 50%;
        }
        
        .more-dots {
          font-size: 10px;
          color: var(--el-text-color-secondary);
        }
      }
      
      .event-list {
        .event-item {
          font-size: 12px;
          padding: 2px 6px;
          border-left: 3px solid;
          background: var(--el-fill-color-lighter);
          margin-bottom: 2px;
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
          
          .event-title {
            color: var(--el-text-color-primary);
          }
        }
        
        .more-events {
          font-size: 11px;
          color: var(--el-color-primary);
          cursor: pointer;
          
          &:hover {
            text-decoration: underline;
          }
        }
      }
    }
  }
}
</style>
```

**Step 2: Commit**

```bash
git add frontend/src/views/Vadmin/Stock/InvestCalendar/components/CalendarMonth.vue
git commit -m "feat(frontend): add calendar month view component"
```

---

## Phase 4-6: 后续任务概要

由于篇幅限制，以下为剩余任务的文件清单和关键步骤：

### Phase 4: AI分析集成（2天）

- Task 4.1: 创建AI分析服务 `services/ai_analysis_service.py`
- Task 4.2: 添加AI分析API端点
- Task 4.3: 创建前端AI分析面板组件

### Phase 5: 提醒服务与联动（2天）

- Task 5.1: 创建提醒服务 `services/reminder_service.py`
- Task 5.2: 添加定时任务调度
- Task 5.3: 实现与自选股模块联动

### Phase 6: 测试与优化（2天）

- Task 6.1: 编写后端单元测试
- Task 6.2: 编写前端组件测试
- Task 6.3: 性能优化和文档完善

---

## 文件清单汇总

### 后端文件
```
backend/apps/admin/stock_calendar/
├── __init__.py
├── views.py                              # API视图
├── models/
│   ├── __init__.py
│   ├── stock_calendar_event.py           # 个股事件模型
│   ├── stock_event_reminder.py           # 用户提醒模型
│   ├── invest_calendar_event.py          # 宏观事件模型
│   └── sector_rotation_opportunity.py    # 板块机会模型
├── schemas/
│   ├── __init__.py
│   ├── event.py                          # 事件Schema
│   └── reminder.py                       # 提醒Schema
├── params/
│   ├── __init__.py
│   └── event_params.py                   # 查询参数
├── crud/
│   ├── __init__.py
│   ├── event_crud.py                     # 事件CRUD
│   └── reminder_crud.py                  # 提醒CRUD
└── services/
    ├── __init__.py
    ├── data_sync_service.py              # 数据同步服务
    ├── ai_analysis_service.py            # AI分析服务
    └── reminder_service.py               # 提醒服务
```

### 前端文件
```
frontend/src/views/Vadmin/Stock/InvestCalendar/
├── InvestCalendar.vue                    # 主页面
├── components/
│   ├── CalendarMonth.vue                 # 月历视图
│   ├── CalendarWeek.vue                  # 周历视图
│   ├── TimelineView.vue                  # 时间线视图
│   ├── EventCard.vue                     # 事件卡片
│   ├── EventDetailDialog.vue             # 事件详情弹窗
│   ├── ReminderDialog.vue                # 提醒设置弹窗
│   └── FilterPanel.vue                   # 筛选面板
├── composables/
│   ├── useCalendarEvents.ts              # 事件数据逻辑
│   └── useEventReminders.ts              # 提醒逻辑
└── types/
    └── calendar.ts                       # 类型定义

frontend/src/api/
└── stockCalendar.ts                      # API接口
```

---

**文档版本**: v1.0
**创建日期**: 2026-03-21
**预估工期**: 13个工作日