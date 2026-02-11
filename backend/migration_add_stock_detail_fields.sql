-- 为 stock_basic_info 表添加实时行情字段和基础字段
-- 执行时间: 2025-01-27

-- 添加基础字段（如果不存在）
ALTER TABLE `stock_basic_info` ADD COLUMN `sector` VARCHAR(50) DEFAULT NULL COMMENT '板块:主板，科创板，创业板' AFTER `industry`;
ALTER TABLE `stock_basic_info` ADD COLUMN `total_shares` DECIMAL(20, 2) DEFAULT NULL COMMENT 'A股总股本' AFTER `list_date`;
ALTER TABLE `stock_basic_info` ADD COLUMN `circulating_shares` DECIMAL(20, 2) DEFAULT NULL COMMENT 'A股流通股本' AFTER `total_shares`;

-- 添加实时行情字段
ALTER TABLE `stock_basic_info` ADD COLUMN `current_price` DECIMAL(20, 4) DEFAULT NULL COMMENT '最新价' AFTER `trade_status`;
ALTER TABLE `stock_basic_info` ADD COLUMN `change_percent` DECIMAL(10, 4) DEFAULT NULL COMMENT '涨跌幅(%)' AFTER `current_price`;
ALTER TABLE `stock_basic_info` ADD COLUMN `change_amount` DECIMAL(20, 4) DEFAULT NULL COMMENT '涨跌额' AFTER `change_percent`;
ALTER TABLE `stock_basic_info` ADD COLUMN `volume` DECIMAL(20, 2) DEFAULT NULL COMMENT '成交量(手)' AFTER `change_amount`;
ALTER TABLE `stock_basic_info` ADD COLUMN `amount` DECIMAL(20, 2) DEFAULT NULL COMMENT '成交额(元)' AFTER `volume`;
ALTER TABLE `stock_basic_info` ADD COLUMN `amplitude` DECIMAL(10, 4) DEFAULT NULL COMMENT '振幅(%)' AFTER `amount`;
ALTER TABLE `stock_basic_info` ADD COLUMN `high_price` DECIMAL(20, 4) DEFAULT NULL COMMENT '最高价' AFTER `amplitude`;
ALTER TABLE `stock_basic_info` ADD COLUMN `low_price` DECIMAL(20, 4) DEFAULT NULL COMMENT '最低价' AFTER `high_price`;
ALTER TABLE `stock_basic_info` ADD COLUMN `open_price` DECIMAL(20, 4) DEFAULT NULL COMMENT '今开' AFTER `low_price`;
ALTER TABLE `stock_basic_info` ADD COLUMN `close_price` DECIMAL(20, 4) DEFAULT NULL COMMENT '昨收' AFTER `open_price`;
ALTER TABLE `stock_basic_info` ADD COLUMN `volume_ratio` DECIMAL(10, 4) DEFAULT NULL COMMENT '量比' AFTER `close_price`;
ALTER TABLE `stock_basic_info` ADD COLUMN `turnover_rate` DECIMAL(10, 4) DEFAULT NULL COMMENT '换手率(%)' AFTER `volume_ratio`;
ALTER TABLE `stock_basic_info` ADD COLUMN `pe_ratio` DECIMAL(20, 4) DEFAULT NULL COMMENT '市盈率-动态' AFTER `turnover_rate`;
ALTER TABLE `stock_basic_info` ADD COLUMN `pb_ratio` DECIMAL(20, 4) DEFAULT NULL COMMENT '市净率' AFTER `pe_ratio`;
ALTER TABLE `stock_basic_info` ADD COLUMN `total_market_cap` DECIMAL(20, 2) DEFAULT NULL COMMENT '总市值(元)' AFTER `pb_ratio`;
ALTER TABLE `stock_basic_info` ADD COLUMN `circulating_market_cap` DECIMAL(20, 2) DEFAULT NULL COMMENT '流通市值(元)' AFTER `total_market_cap`;
ALTER TABLE `stock_basic_info` ADD COLUMN `change_speed` DECIMAL(10, 4) DEFAULT NULL COMMENT '涨速' AFTER `circulating_market_cap`;
ALTER TABLE `stock_basic_info` ADD COLUMN `change_5min` DECIMAL(10, 4) DEFAULT NULL COMMENT '5分钟涨跌(%)' AFTER `change_speed`;
ALTER TABLE `stock_basic_info` ADD COLUMN `change_60day` DECIMAL(10, 4) DEFAULT NULL COMMENT '60日涨跌幅(%)' AFTER `change_5min`;
ALTER TABLE `stock_basic_info` ADD COLUMN `change_ytd` DECIMAL(10, 4) DEFAULT NULL COMMENT '年初至今涨跌幅(%)' AFTER `change_60day';
