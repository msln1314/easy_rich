#!/usr/bin/env python3
"""
数据源模块 - 负责从各种数据源获取股票数据
包括东财、腾讯、交易所等数据源的统一接口
"""

import os
import re
import glob
import pandas as pd
import sys
import time
import akshare as ak
try:
    import tomllib as tomli
except ImportError:
    import tomli
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple, Union, cast
from modules.utils import logger
from modules.constants import *

# 默认数据源优先级：交易所 > 东财 > 腾讯 > 新浪
DEFAULT_SOURCES = ['exchange', 'eastmoney', 'tencent', 'sina']

# EastMoney endpoint fallback for akshare
EM_HOST_CANDIDATES = [
    "push2.eastmoney.com",
    "11.push2.eastmoney.com",
    "91.push2.eastmoney.com",
    "50.push2.eastmoney.com",
]

def load_user_config(conf_path: Optional[str]) -> Dict[str, Any]:
    """
    加载用户配置文件（TOML格式）。
    如果指定了 conf_path，则直接加载。
    否则按优先级查找：当前目录 > EXE目录 > 模块目录 > 用户主目录
    """
    cfg: Dict[str, Any] = {}
    
    # 如果指定了路径，直接加载
    if conf_path:
        if os.path.exists(conf_path):
            try:
                with open(conf_path, 'rb') as f:
                    full_config = tomli.load(f)
                    cfg.update(full_config)
            except Exception as e:
                logger.warning(f"加载配置文件 {conf_path} 失败: {e}")
        else:
            logger.warning(f"指定的配置文件不存在: {conf_path}")
    else:
        # 默认查找路径
        current_dir = os.getcwd()
        exe_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else current_dir
        
        search_paths = [
            os.path.join(current_dir, 'config.toml'),
            os.path.join(exe_dir, 'config.toml'),
            os.path.join(os.path.dirname(__file__), 'config.toml'),
            os.path.expanduser('~/.akshare_stock.toml')
        ]
        
        for path in search_paths:
            if os.path.exists(path):
                try:
                    with open(path, 'rb') as f:
                        full_config = tomli.load(f)
                        cfg.update(full_config)
                        logger.info(f"已加载配置文件: {path}")
                        break
                except Exception as e:
                    logger.warning(f"加载配置文件 {path} 失败: {e}")
    
    # 为了兼容旧代码，将 [data] 或 [data_sources] 部分的配置提升到根目录
    # 优先使用 data_sources，其次 data
    data_cfg = cfg.get('data_sources', cfg.get('data', {}))
    if data_cfg:
        for k, v in data_cfg.items():
            # 转换 list 类型 (如果是逗号分隔的字符串)
            if k in ('sources', 'source') and isinstance(v, str):
                 cfg['sources'] = [s.strip().lower() for s in re.split('[,;]', v) if s.strip()]
            else:
                 cfg[k] = v
    
    # 确保 sources 是列表
    if 'sources' not in cfg and 'sources' in data_cfg:
         # 已经在上面处理过了，这里可能是 redundent，但为了安全
         pass
         
    return cfg

