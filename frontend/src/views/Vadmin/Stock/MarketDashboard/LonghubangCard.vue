<template>
  <div class="longhubang-card">
    <div class="card-header">
      <div class="header-title">
        <el-icon class="icon"><TrendCharts /></el-icon>
        <span>龙虎榜</span>
      </div>
      <el-tag type="warning" size="small" effect="dark" v-if="statistics">
        {{ statistics.trade_date }}
      </el-tag>
    </div>

    <div class="card-content" v-loading="loading">
      <div class="stats-row" v-if="statistics">
        <div class="stat-item">
          <span class="stat-value">{{ statistics.total_count }}</span>
          <span class="stat-label">上榜股票</span>
        </div>
        <div class="stat-item up">
          <span class="stat-value">{{ statistics.up_count }}</span>
          <span class="stat-label">上涨</span>
        </div>
        <div class="stat-item down">
          <span class="stat-value">{{ statistics.down_count }}</span>
          <span class="stat-label">下跌</span>
        </div>
        <div class="stat-item">
          <span class="stat-value">{{ formatNetBuy(statistics.total_net_buy) }}</span>
          <span class="stat-label">净买额(亿)</span>
        </div>
      </div>

      <div class="list-header">
        <span class="title">龙虎榜净买入 TOP5</span>
      </div>
      <div class="stock-list">
        <div
          v-for="(item, idx) in topStocks"
          :key="item.id"
          class="stock-item"
          @click="showDetail(item)"
        >
          <div class="rank" :class="getRankClass(idx + 1)">{{ idx + 1 }}</div>
          <div class="stock-info">
            <span class="name">{{ item.stock_name }}</span>
            <span class="code">{{ item.stock_code }}</span>
          </div>
          <div class="stock-change" :class="getChangeClass(item.change_percent)">
            {{ formatChangePercent(item.change_percent) }}
          </div>
          <div class="net-buy inflow" v-if="item.net_buy_amount && item.net_buy_amount > 0">
            +{{ formatAmount(item.net_buy_amount) }}
          </div>
          <div class="net-buy outflow" v-else>
            {{ formatAmount(item.net_buy_amount) }}
          </div>
        </div>
        <div v-if="topStocks.length === 0 && !loading" class="empty-text"> 暂无龙虎榜数据 </div>
      </div>
    </div>

    <el-dialog
      v-model="detailVisible"
      :title="`${currentStock?.stock_name} 龙虎榜详情`"
      width="700px"
    >
      <div class="detail-content" v-if="detailData">
        <div class="detail-info">
          <div class="info-item">
            <span class="label">股票代码</span>
            <span class="value">{{ detailData.stock_code }}</span>
          </div>
          <div class="info-item">
            <span class="label">收盘价</span>
            <span class="value">{{ detailData.close_price?.toFixed(2) || '-' }}</span>
          </div>
          <div class="info-item">
            <span class="label">涨跌幅</span>
            <span class="value" :class="getChangeClass(detailData.change_percent)">
              {{ formatChangePercent(detailData.change_percent) }}
            </span>
          </div>
          <div class="info-item">
            <span class="label">换手率</span>
            <span class="value">{{ detailData.turnover_rate?.toFixed(2) || '-' }}%</span>
          </div>
          <div class="info-item">
            <span class="label">上榜原因</span>
            <span class="value reason">{{ detailData.reason || '-' }}</span>
          </div>
        </div>

        <div class="detail-section">
          <div class="section-title">买入营业部</div>
          <el-table :data="detailData.buy_details" size="small" max-height="200">
            <el-table-column
              prop="broker_name"
              label="营业部名称"
              min-width="150"
              show-overflow-tooltip
            />
            <el-table-column prop="broker_type" label="类型" width="80" />
            <el-table-column label="买入金额" width="100">
              <template #default="{ row }">
                <span class="inflow">{{ formatAmount(row.buy_amount) }}</span>
              </template>
            </el-table-column>
            <el-table-column label="净买额" width="100">
              <template #default="{ row }">
                <span :class="row.net_amount >= 0 ? 'inflow' : 'outflow'">
                  {{ formatAmount(row.net_amount) }}
                </span>
              </template>
            </el-table-column>
          </el-table>
        </div>

        <div class="detail-section">
          <div class="section-title">卖出营业部</div>
          <el-table :data="detailData.sell_details" size="small" max-height="200">
            <el-table-column
              prop="broker_name"
              label="营业部名称"
              min-width="150"
              show-overflow-tooltip
            />
            <el-table-column prop="broker_type" label="类型" width="80" />
            <el-table-column label="卖出金额" width="100">
              <template #default="{ row }">
                <span class="outflow">{{ formatAmount(row.sell_amount) }}</span>
              </template>
            </el-table-column>
            <el-table-column label="净买额" width="100">
              <template #default="{ row }">
                <span :class="row.net_amount >= 0 ? 'inflow' : 'outflow'">
                  {{ formatAmount(row.net_amount) }}
                </span>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { TrendCharts } from '@element-plus/icons-vue'
