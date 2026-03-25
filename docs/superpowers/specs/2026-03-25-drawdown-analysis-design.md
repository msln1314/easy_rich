# 股票回撤分析系统设计规范

## 一、需求概述

构建综合回撤分析系统，包含三个核心功能模块：

| 模块 | 功能 |
|------|------|
| 回撤分析 | 最大回撤幅度、回撤持续时间、回撤恢复天数、不同幅度回撤次数统计 |
| 回调买点 | 技术支撑位确认、历史回撤规律、量价配合判断 |
| 持仓监控 | 成本回撤监控、最高点回撤提醒、动态止盈建议 |

**使用场景**：单股分析，辅助投资决策。

---

## 二、整体架构

```
backend/stock-service/
├── app/services/
│   └── drawdown_service.py      # 回撤分析核心服务
├── app/api/endpoints/
│   └── drawdown_routes.py       # API路由
├── app/models/
│   └── drawdown_models.py       # 数据模型

frontend/src/
├── api/stock/
│   └── drawdown.ts              # API接口
└── views/Vadmin/Stock/Drawdown/
    ├── Drawdown.vue             # 主页面
    └── components/
        ├── DrawdownAnalysis.vue # 回撤分析组件
        ├── PullbackSignal.vue   # 回调买点组件
        └── PositionMonitor.vue  # 持仓监控组件
```

**数据流：**
```
用户输入股票代码 → 后端获取K线 → 计算回撤指标 → 返回分析结果 → 前端可视化展示
```

---

## 三、数据模型

### 3.1 DrawdownPoint - 单次回撤记录

```python
class DrawdownPoint(BaseModel):
    peak_date: date           # 峰值日期
    peak_price: float         # 峰值价格
    trough_date: date         # 谷值日期
    trough_price: float       # 谷值价格
    drawdown_percent: float   # 回撤幅度(%)
    duration_days: int        # 回撤持续天数
    recovery_date: Optional[date]  # 恢复日期
    recovery_days: Optional[int]   # 恢复天数
```

### 3.2 DrawdownAnalysisResult - 回撤分析结果

```python
class DrawdownAnalysisResult(BaseModel):
    stock_code: str
    stock_name: str
    analysis_period: str      # 分析周期

    # 核心指标
    max_drawdown: float       # 最大回撤(%)
    max_drawdown_duration: int # 最大回撤持续天数
    avg_drawdown: float       # 平均回撤(%)
    avg_recovery_days: float  # 平均恢复天数

    # 回撤次数统计
    drawdown_5p_count: int    # 5%以上回撤次数
    drawdown_10p_count: int   # 10%以上回撤次数
    drawdown_20p_count: int   # 20%以上回撤次数
    drawdown_30p_count: int   # 30%以上回撤次数

    # 详细回撤记录
    drawdown_points: List[DrawdownPoint]
```

### 3.3 PullbackSignal - 回调买入信号

```python
class PullbackSignal(BaseModel):
    signal_date: date
    signal_type: str          # support/volume/pattern
    signal_strength: float    # 信号强度0-100
    current_drawdown: float   # 当前回调幅度
    support_price: float      # 支撑位价格
    stop_loss_price: float    # 建议止损价
    reasoning: str            # 信号理由
```

### 3.4 PositionMonitor - 持仓监控

```python
class PositionMonitor(BaseModel):
    stock_code: str
    cost_price: float         # 成本价
    current_price: float
    highest_price: float      # 持仓期间最高价
    profit_percent: float     # 当前盈利(%)
    drawdown_from_high: float # 从最高点回撤(%)
    drawdown_from_cost: float # 从成本回撤(%)
    suggested_stop_profit: float  # 建议止盈价
    alert_level: str          # 正常/注意/警告
```

---

## 四、核心服务逻辑

### 4.1 DrawdownService 类

```python
class DrawdownService:

    async def analyze_drawdown(
        self,
        stock_code: str,
        start_date: date,
        end_date: date
    ) -> DrawdownAnalysisResult:
        """
        回撤分析主流程：
        1. 获取日K线数据
        2. 计算累计最高点
        3. 识别所有回撤波段（峰值→谷值→恢复）
        4. 统计各项指标
        """

    async def get_pullback_signals(
        self,
        stock_code: str
    ) -> List[PullbackSignal]:
        """
        回调买点检测：
        1. 技术支撑位：均线、前低、布林带下轨
        2. 历史规律：统计该股历史有效回调幅度
        3. 量价配合：缩量回调、放量企稳
        """

    async def monitor_position(
        self,
        stock_code: str,
        cost_price: float,
        position_date: date
    ) -> PositionMonitor:
        """
        持仓监控：
        1. 计算当前盈利/亏损
        2. 追踪持仓期间最高价
        3. 计算从最高点回撤幅度
        4. 生成动态止盈建议
        """

    def _find_drawdown_points(self, prices: List[float]) -> List[DrawdownPoint]:
        """识别所有回撤波段（核心算法）"""
        # 使用波峰波谷检测算法
        # 回撤定义：从峰值下跌超过5%且未恢复前高

    def _calculate_support_levels(self, klines: List[Dict]) -> List[float]:
        """计算技术支撑位"""
        # MA20/MA60、前低点、布林带下轨
```

### 4.2 回撤识别算法

