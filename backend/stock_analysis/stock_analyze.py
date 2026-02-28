import io
import os
import re
import sys
import time
import shutil
import logging
import argparse
import traceback
import multiprocessing
import glob
import numpy as np
import pandas as pd
import akshare as ak
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib as mpl
import warnings

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple, Union, cast
from concurrent.futures import ThreadPoolExecutor, as_completed  # 添加 ThreadPoolExecutor
from tqdm import tqdm
from matplotlib.figure import Figure
from matplotlib.axes import Axes as MplAxes
from mplfinance.original_flavor import candlestick_ohlc
# 添加 AI 分析相关的导入
from modules.ai_analyzer import get_ai_analysis, save_ai_analysis
from modules.utils import logger
from modules.constants import *
# 添加新模块的导入
from modules.data_sources import (
    load_user_config, precheck_sources, ensure_str_series, 
    extract_six_digit_code, standardize_code_name, 
    stock_spot_em_with_fallback, get_historical_data
)
from modules.technical_indicators import calculate_technical_indicators
from modules.scoring import calculate_stock_score, generate_score_details
from modules.chart_generator import set_plot_style, generate_stock_charts, generate_minute_charts

# ==========================================
# 性能优化：针对 EXE 环境的预加载与路径修复
# ==========================================
if getattr(sys, 'frozen', False):
    try:
        # 1. 修复 SSL 证书路径 (requests/certifi)
        import certifi
        # 在 PyInstaller 打包环境中，certifi.where() 返回的是解压后的临时路径，
        # 显式设置环境变量，避免 requests 每次请求都去查找。
        cert_path = certifi.where()
        if os.path.exists(cert_path):
            os.environ['REQUESTS_CA_BUNDLE'] = cert_path
            os.environ['SSL_CERT_FILE'] = cert_path
        
        # 2. 预加载关键库，避免在多线程中触发 PyInstaller 的 import hook
        # 这对于 akshare 这种重度依赖 lazy import 的库尤为重要
        import py_mini_racer
        import execjs
        import requests.adapters
        import urllib3
        
        # 3. 预加载 akshare 常用模块
        # akshare 内部大量使用了局部 import，这在 EXE 中性能极差
        # 我们必须在此处显式导入它们，以便 PyInstaller 将它们加载到 sys.modules 中
        # 从而避免在多线程运行时触发昂贵的冻结导入器查找
        try:
            # 历史行情
            import akshare.stock_feature.stock_zh_a_hist
            import akshare.stock_feature.stock_zh_a_hist_tx
            import akshare.stock.stock_zh_a_daily
            
            # 实时行情
            import akshare.stock_feature.stock_zh_a_spot_em
            import akshare.stock_feature.stock_zh_a_spot
            import akshare.stock.stock_info
            
            # 财务数据
            import akshare.stock_feature.stock_financial_analysis_indicator
            import akshare.stock.stock_a_lg_indicator
            
            # 其他可能用到的内部模块
            import akshare.utils.request
            import akshare.utils.cons
            
            logger.info("已完成 AkShare 模块预加载")
        except ImportError as e:
            logger.warning(f"预加载 AkShare 模块部分失败: {e}")
            pass
            
    except Exception:
        # 仅记录但不中断，避免环境差异导致崩溃
        pass

warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=pd.errors.SettingWithCopyWarning)

# --- 全局默认值，避免未绑定变量导致的类型告警 ---
args: Any = None
is_historical: bool = False
output_dir: str = ""
isall: bool = False

# 源选择默认值（顺序表示优先级）
DEFAULT_SOURCES = ['eastmoney', 'tencent', 'sina', 'exchange']

# 版本信息
__version__ = '1.6.1'
__author__ = 'sam.wan@qq.com'
__release_date__ = '2026-01-27'

# 设置中文编码环境（更健壮的导入与异常处理）
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

try:
    if sys.stdout and hasattr(sys.stdout, 'buffer'):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    if sys.stderr and hasattr(sys.stderr, 'buffer'):
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
except Exception:
    pass

def analyze_stocks(stock_list: pd.DataFrame, start_date: str, end_date: str, pool_size: int = 8, original_stderr=None, preloaded_data: Optional[pd.DataFrame] = None) -> List[Dict]:
    """
    批量分析股票列表
    
    Args:
        stock_list: 股票列表
        start_date: 开始日期
        end_date: 结束日期
        pool_size: 线程池大小
        original_stderr: 原始标准错误输出流，用于显示进度条
        preloaded_data: 预加载的实时行情数据（可选），避免重复获取
    
    Returns:
        List[Dict]: 包含每只股票分析结果的列表
    """
    # 确保stock_list是DataFrame且包含'代码'和'名称'列
    if not isinstance(stock_list, pd.DataFrame) or not {'代码', '名称'}.issubset(stock_list.columns):
        logger.error("股票列表格式不正确")
        return []
    
    # 过滤掉无效的股票代码（避免 .str 引起的类型分析问题）
    code_series = cast(pd.Series, stock_list['代码'])
    # 使用 apply 生成有效代码掩码，避免潜在 ndarray.map 误用
    valid_mask = code_series.apply(lambda x: bool(re.match(r'^\d{6}$', str(x))))
    # 使用 .loc 并通过 pd.DataFrame 强制结果为 DataFrame，消除联合类型误报
    stock_list = pd.DataFrame(stock_list.loc[valid_mask, :])
    # 明确标注为 DataFrame，避免静态分析认为联合类型
    stock_list = cast(pd.DataFrame, stock_list)
    total = len(stock_list)
    
    if total == 0:
        logger.error("没有有效的股票代码")
        return []
    
    logger.info(f"开始分析 {total} 只股票...")
    
    logger.info(f"使用 {pool_size} 个线程进行并行处理")

    # 优化 EXE 运行环境：添加 _internal 到 PATH 以加速 DLL 查找
    if getattr(sys, 'frozen', False):
        try:
            base_dir = os.path.dirname(sys.executable)
            internal_dir = os.path.join(base_dir, '_internal')
            if os.path.exists(internal_dir):
                os.environ['PATH'] = internal_dir + os.pathsep + os.environ['PATH']
                logger.info(f"已添加 DLL 搜索路径: {internal_dir}")
        except Exception as e:
            logger.warning(f"优化 DLL 搜索路径失败: {e}")
    
    # 使用主流程统一配置的日志处理器（此处不再重复添加）
    # 仍保留 log_file 路径用于提示
    log_file = os.path.join(output_dir, 'analysis.log')
    
    results = []
    
    try:
        # 判断数据类型并输出提示
        if is_historical:
            logger.info("使用历史数据进行分析（注意：历史数据不包含市值信息）")
            current_info = None
        else:
            logger.info("使用实时数据进行分析")
            # 快速模式：跳过实时行情获取，避免东财接口不稳定导致的重试与超时
            # 或者是未启用实时数据
            if getattr(args, 'fast', False) or not getattr(args, 'realtime', False):
                if not getattr(args, 'realtime', False):
                    logger.info("未启用实时数据获取（使用 --realtime 开启）")
                else:
                    logger.info("快速模式：跳过实时行情数据获取")
                current_info = None
            else:
                # 预先获取所有股票的实时行情数据
                try:
                    if preloaded_data is not None and not preloaded_data.empty:
                        logger.info("使用预加载的实时行情数据")
                        current_info = preloaded_data
                    else:
                        current_info = stock_spot_em_with_fallback(original_stderr)
                    
                    # 使用赋值而非 inplace，避免类型分析误报
                    # 确保索引唯一，防止重复代码导致索引错误
                    if current_info is not None:
                        current_info = current_info.drop_duplicates(subset=['代码'])
                        current_info = current_info.set_index('代码')
                    logger.info("获取实时行情数据成功")
                except Exception as e:
                    logger.error(f"获取实时行情数据失败: {str(e)}")
                    current_info = None
            
        # 创建线程池
        with ThreadPoolExecutor(max_workers=pool_size) as executor:
            # 准备任务，将 current_info 和 is_historical 作为参数传递给每个任务
            # 显式转换代码与名称为字符串，避免类型推断为 Series/ndarray
            tasks = [(str(row['代码']), str(row['名称']), start_date, end_date, current_info, is_historical)
                    for _, row in stock_list.iterrows()]
            
            # 提交任务到线程池
            futures = []
            for task in tasks:
                future = executor.submit(analyze_stock_wrapper, task)
                futures.append(future)
            
            # 使用 tqdm 显示进度，使用原始stderr确保进度条显示在控制台
            # mininterval=0.5 减少刷新频率，避免在 GUI 或重定向输出时导致 IO 阻塞
            # 在 exe 环境下禁用 ASCII 动画，使用简单的字符，以提高性能
            ascii_bar = getattr(sys, 'frozen', False)
            with tqdm(total=total, desc="分析进度", ncols=100, file=original_stderr, mininterval=0.5, ascii=ascii_bar) as pbar:
                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        results.append(result)
                    pbar.update(1)
        sys.stdout.flush()  # 强制刷新输出
                    
    except KeyboardInterrupt:
        logger.info("\n正在终止进程...")
        return results
    finally:
        # 检查日志文件是否存在且有内容（不再输出到控制台）
        try:
            if os.path.exists(log_file) and os.path.getsize(log_file) > 0:
                logger.info("注意：本次分析可能包含未能成功获取的股票，请查看日志文件以确认是否有您关注的股票未能成功获取。")
                logger.info(f"日志文件位置：{log_file}")
        except Exception:
            pass
        
    return results

