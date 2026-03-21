import json
import logging
from datetime import datetime, timedelta
from typing import List, Optional

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.stock_calendar_event import StockCalendarEvent

logger = logging.getLogger(__name__)


class CalendarDataSyncService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def sync_earnings_calendar(self, days: int = 90) -> int:
        try:
            import akshare as ak

            start_date = datetime.now().strftime("%Y%m%d")
            end_date = (datetime.now() + timedelta(days=days)).strftime("%Y%m%d")

            logger.info(f"开始同步财报日历: {start_date} - {end_date}")

            try:
                df = ak.stock_financial_report_calendar(
                    start_date=start_date, end_date=end_date
                )
            except Exception as e:
                logger.warning(f"获取财报日历失败: {e}")
                return 0

            if df is None or df.empty:
                logger.warning("财报日历数据为空")
                return 0

            count = 0
            for _, row in df.iterrows():
                try:
                    stock_code = str(row.get("股票代码", "")).zfill(6)
                    stock_name = row.get("股票简称", "")
                    report_date_raw = row.get("实际公告日期") or row.get("预约公告日期")
                    report_period = row.get("报告期", "")

                    if not stock_code or not report_date_raw:
                        continue

                    if isinstance(report_date_raw, str):
                        try:
                            report_date = datetime.strptime(
                                report_date_raw, "%Y-%m-%d"
                            ).date()
                        except:
                            continue
                    else:
                        report_date = report_date_raw

                    existing = await self.db.execute(
                        select(StockCalendarEvent).where(
                            and_(
                                StockCalendarEvent.stock_code == stock_code,
                                StockCalendarEvent.event_type == "earnings_report",
                                StockCalendarEvent.event_date == report_date,
                                StockCalendarEvent.is_delete == False,
                            )
                        )
                    )
                    if existing.scalar_one_or_none():
                        continue

                    event = StockCalendarEvent(
                        stock_code=stock_code,
                        stock_name=stock_name,
                        event_type="earnings_report",
                        event_date=report_date,
                        title=f"{stock_name} {report_period}财报发布",
                        content=f"报告期: {report_period}",
                        impact_data=json.dumps({"report_period": str(report_period)}),
                        data_source="akshare",
                    )
                    self.db.add(event)
                    count += 1

                except Exception as e:
                    logger.error(f"处理财报事件失败: {e}")
                    continue

            await self.db.commit()
            logger.info(f"财报日历同步完成，新增 {count} 条记录")
            return count

        except Exception as e:
            await self.db.rollback()
            logger.error(f"同步财报日历失败: {e}")
            raise

    async def sync_dividend_calendar(self) -> int:
        logger.info("分红数据同步功能开发中...")
        return 0

    async def sync_unlock_calendar(self) -> int:
        logger.info("解禁数据同步功能开发中...")
        return 0

    async def sync_all(self) -> dict:
        results = {}

        try:
            results["earnings"] = await self.sync_earnings_calendar()
        except Exception as e:
            results["earnings_error"] = str(e)

        try:
            results["dividend"] = await self.sync_dividend_calendar()
        except Exception as e:
            results["dividend_error"] = str(e)

        try:
            results["unlock"] = await self.sync_unlock_calendar()
        except Exception as e:
            results["unlock_error"] = str(e)

        return results
