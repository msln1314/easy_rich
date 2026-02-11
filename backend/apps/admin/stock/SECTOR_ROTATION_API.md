# 板块轮动分析 API 文档

## 接口概述

板块轮动分析接口基于 `stock_board_industry` 模型，为前端提供板块排行、资金流向趋势、热力图等数据。

## API 列表

### 1. 板块排行榜
**接口地址**: `GET /api/v1/stock/sector/ranking`

**请求参数**:
- `start_date` (可选): 开始日期，格式 YYYY-MM-DD
- `end_date` (可选): 结束日期，格式 YYYY-MM-DD  
- `sector_type` (可选): 板块类型
- `limit` (可选): 返回数量限制，默认50

**响应示例**:
```json
{
  "code": 200,
  "data": [
    {
      "rank": 1,
      "sector_name": "人工智能",
      "sector_code": "BK1001",
      "change_rate": 3.45,
      "volume": 156.78,
      "turnover_rate": 0,
      "leading_stocks": 15,
      "stock_count": 30,
      "market_cap": 0,
      "net_inflow": 12.34,
      "average_price": 45.67,
      "total_volume": 234.56,
      "leading_stock": "比亚迪",
      "leading_stock_code": "601234",
      "leading_stock_change": 2.89,
      "up_count": 15,
      "down_count": 10
    }
  ],
  "count": 1
}
```

### 2. 板块资金流向趋势
**接口地址**: `GET /api/v1/stock/sector/trend`

**请求参数**:
- `start_date` (可选): 开始日期，格式 YYYY-MM-DD，默认30天前
- `end_date` (可选): 结束日期，格式 YYYY-MM-DD，默认今天
- `sector_type` (可选): 板块类型

**响应示例**:
```json
{
  "code": 200,
  "data": [
    {
      "date": "2026-02-01",
      "sectors": {
        "人工智能": {
          "inflow": 100.5,
          "outflow": 0,
          "net_inflow": 12.34
        },
        "新能源汽车": {
          "inflow": 89.2,
          "outflow": 0,
          "net_inflow": -5.67
        }
      }
    }
  ]
}
```

### 3. 板块热力图数据
**接口地址**: `GET /api/v1/stock/sector/heatmap`

**请求参数**:
- `start_date` (可选): 开始日期，格式 YYYY-MM-DD
- `end_date` (可选): 结束日期，格式 YYYY-MM-DD
- `sector_type` (可选): 板块类型

**响应示例**:
```json
{
  "code": 200,
  "data": [
    {
      "rank": 1,
      "sector_name": "人工智能",
      "sector_code": "BK1001",
      "change_rate": 3.45,
      "volume": 156.78,
      "turnover_rate": 0,
      "leading_stocks": 15,
      "stock_count": 30,
      "market_cap": 0,
      "net_inflow": 12.34,
      "average_price": 45.67,
      "total_volume": 234.56,
      "leading_stock": "比亚迪",
      "leading_stock_code": "601234",
      "leading_stock_change": 2.89,
      "up_count": 15,
      "down_count": 10,
      "x": 0,
      "y": 0,
      "r": 3.45
    }
  ]
}
```

### 4. 板块列表
**接口地址**: `GET /api/v1/stock/sector/list`

**请求参数**:
- `sector_type` (可选): 板块类型

**响应示例**:
```json
{
  "code": 200,
  "data": [
    {
      "sector_code": "BK1001",
      "sector_name": "人工智能",
      "sector_type": "industry"
    }
  ]
}
```

### 5. 板块详细信息
**接口地址**: `GET /api/v1/stock/sector/detail/{sector_name}`

**请求参数**:
- `sector_name`: 板块名称 (路径参数)
- `date_str` (可选): 日期，格式 YYYY-MM-DD，默认最新

**响应示例**:
```json
{
  "code": 200,
  "data": {
    "rank": 1,
    "sector_name": "人工智能",
    "sector_code": "BK1001",
    "change_rate": 3.45,
    "volume": 156.78,
    "turnover_rate": 0,
    "leading_stocks": 15,
    "stock_count": 30,
    "market_cap": 0,
    "net_inflow": 12.34,
    "average_price": 45.67,
    "total_volume": 234.56,
    "leading_stock": "比亚迪",
    "leading_stock_code": "601234",
    "leading_stock_change": 2.89,
    "up_count": 15,
    "down_count": 10
  }
}
```

### 6. 板块分析概览
**接口地址**: `GET /api/v1/stock/sector/analysis/summary`

**请求参数**:
- `date_str` (可选): 日期，格式 YYYY-MM-DD，默认最新

**响应示例**:
```json
{
  "code": 200,
  "data": {
    "total_sectors": 50,
    "rising_sectors": 25,
    "falling_sectors": 20,
    "flat_sectors": 5,
    "total_inflow": 1234.56,
    "total_amount": 5678.90,
    "best_sector": {
      "rank": 1,
      "sector_name": "人工智能",
      "change_rate": 8.90
    },
    "worst_sector": {
      "rank": 50,
      "sector_name": "传统能源",
      "change_rate": -6.78
    },
    "date": "2026-02-10"
  }
}
```

## 数据字段说明

### 板块数据字段
- `rank`: 排名
- `sector_name`: 板块名称
- `sector_code`: 板块代码
- `change_rate`: 涨跌幅 (%)
- `volume`: 成交额 (亿元)
- `turnover_rate`: 换手率 (%)
- `leading_stocks`: 上涨家数
- `stock_count`: 总个股数
- `market_cap`: 市值 (亿元)
- `net_inflow`: 净流入 (亿元)
- `average_price`: 均价
- `total_volume`: 总成交量 (万手)
- `leading_stock`: 领涨股名称
- `leading_stock_code`: 领涨股代码
- `leading_stock_change`: 领涨股涨跌幅 (%)
- `up_count`: 上涨家数
- `down_count`: 下跌家数

## 使用说明

1. **默认查询逻辑**: 如果不指定日期，接口默认查询最新日期的数据
2. **日期范围**: 支持指定开始和结束日期进行范围查询
3. **排序逻辑**: 板块排行按涨跌幅降序排列
4. **热力图坐标**: x、y 坐标为自动生成的网格位置，r 为半径大小

## 测试数据生成

可以使用 `sector_rotation_test.py` 脚本生成测试数据：

```bash
cd backend
python apps/admin/stock/sector_rotation_test.py
```

## 前端集成

前端需要对接的接口路径：
- 板块排行: `/api/v1/stock/sector/ranking`
- 资金趋势: `/api/v1/stock/sector/trend`  
- 热力图: `/api/v1/stock/sector/heatmap`

注意：前端需要处理字段名称的映射，因为数据库字段可能与前端期望的字段名称不完全一致。