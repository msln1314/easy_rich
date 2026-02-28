#!/usr/bin/env python3
"""
技术指标模块 - 负责计算各种技术指标
包括MA、MACD、KDJ、RSI、成交量指标等
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple, Any, cast, Optional
from modules.utils import logger

def calculate_technical_indicators(data: pd.DataFrame) -> Dict[str, pd.Series]:
    """
    计算技术指标，包括MA、MACD、KDJ、RSI等
    支持动态窗口大小以适应较短的数据周期
    
    Args:
        data: 包含历史数据的DataFrame
    
    Returns:
        Dict[str, pd.Series]: 包含各种技术指标的字典
    """
    try:
        if data.empty:
            return {}
            
        data_length = len(data)
        
        # 动态调整窗口大小以适应较短的数据周期
        if data_length >= 20:
            # 标准窗口大小
            ma_windows = [5, 10, 20]
            kdj_window = 9
            rsi_window = 14
            macd_fast = 12
            macd_slow = 26
            macd_signal = 9
        elif data_length >= 15:
            # 中等窗口大小
            ma_windows = [3, 7, 15]
            kdj_window = 7
            rsi_window = 10
            macd_fast = 8
            macd_slow = 18
            macd_signal = 6
        elif data_length >= 10:
            # 较小窗口大小
            ma_windows = [3, 5, 10]
            kdj_window = 5
            rsi_window = 8
            macd_fast = 6
            macd_slow = 12
            macd_signal = 4
        else:
            # 最小窗口大小
            ma_windows = [2, 3, min(5, data_length-1)]
            kdj_window = min(5, data_length-1)
            rsi_window = min(6, data_length-1)
            macd_fast = min(4, data_length-1)
            macd_slow = min(8, data_length-1)
            macd_signal = min(3, data_length-1)
            
        # 计算移动平均线
        data['ma5'] = data['close'].rolling(window=ma_windows[0]).mean()
        data['ma10'] = data['close'].rolling(window=ma_windows[1]).mean()
        data['ma20'] = data['close'].rolling(window=ma_windows[2]).mean()
        
        # 计算MACD
        exp_fast = data['close'].ewm(span=macd_fast, adjust=False).mean()
        exp_slow = data['close'].ewm(span=macd_slow, adjust=False).mean()
        data['dif'] = exp_fast - exp_slow
        data['dea'] = data['dif'].ewm(span=macd_signal, adjust=False).mean()
        data['macd'] = 2 * (data['dif'] - data['dea'])
        
        # 计算KDJ
        low_n = data['low'].rolling(window=kdj_window).min()
        high_n = data['high'].rolling(window=kdj_window).max()
        rsv = (data['close'] - low_n) / (high_n - low_n) * 100
        data['k'] = rsv.ewm(span=3, adjust=False).mean()
        data['d'] = data['k'].ewm(span=3, adjust=False).mean()
        data['j'] = 3 * data['k'] - 2 * data['d']
        
        # 计算RSI
        diff = data['close'].diff()
        gain = (diff.where(diff > 0, 0)).rolling(window=rsi_window).mean()
        loss = (-diff.where(diff < 0, 0)).rolling(window=rsi_window).mean()
        rs = gain / loss
        data['rsi'] = 100 - (100 / (1 + rs))
        
        # 计算成交量均线
        vol_window = min(5, ma_windows[0])
        data['volume_ma5'] = data['volume'].rolling(window=vol_window).mean()
        
        return {
            'ma5': cast(pd.Series, data['ma5']),
            'ma10': cast(pd.Series, data['ma10']),
            'ma20': cast(pd.Series, data['ma20']),
            'dif': cast(pd.Series, data['dif']),
            'dea': cast(pd.Series, data['dea']),
            'macd': cast(pd.Series, data['macd']),
            'k': cast(pd.Series, data['k']),
            'd': cast(pd.Series, data['d']),
            'j': cast(pd.Series, data['j']),
            'rsi': cast(pd.Series, data['rsi']),
            'volume_ma5': cast(pd.Series, data['volume_ma5'])
        }
        
    except Exception as e:
        logger.error(f"计算技术指标时出错: {str(e)}")
        return {}

def calculate_minute_indicators(data: pd.DataFrame, period: int = 1) -> Dict[str, pd.Series]:
    """
    计算分钟级技术指标
    根据数据量动态调整指标参数
    
    Args:
        data: 分钟级历史数据
        period: 分钟周期（1, 5, 15, 30, 60）
        
    Returns:
        Dict: 技术指标字典
    """
    try:
        if data.empty:
            return {}
        
        data_length = len(data)
        
        # 根据分钟周期和数据量调整指标参数
        if period == 1:
            # 1分钟数据，使用较短的参数
            ma_periods = [5, 10, 20] if data_length >= 20 else [3, 5, min(10, data_length-1)]
            macd_fast, macd_slow, macd_signal = (6, 12, 4) if data_length >= 15 else (3, 6, 2)
            kdj_period = min(9, data_length-1)
            rsi_period = min(14, data_length-1)
        elif period == 5:
            # 5分钟数据
            ma_periods = [10, 20, 60] if data_length >= 60 else [5, 10, min(30, data_length-1)]
            macd_fast, macd_slow, macd_signal = (12, 26, 9) if data_length >= 30 else (6, 12, 4)
            kdj_period = min(14, data_length-1)
            rsi_period = min(14, data_length-1)
        elif period in [15, 30]:
            # 15/30分钟数据
            ma_periods = [20, 60, 120] if data_length >= 120 else [10, 20, min(60, data_length-1)]
            macd_fast, macd_slow, macd_signal = (12, 26, 9) if data_length >= 30 else (8, 16, 6)
            kdj_period = min(14, data_length-1)
            rsi_period = min(14, data_length-1)
        else:
            # 60分钟及以上数据，使用标准参数
            ma_periods = [5, 10, 20] if data_length >= 20 else [3, 5, min(10, data_length-1)]
            macd_fast, macd_slow, macd_signal = (12, 26, 9) if data_length >= 30 else (6, 12, 4)
            kdj_period = min(9, data_length-1)
            rsi_period = min(14, data_length-1)
        
        # 计算移动平均线
        data['ma5'] = data['close'].rolling(window=ma_periods[0]).mean()
        data['ma10'] = data['close'].rolling(window=ma_periods[1]).mean()
        data['ma20'] = data['close'].rolling(window=ma_periods[2]).mean()
        
        # 计算MACD
        exp_fast = data['close'].ewm(span=macd_fast, adjust=False).mean()
        exp_slow = data['close'].ewm(span=macd_slow, adjust=False).mean()
        data['dif'] = exp_fast - exp_slow
        data['dea'] = data['dif'].ewm(span=macd_signal, adjust=False).mean()
        data['macd'] = 2 * (data['dif'] - data['dea'])
        
        # 计算KDJ
        low_n = data['low'].rolling(window=kdj_period).min()
        high_n = data['high'].rolling(window=kdj_period).max()
        rsv = (data['close'] - low_n) / (high_n - low_n) * 100
        data['k'] = rsv.ewm(span=3, adjust=False).mean()
        data['d'] = data['k'].ewm(span=3, adjust=False).mean()
        data['j'] = 3 * data['k'] - 2 * data['d']
        
        # 计算RSI
        diff = data['close'].diff()
        gain = (diff.where(diff > 0, 0)).rolling(window=rsi_period).mean()
        loss = (-diff.where(diff < 0, 0)).rolling(window=rsi_period).mean()
        rs = gain / loss
        data['rsi'] = 100 - (100 / (1 + rs))
        
        # 计算成交量均线
        vol_period = min(ma_periods[0], 10)
        data['volume_ma'] = data['volume'].rolling(window=vol_period).mean()
        
        return {
            'ma5': cast(pd.Series, data['ma5']),
            'ma10': cast(pd.Series, data['ma10']),
            'ma20': cast(pd.Series, data['ma20']),
            'dif': cast(pd.Series, data['dif']),
            'dea': cast(pd.Series, data['dea']),
            'macd': cast(pd.Series, data['macd']),
            'k': cast(pd.Series, data['k']),
            'd': cast(pd.Series, data['d']),
            'j': cast(pd.Series, data['j']),
            'rsi': cast(pd.Series, data['rsi']),
            'volume_ma': cast(pd.Series, data['volume_ma'])
        }
        
    except Exception as e:
        logger.error(f"计算{period}分钟技术指标时出错: {str(e)}")
        return {}

def calculate_bollinger_bands(data: pd.DataFrame, window: int = 20, num_std: float = 2.0) -> Dict[str, pd.Series]:
    """
    计算布林带指标
    
    Args:
        data: 包含历史数据的DataFrame
        window: 移动平均窗口大小
        num_std: 标准差倍数
    
    Returns:
        Dict[str, pd.Series]: 包含上轨、中轨、下轨的字典
    """
    try:
        if data.empty or len(data) < window:
            return {}
        
        # 中轨（移动平均线）
        middle_band = data['close'].rolling(window=window).mean()
        
        # 标准差
        std = data['close'].rolling(window=window).std()
        
        # 上轨和下轨
        upper_band = middle_band + (std * num_std)
        lower_band = middle_band - (std * num_std)
        
        return {
            'bb_upper': cast(pd.Series, upper_band),
            'bb_middle': cast(pd.Series, middle_band),
            'bb_lower': cast(pd.Series, lower_band),
            'bb_width': cast(pd.Series, (upper_band - lower_band) / middle_band * 100)  # 布林带宽度百分比
        }
        
    except Exception as e:
        logger.error(f"计算布林带指标时出错: {str(e)}")
        return {}

def calculate_atr(data: pd.DataFrame, window: int = 14) -> pd.Series:
    """
    计算平均真实波幅（ATR）
    
    Args:
        data: 包含历史数据的DataFrame
        window: 计算窗口大小
    
    Returns:
        pd.Series: ATR指标
    """
    try:
        if data.empty or len(data) < 2:
            return pd.Series(dtype=float)
        
        # 计算真实波幅
        high_low = data['high'] - data['low']
        high_close_prev = abs(data['high'] - data['close'].shift(1))
        low_close_prev = abs(data['low'] - data['close'].shift(1))
        
        true_range = pd.concat([high_low, high_close_prev, low_close_prev], axis=1).max(axis=1)
        
        # 计算ATR（真实波幅的移动平均）
        atr = true_range.rolling(window=window).mean()
        
        return atr
        
    except Exception as e:
        logger.error(f"计算ATR指标时出错: {str(e)}")
        return pd.Series(dtype=float)

def calculate_stochastic(data: pd.DataFrame, k_window: int = 14, d_window: int = 3) -> Dict[str, pd.Series]:
    """
    计算随机指标（Stochastic Oscillator）
    
    Args:
        data: 包含历史数据的DataFrame
        k_window: %K计算窗口
        d_window: %D平滑窗口
    
    Returns:
        Dict[str, pd.Series]: 包含%K和%D的字典
    """
    try:
        if data.empty or len(data) < k_window:
            return {}
        
        # 计算%K
        lowest_low = data['low'].rolling(window=k_window).min()
        highest_high = data['high'].rolling(window=k_window).max()
        k_percent = 100 * (data['close'] - lowest_low) / (highest_high - lowest_low)
        
        # 计算%D（%K的移动平均）
        d_percent = k_percent.rolling(window=d_window).mean()
        
        return {
            'stoch_k': cast(pd.Series, k_percent),
            'stoch_d': cast(pd.Series, d_percent)
        }
        
    except Exception as e:
        logger.error(f"计算随机指标时出错: {str(e)}")
        return {}

def calculate_williams_r(data: pd.DataFrame, window: int = 14) -> pd.Series:
    """
    计算威廉指标（Williams %R）
    
    Args:
        data: 包含历史数据的DataFrame
        window: 计算窗口大小
    
    Returns:
        pd.Series: Williams %R指标
    """
    try:
        if data.empty or len(data) < window:
            return pd.Series(dtype=float)
        
        highest_high = data['high'].rolling(window=window).max()
        lowest_low = data['low'].rolling(window=window).min()
        
        williams_r = -100 * (highest_high - data['close']) / (highest_high - lowest_low)
        
        return cast(pd.Series, williams_r)
        
    except Exception as e:
        logger.error(f"计算威廉指标时出错: {str(e)}")
        return pd.Series(dtype=float)

def calculate_cci(data: pd.DataFrame, window: int = 20) -> pd.Series:
    """
    计算商品通道指数（CCI）
    
    Args:
        data: 包含历史数据的DataFrame
        window: 计算窗口大小
    
    Returns:
        pd.Series: CCI指标
    """
    try:
        if data.empty or len(data) < window:
            return pd.Series(dtype=float)
        
        # 计算典型价格
        typical_price = (data['high'] + data['low'] + data['close']) / 3
        
        # 计算移动平均
        sma = typical_price.rolling(window=window).mean()
        
        # 计算平均绝对偏差
        mad = typical_price.rolling(window=window).apply(lambda x: abs(x - x.mean()).mean())
        
        # 计算CCI
        cci = (typical_price - sma) / (0.015 * mad)
        
        return cci
        
    except Exception as e:
        logger.error(f"计算CCI指标时出错: {str(e)}")
        return pd.Series(dtype=float)

def calculate_momentum(data: pd.DataFrame, window: int = 10) -> pd.Series:
    """
    计算动量指标（Momentum）
    
    Args:
        data: 包含历史数据的DataFrame
        window: 计算窗口大小
    
    Returns:
        pd.Series: 动量指标
    """
    try:
        if data.empty or len(data) < window:
            return pd.Series(dtype=float)
        
        momentum = data['close'] / data['close'].shift(window) * 100
        
        return momentum
        
    except Exception as e:
        logger.error(f"计算动量指标时出错: {str(e)}")
        return pd.Series(dtype=float)

def calculate_roc(data: pd.DataFrame, window: int = 12) -> pd.Series:
    """
    计算变动率指标（ROC）
    
    Args:
        data: 包含历史数据的DataFrame
        window: 计算窗口大小
    
    Returns:
        pd.Series: ROC指标
    """
    try:
        if data.empty or len(data) < window:
            return pd.Series(dtype=float)
        
        roc = (data['close'] - data['close'].shift(window)) / data['close'].shift(window) * 100
        
        return roc
        
    except Exception as e:
        logger.error(f"计算ROC指标时出错: {str(e)}")
        return pd.Series(dtype=float)

def calculate_obv(data: pd.DataFrame) -> pd.Series:
    """
    计算能量潮指标（OBV）
    
    Args:
        data: 包含历史数据的DataFrame
    
    Returns:
        pd.Series: OBV指标
    """
    try:
        if data.empty or len(data) < 2:
            return pd.Series(dtype=float)
        
        # 计算价格变化方向
        price_change = data['close'].diff()
        
        # 根据价格变化方向调整成交量
        obv_volume = data['volume'].copy()
        obv_volume[price_change < 0] = -obv_volume[price_change < 0]
        obv_volume[price_change == 0] = 0
        
        # 计算累积成交量
        obv = obv_volume.cumsum()
        
        return obv
        
    except Exception as e:
        logger.error(f"计算OBV指标时出错: {str(e)}")
        return pd.Series(dtype=float)

def get_all_indicators(data: pd.DataFrame, period: Optional[int] = None) -> Dict[str, Any]:
    """
    获取所有技术指标
    
    Args:
        data: 包含历史数据的DataFrame
        period: 分钟周期（可选，用于分钟级数据）
    
    Returns:
        Dict[str, Any]: 包含所有技术指标的字典
    """
    try:
        if data.empty:
            return {}
        
        # 基础技术指标
        if period is not None:
            indicators = calculate_minute_indicators(data, period)
        else:
            indicators = calculate_technical_indicators(data)
        
        # 布林带
        bb_indicators = calculate_bollinger_bands(data)
        indicators.update(bb_indicators)
        
        # ATR
        indicators['atr'] = calculate_atr(data)
        
        # 随机指标
        stoch_indicators = calculate_stochastic(data)
        indicators.update(stoch_indicators)
        
        # 威廉指标
        indicators['williams_r'] = calculate_williams_r(data)
        
        # CCI
        indicators['cci'] = calculate_cci(data)
        
        # 动量指标
        indicators['momentum'] = calculate_momentum(data)
        
        # ROC
        indicators['roc'] = calculate_roc(data)
        
        # OBV
        indicators['obv'] = calculate_obv(data)
        
        return indicators
        
    except Exception as e:
        logger.error(f"获取所有技术指标时出错: {str(e)}")
        return {}