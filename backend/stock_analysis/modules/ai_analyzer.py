import os
import base64
import requests
import sys
try:
    import tomllib as tomli
except ImportError:
    import tomli
import urllib3

from typing import Dict, Optional, Any
from .utils import logger

# 禁用 InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def load_ai_config() -> Dict[str, Any]:
    """加载 AI 配置"""
    # 获取当前工作目录
    current_dir = os.getcwd()
    # 获取EXE文件所在目录
    exe_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else current_dir
    
    # 尝试从多个路径查找配置文件
    config_paths = [
        os.path.join(current_dir, 'config.toml'),  # 当前工作目录
        os.path.join(exe_dir, 'config.toml'),      # EXE文件所在目录
        os.path.join(os.path.dirname(__file__), 'config.toml')  # 模块所在目录
    ]
    
    for path in config_paths:
        if os.path.exists(path):
            with open(path, 'rb') as f:
                config = tomli.load(f)
            return config.get('llm', {})
            
    logger.error("未找到 config.toml 文件")
    return {}

def encode_image(image_path: str) -> str:
    """将图片转换为 base64 编码"""
    try:
        with open(image_path, 'rb') as image_file:
            # 添加 base64 前缀
            return f"data:image/png;base64,{base64.b64encode(image_file.read()).decode('utf-8')}"
    except Exception as e:
        logger.error(f"图片编码失败: {str(e)}")
        return ''

def get_ai_analysis(chart_file: str, llm_config: Optional[Dict[str, Any]] = None) -> str:
    """执行AI分析
    Args:
        chart_file: 图表文件路径
        llm_config: AI配置字典 (可选)
    Returns:
        AI分析结果字典
    """
    """获取 AI 分析结果"""
    try:
        if llm_config is None:
            config = load_ai_config()
        else:
            config = llm_config

        if not config:
            return "AI 配置加载失败"
            
        image_path = chart_file
        if not os.path.exists(image_path):
            return "技术分析图表文件不存在"
            
        # 准备 API 请求
        headers = {
            'Authorization': f'Bearer {config["api_key"]}',
            'Content-Type': 'application/json'
        }
        
        # 构建更详细的提示词
        # 修改提示词，要求 AI 在开头明确说明分析的股票
        prompt = f"""你是一个中国股市投资专家，请详细分析这张股票技术分析图表，生成一个分析报告。
        请在分析报告的开头明确说明：股票代码，股票名字，接着以列表形式列出如下信息：
        - **起始日期**:
        - **截止日期**:
        - **起始日价**:
        - **截止日价**:
        - **涨幅**:
        - **总市值**:
        - **得分**:
        
        请使用联网搜索功能获取以下背景信息（如果可用）：
        - 公司最新动态和新闻
        - 行业发展趋势
        - 近期重大公告或事件
        - 市场情绪和投资者关注点
        
        如果无法使用联网搜索功能，请专注于技术分析。
        
        请从以下几个方面进行专业、理性的分析：
        
        1. 趋势分析：
        - 当前主要趋势（上升、下降、盘整）
        - 趋势强度评估
        - 潜在趋势反转信号
        
        2. 技术指标分析：
        - MACD：指标形态、交叉信号、柱状图变化
        - KDJ：超买超卖状态、金叉死叉信号
        - RSI：当前水平、背离信号
        - 均线系统：排列方式、支撑压力位
        
        3. 成交量分析：
        - 成交量变化特征
        - 量价关系
        - 异常成交量信号
        
        4. 形态分析：
        - 识别重要价格形态（如头肩顶、双底等）
        - 形态的可靠性和目标位
        
        5. 风险分析：
        - 当前市场风险水平
        - 潜在的下行风险
        - 止损位建议
        
        6. 操作建议：
        - 基于技术分析的理性操作策略
        - 入场时机建议
        - 目标价位预测
        - 风险控制方案
        
        请遵循以下原则进行分析：
        - 保持客观理性，避免情绪化判断
        - 结合多个指标进行综合分析
        - 明确区分事实和预测
        - 提供可操作的具体建议
        - 注意风险提示和免责声明
        
        请用专业的技术分析语言，以清晰的结构呈现分析结果。"""
        
        # 修改请求体格式
        payload = {
            "model": config["model"],
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},  # 明确指定 text 类型
                        {
                            "type": "image_url",  # 明确指定 image_url 类型
                            "image_url": {
                                "url": encode_image(image_path)
                            }
                        }
                    ]
                }
            ]
        }
        
        # 发送请求到正确的端点
        response = requests.post(
            f"{config['base_url']}chat/completions",
            headers=headers,
            json=payload,
            timeout=30,
            verify=False
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            error_msg = response.json() if response.content else str(response.status_code)
            logger.error(f"AI 请求失败: {error_msg}")
            return f"AI 分析请求失败: {error_msg}"
            
    except Exception as e:
        logger.error(f"获取 AI 分析结果失败: {str(e)}")
        return f"AI 分析失败: {str(e)}"

def save_ai_analysis(analysis: str, output_file: str) -> None:
    """保存 AI 分析结果"""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(analysis)
        logger.debug(f"已保存内容到文件")
    except Exception as e:
        logger.error(f"保存 AI 分析结果失败: {str(e)}")


def main(image_path: str) -> None:
    """
    主函数，执行AI分析并保存结果
    
    Args:
        image_path: 需要分析的图片路径
    """
    try:
        # 执行AI分析
        analysis_result = get_ai_analysis(image_path)
        
        # 生成输出文件名
        output_file = os.path.splitext(image_path)[0] + "_analysis.txt"
        
        # 保存分析结果
        save_ai_analysis(analysis_result, output_file)
        
        logger.info(f"分析结果已保存到: {output_file}")
    except Exception as e:
        logger.error(f"分析过程出错: {str(e)}")

if __name__ == "__main__":
    import argparse
    
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description="股票技术分析图AI分析工具")
    parser.add_argument("image_path", help="需要分析的图片路径")
    
    # 解析参数
    args = parser.parse_args()
    
    # 显式调用main函数
    main(args.image_path)