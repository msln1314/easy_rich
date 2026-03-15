# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/15
# @File           : fund_flow_service.py
# @IDE            : PyCharm
# @desc           : 资金流向服务 - 北向资金、市场资金流向

import akshare as ak
import pandas as pd
import requests
from datetime import datetime, date
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, asdict
from app.core.logging import get_logger
from app.utils.cache import cache_result

logger = get_logger(__name__)


@dataclass
class NorthMoneyData:
    """北向资金数据"""
    date: str
    sh_hk_flow: float  # 沪港通
    sz_hk_flow: float  # 深港通
    total_flow: float  # 北向资金合计


@dataclass
class MarketFundFlowData:
    """市场资金流向数据"""
    date: str
    sh_close: float  # 上证收盘
    sh_change: float  # 上证涨跌幅
    sz_close: float  # 深证收盘
    sz_change: float  # 深证涨跌幅
    main_net_inflow: float  # 主力净流入
    main_net_inflow_pct: float  # 主力净流入占比
    super_large_net_inflow: float  # 超大单净流入
    large_net_inflow: float  # 大单净流入
    medium_net_inflow: float  # 中单净流入
    small_net_inflow: float  # 小单净流入


@dataclass
class NorthMoneyMinute:
    """北向资金分钟数据"""
    date: str
    time: str
    sh_hk_flow: float
    sz_hk_flow: float
    total_flow: float


