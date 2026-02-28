"""
图表生成模块

提供股票技术分析图表生成和样式设置功能
"""

import os
import io
import sys
import platform
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import font_manager as fm
from mplfinance.original_flavor import candlestick_ohlc
from typing import Dict, Optional, Any
from modules.utils import logger
from modules.constants import *


def set_plot_style() -> None:
    """设置Matplotlib的绘图样式，包括字体、网格、线条宽度等参数"""
    # 使用默认样式
    plt.style.use('default')
    
    # 设置中文字体（跨平台稳健检测）
    system = platform.system()

    # 常见中文字体候选列表（优先级从高到低）
    candidates = [
        'PingFang SC',            # macOS 默认中文字体
        'Hiragino Sans GB',       # macOS 旧款中文字体
        'Noto Sans CJK SC',       # Noto 系中文字体
        'Source Han Sans SC',     # 思源黑体
        'Microsoft YaHei',        # Windows雅黑
        'SimHei',                 # 黑体（可能缺失）
        'Heiti SC',               # macOS 旧黑体
        'Arial Unicode MS',       # 覆盖广，但不一定可用
        'DejaVu Sans',            # 兜底
    ]

    # 在系统字体中查找可用候选
    available = {f.name for f in fm.fontManager.ttflist}
    chosen = None
    for name in candidates:
        if name in available:
            chosen = name
            break
    if not chosen:
        # 兜底列表（某些环境下 fm.name 可能不匹配文件名）
        chosen = 'DejaVu Sans'
    plt.rcParams['font.sans-serif'] = [chosen]
    
    # 用来正常显示负号
    plt.rcParams['axes.unicode_minus'] = False
    
    # 设置字体大小和样式
    plt.rcParams['font.size'] = FONT_SIZE_BASE
    plt.rcParams['axes.titlesize'] = FONT_SIZE_SUBTITLE
    plt.rcParams['axes.titleweight'] = 'bold'
    plt.rcParams['figure.titlesize'] = FONT_SIZE_MAIN_TITLE
    plt.rcParams['figure.titleweight'] = 'bold'
    plt.rcParams['legend.fontsize'] = FONT_SIZE_LEGEND
    plt.rcParams['axes.labelsize'] = FONT_SIZE_LABEL
    
    # 设置坐标轴刻度字体大小
    plt.rcParams['xtick.labelsize'] = FONT_SIZE_TICK
    plt.rcParams['ytick.labelsize'] = FONT_SIZE_TICK
    
    # 设置网格样式
    plt.rcParams['axes.grid'] = True
    plt.rcParams['grid.alpha'] = 0.2
    plt.rcParams['grid.linestyle'] = '--'
    
    # 设置图表布局
    plt.rcParams['figure.constrained_layout.use'] = True
    
    # 设置线条宽度
    plt.rcParams['lines.linewidth'] = LINE_WIDTH
    plt.rcParams['axes.linewidth'] = LINE_WIDTH
    
    # 设置坐标轴样式
    plt.rcParams['axes.linewidth'] = 1.5
    plt.rcParams['axes.labelsize'] = 16
    plt.rcParams['axes.labelweight'] = 'bold'


def draw_candlestick_chart(ax: Any, hist_data: pd.DataFrame, indicators: Dict) -> None:
    """
    绘制K线图和均线
    
    Args:
        ax: matplotlib轴对象
        hist_data: 历史数据
        indicators: 技术指标
    """
    try:
        # 将索引稳健转换为 datetime
        dt_index = pd.to_datetime(hist_data.index, errors='coerce')
        # DatetimeIndex 在静态类型中可能缺少 to_pydatetime 方法声明，这里改用列表推导
        dt_list = dt_index.to_list()
        py_dt_list = [ts.to_pydatetime() if hasattr(ts, 'to_pydatetime') else pd.to_datetime(ts).to_pydatetime() for ts in dt_list]
        hist_data_copy = hist_data.copy()
        hist_data_copy['date_num'] = mdates.date2num(py_dt_list)
        ohlc = hist_data_copy[['date_num', 'open', 'high', 'low', 'close']].values
        candlestick_ohlc(ax, ohlc, width=0.6, colorup='red', colordown='green')
        
        # 添加均线
        ax.plot(hist_data.index, indicators['ma5'], label='MA5', linewidth=1)
        ax.plot(hist_data.index, indicators['ma10'], label='MA10', linewidth=1)
        ax.plot(hist_data.index, indicators['ma20'], label='MA20', linewidth=1)
        ax.legend()
        ax.grid(True)
        
    except Exception as e:
        logger.error(f"绘制K线图时出错: {str(e)}")


