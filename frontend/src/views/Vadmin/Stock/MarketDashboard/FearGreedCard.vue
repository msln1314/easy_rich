<template>
  <div class="fear-greed-card">
    <div class="card-header">
      <div class="header-title">
        <el-icon class="icon"><Histogram /></el-icon>
        <span>恐慌贪婪指数</span>
      </div>
      <span class="update-time">{{ formatTime(lastUpdateTime) }}</span>
    </div>

    <div class="card-content" v-loading="loading">
      <div class="main-section">
        <!-- 左侧：恐慌贪婪指数 -->
        <div class="fear-greed-section">
          <div class="index-circle" :class="getStatusClass">
            <span class="index-value">{{ data?.index?.toFixed(0) || '-' }}</span>
          </div>
          <div class="index-info">
            <div class="status-text" :class="getStatusClass">{{ data?.status || '计算中' }}</div>
            <div class="gauge-mini">
              <div class="gauge-bar" :style="{ width: (data?.index || 50) + '%' }"></div>
            </div>
          </div>
        </div>

        <!-- 右侧：市场统计 -->
        <div class="market-stats-section">
          <div class="stats-row">
            <div class="stat-item up">
              <div class="stat-value">{{ marketSummary?.up_stocks || 0 }}</div>
              <div class="stat-label">上涨</div>
            </div>
            <div class="stat-item flat">
              <div class="stat-value">{{ marketSummary?.flat_stocks || 0 }}</div>
              <div class="stat-label">平盘</div>
            </div>
            <div class="stat-item down">
              <div class="stat-value">{{ marketSummary?.down_stocks || 0 }}</div>
              <div class="stat-label">下跌</div>
            </div>
          </div>
          <div class="ratio-bar">
            <div class="ratio-up" :style="{ width: upPercent + '%' }"></div>
            <div class="ratio-flat" :style="{ width: flatPercent + '%' }"></div>
            <div class="ratio-down" :style="{ width: downPercent + '%' }"></div>
          </div>
          <div class="limit-row">
            <div class="limit-item limit-up">
              <span class="limit-value">{{ marketSummary?.limit_up_count || 0 }}</span>
              <span class="limit-label">涨停</span>
            </div>
            <div class="limit-item limit-down">
              <span class="limit-value">{{ marketSummary?.limit_down_count || 0 }}</span>
              <span class="limit-label">跌停</span>
            </div>
            <div class="limit-item amount">
              <span class="limit-value">{{ formatAmount(marketSummary?.total_amount) }}</span>
              <span class="limit-label">成交额</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 分项指标 -->
      <div class="components-mini">
        <div class="comp-item" v-for="(value, key) in data?.components" :key="key">
          <span class="comp-label">{{ getComponentLabel(key) }}</span>
          <span class="comp-value" :class="value >= 50 ? 'up' : 'down'">{{
            (value || 0).toFixed(0)
          }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Histogram } from '@element-plus/icons-vue'
import { getFearGreedIndexApi } from '/@/api/stock/stockIndex'
import type { FearGreedIndex, MarketSummary } from '/@/api/stock/stockIndex'

const props = defineProps<{
  marketSummary?: MarketSummary | null
  lastUpdateTime?: string
}>()

const loading = ref(false)
const data = ref<FearGreedIndex | null>(null)

const getStatusClass = computed(() => {
  const value = data.value?.index || 50
  if (value >= 80) return 'extreme-greed'
  if (value >= 60) return 'greed'
  if (value >= 40) return 'neutral'
  if (value >= 20) return 'fear'
  return 'extreme-fear'
})

const upPercent = computed(() => {
  if (!props.marketSummary?.total_stocks) return 33.3
  return (props.marketSummary.up_stocks / props.marketSummary.total_stocks) * 100
})

const downPercent = computed(() => {
  if (!props.marketSummary?.total_stocks) return 33.3
  return (props.marketSummary.down_stocks / props.marketSummary.total_stocks) * 100
})

const flatPercent = computed(() => {
  if (!props.marketSummary?.total_stocks) return 33.3
  return (props.marketSummary.flat_stocks / props.marketSummary.total_stocks) * 100
})

function getComponentLabel(key: string): string {
  const labels: Record<string, string> = {
    limit_ratio: '涨跌停',
    north_flow: '北向',
    up_down_ratio: '涨跌比',
    volume: '成交量',
    volatility: '波动率'
  }
  return labels[key] || key
}

function formatTime(time: string | undefined): string {
  if (!time) return ''
  const d = new Date(time)
  return d.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}

