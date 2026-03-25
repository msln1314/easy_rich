# 因子挖掘模块设计文档

## 概述

为 easy_rich 项目新增因子挖掘模块，支持因子定义、计算、检验、自动挖掘和组合优化功能。

## 功能范围

- **因子计算**: 计算动量、反转、波动率、估值、成长等技术/基本面因子值
- **因子检验**: 计算 IC、IR、分组收益、单调性等统计指标
- **自动挖掘**: 基于遗传规划等方法自动挖掘新因子表达式
- **因子组合**: 多因子组合优化、权重分配、正交化处理

## 目标用户

- 量化研究员：测试新的技术因子
- 基金经理：构建多因子选股组合
- 量化交易员：回测多因子选股策略

## 数据来源

使用现有数据库表：
- `stock_daily`: 日线行情数据
- `stock_basic_info`: 股票基本信息
- `stock_hot_rank`: 热度排名数据
- `stock_north_money`: 北向资金数据

## 目标变量

预测未来 N 日收益率（N 可配置，默认 1/5/10 日）

---

## 模块结构

```
backend/apps/admin/factor/
├── __init__.py
├── api.py                      # 路由注册入口
├── factor_definition.py        # 因子定义 API
├── factor_calculation.py       # 因子计算 API
├── factor_analysis.py          # 因子检验 API
├── factor_mining.py            # 自动挖掘 API
├── factor_portfolio.py         # 因子组合 API
├── models/
│   ├── __init__.py
│   ├── factor_definition.py    # 因子定义表
│   ├── factor_value.py         # 因子值缓存表
│   ├── factor_test_result.py   # 因子检验结果表
│   ├── factor_version.py       # 因子版本历史表
│   ├── factor_portfolio.py     # 因子组合配置表
│   └── mining_task.py          # 挖掘任务表
├── services/
│   ├── __init__.py
│   ├── calculator.py           # 因子计算引擎
│   ├── validator.py            # 因子验证服务
│   ├── miner.py                # 遗传规划挖掘
│   └── optimizer.py            # 因子组合优化
├── schemas/
│   ├── __init__.py
│   ├── factor_definition.py
│   ├── factor_value.py
│   ├── factor_test.py
│   └── factor_portfolio.py
├── params/
│   ├── __init__.py
│   ├── factor_definition.py
│   ├── factor_calculation.py
│   ├── factor_test.py
│   └── factor_portfolio.py
└── crud/
    ├── __init__.py
    ├── factor_definition.py
    ├── factor_value.py
    ├── factor_test.py
    └── factor_portfolio.py
```

---

## 数据模型设计

### factor_definition（因子定义表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 主键 |
| name | str | 因子名称（唯一） |
| code | text | 因子计算公式/表达式 |
| description | text | 因子描述 |
| category | str | 因子分类 |
| source | str | 来源（preset/user） |
| formula_type | str | 公式类型（expression/function） |
| is_active | bool | 是否启用 |
| created_at | datetime | 创建时间 |
| updated_at | datetime | 更新时间 |

### factor_value（因子值表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | bigint | 主键 |
| factor_id | int | 关联因子定义 |
| stock_code | str | 股票代码 |
| trade_date | date | 交易日期 |
| factor_value | float | 因子值 |
| factor_rank | int | 因子排名（截面排名） |

### factor_test_result（因子检验结果表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 主键 |
| factor_id | int | 关联因子定义 |
| test_start_date | date | 检验开始日期 |
| test_end_date | date | 检验结束日期 |
| forward_period | int | 预测周期（天） |
| ic_mean | float | IC均值 |
| ic_std | float | IC标准差 |
| ic_ir | float | IC信息比率 |
| ic_positive_rate | float | IC正值占比 |
| turnover_rate | float | 换手率 |
| stability_score | float | 稳定性得分 |
| group_returns | json | 分组收益详情 |
| monotonicity_score | float | 单调性得分 |
| test_date | datetime | 检验时间 |

### factor_version（因子版本表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 主键 |
| factor_id | int | 关联因子定义 |
| version_code | str | 版本号 |
| code | text | 该版本的因子代码 |
| description | text | 版本说明 |
| change_reason | str | 变更原因 |
| created_at | datetime | 创建时间 |

