# AI股票分析平台设计方案

## 一、项目背景

基于现有的股票分析系统，扩展AI智能分析能力，集成多种AI模型接口，提供多角色协作分析、研报生成、智能对话等功能。

### 1.1 参考项目

| 项目 | 核心借鉴 |
|------|---------|
| daily_stock_analysis | Multi-Agent Pipeline、AgentContext、ToolRegistry、Skills/Strategies系统 |
| valuecell | DeepResearch Agent、流式响应、多LLM提供商集成 |
| TradingAgents-CN | FastAPI+Vue架构、进度跟踪、批量分析、研报导出、SSE+WebSocket实时通知 |

### 1.2 核心技术架构

```
┌─────────────────────────────────────────────────────────────────┐
│                        前端 (Vue 3 + Vite)                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────┐│
│  │AI对话助手│  │分析师工作台│  │研报中心  │  │每日自动分析     ││
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────────┬─────────┘│
│       │             │             │                  │          │
│       └─────────────┴─────────────┴──────────────────┘          │
│                           │ SSE/WebSocket                       │
└───────────────────────────┼─────────────────────────────────────┘
                            │
┌───────────────────────────┼─────────────────────────────────────┐
│                    后端 (FastAPI)                                │
│  ┌────────────────────────┴────────────────────────────────────┐│
│  │                    API Gateway Layer                         ││
│  │  /ai/chat  /ai/agents  /ai/report  /ai/schedule             ││
│  └────────────────────────┬────────────────────────────────────┘│
│                           │                                      │
│  ┌────────────────────────┴────────────────────────────────────┐│
│  │                 Agent Orchestrator                           ││
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────────────┐ ││
│  │  │Technical│  │ Intel   │  │  Risk   │  │   Decision      │ ││
│  │  │ Agent   │→ │ Agent   │→ │ Agent   │→ │   Agent         │ ││
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────────────┘ ││
│  └────────────────────────┬────────────────────────────────────┘│
│                           │                                      │
│  ┌────────────────────────┴────────────────────────────────────┐│
│  │                  Tool Registry                               ││
│  │  get_quote | get_history | analyze_trend | get_news | ...  ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  ┌──────────────────────┐  ┌──────────────────────────────────┐ │
│  │  Skills/Strategies   │  │      LLM Adapter (LiteLLM)       │ │
│  │  乖离率策略 | 均线策略│  │  OpenAI | DeepSeek | Qwen | ... │ │
│  └──────────────────────┘  └──────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
                            │
┌───────────────────────────┼─────────────────────────────────────┐
│                    数据层                                        │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────────┐│
│  │  MySQL    │  │  Redis    │  │ AkShare   │  │  新闻/公告    ││
│  │  业务数据  │  │  缓存/队列│  │ 行情数据   │  │  外部API     ││
│  └───────────┘  └───────────┘  └───────────┘  └───────────────┘│
└──────────────────────────────────────────────────────────────────┘
```

## 二、功能概览

| 菜单名称 | 核心功能 | 交互特点 |
|---------|---------|---------|
| AI对话助手 | 智能问答、投资建议、快捷分析 | 轻量对话式交互 |
| AI分析师工作台 | 多角色分析、辩论讨论、综合研判 | 多角色可视化 |
| AI研报中心 | 研报生成、导出分享、历史管理 | 专业研报格式 |
| 市场洞察 | 市场情绪、板块轮动、资金流向、热点挖掘 | 全局市场视角 |
| 盘后复盘 | 每日复盘、交易总结、机会挖掘、风险预警 | 复盘报告生成 |

---

## 三、页面一：AI对话助手

### 3.1 功能清单

| 功能模块 | 描述 |
|---------|------|
| 股票输入 | 支持代码/名称搜索，快捷选择自选股/持仓股 |
| 智能对话 | 多轮对话，支持上下文理解 |
| 快捷分析 | 一键触发技术分析、基本面分析等 |
| 投资建议 | 买卖点、仓位、止损止盈建议 |
| 分析历史 | 对话记录保存和查看 |

### 3.2 页面布局

```
┌─────────────────────────────────────────────────────────────┐
│  🤖 AI对话助手                            [模型: GPT-4 ▼]   │
├───────────────────────┬─────────────────────────────────────┤
│                       │                                     │
│   股票信息面板        │    对话区域                         │
│ ┌───────────────────┐ │                                     │
│ │ 🔍 [搜索股票... ] │ │    ┌─────────────────────────────┐ │
│ └───────────────────┘ │    │ 🤖 您好！我是您的AI投资顾问  │ │
│                       │    │                              │ │
│ ┌───────────────────┐ │    │ 请问有什么可以帮您分析？     │ │
│ │ 平安银行 000001   │ │    │                              │ │
│ │ 13.85   +2.35%   │ │    │ 快捷分析：                   │ │
│ │ ─────────────────│ │    │ [技术分析] [走势预测]        │ │
│ │ 今开: 13.60      │ │    │ [基本面]   [风险评估]        │ │
│ │ 最高: 14.02      │ │    └─────────────────────────────┘ │
│ │ 最低: 13.55      │ │                                     │
│ │ 成交量: 1.2亿    │ │    ┌─────────────────────────────┐ │
│ │ 换手: 2.35%      │ │    │ 👤 这只股票适合短线操作吗？  │ │
│ │ ─────────────────│ │    └─────────────────────────────┘ │
│ │ MA5:  13.52 ↑   │ │                                     │
│ │ MA10: 13.28 ↑   │ │    ┌─────────────────────────────┐ │
│ │ MA20: 13.05 ↑   │ │    │ 🤖 从技术面分析：           │ │
│ │ ─────────────────│ │    │                              │ │
│ │ MACD: 金叉      │ │    │ 该股近期走势偏强，5日均线   │ │
│ │ KDJ:  72.5      │ │    │ 上穿10日均线形成金叉...      │ │
│ │ RSI:  65.2      │ │    │                              │ │
│ └───────────────────┘ │    │ **短线建议**：              │ │
│                       │ │    │ • 介入价: 13.70附近        │ │
│   快捷问题            │ │    │ • 目标价: 14.50            │ │
│ ┌───────────────────┐ │    │ • 止损价: 13.40             │ │
│ │ • 技术面如何？    │ │    │ • 建议仓位: 2-3成           │ │
│ │ • 买卖点在哪？    │ │    └─────────────────────────────┘ │
│ │ • 后市怎么看？    │ │                                     │
│ │ • 风险大吗？      │ │                                     │
│ └───────────────────┘ │    [输入问题...        ] [发送]    │
│                       │                                     │
│   📝 历史对话         │                                     │
│ ┌───────────────────┐ │                                     │
│ │ 03-24 平安银行   │ │                                     │
│ │ 03-23 贵州茅台   │ │                                     │
│ │ 03-22 招商银行   │ │                                     │
│ └───────────────────┘ │                                     │
└───────────────────────┴─────────────────────────────────────┘
```

### 3.3 核心组件

