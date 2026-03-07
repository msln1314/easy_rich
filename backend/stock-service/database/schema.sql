-- ============================================
-- 股票分析服务 - MySQL DDL
-- ============================================
-- 本文件包含所有数据表的创建语句
-- 适用于 MySQL 8.0+
-- ============================================

-- ============================================
-- 1. 股票基本信息表
-- ============================================
CREATE TABLE `stock_info` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    `code` VARCHAR(20) NOT NULL COMMENT '股票代码',
    `name` VARCHAR(100) NOT NULL COMMENT '股票名称',
    `industry` VARCHAR(100) DEFAULT NULL COMMENT '行业',
    `listing_date` DATE DEFAULT NULL COMMENT '上市日期',
    `total_market_value` DECIMAL(18,2) DEFAULT NULL COMMENT '总市值(元)',
    `circulating_market_value` DECIMAL(18,2) DEFAULT NULL COMMENT '流通市值(元)',
    `total_share` DECIMAL(18,2) DEFAULT NULL COMMENT '总股本(股)',
    `circulating_share` DECIMAL(18,2) DEFAULT NULL COMMENT '流通股本(股)',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    UNIQUE KEY `uk_code` (`code`),
    KEY `idx_industry` (`industry`),
    KEY `idx_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='股票基本信息表';

-- ============================================
-- 2. 股票实时行情表
-- ============================================
CREATE TABLE `stock_quote` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    `code` VARCHAR(20) NOT NULL COMMENT '股票代码',
    `name` VARCHAR(100) NOT NULL COMMENT '股票名称',
    `price` DECIMAL(12,4) NOT NULL COMMENT '最新价',
    `change` DECIMAL(12,4) NOT NULL COMMENT '涨跌额',
    `change_percent` DECIMAL(8,4) NOT NULL COMMENT '涨跌幅(%)',
    `open` DECIMAL(12,4) NOT NULL COMMENT '开盘价',
    `high` DECIMAL(12,4) NOT NULL COMMENT '最高价',
    `low` DECIMAL(12,4) NOT NULL COMMENT '最低价',
    `volume` BIGINT NOT NULL COMMENT '成交量(股)',
    `amount` DECIMAL(18,2) NOT NULL COMMENT '成交额(元)',
    `turnover_rate` DECIMAL(8,4) NOT NULL COMMENT '换手率(%)',
    `pe_ratio` DECIMAL(12,4) DEFAULT NULL COMMENT '市盈率',
    `pb_ratio` DECIMAL(12,4) DEFAULT NULL COMMENT '市净率',
    `market_cap` DECIMAL(18,2) DEFAULT NULL COMMENT '市值',
    `update_time` DATETIME NOT NULL COMMENT '更新时间',
    KEY `idx_code` (`code`),
    KEY `idx_update_time` (`update_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='股票实时行情表';

