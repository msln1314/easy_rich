from typing import Dict, List, Optional
from app.core.logging import get_logger
from app.services.sector_service import SectorService

logger = get_logger(__name__)

class SectorMCP:
    """
    板块信息MCP接口
    
    本类提供了与板块相关的数据查询接口，包括概念板块和行业板块等。
    所有接口通过调用服务层实现，共享服务层的数据处理和缓存机制。
    
    使用示例:
        sector_mcp = SectorMCP()
        concept_boards = sector_mcp.get_concept_boards()
        industry_boards = sector_mcp.get_industry_boards()
    """
    
    def __init__(self):
        """初始化SectorMCP，创建服务实例"""
        self.sector_service = SectorService()
    
    async def get_concept_boards(self) -> List[Dict]:
        """
        获取概念板块列表及实时行情
        
        Returns:
            List[Dict]: 概念板块列表
        """
        logger.info("MCP获取概念板块列表")
        try:
            # 调用服务层获取数据
            boards = await self.sector_service.get_concept_boards()
            
            # 将Pydantic模型列表转换为字典列表
            return [board.model_dump() for board in boards]
        except Exception as e:
            logger.error(f"获取概念板块列表失败: {str(e)}")
            raise Exception(f"获取概念板块列表失败: {str(e)}")
    
    async def get_concept_board(self, board_code: str) -> Optional[Dict]:
        """
        获取单个概念板块的实时行情
        
        Args:
            board_code: 板块代码，如"BK0892"
            
        Returns:
            Optional[Dict]: 概念板块数据，如果未找到则返回None
        """
        logger.info(f"MCP获取单个概念板块: {board_code}")
        try:
            # 调用服务层获取数据
            board = await self.sector_service.get_concept_board(board_code)
            
            # 如果未找到板块，返回None
            if board is None:
                return None
            
            # 将Pydantic模型转换为字典
            return board.model_dump()
        except Exception as e:
            logger.error(f"获取概念板块失败: {str(e)}")
            raise Exception(f"获取概念板块失败: {str(e)}")
    
    async def get_concept_board_spot(self, name: str) -> Optional[Dict]:
        """
        获取概念板块实时行情详情（通过名称）
        
        Args:
            name: 板块名称，如"可燃冰"
            
        Returns:
            Optional[Dict]: 概念板块实时行情详情，如果未找到则返回None
        """
        logger.info(f"MCP获取概念板块实时行情详情: {name}")
        try:
            # 调用服务层获取数据
            spot = await self.sector_service.get_concept_board_spot(name)
            
            # 如果未找到板块，返回None
            if spot is None:
                return None
            
            # 将Pydantic模型转换为字典
            return spot.model_dump()
        except Exception as e:
            logger.error(f"获取概念板块实时行情详情失败: {str(e)}")
            raise Exception(f"获取概念板块实时行情详情失败: {str(e)}")
    
    async def get_concept_board_spot_by_code(self, board_code: str) -> Optional[Dict]:
        """
        获取概念板块实时行情详情（通过代码）
        
        Args:
            board_code: 板块代码，如"BK0818"
            
        Returns:
            Optional[Dict]: 概念板块实时行情详情，如果未找到则返回None
        """
        logger.info(f"MCP通过代码获取概念板块实时行情详情: {board_code}")
        try:
            # 调用服务层获取数据
            spot = await self.sector_service.get_concept_board_spot_by_code(board_code)
            
            # 如果未找到板块，返回None
            if spot is None:
                return None
            
            # 将Pydantic模型转换为字典
            return spot.model_dump()
        except Exception as e:
            logger.error(f"通过代码获取概念板块实时行情详情失败: {str(e)}")
            raise Exception(f"通过代码获取概念板块实时行情详情失败: {str(e)}")
    
    async def get_concept_board_constituents(self, symbol: str) -> List[Dict]:
        """
        获取概念板块成份股
        
        Args:
            symbol: 板块名称或代码，如"融资融券"或"BK0655"
            
        Returns:
            List[Dict]: 概念板块成份股列表
        """
        logger.info(f"MCP获取概念板块成份股: {symbol}")
        try:
            # 调用服务层获取数据
            constituents = await self.sector_service.get_concept_board_constituents(symbol)
            
            # 将Pydantic模型列表转换为字典列表
            return [constituent.model_dump() for constituent in constituents]
        except Exception as e:
            logger.error(f"获取概念板块成份股失败: {str(e)}")
            raise Exception(f"获取概念板块成份股失败: {str(e)}")
    
    async def get_industry_boards(self) -> List[Dict]:
        """
        获取行业板块列表及实时行情
        
        Returns:
            List[Dict]: 行业板块列表
        """
        logger.info("MCP获取行业板块列表")
        try:
            # 调用服务层获取数据
            boards = await self.sector_service.get_industry_boards()
            
            # 将Pydantic模型列表转换为字典列表
            return [board.model_dump() for board in boards]
        except Exception as e:
            logger.error(f"获取行业板块列表失败: {str(e)}")
            raise Exception(f"获取行业板块列表失败: {str(e)}")
    
    async def get_industry_board(self, board_code: str) -> Optional[Dict]:
        """
        获取单个行业板块的实时行情
        
        Args:
            board_code: 板块代码，如"BK0437"
            
        Returns:
            Optional[Dict]: 行业板块数据，如果未找到则返回None
        """
        logger.info(f"MCP获取单个行业板块: {board_code}")
        try:
            # 调用服务层获取数据
            board = await self.sector_service.get_industry_board(board_code)
            
            # 如果未找到板块，返回None
            if board is None:
                return None
            
            # 将Pydantic模型转换为字典
            return board.model_dump()
        except Exception as e:
            logger.error(f"获取行业板块失败: {str(e)}")
            raise Exception(f"获取行业板块失败: {str(e)}")

    # 修复以下三个方法的缩进，使其成为类的方法
    async def get_industry_board_spot(self, name: str) -> Optional[Dict]:
        """
        获取行业板块实时行情详情（通过名称）
        
        Args:
            name: 板块名称，如"小金属"
            
        Returns:
            Optional[Dict]: 行业板块实时行情详情，如果未找到则返回None
        """
        logger.info(f"MCP获取行业板块实时行情详情: {name}")
        try:
            # 调用服务层获取数据
            spot = await self.sector_service.get_industry_board_spot(name)
            
            # 如果未找到板块，返回None
            if spot is None:
                return None
            
            # 将Pydantic模型转换为字典
            return spot.model_dump()
        except Exception as e:
            logger.error(f"获取行业板块实时行情详情失败: {str(e)}")
            raise Exception(f"获取行业板块实时行情详情失败: {str(e)}")

    async def get_industry_board_spot_by_code(self, board_code: str) -> Optional[Dict]:
        """
        获取行业板块实时行情详情（通过代码）
        
        Args:
            board_code: 板块代码，如"BK1027"
            
        Returns:
            Optional[Dict]: 行业板块实时行情详情，如果未找到则返回None
        """
        logger.info(f"MCP通过代码获取行业板块实时行情详情: {board_code}")
        try:
            # 调用服务层获取数据
            spot = await self.sector_service.get_industry_board_spot_by_code(board_code)
            
            # 如果未找到板块，返回None
            if spot is None:
                return None
            
            # 将Pydantic模型转换为字典
            return spot.model_dump()
        except Exception as e:
            logger.error(f"通过代码获取行业板块实时行情详情失败: {str(e)}")
            raise Exception(f"通过代码获取行业板块实时行情详情失败: {str(e)}")

    async def get_industry_board_constituents(self, symbol: str) -> List[Dict]:
        """
        获取行业板块成份股
        
        Args:
            symbol: 板块名称或代码，如"小金属"或"BK1027"
            
        Returns:
            List[Dict]: 行业板块成份股列表
        """
        logger.info(f"MCP获取行业板块成份股: {symbol}")
        try:
            # 调用服务层获取数据
            constituents = await self.sector_service.get_industry_board_constituents(symbol)
            
            # 将Pydantic模型列表转换为字典列表
            return [constituent.model_dump() for constituent in constituents]
        except Exception as e:
            logger.error(f"获取行业板块成份股失败: {str(e)}")
            raise Exception(f"获取行业板块成份股失败: {str(e)}")