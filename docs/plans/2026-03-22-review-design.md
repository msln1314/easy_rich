# 复盘功能设计文档

## 1. 概述

### 1.1 功能定位

复盘功能是一个综合型投资复盘工作台，帮助用户：
- **学习成长** - 记录交易心得、总结经验教训、形成交易体系
- **数据驱动** - 量化分析交易数据、计算各项指标、发现盈亏规律
- **决策辅助** - 帮助做出下一步操作决策，持仓去留、调仓建议
- **合规记录** - 完整记录交易过程和决策依据，便于回溯和审计

### 1.2 核心模块

| 模块 | 描述 |
|-----|------|
| 复盘工作台 | 每日/每周/每月/不定期复盘，支持手动录入、自动生成、AI辅助 |
| 心得经验库 | 个人投资知识库，支持时间线、分类标签、关联记录、知识检索 |
| 雷区基线 | 投资纪律管理，负面清单+正面清单，支持多种触发检查方式 |

### 1.3 技术栈

- **前端**：Vue 3 + Element Plus + TypeScript + ECharts
- **后端**：FastAPI + SQLAlchemy 2.0 + MySQL
- **AI**：集成现有AI分析能力

---

## 2. 模块一：复盘工作台

### 2.1 功能特性

**复盘周期**
- 每日复盘 - 每天收盘后进行
- 每周复盘 - 周末进行
- 每月复盘 - 月度总结
- 不定期复盘 - 随时进行

**内容来源方式**
- 手动录入 - 用户填写复盘内容，系统提供模板引导
- 自动生成 - 系统汇总数据（持仓、交易、市场等），用户补充分析
- AI辅助 - AI生成复盘报告初稿，用户审核修改

### 2.2 内容模块

| 模块 | 自动生成内容 | 用户补充内容 | AI辅助 |
|------|-------------|-------------|--------|
| 市场回顾 | 大盘走势、板块轮动、资金流向、涨跌分布 | 热点事件解读、市场情绪判断 | 市场趋势分析、风险提示 |
| 持仓分析 | 持仓股票涨跌、盈亏变化、仓位变化 | 技术形态判断、基本面变化 | 持仓风险评估、调仓建议 |
| 交易回顾 | 交易记录汇总、交易统计 | 交易理由、执行情况反思 | 交易质量评估 |
| 策略评估 | 策略触发记录、执行结果 | 策略有效性分析 | 策略优化建议 |
| 盈亏统计 | 收益率、胜率、盈亏比、回撤等指标 | - | 盈亏归因分析 |
| 心得记录 | - | 自由文本记录（富文本） | AI总结提炼 |
| 下期计划 | - | 操作计划、关注标的 | AI建议参考 |
| AI分析 | - | - | 综合分析报告 |

### 2.3 数据模型

```sql
CREATE TABLE review_record (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL COMMENT '用户ID',
    portfolio_id BIGINT COMMENT '关联组合ID',
    
    review_type VARCHAR(20) NOT NULL COMMENT '复盘类型: daily/weekly/monthly/adhoc',
    review_date DATE NOT NULL COMMENT '复盘日期',
    
    -- 市场回顾
    market_summary JSON COMMENT '市场数据JSON',
    market_analysis TEXT COMMENT '用户市场分析',
    
    -- 持仓分析
    position_summary JSON COMMENT '持仓数据JSON',
    position_analysis TEXT COMMENT '用户持仓分析',
    
    -- 交易回顾
    trade_summary JSON COMMENT '交易数据JSON',
    trade_analysis TEXT COMMENT '用户交易分析',
    
    -- 策略评估
    strategy_summary JSON COMMENT '策略数据JSON',
    strategy_analysis TEXT COMMENT '用户策略分析',
    
    -- 盈亏统计
    profit_summary JSON COMMENT '盈亏数据JSON',
    
    -- 心得记录
    notes TEXT COMMENT '心得记录（富文本）',
    
    -- 下期计划
    next_plan TEXT COMMENT '下期计划JSON',
    
    -- AI分析
    ai_analysis TEXT COMMENT 'AI分析报告',
    
    -- 状态
    status VARCHAR(20) DEFAULT 'draft' COMMENT '状态: draft/published',
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_user_date (user_id, review_date),
    INDEX idx_review_type (review_type)
) COMMENT '复盘记录表';
```

