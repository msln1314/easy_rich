<template>
  <div class="fear-greed-card">
    <div class="card-header">
      <div class="header-title">
        <el-icon class="icon"><Histogram /></el-icon>
        <span>恐慌贪婪</span>
      </div>
      <el-tag :type="getTagType()" size="small" effect="dark">{{
        data?.status || '计算中'
      }}</el-tag>
    </div>

    <div class="card-content" v-loading="loading">
      <div class="gauge-container">
        <div class="gauge">
          <div class="gauge-bg"></div>
          <div class="gauge-fill" :style="gaugeStyle"></div>
          <div class="gauge-pointer" :style="pointerStyle"></div>
        </div>
        <div class="gauge-labels">
          <span class="label fear">恐慌</span>
          <span class="label neutral">中性</span>
          <span class="label greed">贪婪</span>
        </div>
      </div>

      <div class="index-value">
        <span class="value">{{ data?.index?.toFixed(1) || '-' }}</span>
        <span class="status">{{ data?.status || '-' }}</span>
      </div>

      <div class="components">
        <div class="component-item" v-for="(value, key) in data?.components" :key="key">
          <div class="comp-label">{{ getComponentLabel(key) }}</div>
          <div class="comp-bar">
            <div class="comp-fill" :style="{ width: (value || 0) + '%' }"></div>
          </div>
          <div class="comp-value">{{ (value || 0).toFixed(0) }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Histogram } from '@element-plus/icons-vue'
import { getFearGreedIndexApi } from '/@/api/stock/stockIndex'
import type { FearGreedIndex } from '/@/api/stock/stockIndex'

const loading = ref(false)
const data = ref<FearGreedIndex | null>(null)

const gaugeStyle = computed(() => {
  const value = data.value?.index || 50
  return {
    background: `conic-gradient(${getGaugeColor(value)} 0deg ${value * 1.8}deg, transparent ${
      value * 1.8
    }deg 180deg)`
  }
})

const pointerStyle = computed(() => {
  const value = data.value?.index || 50
  return {
    transform: `rotate(${value * 1.8 - 90}deg)`
  }
})

function getGaugeColor(value: number): string {
  if (value >= 80) return '#22c55e'
  if (value >= 60) return '#84cc16'
  if (value >= 40) return '#eab308'
  if (value >= 20) return '#f97316'
  return '#ef4444'
}

function getTagType(): string {
  const value = data.value?.index || 50
  if (value >= 80) return 'success'
  if (value >= 60) return 'success'
  if (value >= 40) return 'warning'
  if (value >= 20) return 'danger'
  return 'danger'
}

function getComponentLabel(key: string): string {
  const labels: Record<string, string> = {
    limit_ratio: '涨跌停',
    north_flow: '北向资金',
    up_down_ratio: '涨跌比',
    volume: '成交量',
    volatility: '波动率'
  }
  return labels[key] || key
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
  border-radius: 12px;
  padding: 14px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  height: 100%;
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
    font-size: 14px;
    font-weight: 600;
    color: #fff;

    .icon {
      color: #8b5cf6;
    }
  }
}

.gauge-container {
  margin-bottom: 10px;

  .gauge {
    position: relative;
    width: 100%;
    height: 8px;
    border-radius: 4px;
    overflow: hidden;

    .gauge-bg {
      position: absolute;
      inset: 0;
      background: linear-gradient(to right, #ef4444, #f97316, #eab308, #84cc16, #22c55e);
    }

    .gauge-fill {
      position: absolute;
      inset: 0;
      opacity: 0.6;
    }

    .gauge-pointer {
      position: absolute;
      top: -3px;
      left: 50%;
      width: 2px;
      height: 14px;
      background: #fff;
      border-radius: 1px;
      transform-origin: bottom center;
      box-shadow: 0 0 4px rgba(255, 255, 255, 0.5);
    }
  }

  .gauge-labels {
    display: flex;
    justify-content: space-between;
    margin-top: 4px;

    .label {
      font-size: 10px;
      color: #64748b;

      &.fear {
        color: #ef4444;
      }

      &.greed {
        color: #22c55e;
      }
    }
  }
}

.index-value {
  text-align: center;
  margin-bottom: 12px;

  .value {
    font-size: 28px;
    font-weight: 700;
    color: #fff;
    font-family: 'DIN Alternate', sans-serif;
  }

  .status {
    display: block;
    font-size: 12px;
    color: #94a3b8;
    margin-top: 2px;
  }
}

.components {
  .component-item {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 6px;

    &:last-child {
      margin-bottom: 0;
    }

    .comp-label {
      width: 50px;
      font-size: 10px;
      color: #64748b;
    }

    .comp-bar {
      flex: 1;
      height: 4px;
      background: rgba(255, 255, 255, 0.1);
      border-radius: 2px;
      overflow: hidden;

      .comp-fill {
        height: 100%;
        background: linear-gradient(to right, #3b82f6, #8b5cf6);
        border-radius: 2px;
        transition: width 0.3s;
      }
    }

    .comp-value {
      width: 24px;
      font-size: 10px;
      color: #94a3b8;
      text-align: right;
    }
  }
}
</style>