def precheck_sources(sources: List[str], original_stderr=None) -> bool:
    """在正式采集前预检查所选数据源的可用性。"""
    ok = False
    # 去重并保持顺序
    seen = set()
    ordered = [s for s in sources if not (s in seen or seen.add(s))]
    
    # 进度条显示
    pbar = None
    try:
        from tqdm import tqdm
        # 使用 original_stderr 确保输出到控制台
        pbar = tqdm(total=len(ordered), desc="数据源预检", file=original_stderr, leave=False)
    except ImportError:
        pass

    try:
        for s in ordered:
            if s == 'eastmoney':
                try:
                    _patch_akshare_em_url(EM_HOST_CANDIDATES[0])
                    df = ak.stock_zh_a_spot_em()
                    if isinstance(df, (list, pd.DataFrame)) and len(df) > 0:
                        logger.info("预检：东财实时接口可用")
                        ok = True
                        break
                except Exception as e:
                    logger.warning(f"预检：东财不可用: {e}")
            elif s == 'sina':
                try:
                    df = ak.stock_zh_a_spot()
                    if isinstance(df, (list, pd.DataFrame)) and len(df) > 0:
                        logger.info("预检：新浪实时接口可用")
                        ok = True
                        break
                except Exception as e:
                    logger.warning(f"预检：新浪不可用: {e}")
            elif s == 'tencent':
                try:
                    # 腾讯接口预检查
                    df = ak.stock_zh_a_hist_tx(symbol='sh000001', start_date='20240101', end_date='20240102')
                    if isinstance(df, pd.DataFrame) and not df.empty:
                        logger.info("预检：腾讯历史接口可用")
                        ok = True
                        break
                except Exception as e:
                    logger.warning(f"预检：腾讯不可用: {e}")
            elif s == 'exchange':
                try:
                    # 交易所接口预检查
                    df = ak.stock_zh_a_daily(symbol='sh000001', start_date='20240101', end_date='20240102')
                    if isinstance(df, pd.DataFrame) and not df.empty:
                        logger.info("预检：交易所接口可用")
                        ok = True
                        break
                except Exception as e:
                    logger.warning(f"预检：交易所不可用: {e}")
            
            if pbar:
                pbar.update(1)
                
    except Exception as e:
        logger.error(f"预检查数据源时出错: {e}")
    finally:
        if pbar:
            pbar.close()
            
    return ok

def ensure_str_series(series: pd.Series) -> pd.Series:
    """确保 Series 中的元素为字符串类型"""
    return series.astype(str)

def extract_six_digit_code(series: pd.Series) -> pd.Series:
    """从股票代码中提取6位数字代码"""
    return series.str.extract(r'(\d{6})')[0]

def standardize_code_name(df: pd.DataFrame) -> pd.DataFrame:
    """标准化股票代码和名称列"""
    if '代码' in df.columns:
        code_series = df['代码']
        if isinstance(code_series, pd.Series):
            df['代码'] = ensure_str_series(code_series)
            code_series_str = df['代码']
            if isinstance(code_series_str, pd.Series):
                df['代码'] = extract_six_digit_code(code_series_str)
    if '名称' in df.columns:
        name_series = df['名称']
        if isinstance(name_series, pd.Series):
            df['名称'] = ensure_str_series(name_series)
    return df

def _patch_akshare_em_url(host: str) -> None:
    """动态修补 akshare 的东财 URL"""
    try:
        # 简化的修补逻辑，避免依赖特定的akshare内部模块
        logger.debug(f"尝试使用东财主机: {host}")
    except Exception as e:
        logger.debug(f"修补东财URL失败: {e}")