### 2.4 API接口

```
GET    /api/review                           # 获取复盘列表
GET    /api/review/{review_id}               # 获取复盘详情
POST   /api/review                           # 创建复盘
PUT    /api/review/{review_id}               # 更新复盘
DELETE /api/review/{review_id}               # 删除复盘
POST   /api/review/generate                  # 自动生成复盘数据
POST   /api/review/ai_analyze                # AI分析生成报告
GET    /api/review/history                   # 历史复盘记录
```

---

## 3. 模块二：心得经验库

### 3.1 功能特性

**四种视图**
- 时间线视图 - 按时间倒序展示所有心得，类似日记
- 分类标签视图 - 按主题分类展示，支持自定义标签
- 关联视图 - 心得关联具体股票/交易，点击可跳转
- 知识检索视图 - 支持全文搜索，快速定位

**心得属性**
- 标题、内容（富文本）
- 分类：选股技巧/止损心得/心态管理/策略优化/其他
- 标签：自定义标签，如 #止损 #追高 #分批建仓
- 关联：关联股票代码、关联交易记录
- 心情：得意/平静/懊恼/愤怒
- 重要程度：普通/重要/关键

### 3.2 数据模型

```sql
CREATE TABLE experience_note (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL COMMENT '用户ID',
    
    title VARCHAR(200) NOT NULL COMMENT '标题',
    content TEXT NOT NULL COMMENT '内容（富文本）',
    
    category VARCHAR(50) COMMENT '分类',
    tags JSON COMMENT '标签数组',
    
    related_stocks JSON COMMENT '关联股票代码数组',
    related_trades JSON COMMENT '关联交易ID数组',
    related_review_id BIGINT COMMENT '关联复盘ID',
    
    mood VARCHAR(20) COMMENT '心情: proud/calm/regret/angry',
    importance VARCHAR(20) DEFAULT 'normal' COMMENT '重要程度: normal/important/critical',
    
    view_count INT DEFAULT 0 COMMENT '查看次数',
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_user_id (user_id),
    INDEX idx_category (category),
    INDEX idx_created_at (created_at),
    FULLTEXT INDEX ft_content (title, content)
) COMMENT '心得经验表';
```

### 3.3 API接口

```
GET    /api/experience                       # 获取心得列表
GET    /api/experience/{note_id}             # 获取心得详情
POST   /api/experience                       # 创建心得
PUT    /api/experience/{note_id}             # 更新心得
DELETE /api/experience/{note_id}             # 删除心得
GET    /api/experience/search                # 搜索心得
GET    /api/experience/by_stock/{stock_code} # 按股票获取心得
GET    /api/experience/tags                  # 获取标签列表
GET    /api/experience/categories            # 获取分类列表
```

---

## 4. 模块三：雷区基线

### 4.1 功能特性

**雷区（负面清单）**
- 记录需要避免的错误行为
- 设置严重程度：高/中/低
- 设置触发条件和检查时机

**基线（正面清单）**
- 记录必须遵守的投资原则
- 设置检查时机

**触发检查方式**
- 被动查看 - 用户自己查看列表，自我提醒
- 交易前检查 - 买入/卖出前自动检查并提示
- 定期提醒 - 每日/每周复盘时检查违规行为
- 实时监控 - 监控用户行为，触犯雷区立即警告

### 4.2 数据模型

```sql
CREATE TABLE risk_rule (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL COMMENT '用户ID',
    
    rule_type VARCHAR(20) NOT NULL COMMENT '规则类型: trap/baseline',
    category VARCHAR(50) COMMENT '分类: position/trade/psychology/risk',
    
    name VARCHAR(200) NOT NULL COMMENT '规则名称',
    description TEXT COMMENT '规则描述',
    
    severity VARCHAR(20) COMMENT '严重程度: high/medium/low',
    
    check_timing JSON COMMENT '检查时机: passive/pre_trade/periodic/realtime',
    check_condition JSON COMMENT '触发条件JSON',
    
    is_active TINYINT DEFAULT 1 COMMENT '是否启用',
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_user_type (user_id, rule_type),
    INDEX idx_is_active (is_active)
) COMMENT '雷区基线规则表';

CREATE TABLE rule_violation (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL COMMENT '用户ID',
    rule_id BIGINT NOT NULL COMMENT '规则ID',
    
    violation_time DATETIME NOT NULL COMMENT '违规时间',
    violation_context JSON COMMENT '违规上下文JSON',
    
    related_stock_code VARCHAR(20) COMMENT '关联股票代码',
    related_trade_id BIGINT COMMENT '关联交易ID',
    
    user_note TEXT COMMENT '用户备注',
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_user_time (user_id, violation_time),
    INDEX idx_rule_id (rule_id)
) COMMENT '违规记录表';
```

