import akshare as ak
import pandas as pd
from datetime import datetime, timedelta
import inspect
import time
import threading
import asyncio
from typing import Dict, List, Optional

# Stock Service Client for stock data
from apps.module_task.stock_service_client import StockServiceClient


_A_STOCK_SPOT_CACHE_LOCK = threading.Lock()
_A_STOCK_SPOT_CACHE_FETCHED_AT: float = 0.0
_A_STOCK_SPOT_CACHE_BY_CODE: Optional[Dict[str, Dict]] = None


def _normalize_a_stock_code(stock_code: str) -> str:
    if not stock_code:
        return ""
    stock_code = str(stock_code).strip()
    # Common cases: "600519", "600519.SH", "SZ000001"
    for part in (stock_code.split(".")[0], stock_code):
        digits = "".join(ch for ch in part if ch.isdigit())
        if len(digits) == 6:
            return digits
    return stock_code


def get_all_stock_spot_map(cache_ttl_seconds: int = 30, force_refresh: bool = False) -> Optional[Dict[str, Dict]]:
    """Return a cached mapping {code -> row_dict} built from Stock Service."""
    global _A_STOCK_SPOT_CACHE_FETCHED_AT, _A_STOCK_SPOT_CACHE_BY_CODE

    now = time.time()
    with _A_STOCK_SPOT_CACHE_LOCK:
        if (
            not force_refresh
            and _A_STOCK_SPOT_CACHE_BY_CODE is not None
            and (now - _A_STOCK_SPOT_CACHE_FETCHED_AT) < max(cache_ttl_seconds, 1)
        ):
            return _A_STOCK_SPOT_CACHE_BY_CODE

        try:
            # 使用 StockServiceClient 获取数据
            async def _fetch_stock_list():
                async with StockServiceClient() as client:
                    return await client.get_all_stock_list()

            # 运行异步函数
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    import concurrent.futures
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(asyncio.run, _fetch_stock_list())
                    stock_list = future.result(timeout=30)
                else:
                    stock_list = loop.run_until_complete(_fetch_stock_list())
            except RuntimeError:
                stock_list = asyncio.run(_fetch_stock_list())

            if not stock_list:
                return _A_STOCK_SPOT_CACHE_BY_CODE

            # Build once for O(1) lookups during holdings loops
            by_code = {}
            for stock in stock_list:
                code = stock.get('code', '')
                if code:
                    by_code[code] = {
                        '代码': code,
                        '名称': stock.get('name', ''),
                        '最新价': stock.get('price'),
                        '涨跌幅': stock.get('change_percent'),
                        '涨跌额': stock.get('change'),
                        '成交量': stock.get('volume'),
                        '成交额': stock.get('amount'),
                        '最高': stock.get('high'),
                        '最低': stock.get('low'),
                        '今开': stock.get('open'),
                        '昨收': stock.get('pre_close'),
                    }

            _A_STOCK_SPOT_CACHE_BY_CODE = by_code
            _A_STOCK_SPOT_CACHE_FETCHED_AT = time.time()
            return by_code
        except Exception as e:
            print(f"Error refreshing stock spot map: {e}")
            return _A_STOCK_SPOT_CACHE_BY_CODE

def get_stock_history(code: str, days: int = 100) -> List[Dict]:
    """
    Fetch daily history for a stock.
    Returns: List of {date, value, volume, ...}
    """
    try:
        code = _normalize_a_stock_code(code)
        if not code:
            return []

        # 使用 StockServiceClient 获取数据
        async def _fetch_history():
            async with StockServiceClient() as client:
                end_date = datetime.now()
                start_date = end_date - timedelta(days=int(days * 1.6))
                start_str = start_date.strftime("%Y%m%d")
                end_str = end_date.strftime("%Y%m%d")
                return await client.get_stock_history(code, period="daily", start_date=start_str, end_date=end_str)

        # 运行异步函数
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # 如果在异步环境中，创建新的线程运行
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, _fetch_history())
                    history_data = future.result(timeout=30)
            else:
                history_data = loop.run_until_complete(_fetch_history())
        except RuntimeError:
            history_data = asyncio.run(_fetch_history())

        if not history_data:
            return []

        # 标准化返回格式
        result = []
        for item in history_data:
            result.append({
                "date": str(item.get('date', '')),
                "value": float(item.get('close', 0)),
                "volume": float(item.get('volume', 0))
            })

        return result
    except Exception as e:
        print(f"Error fetching history for {code}: {e}")
        return []

