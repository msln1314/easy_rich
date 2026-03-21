# 投资日历功能设计文档

## 1. 概述

### 1.1 功能定位

投资日历是一个综合规划型功能模块，帮助用户：
- **不遗漏重要节点**：财报发布、分红除权、解禁日等关键事件提前知悉
- **提前布局机会**：基于历史规律识别季节性板块机会
- **智能关联个股**：所有事件与用户自选股深度联动
- **AI辅助决策**：事件影响分析、投资建议自动生成

### 1.2 核心特性

| 特性 | 描述 |
|-----|------|
| 多视图展示 | 支持月历、周历、时间线三种视图切换 |
| 个股关联 | 每个事件精确关联到具体股票，支持自选股筛选 |
| 智能提醒 | 支持提前1-7天提醒，系统通知/邮件双通道 |
| AI分析 | 事件影响评分、情感判断、操作建议 |
| 模块联动 | 与自选股、监听策略、板块轮动深度集成 |

### 1.3 技术栈

- **前端**：Vue 3 + Element Plus + TypeScript + ECharts
- **后端**：FastAPI + SQLAlchemy 2.0 + MySQL + APScheduler
- **数据源**：AkShare（东方财富、巨潮资讯）
- **AI**：用户提供的AI模型API

---

## 2. 系统架构

### 2.1 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                        前端层                                │
├──────────────┬──────────────┬──────────────┬────────────────┤
│  月历视图     │  周历视图     │  时间线视图   │  AI洞察面板    │
│  CalendarMonth│ CalendarWeek │ TimelineView │ AIAnalysisPanel│
└──────────────┴──────────────┴──────────────┴────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                        API网关层                             │
├──────────────┬──────────────┬──────────────┬────────────────┤
│ 事件管理API   │ 提醒服务API   │ AI分析API    │ 数据同步API     │
│ /events      │ /reminders   │ /analysis    │ /sync          │
└──────────────┴──────────────┴──────────────┴────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                        服务层                                │
├──────────────┬──────────────┬──────────────┬────────────────┤
│ EventService │ ReminderService│ AIService  │ SyncService    │
│ 事件业务逻辑  │ 提醒业务逻辑   │ AI分析逻辑   │ 数据同步逻辑    │
└──────────────┴──────────────┴──────────────┴────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                        数据层                                │
├──────────────┬──────────────┬──────────────┬────────────────┤
│ MySQL存储    │ AkShare采集   │ AI模型调用   │ Redis缓存      │
└──────────────┴──────────────┴──────────────┴────────────────┘
```

### 2.2 模块依赖

```
投资日历
    │
    ├── 依赖 → 自选股模块（获取用户自选股列表）
    │
    ├── 依赖 → 监听策略模块（事件触发策略提醒）
    │
    ├── 依赖 → 定时任务模块（数据同步调度）
    │
    └── 依赖 → AI服务（事件分析）
