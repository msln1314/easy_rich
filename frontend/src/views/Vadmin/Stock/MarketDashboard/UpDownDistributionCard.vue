<template>
  <div class="up-down-distribution-card">
    <div class="card-header">
      <div class="header-title">
        <el-icon class="icon"><DataAnalysis /></el-icon>
        <span>涨跌分布</span>
      </div>
      <div class="header-stats">
        <span class="stat up">涨 {{ distributionData.upTotal }}</span>
        <span class="stat down">跌 {{ distributionData.downTotal }}</span>
        <span class="stat flat">平 {{ distributionData.flatTotal }}</span>
      </div>
    </div>

    <div class="card-content" v-loading="loading">
      <!-- 涨跌分布柱状图 -->
      <div class="distribution-chart">
        <div class="chart-bars">
          <!-- 涨停 -->
          <div class="bar-group">
            <div class="bar up extreme">
              <div class="bar-fill" :style="{ height: getBarHeight('limitUp') }"></div>
            </div>
            <span class="bar-label">涨停</span>
            <span class="bar-value">{{ distributionData.limitUp || 0 }}</span>
          </div>

          <!-- 大涨 -->
          <div class="bar-group">
            <div class="bar up high">
              <div class="bar-fill" :style="{ height: getBarHeight('highUp') }"></div>
            </div>
            <span class="bar-label">&gt;7%</span>
            <span class="bar-value">{{ distributionData.highUp || 0 }}</span>
          </div>

          <!-- 中涨 -->
          <div class="bar-group">
            <div class="bar up medium">
              <div class="bar-fill" :style="{ height: getBarHeight('mediumUp') }"></div>
            </div>
            <span class="bar-label">3-7%</span>
            <span class="bar-value">{{ distributionData.mediumUp || 0 }}</span>
          </div>

          <!-- 小涨 -->
          <div class="bar-group">
            <div class="bar up low">
              <div class="bar-fill" :style="{ height: getBarHeight('lowUp') }"></div>
            </div>
            <span class="bar-label">0-3%</span>
            <span class="bar-value">{{ distributionData.lowUp || 0 }}</span>
          </div>

          <!-- 平盘 -->
          <div class="bar-group center">
            <div class="bar flat">
              <div class="bar-fill" :style="{ height: getBarHeight('flat') }"></div>
            </div>
            <span class="bar-label">平盘</span>
            <span class="bar-value">{{ distributionData.flat || 0 }}</span>
          </div>

          <!-- 小跌 -->
          <div class="bar-group">
            <div class="bar down low">
              <div class="bar-fill" :style="{ height: getBarHeight('lowDown') }"></div>
            </div>
            <span class="bar-label">0-3%</span>
            <span class="bar-value">{{ distributionData.lowDown || 0 }}</span>
          </div>

          <!-- 中跌 -->
          <div class="bar-group">
            <div class="bar down medium">
              <div class="bar-fill" :style="{ height: getBarHeight('mediumDown') }"></div>
            </div>
            <span class="bar-label">3-7%</span>
            <span class="bar-value">{{ distributionData.mediumDown || 0 }}</span>
          </div>

          <!-- 大跌 -->
          <div class="bar-group">
            <div class="bar down high">
              <div class="bar-fill" :style="{ height: getBarHeight('highDown') }"></div>
            </div>
            <span class="bar-label">&gt;7%</span>
            <span class="bar-value">{{ distributionData.highDown || 0 }}</span>
          </div>

          <!-- 跌停 -->
          <div class="bar-group">
            <div class="bar down extreme">
              <div class="bar-fill" :style="{ height: getBarHeight('limitDown') }"></div>
            </div>
            <span class="bar-label">跌停</span>
            <span class="bar-value">{{ distributionData.limitDown || 0 }}</span>
          </div>
        </div>
      </div>

      <!-- 市场强度指标 -->
      <div class="strength-indicators">
        <div class="indicator">
          <span class="indicator-label">涨跌比</span>
          <span class="indicator-value" :class="strengthClass">
            {{ upDownRatio }}
          </span>
        </div>
        <div class="indicator">
          <span class="indicator-label">涨停/跌停</span>
          <span class="indicator-value" :class="limitClass">
            {{ limitRatio }}
          </span>
        </div>
        <div class="indicator">
          <span class="indicator-label">市场强度</span>
          <span class="indicator-value" :class="strengthClass">
            {{ marketStrength }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { DataAnalysis } from '@element-plus/icons-vue'
import { getUpDownDistributionApi } from '/@/api/stock/stockIndex'
import type { MarketSummary } from '/@/api/stock/stockIndex'

interface DistributionData {
  limitUp: number
  highUp: number
  mediumUp: number
  lowUp: number
  flat: number
  lowDown: number
  mediumDown: number
  highDown: number
  limitDown: number
  upTotal: number
  downTotal: number
  flatTotal: number
}

const props = defineProps<{
  marketSummary?: MarketSummary | null
}>()

const loading = ref(false)
const distributionData = ref<DistributionData>({
  limitUp: 0,
  highUp: 0,
  mediumUp: 0,
  lowUp: 0,
  flat: 0,
  lowDown: 0,
  mediumDown: 0,
  highDown: 0,
  limitDown: 0,
  upTotal: 0,
  downTotal: 0,
  flatTotal: 0
})

// 计算最大值用于柱状图高度
const maxValue = computed(() => {
  const values = [
    distributionData.value.limitUp,
    distributionData.value.highUp,
    distributionData.value.mediumUp,
    distributionData.value.lowUp,
    distributionData.value.flat,
    distributionData.value.lowDown,
    distributionData.value.mediumDown,
    distributionData.value.highDown,
    distributionData.value.limitDown
  ]
  return Math.max(...values, 1)
})

function getBarHeight(key: keyof DistributionData): string {
  const value = distributionData.value[key] || 0
  const percent = (value / maxValue.value) * 100
  return `${Math.max(percent, 2)}%`
}

// 涨跌比
const upDownRatio = computed(() => {
  const up = distributionData.value.upTotal
  const down = distributionData.value.downTotal
  if (down === 0) return up > 0 ? '∞' : '-'
  return (up / down).toFixed(2)
})

// 涨停跌停比
const limitRatio = computed(() => {
  const up = distributionData.value.limitUp
  const down = distributionData.value.limitDown
  if (down === 0) return up > 0 ? '∞' : '-'
  return (up / down).toFixed(2)
})

// 市场强度
const marketStrength = computed(() => {
  const up = distributionData.value.upTotal
  const down = distributionData.value.downTotal
  const total = up + down
  if (total === 0) return '-'
  const strength = (up / total) * 100
  if (strength >= 70) return '强势'
  if (strength >= 55) return '偏强'
  if (strength >= 45) return '均衡'
  if (strength >= 30) return '偏弱'
  return '弱势'
})

const strengthClass = computed(() => {
  const up = distributionData.value.upTotal
  const down = distributionData.value.downTotal
  const total = up + down
  if (total === 0) return ''
  const strength = (up / total) * 100
  if (strength >= 55) return 'up'
  if (strength >= 45) return 'flat'
  return 'down'
})

const limitClass = computed(() => {
  const up = distributionData.value.limitUp
  const down = distributionData.value.limitDown
  if (up > down) return 'up'
  if (up < down) return 'down'
  return 'flat'
})

async function fetchData() {
  loading.value = true
  try {
    const res = await getUpDownDistributionApi()
    if (res.data) {
      distributionData.value = res.data
    }
  } catch (error) {
    console.error('获取涨跌分布数据失败:', error)
    // 使用 marketSummary 作为备用数据
    if (props.marketSummary) {
      distributionData.value = {
        limitUp: props.marketSummary.limit_up_count || 0,
        highUp: 0,
        mediumUp: 0,
        lowUp: props.marketSummary.up_stocks - (props.marketSummary.limit_up_count || 0),
        flat: props.marketSummary.flat_stocks || 0,
        lowDown: 0,
        mediumDown: 0,
        highDown: 0,
        limitDown: props.marketSummary.limit_down_count || 0,
        upTotal: props.marketSummary.up_stocks || 0,
        downTotal: props.marketSummary.down_stocks || 0,
        flatTotal: props.marketSummary.flat_stocks || 0
      }
    }
  } finally {
    loading.value = false
  }
}

// 监听 marketSummary 变化
watch(
  () => props.marketSummary,
  (newVal) => {
    if (newVal && !loading.value) {
      // 如果接口失败，用 marketSummary 补充
      if (!distributionData.value.upTotal) {
        distributionData.value.upTotal = newVal.up_stocks || 0
        distributionData.value.downTotal = newVal.down_stocks || 0
        distributionData.value.flatTotal = newVal.flat_stocks || 0
        distributionData.value.limitUp = newVal.limit_up_count || 0
        distributionData.value.limitDown = newVal.limit_down_count || 0
      }
    }
  }
)

onMounted(() => {
  fetchData()
})

defineExpose({
  refresh: fetchData
})
</script>

<style scoped lang="scss">
.up-down-distribution-card {
  background: linear-gradient(145deg, #151c2c 0%, #1a2234 100%);
  border-radius: 10px;
  padding: 14px;
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;

  .header-title {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 14px;
    font-weight: 600;
    color: #fff;

    .icon {
      color: #06b6d4;
      font-size: 16px;
    }
  }

  .header-stats {
    display: flex;
    gap: 10px;

    .stat {
      font-size: 11px;
      font-weight: 500;

      &.up {
        color: #f43f5e;
      }
      &.down {
        color: #22c55e;
      }
      &.flat {
        color: #eab308;
      }
    }
  }
}

.card-content {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

// 涨跌分布图
.distribution-chart {
  .chart-bars {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    height: 100px;
    padding: 0 4px;
    gap: 2px;
  }

  .bar-group {
    display: flex;
    flex-direction: column;
    align-items: center;
    flex: 1;

    &.center {
      .bar {
        background: rgba(234, 179, 8, 0.1);
        .bar-fill {
          background: linear-gradient(to top, #eab308, #fbbf24);
        }
      }
    }

    .bar {
      width: 100%;
      max-width: 24px;
      height: 70px;
      background: rgba(255, 255, 255, 0.05);
      border-radius: 4px 4px 0 0;
      display: flex;
      align-items: flex-end;
      overflow: hidden;

      .bar-fill {
        width: 100%;
        border-radius: 4px 4px 0 0;
        transition: height 0.3s;
      }

      &.up {
        .bar-fill {
          background: linear-gradient(to top, #f43f5e, #fb7185);
        }
        &.extreme {
          background: rgba(244, 63, 94, 0.15);
        }
        &.high {
          background: rgba(244, 63, 94, 0.1);
        }
        &.medium {
          background: rgba(244, 63, 94, 0.08);
        }
        &.low {
          background: rgba(244, 63, 94, 0.05);
        }
      }

      &.down {
        .bar-fill {
          background: linear-gradient(to top, #22c55e, #4ade80);
        }
        &.extreme {
          background: rgba(34, 197, 94, 0.15);
        }
        &.high {
          background: rgba(34, 197, 94, 0.1);
        }
        &.medium {
          background: rgba(34, 197, 94, 0.08);
        }
        &.low {
          background: rgba(34, 197, 94, 0.05);
        }
      }
    }

    .bar-label {
      font-size: 9px;
      color: #64748b;
      margin-top: 4px;
    }

    .bar-value {
      font-size: 10px;
      font-weight: 600;
      color: #94a3b8;
      margin-top: 2px;
    }
  }
}

// 强度指标
.strength-indicators {
  display: flex;
  justify-content: space-around;
  padding-top: 10px;
  border-top: 1px solid rgba(255, 255, 255, 0.05);

  .indicator {
    text-align: center;

    .indicator-label {
      display: block;
      font-size: 10px;
      color: #64748b;
      margin-bottom: 2px;
    }

    .indicator-value {
      font-size: 14px;
      font-weight: 600;

      &.up {
        color: #f43f5e;
      }
      &.down {
        color: #22c55e;
      }
      &.flat {
        color: #eab308;
      }
    }
  }
}
</style>
