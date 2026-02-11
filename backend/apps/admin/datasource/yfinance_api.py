"""
YFinance API Wrapper for International Market Data
================================================
Provides access to global commodities, currencies, and macro indicators.
"""

import yfinance as yf
import pandas as pd
from typing import Dict, Optional

class YFinanceAPI:
    """
    Wrapper for yfinance to fetch international market data.
    """
    
    TICKERS = {
        'GOLD_FUTURES': 'GC=F',
        'SILVER_FUTURES': 'SI=F',
        'US_10Y_YIELD': '^TNX',
        'DOLLAR_INDEX': 'DX-Y.NYB',
        'GOLD_ETF': 'GLD',
        'SILVER_ETF': 'SLV',
        'SP500': '^GSPC'
    }

    @staticmethod
    def get_price_history(ticker: str, period: str = "1y") -> pd.DataFrame:
        """
        Fetch historical price data for a given ticker.
        """
        try:
            # Using yf.Ticker(ticker).history(...) is standard
            t = yf.Ticker(ticker)
            df = t.history(period=period)
            return df
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            return pd.DataFrame()

    @classmethod
    def get_gold_silver_ratio(cls, period: str = "1y") -> pd.DataFrame:
        """
        Calculate Gold/Silver ratio history.
        """
        gold = cls.get_price_history(cls.TICKERS['GOLD_FUTURES'], period)
        silver = cls.get_price_history(cls.TICKERS['SILVER_FUTURES'], period)
        
        if gold.empty or silver.empty:
            return pd.DataFrame()
            
        # Align dates
        df = pd.DataFrame()
        df['Gold'] = gold['Close']
        df['Silver'] = silver['Close']
        df.dropna(inplace=True)
        
        df['Ratio'] = df['Gold'] / df['Silver']
        return df

    @classmethod
    def get_macro_data(cls) -> Dict[str, float]:
        """
        Get current macro indicators: US 10Y Yield, DXY.
        """
        data = {}
        try:
            # Fetch multiple tickers at once for latest quote
            tickers = [cls.TICKERS['US_10Y_YIELD'], cls.TICKERS['DOLLAR_INDEX']]
            df = yf.download(tickers, period="1d", progress=False)['Close']
            
            if not df.empty:
                # Handle multi-index columns if necessary (newer yfinance versions)
                # If only one row, it might be a Series or DataFrame
                last_row = df.iloc[-1]
                data['US_10Y_YIELD'] = float(last_row.get(cls.TICKERS['US_10Y_YIELD'], 0))
                data['DOLLAR_INDEX'] = float(last_row.get(cls.TICKERS['DOLLAR_INDEX'], 0))
        except Exception as e:
            print(f"Error fetching macro data: {e}")
            
        return data

    @classmethod
    def get_latest_quote(cls, ticker_key: str) -> Optional[Dict]:
        """
        Get latest quote for a specific configured ticker.
        """
        symbol = cls.TICKERS.get(ticker_key)
        if not symbol:
            return None
            
        try:
            t = yf.Ticker(symbol)
            info = t.fast_info
            return {
                'symbol': symbol,
                'price': info.last_price,
                'previous_close': info.previous_close,
                'change_pct': ((info.last_price - info.previous_close) / info.previous_close) * 100
            }
        except Exception as e:
            print(f"Error fetching quote for {symbol}: {e}")
            return None