def draw_macd_chart(ax: Any, hist_data: pd.DataFrame, indicators: Dict) -> None:
    """
    绘制MACD指标图
    
    Args:
        ax: matplotlib轴对象
        hist_data: 历史数据
        indicators: 技术指标
    """
    try:
        ax.bar(hist_data.index, indicators['macd'], label='MACD')
        ax.plot(hist_data.index, indicators['dif'], label='DIF')
        ax.plot(hist_data.index, indicators['dea'], label='DEA')
        ax.set_title('MACD指标')
        ax.grid(True)
        ax.legend()
        
    except Exception as e:
        logger.error(f"绘制MACD图时出错: {str(e)}")


def draw_kdj_chart(ax: Any, hist_data: pd.DataFrame, indicators: Dict) -> None:
    """
    绘制KDJ指标图
    
    Args:
        ax: matplotlib轴对象
        hist_data: 历史数据
        indicators: 技术指标
    """
    try:
        ax.plot(hist_data.index, indicators['k'], label='K')
        ax.plot(hist_data.index, indicators['d'], label='D')
        ax.plot(hist_data.index, indicators['j'], label='J')
        ax.set_title('KDJ指标')
        ax.grid(True)
        ax.legend()
        
    except Exception as e:
        logger.error(f"绘制KDJ图时出错: {str(e)}")


def draw_rsi_chart(ax: Any, hist_data: pd.DataFrame, indicators: Dict) -> None:
    """
    绘制RSI指标图
    
    Args:
        ax: matplotlib轴对象
        hist_data: 历史数据
        indicators: 技术指标
    """
    try:
        ax.plot(hist_data.index, indicators['rsi'], label='RSI')
        ax.axhline(y=70, color='r', linestyle='--', alpha=0.7, label='超买线')
        ax.axhline(y=30, color='g', linestyle='--', alpha=0.7, label='超卖线')
        ax.set_title('RSI指标')
        ax.grid(True)
        ax.legend()
        
    except Exception as e:
        logger.error(f"绘制RSI图时出错: {str(e)}")


def draw_volume_chart(ax: Any, hist_data: pd.DataFrame, indicators: Dict) -> None:
    """
    绘制成交量图
    
    Args:
        ax: matplotlib轴对象
        hist_data: 历史数据
        indicators: 技术指标
    """
    try:
        ax.bar(hist_data.index, hist_data['volume'], label='成交量', alpha=0.7)
        ax.plot(hist_data.index, indicators['volume_ma5'], label='MA5', color='red')
        ax.set_title('成交量分析')
        ax.grid(True)
        ax.legend()
        
    except Exception as e:
        logger.error(f"绘制成交量图时出错: {str(e)}")


def draw_price_trend_chart(ax: Any, hist_data: pd.DataFrame, indicators: Dict) -> None:
    """
    绘制价格趋势图
    
    Args:
        ax: matplotlib轴对象
        hist_data: 历史数据
        indicators: 技术指标
    """
    try:
        ax.plot(hist_data.index, hist_data['close'], label='收盘价', linewidth=2)
        ax.plot(hist_data.index, indicators['ma5'], label='5日均线', alpha=0.8)
        ax.set_title('价格趋势')
        ax.grid(True)
        ax.legend()
        
    except Exception as e:
        logger.error(f"绘制价格趋势图时出错: {str(e)}")


def draw_volatility_chart(ax: Any, hist_data: pd.DataFrame) -> None:
    """
    绘制波动趋势图
    
    Args:
        ax: matplotlib轴对象
        hist_data: 历史数据
    """
    try:
        daily_return = hist_data['close'].pct_change()
        volatility = daily_return.rolling(5).std()
        ax.plot(hist_data.index, volatility, label='5日波动率', color='orange')
        ax.set_title('波动趋势')
        ax.grid(True)
        ax.legend()
        
    except Exception as e:
        logger.error(f"绘制波动趋势图时出错: {str(e)}")


