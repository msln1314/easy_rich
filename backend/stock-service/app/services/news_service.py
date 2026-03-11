# 先导入 akshare-proxy-patch 来修复网络问题 (已禁用)
# try:
#     from app.utils.akshare_proxy_patch import install_patch
#     install_patch("127.0.0.1", "", 30)  # auth_token 为空时不使用代理
# except ImportError as e:
#     print(f"警告：无法导入 akshare 代理补丁: {e}")
#     pass

import akshare as ak
import pandas as pd
from datetime import datetime
from typing import List, Optional
from app.models.news_models import InteractiveQuestion, GlobalFinanceNews, CLSTelegraph
# 修改这一行，从 akshare_wrapper 导入 handle_akshare_exception
from app.utils.akshare_wrapper import handle_akshare_exception
from app.core.logging import get_logger
from app.utils.cache import cache_result

logger = get_logger(__name__)

class NewsService:
    """资讯服务"""
    
    @cache_result()
    @handle_akshare_exception
    async def get_interactive_questions(self, symbol: str) -> List[InteractiveQuestion]:
        """
        获取互动易提问数据
        
        Args:
            symbol: 股票代码，如"002594"
            
        Returns:
            List[InteractiveQuestion]: 互动易提问数据列表
        """
        logger.info(f"获取互动易提问数据: {symbol}")
        
        # 标准化股票代码（去掉市场前缀）
        if symbol.startswith(("sh", "sz", "bj")):
            symbol = symbol[2:]
        
        # 调用AKShare接口获取互动易提问数据
        df = ak.stock_irm_cninfo(symbol=symbol)
        
        if df.empty:
            logger.warning(f"未获取到股票 {symbol} 的互动易提问数据")
            return []
        
        # 将DataFrame转换为InteractiveQuestion对象列表
        result = []
        for _, row in df.iterrows():
            # 处理可能的NaN值
            industry = row["行业"] if pd.notna(row["行业"]) else None
            industry_code = row["行业代码"] if pd.notna(row["行业代码"]) else None
            questioner_id = row["提问者编号"] if pd.notna(row["提问者编号"]) else None
            question_id = row["问题编号"] if pd.notna(row["问题编号"]) else None
            answer_id = row["回答ID"] if pd.notna(row["回答ID"]) else None
            answer_content = row["回答内容"] if pd.notna(row["回答内容"]) else None
            answerer = row["回答者"] if pd.notna(row["回答者"]) else None
            
            # 安全地处理日期时间
            question_time = None
            update_time = None
            
            # 处理提问时间
            if pd.notna(row["提问时间"]):
                if hasattr(row["提问时间"], "to_pydatetime"):
                    question_time = row["提问时间"].to_pydatetime()
                elif isinstance(row["提问时间"], str):
                    # 如果是字符串，尝试解析
                    try:
                        question_time = datetime.strptime(row["提问时间"], "%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        # 如果格式不匹配，直接使用字符串
                        question_time = row["提问时间"]
                else:
                    # 其他情况，转为字符串
                    question_time = str(row["提问时间"])
            
            # 处理更新时间
            if pd.notna(row["更新时间"]):
                if hasattr(row["更新时间"], "to_pydatetime"):
                    update_time = row["更新时间"].to_pydatetime()
                elif isinstance(row["更新时间"], str):
                    # 如果是字符串，尝试解析
                    try:
                        update_time = datetime.strptime(row["更新时间"], "%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        # 如果格式不匹配，直接使用字符串
                        update_time = row["更新时间"]
                else:
                    # 其他情况，转为字符串
                    update_time = str(row["更新时间"])
            
            # 如果时间字段为空，使用当前时间
            if question_time is None:
                question_time = datetime.now()
            if update_time is None:
                update_time = datetime.now()
            
            question = InteractiveQuestion(
                stock_code=row["股票代码"],
                stock_name=row["公司简称"],
                industry=industry,
                industry_code=industry_code,
                question=row["问题"],
                questioner=row["提问者"],
                source=row["来源"],
                question_time=question_time,
                update_time=update_time,
                questioner_id=questioner_id,
                question_id=question_id,
                answer_id=answer_id,
                answer_content=answer_content,
                answerer=answerer
            )
            result.append(question)
        
        return result
    
    @cache_result()
    @handle_akshare_exception
    async def get_global_finance_news(self) -> List[GlobalFinanceNews]:
        """
        获取全球财经快讯数据
        
        Returns:
            List[GlobalFinanceNews]: 全球财经快讯数据列表
        """
        logger.info("获取全球财经快讯数据")
        
        # 调用AKShare接口获取全球财经快讯数据
        df = ak.stock_info_global_em()
        
        if df.empty:
            logger.warning("未获取到全球财经快讯数据")
            return []
        
        # 将DataFrame转换为GlobalFinanceNews对象列表
        result = []
        for _, row in df.iterrows():
            news = GlobalFinanceNews(
                title=row["标题"],
                summary=row["摘要"],
                publish_time=row["发布时间"],
                link=row["链接"],
                update_time=datetime.now()
            )
            result.append(news)
        
        return result
    
    @cache_result()
    @handle_akshare_exception
    async def get_cls_telegraph(self, symbol: str = "全部") -> List[CLSTelegraph]:
        """
        获取财联社电报数据
        
        Args:
            symbol: 类型，可选值为"全部"或"重点"，默认为"全部"
            
        Returns:
            List[CLSTelegraph]: 财联社电报数据列表
        """
        logger.info(f"获取财联社电报数据: {symbol}")
        
        # 调用AKShare接口获取财联社电报数据
        df = ak.stock_info_global_cls(symbol=symbol)
        
        if df.empty:
            logger.warning(f"未获取到财联社电报数据: {symbol}")
            return []
        
        # 将DataFrame转换为CLSTelegraph对象列表
        result = []
        for _, row in df.iterrows():
            # 处理可能的NaN值
            title = row["标题"] if pd.notna(row["标题"]) else ""
            content = row["内容"] if pd.notna(row["内容"]) else ""
            
            # 处理日期和时间字段，确保转换为字符串
            publish_date = row["发布日期"] if pd.notna(row["发布日期"]) else ""
            if not isinstance(publish_date, str):
                # 如果是日期对象，转换为字符串格式
                try:
                    publish_date = publish_date.strftime("%Y-%m-%d") if hasattr(publish_date, "strftime") else str(publish_date)
                except Exception as e:
                    logger.warning(f"转换发布日期失败: {e}")
                    publish_date = str(publish_date)
            
            publish_time = row["发布时间"] if pd.notna(row["发布时间"]) else ""
            if not isinstance(publish_time, str):
                # 如果是时间对象，转换为字符串格式
                try:
                    publish_time = publish_time.strftime("%H:%M:%S") if hasattr(publish_time, "strftime") else str(publish_time)
                except Exception as e:
                    logger.warning(f"转换发布时间失败: {e}")
                    publish_time = str(publish_time)
            
            telegraph = CLSTelegraph(
                title=title,
                content=content,
                publish_date=publish_date,
                publish_time=publish_time,
                update_time=datetime.now()
            )
            result.append(telegraph)
        
        return result