import {
  getLonghubangListApi,
  getLonghubangDetailApi,
  getLonghubangStatisticsApi
} from '/@/api/stock/stockIndex'
import type {
  LonghubangItem,
  LonghubangDetailResponse,
  LonghubangStatistics
} from '/@/api/stock/stockIndex'

const loading = ref(false)
const statistics = ref<LonghubangStatistics | null>(null)
const topStocks = ref<LonghubangItem[]>([])
const detailVisible = ref(false)
const currentStock = ref<LonghubangItem | null>(null)
const detailData = ref<LonghubangDetailResponse | null>(null)

function formatAmount(value: number | null | undefined): string {
  if (value === null || value === undefined) return '-'
  const absVal = Math.abs(value)
  if (absVal >= 100000000) return (value / 100000000).toFixed(2) + '亿'
  if (absVal >= 10000) return (value / 10000).toFixed(2) + '万'
  return value.toFixed(2)
}

function formatNetBuy(value: number | null | undefined): string {
  if (value === null || value === undefined) return '-'
  return (value / 100000000).toFixed(2)
}

function formatChangePercent(value: number | null | undefined): string {
  if (value === null || value === undefined) return '-'
  const prefix = value > 0 ? '+' : ''
  return `${prefix}${value.toFixed(2)}%`
}

function getChangeClass(value: number | null | undefined): string {
  if (value === null || value === undefined || value === 0) return ''
  return value > 0 ? 'up' : 'down'
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
    const [statsRes, listRes] = await Promise.all([
      getLonghubangStatisticsApi().catch(() => ({ data: null })),
      getLonghubangListApi({ page: 1, page_size: 5 }).catch(() => ({ data: null }))
    ])

    if (statsRes.data) {
      statistics.value = statsRes.data
    }

    if (listRes.data && listRes.data.items) {
      topStocks.value = listRes.data.items
    }
  } catch (error) {
    console.error('获取龙虎榜数据失败:', error)
  } finally {
    loading.value = false
  }
}

async function showDetail(item: LonghubangItem) {
  currentStock.value = item
  detailVisible.value = true
  try {
    const res = await getLonghubangDetailApi(item.id)
    if (res.data) {
      detailData.value = res.data
    }
  } catch (error) {
    console.error('获取龙虎榜详情失败:', error)
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
.longhubang-card {
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
  margin-bottom: 16px;

  .header-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 16px;
    font-weight: 600;
    color: #fff;

    .icon {
      color: #f59e0b;
    }
  }
}

.card-content {
  min-height: 200px;
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);

  .stat-item {
    text-align: center;

    .stat-value {
      display: block;
      font-size: 18px;
      font-weight: 700;
      color: #fff;
      font-family: 'DIN Alternate', sans-serif;
    }

    .stat-label {
      font-size: 11px;
      color: #64748b;
    }

    &.up .stat-value {
      color: #f43f5e;
    }

    &.down .stat-value {
      color: #22c55e;
    }
  }
}

.list-header {
  margin-bottom: 8px;

  .title {
    font-size: 13px;
    color: #94a3b8;
  }
}

.stock-list {
  .stock-item {
    display: flex;
    align-items: center;
    padding: 8px;
    border-radius: 6px;
    cursor: pointer;
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

    .stock-change {
      font-size: 12px;
      font-weight: 500;
      margin-right: 12px;
      width: 60px;
      text-align: right;

      &.up {
        color: #f43f5e;
      }

      &.down {
        color: #22c55e;
      }
    }

    .net-buy {
      font-size: 12px;
      font-weight: 500;
      width: 70px;
      text-align: right;

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
    padding: 40px 0;
    font-size: 13px;
  }
}

.detail-content {
  .detail-info {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 20px;

    .info-item {
      .label {
        display: block;
        font-size: 12px;
        color: #909399;
        margin-bottom: 4px;
      }

      .value {
        font-size: 14px;
        font-weight: 500;

        &.up {
          color: #f43f5e;
        }

        &.down {
          color: #22c55e;
        }

        &.reason {
          font-size: 12px;
          color: #606266;
        }
      }
    }
  }

  .detail-section {
    margin-bottom: 16px;

    .section-title {
      font-size: 14px;
      font-weight: 600;
      margin-bottom: 8px;
      color: #303133;
    }
  }

  .inflow {
    color: #f43f5e;
  }

  .outflow {
    color: #22c55e;
  }
}
</style>
