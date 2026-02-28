import logging

# 将日志处理器配置权交给主程序（如 stock_analyze.main）统一设置。
# 这里仅提供一个共享的根日志记录器引用，避免在模块导入阶段添加额外的处理器，
# 以防止控制台出现重复输出或级别过滤不一致的问题。
logger = logging.getLogger()