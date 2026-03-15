# 热门头条功能开发计划

## 功能概述
在项目中增加"热门头条"页面，展示各大平台的实时热门新闻/话题。数据获取逻辑统一放在 stock-service 微服务中，backend 只负责调用 stock-service 的接口。

## 实现状态

✅ **已完成**

## 架构设计

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (前端)                          │
│   src/views/Vadmin/Stock/HotNews/HotNews.vue                │
│   src/api/stock/hotNews.ts                                   │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                  Backend (端口 8000)                         │
│  主应用 - 业务逻辑、权限控制、调用 stock-service              │
│  apps/admin/stock/hot_news.py                                │
│  apps/admin/stock/services/hot_news_service.py               │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              stock-service (端口 8001) - 独立服务            │
│  数据服务 - 所有数据对接、提供查询接口                         │
│  app/services/hot_news_service.py                            │
│  app/api/endpoints/hot_news_routes.py                        │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    外部数据源                                 │
│  微博 / 知乎 / 雪球 / 金十数据 / 华尔街见闻 / Hacker News 等   │
└─────────────────────────────────────────────────────────────┘
```

## 文件结构

### Frontend (前端)
```
frontend/src/
├── api/stock/
│   └── hotNews.ts           # 热门新闻 API 服务
└── views/Vadmin/Stock/
    └── HotNews/
        └── HotNews.vue      # 热门头条页面组件
```

### stock-service (数据获取)
```
backend/stock-service/app/
├── services/
│   └── hot_news_service.py  # 新闻数据获取服务 (爬取逻辑)
└── api/endpoints/
    └── hot_news_routes.py   # API 路由
```

### backend (接口调用)
```
backend/apps/admin/stock/
├── hot_news.py              # 热门头条 API 接口
└── services/
    └── hot_news_service.py  # 调用 stock-service 接口
```

## 前端页面功能

### 页面特性
- 分类切换：财经 / 综合 / 科技
- 新闻卡片网格布局
- 实时刷新（5分钟自动刷新）
- 单独刷新某个数据源
- 排名高亮显示（前三名）
- 链接跳转到原始新闻

### 路由配置
- 路径：`/stock/hot-news`
- 名称：`HotNews`
- 标题：热门头条

## API 接口

### stock-service 接口 (端口 8001)

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/hot-news/sources` | 获取所有数据源列表 |
| GET | `/api/v1/hot-news/{source_id}` | 获取指定数据源的热门新闻 |
| POST | `/api/v1/hot-news/batch` | 批量获取多个数据源 |
| GET | `/api/v1/hot-news/column/{column}` | 按分类获取热门新闻 |

### backend 接口 (端口 8000)

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/stock/hot-news/sources` | 获取所有数据源列表 |
| GET | `/api/stock/hot-news/{source_id}` | 获取指定数据源的热门新闻 |
| POST | `/api/stock/hot-news/batch` | 批量获取多个数据源 |
| GET | `/api/stock/hot-news/column/{column}` | 按分类获取热门新闻 |

## 已实现的数据源

### 财经类
| 数据源ID | 名称 | 说明 | 状态 |
|----------|------|------|------|
| xueqiu | 雪球 | 热门股票 | ✅ |
| jin10 | 金十数据 | 快讯 | ✅ |
| wallstreetcn-quick | 华尔街见闻 | 快讯 | ✅ |
| wallstreetcn-news | 华尔街见闻 | 新闻 | ✅ |
| wallstreetcn-hot | 华尔街见闻 | 热门 | ✅ |

### 综合类
| 数据源ID | 名称 | 说明 | 状态 |
|----------|------|------|------|
| weibo | 微博 | 实时热搜 | ✅ |
| zhihu | 知乎 | 热榜 | ✅ |
| baidu | 百度热搜 | 热搜 | ✅ |

### 科技类
| 数据源ID | 名称 | 说明 | 状态 |
|----------|------|------|------|
| hackernews | Hacker News | 热门 | ✅ |

## 返回数据格式

### 数据源列表
```json
{
  "code": 200,
  "data": {
    "total": 22,
    "sources": [
      {
        "id": "weibo",
        "name": "微博",
        "title": "实时热搜",
        "column": "china",
        "color": "red",
        "available": true
      }
    ]
  }
}
```

### 新闻列表
```json
{
  "code": 200,
  "data": {
    "status": "success",
    "source_id": "weibo",
    "source_name": "微博",
    "updated_time": 1710400000,
    "items": [
      {
        "id": "热搜标题",
        "title": "热搜标题",
        "url": "https://s.weibo.com/...",
        "mobile_url": "https://s.weibo.com/...",
        "pub_date": null,
        "extra": {
          "icon": {"url": "https://...", "scale": 1.5}
        }
      }
    ]
  }
}
```

## 使用示例

```bash
# 获取微博热搜
curl http://localhost:8000/api/stock/hot-news/weibo

# 获取知乎热榜
curl http://localhost:8000/api/stock/hot-news/zhihu

# 获取雪球热门股票
curl http://localhost:8000/api/stock/hot-news/xueqiu

# 获取财经类新闻
curl http://localhost:8000/api/stock/hot-news/column/finance

# 批量获取
curl -X POST http://localhost:8000/api/stock/hot-news/batch \
  -H "Content-Type: application/json" \
  -d '["weibo", "zhihu", "xueqiu"]'
```

## 依赖

### 后端
- httpx: HTTP 请求
- beautifulsoup4: HTML 解析
- lxml: HTML 解析后端

### 前端
- Vue 3
- Element Plus
- TypeScript

## 配置

在 `application/settings.py` 中配置 stock-service 地址：
```python
STOCK_SERVICE_URL = "http://localhost:8001"
```