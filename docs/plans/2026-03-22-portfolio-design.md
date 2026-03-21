# 投资组合管理功能设计文档

## 1. 概述

### 1.1 功能定位

投资组合管理是一个综合管理型模块，帮助用户：
- **持仓管理**：管理多个股票组合，跟踪持仓成本、盈亏、仓位配置
- **策略执行**：基于策略建议调仓操作，支持定期再平衡
- **分析优化**：组合业绩分析、风险归因、资产配置优化
- **风险控制**：仓位限制、回撤预警、交易前风控检查

### 1.2 核心特性

| 特性 | 描述 |
|-----|------|
| 多组合管理 | 支持创建多个投资组合，灵活切换 |
| 持仓追踪 | 实时计算持仓市值、盈亏、仓位占比 |
| 交易记录 | 完整的买入/卖出/分红记录流水 |
| 业绩分析 | 收益率、年化收益、夏普比率等指标 |
| 风险分析 | 波动率、回撤、行业集中度分析 |
| 风控预警 | 仓位超限、回撤预警、再平衡提醒 |
| 模块联动 | 与自选股、投资日历、AI分析、监听策略深度集成 |

### 1.3 技术栈

- **前端**：Vue 3 + Element Plus + TypeScript + ECharts
- **后端**：FastAPI + SQLAlchemy 2.0 + MySQL
- **数据源**：AkShare（实时行情）、用户手动录入

---

## 2. 系统架构

### 2.1 整体架构

```
┌─────────────────────────────────────────────────────────────────┐
│                         前端层                                   │
├─────────────┬─────────────┬─────────────┬─────────────┬─────────┤
│  组合概览   │  持仓管理   │  交易记录   │  分析报告   │  风控中心│
└─────────────┴─────────────┴─────────────┴─────────────┴─────────┘
                              │
┌─────────────────────────────────────────────────────────────────┐
│                         API层                                   │
├─────────────┬─────────────┬─────────────┬─────────────┬─────────┤
│ 组合管理API │ 持仓操作API │ 交易流水API │ 分析计算API │ 风控API │
└─────────────┴─────────────┴─────────────┴─────────────┴─────────┘
                              │
┌─────────────────────────────────────────────────────────────────┐
│                         服务层                                   │
├─────────────┬─────────────┬─────────────┬─────────────┬─────────┤
│组合服务     │持仓服务      │交易服务     │分析服务     │风控服务  │
└─────────────┴─────────────┴─────────────┴─────────────┴─────────┘
                              │
┌─────────────────────────────────────────────────────────────────┐
│                    联动模块                                      │
├─────────────┬─────────────┬─────────────┬───────────────────────┤
│   自选股    │  投资日历   │  AI分析     │    监听策略           │
└─────────────┴─────────────┴─────────────┴───────────────────────┘
```

### 2.2 核心模块职责

| 模块 | 职责 |
|-----|------|
| 组合服务 | 创建/编辑组合、目标配置设置、组合切换、统计数据更新 |
| 持仓服务 | 持仓记录、成本计算、仓位监控、价格同步 |
| 交易服务 | 买入/卖出/分红记录、交易流水查询、盈亏计算 |
| 分析服务 | 业绩指标计算、归因分析、风险分析、基准对比 |
| 风控服务 | 仓位检查、回撤预警、再平衡提醒、交易前风控 |

---

## 3. 数据模型

### 3.1 投资组合表 (portfolio)

