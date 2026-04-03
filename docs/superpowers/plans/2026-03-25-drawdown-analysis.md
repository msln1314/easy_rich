# 股票回撤分析系统实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建综合回撤分析系统，包含回撤分析、回调买点信号、持仓监控三大功能。

**Architecture:** 后端采用FastAPI + Pydantic模型，服务层封装回撤计算逻辑；前端采用Vue3 + Element Plus，使用ECharts展示回撤图表。

**Tech Stack:** Python, FastAPI, Pydantic, akshare, Vue 3, TypeScript, Element Plus, ECharts

---

## 文件结构

```
backend/stock-service/
├── app/models/
│   └── drawdown_models.py       # 数据模型定义
├── app/services/
│   └── drawdown_service.py      # 回撤分析核心服务
├── app/api/endpoints/
│   └── drawdown_routes.py       # API路由

frontend/src/
├── api/stock/
│   └── drawdown.ts              # API接口封装
└── views/Vadmin/Stock/Drawdown/
    ├── Drawdown.vue             # 主页面
    └── components/
        ├── DrawdownAnalysis.vue # 回撤分析组件
        ├── PullbackSignal.vue   # 回调买点组件
        └── PositionMonitor.vue  # 持仓监控组件
```

---

## Phase 1: 后端数据模型

### Task 1.1: 创建回撤数据模型

**Files:**
- Create: `backend/stock-service/app/models/drawdown_models.py`

- [ ] **Step 1: 创建数据模型文件**

```python
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
```

- [ ] **Step 2: 验证模型导入**

Run: `cd backend/stock-service && python -c "from app.models.drawdown_models import DrawdownPoint; print('OK')"`
Expected: OK

- [ ] **Step 3: 提交**

```bash
git add backend/stock-service/app/models/drawdown_models.py
git commit -m "feat(drawdown): add drawdown data models"
```

---

## Phase 2: 后端核心服务

### Task 2.1: 创建回撤分析服务

**Files:**
- Create: `backend/stock-service/app/services/drawdown_service.py`

- [ ] **Step 1: 创建服务骨架**

