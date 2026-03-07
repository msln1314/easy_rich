# Stock-AKShare 股票数据服务

基于 AKShare 的股票数据服务，提供 FastAPI 和 MCP 双接口模式，为股票分析系统提供稳定、高效的数据支持。

## 设计思想

本项目主要是利用 AKShare 的接口，重新构建 FastAPI 和 MCP 服务，以便为股票分析系统提供完备的数据。主要设计思想如下：

1. **双接口模式**：同时提供 REST API 和 MCP 接口，满足不同场景的需求
   - REST API：适合前端直接调用，提供标准的 HTTP 接口
   - MCP 接口：适合后端服务间调用，提供高性能的 RPC 调用

2. **数据缓存机制**：集成 Redis 缓存，提高数据访问效率
   - 对热点数据进行缓存，减少对 AKShare 的直接调用
   - 通过缓存策略，平衡数据实时性和系统性能

3. **错误处理与稳定性**：
   - 对 AKShare 接口进行封装，统一处理异常情况
   - 将错误尽可能封装在服务内部，减少对调用方的影响
   - 提供优雅的降级和重试机制，提高系统稳定性
   - **多数据源降级策略**：AKShare（主）→ Tushare（备）→ GM（备，部分功能不支持）
   - **akshare-proxy-patch**：自动修复 AKShare 网络连接问题，提高稳定性

4. **模块化设计**：
   - 按业务领域划分模块，如个股信息、指数信息、板块信息等
   - 每个模块独立实现服务层和接口层，便于维护和扩展

5. **统一的数据模型**：
   - 使用 Pydantic 模型定义数据结构，提供类型安全和自动验证
   - 在服务间传递数据时保持一致的数据格式

## 使用方法

### 环境准备

1. 安装依赖：
   ```bash
   cd backend
   uv sync
   ```

2. 配置环境变量（可选）：
   创建 `.env` 文件，配置以下参数：
   ```
   # Redis 缓存配置
   REDIS_URL=redis://localhost:6379/0  # Redis连接地址，用于缓存
   CACHE_ENABLED=true                  # 是否启用缓存
   CACHE_TTL=3600                      # 缓存过期时间（秒）

   # Tushare Pro 配置（备用数据源）
   TUSHARE_TOKEN=your_token_here        # Tushare Pro API token，从 https://tushare.pro/register 获取

   # GM（掘金量化）配置（备用数据源）
   GM_TOKEN=your_token_here           # GM API token（可选，通常不需要）

   # 日志配置
   LOG_LEVEL=INFO                      # 日志级别
   ```

### 启动服务

1. 启动 FastAPI 服务：
   ```bash
   uv run python stock-service/run.py
   ```

2. 服务默认运行在 `http://localhost:8008`，可以通过以下地址访问：
   - API 文档：`http://localhost:8008/docs`
   - MCP 接口：通过 MCP 客户端连接

### 数据源降级策略

本项目采用多数据源降级策略，确保数据获取的稳定性：

| 功能 | 主数据源 | 备用数据源 | 说明 |
|------|----------|------------|------|
| 板块列表 | AKShare | Tushare | GM SDK 不支持板块列表功能 |
| 板块成份股 | AKShare | GM | Tushare 作为第三备用 |
| 个股行情 | AKShare | GM | Tushare 作为第三备用 |
| 历史行情 | AKShare | GM | Tushare 作为第三备用 |

**降级逻辑**：
1. 优先使用主数据源（AKShare）
2. 如果主数据源失败，自动降级到备用数据源
3. 所有数据源都失败时，返回错误信息

**启用 Tushare**：
1. 注册 Tushare Pro 账号：https://tushare.pro/register
2. 获取 API token
3. 在 `.env` 文件中配置 `TUSHARE_TOKEN`
4. 重启服务即可生效

### API 调用示例

1. REST API 调用：
   ```python
   import requests
   
   # 获取概念板块列表
   response = requests.get("http://localhost:8008/api/v1/sector/concept")
   concept_boards = response.json()
   print(concept_boards)
   ```

2. MCP 接口调用：
   ```python
   from mcp.client import MCPClient
   
   # 创建MCP客户端
   client = MCPClient("localhost", 8008)
   
   # 调用概念板块列表接口
   concept_boards = await client.call("get_concept_boards")
   print(concept_boards)
   ```

