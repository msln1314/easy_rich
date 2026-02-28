"""
新闻分析模块

提供股票新闻搜索、关键词分析和热度评分功能
"""

import requests
import json
import time
import re
from typing import Dict, List, Optional, Tuple
from urllib.parse import quote
import socket
from modules.utils import logger


def check_internet_connection() -> bool:
    """检查网络连接状态"""
    try:
        # 尝试连接到一个可靠的DNS服务器
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        try:
            # 尝试连接百度
            socket.create_connection(("www.baidu.com", 80), timeout=3)
            return True
        except OSError:
            return False


def search_news_baidu(stock_name: str, stock_code: str, max_results: int = 10) -> List[Dict]:
    """
    使用百度搜索股票新闻
    
    Args:
        stock_name: 股票名称
        stock_code: 股票代码
        max_results: 最大结果数量
        
    Returns:
        List[Dict]: 新闻结果列表
    """
    try:
        # 构建搜索关键词
        search_query = f"{stock_name} {stock_code} 股票 最新消息"
        encoded_query = quote(search_query)
        
        # 百度搜索URL
        url = f"https://www.baidu.com/s?wd={encoded_query}&rn={max_results}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        # 解析百度搜索结果 - 使用更简单的方法
        results = []
        
        # 尝试多种解析模式
        patterns = [
            r'<h3.*?<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>',
            r'"title":"([^"]*)".*?"url":"([^"]*)"',
            r'<a[^>]*href="([^"]*)"[^>]*target="_blank"[^>]*>(.*?)</a>'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, response.text, re.DOTALL)
            for match in matches:
                if len(match) == 2:
                    link, title = match
                    title = re.sub('<[^>]*>', '', title).strip()  # 清理HTML标签
                    if title and link.startswith('http'):
                        # 处理百度重定向链接
                        if '/link?url=' in link:
                            try:
                                from urllib.parse import unquote
                                url_match = re.search(r'url=([^&]*)', link)
                                if url_match:
                                    link = unquote(url_match.group(1))
                            except:
                                continue
                        
                        results.append({
                            'title': title,
                            'link': link,
                            'source': '百度搜索',
                            'timestamp': int(time.time())
                        })
                        if len(results) >= max_results:
                            return results
        
        return results[:max_results]
        
    except Exception as e:
        logger.warning(f"百度新闻搜索失败: {e}")
        return []


def search_news_sogou(stock_name: str, stock_code: str, max_results: int = 10) -> List[Dict]:
    """
    使用搜狗搜索作为备用新闻源
    
    Args:
        stock_name: 股票名称
        stock_code: 股票代码
        max_results: 最大结果数量
        
    Returns:
        List[Dict]: 新闻结果列表
    """
    try:
        search_query = f"{stock_name} {stock_code} 股票 新闻"
        encoded_query = quote(search_query)
        
        # 搜狗搜索URL
        url = f"https://www.sogou.com/web?query={encoded_query}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        results = []
        
        # 简单的搜狗搜索结果解析
        pattern = r'<h3.*?<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>'
        matches = re.findall(pattern, response.text, re.DOTALL)
        
        for link, title_html in matches:
            title = re.sub('<[^>]*>', '', title_html).strip()
            if title and link.startswith('http'):
                results.append({
                    'title': title,
                    'link': link,
                    'source': '搜狗搜索',
                    'timestamp': int(time.time())
                })
                if len(results) >= max_results:
                    break
        
        return results[:max_results]
        
    except Exception as e:
        logger.warning(f"搜狗新闻搜索失败: {e}")
        return []


def search_news_duckduckgo(stock_name: str, stock_code: str, max_results: int = 10) -> List[Dict]:
    """
    使用DuckDuckGo搜索股票新闻（国外用户）
    
    Args:
        stock_name: 股票名称
        stock_code: 股票代码
        max_results: 最大结果数量
        
    Returns:
        List[Dict]: 新闻结果列表
    """
    try:
        search_query = f"{stock_name} {stock_code} stock news latest"
        
        # DuckDuckGo API
        url = "https://api.duckduckgo.com/"
        params = {
            'q': search_query,
            'format': 'json',
            'no_html': '1',
            'skip_disambig': '1'
        }
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        results = []
        
        # 提取相关主题
        if 'RelatedTopics' in data:
            for topic in data['RelatedTopics']:
                if 'FirstURL' in topic and 'Text' in topic:
                    results.append({
                        'title': topic.get('Text', ''),
                        'link': topic['FirstURL'],
                        'source': 'DuckDuckGo',
                        'timestamp': int(time.time())
                    })
        
        return results[:max_results]
        
    except Exception as e:
        logger.warning(f"DuckDuckGo新闻搜索失败: {e}")
        return []


