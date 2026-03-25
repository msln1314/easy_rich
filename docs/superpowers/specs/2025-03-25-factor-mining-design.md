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
- `stock_daily`: 日线行情数据（字段：close_price, open_price, high_price, low_price, volume）
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
│   ├── sandbox.py              # 公式执行沙箱
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

| 字段 | 类型 | 说明 | 索引 |
|------|------|------|------|
| id | int | 主键 | PK |
| name | str(100) | 因子名称（唯一） | UNIQUE |
| code | text | 因子计算公式/表达式 | - |
| description | text | 因子描述 | - |
| category | str(50) | 因子分类 | INDEX |
| source | str(20) | 来源（preset/user） | INDEX |
| formula_type | str(20) | 公式类型（expression/function） | - |
| user_id | int | 创建用户ID（user因子） | FK, INDEX |
| is_active | bool | 是否启用 | INDEX |
| created_at | datetime | 创建时间 | - |
| updated_at | datetime | 更新时间 | - |

### factor_value（因子值表）

| 字段 | 类型 | 说明 | 索引 |
|------|------|------|------|
| id | bigint | 主键 | PK |
| factor_id | int | 关联因子定义 | FK, INDEX |
| stock_code | str(20) | 股票代码 | INDEX |
| trade_date | date | 交易日期 | INDEX |
| factor_value | float | 因子值 | - |
| factor_rank | int | 因子排名（截面排名） | - |

**复合索引**:
- `idx_factor_stock_date (factor_id, stock_code, trade_date)` - 查询优化
- `idx_stock_date (stock_code, trade_date)` - 单股票查询优化

**分区策略**: 按 `trade_date` 范围分区（年度）

### factor_test_result（因子检验结果表）

| 字段 | 类型 | 说明 | 索引 |
|------|------|------|------|
| id | int | 主键 | PK |
| factor_id | int | 关联因子定义 | FK, INDEX |
| test_start_date | date | 检验开始日期 | - |
| test_end_date | date | 检验结束日期 | - |
| forward_period | int | 预测周期（天） | - |
| ic_mean | float | IC均值 | - |
| ic_std | float | IC标准差 | - |
| ic_ir | float | IC信息比率 | - |
| ic_positive_rate | float | IC正值占比 | - |
| turnover_rate | float | 换手率 | - |
| stability_score | float | 稳定性得分 | - |
| group_returns | json | 分组收益详情 | - |
| monotonicity_score | float | 单调性得分 | - |
| test_date | datetime | 检验时间 | - |

**复合索引**: `idx_factor_period (factor_id, forward_period)`

### factor_version（因子版本表）

| 字段 | 类型 | 说明 | 索引 |
|------|------|------|------|
| id | int | 主键 | PK |
| factor_id | int | 关联因子定义 | FK, INDEX |
| version_code | str(20) | 版本号 | - |
| code | text | 该版本的因子代码 | - |
| description | text | 版本说明 | - |
| change_reason | str(200) | 变更原因 | - |
| created_at | datetime | 创建时间 | - |

### mining_task（挖掘任务表）

| 字段 | 类型 | 说明 | 索引 |
|------|------|------|------|
| id | int | 主键 | PK |
| task_name | str(100) | 任务名称 | - |
| user_id | int | 创建用户ID | FK, INDEX |
| status | str(20) | 状态（pending/running/completed/failed） | INDEX |
| config | json | 挖掘配置 | - |
| progress | int | 进度百分比 | - |
| best_factors | json | 最佳因子列表 | - |
| fitness_history | json | 适应度历史 | - |
| started_at | datetime | 开始时间 | - |
| finished_at | datetime | 完成时间 | - |
| error_message | text | 错误信息 | - |

### factor_portfolio（因子组合表）

| 字段 | 类型 | 说明 | 索引 |
|------|------|------|------|
| id | int | 主键 | PK |
| name | str(100) | 组合名称 | - |
| user_id | int | 创建用户ID | FK, INDEX |
| factor_weights | json | 因子权重配置 | - |
| optimization_method | str(50) | 优化方法 | - |
| performance_metrics | json | 组合绩效指标 | - |
| is_active | bool | 是否启用 | INDEX |
| created_at | datetime | 创建时间 | - |
| updated_at | datetime | 更新时间 | - |

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