| 组件名 | 功能 |
|-------|------|
| StockInfoPanel | 股票基本信息、实时行情、技术指标展示 |
| ChatArea | 对话消息列表、输入框、发送按钮 |
| QuickQuestions | 预设快捷问题按钮组 |
| ChatHistory | 历史对话列表 |
| ModelSelector | AI模型选择器 |

---

## 四、页面二：AI分析师工作台

### 4.1 功能清单

| 功能模块 | 描述 |
|---------|------|
| 股票输入 | 股票选择、分析周期设置 |
| 角色选择 | 预设分析师角色，支持自定义 |
| 独立分析 | 每个角色独立输出分析结论 |
| 角色辩论 | 多角色交互讨论，达成共识 |
| 综合研判 | 汇总各角色观点，给出最终建议 |
| 对话追问 | 基于分析结果深入提问 |

### 4.2 页面布局

```
┌─────────────────────────────────────────────────────────────┐
│  👥 AI分析师工作台                        [模型: GPT-4 ▼]   │
├─────────────────────────────────────────────────────────────┤
│ ┌─分析配置─────────────────────────────────────────────────┐│
│ │ 股票: [000001    ] [分析]  周期: [短线▼]               ││
│ │ 角色: ☑技术 ☑基本面 ☑消息面 ☑风控 ☑量化  [开始分析]   ││
│ └─────────────────────────────────────────────────────────┘│
├───────────────────────┬─────────────────────────────────────┤
│                       │                                     │
│   角色分析面板        │    综合研判区                       │
│                       │                                     │
│  ┌─────────────────┐  │  ┌───────────────────────────────┐ │
│  │ 📊 技术分析师   │  │  │ 🎯 综合结论: 偏多            │ │
│  │                 │  │  │                               │ │
│  │ 判断: 看多      │  │  │ ████████████░░░░ 置信度: 75% │ │
│  │ 置信度: 80%     │  │  │                               │ │
│  │ ████████░░      │  │  │ ─────────────────────────────│ │
│  │                 │  │  │                               │ │
│  │ • 突破关键阻力  │  │  │ 📌 操作建议: 分批建仓        │ │
│  │ • MACD金叉确认  │  │  │ 📍 目标价: 15.20             │ │
│  │ • 均线多头排列  │  │  │ ⛔ 止损价: 13.40             │ │
│  └─────────────────┘  │  │ ⚠️ 风险等级: 中               │ │
│                       │  └───────────────────────────────┘ │
│  ┌─────────────────┐  │                                     │
│  │ 📋 基本面分析师 │  │  ┌─角色辩论记录─────────────────┐ │
│  │                 │  │  │                               │ │
│  │ 判断: 中性偏多  │  │  │ 🗣️ 技术分析师:               │ │
│  │ 置信度: 55%     │  │  │ 从K线形态看，已突破前期高点， │ │
│  │ █████░░░░░      │  │  │ 成交量配合放大，技术面向好。 │ │
│  │                 │  │  │                               │ │
│  │ • 估值合理      │  │  │ 🗣️ 基本面分析师:             │ │
│  │ • ROE低于同行   │  │  │ 但ROE仅10%，低于行业平均，    │ │
│  │ • 业绩增速放缓  │  │  │ 估值优势不明显，需谨慎。     │ │
│  └─────────────────┘  │  │                               │ │
│                       │  │ 🗣️ 消息面分析师:             │ │
│  ┌─────────────────┐  │  │ 近期政策利好持续，行业景气度  │ │
│  │ 📰 消息面分析师 │  │  │ 上升，有望带动估值修复。     │ │
│  │                 │  │  │                               │ │
│  │ 判断: 看多      │  │  │ 🗣️ 风控专家:                 │ │
│  │ 置信度: 70%     │  │  │ 综合各方观点，建议控制仓位   │ │
│  │ ███████░░░      │  │  │ 在30%以内，严格执行止损。    │ │
│  │                 │  │  └───────────────────────────────┘ │
│  │ • 政策利好持续  │  │                                     │
│  │ • 行业景气上升  │  │                                     │
│  └─────────────────┘  │                                     │
│                       │                                     │
│  ┌─────────────────┐  │                                     │
│  │ 🛡️ 风控专家     │  │                                     │
│  │                 │  │                                     │
│  │ 判断: 谨慎      │  │                                     │
│  │ 风险等级: 中    │  │                                     │
│  │ ███░░░░░░░      │  │                                     │
│  │                 │  │                                     │
│  │ • 仓位≤30%      │  │                                     │
│  │ • 严格止损      │  │                                     │
│  └─────────────────┘  │                                     │
├───────────────────────┴─────────────────────────────────────┤
│ ┌─继续对话─────────────────────────────────────────────────┐│
│ │ 用户: 为什么技术面和基本面观点有差异？                    ││
│ │ AI: 技术面关注价格走势和市场情绪，而基本面关注公司内在价值││
│ │ [输入问题继续深入讨论...                      ] [发送]   ││
│ └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

### 4.3 预设分析师角色

| 角色名称 | 职责 | 关注指标 |
|---------|------|---------|
| 技术分析师 | 技术指标分析 | K线、均线、MACD、KDJ、RSI、成交量 |
| 基本面分析师 | 财务与估值分析 | ROE、PE、PB、营收增长、净利润 |
| 消息面分析师 | 新闻与事件分析 | 政策、公告、研报、行业动态 |
| 风控专家 | 风险评估与控制 | 仓位建议、止损位、风险等级 |
| 量化分析师 | 量化因子分析 | 多因子模型、统计套利信号 |
| 投资顾问 | 综合投资建议 | 操作策略、持仓建议 |

### 4.4 核心组件

| 组件名 | 功能 |
|-------|------|
| AnalysisConfig | 分析配置面板（股票选择、角色选择） |
| AgentCard | 单个分析师角色卡片 |
| AgentAnalysisPanel | 角色分析结果展示区 |
| DebateRecord | 角色辩论记录展示 |
| SynthesisResult | 综合研判结论卡片 |
| FollowUpChat | 追问对话区域 |

---

## 五、页面三：AI研报中心

### 5.1 功能清单

| 功能模块 | 描述 |
|---------|------|
| 研报配置 | 股票选择、分析维度、分析周期 |
| 研报生成 | AI自动生成完整分析报告 |
| 研报展示 | 专业格式展示，目录导航 |
| 研报导出 | PDF/Word格式导出 |
| 历史管理 | 研报保存、检索、分享 |

### 5.2 页面布局

```
┌─────────────────────────────────────────────────────────────┐
│  📑 AI研报中心                             [模型: GPT-4 ▼]  │
├─────────────────────────────────────────────────────────────┤
│ [研报生成]  [历史研报]  [研报模板]                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─研报配置────────────────────────────────────────────────┐│
│  │                                                         ││
│  │  股票代码: [000001    ] [查询]   股票名称: 平安银行     ││
│  │                                                         ││
│  │  分析周期: ○短线(1-5天) ○中线(1-3月) ○长线(6月以上)   ││
│  │                                                         ││
│  │  分析维度:                                              ││
│  │  ☑ 技术面分析  ☑ 基本面分析  ☑ 消息面分析             ││
│  │  ☑ 资金流向    ☑ 风险评估    ☑ 投资建议               ││
│  │                                                         ││
│  │  参与角色: ☑技术分析师 ☑基本面分析师 ☑消息面分析师    ││
│  │           ☑风控专家     ☐量化分析师                    ││
│  │                                                         ││
│  │                              [预览] [生成研报]          ││
│  │                                                         ││
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
│  ┌─研报内容────────────────────────────────────────────────┐│
│  │                                                         ││
│  │  ┌─目录───────┐  ┌─正文──────────────────────────────┐ ││
│  │  │            │  │                                   │ ││
│  │  │ 1. 摘要    │  │ # 平安银行(000001)综合分析报告    │ ││
│  │  │ 2. 技术面  │  │                                   │ ││
│  │  │ 3. 基本面  │  │ **分析日期**: 2026-03-24          │ ││
│  │  │ 4. 消息面  │  │ **分析周期**: 短线                │ ││
│  │  │ 5. 资金流向│  │ **参与角色**: 4位分析师          │ ││
│  │  │ 6. 风险评估│  │                                   │ ││
│  │  │ 7. 投资建议│  │ ---                               │ ││
│  │  │            │  │                                   │ ││
│  │  │            │  │ ## 1. 摘要                        │ ││
│  │  │            │  │                                   │ ││
│  │  │            │  │ **综合评级**: 偏多 ★★★☆☆         │ ││
│  │  │            │  │ **置信度**: 75%                   │ ││
│  │  │            │  │ **目标价**: 15.20元               │ ││
│  │  │            │  │ **止损价**: 13.40元               │ ││
│  │  │            │  │                                   │ ││
│  │  │            │  │ ## 2. 技术面分析                  │ ││
│  │  │            │  │                                   │ ││
│  │  │            │  │ ### 2.1 K线形态                   │ ││
│  │  │            │  │ 当前股价突破前期高点，形成...     │ ││
│  │  │            │  │                                   │ ││
│  │  └────────────┘  └───────────────────────────────────┘ ││
│  │                                                         ││
│  │  [导出PDF] [导出Word] [分享链接] [保存到历史]           ││
│  │                                                         ││
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 5.3 研报结构模板

