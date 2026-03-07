import akshare as ak
import pandas as pd
from typing import Dict, List, Optional, Union
from app.core.logging import get_logger
from app.services.stock_service import StockService

logger = get_logger(__name__)

class StockMCP:
    """
    个股信息MCP接口
    
    本类提供了与个股相关的各种数据查询接口，包括基本信息、实时行情、历史行情、
    财务信息、资金流向和融资融券信息等。所有接口通过调用服务层实现，
    共享服务层的数据处理和缓存机制。
    
    使用示例:
        stock_mcp = StockMCP()
        stock_info = stock_mcp.get_stock_info("000001")
    """
    
    def __init__(self):
        """初始化StockMCP，创建服务实例"""
        self.stock_service = StockService()
    
    async def get_stock_info(self, stock_code: str) -> Dict:
        """
        获取个股基本信息
        
        本接口通过调用服务层获取个股的基本信息，
        包括总市值、流通市值、行业、上市时间、股票代码、股票简称、总股本和流通股等。
        
        Args:
            stock_code: 股票代码，如"000001"（平安银行）、"600000"（浦发银行）等
            
        Returns:
            Dict: 包含个股基本信息的字典，字段包括：
                - 总市值: float, 单位：元
                - 流通市值: float, 单位：元
                - 行业: str, 所属行业
                - 上市时间: str, 格式为YYYYMMDD
                - 股票代码: str
                - 股票简称: str
                - 总股本: float, 单位：股
                - 流通股: float, 单位：股
                - formatted_listing_date: str, 格式化的上市日期，格式为YYYY-MM-DD
            
        Raises:
            Exception: 当获取数据失败时抛出，错误信息包含具体原因
        """
        logger.info(f"MCP获取个股基本信息: {stock_code}")
        try:
            # 调用服务层获取数据
            stock_info = await self.stock_service.get_stock_info(stock_code)
            
            # 将Pydantic模型转换为字典
            result = stock_info.model_dump()
            
            # 添加一些额外的处理后的字段
            if stock_info.listing_date:
                listing_date = str(stock_info.listing_date)
                if len(listing_date) == 8:  # 格式为YYYYMMDD
                    formatted_date = f"{listing_date[:4]}-{listing_date[4:6]}-{listing_date[6:8]}"
                    result["formatted_listing_date"] = formatted_date
            
            return result
        except Exception as e:
            logger.error(f"获取个股信息失败: {str(e)}")
            raise Exception(f"获取个股信息失败: {str(e)}")
    
    async def get_stock_quote(self, stock_code: str) -> Dict:
        """
        获取个股实时行情
        
        Args:
            stock_code: 股票代码，如"000001"
            
        Returns:
            Dict: 包含个股实时行情的字典
        """
        logger.info(f"MCP获取个股实时行情: {stock_code}")
        try:
            # 调用服务层获取数据
            stock_quote = await self.stock_service.get_stock_quote(stock_code)
            
            # 将Pydantic模型转换为字典
            return stock_quote.model_dump()
        except Exception as e:
            logger.error(f"获取个股行情失败: {str(e)}")
            raise Exception(f"获取个股行情失败: {str(e)}")
    
    async def get_stock_history(self, stock_code: str, period: str = "daily",
                          start_date: Optional[str] = None,
                          end_date: Optional[str] = None) -> List[Dict]:
        """
        获取个股历史行情

        Args:
            stock_code: 股票代码
            period: 周期，可选 daily, weekly, monthly
            start_date: 开始日期，格式YYYYMMDD
            end_date: 结束日期，格式YYYYMMDD

        Returns:
            List[Dict]: 包含历史行情数据的字典列表
        """
        logger.info(f"MCP获取个股历史行情: {stock_code}, 周期: {period}")
        try:
            # 调用服务层获取数据
            history_data = await self.stock_service.get_stock_history(
                stock_code, period, start_date, end_date
            )

            # 将Pydantic模型列表转换为字典列表
            return [item.model_dump() for item in history_data]
        except Exception as e:
            logger.error(f"获取个股历史行情失败: {str(e)}")
            raise Exception(f"获取个股历史行情失败: {str(e)}")
    
    async def get_stock_financial(self, stock_code: str) -> Dict:
        """
        获取个股财务信息
        
        Args:
            stock_code: 股票代码
            
        Returns:
            Dict: 包含个股财务信息的字典
        """
        logger.info(f"MCP获取个股财务信息: {stock_code}")
        try:
            # 调用服务层获取数据
            financial_data = await self.stock_service.get_stock_financial(stock_code)
            
            # 将Pydantic模型转换为字典
            return financial_data.model_dump()
        except Exception as e:
            logger.error(f"获取个股财务信息失败: {str(e)}")
            raise Exception(f"获取个股财务信息失败: {str(e)}")
    
    async def get_stock_fund_flow(self, stock_code: str) -> Dict:
        """
        获取个股资金流向
        
        Args:
            stock_code: 股票代码
            
        Returns:
            Dict: 包含个股资金流向的字典
        """
        logger.info(f"MCP获取个股资金流向: {stock_code}")
        try:
            # 调用服务层获取数据
            fund_flow_data = await self.stock_service.get_stock_fund_flow(stock_code)
            
            # 将Pydantic模型转换为字典
            return fund_flow_data.model_dump()
        except Exception as e:
            logger.error(f"获取个股资金流向失败: {str(e)}")
            raise Exception(f"获取个股资金流向失败: {str(e)}")
    
    async def get_stock_margin(self, stock_code: str) -> Dict:
        """
        获取个股融资融券信息
        
        Args:
            stock_code: 股票代码
            
        Returns:
            Dict: 包含个股融资融券信息的字典
        """
        logger.info(f"MCP获取个股融资融券信息: {stock_code}")
        try:
            # 调用服务层获取数据
            margin_data = await self.stock_service.get_stock_margin(stock_code)
            
            # 服务层返回的已经是字典
            return margin_data
        except Exception as e:
            logger.error(f"获取个股融资融券信息失败: {str(e)}")
            raise Exception(f"获取个股融资融券信息失败: {str(e)}")