# Stock Analyze 命令详解与使用示例

本文档详细介绍了 `stock_analyze.py` 的所有命令行参数及其使用场景。

## 目录

1.  [基础参数](#1-基础参数)
2.  [数据源与配置](#2-数据源与配置)
3.  [筛选与过滤](#3-筛选与过滤)
4.  [财务指标评分](#4-财务指标评分)
5.  [验证与回测](#5-验证与回测)
6.  [高级分析与AI](#6-高级分析与ai)
7.  [分钟级分析](#7-分钟级分析)

---

## 1. 基础参数

控制分析的基本范围、对象和输出。

| 参数 | 简写 | 说明 | 示例 |
| :--- | :--- | :--- | :--- |
| `--days` | `-d` | 分析的历史天数（默认30天） | `-d 60` |
| `--start-date` | | 指定开始日期 (YYYYMMDD) | `--start-date 20230101` |
| `--end-date` | | 指定结束日期 (YYYYMMDD) | `--end-date 20231231` |
| `--codes` | `-c` | 指定分析特定的股票代码（逗号分隔） | `-c 600519,000858` |
| `--all` | | 分析所有股票（默认只分析上/深证主板） | `--all` |
| `--k` | `-k` | 结果中显示的股票数量（Top K） | `-k 20` |
| `--parallel` | `-p` | 并行处理的进程数（默认8） | `-p 16` |
| `--topgains` | `-g` | 结果按涨幅排序（默认按得分排序） | `-g` |
| `--debug` | | 启用调试模式（输出详细日志） | `--debug` |

### 示例 1：分析特定股票最近60天的表现
```bash
python stock_analyze.py -c 600519,000858 -d 60
```

### 示例 2：分析2023年全年的所有股票，按涨幅排序，显示前50名
```bash
python stock_analyze.py --all --start-date 20230101 --end-date 20231231 -g -k 50
```

---

## 2. 数据源与配置

控制数据的获取方式和程序配置。

| 参数 | 说明 | 示例 |
| :--- | :--- | :--- |
| `--config` | 指定配置文件路径（默认优先查找 config.toml） | `--config my_config.toml` |
| `--fast` | 快速模式：跳过东财接口，优先使用腾讯与缓存 | `--fast` |
| `--source` | 指定数据源优先级（逗号分隔） | `--source sina,tencent` |
| `--cache` | 启用数据缓存（parquet/csv） | `--cache` |
| `--refresh-cache` | 分析前强制刷新缓存 | `--refresh-cache` |
| `--use-spot-price` | 使用实时最新价作为截止日价 | `--use-spot-price` |

### 示例 3：快速模式分析，强制刷新缓存
```bash
python stock_analyze.py --fast --refresh-cache -d 30
```

---

## 3. 筛选与过滤

用于从海量股票中筛选出符合特定条件的股票。

| 参数 | 说明 | 示例 |
| :--- | :--- | :--- |
| `--sector-filter` | 板块筛选（如AI, 芯片, 军工等） | `--sector-filter AI 芯片` |
| `--expert-filter` | 启用专家规则筛选（综合技术面和基本面） | `--expert-filter` |
| `--breakout` | 启用突破过滤（新高 + 量能放大 + MACD） | `--breakout` |
| `--industry-neutral` | 启用行业中性化排名 | `--industry-neutral` |
| `--min-avg-volume` | 过滤平均成交量过低的股票（单位：手） | `--min-avg-volume 5000` |
| `--max-rsi` | 过滤RSI过高（超买）的股票 | `--max-rsi 80` |
| `--max-volatility` | 过滤波动率过高的股票（单位：%） | `--max-volatility 5.0` |

### 示例 4：筛选"芯片"或"AI"板块中，发生突破且成交量活跃的股票
```bash
python stock_analyze.py --sector-filter 芯片 AI --breakout --min-avg-volume 10000
```

### 示例 5：使用专家规则筛选优质股票，并排除波动过大的风险股
```bash
python stock_analyze.py --expert-filter --max-volatility 8.0
```

---

## 4. 财务指标评分

将基本面指标纳入评分系统。

| 参数 | 说明 |
| :--- | :--- |
| `--use-financial` | 启用基础财务因子调整得分 |
| `--pe` | 启用市盈率(PE)评分 |
| `--pb` | 启用市净率(PB)评分 |
| `--volume` | 启用成交量评分（量比） |
| `--turnover` | 启用成交额评分（换手率） |
| `--dividend` | 启用股息评分（暂不可用） |
| `--dividend-yield` | 启用股息率评分（暂不可用） |
| `--eps` | 启用每股收益评分（暂不可用） |
| `--navps` | 启用每股净资产评分（暂不可用） |

### 示例 6：综合评分：技术面 + PE + PB + 换手率
```bash
python stock_analyze.py -d 30 --pe --pb --turnover
```

---

## 5. 验证与回测

用于验证选股策略在历史数据上的有效性。

| 参数 | 说明 | 示例 |
| :--- | :--- | :--- |
| `--validate-days` | 验证窗口天数（评估选股后N天的表现） | `--validate-days 10` |
| `--trend-day` | 趋势验证天数（评估选股后N天内是否出现上涨） | `--trend-day 3` |
| `--strict` | 严格模式：强制正收益、命中趋势验证 | `--strict` |
| `--forward` | 前瞻模式：不进行验证，仅生成选股结果（用于实盘） | `--forward` |

### 示例 7：回测策略：验证2023年10月选出的股票，在随后10天的表现
```bash
python stock_analyze.py --start-date 20230901 --end-date 20231001 --validate-days 10 --trend-day 3
```
*这个命令会告诉你：如果在2023年10月1日买入，持有10天的收益如何，以及前3天是否有赚钱机会。*

### 示例 8：严格回测：只看那些真正赚了钱的股票
```bash
python stock_analyze.py --start-date 20230901 --end-date 20231001 --validate-days 20 --strict
```

---

## 6. 高级分析与AI

利用大模型生成详细的分析报告。

| 参数 | 说明 | 示例 |
| :--- | :--- | :--- |
| `--ai` | 启用AI分析（需配置 config.toml） | `--ai` |

### 示例 9：生成Top 10股票的AI分析报告
```bash
python stock_analyze.py -d 30 -k 10 --ai
```
*注意：AI分析需要配置 `config.toml` 中的 `[llm]` 部分，且只对生成了图表的股票生效。*

---

## 7. 分钟级分析

进行更高频的日内分析。

| 参数 | 简写 | 说明 | 示例 |
| :--- | :--- | :--- | :--- |
| `--mins` | `-m` | 分钟级周期（1, 5, 15, 30, 60） | `-m 15` |
| `--minute-chart` | | 生成分钟级K线图 | `--minute-chart` |
| `--minute-sim` | | 当分钟数据不可用时，使用日线模拟 | `--minute-sim` |

### 示例 10：分析最近5天的15分钟级别数据，并生成图表
```bash
python stock_analyze.py -d 5 -m 15 --minute-chart
```
