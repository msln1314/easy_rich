# 复盘功能实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 构建一个综合型投资复盘工作台，包含复盘工作台、心得经验库、雷区基线三个核心模块。

**Architecture:** 采用前后端分离架构，后端基于FastAPI+SQLAlchemy提供REST API，前端使用Vue3+Element Plus实现三个独立页面，支持与投资组合、投资日历、监听策略等模块联动。

**Tech Stack:** FastAPI, SQLAlchemy 2.0, MySQL, Vue 3, Element Plus, TypeScript, ECharts

---

## Phase 1: 数据模型与基础API（2天）

### Task 1.1: 创建后端模块目录结构

**Files:**
- Create: `backend/apps/admin/review/__init__.py`
- Create: `backend/apps/admin/review/models/__init__.py`
- Create: `backend/apps/admin/review/schemas/__init__.py`
- Create: `backend/apps/admin/review/crud/__init__.py`
- Create: `backend/apps/admin/review/services/__init__.py`

**Step 1: 创建目录**

```bash
mkdir -p backend/apps/admin/review/models
mkdir -p backend/apps/admin/review/schemas
mkdir -p backend/apps/admin/review/crud
mkdir -p backend/apps/admin/review/services
```

**Step 2: 创建初始化文件**

创建空的 `__init__.py` 文件在每个目录下。

**Step 3: 提交**

```bash
git add backend/apps/admin/review/
git commit -m "feat(review): init module directory structure"
```

---

### Task 1.2: 创建复盘记录数据模型

**Files:**
- Create: `backend/apps/admin/review/models/review_record.py`

**Step 1: 编写数据模型**

```python
from datetime import date
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Text, Date, Float, SmallInteger, Index
from db.db_base import BaseModel


class ReviewRecord(BaseModel):
    __tablename__ = "review_record"
    __table_args__ = (
        Index("idx_review_user_date", "user_id", "review_date"),
        Index("idx_review_type", "review_type"),
        {"comment": "复盘记录表"},
    )

    user_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="用户ID")
    portfolio_id: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="关联组合ID")

    review_type: Mapped[str] = mapped_column(String(20), nullable=False, comment="复盘类型: daily/weekly/monthly/adhoc")
    review_date: Mapped[date] = mapped_column(Date, nullable=False, comment="复盘日期")

    market_summary: Mapped[str | None] = mapped_column(Text, nullable=True, comment="市场数据JSON")
    market_analysis: Mapped[str | None] = mapped_column(Text, nullable=True, comment="用户市场分析")

    position_summary: Mapped[str | None] = mapped_column(Text, nullable=True, comment="持仓数据JSON")
    position_analysis: Mapped[str | None] = mapped_column(Text, nullable=True, comment="用户持仓分析")

    trade_summary: Mapped[str | None] = mapped_column(Text, nullable=True, comment="交易数据JSON")
    trade_analysis: Mapped[str | None] = mapped_column(Text, nullable=True, comment="用户交易分析")

    strategy_summary: Mapped[str | None] = mapped_column(Text, nullable=True, comment="策略数据JSON")
    strategy_analysis: Mapped[str | None] = mapped_column(Text, nullable=True, comment="用户策略分析")

    profit_summary: Mapped[str | None] = mapped_column(Text, nullable=True, comment="盈亏数据JSON")

    notes: Mapped[str | None] = mapped_column(Text, nullable=True, comment="心得记录")

    next_plan: Mapped[str | None] = mapped_column(Text, nullable=True, comment="下期计划JSON")

    ai_analysis: Mapped[str | None] = mapped_column(Text, nullable=True, comment="AI分析报告")

    status: Mapped[str] = mapped_column(String(20), default="draft", comment="状态: draft/published")
```

**Step 2: 更新 models/__init__.py**

```python
from .review_record import ReviewRecord

__all__ = ["ReviewRecord"]
```

**Step 3: 提交**

```bash
git add backend/apps/admin/review/models/
git commit -m "feat(review): add ReviewRecord model"
```

---

### Task 1.3: 创建心得经验数据模型

**Files:**
- Create: `backend/apps/admin/review/models/experience_note.py`

**Step 1: 编写数据模型**

```python
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Text, SmallInteger, Index
from db.db_base import BaseModel


class ExperienceNote(BaseModel):
    __tablename__ = "experience_note"
    __table_args__ = (
        Index("idx_exp_user_id", "user_id"),
        Index("idx_exp_category", "category"),
        Index("idx_exp_created", "created_at"),
        {"comment": "心得经验表"},
    )

    user_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="用户ID")

    title: Mapped[str] = mapped_column(String(200), nullable=False, comment="标题")
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="内容")

    category: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="分类")
    tags: Mapped[str | None] = mapped_column(Text, nullable=True, comment="标签JSON数组")

    related_stocks: Mapped[str | None] = mapped_column(Text, nullable=True, comment="关联股票代码JSON")
    related_trades: Mapped[str | None] = mapped_column(Text, nullable=True, comment="关联交易ID JSON")
    related_review_id: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="关联复盘ID")

    mood: Mapped[str | None] = mapped_column(String(20), nullable=True, comment="心情")
    importance: Mapped[str] = mapped_column(String(20), default="normal", comment="重要程度")

    view_count: Mapped[int] = mapped_column(Integer, default=0, comment="查看次数")
```

**Step 2: 更新 models/__init__.py**

```python
from .review_record import ReviewRecord
from .experience_note import ExperienceNote

__all__ = ["ReviewRecord", "ExperienceNote"]
```

**Step 3: 提交**

