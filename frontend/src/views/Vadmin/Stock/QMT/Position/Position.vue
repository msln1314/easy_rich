<!-- frontend/src/views/Vadmin/Stock/QMT/Position/Position.vue -->
<template>
  <div class="qmt-position">
    <!-- 资金余额卡片 -->
    <el-row :gutter="20" class="balance-row">
      <el-col :span="6">
        <el-card shadow="hover" class="balance-card">
          <div class="balance-item">
            <div class="label">总资产</div>
            <div class="value">{{ formatMoney(balance.total_asset) }}</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="balance-card">
          <div class="balance-item">
            <div class="label">可用资金</div>
            <div class="value available">{{ formatMoney(balance.available_cash) }}</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="balance-card">
          <div class="balance-item">
            <div class="label">持仓市值</div>
            <div class="value">{{ formatMoney(balance.market_value) }}</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="balance-card">
          <div class="balance-item">
            <div class="label">今日盈亏</div>
            <div class="value" :class="balance.profit_today >= 0 ? 'profit' : 'loss'">
              {{ balance.profit_today >= 0 ? '+' : '' }}{{ formatMoney(balance.profit_today) }}
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 持仓列表 -->
    <el-card class="position-card">
      <template #header>
        <div class="card-header">
          <span>持仓列表</span>
          <el-button type="primary" size="small" @click="refreshData">刷新</el-button>
        </div>
      </template>

      <el-table :data="positions" v-loading="loading" stripe>
        <el-table-column prop="stock_code" label="股票代码" width="100" />
        <el-table-column prop="stock_name" label="股票名称" width="120" />
        <el-table-column prop="quantity" label="持仓数量" width="100">
          <template #default="{ row }">
            {{ row.quantity.toLocaleString() }}
          </template>
        </el-table-column>
        <el-table-column prop="available" label="可用数量" width="100">
          <template #default="{ row }">
            {{ row.available.toLocaleString() }}
          </template>
        </el-table-column>
        <el-table-column prop="cost_price" label="成本价" width="100">
          <template #default="{ row }">
            {{ row.cost_price.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column prop="current_price" label="当前价" width="100">
          <template #default="{ row }">
            {{ row.current_price.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column prop="profit" label="盈亏金额" width="120">
          <template #default="{ row }">
            <span :class="row.profit >= 0 ? 'profit' : 'loss'">
              {{ row.profit >= 0 ? '+' : '' }}{{ row.profit.toFixed(2) }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="profit_rate" label="盈亏比例" width="100">
          <template #default="{ row }">
            <span :class="row.profit_rate >= 0 ? 'profit' : 'loss'">
              {{ row.profit_rate >= 0 ? '+' : '' }}{{ row.profit_rate.toFixed(2) }}%
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="market_value" label="市值" width="120">
          <template #default="{ row }">
            {{ formatMoney(row.market_value) }}
          </template>
        </el-table-column>
      </el-table>

      <!-- 汇总信息 -->
      <div class="position-summary">
        <span>持仓总市值: <b>{{ formatMoney(totalMarketValue) }}</b></span>
        <span>总盈亏: <b :class="totalProfit >= 0 ? 'profit' : 'loss'">{{ totalProfit >= 0 ? '+' : '' }}{{ formatMoney(totalProfit) }}</b></span>
        <span>持仓数量: <b>{{ positions.length }}</b>只</span>
      </div>
    </el-card>

    <!-- 今日成交 -->
    <el-card class="trades-card">
      <template #header>
        <div class="card-header">
          <span>今日成交</span>
        </div>
      </template>

      <el-table :data="trades" stripe size="small">
        <el-table-column prop="trade_id" label="成交ID" width="100" />
        <el-table-column prop="stock_code" label="股票代码" width="100" />
        <el-table-column prop="stock_name" label="股票名称" width="120" />
        <el-table-column prop="direction" label="方向" width="80">
          <template #default="{ row }">
            <el-tag :type="row.direction === 'buy' ? 'danger' : 'success'" size="small">
              {{ row.direction === 'buy' ? '买入' : '卖出' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="price" label="成交价" width="100" />
        <el-table-column prop="quantity" label="成交量" width="100" />
        <el-table-column prop="trade_time" label="成交时间" width="180">
          <template #default="{ row }">
            {{ formatTime(row.trade_time) }}
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getPositionsApi, getBalanceApi, getTodayTradesApi } from '@/api/stock/qmt'

// 状态
const loading = ref(false)
const positions = ref<any[]>([])
const trades = ref<any[]>([])
const balance = reactive({
  total_asset: 0,
  available_cash: 0,
  market_value: 0,
  frozen_cash: 0,
  profit_today: 0,
  profit_total: 0
})

// 计算属性
const totalMarketValue = computed(() => {
  return positions.value.reduce((sum, p) => sum + p.market_value, 0)
})

const totalProfit = computed(() => {
  return positions.value.reduce((sum, p) => sum + p.profit, 0)
})

// 方法
const refreshData = async () => {
  loading.value = true
  try {
    await Promise.all([
      loadPositions(),
      loadBalance(),
      loadTrades()
    ])
  } finally {
    loading.value = false
  }
}

const loadPositions = async () => {
  try {
    const { data } = await getPositionsApi()
    positions.value = data?.positions || []
  } catch (e: any) {
    ElMessage.error(e.message || '获取持仓失败')
  }
}

const loadBalance = async () => {
  try {
    const { data } = await getBalanceApi()
    Object.assign(balance, data || {})
  } catch (e: any) {
    ElMessage.error(e.message || '获取资金余额失败')
  }
}

const loadTrades = async () => {
  try {
    const { data } = await getTodayTradesApi()
    trades.value = data?.trades || []
  } catch (e: any) {
    // 静默处理
  }
}

const formatMoney = (value: number) => {
  if (!value) return '¥0.00'
  return '¥' + value.toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

const formatTime = (time: string) => {
  if (!time) return '-'
  return new Date(time).toLocaleString('zh-CN')
}

// 生命周期
onMounted(() => {
  refreshData()
})
</script>

<style scoped>
.qmt-position {
  padding: 20px;
}

.balance-row {
  margin-bottom: 20px;
}

.balance-card {
  text-align: center;
}

.balance-item .label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 8px;
}

.balance-item .value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}

.balance-item .value.available {
  color: #409eff;
}

.balance-item .value.profit {
  color: #f56c6c;
}

.balance-item .value.loss {
  color: #67c23a;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.position-card,
.trades-card {
  margin-bottom: 20px;
}

.position-summary {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #ebeef5;
  display: flex;
  gap: 40px;
}

.position-summary span {
  color: #606266;
}

.position-summary b {
  font-size: 16px;
}

.profit {
  color: #f56c6c;
}

.loss {
  color: #67c23a;
}
</style>