### API 请求/响应结构

#### POST /factor/definitions - 创建因子

**请求体**:
```json
{
  "name": "momentum_5d",
  "code": "(close_price - REF(close_price, 5)) / REF(close_price, 5)",
  "category": "动量趋势",
  "description": "5日动量因子",
  "formula_type": "expression"
}
```

**响应**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "momentum_5d",
    "code": "(close_price - REF(close_price, 5)) / REF(close_price, 5)",
    "category": "动量趋势",
    "description": "5日动量因子",
    "source": "user",
    "is_active": true,
    "created_at": "2025-03-25T10:00:00Z"
  },
  "message": "因子创建成功"
}
```

#### POST /factor/validate - 验证因子公式

**请求体**:
```json
{
  "code": "SMA(close_price, 20) / close_price",
  "formula_type": "expression"
}
```

**响应**:
```json
{
  "success": true,
  "data": {
    "valid": true,
    "message": "公式验证通过"
  }
}
```

#### POST /factor/calculate - 计算因子值

**请求体**:
```json
{
  "factor_ids": [1, 2, 3],
  "stock_codes": ["000001", "000002"],
  "start_date": "2024-01-01",
  "end_date": "2024-12-31"
}
```

**响应**:
```json
{
  "success": true,
  "data": {
    "task_id": "calc_20250325_001",
    "status": "pending"
  },
  "message": "计算任务已启动"
}
```

### API 权限控制

| 接口 | 权限要求 |
|------|----------|
| GET /factor/definitions | 登录用户 |
| POST /factor/definitions | 登录用户 |
| PUT /factor/definitions/{id} | 因子创建者或管理员 |
| DELETE /factor/definitions/{id} | 因子创建者或管理员 |
| POST /factor/mining/start | 登录用户 |
| POST /factor/portfolio | 登录用户 |

---

## 公式执行安全机制

### 安全沙箱设计

```python
# 允许的函数白名单
ALLOWED_FUNCTIONS = {
    # 数学运算
    'abs', 'min', 'max', 'sum', 'pow', 'round',
    # numpy 函数
    'np.log', 'np.sqrt', 'np.abs', 'np.mean', 'np.std',
    # pandas 滚动函数
    'rolling', 'shift', 'pct_change', 'rank',
    # 技术指标函数（通过封装）
    'SMA', 'EMA', 'RSI', 'MACD', 'ATR', 'ADX', 'BBANDS',
    # 麦语言函数
    'REF', 'HHV', 'LLV', 'CROSS', 'EVERY', 'EXIST', 'IF',
    'COUNT', 'SUM', 'AVE', 'STD'
}

# 执行限制
MAX_EXPRESSION_DEPTH = 15      # 最大表达式嵌套深度
MAX_EXECUTION_TIME = 30        # 最大执行时间（秒）
MAX_MEMORY_USAGE = 512         # 最大内存使用（MB）
MAX_LOOP_ITERATIONS = 10000    # 最大循环次数
```

### 表达式验证流程

```
1. 语法检查
   ├── AST 解析验证
   └── 禁止危险语法（import, exec, eval, open, etc.）

2. 函数白名单检查
   └── 所有函数调用必须在 ALLOWED_FUNCTIONS 中

3. 复杂度检查
   ├── 嵌套深度检查
   └── 表达式长度检查

4. 沙箱执行测试
   ├── 使用测试数据执行
   ├── 超时保护
   └── 内存限制
```

### 危险操作防护

```python
# 禁止的内置函数
FORBIDDEN_BUILTINS = {
    'import', '__import__', 'exec', 'eval', 'compile',
    'open', 'input', 'breakpoint', 'exit', 'quit',
    'globals', 'locals', 'vars', 'dir',
    'getattr', 'setattr', 'delattr', 'hasattr',
    'type', 'object', 'class',
}

# 沙箱执行环境
def create_safe_namespace(df: pd.DataFrame) -> dict:
    """创建安全的执行命名空间"""
    return {
        '__builtins__': {},  # 禁止所有内置函数
        # 安全的数据访问
        'close_price': df['close_price'],
        'open_price': df['open_price'],
        'high_price': df['high_price'],
        'low_price': df['low_price'],
        'volume': df['volume'],
        # 别名（兼容简写）
        'close': df['close_price'],
        'open': df['open_price'],
        'high': df['high_price'],
        'low': df['low_price'],
        # 允许的函数
        'np': safe_numpy,  # 受限的 numpy
        'pd': safe_pandas,  # 受限的 pandas
        **SAFE_FUNCTIONS,  # 白名单函数
    }
