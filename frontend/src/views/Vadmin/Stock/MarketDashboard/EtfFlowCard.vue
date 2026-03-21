<template>
  <div class="etf-flow-card">
    <div class="card-header">
      <div class="header-title">
        <el-icon class="icon"><TrendCharts /></el-icon>
        <span>ETF资金流向</span>
      </div>
      <el-tag type="warning" size="small" effect="dark">实时</el-tag>
    </div>

    <div class="card-content" v-loading="loading">
      <div class="flow-tabs">
        <div class="tab" :class="{ active: activeTab === 'net' }" @click="activeTab = 'net'"
          >净流入</div
        >
        <div
          class="tab"
          :class="{ active: activeTab === 'subscribe' }"
          @click="activeTab = 'subscribe'"
          >申购</div
        >
        <div class="tab" :class="{ active: activeTab === 'redeem' }" @click="activeTab = 'redeem'"
          >赎回</div
        >
      </div>

      <div class="flow-list">
        <div v-for="(item, idx) in currentList" :key="item.etf_code" class="flow-item">
          <div class="rank" :class="getRankClass(idx + 1)">{{ idx + 1 }}</div>
          <div class="etf-info">
            <span class="name">{{ item.etf_name }}</span>
            <span class="code">{{ item.etf_code }}</span>
          </div>
          <div class="flow-value" :class="getFlowClass(item)">
            {{ formatAmount(item) }}
          </div>
        </div>
        <div v-if="currentList.length === 0 && !loading" class="empty-text">暂无数据</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { TrendCharts } from '@element-plus/icons-vue'
import { getETFFlowOverviewApi } from '/@/api/stock/stockIndex'
import type { ETFFlowItem } from '/@/api/stock/stockIndex'

const loading = ref(false)
const activeTab = ref('net')
const netFlowRank = ref<ETFFlowItem[]>([])
const subscribeRank = ref<ETFFlowItem[]>([])
const redeemRank = ref<ETFFlowItem[]>([])

const currentList = computed(() => {
  if (activeTab.value === 'net') return netFlowRank.value.slice(0, 8)
  if (activeTab.value === 'subscribe') return subscribeRank.value.slice(0, 8)
  return redeemRank.value.slice(0, 8)
})

function formatAmount(item: ETFFlowItem): string {
  let value: number | null = null
  if (activeTab.value === 'net') value = item.net_flow
  else if (activeTab.value === 'subscribe') value = item.subscribe_amount
  else value = item.redeem_amount

  if (value === null || value === undefined) return '-'
  const absVal = Math.abs(value)
  if (absVal >= 100000000) return (value / 100000000).toFixed(2) + '亿'
  if (absVal >= 10000) return (value / 10000).toFixed(2) + '万'
  return value.toFixed(2)
}

function getFlowClass(item: ETFFlowItem): string {
  if (activeTab.value === 'redeem') return 'outflow'
  const value = item.net_flow || item.subscribe_amount || 0
  return value > 0 ? 'inflow' : 'outflow'
}

function getRankClass(rank: number): string {
  if (rank === 1) return 'gold'
  if (rank === 2) return 'silver'
  if (rank === 3) return 'bronze'
  return ''
}

async function fetchData() {
  loading.value = true
  try {
    const res = await getETFFlowOverviewApi(10)
    if (res.data) {
      netFlowRank.value = res.data.net_flow_rank || []
      subscribeRank.value = res.data.subscribe_rank || []
      redeemRank.value = res.data.redeem_rank || []
    }
  } catch (error) {
    console.error('获取ETF资金流向失败:', error)
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
.etf-flow-card {
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
      color: #f59e0b;
    }
  }
}

.flow-tabs {
  display: flex;
  gap: 4px;
  margin-bottom: 10px;

  .tab {
    flex: 1;
    text-align: center;
    padding: 6px 0;
    font-size: 12px;
    color: #64748b;
    background: rgba(0, 0, 0, 0.2);
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.2s;

    &:hover {
      color: #94a3b8;
    }

    &.active {
      background: rgba(245, 158, 11, 0.15);
      color: #f59e0b;
    }
  }
}

.flow-list {
  .flow-item {
    display: flex;
    align-items: center;
    padding: 6px 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.03);

    &:last-child {
      border-bottom: none;
    }

    .rank {
      width: 18px;
      height: 18px;
      border-radius: 4px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 11px;
      font-weight: 600;
      background: rgba(255, 255, 255, 0.05);
      color: #64748b;
      margin-right: 8px;

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

    .etf-info {
      flex: 1;
      min-width: 0;

      .name {
        display: block;
        font-size: 12px;
        font-weight: 500;
        color: #fff;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      .code {
        font-size: 10px;
        color: #64748b;
      }
    }

    .flow-value {
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

  .empty-text {
    text-align: center;
    color: #64748b;
    padding: 20px 0;
    font-size: 12px;
  }
}
</style>