# ============================================================================
# SECTION 1: 全球宏观市场数据 (Global Macro Data)
# ============================================================================

def get_us_market_overview() -> Dict:
    """
    获取隔夜美股市场概览：三大指数
    Returns: {指数名: {最新价, 涨跌幅, ...}}
    """
    result = {}
    try:
        # 使用全球指数接口获取美股三大指数
        df = ak.index_global_spot_em()
        if not df.empty:
            # 美股三大指数映射 (Name -> Code for reference, but here we search by Name)
            # Actually index_global_spot_em has '名称' column.
            # We want to match these names:
            target_names = ['道琼斯', '纳斯达克', '标普500']
            
            # Optimized: Filter dataframe directly
            filtered_df = df[df['名称'].isin(target_names)]
            
            for _, r in filtered_df.iterrows():
                name = r['名称']
                result[name] = {
                    '最新价': r.get('最新价', 'N/A'),
                    '涨跌额': r.get('涨跌额', 'N/A'),
                    '涨跌幅': f"{r.get('涨跌幅', 0)}%",
                    '开盘价': r.get('开盘价', 'N/A'),
                    '最高价': r.get('最高价', 'N/A'),
                    '最低价': r.get('最低价', 'N/A'),
                    '更新时间': r.get('最新行情时间', 'N/A')
                }
    except Exception as e:
        print(f"Error fetching US market: {e}")
    
    return result if result else {"说明": "美股数据暂时无法获取"}

def get_a50_futures() -> Dict:
    """
    获取富时A50相关指数数据
    由于直接A50期货数据不稳定，使用全球指数中的新加坡/恒生指数作为亚太市场参考
    """
    result = {}
    try:
        # 方案1：从全球指数获取亚太市场数据
        df = ak.index_global_spot_em()
        if not df.empty:
            # 获取相关亚太指数
            target_names = ['恒生指数', '富时新加坡海峡时报', '日经225']
            
            # Optimized filtering
            filtered_df = df[df['名称'].isin(target_names)]
            
            for _, r in filtered_df.iterrows():
                name = r['名称']
                result[name] = {
                    '最新价': r.get('最新价', 'N/A'),
                    '涨跌幅': r.get('涨跌幅', 'N/A'),
                    '更新时间': r.get('最新行情时间', 'N/A')
                }
    except Exception as e:
        print(f"Error fetching A50/Asia index: {e}")
    
    if not result:
        return {"说明": "A50期货数据暂时无法获取，请关注盘前竞价"}
    return result

def get_forex_rates() -> Dict:
    """
    获取关键汇率：美元/人民币
    """
    result = {}
    try:
        df = ak.fx_spot_quote()
        if not df.empty:
            # fx_spot_quote 返回的列是: 货币对, 买报价, 卖报价
            usdcny = df[df['货币对'].str.contains('USD/CNY', na=False, case=False)]
            if not usdcny.empty:
                row = usdcny.iloc[0]
                result["美元/人民币"] = {
                    "货币对": row.get('货币对', 'USD/CNY'),
                    "买入价": row.get('买报价', 'N/A'),
                    "卖出价": row.get('卖报价', 'N/A')
                }
            
            # 获取其他重要汇率
            eurcny = df[df['货币对'].str.contains('EUR/CNY', na=False, case=False)]
            if not eurcny.empty:
                row = eurcny.iloc[0]
                result["欧元/人民币"] = {
                    "买入价": row.get('买报价', 'N/A'),
                    "卖出价": row.get('卖报价', 'N/A')
                }
    except Exception as e:
        print(f"Error fetching forex: {e}")
    
    # 备选方案：使用百度汇率
    if not result:
        try:
            fx_data = ak.fx_quote_baidu()
            if not fx_data.empty:
                usd = fx_data[fx_data['货币'].str.contains('美元', na=False)]
                if not usd.empty:
                    result["美元/人民币"] = {"最新价": usd.iloc[0].get('现汇买入价', 'N/A')}
        except Exception as e:
            print(f"Baidu forex fallback failed: {e}")
    
    return result if result else {"说明": "汇率数据暂时无法获取"}