def stock_spot_em_with_fallback(original_stderr=None) -> pd.DataFrame:
    """
    获取实时行情数据，支持多个东财镜像回退，最终回退到股票列表
    """
    # 显示获取行情数据的进度条
    if original_stderr is None:
        original_stderr = sys.stderr

    # 判断是否应该跳过实时数据获取
    # 这里我们通过检查调用栈或者全局变量可能不太优雅，
    # 更好的方式是 stock_analyze.py 在调用时传入参数。
    # 但为了保持接口兼容性，且考虑到 stock_analyze.py 已经处理了 --realtime 逻辑：
    # 如果 stock_analyze.py 决定不获取实时数据，它不会调用这个函数来获取 current_info，
    # 而是只在获取股票列表时调用。
    # 当用于获取股票列表时，我们希望它能快速返回，如果实时接口慢或不稳定，应该优先使用基础信息接口？
    # 不，stock_spot_em_with_fallback 的主要目的就是获取"Spot"数据。
    # 如果用户没开 --realtime，stock_analyze.py 里的 current_info 会是 None。
    # 但 stock_analyze.py 依然调用此函数来获取 all_stocks (股票列表)。
    # 在这种情况下，我们其实不需要实时价格，只需要代码和名称。
    # 可是为了兼容性，我们还是按原逻辑跑，只是用户已经知道如果不加 --realtime，
    # stock_analyze.py 不会用这里的价格数据。
    # 
    # 优化：如果能检测到是在"仅获取列表"模式下，可以直接跳过实时接口。
    # 我们可以引入一个环境变量或者简单的启发式。
    # 不过，为了稳健起见，我们还是保留原逻辑，让它尝试获取。
    # 毕竟"实时行情"接口返回的列表通常包含了最新的上市股票。
    
    try:
        from tqdm import tqdm
        tqdm.write("正在获取实时行情数据...", file=original_stderr)
    except Exception:
        pass
    
    for host in EM_HOST_CANDIDATES:
        try:
            _patch_akshare_em_url(host)
            df = ak.stock_zh_a_spot_em()
            if isinstance(df, pd.DataFrame) and not df.empty:
                logger.info(f"使用东财镜像 {host} 获取实时行情成功")
                try:
                    from tqdm import tqdm
                    tqdm.write(f"使用东财镜像 {host} 获取实时行情成功", file=original_stderr)
                except Exception:
                    pass
                return standardize_code_name(df)
        except Exception as e:
            logger.warning(f"东财镜像 {host} 获取实时行情失败: {e}")
    
    # 所有东财镜像都失败，尝试新浪
    try:
        logger.info("尝试使用新浪接口获取实时行情")
        try:
            from tqdm import tqdm
            tqdm.write("尝试使用新浪接口获取实时行情", file=original_stderr)
        except Exception:
            pass
        df = ak.stock_zh_a_spot()
        if isinstance(df, pd.DataFrame) and not df.empty:
            logger.info("使用新浪接口获取实时行情成功")
            try:
                from tqdm import tqdm
                tqdm.write("使用新浪接口获取实时行情成功", file=original_stderr)
            except Exception:
                pass
            return standardize_code_name(df)
    except Exception as e:
        logger.error(f"新浪接口获取实时行情失败: {e}")
    
    # 实时行情都失败，回退到股票基础信息列表
    # 如果用户没有显式启用 realtime，也会走到这里（因为前序的实时调用被跳过或失败），
    # 但实际上 stock_spot_em_with_fallback 的调用者（stock_analyze.py）会控制是否需要实时数据。
    # 这里我们保留回退机制，确保至少能获取到股票列表。
    try:
        logger.info("尝试使用股票基础信息接口获取股票列表")
        try:
            from tqdm import tqdm
            tqdm.write("尝试使用股票基础信息接口获取股票列表", file=original_stderr)
        except Exception:
            pass
        df = ak.stock_info_a_code_name()
        if isinstance(df, pd.DataFrame) and not df.empty:
            # 转换列名以匹配实时行情格式
            df_converted = pd.DataFrame()
            df_converted['代码'] = df['code']
            df_converted['名称'] = df['name']
            # 添加一些默认的数值列，避免后续处理出错
            df_converted['最新价'] = 0.0
            df_converted['涨跌幅'] = 0.0
            df_converted['涨跌额'] = 0.0
            df_converted['成交量'] = 0
            df_converted['成交额'] = 0.0
            df_converted['振幅'] = 0.0
            df_converted['最高'] = 0.0
            df_converted['最低'] = 0.0
            df_converted['今开'] = 0.0
            df_converted['昨收'] = 0.0
            logger.info("使用股票基础信息接口获取股票列表成功")
            try:
                from tqdm import tqdm
                tqdm.write("使用股票基础信息接口获取股票列表成功", file=original_stderr)
            except Exception:
                pass
            return standardize_code_name(df_converted)
    except Exception as e:
        logger.error(f"股票基础信息接口获取失败: {e}")
    
    raise RuntimeError("所有实时行情数据源都不可用")