```python
# backend/stock-service/app/services/drawdown_service.py
# -*- coding: utf-8 -*-
"""
回撤分析服务
"""
import numpy as np
from datetime import date, timedelta
from typing import List, Optional, Tuple
from app.models.drawdown_models import (
    DrawdownPoint,
    DrawdownAnalysisResult,
    PullbackSignal,
    PositionMonitor,
    DrawdownHistoryData,
)
from app.services.stock_service import StockService
from app.core.logging import get_logger

logger = get_logger(__name__)


class DrawdownService:
    """回撤分析服务"""

    def __init__(self):
        self.stock_service = StockService()

    async def analyze_drawdown(
        self,
        stock_code: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> DrawdownAnalysisResult:
        """
        回撤分析主流程

        Args:
            stock_code: 股票代码
            start_date: 开始日期，默认一年前
            end_date: 结束日期，默认今天

        Returns:
            DrawdownAnalysisResult: 分析结果
        """
        # 设置默认日期范围
        if end_date is None:
            end_date = date.today()
        if start_date is None:
            start_date = end_date - timedelta(days=365)

        # 获取K线数据
        klines = await self._get_klines(stock_code, start_date, end_date)
        if not klines or len(klines) < 10:
            raise ValueError(f"股票 {stock_code} K线数据不足")

        # 提取价格序列
        dates = [k["trade_date"] for k in klines]
        closes = [float(k["close"]) for k in klines]

        # 识别回撤点
        drawdown_points = self._find_drawdown_points(dates, closes)

        # 计算统计指标
        stats = self._calculate_statistics(drawdown_points)

        # 获取股票名称
        stock_name = klines[0].get("name", stock_code)

        return DrawdownAnalysisResult(
            stock_code=stock_code,
            stock_name=stock_name,
            analysis_period=f"{start_date} ~ {end_date}",
            max_drawdown=stats["max_drawdown"],
            max_drawdown_duration=stats["max_drawdown_duration"],
            avg_drawdown=stats["avg_drawdown"],
            avg_recovery_days=stats["avg_recovery_days"],
            drawdown_5p_count=stats["drawdown_5p_count"],
            drawdown_10p_count=stats["drawdown_10p_count"],
            drawdown_20p_count=stats["drawdown_20p_count"],
            drawdown_30p_count=stats["drawdown_30p_count"],
            drawdown_points=drawdown_points,
        )

    async def get_pullback_signals(self, stock_code: str) -> List[PullbackSignal]:
        """
        获取回调买点信号

        Args:
            stock_code: 股票代码

        Returns:
            List[PullbackSignal]: 信号列表
        """
        signals = []

        # 获取近期K线
        end_date = date.today()
        start_date = end_date - timedelta(days=60)
        klines = await self._get_klines(stock_code, start_date, end_date)

        if not klines or len(klines) < 20:
            return signals

        closes = [float(k["close"]) for k in klines]
        volumes = [float(k.get("volume", 0)) for k in klines]
        dates = [k["trade_date"] for k in klines]

        # 计算技术指标
        ma20 = np.mean(closes[-20:])
        ma60 = np.mean(closes[-min(60, len(closes)):]) if len(closes) >= 60 else None
        current_price = closes[-1]

        # 计算当前回撤
        recent_high = max(closes[-30:])
        current_drawdown = (recent_high - current_price) / recent_high * 100

        # 计算支撑位
        support_levels = self._calculate_support_levels(closes, volumes)

        # 计算信号强度
        strength = 0
        reasoning_parts = []

        # 1. 技术支撑位判断 (40%)
        support_score = 0
        nearest_support = None
        for support in support_levels:
            distance = abs(current_price - support) / current_price * 100
            if distance < 3:  # 3%以内视为接近支撑
                support_score = 20
                nearest_support = support
                reasoning_parts.append(f"接近支撑位{support:.2f}元")
                break

        if ma20 and abs(current_price - ma20) / current_price * 100 < 2:
            support_score += 10
            reasoning_parts.append("接近MA20均线")
        if ma60 and abs(current_price - ma60) / current_price * 100 < 3:
            support_score += 10
            reasoning_parts.append("接近MA60均线")

        strength += support_score

        # 2. 历史回撤规律 (30%)
        history_score = 0
        if current_drawdown > 10:
            history_score = 15
            reasoning_parts.append(f"回调幅度{current_drawdown:.1f}%")
        if current_drawdown > 15:
            history_score = 30
            reasoning_parts.append("深度回调")

        strength += history_score

        # 3. 量价配合 (30%)
        volume_score = 0
        if len(volumes) >= 5:
            avg_volume = np.mean(volumes[-10:-5])
            recent_volume = np.mean(volumes[-5:])
            if recent_volume < avg_volume * 0.7:  # 缩量
                volume_score = 20
                reasoning_parts.append("缩量回调")
            elif recent_volume > avg_volume * 1.2:  # 放量企稳
                volume_score = 15
                reasoning_parts.append("放量迹象")

        strength += volume_score

        # 生成信号
        if strength >= 50 and nearest_support:
            stop_loss = nearest_support * 0.95  # 止损位为支撑位下方5%
            signals.append(PullbackSignal(
                signal_date=date.today(),
                signal_type="support" if support_score > 15 else "volume",
                signal_strength=strength,
                current_drawdown=round(current_drawdown, 2),
                support_price=round(nearest_support, 2),
                stop_loss_price=round(stop_loss, 2),
                reasoning="；".join(reasoning_parts) if reasoning_parts else "综合分析",
            ))

        return signals

    async def monitor_position(
        self,
        stock_code: str,
        cost_price: float,
        position_date: date,
    ) -> PositionMonitor:
        """
        持仓监控

        Args:
            stock_code: 股票代码
            cost_price: 成本价
            position_date: 买入日期

        Returns:
            PositionMonitor: 监控结果
        """
        # 获取K线
        end_date = date.today()
        klines = await self._get_klines(stock_code, position_date, end_date)

        if not klines:
            raise ValueError(f"无法获取股票 {stock_code} 的K线数据")

        closes = [float(k["close"]) for k in klines]
        current_price = closes[-1]
        highest_price = max(closes)

        # 计算各项指标
        profit_percent = (current_price - cost_price) / cost_price * 100
        drawdown_from_high = (highest_price - current_price) / highest_price * 100
        drawdown_from_cost = (cost_price - current_price) / cost_price * 100 if current_price < cost_price else 0

        # 计算建议止盈价
        if profit_percent > 20:
            suggested_stop_profit = highest_price * 0.9  # 回撤10%止盈
        elif profit_percent > 10:
            suggested_stop_profit = highest_price * 0.85
        else:
            suggested_stop_profit = cost_price * 1.02  # 微利保本

        # 判断警告级别
        if drawdown_from_high > 15 or profit_percent < -10:
            alert_level = "警告"
        elif drawdown_from_high > 10 or profit_percent < -5:
            alert_level = "注意"
        else:
            alert_level = "正常"

        return PositionMonitor(
            stock_code=stock_code,
            cost_price=cost_price,
            current_price=round(current_price, 2),
            highest_price=round(highest_price, 2),
            profit_percent=round(profit_percent, 2),
            drawdown_from_high=round(drawdown_from_high, 2),
            drawdown_from_cost=round(drawdown_from_cost, 2),
            suggested_stop_profit=round(suggested_stop_profit, 2),
            alert_level=alert_level,
        )

    async def get_history_data(
        self,
        stock_code: str,
        threshold: float = 5.0,
    ) -> DrawdownHistoryData:
        """
        获取历史回撤图表数据

        Args:
            stock_code: 股票代码
            threshold: 回撤阈值(%)

        Returns:
            DrawdownHistoryData: 图表数据
        """
        end_date = date.today()
        start_date = end_date - timedelta(days=365)
        klines = await self._get_klines(stock_code, start_date, end_date)

        if not klines:
            return DrawdownHistoryData()

        dates = [k["trade_date"] for k in klines]
        closes = [float(k["close"]) for k in klines]

        # 计算回撤区域
        drawdown_areas = self._calculate_drawdown_areas(dates, closes, threshold)

        return DrawdownHistoryData(
            dates=dates,
            prices=closes,
            drawdown_areas=drawdown_areas,
        )

    # ========== 私有方法 ==========

    async def _get_klines(
        self,
        stock_code: str,
        start_date: date,
        end_date: date,
    ) -> List[dict]:
        """获取K线数据"""
        try:
            import akshare as ak

            df = ak.stock_zh_a_hist(
                symbol=stock_code,
                period="daily",
                start_date=start_date.strftime("%Y%m%d"),
                end_date=end_date.strftime("%Y%m%d"),
                adjust="qfq",
            )

            if df.empty:
                return []

            return df.to_dict("records")
        except Exception as e:
            logger.error(f"获取K线数据失败: {e}")
            return []

    def _find_drawdown_points(
        self,
        dates: List[str],
        prices: List[float],
    ) -> List[DrawdownPoint]:
        """
        识别所有回撤波段

        算法：
        1. 找局部峰值
        2. 向后搜索谷值
        3. 计算回撤幅度
        4. 搜索恢复点
        """
        if len(prices) < 3:
            return []

        points = []
        i = 0
        n = len(prices)

        while i < n - 1:
            # 找局部峰值
            if i == 0 or prices[i] > prices[i - 1]:
                # 向后搜索确认峰值
                peak_idx = i
                peak_price = prices[i]

                for j in range(i + 1, n):
                    if prices[j] > peak_price:
                        peak_price = prices[j]
                        peak_idx = j
                    elif prices[j] < peak_price * 0.95:  # 回撤超过5%
                        break

                if peak_idx == i:
                    i += 1
                    continue

                # 从峰值向后搜索谷值
                trough_idx = peak_idx
                trough_price = prices[peak_idx]

                for j in range(peak_idx + 1, n):
                    if prices[j] < trough_price:
                        trough_price = prices[j]
                        trough_idx = j
                    elif prices[j] > peak_price:  # 恢复前高
                        break

                # 计算回撤幅度
                drawdown = (peak_price - trough_price) / peak_price * 100

                if drawdown >= 5:
                    # 搜索恢复点
                    recovery_idx = None
                    for j in range(trough_idx + 1, n):
                        if prices[j] >= peak_price:
                            recovery_idx = j
                            break

                    points.append(DrawdownPoint(
                        peak_date=self._parse_date(dates[peak_idx]),
                        peak_price=round(peak_price, 2),
                        trough_date=self._parse_date(dates[trough_idx]),
                        trough_price=round(trough_price, 2),
                        drawdown_percent=round(drawdown, 2),
                        duration_days=trough_idx - peak_idx,
                        recovery_date=self._parse_date(dates[recovery_idx]) if recovery_idx else None,
                        recovery_days=(recovery_idx - trough_idx) if recovery_idx else None,
                    ))

                i = trough_idx + 1
            else:
                i += 1

        return points

    def _calculate_statistics(self, points: List[DrawdownPoint]) -> dict:
        """计算统计指标"""
        if not points:
            return {
                "max_drawdown": 0,
                "max_drawdown_duration": 0,
                "avg_drawdown": 0,
                "avg_recovery_days": 0,
                "drawdown_5p_count": 0,
                "drawdown_10p_count": 0,
                "drawdown_20p_count": 0,
                "drawdown_30p_count": 0,
            }

        drawdowns = [p.drawdown_percent for p in points]
        durations = [p.duration_days for p in points]
        recoveries = [p.recovery_days for p in points if p.recovery_days is not None]

        return {
            "max_drawdown": round(max(drawdowns), 2),
            "max_drawdown_duration": max(durations),
            "avg_drawdown": round(np.mean(drawdowns), 2),
            "avg_recovery_days": round(np.mean(recoveries), 1) if recoveries else 0,
            "drawdown_5p_count": sum(1 for d in drawdowns if d >= 5),
            "drawdown_10p_count": sum(1 for d in drawdowns if d >= 10),
            "drawdown_20p_count": sum(1 for d in drawdowns if d >= 20),
            "drawdown_30p_count": sum(1 for d in drawdowns if d >= 30),
        }

    def _calculate_support_levels(
        self,
        closes: List[float],
        volumes: List[float],
    ) -> List[float]:
        """计算技术支撑位"""
        supports = []

        # MA20
        if len(closes) >= 20:
            supports.append(np.mean(closes[-20:]))

        # MA60
        if len(closes) >= 60:
            supports.append(np.mean(closes[-60:]))

        # 前低点（最近30天最低价）
        if len(closes) >= 30:
            supports.append(min(closes[-30:]))

        # 布林带下轨
        if len(closes) >= 20:
            ma = np.mean(closes[-20:])
            std = np.std(closes[-20:])
            supports.append(ma - 2 * std)

        return sorted(set(round(s, 2) for s in supports))

    def _calculate_drawdown_areas(
        self,
        dates: List[str],
        prices: List[float],
        threshold: float,
    ) -> List[dict]:
        """计算回撤区域用于图表展示"""
        areas = []
        points = self._find_drawdown_points(dates, prices)

        for p in points:
            if p.drawdown_percent >= threshold:
                areas.append({
                    "start": str(p.peak_date),
                    "end": str(p.trough_date),
                    "depth": round(-p.drawdown_percent, 2),
                })

        return areas

    def _parse_date(self, date_str: str) -> date:
        """解析日期字符串"""
        if isinstance(date_str, date):
            return date_str
        if isinstance(date_str, str):
            return date.fromisoformat(date_str.replace("/", "-"))
        return date.today()
```