def process_results(results: List[Dict]) -> pd.DataFrame:
    """
    处理分析结果，生成最终的DataFrame
    
    Args:
        results: 原始分析结果
    
    Returns:
        pd.DataFrame: 处理后的分析结果
    """
    try:
        # 将结果列表转换为DataFrame
        df = pd.DataFrame(results)
        
        # 确保所有必需的列都存在
        required_columns = ['代码', '名称', '总市值（亿元）', '起始日价（元）', '截止日价（元）', 
                            '交易所', '得分', '详情']
        if not all(col in df.columns for col in required_columns):
            logger.error("结果数据缺少必需的列")
            logger.error(f"现有列: {list(df.columns)}")
            logger.error(f"必需列: {required_columns}")
            # 添加调试信息：显示结果数量和前几个结果的内容
            logger.error(f"结果数量: {len(results)}")
            if results:
                logger.error(f"第一个结果的内容: {results[0]}")
            return pd.DataFrame()
            
        # 计算涨幅
        df['涨幅(%)'] = ((df['截止日价（元）'] - df['起始日价（元）']) / df['起始日价（元）'] * 100).round(2)
        
        # 风险过滤：平均成交量/RSI/波动率
        try:
            if getattr(args, 'min_avg_volume', None) is not None and '平均成交量(手)' in df.columns:
                df = df[df['平均成交量(手)'] >= float(args.min_avg_volume)]
            if getattr(args, 'max_rsi', None) is not None and '末值RSI' in df.columns:
                df = df[df['末值RSI'] <= float(args.max_rsi)]
            if getattr(args, 'max_volatility', None) is not None and '区间波动率(%)' in df.columns:
                df = df[df['区间波动率(%)'] <= float(args.max_volatility)]
        except Exception:
            pass

        # 突破过滤（可选）
        try:
            if getattr(args, 'breakout', False) and '突破' in df.columns:
                df = df[df['突破'] == True]
        except Exception:
            pass

        try:
            if getattr(args, 'expert_filter', False) and '专家匹配' in df.columns:
                df = df[df['专家匹配'] == True]
        except Exception:
            pass

        # 板块筛选（可选）
        try:
            if getattr(args, 'sector_filter', []) and len(args.sector_filter) > 0:
                sector_keywords = []
                sector_mapping = {
                    'AI': ['人工智能', 'AI', '智能', '算法', '机器学习', '深度学习'],
                    '芯片': ['芯片', '半导体', '集成电路', 'IC', '晶圆', '光刻'],
                    '航天': ['航天', '航空', '军工', '卫星', '导弹', '国防'],
                    '人工智能': ['人工智能', 'AI', '智能', '机器人', '自动化'],
                    '半导体': ['半导体', '芯片', '集成电路', 'IC'],
                    '军工': ['军工', '国防', '航天', '航空', '兵器'],
                    '能源': ['能源', '电力', '煤炭', '石油', '天然气', '新能源', '光伏', '风电', '储能', '锂电池'],
                    '可控核聚变': ['可控核聚变', '核聚变', '聚变', '核能', '核技术', '等离子体', '托卡马克'],
                    '通讯模块': ['通讯', '通信', '光纤', '光通信', '5G', '6G', '物联网', '模块', '光模块', '光纤通信'],
                    '光纤': ['光纤', '光缆', '光通信', '光纤网络', '光传输'],
                    '新能源': ['新能源', '太阳能', '风能', '储能', '锂电池', '电动汽车', '充电桩', '氢能源'],
                    '电子模块': ['电子', '模块', '电路', 'PCB', '元器件', '集成电路', '电子元件', '电子器件', '传感器', '连接器']
                }
                
                # 收集所有相关的关键词
                for sector in args.sector_filter:
                    if sector in sector_mapping:
                        sector_keywords.extend(sector_mapping[sector])
                    else:
                        sector_keywords.append(sector)
                
                # 去重
                sector_keywords = list(set(sector_keywords))
                
                # 筛选包含关键词的股票
                def _contains_sector_keyword(name, details):
                    name_str = str(name) if pd.notna(name) else ''
                    details_str = str(details) if pd.notna(details) else ''
                    
                    for keyword in sector_keywords:
                        if keyword in name_str or keyword in details_str:
                            return True
                    return False
                
                # 应用筛选
                mask = df.apply(lambda row: _contains_sector_keyword(row['名称'], row.get('详情', '')), axis=1)
                df = df[mask]
                
                logger.info(f"板块筛选后剩余股票数量: {len(df)}")
                if len(df) > 0:
                    logger.info(f"筛选出的板块股票: {list(zip(df['代码'], df['名称']))}")
        except Exception as e:
            logger.error(f"板块筛选出错: {str(e)}")

        # 行业中性化排名（可选）
        neutralized_used = False
        if getattr(args, 'industry_neutral', False):
            try:
                from modules.data_sources import get_industry_map_from_spot
                ind_map = get_industry_map_from_spot(list(df['代码']))
                if isinstance(ind_map, pd.DataFrame) and not ind_map.empty and '行业' in ind_map.columns:
                    df = df.merge(ind_map[['代码','行业']], on='代码', how='left')
                    def _zgrp(g: pd.DataFrame) -> pd.DataFrame:
                        g = g.copy()
                        mu = g['得分'].mean()
                        sd = g['得分'].std()
                        g['行业Z分'] = 0.0 if (pd.isna(sd) or sd == 0) else (g['得分'] - mu) / sd
                        return g
                    df = df.groupby(df['行业'].fillna('未知'), as_index=False).apply(_zgrp)
                    neutralized_used = True
            except Exception:
                neutralized_used = False

        # 风险调整后的期望分排序（可选/自动根据验证窗口）
        used_expected = False
        try:
            _use_expected = bool(getattr(args, 'rank_expected', False) or getattr(args, 'validate_days', None))
            if _use_expected:
                base = df['综合得分'] if '综合得分' in df.columns else df['得分']
                vol = df['区间波动率(%)'] if '区间波动率(%)' in df.columns else 0.0
                vol_safe = vol.replace(0, 0.0001) if isinstance(vol, pd.Series) else vol
                h_days = int(getattr(args, 'validate_days', DEFAULT_DAYS))
                if h_days <= 7:
                    mom = df['近5日收益(%)'] if '近5日收益(%)' in df.columns else 0.0
                    mom_scale, vol_gamma, bcoef = 1.1, 1.0, 1.0
                elif h_days <= 15:
                    m5 = df['近5日收益(%)'] if '近5日收益(%)' in df.columns else 0.0
                    m10 = df['近10日收益(%)'] if '近10日收益(%)' in df.columns else m5
                    mom = (m5 + m10) / 2.0
                    mom_scale, vol_gamma, bcoef = 0.8, 0.8, 0.7
                else:
                    m10 = df['近10日收益(%)'] if '近10日收益(%)' in df.columns else 0.0
                    m20 = df['近20日收益(%)'] if '近20日收益(%)' in df.columns else m10
                    mom = (m10 * 0.4 + m20 * 0.6)
                    mom_scale, vol_gamma, bcoef = 0.6, 0.6, 0.5
                df['期望分'] = base * (1.0 + mom_scale * (mom/100.0)) / (1.0 + vol_gamma * (vol_safe/100.0))
                if '量能放大倍数' in df.columns:
                    try:
                        df['期望分'] = df['期望分'] * (df['量能放大倍数'].fillna(1.0) ** bcoef)
                    except Exception:
                        pass
                df = df.sort_values(['期望分','代码'], ascending=[False, True])
                used_expected = True
        except Exception:
            used_expected = False

        if not used_expected:
            if neutralized_used:
                df = df.sort_values(['行业Z分', '代码'], ascending=[False, True])
            else:
                if args.topgains:
                    df = df.sort_values(['涨幅(%)', '代码'], ascending=[False, True])
                else:
                    df = df.sort_values(['得分', '代码'], ascending=[False, True])
        
        # 重置索引
        df = df.reset_index(drop=True)
        
        # 格式化数值列
        df['得分'] = df['得分'].round(2)
        try:
            df['总市值（亿元）'] = df['总市值（亿元）'].round(2)
        except:
            # 历史数据没有’总市值（亿元）’列，其值是'N/A'，这里不做处理
            pass
        df['起始日价（元）'] = df['起始日价（元）'].round(2)
        df['截止日价（元）'] = df['截止日价（元）'].round(2)
        
        # 重新排列列的顺序
        df = df[['代码', '名称', '总市值（亿元）', '起始日价（元）', '截止日价（元）', 
                 '涨幅(%)', '得分', '交易所', '详情']]
        
        return cast(pd.DataFrame, df)
        
    except Exception as e:
        logger.error(f"处理结果时出错: {str(e)}")
        return pd.DataFrame()