```bash
git add backend/apps/admin/review/models/
git commit -m "feat(review): add ExperienceNote model"
```

---

### Task 1.4: 创建雷区基线数据模型

**Files:**
- Create: `backend/apps/admin/review/models/risk_rule.py`
- Create: `backend/apps/admin/review/models/rule_violation.py`

**Step 1: 编写规则模型**

```python
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Text, SmallInteger, Index
from db.db_base import BaseModel


class RiskRule(BaseModel):
    __tablename__ = "risk_rule"
    __table_args__ = (
        Index("idx_rule_user_type", "user_id", "rule_type"),
        Index("idx_rule_active", "is_active"),
        {"comment": "雷区基线规则表"},
    )

    user_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="用户ID")

    rule_type: Mapped[str] = mapped_column(String(20), nullable=False, comment="规则类型: trap/baseline")
    category: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="分类")

    name: Mapped[str] = mapped_column(String(200), nullable=False, comment="规则名称")
    description: Mapped[str | None] = mapped_column(Text, nullable=True, comment="规则描述")

    severity: Mapped[str | None] = mapped_column(String(20), nullable=True, comment="严重程度")

    check_timing: Mapped[str | None] = mapped_column(Text, nullable=True, comment="检查时机JSON")
    check_condition: Mapped[str | None] = mapped_column(Text, nullable=True, comment="触发条件JSON")

    is_active: Mapped[int] = mapped_column(SmallInteger, default=1, comment="是否启用")
```

**Step 2: 编写违规记录模型**

```python
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Text, DateTime, Index
from db.db_base import BaseModel


class RuleViolation(BaseModel):
    __tablename__ = "rule_violation"
    __table_args__ = (
        Index("idx_viol_user_time", "user_id", "violation_time"),
        Index("idx_viol_rule", "rule_id"),
        {"comment": "违规记录表"},
    )

    user_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="用户ID")
    rule_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="规则ID")

    violation_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, comment="违规时间")
    violation_context: Mapped[str | None] = mapped_column(Text, nullable=True, comment="违规上下文JSON")

    related_stock_code: Mapped[str | None] = mapped_column(String(20), nullable=True, comment="关联股票代码")
    related_trade_id: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="关联交易ID")

    user_note: Mapped[str | None] = mapped_column(Text, nullable=True, comment="用户备注")
```

**Step 3: 更新 models/__init__.py**

```python
from .review_record import ReviewRecord
from .experience_note import ExperienceNote
from .risk_rule import RiskRule
from .rule_violation import RuleViolation

__all__ = ["ReviewRecord", "ExperienceNote", "RiskRule", "RuleViolation"]
```

**Step 4: 提交**

```bash
git add backend/apps/admin/review/models/
git commit -m "feat(review): add RiskRule and RuleViolation models"
```

---

### Task 1.5: 创建Pydantic Schema定义

**Files:**
- Create: `backend/apps/admin/review/schemas/review.py`
- Create: `backend/apps/admin/review/schemas/experience.py`
- Create: `backend/apps/admin/review/schemas/rule.py`

**Step 1: 编写复盘Schema**

```python
from datetime import date
from typing import Optional, List, Any
from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr


class ReviewCreate(BaseModel):
    portfolio_id: Optional[int] = None
    review_type: str = Field(..., description="复盘类型")
    review_date: date = Field(..., description="复盘日期")
    market_summary: Optional[dict] = None
    market_analysis: Optional[str] = None
    position_summary: Optional[dict] = None
    position_analysis: Optional[str] = None
    trade_summary: Optional[dict] = None
    trade_analysis: Optional[str] = None
    strategy_summary: Optional[dict] = None
    strategy_analysis: Optional[str] = None
    profit_summary: Optional[dict] = None
    notes: Optional[str] = None
    next_plan: Optional[dict] = None
    ai_analysis: Optional[str] = None
    status: str = "draft"


class ReviewUpdate(BaseModel):
    market_summary: Optional[dict] = None
    market_analysis: Optional[str] = None
    position_summary: Optional[dict] = None
    position_analysis: Optional[str] = None
    trade_summary: Optional[dict] = None
    trade_analysis: Optional[str] = None
    strategy_summary: Optional[dict] = None
    strategy_analysis: Optional[str] = None
    profit_summary: Optional[dict] = None
    notes: Optional[str] = None
    next_plan: Optional[dict] = None
    ai_analysis: Optional[str] = None
    status: Optional[str] = None


class ReviewOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    portfolio_id: Optional[int] = None
    review_type: str
    review_date: date
    market_summary: Optional[Any] = None
    market_analysis: Optional[str] = None
    position_summary: Optional[Any] = None
    position_analysis: Optional[str] = None
    trade_summary: Optional[Any] = None
    trade_analysis: Optional[str] = None
    strategy_summary: Optional[Any] = None
    strategy_analysis: Optional[str] = None
    profit_summary: Optional[Any] = None
    notes: Optional[str] = None
    next_plan: Optional[Any] = None
    ai_analysis: Optional[str] = None
    status: str
    created_at: DatetimeStr
    updated_at: DatetimeStr


class ReviewListOut(BaseModel):
    total: int
    items: List[ReviewOut]
```

**Step 2: 编写心得Schema**

