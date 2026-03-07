from typing import Dict, List, Optional
from app.core.logging import get_logger
from app.services.index_service import IndexService

logger = get_logger(__name__)

class IndexMCP:
    """
    指数信息MCP接口
    
    本类提供了与指数相关的数据查询接口，包括实时行情等。
    所有接口通过调用服务层实现，共享服务层的数据处理和缓存机制。
    
    使用示例:
        index_mcp = IndexMCP()
        index_quotes = index_mcp.get_index_quotes("沪深重要指数")
    """
    
    def __init__(self):
        """初始化IndexMCP，创建服务实例"""
        self.index_service = IndexService()
    
    async def get_index_quotes(self, symbol: str = "沪深重要指数") -> List[Dict]:
        """
        获取指数实时行情列表
        
        Args:
            symbol: 指数类型，可选值：
                   "沪深重要指数", "上证系列指数", "深证系列指数", "指数成份", "中证系列指数"
                   
        Returns:
            List[Dict]: 指数实时行情数据列表
        """
        logger.info(f"MCP获取指数实时行情列表: {symbol}")
        try:
            # 调用服务层获取数据
            index_quotes = await self.index_service.get_index_quotes(symbol)
            
            # 将Pydantic模型列表转换为字典列表
            return [quote.model_dump() for quote in index_quotes]
        except Exception as e:
            logger.error(f"获取指数行情列表失败: {str(e)}")
            raise Exception(f"获取指数行情列表失败: {str(e)}")
    
    async def get_index_quote(self, index_code: str) -> Optional[Dict]:
        """
        获取单个指数的实时行情数据
        
        Args:
            index_code: 指数代码，如"000001"（上证指数）
            
        Returns:
            Optional[Dict]: 指数实时行情数据，如果未找到则返回None
        """
        logger.info(f"MCP获取单个指数实时行情: {index_code}")
        try:
            # 调用服务层获取数据
            index_quote = await self.index_service.get_index_quote(index_code)
            
            # 如果未找到指数，返回None
            if index_quote is None:
                return None
            
            # 将Pydantic模型转换为字典
            return index_quote.model_dump()  # Changed from .dict() to .model_dump()
        except Exception as e:
            logger.error(f"获取指数行情失败: {str(e)}")
            raise Exception(f"获取指数行情失败: {str(e)}")