```sql
CREATE TABLE portfolio (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL COMMENT '用户ID',
    name VARCHAR(100) NOT NULL COMMENT '组合名称',
    description TEXT COMMENT '组合描述',
    
    -- 目标配置
    target_allocation JSON COMMENT '目标资产配置JSON',
    
    -- 风控参数
    max_single_position DECIMAL(5,2) DEFAULT 20.00 COMMENT '单只股票最大仓位(%)',
    max_sector_position DECIMAL(5,2) DEFAULT 40.00 COMMENT '单个行业最大仓位(%)',
    max_drawdown DECIMAL(5,2) DEFAULT 15.00 COMMENT '最大回撤预警线(%)',
    rebalance_threshold DECIMAL(5,2) DEFAULT 5.00 COMMENT '再平衡触发阈值(%)',
    rebalance_period VARCHAR(20) DEFAULT 'monthly' COMMENT '再平衡周期',
    
    -- 统计指标
    total_value DECIMAL(15,2) COMMENT '组合总市值',
    total_cost DECIMAL(15,2) COMMENT '组合总成本',
    total_profit DECIMAL(15,2) COMMENT '总盈亏',
    profit_rate DECIMAL(8,4) COMMENT '收益率',
    annual_return DECIMAL(8,4) COMMENT '年化收益率',
    max_drawdown_actual DECIMAL(8,4) COMMENT '实际最大回撤',
    sharpe_ratio DECIMAL(8,4) COMMENT '夏普比率',
    
    benchmark_index VARCHAR(20) DEFAULT '000300' COMMENT '基准指数代码',
    
    is_default TINYINT DEFAULT 0 COMMENT '是否默认组合',
    is_active TINYINT DEFAULT 1 COMMENT '是否启用',
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_user_id (user_id),
    INDEX idx_is_active (is_active)
) COMMENT '投资组合表';
```

### 3.2 持仓表 (portfolio_position)

```sql
CREATE TABLE portfolio_position (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    portfolio_id BIGINT NOT NULL COMMENT '组合ID',
    stock_code VARCHAR(20) NOT NULL COMMENT '股票代码',
    stock_name VARCHAR(100) COMMENT '股票名称',
    
    -- 持仓数据
    shares INT NOT NULL COMMENT '持仓股数',
    available_shares INT COMMENT '可用股数',
    cost_price DECIMAL(10,4) NOT NULL COMMENT '成本价',
    current_price DECIMAL(10,4) COMMENT '现价',
    market_value DECIMAL(15,2) COMMENT '市值',
    
    -- 盈亏数据
    profit DECIMAL(15,2) COMMENT '盈亏金额',
    profit_rate DECIMAL(8,4) COMMENT '盈亏比例',
    
    -- 仓位数据
    position_ratio DECIMAL(8,4) COMMENT '仓位占比(%)',
    target_ratio DECIMAL(8,4) COMMENT '目标仓位占比(%)',
    deviation DECIMAL(8,4) COMMENT '与目标偏离度(%)',
    
    -- 分红数据
    dividend_received DECIMAL(15,2) DEFAULT 0 COMMENT '已收分红',
    
    first_buy_date DATE COMMENT '首次买入日期',
    last_trade_date DATE COMMENT '最近交易日期',
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    UNIQUE KEY uk_portfolio_stock (portfolio_id, stock_code),
    INDEX idx_portfolio_id (portfolio_id),
    INDEX idx_stock_code (stock_code)
) COMMENT '持仓表';
```

### 3.3 交易记录表 (portfolio_trade)

```sql
CREATE TABLE portfolio_trade (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    portfolio_id BIGINT NOT NULL COMMENT '组合ID',
    stock_code VARCHAR(20) NOT NULL COMMENT '股票代码',
    stock_name VARCHAR(100) COMMENT '股票名称',
    
    trade_type VARCHAR(10) NOT NULL COMMENT '交易类型: buy/sell/dividend',
    trade_date DATE NOT NULL COMMENT '交易日期',
    shares INT NOT NULL COMMENT '交易股数',
    price DECIMAL(10,4) NOT NULL COMMENT '交易价格',
    amount DECIMAL(15,2) NOT NULL COMMENT '交易金额',
    commission DECIMAL(10,2) DEFAULT 0 COMMENT '手续费',
    stamp_duty DECIMAL(10,2) DEFAULT 0 COMMENT '印花税',
    
    -- 持仓变化
    position_before INT COMMENT '交易前持仓',
    position_after INT COMMENT '交易后持仓',
    cost_price_before DECIMAL(10,4) COMMENT '交易前成本',
    cost_price_after DECIMAL(10,4) COMMENT '交易后成本',
    
    source VARCHAR(20) DEFAULT 'manual' COMMENT '来源: manual/suggested/import',
    related_strategy_id BIGINT COMMENT '关联策略ID',
    remark TEXT COMMENT '备注',
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_portfolio_id (portfolio_id),
    INDEX idx_trade_date (trade_date),
    INDEX idx_stock_code (stock_code)
) COMMENT '交易记录表';
```

