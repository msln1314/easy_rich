---
name: Backtest System Design
description: 基于 Backtrader 的回测系统设计，包含策略管理、回测执行、报告生成和风险评估
type: project
created: 2026-04-02
status: draft
---

# Backtrader 回测系统设计文档

## 一、项目概述

### 1.1 目标

构建一个基于 Backtrader 的量化回测系统，集成到现有股票管理平台，支持：
- 多类型策略：技术指标、因子选股、事件驱动、机器学习
- 多数据源融合：GM（掘金）、本地数据库、AKShare
- 完整风险评估：压力测试、资金管理验证
- 策略模板与代码编写混合模式

### 1.2 用户场景

| 场景 | 描述 |
|------|------|
| 策略展示分享 | 用户创建策略，进行回测验证想法，查看结果报告 |
| 实盘前验证 | 严肃的实盘准备，需要严谨的风险评估、资金管理验证 |

### 1.3 核心设计决策

| 决策点 | 选择 | 理因 |
|--------|------|------|
| 系统架构 | 独立回测服务 | 复用现有 stock-service，资源隔离，计算不影响主系统 |
| 策略管理 | Admin Backend 管理 | 用户体系、权限控制统一管理，stock-service 保持纯粹计算角色 |
| 回测执行 | 实时回测 | 用户体验直接，适合快速迭代验证策略 |
| 策略编写 | 混合模式 | 模板入门 + 代码进阶，兼顾不同用户水平 |
| 社交功能 | 无 | 保持简洁，专注回测功能 |

---

## 二、系统架构

### 2.1 架构图

```
┌─────────────────────────────────────────────────────────────────────┐
│                          Frontend (Vue 3)                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │ 策略管理页面 │  │ 回测执行页面 │  │ 报告查看页面 │  │ 模板选择页面 │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    Admin Backend (FastAPI :8001)                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │ 策略 CRUD   │  │ 用户权限    │  │ 报告存储    │  │ 模板管理    │ │
│  │ 策略元数据  │  │ 认证鉴权    │  │ 报告导出    │  │ 菜单路由    │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼ (HTTP API 调用)
┌─────────────────────────────────────────────────────────────────────┐
│                  Stock-Service (FastAPI :8008)                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │ 数据适配层  │  │ Backtrader  │  │ 回测引擎    │  │ 风险分析    │ │
│  │ GM/AKShare  │  │ 引擎集成    │  │ 执行器      │  │ 压力测试    │ │
│  │ 本地数据库  │  │             │  │             │  │ 报告生成    │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       MySQL + Redis                                  │
│  策略表 │ 回测报告表 │ 策略模板表 │ 数据缓存                         │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.2 职责划分

| 服务 | 职责 |
|------|------|
| **Frontend** | 策略管理界面、回测配置界面、报告展示界面、模板选择界面 |
| **Admin Backend** | 策略元数据 CRUD、用户权限控制、报告持久化、模板管理、菜单路由 |
| **Stock-Service** | 数据获取适配、回测计算执行、风险分析、压力测试、报告生成 |

### 2.3 API 调用流程

```
前端 → Admin Backend → Stock-Service → 返回结果 → Admin Backend 存储 → 前端展示
```

详细流程：
1. 前端调用 Admin Backend 回测执行接口
2. Admin Backend 获取策略详情，调用 Stock-Service 执行回测
3. Stock-Service 执行回测，返回结果
4. Admin Backend 将结果存入 `backtest_report` 表
5. 返回报告 ID 给前端，前端跳转到报告页面

---

## 三、数据模型

### 3.1 核心表结构

#### backtest_strategy（策略表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 主键 |
| name | str | 策略名称 |
| description | str | 策略描述 |
| user_id | int | 创建者，外键关联 sys_user |
| strategy_type | str | 类型：technical/factor/event/ml/custom |
| strategy_code | str | Python 代码，存储策略实现 |
| strategy_config | json | 参数化配置，如均线天数、止损比例等 |
| template_id | int | 关联模板，如使用模板创建 |
| data_source | str | 数据源：gm/local/akshare/custom |
| status | str | 状态：draft/published/archived |
| tags | json | 标签列表，如 ["均线", "趋势跟踪"] |
| created_at | datetime | 创建时间 |
| updated_at | datetime | 更新时间 |

#### backtest_report（回测报告表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 主键 |
| strategy_id | int | 关联策略 |
| user_id | int | 执行者 |
| backtest_config | json | 回测配置：时间范围、初始资金、手续费等 |
| metrics | json | 收益指标：年化收益、夏普比率、最大回撤等 |
| risk_metrics | json | 风险指标：VaR、波动率、压力测试结果等 |
| trades | json | 交易记录明细 |
| equity_curve | json | 权益曲线数据点 |
| benchmark_comparison | json | 基准对比结果 |
| report_file | str | PDF/HTML 报告文件路径 |
| execution_time | float | 回测耗时（秒） |
| status | str | 状态：running/completed/failed |
| error_message | str | 失败时的错误信息 |
| created_at | datetime | 创建时间 |

#### strategy_template（策略模板表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 主键 |
| name | str | 模板名称，如 "双均线交叉策略" |
| description | str | 模板说明 |
| category | str | 分类：technical/factor/event/ml |
| template_code | str | 模板基础代码，含参数占位符 |
| default_params | json | 默认参数配置 |
| param_schema | json | 参数定义：类型、范围、描述 |
| is_official | bool | 是否官方模板 |
| created_at | datetime | 创建时间 |

---

## 四、前端页面设计

### 4.1 页面结构

| 页面 | 路径 | 功能 |
|------|------|------|
| 策略管理 | /stock/backtest/strategy | 策略列表、创建、编辑、删除、克隆 |
| 回测执行 | /stock/backtest/execute | 策略选择、配置参数、执行回测 |
| 回测报告 | /stock/backtest/report/:id | 报告详情、多 Tab 展示、导出 |
| 模板选择 | /stock/backtest/template | 模板列表、预览、选择创建 |

### 4.2 菜单结构

```
股票管理
  └─ 回测系统
      ├─ 策略管理
      ├─ 执行回测
      └─ 历史报告