def generate_single_stock_chart(stock_data: Dict, hist_data: pd.DataFrame, indicators: Dict, output_dir: str) -> str:
    """
    生成单只股票的技术分析图表
    
    Args:
        stock_data: 股票基本信息
        hist_data: 历史数据
        indicators: 技术指标
        output_dir: 输出目录
    
    Returns:
        str: 生成的图表文件路径
    """
    try:
        stock_code = str(stock_data['代码'])
        stock_name = str(stock_data['名称'])
        
        # 创建图表并设置布局
        fig = plt.figure(figsize=(44.70, 35.61))
        
        # 创建网格布局，调整top值给主标题留出足够空间
        gs = fig.add_gridspec(8, 2, height_ratios=[0.5, 2, 1, 1, 1, 1, 1, 1], top=0.95)  # 增加一行用于标题
        
        # 设置整张图的主标题（股票信息）
        title_ax = fig.add_subplot(gs[0, :])
        title_ax.set_axis_off()  # 隐藏坐标轴
        title_ax.text(0.5, 0.5, 
                     f'股票代码:{stock_code} 股票名称:{stock_name} - 起始日价: {stock_data["起始日价（元）"]}元 - 截止日价: {stock_data["截止日价（元）"]}元 - 涨幅: {stock_data["涨幅(%)"]}% - 总市值: {stock_data["总市值（亿元）"]}亿 - 得分: {stock_data["得分"]}分',
                     fontsize=FONT_SIZE_MAIN_TITLE, fontweight='bold', 
                     horizontalalignment='center', verticalalignment='center')
        
        # 计算数据的起始和结束日期
        try:
            date_index = pd.to_datetime(hist_data.index)
            start_date_str = date_index.min().strftime('%Y-%m-%d')
            end_date_str = date_index.max().strftime('%Y-%m-%d')
        except Exception:
            start_date_str = "Unknown"
            end_date_str = "Unknown"

        # 创建并设置K线子图
        ax_k = fig.add_subplot(gs[1, :])
        ax_k.set_title(f'K线图与均线 起始日: {start_date_str}, 截止日: {end_date_str}', pad=20, fontsize=FONT_SIZE_SUBTITLE, fontweight='bold')
        
        # 下方6个子图
        ax_macd = fig.add_subplot(gs[2:4, 0])  # MACD指标
        ax_kdj = fig.add_subplot(gs[2:4, 1])   # KDJ指标
        ax_rsi = fig.add_subplot(gs[4:6, 0])   # RSI指标
        ax_vol = fig.add_subplot(gs[4:6, 1])   # 成交量分析
        ax_trend = fig.add_subplot(gs[6:8, 0])  # 价格趋势
        ax_wave = fig.add_subplot(gs[6:8, 1])   # 波动趋势
        
        # 绘制各个图表
        draw_candlestick_chart(ax_k, hist_data, indicators)
        draw_macd_chart(ax_macd, hist_data, indicators)
        draw_kdj_chart(ax_kdj, hist_data, indicators)
        draw_rsi_chart(ax_rsi, hist_data, indicators)
        draw_volume_chart(ax_vol, hist_data, indicators)
        draw_price_trend_chart(ax_trend, hist_data, indicators)
        draw_volatility_chart(ax_wave, hist_data)
        
        # 设置子图标题
        ax_macd.set_title('MACD指标', fontsize=FONT_SIZE_SUBTITLE, fontweight='bold')
        ax_kdj.set_title('KDJ指标', fontsize=FONT_SIZE_SUBTITLE, fontweight='bold')
        ax_rsi.set_title('RSI指标', fontsize=FONT_SIZE_SUBTITLE, fontweight='bold')
        ax_vol.set_title('成交量分析', fontsize=FONT_SIZE_SUBTITLE, fontweight='bold')
        ax_trend.set_title('价格趋势', fontsize=FONT_SIZE_SUBTITLE, fontweight='bold')
        ax_wave.set_title('波动趋势', fontsize=FONT_SIZE_SUBTITLE, fontweight='bold')
        
        # 保存图表
        output_file = os.path.join(output_dir, f'{stock_code}_{stock_name}_analysis.png')
        plt.savefig(output_file, dpi=100, bbox_inches='tight')
        plt.close()
        
        logger.info(f"已生成 {stock_code} {stock_name} 的技术分析图表")
        return output_file
        
    except Exception as e:
        logger.error(f"生成股票 {stock_data.get('代码', 'Unknown')} 图表时出错: {str(e)}")
        return ""