def _expert_match(indicators: Dict[str, pd.Series], hist_data: pd.DataFrame, current_info: Optional[pd.DataFrame], stock_code: str) -> bool:
    try:
        ma5 = indicators['ma5'].iloc[-1]
        ma10 = indicators['ma10'].iloc[-1]
        ma20 = indicators['ma20'].iloc[-1]
        ma5p = indicators['ma5'].iloc[-2] if len(indicators['ma5']) > 1 else ma5
        ma10p = indicators['ma10'].iloc[-2] if len(indicators['ma10']) > 1 else ma10
        macd = indicators['macd']
        dif = indicators['dif'].iloc[-1]
        dea = indicators['dea'].iloc[-1]
        difp = indicators['dif'].iloc[-2] if len(indicators['dif']) > 1 else dif
        deap = indicators['dea'].iloc[-2] if len(indicators['dea']) > 1 else dea
        
        # 宽松条件：均线多头 或 金叉 或 价格站上均线
        ma_trend = (ma5 > ma10 > ma20)
        ma_cross = (ma5 > ma10) and (ma5p <= ma10p)
        macd_cross = (dif > dea) and (difp <= deap)
        
        # MACD 动能减弱（底背离迹象）
        weaken = False
        try:
            neg = macd[macd < 0]
            if len(neg) >= 3:
                last3 = np.abs(neg.iloc[-3:])
                weaken = bool(last3.iloc[0] >= last3.iloc[1] >= last3.iloc[2])
        except Exception:
            weaken = False
            
        # 成交量：只要最后一天放量即可，不必连续三天
        vol_ok = False
        if len(hist_data) >= 2:
            v = hist_data['volume']
            vol_ok = bool(v.iloc[-1] > v.iloc[-2])
            
        latest = hist_data['close'].iloc[-1]
        price_above = bool(latest > ma5)
        
        # 组合条件：(均线趋势 OR 均线金叉 OR MACD金叉) AND (成交量OK OR 价格在均线上)
        technical_ok = bool((ma_trend or ma_cross or macd_cross) and (vol_ok or price_above))
        
        ok = technical_ok
        
        if current_info is not None and stock_code in current_info.index:
            try:
                pct = current_info.loc[stock_code, '涨跌幅'] if '涨跌幅' in current_info.columns else None
                if pct is not None and not pd.isna(pct):
                    # 放宽涨跌幅限制：0% - 9.5%
                    ok = bool(ok and (float(pct) >= 0.0 and float(pct) <= 9.5))
            except Exception:
                pass
            try:
                vr = current_info.loc[stock_code, '量比'] if '量比' in current_info.columns else None
                if vr is not None and not pd.isna(vr):
                    # 放宽量比限制：> 0.8
                    ok = bool(ok and (float(vr) >= 0.8))
            except Exception:
                pass
            try:
                to = current_info.loc[stock_code, '换手率'] if '换手率' in current_info.columns else None
                if to is not None and not pd.isna(to):
                    # 放宽换手率：3% - 20%
                    ok = bool(ok and (float(to) >= 3.0 and float(to) <= 20.0))
            except Exception:
                pass
            try:
                mcf = current_info.loc[stock_code, '流通市值'] if '流通市值' in current_info.columns else (current_info.loc[stock_code, '总市值'] if '总市值' in current_info.columns else None)
                if mcf is not None and not pd.isna(mcf) and float(mcf) > 0:
                    # 放宽流通市值：20亿 - 1000亿
                    ok = bool(ok and (float(mcf)/100000000.0 >= 20.0 and float(mcf)/100000000.0 <= 1000.0))
            except Exception:
                pass
        return bool(ok)
    except Exception:
        return False

def analyze_stock_wrapper(wrapper_args: Tuple[str, str, str, str, Optional[pd.DataFrame], bool]) -> Optional[Dict]:
    """
    包装股票分析函数，用于多线程处理
    
    Args:
        wrapper_args: 包含股票代码、名称、日期等信息的元组
    
    Returns:
        Optional[Dict]: 单只股票的分析结果
    """
    # 预先定义以避免异常路径上的未绑定告警
    stock_code: str = ""
    stock_name: str = ""
    try:
        stock_code, stock_name, start_date, end_date, current_info, is_historical = wrapper_args
        
        # 从全局参数中获取参数对象
        _global_args = globals().get('args', None)
        
        # 获取历史数据 (传入全局 args 以便支持缓存等配置)
        hist_data = get_historical_data(stock_code, start_date, end_date, _global_args)
        
        # 获取“最少交易日数”阈值（默认 20，可通过 --min-trading-days 修改）
        _min_td = 3
        if _global_args is not None:
            try:
                _min_td = int(getattr(_global_args, 'min_trading_days', 3))
            except Exception:
                _min_td = 3
        if hist_data.empty or len(hist_data) < _min_td:  # 数据长度检查（交易日数）
            logger.warning(f"股票 {stock_code} 历史数据不足，跳过分析")
            return None
            
        # 计算区间涨幅
        # 获取起始日价格和截止日价格
        start_price = hist_data['close'].iloc[0]  # 起始价格
        end_price = hist_data['close'].iloc[-1]   # 结束价格
        price_change = ((end_price - start_price) / start_price * 100)  # 涨幅百分比
        
        # 计算技术指标
        indicators = calculate_technical_indicators(hist_data)
        if not indicators:
            return None
            
        # 获取最新价格和市值数据
        try:
            latest_price = hist_data['close'].iloc[-1]
            # 可选：使用实时最新价作为截止日价
            if (not is_historical) and _global_args is not None and bool(getattr(_global_args, 'use_spot_price', False)):
                if current_info is not None and stock_code in current_info.index:
                    try:
                        sp = float(current_info.loc[stock_code, '最新价'])
                        if sp > 0:
                            latest_price = sp
                    except Exception:
                        pass
            # 市值
            if is_historical:
                market_cap = 'N/A'
            else:
                if current_info is not None and stock_code in current_info.index:
                    market_cap = current_info.loc[stock_code, '总市值'] / 100000000
                else:
                    market_cap = 0.0
        except Exception as e:
            latest_price = hist_data['close'][-1]
            market_cap = 'N/A' if is_historical else 0.0
            logger.warning(f"获取股票 {stock_code} 实时数据失败，使用历史数据最新价格")
            
        # 获取财务数据
        financial_data = None
        
        # 显式检查 PE/PB 等参数是否启用，只有启用时才获取财务数据
        # 这样可以避免在未指定相关参数时出现“尝试获取财务数据”的日志，并提高性能
        _need_financial = False
        if _global_args is not None:
            _need_financial = (
                getattr(_global_args, 'use_financial', False) or 
                getattr(_global_args, 'pe', False) or 
                getattr(_global_args, 'pb', False) or 
                getattr(_global_args, 'turnover', False) or # 换手率用于评分
                getattr(_global_args, 'dividend', False) or 
                getattr(_global_args, 'dividend_yield', False) or 
                getattr(_global_args, 'eps', False) or 
                getattr(_global_args, 'navps', False)
            )
            
        if _need_financial and not is_historical and current_info is not None and stock_code in current_info.index:
            try:
                financial_data = {
                    'pe_ratio': float(current_info.loc[stock_code, '市盈率-动态']),
                    'pb_ratio': float(current_info.loc[stock_code, '市净率']),
                    'turnover_rate': float(current_info.loc[stock_code, '换手率']),
                    'volume_ratio': float(current_info.loc[stock_code, '量比'])
                }
                logger.debug(f"股票 {stock_code} 财务数据: PE={financial_data['pe_ratio']}, PB={financial_data['pb_ratio']}")
            except Exception as e:
                # 仅在需要财务数据时才警告
                logger.warning(f"获取股票 {stock_code} 财务数据失败: {e}")
                financial_data = None
        
        # 计算得分和得分详情（包含财务指标）
        # 注意：使用 _global_args 而不是 wrapper_args (原 args) 来获取参数
        score = calculate_stock_score(hist_data, indicators, financial_data, 
                                    enable_pe=getattr(_global_args, 'pe', False) if _global_args else False,
                                    enable_pb=getattr(_global_args, 'pb', False) if _global_args else False,
                                    enable_volume=getattr(_global_args, 'volume', False) if _global_args else False,
                                    enable_turnover=getattr(_global_args, 'turnover', False) if _global_args else False,
                                    enable_dividend=getattr(_global_args, 'dividend', False) if _global_args else False,
                                    enable_dividend_yield=getattr(_global_args, 'dividend_yield', False) if _global_args else False,
                                    enable_eps=getattr(_global_args, 'eps', False) if _global_args else False,
                                    enable_navps=getattr(_global_args, 'navps', False) if _global_args else False,
                                    enable_news=getattr(_global_args, 'news', False) if _global_args else False,
                                    stock_name=stock_name,
                                    stock_code=stock_code,
                                    region=getattr(_global_args, 'region', 'cn') if _global_args else 'cn')
        
        # 获取得分详情
        score_details = []
        latest_idx = -1
        
        # MACD指标得分详情
        macd_score = 0
        if indicators['macd'].iloc[latest_idx] > 0:
            macd_score += 10
        if len(hist_data) > 1 and (indicators['dif'].iloc[latest_idx] > indicators['dea'].iloc[latest_idx] and 
            indicators['dif'].iloc[latest_idx-1] <= indicators['dea'].iloc[latest_idx-1]):
            macd_score += 10
        score_details.append(f"MACD({macd_score}分)=[柱>0:{10 if indicators['macd'].iloc[latest_idx] > 0 else 0}分 + DIF上穿:{10 if macd_score > 10 else 0}分]")
        
        # KDJ指标得分详情
        kdj_score = 0
        if indicators['k'].iloc[latest_idx] < 30 and indicators['d'].iloc[latest_idx] < 30:
            kdj_score += 10
        if indicators['j'].iloc[latest_idx] < 20:
            kdj_score += 5
        if len(hist_data) > 1 and (indicators['k'].iloc[latest_idx] > indicators['d'].iloc[latest_idx] and 
            indicators['k'].iloc[latest_idx-1] <= indicators['d'].iloc[latest_idx-1]):
            kdj_score += 5
        score_details.append(f"KDJ({kdj_score}分)=[KD<30:{10 if kdj_score >= 10 else 0}分 + J<20:{5 if indicators['j'].iloc[latest_idx] < 20 else 0}分 + K上穿:{5 if kdj_score-15 == 5 else 0}分]")
        
        # RSI指标得分详情
        rsi = indicators['rsi'].iloc[latest_idx]
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
        if (indicators['ma5'].iloc[latest_idx] > indicators['ma10'].iloc[latest_idx] > 
            indicators['ma20'].iloc[latest_idx]):
            ma_score += 10
        latest_price = hist_data['close'].iloc[latest_idx]
        ma_cross_score = 0
        if latest_price > indicators['ma5'].iloc[latest_idx]:
            ma_cross_score += 4
        if latest_price > indicators['ma10'].iloc[latest_idx]:
            ma_cross_score += 3
        if latest_price > indicators['ma20'].iloc[latest_idx]:
            ma_cross_score += 3
        score_details.append(f"均线({ma_score + ma_cross_score}分)=[多头排列:{ma_score}分 + 站上均线:{ma_cross_score}分]")
        
        # 成交量分析得分详情
        vol_score = 0
        if len(hist_data) >= 1 and hist_data['volume'].iloc[latest_idx] > indicators['volume_ma5'].iloc[latest_idx]:
            vol_score += 10
        if len(hist_data) >= 3:  # 确保有足够的数据进行比较
            try:
                if (hist_data['volume'].iloc[latest_idx] > hist_data['volume'].iloc[latest_idx-1] > 
                    hist_data['volume'].iloc[latest_idx-2]):
                    vol_score += 10
            except IndexError:
                # 如果出现索引错误，不增加分数
                pass
                
        score_details.append(f"成交量({vol_score}分)=[量>均量:{10 if vol_score >= 10 else 0}分 + 量增加:{10 if vol_score-10 == 10 else 0}分]")
        
        # 合并所有得分详情
        # 附加过滤相关指标
        avg_volume = float(hist_data['volume'].mean()) / 100.0
        try:
            rsi_last = float(indicators['rsi'].iloc[latest_idx])
        except Exception:
            rsi_last = float('nan')
        try:
            volat_pct = float(hist_data['close'].pct_change().std() * 100.0)
        except Exception:
            volat_pct = float('nan')

        # 近5日动量
        try:
            if len(hist_data) >= 6:
                m5 = float((hist_data['close'].iloc[-1] - hist_data['close'].iloc[-6]) / hist_data['close'].iloc[-6] * 100.0)
            else:
                m5 = float((hist_data['close'].iloc[-1] - hist_data['close'].iloc[0]) / hist_data['close'].iloc[0] * 100.0)
        except Exception:
            m5 = float('nan')

        # 近10/20日动量
        try:
            if len(hist_data) >= 11:
                m10 = float((hist_data['close'].iloc[-1] - hist_data['close'].iloc[-11]) / hist_data['close'].iloc[-11] * 100.0)
            else:
                m10 = m5
        except Exception:
            m10 = float('nan')
        try:
            if len(hist_data) >= 21:
                m20 = float((hist_data['close'].iloc[-1] - hist_data['close'].iloc[-21]) / hist_data['close'].iloc[-21] * 100.0)
            else:
                m20 = m10
        except Exception:
            m20 = float('nan')

        # 突破指标
        breakout_flag = False
        vol_mult = float('nan')
        recent_high = float('nan')
        try:
            _bw = int(getattr(globals().get('args', None), 'breakout_window', 10))
        except Exception:
            _bw = 10
        try:
            close_last = float(hist_data['close'].iloc[latest_idx])
            if len(hist_data) >= (_bw + 1):
                recent_high = float(hist_data['high'].iloc[-_bw-1:-1].max())
            else:
                recent_high = float(hist_data['high'].iloc[:-1].max())
            vol_ma5 = float(indicators['volume_ma5'].iloc[latest_idx]) if 'volume_ma5' in indicators else float('nan')
            cur_vol = float(hist_data['volume'].iloc[latest_idx])
            vol_mult = cur_vol / vol_ma5 if (not pd.isna(vol_ma5) and vol_ma5 > 0) else float('nan')
            macd_pos = bool(indicators['macd'].iloc[latest_idx] > 0) if 'macd' in indicators else False
            _mult_thr = float(getattr(globals().get('args', None), 'breakout_vol_mult', 1.3))
            breakout_flag = bool(close_last > recent_high and (not pd.isna(vol_mult) and vol_mult >= _mult_thr) and macd_pos)
        except Exception:
            breakout_flag = False

        # 获取新闻分析结果（如果启用）
        news_analysis = None
        _global_args = globals().get('args', None)
        if _global_args is not None and getattr(_global_args, 'news', False) and stock_name and stock_code:
            from modules.news_analyzer import get_stock_news_analysis
            logger.info(f"正在获取新闻分析: {stock_name} {stock_code}")
            logger.info(f"新闻分析条件: news={getattr(_global_args, 'news', False)}, stock_name={stock_name}, stock_code={stock_code}")
            news_analysis = get_stock_news_analysis(stock_name, stock_code, 
                                                   enable_news=getattr(_global_args, 'news', False),
                                                   region=getattr(_global_args, 'region', 'cn'))
            logger.info(f"新闻分析结果: {news_analysis['status']}, 新闻数量: {news_analysis.get('news_count', 0)}")
        # 移除else中的调试信息，避免在不启用新闻分析时显示
        
        # 使用新的generate_score_details函数生成详情
        score_detail_str = generate_score_details(
            hist_data, indicators, score, price_change,
            financial_data=financial_data,
            enable_pe=getattr(_global_args, 'pe', False) if _global_args else False,
            enable_pb=getattr(_global_args, 'pb', False) if _global_args else False,
            enable_volume=getattr(_global_args, 'volume', False) if _global_args else False,
            enable_turnover=getattr(_global_args, 'turnover', False) if _global_args else False,
            enable_news=getattr(_global_args, 'news', False) if _global_args else False,
            news_analysis=news_analysis
        )
        
        return {
            '代码': stock_code,
            '名称': stock_name,
            '总市值（亿元）': market_cap,
            '起始日价（元）': start_price,
            '截止日价（元）': latest_price,
            '交易所': 'SH' if str(stock_code).startswith('6') else 'SZ',
            '得分': round(score, 2),
            '详情': score_detail_str,
            '平均成交量(手)': round(avg_volume, 2),
            '末值RSI': rsi_last,
            '区间波动率(%)': volat_pct,
            '突破': breakout_flag,
            '量能放大倍数': vol_mult,
            '近N日最高价': recent_high,
            '近5日收益(%)': m5,
            '近10日收益(%)': m10,
            '近20日收益(%)': m20,
            '量比': float(current_info.loc[stock_code, '量比']) if (current_info is not None and stock_code in current_info.index and '量比' in current_info.columns) else float('nan'),
            '换手率(%)': float(current_info.loc[stock_code, '换手率']) if (current_info is not None and stock_code in current_info.index and '换手率' in current_info.columns) else float('nan'),
            '流通市值（亿元）': float(current_info.loc[stock_code, '流通市值'])/100000000.0 if (current_info is not None and stock_code in current_info.index and '流通市值' in current_info.columns) else (market_cap if isinstance(market_cap, (int, float)) else float('nan')),
            '当日涨跌幅(%)': float(current_info.loc[stock_code, '涨跌幅']) if (current_info is not None and stock_code in current_info.index and '涨跌幅' in current_info.columns) else float('nan'),
            '专家匹配': _expert_match(indicators, hist_data, current_info, stock_code)
        }
        
    except Exception as e:
        logger.error(f"分析股票 {stock_code} 时出错: {str(e)}")
        return None