```

### 4.3 页面详细设计

#### 策略管理页面

- 策略列表表格：名称 | 类型 | 状态 | 创建时间 | 操作
- 操作按钮：编辑 | 删除 | 回测 | 克隆
- 新建策略入口：弹出选择窗口
  - 使用模板创建：选择模板 → 调整参数 → 保存
  - 编写代码创建：代码编辑器 → 输入策略代码

#### 回测执行页面

- 左侧：策略选择区域
  - 选择已有策略（下拉框）
  - 或临时编写策略代码（代码编辑器）
- 右侧：回测配置区域
  - 数据源选择（GM/本地/AKShare）
  - 回测时间范围（开始日期 ~ 结束日期）
  - 初始资金（默认 100 万）
  - 手续费设置（买入/卖出费率）
  - 基准指数（沪深300/中证500/自定义）
  - 股票池设置（全市场/指定股票列表/行业板块）
- 底部：执行按钮
  - 开始回测（实时执行，显示进度条，10-30 秒完成）

#### 回测报告页面

**Tab 1: 收益概览**
- 关键指标卡片：年化收益、夏普比率、最大回撤、胜率等
- 权益曲线图（ECharts 折线图）
- 与基准对比图

**Tab 2: 交易记录**
- 交易明细表格：时间 | 操作 | 价格 | 数量 | 盈亏
- 持仓统计：平均持仓时间、持仓分布
- 导出 CSV 按钮

**Tab 3: 风险分析**
- VaR 分析（95%/99% 置信度下最大损失）
- 波动率分析（日/周/月波动率）
- 压力测试结果（金融危机/暴跌场景模拟）
- 风险归因图表

**Tab 4: 策略对比**
- 选择其他报告进行对比
- 多策略指标横向对比表
- 多策略收益曲线叠加图

**操作按钮**
- 导出 PDF 报告 | 导出 Excel

---

## 五、后端 API 设计

### 5.1 Admin Backend API

#### 策略管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/admin/backtest/strategy/list | 获取策略列表（支持分页、筛选类型/状态） |
| POST | /api/admin/backtest/strategy/create | 创建新策略 |
| GET | /api/admin/backtest/strategy/{id} | 获取策略详情 |
| PUT | /api/admin/backtest/strategy/{id} | 更新策略 |
| DELETE | /api/admin/backtest/strategy/{id} | 删除策略 |
| POST | /api/admin/backtest/strategy/{id}/clone | 克隆策略 |

#### 模板管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/admin/backtest/template/list | 获取模板列表（按分类筛选） |
| GET | /api/admin/backtest/template/{id} | 获取模板详情（含代码和参数定义） |

#### 报告管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/admin/backtest/report/list | 获取报告列表（支持分页、筛选策略/时间范围） |
| GET | /api/admin/backtest/report/{id} | 获取报告详情 |
| DELETE | /api/admin/backtest/report/{id} | 删除报告 |
| GET | /api/admin/backtest/report/{id}/export/pdf | 导出 PDF 报告 |
| GET | /api/admin/backtest/report/{id}/export/excel | 导出 Excel |

#### 回测执行（代理调用）

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/admin/backtest/execute | 执行回测（调用 Stock-Service） |

### 5.2 Stock-Service API

#### 回测执行

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/backtest/execute | 执行回测 |

**请求体：**
```json
{
  "strategy_id": 1,
  // 或 "strategy_code": "...",
  "data_source": "gm",
  "start_date": "2023-01-01",
  "end_date": "2024-01-01",
  "initial_cash": 1000000,
  "commission": 0.0003,
  "benchmark": "000300",
  "stock_pool": ["000001", "600519"]
}
```

**返回：**
```json
{
  "metrics": {...},
  "risk_metrics": {...},
  "trades": [...],
  "equity_curve": [...],
  "execution_time": 12.5
}
```

#### 数据源

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/backtest/data/sources | 获取可用数据源列表 |
| GET | /api/backtest/data/stocks?source={source} | 获取指定数据源可用的股票列表 |
| GET | /api/backtest/data/benchmarks | 获取可用的基准指数列表 |

---

## 六、Stock-Service 核心模块

### 6.1 模块结构

```
backend/stock-service/app/
├─ api/endpoints/
│  └─ backtest_routes.py          # 回测执行 API
├─ services/
│  └─ backtest/
│     ├─ engine.py                 # Backtrader 引擎封装
│     ├─ data_adapter.py           # 数据源适配层（统一接口）
│     ├─ data_sources/
│     │  ├─ gm_adapter.py          # GM（掘金）数据适配
│     │  ├─ local_adapter.py       # 本地数据库适配
│     │  ├─ akshare_adapter.py     # AKShare 数据适配
│     │  └─ base.py                # 数据源基类
│     ├─ strategy_loader.py        # 策略代码动态加载
│     ├─ risk_analyzer.py          # 风险分析模块
│     ├─ stress_test.py            # 压力测试模块
│     ├─ report_generator.py       # 报告生成
│     └─ templates/                # 预置策略模板代码
│        ├─ ma_cross.py            # 双均线交叉模板
│        ├─ rsi_strategy.py        # RSI 策略模板
│        ├─ factor_selection.py    # 因子选股模板
│        └─ ml_strategy.py         # ML 策略模板骨架
```

### 6.2 数据适配层设计

**数据源基类：**
```python
class BaseDataAdapter:
    """统一数据源接口"""
    
    def get_daily_data(
        self, 
        stock_codes: List[str], 
        start_date: date, 
        end_date: date
    ) -> pd.DataFrame:
        """获取日线数据，返回标准格式 DataFrame"""
        raise NotImplementedError
    
    def get_benchmark_data(
        self, 
        benchmark_code: str, 
        start_date: date, 
        end_date: date
    ) -> pd.DataFrame:
        """获取基准指数数据"""
        raise NotImplementedError
    
    def get_available_stocks(self) -> List[dict]:
        """获取可用股票列表"""
        raise NotImplementedError
