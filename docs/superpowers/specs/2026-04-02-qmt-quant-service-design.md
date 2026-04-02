# QMT量化交易服务设计文档

## 概述

本文档描述了基于QMT（迅投量化交易终端）的量化分析功能设计，包括数据获取增强和实盘交易对接两大核心功能。

### 设计目标

1. **数据获取增强**：将QMT作为第4个数据源集成到stock-service，复用现有数据服务架构
2. **实盘交易对接**：创建独立的qmt-service微服务，提供完整的交易、持仓、风控、策略功能

### 技术选型

| 技术 | 用途 | 说明 |
|------|------|------|
| xtquant | QMT官方Python SDK | 数据获取与交易执行 |
| FastAPI | 后端API框架 | 与现有项目保持一致 |
| Redis | 共享缓存 | 复用stock-service配置 |
| Vue 3 + Element Plus | 前端框架 | 与现有项目保持一致 |
| APScheduler | 策略定时调度 | 策略自动化执行 |

---

## 一、系统架构

### 1.1 整体架构图

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           Frontend (Vue 3)                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │ 股票数据面板 │  │ QMT交易面板  │  │ 策略管理    │  │ 风控配置    │    │
│  │ (stock-svc) │  │ (qmt-svc)   │  │ (qmt-svc)   │  │ (qmt-svc)   │    │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        Backend API Gateway                               │
│                    (http://localhost:9000)                               │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│   stock-service  │  │   qmt-service    │  │   其他服务        │
│  port: 8008      │  │  port: 8009      │  │                  │
│                  │  │                  │  │                  │
│  数据获取：       │  │  交易执行        │  │                  │
│  - AKShare       │  │  持仓管理        │  │                  │
│  - Tushare       │  │  风控引擎        │  │                  │
│  - GM            │  │  策略自动化      │  │                  │
│  - QMT(新增)     │  │  智能订单        │  │                  │
└──────────────────┘  └──────────────────┘  └──────────────────┘
         │                     │
         └─────────────┬───────┘
                       ▼
              ┌────────────────┐
              │  Redis Cache   │
              │  (共享缓存)     │
              └────────────────┘
                       │
                       ▼
              ┌────────────────┐
              │  QMT Client    │
              │  (本地运行)     │
              │  xtquant SDK   │
              └────────────────┘
```

### 1.2 服务职责划分

| 服务 | 职责 | 端口 | 说明 |
|------|------|------|------|
| stock-service | 数据获取 | 8008 | 将QMT作为第4个数据源集成，提供统一数据API |
| qmt-service | 交易+风控+策略 | 8009 | 专注于QMT特有的交易执行、持仓管理、风控引擎、策略自动化 |
| Redis | 共享缓存 | 6379 | 数据缓存，与stock-service共享 |
| QMT Client | 本地客户端 | - | 用户本地运行，xtquant SDK连接 |

### 1.3 数据源优先级

stock-service中的数据源降级策略调整为：

```
AKShare（主）→ Tushare（备）→ GM（备）→ QMT（第4备/实盘专用）
```

---

## 二、stock-service扩展设计

### 2.1 新增QMT数据适配器

在现有stock-service中新增QMT数据源支持，遵循现有的数据源适配器模式。

**新增文件位置**：`backend/stock-service/app/services/qmt_data_adapter.py`

```python
class QMTDataAdapter:
    """QMT数据源适配器，集成到stock-service"""

    def __init__(self, client_path: str, account: str, password: str):
        self.client_path = client_path
        self.account = account
        self.password = password
        self._connected = False

    async def connect(self) -> bool:
        """连接QMT客户端"""

    async def disconnect(self) -> None:
        """断开连接"""

    def is_available(self) -> bool:
        """检查QMT服务是否可用"""

    # 行情数据接口
    async def get_realtime_quote(self, stock_code: str) -> Quote:
        """获取实时行情"""

    async def get_history_kline(self, stock_code: str, period: str,
                                 start_date: str, end_date: str) -> List[Kline]:
        """获取历史K线"""

    async def get_depth_data(self, stock_code: str) -> DepthData:
        """获取Level-2深度数据"""

    # 财务数据接口
    async def get_financial_data(self, stock_code: str) -> FinancialData:
        """获取财务数据"""

    # 板块数据接口
    async def get_sector_list(self, sector_type: str) -> List[Sector]:
        """获取板块列表"""

    async def get_sector_constituents(self, sector_code: str) -> List[Stock]:
        """获取板块成分股"""
```

### 2.2 数据源管理器更新

修改`backend/stock-service/app/core/data_source_manager.py`，将QMT加入数据源列表。

---

## 三、qmt-service详细设计

### 3.1 目录结构

```
backend/qmt-service/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI主应用
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py              # QMT配置（账号、端口、连接参数）
│   │   ├── logging.py             # 日志配置
│   │   └── qmt_client.py          # QMT客户端连接管理（xtquant SDK）
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── endpoints/
│   │   │   ├── __init__.py
│   │   │   ├── trade_routes.py    # 交易执行API
│   │   │   ├── position_routes.py # 持仓管理API
│   │   │   ├── risk_routes.py     # 风控配置API
│   │   │   ├── order_routes.py    # 智能订单API
│   │   │   └── strategy_routes.py # 策略管理API
│   │   └── router.py              # API路由聚合
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── trade_service.py       # 交易执行服务
│   │   ├── position_service.py    # 持仓管理服务
│   │   ├── risk_service.py        # 风控引擎服务
│   │   ├── order_service.py       # 智能订单服务
│   │   └── strategy_service.py    # 策略执行服务
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── trade_models.py        # 交易模型
│   │   ├── position_models.py     # 持仓模型
│   │   ├── risk_models.py         # 风控模型
│   │   ├── order_models.py        # 订单模型
│   │   └── strategy_models.py     # 策略模型
│   │
│   ├── risk_engine/               # 风控引擎（核心模块）
│   │   ├── __init__.py
│   │   ├── engine.py              # 风控引擎核心
│   │   ├── evaluator.py           # 规则评估器
│   │   ├── rules/
│   │   │   ├── __init__.py
│   │   │   ├── position_limit.py  # 仓位限制规则
│   │   │   ├── loss_limit.py      # 亏损限制规则
│   │   │   ├── forbidden_stocks.py# 禁买股票规则
│   │   │   ├── trade_frequency.py # 交易频率限制
│   │   │   ├── price_deviation.py # 价格偏离限制
│   │   │   └── sector_concentration.py # 板块集中度限制
│   │   └── alerts/
│   │   │   ├── __init__.py
│   │   │   ├── alert_manager.py   # 告警管理器
│   │   │   └── notifiers.py       # 告警通知渠道
│   │
│   └── utils/
│   │   ├── __init__.py
│   │   ├── cache.py               # Redis缓存工具
│   │   ├── helpers.py             # 辅助函数
│   │   └── converters.py          # 数据格式转换
│   │
├── tests/
├── .env.example
├── README.md
├── run.py
└── pyproject.toml
```

### 3.2 核心服务模块

| 服务模块 | 职责 | 关键方法 |
|----------|------|----------|
| `trade_service` | 基础交易执行 | `place_order`, `cancel_order`, `modify_order`, `batch_order` |
| `position_service` | 持仓与资金管理 | `get_positions`, `get_balance`, `get_trades`, `get_today_trades`, `calculate_profit` |
| `order_service` | 智能订单 | `place_stop_loss`, `place_take_profit`, `place_condition_order`, `place_algo_order` |
| `risk_service` | 风控引擎管理 | `check_pre_trade`, `check_post_trade`, `get_risk_status`, `trigger_alert` |
| `strategy_service` | 策略自动化 | `create_strategy`, `run_strategy`, `stop_strategy`, `get_strategy_status`, `bind_signal_source` |

---

## 四、API接口设计

### 4.1 交易执行API（`/api/v1/trade`）

| 方法 | 路径 | 描述 | 参数 |
|------|------|------|------|
| POST | `/trade/order` | 下单 | `stock_code`, `direction`(buy/sell), `price`, `quantity`, `order_type`(limit/market) |
| DELETE | `/trade/order/{order_id}` | 撤单 | `order_id` |
| PUT | `/trade/order/{order_id}` | 改单 | `order_id`, `price`, `quantity` |
| POST | `/trade/order/batch` | 批量下单 | `orders`: 订单列表 |
| GET | `/trade/orders` | 查询委托列表 | `status`(pending/filled/cancelled), `date` |
| GET | `/trade/orders/{order_id}` | 查询委托详情 | `order_id` |

### 4.2 智能订单API（`/api/v1/order`）

| 方法 | 路径 | 描述 | 参数 |
|------|------|------|------|
| POST | `/order/stop-loss` | 止损单 | `stock_code`, `trigger_price`, `quantity`, `stop_type`(fixed/trailing) |
| POST | `/order/take-profit` | 止盈单 | `stock_code`, `trigger_price`, `quantity` |
| POST | `/order/condition` | 条件单 | `stock_code`, `condition_type`, `trigger_condition`, `action` |
| POST | `/order/algo` | 算法交易单 | `stock_code`, `algo_type`(TWAP/VWAP/POV), `duration`, `quantity` |
| GET | `/order/smart-orders` | 查询智能订单 | `status`, `type` |

### 4.3 持仓管理API（`/api/v1/position`）

| 方法 | 路径 | 描述 | 参数 |
|------|------|------|------|
| GET | `/position/list` | 查询持仓列表 | - |
| GET | `/position/{stock_code}` | 查询单只股票持仓 | `stock_code` |
| GET | `/position/balance` | 查询资金余额 | - |
| GET | `/position/trades` | 查询成交记录 | `date`, `stock_code` |
| GET | `/position/trades/today` | 查询今日成交 | - |
| GET | `/position/profit` | 计算盈亏统计 | `period`(day/week/month) |

### 4.4 风控配置API（`/api/v1/risk`）

| 方法 | 路径 | 描述 | 参数 |
|------|------|------|------|
| GET | `/risk/rules` | 获取风控规则列表 | - |
| POST | `/risk/rules` | 创建风控规则 | `rule_type`, `params`, `severity` |
| PUT | `/risk/rules/{rule_id}` | 更新风控规则 | `rule_id`, `params`, `enabled` |
| DELETE | `/risk/rules/{rule_id}` | 删除风控规则 | `rule_id` |
| GET | `/risk/status` | 获取当前风控状态 | - |
| GET | `/risk/alerts` | 获取风控告警历史 | `date`, `level` |
| POST | `/risk/alerts/ack` | 确认告警 | `alert_id` |

### 4.5 策略管理API（`/api/v1/strategy`）

| 方法 | 路径 | 描述 | 参数 |
|------|------|------|------|
| POST | `/strategy/create` | 创建策略 | `name`, `type`, `params`, `signal_source` |
| GET | `/strategy/list` | 查询策略列表 | `status` |
| GET | `/strategy/{strategy_id}` | 查询策略详情 | `strategy_id` |
| POST | `/strategy/{strategy_id}/run` | 启动策略 | `strategy_id` |
| POST | `/strategy/{strategy_id}/stop` | 停止策略 | `strategy_id` |
| PUT | `/strategy/{strategy_id}` | 更新策略参数 | `strategy_id`, `params` |
| GET | `/strategy/{strategy_id}/logs` | 查询策略执行日志 | `strategy_id`, `date` |

---

## 五、风控引擎设计

### 5.1 风控规则类型

| 规则类型 | 描述 | 关键参数 |
|----------|------|----------|
| **仓位限制** | 单只股票仓位上限、总仓位上限 | `max_single_position`(%), `max_total_position`(%) |
| **亏损限制** | 单日亏损上限、总亏损上限 | `max_daily_loss`(元), `max_total_loss`(元), `stop_trading_on_limit` |
| **禁买股票** | 禁止买入的股票列表 | `forbidden_list`(ST股、退市风险等), `custom_list` |
| **交易频率** | 单日交易次数、单股票交易频率限制 | `max_daily_trades`, `max_stock_trades_per_day` |
| **价格偏离** | 买入价格偏离均价限制 | `max_price_deviation`(%) |
| **板块集中度** | 单板块持仓集中度限制 | `max_sector_concentration`(%) |

### 5.2 风控检查流程

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           交易请求入口                                   │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        Pre-Trade风控检查                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │ 仓位限制检查 │  │ 禁买股票检查 │  │ 价格偏离检查 │  │ 交易频率检查 │    │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘    │
│                                                                          │
│  检查结果：                                                               │
│  - PASS: 通过，进入交易执行                                               │
│  - WARN: 警告，记录日志但允许执行                                          │
│  - BLOCK: 阻止，拒绝交易并告警                                            │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    ▼ (PASS/WARN)   ▼ (BLOCK)
┌──────────────────┐  ┌──────────────────┐
│   交易执行        │  │   拒绝交易        │
│                  │  │   发送告警通知     │
└──────────────────┘  └──────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        Post-Trade风控检查                                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                      │
│  │ 实时仓位更新 │  │ 实时亏损计算 │  │ 板块集中度计算 │                      │
│  └─────────────┘  └─────────────┘  └─────────────┘                      │
│                                                                          │
│  触发条件：                                                               │
│  - 仓位超限 → 告警                                                        │
│  - 亏损达阈值 → 告警 + 自动停止交易                                        │
│  - 板块集中度过高 → 告警                                                   │
└─────────────────────────────────────────────────────────────────────────┘
```

### 5.3 风控引擎核心类

```python
class RiskEngine:
    """风控引擎核心"""

    def __init__(self):
        self.rules: List[RiskRule] = []      # 已配置的规则列表
        self.evaluator = RuleEvaluator()      # 规则评估器
        self.alert_manager = AlertManager()   # 告警管理器

    async def check_pre_trade(self, order: Order) -> RiskResult:
        """交易前风控检查"""
        results = []
        for rule in self.rules:
            if rule.check_type == "pre_trade":
                result = await self.evaluator.evaluate(rule, order)
                results.append(result)
        return self._aggregate_results(results)

    async def check_post_trade(self, trade: Trade) -> None:
        """交易后风控检查与状态更新"""

    def _aggregate_results(self, results: List[RiskResult]) -> RiskResult:
        """汇总检查结果：PASS/WARN/BLOCK"""


class RiskRule:
    """风控规则基类"""

    rule_type: str           # 规则类型
    params: dict             # 规则参数
    severity: str            # 严重程度: warn/block
    enabled: bool            # 是否启用

    async def evaluate(self, context: dict) -> RiskResult:
        """评估规则"""


class AlertManager:
    """告警管理器"""

    async def send_alert(self, alert: Alert) -> None:
        """发送告警通知，支持多渠道：系统通知、邮件、webhook等"""
```

---

## 六、数据模型设计

### 6.1 交易模型

```python
class Order:
    """委托订单"""
    order_id: str              # QMT委托ID
    stock_code: str            # 股票代码
    stock_name: str            # 股票名称
    direction: str             # 方向: buy/sell
    price: float               # 委托价格
    quantity: int              # 委托数量
    order_type: str            # 订单类型: limit/market
    status: str                # 状态: pending/filled/cancelled/partial
    filled_quantity: int       # 成交数量
    filled_price: float        # 成交均价
    created_time: datetime     # 创建时间
    updated_time: datetime     # 更新时间
    user_id: int               # 用户ID


class Trade:
    """成交记录"""
    trade_id: str              # 成交ID
    order_id: str              # 关联委托ID
    stock_code: str            # 股票代码
    direction: str             # 方向
    price: float               # 成交价格
    quantity: int              # 成交数量
    trade_time: datetime       # 成交时间
    commission: float          # 手续费
    user_id: int               # 用户ID
```

### 6.2 持仓模型

```python
class Position:
    """持仓"""
    stock_code: str            # 股票代码
    stock_name: str            # 股票名称
    quantity: int              # 持仓数量
    available: int             # 可用数量
    cost_price: float          # 成本价
    current_price: float       # 当前价
    profit: float              # 盈亏金额
    profit_rate: float         # 盈亏比例
    market_value: float        # 市值
    updated_time: datetime     # 更新时间
    user_id: int               # 用户ID


class Balance:
    """资金余额"""
    total_asset: float         # 总资产
    available_cash: float      # 可用资金
    market_value: float        # 持仓市值
    frozen_cash: float         # 冻结资金
    profit_today: float        # 今日盈亏
    profit_total: float        # 总盈亏
    updated_time: datetime     # 更新时间
    user_id: int               # 用户ID
```

### 6.3 智能订单模型

```python
class SmartOrder:
    """智能订单"""
    order_id: str              # 订单ID
    stock_code: str            # 股票代码
    order_type: str            # 类型: stop_loss/take_profit/condition/algo
    trigger_price: float       # 触发价格（止损/止盈）
    trigger_condition: dict    # 触发条件（条件单）
    algo_params: dict          # 算法参数（算法单）
    action: dict               # 触发后的执行动作
    quantity: int              # 数量
    status: str                # 状态: pending/triggered/executed/cancelled
    created_time: datetime     # 创建时间
    triggered_time: datetime   # 触发时间
    user_id: int               # 用户ID
```

### 6.4 风控模型

```python
class RiskRule:
    """风控规则"""
    rule_id: int               # 规则ID
    rule_type: str             # 规则类型
    params: dict               # 规则参数
    severity: str              # 严重程度: warn/block
    enabled: bool              # 是否启用
    created_time: datetime     # 创建时间
    updated_time: datetime     # 更新时间
    user_id: int               # 用户ID


class RiskAlert:
    """风控告警"""
    alert_id: int              # 告警ID
    rule_id: int               # 触发规则ID
    alert_type: str            # 告警类型
    alert_level: str           # 告警级别: info/warning/critical
    message: str               # 告警消息
    context: dict              # 告警上下文数据
    status: str                # 状态: pending/acknowledged/resolved
    created_time: datetime     # 创建时间
    acknowledged_time: datetime # 确认时间
    user_id: int               # 用户ID
```

### 6.5 策略模型

```python
class Strategy:
    """交易策略"""
    strategy_id: int           # 策略ID
    name: str                  # 策略名称
    type: str                  # 策略类型: signal_follow/custom
    params: dict               # 策略参数
    signal_source: dict        # 信号源配置（关联选股策略、监控策略等）
    status: str                # 状态: created/running/stopped/error
    created_time: datetime     # 创建时间
    started_time: datetime     # 启动时间
    stopped_time: datetime     # 停止时间
    user_id: int               # 用户ID


class StrategyLog:
    """策略执行日志"""
    log_id: int                # 日志ID
    strategy_id: int           # 策略ID
    action: str                # 执行动作
    stock_code: str            # 关联股票
    result: str                # 执行结果: success/failed/skipped
    message: str               # 日志消息
    details: dict              # 详细信息
    created_time: datetime     # 创建时间
```

---

## 七、前端设计

### 7.1 菜单结构

```
侧边栏菜单
├── 股票分析（现有）
│   ├── 股票预测
│   ├── 我的股票
│   ├── 板块轮动
│   └── ...
│
├── QMT量化（新增）
│   ├── 交易面板        # 下单、撤单、委托查询
│   ├── 持仓管理        # 持仓列表、资金余额、盈亏统计
│   ├── 智能订单        # 止损止盈、条件单、算法交易
│   ├── 策略管理        # 创建、运行、监控策略
│   ├── 风控配置        # 规则配置、告警管理
│   └── 交易日志        # 成交记录、策略执行日志
│
└── 系统管理（现有）
```

### 7.2 页面组件结构

```
frontend/src/views/Vadmin/Stock/QMT/
├── Trade/
│   ├── Trade.vue                # 交易面板主页面
│   └── components/
│       ├── OrderForm.vue        # 下单表单组件
│       ├── OrderList.vue        # 委托列表组件
│       ├── QuickTrade.vue       # 快捷交易组件
│       └── BatchOrder.vue       # 批量下单组件
│
├── Position/
│   ├── Position.vue             # 持仓管理主页面
│   └── components/
│       ├── PositionTable.vue    # 持仓列表表格
│       ├── BalanceCard.vue      # 资金余额卡片
│       ├── ProfitChart.vue      # 盈亏统计图表
│       └── TradeHistory.vue     # 成交记录列表
│
├── SmartOrder/
│   ├── SmartOrder.vue           # 智能订单主页面
│   └── components/
│       ├── StopLossForm.vue     # 止损单配置
│       ├── TakeProfitForm.vue   # 止盈单配置
│       ├── ConditionOrder.vue   # 条件单配置
│       ├── AlgoOrder.vue        # 算法交易配置
│       └── SmartOrderList.vue   # 智能订单列表
│
├── Strategy/
│   ├── Strategy.vue             # 策略管理主页面
│   └── components/
│       ├── StrategyCreate.vue   # 策略创建表单
│       ├── StrategyList.vue     # 策略列表
│       ├── StrategyDetail.vue   # 策略详情
│       ├── StrategyLogs.vue     # 策略执行日志
│       └── SignalBinding.vue    # 信号源绑定配置
│
├── Risk/
│   ├── Risk.vue                 # 风控配置主页面
│   └── components/
│       ├── RuleConfig.vue       # 规则配置组件
│       ├── RuleList.vue         # 规则列表
│       ├── RiskStatus.vue       # 风控状态仪表盘
│       ├── AlertHistory.vue     # 告警历史列表
│       └── AlertDetail.vue      # 告警详情弹窗
│
└── Logs/
    └── TradeLogs.vue            # 交易日志页面
```

---

## 八、配置与部署

### 8.1 环境配置

**qmt-service配置文件（`.env.example`）**

```env
# QMT客户端配置
QMT_CLIENT_PATH=C:\迅投QMT交易端\userdata_mini  # QMT客户端路径
QMT_ACCOUNT=your_account         # QMT账号
QMT_PASSWORD=your_password       # QMT密码

# 服务配置
SERVICE_PORT=8009                # qmt-service端口
SERVICE_HOST=0.0.0.0

# Redis配置（共享stock-service）
REDIS_URL=redis://localhost:6379/0
CACHE_ENABLED=true
CACHE_TTL=3600

# 风控默认配置
DEFAULT_MAX_SINGLE_POSITION=20   # 单股仓位上限(%)
DEFAULT_MAX_TOTAL_POSITION=80    # 总仓位上限(%)
DEFAULT_MAX_DAILY_LOSS=5000      # 日亏损上限(元)
DEFAULT_MAX_DAILY_TRADES=50      # 日交易次数上限

# 告警配置
ALERT_EMAIL_ENABLED=false
ALERT_EMAIL_TO=
ALERT_WEBHOOK_ENABLED=false
ALERT_WEBHOOK_URL=

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=qmt-service.log
```

### 8.2 服务依赖

```toml
# backend/qmt-service/pyproject.toml

[project]
name = "qmt-service"
version = "1.0.0"
description = "QMT量化交易服务"

dependencies = [
    "fastapi>=0.101.0",
    "uvicorn>=0.23.0",
    "pydantic>=2.0.0",
    "redis>=4.5.0",
    "xtquant>=1.0.0",           # QMT官方SDK
    "apscheduler>=3.10.0",      # 定时任务（策略调度）
    "python-dotenv>=1.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "httpx>=0.24.0",
]
```

### 8.3 QMT客户端连接管理

```python
# backend/qmt-service/app/core/qmt_client.py

from xtquant import xtdata
from xtquant.xttrader import XtQuantTrader, XtAccount
from app.core.config import settings

class QMTClientManager:
    """QMT客户端连接管理器"""

    _trader: XtQuantTrader = None
    _account: XtAccount = None
    _connected: bool = False

    @classmethod
    async def initialize(cls):
        """初始化QMT连接"""
        try:
            # 创建交易对象
            cls._trader = XtQuantTrader(
                settings.QMT_CLIENT_PATH,
                settings.SERVICE_PORT
            )

            # 创建账号对象
            cls._account = XtAccount(
                settings.QMT_ACCOUNT,
                settings.QMT_PASSWORD
            )

            # 连接QMT
            cls._trader.connect()
            cls._connected = True

        except Exception as e:
            cls._connected = False
            raise RuntimeError(f"QMT连接失败: {e}")

    @classmethod
    async def close(cls):
        """关闭QMT连接"""
        if cls._trader:
            cls._trader.disconnect()
            cls._connected = False

    @classmethod
    def get_trader(cls) -> XtQuantTrader:
        """获取交易对象"""
        if not cls._connected:
            raise RuntimeError("QMT未连接")
        return cls._trader

    @classmethod
    def get_account(cls) -> XtAccount:
        """获取账号对象"""
        if not cls._connected:
            raise RuntimeError("QMT未连接")
        return cls._account

    @classmethod
    def is_connected(cls) -> bool:
        """检查连接状态"""
        return cls._connected
```

---

## 九、开发计划

### 9.1 开发阶段

| 阶段 | 内容 | 优先级 | 预计工作量 |
|------|------|--------|-----------|
| **阶段一** | QMT连接 + 基础交易 + 持仓查询 | 高 | 核心功能 |
| **阶段二** | 风控引擎 + 告警通知 | 高 | 安全保障 |
| **阶段三** | 智能订单 | 中 | 增强交易能力 |
| **阶段四** | 策略自动化 | 中 | 高级功能 |
| **阶段五** | stock-service数据源集成 | 低 | 数据增强 |

### 9.2 阶段一详细任务

1. 创建qmt-service项目骨架
2. 实现QMT客户端连接管理
3. 实现交易执行服务（下单、撤单、改单）
4. 实现持仓管理服务（持仓查询、资金余额）
5. 创建前端交易面板和持仓管理页面
6. 集成到主应用路由

---

## 十、风险与注意事项

### 10.1 技术风险

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| QMT SDK版本兼容性 | 可能导致连接失败 | 使用稳定版本，关注官方更新 |
| 本地连接稳定性 | 网络中断导致交易失败 | 实现重连机制，状态监控 |
| 风控规则遗漏 | 可能造成损失 | 完善规则库，定期审查 |

### 10.2 业务风险

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| 策略执行错误 | 非预期交易 | 策略沙盒测试，人工确认机制 |
| 市场极端行情 | 风控可能失效 | 增加熔断机制，人工干预接口 |
| 账号安全 | 资金风险 | 敏感信息加密，操作日志审计 |

### 10.3 注意事项

1. **模拟环境优先**：所有功能先在QMT模拟账号测试通过后，再考虑实盘
2. **风控先行**：在启用任何交易功能前，必须配置好风控规则
3. **日志完整**：所有交易操作必须有完整日志记录，便于审计和问题排查
4. **用户确认**：关键操作（如策略启动、大额交易）需要用户二次确认

---

## 附录

### A. QMT SDK常用API参考

```python
# 行情数据
xtdata.get_market_data(stock_list, period='1d')  # 获取行情数据
xtdata.get_full_tick(stock_code)                  # 获取实时行情
xtdata.get_local_data(stock_code, period='1d')    # 获取本地数据

# 交易执行
trader.order_stock(account, stock_code, order_type, direction, volume, price)  # 下单
trader.cancel_order(account, order_id)            # 撤单
trader.query_stock_order(account, order_id)       # 查询委托
trader.query_stock_trade(account, order_id)       # 查询成交

# 持仓查询
trader.query_stock_position(account)              # 查询持仓
trader.query_stock_asset(account)                 # 查询资产
```

### B. 相关文档链接

- QMT官方文档：https://dict.thinktrader.net/nativeApi/start_now.html
- xtquant SDK文档：https://dict.thinktrader.net/nativeApi/xtquant.html
- 现有stock-service文档：`backend/stock-service/README.md`
- 现有GM服务集成参考：`backend/GM_SERVICE.md`