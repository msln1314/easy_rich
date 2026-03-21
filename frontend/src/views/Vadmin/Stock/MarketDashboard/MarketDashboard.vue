<template>
  <div class="market-dashboard">
    <!-- 顶部指数行情卡片 -->
    <div class="index-cards">
      <div
        v-for="index in indexData"
        :key="index.index_code"
        class="index-card"
        :class="getChangeClass(index.change_percent)"
      >
        <div class="index-header">
          <div class="index-title">
            <span class="index-name">{{ index.index_name }}</span>
            <span class="index-code">{{ index.index_code }}</span>
          </div>
          <div class="index-badge" :class="getChangeClass(index.change_percent)">
            {{ getChangeText(index.change_percent) }}
          </div>
        </div>
        <div class="index-price">
          {{ formatPrice(index.close_price) }}
        </div>
        <div class="index-change">
          <span class="change-amount">{{ formatChange(index.change_amount) }}</span>
          <span class="change-percent">{{ formatChangePercent(index.change_percent) }}</span>
        </div>
        <div class="index-volume">
          <div class="volume-item">
            <span class="label">成交额</span>
            <span class="value">{{ formatAmount(index.amount) }}</span>
          </div>
          <div class="volume-item">
            <span class="label">成交量</span>
            <span class="value">{{ formatVolume(index.volume) }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 市场统计概览 -->
    <div class="market-overview">
      <div class="overview-card">
        <div class="overview-header">
          <span class="title">市场统计</span>
          <span class="update-time">{{ formatTime(lastUpdateTime) }}</span>
        </div>
        <div class="overview-content">
          <div class="stats-grid">
            <div class="stat-item up">
              <div class="stat-icon">
                <el-icon><CaretTop /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ marketSummary ? marketSummary.up_stocks : 0 }}</div>
                <div class="stat-label">上涨家数</div>
              </div>
            </div>
            <div class="stat-item down">
              <div class="stat-icon">
                <el-icon><CaretBottom /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ marketSummary ? marketSummary.down_stocks : 0 }}</div>
                <div class="stat-label">下跌家数</div>
              </div>
            </div>
            <div class="stat-item flat">
              <div class="stat-icon">
                <el-icon><Minus /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ marketSummary ? marketSummary.flat_stocks : 0 }}</div>
                <div class="stat-label">平盘家数</div>
              </div>
            </div>
          </div>
          <!-- 涨跌比例条 -->
          <div class="stats-ratio">
            <div class="ratio-bar">
              <div class="ratio-up" :style="{ width: upPercentVal + '%' }">
                <span v-if="upPercentVal > 15">{{ upPercentVal.toFixed(1) }}%</span>
              </div>
              <div class="ratio-flat" :style="{ width: flatPercentVal + '%' }"></div>
              <div class="ratio-down" :style="{ width: downPercentVal + '%' }">
                <span v-if="downPercentVal > 15">{{ downPercentVal.toFixed(1) }}%</span>
              </div>
            </div>
            <div class="ratio-legend">
              <span class="legend-item up">上涨 {{ upPercentVal.toFixed(1) }}%</span>
              <span class="legend-item flat">平盘 {{ flatPercentVal.toFixed(1) }}%</span>
              <span class="legend-item down">下跌 {{ downPercentVal.toFixed(1) }}%</span>
            </div>
          </div>
          <!-- 涨跌停统计 -->
          <div class="limit-stats">
            <div class="limit-item limit-up">
              <div class="limit-value">
                <span class="number">{{ marketSummary ? marketSummary.limit_up_count : 0 }}</span>
                <span class="label">涨停</span>
              </div>
            </div>
            <div class="limit-item limit-down">
              <div class="limit-value">
                <span class="number">{{ marketSummary ? marketSummary.limit_down_count : 0 }}</span>
                <span class="label">跌停</span>
              </div>
            </div>
          </div>
          <!-- 成交统计 -->
          <div class="trade-stats">
            <div class="trade-item">
              <span class="label">总成交额</span>
              <span class="value">{{
                formatAmount(marketSummary ? marketSummary.total_amount : null)
              }}</span>
            </div>
            <div class="trade-item">
              <span class="label">总成交量</span>
              <span class="value">{{
                formatVolume(marketSummary ? marketSummary.total_volume : null)
              }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 北向资金 + 市场资金流向 -->
    <div class="fund-flow-section">
      <!-- 北向资金 -->
      <div class="fund-card north-money-card">
        <div class="fund-header">
          <span class="title">北向资金</span>
          <el-tag type="warning" size="small" effect="dark">实时</el-tag>
        </div>
        <div class="north-money-content">
          <div class="total-flow" :class="getFlowClass(northMoney.total_flow)">
            <div class="flow-label">今日净流入</div>
            <div class="flow-value">{{ formatFlowAmount(northMoney.total_flow) }}</div>
            <div class="flow-unit">亿元</div>
          </div>
          <div class="flow-details">
            <div class="flow-item">
              <span class="flow-name">沪港通</span>
              <span class="flow-num" :class="getFlowClass(northMoney.sh_hk_flow)">
                {{ formatFlowNum(northMoney.sh_hk_flow) }}亿
              </span>
            </div>
            <div class="flow-item">
              <span class="flow-name">深港通</span>
              <span class="flow-num" :class="getFlowClass(northMoney.sz_hk_flow)">
                {{ formatFlowNum(northMoney.sz_hk_flow) }}亿
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- 市场资金流向 -->
      <div class="fund-card market-flow-card">
        <div class="fund-header">
          <span class="title">市场资金流向</span>
          <el-tag type="info" size="small" effect="dark">今日</el-tag>
        </div>
        <div class="market-flow-content">
          <div class="main-flow" :class="getFlowClass(marketFundFlow.main_net_inflow)">
            <div class="flow-label">主力净流入</div>
            <div class="flow-value">{{ formatFlowAmount(marketFundFlow.main_net_inflow) }}</div>
            <div class="flow-pct">{{
              marketFundFlow.main_net_inflow_pct
                ? marketFundFlow.main_net_inflow_pct.toFixed(2) + '%'
                : '-'
            }}</div>
          </div>
          <div class="flow-breakdown">
            <div class="breakdown-item">
              <span class="breakdown-label super">超大单</span>
              <span
                class="breakdown-value"
                :class="getFlowClass(marketFundFlow.super_large_net_inflow)"
              >
                {{ formatFlowAmount(marketFundFlow.super_large_net_inflow) }}
              </span>
            </div>
            <div class="breakdown-item">
              <span class="breakdown-label large">大单</span>
              <span class="breakdown-value" :class="getFlowClass(marketFundFlow.large_net_inflow)">
                {{ formatFlowAmount(marketFundFlow.large_net_inflow) }}
              </span>
            </div>
            <div class="breakdown-item">
              <span class="breakdown-label medium">中单</span>
              <span class="breakdown-value" :class="getFlowClass(marketFundFlow.medium_net_inflow)">
                {{ formatFlowAmount(marketFundFlow.medium_net_inflow) }}
              </span>
            </div>
            <div class="breakdown-item">
              <span class="breakdown-label small">小单</span>
              <span class="breakdown-value" :class="getFlowClass(marketFundFlow.small_net_inflow)">
                {{ formatFlowAmount(marketFundFlow.small_net_inflow) }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- 龙虎榜 -->
      <LonghubangCard ref="longhubangRef" />
    </div>

    <!-- 涨跌幅排行 -->
    <div class="ranking-section">
      <div class="ranking-card">
        <div class="ranking-header">
          <div class="title">
            <el-icon class="icon-up"><CaretTop /></el-icon>
            涨幅榜 TOP10
          </div>
          <el-tag type="danger" size="small" effect="dark">实时</el-tag>
        </div>
        <div class="ranking-list">
          <div v-for="(item, idx) in changeRanking" :key="item.stock_code" class="ranking-item">
            <div class="rank" :class="getRankClass(idx + 1)">{{ idx + 1 }}</div>
            <div class="stock-info">
              <span class="name">{{ item.stock_name }}</span>
              <span class="code">{{ item.stock_code }}</span>
            </div>
            <div class="stock-price">{{ formatPrice(item.current_price) }}</div>
            <div class="stock-change up">{{ formatChangePercent(item.change_percent) }}</div>
          </div>
        </div>
      </div>

      <div class="ranking-card">
        <div class="ranking-header">
          <div class="title">
            <el-icon class="icon-down"><CaretBottom /></el-icon>
            跌幅榜 TOP10
          </div>
          <el-tag type="success" size="small" effect="dark">实时</el-tag>
        </div>
        <div class="ranking-list">
          <div v-for="(item, idx) in downRanking" :key="item.stock_code" class="ranking-item">
            <div class="rank" :class="getRankClass(idx + 1)">{{ idx + 1 }}</div>
            <div class="stock-info">
              <span class="name">{{ item.stock_name }}</span>
              <span class="code">{{ item.stock_code }}</span>
            </div>
            <div class="stock-price">{{ formatPrice(item.current_price) }}</div>
            <div class="stock-change down">{{ formatChangePercent(item.change_percent) }}</div>
          </div>
        </div>
      </div>

      <div class="ranking-card">
        <div class="ranking-header">
          <div class="title">
            <el-icon><Refresh /></el-icon>
            换手率 TOP10
          </div>
          <el-tag type="warning" size="small" effect="dark">实时</el-tag>
        </div>
        <div class="ranking-list">
          <div v-for="(item, idx) in turnoverRanking" :key="item.stock_code" class="ranking-item">
            <div class="rank" :class="getRankClass(idx + 1)">{{ idx + 1 }}</div>
            <div class="stock-info">
              <span class="name">{{ item.stock_name }}</span>
              <span class="code">{{ item.stock_code }}</span>
            </div>
            <div class="stock-price">{{ formatPrice(item.current_price) }}</div>
            <div class="stock-turnover">{{ formatTurnover(item.turnover_rate) }}</div>
          </div>
        </div>
      </div>

      <div class="ranking-card">
        <div class="ranking-header">
          <div class="title">
            <el-icon><Money /></el-icon>
            成交额 TOP10
          </div>
          <el-tag type="info" size="small" effect="dark">实时</el-tag>
        </div>
        <div class="ranking-list">
          <div v-for="(item, idx) in amountRanking" :key="item.stock_code" class="ranking-item">
            <div class="rank" :class="getRankClass(idx + 1)">{{ idx + 1 }}</div>
            <div class="stock-info">
              <span class="name">{{ item.stock_name }}</span>
              <span class="code">{{ item.stock_code }}</span>
            </div>
            <div class="stock-price">{{ formatPrice(item.current_price) }}</div>
            <div class="stock-amount">{{ formatAmount(item.amount) }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 市场情绪 + 板块热度 + 涨跌停监控 + 融资融券 -->
    <div class="analysis-section">
      <SentimentCard ref="sentimentRef" />
      <SectorHotCard ref="sectorHotRef" />
      <LimitPoolCard ref="limitPoolRef" />
      <MarginCard ref="marginRef" />
    </div>

    <!-- ETF资金流向 + 全球指数 + 恐慌贪婪指数 -->
    <div class="extended-section">
      <EtfFlowCard ref="etfFlowRef" />
      <GlobalIndexCard ref="globalIndexRef" />
      <FearGreedCard ref="fearGreedRef" />
    </div>

    <!-- 底部操作栏 -->
    <div class="action-bar">
      <div class="data-source">
        <span class="label">数据源:</span>
        <el-tag size="small" effect="plain">{{ dataSource || '加载中' }}</el-tag>
      </div>
      <div class="last-update">
        <el-icon><Clock /></el-icon>
        <span>{{ formatTime(lastUpdateTime) }}</span>
      </div>
      <el-button type="primary" :loading="loading" @click="refreshData">
        <el-icon><Refresh /></el-icon>
        刷新
      </el-button>
      <el-switch v-model="autoRefresh" active-text="自动刷新" @change="toggleAutoRefresh" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Refresh, CaretTop, CaretBottom, Minus, Money, Clock } from '@element-plus/icons-vue'
import {
  getIndexQuotesApi,
  getMarketSummaryApi,
  getRealtimeRankingsApi,
  getNorthMoneyRealtimeApi,
  getMarketFundFlowTodayApi
} from '/@/api/stock/stockIndex'
import type {
  IndexQuoteItem,
  MarketSummary,
  StockRankingItem,
  NorthMoneyRealtime,
  MarketFundFlowToday
} from '/@/api/stock/stockIndex'
import LonghubangCard from './LonghubangCard.vue'
import LimitPoolCard from './LimitPoolCard.vue'
import SectorHotCard from './SectorHotCard.vue'
import SentimentCard from './SentimentCard.vue'
import MarginCard from './MarginCard.vue'
import EtfFlowCard from './EtfFlowCard.vue'
import GlobalIndexCard from './GlobalIndexCard.vue'
import FearGreedCard from './FearGreedCard.vue'

// 数据
const loading = ref(false)
const indexData = ref<IndexQuoteItem[]>([])
const marketSummary = ref<MarketSummary | null>(null)
const changeRanking = ref<StockRankingItem[]>([])
const downRanking = ref<StockRankingItem[]>([])
const turnoverRanking = ref<StockRankingItem[]>([])
const amountRanking = ref<StockRankingItem[]>([])
const lastUpdateTime = ref<string>('')
const dataSource = ref<string>('')
const autoRefresh = ref(true)
const northMoney = ref<NorthMoneyRealtime>({
  sh_hk_flow: 0,
  sz_hk_flow: 0,
  total_flow: 0,
  date: '',
  time: '',
  update_time: ''
})
const marketFundFlow = ref<MarketFundFlowToday>({
  date: '',
  sh_close: null,
  sh_change: null,
  sz_close: null,
  sz_change: null,
  main_net_inflow: 0,
  main_net_inflow_pct: 0,
  super_large_net_inflow: 0,
  large_net_inflow: 0,
  medium_net_inflow: 0,
  small_net_inflow: 0
})

// 定时刷新
let refreshTimer: ReturnType<typeof setInterval> | null = null
const longhubangRef = ref<InstanceType<typeof LonghubangCard> | null>(null)
const limitPoolRef = ref<InstanceType<typeof LimitPoolCard> | null>(null)
const sectorHotRef = ref<InstanceType<typeof SectorHotCard> | null>(null)
const sentimentRef = ref<InstanceType<typeof SentimentCard> | null>(null)
const marginRef = ref<InstanceType<typeof MarginCard> | null>(null)
const etfFlowRef = ref<InstanceType<typeof EtfFlowCard> | null>(null)
const globalIndexRef = ref<InstanceType<typeof GlobalIndexCard> | null>(null)
const fearGreedRef = ref<InstanceType<typeof FearGreedCard> | null>(null)

// 计算涨跌比例
const upPercentVal = computed(() => {
  if (!marketSummary.value || !marketSummary.value.total_stocks) return 0
  return (marketSummary.value.up_stocks / marketSummary.value.total_stocks) * 100
})

const downPercentVal = computed(() => {
  if (!marketSummary.value || !marketSummary.value.total_stocks) return 0
  return (marketSummary.value.down_stocks / marketSummary.value.total_stocks) * 100
})

const flatPercentVal = computed(() => {
  if (!marketSummary.value || !marketSummary.value.total_stocks) return 0
  return (marketSummary.value.flat_stocks / marketSummary.value.total_stocks) * 100
})

// 格式化函数
function formatPrice(price: number | null | undefined): string {
  if (price === null || price === undefined) return '-'
  return price.toFixed(2)
}

function formatChange(value: number | null | undefined): string {
  if (value === null || value === undefined) return '-'
  const prefix = value > 0 ? '+' : ''
  return `${prefix}${value.toFixed(2)}`
}

function formatChangePercent(value: number | null | undefined): string {
  if (value === null || value === undefined) return '-'
  const prefix = value > 0 ? '+' : ''
  return `${prefix}${value.toFixed(2)}%`
}

function formatAmount(amount: number | null | undefined): string {
  if (amount === null || amount === undefined) return '-'
  if (amount >= 100000000) return (amount / 100000000).toFixed(2) + '亿'
  if (amount >= 10000) return (amount / 10000).toFixed(2) + '万'
  return amount.toFixed(2)
}

function formatVolume(volume: number | null | undefined): string {
  if (volume === null || volume === undefined) return '-'
  if (volume >= 100000000) return (volume / 100000000).toFixed(2) + '亿手'
  if (volume >= 10000) return (volume / 10000).toFixed(2) + '万手'
  return volume.toFixed(0) + '手'
}

function formatTime(time: string | undefined): string {
  if (!time) return '-'
  try {
    const date = new Date(time)
    return date.toLocaleString('zh-CN', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    })
  } catch {
    return '-'
  }
}

function formatTurnover(value: number | null | undefined): string {
  if (value === null || value === undefined) return '-'
  return value.toFixed(2) + '%'
}

function getChangeClass(value: number | null | undefined): string {
  if (value === null || value === undefined || value === 0) return ''
  return value > 0 ? 'up' : 'down'
}

function getChangeText(value: number | null | undefined): string {
  if (value === null || value === undefined || value === 0) return '平'
  return value > 0 ? '涨' : '跌'
}

function getRankClass(rank: number): string {
  if (rank === 1) return 'gold'
  if (rank === 2) return 'silver'
  if (rank === 3) return 'bronze'
  return ''
}

function getFlowClass(value: number | null | undefined): string {
  if (value === null || value === undefined || value === 0) return ''
  return value > 0 ? 'inflow' : 'outflow'
}

function formatFlowAmount(value: number | null | undefined): string {
  if (value === null || value === undefined) return '-'
  const absVal = Math.abs(value)
  if (absVal >= 100000000) return (value / 100000000).toFixed(2) + '亿'
  if (absVal >= 10000) return (value / 10000).toFixed(2) + '万'
  return value.toFixed(2)
}

function formatFlowNum(value: number | null | undefined): string {
  if (value === null || value === undefined) return '-'
  const prefix = value > 0 ? '+' : ''
  return prefix + value.toFixed(2)
}

// 获取数据
async function fetchData() {
  loading.value = true
  try {
    // 并行请求所有数据
    const [quoteRes, summaryRes, rankingsRes, northMoneyRes, marketFlowRes] = await Promise.all([
      getIndexQuotesApi(),
      getMarketSummaryApi().catch(() => ({ data: null })),
      getRealtimeRankingsApi(10).catch(() => ({ data: null })),
      getNorthMoneyRealtimeApi().catch(() => ({ data: null })),
      getMarketFundFlowTodayApi().catch(() => ({ data: null }))
    ])

    // 处理指数数据
    if (quoteRes.data && quoteRes.data.items) {
      indexData.value = quoteRes.data.items
      dataSource.value = 'akshare'
    }

    // 处理市场汇总数据
    if (summaryRes.data) {
      marketSummary.value = summaryRes.data
    }

    // 处理排行数据
    if (rankingsRes.data) {
      const rankings = rankingsRes.data
      // 涨幅榜取前10
      changeRanking.value = rankings.change_percent_ranking
        ? rankings.change_percent_ranking.slice(0, 10)
        : []
      // 跌幅榜 - 优先使用 down_ranking，否则从涨幅榜筛选负数
      if (rankings.down_ranking && rankings.down_ranking.length > 0) {
        downRanking.value = rankings.down_ranking.slice(0, 10)
      } else {
        const allChange = rankings.change_percent_ranking || []
        downRanking.value = allChange
          .filter((item: StockRankingItem) => item.change_percent && item.change_percent < 0)
          .sort(
            (a: StockRankingItem, b: StockRankingItem) =>
              (a.change_percent || 0) - (b.change_percent || 0)
          )
          .slice(0, 10)
      }
      // 换手率排行
      turnoverRanking.value = rankings.turnover_ranking
        ? rankings.turnover_ranking.slice(0, 10)
        : []
      // 成交额排行
      amountRanking.value = rankings.amount_ranking ? rankings.amount_ranking.slice(0, 10) : []
    }

    // 处理北向资金数据
    if (northMoneyRes.data) {
      northMoney.value = northMoneyRes.data
    }

    // 处理市场资金流向数据
    if (marketFlowRes.data) {
      marketFundFlow.value = marketFlowRes.data
    }

    lastUpdateTime.value = new Date().toISOString()
  } catch (error) {
    console.error('获取大盘数据失败:', error)
    ElMessage.error('获取大盘数据失败')
  } finally {
    loading.value = false
  }
}

// 刷新数据
async function refreshData() {
  await fetchData()
  if (longhubangRef.value) {
    longhubangRef.value.refresh()
  }
  if (limitPoolRef.value) {
    limitPoolRef.value.refresh()
  }
  if (sectorHotRef.value) {
    sectorHotRef.value.refresh()
  }
  if (sentimentRef.value) {
    sentimentRef.value.refresh()
  }
  if (marginRef.value) {
    marginRef.value.refresh()
  }
  if (etfFlowRef.value) {
    etfFlowRef.value.refresh()
  }
  if (globalIndexRef.value) {
    globalIndexRef.value.refresh()
  }
  if (fearGreedRef.value) {
    fearGreedRef.value.refresh()
  }
  ElMessage.success('数据已刷新')
}

// 切换自动刷新
function toggleAutoRefresh(value: boolean) {
  if (refreshTimer) {
    clearInterval(refreshTimer)
    refreshTimer = null
  }
  if (value) {
    refreshTimer = setInterval(fetchData, 30000) // 30秒刷新
  }
}

// 初始化
onMounted(() => {
  fetchData()
  if (autoRefresh.value) {
    refreshTimer = setInterval(fetchData, 30000)
  }
})

// 清理
onUnmounted(() => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
  }
})
</script>