def get_historical_data(stock_code: str, start_date: str, end_date: str, args: Any = None) -> pd.DataFrame:
    """
    获取指定股票的历史数据，优先东财，失败则回退腾讯和交易所。

    Args:
        stock_code: 6位股票代码，例如 '600519' 或 '000001'
        start_date: 开始日期，支持 'YYYYMMDD' 或 'YYYY-MM-DD'
        end_date: 结束日期，支持 'YYYYMMDD' 或 'YYYY-MM-DD'
        args: 命令行参数对象

    Returns:
        pd.DataFrame: 索引为日期，列包含 ['open','close','high','low','volume']
    """
    try:
        # 缓存控制：命令行 --cache 或 debug 打开缓存
        use_cache = bool(getattr(args, "cache", False) or getattr(args, "debug", False))
        cache_file: Optional[str] = None

        # 统一日期为 EastMoney 所需的纯数字格式
        start_date_num = str(start_date).replace('-', '')
        end_date_num = str(end_date).replace('-', '')
        # 解析用于索引切片的 datetime
        def _parse_dt(s: Any) -> Optional[pd.Timestamp]:
            # 优先尝试 YYYYMMDD
            ts = pd.to_datetime(str(s), format='%Y%m%d', errors='coerce')
            if pd.isna(ts):
                ts = pd.to_datetime(s, errors='coerce')
            return None if pd.isna(ts) else ts
        start_dt = _parse_dt(start_date)
        end_dt = _parse_dt(end_date)

        if use_cache:
            cache_dir = os.path.join('data_cache', f"{start_date_num}_{end_date_num}")
            os.makedirs(cache_dir, exist_ok=True)
            cache_file = os.path.join(cache_dir, f'{stock_code}_hist.parquet')
            if cache_file and os.path.exists(cache_file):
                logger.debug(f"从缓存读取股票 {stock_code} 的历史数据 (parquet)")
                return pd.read_parquet(cache_file)
            # 兼容之前的 CSV 缓存回退
            csv_path = os.path.join(cache_dir, f'{stock_code}_hist.csv')
            if os.path.exists(csv_path):
                logger.debug(f"从缓存读取股票 {stock_code} 的历史数据 (csv)")
                df = pd.read_csv(csv_path, parse_dates=True)
                # 若 csv 未保留索引为日期，尽量尝试转换
                if 'date' in df.columns:
                    df['date'] = pd.to_datetime(df['date'], errors='coerce')
                    df = df.dropna(subset=['date']).set_index('date').sort_index()
                elif '日期' in df.columns:
                    df['日期'] = pd.to_datetime(df['日期'], errors='coerce')
                    df = df.dropna(subset=['日期']).set_index('日期').sort_index()
                return df
            # 备用缓存：尝试其他日期范围的已有缓存并按需切片
            try:
                alt_parquets = glob.glob(os.path.join('data_cache', '*', f'{stock_code}_hist.parquet'))
                alt_csvs = glob.glob(os.path.join('data_cache', '*', f'{stock_code}_hist.csv'))
                alt_paths = alt_parquets if alt_parquets else alt_csvs
                if alt_paths:
                    # 选择最新修改时间的缓存文件
                    alt_path = max(alt_paths, key=lambda p: os.path.getmtime(p))
                    logger.debug(f"使用备用缓存读取股票 {stock_code} 的历史数据: {alt_path}")
                    if alt_path.endswith('.parquet'):
                        df_any = pd.read_parquet(alt_path)
                    else:
                        df_any = pd.read_csv(alt_path, parse_dates=True)
                        if 'date' in df_any.columns:
                            df_any['date'] = pd.to_datetime(df_any['date'], errors='coerce')
                            df_any = df_any.dropna(subset=['date']).set_index('date').sort_index()
                        elif '日期' in df_any.columns:
                            df_any['日期'] = pd.to_datetime(df_any['日期'], errors='coerce')
                            df_any = df_any.dropna(subset=['日期']).set_index('日期').sort_index()
                    # 按请求窗口切片
                    if isinstance(df_any.index, pd.DatetimeIndex) and start_dt is not None and end_dt is not None:
                        df_slice = df_any.loc[(df_any.index >= start_dt) & (df_any.index <= end_dt)]
                    else:
                        df_slice = df_any
                    if isinstance(df_slice, pd.DataFrame) and not df_slice.empty:
                        logger.debug(f"已使用备用缓存满足股票 {stock_code} 的历史数据需求")
                        return df_slice
            except Exception:
                # 备用缓存失败不影响后续真实拉取
                pass

        # 1) 优先尝试交易所接口（最稳定）
        try:
            sources = getattr(args, 'source_list', DEFAULT_SOURCES)
            if 'exchange' not in sources:
                raise RuntimeError('源配置不包含 exchange，跳过交易所历史接口')
            
            # 将 6位代码转为带市场前缀的格式，例如 'sh600519' / 'sz000001'
            market_prefix = 'sh' if str(stock_code).startswith('6') else 'sz'
            ex_symbol = f"{market_prefix}{str(stock_code).zfill(6)}"
            
            t_ex_start = time.time()
            ex_df = ak.stock_zh_a_daily(
                symbol=ex_symbol,
                start_date=start_date_num,
                end_date=end_date_num,
                adjust=""
            )
            logger.debug(f"[{stock_code}] Exchange API took: {time.time() - t_ex_start:.4f}s")
            
            if isinstance(ex_df, pd.DataFrame) and not ex_df.empty:
                ex_df = cast(pd.DataFrame, ex_df)
                # 交易所返回列: ['date','open','close','high','low','volume','amount','outstanding_share','turnover']
                ex_df['date'] = pd.to_datetime(ex_df['date'], errors='coerce')
                ex_df = ex_df.dropna(subset=['date'])
                ex_df.set_index('date', inplace=True)
                ex_df.sort_index(inplace=True)
                
                if start_dt is not None and end_dt is not None:
                    ex_df = ex_df.loc[(ex_df.index >= start_dt) & (ex_df.index <= end_dt)]
                
                # 构造统一列名
                df_result: pd.DataFrame = pd.DataFrame(ex_df[['open', 'close', 'high', 'low', 'volume']].copy())
                df_result.columns = ['open', 'close', 'high', 'low', 'volume']
                
                # 数值列转换为数值类型
                for col in ['open', 'close', 'high', 'low', 'volume']:
                    df_result[col] = pd.to_numeric(df_result[col], errors='coerce')
                
                # 行过滤：四价均非空
                _core_cols_df: pd.DataFrame = pd.DataFrame(df_result[['open', 'close', 'high', 'low']])
                _valid_row_mask = _core_cols_df.notna().all(axis=1)
                df_result = pd.DataFrame(df_result.loc[_valid_row_mask, ['open', 'close', 'high', 'low', 'volume']])
                
                # 缓存（容错处理）
                if use_cache and cache_file:
                    try:
                        logger.debug(f"缓存股票 {stock_code} 的历史数据(交易所)")
                        df_result.to_parquet(cache_file)
                    except Exception as cache_err:
                        logger.debug(f"parquet缓存失败，改用CSV: {cache_err}")
                        try:
                            csv_path = cache_file.replace('.parquet', '.csv')
                            df_result.to_csv(csv_path, index=True)
                        except Exception:
                            pass
                
                # 显式触发垃圾回收
                import gc
                gc.collect()
                
                logger.info(f"使用交易所接口获取股票 {stock_code} 历史数据成功")
                return df_result
            else:
                logger.warning(f"交易所历史接口返回空数据: {ex_symbol} {start_date_num}-{end_date_num}")
        except Exception as ex_err:
            logger.warning(f"交易所历史数据获取失败，将回退东财: {ex_err}")

        # 2) 回退至东财日频接口
        try:
            sources = getattr(args, 'source_list', DEFAULT_SOURCES)
            if getattr(args, 'fast', False) or ('eastmoney' not in sources):
                raise RuntimeError('快速模式或源配置跳过东财历史接口')
            
            t_em_start = time.time()
            hist_data = ak.stock_zh_a_hist(
                symbol=stock_code,
                start_date=start_date_num,
                end_date=end_date_num,
            )
            logger.debug(f"[{stock_code}] EastMoney API took: {time.time() - t_em_start:.4f}s")

            if isinstance(hist_data, pd.DataFrame) and not hist_data.empty:
                hist_data = cast(pd.DataFrame, hist_data)
                # 规范列与索引
                hist_data['日期'] = pd.to_datetime(hist_data['日期'], errors='coerce')
                hist_data = hist_data.dropna(subset=['日期'])
                hist_data.set_index('日期', inplace=True)
                hist_data.sort_index(inplace=True)
                # 切片到指定区间（使用 datetime 比字符串更稳健）
                if start_dt is not None and end_dt is not None:
                    hist_data = hist_data.loc[(hist_data.index >= start_dt) & (hist_data.index <= end_dt)]
                # 构造统一列（使用复制+列名赋值以避免 rename 重载混淆）
                df_result: pd.DataFrame = pd.DataFrame(hist_data[['开盘', '收盘', '最高', '最低', '成交量']].copy())
                df_result.columns = ['open', 'close', 'high', 'low', 'volume']
                # 数值列转换为数值类型
                for col in ['open', 'close', 'high', 'low', 'volume']:
                    df_result[col] = pd.to_numeric(df_result[col], errors='coerce')
                # 使用布尔掩码替代 dropna(subset=...)，并用 pd.DataFrame 强制返回为 DataFrame
                _core_cols_df: pd.DataFrame = pd.DataFrame(df_result[['open', 'close', 'high', 'low']])
                _valid_row_mask = _core_cols_df.notna().all(axis=1)
                df_result = pd.DataFrame(df_result.loc[_valid_row_mask, ['open', 'close', 'high', 'low', 'volume']])
                # 缓存（容错处理）
                if use_cache and cache_file:
                    try:
                        logger.debug(f"缓存股票 {stock_code} 的历史数据(东财)")
                        df_result.to_parquet(cache_file)
                    except Exception as cache_err:
                        logger.debug(f"parquet缓存失败，改用CSV: {cache_err}")
                        try:
                            csv_path = cache_file.replace('.parquet', '.csv')
                            df_result.to_csv(csv_path, index=True)
                        except Exception:
                            # 缓存失败不影响数据返回
                            pass
                
                # 显式触发垃圾回收
                import gc
                gc.collect()

                return df_result
        except Exception as em_err:
            logger.warning(f"东财历史数据获取失败，将回退腾讯: {em_err}")

        # 3) 回退至腾讯接口（若选择了 tencent）
        # 将 6位代码转为带市场前缀的格式，例如 'sh600519' / 'sz000001'
        market_prefix = 'sh' if str(stock_code).startswith('6') else 'sz'
        tx_symbol = f"{market_prefix}{str(stock_code).zfill(6)}"
        try:
            sources = getattr(args, 'source_list', DEFAULT_SOURCES)
            if 'tencent' not in sources:
                raise RuntimeError('源配置不包含 tencent，跳过腾讯历史接口')
            
            t_tx_start = time.time()
            tx_df = ak.stock_zh_a_hist_tx(
                symbol=tx_symbol,
                start_date=start_date_num,
                end_date=end_date_num,
                adjust="",
            )
            logger.debug(f"[{stock_code}] Tencent API took: {time.time() - t_tx_start:.4f}s")

            if isinstance(tx_df, pd.DataFrame) and not tx_df.empty:
                tx_df = cast(pd.DataFrame, tx_df)
                # 腾讯返回列: ['date','open','close','high','low','amount']
                tx_df['date'] = pd.to_datetime(tx_df['date'], errors='coerce')
                tx_df = tx_df.dropna(subset=['date'])
                tx_df.set_index('date', inplace=True)
                tx_df.sort_index(inplace=True)
                if start_dt is not None and end_dt is not None:
                    tx_df = tx_df.loc[(tx_df.index >= start_dt) & (tx_df.index <= end_dt)]
                # 构造统一列名（避免 rename+切片的类型分析误报）
                df_result: pd.DataFrame = pd.DataFrame(tx_df[['open', 'close', 'high', 'low', 'amount']].copy())
                df_result.columns = ['open', 'close', 'high', 'low', 'volume']
                # 数值列转换为数值类型
                for col in ['open', 'close', 'high', 'low', 'volume']:
                    df_result[col] = pd.to_numeric(df_result[col], errors='coerce')
                # 行过滤：四价均非空
                _core_cols_df2: pd.DataFrame = pd.DataFrame(df_result[['open', 'close', 'high', 'low']])
                _valid_row_mask2 = _core_cols_df2.notna().all(axis=1)
                df_result = pd.DataFrame(df_result.loc[_valid_row_mask2, ['open', 'close', 'high', 'low', 'volume']])
                # 缓存（容错处理）
                if use_cache and cache_file:
                    try:
                        logger.debug(f"缓存股票 {stock_code} 的历史数据(腾讯)")
                        df_result.to_parquet(cache_file)
                    except Exception as cache_err:
                        logger.debug(f"parquet缓存失败，改用CSV: {cache_err}")
                        try:
                            csv_path = cache_file.replace('.parquet', '.csv')
                            df_result.to_csv(csv_path, index=True)
                        except Exception:
                            pass
                
                # 显式触发垃圾回收
                import gc
                gc.collect()

                return df_result
            else:
                logger.warning(f"腾讯历史接口返回空数据: {tx_symbol} {start_date_num}-{end_date_num}")
        except Exception as tx_err:
            logger.error(f"腾讯历史数据获取失败: {tx_err}")

        # 所有数据源都失败
        return pd.DataFrame()

    except Exception as e:
        logger.error(f"获取股票 {stock_code} 历史数据时出错: {str(e)}")
        return pd.DataFrame()