```python
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr


class ExperienceCreate(BaseModel):
    title: str = Field(..., description="标题")
    content: str = Field(..., description="内容")
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    related_stocks: Optional[List[str]] = None
    related_trades: Optional[List[int]] = None
    related_review_id: Optional[int] = None
    mood: Optional[str] = None
    importance: str = "normal"


class ExperienceUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    related_stocks: Optional[List[str]] = None
    related_trades: Optional[List[int]] = None
    related_review_id: Optional[int] = None
    mood: Optional[str] = None
    importance: Optional[str] = None


class ExperienceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    title: str
    content: str
    category: Optional[str] = None
    tags: Optional[list] = None
    related_stocks: Optional[list] = None
    related_trades: Optional[list] = None
    related_review_id: Optional[int] = None
    mood: Optional[str] = None
    importance: str
    view_count: int
    created_at: DatetimeStr
    updated_at: DatetimeStr


class ExperienceListOut(BaseModel):
    total: int
    items: List[ExperienceOut]
```

**Step 3: 编写规则Schema**

```python
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr


class RuleCreate(BaseModel):
    rule_type: str = Field(..., description="规则类型: trap/baseline")
    category: Optional[str] = None
    name: str = Field(..., description="规则名称")
    description: Optional[str] = None
    severity: Optional[str] = None
    check_timing: Optional[List[str]] = None
    check_condition: Optional[dict] = None
    is_active: int = 1


class RuleUpdate(BaseModel):
    category: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[str] = None
    check_timing: Optional[List[str]] = None
    check_condition: Optional[dict] = None
    is_active: Optional[int] = None


class RuleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    rule_type: str
    category: Optional[str] = None
    name: str
    description: Optional[str] = None
    severity: Optional[str] = None
    check_timing: Optional[list] = None
    check_condition: Optional[dict] = None
    is_active: int
    created_at: DatetimeStr
    updated_at: DatetimeStr


class ViolationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    rule_id: int
    violation_time: datetime
    violation_context: Optional[dict] = None
    related_stock_code: Optional[str] = None
    related_trade_id: Optional[int] = None
    user_note: Optional[str] = None
    created_at: DatetimeStr
```

**Step 4: 更新 schemas/__init__.py**

```python
from .review import ReviewCreate, ReviewUpdate, ReviewOut, ReviewListOut
from .experience import ExperienceCreate, ExperienceUpdate, ExperienceOut, ExperienceListOut
from .rule import RuleCreate, RuleUpdate, RuleOut, ViolationOut

__all__ = [
    "ReviewCreate", "ReviewUpdate", "ReviewOut", "ReviewListOut",
    "ExperienceCreate", "ExperienceUpdate", "ExperienceOut", "ExperienceListOut",
    "RuleCreate", "RuleUpdate", "RuleOut", "ViolationOut",
]
```

**Step 5: 提交**

```bash
git add backend/apps/admin/review/schemas/
git commit -m "feat(review): add Pydantic schemas"
```

---

### Task 1.6: 创建CRUD操作

**Files:**
- Create: `backend/apps/admin/review/crud/review_crud.py`
- Create: `backend/apps/admin/review/crud/experience_crud.py`
- Create: `backend/apps/admin/review/crud/rule_crud.py`

**Step 1: 编写复盘CRUD**

```python
from typing import List, Optional, Tuple
from datetime import date
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from core.crud import DalBase
from apps.admin.review import models, schemas


class ReviewDal(DalBase):

    def __init__(self, db: AsyncSession):
        super().__init__()
        self.db = db
        self.model = models.ReviewRecord
        self.schema = schemas.ReviewOut

    async def get_list_by_user(
        self, user_id: int, review_type: str = None, page: int = 1, limit: int = 20
    ) -> Tuple[List[models.ReviewRecord], int]:
        conditions = [self.model.user_id == user_id, self.model.is_delete == False]
        if review_type:
            conditions.append(self.model.review_type == review_type)

        sql = select(self.model).where(and_(*conditions)).order_by(self.model.review_date.desc())
        return await self.get_datas(page=page, limit=limit, v_start_sql=sql, v_return_count=True)

    async def get_by_date(self, user_id: int, review_date: date) -> Optional[models.ReviewRecord]:
        sql = select(self.model).where(
            and_(
                self.model.user_id == user_id,
                self.model.review_date == review_date,
                self.model.is_delete == False,
            )
        )
        result = await self.db.scalars(sql)
        return result.first()

    async def create_review(self, data: schemas.ReviewCreate, user_id: int) -> models.ReviewRecord:
        import json
        obj_data = data.model_dump()
        for key in ['market_summary', 'position_summary', 'trade_summary', 'strategy_summary', 'profit_summary', 'next_plan']:
            if obj_data.get(key):
                obj_data[key] = json.dumps(obj_data[key])
        obj = self.model(user_id=user_id, **obj_data)
        self.db.add(obj)
        await self.db.flush()
        return obj
```

**Step 2: 编写心得CRUD**

```python
from typing import List, Optional
from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from core.crud import DalBase
from apps.admin.review import models, schemas


class ExperienceDal(DalBase):

    def __init__(self, db: AsyncSession):
        super().__init__()
        self.db = db
        self.model = models.ExperienceNote
        self.schema = schemas.ExperienceOut

    async def get_list_by_user(
        self, user_id: int, category: str = None, tag: str = None, page: int = 1, limit: int = 20
    ) -> List[models.ExperienceNote]:
        conditions = [self.model.user_id == user_id, self.model.is_delete == False]
        if category:
            conditions.append(self.model.category == category)

        sql = select(self.model).where(and_(*conditions)).order_by(self.model.created_at.desc())
        return await self.get_datas(page=page, limit=limit, v_start_sql=sql)

    async def get_by_stock(self, user_id: int, stock_code: str) -> List[models.ExperienceNote]:
        sql = select(self.model).where(
            and_(
                self.model.user_id == user_id,
                self.model.related_stocks.contains(stock_code),
                self.model.is_delete == False,
            )
        ).order_by(self.model.created_at.desc())
        result = await self.db.scalars(sql)
        return result.all()

    async def create_note(self, data: schemas.ExperienceCreate, user_id: int) -> models.ExperienceNote:
        import json
        obj_data = data.model_dump()
        for key in ['tags', 'related_stocks', 'related_trades']:
            if obj_data.get(key):
                obj_data[key] = json.dumps(obj_data[key])
        obj = self.model(user_id=user_id, **obj_data)
        self.db.add(obj)
        await self.db.flush()
        return obj
```