### 3.4 风控预警表 (portfolio_risk_alert)

```sql
CREATE TABLE portfolio_risk_alert (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    portfolio_id BIGINT NOT NULL COMMENT '组合ID',
    alert_type VARCHAR(50) NOT NULL COMMENT '预警类型',
    alert_level VARCHAR(20) NOT NULL COMMENT '预警级别: info/warning/danger',
    
    title VARCHAR(200) NOT NULL COMMENT '预警标题',
    content TEXT COMMENT '预警详情',
    
    related_stock_code VARCHAR(20) COMMENT '关联股票代码',
    related_value DECIMAL(15,2) COMMENT '相关数值',
    threshold_value DECIMAL(15,2) COMMENT '阈值',
    
    is_read TINYINT DEFAULT 0 COMMENT '是否已读',
    is_handled TINYINT DEFAULT 0 COMMENT '是否处理',
    handle_note TEXT COMMENT '处理备注',
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    handled_at DATETIME COMMENT '处理时间',
    
    INDEX idx_portfolio_id (portfolio_id),
    INDEX idx_alert_type (alert_type),
    INDEX idx_created_at (created_at)
) COMMENT '风控预警记录表';
```

### 3.5 组合快照表 (portfolio_snapshot)

```sql
CREATE TABLE portfolio_snapshot (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    portfolio_id BIGINT NOT NULL COMMENT '组合ID',
    snapshot_date DATE NOT NULL COMMENT '快照日期',
    
    total_value DECIMAL(15,2) COMMENT '组合总市值',
    total_cost DECIMAL(15,2) COMMENT '组合总成本',
    profit_rate DECIMAL(8,4) COMMENT '收益率',
    
    sector_allocation JSON COMMENT '行业分布JSON',
    top_holdings JSON COMMENT '前十大持仓JSON',
    
    volatility DECIMAL(8,4) COMMENT '波动率',
    beta DECIMAL(8,4) COMMENT 'Beta值',
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE KEY uk_portfolio_date (portfolio_id, snapshot_date),
    INDEX idx_snapshot_date (snapshot_date)
) COMMENT '组合快照表';
```

---

## 4. API接口设计

### 4.1 组合管理接口

```
GET    /api/portfolio                     # 获取用户组合列表
GET    /api/portfolio/{portfolio_id}      # 获取组合详情
POST   /api/portfolio                     # 创建组合
PUT    /api/portfolio/{portfolio_id}      # 更新组合配置
DELETE /api/portfolio/{portfolio_id}      # 删除组合
GET    /api/portfolio/{portfolio_id}/summary  # 获取组合概览
PUT    /api/portfolio/{portfolio_id}/default  # 设置为默认组合
```

### 4.2 持仓管理接口

```
GET    /api/portfolio/position/{portfolio_id}           # 获取持仓列表
POST   /api/portfolio/position/{portfolio_id}           # 添加持仓
PUT    /api/portfolio/position/{portfolio_id}/{stock_code}  # 更新持仓
DELETE /api/portfolio/position/{portfolio_id}/{stock_code}  # 删除持仓
POST   /api/portfolio/position/{portfolio_id}/sync_price    # 同步价格
```

### 4.3 交易记录接口

```
GET    /api/portfolio/trade/{portfolio_id}       # 获取交易记录
POST   /api/portfolio/trade/{portfolio_id}/buy    # 记录买入
POST   /api/portfolio/trade/{portfolio_id}/sell   # 记录卖出
POST   /api/portfolio/trade/{portfolio_id}/dividend  # 记录分红
GET    /api/portfolio/trade/{portfolio_id}/export    # 导出记录
```

### 4.4 分析服务接口

```
GET    /api/portfolio/analysis/{portfolio_id}/performance   # 业绩指标
GET    /api/portfolio/analysis/{portfolio_id}/attribution   # 归因分析
GET    /api/portfolio/analysis/{portfolio_id}/risk          # 风险分析
GET    /api/portfolio/analysis/{portfolio_id}/benchmark     # 基准对比
GET    /api/portfolio/analysis/{portfolio_id}/history       # 历史净值
GET    /api/portfolio/analysis/{portfolio_id}/allocation    # 资产配置
```