- [ ] **Step 2: 验证服务导入**

Run: `cd backend/stock-service && python -c "from app.services.drawdown_service import DrawdownService; print('OK')"`
Expected: OK

- [ ] **Step 3: 提交**

```bash
git add backend/stock-service/app/services/drawdown_service.py
git commit -m "feat(drawdown): add drawdown analysis service"
```

---

## Phase 3: 后端API路由

### Task 3.1: 创建API路由

**Files:**
- Create: `backend/stock-service/app/api/endpoints/drawdown_routes.py`
- Modify: `backend/stock-service/app/api/router.py`

- [ ] **Step 1: 创建路由文件**

```python
# backend/stock-service/app/api/endpoints/drawdown_routes.py
# -*- coding: utf-8 -*-
"""
回撤分析API路由
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from datetime import date

from app.models.drawdown_models import (
    DrawdownAnalysisResult,
    PullbackSignal,
    PositionMonitor,
    DrawdownHistoryData,
    DrawdownAnalyzeRequest,
    PositionMonitorRequest,
)
from app.services.drawdown_service import DrawdownService

router = APIRouter()
drawdown_service = DrawdownService()


@router.post("/analyze", response_model=DrawdownAnalysisResult)
async def analyze_drawdown(request: DrawdownAnalyzeRequest):
    """
    回撤分析

    分析指定股票的历史回撤情况，返回各项指标
    """
    try:
        result = await drawdown_service.analyze_drawdown(
            stock_code=request.stock_code,
            start_date=request.start_date,
            end_date=request.end_date,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析失败: {str(e)}")


@router.get("/signals/{stock_code}", response_model=list[PullbackSignal])
async def get_pullback_signals(stock_code: str):
    """
    获取回调买点信号

    基于技术支撑位、历史回撤规律、量价配合判断买点
    """
    try:
        signals = await drawdown_service.get_pullback_signals(stock_code)
        return signals
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取信号失败: {str(e)}")


@router.post("/position", response_model=PositionMonitor)
async def monitor_position(request: PositionMonitorRequest):
    """
    持仓监控

    输入成本价和买入日期，监控盈利/亏损和回撤情况
    """
    try:
        result = await drawdown_service.monitor_position(
            stock_code=request.stock_code,
            cost_price=request.cost_price,
            position_date=request.position_date,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"监控失败: {str(e)}")


@router.get("/history/{stock_code}", response_model=DrawdownHistoryData)
async def get_history_data(
    stock_code: str,
    threshold: float = Query(5.0, ge=1, le=50, description="回撤阈值(%)"),
):
    """
    获取历史回撤图表数据

    用于前端ECharts展示回撤走势图
    """
    try:
        result = await drawdown_service.get_history_data(stock_code, threshold)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取历史数据失败: {str(e)}")
```