```markdown
# {股票名称}({股票代码})综合分析报告

## 1. 摘要
- 综合评级
- 置信度
- 核心观点
- 操作建议

## 2. 技术面分析
- K线形态
- 均线系统
- 技术指标(MACD/KDJ/RSI)
- 支撑压力位

## 3. 基本面分析
- 财务指标
- 估值分析
- 行业地位
- 成长性

## 4. 消息面分析
- 近期公告
- 行业动态
- 政策影响

## 5. 资金流向
- 主力资金
- 北向资金
- 融资融券

## 6. 风险评估
- 风险等级
- 风险因素
- 注意事项

## 7. 投资建议
- 操作策略
- 仓位建议
- 止盈止损

## 附录
- 角色辩论记录
- 数据来源
- 免责声明
```

### 5.4 核心组件

| 组件名 | 功能 |
|-------|------|
| ReportConfig | 研报配置面板 |
| ReportContent | 研报正文展示（支持Markdown渲染） |
| ReportToc | 目录导航 |
| ReportExport | 导出功能（PDF/Word） |
| ReportHistory | 历史研报列表 |

---

## 六、页面四：市场洞察

### 6.1 功能清单

| 功能模块 | 描述 |
|---------|------|
| 市场情绪 | 大盘走势、涨跌分布、赚钱效应、恐慌贪婪指数 |
| 板块轮动 | 热门板块、板块资金流向、板块涨跌排名 |
| 资金流向 | 主力资金、北向资金、融资融券、ETF申赎 |
| 热点挖掘 | 概念炒作、题材联动、龙头股识别 |
| AI解读 | AI实时解读市场动态，提供操作建议 |

### 6.2 页面布局

```
┌─────────────────────────────────────────────────────────────┐
│  🔍 市场洞察                               [模型: GPT-4 ▼]   │
├─────────────────────────────────────────────────────────────┤
│ [市场概览]  [板块轮动]  [资金流向]  [热点挖掘]  [AI解读]    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─市场概览────────────────────────────────────────────────┐│
│  │                                                         ││
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌────────────┐ ││
│  │  │上证指数 │  │深证成指 │  │创业板指 │  │ 恐慌贪婪   │ ││
│  │  │ 3,258   │  │ 10,852  │  │ 2,156   │  │ 指数: 65   │ ││
│  │  │ +1.25%  │  │ +0.89%  │  │ +1.52%  │  │ ████████░░ │ ││
│  │  │ 📈      │  │ 📈      │  │ 📈      │  │ 贪婪区间   │ ││
│  │  └─────────┘  └─────────┘  └─────────┘  └────────────┘ ││
│  │                                                         ││
│  │  ┌─涨跌分布──────────────────────────────────────────┐  ││
│  │  │  涨停: 128  涨幅>5%: 356  涨: 2156  平: 156      │  ││
│  │  │  跌停: 23   跌幅>5%: 89   跌: 1235              │  ││
│  │  │  ████████████████░░░░░ 赚钱效应: 65%           │  ││
│  │  └─────────────────────────────────────────────────┘  ││
│  │                                                         ││
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
│  ┌─板块资金流向────────────────────────────────────────────┐│
│  │                                                         ││
│  │  流入TOP5                    流出TOP5                  ││
│  │  ┌──────────────────────┐  ┌──────────────────────┐   ││
│  │  │ 1. 人工智能 +52.3亿  │  │ 1. 房地产 -28.5亿    │   ││
│  │  │ 2. 新能源   +38.1亿  │  │ 2. 银行   -21.2亿    │   ││
│  │  │ 3. 医药     +25.6亿  │  │ 3. 保险   -15.8亿    │   ││
│  │  │ 4. 军工     +18.9亿  │  │ 4. 煤炭   -12.3亿    │   ││
│  │  │ 5. 半导体   +15.2亿  │  │ 5. 钢铁   -9.6亿     │   ││
│  │  └──────────────────────┘  └──────────────────────┘   ││
│  │                                                         ││
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
│  ┌─AI实时解读──────────────────────────────────────────────┐│
│  │                                                         ││
│  │  🤖 今日市场解读：                                      ││
│  │                                                         ││
│  │  今日大盘延续反弹态势，三大指数集体收涨。市场情绪回暖，││
│  │  成交量较昨日放大15%，显示增量资金进场。                ││
│  │                                                         ││
│  │  **核心观点**：                                         ││
│  │  • 人工智能板块持续获资金追捧，主力净流入超50亿        ││
│  │  • 北向资金今日净买入35亿，连续3日净流入               ││
│  │  • 技术面上证突破3250压力位，短期看高一线              ││
│  │                                                         ││
│  │  **操作建议**：                                         ││
│  │  建议关注人工智能、新能源主线，控制仓位5-7成，          ││
│  │  关注权重股走势，跌破3200点需警惕回调风险。             ││
│  │                                                         ││
│  │  [深度分析] [生成研报] [追问]                           ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

### 6.3 核心组件

| 组件名 | 功能 |
|-------|------|
| MarketOverview | 大盘指数、涨跌分布、市场情绪概览 |
| SectorRotation | 板块轮动图、板块涨跌排名 |
| CapitalFlow | 资金流向图表（主力/北向/融资） |
| HotSpotDiscovery | 热点概念、龙头股识别 |
| AIMarketInterpret | AI市场解读、操作建议 |

### 6.4 后端API

```python
# 获取市场概览
GET /ai/market/overview