function formatAmount(value: number | null | undefined): string {
  if (!value) return '-'
  if (value >= 100000000) return (value / 100000000).toFixed(0) + '亿'
  if (value >= 10000) return (value / 10000).toFixed(0) + '万'
  return value.toFixed(0)
}

async function fetchData() {
  loading.value = true
  try {
    const res = await getFearGreedIndexApi()
    if (res.data) {
      data.value = res.data
    }
  } catch (error) {
    console.error('获取恐慌贪婪指数失败:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchData()
})

defineExpose({
  refresh: fetchData
})
</script>

<style scoped lang="scss">
.fear-greed-card {
  background: linear-gradient(145deg, #151c2c 0%, #1a2234 100%);
  border-radius: 10px;
  padding: 12px;
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;

  .header-title {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 13px;
    font-weight: 600;
    color: #fff;

    .icon {
      color: #8b5cf6;
      font-size: 14px;
    }
  }

  .update-time {
    font-size: 10px;
    color: #64748b;
  }
}

.main-section {
  display: flex;
  gap: 16px;
  margin-bottom: 10px;
}

// 恐慌贪婪指数区域
.fear-greed-section {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
}

.index-circle {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.05);
  border: 2px solid;

  &.extreme-greed {
    border-color: #22c55e;
    .index-value {
      color: #22c55e;
    }
  }
  &.greed {
    border-color: #84cc16;
    .index-value {
      color: #84cc16;
    }
  }
  &.neutral {
    border-color: #eab308;
    .index-value {
      color: #eab308;
    }
  }
  &.fear {
    border-color: #f97316;
    .index-value {
      color: #f97316;
    }
  }
  &.extreme-fear {
    border-color: #ef4444;
    .index-value {
      color: #ef4444;
    }
  }

  .index-value {
    font-size: 18px;
    font-weight: 700;
    font-family: 'DIN Alternate', sans-serif;
  }
}

.index-info {
  .status-text {
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 4px;

    &.extreme-greed {
      color: #22c55e;
    }
    &.greed {
      color: #84cc16;
    }
    &.neutral {
      color: #eab308;
    }
    &.fear {
      color: #f97316;
    }
    &.extreme-fear {
      color: #ef4444;
    }
  }

  .gauge-mini {
    width: 60px;
    height: 3px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 2px;
    overflow: hidden;

    .gauge-bar {
      height: 100%;
      background: linear-gradient(to right, #ef4444, #eab308, #22c55e);
      border-radius: 2px;
      transition: width 0.3s;
    }
  }
}

// 市场统计区域
.market-stats-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding-left: 12px;
  border-left: 1px solid rgba(255, 255, 255, 0.08);
}

.stats-row {
  display: flex;
  justify-content: space-around;

  .stat-item {
    text-align: center;

    .stat-value {
      font-size: 16px;
      font-weight: 700;
      font-family: 'DIN Alternate', sans-serif;
    }

    .stat-label {
      font-size: 9px;
      color: #64748b;
      margin-top: 1px;
    }

    &.up .stat-value {
      color: #f43f5e;
    }
    &.flat .stat-value {
      color: #eab308;
    }
    &.down .stat-value {
      color: #22c55e;
    }
  }
}

.ratio-bar {
  display: flex;
  height: 3px;
  border-radius: 2px;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.05);

  .ratio-up {
    background: #f43f5e;
    transition: width 0.3s;
  }

  .ratio-flat {
    background: #eab308;
    transition: width 0.3s;
  }

  .ratio-down {
    background: #22c55e;
    transition: width 0.3s;
  }
}

.limit-row {
  display: flex;
  justify-content: space-around;
  padding-top: 4px;
  border-top: 1px solid rgba(255, 255, 255, 0.05);

  .limit-item {
    text-align: center;

    .limit-value {
      display: block;
      font-size: 12px;
      font-weight: 600;
      font-family: 'DIN Alternate', sans-serif;
    }

    .limit-label {
      font-size: 8px;
      color: #64748b;
    }

    &.limit-up .limit-value {
      color: #f43f5e;
    }
    &.limit-down .limit-value {
      color: #22c55e;
    }
    &.amount .limit-value {
      color: #06b6d4;
    }
  }
}

.components-mini {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;

  .comp-item {
    display: flex;
    align-items: center;
    gap: 4px;
    padding: 4px 8px;
    background: rgba(0, 0, 0, 0.2);
    border-radius: 4px;

    .comp-label {
      font-size: 12px;
      color: #94a3b8;
    }

    .comp-value {
      font-size: 14px;
      font-weight: 700;

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