def generate_stock_charts(stocks: pd.DataFrame, start_date: str, end_date: str, output_dir: str, k_limit: int = 10) -> None:
    """
    生成股票技术分析图表
    
    Args:
        stocks: 股票列表
        start_date: 开始日期
        end_date: 结束日期
        output_dir: 输出目录
        k_limit: 生成图表的股票数量限制
    """
    try:
        # 导入数据获取和技术指标模块
        from modules.data_sources import get_historical_data
        from modules.technical_indicators import get_all_indicators
        
        # 只处理前K只股票
        stocks = stocks.head(k_limit)
        
        for _, stock in stocks.iterrows():
            # 显式转换，避免将 Series 传入下游函数引发类型检查告警
            stock_code = str(stock['代码'])
            stock_name = str(stock['名称'])
            
            # 获取历史数据
            hist_data = get_historical_data(stock_code, start_date, end_date)
            if hist_data.empty:
                continue
                
            # 计算技术指标
            indicators = get_all_indicators(hist_data)
            if not indicators:
                continue
                
            # 生成单只股票的图表
            stock_dict = stock.to_dict()
            generate_single_stock_chart(stock_dict, hist_data, indicators, output_dir)
            
    except Exception as e:
        logger.error(f"生成技术分析图表时出错: {str(e)}")


def setup_chinese_encoding() -> None:
    """设置中文编码环境"""
    try:
        import locale as _locale
        try:
            _locale.setlocale(_locale.LC_ALL, 'zh_CN.UTF-8')
        except Exception:
            try:
                _locale.setlocale(_locale.LC_ALL, 'zh_CN')
            except Exception:
                pass
    except ImportError:
        pass

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def generate_minute_stock_chart(stock_code: str, stock_name: str, minute_df: pd.DataFrame, output_dir: str, period: int) -> str:
    """
    生成分钟级价格与成交量图表（简洁版）

    Args:
        stock_code: 股票代码
        stock_name: 股票名称
        minute_df: 分钟级数据，索引为 datetime，包含 open/high/low/close/volume
        output_dir: 输出目录
        period: 分钟周期（1/5/15/30/60）

    Returns:
        图表文件路径
    """
    try:
        if minute_df is None or minute_df.empty:
            return ""

        # 风格与中文设置
        set_plot_style()

        # 确保索引是 datetime
        df = minute_df.copy()
        df.index = pd.to_datetime(df.index, errors='coerce')
        df = df.sort_index()
        df = df[~df.index.isna()]
        if df.empty:
            return ""

        # 计算简易均线
        ma_short = 5
        ma_long = 10
        df['ma_short'] = df['close'].rolling(ma_short, min_periods=1).mean()
        df['ma_long'] = df['close'].rolling(ma_long, min_periods=1).mean()

        # 绘图
        fig, (ax_price, ax_vol) = plt.subplots(2, 1, figsize=(22, 12), sharex=True)
        fig.suptitle(f"{stock_code} {stock_name} - {period}分钟价格与成交量", fontsize=FONT_SIZE_MAIN_TITLE, fontweight='bold')

        # 价格走势
        ax_price.plot(df.index, df['close'], label='收盘价', linewidth=2)
        ax_price.plot(df.index, df['ma_short'], label=f'MA{ma_short}', alpha=0.8)
        ax_price.plot(df.index, df['ma_long'], label=f'MA{ma_long}', alpha=0.8)
        ax_price.set_ylabel('价格')
        ax_price.legend()
        ax_price.grid(True)

        # 成交量
        ax_vol.bar(df.index, df['volume'], label='成交量', alpha=0.6)
        ax_vol.set_ylabel('成交量')
        ax_vol.grid(True)

        # 时间格式化
        try:
            ax_vol.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
        except Exception:
            pass

        output_file = os.path.join(output_dir, f"{stock_code}_{stock_name}_minute_{period}m.png")
        plt.savefig(output_file, dpi=100, bbox_inches='tight')
        plt.close(fig)
        logger.info(f"已生成 {stock_code} {stock_name} 的 {period} 分钟图表")
        return output_file
    except Exception as e:
        logger.error(f"生成分钟图表时出错: {str(e)}")
        return ""


def generate_minute_charts(stocks: pd.DataFrame, analyzer: Any, days: int, output_dir: str, k_limit: int, period: int) -> None:
    """为前K只股票生成分钟级图表"""
    try:
        if stocks is None or stocks.empty:
            return
        stocks = stocks.head(k_limit)
        for _, row in stocks.iterrows():
            code = str(row.get('代码'))
            name = str(row.get('名称'))
            try:
                df = analyzer.get_minute_data(code, days=days)
                if df is None or df.empty:
                    continue
                generate_minute_stock_chart(code, name, df, output_dir, period)
            except Exception as _e:
                logger.debug(f"生成 {code} {name} 分钟图表时异常：{_e}")
    except Exception as e:
        logger.error(f"批量生成分钟图表时出错: {str(e)}")