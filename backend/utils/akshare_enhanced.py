#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/8
# @File           : akshare_enhanced.py
# @IDE            : PyCharm
# @desc           : AKShare 增强服务 - 选股功能数据封装

"""
AKShare 增强服务模块

提供以下功能的数据封装:
1. 资金流向数据 (个股/大盘/板块/北向资金)
2. 涨停板数据 (涨停池/跌停池/强势板)
3. 融资融券数据 (个股两融/市场两融)
4. 机构持仓数据
5. 券商研报数据

支持缓存机制，减少API调用频率
"""

import asyncio
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any
from functools import lru_cache
import akshare as ak
import pandas as pd
from core.logger import logger


class AkShareEnhanced:
    """AKShare 增强服务类"""
    
    def __init__(self):
        self._cache: Dict[str, tuple[Any, float]] = {}
        self._cache_ttl = 300  # 默认缓存5分钟
        
    def _get_cached(self, key: str) -> Optional[Any]:
        """获取缓存数据"""
        if key in self._cache:
            data, timestamp = self._cache[key]
            if time.time() - timestamp < self._cache_ttl:
                return data
            else:
                del self._cache[key]
        return None
    
    def _set_cache(self, key: str, data: Any, ttl: int = None):
        """设置缓存数据"""
        self._cache[key] = (data, time.time())
        if ttl:
            self._cache_ttl = ttl
    
    def clear_cache(self):
        """清空缓存"""
        self._cache.clear()
        logger.info("AKShare 缓存已清空")
    
    # ============================================================
    # 资金流向数据
    # ============================================================
    
    async def get_individual_fund_flow(self, stock: str, market: str = "sh") -> pd.DataFrame:
        """
        获取个股资金流向
        
        Args:
            stock: 股票代码，如 "000425"
            market: 市场标识，"sh" 上交所，"sz" 深交所
            
        Returns:
            DataFrame: 包含主力净流入、小单净流入、中单净流入、大单净流入、超大单净流入等数据
        """
        cache_key = f"fund_flow_{market}_{stock}"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached
            
        try:
            df = ak.stock_individual_fund_flow(stock=stock, market=market)
            self._set_cache(cache_key, df, ttl=300)  # 5分钟缓存
            return df
        except Exception as e:
            logger.error(f"获取个股资金流向失败: {stock}, 错误: {e}")
            return pd.DataFrame()
    
    async def get_market_fund_flow(self) -> pd.DataFrame:
        """
        获取大盘资金流向
        
        Returns:
            DataFrame: 包含市场主力资金流向数据
        """
        cache_key = "market_fund_flow"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached
            
        try:
            df = ak.stock_market_fund_flow()
            self._set_cache(cache_key, df, ttl=300)
            return df
        except Exception as e:
            logger.error(f"获取大盘资金流向失败: {e}")
            return pd.DataFrame()
    
    async def get_sector_fund_flow_rank(self, sector_type: str = "行业资金流") -> pd.DataFrame:
        """
        获取板块资金流排行
        
        Args:
            sector_type: 板块类型，"行业资金流" 或 "概念资金流"
            
        Returns:
            DataFrame: 板块资金流排行数据
        """
        cache_key = f"sector_fund_flow_{sector_type}"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached
            
        try:
            df = ak.stock_sector_fund_flow_rank(sector_type=sector_type)
            self._set_cache(cache_key, df, ttl=300)
            return df
        except Exception as e:
            logger.error(f"获取板块资金流排行失败: {e}")
            return pd.DataFrame()
    
    async def get_hk_hsgt_north_flow(self) -> pd.DataFrame:
        """
        获取北向资金流向
        
        Returns:
            DataFrame: 沪股通和深股通的资金流向数据
        """
        cache_key = "hk_hsgt_north_flow"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached
            
        try:
            df = ak.stock_hk_hsgt_north_flow()
            self._set_cache(cache_key, df, ttl=300)
            return df
        except Exception as e:
            logger.error(f"获取北向资金流向失败: {e}")
            return pd.DataFrame()
    
    async def get_hk_hsgt_north Holding(self) -> pd.DataFrame:
        """
        获取北向资金持股明细
        
        Returns:
            DataFrame: 北向资金持股数据
        """
        cache_key = "hk_hsgt_north_holding"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached
            
        try:
            df = ak.stock_hk_hsgt_north_holding()
            self._set_cache(cache_key, df, ttl=3600)  # 1小时缓存
            return df
        except Exception as e:
            logger.error(f"获取北向资金持股失败: {e}")
            return pd.DataFrame()
    
    # ============================================================
    # 涨停板数据
    # ============================================================
    
    async def get_zt_pool(self, date: str = None) -> pd.DataFrame:
        """
        获取涨停板池
        
        Args:
            date: 日期，格式 "YYYYMMDD"，默认最新交易日
            
        Returns:
            DataFrame: 涨停板股票列表
        """
        cache_key = f"zt_pool_{date or 'latest'}"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached
            
        try:
            df = ak.stock_zt_pool(date=date)
            self._set_cache(cache_key, df, ttl=600)  # 10分钟缓存
            return df
        except Exception as e:
            logger.error(f"获取涨停板池失败: {e}")
            return pd.DataFrame()
    
    async def get_zt_pool_sub(self, date: str = None) -> pd.DataFrame:
        """
        获取跌停板池
        
        Args:
            date: 日期，格式 "YYYYMMDD"，默认最新交易日
            
        Returns:
            DataFrame: 跌停板股票列表
        """
        cache_key = f"zt_pool_sub_{date or 'latest'}"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached
            
        try:
            df = ak.stock_zt_pool_sub(date=date)
            self._set_cache(cache_key, df, ttl=600)
            return df
        except Exception as e:
            logger.error(f"获取跌停板池失败: {e}")
            return pd.DataFrame()
    
    async def get_zt_pool_strong(self, date: str = None) -> pd.DataFrame:
        """
        获取强势涨停板 (封板后未打开)
        
        Args:
            date: 日期，格式 "YYYYMMDD"，默认最新交易日
            
        Returns:
            DataFrame: 强势涨停板列表
        """
        cache_key = f"zt_pool_strong_{date or 'latest'}"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached
            
        try:
            df = ak.stock_zt_pool_strong(date=date)
            self._set_cache(cache_key, df, ttl=600)
            return df
        except Exception as e:
            logger.error(f"获取强势涨停板失败: {e}")
            return pd.DataFrame()
    
    async def get_zt_pool_zbgc(self, date: str = None) -> pd.DataFrame:
        """
        获取涨停板炸板池 (涨停后打开)
        
        Args:
            date: 日期，格式 "YYYYMMDD"，默认最新交易日
            
        Returns:
            DataFrame: 炸板股票列表
        """
        cache_key = f"zt_pool_zbgc_{date or 'latest'}"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached
            
        try:
            df = ak.stock_zt_pool_zbgc(date=date)
            self._set_cache(cache_key, df, ttl=600)
            return df
        except Exception as e:
            logger.error(f"获取涨停板炸板池失败: {e}")
            return pd.DataFrame()
    
    # ============================================================
    # 融资融券数据
    # ============================================================
    
    async def get_margin_detail(self, stock: str, symbol: str = "融资融券") -> pd.DataFrame:
        """
        获取个股融资融券详情
        
        Args:
            stock: 股票代码，如 "000001"
            symbol: 标识，"融资融券" 或 "融券"
            
        Returns:
            DataFrame: 融资融券明细数据
        """
        cache_key = f"margin_detail_{stock}_{symbol}"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached
            
        try:
            df = ak.stock_margin_detail(stock=stock, symbol=symbol)
            self._set_cache(cache_key, df, ttl=3600)  # 1小时缓存
            return df
        except Exception as e:
            logger.error(f"获取融资融券详情失败: {stock}, 错误: {e}")
            return pd.DataFrame()
    
    async def get_margin_sse(self) -> pd.DataFrame:
        """
        获取市场融资融券汇总
        
        Returns:
            DataFrame: 市场两融数据
        """
        cache_key = "margin_sse"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached
            
        try:
            df = ak.stock_margin_sse()
            self._set_cache(cache_key, df, ttl=1800)  # 30分钟缓存
            return df
        except Exception as e:
            logger.error(f"获取市场融资融券汇总失败: {e}")
            return pd.DataFrame()
    
    # ============================================================
    # 龙虎榜数据
    # ============================================================
    
    async def get_lhb(self, date: str = None) -> pd.DataFrame:
        """
        获取龙虎榜数据
        
        Args:
            date: 日期，格式 "YYYYMMDD"，默认最新交易日
            
        Returns:
            DataFrame: 龙虎榜数据
        """
        cache_key = f"lhb_{date or 'latest'}"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached
            
        try:
            df = ak.stock_lhb(date=date)
            self._set_cache(cache_key, df, ttl=3600)
            return df
        except Exception as e:
            logger.error(f"获取龙虎榜数据失败: {e}")
            return pd.DataFrame()
    
    async def get_lhb_detail(self, date: str) -> pd.DataFrame:
        """
        获取龙虎榜明细
        
        Args:
            date: 日期，格式 "YYYYMMDD"
            
        Returns:
            DataFrame: 龙虎榜明细数据
        """
        cache_key = f"lhb_detail_{date}"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached
            
        try:
            df = ak.stock_lhb_detail(date=date)
            self._set_cache(cache_key, df, ttl=3600)
            return df
        except Exception as e:
            logger.error(f"获取龙虎榜明细失败: {e}")
            return pd.DataFrame()
    
    # ============================================================
    # 机构持仓数据
    # ============================================================
    
    async def get_institution_holding(self, stock: str) -> pd.DataFrame:
        """
        获取机构持仓数据
        
        Args:
            stock: 股票代码
            
        Returns:
            DataFrame: 机构持仓数据
        """
        cache_key = f"institution_holding_{stock}"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached
            
        try:
            df = ak.stock_fund_flow(stock=stock)
            self._set_cache(cache_key, df, ttl=86400)  # 1天缓存
            return df
        except Exception as e:
            logger.error(f"获取机构持仓数据失败: {stock}, 错误: {e}")
            return pd.DataFrame()
    
    # ============================================================
    # 券商研报数据
    # ============================================================
    
    async def get_research_report(self, symbol: str = "推荐") -> pd.DataFrame:
        """
        获取券商研报
        
        Args:
            symbol: 研报类型，"推荐" 等
            
        Returns:
            DataFrame: 券商研报数据
        """
        cache_key = f"research_report_{symbol}"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached
            
        try:
            df = ak.stock_research_report(symbol=symbol)
            self._set_cache(cache_key, df, ttl=3600)  # 1小时缓存
            return df
        except Exception as e:
            logger.error(f"获取券商研报失败: {e}")
            return pd.DataFrame()
    
    # ============================================================
    # 多因子数据
    # ============================================================
    
    async def get_financial_abstract(self, stock: str) -> pd.DataFrame:
        """
        获取财务摘要
        
        Args:
            stock: 股票代码
            
        Returns:
            DataFrame: 财务摘要数据
        """
        cache_key = f"financial_abstract_{stock}"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached
            
        try:
            df = ak.stock_financial_abstract(stock=stock)
            self._set_cache(cache_key, df, ttl=86400)  # 1天缓存
            return df
        except Exception as e:
            logger.error(f"获取财务摘要失败: {stock}, 错误: {e}")
            return pd.DataFrame()
    
    async def get_financial_indicators(self, stock: str) -> pd.DataFrame:
        """
        获取财务指标
        
        Args:
            stock: 股票代码
            
        Returns:
            DataFrame: 财务指标数据
        """
        cache_key = f"financial_indicators_{stock}"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached
            
        try:
            df = ak.stock_financial_indicators(stock=stock)
            self._set_cache(cache_key, df, ttl=86400)
            return df
        except Exception as e:
            logger.error(f"获取财务指标失败: {stock}, 错误: {e}")
            return pd.DataFrame()
    
    async def get_stock_price_change(self, stock: str) -> pd.DataFrame:
        """
        获取股票涨跌幅
        
        Args:
            stock: 股票代码
            
        Returns:
            DataFrame: 股票涨跌幅数据
        """
        cache_key = f"price_change_{stock}"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached
            
        try:
            df = ak.stock_price_change(stock=stock)
            self._set_cache(cache_key, df, ttl=3600)
            return df
        except Exception as e:
            logger.error(f"获取股票涨跌幅失败: {stock}, 错误: {e}")
            return pd.DataFrame()