**Step 3: 编写规则CRUD**

```python
from typing import List, Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from core.crud import DalBase
from apps.admin.review import models, schemas


class RuleDal(DalBase):

    def __init__(self, db: AsyncSession):
        super().__init__()
        self.db = db
        self.model = models.RiskRule
        self.schema = schemas.RuleOut

    async def get_list_by_user(
        self, user_id: int, rule_type: str = None
    ) -> List[models.RiskRule]:
        conditions = [self.model.user_id == user_id, self.model.is_delete == False]
        if rule_type:
            conditions.append(self.model.rule_type == rule_type)

        sql = select(self.model).where(and_(*conditions)).order_by(self.model.severity.desc())
        result = await self.db.scalars(sql)
        return result.all()

    async def get_active_rules(self, user_id: int, check_timing: str = None) -> List[models.RiskRule]:
        conditions = [
            self.model.user_id == user_id,
            self.model.is_active == 1,
            self.model.is_delete == False,
        ]
        if check_timing:
            conditions.append(self.model.check_timing.contains(check_timing))

        sql = select(self.model).where(and_(*conditions))
        result = await self.db.scalars(sql)
        return result.all()


class ViolationDal(DalBase):

    def __init__(self, db: AsyncSession):
        super().__init__()
        self.db = db
        self.model = models.RuleViolation
        self.schema = schemas.ViolationOut

    async def get_list_by_user(
        self, user_id: int, limit: int = 50
    ) -> List[models.RuleViolation]:
        sql = select(self.model).where(
            and_(self.model.user_id == user_id, self.model.is_delete == False)
        ).order_by(self.model.violation_time.desc()).limit(limit)
        result = await self.db.scalars(sql)
        return result.all()

    async def create_violation(
        self, user_id: int, rule_id: int, context: dict, stock_code: str = None
    ) -> models.RuleViolation:
        import json
        obj = self.model(
            user_id=user_id,
            rule_id=rule_id,
            violation_context=json.dumps(context) if context else None,
            related_stock_code=stock_code,
        )
        self.db.add(obj)
        await self.db.flush()
        return obj
```

**Step 4: 更新 crud/__init__.py**

```python
from .review_crud import ReviewDal
from .experience_crud import ExperienceDal
from .rule_crud import RuleDal, ViolationDal

__all__ = ["ReviewDal", "ExperienceDal", "RuleDal", "ViolationDal"]
```

**Step 5: 提交**

```bash
git add backend/apps/admin/review/crud/
git commit -m "feat(review): add CRUD operations"
```

---

### Task 1.7: 创建API视图并注册路由

**Files:**
- Create: `backend/apps/admin/review/views.py`
- Modify: `backend/apps/admin/stock/api.py`

**Step 1: 编写API视图**