```

---

## 3. 数据模型

### 3.1 个股事件表 (stock_calendar_event)

存储所有与个股相关的事件信息。

```sql
CREATE TABLE stock_calendar_event (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    
    -- 股票信息
    stock_code VARCHAR(20) NOT NULL COMMENT '股票代码',
    stock_name VARCHAR(100) COMMENT '股票名称',
    
    -- 事件信息
    event_type VARCHAR(50) NOT NULL COMMENT '事件类型',
    event_date DATE NOT NULL COMMENT '事件日期',
    event_time TIME COMMENT '事件时间',
    title VARCHAR(500) NOT NULL COMMENT '事件标题',
    content TEXT COMMENT '事件详情',
    
    -- 事件影响数据
    impact_data JSON COMMENT '事件影响数据JSON',
    
    -- AI分析结果
    ai_impact_score DECIMAL(5,2) COMMENT '影响评分 -5~5',
    ai_sentiment TINYINT COMMENT '情感: 1-利好 2-中性 3-利空',
    ai_analysis TEXT COMMENT 'AI影响分析',
    ai_suggestion TEXT COMMENT 'AI操作建议',
    
    -- 辅助字段
    is_in_watchlist TINYINT DEFAULT 0 COMMENT '是否在用户自选股中',
    data_source VARCHAR(50) DEFAULT 'akshare' COMMENT '数据来源',
    source_url VARCHAR(500) COMMENT '来源链接',
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_stock_code (stock_code),
    INDEX idx_event_date (event_date),
    INDEX idx_event_type (event_type),
    INDEX idx_is_watchlist (is_in_watchlist),
    INDEX idx_date_type (event_date, event_type)
) COMMENT '个股日历事件表';
```

### 3.2 事件类型枚举

| 事件类型 | 英文标识 | 描述 |
|---------|---------|------|
| 财报发布 | earnings_report | 年报/季报发布日期 |
| 业绩预告 | earnings_forecast | 业绩预告发布 |
| 分红除权 | dividend | 分红派息、除权除息 |
| 解禁日 | unlock | 限售股解禁 |
| 股东大会 | shareholders_mtg | 股东大会召开 |
| 新股上市 | ipo_listing | 新股上市日期 |
| 评级变动 | rating_change | 机构评级调整 |
| 大宗交易 | block_trade | 大宗交易信息 |
| 回购 | repurchase | 股票回购 |
| 重要公告 | major_news | 重大事项公告 |

### 3.3 用户提醒表 (stock_event_reminder)

存储用户设置的事件提醒。

```sql
CREATE TABLE stock_event_reminder (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL COMMENT '用户ID',
    stock_code VARCHAR(20) NOT NULL COMMENT '股票代码',
    event_id BIGINT NOT NULL COMMENT '事件ID',
    
    remind_days INT DEFAULT 1 COMMENT '提前几天提醒: 1-7',
    remind_time TIME DEFAULT '09:00:00' COMMENT '提醒时间',
    remind_type VARCHAR(20) DEFAULT 'system' COMMENT '提醒方式: system/email',
    is_active TINYINT DEFAULT 1 COMMENT '是否启用',
    
    last_remind_at DATETIME COMMENT '上次提醒时间',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    UNIQUE KEY uk_user_stock_event (user_id, stock_code, event_id),
    INDEX idx_user_active (user_id, is_active),
    INDEX idx_remind_date (remind_days)
) COMMENT '用户事件提醒表';
```

### 3.4 宏观事件表 (invest_calendar_event)

存储宏观经济事件、政策发布等非个股事件。

```sql
CREATE TABLE invest_calendar_event (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    
    event_type VARCHAR(50) NOT NULL COMMENT '事件类型: macro/policy/meeting',
    title VARCHAR(500) NOT NULL COMMENT '事件标题',
    content TEXT COMMENT '事件详情',
    
    event_date DATE NOT NULL COMMENT '事件日期',
    event_time TIME COMMENT '事件时间',
    importance TINYINT DEFAULT 2 COMMENT '重要程度: 1-低 2-中 3-高',
    
    -- 关联信息
    related_stocks JSON COMMENT '关联股票代码列表',
    related_sectors JSON COMMENT '关联板块列表',
    
    -- AI分析
    ai_analysis TEXT COMMENT 'AI分析的事件影响',
    ai_sentiment TINYINT COMMENT 'AI情感: 1-利好 2-中性 3-利空',
    ai_suggestion TEXT COMMENT 'AI投资建议',
    
    data_source VARCHAR(50) DEFAULT 'akshare' COMMENT '数据来源',
    source_url VARCHAR(500) COMMENT '来源链接',
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_event_date (event_date),
    INDEX idx_event_type (event_type),
    INDEX idx_importance (importance)
) COMMENT '投资日历宏观事件表';
```

### 3.5 板块轮动机会表 (sector_rotation_opportunity)

存储基于历史规律和AI预测的板块投资机会。

```sql
CREATE TABLE sector_rotation_opportunity (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    
    sector_name VARCHAR(100) NOT NULL COMMENT '板块名称',
    sector_code VARCHAR(50) COMMENT '板块代码',
    
    opportunity_type VARCHAR(50) COMMENT '机会类型: seasonal/policy/event',
    start_date DATE COMMENT '机会开始日期',
    end_date DATE COMMENT '机会结束日期',
    
    confidence_score DECIMAL(5,2) COMMENT 'AI置信度评分 0-100',
    historical_return DECIMAL(10,4) COMMENT '历史平均收益率',
    win_rate DECIMAL(5,2) COMMENT '历史胜率',
    
    description TEXT COMMENT '机会描述',
    ai_analysis TEXT COMMENT 'AI详细分析',
    related_stocks JSON COMMENT '相关个股列表',
    
    is_active TINYINT DEFAULT 1 COMMENT '是否有效',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_sector (sector_name),
    INDEX idx_dates (start_date, end_date),
    INDEX idx_active (is_active)
) COMMENT '板块轮动机会表';
```

---

## 4. API接口设计

### 4.1 事件管理接口

#### 获取事件列表
```
GET /api/stock_calendar/events

