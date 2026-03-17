# 板块轮动功能增强设计文档

## 概述

本文档描述了 Easy Rich 股票量化分析系统中板块轮动模块的功能增强设计。

### 目标

在现有板块轮动模块基础上，新增以下功能：
1. **龙头股追踪** - 追踪各板块龙头股，分析板块活跃度
2. **实时监控告警** - 板块涨跌幅突破阈值时自动告警
3. **轮动策略分析** - 分析板块轮动规律，提供策略回测
4. **板块轮动预测** - 基于AI/量化模型预测下一轮动板块

### 技术栈

- 前端：Vue 3 + Element Plus + TypeScript + ECharts
- 后端：FastAPI + SQLAlchemy
- 数据服务：stock-service (AkShare)
- 数据源：AkShare

---

## 架构设计

### 整体架构

```
┌─────────────────────────────────────────────────────────────────────┐
│                          前端 (Vue 3)                                │
│  SectorRotation.vue + SectorLeader/Monitor/Strategy/Prediction      │
└─────────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    Backend 主服务 (FastAPI)                          │
│  stock_sector_leader.py / stock_sector_monitor.py                   │
│  stock_sector_strategy.py / stock_sector_prediction.py              │
└─────────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    Stock-Service (localhost:8008)                   │
│  sector_leader_service.py / sector_monitor_service.py               │
│  sector_strategy_service.py / sector_prediction_service.py          │
└─────────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         AkShare 数据源                               │
└─────────────────────────────────────────────────────────────────────┘
```

### 页面布局

采用混合布局：核心数据卡片展示 + 子功能Tab切换

```
┌─────────────────────────────────────────────────────────────────────┐
│                        板块轮动分析页面                               │
├─────────────────────────────────────────────────────────────────────┤
│  [日期范围] [板块类型] [刷新按钮]                                      │
├─────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐      │
│  │  板块排行TOP10    │ │  板块资金趋势图   │ │  板块热力图       │      │
│  │  (现有功能保留)   │ │  (现有功能保留)   │ │  (现有功能保留)   │      │
│  └──────────────────┘ └──────────────────┘ └──────────────────┘      │
├─────────────────────────────────────────────────────────────────────┤
│  [龙头股追踪] [实时监控] [策略分析] [轮动预测]   ← Tab切换              │
├─────────────────────────────────────────────────────────────────────┤
│                      Tab 内容区域                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 模块一：龙头股追踪

### 功能描述

追踪各板块龙头股，分析板块活跃度和资金流向。

### 核心功能

1. **板块龙头股列表** - 显示每个板块的领涨股、涨停股
2. **龙头股评分** - 基于涨幅、成交量、资金流入计算综合评分
3. **板块活跃度指标** - 涨停家数、涨幅超5%家数、资金净流入
4. **龙头股切换监控** - 追踪板块龙头变更

### 数据模型

```typescript
interface SectorLeader {
  sector_code: string      // 板块代码
  sector_name: string      // 板块名称
  leader_stock: {          // 龙头股信息
    code: string
    name: string
    change_rate: number
    volume: number
    score: number          // 龙头评分 0-100
  }
  second_leader?: {        // 二龙头
    code: string
    name: string
    change_rate: number
  }
  active_stocks: number    // 活跃股数量
  limit_up_count: number   // 涨停家数
  fund_inflow: number      // 资金净流入
  activity_score: number   // 板块活跃度评分
}
```

### API 接口

#### stock-service 接口

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/api/v1/sector/industry/{board_code}/leaders` | 获取行业板块龙头股 |
| GET | `/api/v1/sector/concept/{board_code}/leaders` | 获取概念板块龙头股 |
| GET | `/api/v1/sector/leaders/ranking` | 获取所有板块龙头股排行 |

