<template>
  <div class="market-cloud-map">
    <!-- 顶部工具栏 -->
    <div class="toolbar">
      <div class="title-section">
        <h2>大盘云图</h2>
        <span class="update-time">{{ formatTime(updateTime) }}</span>
      </div>
      <div class="action-section">
        <el-button :loading="loading" @click="refreshData">
          <el-icon><Refresh /></el-icon>
          刷新
        </el-button>
        <el-button @click="handleScreenshot">
          <el-icon><Camera /></el-icon>
          截图
        </el-button>
      </div>
    </div>

    <!-- 市场切换 -->
    <div class="market-tabs">
      <el-radio-group v-model="currentMarket" @change="handleMarketChange">
        <el-radio-button label="all">A股全图</el-radio-button>
        <el-radio-button label="sh">上证A股</el-radio-button>
        <el-radio-button label="sz">深证A股</el-radio-button>
        <el-radio-button label="kc">科创板</el-radio-button>
        <el-radio-button label="cy">创业板</el-radio-button>
        <el-radio-button label="bj">北交所</el-radio-button>
      </el-radio-group>
    </div>

    <!-- 维度切换 -->
    <div class="metric-tabs">
      <div class="metric-group">
        <span class="label">维度:</span>
        <el-radio-group v-model="currentMetric" size="small" @change="handleMetricChange">
          <el-radio-button label="change">涨跌幅</el-radio-button>
          <el-radio-button label="pe">PE(TTM)</el-radio-button>
          <el-radio-button label="pb">市净率</el-radio-button>
          <el-radio-button label="amount">成交额</el-radio-button>
        </el-radio-group>
      </div>
      <div class="period-group">
        <span class="label">周期:</span>
        <el-radio-group v-model="currentPeriod" size="small" @change="handlePeriodChange">
          <el-radio-button label="today">今日</el-radio-button>
          <el-radio-button label="week">近1周</el-radio-button>
          <el-radio-button label="month">近1月</el-radio-button>
          <el-radio-button label="ytd">年初至今</el-radio-button>
        </el-radio-group>
      </div>
    </div>

    <!-- 云图区域 -->
    <div class="cloud-map-container" ref="chartContainer" v-loading="loading">
      <CloudMapTreemap
        v-if="chartData.length > 0"
        :data="chartData"
        :metric="currentMetric"
        @stock-click="handleStockClick"
      />
      <el-empty v-else description="暂无数据" />
    </div>

    <!-- 分时复盘 -->
    <div class="snapshot-section">
      <span class="label">分时复盘:</span>
      <div class="snapshot-buttons">
        <el-button
          v-for="(info, time) in snapshots"
          :key="time"
          :disabled="!info.available"
          size="small"
          @click="handleSnapshotClick(time as string)"
        >
          {{ time }}
        </el-button>
      </div>
    </div>

    <!-- 市场概览 -->
    <div class="summary-section">
      <div class="summary-item up">
        <span class="value">{{ summary.up }}</span>
        <span class="label">上涨</span>
      </div>
      <div class="summary-item down">
        <span class="value">{{ summary.down }}</span>
        <span class="label">下跌</span>
      </div>
      <div class="summary-item flat">
        <span class="value">{{ summary.flat }}</span>
        <span class="label">平盘</span>
      </div>
      <div class="summary-item limit-up">
        <span class="value">{{ summary.limit_up }}</span>
        <span class="label">涨停</span>
      </div>
      <div class="summary-item limit-down">
        <span class="value">{{ summary.limit_down }}</span>
        <span class="label">跌停</span>
      </div>
    </div>

    <!-- 股票详情弹窗 -->
    <el-dialog v-model="showStockDialog" :title="selectedStock?.name" width="400px">
      <div v-if="selectedStock" class="stock-detail">
        <div class="detail-row">
          <span class="label">代码:</span>
          <span class="value">{{ selectedStock.code }}</span>
        </div>
        <div class="detail-row">
          <span class="label">市场:</span>
          <span class="value">{{ selectedStock.market }}</span>
        </div>
        <div class="detail-row">
          <span class="label">行业:</span>
          <span class="value">{{ selectedStock.industry }}</span>
        </div>
        <div class="detail-row">
          <span class="label">最新价:</span>
          <span class="value">{{ selectedStock.price }}</span>
        </div>
        <div class="detail-row">
          <span class="label">涨跌幅:</span>
          <span class="value" :class="getChangeClass(selectedStock.change)">
            {{ selectedStock.change }}%
          </span>
        </div>
        <div class="detail-row">
          <span class="label">市值:</span>
          <span class="value">{{ formatValue(selectedStock.value) }}亿</span>
        </div>
        <div class="detail-row">
          <span class="label">市盈率:</span>
          <span class="value">{{ selectedStock.pe || '-' }}</span>
        </div>
        <div class="detail-row">
          <span class="label">市净率:</span>
          <span class="value">{{ selectedStock.pb || '-' }}</span>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { Refresh, Camera } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import CloudMapTreemap from './components/CloudMapTreemap.vue'
import {
  getCloudMapDataApi,
  type CloudMapData,
  type CloudMapIndustry,
  type CloudMapStock,
  type CloudMapSummary
} from '/@/api/stock/stockIndex'

const loading = ref(false)
const currentMarket = ref('all')
const currentMetric = ref('change')
const currentPeriod = ref('today')
const updateTime = ref('')

const rawData = ref<CloudMapData | null>(null)
const chartContainer = ref<HTMLElement | null>(null)

const summary = ref<CloudMapSummary>({
  up: 0,
  down: 0,
  flat: 0,
  limit_up: 0,
  limit_down: 0,
  total: 0
})

