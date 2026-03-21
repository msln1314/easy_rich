<template>
  <div class="margin-card">
    <div class="card-header">
      <div class="header-title">
        <el-icon class="icon"><Coin /></el-icon>
        <span>融资融券</span>
      </div>
      <el-tag type="info" size="small" effect="dark">每日更新</el-tag>
    </div>

    <div class="card-content" v-loading="loading">
      <div class="margin-summary" v-if="summary">
        <div class="summary-item">
          <div class="label">融资余额</div>
          <div class="value">{{ formatMoney(summary.rzye) }}</div>
          <div class="unit">亿元</div>
        </div>
        <div class="summary-item">
          <div class="label">融券余额</div>
          <div class="value">{{ formatMoney(summary.rqye) }}</div>
          <div class="unit">亿元</div>
        </div>
        <div class="summary-item">
          <div class="label">融资买入</div>
          <div class="value" :class="getFlowClass(summary.rzmre)">
            {{ formatChange(summary.rzmre) }}
          </div>
          <div class="unit">亿元</div>
        </div>
        <div class="summary-item">
          <div class="label">融券卖出</div>
          <div class="value" :class="getFlowClass(-summary.rqmcl)">
            {{ formatChange(summary.rqmcl) }}
          </div>
          <div class="unit">亿元</div>
        </div>
      </div>

      <div class="rank-section">
        <div class="rank-header">
          <span class="title">融资余额 TOP10</span>
        </div>
        <div class="rank-list">
          <div v-for="(item, idx) in rankList" :key="item.stock_code" class="rank-item">
            <div class="rank" :class="getRankClass(idx + 1)">{{ idx + 1 }}</div>
            <div class="stock-info">
              <span class="name">{{ item.stock_name }}</span>
              <span class="code">{{ item.stock_code }}</span>
            </div>
            <div class="margin-value">{{ formatMoney(item.rzye) }}亿</div>
          </div>
          <div v-if="rankList.length === 0 && !loading" class="empty-text"> 暂无融资融券数据 </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Coin } from '@element-plus/icons-vue'
import { getMarginSummaryApi } from '/@/api/stock/stockIndex'

interface MarginSummary {
  rzye?: number
  rqye?: number
  rzmre?: number
  rqmcl?: number
  rzche?: number
  rqchl?: number
}

interface MarginRankItem {
  stock_code: string
  stock_name: string
  rzye: number
  rqye: number
}

const loading = ref(false)
const summary = ref<MarginSummary | null>(null)
const rankList = ref<MarginRankItem[]>([])

function formatMoney(value: number | null | undefined): string {
  if (value === null || value === undefined) return '-'
  if (value >= 100000000) return (value / 100000000).toFixed(2)
  if (value >= 10000) return (value / 10000).toFixed(2)
  return value.toFixed(2)
}

function formatChange(value: number | null | undefined): string {
  if (value === null || value === undefined) return '-'
  const prefix = value > 0 ? '+' : ''
  return prefix + (value / 100000000).toFixed(2)
}

function getFlowClass(value: number | null | undefined): string {
  if (value === null || value === undefined || value === 0) return ''
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
    const res = await getMarginSummaryApi()
    if (res.data) {
      summary.value = res.data.summary || null
      rankList.value = res.data.rank || []
    }
  } catch (error) {
    console.error('获取融资融券数据失败:', error)
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
.margin-card {
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
    gap: 8px;
    font-size: 15px;
    font-weight: 600;
    color: #fff;

    .icon {
      color: #f59e0b;
    }
  }
}

.margin-summary {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);

  .summary-item {
    text-align: center;
    padding: 8px;
    background: rgba(0, 0, 0, 0.2);
    border-radius: 6px;

    .label {
      font-size: 11px;
      color: #64748b;
      margin-bottom: 4px;
    }

    .value {
      font-size: 16px;
      font-weight: 700;
      font-family: 'DIN Alternate', sans-serif;
      color: #fff;

      &.inflow {
        color: #f43f5e;
      }
      &.outflow {
        color: #22c55e;
      }
    }

    .unit {
      font-size: 10px;
      color: #64748b;
      margin-top: 2px;
    }
  }
}

.rank-section {
  .rank-header {
    margin-bottom: 8px;

    .title {
      font-size: 13px;
      color: #94a3b8;
    }
  }

  .rank-list {
    max-height: 200px;
    overflow-y: auto;

    .rank-item {
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

      .margin-value {
        font-size: 12px;
        color: #f59e0b;
        font-weight: 500;
      }
    }

    .empty-text {
      text-align: center;
      color: #64748b;
      padding: 30px 0;
      font-size: 13px;
    }
  }
}
</style>