<style scoped lang="scss">
.market-dashboard {
  padding: 16px;
  background-color: #0a0e17;
  min-height: calc(100vh - 100px);
  color: #e0e6ed;
}

// 指数卡片区域
.index-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin-bottom: 12px;

  @media (max-width: 1200px) {
    grid-template-columns: repeat(2, 1fr);
  }

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
}

.index-card {
  background: linear-gradient(145deg, #151c2c 0%, #1a2234 100%);
  border-radius: 10px;
  padding: 12px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
  }

  &.up {
    .index-price,
    .change-amount,
    .change-percent {
      color: #f43f5e;
    }
    .index-badge {
      background: rgba(244, 63, 94, 0.15);
      color: #f43f5e;
    }
  }

  &.down {
    .index-price,
    .change-amount,
    .change-percent {
      color: #22c55e;
    }
    .index-badge {
      background: rgba(34, 197, 94, 0.15);
      color: #22c55e;
    }
  }
}

.index-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.index-title {
  display: flex;
  flex-direction: column;
  gap: 2px;

  .index-name {
    font-size: 16px;
    font-weight: 600;
    color: #fff;
  }

  .index-code {
    font-size: 12px;
    color: #64748b;
  }
}

.index-badge {
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.index-price {
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 8px;
  font-family: 'DIN Alternate', sans-serif;
}

.index-change {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;

  .change-amount {
    font-size: 14px;
  }

  .change-percent {
    font-size: 14px;
    font-weight: 600;
  }
}

.index-volume {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-top: 1px solid rgba(255, 255, 255, 0.05);

  .volume-item {
    text-align: center;

    .label {
      display: block;
      font-size: 11px;
      color: #64748b;
      margin-bottom: 2px;
    }

    .value {
      font-size: 13px;
      font-weight: 500;
      color: #94a3b8;
    }
  }
}

// 市场统计概览
.market-overview {
  margin-bottom: 12px;
}

.overview-card {
  background: linear-gradient(145deg, #151c2c 0%, #1a2234 100%);
  border-radius: 10px;
  padding: 14px;
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.overview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;

  .title {
    font-size: 16px;
    font-weight: 600;
  }

  .update-time {
    font-size: 12px;
    color: #64748b;
  }
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 20px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 8px;

  .stat-icon {
    width: 40px;
    height: 40px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
  }

  .stat-info {
    .stat-value {
      font-size: 24px;
      font-weight: 700;
      font-family: 'DIN Alternate', sans-serif;
    }

    .stat-label {
      font-size: 12px;
      color: #64748b;
    }
  }

  &.up {
    .stat-icon {
      background: rgba(244, 63, 94, 0.15);
      color: #f43f5e;
    }
    .stat-value {
      color: #f43f5e;
    }
  }

  &.down {
    .stat-icon {
      background: rgba(34, 197, 94, 0.15);
      color: #22c55e;
    }
    .stat-value {
      color: #22c55e;
    }
  }

  &.flat {
    .stat-icon {
      background: rgba(100, 116, 139, 0.15);
      color: #64748b;
    }
    .stat-value {
      color: #94a3b8;
    }
  }
}

.stats-ratio {
  margin-bottom: 20px;

  .ratio-bar {
    display: flex;
    height: 24px;
    border-radius: 4px;
    overflow: hidden;

    > div {
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 12px;
      font-weight: 500;
    }

    .ratio-up {
      background: #f43f5e;
      color: #fff;
    }

    .ratio-flat {
      background: #475569;
    }

    .ratio-down {
      background: #22c55e;
      color: #fff;
    }
  }

  .ratio-legend {
    display: flex;
    justify-content: center;
    gap: 24px;
    margin-top: 8px;

    .legend-item {
      font-size: 12px;
      color: #94a3b8;

      &.up::before {
        content: '';
        display: inline-block;
        width: 8px;
        height: 8px;
        background: #f43f5e;
        border-radius: 2px;
        margin-right: 6px;
      }

      &.flat::before {
        content: '';
        display: inline-block;
        width: 8px;
        height: 8px;
        background: #475569;
        border-radius: 2px;
        margin-right: 6px;
      }

      &.down::before {
        content: '';
        display: inline-block;
        width: 8px;
        height: 8px;
        background: #22c55e;
        border-radius: 2px;
        margin-right: 6px;
      }
    }
  }
}

.limit-stats {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;

  .limit-item {
    flex: 1;
    padding: 16px;
    border-radius: 8px;
    text-align: center;

    &.limit-up {
      background: linear-gradient(135deg, rgba(244, 63, 94, 0.2) 0%, rgba(244, 63, 94, 0.05) 100%);
      border: 1px solid rgba(244, 63, 94, 0.3);
    }

    &.limit-down {
      background: linear-gradient(135deg, rgba(34, 197, 94, 0.2) 0%, rgba(34, 197, 94, 0.05) 100%);
      border: 1px solid rgba(34, 197, 94, 0.3);
    }

    .limit-value {
      .number {
        display: block;
        font-size: 28px;
        font-weight: 700;
        font-family: 'DIN Alternate', sans-serif;
      }

      .label {
        font-size: 12px;
        color: #94a3b8;
      }
    }
  }

  .limit-up .number {
    color: #f43f5e;
  }
  .limit-down .number {
    color: #22c55e;
  }
}

.trade-stats {
  display: flex;
  justify-content: space-around;
  padding-top: 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.05);

  .trade-item {
    text-align: center;

    .label {
      display: block;
      font-size: 12px;
      color: #64748b;
      margin-bottom: 4px;
    }

    .value {
      font-size: 18px;
      font-weight: 600;
      color: #3b82f6;
    }
  }
}

// 资金流向区域
.fund-flow-section {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-bottom: 12px;

  @media (max-width: 1200px) {
    grid-template-columns: repeat(2, 1fr);
  }

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
}

// 分析区域
.analysis-section {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 16px;

  @media (max-width: 1400px) {
    grid-template-columns: repeat(2, 1fr);
  }

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
}

.fund-card {
  background: linear-gradient(145deg, #151c2c 0%, #1a2234 100%);
  border-radius: 10px;
  padding: 12px;
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.fund-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;

  .title {
    font-size: 16px;
    font-weight: 600;
  }
}

// 北向资金卡片
.north-money-content {
  display: flex;
  gap: 20px;
  align-items: center;

  .total-flow {
    flex: 0 0 140px;
    text-align: center;
    padding: 16px;
    background: rgba(0, 0, 0, 0.2);
    border-radius: 8px;

    &.inflow {
      .flow-value {
        color: #f43f5e;
      }
      .flow-unit {
        color: #f43f5e;
      }
    }

    &.outflow {
      .flow-value {
        color: #22c55e;
      }
      .flow-unit {
        color: #22c55e;
      }
    }

    .flow-label {
      font-size: 12px;
      color: #64748b;
      margin-bottom: 4px;
    }

    .flow-value {
      font-size: 28px;
      font-weight: 700;
      font-family: 'DIN Alternate', sans-serif;
    }

    .flow-unit {
      font-size: 12px;
      margin-top: 4px;
    }
  }

  .flow-details {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 12px;

    .flow-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 10px 12px;
      background: rgba(0, 0, 0, 0.15);
      border-radius: 6px;

      .flow-name {
        font-size: 13px;
        color: #94a3b8;
      }

      .flow-num {
        font-size: 14px;
        font-weight: 600;

        &.inflow {
          color: #f43f5e;
        }
        &.outflow {
          color: #22c55e;
        }
      }
    }
  }
}

// 市场资金流向卡片
.market-flow-content {
  display: flex;
  gap: 20px;
  align-items: flex-start;

  .main-flow {
    flex: 0 0 140px;
    text-align: center;
    padding: 16px;
    background: rgba(0, 0, 0, 0.2);
    border-radius: 8px;

    &.inflow {
      .flow-value {
        color: #f43f5e;
      }
      .flow-pct {
        color: #f43f5e;
      }
    }

    &.outflow {
      .flow-value {
        color: #22c55e;
      }
      .flow-pct {
        color: #22c55e;
      }
    }

    .flow-label {
      font-size: 12px;
      color: #64748b;
      margin-bottom: 4px;
    }

    .flow-value {
      font-size: 24px;
      font-weight: 700;
      font-family: 'DIN Alternate', sans-serif;
    }

    .flow-pct {
      font-size: 12px;
      margin-top: 4px;
    }
  }

  .flow-breakdown {
    flex: 1;
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;

    .breakdown-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 8px 12px;
      background: rgba(0, 0, 0, 0.15);
      border-radius: 6px;

      .breakdown-label {
        font-size: 12px;

        &.super {
          color: #f43f5e;
        }
        &.large {
          color: #fb923c;
        }
        &.medium {
          color: #f59e0b;
        }
        &.small {
          color: #94a3b8;
        }
      }

      .breakdown-value {
        font-size: 12px;
        font-weight: 500;

        &.inflow {
          color: #f43f5e;
        }
        &.outflow {
          color: #22c55e;
        }
      }
    }
  }
}