```

---

## 因子计算引擎

### 表达式解析实现

```python
class FactorCalculator:
    """因子计算引擎"""

    def __init__(self):
        self.mylanguage_funcs = {
            'REF': self._ref,      # 引用N日前值
            'HHV': self._hhv,      # N日最高值
            'LLV': self._llv,      # N日最低值
            'SMA': self._sma,      # 简单移动平均
            'EMA': self._ema,      # 指数移动平均
            'CROSS': self._cross,  # 金叉
            'EVERY': self._every,  # 连续满足
            'EXIST': self._exist,  # 存在满足
        }
        self.talib_funcs = {
            'RSI': talib.RSI,
            'MACD': talib.MACD,
            'ATR': talib.ATR,
            'ADX': talib.ADX,
            'BBANDS': talib.BBANDS,
        }

    def calculate(self, df: pd.DataFrame, code: str) -> pd.Series:
        """计算因子值"""
        # 1. 创建安全命名空间
        namespace = create_safe_namespace(df)

        # 2. 添加麦语言函数
        namespace.update(self.mylanguage_funcs)

        # 3. 添加TALib函数（已封装）
        namespace.update(self.talib_funcs)

        # 4. 在沙箱中执行
        with timeout(MAX_EXECUTION_TIME):
            result = eval(code, {'__builtins__': {}}, namespace)

        return result

    def _ref(self, series, n: int) -> pd.Series:
        """引用N日前值"""
        return series.shift(n)

    def _hhv(self, series, n: int) -> pd.Series:
        """N日最高值"""
        return series.rolling(n, min_periods=1).max()

    def _llv(self, series, n: int) -> pd.Series:
        """N日最低值"""
        return series.rolling(n, min_periods=1).min()

    def _sma(self, series, n: int) -> pd.Series:
        """简单移动平均"""
        return series.rolling(n, min_periods=1).mean()

    def _cross(self, series1, series2) -> pd.Series:
        """金叉信号"""
        return (series1 > series2) & (series1.shift(1) <= series2.shift(1))

    def _every(self, condition, n: int) -> pd.Series:
        """连续N日满足条件"""
        return condition.rolling(n, min_periods=1).apply(lambda x: x.all())
