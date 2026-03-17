# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/16
# @File           : export_service.py
# @IDE            : PyCharm
# @desc           : 数据导出服务 - Excel/CSV/JSON导出

import io
import json
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any, Optional

from app.core.logging import get_logger
from app.services.stock_service import stock_service

logger = get_logger(__name__)


class ExportService:
    async def export_stock_list(self, format: str = "excel") -> bytes:
        """导出股票列表"""
        data = await stock_service.get_all_stock_list()
        df = pd.DataFrame(data)
        return self._export_dataframe(df, format)

    async def export_stock_history(
        self,
        stock_code: str,
        period: str = "daily",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        format: str = "excel",
    ) -> bytes:
        """导出股票历史数据"""
        data = await stock_service.get_stock_history(
            stock_code, period, start_date, end_date
        )
        df = pd.DataFrame([d.__dict__ for d in data])
        return self._export_dataframe(df, format)

    async def export_custom_data(
        self, data: List[Dict[str, Any]], format: str = "excel"
    ) -> bytes:
        """导出自定义数据"""
        df = pd.DataFrame(data)
        return self._export_dataframe(df, format)

    def _export_dataframe(self, df: pd.DataFrame, format: str) -> bytes:
        """将DataFrame导出为指定格式"""
        if format == "excel":
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name="Sheet1")
            return output.getvalue()
        elif format == "csv":
            return df.to_csv(index=False).encode("utf-8-sig")
        elif format == "json":
            return json.dumps(
                df.to_dict(orient="records"), ensure_ascii=False, indent=2
            ).encode("utf-8")
        else:
            raise ValueError(f"不支持的导出格式: {format}")

    def get_content_type(self, format: str) -> str:
        """获取Content-Type"""
        types = {
            "excel": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "csv": "text/csv",
            "json": "application/json",
        }
        return types.get(format, "application/octet-stream")

    def get_file_extension(self, format: str) -> str:
        """获取文件扩展名"""
        extensions = {"excel": ".xlsx", "csv": ".csv", "json": ".json"}
        return extensions.get(format, ".dat")


export_service = ExportService()