```python
from datetime import date
from typing import Optional, List
from fastapi import APIRouter, Depends, Query
from utils.response import SuccessResponse, ErrorResponse
from apps.admin.auth.utils.current import AllUserAuth, Auth
from . import schemas, crud

router = APIRouter()


# ==================== 复盘工作台 ====================

@router.get("", summary="获取复盘列表")
async def get_reviews(
    review_type: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    auth: Auth = Depends(AllUserAuth()),
):
    dal = crud.ReviewDal(auth.db)
    items, total = await dal.get_list_by_user(auth.user.id, review_type, page, limit)
    datas = [schemas.ReviewOut.model_validate(i).model_dump() for i in items]
    return SuccessResponse(datas, count=total)


@router.get("/{review_id}", summary="获取复盘详情")
async def get_review(review_id: int, auth: Auth = Depends(AllUserAuth())):
    dal = crud.ReviewDal(auth.db)
    review = await dal.get_data(review_id, v_return_none=True)
    if not review:
        return ErrorResponse("复盘记录不存在")
    return SuccessResponse(schemas.ReviewOut.model_validate(review).model_dump())


@router.post("", summary="创建复盘")
async def create_review(data: schemas.ReviewCreate, auth: Auth = Depends(AllUserAuth())):
    dal = crud.ReviewDal(auth.db)
    review = await dal.create_review(data, auth.user.id)
    return SuccessResponse(schemas.ReviewOut.model_validate(review).model_dump())


@router.put("/{review_id}", summary="更新复盘")
async def update_review(review_id: int, data: schemas.ReviewUpdate, auth: Auth = Depends(AllUserAuth())):
    dal = crud.ReviewDal(auth.db)
    review = await dal.put_data(review_id, data)
    return SuccessResponse(schemas.ReviewOut.model_validate(review).model_dump())


@router.delete("/{review_id}", summary="删除复盘")
async def delete_review(review_id: int, auth: Auth = Depends(AllUserAuth())):
    dal = crud.ReviewDal(auth.db)
    await dal.delete_datas([review_id], v_soft=False)
    return SuccessResponse("删除成功")


# ==================== 心得经验库 ====================

@router.get("/experience", summary="获取心得列表")
async def get_experiences(
    category: Optional[str] = None,
    tag: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    auth: Auth = Depends(AllUserAuth()),
):
    dal = crud.ExperienceDal(auth.db)
    items = await dal.get_list_by_user(auth.user.id, category, tag, page, limit)
    datas = [schemas.ExperienceOut.model_validate(i).model_dump() for i in items]
    return SuccessResponse(datas, count=len(datas))


@router.post("/experience", summary="创建心得")
async def create_experience(data: schemas.ExperienceCreate, auth: Auth = Depends(AllUserAuth())):
    dal = crud.ExperienceDal(auth.db)
    note = await dal.create_note(data, auth.user.id)
    return SuccessResponse(schemas.ExperienceOut.model_validate(note).model_dump())


@router.put("/experience/{note_id}", summary="更新心得")
async def update_experience(note_id: int, data: schemas.ExperienceUpdate, auth: Auth = Depends(AllUserAuth())):
    dal = crud.ExperienceDal(auth.db)
    note = await dal.put_data(note_id, data)
    return SuccessResponse(schemas.ExperienceOut.model_validate(note).model_dump())


@router.delete("/experience/{note_id}", summary="删除心得")
async def delete_experience(note_id: int, auth: Auth = Depends(AllUserAuth())):
    dal = crud.ExperienceDal(auth.db)
    await dal.delete_datas([note_id], v_soft=False)
    return SuccessResponse("删除成功")


# ==================== 雷区基线 ====================

@router.get("/rule", summary="获取规则列表")
async def get_rules(rule_type: Optional[str] = None, auth: Auth = Depends(AllUserAuth())):
    dal = crud.RuleDal(auth.db)
    items = await dal.get_list_by_user(auth.user.id, rule_type)
    datas = [schemas.RuleOut.model_validate(i).model_dump() for i in items]
    return SuccessResponse(datas, count=len(datas))


@router.post("/rule", summary="创建规则")
async def create_rule(data: schemas.RuleCreate, auth: Auth = Depends(AllUserAuth())):
    dal = crud.RuleDal(auth.db)
    rule = await dal.create_data(data)
    return SuccessResponse(schemas.RuleOut.model_validate(rule).model_dump())


@router.put("/rule/{rule_id}", summary="更新规则")
async def update_rule(rule_id: int, data: schemas.RuleUpdate, auth: Auth = Depends(AllUserAuth())):
    dal = crud.RuleDal(auth.db)
    rule = await dal.put_data(rule_id, data)
    return SuccessResponse(schemas.RuleOut.model_validate(rule).model_dump())


@router.delete("/rule/{rule_id}", summary="删除规则")
async def delete_rule(rule_id: int, auth: Auth = Depends(AllUserAuth())):
    dal = crud.RuleDal(auth.db)
    await dal.delete_datas([rule_id], v_soft=False)
    return SuccessResponse("删除成功")


@router.get("/violation", summary="获取违规记录")
async def get_violations(auth: Auth = Depends(AllUserAuth())):
    dal = crud.ViolationDal(auth.db)
    items = await dal.get_list_by_user(auth.user.id)
    datas = [schemas.ViolationOut.model_validate(i).model_dump() for i in items]
    return SuccessResponse(datas, count=len(datas))
```

**Step 2: 更新 review/__init__.py**

```python
from . import models, schemas, crud
from .views import router

__all__ = ["models", "schemas", "crud", "router"]
```

**Step 3: 注册路由到 stock/api.py**

在 `backend/apps/admin/stock/api.py` 中添加：

```python
from apps.admin.review import router as review_router
# ...
router.include_router(
    review_router, prefix="/review", tags=["复盘"]
)
```

**Step 4: 提交**

```bash
git add backend/apps/admin/review/
git commit -m "feat(review): add API views and register routes"
```

---

## Phase 2: 复盘工作台服务（2天）

### Task 2.1: 创建复盘服务

**Files:**
- Create: `backend/apps/admin/review/services/review_service.py`

**Step 1: 编写复盘服务**

```python
import json
from datetime import date, timedelta
from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from apps.admin.review import crud, schemas


class ReviewService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.review_dal = crud.ReviewDal(db)

    async def generate_market_summary(self) -> Dict[str, Any]:
        return {
            "index_data": {},
            "sector_rotation": [],
            "fund_flow": {},
            "up_down_distribution": {},
        }

    async def generate_position_summary(self, portfolio_id: int) -> Dict[str, Any]:
        return {
            "positions": [],
            "total_value": 0,
            "total_profit": 0,
            "profit_rate": 0,
        }

    async def generate_trade_summary(self, portfolio_id: int, review_date: date, review_type: str) -> Dict[str, Any]:
        return {
            "trades": [],
            "buy_count": 0,
            "sell_count": 0,
            "total_amount": 0,
        }

    async def generate_profit_summary(self, portfolio_id: int) -> Dict[str, Any]:
        return {
            "profit_rate": 0,
            "win_rate": 0,
            "profit_loss_ratio": 0,
            "max_drawdown": 0,
        }

    async def auto_generate_review(
        self, user_id: int, review_type: str, review_date: date, portfolio_id: int = None
    ) -> schemas.ReviewCreate:
        market_summary = await self.generate_market_summary()
        position_summary = None
        trade_summary = None
        profit_summary = None

        if portfolio_id:
            position_summary = await self.generate_position_summary(portfolio_id)
            trade_summary = await self.generate_trade_summary(portfolio_id, review_date, review_type)
            profit_summary = await self.generate_profit_summary(portfolio_id)

        return schemas.ReviewCreate(
            portfolio_id=portfolio_id,
            review_type=review_type,
            review_date=review_date,
            market_summary=market_summary,
            position_summary=position_summary,
            trade_summary=trade_summary,
            profit_summary=profit_summary,
        )

    async def get_review_history(self, user_id: int, days: int = 30) -> list:
        start_date = date.today() - timedelta(days=days)
        items = await self.review_dal.get_datas(
            limit=0,
            v_where=[
                self.review_dal.model.user_id == user_id,
                self.review_dal.model.review_date >= start_date,
            ],
            v_return_objs=True,
        )
        return items
```