-- ============================================
-- 3. 股票财务信息表
-- ============================================
CREATE TABLE `stock_financial` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    `code` VARCHAR(20) NOT NULL COMMENT '股票代码',
    `name` VARCHAR(100) NOT NULL COMMENT '股票名称',
    `eps` DECIMAL(10,4) DEFAULT NULL COMMENT '每股收益',
    `bvps` DECIMAL(10,4) DEFAULT NULL COMMENT '每股净资产',
    `roe` DECIMAL(8,4) DEFAULT NULL COMMENT '净资产收益率(%)',
    `revenue` DECIMAL(18,2) DEFAULT NULL COMMENT '营业收入(元)',
    `revenue_yoy` DECIMAL(8,4) DEFAULT NULL COMMENT '营业收入同比增长(%)',
    `net_profit` DECIMAL(18,2) DEFAULT NULL COMMENT '净利润(元)',
    `net_profit_yoy` DECIMAL(8,4) DEFAULT NULL COMMENT '净利润同比增长(%)',
    `report_date` DATE DEFAULT NULL COMMENT '报告日期',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    KEY `idx_code` (`code`),
    KEY `idx_report_date` (`report_date`),
    UNIQUE KEY `uk_code_report_date` (`code`, `report_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='股票财务信息表';

-- ============================================
-- 4. 股票资金流向表
-- ============================================
CREATE TABLE `stock_fund_flow` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    `code` VARCHAR(20) NOT NULL COMMENT '股票代码',
    `name` VARCHAR(100) NOT NULL COMMENT '股票名称',
    `trade_date` DATE NOT NULL COMMENT '交易日期',
    `close_price` DECIMAL(12,4) NOT NULL COMMENT '收盘价',
    `change_percent` DECIMAL(8,4) NOT NULL COMMENT '涨跌幅(%)',
    `main_net_inflow` DECIMAL(18,2) DEFAULT NULL COMMENT '主力净流入(元)',
    `main_net_ratio` DECIMAL(8,4) DEFAULT NULL COMMENT '主力净流入占比(%)',
    `super_net_inflow` DECIMAL(18,2) DEFAULT NULL COMMENT '超大单净流入(元)',
    `super_net_ratio` DECIMAL(8,4) DEFAULT NULL COMMENT '超大单净流入占比(%)',
    `large_net_inflow` DECIMAL(18,2) DEFAULT NULL COMMENT '大单净流入(元)',
    `large_net_ratio` DECIMAL(8,4) DEFAULT NULL COMMENT '大单净流入占比(%)',
    `medium_net_inflow` DECIMAL(18,2) DEFAULT NULL COMMENT '中单净流入(元)',
    `medium_net_ratio` DECIMAL(8,4) DEFAULT NULL COMMENT '中单净流入占比(%)',
    `small_net_inflow` DECIMAL(18,2) DEFAULT NULL COMMENT '小单净流入(元)',
    `small_net_ratio` DECIMAL(8,4) DEFAULT NULL COMMENT '小单净流入占比(%)',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    KEY `idx_code_trade_date` (`code`, `trade_date`),
    KEY `idx_trade_date` (`trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='股票资金流向表';

-- ============================================
-- 5. 概念板块表
-- ============================================
CREATE TABLE `concept_board` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    `rank` INT NOT NULL COMMENT '排名',
    `name` VARCHAR(100) NOT NULL COMMENT '板块名称',
    `code` VARCHAR(20) NOT NULL COMMENT '板块代码',
    `price` DECIMAL(12,4) NOT NULL COMMENT '最新价',
    `change` DECIMAL(12,4) NOT NULL COMMENT '涨跌额',
    `change_percent` DECIMAL(8,4) NOT NULL COMMENT '涨跌幅(%)',
    `market_value` BIGINT DEFAULT NULL COMMENT '总市值(元)',
    `turnover_rate` DECIMAL(8,4) NOT NULL COMMENT '换手率(%)',
    `up_count` INT NOT NULL DEFAULT 0 COMMENT '上涨家数',
    `down_count` INT NOT NULL DEFAULT 0 COMMENT '下跌家数',
    `leading_stock` VARCHAR(100) NOT NULL COMMENT '领涨股票',
    `leading_stock_change_percent` DECIMAL(8,4) NOT NULL COMMENT '领涨股票涨跌幅(%)',
    `update_time` DATETIME NOT NULL COMMENT '更新时间',
    UNIQUE KEY `uk_code` (`code`),
    KEY `idx_name` (`name`),
    KEY `idx_rank` (`rank`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='概念板块表';

-- ============================================
-- 6. 行业板块表
-- ============================================
CREATE TABLE `industry_board` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    `rank` INT NOT NULL COMMENT '排名',
    `name` VARCHAR(100) NOT NULL COMMENT '板块名称',
    `code` VARCHAR(20) NOT NULL COMMENT '板块代码',
    `price` DECIMAL(12,4) NOT NULL COMMENT '最新价',
    `change` DECIMAL(12,4) NOT NULL COMMENT '涨跌额',
    `change_percent` DECIMAL(8,4) NOT NULL COMMENT '涨跌幅(%)',
    `market_value` BIGINT DEFAULT NULL COMMENT '总市值(元)',
    `turnover_rate` DECIMAL(8,4) NOT NULL COMMENT '换手率(%)',
    `up_count` INT NOT NULL DEFAULT 0 COMMENT '上涨家数',
    `down_count` INT NOT NULL DEFAULT 0 COMMENT '下跌家数',
    `leading_stock` VARCHAR(100) NOT NULL COMMENT '领涨股票',
    `leading_stock_change_percent` DECIMAL(8,4) NOT NULL COMMENT '领涨股票涨跌幅(%)',
    `update_time` DATETIME NOT NULL COMMENT '更新时间',
    UNIQUE KEY `uk_code` (`code`),
    KEY `idx_name` (`name`),
    KEY `idx_rank` (`rank`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='行业板块表';

-- ============================================
-- 7. 板块实时行情表
-- ============================================
CREATE TABLE `board_spot` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    `board_code` VARCHAR(20) NOT NULL COMMENT '板块代码',
    `board_name` VARCHAR(100) NOT NULL COMMENT '板块名称',
    `price` DECIMAL(12,4) NOT NULL COMMENT '最新价',
    `high` DECIMAL(12,4) NOT NULL COMMENT '最高价',
    `low` DECIMAL(12,4) NOT NULL COMMENT '最低价',
    `open` DECIMAL(12,4) NOT NULL COMMENT '开盘价',
    `volume` DECIMAL(18,2) NOT NULL COMMENT '成交量',
    `amount` DECIMAL(18,2) NOT NULL COMMENT '成交额',
    `turnover_rate` DECIMAL(8,4) NOT NULL COMMENT '换手率(%)',
    `change` DECIMAL(12,4) NOT NULL COMMENT '涨跌额',
    `change_percent` DECIMAL(8,4) NOT NULL COMMENT '涨跌幅(%)',
    `update_time` DATETIME NOT NULL COMMENT '更新时间',
    KEY `idx_board_code` (`board_code`),
    KEY `idx_update_time` (`update_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='板块实时行情表';

-- ============================================
-- 8. 板块成份股表
-- ============================================
CREATE TABLE `board_constituents` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    `board_code` VARCHAR(20) NOT NULL COMMENT '板块代码',
    `board_name` VARCHAR(100) NOT NULL COMMENT '板块名称',
    `stock_code` VARCHAR(20) NOT NULL COMMENT '股票代码',
    `stock_name` VARCHAR(100) NOT NULL COMMENT '股票名称',
    `weight` DECIMAL(8,4) DEFAULT NULL COMMENT '权重(%)',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    KEY `idx_board_code` (`board_code`),
    KEY `idx_stock_code` (`stock_code`),
    KEY `idx_board_stock` (`board_code`, `stock_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='板块成份股表';

-- ============================================
-- 9. 融资融券明细表
-- ============================================
CREATE TABLE `margin_detail` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    `trade_date` DATE NOT NULL COMMENT '交易日期',
    `stock_code` VARCHAR(20) NOT NULL COMMENT '证券代码',
    `stock_name` VARCHAR(100) NOT NULL COMMENT '证券简称',
    `market` VARCHAR(10) NOT NULL COMMENT '市场(上海/深圳)',
    `financing_buy` BIGINT NOT NULL COMMENT '融资买入额(元)',
    `financing_balance` BIGINT NOT NULL COMMENT '融资余额(元)',
    `financing_repay` BIGINT DEFAULT NULL COMMENT '融资偿还额(元)',
    `securities_sell` BIGINT NOT NULL COMMENT '融券卖出量(股/份)',
    `securities_balance` BIGINT NOT NULL COMMENT '融券余量(股/份)',
    `securities_repay` BIGINT DEFAULT NULL COMMENT '融券偿还量(股/份)',
    `securities_balance_amount` BIGINT DEFAULT NULL COMMENT '融券余额(元)',
    `margin_balance` BIGINT DEFAULT NULL COMMENT '融资融券余额(元)',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    KEY `idx_trade_date_stock_code` (`trade_date`, `stock_code`),
    KEY `idx_stock_code` (`stock_code`),
    UNIQUE KEY `uk_trade_date_stock_code` (`trade_date`, `stock_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='融资融券明细表';

-- ============================================
-- 10. 股票热度排名表
-- ============================================
CREATE TABLE `stock_hot_rank` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    `rank` INT NOT NULL COMMENT '当前排名',
    `stock_code` VARCHAR(20) NOT NULL COMMENT '股票代码',
    `stock_name` VARCHAR(100) NOT NULL COMMENT '股票名称',
    `price` DECIMAL(12,4) NOT NULL COMMENT '最新价',
    `change` DECIMAL(12,4) NOT NULL COMMENT '涨跌额',
    `change_percent` DECIMAL(8,4) NOT NULL COMMENT '涨跌幅(%)',
    `update_time` DATETIME NOT NULL COMMENT '更新时间',
    KEY `idx_rank` (`rank`),
    KEY `idx_stock_code` (`stock_code`),
    KEY `idx_update_time` (`update_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='股票热度排名表';

-- ============================================
-- 11. 股票飙升榜表
-- ============================================
CREATE TABLE `stock_hot_up_rank` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    `rank_change` INT NOT NULL COMMENT '排名较昨日变动',
    `rank` INT NOT NULL COMMENT '当前排名',
    `stock_code` VARCHAR(20) NOT NULL COMMENT '股票代码',
    `stock_name` VARCHAR(100) NOT NULL COMMENT '股票名称',
    `price` DECIMAL(12,4) NOT NULL COMMENT '最新价',
    `change` DECIMAL(12,4) NOT NULL COMMENT '涨跌额',
    `change_percent` DECIMAL(8,4) NOT NULL COMMENT '涨跌幅(%)',
    `update_time` DATETIME NOT NULL COMMENT '更新时间',
    KEY `idx_rank` (`rank`),
    KEY `idx_stock_code` (`stock_code`),
    KEY `idx_update_time` (`update_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='股票飙升榜表';

-- ============================================
-- 12. 股票热门关键词表
-- ============================================
CREATE TABLE `stock_hot_keyword` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    `time` DATETIME NOT NULL COMMENT '时间',
    `stock_code` VARCHAR(20) NOT NULL COMMENT '股票代码',
    `concept_name` VARCHAR(100) NOT NULL COMMENT '概念名称',
    `concept_code` VARCHAR(20) NOT NULL COMMENT '概念代码',
    `heat` INT NOT NULL COMMENT '热度',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    KEY `idx_stock_code_time` (`stock_code`, `time`),
    KEY `idx_concept_code` (`concept_code`),
    KEY `idx_heat` (`heat`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='股票热门关键词表';

-- ============================================
-- 13. 全球财经快讯表
-- ============================================
CREATE TABLE `global_finance_news` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    `title` VARCHAR(500) NOT NULL COMMENT '标题',
    `summary` TEXT NOT NULL COMMENT '摘要',
    `publish_time` VARCHAR(50) NOT NULL COMMENT '发布时间',
    `link` VARCHAR(500) NOT NULL COMMENT '链接',
    `update_time` DATETIME NOT NULL COMMENT '更新时间',
    KEY `idx_publish_time` (`publish_time`),
    FULLTEXT KEY `ft_title` (`title`),
    FULLTEXT KEY `ft_summary` (`summary`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='全球财经快讯表';

-- ============================================
-- 14. 互动易提问表
-- ============================================
CREATE TABLE `interactive_question` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    `stock_code` VARCHAR(20) NOT NULL COMMENT '股票代码',
    `stock_name` VARCHAR(100) NOT NULL COMMENT '公司简称',
    `industry` VARCHAR(100) DEFAULT NULL COMMENT '行业',
    `industry_code` VARCHAR(20) DEFAULT NULL COMMENT '行业代码',
    `question` TEXT NOT NULL COMMENT '问题',
    `questioner` VARCHAR(100) NOT NULL COMMENT '提问者',
    `source` VARCHAR(100) NOT NULL COMMENT '来源',
    `question_time` DATETIME NOT NULL COMMENT '提问时间',
    `update_time` DATETIME NOT NULL COMMENT '更新时间',
    `questioner_id` VARCHAR(50) DEFAULT NULL COMMENT '提问者编号',
    `question_id` VARCHAR(50) DEFAULT NULL COMMENT '问题编号',
    `answer_id` VARCHAR(50) DEFAULT NULL COMMENT '回答ID',
    `answer_content` TEXT DEFAULT NULL COMMENT '回答内容',
    `answerer` VARCHAR(100) DEFAULT NULL COMMENT '回答者',
    KEY `idx_stock_code` (`stock_code`),
    KEY `idx_question_time` (`question_time`),
    FULLTEXT KEY `ft_question` (`question`),
    FULLTEXT KEY `ft_answer` (`answer_content`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='互动易提问表';

-- ============================================
-- 15. 财联社电报表
-- ============================================
CREATE TABLE `cls_telegraph` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    `title` VARCHAR(500) NOT NULL COMMENT '标题',
    `content` TEXT NOT NULL COMMENT '内容',
    `publish_date` VARCHAR(20) NOT NULL COMMENT '发布日期',
    `publish_time` VARCHAR(20) NOT NULL COMMENT '发布时间',
    `update_time` DATETIME NOT NULL COMMENT '更新时间',
    KEY `idx_publish_date` (`publish_date`),
    FULLTEXT KEY `ft_title` (`title`),
    FULLTEXT KEY `ft_content` (`content`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='财联社电报表';

-- ============================================
-- 16. 指数实时行情表
-- ============================================
CREATE TABLE `index_quote` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    `code` VARCHAR(20) NOT NULL COMMENT '指数代码',
    `name` VARCHAR(100) NOT NULL COMMENT '指数名称',
    `price` DECIMAL(12,4) NOT NULL COMMENT '最新价',
    `change` DECIMAL(12,4) NOT NULL COMMENT '涨跌额',
    `change_percent` DECIMAL(8,4) NOT NULL COMMENT '涨跌幅(%)',
    `volume` DECIMAL(18,2) DEFAULT NULL COMMENT '成交量',
    `amount` DECIMAL(18,2) DEFAULT NULL COMMENT '成交额',
    `amplitude` DECIMAL(8,4) DEFAULT NULL COMMENT '振幅(%)',
    `high` DECIMAL(12,4) DEFAULT NULL COMMENT '最高价',
    `low` DECIMAL(12,4) DEFAULT NULL COMMENT '最低价',
    `open` DECIMAL(12,4) DEFAULT NULL COMMENT '今开',
    `pre_close` DECIMAL(12,4) DEFAULT NULL COMMENT '昨收',
    `volume_ratio` DECIMAL(8,4) DEFAULT NULL COMMENT '量比',
    `update_time` DATETIME NOT NULL COMMENT '更新时间',
    KEY `idx_code` (`code`),
    KEY `idx_update_time` (`update_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='指数实时行情表';

-- ============================================
-- 17. 筹码分布表
-- ============================================
CREATE TABLE `chip_distribution` (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    `stock_code` VARCHAR(20) NOT NULL COMMENT '股票代码',
    `full_code` VARCHAR(20) NOT NULL COMMENT '股票代码',
    `stock_name` VARCHAR(50) DEFAULT NULL COMMENT '股票名称',
    `trade_date` DATE NOT NULL COMMENT '交易日期',
    `profit_ratio` DECIMAL(8,4) NOT NULL COMMENT '获利比例(%)',
    `avg_cost` DECIMAL(12,4) NOT NULL COMMENT '平均成本',
    `cost_90_low` DECIMAL(12,4) NOT NULL COMMENT '90成本-低',
    `cost_90_high` DECIMAL(12,4) NOT NULL COMMENT '90成本-高',
    `concentration_90` DECIMAL(8,4) NOT NULL COMMENT '90集中度(%)',
    `cost_70_low` DECIMAL(12,4) NOT NULL COMMENT '70成本-低',
    `cost_70_high` DECIMAL(12,4) NOT NULL COMMENT '70成本-高',
    `concentration_70` DECIMAL(8,4) NOT NULL COMMENT '70集中度(%)',
    `data_time` DATETIME DEFAULT NULL COMMENT '数据时间（采集时间）',
    `data_from` VARCHAR(50) DEFAULT 'akshare' COMMENT '数据来源：akshare',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    UNIQUE KEY `uk_stock_code_trade_date` (`stock_code`, `trade_date`),
    KEY `idx_stock_code` (`stock_code`),
    KEY `idx_trade_date` (`trade_date`),
    KEY `idx_profit_ratio` (`profit_ratio`),
    KEY `idx_avg_cost` (`avg_cost`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='筹码分布表';

-- ============================================
-- 索引优化建议
-- ============================================
-- 1. 定期分析表：ANALYZE TABLE table_name;
-- 2. 定期优化表：OPTIMIZE TABLE table_name;
-- 3. 根据查询需求调整索引
-- 4. 考虑分区表（如按日期分区）

-- ============================================
-- 字符集说明
-- ============================================
-- utf8mb4：支持完整的UTF-8字符集，包括emoji
-- utf8mb4_unicode_ci：基于Unicode的排序规则，支持多语言

-- ============================================
-- 引擎说明
-- ============================================
-- InnoDB：支持事务、外键、行级锁
-- 适合高并发、数据一致性要求高的场景