3. FastMCP 接口调用（推荐）：
   ```python
   from mcp.client import FastMCPClient
   
   # 创建FastMCP客户端
   client = FastMCPClient("http://localhost:8008")
   
   # 调用概念板块列表接口
   concept_boards = await client.get_concept_boards()
   print(concept_boards)
   ```

## API 接口列表

### 基础信息

服务默认运行在 `http://localhost:8008`，所有接口前缀为 `/api/v1`

### 个股信息接口 (`/api/v1/stock`)

| 方法 | 路径 | 描述 | 参数 |
|------|------|------|------|
| GET | `/stock/{stock_code}/info` | 获取个股基本信息 | `stock_code`: 股票代码 |
| GET | `/stock/{stock_code}/quote` | 获取个股实时行情 | `stock_code`: 股票代码 |
| GET | `/stock/{stock_code}/financial` | 获取个股财务信息 | `stock_code`: 股票代码 |
| GET | `/stock/{stock_code}/fund-flow` | 获取个股资金流向 | `stock_code`: 股票代码 |
| GET | `/stock/{stock_code}/margin` | 获取个股融资融券信息 | `stock_code`: 股票代码 |
| GET | `/stock/{stock_code}/history` | 获取个股历史行情数据 | `stock_code`: 股票代码<br>`period`: 数据周期 (daily/weekly/monthly)<br>`start_date`: 开始日期 (YYYYMMDD)<br>`end_date`: 结束日期 (YYYYMMDD) |

### 板块信息接口 (`/api/v1/sector`)

#### 概念板块

| 方法 | 路径 | 描述 | 参数 |
|------|------|------|------|
| GET | `/sector/concept` | 获取概念板块列表及实时行情 | - |
| GET | `/sector/concept/by-name/spot` | 获取概念板块实时行情详情（通过名称） | `name`: 板块名称 |
| GET | `/sector/concept/by-symbol/constituents` | 获取概念板块成份股 | `symbol`: 板块名称或代码 |
| GET | `/sector/concept/by-params/info` | 获取概念板块基本信息 | `code`: 板块代码<br>`name`: 板块名称 |
| GET | `/sector/concept/{board_code}` | 获取单个概念板块的实时行情 | `board_code`: 板块代码 |
| GET | `/sector/concept/{board_code}/spot` | 获取概念板块实时行情详情（通过代码） | `board_code`: 板块代码 |
| GET | `/sector/concept/{board_code}/constituents` | 通过板块代码获取概念板块成份股 | `board_code`: 板块代码 |

#### 行业板块

| 方法 | 路径 | 描述 | 参数 |
|------|------|------|------|
| GET | `/sector/industry` | 获取行业板块列表及实时行情 | - |
| GET | `/sector/industry/by-name/spot` | 获取行业板块实时行情详情 | `board_name`: 板块名称 |
| GET | `/sector/industry/by-symbol/constituents` | 获取行业板块成份股 | `symbol`: 板块名称或代码 |
| GET | `/sector/industry/{board_code}` | 获取单个行业板块的实时行情 | `board_code`: 板块代码 |
| GET | `/sector/industry/{board_code}/spot` | 获取行业板块实时行情详情（通过代码） | `board_code`: 板块代码 |
| GET | `/sector/industry/{board_code}/constituents` | 通过板块代码获取行业板块成份股 | `board_code`: 板块代码 |

### 指数信息接口 (`/api/v1/index`)

| 方法 | 路径 | 描述 | 参数 |
|------|------|------|------|
| GET | `/index/quotes` | 获取指数实时行情列表 | `symbol`: 指数类型（默认：沪深重要指数） |
| GET | `/index/{index_code}` | 获取单个指数实时行情 | `index_code`: 指数代码 |

### 市场情绪接口 (`/api/v1/sentiment`)

| 方法 | 路径 | 描述 | 参数 |
|------|------|------|------|
| GET | `/sentiment/margin/details` | 获取融资融券明细数据 | `trade_date`: 交易日期 (YYYYMMDD) |
| GET | `/sentiment/stock/hot-rank` | 获取股票热度排名数据 | - |
| GET | `/sentiment/stock/hot-up-rank` | 获取股票飙升榜数据 | - |
| GET | `/sentiment/stock/hot-keywords` | 获取股票热门关键词数据 | `symbol`: 股票代码 |

