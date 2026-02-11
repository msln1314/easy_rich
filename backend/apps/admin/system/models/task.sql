-- 定时任务调度表
CREATE TABLE `sys_task` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `name` VARCHAR(64) DEFAULT '' NULL COMMENT '任务名称',
  `jobstore` VARCHAR(64) DEFAULT 'default' NULL COMMENT '存储器',
  `executor` VARCHAR(64) DEFAULT 'default' NULL COMMENT '执行器:将运行此作业的执行程序的名称',
  `trigger` VARCHAR(64) NOT NULL COMMENT '触发器:控制此作业计划的 trigger 对象',
  `trigger_args` TEXT NULL COMMENT '触发器参数',
  `func` TEXT NOT NULL COMMENT '任务函数',
  `args` TEXT NULL COMMENT '位置参数',
  `kwargs` TEXT NULL COMMENT '关键字参数',
  `coalesce` TINYINT(1) DEFAULT 0 NULL COMMENT '是否合并运行:是否在多个运行时间到期时仅运行作业一次',
  `max_instances` INT DEFAULT 1 NULL COMMENT '最大实例数:允许的最大并发执行实例数 工作',
  `start_date` VARCHAR(64) NULL COMMENT '开始时间',
  `end_date` VARCHAR(64) NULL COMMENT '结束时间',
  `status` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否启用(True:启用 False:禁用)',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `delete_datetime` DATETIME NULL COMMENT '删除时间',
  `is_delete` TINYINT(1) DEFAULT 0 COMMENT '是否软删除',
  PRIMARY KEY (`id`),
  INDEX `idx_created_at` (`created_at`),
  INDEX `idx_updated_at` (`updated_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='定时任务调度表';


-- 定时任务调度日志表
CREATE TABLE `sys_task_log` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `job_name` VARCHAR(64) NOT NULL COMMENT '任务名称',
  `job_group` VARCHAR(64) NOT NULL COMMENT '任务组名',
  `job_executor` VARCHAR(64) NOT NULL COMMENT '任务执行器',
  `invoke_target` VARCHAR(500) NOT NULL COMMENT '调用目标字符串',
  `job_args` VARCHAR(255) DEFAULT '' NULL COMMENT '位置参数',
  `job_kwargs` VARCHAR(255) DEFAULT '' NULL COMMENT '关键字参数',
  `job_trigger` VARCHAR(255) DEFAULT '' NULL COMMENT '任务触发器',
  `job_message` VARCHAR(500) DEFAULT '' NULL COMMENT '日志信息',
  `exception_info` VARCHAR(2000) DEFAULT '' NULL COMMENT '异常信息',
  `job_id` INT NULL COMMENT '任务ID',
  `status` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否启用(True:启用 False:禁用)',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `delete_datetime` DATETIME NULL COMMENT '删除时间',
  `is_delete` TINYINT(1) DEFAULT 0 COMMENT '是否软删除',
  PRIMARY KEY (`id`),
  INDEX `idx_created_at` (`created_at`),
  INDEX `idx_updated_at` (`updated_at`),
  INDEX `idx_job_id` (`job_id`),
  CONSTRAINT `fk_task_log_task_id` FOREIGN KEY (`job_id`) REFERENCES `sys_task` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='定时任务调度日志表';
