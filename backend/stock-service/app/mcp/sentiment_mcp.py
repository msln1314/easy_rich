from typing import Dict, List, Optional
from app.core.logging import get_logger
from app.services.sentiment_service import SentimentService

logger = get_logger(__name__)

class SentimentMCP:
    """
    市场情绪MCP接口
    
    本类提供了与市场情绪相关的数据查询接口，包括融资融券、股票热度等。
    所有接口通过调用服务层实现，共享服务层的数据处理和缓存机制。
    
    使用示例:
        sentiment_mcp = SentimentMCP()
        margin_details = sentiment_mcp.get_margin_details("20230922")
        hot_ranks = sentiment_mcp.get_stock_hot_rank()
    """
    
    def __init__(self):
        """初始化SentimentMCP，创建服务实例"""
        self.sentiment_service = SentimentService()
    
    async def get_margin_details(self, trade_date: str) -> List[Dict]:
        """
        获取融资融券明细数据（上海和深圳市场合并）
        
        Args:
            trade_date: 交易日期，格式为"YYYYMMDD"，如"20230922"
            
        Returns:
            List[Dict]: 融资融券明细数据列表
        """
        logger.info(f"MCP获取融资融券明细数据: {trade_date}")
        try:
            # 调用服务层获取数据
            details = await self.sentiment_service.get_margin_details(trade_date)
            
            # 将Pydantic模型列表转换为字典列表
            return [detail.model_dump() for detail in details]
        except Exception as e:
            logger.error(f"获取融资融券明细数据失败: {str(e)}")
            raise Exception(f"获取融资融券明细数据失败: {str(e)}")
    
    async def get_stock_hot_rank(self) -> List[Dict]:
        """
        获取股票热度排名数据
        
        Returns:
            List[Dict]: 股票热度排名数据列表
        """
        logger.info("MCP获取股票热度排名数据")
        try:
            # 调用服务层获取数据
            hot_ranks = await self.sentiment_service.get_stock_hot_rank()
            
            # 将Pydantic模型列表转换为字典列表
            return [rank.model_dump() for rank in hot_ranks]
        except Exception as e:
            logger.error(f"获取股票热度排名数据失败: {str(e)}")
            raise Exception(f"获取股票热度排名数据失败: {str(e)}")
    
    async def get_stock_hot_up_rank(self) -> List[Dict]:
        """
        获取股票飙升榜数据
        
        Returns:
            List[Dict]: 股票飙升榜数据列表
        """
        logger.info("MCP获取股票飙升榜数据")
        try:
            # 调用服务层获取数据
            hot_up_ranks = await self.sentiment_service.get_stock_hot_up_rank()
            
            # 将Pydantic模型列表转换为字典列表
            return [rank.model_dump() for rank in hot_up_ranks]
        except Exception as e:
            logger.error(f"获取股票飙升榜数据失败: {str(e)}")
            raise Exception(f"获取股票飙升榜数据失败: {str(e)}")
    
    async def get_stock_hot_keywords(self, symbol: str) -> List[Dict]:
        """
        获取股票热门关键词数据
        
        Args:
            symbol: 股票代码，如"SZ000665"
            
        Returns:
            List[Dict]: 股票热门关键词数据列表
        """
        logger.info(f"MCP获取股票热门关键词数据: {symbol}")
        try:
            # 调用服务层获取数据
            keywords = await self.sentiment_service.get_stock_hot_keywords(symbol)
            
            # 将Pydantic模型列表转换为字典列表
            return [keyword.model_dump() for keyword in keywords]
        except Exception as e:
            logger.error(f"获取股票热门关键词数据失败: {str(e)}")
            raise Exception(f"获取股票热门关键词数据失败: {str(e)}")