```

**标准数据格式：**
```
DataFrame columns:
  datetime, open, high, low, close, volume, openinterest, stock_code
```

### 6.3 回测引擎设计

```python
class BacktestEngine:
    """回测执行引擎"""
    
    def run_backtest(
        self,
        strategy_class: Type[bt.Strategy],
        data: pd.DataFrame,
        config: BacktestConfig
    ) -> BacktestResult:
        """执行回测"""
        
    def add_analyzer(self, analyzer_class) -> None:
        """添加分析器"""
        
    def set_commission(self, commission: float) -> None:
        """设置手续费"""
        
    def set_slippage(self, slippage: float) -> None:
        """设置滑点"""
```

### 6.4 策略动态加载

```python
class StrategyLoader:
    """安全的策略代码加载"""
    
    FORBIDDEN_IMPORTS = [
        'os', 'sys', 'subprocess', 'socket',
        'requests', 'urllib', 'http',
        'pickle', 'shelve', 'marshal',
        'eval', 'exec', 'compile',
        '__import__', 'open', 'file'
    ]
    
    SAFE_NAMESPACE = {
        'bt': backtrader,
        'btind': backtrader.indicators,
        'bta': backtrader.analyzers,
        'datetime': datetime,
        'math': math,
        'np': numpy,
        'pd': pandas,
    }
    
    def load_from_code(self, code: str) -> Type[bt.Strategy]:
        """从代码字符串加载策略（安全执行）"""
        
    def load_from_template(
        self, 
        template_code: str, 
        params: dict
    ) -> Type[bt.Strategy]:
        """从模板 + 参数生成策略类"""
