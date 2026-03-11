<template>
  <div class="market-dashboard">
    <!-- 顶部指数行情卡片 -->
    <el-row :gutter="16" class="index-row">
      <el-col v-for="index in indexData" :key="index.indexCode" :span="6">
        <el-card class="index-card" :class="getChangeClass(index.changePercent)">
          <div class="index-header">
            <span class="index-name">{{ index.indexName }}</span>
            <span class="index-code">{{ index.indexCode }}</span>
          </div>
          <div class="index-price">
            {{ formatPrice(index.currentPrice) }}
          </div>
          <div class="index-change">
            <span class="change-amount">{{ formatChangeAmount(index.changeAmount) }}</span>
            <span class="change-percent">{{ formatChangePercent(index.changePercent) }}</span>
          </div>
          <div class="index-volume">
            <span>成交额: {{ formatAmount(index.amount) }}</span>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 中间区域 -->
    <el-row :gutter="16" class="middle-row">
      <!-- 市场统计 -->
      <el-col :span="8">
        <el-card class="stats-card">
          <template #header>
            <div class="card-header">
              <span>市场统计</span>
              <span class="update-time">{{ formatTime(marketSummary?.updateTime) }}</span>
            </div>
          </template>
          <div class="stats-content">
            <div class="stats-row">
              <div class="stats-item up">
                <div class="stats-label">上涨</div>
                <div class="stats-value">{{ marketSummary?.upStocks || 0 }}</div>
              </div>
              <div class="stats-item down">
                <div class="stats-label">下跌</div>
                <div class="stats-value">{{ marketSummary?.downStocks || 0 }}</div>
              </div>
              <div class="stats-item flat">
                <div class="stats-label">平盘</div>
                <div class="stats-value">{{ marketSummary?.flatStocks || 0 }}</div>
              </div>
            </div>
            <div class="stats-bar">
              <div class="bar-up" :style="{ width: upPercent + '%' }"></div>
              <div class="bar-flat" :style="{ width: flatPercent + '%' }"></div>
              <div class="bar-down" :style="{ width: downPercent + '%' }"></div>
            </div>
            <div class="limit-stats">
              <div class="limit-item">
                <span class="limit-label">涨停</span>
                <span class="limit-value up">{{ marketSummary?.limitUpCount || 0 }}</span>
              </div>
              <div class="limit-item">
                <span class="limit-label">跌停</span>
                <span class="limit-value down">{{ marketSummary?.limitDownCount || 0 }}</span>
              </div>
            </div>
            <div class="total-stats">
              <div class="total-item">
                <span class="total-label">总成交额</span>
                <span class="total-value">{{ formatAmount(marketSummary?.totalAmount) }}</span>
              </div>
              <div class="total-item">
                <span class="total-label">总成交量</span>
                <span class="total-value">{{ formatVolume(marketSummary?.totalVolume) }}</span>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>

      <!-- 涨幅榜 -->
      <el-col :span="8">
        <el-card class="ranking-card">
          <template #header>
            <div class="card-header">
              <span>涨幅榜 TOP10</span>
              <el-tag type="danger" size="small">实时</el-tag>
            </div>
          </template>
          <el-table :data="changeRanking" stripe size="small" max-height="300">
            <el-table-column prop="rank" label="排名" width="50" align="center">
              <template #default="{ row }">
                <el-tag :type="getRankTagType(row.rank)" size="small">{{ row.rank }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="stockName" label="名称" width="80" show-overflow-tooltip />
            <el-table-column prop="currentPrice" label="现价" width="70" align="right">
              <template #default="{ row }">
                {{ formatPrice(row.currentPrice) }}
              </template>
            </el-table-column>
            <el-table-column prop="changePercent" label="涨幅" align="right">
              <template #default="{ row }">
                <span class="text-up">{{ formatChangePercent(row.changePercent) }}</span>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>

      <!-- 跌幅榜 -->
      <el-col :span="8">
        <el-card class="ranking-card">
          <template #header>
            <div class="card-header">
              <span>跌幅榜 TOP10</span>
              <el-tag type="success" size="small">实时</el-tag>
            </div>
          </template>
          <el-table :data="downRanking" stripe size="small" max-height="300">
            <el-table-column prop="rank" label="排名" width="50" align="center">
              <template #default="{ row }">
                <el-tag :type="getRankTagType(row.rank)" size="small">{{ row.rank }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="stockName" label="名称" width="80" show-overflow-tooltip />
            <el-table-column prop="currentPrice" label="现价" width="70" align="right">
              <template #default="{ row }">
                {{ formatPrice(row.currentPrice) }}
              </template>
            </el-table-column>
            <el-table-column prop="changePercent" label="跌幅" align="right">
              <template #default="{ row }">
                <span class="text-down">{{ formatChangePercent(row.changePercent) }}</span>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>

    <!-- 底部排行 -->
    <el-row :gutter="16" class="bottom-row">
      <!-- 换手率排行 -->
      <el-col :span="12">
        <el-card class="ranking-card">
          <template #header>
            <div class="card-header">
              <span>换手率排行 TOP10</span>
              <el-tag type="warning" size="small">实时</el-tag>
            </div>
          </template>
          <el-table :data="turnoverRanking" stripe size="small" max-height="250">
            <el-table-column prop="rank" label="排名" width="60" align="center">
              <template #default="{ row }">
                <el-tag :type="getRankTagType(row.rank)" size="small">{{ row.rank }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="stockCode" label="代码" width="100" />
            <el-table-column prop="stockName" label="名称" width="100" show-overflow-tooltip />
            <el-table-column prop="currentPrice" label="现价" width="80" align="right">
              <template #default="{ row }">
                {{ formatPrice(row.currentPrice) }}
              </template>
            </el-table-column>
            <el-table-column prop="turnoverRate" label="换手率" width="90" align="right">
              <template #default="{ row }">
                {{ row.turnoverRate?.toFixed(2) || '-' }}%
              </template>
            </el-table-column>
            <el-table-column prop="changePercent" label="涨跌幅" align="right">
              <template #default="{ row }">
                <span :class="getChangeClass(row.changePercent)">{{ formatChangePercent(row.changePercent) }}</span>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>

      <!-- 成交额排行 -->
      <el-col :span="12">
        <el-card class="ranking-card">
          <template #header>
            <div class="card-header">
              <span>成交额排行 TOP10</span>
              <el-tag type="info" size="small">实时</el-tag>
            </div>
          </template>
          <el-table :data="amountRanking" stripe size="small" max-height="250">
            <el-table-column prop="rank" label="排名" width="60" align="center">
              <template #default="{ row }">
                <el-tag :type="getRankTagType(row.rank)" size="small">{{ row.rank }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="stockCode" label="代码" width="100" />
            <el-table-column prop="stockName" label="名称" width="100" show-overflow-tooltip />
            <el-table-column prop="currentPrice" label="现价" width="80" align="right">
              <template #default="{ row }">
                {{ formatPrice(row.currentPrice) }}
              </template>
            </el-table-column>
            <el-table-column prop="amount" label="成交额" width="100" align="right">
              <template #default="{ row }">
                {{ formatAmount(row.amount) }}
              </template>
            </el-table-column>
            <el-table-column prop="changePercent" label="涨跌幅" align="right">
              <template #default="{ row }">
                <span :class="getChangeClass(row.changePercent)">{{ formatChangePercent(row.changePercent) }}</span>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>

    <!-- 刷新按钮 -->
    <div class="refresh-bar">
      <el-button type="primary" :loading="loading" @click="refreshData">
        <el-icon><Refresh /></el-icon>
        刷新数据
      </el-button>
      <span class="last-update">最后更新: {{ formatTime(lastUpdateTime) }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'
import {
  getIndexQuote,
  getMarketSummary,
  getRealtimeRankings,
  type IndexQuoteItem,
  type MarketSummary,
  type StockRankingItem,
} from '/@/api/stock/stockIndex'

// 数据
const loading = ref(false)
const indexData = ref<IndexQuoteItem[]>([])
const marketSummary = ref<MarketSummary | null>(null)
const changeRanking = ref<StockRankingItem[]>([])
const downRanking = ref<StockRankingItem[]>([])
const turnoverRanking = ref<StockRankingItem[]>([])
const amountRanking = ref<StockRankingItem[]>([])
const lastUpdateTime = ref<string>('')

// 定时刷新
let refreshTimer: ReturnType<typeof setInterval> | null = null

// 计算涨跌比例
const upPercent = computed(() => {
  if (!marketSummary.value?.totalStocks) return 0
  return (marketSummary.value.upStocks / marketSummary.value.totalStocks) * 100
})

const downPercent = computed(() => {
  if (!marketSummary.value?.totalStocks) return 0
  return (marketSummary.value.downStocks / marketSummary.value.totalStocks) * 100
})

const flatPercent = computed(() => {
  if (!marketSummary.value?.totalStocks) return 0
  return (marketSummary.value.flatStocks / marketSummary.value.totalStocks) * 100
})

// 格式化函数
function formatPrice(price: number | null | undefined): string {
  if (price === null || price === undefined) return '-'
  return price.toFixed(2)
}

function formatChangePercent(value: number | null | undefined): string {
  if (value === null || value === undefined) return '-'
  const prefix = value > 0 ? '+' : ''
  return `${prefix}${value.toFixed(2)}%`
}

function formatChangeAmount(value: number | null | undefined): string {
  if (value === null || value === undefined) return '-'
  const prefix = value > 0 ? '+' : ''
  return `${prefix}${value.toFixed(2)}`
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
      second: '2-digit',
    })
  } catch {
    return '-'
  }
}

function getChangeClass(value: number | null | undefined): string {
  if (value === null || value === undefined || value === 0) return ''
  return value > 0 ? 'up' : 'down'
}

function getRankTagType(rank: number): string {
  if (rank === 1) return 'danger'
  if (rank === 2) return 'warning'
  if (rank === 3) return 'success'
  return 'info'
}

// 获取数据
async function fetchData() {
  loading.value = true
  try {
    // 并行请求所有数据
    const [quoteRes, summaryRes, rankingsRes] = await Promise.all([
      getIndexQuote(),
      getMarketSummary(),
      getRealtimeRankings(10),
    ])

    // 处理指数数据
    if (quoteRes.data?.items) {
      indexData.value = quoteRes.data.items
    }

    // 处理市场汇总数据
    if (summaryRes.data) {
      marketSummary.value = summaryRes.data
    }

    // 处理排行数据
    if (rankingsRes.data) {
      const rankings = rankingsRes.data
      // 涨幅榜取前10
      changeRanking.value = rankings.changePercentRanking?.slice(0, 10) || []
      // 跌幅榜取后10并反转（因为后端返回的是涨幅排序）
      const allChange = rankings.changePercentRanking || []
      downRanking.value = allChange.slice(-10).reverse().map((item, idx) => ({
        ...item,
        rank: idx + 1,
      }))
      // 换手率排行
      turnoverRanking.value = rankings.turnoverRanking?.slice(0, 10) || []
      // 成交额排行
      amountRanking.value = rankings.amountRanking?.slice(0, 10) || []
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
  ElMessage.success('数据已刷新')
}

// 初始化
onMounted(() => {
  fetchData()
  // 每60秒自动刷新
  refreshTimer = setInterval(fetchData, 60000)
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
  background-color: #f5f7fa;
  min-height: calc(100vh - 100px);

  .index-row {
    margin-bottom: 16px;
  }

  .index-card {
    text-align: center;
    padding: 12px;

    .index-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;

      .index-name {
        font-size: 16px;
        font-weight: 600;
      }

      .index-code {
        font-size: 12px;
        color: #909399;
      }
    }

    .index-price {
      font-size: 28px;
      font-weight: 700;
      margin: 8px 0;
    }

    .index-change {
      display: flex;
      justify-content: center;
      gap: 16px;
      margin-bottom: 8px;

      .change-amount {
        font-size: 14px;
      }

      .change-percent {
        font-size: 14px;
        font-weight: 600;
      }
    }

    .index-volume {
      font-size: 12px;
      color: #909399;
    }

    &.up {
      .index-price,
      .change-amount,
      .change-percent {
        color: #f56c6c;
      }
    }

    &.down {
      .index-price,
      .change-amount,
      .change-percent {
        color: #67c23a;
      }
    }
  }

  .middle-row,
  .bottom-row {
    margin-bottom: 16px;
  }

  .stats-card {
    height: 100%;

    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;

      .update-time {
        font-size: 12px;
        color: #909399;
      }
    }

    .stats-content {
      .stats-row {
        display: flex;
        justify-content: space-around;
        margin-bottom: 16px;

        .stats-item {
          text-align: center;

          .stats-label {
            font-size: 12px;
            color: #909399;
            margin-bottom: 4px;
          }

          .stats-value {
            font-size: 24px;
            font-weight: 600;
          }

          &.up .stats-value {
            color: #f56c6c;
          }

          &.down .stats-value {
            color: #67c23a;
          }

          &.flat .stats-value {
            color: #909399;
          }
        }
      }

      .stats-bar {
        display: flex;
        height: 8px;
        border-radius: 4px;
        overflow: hidden;
        margin-bottom: 16px;

        .bar-up {
          background-color: #f56c6c;
        }

        .bar-flat {
          background-color: #909399;
        }

        .bar-down {
          background-color: #67c23a;
        }
      }

      .limit-stats {
        display: flex;
        justify-content: space-around;
        margin-bottom: 16px;
        padding: 12px;
        background-color: #f5f7fa;
        border-radius: 4px;

        .limit-item {
          text-align: center;

          .limit-label {
            font-size: 12px;
            color: #909399;
          }

          .limit-value {
            display: block;
            font-size: 20px;
            font-weight: 600;

            &.up {
              color: #f56c6c;
            }

            &.down {
              color: #67c23a;
            }
          }
        }
      }

      .total-stats {
        display: flex;
        justify-content: space-around;

        .total-item {
          text-align: center;

          .total-label {
            font-size: 12px;
            color: #909399;
          }

          .total-value {
            display: block;
            font-size: 16px;
            font-weight: 600;
            color: #409eff;
          }
        }
      }
    }
  }

  .ranking-card {
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
  }

  .text-up {
    color: #f56c6c;
  }

  .text-down {
    color: #67c23a;
  }

  .refresh-bar {
    position: fixed;
    bottom: 20px;
    right: 20px;
    display: flex;
    align-items: center;
    gap: 16px;
    background: white;
    padding: 12px 20px;
    border-radius: 8px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);

    .last-update {
      font-size: 12px;
      color: #909399;
    }
  }
}
</style>