**Step 2: 更新 services/__init__.py**

```python
from .review_service import ReviewService

__all__ = ["ReviewService"]
```

**Step 3: 提交**

```bash
git add backend/apps/admin/review/services/
git commit -m "feat(review): add ReviewService"
```

---

## Phase 3: 心得经验库服务（1天）

### Task 3.1: 创建心得服务

**Files:**
- Create: `backend/apps/admin/review/services/experience_service.py`

**Step 1: 编写心得服务**

```python
import json
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from apps.admin.review import crud, schemas, models


class ExperienceService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.exp_dal = crud.ExperienceDal(db)

    async def get_timeline(self, user_id: int, limit: int = 50) -> List[models.ExperienceNote]:
        return await self.exp_dal.get_list_by_user(user_id, limit=limit)

    async def get_by_category(self, user_id: int, category: str) -> List[models.ExperienceNote]:
        return await self.exp_dal.get_list_by_user(user_id, category=category)

    async def get_by_stock(self, user_id: int, stock_code: str) -> List[models.ExperienceNote]:
        return await self.exp_dal.get_by_stock(user_id, stock_code)

    async def get_categories(self, user_id: int) -> List[str]:
        items = await self.exp_dal.get_datas(limit=0, v_return_objs=True)
        categories = set()
        for item in items:
            if item.category:
                categories.add(item.category)
        return list(categories)

    async def get_tags(self, user_id: int) -> List[str]:
        items = await self.exp_dal.get_datas(limit=0, v_return_objs=True)
        tags = set()
        for item in items:
            if item.tags:
                try:
                    tag_list = json.loads(item.tags) if isinstance(item.tags, str) else item.tags
                    tags.update(tag_list)
                except:
                    pass
        return list(tags)

    async def increment_view_count(self, note_id: int):
        note = await self.exp_dal.get_data(note_id, v_return_none=True)
        if note:
            note.view_count = (note.view_count or 0) + 1
            await self.db.flush()
```

**Step 2: 更新 services/__init__.py**

```python
from .review_service import ReviewService
from .experience_service import ExperienceService

__all__ = ["ReviewService", "ExperienceService"]
```

**Step 3: 提交**

```bash
git add backend/apps/admin/review/services/
git commit -m "feat(review): add ExperienceService"
```

---

## Phase 4: 雷区基线服务（2天）

### Task 4.1: 创建规则服务

**Files:**
- Create: `backend/apps/admin/review/services/rule_service.py`

**Step 1: 编写规则服务**

```python
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from apps.admin.review import crud, schemas, models


class RuleService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.rule_dal = crud.RuleDal(db)
        self.violation_dal = crud.ViolationDal(db)

    async def get_preset_rules(self) -> Dict[str, List[Dict]]:
        return {
            "traps": [
                {"name": "单只股票仓位超过30%", "category": "position", "severity": "high"},
                {"name": "不设止损就买入", "category": "trade", "severity": "high"},
                {"name": "追高买入（涨幅>5%）", "category": "trade", "severity": "medium"},
                {"name": "频繁交易（日内>3次）", "category": "trade", "severity": "medium"},
                {"name": "亏损后急于翻本", "category": "psychology", "severity": "medium"},
            ],
            "baselines": [
                {"name": "单只股票仓位≤20%", "category": "position"},
                {"name": "保留10%现金应对机会", "category": "position"},
                {"name": "买入前必须设置止损位", "category": "trade"},
                {"name": "买入前必须分析理由", "category": "trade"},
                {"name": "分批建仓，首次≤50%目标仓位", "category": "trade"},
                {"name": "持仓股票不超过10只", "category": "risk"},
            ],
        }

    async def apply_presets(self, user_id: int, rule_types: List[str] = None) -> int:
        presets = await self.get_preset_rules()
        count = 0

        if not rule_types or "trap" in rule_types:
            for trap in presets["traps"]:
                data = schemas.RuleCreate(
                    rule_type="trap",
                    category=trap["category"],
                    name=trap["name"],
                    severity=trap.get("severity"),
                    check_timing=["realtime", "pre_trade"],
                )
                await self.rule_dal.create_data(data)
                count += 1

        if not rule_types or "baseline" in rule_types:
            for baseline in presets["baselines"]:
                data = schemas.RuleCreate(
                    rule_type="baseline",
                    category=baseline["category"],
                    name=baseline["name"],
                    check_timing=["pre_trade", "periodic"],
                )
                await self.rule_dal.create_data(data)
                count += 1

        return count

    async def check_pre_trade(
        self, user_id: int, stock_code: str, trade_type: str, amount: float
    ) -> Dict[str, Any]:
        rules = await self.rule_dal.get_active_rules(user_id, "pre_trade")
        violations = []
        warnings = []

        for rule in rules:
            if rule.rule_type == "trap":
                violations.append({
                    "rule_id": rule.id,
                    "rule_name": rule.name,
                    "severity": rule.severity,
                })
            elif rule.rule_type == "baseline":
                warnings.append({
                    "rule_id": rule.id,
                    "rule_name": rule.name,
                    "category": rule.category,
                })

        return {
            "violations": violations,
            "warnings": warnings,
            "can_proceed": len([v for v in violations if v["severity"] == "high"]) == 0,
        }

    async def record_violation(
        self, user_id: int, rule_id: int, context: dict, stock_code: str = None
    ) -> models.RuleViolation:
        return await self.violation_dal.create_violation(user_id, rule_id, context, stock_code)

    async def get_violation_stats(self, user_id: int, days: int = 30) -> Dict[str, Any]:
        violations = await self.violation_dal.get_list_by_user(user_id, limit=100)
        return {
            "total": len(violations),
            "by_severity": {},
            "by_category": {},
        }
```