def get_global_macro_summary() -> Dict:
    """
    汇总全球宏观数据 - 盘前分析核心输入
    """
    return {
        "美股市场": get_us_market_overview(),
        "A50期货": get_a50_futures(),
        "汇率": get_forex_rates()
    }

# ============================================================================
# SECTION 2: 北向资金与资金流向 (Capital Flow)
# ============================================================================

def get_northbound_flow() -> Dict:
    """
    获取北向资金（沪股通+深股通）净流入数据
    从 Stock Service 获取数据
    """
    result = {}
    try:
        # 使用 StockServiceClient 获取数据
        async def _fetch_north_money():
            async with StockServiceClient() as client:
                # 获取实时北向资金
                realtime = await client.get_realtime_north_money()
                # 获取北向资金汇总
                summary = await client.get_north_money_summary()
                return realtime, summary

        # 运行异步函数
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, _fetch_north_money())
                    realtime, summary = future.result(timeout=10)
            else:
                realtime, summary = loop.run_until_complete(_fetch_north_money())
        except RuntimeError:
            realtime, summary = asyncio.run(_fetch_north_money())

        # 处理实时数据
        if realtime:
            sh_flow = realtime.get('sh_hk_flow', 0)
            sz_flow = realtime.get('sz_hk_flow', 0)
            total_flow = realtime.get('total_flow', 0)

            result['沪股通'] = {
                '成交净买额': f"{sh_flow:.2f}亿",
            }
            result['深股通'] = {
                '成交净买额': f"{sz_flow:.2f}亿",
            }
            result['最新净流入'] = f"{total_flow:.2f}亿"
            result['数据日期'] = realtime.get('date', 'N/A')
            result['更新时间'] = realtime.get('time', 'N/A')

        # 处理汇总数据
        if summary and summary.get('items'):
            for item in summary['items']:
                channel = item.get('channel', '')
                net_buy = item.get('net_buy_amount', 0)
                if '沪股通' in channel or '港股通(沪)' in channel:
                    result['沪股通'] = {
                        '成交净买额': f"{net_buy:.2f}亿",
                        '交易状态': '交易中' if item.get('status') else '休市',
                    }
                elif '深股通' in channel or '港股通(深)' in channel:
                    result['深股通'] = {
                        '成交净买额': f"{net_buy:.2f}亿",
                        '交易状态': '交易中' if item.get('status') else '休市',
                    }

    except Exception as e:
        print(f"Error fetching northbound flow: {e}")

    return result if result else {"说明": "北向资金数据暂时无法获取"}

def get_industry_capital_flow(industry: str = None) -> Dict:
    """
    获取行业资金流向
    从 Stock Service 获取数据
    """
    try:
        # 使用 StockServiceClient 获取数据
        async def _fetch_flow():
            async with StockServiceClient() as client:
                return await client.get_market_fund_flow(days=1)

        # 运行异步函数
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, _fetch_flow())
                    flow_data = future.result(timeout=10)
            else:
                flow_data = loop.run_until_complete(_fetch_flow())
        except RuntimeError:
            flow_data = asyncio.run(_fetch_flow())

        if not flow_data:
            return {}

        # 返回今日资金流向数据
        today = flow_data[-1] if flow_data else {}
        if industry:
            # 暂不支持行业筛选，返回今日数据
            return today

        return {"今日资金流向": today}
    except Exception as e:
        print(f"Error fetching industry capital flow: {e}")
    return {}

# ============================================================================
# SECTION 3: 个股深度数据 (Stock Deep Dive)
# ============================================================================

