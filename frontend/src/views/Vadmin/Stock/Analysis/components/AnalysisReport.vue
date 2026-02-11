<script setup lang="tsx">
import { computed } from 'vue'
import {
  ElCard,
  ElDescriptions,
  ElDescriptionsItem,
  ElTag,
  ElDivider,
  ElRow,
  ElCol,
  ElProgress
} from 'element-plus'
import dayjs from 'dayjs'

defineOptions({
  name: 'AnalysisReport'
})

const props = defineProps({
  analysisData: {
    type: Object,
    default: () => null
  }
})

// 格式化日期
const formatDate = (date: string | null) => {
  return date ? dayjs(date).format('YYYY-MM-DD') : '-'
}

// 格式化时间
const formatDateTime = (datetime: string | null) => {
  return datetime ? dayjs(datetime).format('YYYY-MM-DD HH:mm:ss') : '-'
}

// 格式化金额
const formatAmount = (amount: number | null, precision: number = 2) => {
  if (amount === null || amount === undefined) return '-'
  return amount.toFixed(precision)
}

// 格式化大数字
const formatNumber = (num: number | null) => {
  if (num === null || num === undefined) return '-'
  if (num >= 100000000) return (num / 100000000).toFixed(2) + '亿'
  if (num >= 10000) return (num / 10000).toFixed(2) + '万'
  return num.toFixed(2)
}

// 获取分析结果样式
const getResultStyle = (result: string) => {
  const colorMap: Record<string, { color: string; bg: string; border: string }> = {
    看涨: { color: '#ef4444', bg: '#fee2e2', border: '#ef4444' },
    看跌: { color: '#3b82f6', bg: '#dbeafe', border: '#3b82f6' },
    中性: { color: '#8b5cf6', bg: '#ddd6fe', border: '#8b5cf6' }
  }
  return colorMap[result] || { color: '#6b7280', bg: '#f3f4f6', border: '#6b7280' }
}

// 获取风险等级样式
const getRiskStyle = (level: string) => {
  const colorMap: Record<string, { color: string; bg: string; border: string }> = {
    low: { color: '#3b82f6', bg: '#dbeafe', border: '#3b82f6' },
    medium: { color: '#f59e0b', bg: '#fef3c7', border: '#f59e0b' },
    high: { color: '#ef4444', bg: '#fee2e2', border: '#ef4444' }
  }
  return colorMap[level] || { color: '#6b7280', bg: '#f3f4f6', border: '#6b7280' }
}

// 获取操作方向样式
const getDirectionStyle = (direction: string) => {
  const colorMap: Record<string, { color: string; bg: string; border: string; icon: string }> = {
    买入: { color: '#ef4444', bg: '#fee2e2', border: '#ef4444', icon: '📈' },
    观望: { color: '#f59e0b', bg: '#fef3c7', border: '#f59e0b', icon: '⏸' },
    卖出: { color: '#3b82f6', bg: '#dbeafe', border: '#3b82f6', icon: '📉' }
  }
  return colorMap[direction] || { color: '#6b7280', bg: '#f3f4f6', border: '#6b7280', icon: '➖' }
}

// 获取涨跌颜色
const getChangeColor = (change: number | null) => {
  if (change === null || change === undefined) return '#6b7280'
  return change > 0 ? '#ef4444' : change < 0 ? '#3b82f6' : '#6b7280'
}

// 获取RSI状态
const getRSIStatus = (rsi: number | null) => {
  if (rsi === null || rsi === undefined) return { text: '-', color: '#6b7280' }
  if (rsi > 70) return { text: '超买', color: '#ef4444' }
  if (rsi < 30) return { text: '超卖', color: '#3b82f6' }
  return { text: '正常', color: '#f59e0b' }
}

// 获取验证状态
const getVerificationStatus = (verified: number | null, result: string | null) => {
  if (!verified) return { text: '未验证', color: '#6b7280', bg: '#f3f4f6' }
  const statusMap: Record<string, { text: string; color: string; bg: string }> = {
    正确: { text: '正确', color: '#ef4444', bg: '#fee2e2' },
    错误: { text: '错误', color: '#3b82f6', bg: '#dbeafe' },
    部分正确: { text: '部分正确', color: '#f59e0b', bg: '#fef3c7' }
  }
  return statusMap[result] || { text: '已验证', color: '#8b5cf6', bg: '#ddd6fe' }
}

// 获取风险等级文本
const getRiskLevelText = (level: string) => {
  const textMap: Record<string, string> = {
    low: '低风险',
    medium: '中风险',
    high: '高风险'
  }
  return textMap[level] || '未知'
}

// 获取涨跌幅显示
const getChangeDisplay = (change: number | null) => {
  if (change === null || change === undefined) return '-'
  const prefix = change > 0 ? '+' : ''
  return prefix + change.toFixed(2) + '%'
}

// 获取操作方向
const getRecommendation = (direction: string, result: string) => {
  if (direction) {
    if (direction.includes('观望')) return { text: '观望', icon: '⏸' }
    if (direction.includes('买入')) return { text: '买入', icon: '📈' }
    if (direction.includes('卖出')) return { text: '卖出', icon: '📉' }
  }
  if (result === '看涨') return { text: '看涨', icon: '📈' }
  if (result === '看跌') return { text: '看跌', icon: '📉' }
  return { text: '中性', icon: '➖' }
}

// 获取方向样式类
const getDirectionClass = () => {
  const direction = props.analysisData?.operation_direction
  if (!direction) return 'direction-neutral'
  if (direction.includes('买入')) return 'direction-buy'
  if (direction.includes('卖出')) return 'direction-sell'
  if (direction.includes('观望')) return 'direction-watch'
  return 'direction-neutral'
}
</script>