#### backend 主服务接口

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/stock/sector/leaders` | 获取板块龙头股排行 |
| GET | `/stock/sector/{board_code}/leaders` | 获取指定板块龙头股 |

### AkShare 数据源

- `ak.stock_board_industry_cons_em(symbol)` - 行业板块成份股
- `ak.stock_board_concept_cons_em(symbol)` - 概念板块成份股
- `ak.stock_zh_a_spot_em()` - A股实时行情

---

## 模块二：实时监控告警

### 功能描述

实时监控板块涨跌幅，自动触发告警提醒。

### 核心功能

1. **告警规则配置** - 设置涨跌幅阈值、监控板块范围
2. **实时监控状态** - 显示当前监控中的板块状态
3. **告警记录历史** - 历史告警记录和触发时间
4. **告警通知** - 系统通知、邮件等

### 数据模型

```typescript
interface SectorMonitor {
  id: number
  sector_code: string
  sector_name: string
  threshold_up: number      // 上涨告警阈值
  threshold_down: number    // 下跌告警阈值
  is_active: boolean        // 是否启用
  created_at: string
}

interface SectorAlert {
  id: number
  sector_code: string
  sector_name: string
  alert_type: 'up' | 'down'
  threshold: number
  actual_value: number
  triggered_at: string
  is_read: boolean
}
```

### API 接口

#### stock-service 接口

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/api/v1/sector/industry/realtime` | 行业板块实时行情 |
| GET | `/api/v1/sector/concept/realtime` | 概念板块实时行情 |

#### backend 主服务接口

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | `/stock/sector/monitor` | 创建监控规则 |
| GET | `/stock/sector/monitor` | 获取监控规则列表 |
| PUT | `/stock/sector/monitor/{id}` | 更新监控规则 |
| DELETE | `/stock/sector/monitor` | 删除监控规则 |
| GET | `/stock/sector/alerts` | 获取告警记录 |

### AkShare 数据源

- `ak.stock_board_industry_spot_em()` - 行业板块实时行情
- `ak.stock_board_concept_spot_em()` - 概念板块实时行情

---

## 模块三：轮动策略分析

### 功能描述

分析板块轮动规律，提供策略回测和收益分析。

### 核心功能

1. **轮动规律分析** - 基于历史数据识别板块轮动周期
2. **策略模板库** - 预设多种轮动策略模板
3. **策略回测** - 模拟策略历史收益
4. **策略对比** - 多策略收益对比

### 数据模型

```typescript
interface RotationStrategy {
  id: number
  name: string
  description: string
  entry_rule: string
  exit_rule: string
  sectors: string[]
  backtest_result?: {
    total_return: number
    annual_return: number
    max_drawdown: number
    win_rate: number
    sharpe_ratio: number
  }
}

interface RotationPattern {
  pattern_id: string
  pattern_name: string
  trigger_condition: string
  next_sectors: string[]
  confidence: number
  historical_accuracy: number
}
```

### API 接口

#### stock-service 接口

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/api/v1/sector/rotation/history` | 板块历史轮动数据 |
| GET | `/api/v1/sector/rotation/patterns` | 板块轮动规律识别 |
| GET | `/api/v1/sector/{board_code}/history` | 板块历史行情 |

#### backend 主服务接口

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/stock/sector/strategy` | 获取策略列表 |
| POST | `/stock/sector/strategy` | 创建策略 |
| POST | `/stock/sector/strategy/backtest` | 策略回测 |
| GET | `/stock/sector/rotation/patterns` | 获取轮动规律 |

### AkShare 数据源

- `ak.stock_board_industry_hist_em()` - 行业板块历史行情
- `ak.stock_board_concept_hist_em()` - 概念板块历史行情

---

## 模块四：板块轮动预测

### 功能描述

基于AI/量化模型预测下一轮动板块。

### 核心功能

1. **多因子预测模型** - 基于资金流、情绪、技术指标
2. **预测结果展示** - 下一轮动板块概率排序
3. **置信度分析** - 预测结果置信度评估
4. **历史预测追踪** - 历史预测准确性统计

### 数据模型

```typescript
interface RotationPrediction {
  prediction_id: string
  prediction_time: string
  target_date: string
  predictions: {
    sector_code: string
    sector_name: string
    probability: number
    confidence: number
    factors: {
      fund_flow: number
      sentiment: number
      technical: number
      pattern: number
    }
  }[]
  model_version: string
}

interface PredictionAccuracy {
  date: string
  total_predictions: number
  correct_predictions: number
  accuracy_rate: number
  avg_probability: number
}
```