### 4.5 风控服务接口

```
GET    /api/portfolio/risk/{portfolio_id}/alerts         # 预警列表
POST   /api/portfolio/risk/{portfolio_id}/check          # 交易前风控检查
POST   /api/portfolio/risk/{portfolio_id}/rebalance/suggest  # 再平衡建议
PUT    /api/portfolio/risk/alerts/{alert_id}/handle      # 处理预警
GET    /api/portfolio/risk/{portfolio_id}/check_result   # 检查结果
```

### 4.6 联动服务接口

```
POST   /api/portfolio/integration/{portfolio_id}/import_watchlist  # 从自选股导入
GET    /api/portfolio/integration/{portfolio_id}/calendar_events   # 日历事件
POST   /api/portfolio/integration/{portfolio_id}/ai_analyze        # AI分析
POST   /api/portfolio/integration/{portfolio_id}/create_monitors   # 创建监听
```

---

## 5. 前端页面设计

### 5.1 页面结构

```
Portfolio/
├── Portfolio.vue                 # 主页面
├── components/
│   ├── PortfolioCard.vue         # 组合卡片
│   ├── PositionTable.vue         # 持仓表格
│   ├── TradeRecord.vue           # 交易记录
│   ├── TradeDialog.vue           # 交易弹窗
│   ├── AnalysisPanel.vue         # 分析面板
│   │   ├── PerformanceCard.vue   # 业绩卡片
│   │   ├── AttributionChart.vue  # 归因图表
│   │   ├── RiskChart.vue         # 风险图表
│   │   └── BenchmarkChart.vue    # 基准图表
│   ├── RiskAlertPanel.vue        # 风控面板
│   ├── RebalanceSuggest.vue      # 再平衡建议
│   ├── AllocationChart.vue       # 配置饼图
│   └── SettingsDialog.vue        # 设置弹窗
└── composables/
    ├── usePortfolio.ts
    ├── usePosition.ts
    └── useAnalysis.ts
```

### 5.2 页面布局

```
┌─────────────────────────────────────────────────────────────────┐
│ 组合选择器: [默认组合 ▼]  [+ 新建组合]  [设置]                   │
├─────────────────────────────────────────────────────────────────┤
│ 组合概览                                                         │
│ ┌──────────────┬──────────────┬──────────────┬──────────────┐  │
│ │ 总市值       │ 总盈亏       │ 收益率       │ 年化收益     │  │
│ │ ¥125,680.00  │ +¥25,680.00  │ +25.68%      │ +18.32%      │  │
│ └──────────────┴──────────────┴──────────────┴──────────────┘  │
├────────────────────────────┬────────────────────────────────────┤
│ 资产配置                   │ 持仓列表                           │
│ ┌──────────────────────┐  │ [添加持仓] [记录交易] [同步价格]   │
│ │     [饼图]           │  │ ────────────────────────────────  │
│ │  科技 35%            │  │ 股票    持仓   成本   现价   盈亏 │
│ │  金融 40%            │  │ 平安银行  500   12.50  15.20  +21%│
│ │  消费 25%            │  │ 招商银行  300   35.00  42.80  +22%│
│ └──────────────────────┘  │ ...                               │
├────────────────────────────┴────────────────────────────────────┤
│ 风控预警                                          [查看全部 >] │
│ ⚠️ 回撤预警: 组合近5日回撤达12%，接近预警线15%                   │
│ ℹ️ 再平衡提醒: 科技板块偏离目标配置5.2%，建议调仓                │
└─────────────────────────────────────────────────────────────────┘
```

---

## 6. 模块联动设计

### 6.1 与自选股联动

| 触发 | 动作 |
|-----|------|
| 添加持仓到组合 | 自动添加到自选股 |
| 从自选股导入 | 批量导入自选股到组合 |
| 删除持仓 | 可选是否从自选股移除 |

### 6.2 与投资日历联动

| 触发 | 动作 |
|-----|------|
| 持仓股票有财报发布 | 推送事件提醒 |
| 解禁日临近 | 提前3天预警 |
| 分红除权日 | 自动记录分红（可配置） |

### 6.3 与AI分析联动