```

---

## 预置因子库

### 字段命名规范

所有因子公式使用现有数据库字段名：
- `close_price` - 收盘价
- `open_price` - 开盘价
- `high_price` - 最高价
- `low_price` - 最低价
- `volume` - 成交量

**别名支持**: 为方便输入，同时支持 `close`, `open`, `high`, `low` 别名。

### 价格收益率

| 因子名 | 公式 | 说明 |
|--------|------|------|
| log_return_1 | `np.log(close_price / REF(close_price, 1))` | 日对数收益率 |
| log_return_5 | `np.log(close_price / REF(close_price, 5))` | 5日累计收益 |
| price_vs_sma20 | `close_price / SMA(close_price, 20)` | 相对20日均线位置 |
| close_open_ratio | `close_price / open_price` | 收盘相对开盘强度 |

### 动量趋势

| 因子名 | 公式 | 说明 |
|--------|------|------|
| rsi_14 | `RSI(close_price, 14)` | RSI指标 |
| macd_line | `MACD(close_price, 12, 26, 9)[0]` | MACD差值线 |
| adx_14 | `ADX(high_price, low_price, close_price, 14)` | 趋势强度 |
| roc_10 | `(close_price - REF(close_price, 10)) / REF(close_price, 10)` | 10日变化率 |

### 波动率风险

| 因子名 | 公式 | 说明 |
|--------|------|------|
| atr_14 | `ATR(high_price, low_price, close_price, 14)` | 平均真实波幅 |
| volatility_20 | `close_price.pct_change().rolling(20).std()` | 20日波动率 |
| bollinger_bandwidth | `(BBANDS(close_price, 20)[0] - BBANDS(close_price, 20)[2]) / BBANDS(close_price, 20)[1]` | 布林带宽度 |

### 成交量资金流

| 因子名 | 公式 | 说明 |
|--------|------|------|
| volume_ma_ratio | `volume / SMA(volume, 10)` | 量比 |
| obv | `OBV(close_price, volume)` | 累积量能 |
| force_index | `(close_price - REF(close_price, 1)) * volume` | 强力指数 |

### 技术形态

| 因子名 | 公式 | 说明 |
|--------|------|------|
| golden_cross | `CROSS(SMA(close_price, 5), SMA(close_price, 20))` | 金叉信号 |
| new_high_20 | `close_price >= HHV(high_price, 20)` | 触及20日新高 |
| three_rising | `EVERY(close_price > open_price, 3)` | 三连阳 |

### 反转信号

| 因子名 | 公式 | 说明 |
|--------|------|------|
| reversal_5 | `-(close_price / REF(close_price, 5) - 1)` | 5日反转因子 |
| deviation_ma20 | `(close_price - SMA(close_price, 20)) / SMA(close_price, 20)` | 偏离均线程度 |
| stochastic_k | `(close_price - LLV(low_price, 14)) / (HHV(high_price, 14) - LLV(low_price, 14) + 1e-10)` | 随机指标K值 |

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
   ├── 定义终端集合（open_price、close_price、high_price、low_price、volume）
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

### 挖掘任务配置验证

```python
MINING_CONFIG_SCHEMA = {
    'stock_codes': {
        'type': 'list',
        'required': True,
        'max_length': 100,  # 最多100只股票
    },
    'start_date': {
        'type': 'date',
        'required': True,
    },
    'end_date': {
        'type': 'date',
        'required': True,
    },
    'population_size': {
        'type': 'int',
        'min': 10,
        'max': 200,
        'default': 50,
    },
    'n_generations': {
        'type': 'int',
        'min': 5,
        'max': 100,
        'default': 20,
    },
    'base_factors': {
        'type': 'list',
        'max_length': 20,  # 最多20个基础因子
    },
}
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

## 性能优化策略

### 数据缓存策略

```python
# 因子值缓存配置
CACHE_CONFIG = {
    'factor_value': {
        'backend': 'redis',
        'ttl': 86400,  # 1天
        'key_pattern': 'factor:{factor_id}:{stock_code}:{date}',
    },
    'factor_test_result': {
        'backend': 'redis',
        'ttl': 604800,  # 7天
    },
}
```

### 数据分区策略

```sql
-- factor_value 表按年度分区
CREATE TABLE factor_value (
    ...
) PARTITION BY RANGE (trade_date);

CREATE TABLE factor_value_2024 PARTITION OF factor_value
    FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');

CREATE TABLE factor_value_2025 PARTITION OF factor_value
    FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');
```

### 数据清理策略

```python
# 定期清理过期因子值
DATA_RETENTION_CONFIG = {
    'factor_value': {
        'retention_days': 365,  # 保留1年
        'cleanup_frequency': 'monthly',
    },
}
```

---

## 技术依赖

### 新增 Python 依赖

```toml
# pyproject.toml 或 requirements.txt
talib>=0.4.28      # 技术分析库（Windows需预编译wheel）
deap>=1.3.0        # 遗传算法框架
scipy>=1.10.0      # 统计检验
redis>=4.5.0       # 缓存（可选）
```

### TALib 安装指引

**Windows**:
```bash
# 下载预编译wheel（推荐）
pip install TA_Lib-0.4.28-cp311-cp311-win_amd64.whl

# 或使用conda
conda install -c conda-forge ta-lib
```

**Linux**:
```bash
sudo apt-get install ta-lib
pip install TA-Lib
```

**macOS**:
```bash
brew install ta-lib
pip install TA-Lib
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
- 公式编辑器（带语法高亮和验证）

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
3. 公式执行沙箱
4. 基础 IC/IR 检验
5. 预置因子库初始化

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
5. **安全风险**: 用户定义公式需要沙箱隔离

---

## 参考资料

- FactorHub 开源项目: https://github.com/FactorHub/FactorHub
- TALib 文档: https://ta-lib.org/
- DEAP 文档: https://deap.readthedocs.io/