# 获取板块轮动
GET /ai/market/sectors

# 获取资金流向
GET /ai/market/capital-flow

# AI市场解读
POST /ai/market/interpret
{
    "focus": ["人工智能", "新能源"],  # 关注板块
    "depth": "standard"              # quick | standard | deep
}
```

---

## 七、页面五：盘后复盘

### 7.1 功能清单

| 功能模块 | 描述 |
|---------|------|
| 每日复盘 | 自动生成每日复盘报告 |
| 交易总结 | 用户交易记录与AI点评 |
| 机会挖掘 | AI识别潜在机会股 |
| 风险预警 | 持仓股风险提示 |
| 复盘历史 | 历史复盘报告查阅 |

### 7.2 页面布局

```
┌─────────────────────────────────────────────────────────────┐
│  📊 盘后复盘                               [模型: GPT-4 ▼]   │
├─────────────────────────────────────────────────────────────┤
│ [今日复盘]  [交易总结]  [机会挖掘]  [风险预警]  [历史复盘]  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─今日复盘报告───────────────────────────────────────────┐│
│  │                                                         ││
│  │  📅 日期: 2026-03-24  星期一                           ││
│  │                                                         ││
│  │  ## 市场概况                                            ││
│  │  今日A股三大指数集体收涨，上证指数收报3258点，          ││
│  │  涨幅1.25%，成交额4850亿，较昨日放大15%。               ││
│  │                                                         ││
│  │  ## 盘面特点                                            ││
│  │  1. **人工智能板块领涨**：ChatGPT概念持续活跃，         ││
│  │     龙头股科大讯飞涨停，板块涨幅3.5%                    ││
│  │  2. **新能源反弹**：锂电池、光伏板块超跌反弹，          ││
│  │     宁德时代涨超3%                                      ││
│  │  3. **北向资金回流**：全天净买入35亿，终结连续          ││
│  │     5日净流出                                           ││
│  │                                                         ││
│  │  ## 明日展望                                            ││
│  │  预计明日大盘延续震荡上行，关注3280点压力位，           ││
│  │  若放量突破可加仓，否则维持震荡格局。                   ││
│  │                                                         ││
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
│  ┌─交易总结────────────────────────────────────────────────┐│
│  │                                                         ││
│  │  今日操作:                                              ││
│  │  ┌──────────────────────────────────────────────────┐  ││
│  │  │ 代码    名称    操作   价格   数量   盈亏    评价 │  ││
│  │  │ 000001 平安银行 买入  13.85   1000    -    👍    │  ││
│  │  │ 600519 贵州茅台 卖出  1850    100  +5.2%  ✅    │  ││
│  │  │ 300750 宁德时代 买入  215     500    -    ⚠️    │  ││
│  │  └──────────────────────────────────────────────────┘  ││
│  │                                                         ││
│  │  🤖 AI点评：                                            ││
│  │  今日操作整体合理。平安银行买入价位适中，短线有套利空间；││
│  │  茅台卖出时机正确，成功锁定利润；宁德时代买入稍激进，   ││
│  │  建议设置止损位205元。                                  ││
│  │                                                         ││
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
│  ┌─机会挖掘────────────────────────────────────────────────┐│
│  │                                                         ││
│  │  AI识别潜在机会:                                        ││
│  │  ┌──────────────────────────────────────────────────┐  ││
│  │  │ 股票     理由                        评分        │  ││
│  │  │ 比亚迪   新能源反弹龙头，技术面突破   ⭐⭐⭐⭐  │  ││
│  │  │ 科大讯飞 AI龙头，主力资金持续流入    ⭐⭐⭐⭐  │  ││
│  │  │ 中际旭创 光模块龙头，业绩超预期      ⭐⭐⭐    │  ││
│  │  └──────────────────────────────────────────────────┘  ││
│  │                                                         ││
│  │  [详细分析] [加入自选]                                   ││
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
│  ┌─风险预警────────────────────────────────────────────────┐│
│  │                                                         ││
│  │  ⚠️ 持仓风险提示:                                       ││
│  │                                                         ││
│  │  • 000651 格力电器: 破位20日均线，建议减仓观望         ││
│  │  • 601318 中国平安: 北向资金连续3日净流出，注意风险     ││
│  │                                                         ││
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
│  [导出PDF] [分享] [历史复盘]                                 │
└─────────────────────────────────────────────────────────────┘
```

### 7.3 核心组件

| 组件名 | 功能 |
|-------|------|
| DailyReviewReport | 每日复盘报告生成与展示 |
| TradingSummary | 交易记录导入与AI点评 |
| OpportunityDiscovery | AI机会挖掘与推荐 |
| RiskWarning | 持仓股风险预警 |
| ReviewHistory | 历史复盘报告列表 |

### 7.4 后端API

```python
# 生成每日复盘
POST /ai/review/daily
{
    "date": "2026-03-24",
    "include_sectors": true,
    "include_capital_flow": true,
    "include_outlook": true
}

# 获取交易总结
GET /ai/review/trading-summary?date=2026-03-24

# AI机会挖掘
POST /ai/review/opportunities
{
    "focus_sectors": ["人工智能", "新能源"],
    "risk_preference": "moderate",  # conservative | moderate | aggressive
    "capital_size": 100000
}

# 风险预警
GET /ai/review/risk-warnings?user_id=xxx

# 历史复盘
GET /ai/review/history?limit=30
```

### 7.5 复盘报告模板

```markdown
# 每日复盘报告 - {date}

## 一、市场概况
- 三大指数走势
- 成交量变化
- 涨跌分布
- 市场情绪

## 二、板块表现
- 领涨板块及原因
- 领跌板块及原因
- 板块轮动分析

## 三、资金动向
- 主力资金流向
- 北向资金动向
- 融资融券变化

## 四、热点事件
- 重要新闻
- 政策解读
- 公告影响

## 五、明日展望
- 大盘走势预判
- 关注板块
- 操作建议

## 六、AI建议
- 仓位建议
- 风险提示
- 机会提示
```

---

## 八、后端架构设计

### 6.1 多Agent协调器（核心参考 daily_stock_analysis）

参考 `daily_stock_analysis-main/src/agent/orchestrator.py` 设计：

```python
# backend/stock-service/app/services/agent_orchestrator.py

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum

class Signal(str, Enum):
    """标准交易信号"""
    STRONG_BUY = "strong_buy"
    BUY = "buy"
    HOLD = "hold"
    SELL = "sell"
    STRONG_SELL = "strong_sell"

class StageStatus(str, Enum):
    """阶段状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class AgentContext:
    """Agent共享上下文 - 多Agent数据传递"""
    query: str = ""
    stock_code: str = ""
    stock_name: str = ""
    session_id: str = ""

    # 收集的数据（由数据获取阶段填充）
    data: Dict[str, Any] = field(default_factory=dict)
    # 典型键: "realtime_quote", "daily_history", "trend_result",
    #        "chip_distribution", "news_context"

    # 各Agent的观点
    opinions: List["AgentOpinion"] = field(default_factory=list)

    # 风险标记
    risk_flags: List[Dict[str, Any]] = field(default_factory=list)

    # 元数据
    meta: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AgentOpinion:
    """单个Agent的分析意见"""
    agent_name: str = ""
    signal: str = ""
    confidence: float = 0.0
    reasoning: str = ""
    key_levels: Dict[str, float] = field(default_factory=dict)
    raw_data: Dict[str, Any] = field(default_factory=dict)

@dataclass
class StageResult:
    """单个阶段的执行结果"""
    stage_name: str = ""
    status: StageStatus = StageStatus.PENDING
    opinion: Optional[AgentOpinion] = None
    error: Optional[str] = None
    duration_s: float = 0.0
    tokens_used: int = 0
    tool_calls_count: int = 0

VALID_MODES = ("quick", "standard", "full", "specialist")

class AgentOrchestrator:
    """多Agent协调器"""

    def __init__(self, mode: str = "standard", config: Dict = None):
        self.mode = mode
        self.config = config or {}
        self.llm_adapter = LLMToolAdapter(config)
        self.tool_registry = ToolRegistry()

    def _build_agent_chain(self, ctx: AgentContext) -> list:
        """根据模式构建Agent链"""
        agents = []

        if self.mode == "quick":
            # 快速模式：技术分析 → 决策
            agents = [
                TechnicalAgent(self.tool_registry, self.llm_adapter),
                DecisionAgent(self.tool_registry, self.llm_adapter),
            ]
        elif self.mode == "standard":
            # 标准模式：技术 → 情报 → 决策
            agents = [
                TechnicalAgent(self.tool_registry, self.llm_adapter),
                IntelAgent(self.tool_registry, self.llm_adapter),
                DecisionAgent(self.tool_registry, self.llm_adapter),
            ]
        elif self.mode == "full":
            # 完整模式：技术 → 情报 → 风险 → 决策
            agents = [
                TechnicalAgent(self.tool_registry, self.llm_adapter),
                IntelAgent(self.tool_registry, self.llm_adapter),
                RiskAgent(self.tool_registry, self.llm_adapter),
                DecisionAgent(self.tool_registry, self.llm_adapter),
            ]
        elif self.mode == "specialist":
            # 专家模式：技术 → 情报 → 风险 → 专家 → 决策
            agents = [
                TechnicalAgent(self.tool_registry, self.llm_adapter),
                IntelAgent(self.tool_registry, self.llm_adapter),
                RiskAgent(self.tool_registry, self.llm_adapter),
                SpecialistAgent(self.tool_registry, self.llm_adapter),
                DecisionAgent(self.tool_registry, self.llm_adapter),
            ]

        return agents

    async def run(
        self,
        stock_code: str,
        query: str = "",
        progress_callback: Callable = None,
        timeout_seconds: float = None,
    ) -> Dict[str, Any]:
        """执行完整分析流程"""
        ctx = AgentContext(
            query=query,
            stock_code=stock_code,
            session_id=str(uuid.uuid4()),
        )

        agents = self._build_agent_chain(ctx)
        stats = AgentRunStats()

        for agent in agents:
            result = agent.run(ctx, progress_callback, timeout_seconds)
            stats.record_stage(result)

            if not result.success:
                break

        return self._build_final_response(ctx, stats)
```

### 6.2 工具注册中心（参考 daily_stock_analysis）

```python
# backend/stock-service/app/services/tool_registry.py

from dataclasses import dataclass
from typing import Callable, List, Optional, Any, Dict

@dataclass
class ToolParameter:
    """工具参数定义"""
    name: str
    type: str  # "string" | "number" | "integer" | "boolean" | "array"
    description: str
    required: bool = True
    enum: Optional[List[str]] = None
    default: Any = None

@dataclass
class ToolDefinition:
    """工具完整定义"""
    name: str
    description: str
    parameters: List[ToolParameter]
    handler: Callable
    category: str = "data"  # data | analysis | search | action

    def to_openai_tool(self) -> dict:
        """转换为OpenAI工具格式"""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self._params_json_schema(),
            },
        }

class ToolRegistry:
    """工具注册中心"""

    def __init__(self):
        self._tools: Dict[str, ToolDefinition] = {}

    def register(self, tool_def: ToolDefinition) -> None:
        self._tools[tool_def.name] = tool_def

    def execute(self, name: str, **kwargs) -> Any:
        tool_def = self._tools.get(name)
        if tool_def is None:
            raise KeyError(f"Tool '{name}' not found")
        return tool_def.handler(**kwargs)

    def to_openai_tools(self) -> List[dict]:
        return [t.to_openai_tool() for t in self._tools.values()]

# 注册内置工具
def register_default_tools(registry: ToolRegistry):
    """注册默认工具集"""

    @tool(name="get_realtime_quote", description="获取股票实时行情")
    def get_realtime_quote(stock_code: str) -> dict:
        # 调用AkShare获取实时行情
        pass

    @tool(name="get_daily_history", description="获取日K线历史数据")
    def get_daily_history(stock_code: str, days: int = 60) -> list:
        pass

    @tool(name="analyze_trend", description="分析股票趋势")
    def analyze_trend(kline_data: list) -> dict:
        pass

    @tool(name="get_chip_distribution", description="获取筹码分布")
    def get_chip_distribution(stock_code: str) -> dict:
        pass

    @tool(name="get_news", description="获取股票相关新闻")
    def get_news(stock_code: str, days: int = 7) -> list:
        pass
```

### 6.3 BaseAgent 基类设计（参考 daily_stock_analysis）

```python
# backend/stock-service/app/services/agents/base_agent.py

from abc import ABC, abstractmethod
from typing import Optional, List

class BaseAgent(ABC):
    """Agent基类"""

    agent_name: str = "base"
    tool_names: Optional[List[str]] = None  # None = 所有工具可用
    max_steps: int = 6

    def __init__(
        self,
        tool_registry: ToolRegistry,
        llm_adapter: LLMToolAdapter,
        skill_instructions: str = "",
    ):
        self.tool_registry = tool_registry
        self.llm_adapter = llm_adapter
        self.skill_instructions = skill_instructions

    @abstractmethod
    def system_prompt(self, ctx: AgentContext) -> str:
        """返回系统提示词"""

    @abstractmethod
    def build_user_message(self, ctx: AgentContext) -> str:
        """构建用户消息"""

    def post_process(self, ctx: AgentContext, raw_text: str) -> Optional[AgentOpinion]:
        """后处理LLM输出，提取结构化意见"""
        return None

    def run(
        self,
        ctx: AgentContext,
        progress_callback: Callable = None,
        timeout_seconds: float = None,
    ) -> StageResult:
        """执行Agent分析"""
        result = StageResult(stage_name=self.agent_name, status=StageStatus.RUNNING)

        try:
            messages = self._build_messages(ctx)
            registry = self._filtered_registry()

            loop_result = run_agent_loop(
                messages=messages,
                tool_registry=registry,
                llm_adapter=self.llm_adapter,
                max_steps=self.max_steps,
                progress_callback=progress_callback,
                max_wall_clock_seconds=timeout_seconds,
            )

            if loop_result.success:
                opinion = self.post_process(ctx, loop_result.content)
                if opinion:
                    ctx.add_opinion(opinion)
                    result.opinion = opinion

            result.status = StageStatus.COMPLETED

        except Exception as exc:
            result.status = StageStatus.FAILED
            result.error = str(exc)

        return result

    def _filtered_registry(self) -> ToolRegistry:
        """返回过滤后的工具注册表"""
        if self.tool_names is None:
            return self.tool_registry

        filtered = ToolRegistry()
        for name in self.tool_names:
            tool_def = self.tool_registry.get(name)
            if tool_def:
                filtered.register(tool_def)
        return filtered
```

### 6.4 Skills/Strategies 系统（参考 daily_stock_analysis）

```python
# backend/stock-service/app/services/skills/defaults.py

CORE_TRADING_SKILL_POLICY_ZH = """## 默认技能基线（必须严格遵守）