参数:
- start_date: 开始日期 (可选)
- end_date: 结束日期 (可选)
- stock_code: 股票代码 (可选)
- event_type: 事件类型 (可选)
- is_watchlist: 是否仅自选股 (可选，默认false)
- page: 页码
- page_size: 每页数量

响应:
{
  "code": 200,
  "data": {
    "total": 100,
    "items": [
      {
        "id": 1,
        "stock_code": "000001",
        "stock_name": "平安银行",
        "event_type": "earnings_report",
        "event_date": "2026-03-25",
        "title": "2025年年报发布",
        "ai_impact_score": 2.5,
        "ai_sentiment": 1
      }
    ]
  }
}
```

#### 获取自选股相关事件
```
GET /api/stock_calendar/events/my_watchlist

参数:
- user_id: 用户ID (必填)
- days: 未来天数 (可选，默认30)

响应: 同事件列表
```

#### 获取某股票的所有事件
```
GET /api/stock_calendar/events/by_stock/{stock_code}

参数:
- days: 未来天数 (可选，默认90)

响应: 同事件列表
```

#### 获取某日期的所有事件
```
GET /api/stock_calendar/events/by_date/{date}

响应: 同事件列表
```

#### 添加自定义事件
```
POST /api/stock_calendar/events

请求体:
{
  "stock_code": "000001",
  "event_type": "major_news",
  "event_date": "2026-04-01",
  "title": "自定义事件标题",
  "content": "事件详情"
}
```

### 4.2 提醒管理接口

#### 获取用户提醒列表
```
GET /api/stock_calendar/reminders

参数:
- user_id: 用户ID
- is_active: 是否启用 (可选)
```

#### 创建提醒
```
POST /api/stock_calendar/reminders

请求体:
{
  "user_id": 1,
  "stock_code": "000001",
  "event_id": 123,
  "remind_days": 3,
  "remind_time": "09:00:00",
  "remind_type": "system"
}
```

#### 更新提醒
```
PUT /api/stock_calendar/reminders/{reminder_id}

请求体: 同创建
```

#### 删除提醒
```
DELETE /api/stock_calendar/reminders/{reminder_id}
```

### 4.3 AI分析接口

#### 分析单个事件影响
```
POST /api/stock_calendar/analysis/event/{event_id}

响应:
{
  "code": 200,
  "data": {
    "impact_score": 2.5,
    "sentiment": 1,
    "analysis": "该财报预期净利润同比增长15%...",
    "suggestion": "建议关注业绩兑现情况..."
  }
}
```

#### 分析股票近期事件影响
```
POST /api/stock_calendar/analysis/stock/{stock_code}

参数:
- days: 分析未来天数 (默认30)

响应:
{
  "code": 200,
  "data": {
    "events": [...],
    "overall_score": 1.8,
    "overall_sentiment": 1,
    "summary": "未来30天有3个重要事件...",
    "suggestion": "建议..."
  }
}
```

#### 获取板块轮动机会
```
GET /api/stock_calendar/analysis/opportunities

参数:
- type: 机会类型 (可选)
- min_score: 最低置信度 (可选)