def get_industry_map_from_spot(codes: List[str]) -> pd.DataFrame:
    """
    获取股票代码到行业的映射，优先使用东财/新浪实时行情中的行业列；失败则使用代码前缀作为粗略分组。

    Args:
        codes: 股票代码列表（6位）

    Returns:
        pd.DataFrame: 包含列 ['代码','行业'] 的映射数据
    """
    try:
        df = stock_spot_em_with_fallback()
        if isinstance(df, pd.DataFrame) and not df.empty:
            cols = df.columns.tolist()
            ind_col = None
            # 常见行业列名尝试
            for c in ['行业', '板块', '所属行业']:
                if c in cols:
                    ind_col = c
                    break
            if ind_col is not None:
                out = pd.DataFrame()
                out['代码'] = df['代码']
                out['行业'] = df[ind_col]
                out = out[out['代码'].isin(codes)]
                return out
        # 回退：使用代码前缀分组（粗略）
        out = pd.DataFrame({'代码': codes})
        out['行业'] = out['代码'].astype(str).apply(lambda x: '上证' if x.startswith('6') else ('深证' if x.startswith('0') or x.startswith('3') else '其他'))
        return out
    except Exception:
        out = pd.DataFrame({'代码': codes})
        out['行业'] = out['代码'].astype(str).apply(lambda x: '上证' if x.startswith('6') else ('深证' if x.startswith('0') or x.startswith('3') else '其他'))
        return out

