<template>
  <div class="limit-pool-card">
    <div class="card-header">
      <div class="header-title">
        <el-icon class="icon-up"><Top /></el-icon>
        <el-icon class="icon-down"><Bottom /></el-icon>
        <span>涨跌停监控</span>
      </div>
      <div class="header-tabs">
        <span class="tab" :class="{ active: activeTab === 'zt' }" @click="activeTab = 'zt'">
          涨停 {{ ztCount }}
        </span>
        <span class="tab" :class="{ active: activeTab === 'dt' }" @click="activeTab = 'dt'">
          跌停 {{ dtCount }}
        </span>
      </div>
    </div>

    <div class="card-content" v-loading="loading">
      <div class="continuous-stats" v-if="activeTab === 'zt' && continuousStats">
        <div
          v-for="(count, days) in sortedContinuousStats"
          :key="days"
          class="stat-badge"
          :class="getContinuousClass(Number(days))"
        >
          {{ days }}板: {{ count }}只
        </div>
      </div>

      <div class="stock-list">
        <div v-for="item in displayList" :key="item.stock_code" class="stock-item">
          <div class="stock-info">
            <span class="name">{{ item.stock_name }}</span>
            <span class="code">{{ item.stock_code }}</span>
            <span v-if="item.continuous_days && item.continuous_days > 1" class="continuous-badge">
              {{ item.continuous_days }}连板
            </span>
          </div>
          <div class="stock-data">
            <span class="price">{{ item.close_price?.toFixed(2) }}</span>
            <span class="change" :class="activeTab === 'zt' ? 'up' : 'down'">
              {{ formatChange(item.change_percent) }}
            </span>
            <span class="amount">{{ formatAmount(item.amount) }}</span>
          </div>
        </div>
        <div v-if="displayList.length === 0 && !loading" class="empty-text"> 暂无数据 </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Top, Bottom } from '@element-plus/icons-vue'
import { getLimitPoolApi } from '/@/api/stock/stockIndex'
import type { LimitPoolItem } from '/@/api/stock/stockIndex'

const loading = ref(false)
const activeTab = ref<'zt' | 'dt'>('zt')
const ztPool = ref<LimitPoolItem[]>([])
const dtPool = ref<LimitPoolItem[]>([])
const ztCount = ref(0)
const dtCount = ref(0)
const continuousStats = ref<Record<number, number>>({})

const displayList = computed(() => {
  return activeTab.value === 'zt' ? ztPool.value.slice(0, 10) : dtPool.value.slice(0, 10)
})

const sortedContinuousStats = computed(() => {
  const entries = Object.entries(continuousStats.value)
  return entries.sort((a, b) => Number(b[0]) - Number(a[0]))
})

function formatChange(value: number | null | undefined): string {
  if (value === null || value === undefined) return '-'
  const prefix = value > 0 ? '+' : ''
  return `${prefix}${value.toFixed(2)}%`
}

function formatAmount(value: number | null | undefined): string {
  if (value === null || value === undefined) return '-'
  if (value >= 100000000) return (value / 100000000).toFixed(2) + '亿'
  if (value >= 10000) return (value / 10000).toFixed(0) + '万'
  return value.toFixed(0)
}

function getContinuousClass(days: number): string {
  if (days >= 5) return 'super-hot'
  if (days >= 3) return 'hot'
  return 'normal'
}

async function fetchData() {
  loading.value = true
  try {
    const res = await getLimitPoolApi()
    if (res.data) {
      ztPool.value = res.data.zt_pool || []
      dtPool.value = res.data.dt_pool || []
      ztCount.value = res.data.zt_count || 0
      dtCount.value = res.data.dt_count || 0
      continuousStats.value = res.data.continuous_stats || {}
    }
  } catch (error) {
    console.error('获取涨跌停数据失败:', error)
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
.limit-pool-card {
  background: linear-gradient(145deg, #151c2c 0%, #1a2234 100%);
  border-radius: 12px;
  padding: 16px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  height: 100%;
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
    font-size: 15px;
    font-weight: 600;
    color: #fff;

    .icon-up {
      color: #f43f5e;
    }
    .icon-down {
      color: #22c55e;
    }
  }

  .header-tabs {
    display: flex;
    gap: 8px;

    .tab {
      padding: 4px 12px;
      border-radius: 12px;
      font-size: 12px;
      cursor: pointer;
      background: rgba(255, 255, 255, 0.05);
      color: #94a3b8;
      transition: all 0.2s;

      &:hover {
        background: rgba(255, 255, 255, 0.1);
      }

      &.active {
        background: rgba(244, 63, 94, 0.2);
        color: #f43f5e;
      }
    }
  }
}

.continuous-stats {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 12px;
  padding-bottom: 10px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);

  .stat-badge {
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 500;

    &.normal {
      background: rgba(100, 116, 139, 0.2);
      color: #94a3b8;
    }

    &.hot {
      background: rgba(251, 146, 60, 0.2);
      color: #fb923c;
    }

    &.super-hot {
      background: rgba(244, 63, 94, 0.2);
      color: #f43f5e;
    }
  }
}

.stock-list {
  max-height: 280px;
  overflow-y: auto;

  .stock-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px;
    border-radius: 6px;
    transition: background 0.2s;

    &:hover {
      background: rgba(255, 255, 255, 0.03);
    }

    .stock-info {
      display: flex;
      align-items: center;
      gap: 8px;

      .name {
        font-size: 13px;
        font-weight: 500;
        color: #fff;
        max-width: 80px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      .code {
        font-size: 11px;
        color: #64748b;
      }

      .continuous-badge {
        font-size: 10px;
        padding: 2px 6px;
        border-radius: 4px;
        background: rgba(244, 63, 94, 0.2);
        color: #f43f5e;
      }
    }

    .stock-data {
      display: flex;
      align-items: center;
      gap: 12px;

      .price {
        font-size: 13px;
        color: #fff;
      }

      .change {
        font-size: 12px;
        font-weight: 500;
        min-width: 60px;
        text-align: right;

        &.up {
          color: #f43f5e;
        }
        &.down {
          color: #22c55e;
        }
      }

      .amount {
        font-size: 11px;
        color: #64748b;
        min-width: 50px;
        text-align: right;
      }
    }
  }

  .empty-text {
    text-align: center;
    color: #64748b;
    padding: 40px 0;
    font-size: 13px;
  }
}
</style>
