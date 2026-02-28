"""
分钟级数据分析模块
支持1/5/15/30/60分钟周期的股票数据分析
"""

import pandas as pd
import numpy as np
import akshare as ak
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from .utils import logger
from .constants import *

class MinuteAnalyzer:
    """分钟级数据分析器"""
    
    SUPPORTED_PERIODS = [1, 5, 15, 30, 60]
    
    def __init__(self, period: int = 5, use_simulation: bool = False):
        """
        初始化分钟级分析器
        
        Args:
            period: 分钟周期，支持1/5/15/30/60
            use_simulation: 当真实分钟数据不可用时，是否使用日线数据模拟
        """
        if period not in self.SUPPORTED_PERIODS:
            raise ValueError(f"不支持的分钟周期: {period}，支持的周期: {self.SUPPORTED_PERIODS}")
        
        self.period = period
        self.max_days = 5 if period == 1 else 30  # 1分钟数据最多5天，其他可以30天
        self.use_simulation = use_simulation
        
    def get_minute_data(self, stock_code: str, days: int = 5) -> Optional[pd.DataFrame]:
        """
        获取分钟级数据。
        优先尝试真实分钟数据；当 use_simulation=True 时，失败则使用日线模拟。
        """
        try:
            # 限制获取天数（避免超大范围）
            if self.period == 1 and days > 5:
                days = 5
            elif days > self.max_days:
                days = self.max_days

            # 尝试真实分钟数据
            data = self._try_get_minute_data_primary(stock_code, days)
            if data is not None and not data.empty:
                return data

            # 根据配置决定是否使用模拟数据
            if self.use_simulation:
                logger.warning(f"分钟级数据获取失败，使用降级策略为股票 {stock_code} 生成模拟{self.period}分钟数据")
                data = self._get_fallback_data(stock_code, days)
                if data is not None and not data.empty:
                    logger.info(f"成功获取股票 {stock_code} 的{self.period}分钟数据，共{len(data)}条记录")
                return data
            else:
                logger.warning(f"分钟级数据获取失败且已禁用模拟，跳过 {stock_code}")
                return None

        except Exception as e:
            logger.error(f"获取股票 {stock_code} 分钟数据时发生错误: {str(e)}")
            return None
    
    def _try_get_minute_data_primary(self, stock_code: str, days: int) -> Optional[pd.DataFrame]:
        """
        尝试获取分钟级数据的主要方法
        """
        try:
            # 使用akshare获取分钟数据
            data = ak.stock_zh_a_hist_min_em(
                symbol=stock_code,
                period=str(self.period),
                start_date=(datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S'),
                end_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
            
            if data.empty:
                return None
                
            # 标准化列名
            data.columns = ['datetime', 'open', 'close', 'high', 'low', 'volume', 'amount']
            
            # 转换数据类型
            data['datetime'] = pd.to_datetime(data['datetime'])
            for col in ['open', 'close', 'high', 'low', 'volume', 'amount']:
                data[col] = pd.to_numeric(data[col], errors='coerce')
            
            # 设置索引
            data.set_index('datetime', inplace=True)
            
            # 过滤掉非交易时间的数据
            data = self._filter_trading_hours(data)
            
            logger.info(f"成功获取股票 {stock_code} 的{self.period}分钟数据，共{len(data)}条记录")
            return data
            
        except Exception as e:
            logger.debug(f"主要分钟数据获取方法失败: {str(e)}")
            return None
    
    def _get_fallback_data(self, stock_code: str, days: int) -> Optional[pd.DataFrame]:
        """
        降级策略：使用日线数据模拟分钟级数据
        """
        try:
            # 导入日线数据获取函数
            from .data_sources import get_historical_data
            
            # 计算需要的日期范围
            end_date = datetime.now().strftime('%Y%m%d')
            start_date = (datetime.now() - timedelta(days=days+5)).strftime('%Y%m%d')  # 多取几天确保有足够数据
            
            # 获取日线数据
            daily_data = get_historical_data(stock_code, start_date, end_date)
            if daily_data is None or daily_data.empty:
                logger.warning(f"无法获取股票 {stock_code} 的日线数据作为降级方案")
                return None
            
            # 使用最近的日线数据模拟分钟级数据
            minute_data = self._simulate_minute_data_from_daily(daily_data, stock_code)
            
            if minute_data is not None and not minute_data.empty:
                logger.info(f"使用日线数据成功模拟股票 {stock_code} 的{self.period}分钟数据，共{len(minute_data)}条记录")
            
            return minute_data
            
        except Exception as e:
            logger.error(f"降级策略失败: {str(e)}")
            return None
    
    def _simulate_minute_data_from_daily(self, daily_data: pd.DataFrame, stock_code: str) -> Optional[pd.DataFrame]:
        """
        从日线数据模拟分钟级数据 - 优化版本
        """
        try:
            if daily_data.empty:
                return None
            
            # 只取最近的2天数据，减少计算量
            recent_data = daily_data.tail(min(2, len(daily_data)))
            
            minute_records = []
            
            for _, day_row in recent_data.iterrows():
                # 简化日期处理（使用 pandas 安全解析，避免对 Hashable/NaTType 直接访问属性）
                try:
                    ts = pd.to_datetime(day_row.name, errors='coerce')
                    if pd.isna(ts):
                        continue  # 跳过无效日期
                    date_str = ts.strftime('%Y-%m-%d')
                except Exception:
                    continue  # 跳过无效日期
                
                # 获取价格数据
                open_price = float(day_row.get('open', 0) or 0)
                close_price = float(day_row.get('close', 0) or 0)
                high_price = float(day_row.get('high', 0) or 0)
                low_price = float(day_row.get('low', 0) or 0)
                volume = float(day_row.get('volume', 0) or 0)
                
                if open_price <= 0 or close_price <= 0:
                    continue  # 跳过无效数据
                
                # 简化：只生成几个关键时间点，而不是所有分钟
                key_times = self._generate_key_trading_times(date_str)
                
                # 简化价格计算
                price_step = (close_price - open_price) / max(1, len(key_times) - 1)
                volume_per_point = volume / len(key_times) if len(key_times) > 0 else 0
                
                for i, time_point in enumerate(key_times):
                    price = open_price + price_step * i
                    minute_records.append({
                        'datetime': pd.to_datetime(time_point),
                        'open': price,
                        'close': price,
                        'high': price * 1.002,  # 简单的高低价
                        'low': price * 0.998,
                        'volume': volume_per_point,
                        'amount': volume_per_point * price
                    })
            
            if not minute_records:
                return None
            
            # 创建DataFrame
            minute_df = pd.DataFrame(minute_records)
            minute_df.set_index('datetime', inplace=True)
            minute_df = minute_df.sort_index()
            
            return minute_df
            
        except Exception as e:
            logger.error(f"模拟分钟数据失败: {str(e)}")
            return None
    
    def _generate_key_trading_times(self, date_str: str) -> List[str]:
        """
        生成关键交易时间点 - 简化版本，只生成少量时间点
        """
        times = []
        
        try:
            # 根据period生成不同数量的时间点
            if self.period >= 60:
                # 60分钟：只生成4个时间点
                times = [
                    f"{date_str} 09:30:00",
                    f"{date_str} 10:30:00", 
                    f"{date_str} 13:30:00",
                    f"{date_str} 14:30:00"
                ]
            elif self.period >= 30:
                # 30分钟：生成8个时间点
                times = [
                    f"{date_str} 09:30:00", f"{date_str} 10:00:00",
                    f"{date_str} 10:30:00", f"{date_str} 11:00:00",
                    f"{date_str} 13:00:00", f"{date_str} 13:30:00",
                    f"{date_str} 14:00:00", f"{date_str} 14:30:00"
                ]
            else:
                # 其他：生成12个时间点
                times = [
                    f"{date_str} 09:30:00", f"{date_str} 09:45:00",
                    f"{date_str} 10:00:00", f"{date_str} 10:15:00",
                    f"{date_str} 10:30:00", f"{date_str} 10:45:00",
                    f"{date_str} 11:00:00", f"{date_str} 11:15:00",
                    f"{date_str} 13:00:00", f"{date_str} 13:30:00",
                    f"{date_str} 14:00:00", f"{date_str} 14:30:00"
                ]
        except:
            # 如果出错，返回最简单的时间点
            times = [f"{date_str} 10:00:00", f"{date_str} 14:00:00"]
        
        return times
    
    def _generate_trading_times(self, date_str: str) -> List[str]:
        """
        生成交易时间点
        """
        times = []
        
        # 上午交易时间 9:30-11:30
        current_time = datetime.strptime(f"{date_str} 09:30:00", '%Y-%m-%d %H:%M:%S')
        end_morning = datetime.strptime(f"{date_str} 11:30:00", '%Y-%m-%d %H:%M:%S')
        
        while current_time <= end_morning:
            times.append(current_time.strftime('%Y-%m-%d %H:%M:%S'))
            current_time += timedelta(minutes=self.period)
        
        # 下午交易时间 13:00-15:00
        current_time = datetime.strptime(f"{date_str} 13:00:00", '%Y-%m-%d %H:%M:%S')
        end_afternoon = datetime.strptime(f"{date_str} 15:00:00", '%Y-%m-%d %H:%M:%S')
        
        while current_time <= end_afternoon:
            times.append(current_time.strftime('%Y-%m-%d %H:%M:%S'))
            current_time += timedelta(minutes=self.period)
        
        return times
    
    def _generate_price_sequence(self, open_price: float, close_price: float, 
                               high_price: float, low_price: float, num_points: int) -> List[float]:
        """
        生成价格序列
        """
        if num_points <= 0:
            return []
        
        if num_points == 1:
            return [close_price]
        
        # 简单的线性插值
        price_diff = close_price - open_price
        step = price_diff / (num_points - 1)
        
        prices = []
        for i in range(num_points):
            base_price = open_price + step * i
            # 添加小幅随机波动，但保持在合理范围内
            price_range = max(high_price - low_price, abs(close_price - open_price)) * 0.1
            if price_range > 0:
                random_factor = (np.random.random() - 0.5) * 2 * price_range * 0.1
                price = max(low_price * 0.99, min(high_price * 1.01, base_price + random_factor))
            else:
                price = base_price
            prices.append(price)
        
        return prices
    
    def _filter_trading_hours(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        过滤非交易时间的数据
        A股交易时间：9:30-11:30, 13:00-15:00
        """
        try:
            # 确保索引为 DatetimeIndex
            if not isinstance(data.index, pd.DatetimeIndex):
                data = data.copy()
                data.index = pd.to_datetime(data.index, errors='coerce')
                # 去除无法解析为时间的索引
                data = data[~data.index.isna()]
            
            if data.empty:
                return data

            data = data.sort_index()

            # 过滤周末（使用 dayofweek，避免静态检查器对 weekday 的抱怨）
            weekday_mask = data.index.dayofweek < 5
            data = data[weekday_mask]

            if data.empty:
                return data

            # 使用 between_time 过滤交易时间，兼容 pandas 2.1+ 的 inclusive 参数
            try:
                morning = data.between_time('09:30', '11:30', inclusive='both')
                afternoon = data.between_time('13:00', '15:00', inclusive='both')
            except TypeError:
                # 兼容旧版本 pandas
                morning = data.between_time('09:30', '11:30', include_start=True, include_end=True)
                afternoon = data.between_time('13:00', '15:00', include_start=True, include_end=True)

            filtered = pd.concat([morning, afternoon]).sort_index()
            return filtered
            
        except Exception as e:
            logger.warning(f"过滤交易时间数据时出错: {str(e)}")
            return data
    
    def calculate_minute_indicators(self, data: pd.DataFrame) -> Dict[str, pd.Series]:
        """
        计算分钟级技术指标
        根据数据量动态调整指标参数，并集成更多技术指标
        
        Args:
            data: 分钟级历史数据
            
        Returns:
            Dict: 技术指标字典
        """
        try:
            if data.empty:
                return {}
            
            data_length = len(data)
            
            # 根据分钟周期和数据量调整指标参数
            if self.period == 1:
                # 1分钟数据，使用较短的参数
                ma_periods = [5, 10, 20] if data_length >= 20 else [3, 5, min(10, data_length-1)]
                macd_fast, macd_slow, macd_signal = (6, 12, 4) if data_length >= 15 else (3, 6, 2)
                kdj_period = min(9, data_length-1)
                rsi_period = min(14, data_length-1)
                bb_window = min(20, data_length-1)
                atr_window = min(14, data_length-1)
            elif self.period == 5:
                # 5分钟数据
                ma_periods = [10, 20, 60] if data_length >= 60 else [5, 10, min(30, data_length-1)]
                macd_fast, macd_slow, macd_signal = (12, 26, 9) if data_length >= 30 else (6, 12, 4)
                kdj_period = min(14, data_length-1)
                rsi_period = min(14, data_length-1)
                bb_window = min(20, data_length-1)
                atr_window = min(14, data_length-1)
            elif self.period in [15, 30]:
                # 15/30分钟数据
                ma_periods = [20, 60, 120] if data_length >= 120 else [10, 20, min(60, data_length-1)]
                macd_fast, macd_slow, macd_signal = (12, 26, 9)
                kdj_period = min(14, data_length-1)
                rsi_period = min(14, data_length-1)
                bb_window = min(20, data_length-1)
                atr_window = min(14, data_length-1)
            else:  # 60分钟
                # 60分钟数据，接近日线参数
                ma_periods = [5, 10, 20] if data_length >= 20 else [3, 5, min(10, data_length-1)]
                macd_fast, macd_slow, macd_signal = (12, 26, 9)
                kdj_period = min(9, data_length-1)
                rsi_period = min(14, data_length-1)
                bb_window = min(20, data_length-1)
                atr_window = min(14, data_length-1)
            
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
            
            # 计算布林带
            middle_band = data['close'].rolling(window=bb_window).mean()
            std = data['close'].rolling(window=bb_window).std()
            data['bb_upper'] = middle_band + (std * 2.0)
            data['bb_middle'] = middle_band
            data['bb_lower'] = middle_band - (std * 2.0)
            data['bb_width'] = (data['bb_upper'] - data['bb_lower']) / middle_band * 100
            
            # 计算ATR（平均真实波幅）
            high_low = data['high'] - data['low']
            high_close_prev = abs(data['high'] - data['close'].shift(1))
            low_close_prev = abs(data['low'] - data['close'].shift(1))
            true_range = pd.concat([high_low, high_close_prev, low_close_prev], axis=1).max(axis=1)
            data['atr'] = true_range.rolling(window=atr_window).mean()
            
            # 计算动量指标
            momentum_window = min(10, data_length-1)
            if momentum_window > 0:
                data['momentum'] = data['close'] / data['close'].shift(momentum_window) * 100
            else:
                data['momentum'] = pd.Series([100] * len(data), index=data.index)
            
            # 计算OBV（能量潮）
            price_change = data['close'].diff()
            obv_volume = data['volume'].copy()
            obv_volume[price_change < 0] = -obv_volume[price_change < 0]
            obv_volume[price_change == 0] = 0
            data['obv'] = obv_volume.cumsum()
            
            return {
                'ma5': data['ma5'],
                'ma10': data['ma10'],
                'ma20': data['ma20'],
                'dif': data['dif'],
                'dea': data['dea'],
                'macd': data['macd'],
                'k': data['k'],
                'd': data['d'],
                'j': data['j'],
                'rsi': data['rsi'],
                'volume_ma': data['volume_ma'],
                'bb_upper': data['bb_upper'],
                'bb_middle': data['bb_middle'],
                'bb_lower': data['bb_lower'],
                'bb_width': data['bb_width'],
                'atr': data['atr'],
                'momentum': data['momentum'],
                'obv': data['obv']
            }
            
        except Exception as e:
            logger.error(f"计算{self.period}分钟技术指标时出错: {str(e)}")
            return {}
    
    def calculate_minute_score(self, data: pd.DataFrame, indicators: Dict) -> float:
        """
        计算分钟级股票评分 - 优化版
        针对短周期数据调整评分标准，增加动量分析和趋势强度评估
        集成布林带突破分析、成交量异动检测、动量持续性分析
        
        Args:
            data: 分钟级历史数据
            indicators: 技术指标
            
        Returns:
            float: 评分 (0-100)
        """
        try:
            if data.empty or not indicators or len(data) < 5:
                return 0.0
            
            # 优化后的分钟级评分权重 - 增加新指标权重
            if self.period == 1:
                # 1分钟数据：极度注重短期动量和技术信号
                weights = {'macd': 0.20, 'kdj': 0.20, 'rsi': 0.12, 'ma': 0.12, 'volume': 0.08, 
                          'momentum': 0.10, 'bollinger': 0.10, 'atr': 0.08}
            elif self.period == 5:
                # 5分钟数据：平衡技术指标和动量，推荐使用
                weights = {'macd': 0.16, 'kdj': 0.16, 'rsi': 0.12, 'ma': 0.16, 'volume': 0.08, 
                          'momentum': 0.12, 'bollinger': 0.12, 'atr': 0.08}
            elif self.period == 15:
                # 15分钟数据：注重趋势和动量持续性，推荐使用
                weights = {'macd': 0.14, 'kdj': 0.14, 'rsi': 0.12, 'ma': 0.20, 'volume': 0.10, 
                          'momentum': 0.10, 'bollinger': 0.12, 'atr': 0.08}
            elif self.period == 30:
                # 30分钟数据：更注重趋势分析
                weights = {'macd': 0.12, 'kdj': 0.12, 'rsi': 0.12, 'ma': 0.24, 'volume': 0.12, 
                          'momentum': 0.08, 'bollinger': 0.14, 'atr': 0.10}
            else:  # 60分钟
                # 60分钟数据：接近日线分析，注重趋势确认
                weights = {'macd': 0.12, 'kdj': 0.12, 'rsi': 0.12, 'ma': 0.24, 'volume': 0.12, 
                          'momentum': 0.08, 'bollinger': 0.14, 'atr': 0.10}
            
            total_score = 0.0
            latest_price = data['close'].iloc[-1]
            
            # 1. MACD指标评分 - 增加趋势强度评估
            macd_score = 0
            if not indicators['macd'].empty and len(indicators['macd']) >= 2:
                macd_value = indicators['macd'].iloc[-1]
                if macd_value > 0:
                    macd_score += 8  # 金叉状态
                    # MACD柱状图强度
                    if len(indicators['macd']) > 5 and macd_value > indicators['macd'].iloc[-2]:
                        macd_score += 4  # 柱状图放大
                
                # MACD趋势确认
                if len(indicators['macd']) > 3 and all(indicators['macd'].iloc[-3:] > 0):
                    macd_score += 6  # 持续金叉
            
            # MACD信号线交叉
            if (len(data) > 1 and not indicators['dif'].empty and not indicators['dea'].empty and
                len(indicators['dif']) >= 2 and len(indicators['dea']) >= 2 and
                indicators['dif'].iloc[-1] > indicators['dea'].iloc[-1] and 
                indicators['dif'].iloc[-2] <= indicators['dea'].iloc[-2]):
                macd_score += 8  # 信号线金叉
            
            total_score += macd_score * weights['macd']
            
            # 2. KDJ指标评分 - 优化超买超卖判断
            kdj_score = 0
            if not indicators['k'].empty and not indicators['d'].empty and len(indicators['k']) >= 2 and len(indicators['d']) >= 2:
                k_value = indicators['k'].iloc[-1]
                d_value = indicators['d'].iloc[-1]
                
                # 超卖区域
                if k_value < 20 and d_value < 20:
                    kdj_score += 12  # 强烈超卖
                elif k_value < 30 and d_value < 30:
                    kdj_score += 8   # 超卖
                
                # KDJ金叉
                if k_value > d_value and indicators['k'].iloc[-2] <= indicators['d'].iloc[-2]:
                    kdj_score += 8
                
                # J值超卖
                if not indicators['j'].empty and len(indicators['j']) >= 1 and indicators['j'].iloc[-1] < 10:
                    kdj_score += 6
            
            total_score += kdj_score * weights['kdj']
            
            # 3. RSI指标评分 - 更精细的分级
            rsi_score = 0
            if not indicators['rsi'].empty and len(indicators['rsi']) >= 1:
                rsi = indicators['rsi'].iloc[-1]
                if rsi < 20:
                    rsi_score = 25  # 极度超卖
                elif rsi < 30:
                    rsi_score = 18  # 超卖
                elif rsi < 40:
                    rsi_score = 12  # 偏弱
                elif rsi < 50:
                    rsi_score = 8   # 中性偏弱
                elif rsi < 60:
                    rsi_score = 5   # 中性偏强
                
                # RSI趋势
                if len(indicators['rsi']) >= 3 and rsi > indicators['rsi'].iloc[-2] > indicators['rsi'].iloc[-3]:
                    rsi_score += 6  # RSI上升趋势
            
            total_score += rsi_score * weights['rsi']
            
            # 4. 均线系统评分 - 增加趋势强度评估
            ma_score = 0
            
            # 均线多头排列
            if (not indicators['ma5'].empty and not indicators['ma10'].empty and 
                not indicators['ma20'].empty and len(indicators['ma5']) >= 1 and 
                len(indicators['ma10']) >= 1 and len(indicators['ma20']) >= 1 and
                indicators['ma5'].iloc[-1] > indicators['ma10'].iloc[-1] > indicators['ma20'].iloc[-1]):
                ma_score += 15  # 强烈多头排列
            
            # 价格相对于均线位置
            if not indicators['ma5'].empty and len(indicators['ma5']) >= 1 and latest_price > indicators['ma5'].iloc[-1]:
                ma_score += 6
            if not indicators['ma10'].empty and len(indicators['ma10']) >= 1 and latest_price > indicators['ma10'].iloc[-1]:
                ma_score += 5
            if not indicators['ma20'].empty and len(indicators['ma20']) >= 1 and latest_price > indicators['ma20'].iloc[-1]:
                ma_score += 4
            
            # 均线趋势强度
            if (not indicators['ma5'].empty and not indicators['ma10'].empty and 
                len(indicators['ma5']) >= 3 and len(indicators['ma10']) >= 3 and
                all(indicators['ma5'].iloc[-3:] > indicators['ma10'].iloc[-3:])):
                ma_score += 8  # 短期均线持续在上
            
            total_score += ma_score * weights['ma']
            
            # 5. 成交量分析评分 - 增加量价关系分析和OBV指标
            vol_score = 0
            if not indicators['volume_ma'].empty and len(indicators['volume_ma']) >= 1:
                current_volume = data['volume'].iloc[-1]
                volume_ma = indicators['volume_ma'].iloc[-1]
                
                if current_volume > volume_ma * 1.5:
                    vol_score += 12  # 显著放量
                elif current_volume > volume_ma:
                    vol_score += 8   # 温和放量
                
                # 量价齐升
                if len(data) > 1 and current_volume > data['volume'].iloc[-2] and latest_price > data['close'].iloc[-2]:
                    vol_score += 6
            
            # 成交量趋势
            if len(data) >= 3:
                try:
                    if (data['volume'].iloc[-1] > data['volume'].iloc[-2] > data['volume'].iloc[-3] and
                        data['close'].iloc[-1] > data['close'].iloc[-2] > data['close'].iloc[-3]):
                        vol_score += 10  # 量价齐升趋势
                except IndexError:
                    pass
            
            # OBV指标分析
            if not indicators['obv'].empty and len(indicators['obv']) >= 3:
                obv_current = indicators['obv'].iloc[-1]
                obv_prev = indicators['obv'].iloc[-2]
                obv_prev2 = indicators['obv'].iloc[-3]
                
                if obv_current > obv_prev > obv_prev2:
                    vol_score += 8  # OBV持续上升
                elif obv_current > obv_prev and latest_price > data['close'].iloc[-2]:
                    vol_score += 5  # OBV与价格同步上升
            
            total_score += vol_score * weights['volume']
            
            # 6. 动量指标评分 - 优化动量分析
            momentum_score = 0
            if len(data) >= 5:
                # 短期动量（最近3个周期）
                short_momentum = (latest_price / data['close'].iloc[-3] - 1) * 100
                
                # 中期动量（最近10个周期，如果数据足够）
                mid_momentum = 0
                if len(data) >= 10:
                    mid_momentum = (latest_price / data['close'].iloc[-10] - 1) * 100
                
                # 动量评分
                if short_momentum > 2.0:  # 短期强势
                    momentum_score += 15
                elif short_momentum > 1.0:
                    momentum_score += 10
                
                if mid_momentum > 5.0:  # 中期强势
                    momentum_score += 12
                elif mid_momentum > 3.0:
                    momentum_score += 8
                
                # 动量加速
                if len(data) >= 6 and short_momentum > mid_momentum:
                    momentum_score += 8
                
                # 动量持续性
                if len(data) >= 8:
                    momentum_trend = [
                        (data['close'].iloc[-1] / data['close'].iloc[-2] - 1) * 100,
                        (data['close'].iloc[-2] / data['close'].iloc[-3] - 1) * 100,
                        (data['close'].iloc[-3] / data['close'].iloc[-4] - 1) * 100
                    ]
                    if all(m > 0 for m in momentum_trend):
                        momentum_score += 6  # 连续上涨
                    elif all(m < 0 for m in momentum_trend):
                        momentum_score -= 5  # 连续下跌
            
            total_score += momentum_score * weights['momentum']
            
            # 7. 布林带突破分析评分
            bollinger_score = 0
            if (not indicators['bb_upper'].empty and not indicators['bb_lower'].empty and 
                len(indicators['bb_upper']) >= 1 and len(indicators['bb_lower']) >= 1):
                
                bb_upper = indicators['bb_upper'].iloc[-1]
                bb_lower = indicators['bb_lower'].iloc[-1]
                bb_middle = indicators['bb_middle'].iloc[-1]
                
                # 布林带突破
                if latest_price > bb_upper:
                    bollinger_score += 12  # 突破上轨
                elif latest_price < bb_lower:
                    bollinger_score += 8   # 突破下轨
                
                # 布林带宽度分析
                if not indicators['bb_width'].empty and len(indicators['bb_width']) >= 2:
                    bb_width_current = indicators['bb_width'].iloc[-1]
                    bb_width_prev = indicators['bb_width'].iloc[-2]
                    
                    if bb_width_current > bb_width_prev:
                        bollinger_score += 6  # 布林带扩张
                    elif bb_width_current < bb_width_prev:
                        bollinger_score += 4  # 布林带收缩
                
                # 价格相对于中轨位置
                if latest_price > bb_middle:
                    bollinger_score += 5
                
                # 布林带挤压（低波动率机会）
                if not indicators['bb_width'].empty and len(indicators['bb_width']) >= 1:
                    if indicators['bb_width'].iloc[-1] < 5.0:  # 宽度小于5%
                        bollinger_score += 8  # 低波动率机会
            
            total_score += bollinger_score * weights['bollinger']
            
            # 8. ATR波动率风险调整评分
            atr_score = 0
            if not indicators['atr'].empty and len(indicators['atr']) >= 1:
                atr_value = indicators['atr'].iloc[-1]
                atr_percent = atr_value / latest_price * 100 if latest_price > 0 else 0
                
                # ATR相对风险评估
                if atr_percent < 1.0:
                    atr_score += 10  # 低波动，稳定性好
                elif atr_percent < 2.0:
                    atr_score += 8   # 中等偏低波动
                elif atr_percent < 3.0:
                    atr_score += 5   # 中等波动
                elif atr_percent < 4.0:
                    atr_score += 3   # 中等偏高波动
                else:
                    atr_score -= 5   # 高波动，风险较大
                
                # ATR趋势
                if len(indicators['atr']) >= 3:
                    atr_trend = [
                        indicators['atr'].iloc[-1],
                        indicators['atr'].iloc[-2],
                        indicators['atr'].iloc[-3]
                    ]
                    if atr_trend[0] > atr_trend[1] > atr_trend[2]:
                        atr_score -= 3  # 波动率上升趋势
                    elif atr_trend[0] < atr_trend[1] < atr_trend[2]:
                        atr_score += 3  # 波动率下降趋势
            
            total_score += atr_score * weights['atr']
            
            # 增强风险调整机制 - 加入最大回撤和流动性考量
            if len(data) >= 10:
                # 计算波动率（使用更精确的方法）
                returns = data['close'].pct_change().dropna()
                if len(returns) > 0:
                    volatility = returns.std()
                    
                    # 计算最大回撤
                    max_drawdown = 0.0
                    peak = data['close'].iloc[0]
                    for price in data['close']:
                        if price > peak:
                            peak = price
                        else:
                            drawdown = (peak - price) / peak
                            if drawdown > max_drawdown:
                                max_drawdown = drawdown
                    
                    # 计算流动性指标（平均成交量相对于市值的比例）
                    avg_volume = data['volume'].mean()
                    # 假设平均市值为50亿（可根据实际情况调整或从外部获取）
                    avg_market_cap = 5_000_000_000
                    liquidity_ratio = avg_volume / (avg_market_cap / data['close'].mean()) if avg_market_cap > 0 else 0
                    
                    # 动态风险调整 - 综合考虑波动率、最大回撤和流动性
                    risk_adjustment = 1.0
                    
                    # 波动率调整
                    if volatility > 0.04:  # 极高波动（>4%）
                        risk_adjustment *= 0.80
                    elif volatility > 0.03:  # 高波动（3-4%）
                        risk_adjustment *= 0.88
                    elif volatility > 0.02:  # 中等偏高波动（2-3%）
                        risk_adjustment *= 0.94
                    elif volatility > 0.015:  # 中等波动（1.5-2%）
                        risk_adjustment *= 0.98
                    elif volatility > 0.01:  # 中等偏低波动（1-1.5%）
                        risk_adjustment *= 1.02
                    elif volatility > 0.005:  # 低波动（0.5-1%）
                        risk_adjustment *= 1.06
                    else:  # 极低波动（<0.5%）
                        risk_adjustment *= 1.12
                    
                    # 最大回撤调整
                    if max_drawdown > 0.15:  # 回撤超过15%
                        risk_adjustment *= 0.85
                    elif max_drawdown > 0.10:  # 回撤10-15%
                        risk_adjustment *= 0.92
                    elif max_drawdown > 0.05:  # 回撤5-10%
                        risk_adjustment *= 0.97
                    elif max_drawdown < 0.02:  # 回撤小于2%
                        risk_adjustment *= 1.08
                    
                    # 流动性调整
                    if liquidity_ratio < 0.0001:  # 极低流动性
                        risk_adjustment *= 0.85
                    elif liquidity_ratio < 0.0005:  # 低流动性
                        risk_adjustment *= 0.92
                    elif liquidity_ratio < 0.001:  # 中等偏低流动性
                        risk_adjustment *= 0.97
                    elif liquidity_ratio > 0.005:  # 高流动性
                        risk_adjustment *= 1.05
                    elif liquidity_ratio > 0.002:  # 中等偏高流动性
                        risk_adjustment *= 1.02
                    
                    # 记录风险指标信息
                    logger.info(f"风险指标 - 波动率: {volatility:.4f}, 最大回撤: {max_drawdown:.4f}, "
                               f"流动性比率: {liquidity_ratio:.6f}, 风险调整系数: {risk_adjustment:.3f}")
                    
                    total_score *= risk_adjustment
            
            # 确保评分在合理范围内
            total_score = max(0, min(total_score, 100))
            
            # 记录使用的指标信息
            used_indicators = []
            if macd_score > 0: used_indicators.append('MACD')
            if kdj_score > 0: used_indicators.append('KDJ')
            if rsi_score > 0: used_indicators.append('RSI')
            if ma_score > 0: used_indicators.append('MA')
            if vol_score > 0: used_indicators.append('Volume')
            if momentum_score > 0: used_indicators.append('Momentum')
            if bollinger_score > 0: used_indicators.append('Bollinger')
            if atr_score > 0: used_indicators.append('ATR')
            
            if used_indicators:
                logger.info(f"{self.period}分钟评分使用指标: {', '.join(used_indicators)}")
            
            return round(total_score, 2)
            
        except Exception as e:
            logger.error(f"计算{self.period}分钟评分时出错: {str(e)}")
            return 0.0
    
    def analyze_stock_minute(self, stock_code: str, stock_name: str, days: int = 5) -> Optional[Dict]:
        """
        分析单只股票的分钟级数据
        
        Args:
            stock_code: 股票代码
            stock_name: 股票名称
            days: 分析天数
            
        Returns:
            Dict: 分析结果
        """
        try:
            # 获取分钟级数据
            data = self.get_minute_data(stock_code, days)
            if data is None or data.empty:
                return None
            
            # 计算技术指标
            indicators = self.calculate_minute_indicators(data)
            if not indicators:
                return None
            
            # 计算评分
            score = self.calculate_minute_score(data, indicators)
            
            # 计算涨跌幅
            if len(data) > 1:
                price_change = ((data['close'].iloc[-1] - data['close'].iloc[0]) / data['close'].iloc[0] * 100)
            else:
                price_change = 0.0
            
            # 构建分析结果（与主程序格式兼容）
            result = {
                '代码': stock_code,
                '名称': stock_name,
                '总市值（亿元）': 'N/A',  # 分钟级数据不包含市值信息
                '起始日价（元）': round(data['close'].iloc[0], 2) if len(data) > 0 else 0,
                '截止日价（元）': round(data['close'].iloc[-1], 2) if len(data) > 0 else 0,
                '交易所': 'SH' if str(stock_code).startswith('6') else 'SZ',
                '得分': score,
                '详情': f"{self.period}分钟数据 - 涨跌幅: {round(price_change, 2)}% - 数据量: {len(data)}条"
            }
            
            return result
            
        except Exception as e:
            logger.error(f"分析股票 {stock_code} 的{self.period}分钟数据时出错: {str(e)}")
            return None


def get_supported_periods() -> List[int]:
    """获取支持的分钟周期列表"""
    return MinuteAnalyzer.SUPPORTED_PERIODS


def create_minute_analyzer(period: int, use_simulation: bool = False) -> MinuteAnalyzer:
    """创建分钟级分析器实例"""
    return MinuteAnalyzer(period, use_simulation=use_simulation)