响应:
{
  "code": 200,
  "data": {
    "items": [
      {
        "sector_name": "白酒",
        "opportunity_type": "seasonal",
        "start_date": "2026-04-01",
        "end_date": "2026-04-30",
        "confidence_score": 75.5,
        "historical_return": 8.5,
        "description": "春季糖酒会催化..."
      }
    ]
  }
}
```

### 4.4 数据同步接口

#### 同步财报日历
```
POST /api/stock_calendar/sync/earnings
```

#### 同步分红除权
```
POST /api/stock_calendar/sync/dividends
```

#### 同步解禁日
```
POST /api/stock_calendar/sync/unlocks
```

#### 全量同步
```
POST /api/stock_calendar/sync/all
```

---

## 5. 前端页面设计

### 5.1 页面结构

```
InvestCalendar/
├── InvestCalendar.vue              # 主页面容器
│   ├── Header                      # 顶部操作栏
│   │   ├── ViewToggle              # 视图切换 (月/周/时间线)
│   │   ├── DateNavigator           # 日期导航
│   │   └── FilterPanel             # 筛选面板
│   │
│   ├── MainContent                 # 主内容区
│   │   ├── CalendarMonth           # 月历视图
│   │   ├── CalendarWeek            # 周历视图
│   │   └── TimelineView            # 时间线视图
│   │
│   └── SidePanel                   # 侧边面板
│       ├── WatchlistEvents         # 自选股事件
│       ├── AIInsights              # AI洞察
│       └── Opportunities           # 板块机会
│
└── components/
    ├── EventCard.vue               # 事件卡片组件
    ├── StockEventPanel.vue         # 个股事件详情面板
    ├── AIAnalysisPanel.vue         # AI分析面板
    ├── ReminderDialog.vue          # 提醒设置弹窗
    ├── FilterPanel.vue             # 筛选面板
    ├── EventTypeTag.vue            # 事件类型标签
    └── ImpactScore.vue             # 影响评分组件
```

### 5.2 视图设计

#### 月历视图
- 网格布局，每月一行
- 每个日期单元格显示当日事件数量和重要事件标记
- 点击日期展开当日事件列表
- 支持拖拽选择日期范围

#### 周历视图
- 7列布局，每日一列
- 按时间顺序排列当日事件
- 显示事件类型图标、股票名称、事件标题
- 支持快速添加提醒

#### 时间线视图
- 垂直时间线布局
- 按日期分组，从上到下时间递增
- 每个事件卡片展示完整信息
- 支持按事件类型筛选

### 5.3 交互设计

#### 事件卡片
```
┌─────────────────────────────────────────┐
│ [财报] 平安银行(000001)              ⭐ │
├─────────────────────────────────────────┤
│ 2025年年报发布                          │
│ 日期: 2026-03-25                        │
│                                         │
│ AI影响: ↗ +2.5 (利好)                   │
│ 分析: 净利润预期同比增长15%...           │
│                                         │
│ [设置提醒] [查看详情] [加入自选]         │
└─────────────────────────────────────────┘
```

#### 筛选面板
- 事件类型筛选（多选）
- 日期范围选择
- 自选股筛选开关
- 重要程度筛选
- AI情感筛选

#### 提醒设置弹窗
```
┌─────────────────────────────────────────┐
│ 设置事件提醒                          ✕ │
├─────────────────────────────────────────┤
│ 事件: 平安银行 2025年年报发布            │
│ 日期: 2026-03-25                        │
│                                         │
│ 提前: [  3  ] 天提醒                    │
│ 时间: [09:00]                           │
│ 方式: ◉ 系统通知  ○ 邮件                │
│                                         │
│         [取消]        [确认]            │
└─────────────────────────────────────────┘
```

### 5.4 视觉设计

#### 事件类型颜色
| 事件类型 | 主色 | 含义 |
|---------|------|------|
| 财报发布 | #409EFF | 蓝色，重要信息 |
| 业绩预告 | #67C23A | 绿色，预期向好 |
| 分红除权 | #E6A23C | 橙色，收益分配 |
| 解禁日 | #F56C6C | 红色，风险提示 |
| 股东大会 | #909399 | 灰色，常规事项 |

#### AI情感颜色
| 情感 | 颜色 | 图标 |
|------|------|------|
| 利好 | #67C23A | ↗ |
| 中性 | #909399 | → |
| 利空 | #F56C6C | ↘ |

---

## 6. 数据采集方案

### 6.1 采集源配置

| 数据类型 | 数据源 | AkShare接口 | 采集频率 | 更新时间 |
|---------|--------|-------------|---------|---------|
| 财报日历 | 东方财富 | `stock_financial_report_calendar` | 每日 | 02:00 |
| 分红除权 | 东方财富 | `stock_dividend_cninfo` | 每日 | 02:30 |
| 解禁日 | 东方财富 | `stock_restricted_release_summary` | 每日 | 03:00 |
| IPO日历 | 东方财富 | `stock_ipo_info` | 每日 | 03:30 |
| 评级变动 | 东方财富 | `stock_rank_forecast_cninfo` | 每日 | 04:00 |

### 6.2 采集服务实现

```python
# backend/apps/admin/stock_calendar/services/data_sync_service.py