**Step 2: 更新 services/__init__.py**

```python
from .review_service import ReviewService
from .experience_service import ExperienceService
from .rule_service import RuleService

__all__ = ["ReviewService", "ExperienceService", "RuleService"]
```

**Step 3: 提交**

```bash
git add backend/apps/admin/review/services/
git commit -m "feat(review): add RuleService"
```

---

## Phase 5: 前端页面开发（4天）

### Task 5.1: 创建前端目录结构和类型定义

**Files:**
- Create: `frontend/src/views/Vadmin/Stock/Review/types/review.ts`
- Create: `frontend/src/views/Vadmin/Stock/Experience/types/experience.ts`
- Create: `frontend/src/views/Vadmin/Stock/RiskRule/types/rule.ts`
- Create: `frontend/src/api/review.ts`
- Create: `frontend/src/api/experience.ts`
- Create: `frontend/src/api/riskRule.ts`

**Step 1: 创建目录**

```bash
mkdir -p frontend/src/views/Vadmin/Stock/Review/components
mkdir -p frontend/src/views/Vadmin/Stock/Experience/components
mkdir -p frontend/src/views/Vadmin/Stock/RiskRule/components
```

**Step 2: 编写类型定义**

`review.ts`:
```typescript
export type ReviewType = 'daily' | 'weekly' | 'monthly' | 'adhoc'

export interface ReviewRecord {
  id: number
  user_id: number
  portfolio_id: number | null
  review_type: ReviewType
  review_date: string
  market_summary: any
  market_analysis: string | null
  position_summary: any
  position_analysis: string | null
  trade_summary: any
  trade_analysis: string | null
  strategy_summary: any
  strategy_analysis: string | null
  profit_summary: any
  notes: string | null
  next_plan: any
  ai_analysis: string | null
  status: string
  created_at: string
  updated_at: string
}
```

`experience.ts`:
```typescript
export type ExperienceCategory = '选股技巧' | '止损心得' | '心态管理' | '策略优化' | '其他'
export type ExperienceMood = 'proud' | 'calm' | 'regret' | 'angry'
export type ExperienceImportance = 'normal' | 'important' | 'critical'

export interface ExperienceNote {
  id: number
  user_id: number
  title: string
  content: string
  category: ExperienceCategory | null
  tags: string[] | null
  related_stocks: string[] | null
  related_trades: number[] | null
  related_review_id: number | null
  mood: ExperienceMood | null
  importance: ExperienceImportance
  view_count: number
  created_at: string
  updated_at: string
}
```

`rule.ts`:
```typescript
export type RuleType = 'trap' | 'baseline'
export type RuleCategory = 'position' | 'trade' | 'psychology' | 'risk'
export type RuleSeverity = 'high' | 'medium' | 'low'

export interface RiskRule {
  id: number
  user_id: number
  rule_type: RuleType
  category: RuleCategory | null
  name: string
  description: string | null
  severity: RuleSeverity | null
  check_timing: string[] | null
  check_condition: any
  is_active: number
  created_at: string
  updated_at: string
}

export interface RuleViolation {
  id: number
  user_id: number
  rule_id: number
  violation_time: string
  violation_context: any
  related_stock_code: string | null
  related_trade_id: number | null
  user_note: string | null
  created_at: string
}
```

**Step 3: 编写API接口**

`review.ts`:
```typescript
import request from '@/utils/request'

const API_PREFIX = '/review'

export function getReviewList(params: { review_type?: string; page?: number; limit?: number }) {
  return request.get(API_PREFIX, { params })
}

export function getReviewDetail(reviewId: number) {
  return request.get(`${API_PREFIX}/${reviewId}`)
}

export function createReview(data: any) {
  return request.post(API_PREFIX, data)
}

export function updateReview(reviewId: number, data: any) {
  return request.put(`${API_PREFIX}/${reviewId}`, data)
}

export function deleteReview(reviewId: number) {
  return request.delete(`${API_PREFIX}/${reviewId}`)
}
```

`experience.ts`:
```typescript
import request from '@/utils/request'

const API_PREFIX = '/review/experience'

export function getExperienceList(params: { category?: string; tag?: string; page?: number; limit?: number }) {
  return request.get(API_PREFIX, { params })
}

export function createExperience(data: any) {
  return request.post(API_PREFIX, data)
}

export function updateExperience(noteId: number, data: any) {
  return request.put(`${API_PREFIX}/${noteId}`, data)
}

export function deleteExperience(noteId: number) {
  return request.delete(`${API_PREFIX}/${noteId}`)
}
```