### 技术指标接口 (`/api/v1/technical`)

| 方法 | 路径 | 描述 | 参数 |
|------|------|------|------|
| GET | `/technical/chip-distribution` | 获取股票筹码分布数据 | `symbol`: 股票代码<br>`adjust`: 复权类型 (qfq/hfq/空) |

### 资讯信息接口 (`/api/v1/news`)

| 方法 | 路径 | 描述 | 参数 |
|------|------|------|------|
| GET | `/news/interactive/questions` | 获取互动易提问数据 | `symbol`: 股票代码 |
| GET | `/news/global-finance` | 获取全球财经快讯数据 | - |
| GET | `/news/cls-telegraph` | 获取财联社电报数据 | `symbol`: 类型（全部/重点） |

## 目录结构

```
stock-akshare/
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI主应用
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py            # 配置文件
│   │   └── logging.py           # 日志配置
│   ├── api/
│   │   ├── __init__.py
│   │   ├── endpoints/           # REST API端点
│   │   │   ├── __init__.py
│   │   │   ├── stock.py         # 个股信息API
│   │   │   ├── index.py         # 指数信息API
│   │   │   ├── sector.py        # 板块信息API
│   │   │   ├── sentiment.py     # 市场情绪API
│   │   │   ├── technical.py     # 技术指标API
│   │   │   └── news.py          # 资讯信息API
│   │   └── router.py            # API路由聚合
│   ├── services/                # 业务服务层
│   │   ├── __init__.py
│   │   ├── stock_service.py     # 个股信息服务
│   │   ├── index_service.py     # 指数信息服务
│   │   ├── sector_service.py    # 板块信息服务
│   │   ├── sentiment_service.py # 市场情绪服务
│   │   ├── technical_service.py # 技术指标服务
│   │   └── news_service.py      # 资讯信息服务
│   ├── models/                  # 数据模型
│   │   ├── __init__.py
│   │   ├── stock_models.py      # 个股相关模型
│   │   ├── index_models.py      # 指数相关模型
│   │   ├── sector_models.py     # 板块相关模型
│   │   ├── sentiment_models.py  # 市场情绪相关模型
│   │   ├── technical_models.py  # 技术指标相关模型
│   │   └── news_models.py       # 资讯相关模型
│   ├── utils/                   # 工具函数
│   │   ├── __init__.py
│   │   ├── akshare_wrapper.py   # AKShare接口封装
│   │   ├── cache.py             # 缓存工具
│   │   └── helpers.py           # 辅助函数
│   └── mcp/                     # MCP接口
│       ├── __init__.py
│       ├── router.py            # MCP路由
│       ├── stock_mcp.py         # 个股信息MCP
│       ├── index_mcp.py         # 指数信息MCP
│       ├── sector_mcp.py        # 板块信息MCP
│       ├── sentiment_mcp.py     # 市场情绪MCP
│       ├── technical_mcp.py     # 技术指标MCP
│       └── news_mcp.py          # 资讯信息MCP
├── tests/                       # 测试
│   ├── __init__.py
│   ├── test_api/               # API测试
│   │   ├── __init__.py
│   │   ├── test_stock.py
│   │   └── ...
│   └── test_services/          # 服务测试
│       ├── __init__.py
│       ├── test_stock_service.py
│       └── ...
├── .env                         # 环境变量
├── .gitignore
├── requirements.txt             # 依赖包
├── README.md                    # 项目说明
└── run.py                       # 启动脚本
```

## 升级建议

为了进一步提高开发效率和代码质量，建议考虑使用 FastMCP 来简化 MCP 接口的实现：

```python
from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP

app = FastAPI()
mcp = FastMCP(app)

@mcp.method("get_concept_boards")
async def get_concept_boards():
    """获取概念板块列表及实时行情"""
    sector_service = SectorService()
    return await sector_service.get_concept_boards()
```

使用 FastMCP 的主要优势：
1. 代码更简洁，减少重复性工作
2. 更好的类型支持和自动文档生成
3. 统一的错误处理和日志记录
4. 更容易维护和扩展

## 贡献

欢迎提交 Issue 和 Pull Request 来帮助改进项目。

## 许可

[MIT License](LICENSE)