```
输入: 价格序列 prices[]
输出: 回撤点列表 drawdown_points[]

算法流程:
1. 找所有局部峰值 (peak): prices[i] > prices[i-1] && prices[i] > prices[i+1]
2. 对每个峰值，向后搜索谷值 (trough): 谷值 = min(prices[peak_index:end])
3. 计算回撤幅度 = (peak - trough) / peak * 100
4. 如果回撤幅度 >= 5%，记录一次回撤
5. 搜索恢复点: 从谷值后第一个价格 >= 峰值的位置
6. 统计指标: 最大值、平均值、次数分布
```

### 4.3 回调买点判断逻辑

```
信号强度计算 (0-100):

1. 技术支撑位确认 (权重40%):
   - 价格接近MA20/MA60: +20分
   - 价格接近前低点: +10分
   - 布林带下轨支撑: +10分

2. 历史回撤规律 (权重30%):
   - 当前回调幅度接近历史平均有效回调: +15分
   - 历史该幅度反弹概率 > 60%: +15分

3. 量价配合 (权重30%):
   - 回调过程中缩量: +10分
   - 企稳时放量: +10分
   - 量价背离: +10分

信号强度 >= 70: 强买点
信号强度 50-70: 中等买点
信号强度 < 50: 观望
```

---

## 五、API接口设计

### 5.1 回撤分析

```
POST /api/v1/drawdown/analyze

请求体:
{
    "stock_code": "000001",
    "start_date": "2024-01-01",
    "end_date": "2024-12-31"
}

响应:
{
    "code": 200,
    "data": DrawdownAnalysisResult
}
```

### 5.2 回调买点信号

```
GET /api/v1/drawdown/signals/{stock_code}

响应:
{
    "code": 200,
    "data": [PullbackSignal, ...]
}
```

### 5.3 持仓监控

```
POST /api/v1/drawdown/position

请求体:
{
    "stock_code": "000001",
    "cost_price": 15.00,
    "position_date": "2024-01-15"
}

响应:
{
    "code": 200,
    "data": PositionMonitor
}
```

### 5.4 历史回撤图表

```
GET /api/v1/drawdown/history/{stock_code}?threshold=5

响应:
{
    "code": 200,
    "data": {
        "dates": ["2024-01-01", ...],
        "prices": [10.5, ...],
        "drawdown_areas": [
            {"start": "2024-02-01", "end": "2024-03-15", "depth": -15.2},
            ...
        ]
    }
}
```

---

## 六、前端页面设计

### 6.1 页面布局

```
┌─────────────────────────────────────────────────────────────┐
│ 回撤分析                                                    │
├─────────────────────────────────────────────────────────────┤
│ 股票代码: [____000001____] [分析]    时间范围: [近一年 ▼]   │
├─────────────────────────────────────────────────────────────┤
│ ┌─回撤概览──────────────────────────────────────────────┐  │
│ │ 最大回撤: -23.5%    平均回撤: -8.2%    回撤次数: 12    │  │
│ │ 持续天数: 45天      恢复天数: 32天    5%以上: 8次      │  │
│ └───────────────────────────────────────────────────────┘  │
│ ┌─回撤走势图────────────────────────────────────────────┐  │
│ │ [价格曲线 + 回撤区域标注 + 峰值/谷值标记]              │  │
│ └───────────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│ ┌─回调买点信号──────────────────────────────────────────┐  │
│ │ 当前回调: -12.3%  信号强度: ████████░░ 80%             │  │
│ │ 支撑位: 12.50元   建议止损: 11.80元                    │  │
│ │ 理由: 回调至MA20支撑位，缩量企稳，历史该幅度反弹概率68% │  │
│ └───────────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│ ┌─持仓监控──────────────────────────────────────────────┐  │
│ │ 成本价: [___15.00___] 买入日期: [2024-01-15]  [监控]   │  │
│ │ 当前价: 13.50  盈亏: -10.0%  最高: 16.80               │  │
│ │ 从高点回撤: -19.6%  ⚠️ 建议: 跌破13.20考虑止盈         │  │
│ └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 6.2 组件说明

| 组件 | 功能 |
|------|------|
| `DrawdownAnalysis.vue` | 回撤概览 + 走势图（使用ECharts） |
| `PullbackSignal.vue` | 回调买点信号卡片 |
| `PositionMonitor.vue` | 持仓成本输入 + 监控面板 |

### 6.3 路由配置

```typescript
{
  path: 'drawdown',
  component: () => import('@/views/Vadmin/Stock/Drawdown/Drawdown.vue'),
  name: 'DrawdownAnalysis',
  meta: { title: '回撤分析', noCache: true }
}
```

---

## 七、文件清单

### 7.1 新建文件

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

### 7.2 修改文件

| 文件路径 | 修改内容 |
|---------|---------|
| `backend/stock-service/app/api/router.py` | 添加drawdown路由 |
| `frontend/src/router/index.ts` | 添加页面路由 |

---

## 八、验收标准

1. **回撤分析**: 输入股票代码和时间范围，正确计算并展示各项回撤指标
2. **回调买点**: 当股票回调至支撑位时，正确生成买入信号
3. **持仓监控**: 输入成本价后，实时监控盈利/亏损和回撤情况
4. **图表展示**: 回撤走势图正确标注峰值、谷值和回撤区域