def get_stock_announcement(stock_code: str, stock_name: str) -> List[Dict]:
    """
    获取个股最新公告（巨潮资讯）
    """
    announcements = []
    try:
        # 尝试获取公告 - 使用巨潮资讯接口，支持更多市场（包括北交所）
        df = ak.stock_zh_a_disclosure_report_cninfo(symbol=stock_code)
        if df is not None and not df.empty:
            # 按时间倒序排序 (API通常已排序，但也可能未排序)
            if '公告时间' in df.columns:
                 df.sort_values(by='公告时间', ascending=False, inplace=True)
            
            # 最近5条公告
            recent = df.head(5)
            announcements = recent.to_dict('records')
    except Exception as e:
        print(f"Error fetching announcements for {stock_name} ({stock_code}): {e}")
    return announcements

def get_stock_realtime_quote(
    stock_code: str,
    use_cache: bool = True,
    cache_ttl_seconds: int = 30,
    force_refresh: bool = False,
) -> Dict:
    """
    获取个股实时/最新行情
    从 Stock Service 获取数据
    """
    try:
        code = _normalize_a_stock_code(stock_code)
        if not code:
            return {}

        # 使用 StockServiceClient 获取数据
        async def _fetch_quote():
            async with StockServiceClient() as client:
                return await client.get_stock_quote(code)

        # 运行异步函数
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, _fetch_quote())
                    quote_data = future.result(timeout=10)
            else:
                quote_data = loop.run_until_complete(_fetch_quote())
        except RuntimeError:
            quote_data = asyncio.run(_fetch_quote())

        if not quote_data:
            return {}

        # 标准化返回格式
        return {
            '代码': code,
            '名称': quote_data.get('name', ''),
            '最新价': quote_data.get('price'),
            '涨跌幅': quote_data.get('change_percent'),
            '涨跌额': quote_data.get('change'),
            '成交量': quote_data.get('volume'),
            '成交额': quote_data.get('amount'),
            '最高': quote_data.get('high'),
            '最低': quote_data.get('low'),
            '今开': quote_data.get('open'),
            '昨收': quote_data.get('pre_close'),
            '量比': quote_data.get('volume_ratio'),
            '换手率': quote_data.get('turnover_rate'),
        }

    except Exception as e:
        print(f"Error fetching realtime quote for {stock_code}: {e}")
    return {}

def get_stock_news_sentiment(stock_name: str) -> List[Dict]:
    """
    获取个股相关新闻（东方财富）
    """
    try:
        df = ak.stock_news_em(symbol=stock_name)
        if not df.empty:
            return df.head(5).to_dict('records')
    except Exception as e:
        print(f"Error fetching news for {stock_name}: {e}")
    return []

# ============================================================================
# SECTION 4: 行业与板块数据 (Sector Data)
# ============================================================================

def get_sector_performance(sector_name: str = None) -> Dict:
    """
    获取板块行情表现
    从 Stock Service 获取数据
    """
    try:
        # 使用 StockServiceClient 获取数据
        async def _fetch_boards():
            async with StockServiceClient() as client:
                return await client.get_industry_boards()

        # 运行异步函数
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, _fetch_boards())
                    boards = future.result(timeout=10)
            else:
                boards = loop.run_until_complete(_fetch_boards())
        except RuntimeError:
            boards = asyncio.run(_fetch_boards())

        if not boards:
            return {}

        if sector_name:
            # 模糊匹配
            filtered = [b for b in boards if sector_name in b.get('name', '')]
            if filtered:
                return filtered[0]
            return {}

        # 返回前10行业
        return {"板块涨幅榜": boards[:10]}
    except Exception as e:
        print(f"Error fetching sector performance: {e}")
    return {}

