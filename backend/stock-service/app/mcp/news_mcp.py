import logging
from typing import List, Dict
from app.services.news_service import NewsService
from app.core.logging import get_logger

logger = get_logger(__name__)

class NewsMCP:
    """
    资讯MCP接口
    
    本类提供了与资讯相关的数据查询接口，包括互动易提问、全球财经快讯等。
    所有接口通过调用服务层实现，共享服务层的数据处理和缓存机制。
    
    使用示例:
        news_mcp = NewsMCP()
        interactive_questions = news_mcp.get_interactive_questions("002594")
        global_finance_news = news_mcp.get_global_finance_news()
    """
    
    def __init__(self):
        """初始化NewsMCP，创建服务实例"""
        self.news_service = NewsService()
    
    async def get_interactive_questions(self, symbol: str) -> List[Dict]:
        """
        获取互动易提问数据
        
        Args:
            symbol: 股票代码，如"002594"
            
        Returns:
            List[Dict]: 互动易提问数据列表
        """
        logger.info(f"MCP获取互动易提问数据: {symbol}")
        try:
            # 调用服务层获取数据
            questions = await self.news_service.get_interactive_questions(symbol)
            
            # 将Pydantic模型列表转换为字典列表
            return [question.model_dump() for question in questions]
        except Exception as e:
            logger.error(f"获取互动易提问数据失败: {str(e)}")
            raise Exception(f"获取互动易提问数据失败: {str(e)}")
    
    async def get_cls_telegraph(self, symbol: str = "全部") -> List[Dict]:
        """
        获取财联社电报数据
        
        Args:
            symbol: 类型，可选值为"全部"或"重点"，默认为"全部"
            
        Returns:
            List[Dict]: 财联社电报数据列表
        """
        logger.info(f"MCP获取财联社电报数据: {symbol}")
        try:
            # 调用服务层获取数据
            telegraphs = await self.news_service.get_cls_telegraph(symbol)
            
            # 将Pydantic模型列表转换为字典列表
            return [telegraph.model_dump() for telegraph in telegraphs]
        except Exception as e:
            logger.error(f"获取财联社电报数据失败: {str(e)}")
            raise Exception(f"获取财联社电报数据失败: {str(e)}")
    
    async def get_global_finance_news(self) -> List[Dict]:
        """
        获取全球财经快讯数据

        Returns:
            List[Dict]: 全球财经快讯数据列表
        """
        logger.info("MCP获取全球财经快讯数据")
        try:
            # 调用服务层获取数据
            news_list = await self.news_service.get_global_finance_news()

            # 将Pydantic模型列表转换为字典列表
            return [news.model_dump() for news in news_list]
        except Exception as e:
            logger.error(f"获取全球财经快讯数据失败: {str(e)}")
            raise Exception(f"获取全球财经快讯数据失败: {str(e)}")