```

### 6.5 风险分析模块

```python
class RiskAnalyzer:
    """风险指标计算"""
    
    def calculate_var(
        self, 
        equity_curve: List[float], 
        confidence: float = 0.95
    ) -> dict:
        """计算 VaR"""
        
    def calculate_volatility(
        self, 
        daily_returns: List[float]
    ) -> dict:
        """计算波动率"""
        
    def analyze_drawdown(
        self, 
        equity_curve: List[float]
    ) -> dict:
        """回撤分析"""
        
    def risk_decomposition(
        self, 
        trades: List[dict]
    ) -> dict:
        """风险归因分析"""
```

### 6.6 压力测试模块

```python
class StressTester:
    """模拟极端市场场景"""
    
    SCENARIOS = {
        'financial_crisis_2008': {
            'start': '2008-09-01',
            'end': '2008-12-31',
            'description': '2008年金融危机'
        },
        'covid_2020': {
            'start': '2020-02-01',
            'end': '2020-04-30',
            'description': '2020年疫情暴跌'
        },
        'custom': None
    }
    
    def run_stress_test(
        self,
        strategy: Type[bt.Strategy],
        scenario: str,
        config: BacktestConfig
    ) -> dict:
        """在极端场景下运行策略"""
```

---

## 七、安全性设计

### 7.1 代码执行安全

| 安全措施 | 说明 |
|----------|------|
| 静态检查 | 扫描禁止的 import 和函数调用 |
| 受限命名空间 | 只允许 safe_namespace 中的模块 |
| 类型验证 | 结果必须是 bt.Strategy 子类 |
| 超时限制 | 执行时间超过 5 秒则终止 |

**禁止的危险模块和函数：**
```python
FORBIDDEN_IMPORTS = [
    'os', 'sys', 'subprocess', 'socket',
    'requests', 'urllib', 'http',
    'pickle', 'shelve', 'marshal',
    'eval', 'exec', 'compile',
    '__import__', 'open', 'file'
]
```

### 7.2 用户输入验证

| 参数 | 验证规则 |
|------|----------|
| 时间范围 | 开始日期 < 结束日期，最多 5 年 |
| 初始资金 | 1 ~ 10 亿 |
| 手续费 | 0 ~ 1% |
| 股票池 | 最多 500 只股票 |

---

## 八、错误处理

### 8.1 错误分类

| 错误类型 | HTTP 状态码 | 说明 |
|----------|-------------|------|
| StrategyLoadError | 400 | 代码语法错误、缺少 Strategy 类 |
| StrategySecurityError | 400 | 安全检查失败 |
| DataSourceError | 503 | 数据源连接失败、数据不存在 |
| BacktestRuntimeError | 500 | 策略运行时异常 |
| BacktestTimeoutError | 500 | 执行超时（超过 60 秒） |
| ValidationError | 400 | 参数范围不合理 |

### 8.2 错误响应格式

```json
{
  "success": false,
  "error": {
    "type": "StrategyLoadError",
    "message": "策略代码第 15 行语法错误：缺少右括号",
    "details": {
      "line": 15,
      "code_snippet": "if self.position.size > 0"
    }
  }
}
```

### 8.3 超时控制

- 最大执行时间：60 秒
- 超时后终止执行，返回 BacktestTimeoutError

---

## 九、测试策略

### 9.1 测试层次

| 层次 | 测试内容 |
|------|----------|
| 单元测试 | 数据适配器、风险分析器、策略加载器、配置验证器 |
| 集成测试 | 回测完整流程、API 接口、数据流 |
| 策略功能测试 | 预置模板回归测试、经典策略验证、边界场景测试 |

### 9.2 关键测试用例

| 测试用例 | 说明 |
|----------|------|
| test_ma_cross_strategy_known_result | 双均线策略在已知数据上的结果验证 |
| test_strategy_with_no_signals | 策略不产生任何交易信号 |
| test_commission_impact | 手续费对收益的影响 |
| test_data_adapter_standard_format | 数据适配器返回标准格式 |
| test_strategy_security_check | 策略安全检查（禁止危险代码） |

---

## 十、性能优化

### 10.1 优化措施

| 优化点 | 措施 |
|--------|------|
| 数据缓存 | Redis 缓存热点数据，按股票代码+时间范围缓存 7 天 |
| 数据预加载 | 批量加载股票池数据，避免逐条查询 |
| 计算优化 | Numpy 向量化计算，使用 Backtrader 内置指标 |
| 并发控制 | 单次回测独占线程，最大并发数根据 CPU 核数配置 |

### 10.2 预期性能指标

| 场景 | 预期耗时（优化后） |
|------|-------------------|
| 单股票 1 年回测 | ~2 秒（缓存命中） |
| 10 股票池 1 年回测 | ~8 秒 |
| 100 股票池 1 年回测 | ~30 秒（批量加载） |
| 风险指标计算 | ~0.3 秒（向量化） |

---

## 十一、技术栈确认

| 层级 | 技术 |
|------|------|
| 前端 | Vue 3 + Element Plus + TypeScript + ECharts |
| Admin Backend | FastAPI + SQLAlchemy + MySQL + Redis |
| Stock-Service | FastAPI + Backtrader + Pandas + Numpy |
| 回测引擎 | Backtrader |
| 数据源 | GM（掘金）+ AKShare + 本地 MySQL |

---

## 十二、参考开源项目

### 12.1 Backtrader 官方资源

- 官方文档：https://www.backtrader.com/dochome/
- GitHub：https://github.com/mementum/backtrader

### 12.2 相关开源回测系统

| 项目 | 特点 | 参考价值 |
|------|------|----------|
| **Zipline** | Quantopian 开源引擎，事件驱动架构 | 数据管道设计、风险分析模块 |
| **PyAlgoTrade** | 轻量级回测框架 | 简洁的策略 API 设计 |
| **vnpy** | 国内量化交易框架 | 中文社区支持、国内数据源适配 |
| **quantaxis** | 国产量化平台 | 报告生成、可视化展示 |
| **bt** | 灵活的回测库 | 组合策略回测思路 |

### 12.3 设计借鉴

| 功能模块 | 参考项目 | 借鉴点 |
|----------|----------|--------|
| 数据适配层 | Zipline | 数据管道 bundles 设计 |
| 策略动态加载 | Zipline | 安全的代码执行环境 |
| 报告生成 | Quantaxis | HTML 报告模板、图表布局 |
| 风险分析 | Zipline | 风险指标计算方法 |
| 压力测试 | vnpy | 场景定义、模拟方法 |