当前激活的 skills 可以补充细化分析视角，但默认风险控制和交易节奏必须遵守以下基线。

### 1. 严进策略（不追高）
- **绝对不追高**：当股价偏离 MA5 超过 5% 时，坚决不买入
- 乖离率 < 2%：最佳买点区间
- 乖离率 2-5%：可小仓介入
- 乖离率 > 5%：严禁追高！直接判定为"观望"

### 2. 趋势交易（顺势而为）
- **多头排列必须条件**：MA5 > MA10 > MA20
- 只做多头排列的股票，空头排列坚决不碰
- 均线发散上行优于均线粘合

### 3. 效率优先（筹码结构）
- 关注筹码集中度：90%集中度 < 15% 表示筹码集中
- 获利比例分析：70-90% 获利盘时需警惕获利回吐
- 平均成本与现价关系：现价高于平均成本 5-15% 为健康

### 4. 买点偏好（回踩支撑）
- **最佳买点**：缩量回踩 MA5 获得支撑
- **次优买点**：回踩 MA10 获得支撑
- **观望情况**：跌破 MA20 时观望

### 5. 风险排查重点
- 减持公告、业绩预亏、监管处罚、行业政策利空、大额解禁

### 6. 估值关注（PE/PB）
- PE 明显偏高时需在风险点中说明

### 7. 强势趋势股放宽
- 强势趋势股可适当放宽乖离率要求，轻仓追踪但需设止损
"""

# 策略加载器
def load_skills_from_directory(directory: Path) -> List[Skill]:
    """从目录加载策略/技能"""
    skills = []
    for file_path in directory.glob("*.py"):
        module = import_module_from_path(file_path)
        if hasattr(module, "SKILL"):
            skills.append(module.SKILL)
    return skills
```

### 6.5 API 路由设计

```python
# backend/stock-service/app/api/endpoints/ai_analysis_routes.py

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sse_starlette.sse import EventSourceResponse

router = APIRouter(prefix="/ai", tags=["AI分析"])

@router.post("/chat")
async def chat(request: ChatRequest):
    """AI对话接口"""
    pass

@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """AI对话流式响应（SSE）"""
    async def generate():
        async for chunk in ai_service.chat_stream(request):
            yield {"data": json.dumps(chunk)}
    return EventSourceResponse(generate())

@router.post("/agents/analyze")
async def agents_analyze(request: AgentAnalyzeRequest):
    """多Agent分析"""
    result = await agent_orchestrator.run(
        stock_code=request.stock_code,
        query=request.query,
        mode=request.mode,
    )
    return result

@router.post("/agents/analyze/stream")
async def agents_analyze_stream(request: AgentAnalyzeRequest):
    """多Agent分析流式响应（实时进度）"""
    async def generate():
        async for event in agent_orchestrator.run_stream(request):
            yield {"event": event.type, "data": json.dumps(event.data)}
    return EventSourceResponse(generate())

@router.post("/report/generate")
async def generate_report(request: ReportGenerateRequest):
    """生成研报"""
    pass

@router.get("/report/{report_id}/export")
async def export_report(report_id: str, format: str = "pdf"):
    """导出研报 (PDF/Word/Markdown)"""
    pass

@router.post("/schedule/create")
async def create_schedule(request: ScheduleCreateRequest):
    """创建定时分析任务"""
    pass

@router.get("/history")
async def get_analysis_history(stock_code: str = None, limit: int = 20):
    """获取分析历史"""
    pass
```

### 6.6 进度跟踪服务（参考 TradingAgents-CN）

```python
# backend/stock-service/app/services/progress_tracker.py

import redis
from datetime import datetime
from typing import Dict, Any, List

class RedisProgressTracker:
    """Redis进度跟踪器"""

    def __init__(self, task_id: str, redis_client: redis.Redis):
        self.task_id = task_id
        self.redis = redis_client
        self.start_time = datetime.now()

    def update_progress(self, message: str, step: str = None):
        """更新进度"""
        data = {
            "task_id": self.task_id,
            "status": "processing",
            "message": message,
            "current_step": step,
            "elapsed_time": (datetime.now() - self.start_time).total_seconds(),
            "updated_at": datetime.now().isoformat(),
        }
        self.redis.hset(f"task_progress:{self.task_id}", mapping=data)

    def mark_completed(self, message: str):
        """标记完成"""
        self.redis.hset(f"task_progress:{self.task_id}", mapping={
            "status": "completed",
            "message": message,
            "completed_at": datetime.now().isoformat(),
        })

    def mark_failed(self, error: str):
        """标记失败"""
        self.redis.hset(f"task_progress:{self.task_id}", mapping={
            "status": "failed",
            "error": error,
            "failed_at": datetime.now().isoformat(),
        })

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        data = self.redis.hgetall(f"task_progress:{self.task_id}")
        return {k.decode(): v.decode() for k, v in data.items()}
```

### 6.7 批量分析服务（参考 TradingAgents-CN）

```python
# backend/stock-service/app/services/batch_analysis_service.py

from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor
import asyncio

class BatchAnalysisService:
    """批量分析服务"""

    def __init__(self, max_concurrent: int = 3):
        self.max_concurrent = max_concurrent
        self.queue_service = QueueService()

    async def submit_batch(
        self,
        stock_codes: List[str],
        config: Dict,
        user_id: str,
    ) -> Dict:
        """提交批量分析任务"""
        batch_id = str(uuid.uuid4())
        tasks = []

        for stock_code in stock_codes:
            task_id = str(uuid.uuid4())
            task = AnalysisTask(
                task_id=task_id,
                batch_id=batch_id,
                user_id=user_id,
                stock_code=stock_code,
                config=config,
                status="pending",
            )
            tasks.append(task)
            await self.queue_service.enqueue(task)

        # 保存批次信息
        await db.analysis_batches.insert_one({
            "batch_id": batch_id,
            "total_tasks": len(tasks),
            "completed_tasks": 0,
            "failed_tasks": 0,
            "status": "pending",
            "created_at": datetime.now(),
        })

        return {
            "batch_id": batch_id,
            "total_tasks": len(tasks),
        }

    async def get_batch_status(self, batch_id: str) -> Dict:
        """获取批次状态"""
        batch = await db.analysis_batches.find_one({"batch_id": batch_id})
        tasks = await db.analysis_tasks.find({"batch_id": batch_id}).to_list()

        return {
            "batch_id": batch_id,
            "status": batch.get("status"),
            "total_tasks": batch.get("total_tasks"),
            "completed_tasks": batch.get("completed_tasks"),
            "failed_tasks": batch.get("failed_tasks"),
            "tasks": [
                {
                    "task_id": t["task_id"],
                    "stock_code": t["stock_code"],
                    "status": t["status"],
                    "result": t.get("result"),
                }
                for t in tasks
            ],
        }
```

### 6.8 研报导出服务（参考 TradingAgents-CN）

```python
# backend/stock-service/app/services/report_export_service.py

from docx import Document
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import markdown

class ReportExportService:
    """研报导出服务"""

    async def export_to_pdf(self, report: Report) -> bytes:
        """导出为PDF"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)

        story = []
        # 解析Markdown内容
        for line in report.content.split("\n"):
            if line.startswith("# "):
                story.append(Paragraph(line[2:], self.styles["Heading1"]))
            elif line.startswith("## "):
                story.append(Paragraph(line[3:], self.styles["Heading2"]))
            else:
                story.append(Paragraph(line, self.styles["Normal"]))
            story.append(Spacer(1, 6))

        doc.build(story)
        return buffer.getvalue()

    async def export_to_word(self, report: Report) -> bytes:
        """导出为Word"""
        doc = Document()

        # 解析Markdown内容
        for line in report.content.split("\n"):
            if line.startswith("# "):
                doc.add_heading(line[2:], level=1)
            elif line.startswith("## "):
                doc.add_heading(line[3:], level=2)
            elif line.startswith("### "):
                doc.add_heading(line[4:], level=3)
            else:
                doc.add_paragraph(line)

        buffer = io.BytesIO()
        doc.save(buffer)
        return buffer.getvalue()

    async def export_to_markdown(self, report: Report) -> str:
        """导出为Markdown"""
        return report.content