from datetime import datetime, timedelta
import akshare as ak
from sqlalchemy.orm import Session

class CalendarDataSyncService:
    """投资日历数据同步服务"""
    
    def sync_earnings_calendar(self, db: Session) -> int:
        """同步财报日历"""
        try:
            # 获取未来90天的财报发布日历
            df = ak.stock_financial_report_calendar(
                start_date=datetime.now().strftime('%Y%m%d'),
                end_date=(datetime.now() + timedelta(days=90)).strftime('%Y%m%d')
            )
            
            count = 0
            for _, row in df.iterrows():
                event = StockCalendarEvent(
                    stock_code=row['股票代码'],
                    stock_name=row['股票简称'],
                    event_type='earnings_report',
                    event_date=row['报告日期'],
                    title=f"{row['股票简称']} {row['报告期']}财报发布",
                    data_source='akshare'
                )
                db.merge(event)
                count += 1
            
            db.commit()
            return count
        except Exception as e:
            db.rollback()
            raise e
    
    def sync_dividend_calendar(self, db: Session) -> int:
        """同步分红除权日历"""
        # 实现类似...
        pass
    
    def sync_unlock_calendar(self, db: Session) -> int:
        """同步解禁日历"""
        # 实现类似...
        pass
```

### 6.3 定时任务配置

```python
# backend/apps/admin/stock_calendar/tasks.py

from apscheduler.schedulers.background import BackgroundScheduler

def setup_calendar_tasks(scheduler: BackgroundScheduler):
    """配置投资日历定时任务"""
    
    # 每日02:00同步财报日历
    scheduler.add_job(
        'stock_calendar.tasks.sync_earnings',
        trigger='cron',
        hour=2, minute=0,
        id='sync_earnings_calendar'
    )
    
    # 每日02:30同步分红除权
    scheduler.add_job(
        'stock_calendar.tasks.sync_dividends',
        trigger='cron',
        hour=2, minute=30,
        id='sync_dividend_calendar'
    )
    
    # 每日03:00同步解禁日
    scheduler.add_job(
        'stock_calendar.tasks.sync_unlocks',
        trigger='cron',
        hour=3, minute=0,
        id='sync_unlock_calendar'
    )
    
    # 每日09:00检查并发送提醒
    scheduler.add_job(
        'stock_calendar.tasks.check_reminders',
        trigger='cron',
        hour=9, minute=0,
        id='check_calendar_reminders'
    )
```

---

## 7. AI分析服务

### 7.1 分析流程

```
事件触发 → 获取事件上下文 → 调用AI模型 → 解析分析结果 → 存储到数据库
    │              │              │              │
    │              │              │              └── 更新ai_analysis等字段
    │              │              └── 调用用户提供的AI API
    │              └── 股票历史数据、市场环境、同类事件历史影响
    └── 财报发布、解禁、评级变动等
