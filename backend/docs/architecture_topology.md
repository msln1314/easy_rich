# Easy Rich 股票分析系统架构拓扑图

## 一、整体架构拓扑图

```mermaid
graph TB
    subgraph "客户端层"
        WEB[Web浏览器]
        MOBILE[移动端]
        API_CLIENT[API客户端]
    end

    subgraph "前端层 - Vue3"
        FE_APP[前端应用]
        FE_ROUTER[Vue Router]
        FE_STORE[Pinia Store]
        FE_API[API层]
    end

    subgraph "网关层"
        NGINX[Nginx反向代理]
    end

    subgraph "后端服务层"
        subgraph "Admin服务 - FastAPI"
            ADMIN_AUTH[认证授权模块]
            ADMIN_SYSTEM[系统管理模块]
            ADMIN_STOCK[股票管理模块]
        end

        subgraph "Stock-Service微服务 - FastAPI"
            STOCK_API[股票数据API]
            INDEX_API[指数数据API]
            SECTOR_API[板块数据API]
            HOTNEWS_API[热门新闻API]
            TECH_API[技术分析API]
            SENTIMENT_API[情绪分析API]
            EXT_API[扩展数据API]
        end
    end

    subgraph "数据源层"
        AKSHARE[AKShare]
        PYTDX[pytdx]
        SINA[新浪财经]
        GM[掘金量化]
        TUSHARE[Tushare Pro]

        HOT_SOURCES[热门新闻源<br/>微博/知乎/雪球/金十等]
    end

    subgraph "存储层"
        MYSQL[(MySQL)]
        REDIS[(Redis缓存)]
        MONGO[(MongoDB)]
    end

    WEB --> FE_APP
    MOBILE --> FE_APP
    API_CLIENT --> NGINX

    FE_APP --> FE_ROUTER
    FE_APP --> FE_STORE
    FE_APP --> FE_API

    FE_API --> NGINX
    NGINX --> ADMIN_AUTH
    NGINX --> STOCK_API

    ADMIN_AUTH --> ADMIN_SYSTEM
    ADMIN_AUTH --> ADMIN_STOCK

    STOCK_API --> AKSHARE
    STOCK_API --> PYTDX
    STOCK_API --> SINA

    INDEX_API --> AKSHARE
    SECTOR_API --> AKSHARE
    TECH_API --> AKSHARE

    HOTNEWS_API --> HOT_SOURCES

    ADMIN_SYSTEM --> MYSQL
    ADMIN_STOCK --> MYSQL
    ADMIN_STOCK --> REDIS

    STOCK_API --> REDIS
    SENTIMENT_API --> MONGO
```

## 二、热门新闻服务架构拓扑

```mermaid
graph TB
    subgraph "前端展示"
        FE_TAB[Tab切换<br/>更多/关注/最热/实时]
        FE_CARDS[卡片Grid布局]
        FE_LIST[新闻列表]
    end

    subgraph "API网关"
        ROUTER[FastAPI Router]
    end

    subgraph "热门新闻服务"
        SVC_HOT[HotNewsService]
        SVC_CACHE[缓存管理]
        SVC_PARSE[数据解析器]
    end

    subgraph "数据源 - 财经类"
        XUEQIU[雪球<br/>热门股票]
        JIN10[金十数据<br/>快讯]
        WSJ[华尔街见闻<br/>快讯/新闻/热门]
        CLS[财联社<br/>电报/热门]
        GLH[格隆汇<br/>事件]
    end

    subgraph "数据源 - 综合类"
        WEIBO[微博<br/>实时热搜]
        ZHIHU[知乎<br/>热榜]
        BAIDU[百度<br/>热搜]
        TOUTIAO[今日头条<br/>热门]
    end

    subgraph "数据源 - 科技类"
        HACKER[Hacker News<br/>热门]
        GITHUB[GitHub<br/>Trending]
        ITHOME[IT之家<br/>最新]
        JUEJIN[稀土掘金<br/>热门]
    end

    FE_TAB --> FE_CARDS
    FE_CARDS --> FE_LIST
    FE_LIST --> ROUTER

    ROUTER --> SVC_HOT
    SVC_HOT --> SVC_CACHE
    SVC_HOT --> SVC_PARSE

    SVC_PARSE --> XUEQIU
    SVC_PARSE --> JIN10
    SVC_PARSE --> WSJ
    SVC_PARSE --> CLS
    SVC_PARSE --> GLH
    SVC_PARSE --> WEIBO
    SVC_PARSE --> ZHIHU
    SVC_PARSE --> BAIDU
    SVC_PARSE --> TOUTIAO
    SVC_PARSE --> HACKER
    SVC_PARSE --> GITHUB
    SVC_PARSE --> ITHOME
    SVC_PARSE --> JUEJIN

    style XUEQIU fill:#409eff,color:#fff
    style JIN10 fill:#409eff,color:#fff
    style WSJ fill:#409eff,color:#fff
    style CLS fill:#f56c6c,color:#fff
    style WEIBO fill:#f56c6c,color:#fff
    style ZHIHU fill:#409eff,color:#fff
    style HACKER fill:#e6a23c,color:#fff
    style GITHUB fill:#909399,color:#fff
```

## 三、数据流向拓扑图

