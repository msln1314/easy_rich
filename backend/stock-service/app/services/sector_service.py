import math
from datetime import datetime
from typing import List, Optional
import pandas as pd

# 先导入 akshare-proxy-patch 来修复网络问题
# try:
#     import akshare_proxy_patch
#     # 安装补丁，参数：网关、AUTH_TOKEN、重试次数
#     # 增加重试次数到 60，提高稳定性
#     akshare_proxy_patch.install_patch("101.201.173.125", "", 60)
# except ImportError:
#     pass

import akshare as ak
from app.models.sector_models import (
    ConceptBoard,
    IndustryBoard,
    BoardSpot,
    ConceptBoardSpot,
    IndustryBoardSpot,
    ConceptBoardConstituent,
    IndustryBoardConstituent,
    LeaderStock,
    SectorLeader,
    SectorLeaderRanking,
    SectorRealtimeStatus,
    SectorRotationHistory,
    RotationPattern,
    RotationPrediction,
    SectorFactor,
)
from app.utils.akshare_wrapper import handle_akshare_exception, with_retry
from app.core.logging import get_logger
from app.utils.cache import cache_result
from app.services.gm_service import gm_service
from app.services.tushare_service import tushare_service

logger = get_logger(__name__)


# 添加一个辅助函数来处理特殊浮点值
def safe_float(value, default=None):
    """
    安全地将值转换为浮点数，处理NaN和Infinity

    Args:
        value: 要转换的值
        default: 如果转换失败或值为特殊值时返回的默认值

    Returns:
        float: 转换后的浮点数或默认值
    """
    if pd.isna(value):
        return default

    try:
        float_value = float(value)
        if math.isnan(float_value) or math.isinf(float_value):
            return default
        return float_value
    except (ValueError, TypeError):
        return default