```

### 7.2 Prompt模板

```python
ANALYSIS_PROMPT = """
你是一位专业的投资分析师。请分析以下事件对股票的潜在影响：

事件信息：
- 股票：{stock_name}({stock_code})
- 事件类型：{event_type}
- 事件标题：{event_title}
- 事件详情：{event_content}
- 事件日期：{event_date}

股票背景：
- 行业：{industry}
- 近期涨跌幅(20日)：{change_20d}%
- 当前PE：{pe}
- 当前PB：{pb}

请从以下维度分析：
1. 事件影响评分（-5到5分，负分利空，正分利好）
2. 情感判断（利好/中性/利空）
3. 具体影响分析（200字内）
4. 操作建议（100字内）

请以JSON格式返回：
{{
    "impact_score": 2.5,
    "sentiment": "利好",
    "analysis": "...",
    "suggestion": "..."
}}
"""
```

### 7.3 批量分析策略

```python
class AIAnalysisService:
    """AI分析服务"""
    
    async def analyze_event(self, event_id: int) -> dict:
        """分析单个事件"""
        event = self.db.query(StockCalendarEvent).get(event_id)
        
        # 获取股票背景信息
        stock_info = await self.get_stock_context(event.stock_code)
        
        # 构建prompt
        prompt = ANALYSIS_PROMPT.format(
            stock_name=event.stock_name,
            stock_code=event.stock_code,
            event_type=event.event_type,
            event_title=event.title,
            event_content=event.content or '',
            event_date=str(event.event_date),
            **stock_info
        )
        
        # 调用AI API
        result = await self.call_ai_api(prompt)
        
        # 更新事件
        event.ai_impact_score = result['impact_score']
        event.ai_sentiment = self._map_sentiment(result['sentiment'])
        event.ai_analysis = result['analysis']
        event.ai_suggestion = result['suggestion']
        self.db.commit()
        
        return result
    
    async def batch_analyze(self, event_ids: list[int]):
        """批量分析事件"""
        for event_id in event_ids:
            try:
                await self.analyze_event(event_id)
            except Exception as e:
                logger.error(f"分析事件{event_id}失败: {e}")
```

---

## 8. 提醒服务

### 8.1 提醒逻辑

```python
class ReminderService:
    """提醒服务"""
    
    def check_and_send_reminders(self):
        """检查并发送提醒"""
        today = datetime.now().date()
        
        # 获取所有启用的提醒
        reminders = self.db.query(StockEventReminder).filter(
            StockEventReminder.is_active == 1
        ).all()
        
        for reminder in reminders:
            event = self.db.query(StockCalendarEvent).get(reminder.event_id)
            
            # 计算提醒日期
            remind_date = event.event_date - timedelta(days=reminder.remind_days)
            
            if remind_date == today:
                self.send_reminder(reminder, event)
    
    def send_reminder(self, reminder: StockEventReminder, event: StockCalendarEvent):
        """发送提醒"""
        message = f"""
【投资日历提醒】
股票：{event.stock_name}({event.stock_code})
事件：{event.title}
日期：{event.event_date}
{'AI建议：' + event.ai_suggestion if event.ai_suggestion else ''}

请及时关注！
"""
        
        if reminder.remind_type == 'system':
            self.send_system_notification(reminder.user_id, message)
        elif reminder.remind_type == 'email':
            self.send_email_notification(reminder.user_id, message)