```

---

## 九、前端文件结构

```
frontend/src/views/Vadmin/Stock/AI/
├── Chat/                          # AI对话助手
│   ├── Chat.vue                   # 主页面
│   └── components/
│       ├── StockInfoPanel.vue     # 股票信息面板
│       ├── ChatArea.vue           # 对话区域
│       ├── QuickQuestions.vue     # 快捷问题
│       └── ChatHistory.vue        # 历史对话
│
├── Workbench/                     # AI分析师工作台
│   ├── Workbench.vue              # 主页面
│   └── components/
│       ├── AnalysisConfig.vue     # 分析配置
│       ├── AgentCard.vue          # 角色卡片
│       ├── AgentPanel.vue         # 角色分析面板
│       ├── DebateRecord.vue       # 辩论记录
│       ├── SynthesisResult.vue    # 综合研判
│       └── FollowUpChat.vue       # 追问对话
│
├── Report/                        # AI研报中心
│   ├── Report.vue                 # 主页面
│   └── components/
│       ├── ReportConfig.vue       # 研报配置
│       ├── ReportContent.vue      # 研报内容
│       ├── ReportToc.vue          # 目录导航
│       ├── ReportExport.vue       # 导出功能
│       └── ReportHistory.vue      # 历史研报
│
├── MarketInsight/                 # 市场洞察
│   ├── MarketInsight.vue          # 主页面
│   └── components/
│       ├── MarketOverview.vue     # 市场概览
│       ├── SectorRotation.vue     # 板块轮动
│       ├── CapitalFlow.vue        # 资金流向
│       ├── HotSpotDiscovery.vue   # 热点挖掘
│       └── AIMarketInterpret.vue  # AI解读
│
├── DailyReview/                   # 盘后复盘
│   ├── DailyReview.vue            # 主页面
│   └── components/
│       ├── DailyReviewReport.vue  # 每日复盘报告
│       ├── TradingSummary.vue     # 交易总结
│       ├── OpportunityDiscovery.vue # 机会挖掘
│       ├── RiskWarning.vue        # 风险预警
│       └── ReviewHistory.vue      # 历史复盘
│
├── Schedule/                      # 每日自动分析
│   ├── Schedule.vue               # 主页面
│   └── components/
│       ├── ScheduleConfig.vue     # 定时配置
│       ├── StockPool.vue          # 股票池管理
│       ├── PushConfig.vue         # 推送配置
│       └── AnalysisHistory.vue    # 分析历史
│
└── components/                    # 公共组件
    ├── ModelSelector.vue          # 模型选择器
    └── StockSearch.vue            # 股票搜索