- [ ] **Step 2: 注册路由到router.py**

在 `backend/stock-service/app/api/router.py` 中添加：

```python
# 在导入部分添加
try:
    from app.api.endpoints import drawdown_routes
except ImportError:
    print("警告: 无法导入 drawdown_routes 模块")
    drawdown_routes = None

# 在路由注册部分添加
if drawdown_routes:
    api_router.include_router(
        drawdown_routes.router, prefix="/drawdown", tags=["drawdown"]
    )
```

- [ ] **Step 3: 验证路由注册**

Run: `cd backend/stock-service && python -c "from app.api.router import api_router; print('OK')"`
Expected: OK

- [ ] **Step 4: 提交**

```bash
git add backend/stock-service/app/api/endpoints/drawdown_routes.py backend/stock-service/app/api/router.py
git commit -m "feat(drawdown): add drawdown API routes"
```

---

## Phase 4: 前端API封装

### Task 4.1: 创建前端API文件

**Files:**
- Create: `frontend/src/api/stock/drawdown.ts`

- [ ] **Step 1: 创建API封装**

```typescript
// frontend/src/api/stock/drawdown.ts
import request from '@/config/axios'

// ========== 类型定义 ==========

export interface DrawdownPoint {
  peak_date: string
  peak_price: number
  trough_date: string
  trough_price: number
  drawdown_percent: number
  duration_days: number
  recovery_date?: string
  recovery_days?: number
}

export interface DrawdownAnalysisResult {
  stock_code: string
  stock_name: string
  analysis_period: string
  max_drawdown: number
  max_drawdown_duration: number
  avg_drawdown: number
  avg_recovery_days: number
  drawdown_5p_count: number
  drawdown_10p_count: number
  drawdown_20p_count: number
  drawdown_30p_count: number
  drawdown_points: DrawdownPoint[]
}

export interface PullbackSignal {
  signal_date: string
  signal_type: string
  signal_strength: number
  current_drawdown: number
  support_price: number
  stop_loss_price: number
  reasoning: string
}

export interface PositionMonitor {
  stock_code: string
  cost_price: number
  current_price: number
  highest_price: number
  profit_percent: number
  drawdown_from_high: number
  drawdown_from_cost: number
  suggested_stop_profit: number
  alert_level: string
}

export interface DrawdownHistoryData {
  dates: string[]
  prices: number[]
  drawdown_areas: Array<{
    start: string
    end: string
    depth: number
  }>
}

// ========== API函数 ==========

/**
 * 回撤分析
 */
export const analyzeDrawdown = (data: {
  stock_code: string
  start_date?: string
  end_date?: string
}): Promise<IResponse<DrawdownAnalysisResult>> => {
  return request.post({ url: '/drawdown/analyze', data })
}

/**
 * 获取回调买点信号
 */
export const getPullbackSignals = (
  stockCode: string
): Promise<IResponse<PullbackSignal[]>> => {
  return request.get({ url: `/drawdown/signals/${stockCode}` })
}

/**
 * 持仓监控
 */
export const monitorPosition = (data: {
  stock_code: string
  cost_price: number
  position_date: string
}): Promise<IResponse<PositionMonitor>> => {
  return request.post({ url: '/drawdown/position', data })
}

/**
 * 获取历史回撤图表数据
 */
export const getDrawdownHistory = (
  stockCode: string,
  threshold: number = 5
): Promise<IResponse<DrawdownHistoryData>> => {
  return request.get({ url: `/drawdown/history/${stockCode}`, params: { threshold } })
}
```

