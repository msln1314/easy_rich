"""
股票评分模块

提供股票评分计算和评分详情生成功能
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from modules.utils import logger
from modules.news_analyzer import get_stock_news_analysis


def calculate_stock_score(hist_data: pd.DataFrame, indicators: Dict, financial_data: Optional[Dict] = None, 
                                 enable_pe: bool = False, enable_pb: bool = False, 
                                 enable_volume: bool = False, enable_turnover: bool = False,
                                 enable_dividend: bool = False, enable_dividend_yield: bool = False,
                                 enable_eps: bool = False, enable_navps: bool = False,
                                 enable_news: bool = False, stock_name: Optional[str] = None, 
                                 stock_code: Optional[str] = None, region: str = 'cn') -> float:
    """
    根据历史数据、技术指标和财务数据预测性计算股票评分，专注于识别涨停前的买入信号
    
    Args:
        hist_data: 历史数据
        indicators: 技术指标
        financial_data: 财务数据，包含市盈率、市净率、成交量、成交额等指标
        enable_pe: 是否启用市盈率评分
        enable_pb: 是否启用市净率评分
        enable_volume: 是否启用成交量评分
        enable_turnover: 是否启用成交额评分
        enable_dividend: 是否启用股息评分
        enable_dividend_yield: 是否启用股息率评分
        enable_eps: 是否启用每股收益评分
        enable_navps: 是否启用每股净资产评分
        enable_news: 是否启用新闻分析评分
        stock_name: 股票名称（用于新闻分析）
        stock_code: 股票代码（用于新闻分析）
        region: 地区，'cn'或'intl'（用于新闻分析）
    
    Returns:
        float: 股票评分，范围0-100
    """
    try:
        # 增加数据长度检查
        min_data_length = 3  # 至少需要3个交易日的数据（降低阈值以支持短周期分析）
        if hist_data.empty or len(hist_data) < min_data_length:
            return 0.0
        
        # 检查indicators是否为空或缺少必要的指标
        required_indicators = ['macd', 'dif', 'dea', 'k', 'd', 'j', 'rsi', 'ma5', 'ma10', 'ma20', 'volume_ma5']
        for indicator in required_indicators:
            if indicator not in indicators or indicators[indicator] is None or len(indicators[indicator]) == 0:
                logger.warning(f"Missing or empty indicator: {indicator}")
                return 0.0
            
        # 动态权重计算 - 优化为更注重潜力指标
        volatility = hist_data['close'].pct_change().std()  # 波动率
        if volatility > 0.05:  # 高波动率时增加潜力指标权重
            weights = {'macd': 0.3, 'kdj': 0.25, 'rsi': 0.15, 'ma': 0.2, 'volume': 0.1}
        else:  # 低波动率时大幅增加潜力指标权重
            weights = {'macd': 0.35, 'kdj': 0.25, 'rsi': 0.1, 'ma': 0.2, 'volume': 0.1}
        
        # 安全的数据访问函数
        def safe_get_value(data, index=-1, default=0):
            """安全获取数据值，避免索引越界"""
            try:
                if isinstance(data, pd.Series) and len(data) > abs(index):
                    return data.iloc[index]
                elif isinstance(data, pd.DataFrame) and len(data) > abs(index):
                    return data.iloc[index]
                else:
                    return default
            except (IndexError, KeyError):
                return default
        
        # 1. MACD指标
        macd_score = 0
        macd_latest = safe_get_value(indicators['macd'])
        if macd_latest > 0:
            macd_score += 10
        if len(hist_data) > 1:
            dif_latest = safe_get_value(indicators['dif'])
            dea_latest = safe_get_value(indicators['dea'])
            dif_prev = safe_get_value(indicators['dif'], -2)
            dea_prev = safe_get_value(indicators['dea'], -2)
            if dif_latest > dea_latest and dif_prev <= dea_prev:
                macd_score += 10
        macd_score *= weights['macd']
        
        # 2. KDJ指标
        kdj_score = 0
        k_latest = safe_get_value(indicators['k'])
        d_latest = safe_get_value(indicators['d'])
        j_latest = safe_get_value(indicators['j'])
        
        if k_latest < 30 and d_latest < 30:
            kdj_score += 10
        if j_latest < 20:
            kdj_score += 5
        if len(hist_data) > 1:
            k_prev = safe_get_value(indicators['k'], -2)
            d_prev = safe_get_value(indicators['d'], -2)
            if k_latest > d_latest and k_prev <= d_prev:
                kdj_score += 5
        kdj_score *= weights['kdj']
        
        # 3. RSI指标
        rsi = safe_get_value(indicators['rsi'])
        rsi_score = 0
        if rsi < 30:
            rsi_score = 20
        elif rsi < 40:
            rsi_score = 15
        elif rsi < 50:
            rsi_score = 10
        rsi_score *= weights['rsi']
        
        # 4. 均线系统
        ma_score = 0
        ma5_latest = safe_get_value(indicators['ma5'])
        ma10_latest = safe_get_value(indicators['ma10'])
        ma20_latest = safe_get_value(indicators['ma20'])
        
        if ma5_latest > ma10_latest > ma20_latest:
            ma_score += 10
        latest_price = safe_get_value(hist_data['close'])
        if latest_price > ma5_latest:
            ma_score += 4
        if latest_price > ma10_latest:
            ma_score += 3
        if latest_price > ma20_latest:
            ma_score += 3
        ma_score *= weights['ma']
        
        # 5. 成交量分析
        vol_score = 0
        volume_latest = safe_get_value(hist_data['volume'])
        volume_ma5_latest = safe_get_value(indicators['volume_ma5'])
        if volume_latest > volume_ma5_latest:
            vol_score += 10
        if len(hist_data) >= 3:
            volume_prev = safe_get_value(hist_data['volume'], -2)
            volume_prev2 = safe_get_value(hist_data['volume'], -3)
            if volume_latest > volume_prev > volume_prev2:
                vol_score += 10
        vol_score *= weights['volume']
        
        # 6. 趋势强度指标（新增）
        trend_score = 0
        if len(hist_data) >= 5:
            # 计算短期（5日）和长期（20日）趋势
            try:
                short_term = hist_data['close'].iloc[-5:].pct_change().mean()
                if len(hist_data) >= 20:
                    long_term = hist_data['close'].iloc[-20:].pct_change().mean()
                else:
                    long_term = hist_data['close'].pct_change().mean()
                
                # 趋势强度评分
                if short_term > long_term:  # 短期趋势强于长期趋势
                    trend_score += 10
                
                close_5_ago = safe_get_value(hist_data['close'], -5)
                close_20_ago = safe_get_value(hist_data['close'], -20) if len(hist_data) >= 20 else safe_get_value(hist_data['close'], 0)
                
                if latest_price > close_5_ago:  # 近期上涨
                    trend_score += 5
                if latest_price > close_20_ago:  # 长期上涨
                    trend_score += 5
            except Exception:
                trend_score = 0
                
        # 7. 潜力爆发指标（新增）- 识别即将爆发的股票
        potential_score = 0
        if len(hist_data) >= 3:
            try:
                # 价格突破近期高点
                recent_high = hist_data['high'].iloc[-5:].max()
                if latest_price > recent_high:
                    potential_score += 8
                
                # 成交量放大突破
                volume_avg_10 = hist_data['volume'].iloc[-10:].mean() if len(hist_data) >= 10 else hist_data['volume'].mean()
                if volume_latest > volume_avg_10 * 1.5:
                    potential_score += 7
                
                # MACD金叉确认
                if macd_latest > 0 and len(hist_data) > 1:
                    dif_latest_potential = safe_get_value(indicators['dif'])
                    dea_latest_potential = safe_get_value(indicators['dea'])
                    dif_prev = safe_get_value(indicators['dif'], -2)
                    dea_prev = safe_get_value(indicators['dea'], -2)
                    if dif_latest_potential > dea_latest_potential and dif_prev <= dea_prev:
                        potential_score += 10
                
                # KDJ低位金叉
                if k_latest < 30 and d_latest < 30 and k_latest > d_latest:
                    potential_score += 8
                    
            except Exception:
                potential_score = 0
                
        # 7. 风险调整（新增）
        risk_adjustment = 1.0
        # 基于波动率调整
        if volatility > 0.1:  # 高波动率
            risk_adjustment *= 0.9
        elif volatility < 0.05:  # 低波动率
            risk_adjustment *= 1.1
        # 基于最大回撤调整
        try:
            max_drawdown = (hist_data['close'].cummax() - hist_data['close']).max() / hist_data['close'].cummax().max()
            if max_drawdown > 0.2:  # 最大回撤超过20%
                risk_adjustment *= 0.9
        except Exception:
            pass
            
        # 7. 财务指标评分（新增）- 支持开关控制
        financial_score = 0
        financial_details = []
        if financial_data:
            # 市盈率评分：低PE有优势，但避免负值
            if enable_pe:
                pe_ratio = financial_data.get('pe_ratio')
                if pe_ratio is not None and pe_ratio > 0:
                    if pe_ratio < 15:  # 低市盈率
                        financial_score += 8
                        financial_details.append(f"PE({pe_ratio:.1f}):+8分")
                    elif pe_ratio < 25:  # 中等市盈率
                        financial_score += 5
                        financial_details.append(f"PE({pe_ratio:.1f}):+5分")
                    elif pe_ratio < 40:  # 较高市盈率
                        financial_score += 3
                        financial_details.append(f"PE({pe_ratio:.1f}):+3分")
            
            # 市净率评分：低PB有优势
            if enable_pb:
                pb_ratio = financial_data.get('pb_ratio')
                if pb_ratio is not None and pb_ratio > 0:
                    if pb_ratio < 1.5:  # 低市净率
                        financial_score += 7
                        financial_details.append(f"PB({pb_ratio:.1f}):+7分")
                    elif pb_ratio < 2.0:  # 中等市净率
                        financial_score += 5
                        financial_details.append(f"PB({pb_ratio:.1f}):+5分")
                    elif pb_ratio < 3.0:  # 较高市净率
                        financial_score += 3
                        financial_details.append(f"PB({pb_ratio:.1f}):+3分")
            
            # 换手率评分：适度活跃有优势
            if enable_turnover:
                turnover_rate = financial_data.get('turnover_rate')
                if turnover_rate is not None:
                    if 3 <= turnover_rate <= 15:  # 适度活跃
                        financial_score += 6
                        financial_details.append(f"换手率({turnover_rate:.1f}%):+6分")
                    elif turnover_rate > 20:  # 过度活跃，可能过热
                        financial_score -= 2
                        financial_details.append(f"换手率({turnover_rate:.1f}%):-2分")
            
            # 量比评分：量比大于1表示成交量放大
            if enable_volume:
                volume_ratio = financial_data.get('volume_ratio')
                if volume_ratio is not None and volume_ratio > 1.5:
                    financial_score += 5
                    financial_details.append(f"量比({volume_ratio:.1f}):+5分")
            
            # 股息评分：高股息有优势
            if enable_dividend:
                dividend = financial_data.get('dividend')
                if dividend is not None and dividend > 0:
                    if dividend > 1.0:  # 高股息
                        financial_score += 7
                        financial_details.append(f"股息({dividend:.2f}元):+7分")
                    elif dividend > 0.5:  # 中等股息
                        financial_score += 5
                        financial_details.append(f"股息({dividend:.2f}元):+5分")
                    elif dividend > 0.2:  # 低股息
                        financial_score += 3
                        financial_details.append(f"股息({dividend:.2f}元):+3分")
            
            # 股息率评分：高股息率有优势
            if enable_dividend_yield:
                dividend_yield = financial_data.get('dividend_yield')
                if dividend_yield is not None and dividend_yield > 0:
                    if dividend_yield > 5.0:  # 高股息率
                        financial_score += 6
                        financial_details.append(f"股息率({dividend_yield:.1f}%):+6分")
                    elif dividend_yield > 3.0:  # 中等股息率
                        financial_score += 4
                        financial_details.append(f"股息率({dividend_yield:.1f}%):+4分")
                    elif dividend_yield > 1.0:  # 低股息率
                        financial_score += 2
                        financial_details.append(f"股息率({dividend_yield:.1f}%):+2分")
            
            # 每股收益评分：高EPS有优势
            if enable_eps:
                eps = financial_data.get('eps')
                if eps is not None and eps > 0:
                    if eps > 1.0:  # 高每股收益
                        financial_score += 8
                        financial_details.append(f"每股收益({eps:.2f}元):+8分")
                    elif eps > 0.5:  # 中等每股收益
                        financial_score += 5
                        financial_details.append(f"每股收益({eps:.2f}元):+5分")
                    elif eps > 0.2:  # 低每股收益
                        financial_score += 3
                        financial_details.append(f"每股收益({eps:.2f}元):+3分")
            
            # 每股净资产评分：高NAVPS有优势
            if enable_navps:
                navps = financial_data.get('navps')
                if navps is not None and navps > 0:
                    if navps > 5.0:  # 高每股净资产
                        financial_score += 7
                        financial_details.append(f"每股净资产({navps:.2f}元):+7分")
                    elif navps > 3.0:  # 中等每股净资产
                        financial_score += 5
                        financial_details.append(f"每股净资产({navps:.2f}元):+5分")
                    elif navps > 1.0:  # 低每股净资产
                        financial_score += 3
                        financial_details.append(f"每股净资产({navps:.2f}元):+3分")
        
        # 8. 新闻热度评分（新增）- 支持开关控制
        news_score = 0
        news_details = []
        if enable_news and stock_name and stock_code:
            try:
                news_analysis = get_stock_news_analysis(stock_name, stock_code, enable_news=True, region=region)
                if news_analysis['status'] == 'success' and news_analysis['score'] > 0:
                    news_score = news_analysis['score']
                    news_details.append(f"新闻热度({news_score}分)=[新闻{news_analysis['news_count']}条 + 关键词得分{news_analysis['total_score']}]")
                elif news_analysis['status'] == 'success':
                    news_details.append(f"新闻热度(0分)=[新闻{news_analysis['news_count']}条，无显著关键词]")
                else:
                    news_details.append(f"新闻分析: {news_analysis['message']}")
            except Exception as e:
                logger.warning(f"新闻评分计算失败: {e}")
                news_details.append("新闻分析: 计算失败")
        
        # 综合评分 - 加入潜力爆发指标、财务指标和新闻热度
        total_score = (macd_score + kdj_score + rsi_score + ma_score + vol_score + trend_score + potential_score + financial_score + news_score) * risk_adjustment
        
        # 根据历史表现调整评分 - 优化为更注重潜力
        try:
            first_price = safe_get_value(hist_data['close'], 0)
            if first_price > 0:
                recent_performance = latest_price / first_price - 1
                # 对于潜力股，小幅上涨或下跌的股票给予更高权重
                if -0.05 <= recent_performance <= 0.1:  # 小幅波动，有潜力
                    total_score *= 1.2  # 大幅提升潜力股评分
                elif recent_performance > 0.1:  # 已经大幅上涨
                    total_score *= 0.9  # 降低已大涨股票的评分
                elif recent_performance < -0.05:  # 大幅下跌
                    total_score *= 0.8  # 降低大幅下跌股票的评分
        except Exception:
            pass
            
        return round(min(total_score, 100), 2)  # 确保评分不超过100，并保留2位小数
        
    except Exception as e:
        logger.error(f"计算股票评分时出错: {str(e)}")
        return 0.0


def calculate_predictive_score(hist_data: pd.DataFrame, indicators: Dict) -> float:
    """
    预测性评分算法 - 专注于识别涨停前的买入信号
    
    Args:
        hist_data: 历史数据
        indicators: 技术指标
    
    Returns:
        float: 预测性评分，范围0-100
    """
    try:
        # 基本数据检查
        if hist_data.empty or len(hist_data) < 5:
            return 0.0
            
        # 检查必要的技术指标
        required_indicators = ['macd', 'dif', 'dea', 'k', 'd', 'j', 'rsi', 'ma5', 'ma10', 'ma20', 'volume_ma5']
        for indicator in required_indicators:
            if indicator not in indicators or indicators[indicator] is None or len(indicators[indicator]) == 0:
                return 0.0
        
        # 安全的数据访问函数
        def safe_get_value(data, index=-1, default=0):
            try:
                if isinstance(data, pd.Series) and len(data) > abs(index):
                    return data.iloc[index]
                elif isinstance(data, pd.DataFrame) and len(data) > abs(index):
                    return data.iloc[index]
                else:
                    return default
            except (IndexError, KeyError):
                return default
        
        latest_price = safe_get_value(hist_data['close'])
        
        # 1. 量价关系分析（权重最高）
        volume_score = 0
        volume_latest = safe_get_value(hist_data['volume'])
        volume_ma5 = safe_get_value(indicators['volume_ma5'])
        
        # 成交量显著放大（2倍以上）
        if volume_latest > volume_ma5 * 2:
            volume_score += 20
        # 连续放量
        if len(hist_data) >= 3:
            volume_prev1 = safe_get_value(hist_data['volume'], -2)
            volume_prev2 = safe_get_value(hist_data['volume'], -3)
            if volume_latest > volume_prev1 > volume_prev2:
                volume_score += 15
        
        # 2. 价格突破分析
        breakout_score = 0
        ma5 = safe_get_value(indicators['ma5'])
        ma10 = safe_get_value(indicators['ma10'])
        ma20 = safe_get_value(indicators['ma20'])
        
        # 突破重要均线
        if latest_price > ma5 > ma10 > ma20:  # 多头排列且价格在均线之上
            breakout_score += 15
        # 突破近期高点
        if len(hist_data) >= 10:
            recent_high = hist_data['close'].iloc[-10:].max()
            if latest_price > recent_high:
                breakout_score += 10
        
        # 3. 技术指标金叉信号
        crossover_score = 0
        
        # MACD金叉
        dif = safe_get_value(indicators['dif'])
        dea = safe_get_value(indicators['dea'])
        if len(hist_data) > 1:
            dif_prev = safe_get_value(indicators['dif'], -2)
            dea_prev = safe_get_value(indicators['dea'], -2)
            if dif > dea and dif_prev <= dea_prev:  # DIF上穿DEA
                crossover_score += 15
        
        # KDJ金叉
        k = safe_get_value(indicators['k'])
        d = safe_get_value(indicators['d'])
        if len(hist_data) > 1:
            k_prev = safe_get_value(indicators['k'], -2)
            d_prev = safe_get_value(indicators['d'], -2)
            if k > d and k_prev <= d_prev:  # K上穿D
                crossover_score += 10
        
        # 4. 超卖反弹信号
        rebound_score = 0
        rsi = safe_get_value(indicators['rsi'])
        
        # RSI从超卖区域反弹
        if len(hist_data) >= 3:
            rsi_prev1 = safe_get_value(indicators['rsi'], -2)
            rsi_prev2 = safe_get_value(indicators['rsi'], -3)
            if rsi_prev2 < 30 and rsi_prev1 > 30 and rsi > 40:  # 从超卖区域反弹
                rebound_score += 12
        
        # 5. 价格动量分析
        momentum_score = 0
        
        # 短期强势
        if len(hist_data) >= 5:
            price_change_5d = (latest_price / safe_get_value(hist_data['close'], -5) - 1) * 100
            if price_change_5d > 5:  # 5日内涨幅超过5%
                momentum_score += 8
        
        # 6. 波动率分析（低波动后的突破）
        volatility_score = 0
        volatility = hist_data['close'].pct_change().std()
        
        # 低波动后的首次放量
        if volatility < 0.03 and volume_latest > volume_ma5 * 1.5:
            volatility_score += 10
        
        # 综合评分（加权计算）
        weights = {
            'volume': 0.25,      # 量价关系最重要
            'breakout': 0.20,    # 突破信号
            'crossover': 0.20,   # 技术金叉
            'rebound': 0.15,     # 超卖反弹
            'momentum': 0.10,    # 价格动量
            'volatility': 0.10   # 波动率特征
        }
        
        total_score = (
            volume_score * weights['volume'] +
            breakout_score * weights['breakout'] +
            crossover_score * weights['crossover'] +
            rebound_score * weights['rebound'] +
            momentum_score * weights['momentum'] +
            volatility_score * weights['volatility']
        )
        
        # 风险调整因子
        risk_adjustment = 1.0
        
        # 如果已经大幅上涨，降低评分（避免追高）
        if len(hist_data) >= 3:
            recent_gain = (latest_price / safe_get_value(hist_data['close'], -3) - 1) * 100
            if recent_gain > 15:  # 3日内涨幅超过15%
                risk_adjustment *= 0.7
        
        final_score = total_score * risk_adjustment
        
        return round(min(final_score, 100), 2)
        
    except Exception as e:
        logger.error(f"计算预测性评分时出错: {str(e)}")
        return 0.0


def generate_score_details(hist_data: pd.DataFrame, indicators: Dict, score: float, price_change: float,
                          financial_data: Optional[Dict] = None, enable_pe: bool = False, enable_pb: bool = False,
                          enable_volume: bool = False, enable_turnover: bool = False, 
                          enable_news: bool = False, news_analysis: Optional[Dict] = None) -> str:
    """
    生成评分详情字符串
    
    Args:
        hist_data: 历史数据
        indicators: 技术指标
        score: 总评分
        price_change: 价格变化百分比
        financial_data: 财务数据
        enable_pe: 是否启用市盈率评分
        enable_pb: 是否启用市净率评分
        enable_volume: 是否启用成交量评分
        enable_turnover: 是否启用成交额评分
        enable_news: 是否启用新闻评分
        news_analysis: 新闻分析结果
    
    Returns:
        str: 评分详情字符串
    """
    try:
        # 安全的数据访问函数
        def safe_get_value(data, index=-1, default=0):
            """安全获取数据值，避免索引越界"""
            try:
                if isinstance(data, pd.Series) and len(data) > abs(index):
                    return data.iloc[index]
                elif isinstance(data, pd.DataFrame) and len(data) > abs(index):
                    return data.iloc[index]
                else:
                    return default
            except (IndexError, KeyError):
                return default
        
        score_details = []
        
        # MACD指标得分详情
        macd_score = 0
        macd_latest = safe_get_value(indicators.get('macd', pd.Series()))
        if macd_latest > 0:
            macd_score += 10
        
        dif_latest = safe_get_value(indicators.get('dif', pd.Series()))
        dea_latest = safe_get_value(indicators.get('dea', pd.Series()))
        dif_prev = safe_get_value(indicators.get('dif', pd.Series()), -2)
        dea_prev = safe_get_value(indicators.get('dea', pd.Series()), -2)
        
        if len(hist_data) > 1 and dif_latest > dea_latest and dif_prev <= dea_prev:
            macd_score += 10
        score_details.append(f"MACD({macd_score}分)=[柱>0:{10 if macd_latest > 0 else 0}分 + DIF上穿:{10 if macd_score > 10 else 0}分]")
        
        # KDJ指标得分详情
        kdj_score = 0
        k_latest = safe_get_value(indicators.get('k', pd.Series()))
        d_latest = safe_get_value(indicators.get('d', pd.Series()))
        j_latest = safe_get_value(indicators.get('j', pd.Series()))
        
        if k_latest < 30 and d_latest < 30:
            kdj_score += 10
        if j_latest < 20:
            kdj_score += 5
        
        k_prev = safe_get_value(indicators.get('k', pd.Series()), -2)
        d_prev = safe_get_value(indicators.get('d', pd.Series()), -2)
        
        if len(hist_data) > 1 and k_latest > d_latest and k_prev <= d_prev:
            kdj_score += 5
        score_details.append(f"KDJ({kdj_score}分)=[KD<30:{10 if k_latest < 30 and d_latest < 30 else 0}分 + J<20:{5 if j_latest < 20 else 0}分 + K上穿:{5 if kdj_score >= 15 else 0}分]")
        
        # RSI指标得分详情
        rsi = safe_get_value(indicators.get('rsi', pd.Series()))
        rsi_score = 0
        if rsi < 30:
            rsi_score = 20
        elif rsi < 40:
            rsi_score = 15
        elif rsi < 50:
            rsi_score = 10
        score_details.append(f"RSI({rsi_score}分)=[RSI={rsi:.1f}]")
        
        # 均线系统得分详情
        ma_score = 0
        ma5_latest = safe_get_value(indicators.get('ma5', pd.Series()))
        ma10_latest = safe_get_value(indicators.get('ma10', pd.Series()))
        ma20_latest = safe_get_value(indicators.get('ma20', pd.Series()))
        
        if ma5_latest > ma10_latest > ma20_latest:
            ma_score += 10
        latest_price = safe_get_value(hist_data['close'])
        ma_cross_score = 0
        if latest_price > ma5_latest:
            ma_cross_score += 4
        if latest_price > ma10_latest:
            ma_cross_score += 3
        if latest_price > ma20_latest:
            ma_cross_score += 3
        score_details.append(f"均线({ma_score + ma_cross_score}分)=[多头排列:{ma_score}分 + 站上均线:{ma_cross_score}分]")
        
        # 成交量分析得分详情
        vol_score = 0
        volume_latest = safe_get_value(hist_data['volume'])
        volume_ma5_latest = safe_get_value(indicators.get('volume_ma5', pd.Series()))
        
        if volume_latest > volume_ma5_latest:
            vol_score += 10
        if len(hist_data) >= 3:  # 确保有足够的数据进行比较
            volume_prev = safe_get_value(hist_data['volume'], -2)
            volume_prev2 = safe_get_value(hist_data['volume'], -3)
            if volume_latest > volume_prev > volume_prev2:
                vol_score += 10
                
        score_details.append(f"成交量({vol_score}分)=[量>均量:{10 if volume_latest > volume_ma5_latest else 0}分 + 量增加:{10 if vol_score >= 20 else 0}分]")
        
        # 添加财务指标详情（如果启用）
        financial_details = []
        if financial_data:
            if enable_pe:
                pe_ratio = financial_data.get('pe_ratio')
                if pe_ratio is not None and pe_ratio > 0:
                    if pe_ratio < 15:
                        financial_details.append(f"PE({pe_ratio:.1f}):+8分")
                    elif pe_ratio < 30:
                        financial_details.append(f"PE({pe_ratio:.1f}):+5分")
                    elif pe_ratio > 100:
                        financial_details.append(f"PE({pe_ratio:.1f}):-5分")
            
            if enable_pb:
                pb_ratio = financial_data.get('pb_ratio')
                if pb_ratio is not None and pb_ratio > 0:
                    if pb_ratio < 1.5:
                        financial_details.append(f"PB({pb_ratio:.1f}):+7分")
                    elif pb_ratio < 3:
                        financial_details.append(f"PB({pb_ratio:.1f}):+4分")
                    elif pb_ratio > 5:
                        financial_details.append(f"PB({pb_ratio:.1f}):-3分")
            
            if enable_turnover:
                turnover_rate = financial_data.get('turnover_rate')
                if turnover_rate is not None:
                    if 3 <= turnover_rate <= 15:
                        financial_details.append(f"换手率({turnover_rate:.1f}%):+6分")
                    elif turnover_rate > 20:
                        financial_details.append(f"换手率({turnover_rate:.1f}%):-2分")
            
            if enable_volume:
                volume_ratio = financial_data.get('volume_ratio')
                if volume_ratio is not None and volume_ratio > 1.5:
                    financial_details.append(f"量比({volume_ratio:.1f}):+5分")
        
        # 添加新闻评分详情（如果启用）
        news_details = []
        if enable_news and news_analysis:
            news_score = news_analysis.get('score', 0)
            news_count = news_analysis.get('news_count', 0)
            keyword_count = news_analysis.get('keyword_count', 0)
            total_keyword_score = news_analysis.get('total_score', 0)
            status = news_analysis.get('status', '')
            
            if status == 'success':
                if news_score > 0:
                    news_details.append(f"新闻热度({news_score}分):{news_count}条新闻, {keyword_count}个关键词")
                elif news_score == 0 and total_keyword_score != 0:
                    news_details.append(f"新闻热度(0分):{news_count}条新闻, 关键词得分{total_keyword_score}")
                else:
                    news_details.append(f"新闻热度(0分):{news_count}条新闻, 无显著关键词")
            elif status == 'no_news':
                news_details.append("新闻热度(0分):未找到相关新闻")
            elif status == 'no_internet':
                news_details.append("新闻热度(0分):网络连接不可用")
            elif status == 'error':
                news_details.append("新闻热度(0分):分析过程出错")
        
        # 合并所有得分详情
        score_detail_str = f"总分{round(score, 2)}分 = " + " + ".join(score_details)
        if financial_details:
            score_detail_str += " + [财务指标:" + ", ".join(financial_details) + "]"
        if news_details:
            score_detail_str += " + [新闻分析:" + ", ".join(news_details) + "]"
        
        return score_detail_str
        
    except Exception as e:
        logger.error(f"生成评分详情时出错: {str(e)}")
        return f"总分{round(score, 2)}分"


def calculate_dynamic_weights(hist_data: pd.DataFrame) -> Dict[str, float]:
    """
    根据市场条件动态计算权重
    
    Args:
        hist_data: 历史数据
    
    Returns:
        Dict[str, float]: 各指标权重
    """
    try:
        volatility = hist_data['close'].pct_change().std()  # 波动率
        
        if volatility > 0.05:  # 高波动率时增加技术指标权重
            weights = {'macd': 0.25, 'kdj': 0.25, 'rsi': 0.2, 'ma': 0.2, 'volume': 0.1}
        else:  # 低波动率时增加趋势指标权重
            weights = {'macd': 0.2, 'kdj': 0.2, 'rsi': 0.15, 'ma': 0.3, 'volume': 0.15}
            
        return weights
        
    except Exception as e:
        logger.error(f"计算动态权重时出错: {str(e)}")
        # 返回默认权重
        return {'macd': 0.2, 'kdj': 0.2, 'rsi': 0.15, 'ma': 0.25, 'volume': 0.2}


def calculate_risk_adjustment(hist_data: pd.DataFrame) -> float:
    """
    计算风险调整系数
    
    Args:
        hist_data: 历史数据
    
    Returns:
        float: 风险调整系数
    """
    try:
        risk_adjustment = 1.0
        
        # 基于波动率调整
        volatility = hist_data['close'].pct_change().std()
        if volatility > 0.1:  # 高波动率
            risk_adjustment *= 0.9
        elif volatility < 0.05:  # 低波动率
            risk_adjustment *= 1.1
            
        # 基于最大回撤调整
        max_drawdown = (hist_data['close'].cummax() - hist_data['close']).max() / hist_data['close'].cummax().max()
        if max_drawdown > 0.2:  # 最大回撤超过20%
            risk_adjustment *= 0.9
            
        return risk_adjustment
        
    except Exception as e:
        logger.error(f"计算风险调整系数时出错: {str(e)}")
        return 1.0


def calculate_trend_score(hist_data: pd.DataFrame) -> float:
    """
    计算趋势强度评分
    
    Args:
        hist_data: 历史数据
    
    Returns:
        float: 趋势评分
    """
    try:
        trend_score = 0
        
        if len(hist_data) >= 5:
            # 计算短期（5日）和长期（20日）趋势
            short_term = hist_data['close'].iloc[-5:].pct_change().mean()
            long_term = hist_data['close'].iloc[-20:].pct_change().mean()
            
            # 趋势强度评分
            if short_term > long_term:  # 短期趋势强于长期趋势
                trend_score += 10
            if hist_data['close'].iloc[-1] > hist_data['close'].iloc[-5]:  # 近期上涨
                trend_score += 5
            if hist_data['close'].iloc[-1] > hist_data['close'].iloc[-20]:  # 长期上涨
                trend_score += 5
                
        return trend_score
        
    except Exception as e:
        logger.error(f"计算趋势评分时出错: {str(e)}")
        return 0.0