```

---

## 十、路由配置

在 `frontend/src/router/index.ts` 添加：

```typescript
{
  path: 'ai-chat',
  component: () => import('@/views/Vadmin/Stock/AI/Chat/Chat.vue'),
  name: 'AIChat',
  meta: { title: 'AI对话助手', noCache: true }
},
{
  path: 'ai-workbench',
  component: () => import('@/views/Vadmin/Stock/AI/Workbench/Workbench.vue'),
  name: 'AIWorkbench',
  meta: { title: 'AI分析师工作台', noCache: true }
},
{
  path: 'ai-report',
  component: () => import('@/views/Vadmin/Stock/AI/Report/Report.vue'),
  name: 'AIReport',
  meta: { title: 'AI研报中心', noCache: true }
},
{
  path: 'ai-market-insight',
  component: () => import('@/views/Vadmin/Stock/AI/MarketInsight/MarketInsight.vue'),
  name: 'AIMarketInsight',
  meta: { title: '市场洞察', noCache: true }
},
{
  path: 'ai-daily-review',
  component: () => import('@/views/Vadmin/Stock/AI/DailyReview/DailyReview.vue'),
  name: 'AIDailyReview',
  meta: { title: '盘后复盘', noCache: true }
},
{
  path: 'ai-schedule',
  component: () => import('@/views/Vadmin/Stock/AI/Schedule/Schedule.vue'),
  name: 'AISchedule',
  meta: { title: '每日自动分析', noCache: true }
}
```

---

## 十一、数据模型

### 11.1 对话模型

```typescript
interface ChatMessage {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

interface Conversation {
  id: string
  stock_code: string
  stock_name: string
  messages: ChatMessage[]
  created_at: Date
  updated_at: Date
}
```

### 11.2 分析模型

```typescript
interface AgentResult {
  agent_type: string
  agent_name: string
  judgment: 'bullish' | 'bearish' | 'neutral'
  confidence: number
  key_points: string[]
  detail: string
}

interface DebateMessage {
  agent_type: string
  agent_name: string
  content: string
  timestamp: Date
}

interface SynthesisResult {
  conclusion: 'bullish' | 'bearish' | 'neutral'
  confidence: number
  target_price: number
  stop_loss: number
  risk_level: string
  operation_advice: string
}
```

### 11.3 研报模型

```typescript
interface Report {
  id: string
  stock_code: string
  stock_name: string
  period: string
  dimensions: string[]
  agents: string[]
  content: string
  conclusion: SynthesisResult
  created_at: Date
}
```

---

## 十二、AI Prompt 模板

### 12.1 技术分析师

```
你是一位资深技术分析师，拥有20年A股技术分析经验。
请基于以下数据分析股票的技术面：

股票代码：{stock_code}
当前价格：{current_price}
K线数据：{kline_data}
技术指标：{indicators}

请从以下维度分析：
1. K线形态
2. 均线系统
3. MACD/KDJ/RSI指标
4. 成交量分析
5. 支撑压力位

输出格式：
- 判断：看多/看空/中性
- 置信度：0-100%
- 关键点位
- 详细分析
```

### 12.2 基本面分析师

```
你是一位基本面分析专家，专注于价值投资分析。
请基于以下数据分析股票的基本面：

股票代码：{stock_code}
财务数据：{financial_data}
估值指标：{valuation}
行业数据：{industry_data}

请从以下维度分析：
1. 盈利能力（ROE、毛利率、净利率）
2. 成长性（营收增速、利润增速）
3. 估值水平（PE、PB、PS）
4. 财务健康（资产负债率、现金流）

输出格式：
- 判断：看多/看空/中性
- 置信度：0-100%
- 核心观点
- 详细分析
```

---

## 十三、每日自动分析

参考 `daily_stock_analysis` 项目，增加每日自动分析功能：

### 13.1 功能描述

| 功能 | 描述 |
|------|------|
| 定时任务 | 每日收盘后自动分析指定股票池 |
| 股票池管理 | 自选股、持仓股、关注板块 |
| 自动推送 | 分析结果推送到微信/邮件/Webhook |
| 历史回溯 | 查看历史分析记录和准确性 |

### 13.2 定时任务配置

```python
# backend/stock-service/app/services/scheduled_analysis.py

from apscheduler.schedulers.asyncio import AsyncIOScheduler

class ScheduledAnalysisService:
    """定时分析服务"""

    def __init__(self):
        self.scheduler = AsyncIOScheduler()

    async def start(self):
        """启动定时任务"""
        # 每日收盘后15:30执行
        self.scheduler.add_job(
            self.daily_analysis,
            'cron',
            hour=15,
            minute=30,
            day_of_week='mon-fri'
        )
        self.scheduler.start()

    async def daily_analysis(self):
        """每日分析任务"""
        # 1. 获取待分析股票池
        stocks = await self.get_analysis_pool()

        # 2. 多Agent分析
        for stock in stocks:
            result = await self.agent_orchestrator.analyze(
                stock_code=stock.code,
                period='短线',
                agents=['technical', 'fundamental', 'news', 'risk']
            )

            # 3. 保存分析结果
            await self.save_analysis_result(result)

            # 4. 触发推送
            await self.push_notification(result)
```

### 13.3 推送渠道

| 渠道 | 配置 | 说明 |
|------|------|------|
| 企业微信 | Webhook URL | 推送分析摘要 |
| 钉钉 | Webhook URL | 推送分析摘要 |
| 邮件 | SMTP配置 | 发送完整研报 |
| Telegram | Bot Token | 推送分析摘要 |

### 13.4 前端配置页面

```
┌─────────────────────────────────────────────────────────────┐
│  ⏰ 每日自动分析配置                                         │
├─────────────────────────────────────────────────────────────┤
│ ┌─分析时间─────────────────────────────────────────────────┐│
│ │ 执行时间: [15:30]  分析周期: [每个交易日]                ││
│ └─────────────────────────────────────────────────────────┘│
│ ┌─股票池───────────────────────────────────────────────────┐│
│ │ ☑ 自选股  ☑ 持仓股  ☐ 指定板块 [选择板块...]            ││
│ │ ☐ 指定股票 [添加股票...]                                 ││
│ └─────────────────────────────────────────────────────────┘│
│ ┌─分析角色─────────────────────────────────────────────────┐│
│ │ ☑ 技术分析师  ☑ 基本面分析师  ☑ 消息面分析师            ││
│ │ ☑ 风控专家    ☐ 量化分析师                               ││
│ └─────────────────────────────────────────────────────────┘│
│ ┌─推送配置─────────────────────────────────────────────────┐│
│ │ ☑ 企业微信  Webhook: [https://...]                       ││
│ │ ☐ 钉钉      Webhook: [                                   ]││
│ │ ☐ 邮件      收件人: [                                   ]││
│ └─────────────────────────────────────────────────────────┘│
│                                                             │
│ [立即执行] [保存配置] [查看历史]                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 十四、实施步骤

### Phase 1: 基础架构
1. 创建API路由文件
2. 创建AI服务层
3. 创建Agent协调器和工具注册中心
4. 创建前端页面骨架

### Phase 2: AI对话助手
1. 实现对话API
2. 实现前端对话组件
3. 集成多模型支持
4. 实现流式响应（SSE）

### Phase 3: AI分析师工作台
1. 实现多Agent分析
2. 实现角色辩论
3. 实现综合研判
4. 实现追问对话

### Phase 4: AI研报中心
1. 实现研报生成
2. 实现研报展示
3. 实现导出功能（PDF/Word）

### Phase 5: 市场洞察
1. 实现市场概览API
2. 实现板块轮动分析
3. 实现资金流向分析
4. 实现AI市场解读

### Phase 6: 盘后复盘
1. 实现每日复盘报告生成
2. 实现交易总结与AI点评
3. 实现机会挖掘
4. 实现风险预警

### Phase 7: 每日自动分析
1. 实现定时任务调度
2. 实现股票池管理
3. 实现推送通知

---

## 十五、扩展功能

- 自定义Agent角色
- 分析模板管理
- 多股票对比分析
- 实时推送更新
- 语音交互