- [ ] **Step 2: 验证导入**

Run: `cd frontend && npm run build 2>&1 | head -20`
Expected: 无错误

- [ ] **Step 3: 提交**

```bash
git add frontend/src/api/stock/drawdown.ts
git commit -m "feat(drawdown): add frontend API"
```

---

## Phase 5: 前端页面组件

### Task 5.1: 创建主页面

**Files:**
- Create: `frontend/src/views/Vadmin/Stock/Drawdown/Drawdown.vue`

- [ ] **Step 1: 创建主页面**

```vue
<!-- frontend/src/views/Vadmin/Stock/Drawdown/Drawdown.vue -->
<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage, ElCard, ElInput, ElButton, ElSelect, ElOption, ElRow, ElCol } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import { ContentWrap } from '@/components/ContentWrap'
import DrawdownAnalysis from './components/DrawdownAnalysis.vue'
import PullbackSignal from './components/PullbackSignal.vue'
import PositionMonitor from './components/PositionMonitor.vue'

defineOptions({
  name: 'DrawdownAnalysis'
})

// 股票代码
const stockCode = ref('')
const loading = ref(false)

// 时间范围选项
const timeRange = ref('1y')
const timeRangeOptions = [
  { label: '近半年', value: '6m' },
  { label: '近一年', value: '1y' },
  { label: '近两年', value: '2y' },
  { label: '近三年', value: '3y' }
]

// 分析结果
const analysisResult = ref<any>(null)

// 执行分析
const handleAnalyze = async () => {
  if (!stockCode.value) {
    ElMessage.warning('请输入股票代码')
    return
  }

  loading.value = true
  try {
    const { analyzeDrawdown } = await import('@/api/stock/drawdown')
    const res = await analyzeDrawdown({
      stock_code: stockCode.value
    })
    if (res.code === 200) {
      analysisResult.value = res.data
      ElMessage.success('分析完成')
    } else {
      ElMessage.error(res.msg || '分析失败')
    }
  } catch (error) {
    ElMessage.error('分析失败')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <ContentWrap>
    <ElCard>
      <template #header>
        <div class="flex items-center justify-between">
          <span class="font-bold text-lg">回撤分析</span>
        </div>
      </template>

      <!-- 搜索栏 -->
      <ElRow :gutter="20" class="mb-4">
        <ElCol :span="6">
          <ElInput
            v-model="stockCode"
            placeholder="请输入股票代码"
            clearable
            @keyup.enter="handleAnalyze"
          />
        </ElCol>
        <ElCol :span="4">
          <ElSelect v-model="timeRange" style="width: 100%">
            <ElOption
              v-for="item in timeRangeOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </ElSelect>
        </ElCol>
        <ElCol :span="4">
          <ElButton type="primary" :icon="Search" :loading="loading" @click="handleAnalyze">
            分析
          </ElButton>
        </ElCol>
      </ElRow>

      <!-- 分析结果 -->
      <template v-if="analysisResult">
        <DrawdownAnalysis :result="analysisResult" class="mb-4" />
        <PullbackSignal :stock-code="stockCode" class="mb-4" />
        <PositionMonitor :stock-code="stockCode" />
      </template>

      <!-- 空状态 -->
      <div v-else class="text-center text-gray-400 py-20">
        请输入股票代码开始分析
      </div>
    </ElCard>
  </ContentWrap>
</template>
```