def analyze_news_keywords(news_results: List[Dict]) -> Dict:
    """
    分析新闻中的关键词频率
    
    Args:
        news_results: 新闻结果列表
        
    Returns:
        Dict: 包含关键词统计和得分的字典
    """
    # 正面关键词
    positive_keywords = {
        '上涨': 3, '涨停': 5, '大涨': 4, '突破': 3, '利好': 4, '增长': 3,
        '盈利': 3, '业绩': 3, '订单': 2, '合作': 2, '收购': 2, '重组': 2,
        '创新': 2, '技术': 2, '领先': 2, '龙头': 3, '推荐': 3, '买入': 4,
        '增持': 3, '看好': 3, '机会': 2, '潜力': 2, '价值': 2, '低估': 2
    }
    
    # 负面关键词
    negative_keywords = {
        '下跌': -3, '跌停': -5, '大跌': -4, '利空': -4, '亏损': -3,
        '下滑': -3, '风险': -3, '警告': -3, '减持': -3, '卖出': -4,
        '谨慎': -2, '问题': -2, '调查': -3, '处罚': -3, '诉讼': -2,
        '债务': -2, '危机': -3, '退市': -5, 'st': -4, '风险提示': -3
    }
    
    keyword_scores = {}
    total_score = 0
    keyword_count = 0
    
    for news in news_results:
        title = news['title'].lower()
        
        # 检查正面关键词
        for keyword, score in positive_keywords.items():
            if keyword.lower() in title:
                keyword_scores[keyword] = keyword_scores.get(keyword, 0) + 1
                total_score += score
                keyword_count += 1
        
        # 检查负面关键词
        for keyword, score in negative_keywords.items():
            if keyword.lower() in title:
                keyword_scores[keyword] = keyword_scores.get(keyword, 0) + 1
                total_score += score
                keyword_count += 1
    
    return {
        'total_score': total_score,
        'keyword_count': keyword_count,
        'keyword_frequency': keyword_scores,
        'news_count': len(news_results)
    }


def calculate_news_score(stock_name: str, stock_code: str, region: str = 'cn') -> Dict:
    """
    计算股票新闻热度评分
    
    Args:
        stock_name: 股票名称
        stock_code: 股票代码
        region: 地区，'cn'或'intl'
        
    Returns:
        Dict: 包含评分和详细信息的字典
    """
    # 检查网络连接
    if not check_internet_connection():
        return {
            'score': 0,
            'news_count': 0,
            'keyword_count': 0,
            'total_score': 0,
            'status': 'no_internet',
            'message': '网络连接不可用'
        }
    
    try:
        # 根据地区选择搜索引擎
        news_results = []
        if region == 'cn':
            # 尝试多个搜索引擎
            news_results = search_news_baidu(stock_name, stock_code, max_results=15)
            if not news_results:
                news_results = search_news_sogou(stock_name, stock_code, max_results=15)
        else:
            news_results = search_news_duckduckgo(stock_name, stock_code, max_results=15)
        
        if not news_results:
            return {
                'score': 0,
                'news_count': 0,
                'keyword_count': 0,
                'total_score': 0,
                'status': 'no_news',
                'message': '未找到相关新闻'
            }
        
        # 分析关键词
        analysis_result = analyze_news_keywords(news_results)
        
        # 计算最终评分（0-20分）
        raw_score = analysis_result['total_score']
        news_count = analysis_result['news_count']
        
        # 基础评分计算
        if raw_score > 0:
            # 正分：每5分得1分，最高15分
            base_score = min(raw_score // 5, 15)
        else:
            # 负分：每-5分扣1分，最低-5分
            base_score = max(raw_score // 5, -5)
        
        # 新闻数量加成（1-5分）
        news_bonus = min(news_count // 3, 5)
        
        # 最终评分（0-20分范围）
        final_score = max(0, min(base_score + news_bonus, 20))
        
        return {
            'score': final_score,
            'news_count': news_count,
            'keyword_count': analysis_result['keyword_count'],
            'total_score': raw_score,
            'keyword_frequency': analysis_result['keyword_frequency'],
            'news_results': news_results[:5],  # 只返回前5条新闻
            'status': 'success',
            'message': f'找到{news_count}条新闻，关键词得分{raw_score}'
        }
        
    except Exception as e:
        logger.error(f"新闻评分计算失败: {e}")
        return {
            'score': 0,
            'news_count': 0,
            'keyword_count': 0,
            'total_score': 0,
            'status': 'error',
            'message': f'计算失败: {str(e)}'
        }


def get_stock_news_analysis(stock_name: str, stock_code: str, 
                           enable_news: bool = False, region: str = 'cn') -> Dict:
    """
    获取股票新闻分析结果
    
    Args:
        stock_name: 股票名称
        stock_code: 股票代码
        enable_news: 是否启用新闻分析
        region: 地区，'cn'或'intl'
        
    Returns:
        Dict: 新闻分析结果
    """
    if not enable_news:
        return {
            'score': 0,
            'news_count': 0,
            'keyword_count': 0,
            'total_score': 0,
            'status': 'disabled',
            'message': '新闻分析未启用'
        }
    
    return calculate_news_score(stock_name, stock_code, region)