| 触发 | 动作 |
|-----|------|
| 请求组合分析 | AI分析整体风险和配置建议 |
| 请求个股分析 | 调用AI分析持仓内股票 |
| 调仓建议 | AI生成调仓建议 |

### 6.4 与监听策略联动

| 触发 | 动作 |
|-----|------|
| 添加持仓 | 可一键创建价格监控 |
| 策略触发 | 关联持仓显示影响 |
| 再平衡建议 | 可一键创建调仓监控 |

---

## 7. 风控规则设计

### 7.1 仓位控制规则

**单只股票仓位上限**
- 默认：20%
- 检查时机：交易前、每日收盘后
- 触发条件：当前仓位 > 阈值
- 预警级别：warning

**行业集中度上限**
- 默认：40%
- 检查时机：交易前、每日收盘后
- 触发条件：行业仓位 > 阈值
- 预警级别：warning

### 7.2 回撤预警规则

**最大回撤预警**
- 默认：15%
- 计算周期：近30日
- 检查频率：每日
- 预警级别：
  - 回撤 >= 80% 预警线：warning
  - 回撤 >= 100% 预警线：danger

### 7.3 再平衡提醒规则

**配置偏离阈值**
- 默认：5%
- 检查频率：每周
- 触发条件：任一板块偏离目标配置 > 阈值
- 预警级别：info
- 生成内容：调仓建议列表

### 7.4 交易前风控检查

**检查项目**
1. 单只股票仓位是否超限
2. 行业集中度是否超限
3. 是否在禁止买入清单（ST、退市风险等）
4. 资金是否充足

**检查结果**
- pass：允许交易
- warning：允许但提示风险
- block：阻止交易

---

## 8. 开发计划

### 8.1 开发阶段

| 阶段 | 内容 | 预估时间 |
|------|------|---------|
| Phase 1 | 数据模型 + 基础API | 2天 |
| Phase 2 | 持仓管理 + 交易记录 | 2天 |
| Phase 3 | 分析服务 | 2天 |
| Phase 4 | 风控服务 | 2天 |
| Phase 5 | 前端页面开发 | 3天 |
| Phase 6 | 模块联动 | 1天 |
| Phase 7 | 测试 + 优化 | 1天 |

**总计：约13个工作日**

### 8.2 后端文件结构

```
backend/apps/admin/portfolio/
├── __init__.py
├── views.py
├── models/
│   ├── portfolio.py
│   ├── portfolio_position.py
│   ├── portfolio_trade.py
│   ├── portfolio_risk_alert.py
│   └── portfolio_snapshot.py
├── schemas/
│   ├── portfolio.py
│   ├── position.py
│   ├── trade.py
│   └── analysis.py
├── params/
│   └── portfolio_params.py
├── crud/
│   ├── portfolio_crud.py
│   ├── position_crud.py
│   └── trade_crud.py
└── services/
    ├── position_service.py
    ├── trade_service.py
    ├── analysis_service.py
    └── risk_service.py
```

### 8.3 前端文件结构

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
│   ├── RebalanceSuggest.vue
│   ├── AllocationChart.vue
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

## 9. 风险与注意事项

### 9.1 数据风险

- **价格同步延迟**：依赖AkShare接口，可能存在延迟
- **历史数据缺失**：新建组合无法获取历史净值
- **分红处理**：需要手动或自动记录分红

### 9.2 计算风险

- **成本价计算**：卖出时成本价计算需考虑移动平均
- **收益率计算**：需要考虑资金出入的影响
- **年化收益**：持仓时间不足一年时需要折算

### 9.3 性能风险

- **快照数据**：每日快照可能导致数据量快速增长
- **分析计算**：复杂指标计算可能耗时
- **并发更新**：多用户同时更新组合需要加锁

---

## 10. 后续优化方向

1. **券商API对接**：自动同步持仓和交易记录
2. **多账户支持**：支持多个券商账户
3. **策略回测**：基于历史数据回测调仓策略
4. **移动端适配**：响应式设计
5. **数据导入导出**：支持Excel导入导出
6. **组合对比**：多个组合之间对比分析

---

**文档版本**: v1.0
**创建日期**: 2026-03-22
**作者**: AI Assistant