- [ ] **Step 2: 创建回撤分析组件**

```vue
<!-- frontend/src/views/Vadmin/Stock/Drawdown/components/DrawdownAnalysis.vue -->
<script setup lang="ts">
import { computed } from 'vue'
import { ElCard, ElStatistic, ElRow, ElCol, ElTable, ElTableColumn, ElTag } from 'element-plus'
import type { DrawdownAnalysisResult } from '@/api/stock/drawdown'

const props = defineProps<{
  result: DrawdownAnalysisResult
}>()

// 格式化百分比
const formatPercent = (val: number) => `${val.toFixed(2)}%`

// 表格数据
const tableData = computed(() => props.result.drawdown_points.slice(0, 10))
</script>

<template>
  <ElCard header="回撤概览">
    <ElRow :gutter="20" class="mb-4">
      <ElCol :span="4">
        <ElStatistic title="最大回撤" :value="result.max_drawdown" suffix="%" />
      </ElCol>
      <ElCol :span="4">
        <ElStatistic title="平均回撤" :value="result.avg_drawdown" suffix="%" />
      </ElCol>
      <ElCol :span="4">
        <ElStatistic title="最大持续天数" :value="result.max_drawdown_duration" suffix="天" />
      </ElCol>
      <ElCol :span="4">
        <ElStatistic title="平均恢复天数" :value="result.avg_recovery_days" suffix="天" />
      </ElCol>
    </ElRow>

    <ElRow :gutter="20" class="mb-4">
      <ElCol :span="2">
        <ElTag>5%+: {{ result.drawdown_5p_count }}次</ElTag>
      </ElCol>
      <ElCol :span="2">
        <ElTag type="warning">10%+: {{ result.drawdown_10p_count }}次</ElTag>
      </ElCol>
      <ElCol :span="2">
        <ElTag type="danger">20%+: {{ result.drawdown_20p_count }}次</ElTag>
      </ElCol>
      <ElCol :span="2">
        <ElTag type="danger" effect="dark">30%+: {{ result.drawdown_30p_count }}次</ElTag>
      </ElCol>
    </ElRow>

    <!-- 回撤记录表 -->
    <ElTable :data="tableData" stripe max-height="300">
      <ElTableColumn prop="peak_date" label="峰值日期" width="120" />
      <ElTableColumn prop="peak_price" label="峰值价格" width="100" />
      <ElTableColumn prop="trough_date" label="谷值日期" width="120" />
      <ElTableColumn prop="trough_price" label="谷值价格" width="100" />
      <ElTableColumn prop="drawdown_percent" label="回撤幅度" width="100">
        <template #default="{ row }">
          <ElTag type="danger">-{{ row.drawdown_percent.toFixed(2) }}%</ElTag>
        </template>
      </ElTableColumn>
      <ElTableColumn prop="duration_days" label="持续天数" width="100" />
      <ElTableColumn prop="recovery_days" label="恢复天数" width="100">
        <template #default="{ row }">
          {{ row.recovery_days ?? '-' }}
        </template>
      </ElTableColumn>
    </ElTable>
  </ElCard>
</template>
```