def get_sector_performance_ths(sector_name: str) -> Dict:
    """
    获取同花顺行业板块表现
    """
    try:
        # 1. Get all board names
        boards = ak.stock_board_industry_name_ths()
        if boards.empty:
            return {}
            
        target_name = None
        # Simple fuzzy match
        # If input is "半导体", match "半导体"
        # If input is "新能源", match "新能源汽车" or similar?
        # Let's try exact match first, then contains
        
        # Check if direct match exists
        if sector_name in boards['name'].values:
            target_name = sector_name
        else:
            # Contains
            matches = boards[boards['name'].str.contains(sector_name, na=False, regex=False)]
            if not matches.empty:
                target_name = matches.iloc[0]['name']
        
        if not target_name:
            return {}
            
        # 2. Fetch Index Data
        # akshare expects start/end date usually to reduce data
        end_date = datetime.now().strftime("%Y%m%d")
        start_date = (datetime.now() - timedelta(days=10)).strftime("%Y%m%d")
        
        df = ak.stock_board_industry_index_ths(symbol=target_name, start_date=start_date, end_date=end_date)
        
        if not df.empty:
            latest = df.iloc[-1]
            # Calculate change
            change_pct = "N/A"
            if len(df) >= 2:
                prev = df.iloc[-2]['收盘价']
                curr = latest['收盘价']
                if prev and float(prev) != 0:
                    pct = ((float(curr) - float(prev)) / float(prev)) * 100
                    change_pct = f"{pct:.2f}"
            
            return {
                "板块名称": target_name,
                "收盘价": latest['收盘价'],
                "涨跌幅": change_pct,
                "成交量": latest['成交量'],
                "成交额": latest['成交额'],
                "日期": latest['日期']
            }
            
    except Exception as e:
        print(f"Error fetching THS sector performance for {sector_name}: {e}")
    return {}

def get_concept_board_performance(concept: str = None) -> Dict:
    """
    获取概念板块表现（如：AI、新能源等）
    从 Stock Service 获取数据
    """
    try:
        # 使用 StockServiceClient 获取数据
        async def _fetch_boards():
            async with StockServiceClient() as client:
                return await client.get_concept_boards()

        # 运行异步函数
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, _fetch_boards())
                    boards = future.result(timeout=10)
            else:
                boards = loop.run_until_complete(_fetch_boards())
        except RuntimeError:
            boards = asyncio.run(_fetch_boards())

        if not boards:
            return {}

        if concept:
            # 模糊匹配
            filtered = [b for b in boards if concept in b.get('name', '')]
            if filtered:
                return filtered
            return {}

        # 返回前10概念板块
        return {"概念板块Top10": boards[:10]}
    except Exception as e:
        print(f"Error fetching concept board: {e}")
    return {}

# ============================================================================
# SECTION 5: 原有函数（保留并优化）
# ============================================================================

def get_fund_info(fund_code: str):
    """
    Fetch basic fund information and net value history.
    Uses akshare's fund_open_fund_info_em or similar.
    """
    try:
        # Fetching net value history
        df = ak.fund_open_fund_info_em(symbol=fund_code, indicator="单位净值走势")

        if df is None or df.empty:
            return pd.DataFrame()

        # Expected columns: 净值日期, 单位净值, 日增长率
        # NOTE: Some environments may return mojibake column names (encoding issues).
        # To keep downstream logic stable, normalize columns when we can.
        if '净值日期' not in df.columns:
            cols = list(df.columns)
            if len(cols) >= 3:
                df = df.rename(
                    columns={
                        cols[0]: '净值日期',
                        cols[1]: '单位净值',
                        cols[2]: '日增长率',
                    }
                )

        # Sort by date descending so iloc[0] is the latest NAV
        if '净值日期' in df.columns:
            df['净值日期'] = pd.to_datetime(df['净值日期'], errors='coerce')
            df = df.sort_values('净值日期', ascending=False).reset_index(drop=True)
            # Keep a consistent display format
            df['净值日期'] = df['净值日期'].dt.date
        return df
    except Exception as e:
        print(f"Error fetching fund info for {fund_code}: {e}")
        return pd.DataFrame()