### mining_task（挖掘任务表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 主键 |
| task_name | str | 任务名称 |
| status | str | 状态（pending/running/completed/failed） |
| config | json | 挖掘配置 |
| progress | int | 进度百分比 |
| best_factors | json | 最佳因子列表 |
| fitness_history | json | 适应度历史 |
| started_at | datetime | 开始时间 |
| finished_at | datetime | 完成时间 |
| error_message | text | 错误信息 |

### factor_portfolio（因子组合表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 主键 |
| name | str | 组合名称 |
| factor_weights | json | 因子权重配置 |
| optimization_method | str | 优化方法 |
| performance_metrics | json | 组合绩效指标 |
| created_at | datetime | 创建时间 |
| updated_at | datetime | 更新时间 |

---

## API 接口设计

### 因子定义管理

```
GET    /factor/definitions              # 获取因子列表（支持分类筛选）
POST   /factor/definitions              # 创建因子
GET    /factor/definitions/{id}         # 获取因子详情
PUT    /factor/definitions/{id}         # 更新因子
DELETE /factor/definitions/{id}         # 删除因子
POST   /factor/validate                 # 验证因子公式
POST   /factor/definitions/{id}/copy    # 复制因子
GET    /factor/definitions/{id}/versions # 获取版本历史
POST   /factor/definitions/{id}/rollback # 回滚到指定版本
GET    /factor/categories               # 获取因子分类列表
GET    /factor/stats                    # 获取因子统计信息
```

### 因子计算

```
POST   /factor/calculate                # 计算因子值
GET    /factor/values                   # 查询因子值
GET    /factor/values/{stock_code}      # 查询单股票因子值
```

### 因子检验

```
POST   /factor/test                     # 执行因子检验
GET    /factor/test-results/{factor_id} # 获取检验结果
GET    /factor/test-results/{factor_id}/chart # 获取检验可视化数据
```

### 因子挖掘

```
POST   /factor/mining/start             # 启动挖掘任务
GET    /factor/mining/tasks             # 获取挖掘任务列表
GET    /factor/mining/status/{task_id}  # 查询任务进度
GET    /factor/mining/results/{task_id} # 获取挖掘结果
POST   /factor/mining/tasks/{task_id}/cancel # 取消任务
```

### 因子组合

```
GET    /factor/portfolio                # 获取组合列表
POST   /factor/portfolio                # 创建组合
GET    /factor/portfolio/{id}           # 获取组合详情
PUT    /factor/portfolio/{id}           # 更新组合
DELETE /factor/portfolio/{id}           # 删除组合
POST   /factor/portfolio/{id}/optimize  # 执行组合优化
GET    /factor/portfolio/{id}/performance # 获取组合表现
```

---

## 预置因子库

### 价格收益率

| 因子名 | 公式 | 说明 |
|--------|------|------|
| log_return_1 | `np.log(close / close.shift(1))` | 日对数收益率 |
| log_return_5 | `np.log(close / close.shift(5))` | 5日累计收益 |
| price_vs_sma20 | `close / SMA(close, 20)` | 相对20日均线位置 |
| close_open_ratio | `close / open` | 收盘相对开盘强度 |

### 动量趋势

| 因子名 | 公式 | 说明 |
|--------|------|------|
| rsi_14 | `RSI(close, 14)` | RSI指标 |
| macd_line | `MACD(close, 12, 26, 9)[0]` | MACD差值线 |
| adx_14 | `ADX(high, low, close, 14)` | 趋势强度 |
| roc_10 | `(close - close.shift(10)) / close.shift(10)` | 10日变化率 |

### 波动率风险

| 因子名 | 公式 | 说明 |
|--------|------|------|
| atr_14 | `ATR(high, low, close, 14)` | 平均真实波幅 |
| volatility_20 | `close.pct_change().rolling(20).std()` | 20日波动率 |
| bollinger_bandwidth | `(upper - lower) / middle` | 布林带宽度 |

### 成交量资金流

| 因子名 | 公式 | 说明 |
|--------|------|------|
| volume_ma_ratio | `volume / SMA(volume, 10)` | 量比 |
| obv | `OBV(close, volume)` | 累积量能 |
| force_index | `(close - close.shift(1)) * volume` | 强力指数 |

### 技术形态

| 因子名 | 公式 | 说明 |
|--------|------|------|
| golden_cross | `CROSS(SMA(close, 5), SMA(close, 20))` | 金叉信号 |
| new_high_20 | `close >= HHV(high, 20)` | 触及20日新高 |
| three_rising | `EVERY(close > open, 3)` | 三连阳 |

### 反转信号