- [ ] **Step 3: 创建回调买点组件**

```vue
<!-- frontend/src/views/Vadmin/Stock/Drawdown/components/PullbackSignal.vue -->
<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { ElCard, ElProgress, ElTag, ElEmpty } from 'element-plus'
import { getPullbackSignals, type PullbackSignal } from '@/api/stock/drawdown'

const props = defineProps<{
  stockCode: string
}>()

const signals = ref<PullbackSignal[]>([])
const loading = ref(false)

const loadSignals = async () => {
  if (!props.stockCode) return
  loading.value = true
  try {
    const res = await getPullbackSignals(props.stockCode)
    if (res.code === 200) {
      signals.value = res.data || []
    }
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

watch(() => props.stockCode, loadSignals)
onMounted(loadSignals)

const getStrengthType = (strength: number) => {
  if (strength >= 70) return 'success'
  if (strength >= 50) return 'warning'
  return 'info'
}
</script>

<template>
  <ElCard header="回调买点信号">
    <template v-if="signals.length > 0">
      <div v-for="signal in signals" :key="signal.signal_date" class="mb-4 p-4 border rounded">
        <div class="flex items-center justify-between mb-2">
          <span>信号强度</span>
          <ElTag :type="getStrengthType(signal.signal_strength)">
            {{ signal.signal_strength >= 70 ? '强买点' : signal.signal_strength >= 50 ? '中等买点' : '观望' }}
          </ElTag>
        </div>
        <ElProgress
          :percentage="signal.signal_strength"
          :status="getStrengthType(signal.signal_strength)"
          class="mb-2"
        />
        <div class="grid grid-cols-3 gap-4 text-sm">
          <div>
            <span class="text-gray-500">当前回调:</span>
            <ElTag type="danger" class="ml-1">{{ signal.current_drawdown.toFixed(2) }}%</ElTag>
          </div>
          <div>
            <span class="text-gray-500">支撑位:</span>
            <span class="ml-1 font-bold">{{ signal.support_price }}</span>
          </div>
          <div>
            <span class="text-gray-500">建议止损:</span>
            <span class="ml-1">{{ signal.stop_loss_price }}</span>
          </div>
        </div>
        <div class="mt-2 text-sm text-gray-600">{{ signal.reasoning }}</div>
      </div>
    </template>
    <ElEmpty v-else description="暂无买点信号" />
  </ElCard>
</template>
```

- [ ] **Step 4: 创建持仓监控组件**

```vue
<!-- frontend/src/views/Vadmin/Stock/Drawdown/components/PositionMonitor.vue -->
<script setup lang="ts">
import { ref } from 'vue'
import { ElCard, ElForm, ElFormItem, ElInputNumber, ElDatePicker, ElButton, ElRow, ElCol, ElTag, ElAlert } from 'element-plus'
import { monitorPosition, type PositionMonitor as PositionMonitorType } from '@/api/stock/drawdown'

const props = defineProps<{
  stockCode: string
}>()

const form = ref({
  costPrice: null as number | null,
  positionDate: null as Date | null
})

const monitorData = ref<PositionMonitorType | null>(null)
const loading = ref(false)

const handleMonitor = async () => {
  if (!props.stockCode || !form.value.costPrice || !form.value.positionDate) {
    return
  }

  loading.value = true
  try {
    const res = await monitorPosition({
      stock_code: props.stockCode,
      cost_price: form.value.costPrice,
      position_date: form.value.positionDate.toISOString().split('T')[0]
    })
    if (res.code === 200) {
      monitorData.value = res.data
    }
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

const getAlertType = (level: string) => {
  if (level === '警告') return 'error'
  if (level === '注意') return 'warning'
  return 'success'
}
</script>

<template>
  <ElCard header="持仓监控">
    <ElForm :inline="true" class="mb-4">
      <ElFormItem label="成本价">
        <ElInputNumber v-model="form.costPrice" :min="0" :precision="2" />
      </ElFormItem>
      <ElFormItem label="买入日期">
        <ElDatePicker v-model="form.positionDate" type="date" />
      </ElFormItem>
      <ElFormItem>
        <ElButton type="primary" :loading="loading" @click="handleMonitor">监控</ElButton>
      </ElFormItem>
    </ElForm>

    <template v-if="monitorData">
      <ElAlert
        v-if="monitorData.alert_level !== '正常'"
        :title="`${monitorData.alert_level}：从最高点回撤 ${monitorData.drawdown_from_high}%`"
        :type="getAlertType(monitorData.alert_level)"
        show-icon
        class="mb-4"
      />

      <ElRow :gutter="20">
        <ElCol :span="4">
          <div class="text-gray-500">当前价</div>
          <div class="text-xl font-bold">{{ monitorData.current_price }}</div>
        </ElCol>
        <ElCol :span="4">
          <div class="text-gray-500">盈亏</div>
          <ElTag :type="monitorData.profit_percent >= 0 ? 'success' : 'danger'" size="large">
            {{ monitorData.profit_percent >= 0 ? '+' : '' }}{{ monitorData.profit_percent }}%
          </ElTag>
        </ElCol>
        <ElCol :span="4">
          <div class="text-gray-500">最高价</div>
          <div class="text-xl">{{ monitorData.highest_price }}</div>
        </ElCol>
        <ElCol :span="4">
          <div class="text-gray-500">从高点回撤</div>
          <ElTag type="warning">{{ monitorData.drawdown_from_high }}%</ElTag>
        </ElCol>
        <ElCol :span="4">
          <div class="text-gray-500">建议止盈价</div>
          <div class="text-xl font-bold text-primary">{{ monitorData.suggested_stop_profit }}</div>
        </ElCol>
      </ElRow>
    </template>
  </ElCard>
</template>
```