### 4.3 预设规则

**雷区（负面清单）**

| 分类 | 规则 | 严重程度 | 检查时机 |
|-----|------|---------|---------|
| 仓位风险 | 单只股票仓位超过30% | 高 | 实时监控 |
| 仓位风险 | 单一行业仓位超过50% | 高 | 实时监控 |
| 交易纪律 | 追高买入（涨幅>5%买入） | 中 | 交易前检查 |
| 交易纪律 | 不设止损就买入 | 高 | 交易前检查 |
| 交易纪律 | 频繁交易（日内交易>3次） | 中 | 实时监控 |
| 心态管理 | 亏损后急于翻本 | 中 | 定期提醒 |
| 心态管理 | 盈利后过度自信 | 低 | 定期提醒 |

**基线（正面清单）**

| 分类 | 规则 | 检查时机 |
|-----|------|---------|
| 仓位管理 | 单只股票仓位≤20% | 交易前检查 |
| 仓位管理 | 保留10%现金应对机会 | 每日检查 |
| 交易纪律 | 买入前必须设置止损位 | 交易前检查 |
| 交易纪律 | 买入前必须分析理由 | 交易前检查 |
| 交易纪律 | 分批建仓，首次≤50%目标仓位 | 交易前检查 |
| 风险控制 | 持仓股票不超过10只 | 每日检查 |
| 学习成长 | 每周至少复盘一次 | 定期提醒 |

### 4.4 API接口

```
GET    /api/rule                            # 获取规则列表
GET    /api/rule/{rule_id}                  # 获取规则详情
POST   /api/rule                            # 创建规则
PUT    /api/rule/{rule_id}                  # 更新规则
DELETE /api/rule/{rule_id}                  # 删除规则
GET    /api/rule/presets                    # 获取预设规则
POST   /api/rule/apply_presets              # 应用预设规则

GET    /api/rule/violations                 # 获取违规记录
POST   /api/rule/check                      # 检查规则（交易前）
POST   /api/rule/check_realtime             # 实时检查
GET    /api/rule/violation/{violation_id}   # 获取违规详情
PUT    /api/rule/violation/{violation_id}   # 更新违规备注
```

---

## 5. 前端页面设计

### 5.1 页面结构

```
Review/
├── Review.vue                    # 复盘工作台主页面
├── components/
│   ├── MarketReview.vue          # 市场回顾组件
│   ├── PositionReview.vue        # 持仓分析组件
│   ├── TradeReview.vue           # 交易回顾组件
│   ├── StrategyReview.vue        # 策略评估组件
│   ├── ProfitStats.vue           # 盈亏统计组件
│   ├── NotesEditor.vue           # 心得编辑器
│   ├── PlanEditor.vue            # 计划编辑器
│   └── AIAnalysis.vue            # AI分析组件
├── types/
│   └── review.ts                 # 类型定义

Experience/
├── Experience.vue                # 心得经验库主页面
├── components/
│   ├── TimelineView.vue          # 时间线视图
│   ├── CategoryView.vue          # 分类视图
│   ├── RelatedView.vue           # 关联视图
│   ├── SearchView.vue            # 搜索视图
│   ├── NoteCard.vue              # 心得卡片
│   └── NoteEditor.vue            # 心得编辑器
├── types/
│   └── experience.ts             # 类型定义

RiskRule/
├── RiskRule.vue                  # 雷区基线主页面
├── components/
│   ├── TrapList.vue              # 雷区列表
│   ├── BaselineList.vue          # 基线列表
│   ├── RuleEditor.vue            # 规则编辑器
│   ├── ViolationList.vue         # 违规记录列表
│   └── CheckDialog.vue           # 检查弹窗
├── types/
│   └── rule.ts                   # 类型定义
```