<template>
  <div v-if="analysisData" class="analysis-report">
    <!-- 头部卡片 -->
    <ElCard shadow="never" class="header-card">
      <div class="header-content">
        <div class="stock-info">
          <div class="stock-name">{{ analysisData.stock_name || '-' }}</div>
          <div class="stock-code">{{ analysisData.stock_code }}</div>
          <div class="stock-meta">
            <span class="meta-item">{{ analysisData.stock_industry || '-' }}</span>
            <span class="meta-item">•</span>
            <span class="meta-item">{{ analysisData.analysis_period || '-' }}</span>
            <span class="meta-item">•</span>
            <span class="meta-item">{{ analysisData.analysis_type || '-' }}</span>
          </div>
        </div>
        <div class="price-info">
          <div class="current-price">{{
            analysisData.analysis_price ? formatAmount(analysisData.analysis_price) : '-'
          }}</div>
          <div
            class="price-change"
            :style="{ color: getChangeColor(analysisData.analysis_change_percent) }"
          >
            {{ getChangeDisplay(analysisData.analysis_change_percent) }}
          </div>
          <div class="recommendation-badge" :class="getDirectionClass()">
            <span class="badge-icon">{{
              getRecommendation(analysisData.operation_direction, analysisData.analysis_result).icon
            }}</span>
            <span class="badge-text">{{
              getRecommendation(analysisData.operation_direction, analysisData.analysis_result).text
            }}</span>
          </div>
        </div>
      </div>
      <div class="header-footer">
        <div class="footer-badge">
          <span class="badge-dot"></span>
          <span class="footer-label">分析时间</span>
          <span class="footer-value">{{ formatDateTime(analysisData.analysis_time) }}</span>
        </div>
        <div class="footer-badge">
          <span class="badge-dot"></span>
          <span class="footer-label">分析师</span>
          <span class="footer-value">{{ analysisData.analyzer || '-' }}</span>
        </div>
        <div class="footer-badge">
          <span class="badge-dot"></span>
          <span class="footer-label">分析来源</span>
          <span class="footer-value">{{ analysisData.analysis_source || '-' }}</span>
        </div>
      </div>
    </ElCard>

    <!-- 关键指标卡片 -->
    <ElRow :gutter="16" class="metrics-row">
      <ElCol :xs="24" :sm="12" :md="8" :lg="6" :xl="4">
        <div class="metric-card">
          <div
            class="metric-icon"
            style="background: linear-gradient(135deg, #bfdbfe 0%, #93c5fd 100%); color: #1e40af"
          >
            <span>🎯</span>
          </div>
          <div class="metric-content">
            <div class="metric-label">目标价格</div>
            <div class="metric-value"
              >{{ analysisData.target_price ? formatAmount(analysisData.target_price) : '-' }}
              <span class="metric-unit">元</span></div
            >
          </div>
        </div>
      </ElCol>
      <ElCol :xs="24" :sm="12" :md="8" :lg="6" :xl="4">
        <div class="metric-card">
          <div
            class="metric-icon"
            style="background: linear-gradient(135deg, #fde68a 0%, #fcd34d 100%); color: #b45309"
          >
            <span>🛡</span>
          </div>
          <div class="metric-content">
            <div class="metric-label">止损价格</div>
            <div class="metric-value"
              >{{ analysisData.stop_price ? formatAmount(analysisData.stop_price) : '-' }}
              <span class="metric-unit">元</span></div
            >
          </div>
        </div>
      </ElCol>
      <ElCol :xs="24" :sm="12" :md="8" :lg="6" :xl="4">
        <div class="metric-card">
          <div
            class="metric-icon"
            style="background: linear-gradient(135deg, #ddd6fe 0%, #c4b5fd 100%); color: #5b21b6"
          >
            <span>📊</span>
          </div>
          <div class="metric-content">
            <div class="metric-label">期望收益</div>
            <div class="metric-value"
              >{{ analysisData.ev ? formatAmount(analysisData.ev) : '-' }}
              <span class="metric-unit">%</span></div
            >
          </div>
        </div>
      </ElCol>
      <ElCol :xs="24" :sm="12" :md="8" :lg="6" :xl="4">
        <div class="metric-card">
          <div
            class="metric-icon"
            style="background: linear-gradient(135deg, #bfdbfe 0%, #93c5fd 100%); color: #1e40af"
          >
            <span>🎲</span>
          </div>
          <div class="metric-content">
            <div class="metric-label">置信值</div>
            <div class="metric-value"
              >{{
                analysisData.confidence_value ? formatAmount(analysisData.confidence_value) : '-'
              }}
              <span class="metric-unit">%</span></div
            >
          </div>
        </div>
      </ElCol>
      <ElCol :xs="24" :sm="12" :md="8" :lg="6" :xl="4">
        <div class="metric-card">
          <div
            class="metric-icon"
            style="background: linear-gradient(135deg, #fecaca 0%, #fca5a5 100%); color: #991b1b"
          >
            <span>⚖</span>
          </div>
          <div class="metric-content">
            <div class="metric-label">风险收益比</div>
            <div class="metric-value">{{ analysisData.risk_rate || '-' }}</div>
          </div>
        </div>
      </ElCol>
      <ElCol :xs="24" :sm="12" :md="8" :lg="6" :xl="4">
        <div class="metric-card">
          <div
            class="metric-icon"
            style="background: linear-gradient(135deg, #ddd6fe 0%, #c4b5fd 100%); color: #5b21b6"
          >
            <span>⭐</span>
          </div>
          <div class="metric-content">
            <div class="metric-label">评分</div>
            <div class="metric-value">{{ analysisData.score || '-' }}</div>
          </div>
        </div>
      </ElCol>
    </ElRow>

    <!-- 价格区间卡片 -->
    <ElCard shadow="hover" class="section-card">
      <template #header>
        <div class="card-header">
          <span class="header-icon">📈</span>
          <span class="header-title">价格区间</span>
        </div>
      </template>
      <ElRow :gutter="20">
        <ElCol :span="8">
          <div class="price-item">
            <div class="price-label">最高价</div>
            <div class="price-value high"
              >{{ analysisData.high_price ? formatAmount(analysisData.high_price) : '-' }}
              <span class="unit">元</span></div
            >
          </div>
        </ElCol>
        <ElCol :span="8">
          <div class="price-item">
            <div class="price-label">最低价</div>
            <div class="price-value low"
              >{{ analysisData.low_price ? formatAmount(analysisData.low_price) : '-' }}
              <span class="unit">元</span></div
            >
          </div>
        </ElCol>
        <ElCol :span="8">
          <div class="price-item">
            <div class="price-label">开盘价</div>
            <div class="price-value"
              >{{ analysisData.open_price ? formatAmount(analysisData.open_price) : '-' }}
              <span class="unit">元</span></div
            >
          </div>
        </ElCol>
      </ElRow>
      <ElRow :gutter="20" class="mt-3">
        <ElCol :span="12">
          <div class="price-item">
            <div class="price-label">支撑位</div>
            <div class="price-value">{{ analysisData.support || '-' }}</div>
          </div>
        </ElCol>
        <ElCol :span="12">
          <div class="price-item">
            <div class="price-label">阻力位</div>
            <div class="price-value">{{ analysisData.resistance || '-' }}</div>
          </div>
        </ElCol>
      </ElRow>
    </ElCard>

    <!-- 成交数据卡片 -->
    <ElCard shadow="hover" class="section-card">
      <template #header>
        <div class="card-header">
          <span class="header-icon">💹</span>
          <span class="header-title">成交数据</span>
        </div>
      </template>
      <ElRow :gutter="20">
        <ElCol :xs="24" :sm="12" :md="8">
          <div class="data-item">
            <div class="data-label">成交量(手)</div>
            <div class="data-value">{{
              analysisData.volume ? formatNumber(analysisData.volume) : '-'
            }}</div>
          </div>
        </ElCol>
        <ElCol :xs="24" :sm="12" :md="8">
          <div class="data-item">
            <div class="data-label">成交额(万元)</div>
            <div class="data-value">{{
              analysisData.amount ? formatNumber(analysisData.amount) : '-'
            }}</div>
          </div>
        </ElCol>
        <ElCol :xs="24" :sm="12" :md="8">
          <div class="data-item">
            <div class="data-label">换手率(%)</div>
            <div
              class="data-value"
              :style="{
                color:
                  parseFloat(analysisData.analysis_turnover_rate) > 5
                    ? '#ef4444'
                    : parseFloat(analysisData.analysis_turnover_rate) > 3
                    ? '#f59e0b'
                    : '#3b82f6'
              }"
            >
              {{
                analysisData.analysis_turnover_rate
                  ? formatAmount(analysisData.analysis_turnover_rate)
                  : '-'
              }}
            </div>
          </div>
        </ElCol>
        <ElCol :xs="24" :sm="12" :md="8">
          <div class="data-item">
            <div class="data-label">量比</div>
            <div
              class="data-value"
              :style="{
                color:
                  parseFloat(analysisData.analysis_volume_ratio) > 2
                    ? '#ef4444'
                    : parseFloat(analysisData.analysis_volume_ratio) > 1
                    ? '#f59e0b'
                    : '#3b82f6'
              }"
            >
              {{
                analysisData.analysis_volume_ratio
                  ? formatAmount(analysisData.analysis_volume_ratio)
                  : '-'
              }}
            </div>
          </div>
        </ElCol>
        <ElCol :xs="24" :sm="12" :md="8">
          <div class="data-item">
            <div class="data-label">流通市值(万元)</div>
            <div class="data-value">{{
              analysisData.circulating_market_cap
                ? formatNumber(analysisData.circulating_market_cap)
                : '-'
            }}</div>
          </div>
        </ElCol>
        <ElCol :xs="24" :sm="12" :md="8">
          <div class="data-item">
            <div class="data-label">总市值(万元)</div>
            <div class="data-value">{{
              analysisData.total_market_cap ? formatNumber(analysisData.total_market_cap) : '-'
            }}</div>
          </div>
        </ElCol>
      </ElRow>
    </ElCard>

    <!-- 技术指标卡片 -->
    <ElCard shadow="hover" class="section-card">
      <template #header>
        <div class="card-header">
          <span class="header-icon">📊</span>
          <span class="header-title">技术指标</span>
        </div>
      </template>
      <ElRow :gutter="20">
        <ElCol :xs="12" :sm="8" :md="6">
          <div class="indicator-item">
            <div class="indicator-label">MA5</div>
            <div class="indicator-value"
              >{{ analysisData.ma5 ? formatAmount(analysisData.ma5) : '-' }}
              <span class="unit">元</span></div
            >
          </div>
        </ElCol>
        <ElCol :xs="12" :sm="8" :md="6">
          <div class="indicator-item">
            <div class="indicator-label">MA10</div>
            <div class="indicator-value"
              >{{ analysisData.ma10 ? formatAmount(analysisData.ma10) : '-' }}
              <span class="unit">元</span></div
            >
          </div>
        </ElCol>
        <ElCol :xs="12" :sm="8" :md="6">
          <div class="indicator-item">
            <div class="indicator-label">MA20</div>
            <div class="indicator-value"
              >{{ analysisData.ma20 ? formatAmount(analysisData.ma20) : '-' }}
              <span class="unit">元</span></div
            >
          </div>
        </ElCol>
        <ElCol :xs="12" :sm="8" :md="6">
          <div class="indicator-item">
            <div class="indicator-label">RSI</div>
            <div class="indicator-value" :style="{ color: getRSIStatus(analysisData.rsi).color }">
              {{ analysisData.rsi ? formatAmount(analysisData.rsi) : '-' }}
            </div>
            <ElTag
              v-if="analysisData.rsi"
              :type="
                getRSIStatus(analysisData.rsi).text === '超买'
                  ? 'danger'
                  : getRSIStatus(analysisData.rsi).text === '超卖'
                  ? 'success'
                  : 'warning'
              "
              size="small"
              class="mt-1"
            >
              {{ getRSIStatus(analysisData.rsi).text }}
            </ElTag>
          </div>
        </ElCol>
        <ElCol :xs="12" :sm="8" :md="6">
          <div class="indicator-item">
            <div class="indicator-label">MACD</div>
            <div
              class="indicator-value"
              :style="{
                color:
                  analysisData.macd > 0 ? '#3b82f6' : analysisData.macd < 0 ? '#ef4444' : '#6b7280'
              }"
            >
              {{ analysisData.macd ? formatAmount(analysisData.macd, 4) : '-' }}
            </div>
          </div>
        </ElCol>
        <ElCol :xs="12" :sm="8" :md="6">
          <div class="indicator-item">
            <div class="indicator-label">市盈率</div>
            <div
              class="indicator-value"
              :style="{
                color:
                  parseFloat(analysisData.pe_ratio) < 15
                    ? '#8b5cf6'
                    : parseFloat(analysisData.pe_ratio) > 30
                    ? '#ef4444'
                    : '#f59e0b'
              }"
            >
              {{ analysisData.pe_ratio ? formatAmount(analysisData.pe_ratio) : '-' }}
              <span class="unit">倍</span>
            </div>
          </div>
        </ElCol>
      </ElRow>
      <ElRow :gutter="20" class="mt-3">
        <ElCol :span="12">
          <div class="analysis-item">
            <div class="analysis-label">趋势判断</div>
            <div class="analysis-value">{{ analysisData.trend_judgment || '-' }}</div>
          </div>
        </ElCol>
        <ElCol :span="12">
          <div class="analysis-item">
            <div class="analysis-label">价格行为</div>
            <div class="analysis-value">{{ analysisData.price_action || '-' }}</div>
          </div>
        </ElCol>
      </ElRow>
    </ElCard>

    <!-- 操作建议卡片 -->
    <ElCard shadow="hover" class="section-card operation-card">
      <template #header>
        <div class="card-header">
          <span class="header-icon">🎯</span>
          <span class="header-title">操作建议</span>
        </div>
      </template>

      <!-- 核心操作方向 -->
      <div class="action-banner" :class="getDirectionClass()">
        <div class="banner-content">
          <div class="action-icon">{{
            getDirectionStyle(analysisData.operation_direction).icon
          }}</div>
          <div class="action-info">
            <div class="action-label">核心操作建议</div>
            <div class="action-title">{{
              getRecommendation(analysisData.operation_direction, analysisData.analysis_result).text
            }}</div>
          </div>
        </div>
        <div class="action-meta">
          <div class="meta-item">
            <span class="meta-label">建议仓位</span>
            <span class="meta-value">{{ analysisData.action_position || '-' }}</span>
          </div>
          <div class="meta-item">
            <span class="meta-label">风险等级</span>
            <span class="meta-value">{{ getRiskLevelText(analysisData.risk_level) }}</span>
          </div>
        </div>
      </div>

      <!-- 详细指标 -->
      <div class="metrics-grid">
        <div class="metric-box">
          <div class="metric-box-icon period-icon">📅</div>
          <div class="metric-box-content">
            <div class="metric-box-label">持仓周期</div>
            <div class="metric-box-value">{{ analysisData.hold_period || '-' }}</div>
          </div>
        </div>
        <div class="metric-box">
          <div class="metric-box-icon type-icon">💼</div>
          <div class="metric-box-content">
            <div class="metric-box-label">持有类型</div>
            <div class="metric-box-value">{{ analysisData.hold_type || '-' }}</div>
          </div>
        </div>
        <div class="metric-box">
          <div class="metric-box-icon range-icon">📍</div>
          <div class="metric-box-content">
            <div class="metric-box-label">操作区间</div>
            <div class="metric-box-value">{{
              analysisData.operation_price_range || analysisData.action_range || '-'
            }}</div>
          </div>
        </div>
        <div class="metric-box">
          <div class="metric-box-icon ratio-icon">📈</div>
          <div class="metric-box-content">
            <div class="metric-box-label">风险收益比</div>
            <div class="metric-box-value">{{ analysisData.risk_rate || '-' }}</div>
          </div>
        </div>
      </div>
    </ElCard>

    <!-- 分析内容卡片 -->
    <ElCard shadow="hover" class="section-card">
      <template #header>
        <div class="card-header">
          <span class="header-icon">📝</span>
          <span class="header-title">分析内容</span>
        </div>
      </template>
      <div class="content-section">
        <div v-if="analysisData.analysis_summary" class="summary-box">
          <div class="summary-title">分析摘要</div>
          <div class="summary-content">{{ analysisData.analysis_summary }}</div>
        </div>
        <div v-if="analysisData.analysis_content" class="analysis-content-box">
          <div class="content-title">详细分析</div>
          <div class="content-text">{{ analysisData.analysis_content }}</div>
        </div>
      </div>
    </ElCard>

    <!-- 其他信息卡片 -->
    <ElRow :gutter="16">
      <ElCol :xs="24" :sm="12">
        <ElCard shadow="hover" class="info-card">
          <template #header>
            <div class="card-header">
              <span class="header-icon">🏦</span>
              <span class="header-title">估值信息</span>
            </div>
          </template>
          <ElDescriptions :column="2" border>
            <ElDescriptionsItem label="市盈率(PE)"
              >{{ analysisData.pe_ratio ? formatAmount(analysisData.pe_ratio) : '-' }}
              <span class="unit">倍</span></ElDescriptionsItem
            >
            <ElDescriptionsItem label="市净率(PB)"
              >{{ analysisData.pb_ratio ? formatAmount(analysisData.pb_ratio) : '-' }}
              <span class="unit">倍</span></ElDescriptionsItem
            >
            <ElDescriptionsItem label="核心价值">{{
              analysisData.valuation || '-'
            }}</ElDescriptionsItem>
            <ElDescriptionsItem label="市场情绪">{{
              analysisData.market_sentiment || '-'
            }}</ElDescriptionsItem>
          </ElDescriptions>
        </ElCard>
      </ElCol>
      <ElCol :xs="24" :sm="12">
        <ElCard shadow="hover" class="info-card">
          <template #header>
            <div class="card-header">
              <span class="header-icon">⚠️</span>
              <span class="header-title">风险提示</span>
            </div>
          </template>
          <div class="risk-box">
            <div v-if="analysisData.main_risks" class="risk-item">
              <div class="risk-label">主要风险</div>
              <div class="risk-content">{{ analysisData.main_risks }}</div>
            </div>
            <div v-if="analysisData.key_catalysts" class="risk-item">
              <div class="risk-label">关键催化剂</div>
              <div class="risk-content">{{ analysisData.key_catalysts }}</div>
            </div>
          </div>
        </ElCard>
      </ElCol>
    </ElRow>

    <!-- 标签和备注 -->
    <ElCard shadow="hover" class="section-card">
      <template #header>
        <div class="card-header">
          <span class="header-icon">🏷️</span>
          <span class="header-title">标签与备注</span>
        </div>
      </template>
      <div v-if="analysisData.tags" class="tags-box">
        <ElTag
          v-for="(tag, index) in analysisData.tags.split(',')"
          :key="index"
          class="tag-item"
          type="info"
        >
          {{ tag.trim() }}
        </ElTag>
      </div>
      <div v-if="analysisData.notes" class="notes-box">
        <div class="notes-label">备注信息</div>
        <div class="notes-content">{{ analysisData.notes }}</div>
      </div>
    </ElCard>

    <!-- 状态信息 -->
    <ElCard shadow="hover" class="status-card">
      <template #header>
        <div class="card-header">
          <span class="header-icon">✅</span>
          <span class="header-title">状态信息</span>
        </div>
      </template>
      <ElRow :gutter="20" class="status-grid">
        <ElCol :xs="24" :sm="8">
          <div class="status-item-wrapper">
            <div class="status-icon-wrapper">
              <div class="status-icon verify-icon">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z" />
                </svg>
              </div>
            </div>
            <div class="status-content">
              <div class="status-label">验证状态</div>
              <div class="status-tags">
                <ElTag
                  :type="analysisData.is_verified === 1 ? 'success' : 'info'"
                  size="large"
                  effect="dark"
                >
                  {{ analysisData.is_verified === 1 ? '已验证' : '未验证' }}
                </ElTag>
                <ElTag
                  v-if="analysisData.is_verified === 1 && analysisData.verification_result"
                  :type="
                    analysisData.verification_result === '正确'
                      ? 'success'
                      : analysisData.verification_result === '错误'
                      ? 'danger'
                      : 'warning'
                  "
                  effect="dark"
                  size="large"
                >
                  {{ analysisData.verification_result }}
                </ElTag>
              </div>
            </div>
          </div>
        </ElCol>
        <ElCol :xs="24" :sm="8">
          <div class="status-item-wrapper">
            <div class="status-icon-wrapper">
              <div class="status-icon send-icon">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" />
                </svg>
              </div>
            </div>
            <div class="status-content">
              <div class="status-label">发送状态</div>
              <div class="status-tags">
                <ElTag
                  :type="analysisData.is_send === 1 ? 'success' : 'info'"
                  size="large"
                  effect="dark"
                >
                  {{ analysisData.is_send === 1 ? '已发送' : '未发送' }}
                </ElTag>
              </div>
            </div>
          </div>
        </ElCol>
        <ElCol :xs="24" :sm="8">
          <div class="status-item-wrapper">
            <div class="status-icon-wrapper">
              <div class="status-icon date-icon">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path
                    d="M19 4h-1V2h-2v2H8V2H6v2H5c-1.11 0-1.99.9-1.99 2L3 20a2 2 0 0 0 2 2h14c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 16H5V10h14v10zm0-12H5V6h14v2zm-7 5h5v5h-5z"
                  />
                </svg>
              </div>
            </div>
            <div class="status-content">
              <div class="status-label">验证日期</div>
              <div class="status-value">{{ formatDate(analysisData.verification_date) }}</div>
            </div>
          </div>
        </ElCol>
      </ElRow>
      <div class="footer-info">
        <div class="timeline-info">
          <div class="timeline-item">
            <div class="timeline-dot"></div>
            <div class="timeline-content">
              <div class="timeline-label">创建时间</div>
              <div class="timeline-value">{{ formatDateTime(analysisData.created_at) }}</div>
            </div>
          </div>
          <div class="timeline-item">
            <div class="timeline-dot"></div>
            <div class="timeline-content">
              <div class="timeline-label">更新时间</div>
              <div class="timeline-value">{{ formatDateTime(analysisData.updated_at) }}</div>
            </div>
          </div>
          <div class="timeline-item">
            <div class="timeline-dot"></div>
            <div class="timeline-content">
              <div class="timeline-label">触发来源</div>
              <div class="timeline-value">{{ analysisData.data_from || '-' }}</div>
            </div>
          </div>
        </div>
      </div>
    </ElCard>

    <!-- 免责声明 -->
    <ElCard shadow="never" class="disclaimer-card">
      <div class="disclaimer-content">
        <div class="disclaimer-icon">⚠️</div>
        <div class="disclaimer-text">
          本报告由人工智能模型自动生成，基于公开市场信息进行分析。报告内容仅供参考，不构成任何投资建议或买卖依据。投资者应结合自身风险承受能力和投资目标独立决策。股市有风险，投资需谨慎。
        </div>
      </div>
    </ElCard>
  </div>