- [ ] **Step 5: 提交前端代码**

```bash
git add frontend/src/views/Vadmin/Stock/Drawdown/
git commit -m "feat(drawdown): add frontend components"
```

---

## Phase 6: 路由配置

### Task 6.1: 添加前端路由

**Files:**
- Modify: `frontend/src/router/index.ts`

- [ ] **Step 1: 添加路由配置**

在 `frontend/src/router/index.ts` 的 `asyncRouterMap` 中 `Stock` 的 `children` 数组添加：

```typescript
{
  path: 'drawdown',
  component: () => import('@/views/Vadmin/Stock/Drawdown/Drawdown.vue'),
  name: 'DrawdownAnalysis',
  meta: { title: '回撤分析', noCache: true }
}
```

- [ ] **Step 2: 验证路由**

Run: `cd frontend && npm run build 2>&1 | tail -5`
Expected: 构建成功

- [ ] **Step 3: 提交**

```bash
git add frontend/src/router/index.ts
git commit -m "feat(drawdown): add route configuration"
```

---

## Phase 7: 集成测试

### Task 7.1: 验证功能

- [ ] **Step 1: 启动后端服务**

Run: `cd backend/stock-service && uvicorn app.main:app --reload --port 8001`

- [ ] **Step 2: 测试API**

```bash
# 测试回撤分析
curl -X POST "http://localhost:8001/api/v1/drawdown/analyze" \
  -H "Content-Type: application/json" \
  -d '{"stock_code": "000001"}'

# 测试回调信号
curl "http://localhost:8001/api/v1/drawdown/signals/000001"

# 测试持仓监控
curl -X POST "http://localhost:8001/api/v1/drawdown/position" \
  -H "Content-Type: application/json" \
  -d '{"stock_code": "000001", "cost_price": 12.0, "position_date": "2024-01-01"}'
```

- [ ] **Step 3: 启动前端验证**

Run: `cd frontend && npm run dev`

---

## 文件清单汇总

### 新建文件

| 文件路径 | 说明 |
|---------|------|
| `backend/stock-service/app/models/drawdown_models.py` | 数据模型 |
| `backend/stock-service/app/services/drawdown_service.py` | 核心服务 |
| `backend/stock-service/app/api/endpoints/drawdown_routes.py` | API路由 |
| `frontend/src/api/stock/drawdown.ts` | 前端API |
| `frontend/src/views/Vadmin/Stock/Drawdown/Drawdown.vue` | 主页面 |
| `frontend/src/views/Vadmin/Stock/Drawdown/components/DrawdownAnalysis.vue` | 分析组件 |
| `frontend/src/views/Vadmin/Stock/Drawdown/components/PullbackSignal.vue` | 买点组件 |
| `frontend/src/views/Vadmin/Stock/Drawdown/components/PositionMonitor.vue` | 监控组件 |

### 修改文件

| 文件路径 | 修改内容 |
|---------|---------|
| `backend/stock-service/app/api/router.py` | 添加drawdown路由注册 |
| `frontend/src/router/index.ts` | 添加页面路由 |