const snapshots = ref<Record<string, { available: boolean }>>({})

const chartData = computed(() => {
  if (!rawData.value?.industries) return []
  return rawData.value.industries
})

const showStockDialog = ref(false)
const selectedStock = ref<CloudMapStock | null>(null)

async function fetchData() {
  loading.value = true
  try {
    const res = await getCloudMapDataApi(
      currentMarket.value,
      currentMetric.value,
      currentPeriod.value
    )
    if (res.data) {
      rawData.value = res.data
      updateTime.value = res.data.update_time || ''
      if (res.data.summary) {
        summary.value = res.data.summary
      }
      if (res.data.snapshots) {
        snapshots.value = res.data.snapshots
      }
    }
  } catch (error) {
    console.error('获取云图数据失败:', error)
    ElMessage.error('获取云图数据失败')
  } finally {
    loading.value = false
  }
}

function handleMarketChange() {
  fetchData()
}

function handleMetricChange() {
  fetchData()
}

function handlePeriodChange() {
  fetchData()
}

function refreshData() {
  fetchData()
  ElMessage.success('数据已刷新')
}

function handleScreenshot() {
  ElMessage.info('截图功能开发中')
}

function handleSnapshotClick(time: string) {
  ElMessage.info(`加载 ${time} 快照`)
}

function handleStockClick(stock: CloudMapStock) {
  selectedStock.value = stock
  showStockDialog.value = true
}

function formatTime(time: string): string {
  if (!time) return ''
  const d = new Date(time)
  return d.toLocaleString('zh-CN', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

function formatValue(value: number): string {
  if (value >= 10000) {
    return (value / 10000).toFixed(2) + '万'
  }
  return value.toFixed(2)
}

function getChangeClass(change: number): string {
  if (change > 0) return 'up'
  if (change < 0) return 'down'
  return 'flat'
}

let autoRefreshTimer: ReturnType<typeof setInterval> | null = null

onMounted(() => {
  fetchData()
  // 开盘期间自动刷新
  const now = new Date()
  const hour = now.getHours()
  const minute = now.getMinutes()
  const isTradingTime =
    (hour >= 9 && hour < 12) || (hour >= 13 && hour < 15) || (hour === 15 && minute === 0)

  if (isTradingTime) {
    autoRefreshTimer = setInterval(fetchData, 60000) // 每分钟刷新
  }
})

onUnmounted(() => {
  if (autoRefreshTimer) {
    clearInterval(autoRefreshTimer)
  }
})
</script>

<style scoped lang="scss">
.market-cloud-map {
  padding: 16px;
  background: #0f1419;
  min-height: 100vh;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;

  .title-section {
    display: flex;
    align-items: center;
    gap: 12px;

    h2 {
      margin: 0;
      font-size: 20px;
      color: #fff;
    }

    .update-time {
      font-size: 12px;
      color: #64748b;
    }
  }
}

.market-tabs {
  margin-bottom: 12px;

  :deep(.el-radio-button__inner) {
    background: #1a1f2e;
    border-color: #2d3748;
    color: #94a3b8;
  }

  :deep(.el-radio-button__original-radio:checked + .el-radio-button__inner) {
    background: #3b82f6;
    border-color: #3b82f6;
    color: #fff;
  }
}

.metric-tabs {
  display: flex;
  gap: 24px;
  margin-bottom: 16px;
  padding: 12px;
  background: #151c2c;
  border-radius: 8px;

  .metric-group,
  .period-group {
    display: flex;
    align-items: center;
    gap: 8px;

    .label {
      font-size: 13px;
      color: #64748b;
    }
  }

  :deep(.el-radio-button__inner) {
    background: transparent;
    border-color: transparent;
    color: #94a3b8;
    padding: 4px 12px;
  }

  :deep(.el-radio-button__original-radio:checked + .el-radio-button__inner) {
    background: rgba(59, 130, 246, 0.2);
    border-color: transparent;
    color: #3b82f6;
  }
}

.cloud-map-container {
  background: #151c2c;
  border-radius: 12px;
  min-height: 500px;
  margin-bottom: 16px;
  overflow: hidden;
}

.snapshot-section {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
  padding: 12px;
  background: #151c2c;
  border-radius: 8px;

  .label {
    font-size: 13px;
    color: #64748b;
  }

  .snapshot-buttons {
    display: flex;
    gap: 8px;
  }
}

.summary-section {
  display: flex;
  justify-content: center;
  gap: 32px;
  padding: 16px;
  background: #151c2c;
  border-radius: 8px;

  .summary-item {
    text-align: center;

    .value {
      display: block;
      font-size: 24px;
      font-weight: 700;
      font-family: 'DIN Alternate', sans-serif;
    }

    .label {
      font-size: 12px;
      color: #64748b;
    }

    &.up .value {
      color: #f43f5e;
    }

    &.down .value {
      color: #22c55e;
    }

    &.flat .value {
      color: #eab308;
    }

    &.limit-up .value {
      color: #f43f5e;
    }

    &.limit-down .value {
      color: #22c55e;
    }
  }
}

.stock-detail {
  .detail-row {
    display: flex;
    justify-content: space-between;
    padding: 8px 0;
    border-bottom: 1px solid #2d3748;

    &:last-child {
      border-bottom: none;
    }

    .label {
      color: #64748b;
    }

    .value {
      color: #fff;
      font-weight: 500;

      &.up {
        color: #f43f5e;
      }

      &.down {
        color: #22c55e;
      }
    }
  }
}
</style>