class FundFlowService:
    """资金流向服务"""

    @cache_result(expire=60)  # 缓存60秒
    async def get_north_money_flow(self, days: int = 30) -> List[Dict[str, Any]]:
        """
        获取北向资金历史流向数据

        Args:
            days: 获取最近N天的数据

        Returns:
            北向资金流向数据列表
        """
        logger.info(f"获取北向资金历史流向: 最近{days}天")

        # 尝试 AKShare 分钟数据
        try:
            df = ak.stock_hsgt_fund_min_em(symbol='北向资金')

            if df is not None and not df.empty:
                result = []
                for _, row in df.iterrows():
                    try:
                        sh_flow = float(row.get('沪港通', 0) or 0)
                        sz_flow = float(row.get('深港通', 0) or 0)
                        total_flow = float(row.get('北向资金', 0) or 0)

                        # 只有当有实际数据时才添加
                        if sh_flow != 0 or sz_flow != 0 or total_flow != 0:
                            result.append({
                                'date': str(row.get('日期', '')),
                                'time': str(row.get('时间', '')),
                                'sh_hk_flow': sh_flow,
                                'sz_hk_flow': sz_flow,
                                'total_flow': total_flow
                            })
                    except Exception as e:
                        logger.warning(f"解析北向资金分钟数据失败: {e}")
                        continue

                if result:
                    logger.info(f"AKShare 获取到 {len(result)} 条北向资金分钟数据")
                    return result
        except Exception as e:
            logger.warning(f"AKShare 北向资金分钟数据失败: {e}")

        # 尝试从汇总接口获取
        try:
            summary = await self.get_north_money_summary()
            if summary and summary.get('items'):
                # 从汇总数据构建
                result = []
                seen_dates = set()
                for item in summary['items']:
                    date_str = item.get('date', '')
                    if date_str and date_str not in seen_dates:
                        channel = item.get('channel', '')
                        net_buy = item.get('net_buy_amount', 0)

                        # 根据通道确定是沪港通还是深港通
                        if '沪股通' in channel or '港股通(沪)' in channel:
                            result.append({
                                'date': date_str,
                                'time': '15:00',
                                'sh_hk_flow': net_buy,
                                'sz_hk_flow': 0,
                                'total_flow': net_buy
                            })
                            seen_dates.add(date_str)
                        elif '深股通' in channel or '港股通(深)' in channel:
                            result.append({
                                'date': date_str,
                                'time': '15:00',
                                'sh_hk_flow': 0,
                                'sz_hk_flow': net_buy,
                                'total_flow': net_buy
                            })
                            seen_dates.add(date_str)

                if result:
                    logger.info(f"从汇总获取到 {len(result)} 条北向资金数据")
                    return result
        except Exception as e:
            logger.warning(f"从汇总获取北向资金失败: {e}")

        logger.error("所有数据源均无法获取北向资金数据")
        return []

    @cache_result(expire=300)  # 缓存5分钟
    async def get_market_fund_flow(self, days: int = 30) -> List[Dict[str, Any]]:
        """
        获取市场资金流向数据

        Args:
            days: 获取最近N天的数据

        Returns:
            市场资金流向数据列表
        """
        logger.info(f"获取市场资金流向: 最近{days}天")

        try:
            df = ak.stock_market_fund_flow()

            if df.empty:
                return []

            # 取最近N天
            df = df.tail(days)

            result = []
            for _, row in df.iterrows():
                try:
                    item = {
                        'date': str(row.iloc[0]),  # 日期
                        'sh_close': float(row.iloc[1]) if pd.notna(row.iloc[1]) else None,  # 上证收盘
                        'sh_change': float(row.iloc[2]) if pd.notna(row.iloc[2]) else None,  # 上证涨跌幅
                        'sz_close': float(row.iloc[3]) if pd.notna(row.iloc[3]) else None,  # 深证收盘
                        'sz_change': float(row.iloc[4]) if pd.notna(row.iloc[4]) else None,  # 深证涨跌幅
                        'main_net_inflow': float(row.iloc[5]) if pd.notna(row.iloc[5]) else 0,  # 主力净流入
                        'main_net_inflow_pct': float(row.iloc[6]) if pd.notna(row.iloc[6]) else 0,  # 主力净流入占比
                        'super_large_net_inflow': float(row.iloc[7]) if pd.notna(row.iloc[7]) else 0,  # 超大单净流入
                        'large_net_inflow': float(row.iloc[9]) if pd.notna(row.iloc[9]) else 0,  # 大单净流入
                        'medium_net_inflow': float(row.iloc[11]) if pd.notna(row.iloc[11]) else 0,  # 中单净流入
                        'small_net_inflow': float(row.iloc[13]) if pd.notna(row.iloc[13]) else 0,  # 小单净流入
                    }
                    result.append(item)
                except Exception as e:
                    logger.warning(f"解析市场资金流向数据失败: {e}")
                    continue

            logger.info(f"获取到 {len(result)} 条市场资金流向数据")
            return result

        except Exception as e:
            logger.error(f"获取市场资金流向数据失败: {e}")
            return []

    async def get_today_market_fund_flow(self) -> Optional[Dict[str, Any]]:
        """
        获取今日市场资金流向

        Returns:
            今日市场资金流向数据
        """
        try:
            data = await self.get_market_fund_flow(days=1)
            if data:
                return data[-1]
            return None
        except Exception as e:
            logger.error(f"获取今日市场资金流向失败: {e}")
            return None

    @cache_result(expire=60)  # 缓存60秒
    async def get_north_money_summary(self) -> Dict[str, Any]:
        """
        获取北向资金汇总

        Returns:
            北向资金汇总数据
        """
        logger.info("获取北向资金汇总")

        try:
            # 获取北向资金汇总数据
            df = ak.stock_hsgt_fund_flow_summary_em()

            if df is None or df.empty:
                logger.warning("北向资金汇总数据为空")
                return {'items': [], 'update_time': datetime.now().isoformat()}

            result = {
                'items': [],
                'update_time': datetime.now().isoformat()
            }

            for _, row in df.iterrows():
                try:
                    item = {
                        'date': str(row.iloc[0]),  # 日期
                        'market': str(row.iloc[1]),  # 市场
                        'channel': str(row.iloc[2]),  # 通道
                        'status': str(row.iloc[3]),  # 交易状态
                        'buy_count': int(row.iloc[4]) if pd.notna(row.iloc[4]) else 0,  # 买入数量
                        'buy_amount': float(row.iloc[5]) if pd.notna(row.iloc[5]) else 0,  # 买入金额(亿)
                        'sell_amount': float(row.iloc[6]) if pd.notna(row.iloc[6]) else 0,  # 卖出金额(亿)
                        'net_buy_amount': float(row.iloc[7]) if pd.notna(row.iloc[7]) else 0,  # 净买入金额(亿)
                        'up_count': int(row.iloc[8]) if pd.notna(row.iloc[8]) else 0,  # 上涨家数
                        'down_count': int(row.iloc[9]) if pd.notna(row.iloc[9]) else 0,  # 下跌家数
                        'index_name': str(row.iloc[10]) if pd.notna(row.iloc[10]) else '',  # 指数名称
                        'index_change': float(row.iloc[11]) if pd.notna(row.iloc[11]) else 0,  # 指数涨跌幅
                    }
                    result['items'].append(item)
                except Exception as e:
                    logger.warning(f"解析北向资金汇总数据失败: {e}")
                    continue

            logger.info(f"获取到 {len(result['items'])} 条北向资金汇总数据")
            return result

        except Exception as e:
            logger.error(f"获取北向资金汇总失败: {e}")
            return {'items': [], 'update_time': datetime.now().isoformat()}

    @cache_result(expire=60)  # 缓存60秒
    async def get_realtime_north_money(self) -> Dict[str, Any]:
        """
        获取实时北向资金

        Returns:
            实时北向资金数据
        """
        logger.info("获取实时北向资金")

        try:
            # 从汇总数据获取
            summary = await self.get_north_money_summary()

            sh_flow = 0.0
            sz_flow = 0.0

            if summary and summary.get('items'):
                for item in summary['items']:
                    channel = item.get('channel', '')
                    net_buy = item.get('net_buy_amount', 0)

                    # 根据通道判断
                    if '沪股通' in channel or '港股通(沪)' in channel:
                        sh_flow += net_buy
                    elif '深股通' in channel or '港股通(深)' in channel:
                        sz_flow += net_buy

            total_flow = sh_flow + sz_flow

            # 如果汇总数据为0，尝试从分钟数据获取
            if total_flow == 0:
                minute_data = await self.get_north_money_flow(days=1)
                if minute_data:
                    latest = minute_data[-1] if minute_data else {}
                    sh_flow = latest.get('sh_hk_flow', 0)
                    sz_flow = latest.get('sz_hk_flow', 0)
                    total_flow = latest.get('total_flow', 0)

            return {
                'sh_hk_flow': sh_flow,
                'sz_hk_flow': sz_flow,
                'total_flow': total_flow,
                'date': str(date.today()),
                'time': datetime.now().strftime('%H:%M'),
                'update_time': datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"获取实时北向资金失败: {e}")
            return {
                'sh_hk_flow': 0,
                'sz_hk_flow': 0,
                'total_flow': 0,
                'date': str(date.today()),
                'time': datetime.now().strftime('%H:%M'),
                'update_time': datetime.now().isoformat()
            }


# 创建服务实例
fund_flow_service = FundFlowService()