def get_fund_holdings(fund_code: str, year: str = None):
    """
    Fetch the latest top 10 holdings for the fund.
    Defaults to the current year if not specified.
    """
    current_year = str(datetime.now().year)
    if not year:
        year = current_year
    
    try:
        # fund_portfolio_hold_em signature varies by AkShare version.
        # In the installed AkShare (2024/06+), it is: fund_portfolio_hold_em(symbol, date)
        sig = None
        try:
            sig = inspect.signature(ak.fund_portfolio_hold_em)
        except Exception:
            sig = None

        def _call_holdings(target_year: str):
            if sig and "symbol" in sig.parameters:
                return ak.fund_portfolio_hold_em(symbol=fund_code, date=target_year)
            # Fallback for older/newer variants: try positional to avoid keyword mismatches
            try:
                return ak.fund_portfolio_hold_em(fund_code, target_year)
            except TypeError:
                # Last-resort: try legacy keywords if positional fails
                return ak.fund_portfolio_hold_em(code=fund_code, year=target_year)

        # fund_portfolio_hold_em: returns holding details
        df = _call_holdings(year)
        
        # Fallback to previous year if current year is empty (common in early Jan)
        if df.empty and year == current_year:
            prev_year = str(int(year) - 1)
            print(f"DEBUG: No data for {year}, trying {prev_year}...")
            df = _call_holdings(prev_year)

        # We generally want the latest quarter available
        if not df.empty:
            # Sort by date/quarter to get the latest
            # This API usually returns all quarters for the year.
            # We might need to filter for the latest '季度'
            return df
        return df
    except Exception as e:
        print(f"Error fetching holdings for {fund_code}: {e}")
        return pd.DataFrame()

def get_market_indices():
    """
    获取关键市场指数数据
    从 Stock Service 获取数据
    """
    market_data: Dict[str, Dict] = {}

    try:
        # 使用 StockServiceClient 获取数据
        async def _fetch_indices():
            async with StockServiceClient() as client:
                return await client.get_index_quotes()

        # 运行异步函数
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, _fetch_indices())
                    indices = future.result(timeout=10)
            else:
                indices = loop.run_until_complete(_fetch_indices())
        except RuntimeError:
            indices = asyncio.run(_fetch_indices())

        if not indices:
            return {}

        for idx in indices:
            name = idx.get('name', '')
            if '上证' in name or '沪指' in name:
                market_data['上证指数'] = {
                    '日期': idx.get('update_time', ''),
                    '收盘': idx.get('price'),
                    '涨跌幅': idx.get('change_percent'),
                }
            elif '深证' in name or '深成' in name:
                market_data['深证成指'] = {
                    '日期': idx.get('update_time', ''),
                    '收盘': idx.get('price'),
                    '涨跌幅': idx.get('change_percent'),
                }
            elif '创业' in name:
                market_data['创业板指'] = {
                    '日期': idx.get('update_time', ''),
                    '收盘': idx.get('price'),
                    '涨跌幅': idx.get('change_percent'),
                }
            elif '科创' in name:
                market_data['科创50'] = {
                    '日期': idx.get('update_time', ''),
                    '收盘': idx.get('price'),
                    '涨跌幅': idx.get('change_percent'),
                }

        return market_data
    except Exception as e:
        print(f"Error fetching market indices: {e}")
        return {}

def get_all_fund_list() -> List[Dict]:

    """

    获取全市场所有基金列表

    Returns: List of dicts with 'code', 'name', 'type', etc.

    """

    try:

        # fund_name_em returns: 基金代码, 基金简称, 基金类型, 拼音缩写

        df = ak.fund_name_em()

        if not df.empty:

            # Rename columns for consistency

            # 基金代码 -> code, 基金简称 -> name, 基金类型 -> type, 拼音缩写 -> pinyin

            df = df.rename(columns={

                '基金代码': 'code',

                '基金简称': 'name',

                '基金类型': 'type',

                '拼音缩写': 'pinyin'

            })

            return df[['code', 'name', 'type', 'pinyin']].to_dict('records')

    except Exception as e:

        print(f"Error fetching all fund list: {e}")

    return []



def search_funds(query: str, limit: int = 10) -> List[Dict]:

    """

    Search funds by code or name (fuzzy matching)

    """

    query = query.strip().lower()

    if not query:

        return []



    all_funds = get_all_fund_list()

    results = []

    

    # Priority 1: Exact Code Match

    for fund in all_funds:

        if fund['code'] == query:

            results.append(fund)

    

    # Priority 2: Code Starts With

    for fund in all_funds:

        if fund['code'].startswith(query) and fund not in results:

            results.append(fund)

            

    # Priority 3: Name Contains

    for fund in all_funds:

        if query in fund['name'].lower() and fund not in results:

            results.append(fund)

            

    # Priority 4: Pinyin Contains

    for fund in all_funds:

        if 'pinyin' in fund and query in str(fund['pinyin']).lower() and fund not in results:

            results.append(fund)

            

    return results[:limit]