```mermaid
flowchart LR
    subgraph "数据采集"
        A1[AKShare<br/>A股数据]
        A2[pytdx<br/>通达信]
        A3[新浪财经<br/>实时行情]
        A4[外部API<br/>热门新闻]
    end

    subgraph "数据处理"
        B1[数据清洗]
        B2[格式转换]
        B3[缓存处理]
    end

    subgraph "数据存储"
        C1[(MySQL<br/>持久化)]
        C2[(Redis<br/>缓存)]
        C3[(MongoDB<br/>日志/分析)]
    end

    subgraph "API服务"
        D1[REST API]
        D2[MCP协议]
    end

    subgraph "前端应用"
        E1[数据展示]
        E2[图表渲染]
        E3[用户交互]
    end

    A1 --> B1
    A2 --> B1
    A3 --> B1
    A4 --> B1

    B1 --> B2
    B2 --> B3

    B3 --> C1
    B3 --> C2
    B3 --> C3

    C1 --> D1
    C2 --> D1
    C3 --> D1
    C2 --> D2

    D1 --> E1
    D2 --> E1
    E1 --> E2
    E2 --> E3
```

## 四、部署架构拓扑

```mermaid
graph TB
    subgraph "用户访问"
        USER[用户]
    end

    subgraph "负载均衡层"
        LB[Nginx负载均衡<br/>:80/443]
    end

    subgraph "应用服务器集群"
        FE1[前端静态资源<br/>Nginx]
        FE2[前端静态资源<br/>Nginx]

        BE1[Admin服务<br/>:8000]
        BE2[Admin服务<br/>:8000]

        STOCK1[Stock-Service<br/>:8001]
        STOCK2[Stock-Service<br/>:8001]
    end

    subgraph "数据服务集群"
        MYSQL_MASTER[(MySQL Master)]
        MYSQL_SLAVE[(MySQL Slave)]

        REDIS_CLUSTER[(Redis Cluster)]

        MONGO_CLUSTER[(MongoDB)]
    end

    subgraph "外部数据源"
        EXT_API[外部API<br/>AKShare/新浪等]
    end

    USER --> LB

    LB --> FE1
    LB --> FE2

    LB --> BE1
    LB --> BE2

    LB --> STOCK1
    LB --> STOCK2

    BE1 --> MYSQL_MASTER
    BE2 --> MYSQL_MASTER
    MYSQL_MASTER --> MYSQL_SLAVE

    BE1 --> REDIS_CLUSTER
    BE2 --> REDIS_CLUSTER

    STOCK1 --> REDIS_CLUSTER
    STOCK2 --> REDIS_CLUSTER

    STOCK1 --> MONGO_CLUSTER
    STOCK2 --> MONGO_CLUSTER

    STOCK1 --> EXT_API
    STOCK2 --> EXT_API
```

## 五、模块依赖关系图

```mermaid
graph LR
    subgraph "核心模块"
        CORE[Core配置]
        LOG[日志模块]
        CACHE[缓存模块]
    end

    subgraph "股票模块"
        STOCK_SVC[StockService]
        STOCK_EXT[StockExtended]
        STOCK_TECH[TechnicalService]
    end

    subgraph "市场模块"
        MARKET_SVC[MarketService]
        INDEX_SVC[IndexService]
        SECTOR_SVC[SectorService]
    end

    subgraph "新闻模块"
        NEWS_SVC[NewsService]
        HOTNEWS_SVC[HotNewsService]
        SENTIMENT_SVC[SentimentService]
    end

    subgraph "数据源适配器"
        AKSHARE_ADAPTER[AKShare适配器]
        PYTDX_ADAPTER[pytdx适配器]
        HTTP_ADAPTER[HTTP适配器]
    end

    STOCK_SVC --> CORE
    STOCK_SVC --> LOG
    STOCK_SVC --> CACHE

    STOCK_EXT --> STOCK_SVC
    STOCK_TECH --> STOCK_SVC

    MARKET_SVC --> STOCK_SVC
    INDEX_SVC --> STOCK_SVC
    SECTOR_SVC --> STOCK_SVC

    HOTNEWS_SVC --> CORE
    HOTNEWS_SVC --> LOG
    HOTNEWS_SVC --> HTTP_ADAPTER

    SENTIMENT_SVC --> NEWS_SVC

    STOCK_SVC --> AKSHARE_ADAPTER
    STOCK_SVC --> PYTDX_ADAPTER

    HOTNEWS_SVC --> HTTP_ADAPTER
```

---

## 架构说明

### 层级划分

| 层级 | 组件 | 职责 |
|------|------|------|
| **客户端层** | Web/Mobile/API Client | 用户交互入口 |
| **网关层** | Nginx | 反向代理、负载均衡、静态资源 |
| **前端层** | Vue3 + Element Plus | 页面渲染、状态管理、API调用 |
| **后端服务层** | FastAPI微服务 | 业务逻辑、数据处理、API提供 |
| **数据源层** | AKShare/pytdx/外部API | 数据采集、实时行情 |
| **存储层** | MySQL/Redis/MongoDB | 数据持久化、缓存、日志存储 |

### 关键特性

1. **微服务架构**: Admin服务与Stock-Service解耦，独立部署
2. **多数据源兼容**: 主备降级策略保证数据可用性
3. **异步处理**: asyncio + httpx实现高并发数据抓取
4. **缓存优化**: Redis缓存减少外部API调用
5. **水平扩展**: 无状态服务设计，支持横向扩展