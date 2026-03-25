# -*- coding: utf-8 -*-
"""股票数据工具 - 提供给Agent调用的数据获取函数

使用 akshare 库实现股票数据获取功能，包括实时行情、K线数据、
趋势分析、新闻资讯、基本信息、财务数据和公司公告等。
"""
import akshare as ak
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

from app.services.ai.tool_registry import ToolRegistry, tool, ToolParameter


def register_stock_tools(registry: ToolRegistry):
    """注册股票数据工具到指定的注册中心

    Args:
        registry: 工具注册中心实例
    """

    @tool(
        name="get_realtime_quote",
        description="获取股票实时行情数据，包括最新价、涨跌幅、成交量等",
        parameters=[
            ToolParameter(name="stock_code", type="string", description="股票代码，如 000001"),
        ],
        registry=registry,
    )
    def get_realtime_quote(stock_code: str) -> Dict[str, Any]:
        """获取股票实时行情数据

        Args:
            stock_code: 股票代码，如 000001

        Returns:
            包含实时行情数据的字典，包括价格、涨跌幅、成交量等信息
        """
        try:
            df = ak.stock_zh_a_spot_em()
            row = df[df['代码'] == stock_code]
            if row.empty:
                return {"error": f"股票 {stock_code} 未找到"}
            data = row.iloc[0].to_dict()
            return {
                "code": data.get("代码"),
                "name": data.get("名称"),
                "price": float(data.get("最新价", 0) or 0),
                "change_percent": float(data.get("涨跌幅", 0) or 0),
                "change": float(data.get("涨跌额", 0) or 0),
                "volume": float(data.get("成交量", 0) or 0),
                "amount": float(data.get("成交额", 0) or 0),
                "high": float(data.get("最高", 0) or 0),
                "low": float(data.get("最低", 0) or 0),
                "open": float(data.get("今开", 0) or 0),
                "pre_close": float(data.get("昨收", 0) or 0),
                "volume_ratio": float(data.get("量比", 0) or 0),
                "turnover_rate": float(data.get("换手率", 0) or 0),
                "pe_ratio": float(data.get("市盈率-动态", 0) or 0),
                "pb_ratio": float(data.get("市净率", 0) or 0),
                "total_market_value": float(data.get("总市值", 0) or 0),
                "circulating_market_value": float(data.get("流通市值", 0) or 0),
            }
        except Exception as e:
            return {"error": str(e)}

    @tool(
        name="get_daily_kline",
        description="获取股票日K线历史数据，用于技术分析",
        parameters=[
            ToolParameter(name="stock_code", type="string", description="股票代码，如 000001"),
            ToolParameter(name="days", type="integer", description="获取天数", default=60, required=False),
            ToolParameter(name="adjust", type="string", description="复权类型：qfq-前复权, hfq-后复权, 空-不复权", default="qfq", required=False),
        ],
        registry=registry,
    )
    def get_daily_kline(stock_code: str, days: int = 60, adjust: str = "qfq") -> List[Dict[str, Any]]:
        """获取股票日K线历史数据

        Args:
            stock_code: 股票代码
            days: 获取天数，默认60天
            adjust: 复权类型，qfq-前复权，hfq-后复权，空-不复权

        Returns:
            K线数据列表，每个元素包含日期、开盘价、收盘价、最高价、最低价、成交量等
        """
        try:
            df = ak.stock_zh_a_hist(symbol=stock_code, period="daily", adjust=adjust)
            if df.empty:
                return []
            df = df.tail(days)
            records = df.to_dict("records")

            # 标准化字段名
            result = []
            for record in records:
                result.append({
                    "date": str(record.get("日期", "")),
                    "open": float(record.get("开盘", 0) or 0),
                    "close": float(record.get("收盘", 0) or 0),
                    "high": float(record.get("最高", 0) or 0),
                    "low": float(record.get("最低", 0) or 0),
                    "volume": float(record.get("成交量", 0) or 0),
                    "amount": float(record.get("成交额", 0) or 0),
                    "amplitude": float(record.get("振幅", 0) or 0),
                    "change_percent": float(record.get("涨跌幅", 0) or 0),
                    "change": float(record.get("涨跌额", 0) or 0),
                    "turnover": float(record.get("换手率", 0) or 0),
                })
            return result
        except Exception as e:
            return [{"error": str(e)}]

    @tool(
        name="analyze_trend",
        description="分析股票趋势，计算均线并判断多空方向",
        parameters=[
            ToolParameter(name="stock_code", type="string", description="股票代码，如 000001"),
        ],
        registry=registry,
        category="analysis",
    )
    def analyze_trend(stock_code: str) -> Dict[str, Any]:
        """分析股票趋势

        通过计算移动平均线（MA5、MA10、MA20）来判断股票的多空方向。

        Args:
            stock_code: 股票代码

        Returns:
            包含趋势分析结果的字典，包括趋势方向、均线值等信息
        """
        try:
            # 获取K线数据
            kline = get_daily_kline(stock_code, 30)
            if not kline or "error" in kline[0]:
                return {"error": "无法获取K线数据"}

            # 提取收盘价
            closes = [k.get("close", 0) for k in kline[-20:] if k.get("close")]
            if len(closes) < 20:
                return {"error": "数据不足，无法分析趋势"}

            # 计算均线
            ma5 = sum(closes[-5:]) / 5
            ma10 = sum(closes[-10:]) / 10
            ma20 = sum(closes[-20:]) / 20

            # 计算价格相对位置
            latest_close = closes[-1]
            price_position = "above_ma20" if latest_close > ma20 else "below_ma20"

            # 判断趋势
            if ma5 > ma10 > ma20:
                trend = "up"
                trend_desc = "多头排列，上涨趋势"
            elif ma5 < ma10 < ma20:
                trend = "down"
                trend_desc = "空头排列，下跌趋势"
            else:
                trend = "sideways"
                trend_desc = "震荡整理"

            # 计算均线发散程度
            ma_spread = abs(ma5 - ma20) / ma20 * 100 if ma20 > 0 else 0

            # 判断均线交叉信号
            cross_signal = "none"
            if len(closes) >= 10:
                prev_ma5 = sum(closes[-6:-1]) / 5
                prev_ma10 = sum(closes[-11:-1]) / 10
                if prev_ma5 <= prev_ma10 and ma5 > ma10:
                    cross_signal = "golden_cross"
                elif prev_ma5 >= prev_ma10 and ma5 < ma10:
                    cross_signal = "death_cross"

            return {
                "stock_code": stock_code,
                "trend": trend,
                "trend_desc": trend_desc,
                "ma5": round(ma5, 2),
                "ma10": round(ma10, 2),
                "ma20": round(ma20, 2),
                "latest_close": round(latest_close, 2),
                "price_position": price_position,
                "ma_spread": round(ma_spread, 2),
                "cross_signal": cross_signal,
                "analysis_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        except Exception as e:
            return {"error": str(e)}

    @tool(
        name="get_stock_news",
        description="获取股票相关新闻资讯",
        parameters=[
            ToolParameter(name="stock_code", type="string", description="股票代码，如 000001"),
            ToolParameter(name="limit", type="integer", description="返回新闻数量", default=10, required=False),
        ],
        registry=registry,
        category="search",
    )
    def get_stock_news(stock_code: str, limit: int = 10) -> List[Dict[str, Any]]:
        """获取股票相关新闻资讯

        Args:
            stock_code: 股票代码
            limit: 返回新闻数量，默认10条

        Returns:
            新闻列表，每个元素包含标题、发布时间、来源等信息
        """
        try:
            df = ak.stock_news_em(symbol=stock_code)
            if df.empty:
                return []

            records = df.head(limit).to_dict("records")
            result = []
            for record in records:
                result.append({
                    "title": record.get("新闻标题", ""),
                    "content": record.get("新闻内容", "")[:200] + "..." if record.get("新闻内容") else "",
                    "publish_time": str(record.get("发布时间", "")),
                    "source": record.get("文章来源", ""),
                    "url": record.get("新闻链接", ""),
                })
            return result
        except Exception as e:
            return [{"error": str(e)}]

    @tool(
        name="get_stock_info",
        description="获取股票基本信息，包括公司名称、行业、上市日期等",
        parameters=[
            ToolParameter(name="stock_code", type="string", description="股票代码，如 000001"),
        ],
        registry=registry,
    )
    def get_stock_info(stock_code: str) -> Dict[str, Any]:
        """获取股票基本信息

        Args:
            stock_code: 股票代码

        Returns:
            包含股票基本信息的字典
        """
        try:
            # 获取A股股票信息
            df = ak.stock_info_a_code_name()
            row = df[df['code'] == stock_code]
            if row.empty:
                return {"error": f"股票 {stock_code} 未找到"}

            stock_name = row.iloc[0]['name']

            # 尝试获取更详细的信息
            try:
                # 获取个股信息
                info_df = ak.stock_individual_info_em(symbol=stock_code)
                if not info_df.empty:
                    info_dict = dict(zip(info_df['item'], info_df['value']))
                    return {
                        "code": stock_code,
                        "name": stock_name,
                        "industry": info_dict.get("行业", ""),
                        "list_date": info_dict.get("上市时间", ""),
                        "total_share": info_dict.get("总市值", ""),
                        "circulating_share": info_dict.get("流通市值", ""),
                        "company_name": info_dict.get("公司名称", stock_name),
                        "main_business": info_dict.get("主营业务", ""),
                    }
            except Exception:
                pass

            return {
                "code": stock_code,
                "name": stock_name,
                "industry": "",
                "list_date": "",
                "total_share": "",
                "circulating_share": "",
                "company_name": stock_name,
                "main_business": "",
            }
        except Exception as e:
            return {"error": str(e)}

    @tool(
        name="get_financial_data",
        description="获取股票财务数据，包括营收、利润、资产负债等",
        parameters=[
            ToolParameter(name="stock_code", type="string", description="股票代码，如 000001"),
            ToolParameter(name="report_type", type="string", description="报表类型：balance-资产负债表, income-利润表, cashflow-现金流量表", default="income", required=False),
        ],
        registry=registry,
    )
    def get_financial_data(stock_code: str, report_type: str = "income") -> Dict[str, Any]:
        """获取股票财务数据

        Args:
            stock_code: 股票代码
            report_type: 报表类型，balance-资产负债表, income-利润表, cashflow-现金流量表

        Returns:
            包含财务数据的字典
        """
        try:
            result = {
                "stock_code": stock_code,
                "report_type": report_type,
                "data": [],
            }

            if report_type == "balance":
                # 资产负债表
                try:
                    df = ak.stock_balance_sheet_by_report_em(symbol=stock_code)
                    if not df.empty:
                        result["data"] = df.tail(4).to_dict("records")
                except Exception:
                    result["error"] = "暂无资产负债表数据"

            elif report_type == "income":
                # 利润表
                try:
                    df = ak.stock_profit_sheet_by_report_em(symbol=stock_code)
                    if not df.empty:
                        result["data"] = df.tail(4).to_dict("records")
                except Exception:
                    result["error"] = "暂无利润表数据"

            elif report_type == "cashflow":
                # 现金流量表
                try:
                    df = ak.stock_cash_flow_sheet_by_report_em(symbol=stock_code)
                    if not df.empty:
                        result["data"] = df.tail(4).to_dict("records")
                except Exception:
                    result["error"] = "暂无现金流量表数据"

            else:
                result["error"] = f"不支持的报表类型: {report_type}"

            return result
        except Exception as e:
            return {"error": str(e)}

    @tool(
        name="get_announcements",
        description="获取公司公告信息",
        parameters=[
            ToolParameter(name="stock_code", type="string", description="股票代码，如 000001"),
            ToolParameter(name="limit", type="integer", description="返回公告数量", default=10, required=False),
        ],
        registry=registry,
        category="search",
    )
    def get_announcements(stock_code: str, limit: int = 10) -> List[Dict[str, Any]]:
        """获取公司公告信息

        Args:
            stock_code: 股票代码
            limit: 返回公告数量，默认10条

        Returns:
            公告列表，每个元素包含公告标题、发布时间、公告类型等信息
        """
        try:
            # 尝试获取公司公告
            try:
                df = ak.stock_notice_report(symbol=stock_code)
                if not df.empty:
                    records = df.head(limit).to_dict("records")
                    result = []
                    for record in records:
                        result.append({
                            "title": record.get("公告标题", record.get("title", "")),
                            "publish_time": str(record.get("公告日期", record.get("publish_time", ""))),
                            "type": record.get("公告类型", record.get("type", "")),
                            "url": record.get("公告链接", record.get("url", "")),
                        })
                    return result
            except Exception:
                pass

            # 备用方案：尝试其他公告接口
            try:
                df = ak.stock_yjyg_em(symbol=stock_code)
                if not df.empty:
                    records = df.head(limit).to_dict("records")
                    result = []
                    for record in records:
                        result.append({
                            "title": record.get("公告标题", str(record.get("股票代码", "")) + " 公告"),
                            "publish_time": str(record.get("公告日期", "")),
                            "type": "公告",
                            "url": "",
                        })
                    return result
            except Exception:
                pass

            return [{"error": "暂无公告数据"}]
        except Exception as e:
            return [{"error": str(e)}]


# 创建默认注册的便捷函数
def register_default_stock_tools():
    """注册股票工具到默认注册中心"""
    from app.services.ai.tool_registry import get_default_registry
    register_stock_tools(get_default_registry())