`riskRule.ts`:
```typescript
import request from '@/utils/request'

const API_PREFIX = '/review'

export function getRuleList(ruleType?: string) {
  return request.get(`${API_PREFIX}/rule`, { params: { rule_type: ruleType } })
}

export function createRule(data: any) {
  return request.post(`${API_PREFIX}/rule`, data)
}

export function updateRule(ruleId: number, data: any) {
  return request.put(`${API_PREFIX}/rule/${ruleId}`, data)
}

export function deleteRule(ruleId: number) {
  return request.delete(`${API_PREFIX}/rule/${ruleId}`)
}

export function getViolations() {
  return request.get(`${API_PREFIX}/violation`)
}
```

**Step 4: 提交**

```bash
git add frontend/src/views/Vadmin/Stock/Review/
git add frontend/src/views/Vadmin/Stock/Experience/
git add frontend/src/views/Vadmin/Stock/RiskRule/
git add frontend/src/api/review.ts
git add frontend/src/api/experience.ts
git add frontend/src/api/riskRule.ts
git commit -m "feat(review): add frontend types and API"
```

---

### Task 5.2: 创建复盘工作台主页面

**Files:**
- Create: `frontend/src/views/Vadmin/Stock/Review/Review.vue`

**Step 1: 编写主页面**

创建完整的复盘工作台页面，包含：
- 复盘类型切换（每日/每周/每月/不定期）
- 市场回顾组件
- 持仓分析组件
- 交易回顾组件
- 心得编辑器
- 计划编辑器
- AI分析按钮

**Step 2: 提交**

```bash
git add frontend/src/views/Vadmin/Stock/Review/
git commit -m "feat(review): add Review main page"
```

---

### Task 5.3: 创建心得经验库主页面

**Files:**
- Create: `frontend/src/views/Vadmin/Stock/Experience/Experience.vue`

**Step 1: 编写主页面**

创建完整的心得经验库页面，包含：
- 四种视图切换（时间线/分类/关联/搜索）
- 分类筛选
- 标签筛选
- 心得卡片列表
- 新增/编辑心得弹窗

**Step 2: 提交**

```bash
git add frontend/src/views/Vadmin/Stock/Experience/
git commit -m "feat(review): add Experience main page"
```

---

### Task 5.4: 创建雷区基线主页面

**Files:**
- Create: `frontend/src/views/Vadmin/Stock/RiskRule/RiskRule.vue`

**Step 1: 编写主页面**

创建完整的雷区基线页面，包含：
- 雷区列表（负面清单）
- 基线列表（正面清单）
- 违规记录列表
- 规则编辑弹窗
- 应用预设规则按钮

**Step 2: 提交**

```bash
git add frontend/src/views/Vadmin/Stock/RiskRule/
git commit -m "feat(review): add RiskRule main page"
```

---

## Phase 6: 模块联动（1天）

### Task 6.1: 实现与投资组合联动

**Files:**
- Modify: `backend/apps/admin/review/services/review_service.py`

**Step 1: 完善复盘服务**

在 ReviewService 中完善：
- `generate_position_summary` - 从投资组合获取持仓数据
- `generate_trade_summary` - 从投资组合获取交易记录
- `generate_profit_summary` - 从投资组合获取盈亏统计

**Step 2: 提交**

```bash
git add backend/apps/admin/review/services/
git commit -m "feat(review): integrate with portfolio module"
```

---

### Task 6.2: 实现交易前风控检查

**Files:**
- Modify: `backend/apps/admin/portfolio/views.py`

**Step 1: 在交易API中集成风控检查**

在买入/卖出API中调用 RuleService 进行交易前检查。

**Step 2: 提交**

```bash
git add backend/apps/admin/portfolio/views.py
git commit -m "feat(review): integrate pre-trade risk check"
```

---

## Phase 7: 测试与优化（1天）

### Task 7.1: 验证API功能

**Step 1: 启动后端服务**

```bash
cd backend
uv run python main.py run
```

**Step 2: 测试API端点**

访问 `http://localhost:9000/docs` 测试所有API端点。

**Step 3: 提交**

```bash
git add -A
git commit -m "test(review): verify API functionality"
```

---

## 文件清单汇总

### 后端文件

```
backend/apps/admin/review/
├── __init__.py
├── views.py
├── models/
│   ├── __init__.py
│   ├── review_record.py
│   ├── experience_note.py
│   ├── risk_rule.py
│   └── rule_violation.py
├── schemas/
│   ├── __init__.py
│   ├── review.py
│   ├── experience.py
│   └── rule.py
├── crud/
│   ├── __init__.py
│   ├── review_crud.py
│   ├── experience_crud.py
│   └── rule_crud.py
└── services/
    ├── __init__.py
    ├── review_service.py
    ├── experience_service.py
    └── rule_service.py
```

### 前端文件

```
frontend/src/views/Vadmin/Stock/Review/
├── Review.vue
├── components/
│   ├── MarketReview.vue
│   ├── PositionReview.vue
│   ├── TradeReview.vue
│   ├── NotesEditor.vue
│   └── PlanEditor.vue
└── types/
    └── review.ts

frontend/src/views/Vadmin/Stock/Experience/
├── Experience.vue
├── components/
│   ├── NoteCard.vue
│   └── NoteEditor.vue
└── types/
    └── experience.ts

frontend/src/views/Vadmin/Stock/RiskRule/
├── RiskRule.vue
├── components/
│   ├── TrapList.vue
│   ├── BaselineList.vue
│   ├── RuleEditor.vue
│   └── ViolationList.vue
└── types/
    └── rule.ts

frontend/src/api/
├── review.ts
├── experience.ts
└── riskRule.ts
```

---

**文档版本**: v1.0
**创建日期**: 2026-03-22
**预估工期**: 13个工作日