| 因子名 | 公式 | 说明 |
|--------|------|------|
| reversal_5 | `-(close / close.shift(5) - 1)` | 5日反转因子 |
| deviation_ma20 | `(close - SMA(close, 20)) / SMA(close, 20)` | 偏离均线程度 |
| stochastic_k | `(close - LLV(low, 14)) / (HHV(high, 14) - LLV(low, 14))` | 随机指标K值 |

---

## 因子检验流程

```
1. 数据准备
   ├── 获取因子值序列
   └── 计算未来 N 日收益率作为标签

2. IC 检验
   ├── 计算每期 RankIC（Spearman相关系数）
   ├── 统计 IC 均值、ICIR、IC 正值占比
   └── 有效因子标准：|IC| > 0.03 且 ICIR > 0.5

3. 分组检验
   ├── 按因子值分 5/10 组
   ├── 计算各组平均收益
   └── 检验单调性（多空组合收益）

4. 稳定性检验
   ├── 分段 KS 检验
   └── 稳定性得分

5. 换手率检验
   ├── 计算因子排名变化
   └── 换手率指标

6. 输出报告
   ├── IC 时序图
   ├── 分组收益柱状图
   └── 因子衰减分析
```

---

## 遗传规划挖掘流程

```
1. 初始化
   ├── 定义基础算子（+、-、*、/、rank、log、abs）
   ├── 定义时序算子（SMA、STD、HHV、LLV、REF）
   ├── 定义终端集合（open、close、high、low、volume）
   └── 设置种群大小（默认 50）

2. 适应度评估
   ├── 计算因子 ICIR
   ├── 计算换手率惩罚
   └── 综合得分 = ICIR - 换手率 * 0.1

3. 遗传操作
   ├── 选择：锦标赛选择（tournsize=3）
   ├── 交叉：子树交叉
   └── 变异：点变异/子树变异

4. 输出
   ├── Top-K 最优因子表达式
   └── 自动入库并执行检验
```

---

## 因子组合优化

### 组合方法

1. **等权组合**: 所有因子权重相等
2. **ICIR最大化**: 基于历史ICIR优化权重
3. **风险平价**: 基于因子波动率分配权重
4. **均值方差优化**: 考虑收益和风险

### 正交化处理

- 施密特正交化
- 残差正交化

---

## 技术依赖

### 新增 Python 依赖

```
talib>=0.4.28      # 技术分析库
deap>=1.3.0        # 遗传算法框架
scipy>=1.10.0      # 统计检验
```

### 复用现有依赖

```
pandas>=2.0.0
numpy>=1.24.0
sqlalchemy>=2.0.0
fastapi>=0.100.0
```

---

## 前端界面需求

### 因子列表展示

- 因子表格（名称、分类、IC、状态）
- 因子详情弹窗
- 因子创建/编辑表单
- 公式编辑器（带语法高亮）

### 因子检验可视化

- IC 时序图
- 分组收益柱状图
- 因子相关性热力图
- 换手率趋势图

### 自动挖掘管理

- 挖掘任务配置面板
- 进度条和状态显示
- 结果因子列表
- 因子入库操作

### 因子组合管理

- 组合配置面板
- 权重调整滑块
- 组合表现图表
- 优化配置选项

---

## 实现优先级

### Phase 1: 核心功能（MVP）

1. 因子定义模型和 CRUD
2. 因子计算引擎（支持麦语言）
3. 基础 IC/IR 检验
4. 预置因子库初始化

### Phase 2: 高级功能

1. 因子版本管理
2. 分组检验和单调性分析
3. 稳定性检验
4. 因子值缓存优化

### Phase 3: 自动挖掘

1. 遗传算法挖掘服务
2. 任务管理和进度追踪
3. 因子表达式解析

### Phase 4: 组合优化

1. 多因子组合配置
2. 权重优化算法
3. 正交化处理
4. 组合绩效分析

---

## 风险和限制

1. **性能风险**: 大规模因子计算可能耗时，需要异步处理和缓存
2. **数据质量**: 依赖现有数据表的数据质量
3. **过拟合风险**: 遗传规划挖掘可能导致过拟合，需要样本外验证
4. **计算资源**: 遗传算法需要较多计算资源

---

## 参考资料

- FactorHub 开源项目: https://github.com/FactorHub/FactorHub
- TALib 文档: https://ta-lib.org/
- DEAP 文档: https://deap.readthedocs.io/