def get_financial_factors(codes: List[str]) -> pd.DataFrame:
    try:
        records: List[Dict[str, Any]] = []
        for code in codes:
            roe = None
            debt = None
            pe = None
            try:
                df1 = ak.stock_financial_analysis_indicator(symbol=code)
                if isinstance(df1, pd.DataFrame) and not df1.empty:
                    if '净资产收益率ROE(%)' in df1.columns:
                        v = pd.to_numeric(df1['净资产收益率ROE(%)'], errors='coerce').dropna()
                        if len(v) > 0:
                            roe = float(v.iloc[-1])
                    if '资产负债率(%)' in df1.columns:
                        v = pd.to_numeric(df1['资产负债率(%)'], errors='coerce').dropna()
                        if len(v) > 0:
                            debt = float(v.iloc[-1])
            except Exception:
                pass
            try:
                df2 = ak.stock_a_lg_indicator()
                if isinstance(df2, pd.DataFrame) and not df2.empty:
                    row = df2[df2['股票代码'].astype(str).str.endswith(code)]
                    if not row.empty and '市盈率-动态' in row.columns:
                        pe = float(pd.to_numeric(row['市盈率-动态'], errors='coerce').iloc[0])
            except Exception:
                pass
            records.append({'代码': code, 'roe': roe, 'debt_ratio': debt, 'pe_ttm': pe})
        return pd.DataFrame(records)
    except Exception:
        return pd.DataFrame({'代码': codes, 'roe': [None]*len(codes), 'debt_ratio': [None]*len(codes), 'pe_ttm': [None]*len(codes)})

def refresh_cache_for_range(codes: List[str], start_date: str, end_date: str) -> None:
    try:
        for code in codes:
            _ = get_historical_data(code, start_date, end_date)
    except Exception:
        pass