### 5.2 页面布局

**复盘工作台**

```
┌─────────────────────────────────────────────────────────────┐
│ 复盘工作台                    [每日] [每周] [每月] [不定期] │
├─────────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ 市场回顾                                    [AI生成]    │ │
│ │ 上证指数 +1.2%  深证成指 +0.8%  创业板指 +0.5%          │ │
│ │ 板块：科技领涨 +2.3%  金融回调 -0.5%                    │ │
│ │ ─────────────────────────────────────────────────────── │ │
│ │ [用户输入] 今日热点事件：_______________________        │ │
│ └─────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│ ┌──────────────────────┬──────────────────────────────────┐ │
│ │ 持仓分析             │ 交易回顾                         │ │
│ │ 股票    涨跌   盈亏  │ 买入  卖出  盈亏统计             │ │
│ │ 平安银行 +2.1% +1200 │ 3笔   1笔   +2,350              │ │
│ │ 招商银行 -0.5%  -300 │ ─────────────────────────────── │ │
│ │ [用户补充分析]       │ [交易理由记录]                   │ │
│ └──────────────────────┴──────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ 心得记录                                                │ │
│ │ ─────────────────────────────────────────────────────── │ │
│ │ [富文本编辑器]                                          │ │
│ └─────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ 明日/下周计划                                           │ │
│ │ □ 关注科技板块回调机会                                  │ │
│ │ □ 招商银行跌破30日均线考虑减仓                          │ │
│ │ [添加计划项]                                            │ │
│ └─────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│ [保存草稿] [生成报告] [AI辅助分析] [查看历史]              │
└─────────────────────────────────────────────────────────────┘
```

**心得经验库**

```
┌─────────────────────────────────────────────────────────────┐
│ 心得经验库                    [时间线] [分类] [关联] [搜索] │
├─────────────────────────────────────────────────────────────┤
│ ┌────────────┬─────────────────────────────────────────────┐│
│ │ 分类筛选   │ 心得列表                                    ││
│ │ ─────────  │ ─────────────────────────────────────────── ││
│ │ □ 选股技巧 │ [重要] 止损的重要性                         ││
│ │ ☑ 止损心得 │ 2026-03-22 | 止损心得 | 关联: 平安银行      ││
│ │ □ 心态管理 │ 今天平安银行跌破止损位，犹豫没卖，结果...   ││
│ │ □ 策略优化 │ ─────────────────────────────────────────── ││
│ │ □ 其他     │ [普通] 科技板块轮动规律                     ││
│ │            │ 2026-03-20 | 选股技巧 | 关联: 科技板块      ││
│ │ 标签筛选   │ 发现科技板块在月初和月中会有两波行情...     ││
│ │ ─────────  │ ─────────────────────────────────────────── ││
│ │ #止损      │ [+ 新增心得]                                ││
│ │ #追高      │                                             ││
│ │ #分批建仓  │                                             ││
│ └────────────┴─────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

**雷区基线**

```
┌─────────────────────────────────────────────────────────────┐
│ 雷区基线管理                    [雷区] [基线] [违规记录]   │
├─────────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ 雷区列表（负面清单）                    [+ 添加雷区]    │ │
│ │ ─────────────────────────────────────────────────────── │ │
│ │ ⚠️ 高风险                                              │ │
│ │ • 单只股票仓位超过30%          [编辑] [删除]           │ │
│ │ • 不设止损就买入               [编辑] [删除]           │ │
│ │ ─────────────────────────────────────────────────────── │ │
│ │ ⚡ 中风险                                               │ │
│ │ • 追高买入（涨幅>5%）          [编辑] [删除]           │ │
│ └─────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ 基线列表（正面清单）                    [+ 添加基线]    │ │
│ │ ─────────────────────────────────────────────────────── │ │
│ │ ✅ 仓位管理                                             │ │
│ │ • 单只股票仓位≤20%             [编辑] [删除]           │ │
│ ─────────────────────────────────────────────────────────── │ │
│ │ ✅ 交易纪律                                             │ │
│ │ • 买入前必须设置止损位         [编辑] [删除]           │ │
│ └─────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ 近期违规记录                                            │ │
│ │ ─────────────────────────────────────────────────────── │ │
│ │ 2026-03-22 触犯雷区：追高买入平安银行（涨幅6.2%）       │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 6. 模块联动设计

