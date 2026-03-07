from typing import Dict, List, Optional
from app.core.logging import get_logger
from app.services.technical_service import TechnicalService

logger = get_logger(__name__)

class TechnicalMCP:
    """
    技术指标MCP接口
    
    本类提供了与技术指标相关的数据查询接口，包括筹码分布等。
    所有接口通过调用服务层实现，共享服务层的数据处理和缓存机制。
    
    使用示例:
        technical_mcp = TechnicalMCP()
        chip_distribution = technical_mcp.get_chip_distribution("000001")
    """
    
    def __init__(self):
        """初始化TechnicalMCP，创建服务实例"""
        self.technical_service = TechnicalService()
    
    async def get_chip_distribution(self, symbol: str, adjust: str = "") -> List[Dict]:
        """
        获取股票筹码分布数据

        Args:
            symbol: 股票代码，如"000001"
            adjust: 复权类型，可选值为"qfq"(前复权)、"hfq"(后复权)、""(不复权)，默认为不复权

        Returns:
            List[Dict]: 筹码分布数据列表
        """
        logger.info(f"MCP获取股票筹码分布数据: {symbol}, 复权类型: {adjust}")
        try:
            # 调用服务层获取数据
            chips = await self.technical_service.get_chip_distribution(symbol, adjust)

            # 将Pydantic模型列表转换为字典列表
            return [chip.model_dump() for chip in chips]
        except Exception as e:
            logger.error(f"获取筹码分布数据失败: {str(e)}")
            raise Exception(f"获取筹码分布数据失败: {str(e)}")