-- 通知渠道配置表
CREATE TABLE IF NOT EXISTS `notification_channel` (
    `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    `user_id` INT NOT NULL COMMENT '用户ID',
    `channel_type` VARCHAR(20) NOT NULL COMMENT '渠道类型: email/wechat/system',
    `channel_name` VARCHAR(100) NOT NULL COMMENT '渠道名称',
    `channel_config` TEXT COMMENT '渠道配置JSON',
    `is_enabled` TINYINT(1) DEFAULT 1 COMMENT '是否启用',
    `verified` TINYINT(1) DEFAULT 0 COMMENT '是否已验证',
    `verify_code` VARCHAR(20) COMMENT '验证码',
    `verified_at` DATETIME COMMENT '验证时间',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `delete_datetime` DATETIME COMMENT '删除时间',
    `is_delete` TINYINT(1) DEFAULT 0 COMMENT '是否软删除',
    INDEX `idx_user_channel` (`user_id`, `channel_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='通知渠道配置表';

-- 通知模板表
CREATE TABLE IF NOT EXISTS `notification_template` (
    `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    `name` VARCHAR(100) NOT NULL COMMENT '模板名称',
    `code` VARCHAR(50) NOT NULL UNIQUE COMMENT '模板编码',
    `title_template` VARCHAR(200) NOT NULL COMMENT '标题模板',
    `content_template` TEXT NOT NULL COMMENT '内容模板',
    `channel_types` TEXT COMMENT '支持的渠道类型JSON',
    `is_system` TINYINT(1) DEFAULT 0 COMMENT '是否系统内置',
    `description` VARCHAR(500) COMMENT '模板描述',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `delete_datetime` DATETIME COMMENT '删除时间',
    `is_delete` TINYINT(1) DEFAULT 0 COMMENT '是否软删除'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='通知模板表';

-- 通知日志表
CREATE TABLE IF NOT EXISTS `notification_log` (
    `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    `user_id` INT NOT NULL COMMENT '用户ID',
    `channel_type` VARCHAR(20) NOT NULL COMMENT '渠道类型',
    `template_code` VARCHAR(50) COMMENT '使用的模板编码',
    `title` VARCHAR(200) NOT NULL COMMENT '通知标题',
    `content` TEXT NOT NULL COMMENT '通知内容',
    `status` VARCHAR(20) DEFAULT 'pending' COMMENT '状态: pending/sent/failed',
    `error_msg` TEXT COMMENT '错误信息',
    `sent_at` DATETIME COMMENT '发送时间',
    `extra_data` TEXT COMMENT '额外数据JSON',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `delete_datetime` DATETIME COMMENT '删除时间',
    `is_delete` TINYINT(1) DEFAULT 0 COMMENT '是否软删除',
    INDEX `idx_user_status` (`user_id`, `status`),
    INDEX `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='通知日志表';

-- 系统通知表
CREATE TABLE IF NOT EXISTS `system_notification` (
    `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    `user_id` INT NOT NULL COMMENT '用户ID',
    `title` VARCHAR(200) NOT NULL COMMENT '通知标题',
    `content` TEXT NOT NULL COMMENT '通知内容',
    `notification_type` VARCHAR(50) DEFAULT 'info' COMMENT '通知类型: info/warning/success/error',
    `is_read` TINYINT(1) DEFAULT 0 COMMENT '是否已读',
    `read_at` DATETIME COMMENT '阅读时间',
    `link` VARCHAR(500) COMMENT '跳转链接',
    `extra_data` TEXT COMMENT '额外数据JSON',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `delete_datetime` DATETIME COMMENT '删除时间',
    `is_delete` TINYINT(1) DEFAULT 0 COMMENT '是否软删除',
    INDEX `idx_user_read` (`user_id`, `is_read`),
    INDEX `idx_user_created` (`user_id`, `created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='系统通知表';

-- 股票通知规则表
CREATE TABLE IF NOT EXISTS `stock_notification_rule` (
    `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    `user_id` INT NOT NULL COMMENT '用户ID',
    `rule_name` VARCHAR(100) NOT NULL COMMENT '规则名称',
    `rule_type` VARCHAR(50) NOT NULL COMMENT '规则类型: holiday/earnings/dividend/unlock/custom',
    `event_type_filter` VARCHAR(100) COMMENT '事件类型过滤',
    `stock_codes` TEXT COMMENT '股票代码列表JSON',
    `condition_config` TEXT COMMENT '条件配置JSON',
    `action_config` TEXT COMMENT '动作配置JSON',
    `priority` INT DEFAULT 0 COMMENT '优先级',
    `is_enabled` TINYINT(1) DEFAULT 1 COMMENT '是否启用',
    `valid_from` DATE COMMENT '有效期开始',
    `valid_to` DATE COMMENT '有效期结束',
    `last_triggered_at` VARCHAR(30) COMMENT '上次触发时间',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `delete_datetime` DATETIME COMMENT '删除时间',
    `is_delete` TINYINT(1) DEFAULT 0 COMMENT '是否软删除',
    INDEX `idx_user_enabled` (`user_id`, `is_enabled`),
    INDEX `idx_rule_type` (`rule_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='股票通知规则表';

-- 插入默认通知模板
INSERT INTO `notification_template` (`name`, `code`, `title_template`, `content_template`, `channel_types`, `is_system`, `description`) VALUES
('节假日提醒', 'holiday_reminder', '节假日提醒', '尊敬的用户，{{message}}\n\n事件详情：\n{{event_list}}', '["email", "wechat", "system"]', 1, '节假日相关提醒模板'),
('财报提醒', 'earnings_reminder', '财报发布提醒', '尊敬的用户，以下股票即将发布财报：\n\n{{event_list}}\n\n请关注相关公告。', '["email", "wechat", "system"]', 1, '财报发布提醒模板'),
('解禁提醒', 'unlock_reminder', '股票解禁提醒', '尊敬的用户，以下股票即将解禁：\n\n{{event_list}}\n\n请注意风险。', '["email", "wechat", "system"]', 1, '股票解禁提醒模板'),
('分红提醒', 'dividend_reminder', '分红除权提醒', '尊敬的用户，以下股票即将分红除权：\n\n{{event_list}}\n\n请注意股权登记日。', '["email", "wechat", "system"]', 1, '分红除权提醒模板');