import asyncio
import json
from datetime import datetime, date
from typing import Optional, List
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import db_getter
from apps.admin.fund import models, schemas

try:
    import akshare as ak

    AKSHARE_AVAILABLE = True
except ImportError:
    AKSHARE_AVAILABLE = False


class FundDataSyncService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def sync_stock_fund_holders(self, stock_code: str) -> dict:
        if not AKSHARE_AVAILABLE:
            return {"success": False, "message": "akshare 未安装"}

        try:
            df = ak.stock_fund_stock_holder(symbol=stock_code)
            if df.empty:
                return {"success": False, "message": "未获取到数据"}

            records = df.to_dict("records")
            synced_count = 0
            report_date = None

            for record in records:
                fund_code = record.get("基金代码", "")
                if not fund_code:
                    continue

                report_date_str = record.get("截止日期", "")
                if report_date_str:
                    try:
                        report_date = datetime.strptime(
                            str(report_date_str), "%Y-%m-%d"
                        ).date()
                    except:
                        continue

                holding_value = record.get("持仓市值", 0)
                holding_ratio = record.get("占净值比例", 0)
                holding_shares = record.get("持股数", 0)

                change_type = self._get_change_type(record.get("较上期增减", ""))

                obj = models.FundHolding(
                    fund_code=str(fund_code),
                    fund_name=record.get("基金简称", ""),
                    stock_code=stock_code,
                    stock_name=record.get("股票名称", ""),
                    report_date=report_date or date.today(),
                    holding_shares=float(holding_shares) if holding_shares else None,
                    holding_value=float(holding_value) if holding_value else None,
                    holding_ratio=float(holding_ratio) if holding_ratio else None,
                    change_type=change_type,
                )
                self.db.add(obj)
                synced_count += 1

            await self.db.commit()

            if report_date:
                await self._update_mainforce_overview(stock_code, report_date)

            return {
                "success": True,
                "message": f"同步成功 {synced_count} 条记录",
                "count": synced_count,
            }

        except Exception as e:
            await self.db.rollback()
            return {"success": False, "message": f"同步失败: {str(e)}"}

    async def sync_fund_portfolio(
        self, fund_code: str, report_date: str = None
    ) -> dict:
        if not AKSHARE_AVAILABLE:
            return {"success": False, "message": "akshare 未安装"}

        try:
            df = ak.stock_report_fund_hold_detail(symbol=fund_code)
            if df.empty:
                return {"success": False, "message": "未获取到数据"}

            records = df.to_dict("records")
            synced_count = 0
            actual_report_date = date.today()

            for record in records:
                stock_code = record.get("股票代码", "")
                if not stock_code:
                    continue

                holding_value = record.get("持仓市值", 0)
                holding_ratio = record.get("占总股本比例", 0) or record.get(
                    "占流通股比例", 0
                )
                holding_shares = record.get("持股数", 0)

                obj = models.FundHolding(
                    fund_code=fund_code,
                    fund_name="",
                    stock_code=str(stock_code),
                    stock_name=record.get("股票名称", ""),
                    report_date=actual_report_date,
                    holding_shares=float(holding_shares) if holding_shares else None,
                    holding_value=float(holding_value) if holding_value else None,
                    holding_ratio=float(holding_ratio) if holding_ratio else None,
                )
                self.db.add(obj)
                synced_count += 1

            await self.db.commit()
            return {
                "success": True,
                "message": f"同步成功 {synced_count} 条记录",
                "count": synced_count,
            }

        except Exception as e:
            await self.db.rollback()
            return {"success": False, "message": f"同步失败: {str(e)}"}

    async def sync_fund_companies(self) -> dict:
        """
        同步基金公司列表
        :return: 同步结果
        """
        if not AKSHARE_AVAILABLE:
            return {"success": False, "message": "akshare 未安装"}

        try:
            df = ak.fund_company_category_em()
            if df.empty:
                return {"success": False, "message": "未获取到数据"}

            records = df.to_dict("records")
            synced_count = 0

            for record in records:
                company_code = record.get("基金公司代码", "")
                if not company_code:
                    continue

                existing = await self.db.scalar(
                    select(models.FundCompany).where(
                        models.FundCompany.company_code == str(company_code)
                    )
                )

                if existing:
                    existing.company_name = record.get("基金公司简称", "")
                    existing.management_scale = self._parse_scale(
                        record.get("管理规模", "")
                    )
                    existing.fund_count = record.get("基金数量", 0)
                else:
                    obj = models.FundCompany(
                        company_code=str(company_code),
                        company_name=record.get("基金公司简称", ""),
                        management_scale=self._parse_scale(record.get("管理规模", "")),
                        fund_count=record.get("基金数量", 0),
                    )
                    self.db.add(obj)
                synced_count += 1

            await self.db.commit()
            return {
                "success": True,
                "message": f"同步成功 {synced_count} 条记录",
                "count": synced_count,
            }

        except Exception as e:
            await self.db.rollback()
            return {"success": False, "message": f"同步失败: {str(e)}"}

    async def _update_mainforce_overview(self, stock_code: str, report_date: date):
        """
        更新个股主力概览
        """
        result = await self.db.execute(
            select(models.FundHolding).where(
                models.FundHolding.stock_code == stock_code,
                models.FundHolding.report_date == report_date,
            )
        )
        holdings = result.scalars().all()

        if not holdings:
            return

        total_value = sum(h.holding_value or 0 for h in holdings)
        fund_count = len(holdings)

        increase_count = sum(1 for h in holdings if h.change_type == "increase")
        decrease_count = sum(1 for h in holdings if h.change_type == "decrease")
        new_count = sum(1 for h in holdings if h.change_type == "new")
        exit_count = sum(1 for h in holdings if h.change_type == "exit")

        sorted_holdings = sorted(
            holdings, key=lambda x: x.holding_value or 0, reverse=True
        )
        top10_value = sum(h.holding_value or 0 for h in sorted_holdings[:10])
        top20_value = sum(h.holding_value or 0 for h in sorted_holdings[:20])
        top10_ratio = (top10_value / total_value * 100) if total_value > 0 else 0
        top20_ratio = (top20_value / total_value * 100) if total_value > 0 else 0

        existing = await self.db.scalar(
            select(models.StockMainForceOverview).where(
                models.StockMainForceOverview.stock_code == stock_code,
                models.StockMainForceOverview.report_date == report_date,
            )
        )

        if existing:
            existing.fund_count = fund_count
            existing.holding_value = total_value
            existing.top10_ratio = top10_ratio
            existing.top20_ratio = top20_ratio
            existing.increase_count = increase_count
            existing.decrease_count = decrease_count
            existing.new_count = new_count
            existing.exit_count = exit_count
        else:
            stock_name = holdings[0].stock_name if holdings else None
            obj = models.StockMainForceOverview(
                stock_code=stock_code,
                stock_name=stock_name,
                report_date=report_date,
                fund_count=fund_count,
                holding_value=total_value,
                top10_ratio=top10_ratio,
                top20_ratio=top20_ratio,
                increase_count=increase_count,
                decrease_count=decrease_count,
                new_count=new_count,
                exit_count=exit_count,
            )
            self.db.add(obj)

        await self.db.commit()

    def _get_change_type(self, change_str: str) -> Optional[str]:
        """解析变动类型"""
        if not change_str:
            return None
        change_str = str(change_str).lower()
        if "新进" in change_str:
            return "new"
        elif "增持" in change_str or change_str.startswith("+"):
            return "increase"
        elif "减持" in change_str or change_str.startswith("-"):
            return "decrease"
        elif "退出" in change_str:
            return "exit"
        return None

    def _parse_scale(self, scale_str: str) -> Optional[float]:
        """解析管理规模"""
        if not scale_str:
            return None
        try:
            scale_str = str(scale_str).replace("亿", "").strip()
            return float(scale_str)
        except:
            return None


async def sync_stock_mainforce(stock_code: str) -> dict:
    """同步个股主力数据的便捷函数"""
    async_session = db_getter()
    db = await async_session.__anext__()
    try:
        service = FundDataSyncService(db)
        result = await service.sync_stock_fund_holders(stock_code)
        return result
    finally:
        await db.close()


async def sync_fund_data(fund_code: str, report_date: str = None) -> dict:
    """同步基金持仓数据的便捷函数"""
    async_session = db_getter()
    db = await async_session.__anext__()
    try:
        service = FundDataSyncService(db)
        result = await service.sync_fund_portfolio(fund_code, report_date)
        return result
    finally:
        await db.close()