def main():
    global args
    global isall
    global is_historical
    global output_dir
    
    # 解析命令行参数
    parser = argparse.ArgumentParser(
        description=PROGRAM_DESC,
        formatter_class=argparse.RawTextHelpFormatter)
    
    parser.add_argument('-k', type=int, default=10, help='显示前K只股票')
    parser.add_argument('-d','--days', type=int, default=30, help='分析天数，默认30天（最少5个交易日）')
    parser.add_argument('-p', '--parallel', type=int, default=8, help='并行处理的进程数')
    parser.add_argument('--start-date', type=str, help='指定开始日期 (YYYYMMDD)，不能与-d同时使用')
    parser.add_argument('--end-date', type=str, help='指定结束日期 (YYYYMMDD)，不能与-d同时使用')
    parser.add_argument('--debug', action='store_true', help='启用调试模式')
    parser.add_argument('-g', '--topgains', action='store_true', help='按照区间涨幅排序（仅在分析多只股票时有效）')
    parser.add_argument('-c', '--codes', type=str, help='指定股票代码（用逗号分隔多个代码）')
    parser.add_argument('--sector-filter', nargs='+', default=[], help='指定热门板块筛选（如AI,芯片,航天,人工智能,半导体,军工）')
    parser.add_argument('--ai', action='store_true', help='启用AI分析功能, 需要在 config.toml 中配置 [llm] 部分')
    parser.add_argument('--all', action='store_true', help='分析所有股票（默认只分析上证和深证股票）')
    parser.add_argument('--fast', action='store_true', help='快速模式：跳过东财实时与历史接口，优先使用腾讯与缓存')
    parser.add_argument('--config', type=str, help='配置文件路径，默认优先查找 config.toml')
    parser.add_argument('--source', type=str, help='数据源优先级，逗号分隔，例如 eastmoney,tencent,sina,exchange')
    parser.add_argument('--cache', action='store_true', help='启用缓存（parquet/csv），命令行优先于配置文件')
    parser.add_argument('-f', '--force', action='store_true', help='预检失败仍然强制运行')
    parser.add_argument('-m', '--mins', type=int, choices=[1, 5, 15, 30, 60], help='分钟级分析周期，支持1/5/15/30/60分钟（推荐使用5或15分钟周期）')
    parser.add_argument('--minute-sim', action='store_true', help='允许在分钟数据不可用时使用日线模拟分钟数据（默认关闭）')
    parser.add_argument('--minute-chart', action='store_true', help='为分钟级分析生成图表（仅在启用 -m 或 -d 5 时生效）')
    parser.add_argument('--trend-day', type=int, help='趋势验证天数，表示预期在N天内出现上涨')
    parser.add_argument('--validate-days', type=int, help='验证窗口天数，用于评估所选股票在后续区间的表现')
    parser.add_argument('--industry-neutral', action='store_true', help='启用行业中性化排名（按行业内z-score排序后再合并）')
    parser.add_argument('--min-avg-volume', type=float, help='过滤平均成交量过低的股票（单位：手，按所选区间平均）')
    parser.add_argument('--max-rsi', type=float, help='过滤末值RSI过高（超买）的股票')
    parser.add_argument('--max-volatility', type=float, help='过滤区间波动率过高的股票（单位：百分比）')
    parser.add_argument('--use-financial', action='store_true', help='启用财务因子调整得分')
    parser.add_argument('--refresh-cache', action='store_true', help='分析前刷新所选区间的历史数据缓存')
    parser.add_argument('--breakout', action='store_true', help='启用突破过滤（新高+量能放大+MACD为正）')
    parser.add_argument('--breakout-window', type=int, default=10, help='突破窗口天数（默认10）')
    parser.add_argument('--breakout-vol-mult', type=float, default=1.3, help='突破量能放大倍数阈值（默认1.3）')
    parser.add_argument('--rank-expected', action='store_true', help='按风险调整后的期望分排序')
    parser.add_argument('--require-profitable', action='store_true', help='仅保留验证期正收益股票')
    parser.add_argument('--require-trend-hit', action='store_true', help='仅保留在trend_day窗口内命中上涨的股票')
    parser.add_argument('--candidate-mult', type=int, help='验证候选集放大倍数（默认5，开启约束默认10）')
    parser.add_argument('--strict', action='store_true', help='严格模式：强制正收益、trend命中、期望分排序并扩大候选集')
    parser.add_argument('--forward', action='store_true', help='前瞻模式：仅生成analysis_results与图表，不执行验证（validate-days仅用于排序）')
    parser.add_argument('--use-spot-price', action='store_true', help='使用实时最新价作为截止日价（当实时行情可用且非历史查询）')
    parser.add_argument('--expert-filter', action='store_true', help='启用经验规则筛选')
    
    # 财务指标开关参数
    parser.add_argument('--pe', action='store_true', help='启用市盈率(PE)评分')
    parser.add_argument('--pb', action='store_true', help='启用市净率(PB)评分')
    parser.add_argument('--volume', action='store_true', help='启用成交量评分')
    parser.add_argument('--turnover', action='store_true', help='启用成交额评分')
    parser.add_argument('--dividend', action='store_true', help='启用股息评分（暂不可用，等待数据源支持）')
    parser.add_argument('--dividend-yield', action='store_true', help='启用股息率评分（暂不可用，等待数据源支持）')
    parser.add_argument('--eps', action='store_true', help='启用每股收益(EPS)评分（暂不可用，等待数据源支持）')
    parser.add_argument('--navps', action='store_true', help='启用每股净资产(NAVPS)评分（暂不可用，等待数据源支持）')
    
    # 新闻分析参数
    parser.add_argument('--news', action='store_true', help='启用新闻热度分析，从互联网搜索股票相关新闻并分析关键词')
    parser.add_argument('--region', type=str, choices=['cn', 'intl'], default='cn', 
                        help='新闻搜索地区，cn: 中国(使用百度)，intl: 国际(使用DuckDuckGo)，默认cn')
    parser.add_argument('--realtime', action='store_true', help='启用实时数据获取（默认禁用，以提高速度并减少API失败概率）')
    
    # GUI模式参数 - 已移除


    # 解析命令行参数后，设置全局变量
    args = parser.parse_args()
    if getattr(args, 'strict', False):
        try:
            if not getattr(args, 'require_profitable', False):
                setattr(args, 'require_profitable', True)
            if not getattr(args, 'require_trend_hit', False):
                setattr(args, 'require_trend_hit', True)
            if not getattr(args, 'rank_expected', False):
                setattr(args, 'rank_expected', True)
            argv = sys.argv if isinstance(sys.argv, list) else []
            h_days = getattr(args, 'validate_days', None)
            has_c_mult = any(a.startswith('--candidate-mult') for a in argv)
            has_minvol = any(a.startswith('--min-avg-volume') for a in argv)
            has_maxrsi = any(a.startswith('--max-rsi') for a in argv)
            has_maxvol = any(a.startswith('--max-volatility') for a in argv)
            has_trend = any(a.startswith('--trend-day') for a in argv)

            if h_days is None:
                if not has_c_mult and not getattr(args, 'candidate_mult', None):
                    setattr(args, 'candidate_mult', 12)
                if not has_minvol and getattr(args, 'min_avg_volume', None) is None:
                    setattr(args, 'min_avg_volume', 10000)
                if not has_maxrsi and getattr(args, 'max_rsi', None) is None:
                    setattr(args, 'max_rsi', 72)
                if not has_maxvol and getattr(args, 'max_volatility', None) is None:
                    setattr(args, 'max_volatility', 15)
            else:
                try:
                    h = int(h_days)
                except Exception:
                    h = 13
                if h <= 7:
                    if not has_trend and getattr(args, 'trend_day', None) is None:
                        setattr(args, 'trend_day', 3)
                    if not has_c_mult:
                        setattr(args, 'candidate_mult', 15)
                    if not has_minvol and getattr(args, 'min_avg_volume', None) is None:
                        setattr(args, 'min_avg_volume', 10000)
                    if not has_maxrsi and getattr(args, 'max_rsi', None) is None:
                        setattr(args, 'max_rsi', 72)
                    if not has_maxvol and getattr(args, 'max_volatility', None) is None:
                        setattr(args, 'max_volatility', 15)
                elif h <= 15:
                    if not has_trend and getattr(args, 'trend_day', None) is None:
                        setattr(args, 'trend_day', 5)
                    if not has_c_mult:
                        setattr(args, 'candidate_mult', 12)
                    if not has_minvol and getattr(args, 'min_avg_volume', None) is None:
                        setattr(args, 'min_avg_volume', 10000)
                    if not has_maxrsi and getattr(args, 'max_rsi', None) is None:
                        setattr(args, 'max_rsi', 72)
                    if not has_maxvol and getattr(args, 'max_volatility', None) is None:
                        setattr(args, 'max_volatility', 15)
                else:
                    if not has_trend and getattr(args, 'trend_day', None) is None:
                        setattr(args, 'trend_day', 7)
                    if not has_c_mult:
                        setattr(args, 'candidate_mult', 12)
                    if not has_minvol and getattr(args, 'min_avg_volume', None) is None:
                        setattr(args, 'min_avg_volume', 8000)
                    if not has_maxrsi and getattr(args, 'max_rsi', None) is None:
                        setattr(args, 'max_rsi', 70)
                    if not has_maxvol and getattr(args, 'max_volatility', None) is None:
                        setattr(args, 'max_volatility', 18)
        except Exception:
            pass
    
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG if args.debug else logging.INFO)
    
    # 清除所有现有的处理器（不再添加控制台处理器，避免控制台日志干扰）
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # 预先创建输出目录与文件日志处理器，确保所有日志写入文件
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = os.path.join('data_archive', timestamp)
    os.makedirs(output_dir, exist_ok=True)
    # 进度条输出到控制台 (sys.stderr)，日志输出到文件
    original_stderr = sys.stderr
    try:
        log_file = os.path.join(output_dir, 'analysis.log')
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG if args.debug else logging.INFO)
        file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        logger.debug(f"日志文件处理器已创建：{log_file}")
        # 不再重定向 sys.stderr 到文件，以确保 tqdm 等进度条能正常显示在控制台
        # try:
        #     sys.stderr = open(log_file, 'a', encoding='utf-8')
        # except Exception:
        #     pass
    except Exception as _log_err:
        # 如果文件处理器创建失败，仍然不向控制台输出，保留日志对象可用
        pass
    
    # 显示版本信息（日志写文件，同时在控制台打印版权与免责声明）
    logger.info(f"股票潜力分析工具 v{__version__}")
    logger.info(f"作者: {__author__}")
    logger.info(f"发布日期: {__release_date__}")
    logger.info(DISCLAIMER)
    try:
        print(f"股票潜力分析工具 v{__version__}")
        print(f"作者: {__author__}")
        print(f"发布日期: {__release_date__}")
        print("")
        print(DISCLAIMER)
        sys.stdout.flush()  # 强制刷新缓冲区，防止与 stderr 的进度条混杂
    except Exception:
        pass
    
    # 参数验证
    if args.k <= 0:
        logger.error("K必须大于0")
        return
    
    # 检查时间参数冲突
    if args.days != 30 and (args.start_date or args.end_date):
        logger.error("不能同时使用-d参数和--start-date/--end-date参数")
        return

    if not args.start_date and args.end_date:
        logger.error("必须提供开始日期: --start-date")
        return

    if args.ai and (args.start_date or args.end_date):
        logger.warning("AI分析仅对实时数据时有意义，对于历史查询结果无效")
        logger.warning("如果希望执行AI分析，请使用'-d'参数")

    # 加载配置并合并（命令行优先）
    cfg = load_user_config(args.config if hasattr(args, 'config') else None)
    sources_cfg = cfg.get('sources', DEFAULT_SOURCES)
    if isinstance(sources_cfg, str):
        sources_cfg = [s.strip().lower() for s in re.split('[,;]', sources_cfg) if s.strip()]
    if getattr(args, 'source', None):
        source_list = [s.strip().lower() for s in re.split('[,;]', args.source) if s.strip()]
    else:
        source_list = sources_cfg if sources_cfg else DEFAULT_SOURCES
    # 保存到全局 args 以便各函数使用
    setattr(args, 'source_list', source_list)
    # 缓存与强制参数
    if not hasattr(args, 'cache') or args.cache is False:
        args.cache = bool(cfg.get('use_cache', False)) or bool(args.debug)
    # days 覆盖
    if not getattr(args, 'days', None):
        if isinstance(cfg.get('days'), int):
            args.days = cfg.get('days')
    # force 覆盖
    if not getattr(args, 'force', False):
        args.force = bool(cfg.get('force', False))

    # 预检数据源：若失败且未启用 --force 则退出
    try:
        if not precheck_sources(source_list, original_stderr=original_stderr):
            msg = f"数据源预检失败，所选源不可用: {','.join(source_list)}"
            if args.force:
                logger.warning(msg + "，已启用 --force，继续执行")
            else:
                logger.error(msg + "，使用 -f/--force 可忽略预检继续执行")
                sys.exit(1)
    except Exception as e:
        if args.force:
            logger.warning(f"预检过程中发生异常但已启用 --force：{e}")
        else:
            logger.error(f"预检过程中发生异常：{e}")
            sys.exit(1)

    # 设置日期范围
    end_date = args.end_date if args.end_date else datetime.now().strftime('%Y%m%d')
    isall=False   
    if args.all:
        if args.codes:
            logger.error("不能同时使用--all参数和--codes参数")
            sys.exit(1)
        isall=True

    is_historical = bool(args.start_date or args.end_date)
    if args.start_date:
        start_date = args.start_date
        # 计算时间间隔
        delta = (datetime.strptime(end_date, '%Y%m%d') - 
                datetime.strptime(start_date, '%Y%m%d')).days
        if delta < MIN_RANGE_DAYS:
            logger.error(f"时间间隔不能少于{MIN_RANGE_DAYS}天")
            return
    else:
        days = DEFAULT_DAYS if args.days is None else args.days
        # 优先按“交易日”计算起始日期，确保近 N 个交易日的数据充足
        start_date = None
        try:
            trade_cal = ak.tool_trade_date_hist_sina()
            if isinstance(trade_cal, pd.DataFrame) and not trade_cal.empty:
                # 兼容不同列名：可能是 'date'、'trade_date' 或 '日期'，并确保列名为 str
                dcol_name: str
                if 'date' in trade_cal.columns:
                    dcol_name = 'date'
                elif 'trade_date' in trade_cal.columns:
                    dcol_name = 'trade_date'
                elif '日期' in trade_cal.columns:
                    dcol_name = '日期'
                else:
                    # 使用 tolist() 获取 Python 字符串，避免类型为 Index 导致的类型检查告警
                    cols_list = trade_cal.columns.tolist()
                    dcol_name = str(cols_list[0]) if len(cols_list) > 0 else 'date'

                # 兼容 ISO8601 与混合格式的日期解析，尽量避免解析失败
                try:
                    trade_cal[dcol_name] = pd.to_datetime(trade_cal[dcol_name], format='ISO8601', errors='coerce')
                except Exception:
                    try:
                        # pandas 混合格式解析
                        trade_cal[dcol_name] = pd.to_datetime(trade_cal[dcol_name], format='mixed', errors='coerce')
                    except Exception:
                        trade_cal[dcol_name] = pd.to_datetime(trade_cal[dcol_name], errors='coerce')

                # 显式传入 List[str] 以满足类型检查器对 IndexLabel 的约束
                trade_cal = trade_cal.dropna(subset=[dcol_name]).sort_values(by=[dcol_name])
                # 过滤到结束日期之前（含当日）
                end_ts = pd.to_datetime(end_date, format='%Y%m%d', errors='coerce')
                if pd.isna(end_ts):
                    end_ts = pd.to_datetime(end_date, errors='coerce')
                valid_days = trade_cal[trade_cal[dcol_name] <= end_ts][dcol_name].tolist()
                if len(valid_days) >= 1:
                    # 取最近 days 个交易日的首日作为起始
                    idx = max(0, len(valid_days) - days)
                    start_ts = valid_days[idx]
                    # 统一为 pandas.Timestamp，稳健格式化
                    start_ts = pd.to_datetime(start_ts)
                    start_date = start_ts.strftime('%Y%m%d')
                    # 将区间右端改为 ≤ end_date 的最后一个交易日
                    end_trading_ts = pd.to_datetime(valid_days[-1])
                    end_date = end_trading_ts.strftime('%Y%m%d')
                    logger.info(f"按交易日计算起始日期: {start_date} (近{days}个交易日)")
                    # 额外显示：工作日区间（YYYYMMDD-YYYYMMDD）
                    logger.info(f"工作日区间: {start_date}-{end_date} (由 -d {days} 转换)")
        except Exception as _cal_err:
            logger.warning(f"交易日历获取失败，回退为日历天数: {_cal_err}")

        if not start_date:
            # 回退为按日历天数计算
            start_date = (datetime.strptime(end_date, '%Y%m%d') - 
                         timedelta(days)).strftime('%Y%m%d')
            logger.info(f"按日历天计算起始日期: {start_date} (近{days}天)")
            # 也显示区间（YYYYMMDD-YYYYMMDD）
            logger.info(f"日历天区间: {start_date}-{end_date} (由 -d {days} 转换)")

    logger.info("开始分析股票...")
    logger.info(f"日期范围: {start_date} 至 {end_date}")
    
    # 输出目录提示
    logger.info(f"输出目录: {output_dir}")
    
    # 设置matplotlib样式
    set_plot_style()
    
    # 获取股票列表
    logger.info("正在获取股票列表...")
    try:
        # 始终需要获取股票列表。虽然 stock_spot_em_with_fallback 会尝试实时接口，
        # 但它内部有回退机制（stock_info_a_code_name）以应对实时接口失败或被主动跳过的情况。
        # 在这里我们不需刻意区分，因为获取列表是基础。
        all_stocks = stock_spot_em_with_fallback(original_stderr)
        # 统一代码与名称的格式，兼容不同数据源（避免 .str 引起的类型分析问题）
        if '代码' in all_stocks.columns:
            all_stocks['代码'] = ensure_str_series(cast(pd.Series, all_stocks['代码']))
            # 提取6位数字代码，兼容如 'sh600519' / 'sz000001'
            all_stocks['代码'] = extract_six_digit_code(cast(pd.Series, all_stocks['代码']))
            # 使用 apply 进行过滤与填充，确保类型保持为 Series
            all_stocks = all_stocks[cast(pd.Series, all_stocks['代码']).apply(lambda x: isinstance(x, str) and len(x) == 6)]
            all_stocks['代码'] = cast(pd.Series, all_stocks['代码']).apply(lambda x: x.zfill(6))
        if '名称' in all_stocks.columns:
            all_stocks['名称'] = ensure_str_series(cast(pd.Series, all_stocks['名称']))
    except Exception as e:
        logger.error(f"获取股票列表失败: {str(e)}")
        sys.exit(1)

    # 处理用户指定的股票代码
    if args.codes:
        # 将输入的股票代码字符串转换为列表
        stock_codes = args.codes.split(',')
        code_series = cast(pd.Series, all_stocks['代码'])
        stock_list = all_stocks[code_series.isin(stock_codes)][['代码', '名称']]
        if len(stock_list) < len(stock_codes):
            missing_codes = set(stock_codes) - set(stock_list['代码'])
            logger.warning(f"以下股票代码未找到: {', '.join(missing_codes)}")
        
        # 当指定了股票代码时，如果指定的代码数量小于K值，则将K值设置为代码数量
        # 如果指定的代码数量大于K值，则保留K值（只显示前K个）
        if len(stock_list) < args.k:
            logger.info(f"指定股票数量({len(stock_list)})小于K值({args.k})，自动将K值调整为: {len(stock_list)}")
            args.k = len(stock_list)
    else:
        # 获取所有股票代码
        stock_list = all_stocks[['代码', '名称']]
        logger.info(f"股票总数： {len(stock_list)}")
        try:
            from tqdm import tqdm as _tq
            _tq.write(f"股票总数： {len(stock_list)}", file=original_stderr)
        except Exception:
            pass
        # 使用显式掩码避免 .str 导致的类型检查误报
        st_mask = cast(pd.Series, stock_list['名称']).apply(lambda x: bool(re.search(r'(ST|退市)', str(x))))
        st_stocks = stock_list[st_mask]
        stock_list = stock_list[~st_mask]
        logger.info(f"排除 'ST以及退市' 股票 {len(st_stocks)} 只, 有效股票 {len(stock_list)} 只")
        try:
            from tqdm import tqdm as _tq
            _tq.write(f"排除 'ST以及退市' 股票 {len(st_stocks)} 只, 有效股票 {len(stock_list)} 只", file=original_stderr)
        except Exception:
            pass
        # 非'ST|退市'股票，使用显式 startswith 掩码
        code_s = cast(pd.Series, stock_list['代码']).apply(lambda x: str(x))
        sh_mask = code_s.apply(lambda x: x.startswith('6') and not x.startswith('688'))
        sz_mask = code_s.apply(lambda x: x.startswith('0'))
        kc_mask = code_s.apply(lambda x: x.startswith('688'))
        cy_mask = code_s.apply(lambda x: x.startswith('3'))
        bj_mask = code_s.apply(lambda x: x.startswith('8') and not x.startswith('688'))
        b_mask = code_s.apply(lambda x: x.startswith('2') or x.startswith('9'))
        other_mask = ~(code_s.apply(lambda x: x.startswith('0') or x.startswith('2') or x.startswith('3') or x.startswith('6') or x.startswith('8') or x.startswith('9')))
        sh_stocks = stock_list[sh_mask]
        sz_stocks = stock_list[sz_mask]
        kc_stocks = stock_list[kc_mask]
        cy_stocks = stock_list[cy_mask]
        bj_stocks = stock_list[bj_mask]
        b_stocks = stock_list[b_mask]
        other_stocks = stock_list[other_mask]
        if isall:
            stock_list = stock_list
            logger.info(f"上证主板 {len(sh_stocks)} 只，深证主板 {len(sz_stocks)} 只，"
                        f"科创板 {len(kc_stocks)} 只，创业板 {len(cy_stocks)} 只，"
                        f"北交所 {len(bj_stocks)} 只，B股 {len(b_stocks)} 只，"
                        f"其他股票 {len(other_stocks)} 只")
            logger.info(f"共计 {len(stock_list)} 只")
            try:
                from tqdm import tqdm as _tq
                _tq.write(
                    f"上证主板 {len(sh_stocks)} 只，深证主板 {len(sz_stocks)} 只，科创板 {len(kc_stocks)} 只，"
                    f"创业板 {len(cy_stocks)} 只，北交所 {len(bj_stocks)} 只，B股 {len(b_stocks)} 只，其他股票 {len(other_stocks)} 只",
                    file=original_stderr,
                )
                _tq.write(f"共计 {len(stock_list)} 只", file=original_stderr)
            except Exception:
                pass
        else:
            # 使用pd.concat()合并上证和深证股票
            objs2: List[pd.DataFrame] = [cast(pd.DataFrame, sh_stocks), cast(pd.DataFrame, sz_stocks)]
            stock_list = pd.concat(objs2, ignore_index=True)
            logger.info(f"上证主板 {len(sh_stocks)} 只，深证主板 {len(sz_stocks)} 只, 共计 {len(stock_list)} 只")
            try:
                from tqdm import tqdm as _tq
                _tq.write(f"上证主板 {len(sh_stocks)} 只，深证主板 {len(sz_stocks)} 只, 共计 {len(stock_list)} 只", file=original_stderr)
            except Exception:
                pass
            
    # 分析股票（显式标注类型，避免联合类型干扰）
    stock_list = cast(pd.DataFrame, stock_list)

    # 刷新缓存（可选）
    try:
        if getattr(args, 'refresh_cache', False) and (start_date and end_date):
            from modules.data_sources import refresh_cache_for_range
            refresh_cache_for_range(list(stock_list['代码']), start_date, end_date)
    except Exception:
        pass
    
    # 检查是否启用分钟级分析
    # 如果指定了--start-date或--end-date，强制使用日线分析
    if (args.mins or args.days == 5) and not (args.start_date or args.end_date):
        # 如果指定了-m参数，或者-d 5，则使用分钟级分析
        if args.mins:
            period = args.mins
            logger.info(f"启用分钟级分析，周期: {period}分钟")
        else:
            # 当-d 5且未指定-m时，自动使用60分钟数据
            period = 60
            logger.info(f"检测到-d 5，自动启用60分钟级分析")
        
        # 导入分钟级分析模块
        from modules.minute_analyzer import MinuteAnalyzer
        
        # 创建分钟级分析器实例
        analyzer = MinuteAnalyzer(period=period, use_simulation=bool(args.minute_sim))
        
        # 预检：快速检测分钟数据是否可用（选取第一只股票）
        results = []
        total_stocks = len(stock_list)
        logger.info(f"开始分析 {total_stocks} 只股票的{period}分钟数据...")
        try:
            from tqdm import tqdm as _tq
            _tq.write(f"开始分析 {total_stocks} 只股票的{period}分钟数据...", file=original_stderr)
        except Exception:
            pass
        try:
            if total_stocks > 0:
                first_code = str(stock_list.iloc[0]['代码'])
                first_name = str(stock_list.iloc[0]['名称'])
                precheck_days = args.days if args.days is not None else 5
                _pre_data = analyzer.get_minute_data(first_code, days=precheck_days)
                if (_pre_data is None or _pre_data.empty) and not args.minute_sim:
                    logger.warning("分钟数据不可用，且已禁用模拟。将自动回退到日线分析以避免长时间等待。")
                    # 回退到日线分析
                    results = analyze_stocks(stock_list, start_date, end_date, args.parallel, original_stderr, preloaded_data=all_stocks)
                    df = process_results(results)
                    # 保存并退出分钟分析分支
                    if not df.empty:
                        output_file = os.path.join(output_dir, 'analysis_results.csv')
                        df.to_csv(output_file, index=False, encoding='utf_8_sig')
                        logger.info(f"分析结果已保存至: {output_file}")
                        if not args.mins:
                            generate_stock_charts(df, start_date, end_date, output_dir, args.k)
                        # 当生成了图表且启用 AI 分析时，按单股生成并保存 AI 分析
                        if args.ai and not args.mins:
                            try:
                                chart_stocks = df.head(args.k)
                                for _, _stock in chart_stocks.iterrows():
                                    _code = _stock['代码']
                                    _name = _stock['名称']
                                    _chart_file = os.path.join(output_dir, f"{_code}_{_name}_analysis.png")
                                    _ai_result = get_ai_analysis(_chart_file, cfg.get('llm'))
                                    _ai_output_file = os.path.join(output_dir, f"{_code}_{_name}_ai_analysis.txt")
                                    save_ai_analysis(_ai_result, _ai_output_file)
                                    logger.info(f"已保存 {_code} {_name} 的 AI 分析结果")
                            except Exception as _ai_e:
                                logger.error(f"AI 分析失败: {_ai_e}")
                    return
        except Exception as _e:
            logger.debug(f"分钟数据预检异常: {_e}")
        
        # 并发处理分钟级分析，并加入阶段性保存，避免长时间运行未生成CSV
        days_param = args.days if args.days is not None else 5
        save_interval = max(25, args.parallel * 5)  # 每隔一定数量结果进行阶段性保存
        last_save_ts = time.time()

        def _stage_save_if_needed():
            nonlocal last_save_ts
            try:
                # 每达到间隔或超过时间阈值就保存一次
                if len(results) % save_interval == 0 or (time.time() - last_save_ts) >= 20:
                    df_tmp = pd.DataFrame(results)
                    if not df_tmp.empty:
                        df_tmp = df_tmp.sort_values('得分', ascending=False).reset_index(drop=True)
                        output_file = os.path.join(output_dir, 'analysis_results.csv')
                        df_tmp.to_csv(output_file, index=False, encoding='utf_8_sig')
                        logger.info(f"阶段性保存分析结果至: {output_file}（当前 {len(df_tmp)} 条）")
                        last_save_ts = time.time()
            except Exception as _sv_e:
                logger.warning(f"阶段性保存分析结果失败：{_sv_e}")

        # 使用线程池并发分析
        try:
            with ThreadPoolExecutor(max_workers=args.parallel) as executor:
                futures = []
                for _, stock in stock_list.iterrows():
                    stock_code = str(stock['代码'])
                    stock_name = str(stock['名称'])
                    futures.append(executor.submit(analyzer.analyze_stock_minute, stock_code, stock_name, days_param))

                with tqdm(total=total_stocks, desc="分钟分析进度", ncols=100, file=original_stderr, dynamic_ncols=True) as pbar:
                    for future in as_completed(futures):
                        try:
                            result = future.result()
                            if result:
                                results.append(result)
                                logger.info(f"完成分析 {result.get('代码', '')} {result.get('名称', '')}，得分: {result.get('得分', 'N/A')}")
                                _stage_save_if_needed()
                            else:
                                logger.warning("分钟分析失败（分钟数据不可用或已禁用模拟）")
                        except Exception as e:
                            logger.error(f"分钟分析线程执行出错: {str(e)}")
                        finally:
                            pbar.update(1)
        except Exception as _thr_e:
            logger.error(f"并发分钟分析初始化失败：{_thr_e}")
        
        logger.info(f"分钟级分析完成，成功分析 {len(results)}/{total_stocks} 只股票")
        
        # 处理分钟级分析结果（最终保存一次）
        df = pd.DataFrame(results)
        if not df.empty:
            # 按得分降序排序
            df = df.sort_values('得分', ascending=False)
            df = df.reset_index(drop=True)
            # 生成分钟图表（可选）
            if getattr(args, 'minute_chart', False):
                try:
                    from modules.minute_analyzer import MinuteAnalyzer as _MA
                    _ana = _MA(period=period, use_simulation=bool(args.minute_sim))
                    generate_minute_charts(df, _ana, days_param, output_dir, args.k, period)
                except Exception as _mc_e:
                    logger.warning(f"分钟图表生成失败：{_mc_e}")
    else:
        # 执行日线级分析
        results = analyze_stocks(stock_list, start_date, end_date, args.parallel, original_stderr, preloaded_data=all_stocks)
        # 处理结果
        df = process_results(results)
        try:
            if getattr(args, 'use_financial', False) and not df.empty:
                from modules.data_sources import get_financial_factors
                fin = get_financial_factors(list(df['代码']))
                if isinstance(fin, pd.DataFrame) and not fin.empty:
                    df = df.merge(fin, on='代码', how='left')
                    def _adj(row):
                        f = 1.0
                        try:
                            if pd.notna(row.get('roe')) and float(row['roe']) > 15.0:
                                f *= 1.05
                        except Exception:
                            pass
                        try:
                            if pd.notna(row.get('debt_ratio')) and float(row['debt_ratio']) > 60.0:
                                f *= 0.95
                        except Exception:
                            pass
                        try:
                            if pd.notna(row.get('pe_ttm')) and float(row['pe_ttm']) > 60.0:
                                f *= 0.95
                        except Exception:
                            pass
                        if f < 0.85:
                            f = 0.85
                        if f > 1.15:
                            f = 1.15
                        return float(row['得分']) * f
                    df['综合得分'] = df.apply(_adj, axis=1)
                    if not getattr(args, 'industry_neutral', False) and not getattr(args, 'topgains', False):
                        df = df.sort_values(['综合得分','代码'], ascending=[False, True]).reset_index(drop=True)
        except Exception:
            pass
    
    # 保存结果
    if not df.empty:
        # 前瞻模式下，强制按得分降序，便于明确 Top-K
        try:
            if getattr(args, 'forward', False):
                if getattr(args, 'topgains', False):
                    df = df.sort_values(['涨幅(%)', '代码'], ascending=[False, True])
                else:
                    df = df.sort_values(['得分', '代码'], ascending=[False, True])
        except Exception:
            pass
        output_file = os.path.join(output_dir, 'analysis_results.csv')
        df.to_csv(output_file, index=False, encoding='utf_8_sig')
        logger.info(f"分析结果已保存至: {output_file}")
        # 前瞻模式生成 Top-K 清单
        try:
            if getattr(args, 'forward', False):
                _top_df = df.head(args.k)
                _top_file = os.path.join(output_dir, 'analysis_top_k.csv')
                _top_df.to_csv(_top_file, index=False, encoding='utf_8_sig')
                logger.info(f"Top-K清单已保存至: { _top_file }")
        except Exception:
            pass

        # 生成图表（分钟级分析暂不生成图表）
        if not args.mins:
            generate_stock_charts(df, start_date, end_date, output_dir, args.k)

        # 验证所选股票在后续区间的表现
        try:
            _trend_day = getattr(args, 'trend_day', None)
            _validate_days = getattr(args, 'validate_days', None)
            if (not getattr(args, 'forward', False)) and (_validate_days is not None and int(_validate_days) > 0):
                try:
                    _end_dt = pd.to_datetime(end_date, format='%Y%m%d', errors='coerce')
                    if pd.isna(_end_dt):
                        _end_dt = pd.to_datetime(end_date, errors='coerce')
                except Exception:
                    _end_dt = pd.to_datetime(end_date, errors='coerce')
                _next_start_dt = _end_dt + timedelta(days=1)
                if _validate_days is not None and _validate_days > 0:
                    _next_end_dt = _next_start_dt + timedelta(days=int(_validate_days))
                else:
                    if bool(args.start_date and args.end_date):
                        try:
                            _sd = pd.to_datetime(args.start_date, format='%Y%m%d', errors='coerce')
                            if pd.isna(_sd):
                                _sd = pd.to_datetime(args.start_date, errors='coerce')
                        except Exception:
                            _sd = pd.to_datetime(args.start_date, errors='coerce')
                        _validate_span_days = max(1, int(((_end_dt - _sd).days)))
                        _next_end_dt = _next_start_dt + timedelta(days=_validate_span_days)
                    else:
                        _days_val = DEFAULT_DAYS if args.days is None else int(args.days)
                        _next_end_dt = _next_start_dt + timedelta(days=_days_val)

                _next_start_str = _next_start_dt.strftime('%Y%m%d')
                _next_end_str = _next_end_dt.strftime('%Y%m%d')

                _res_list: List[Dict[str, Any]] = []
                try:
                    _mult = int(getattr(args, 'candidate_mult', 0) or 0)
                except Exception:
                    _mult = 0
                if _mult <= 0:
                    if bool(getattr(args, 'require_profitable', False) or getattr(args, 'require_trend_hit', False)):
                        _eval_count = len(df)
                    else:
                        _mult = 5
                        _eval_count = min(len(df), args.k * _mult)
                else:
                    _eval_count = min(len(df), args.k * _mult)
                _cand_df = df.head(_eval_count)
                for _, _row in _cand_df.iterrows():
                    _code = str(_row['代码'])
                    _name = str(_row['名称'])
                    _start_price = float(_row['截止日价（元）'])
                    _hist = get_historical_data(_code, _next_start_str, _next_end_str, args)
                    if _hist is None or _hist.empty:
                        continue
                    try:
                        _end_price = float(_hist['close'].iloc[-1])
                        _actual_return = (_end_price - _start_price) / _start_price * 100.0
                    except Exception:
                        _end_price = _start_price
                        _actual_return = 0.0

                    try:
                        _max_price = float(_hist['high'].max())
                        _min_price = float(_hist['low'].min())
                        _max_gain = (_max_price - _start_price) / _start_price * 100.0
                        _max_loss = (_min_price - _start_price) / _start_price * 100.0
                    except Exception:
                        _max_gain = 0.0
                        _max_loss = 0.0

                    try:
                        _volatility = _hist['close'].pct_change().std() * 100.0
                    except Exception:
                        _volatility = 0.0

                    _trend_hit = None
                    _trend_hit_days = None
                    _trend_max_gain = None
                    if _trend_day is not None and int(_trend_day) > 0:
                        _trend_end_dt = _next_start_dt + timedelta(days=int(_trend_day))
                        _trend_end_str = _trend_end_dt.strftime('%Y%m%d')
                        _trend_hist = _hist.loc[_hist.index <= pd.to_datetime(_trend_end_str, format='%Y%m%d', errors='coerce')]
                        _trend_hist = _trend_hist.copy()
                        try:
                            _trend_gain_series = (_trend_hist['close'] - _start_price) / _start_price * 100.0
                            _trend_max_gain = float(_trend_gain_series.max()) if len(_trend_gain_series) > 0 else 0.0
                            _trend_hit = bool((_trend_hist['close'] > _start_price).any())
                            if _trend_hit:
                                _hit_idx = _trend_hist.index[_trend_hist['close'] > _start_price][0]
                                _trend_hit_days = int((_hit_idx - _next_start_dt).days)
                            else:
                                _trend_hit_days = -1
                        except Exception:
                            _trend_hit = False
                            _trend_hit_days = -1
                            _trend_max_gain = 0.0

                    _res = {
                        '代码': _code,
                        '名称': _name,
                        '预测截止日': end_date,
                        '验证起始日': _next_start_str,
                        '验证截止日': _next_end_str,
                        '得分': float(_row['得分']),
                        '起始价': round(_start_price, 2),
                        '验证期结束价': round(_end_price, 2),
                        '验证期涨幅(%)': round(_actual_return, 2),
                        '验证期最大涨幅(%)': round(_max_gain, 2),
                        '验证期最大跌幅(%)': round(_max_loss, 2),
                        '验证期波动率(%)': round(float(_volatility), 2),
                    }
                    if _trend_day is not None and int(_trend_day) > 0:
                        _res.update({
                            'trend_day': int(_trend_day),
                            'trend_day最大涨幅(%)': round(float(_trend_max_gain or 0.0), 2),
                            'trend_day命中': bool(_trend_hit),
                            'trend_day首日上涨天数': int(_trend_hit_days if _trend_hit_days is not None else -1)
                        })
                    _res_list.append(_res)

                _vdf = pd.DataFrame(_res_list)
                _vfile = os.path.join(output_dir, 'validation_results.csv')
                _vdf.to_csv(_vfile, index=False, encoding='utf_8_sig')
                logger.info(f"验证结果已保存至: { _vfile }")

                # 依据用户约束选择最终Top-K
                _final_sel = _vdf.copy()
                try:
                    if getattr(args, 'require_profitable', False):
                        _final_sel = _final_sel[_final_sel['验证期涨幅(%)'] > 0]
                    if getattr(args, 'require_trend_hit', False) and 'trend_day命中' in _final_sel.columns:
                        _final_sel = _final_sel[_final_sel['trend_day命中'] == True]
                except Exception:
                    pass
                # 按原排序对应的顺序截取前K
                try:
                    _final_sel = _final_sel.sort_values(['验证期涨幅(%)','代码'], ascending=[False, True])
                except Exception:
                    pass
                _final_sel = _final_sel.head(args.k)
                _final_file = os.path.join(output_dir, 'final_selection.csv')
                _final_sel.to_csv(_final_file, index=False, encoding='utf_8_sig')
                logger.info(f"最终选股已保存至: { _final_file }")

                # 如果最终选股为空，提示
                if len(_final_sel) == 0:
                    logger.warning("根据约束无法选出正收益/命中股票，请适当放宽条件或增大样本")

                # 生成验证摘要（针对最终选股）
                try:
                    _summary = {
                        '样本数': int(len(_final_sel)),
                        '平均验证期涨幅(%)': float(_final_sel['验证期涨幅(%)'].mean()) if len(_final_sel) > 0 else 0.0,
                        '平均验证期最大涨幅(%)': float(_final_sel['验证期最大涨幅(%)'].mean()) if len(_final_sel) > 0 else 0.0,
                        '平均验证期最大跌幅(%)': float(_final_sel['验证期最大跌幅(%)'].mean()) if len(_final_sel) > 0 else 0.0,
                        '正收益数量': int((_final_sel['验证期涨幅(%)'] > 0).sum()) if len(_final_sel) > 0 else 0,
                        '负收益数量': int((_final_sel['验证期涨幅(%)'] < 0).sum()) if len(_final_sel) > 0 else 0
                    }
                    if 'trend_day命中' in _final_sel.columns and len(_final_sel) > 0:
                        _summary['trend_day命中率(%)'] = float((_final_sel['trend_day命中'] == True).mean() * 100.0)
                    _sfile = os.path.join(output_dir, 'validation_summary.json')
                    import json as _json
                    with open(_sfile, 'w', encoding='utf-8') as _sf:
                        _json.dump(_summary, _sf, ensure_ascii=False, indent=2)
                    logger.info(f"验证分析摘要已保存至: { _sfile }")
                except Exception as _se:
                    logger.warning(f"保存验证摘要失败: { _se }")
        except Exception as _ve:
            logger.warning(f"验证分析执行失败: { _ve }")
        
        # 如果启用了AI分析
        if args.ai:
            if args.start_date or args.end_date:
                logger.warning("AI分析仅对实时数据时有意义，对于历史查询结果无效")
                logger.warning("如果希望执行AI分析，请使用'-d'参数")
                return
            logger.info("正在执行AI分析...")
            try:
                # 只处理生成图表的股票
                chart_stocks = df.head(args.k)
                # 为每个股票创建单独的AI分析文件
                for _, stock in chart_stocks.iterrows():
                    stock_code = stock['代码']
                    stock_name = stock['名称']
                    # 获取图表文件路径
                    chart_file = os.path.join(output_dir, f"{stock_code}_{stock_name}_analysis.png")
                    # 调用AI分析，仅传递必要信息
                    ai_result = get_ai_analysis(chart_file, cfg.get('llm'))
                    # 保存为单独的文件
                    ai_output_file = os.path.join(output_dir, f'{stock_code}_{stock_name}_ai_analysis.txt')
                    save_ai_analysis(ai_result, ai_output_file)
                    logger.info(f"已保存 {stock_code} {stock_name} 的 AI 分析结果")
            except Exception as e:
                logger.error(f"AI分析失败: {str(e)}")
        
    logger.info("分析完成！")
    # 输出目录路径到控制台
    try:
        print(f"分析完成！结果已保存至目录: {output_dir}")
    except Exception:
        pass

if __name__ == '__main__':
    multiprocessing.freeze_support()
    # 手动初始化 PyMiniRacer 以确保其资源被正确解压和加载（针对单文件/目录打包）
    # 这虽然不是必须的，但有助于预热 V8 引擎，避免在多线程中首次调用时发生竞争或延迟
    try:
        import py_mini_racer
        _ = py_mini_racer.MiniRacer()
    except Exception:
        pass
        
    try:
        main()
    except Exception as e:
        logger.error(f"程序执行出错: {str(e)}")
        logger.debug(traceback.format_exc())
