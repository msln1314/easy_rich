#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/01/28
# @File           : news.py
# @IDE            : PyCharm
# @desc           : 新闻信息 pydantic 模型，用于数据库序列化操作

from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr, DecimalField
from datetime import datetime


class NewsCreate(BaseModel):
    """创建新闻信息"""
    name: str = Field(..., description="新闻标题")
    content: str = Field(..., description="新闻内容")
    data_from: str = Field(..., description="数据来源")
    agent: str = Field(..., description="代理")
    tag: str | None = Field(None, description="标签")
    is_send: int = Field(..., description="是否发送")
    priority: int | None = Field(None, description="优先级 1 2 3 4")
    date_at: datetime = Field(..., description="新闻日期")
    remark: str | None = Field(None, description="AI分析")
    url: str | None = Field(None, description="链接")
    category: str | None = Field(None, description="板块")
    summary: str | None = Field(None, description="大纲")
    views: int | None = Field(None, description="浏览量")
    is_analyze: int | None = Field(None, description="是否分析")
    analyzed_at: datetime | None = Field(None, description="分析时间")
    geo_scope: str | None = Field(None, description="全球范围")
    industry_scope: str | None = Field(None, description="行业范围")
    impact_on_business: str | None = Field(None, description="企业影响")
    impact_on_industry: str | None = Field(None, description="行业影响")
    impact_on_market: str | None = Field(None, description="市场影响")
    policy_level: str | None = Field(None, description="政策级别")
    policy_intensity: str | None = Field(None, description="政策力度")
    time_sensitivity: str | None = Field(None, description="时间敏感性")
    market_expectation: str | None = Field(None, description="市场预期")
    eps_impact: str | None = Field(None, description="收益影响 正面还是负面")
    primary_sectors: str | None = Field(None, description="受影响板块")
    secondary_sectors: str | None = Field(None, description="间接传导板块")
    style_rotation: str | None = Field(None, description="价值/成长/防御/周期风格影响")
    has_concept_stocks: int | None = Field(None, description="是否有概念股")
    recommendation_level: str | None = Field(None, description="推荐级别")
    confidence_level: str | None = Field(None, description="置信级别")
    confidence_score: DecimalField = Field(None, description="置信度")
    concept_stocks: str | None = Field(None, description="相关股 json")
    risks: str | None = Field(None, description="风险")
    key_points: str | None = Field(None, description="要点")
    analysis_report: str | None = Field(None, description="分析报告")
    score: int | None = Field(None, description="评分")


class NewsUpdate(BaseModel):
    """更新新闻信息"""
    name: str | None = Field(None, description="新闻标题")
    content: str | None = Field(None, description="新闻内容")
    data_from: str | None = Field(None, description="数据来源")
    agent: str | None = Field(None, description="代理")
    tag: str | None = Field(None, description="标签")
    is_send: int | None = Field(None, description="是否发送")
    priority: int | None = Field(None, description="优先级 1 2 3 4")
    date_at: datetime | None = Field(None, description="新闻日期")
    remark: str | None = Field(None, description="AI分析")
    url: str | None = Field(None, description="链接")
    category: str | None = Field(None, description="板块")
    summary: str | None = Field(None, description="大纲")
    views: int | None = Field(None, description="浏览量")
    is_analyze: int | None = Field(None, description="是否分析")
    analyzed_at: datetime | None = Field(None, description="分析时间")
    geo_scope: str | None = Field(None, description="全球范围")
    industry_scope: str | None = Field(None, description="行业范围")
    impact_on_business: str | None = Field(None, description="企业影响")
    impact_on_industry: str | None = Field(None, description="行业影响")
    impact_on_market: str | None = Field(None, description="市场影响")
    policy_level: str | None = Field(None, description="政策级别")
    policy_intensity: str | None = Field(None, description="政策力度")
    time_sensitivity: str | None = Field(None, description="时间敏感性")
    market_expectation: str | None = Field(None, description="市场预期")
    eps_impact: str | None = Field(None, description="收益影响 正面还是负面")
    primary_sectors: str | None = Field(None, description="受影响板块")
    secondary_sectors: str | None = Field(None, description="间接传导板块")
    style_rotation: str | None = Field(None, description="价值/成长/防御/周期风格影响")
    has_concept_stocks: int | None = Field(None, description="是否有概念股")
    recommendation_level: str | None = Field(None, description="推荐级别")
    confidence_level: str | None = Field(None, description="置信级别")
    confidence_score: DecimalField = Field(None, description="置信度")
    concept_stocks: str | None = Field(None, description="相关股 json")
    risks: str | None = Field(None, description="风险")
    key_points: str | None = Field(None, description="要点")
    analysis_report: str | None = Field(None, description="分析报告")
    score: int | None = Field(None, description="评分")


class NewsOut(BaseModel):
    """新闻信息输出"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    content: str
    data_from: str
    agent: str
    tag: str | None = None
    is_send: int
    priority: int | None = None
    date_at: DatetimeStr
    remark: str | None = None
    url: str | None = None
    category: str | None = None
    summary: str | None = None
    views: int | None = None
    is_analyze: int | None = None
    analyzed_at: DatetimeStr | None = None
    geo_scope: str | None = None
    industry_scope: str | None = None
    impact_on_business: str | None = None
    impact_on_industry: str | None = None
    impact_on_market: str | None = None
    policy_level: str | None = None
    policy_intensity: str | None = None
    time_sensitivity: str | None = None
    market_expectation: str | None = None
    eps_impact: str | None = None
    primary_sectors: str | None = None
    secondary_sectors: str | None = None
    style_rotation: str | None = None
    has_concept_stocks: int | None = None
    recommendation_level: str | None = None
    confidence_level: str | None = None
    confidence_score: DecimalField
    concept_stocks: str | None = None
    risks: str | None = None
    key_points: str | None = None
    analysis_report: str | None = None
    score: int | None = None
    created_at: DatetimeStr
    updated_at: DatetimeStr