### 6.1 与投资组合联动

| 触发 | 动作 |
|-----|------|
| 复盘工作台 | 自动获取持仓数据、交易记录、盈亏统计 |
| 心得经验库 | 可关联持仓股票、交易记录 |
| 雷区基线 | 交易前检查仓位、实时监控仓位 |

### 6.2 与投资日历联动

| 触发 | 动作 |
|-----|------|
| 复盘工作台 | 市场回顾纳入重要事件 |
| 心得经验库 | 可关联日历事件 |

### 6.3 与监听策略联动

| 触发 | 动作 |
|-----|------|
| 复盘工作台 | 策略评估模块获取策略触发记录 |
| 心得经验库 | 可关联策略 |

### 6.4 与AI分析联动

| 触发 | 动作 |
|-----|------|
| 复盘工作台 | AI辅助生成分析报告 |
| 心得经验库 | AI总结提炼心得要点 |

---

## 7. 开发计划

### 7.1 开发阶段

| 阶段 | 内容 | 预估时间 |
|------|------|---------|
| Phase 1 | 数据模型 + 基础API | 2天 |
| Phase 2 | 复盘工作台服务 | 2天 |
| Phase 3 | 心得经验库服务 | 1天 |
| Phase 4 | 雷区基线服务 | 2天 |
| Phase 5 | 前端页面开发 | 4天 |
| Phase 6 | 模块联动 | 1天 |
| Phase 7 | 测试 + 优化 | 1天 |

**总计：约13个工作日**

### 7.2 后端文件结构

```
backend/apps/admin/review/
├── __init__.py
├── views.py
├── models/
│   ├── __init__.py
│   ├── review_record.py
│   ├── experience_note.py
│   └── risk_rule.py
├── schemas/
│   ├── __init__.py
│   ├── review.py
│   ├── experience.py
│   └── rule.py
├── crud/
│   ├── __init__.py
│   ├── review_crud.py
│   ├── experience_crud.py
│   └── rule_crud.py
└── services/
    ├── __init__.py
    ├── review_service.py
    ├── experience_service.py
    └── rule_service.py
```

### 7.3 前端文件结构

```
frontend/src/views/Vadmin/Stock/Review/
├── Review.vue
├── components/
│   ├── MarketReview.vue
│   ├── PositionReview.vue
│   ├── TradeReview.vue
│   ├── StrategyReview.vue
│   ├── ProfitStats.vue
│   ├── NotesEditor.vue
│   ├── PlanEditor.vue
│   └── AIAnalysis.vue
└── types/
    └── review.ts

frontend/src/views/Vadmin/Stock/Experience/
├── Experience.vue
├── components/
│   ├── TimelineView.vue
│   ├── CategoryView.vue
│   ├── RelatedView.vue
│   ├── SearchView.vue
│   ├── NoteCard.vue
│   └── NoteEditor.vue
└── types/
    └── experience.ts

frontend/src/views/Vadmin/Stock/RiskRule/
├── RiskRule.vue
├── components/
│   ├── TrapList.vue
│   ├── BaselineList.vue
│   ├── RuleEditor.vue
│   ├── ViolationList.vue
│   └── CheckDialog.vue
└── types/
    └── rule.ts

frontend/src/api/
├── review.ts
├── experience.ts
└── riskRule.ts
```

---

## 8. 风险与注意事项

### 8.1 数据风险

- **历史数据缺失**：新建用户无历史复盘数据
- **AI分析依赖**：AI服务不可用时影响功能体验

### 8.2 性能风险

- **全文搜索**：心得内容全文搜索可能影响性能
- **实时监控**：频繁检查可能增加系统负担

### 8.3 用户体验风险

- **功能复杂度**：三个模块功能较多，需要良好的引导
- **数据录入负担**：需要平衡自动生成和手动录入

---

## 9. 后续优化方向

1. **复盘模板**：支持自定义复盘模板
2. **数据导出**：支持复盘报告导出PDF/Excel
3. **分享功能**：支持心得分享到社区
4. **移动端适配**：响应式设计
5. **智能提醒**：基于历史行为的智能提醒

---

**文档版本**: v1.0
**创建日期**: 2026-03-22
**作者**: AI Assistant