### API 接口

#### stock-service 接口

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/api/v1/sector/rotation/predict` | 板块轮动预测 |
| GET | `/api/v1/sector/factors` | 板块多因子数据 |

#### backend 主服务接口

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/stock/sector/prediction` | 获取轮动预测 |
| GET | `/stock/sector/prediction/accuracy` | 获取预测准确率 |
| GET | `/stock/sector/factors` | 获取板块因子数据 |

### AkShare 数据源

- `ak.stock_board_industry_fund_flow_em()` - 板块资金流向
- `ak.stock_board_industry_hist_em()` - 板块历史行情（技术指标计算）

---

## 前端文件结构

```
frontend/src/views/Vadmin/Stock/SectorRotation/
├── SectorRotation.vue              # 主页面（改造）
├── components/
│   ├── SectorRanking.vue           # 现有：板块排行
│   ├── SectorTrend.vue             # 现有：资金趋势图
│   ├── SectorHeatmap.vue           # 现有：热力图
│   ├── SectorLeader.vue            # 新增：龙头股追踪
│   ├── SectorMonitor.vue           # 新增：实时监控告警
│   ├── SectorStrategy.vue          # 新增：轮动策略分析
│   └── SectorPrediction.vue        # 新增：板块轮动预测
├── hooks/
│   └── useSectorData.ts            # 新增：板块数据Hook
└── types/
    └── sector.ts                   # 新增：类型定义
```

## 后端文件结构

```
backend/apps/admin/stock/
├── stock_board_industry.py         # 现有：行业板块API（扩展）
├── stock_sector_leader.py          # 新增：龙头股追踪API
├── stock_sector_monitor.py         # 新增：监控告警API
├── stock_sector_strategy.py        # 新增：策略分析API
├── stock_sector_prediction.py      # 新增：轮动预测API
├── services/
│   └── stock_service.py            # 现有：stock-service客户端（扩展）
├── models/
│   ├── stock_sector_monitor.py     # 新增：监控模型
│   └── stock_sector_alert.py       # 新增：告警模型
├── schemas/
│   └── sector_rotation.py          # 新增：板块轮动相关Schema
└── crud/
    └── stock_sector_monitor.py     # 新增：监控CRUD
```

## stock-service 文件结构

```
backend/stock-service/app/
├── api/endpoints/
│   └── sector.py                   # 扩展：新增接口
├── services/
│   ├── sector_service.py           # 扩展
│   ├── sector_leader_service.py    # 新增：龙头股服务
│   ├── sector_monitor_service.py   # 新增：监控服务
│   ├── sector_strategy_service.py  # 新增：策略服务
│   └── sector_prediction_service.py # 新增：预测服务
└── models/
    └── sector_models.py            # 扩展：新增数据模型
```

---

## 实现计划

### Phase 1: 龙头股追踪（优先级最高）

1. stock-service 新增龙头股相关接口
2. backend 主服务新增龙头股 API
3. 前端 SectorLeader 组件开发
4. 集成测试

### Phase 2: 实时监控告警

1. stock-service 新增实时行情接口
2. backend 主服务新增监控告警 API 和数据模型
3. 前端 SectorMonitor 组件开发
4. 定时任务集成

### Phase 3: 轮动策略分析

1. stock-service 新增历史数据和规律分析接口
2. backend 主服务新增策略分析 API
3. 前端 SectorStrategy 组件开发
4. 回测功能实现

### Phase 4: 板块轮动预测

1. stock-service 新增预测相关接口
2. backend 主服务新增预测 API
3. 前端 SectorPrediction 组件开发
4. 预测模型集成

---

## 注意事项

1. **数据缓存**：stock-service 应合理使用缓存，减少 AkShare 调用频率
2. **错误处理**：所有接口应有优雅的降级和错误处理
3. **性能优化**：批量接口应考虑分页和限制
4. **实时性**：监控告警需要定时任务支持
5. **用户体验**：前端应提供加载状态和空数据提示

---

## 更新日志

- 2026-03-17: 初始设计文档创建