# 全局单例
_ak_enhanced_instance: Optional[AkShareEnhanced] = None


def get_ak_enhanced() -> AkShareEnhanced:
    """获取 AKShare 增强服务单例"""
    global _ak_enhanced_instance
    if _ak_enhanced_instance is None:
        _ak_enhanced_instance = AkShareEnhanced()
    return _ak_enhanced_instance


# 便捷函数
async def get_individual_fund_flow(stock: str, market: str = "sh") -> pd.DataFrame:
    """获取个股资金流向"""
    return await get_ak_enhanced().get_individual_fund_flow(stock, market)


async def get_market_fund_flow() -> pd.DataFrame:
    """获取大盘资金流向"""
    return await get_ak_enhanced().get_market_fund_flow()


async def get_sector_fund_flow_rank(sector_type: str = "行业资金流") -> pd.DataFrame:
    """获取板块资金流排行"""
    return await get_ak_enhanced().get_sector_fund_flow_rank(sector_type)


async def get_hk_hsgt_north_flow() -> pd.DataFrame:
    """获取北向资金流向"""
    return await get_ak_enhanced().get_hk_hsgt_north_flow()


async def get_zt_pool(date: str = None) -> pd.DataFrame:
    """获取涨停板池"""
    return await get_ak_enhanced().get_zt_pool(date)


async def get_zt_pool_sub(date: str = None) -> pd.DataFrame:
    """获取跌停板池"""
    return await get_ak_enhanced().get_zt_pool_sub(date)


async def get_zt_pool_strong(date: str = None) -> pd.DataFrame:
    """获取强势涨停板"""
    return await get_ak_enhanced().get_zt_pool_strong(date)


async def get_margin_detail(stock: str, symbol: str = "融资融券") -> pd.DataFrame:
    """获取个股融资融券详情"""
    return await get_ak_enhanced().get_margin_detail(stock, symbol)


async def get_margin_sse() -> pd.DataFrame:
    """获取市场融资融券汇总"""
    return await get_ak_enhanced().get_margin_sse()


async def get_lhb(date: str = None) -> pd.DataFrame:
    """获取龙虎榜数据"""
    return await get_ak_enhanced().get_lhb(date)


async def get_research_report(symbol: str = "推荐") -> pd.DataFrame:
    """获取券商研报"""
    return await get_ak_enhanced().get_research_report(symbol)