// 排行榜区域
.ranking-section {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin-bottom: 12px;

  @media (max-width: 1400px) {
    grid-template-columns: repeat(2, 1fr);
  }

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
}

// 分析区域
.analysis-section {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin-bottom: 12px;

  @media (max-width: 1400px) {
    grid-template-columns: repeat(2, 1fr);
  }

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
}

// 扩展区域
.extended-section {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-bottom: 16px;

  @media (max-width: 1200px) {
    grid-template-columns: repeat(2, 1fr);
  }

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
}

.ranking-card {
  background: linear-gradient(145deg, #151c2c 0%, #1a2234 100%);
  border-radius: 12px;
  padding: 14px;
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.ranking-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;

  .title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 14px;
    font-weight: 600;

    .icon-up {
      color: #f43f5e;
    }
    .icon-down {
      color: #22c55e;
    }
  }
}

.ranking-list {
  .ranking-item {
    display: flex;
    align-items: center;
    padding: 8px;
    border-radius: 6px;
    transition: background 0.2s;

    &:hover {
      background: rgba(255, 255, 255, 0.03);
    }

    .rank {
      width: 22px;
      height: 22px;
      border-radius: 4px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 12px;
      font-weight: 600;
      background: rgba(255, 255, 255, 0.05);
      color: #94a3b8;
      margin-right: 10px;

      &.gold {
        background: linear-gradient(135deg, #ffd700 0%, #ffaa00 100%);
        color: #000;
      }

      &.silver {
        background: linear-gradient(135deg, #c0c0c0 0%, #a0a0a0 100%);
        color: #000;
      }

      &.bronze {
        background: linear-gradient(135deg, #cd7f32 0%, #b87333 100%);
        color: #fff;
      }
    }

    .stock-info {
      flex: 1;
      min-width: 0;

      .name {
        display: block;
        font-size: 13px;
        font-weight: 500;
        color: #fff;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      .code {
        font-size: 11px;
        color: #64748b;
      }
    }

    .stock-price {
      font-size: 13px;
      color: #fff;
      margin-right: 12px;
    }

    .stock-change {
      font-size: 12px;
      font-weight: 500;

      &.up {
        color: #f43f5e;
      }
      &.down {
        color: #22c55e;
      }
    }

    .stock-turnover {
      font-size: 12px;
      color: #f59e0b;
      font-weight: 500;
    }

    .stock-amount {
      font-size: 12px;
      color: #3b82f6;
      font-weight: 500;
    }
  }
}

// 底部操作栏
.action-bar {
  position: fixed;
  bottom: 20px;
  right: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  background: linear-gradient(145deg, #1a2234 0%, #151c2c 100%);
  padding: 12px 20px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);

  .data-source {
    display: flex;
    align-items: center;
    gap: 6px;

    .label {
      font-size: 12px;
      color: #64748b;
    }
  }

  .last-update {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 12px;
    color: #94a3b8;
  }
}
</style>