</template>

<style scoped lang="scss">
.analysis-report {
  padding: 20px;
  background: #f5f7fa;
  min-height: auto;
  width: 100%;
  position: relative;
  display: block;
  overflow: visible;

  // 头部卡片
  .header-card {
    margin-bottom: 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border: none;

    :deep(.el-card__body) {
      padding: 30px;
    }

    .header-content {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 25px;

      @media (max-width: 768px) {
        flex-direction: column;
        gap: 20px;
        text-align: center;
      }
    }

    .stock-info {
      text-align: left;

      @media (max-width: 768px) {
        text-align: center;
      }

      .stock-name {
        font-size: 32px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 8px;
      }

      .stock-code {
        font-size: 20px;
        color: #e0e7ff;
        margin-bottom: 12px;
        font-weight: 500;
      }

      .stock-meta {
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 14px;
        color: #c7d2fe;

        @media (max-width: 768px) {
          justify-content: center;
        }
      }
    }

    .price-info {
      text-align: right;

      @media (max-width: 768px) {
        text-align: center;
      }

      .current-price {
        font-size: 36px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 8px;
      }

      .price-change {
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 15px;
      }

      .recommendation-badge {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        padding: 12px 28px;
        border-radius: 12px;
        font-weight: 700;
        font-size: 17px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);

        .badge-icon {
          font-size: 22px;
        }

        .badge-text {
          font-weight: 800;
          letter-spacing: 0.5px;
        }

        &.direction-buy {
          background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
          color: white;
          border: 2px solid #7f1d1d;
        }

        &.direction-sell {
          background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
          color: white;
          border: 2px solid #1e3a8a;
        }

        &.direction-watch {
          background: linear-gradient(135deg, #d97706 0%, #b45309 100%);
          color: white;
          border: 2px solid #78350f;
        }

        &.direction-neutral {
          background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
          color: white;
          border: 2px solid #1e3a8a;
        }
      }
    }

    .header-footer {
      display: flex;
      justify-content: space-around;
      padding-top: 20px;
      border-top: 2px solid rgba(255, 255, 255, 0.3);

      @media (max-width: 768px) {
        flex-direction: column;
        gap: 15px;
      }

      .footer-badge {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 8px 16px;
        background: rgba(255, 255, 255, 0.15);
        border-radius: 8px;
        backdrop-filter: blur(5px);

        .badge-dot {
          width: 8px;
          height: 8px;
          border-radius: 50%;
          background: #a5b4fc;
          box-shadow: 0 0 8px rgba(165, 180, 252, 0.6);
        }

        .footer-label {
          font-size: 12px;
          color: #c7d2fe;
          font-weight: 600;
          margin-right: 6px;
        }

        .footer-value {
          font-size: 14px;
          color: #ffffff;
          font-weight: 700;
        }
      }
    }
  }

  // 指标行
  .metrics-row {
    margin-bottom: 20px;
  }

  // 指标卡片
  .metric-card {
    background: white;
    border-radius: 12px;
    padding: 20px;
    display: flex;
    align-items: center;
    gap: 15px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    transition: all 0.3s;

    &:hover {
      transform: translateY(-4px);
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
    }

    .metric-icon {
      width: 56px;
      height: 56px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 28px;
      flex-shrink: 0;
    }

    .metric-content {
      flex: 1;

      .metric-label {
        font-size: 13px;
        color: #6b7280;
        margin-bottom: 5px;
      }

      .metric-value {
        font-size: 22px;
        font-weight: 700;
        color: #1f2937;

        .metric-unit {
          font-size: 14px;
          font-weight: 400;
          color: #9ca3af;
          margin-left: 4px;
        }
      }
    }
  }

  // 通用卡片样式
  .section-card {
    margin-bottom: 20px;

    :deep(.el-card__header) {
      background: #f8fafc;
      border-bottom: 2px solid #e5e7eb;
    }

    .card-header {
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 18px;
      font-weight: 600;
      color: #1f2937;
    }

    .header-icon {
      font-size: 22px;
    }
  }

  // 价格项
  .price-item {
    text-align: center;
    padding: 15px;
    background: #f9fafb;
    border-radius: 8px;

    .price-label {
      font-size: 13px;
      color: #6b7280;
      margin-bottom: 8px;
    }

    .price-value {
      font-size: 24px;
      font-weight: 700;
      color: #1f2937;

      .unit {
        font-size: 14px;
        color: #9ca3af;
        margin-left: 4px;
      }

      &.high {
        color: #ef4444;
      }

      &.low {
        color: #3b82f6;
      }
    }
  }

  // 数据项
  .data-item {
    text-align: center;
    padding: 15px;
    background: #f9fafb;
    border-radius: 8px;
    margin-bottom: 15px;

    .data-label {
      font-size: 13px;
      color: #6b7280;
      margin-bottom: 8px;
    }

    .data-value {
      font-size: 20px;
      font-weight: 700;
      color: #1f2937;
    }
  }

  // 技术指标项
  .indicator-item {
    text-align: center;
    padding: 15px;
    background: #f9fafb;
    border-radius: 8px;
    margin-bottom: 15px;

    .indicator-label {
      font-size: 13px;
      color: #6b7280;
      margin-bottom: 8px;
    }

    .indicator-value {
      font-size: 20px;
      font-weight: 700;
      color: #1f2937;
      margin-bottom: 5px;

      .unit {
        font-size: 14px;
        color: #9ca3af;
        margin-left: 4px;
      }
    }
  }

  // 分析项
  .analysis-item {
    padding: 15px;
    background: #f9fafb;
    border-radius: 8px;
    margin-bottom: 15px;

    .analysis-label {
      font-size: 13px;
      color: #6b7280;
      margin-bottom: 8px;
    }

    .analysis-value {
      font-size: 15px;
      color: #1f2937;
      font-weight: 500;
      line-height: 1.6;
    }
  }

  // 操作项
  .operation-item {
    text-align: center;
    padding: 15px;

    .operation-label {
      font-size: 13px;
      color: #6b7280;
      margin-bottom: 10px;
    }

    .operation-value {
      font-size: 18px;
      font-weight: 600;
      color: #1f2937;
    }
  }

  // 操作卡片特殊样式
  .operation-card {
    background: #ffffff;

    :deep(.el-card__header) {
      background: #f8fafc;
    }

    // 核心操作横幅
    .action-banner {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 28px 32px;
      border-radius: 16px;
      margin-bottom: 24px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
      transition: all 0.3s;

      &:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
      }

      @media (max-width: 768px) {
        flex-direction: column;
        gap: 20px;
        padding: 24px 20px;
      }

      .banner-content {
        display: flex;
        align-items: center;
        gap: 20px;

        @media (max-width: 768px) {
          flex-direction: column;
          text-align: center;
        }

        .action-icon {
          font-size: 56px;
          animation: pulse 2s ease-in-out infinite;
        }

        .action-info {
          .action-label {
            font-size: 13px;
            color: rgba(255, 255, 255, 0.95);
            margin-bottom: 6px;
            font-weight: 600;
            letter-spacing: 0.5px;
          }

          .action-title {
            font-size: 32px;
            font-weight: 800;
            color: white;
            letter-spacing: 1px;
          }
        }
      }

      .action-meta {
        display: flex;
        gap: 16px;

        @media (max-width: 768px) {
          flex-wrap: wrap;
          justify-content: center;
        }

        .meta-item {
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 4px;
          background: rgba(255, 255, 255, 0.4);
          padding: 12px 20px;
          border-radius: 10px;
          backdrop-filter: blur(5px);
          border: 1px solid rgba(255, 255, 255, 0.3);

          .meta-label {
            font-size: 11px;
            color: rgba(255, 255, 255, 0.9);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
          }

          .meta-value {
            font-size: 16px;
            font-weight: 800;
            color: white;
          }
        }
      }

      &.direction-buy {
        background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
      }

      &.direction-sell {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
      }

      &.direction-watch {
        background: linear-gradient(135deg, #d97706 0%, #b45309 100%);
      }

      &.direction-neutral {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
      }
    }

    @keyframes pulse {
      0%,
      100% {
        transform: scale(1);
      }
      50% {
        transform: scale(1.1);
      }
    }

    // 详细指标网格
    .metrics-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 16px;

      .metric-box {
        display: flex;
        align-items: center;
        gap: 16px;
        padding: 20px;
        background: white;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        transition: all 0.3s;
        border: 2px solid #e5e7eb;

        &:hover {
          transform: translateY(-4px);
          box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
          border-color: #3b82f6;
        }

        .metric-box-icon {
          width: 56px;
          height: 56px;
          border-radius: 12px;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 28px;
          flex-shrink: 0;

          &.period-icon {
            background: linear-gradient(135deg, #bfdbfe 0%, #93c5fd 100%);
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.25);
          }

          &.type-icon {
            background: linear-gradient(135deg, #ddd6fe 0%, #c4b5fd 100%);
            box-shadow: 0 4px 12px rgba(139, 92, 246, 0.25);
          }

          &.range-icon {
            background: linear-gradient(135deg, #fde68a 0%, #fcd34d 100%);
            box-shadow: 0 4px 12px rgba(245, 158, 11, 0.25);
          }

          &.ratio-icon {
            background: linear-gradient(135deg, #ddd6fe 0%, #c4b5fd 100%);
            box-shadow: 0 4px 12px rgba(139, 92, 246, 0.25);
          }
        }

        .metric-box-content {
          flex: 1;

          .metric-box-label {
            font-size: 13px;
            color: #4b5563;
            margin-bottom: 6px;
            font-weight: 600;
          }

          .metric-box-value {
            font-size: 18px;
            font-weight: 700;
            color: #111827;
          }
        }
      }
    }
  }

  // 内容区域
  .content-section {
    .summary-box {
      background: linear-gradient(135deg, #fff7ed 0%, #fef9e7 100%);
      border-left: 4px solid #f59e0b;
      padding: 20px;
      border-radius: 8px;
      margin-bottom: 20px;

      .summary-title {
        font-size: 16px;
        font-weight: 600;
        color: #92400e;
        margin-bottom: 12px;
      }

      .summary-content {
        font-size: 15px;
        color: #78350f;
        line-height: 1.8;
      }
    }

    .analysis-content-box {
      background: white;
      padding: 20px;
      border-radius: 8px;
      border: 1px solid #e5e7eb;

      .content-title {
        font-size: 16px;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 12px;
      }

      .content-text {
        font-size: 15px;
        color: #4b5563;
        line-height: 1.8;
        white-space: pre-wrap;
      }
    }
  }

  // 信息卡片
  .info-card {
    margin-bottom: 20px;

    :deep(.el-card__header) {
      background: #f8fafc;
      border-bottom: 2px solid #e5e7eb;
    }
  }

  // 风险框
  .risk-box {
    .risk-item {
      margin-bottom: 15px;

      &:last-child {
        margin-bottom: 0;
      }

      .risk-label {
        font-size: 14px;
        font-weight: 600;
        color: #92400e;
        margin-bottom: 8px;
      }

      .risk-content {
        font-size: 14px;
        color: #78350f;
        line-height: 1.6;
      }
    }
  }

  // 标签和备注
  .tags-box {
    margin-bottom: 15px;

    .tag-item {
      margin-right: 10px;
      margin-bottom: 10px;
    }
  }

  .notes-box {
    background: #f9fafb;
    padding: 20px;
    border-radius: 8px;

    .notes-label {
      font-size: 14px;
      font-weight: 600;
      color: #1f2937;
      margin-bottom: 10px;
    }

    .notes-content {
      font-size: 14px;
      color: #4b5563;
      line-height: 1.6;
    }
  }

  // 状态卡片
  .status-card {
    margin-bottom: 20px;
    background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);

    :deep(.el-card__header) {
      background: rgba(255, 255, 255, 0.9);
      border-bottom: 2px solid #7dd3fc;
    }

    .status-grid {
      margin-bottom: 25px;
    }

    .status-item-wrapper {
      display: flex;
      align-items: center;
      gap: 15px;
      padding: 20px;
      background: white;
      border-radius: 12px;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
      transition: all 0.3s;

      &:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
      }

      .status-icon-wrapper {
        flex-shrink: 0;

        .status-icon {
          width: 50px;
          height: 50px;
          border-radius: 12px;
          display: flex;
          align-items: center;
          justify-content: center;
          svg {
            width: 28px;
            height: 28px;
          }

          &.verify-icon {
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
            color: white;
          }

          &.send-icon {
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
            color: white;
          }

          &.date-icon {
            background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
            color: white;
          }
        }
      }

      .status-content {
        flex: 1;

        .status-label {
          font-size: 13px;
          color: #6b7280;
          margin-bottom: 8px;
          font-weight: 500;
        }

        .status-tags {
          display: flex;
          gap: 8px;
          flex-wrap: wrap;

          :deep(.el-tag) {
            font-weight: 600;
            border-radius: 6px;
          }
        }

        .status-value {
          font-size: 16px;
          font-weight: 600;
          color: #1f2937;
        }
      }
    }

    .footer-info {
      margin-top: 20px;
      padding-top: 20px;
      border-top: 2px solid #7dd3fc;

      .timeline-info {
        display: flex;
        flex-direction: column;
        gap: 15px;

        .timeline-item {
          display: flex;
          align-items: center;
          gap: 15px;
          background: white;
          padding: 12px 16px;
          border-radius: 8px;
          box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);

          .timeline-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
            flex-shrink: 0;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
          }

          .timeline-content {
            flex: 1;
            display: flex;
            align-items: center;
            gap: 10px;
            flex-wrap: wrap;

            .timeline-label {
              font-size: 13px;
              color: #6b7280;
              font-weight: 500;
              min-width: 80px;
            }

            .timeline-value {
              font-size: 14px;
              color: #1f2937;
              font-weight: 600;
            }
          }
        }
      }
    }
  }

  // 免责声明卡片
  .disclaimer-card {
    margin-bottom: 20px;
    background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
    border: 2px solid #f59e0b;

    :deep(.el-card__body) {
      padding: 24px;
    }

    .disclaimer-content {
      display: flex;
      align-items: flex-start;
      gap: 16px;

      .disclaimer-icon {
        font-size: 32px;
        flex-shrink: 0;
        animation: pulse 2s ease-in-out infinite;
      }

      .disclaimer-text {
        font-size: 14px;
        color: #78350f;
        line-height: 1.8;
        font-weight: 500;
        flex: 1;
      }
    }
  }

  @keyframes pulse {
    0%,
    100% {
      opacity: 1;
      transform: scale(1);
    }
    50% {
      opacity: 0.7;
      transform: scale(1.1);
    }
  }

  // 工具类
  .mt-1 {
    margin-top: 5px;
  }

  .mt-3 {
    margin-top: 15px;
  }

  .ml-2 {
    margin-left: 10px;
  }

  .unit {
    font-size: 12px;
    color: #9ca3af;
    margin-left: 4px;
  }
}
</style>
