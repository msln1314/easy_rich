# -*- coding: utf-8 -*-
# @version        : 1.1
# @Create Time    : 2026/3/10
# @File           : index_service.py
# @IDE            : PyCharm
# @desc           : 指数行情服务 - 支持 AKShare、腾讯财经、新浪、掘金量化、pytdx 多数据源

import akshare as ak
import pandas as pd
import requests
from datetime import datetime
from typing import List, Optional, Dict, Any
from app.models.index_models import IndexQuote
from app.core.logging import get_logger
from app.utils.cache import cache_result
from app.services.pytdx_source import pytdx_source
from app.services.tencent_source import tencent_source  # 腾讯财经 - 成功率高

logger = get_logger(__name__)

# 主要指数代码映射
MAIN_INDICES = {
    "000001.SH": {"name": "上证指数", "ak_code": "sh000001", "gm_code": "SHSE.000001"},
    "399001.SZ": {"name": "深证成指", "ak_code": "sz399001", "gm_code": "SZSE.399001"},
    "399006.SZ": {"name": "创业板指", "ak_code": "sz399006", "gm_code": "SZSE.399006"},
    "000688.SH": {"name": "科创50", "ak_code": "sh000688", "gm_code": "SHSE.000688"},
}


class IndexService:
    """指数行情服务 - 多数据源支持"""

    def __init__(self):
        """初始化服务，延迟加载 GM 服务"""
        self._gm_service = None

    @property
    def gm_service(self):
        """延迟加载 GM 服务"""
        if self._gm_service is None:
            try:
                from app.services.gm_service import gm_service

                self._gm_service = gm_service
            except ImportError:
                logger.warning("GM 服务不可用")
                self._gm_service = None
        return self._gm_service

    @cache_result(expire=30)  # 缓存30秒
    async def get_index_quotes(
        self, symbol: str = "沪深重要指数"
    ) -> tuple[List[IndexQuote], str]:
        """
        获取指数实时行情数据

        Args:
            symbol: 指数类型

        Returns:
            tuple[List[IndexQuote], str]: (指数实时行情数据列表, 数据源)
        """
        logger.info(f"获取指数实时行情: {symbol}")

        # 数据源优先级：AKShare > 腾讯财经 > 新浪 > GM > pytdx
        # 1. 尝试 AKShare 东方财富
        result, source = await self._try_akshare_em()
        if result:
            logger.info(f"当前数据源: AKShare 东方财富")
            return result, source

        # 2. 尝试腾讯财经（成功率高）
        result, source = await self._try_tencent()
        if result:
            logger.info(f"当前数据源: 腾讯财经")
            return result, source

        # 3. 尝试新浪接口
        result, source = await self._try_sina()
        if result:
            logger.info(f"当前数据源: 新浪财经")
            return result, source

        # 4. 尝试掘金量化
        result, source = await self._try_gm()
        if result:
            logger.info(f"当前数据源: 掘金量化")
            return result, source

        # 5. 尝试 pytdx
        result, source = await self._try_pytdx()
        if result:
            logger.info(f"当前数据源: pytdx")
            return result, source

        logger.warning("所有数据源均无法获取指数行情")
        return [], ""

    async def _try_akshare_em(self) -> tuple[Optional[List[IndexQuote]], str]:
        """尝试使用 AKShare 东方财富接口"""
        try:
            df = ak.stock_zh_index_spot_em(symbol="沪深重要指数")

            if df.empty:
                return None, ""

            result = []
            main_codes = ["000001", "399001", "399006", "000688"]
            df_main = df[df["代码"].isin(main_codes)]

            for _, row in df_main.iterrows():
                try:
                    code = str(row.get("代码", ""))
                    # 转换代码格式
                    if code in ["000001", "000688"]:
                        std_code = f"{code}.SH"
                    else:
                        std_code = f"{code}.SZ"

                    quote = IndexQuote(
                        code=std_code,
                        name=str(row.get("名称", "")),
                        price=self._safe_float(row.get("最新价")),
                        change=self._safe_float(row.get("涨跌额")),
                        change_percent=self._safe_float(row.get("涨跌幅")),
                        volume=self._safe_float(row.get("成交量")),
                        amount=self._safe_float(row.get("成交额")),
                        amplitude=self._safe_float(row.get("振幅")),
                        high=self._safe_float(row.get("最高")),
                        low=self._safe_float(row.get("最低")),
                        open=self._safe_float(row.get("今开")),
                        pre_close=self._safe_float(row.get("昨收")),
                        volume_ratio=self._safe_float(row.get("量比")),
                        update_time=datetime.now(),
                    )
                    result.append(quote)
                except Exception as e:
                    logger.warning(f"解析指数数据失败: {e}")
                    continue

            logger.info(f"AKShare EM 接口获取到 {len(result)} 条指数数据")
            return result, "akshare_em"

        except Exception as e:
            logger.warning(f"AKShare EM 接口失败: {e}")
            return None, ""

    async def _try_tencent(self) -> tuple[Optional[List[IndexQuote]], str]:
        """尝试使用腾讯财经接口获取主要指数"""
        try:
            result = []
            index_codes = ["000001", "399001", "399006", "000688"]

            for code in index_codes:
                try:
                    quote = await tencent_source.get_index_quote(code)
                    if quote:
                        if code in ["000001", "000688"]:
                            std_code = f"{code}.SH"
                        else:
                            std_code = f"{code}.SZ"

                        index_quote = IndexQuote(
                            code=std_code,
                            name=quote.stock_name,
                            price=quote.price,
                            change=quote.change,
                            change_percent=quote.change_percent,
                            volume=quote.volume,
                            amount=quote.amount,
                            high=quote.high,
                            low=quote.low,
                            open=quote.open,
                            pre_close=quote.pre_close,
                            update_time=datetime.now(),
                        )
                        result.append(index_quote)
                except Exception as e:
                    logger.warning(f"腾讯财经获取指数 {code} 失败: {e}")
                    continue

            if result:
                logger.info(f"腾讯财经接口获取到 {len(result)} 条指数数据")
                return result, "tencent"

            return None, ""

        except Exception as e:
            logger.warning(f"腾讯财经接口失败: {e}")
            return None, ""

    async def _try_sina(self) -> tuple[Optional[List[IndexQuote]], str]:
        """尝试使用新浪接口获取主要指数"""
        try:
            # 新浪指数接口
            url = "http://hq.sinajs.cn/list=sh000001,sz399001,sz399006,sh000688"
            headers = {
                "Referer": "http://finance.sina.com.cn",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            }

            response = requests.get(url, headers=headers, timeout=10)
            response.encoding = "gbk"

            if response.status_code != 200:
                return None, ""

            result = []
            for line in response.text.strip().split("\n"):
                if not line or "hq_str_" not in line:
                    continue

                try:
                    # 解析格式: var hq_str_sh000001="上证指数,3391.88,..."
                    code_part, data_part = line.split('="')
                    code = code_part.replace("var hq_str_", "").upper()
                    data = data_part.rstrip('";').split(",")

                    if len(data) < 10:
                        continue

                    name = data[0]
                    open_price = float(data[1]) if data[1] else None
                    pre_close = float(data[2]) if data[2] else None
                    price = float(data[3]) if data[3] else None
                    high = float(data[4]) if data[4] else None
                    low = float(data[5]) if data[5] else None
                    volume = float(data[8]) if data[8] else None
                    amount = float(data[9]) if data[9] else None

                    change = (
                        round(price - pre_close, 2) if price and pre_close else None
                    )
                    change_percent = (
                        round((price - pre_close) / pre_close * 100, 2)
                        if price and pre_close
                        else None
                    )

                    # 转换代码格式
                    if code.startswith("SH"):
                        std_code = code.replace("SH", "") + ".SH"
                    else:
                        std_code = code.replace("SZ", "") + ".SZ"

                    quote = IndexQuote(
                        code=std_code,
                        name=name,
                        price=price,
                        change=change,
                        change_percent=change_percent,
                        volume=volume,
                        amount=amount,
                        high=high,
                        low=low,
                        open=open_price,
                        pre_close=pre_close,
                        update_time=datetime.now(),
                    )
                    result.append(quote)

                except Exception as e:
                    logger.warning(f"解析新浪指数数据失败: {e}")
                    continue

            logger.info(f"新浪接口获取到 {len(result)} 条指数数据")
            return result, "sina"

        except Exception as e:
            logger.warning(f"新浪接口失败: {e}")
            return None, ""

    async def _try_gm(self) -> tuple[Optional[List[IndexQuote]], str]:
        """尝试使用掘金量化接口获取指数行情"""
        try:
            gm = self.gm_service
            if not gm or not gm.is_available():
                logger.debug("GM 服务不可用，跳过")
                return None, ""

            # 获取主要指数的 GM 代码列表
            gm_codes = [v["gm_code"] for v in MAIN_INDICES.values()]

            # 使用 GM 的 current 方法获取实时行情
            quotes = gm.gm.current(symbols=gm_codes)

            if not quotes:
                return None, ""

            result = []
            for quote in quotes:
                try:
                    # GM 代码转换回标准格式
                    gm_symbol = quote.get("symbol", "")
                    std_code = self._gm_to_std_code(gm_symbol)

                    if not std_code:
                        continue

                    price = float(quote.get("last", 0) or 0)
                    pre_close = float(quote.get("pre_close", 0) or 0)

                    index_quote = IndexQuote(
                        code=std_code,
                        name=MAIN_INDICES.get(std_code, {}).get(
                            "name", quote.get("sec_name", "")
                        ),
                        price=price,
                        change=round(price - pre_close, 2)
                        if price and pre_close
                        else None,
                        change_percent=round((price - pre_close) / pre_close * 100, 2)
                        if pre_close
                        else None,
                        volume=float(quote.get("volume", 0) or 0),
                        amount=float(quote.get("amount", 0) or 0),
                        high=float(quote.get("high", 0) or 0),
                        low=float(quote.get("low", 0) or 0),
                        open=float(quote.get("open", 0) or 0),
                        pre_close=pre_close,
                        update_time=datetime.now(),
                    )
                    result.append(index_quote)

                except Exception as e:
                    logger.warning(f"解析 GM 指数数据失败: {e}")
                    continue

            logger.info(f"GM 接口获取到 {len(result)} 条指数数据")
            return result, "gm"

        except Exception as e:
            logger.warning(f"GM 接口失败: {e}")
            return None, ""

    async def _try_pytdx(self) -> tuple[Optional[List[IndexQuote]], str]:
        """尝试使用 pytdx 接口获取指数行情"""
        try:
            pytdx_quotes = await pytdx_source.get_index_quotes()
            if not pytdx_quotes:
                return None, ""

            result = []
            for q in pytdx_quotes:
                code = q.get("code", "")
                # 转换代码格式
                if code.startswith("6"):
                    std_code = f"{code}.SH"
                else:
                    std_code = f"{code}.SZ"

                index_quote = IndexQuote(
                    code=std_code,
                    name=q.get("name", ""),
                    price=q.get("price"),
                    change=q.get("change"),
                    change_percent=q.get("change_percent"),
                    volume=q.get("volume"),
                    amount=q.get("amount"),
                    update_time=datetime.now(),
                )
                result.append(index_quote)

            logger.info(f"pytdx 接口获取到 {len(result)} 条指数数据")
            return result, "pytdx"

        except Exception as e:
            logger.warning(f"pytdx 接口失败: {e}")
            return None, ""

    def _gm_to_std_code(self, gm_code: str) -> Optional[str]:
        """将 GM 代码转换为标准代码格式"""
        # GM 格式: SHSE.000001 -> 000001.SH
        for std_code, info in MAIN_INDICES.items():
            if info.get("gm_code") == gm_code:
                return std_code
        return None

    def _safe_float(self, value) -> Optional[float]:
        """安全转换为浮点数"""
        if value is None or pd.isna(value):
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None

    async def get_index_quote(
        self, index_code: str
    ) -> tuple[Optional[IndexQuote], str]:
        """
        获取单个指数的实时行情数据

        Args:
            index_code: 指数代码

        Returns:
            tuple[Optional[IndexQuote], str]: (指数实时行情数据, 数据源)
        """
        logger.info(f"获取单个指数实时行情: {index_code}")

        # 获取所有指数
        all_indices, source = await self.get_index_quotes()

        # 查找匹配的指数
        for index in all_indices:
            if index.code == index_code or index.code.replace(
                ".", ""
            ) == index_code.replace(".", ""):
                return index, source

        logger.warning(f"未找到指数代码 {index_code} 的实时行情数据")
        return None, ""

    async def get_index_history(
        self, index_code: str, start_date: str, end_date: str
    ) -> tuple[List[dict], str]:
        """
        获取指数历史数据

        Args:
            index_code: 指数代码 (如 sh000001 或 000001.SH)
            start_date: 开始日期 YYYYMMDD
            end_date: 结束日期 YYYYMMDD

        Returns:
            tuple[List[dict], str]: (历史数据列表, 数据源)
        """
        logger.info(f"获取指数历史数据: {index_code}, {start_date} - {end_date}")

        # 尝试 AKShare
        result = await self._try_akshare_history(index_code, start_date, end_date)
        if result:
            return result, "akshare"

        # 尝试 GM
        result = await self._try_gm_history(index_code, start_date, end_date)
        if result:
            return result, "gm"

        return [], ""

    async def _try_akshare_history(
        self, index_code: str, start_date: str, end_date: str
    ) -> Optional[List[dict]]:
        """尝试使用 AKShare 获取历史数据"""
        try:
            # 转换代码格式
            ak_code = index_code
            if index_code.endswith(".SH"):
                ak_code = f"sh{index_code.replace('.SH', '')}"
            elif index_code.endswith(".SZ"):
                ak_code = f"sz{index_code.replace('.SZ', '')}"

            df = ak.stock_zh_index_daily(symbol=ak_code)

            if df.empty:
                return None

            # 过滤日期范围
            df["date"] = pd.to_datetime(df["date"])
            start_dt = pd.to_datetime(start_date)
            end_dt = pd.to_datetime(end_date)

            df = df[(df["date"] >= start_dt) & (df["date"] <= end_dt)]

            result = []
            for _, row in df.iterrows():
                result.append(
                    {
                        "date": row["date"].strftime("%Y-%m-%d"),
                        "open": self._safe_float(row.get("open")),
                        "high": self._safe_float(row.get("high")),
                        "low": self._safe_float(row.get("low")),
                        "close": self._safe_float(row.get("close")),
                        "volume": self._safe_float(row.get("volume")),
                    }
                )

            logger.info(f"AKShare 获取到 {len(result)} 条历史数据")
            return result

        except Exception as e:
            logger.warning(f"AKShare 历史数据接口失败: {e}")
            return None

    async def _try_gm_history(
        self, index_code: str, start_date: str, end_date: str
    ) -> Optional[List[dict]]:
        """尝试使用 GM 获取历史数据"""
        try:
            gm = self.gm_service
            if not gm or not gm.is_available():
                return None

            # 转换代码格式
            gm_code = self._std_to_gm_code(index_code)
            if not gm_code:
                return None

            # 格式化日期
            start_time = f"{start_date} 09:30:00"
            end_time = f"{end_date} 15:00:00"

            # 使用 GM 的 history 方法
            history_data = gm.gm.history(
                symbol=gm_code,
                frequency="1d",
                start_time=start_time,
                end_time=end_time,
                adjust=0,  # 不复权
            )

            if not history_data:
                return None

            result = []
            for item in history_data:
                result.append(
                    {
                        "date": item.get("eob", "").strftime("%Y-%m-%d")
                        if hasattr(item.get("eob"), "strftime")
                        else str(item.get("eob", ""))[:10],
                        "open": self._safe_float(item.get("open")),
                        "high": self._safe_float(item.get("high")),
                        "low": self._safe_float(item.get("low")),
                        "close": self._safe_float(item.get("close")),
                        "volume": self._safe_float(item.get("volume")),
                    }
                )

            logger.info(f"GM 获取到 {len(result)} 条历史数据")
            return result

        except Exception as e:
            logger.warning(f"GM 历史数据接口失败: {e}")
            return None

    def _std_to_gm_code(self, std_code: str) -> Optional[str]:
        """将标准代码转换为 GM 代码格式"""
        # 标准格式: 000001.SH -> SHSE.000001
        for code, info in MAIN_INDICES.items():
            if code == std_code:
                return info.get("gm_code")
        return None

    @cache_result(expire=60)
    async def get_global_indices(self) -> List[Dict[str, Any]]:
        """获取全球主要指数行情"""
        logger.info("获取全球主要指数行情")

        result = []

        # 定义需要获取的指数
        indices_config = [
            {"symbol": "道琼斯", "name": "道琼斯", "region": "美股"},
            {"symbol": "纳斯达克", "name": "纳斯达克", "region": "美股"},
            {"symbol": "标普500", "name": "标普500", "region": "美股"},
            {"symbol": "日经225", "name": "日经225", "region": "亚太"},
            {"symbol": "恒生指数", "name": "恒生指数", "region": "亚太"},
            {"symbol": "韩国KOSPI", "name": "韩国综指", "region": "亚太"},
            {"symbol": "英国富时100", "name": "英国富时", "region": "欧洲"},
            {"symbol": "德国DAX30", "name": "德国DAX", "region": "欧洲"},
            {"symbol": "法国CAC40", "name": "法国CAC", "region": "欧洲"},
        ]

        for idx_config in indices_config:
            try:
                df = ak.index_global_spot_em(symbol=idx_config["symbol"])
                if df is not None and not df.empty:
                    latest = df.iloc[-1]
                    cols = list(df.columns)
                    item = {
                        "index_code": idx_config["symbol"],
                        "index_name": idx_config["name"],
                        "region": idx_config["region"],
                        "price": self._safe_float(latest.iloc[1])
                        if len(cols) > 1
                        else None,
                        "change": self._safe_float(latest.iloc[2])
                        if len(cols) > 2
                        else None,
                        "change_percent": self._safe_float(latest.iloc[3])
                        if len(cols) > 3
                        else None,
                        "update_time": datetime.now().isoformat(),
                    }
                    result.append(item)
            except Exception as e:
                logger.warning(f"获取 {idx_config['name']} 失败: {e}")
                # 添加默认数据
                result.append(
                    {
                        "index_code": idx_config["symbol"],
                        "index_name": idx_config["name"],
                        "region": idx_config["region"],
                        "price": None,
                        "change": None,
                        "change_percent": None,
                        "update_time": datetime.now().isoformat(),
                    }
                )

        logger.info(f"获取到 {len(result)} 条全球指数数据")
        return result


index_service = IndexService()
