import sys
from loguru import logger
from app.core.config import settings

def setup_logging():
    """
    设置日志配置
    默认只启用控制台日志，文件日志暂不开启
    使用loguru实现彩色日志输出
    """
    # 移除默认的处理器
    logger.remove()
    
    # 获取配置中的日志级别，默认为INFO
    log_level = settings.LOG_LEVEL.upper()
    
    # 添加控制台处理器
    logger.add(
        sys.stdout,
        colorize=True,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=log_level,
        backtrace=True,  # 显示异常的完整堆栈跟踪
        diagnose=True,   # 显示变量值等诊断信息
    )
    
    # 文件日志暂不开启
    # logger.add(
    #     "logs/app.log",
    #     rotation="10 MB",  # 日志文件达到10MB时轮转
    #     retention="10 days",  # 保留10天的日志
    #     compression="zip",  # 压缩轮转的日志
    #     level=log_level,
    #     format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{line} - {message}",
    # )
    
    # 设置第三方库的日志级别
    import logging
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
    logging.getLogger("fastapi").setLevel(logging.INFO)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)
    
    logger.info("日志系统初始化完成")

def get_logger(name):
    """
    获取带有上下文信息的logger
    
    Args:
        name: 模块名称
        
    Returns:
        loguru.logger: 带有上下文信息的logger
    """
    return logger.bind(name=name)