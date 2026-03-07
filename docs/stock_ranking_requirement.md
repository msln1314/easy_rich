# 个股排行功能需求文档

## 一、功能概述

基于 akshare 接口实现个股数据排行功能，提供多种维度的排行榜，帮助用户快速发现市场热点和交易机会。

## 二、功能需求

### 2.1 排行类型

| 排行类型 | 排序字段 | 说明 |
|---------|---------|------|
| 换手率排行 | turnover_rate | 按换手率降序排列，反映股票活跃度 |
| 资金量排行 | amount | 按成交额降序排列，反映资金关注度 |
| 量比排行 | volume_ratio | 按量比降序排列，反映成交量放大倍数 |
| 涨跌幅排行 | change_percent | 按涨跌幅降序/升序排列，反映涨跌情况 |
| 市值排行 | total_market_cap | 按总市值降序排列，反映公司规模 |
| 振幅排行 | amplitude | 按振幅降序排列，反映价格波动程度 |

### 2.2 数据来源

使用 akshare 的 `stock_zh_a_spot_em()` 接口获取实时行情数据，该接口包含所需的所有排行字段。

### 2.3 数据存储

#### 方案一：使用现有表（推荐）
- **表名**: `stock_basic_info`
- **说明**: 现有表已包含所有排行所需的字段
- **更新策略**: 定时任务从 akshare 更新实时行情数据

#### 方案二：创建排行快照表
- **表名**: `stock_ranking_snapshot`
- **说明**: 存储历史排行快照，支持时间序列分析
- **字段**: 快照时间 + 排行类型 + 排名 + 股票信息

**本次开发采用方案一**，后续可扩展方案二。

### 2.4 功能列表

#### 后端功能
1. **个股排行 API**
   - 按类型获取排行列表（支持分页）
   - 支持多维度排序
   - 支持行业、板块筛选

2. **数据更新任务**
   - 定时从 akshare 更新实时行情
   - 更新频率建议：每 10-30 分钟

#### 前端功能
1. **排行页面**
   - 多 Tab 切换不同排行类型
   - 表格展示排行数据
   - 支持搜索、筛选、导出

2. **排行榜特性**
   - Top 标记（前三名高亮）
   - 排名数字显示
   - 涨跌颜色标识（红涨绿跌）

## 三、数据模型设计

### 3.1 扩展 stock_basic_info 表（已存在）

现有字段已满足需求：
- `turnover_rate` - 换手率
- `amount` - 成交额
- `volume_ratio` - 量比
- `change_percent` - 涨跌幅
- `total_market_cap` - 总市值
- `amplitude` - 振幅

### 3.2 排行返回数据结构

```python
class StockRankingOut(BaseModel):
    """排行数据输出"""
    id: int
    rank: int  # 排名
    stock_code: str
    stock_name: str
    industry: str | None
    current_price: float
    change_percent: float
    change_amount: float
    turnover_rate: float | None
    amount: float | None
    volume_ratio: float | None
    total_market_cap: float | None
    amplitude: float | None
    # ... 其他字段
```

### 3.3 排行类型枚举

```python
class RankingType(str, Enum):
    """排行类型"""
    TURNOVER = "turnover"  # 换手率
    AMOUNT = "amount"  # 资金量
    VOLUME_RATIO = "volume_ratio"  # 量比
    CHANGE_PERCENT = "change_percent"  # 涨跌幅
    MARKET_CAP = "market_cap"  # 市值
    AMPLITUDE = "amplitude"  # 振幅
```

## 四、API 接口设计

### 4.1 获取排行列表

```
GET /api/v1/stock/ranking
```

**请求参数:**
```json
{
  "ranking_type": "turnover",  // 排行类型: turnover/amount/volume_ratio/change_percent/market_cap/amplitude
  "page": 1,
  "page_size": 20,
  "order": "desc",  // 排序方向: desc/asc
  "industry": null,  // 行业筛选（可选）
  "market": null  // 市场筛选（可选）
}
```

**响应数据:**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "items": [
      {
        "rank": 1,
        "stock_code": "000001",
        "stock_name": "平安银行",
        "industry": "银行",
        "current_price": 10.50,
        "change_percent": 5.23,
        "turnover_rate": 15.23,
        "amount": 1234567890.0,
        ...
      }
    ],
    "total": 5000,
    "page": 1,
    "page_size": 20
  }
}
```

### 4.2 更新实时行情（定时任务）

```
POST /api/v1/stock/sync/realtime
```

## 五、前端页面设计

### 5.1 页面路由

- 路径: `/stock/ranking`
- 菜单: 股票分析 > 个股排行

### 5.2 页面布局

```
┌─────────────────────────────────────────┐
│  个股排行                              │
├─────────────────────────────────────────┤
│  [换手率] [资金量] [量比] [涨跌幅]       │
├─────────────────────────────────────────┤
│  排名 | 代码 | 名称 | 最新价 | 涨跌幅  │
│  🔥 1 | 000001 | 平安银行 | 10.50 | +5.23% │
│  🥈 2 | 000002 | 万科A | 12.30 | +4.56% │
│  🥉 3 | 000003 | 国农科技 | 8.90 | +3.21% │
│  4   | 000004 | ... | ... | ...   │
│  ...                                 │
└─────────────────────────────────────────┘
```

### 5.3 交互功能

1. **Tab 切换**: 点击不同 Tab 切换排行类型
2. **排序切换**: 涨跌幅支持升序/降序切换
3. **筛选**: 支持行业、市场筛选
4. **搜索**: 支持股票代码/名称搜索
5. **刷新**: 手动刷新数据
6. **导出**: 导出排行数据到 Excel

## 六、技术实现要点

### 6.1 后端实现

1. **数据获取**
   - 使用 akshare `stock_zh_a_spot_em()` 获取实时行情
   - 使用 `stock_service.py` 中的方法

2. **数据排序**
   - 使用 SQLAlchemy 的 `order_by()` 动态排序
   - 支持 NULL 值处理（NULL 排在最后）

3. **排名计算**
   - 使用窗口函数 `ROW_NUMBER()` 或应用层计算

4. **定时任务**
   - 使用 APScheduler 每 15 分钟更新一次
   - 任务路径: `apps/module_task/scheduler.py`

### 6.2 前端实现

1. **组件结构**
   - 使用 Vue 3 + TypeScript
   - 使用 TDesign 组件库
   - 参考 `AnalysisWrite.vue` 的表格实现

2. **状态管理**
   - 当前排行类型
   - 排序方向
   - 筛选条件
   - 数据列表

3. **性能优化**
   - 分页加载
   - 防抖搜索
   - 缓存请求结果

## 七、开发计划

### Phase 1: 后端开发
- [ ] 创建排行 API 接口
- [ ] 添加排行类型枚举
- [ ] 实现排行查询逻辑
- [ ] 添加数据更新定时任务

### Phase 2: 前端开发
- [ ] 创建排行页面组件
- [ ] 实现 Tab 切换
- [ ] 实现表格展示
- [ ] 实现筛选和搜索
- [ ] 添加导出功能

### Phase 3: 测试和优化
- [ ] 单元测试
- [ ] 集成测试
- [ ] 性能优化
- [ ] 文档完善

## 八、后续扩展

1. **历史排行**: 支持查看历史某一天的排行
2. **自定义排行**: 支持用户自定义排序规则
3. **排行对比**: 支持多日排行对比
4. **排行预警**: 某股进入榜单时推送通知
5. **AI 分析**: 基于排行数据生成分析报告