class SectorService:
    """板块服务"""

    async def get_concept_boards(self) -> List[ConceptBoard]:
        """
        获取概念板块列表及实时行情
        降级策略：AKShare → Tushare

        Returns:
            List[ConceptBoard]: 概念板块列表
        """
        logger.info("获取概念板块列表（优先 AKShare，失败时降级到 Tushare）")

        # 尝试使用 AKShare 获取数据
        try:
            return await self._get_concept_boards_from_akshare()
        except Exception as e:
            logger.warning(f"AKShare 获取概念板块失败: {str(e)}")

            # 如果 Tushare 服务可用，使用 Tushare 获取
            if tushare_service.is_available():
                logger.info("降级使用 Tushare 获取概念板块")
                try:
                    return await tushare_service.get_concept_boards()
                except Exception as tushare_error:
                    logger.error(f"Tushare 获取概念板块也失败: {str(tushare_error)}")

            # 两个数据源都失败，抛出异常
            raise ValueError(f"无法获取概念板块数据，AKShare 失败: {str(e)}")

    @cache_result()
    @with_retry(max_retries=3, retry_delay=2.0)
    @handle_akshare_exception
    async def _get_concept_boards_from_akshare(self) -> List[ConceptBoard]:
        """
        从 AKShare 获取概念板块列表（内部方法）

        Returns:
            List[ConceptBoard]: 概念板块列表
        """
        logger.debug("使用 AKShare 获取概念板块数据")

        # 调用AKShare接口获取概念板块数据
        df = ak.stock_board_concept_name_em()

        if df.empty:
            logger.warning("未获取到概念板块数据")
            return []

        # 将DataFrame转换为ConceptBoard对象列表
        result = []
        for _, row in df.iterrows():
            # 使用safe_float函数处理所有浮点值
            market_value = int(row["总市值"]) if not pd.isna(row["总市值"]) else None

            board = ConceptBoard(
                rank=int(row["排名"]),
                name=row["板块名称"],
                code=row["板块代码"],
                price=safe_float(row["最新价"], 0),
                change=safe_float(row["涨跌额"], 0),
                change_percent=safe_float(row["涨跌幅"], 0),
                market_value=market_value,
                turnover_rate=safe_float(row["换手率"], 0),
                up_count=int(row["上涨家数"]),
                down_count=int(row["下跌家数"]),
                leading_stock=row["领涨股票"],
                leading_stock_change_percent=safe_float(row["领涨股票-涨跌幅"], 0),
                update_time=datetime.now(),
            )
            result.append(board)

        return result

    async def get_concept_board(
        self, board_code: str, name: Optional[str] = None
    ) -> Optional[ConceptBoard]:
        """
        获取单个概念板块信息

        Args:
            board_code: 板块代码，如"BK0715"
            name: 板块名称，如"可燃冰"，当提供名称时，会尝试通过名称查找板块代码

        Returns:
            Optional[ConceptBoard]: 概念板块信息，如果未找到则返回None
        """
        logger.info(f"获取单个概念板块 get_concept_board : {board_code}")

        # 如果提供了名称，尝试通过名称查找板块代码
        if name:
            logger.info(f"尝试通过名称查找板块代码: {name}")
            all_boards = await self._get_concept_boards_from_akshare()

            # 查找匹配的板块
            for board in all_boards:
                if board.name == name:
                    board_code = board.code
                    logger.info(f"找到板块代码: {board_code}")
                    break

        # 获取所有概念板块
        all_boards = await self._get_concept_boards_from_akshare()

        # 查找匹配的板块
        for board in all_boards:
            if board.code == board_code:
                return board

        logger.warning(f"未找到板块代码 {board_code} 的数据")
        return None

    @cache_result()
    @handle_akshare_exception
    async def get_concept_board_spot(
        self, board_name: str
    ) -> Optional[ConceptBoardSpot]:
        """
        获取概念板块实时行情详情

        Args:
            board_name: 板块名称，如"可燃冰"

        Returns:
            Optional[ConceptBoardSpot]: 概念板块实时行情详情，如果未找到则返回None
        """
        logger.info(f"获取概念板块实时行情详情: {board_name}")

        try:
            # 调用AKShare接口获取概念板块实时行情
            df = ak.stock_board_concept_spot_em(symbol=board_name)

            if df.empty:
                logger.warning(f"未找到板块名称 {board_name} 的实时行情数据")
                return None

            # 将DataFrame转换为字典
            data_dict = {}
            for _, row in df.iterrows():
                data_dict[row["item"]] = row["value"]

            # 创建ConceptBoardSpot对象，使用safe_float处理所有浮点值
            spot = ConceptBoardSpot(
                name=board_name,
                price=safe_float(data_dict.get("最新", 0), 0),
                high=safe_float(data_dict.get("最高", 0), 0),
                low=safe_float(data_dict.get("最低", 0), 0),
                open=safe_float(data_dict.get("开盘", 0), 0),
                volume=safe_float(data_dict.get("成交量", 0), 0),
                amount=safe_float(data_dict.get("成交额", 0), 0),
                turnover_rate=safe_float(data_dict.get("换手率", 0), 0),
                change=safe_float(data_dict.get("涨跌额", 0), 0),
                change_percent=safe_float(data_dict.get("涨跌幅", 0), 0),
                amplitude=safe_float(data_dict.get("振幅", 0), 0),
                update_time=datetime.now(),
            )

            return spot
        except Exception as e:
            logger.error(f"获取概念板块实时行情详情失败: {str(e)}")
            raise

    @cache_result()
    @handle_akshare_exception
    async def get_concept_board_spot_by_code(
        self, board_code: str
    ) -> Optional[ConceptBoardSpot]:
        """
        通过板块代码获取概念板块实时行情详情

        Args:
            board_code: 板块代码，如"BK0818"

        Returns:
            Optional[ConceptBoardSpot]: 概念板块实时行情详情，如果未找到则返回None
        """
        logger.info(f"通过代码获取概念板块实时行情详情: {board_code}")

        # 先获取板块名称
        board = await self.get_concept_board(board_code)
        if board is None:
            logger.warning(f"未找到板块代码 {board_code} 对应的板块")
            return None

        # 通过板块名称获取实时行情
        return await self.get_concept_board_spot(board.name)

    async def get_concept_board_constituents(
        self, symbol: str
    ) -> List[ConceptBoardConstituent]:
        """
        获取概念板块成份股

        Args:
            symbol: 板块名称或代码，如"融资融券"或"BK0655"

        Returns:
            List[ConceptBoardConstituent]: 概念板块成份股列表
        """
        logger.info(f"获取概念板块成份股: {symbol}")

        return await self._get_concept_board_constituents_from_akshare(symbol)

    @cache_result()
    @handle_akshare_exception
    async def _get_concept_board_constituents_from_akshare(
        self, symbol: str
    ) -> List[ConceptBoardConstituent]:
        """
        从 AKShare 获取概念板块成份股（内部方法）

        Args:
            symbol: 板块名称或代码

        Returns:
            List[ConceptBoardConstituent]: 概念板块成份股列表
        """
        logger.debug(f"使用 AKShare 获取概念板块成份股: {symbol}")

        try:
            # 调用AKShare接口获取概念板块成份股
            df = ak.stock_board_concept_cons_em(symbol=symbol)

            if df.empty:
                logger.warning(f"未获取到板块 {symbol} 的成份股数据")
                return []

            # 将DataFrame转换为ConceptBoardConstituent对象列表
            result = []
            for _, row in df.iterrows():
                # 使用safe_float函数处理所有浮点值
                constituent = ConceptBoardConstituent(
                    rank=int(row["序号"]),
                    code=row["代码"],
                    name=row["名称"],
                    price=safe_float(row["最新价"], 0),
                    change_percent=safe_float(row["涨跌幅"], 0),
                    change=safe_float(row["涨跌额"], 0),
                    volume=safe_float(row["成交量"], 0),
                    amount=safe_float(row["成交额"], 0),
                    amplitude=safe_float(row["振幅"], 0),
                    high=safe_float(row["最高"], 0),
                    low=safe_float(row["最低"], 0),
                    open=safe_float(row["今开"], 0),
                    pre_close=safe_float(row["昨收"], 0),
                    turnover_rate=safe_float(row["换手率"], 0),
                    pe_ratio=safe_float(row["市盈率-动态"]),
                    pb_ratio=safe_float(row["市净率"]),
                    update_time=datetime.now(),
                )
                result.append(constituent)

            return result
        except Exception as e:
            logger.error(f"获取概念板块成份股失败: {str(e)}")
            # 重要：这里需要抛出异常，而不是返回None
            raise ValueError(f"获取概念板块成份股失败: {str(e)}")

    async def get_industry_boards(self) -> List[IndustryBoard]:
        """
        获取行业板块列表及实时行情
        降级策略：AKShare → Tushare

        Returns:
            List[IndustryBoard]: 行业板块列表
        """
        logger.info("获取行业板块列表（优先 AKShare，失败时降级到 Tushare）")

        # 尝试使用 AKShare 获取数据
        try:
            return await self._get_industry_boards_from_akshare()
        except Exception as e:
            logger.warning(f"AKShare 获取行业板块失败: {str(e)}")

            # 如果 Tushare 服务可用，使用 Tushare 获取
            if tushare_service.is_available():
                logger.info("降级使用 Tushare 获取行业板块")
                try:
                    return await tushare_service.get_industry_boards()
                except Exception as tushare_error:
                    logger.error(f"Tushare 获取行业板块也失败: {str(tushare_error)}")

            # 两个数据源都失败，抛出异常
            raise ValueError(f"无法获取行业板块数据，AKShare 失败: {str(e)}")

    @cache_result()
    @with_retry(max_retries=3, retry_delay=2.0)
    @handle_akshare_exception
    async def _get_industry_boards_from_akshare(self) -> List[IndustryBoard]:
        """
        从 AKShare 获取行业板块列表（内部方法）

        Returns:
            List[IndustryBoard]: 行业板块列表
        """
        logger.debug("使用 AKShare 获取行业板块数据")

        # 调用AKShare接口获取行业板块数据
        df = ak.stock_board_industry_name_em()

        if df.empty:
            logger.warning("未获取到行业板块数据")
            return []

        # 将DataFrame转换为IndustryBoard对象列表
        result = []
        for _, row in df.iterrows():
            # 使用safe_float函数处理所有浮点值
            market_value = int(row["总市值"]) if not pd.isna(row["总市值"]) else None

            board = IndustryBoard(
                rank=int(row["排名"]),
                name=row["板块名称"],
                code=row["板块代码"],
                price=safe_float(row["最新价"], 0),
                change=safe_float(row["涨跌额"], 0),
                change_percent=safe_float(row["涨跌幅"], 0),
                market_value=market_value,
                turnover_rate=safe_float(row["换手率"], 0),
                up_count=int(row["上涨家数"]),
                down_count=int(row["下跌家数"]),
                leading_stock=row["领涨股票"],
                leading_stock_change_percent=safe_float(row["领涨股票-涨跌幅"], 0),
                update_time=datetime.now(),
            )
            result.append(board)

        return result

    @cache_result()
    @handle_akshare_exception
    async def get_industry_board(self, board_code: str) -> Optional[IndustryBoard]:
        """
        获取单个行业板块的实时行情

        Args:
            board_code: 板块代码，如"BK0437"

        Returns:
            Optional[IndustryBoard]: 行业板块数据，如果未找到则返回None
        """
        logger.info(f"获取单个行业板块: {board_code}")

        # 获取所有行业板块
        all_boards = await self.get_industry_boards()

        # 查找匹配的板块
        for board in all_boards:
            if board.code == board_code:
                return board

        logger.warning(f"未找到板块代码 {board_code} 的数据")
        return None

    @cache_result()
    @handle_akshare_exception
    async def get_industry_board_spot(
        self, board_name: str
    ) -> Optional[IndustryBoardSpot]:
        """
        获取行业板块实时行情详情

        Args:
            board_name: 板块名称，如"小金属"

        Returns:
            Optional[IndustryBoardSpot]: 行业板块实时行情详情，如果未找到则返回None
        """
        logger.info(f"获取行业板块实时行情详情: {board_name}")

        try:
            # 调用AKShare接口获取行业板块实时行情
            df = ak.stock_board_industry_spot_em(symbol=board_name)

            if df.empty:
                logger.warning(f"未找到板块名称 {board_name} 的实时行情数据")
                return None

            # 将DataFrame转换为字典
            data_dict = {}
            for _, row in df.iterrows():
                data_dict[row["item"]] = row["value"]

            # 创建IndustryBoardSpot对象，使用safe_float处理所有浮点值
            spot = IndustryBoardSpot(
                name=board_name,
                price=safe_float(data_dict.get("最新", 0), 0),
                high=safe_float(data_dict.get("最高", 0), 0),
                low=safe_float(data_dict.get("最低", 0), 0),
                open=safe_float(data_dict.get("开盘", 0), 0),
                volume=safe_float(data_dict.get("成交量", 0), 0),
                amount=safe_float(data_dict.get("成交额", 0), 0),
                turnover_rate=safe_float(data_dict.get("换手率", 0), 0),
                change=safe_float(data_dict.get("涨跌额", 0), 0),
                change_percent=safe_float(data_dict.get("涨跌幅", 0), 0),
                amplitude=safe_float(data_dict.get("振幅", 0), 0),
                update_time=datetime.now(),
            )

            return spot
        except Exception as e:
            logger.error(f"获取行业板块实时行情详情失败: {str(e)}")
            raise

    @cache_result()
    @handle_akshare_exception
    async def get_industry_board_spot_by_code(
        self, board_code: str
    ) -> Optional[IndustryBoardSpot]:
        """
        通过板块代码获取行业板块实时行情详情

        Args:
            board_code: 板块代码，如"BK1027"

        Returns:
            Optional[IndustryBoardSpot]: 行业板块实时行情详情，如果未找到则返回None
        """
        logger.info(f"通过代码获取行业板块实时行情详情: {board_code}")

        # 先获取板块名称
        board = await self.get_industry_board(board_code)
        if board is None:
            logger.warning(f"未找到板块代码 {board_code} 对应的板块")
            return None

        # 通过板块名称获取实时行情
        return await self.get_industry_board_spot(board.name)

    async def get_industry_board_constituents(
        self, symbol: str
    ) -> List[IndustryBoardConstituent]:
        """
        获取行业板块成份股

        Args:
            symbol: 板块名称或代码，如"小金属"或"BK1027"

        Returns:
            List[IndustryBoardConstituent]: 行业板块成份股列表
        """
        logger.info(f"获取行业板块成份股: {symbol}")

        return await self._get_industry_board_constituents_from_akshare(symbol)

    @cache_result()
    @handle_akshare_exception
    async def _get_industry_board_constituents_from_akshare(
        self, symbol: str
    ) -> List[IndustryBoardConstituent]:
        """
        从 AKShare 获取行业板块成份股（内部方法）

        Args:
            symbol: 板块名称或代码

        Returns:
            List[IndustryBoardConstituent]: 行业板块成份股列表
        """
        logger.debug(f"使用 AKShare 获取行业板块成份股: {symbol}")

        try:
            # 调用AKShare接口获取行业板块成份股
            df = ak.stock_board_industry_cons_em(symbol=symbol)

            if df.empty:
                logger.warning(f"未获取到板块 {symbol} 的成份股数据")
                return []

            # 将DataFrame转换为IndustryBoardConstituent对象列表
            result = []
            for _, row in df.iterrows():
                # 使用safe_float函数处理所有浮点值
                constituent = IndustryBoardConstituent(
                    rank=int(row["序号"]),
                    code=row["代码"],
                    name=row["名称"],
                    price=safe_float(row["最新价"], 0),
                    change_percent=safe_float(row["涨跌幅"], 0),
                    change=safe_float(row["涨跌额"], 0),
                    volume=safe_float(row["成交量"], 0),
                    amount=safe_float(row["成交额"], 0),
                    amplitude=safe_float(row["振幅"], 0),
                    high=safe_float(row["最高"], 0),
                    low=safe_float(row["最低"], 0),
                    open=safe_float(row["今开"], 0),
                    pre_close=safe_float(row["昨收"], 0),
                    turnover_rate=safe_float(row["换手率"], 0),
                    pe_ratio=safe_float(row["市盈率-动态"]),
                    pb_ratio=safe_float(row["市净率"]),
                    update_time=datetime.now(),
                )
                result.append(constituent)

            return result
        except Exception as e:
            logger.error(f"获取行业板块成份股失败: {str(e)}")
            raise ValueError(f"获取行业板块成份股失败: {str(e)}")

    async def get_sector_leaders(
        self, sector_type: str = "industry", limit: int = 50
    ) -> List[SectorLeader]:
        """
        获取板块龙头股排行

        Args:
            sector_type: 板块类型，"industry" 或 "concept"
            limit: 返回数量限制

        Returns:
            List[SectorLeader]: 板块龙头股列表
        """
        logger.info(f"获取板块龙头股排行, 类型: {sector_type}, 限制: {limit}")

        try:
            boards = await (
                self.get_industry_boards()
                if sector_type == "industry"
                else self.get_concept_boards()
            )

            result = []
            for board in boards[:limit]:
                constituents = await self._get_board_constituents(
                    board.name, sector_type
                )

                leaders = self._calculate_leaders(constituents)

                sector_leader = SectorLeader(
                    sector_code=board.code,
                    sector_name=board.name,
                    sector_type=sector_type,
                    leader_stock=leaders[0] if len(leaders) > 0 else None,
                    second_leader=leaders[1] if len(leaders) > 1 else None,
                    third_leader=leaders[2] if len(leaders) > 2 else None,
                    change_percent=board.change_percent,
                    up_count=board.up_count,
                    down_count=board.down_count,
                    limit_up_count=self._count_limit_up(constituents),
                    limit_down_count=self._count_limit_down(constituents),
                    active_stocks=self._count_active_stocks(constituents),
                    fund_inflow=0,
                    total_amount=sum(c.amount or 0 for c in constituents),
                    activity_score=self._calculate_activity_score(board, constituents),
                )
                result.append(sector_leader)

            result.sort(key=lambda x: x.activity_score, reverse=True)
            return result

        except Exception as e:
            logger.error(f"获取板块龙头股排行失败: {str(e)}")
            raise ValueError(f"获取板块龙头股排行失败: {str(e)}")

    async def get_sector_leader_by_code(
        self, board_code: str, sector_type: str = "industry"
    ) -> Optional[SectorLeader]:
        """
        获取指定板块的龙头股信息

        Args:
            board_code: 板块代码
            sector_type: 板块类型

        Returns:
            Optional[SectorLeader]: 板块龙头股信息
        """
        logger.info(f"获取板块龙头股: {board_code}, 类型: {sector_type}")

        try:
            board = await (
                self.get_industry_board(board_code)
                if sector_type == "industry"
                else self.get_concept_board(board_code)
            )

            if not board:
                return None

            constituents = await self._get_board_constituents(board.name, sector_type)
            leaders = self._calculate_leaders(constituents)

            return SectorLeader(
                sector_code=board.code,
                sector_name=board.name,
                sector_type=sector_type,
                leader_stock=leaders[0] if len(leaders) > 0 else None,
                second_leader=leaders[1] if len(leaders) > 1 else None,
                third_leader=leaders[2] if len(leaders) > 2 else None,
                change_percent=board.change_percent,
                up_count=board.up_count,
                down_count=board.down_count,
                limit_up_count=self._count_limit_up(constituents),
                limit_down_count=self._count_limit_down(constituents),
                active_stocks=self._count_active_stocks(constituents),
                fund_inflow=0,
                total_amount=sum(c.amount or 0 for c in constituents),
                activity_score=self._calculate_activity_score(board, constituents),
            )

        except Exception as e:
            logger.error(f"获取板块龙头股失败: {str(e)}")
            return None

    async def get_sector_realtime_status(
        self, sector_type: str = "industry"
    ) -> List[SectorRealtimeStatus]:
        """
        获取板块实时状态（用于监控）

        Args:
            sector_type: 板块类型

        Returns:
            List[SectorRealtimeStatus]: 板块实时状态列表
        """
        logger.info(f"获取板块实时状态, 类型: {sector_type}")

        try:
            boards = await (
                self.get_industry_boards()
                if sector_type == "industry"
                else self.get_concept_boards()
            )

            result = []
            for board in boards:
                status = SectorRealtimeStatus(
                    sector_code=board.code,
                    sector_name=board.name,
                    sector_type=sector_type,
                    change_percent=board.change_percent,
                    change=board.change,
                    price=board.price,
                    high=0,
                    low=0,
                    open=0,
                    volume=0,
                    amount=0,
                    turnover_rate=board.turnover_rate,
                    up_count=board.up_count,
                    down_count=board.down_count,
                    leading_stock=board.leading_stock,
                    leading_stock_change_percent=board.leading_stock_change_percent,
                )
                result.append(status)

            return result

        except Exception as e:
            logger.error(f"获取板块实时状态失败: {str(e)}")
            raise ValueError(f"获取板块实时状态失败: {str(e)}")

    async def get_sector_rotation_history(
        self,
        board_code: str,
        sector_type: str = "industry",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> List[SectorRotationHistory]:
        """
        获取板块历史行情数据

        Args:
            board_code: 板块代码
            sector_type: 板块类型
            start_date: 开始日期
            end_date: 结束日期

        Returns:
            List[SectorRotationHistory]: 板块历史行情列表
        """
        logger.info(f"获取板块历史行情: {board_code}, 类型: {sector_type}")

        try:
            board = await (
                self.get_industry_board(board_code)
                if sector_type == "industry"
                else self.get_concept_board(board_code)
            )

            if not board:
                return []

            df = await self._get_board_history_df(
                board.name, sector_type, start_date, end_date
            )

            if df is None or df.empty:
                return []

            result = []
            for _, row in df.iterrows():
                history = SectorRotationHistory(
                    date=str(row.get("日期", "")),
                    sector_code=board_code,
                    sector_name=board.name,
                    sector_type=sector_type,
                    open=safe_float(row.get("开盘", 0), 0),
                    close=safe_float(row.get("收盘", 0), 0),
                    high=safe_float(row.get("最高", 0), 0),
                    low=safe_float(row.get("最低", 0), 0),
                    volume=safe_float(row.get("成交量", 0), 0),
                    amount=safe_float(row.get("成交额", 0), 0),
                    change_percent=safe_float(row.get("涨跌幅", 0), 0),
                    amplitude=safe_float(row.get("振幅", 0), 0),
                    turnover_rate=safe_float(row.get("换手率", 0), 0),
                )
                result.append(history)

            return result

        except Exception as e:
            logger.error(f"获取板块历史行情失败: {str(e)}")
            return []

    async def get_sector_factors(
        self, sector_type: str = "industry", limit: int = 30
    ) -> List[SectorFactor]:
        """
        获取板块多因子数据

        Args:
            sector_type: 板块类型
            limit: 返回数量限制

        Returns:
            List[SectorFactor]: 板块多因子数据列表
        """
        logger.info(f"获取板块多因子数据, 类型: {sector_type}")

        try:
            boards = await (
                self.get_industry_boards()
                if sector_type == "industry"
                else self.get_concept_boards()
            )

            result = []
            for board in boards[:limit]:
                factor = SectorFactor(
                    sector_code=board.code,
                    sector_name=board.name,
                    sector_type=sector_type,
                    fund_flow_score=self._calculate_fund_flow_score(board),
                    sentiment_score=self._calculate_sentiment_score(board),
                    technical_score=self._calculate_technical_score(board),
                    pattern_score=self._calculate_pattern_score(board),
                    total_score=self._calculate_total_score(board),
                    limit_up_count=0,
                    up_count=board.up_count,
                )
                result.append(factor)

            result.sort(key=lambda x: x.total_score, reverse=True)
            return result

        except Exception as e:
            logger.error(f"获取板块多因子数据失败: {str(e)}")
            raise ValueError(f"获取板块多因子数据失败: {str(e)}")

    async def predict_rotation(
        self, sector_type: str = "industry"
    ) -> RotationPrediction:
        """
        预测板块轮动

        Args:
            sector_type: 板块类型

        Returns:
            RotationPrediction: 轮动预测结果
        """
        logger.info(f"预测板块轮动, 类型: {sector_type}")

        try:
            factors = await self.get_sector_factors(sector_type, limit=20)

            predictions = []
            for i, factor in enumerate(factors[:10]):
                predictions.append(
                    {
                        "rank": i + 1,
                        "sector_code": factor.sector_code,
                        "sector_name": factor.sector_name,
                        "probability": round(factor.total_score / 100, 4),
                        "confidence": round(0.7 + factor.total_score / 500, 4),
                        "factors": {
                            "fund_flow": factor.fund_flow_score,
                            "sentiment": factor.sentiment_score,
                            "technical": factor.technical_score,
                            "pattern": factor.pattern_score,
                        },
                    }
                )

            prediction_id = f"pred_{datetime.now().strftime('%Y%m%d%H%M%S')}"

            return RotationPrediction(
                prediction_id=prediction_id,
                prediction_time=datetime.now(),
                target_date=datetime.now().strftime("%Y-%m-%d"),
                predictions=predictions,
                model_version="1.0",
                confidence=predictions[0]["confidence"] if predictions else 0,
            )

        except Exception as e:
            logger.error(f"预测板块轮动失败: {str(e)}")
            raise ValueError(f"预测板块轮动失败: {str(e)}")

    async def _get_board_constituents(self, board_name: str, sector_type: str):
        """获取板块成份股"""
        try:
            if sector_type == "industry":
                return await self.get_industry_board_constituents(board_name)
            else:
                return await self.get_concept_board_constituents(board_name)
        except:
            return []

    async def _get_board_history_df(
        self,
        board_name: str,
        sector_type: str,
        start_date: str = None,
        end_date: str = None,
    ):
        """获取板块历史数据DataFrame"""
        try:
            if sector_type == "industry":
                return ak.stock_board_industry_hist_em(
                    symbol=board_name,
                    start_date=start_date or "20240101",
                    end_date=end_date or datetime.now().strftime("%Y%m%d"),
                    adjust="",
                )
            else:
                return ak.stock_board_concept_hist_em(
                    symbol=board_name,
                    start_date=start_date or "20240101",
                    end_date=end_date or datetime.now().strftime("%Y%m%d"),
                    adjust="",
                )
        except Exception as e:
            logger.warning(f"获取板块历史数据失败: {str(e)}")
            return None

    def _calculate_leaders(self, constituents: List) -> List[LeaderStock]:
        """计算龙头股"""
        if not constituents:
            return []

        sorted_stocks = sorted(
            constituents, key=lambda x: x.change_percent, reverse=True
        )

        leaders = []
        for stock in sorted_stocks[:3]:
            score = self._calculate_leader_score(stock)
            leader = LeaderStock(
                code=stock.code,
                name=stock.name,
                price=stock.price,
                change_percent=stock.change_percent,
                change=stock.change,
                volume=stock.volume,
                amount=stock.amount,
                turnover_rate=stock.turnover_rate,
                score=score,
                is_limit_up=stock.change_percent >= 9.9,
            )
            leaders.append(leader)

        return leaders

    def _calculate_leader_score(self, stock) -> float:
        """计算龙头股评分"""
        score = 50.0

        if stock.change_percent > 0:
            score += min(stock.change_percent * 3, 20)

        if stock.amount > 100000:
            score += 10
        elif stock.amount > 50000:
            score += 5

        if stock.turnover_rate > 10:
            score += 10
        elif stock.turnover_rate > 5:
            score += 5

        if stock.change_percent >= 9.9:
            score += 10

        return min(score, 100)

    def _count_limit_up(self, constituents: List) -> int:
        """统计涨停家数"""
        return sum(1 for c in constituents if c.change_percent >= 9.9)

    def _count_limit_down(self, constituents: List) -> int:
        """统计跌停家数"""
        return sum(1 for c in constituents if c.change_percent <= -9.9)

    def _count_active_stocks(self, constituents: List) -> int:
        """统计活跃股数量"""
        return sum(1 for c in constituents if c.change_percent >= 3)

    def _calculate_activity_score(self, board, constituents: List) -> float:
        """计算板块活跃度评分"""
        score = 50.0

        if board.change_percent > 0:
            score += min(board.change_percent * 5, 20)

        limit_up = self._count_limit_up(constituents)
        score += min(limit_up * 5, 15)

        active = self._count_active_stocks(constituents)
        score += min(active, 15)

        return min(score, 100)

    def _calculate_fund_flow_score(self, board) -> float:
        """计算资金流因子得分"""
        score = 50.0
        if board.change_percent > 0:
            score += min(board.change_percent * 3, 30)
        if board.turnover_rate > 5:
            score += min(board.turnover_rate, 20)
        return min(score, 100)

    def _calculate_sentiment_score(self, board) -> float:
        """计算情绪因子得分"""
        score = 50.0
        if board.up_count > board.down_count:
            ratio = board.up_count / max(board.down_count, 1)
            score += min(ratio * 10, 30)
        if board.leading_stock_change_percent > 5:
            score += 20
        return min(score, 100)

    def _calculate_technical_score(self, board) -> float:
        """计算技术因子得分"""
        score = 50.0
        if board.change_percent > 0:
            score += min(board.change_percent * 5, 25)
        if board.turnover_rate > 3:
            score += min(board.turnover_rate * 2, 25)
        return min(score, 100)

    def _calculate_pattern_score(self, board) -> float:
        """计算模式因子得分"""
        score = 50.0
        if board.up_count > 10:
            score += 20
        if board.change_percent > 2:
            score += 20
        if board.turnover_rate > 3:
            score += 10
        return min(score, 100)

    def _calculate_total_score(self, board) -> float:
        """计算综合得分"""
        fund = self._calculate_fund_flow_score(board)
        sentiment = self._calculate_sentiment_score(board)
        technical = self._calculate_technical_score(board)
        pattern = self._calculate_pattern_score(board)

        return round(
            fund * 0.3 + sentiment * 0.25 + technical * 0.25 + pattern * 0.2, 2
        )


sector_service = SectorService()