```

---

## 9. 与现有模块联动

### 9.1 自选股联动

- 打开投资日历时，自动加载用户自选股相关事件
- 在事件卡片中显示"已加入自选"标识
- 点击"加入自选"可直接将股票添加到自选股

### 9.2 监听策略联动

- 重要事件可一键创建监听策略
- 事件触发时自动检查相关监听策略
- AI分析结果可同步到监听策略备注

### 9.3 板块轮动联动

- 板块轮动机会在日历中标记
- 点击板块机会可跳转到板块轮动页面
- 板块相关个股的事件聚合展示

---

## 10. 开发计划

### 10.1 开发阶段

| 阶段 | 内容 | 预估时间 |
|------|------|---------|
| Phase 1 | 数据模型 + 基础API | 2天 |
| Phase 2 | 数据采集服务 | 2天 |
| Phase 3 | 前端页面开发 | 3天 |
| Phase 4 | AI分析集成 | 2天 |
| Phase 5 | 提醒服务 + 联动 | 2天 |
| Phase 6 | 测试 + 优化 | 2天 |

**总计：约13个工作日**

### 10.2 文件清单

#### 后端文件
```
backend/apps/admin/stock_calendar/
├── __init__.py
├── models/
│   ├── __init__.py
│   ├── stock_calendar_event.py
│   ├── stock_event_reminder.py
│   ├── invest_calendar_event.py
│   └── sector_rotation_opportunity.py
├── schemas/
│   ├── __init__.py
│   ├── event.py
│   ├── reminder.py
│   └── analysis.py
├── params/
│   ├── __init__.py
│   └── event_params.py
├── crud/
│   ├── __init__.py
│   ├── event_crud.py
│   └── reminder_crud.py
├── services/
│   ├── __init__.py
│   ├── data_sync_service.py
│   ├── ai_analysis_service.py
│   └── reminder_service.py
├── tasks/
│   ├── __init__.py
│   └── calendar_tasks.py
└── views.py
```

#### 前端文件
```
frontend/src/views/Vadmin/Stock/InvestCalendar/
├── InvestCalendar.vue
├── components/
│   ├── CalendarMonth.vue
│   ├── CalendarWeek.vue
│   ├── TimelineView.vue
│   ├── EventCard.vue
│   ├── StockEventPanel.vue
│   ├── AIAnalysisPanel.vue
│   ├── ReminderDialog.vue
│   ├── FilterPanel.vue
│   ├── EventTypeTag.vue
│   └── ImpactScore.vue
├── composables/
│   ├── useCalendarEvents.ts
│   └── useEventReminders.ts
└── types/
    └── calendar.ts

frontend/src/api/
└── stockCalendar.ts
```

---

## 11. 风险与注意事项

### 11.1 数据风险

- **数据源稳定性**：AkShare接口可能变动，需要监控和适配
- **数据时效性**：事件信息可能延迟更新，需要多源校验
- **数据准确性**：财报日期可能变更，需要及时同步更新

### 11.2 AI风险

- **分析准确性**：AI分析仅供参考，不构成投资建议
- **API限流**：批量分析时需要注意API调用限制
- **结果解析**：需要完善的异常处理和重试机制

### 11.3 性能风险

- **事件数量**：全市场事件数量大，需要分页和缓存
- **AI调用**：批量分析需要异步处理，避免阻塞

---

## 12. 后续优化方向

1. **移动端适配**：响应式设计，支持手机端查看
2. **事件订阅**：支持按股票/板块订阅事件推送
3. **历史回测**：验证AI分析的准确性
4. **个性化推荐**：基于用户偏好推荐相关事件
5. **日历导出**：支持导出到Outlook/Google日历

---

## 附录

### A. 事件类型详细说明

#### 财报发布 (earnings_report)
- 来源：东方财富财报日历
- 数据：报告期、预约披露日期、实际披露日期
- AI分析维度：业绩预期、同比环比、行业对比

#### 分红除权 (dividend)
- 来源：东方财富分红数据
- 数据：每股分红、除权除息日、股权登记日
- AI分析维度：分红率、股息率、历史分红趋势

#### 解禁日 (unlock)
- 来源：东方财富解禁数据
- 数据：解禁股数、解禁市值、占流通股比例
- AI分析维度：解禁压力、股东类型、历史解禁影响

### B. AkShare接口示例

```python
# 财报日历
import akshare as ak
df = ak.stock_financial_report_calendar(start_date='20260301', end_date='20260630')

# 分红数据
df = ak.stock_dividend_cninfo(symbol='000001')

# 解禁数据
df = ak.stock_restricted_release_summary(symbol='000001')

# IPO日历
df = ak.stock_ipo_info()
```

---

**文档版本**: v1.0
**创建日期**: 2026-03-21
**作者**: AI Assistant