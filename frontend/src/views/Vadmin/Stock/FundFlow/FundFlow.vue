<template>
  <div class="fund-flow-container">
    <el-tabs v-model="activeTab" type="border-card">
      <el-tab-pane label="个股资金流" name="individual">
        <el-card>
          <el-form :model="filterForm" inline>
            <el-form-item label="股票代码">
              <el-input v-model="filterForm.stock" placeholder="输入股票代码" clearable />
            </el-form-item>
            <el-form-item label="市场">
              <el-select v-model="filterForm.market" placeholder="选择市场">
                <el-option label="上海" value="sh" />
                <el-option label="深圳" value="sz" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleSearchIndividual">查询</el-button>
            </el-form-item>
          </el-form>
          <el-table :data="individualData" stripe v-loading="loading" max-height="400">
            <el-table-column prop="date" label="日期" width="120" />
            <el-table-column prop="main_net_inflow" label="主力净流入" width="150">
              <template #default="{ row }">
                <span :class="{ 'positive': row.main_net_inflow > 0, 'negative': row.main_net_inflow < 0 }">
                  {{ formatMoney(row.main_net_inflow) }}
                </span>
              </template>
            </el-table-column>
            <el-table-column prop="main_net_inflow_percent" label="主力净流入占比" width="150">
              <template #default="{ row }">
                {{ row.main_net_inflow_percent?.toFixed(2) }}%
              </template>
            </el-table-column>
            <el-table-column prop="close_price" label="收盘价" width="100" />
            <el-table-column prop="change_pct" label="涨跌幅" width="100">
              <template #default="{ row }">
                <span :class="{ 'positive': row.change_pct > 0, 'negative': row.change_pct < 0 }">
                  {{ row.change_pct?.toFixed(2) }}%
                </span>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-tab-pane>

      <el-tab-pane label="板块资金流" name="sector">
        <el-card>
          <el-form :model="sectorForm" inline>
            <el-form-item label="板块类型">
              <el-select v-model="sectorForm.sectorType">
                <el-option label="行业资金流" value="行业资金流" />
                <el-option label="概念资金流" value="概念资金流" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleSearchSector">查询</el-button>
            </el-form-item>
          </el-form>
          <el-table :data="sectorData" stripe v-loading="loading" max-height="500">
            <el-table-column prop="名称" label="板块名称" width="200" />
            <el-table-column prop="今日涨跌幅" label="今日涨跌幅" width="120">
              <template #default="{ row }">
                <span :class="{ 'positive': row['今日涨跌幅'] > 0, 'negative': row['今日涨跌幅'] < 0 }">
                  {{ row['今日涨跌幅']?.toFixed(2) }}%
                </span>
              </template>
            </el-table-column>
            <el-table-column prop="主力净流入" label="主力净流入" width="150">
              <template #default="{ row }">
                <span :class="{ 'positive': row['主力净流入'] > 0, 'negative': row['主力净流入'] < 0 }">
                  {{ formatMoney(row['主力净流入']) }}
                </span>
              </template>
            </el-table-column>
            <el-table-column prop="超大单净流入" label="超大单净流入" width="150" />
            <el-table-column prop="大单净流入" label="大单净流入" width="150" />
          </el-table>
        </el-card>
      </el-tab-pane>

      <el-tab-pane label="北向资金" name="north">
        <el-card>
          <el-button type="primary" @click="handleSearchNorth">刷新数据</el-button>
          <el-table :data="northData" stripe v-loading="loading" max-height="500" style="margin-top: 20px;">
            <el-table-column prop="日期" label="日期" width="120" />
            <el-table-column prop="沪股通" label="沪股通" width="180">
              <template #default="{ row }">
                <span :class="{ 'positive': row['沪股通'] > 0, 'negative': row['沪股通'] < 0 }">
                  {{ formatMoney(row['沪股通']) }}
                </span>
              </template>
            </el-table-column>
            <el-table-column prop="深股通" label="深股通" width="180">
              <template #default="{ row }">
                <span :class="{ 'positive': row['深股通'] > 0, 'negative': row['深股通'] < 0 }">
                  {{ formatMoney(row['深股通']) }}
                </span>
              </template>
            </el-table-column>
            <el-table-column prop="北向合计" label="北向合计" width="180">
              <template #default="{ row }">
                <span :class="{ 'positive': row['北向合计'] > 0, 'negative': row['北向合计'] < 0 }">
                  {{ formatMoney(row['北向合计']) }}
                </span>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { getIndividualFundFlowApi, getSectorFundFlowApi, getNorthFundFlowApi } from '@/api/stock/fundFlow'

const activeTab = ref('individual')
const loading = ref(false)

const filterForm = reactive({
  stock: '000001',
  market: 'sh'
})

const sectorForm = reactive({
  sectorType: '行业资金流'
})

const individualData = ref<any[]>([])
const sectorData = ref<any[]>([])
const northData = ref<any[]>([])

const handleSearchIndividual = async () => {
  loading.value = true
  try {
    const res = await getIndividualFundFlowApi(filterForm.stock, filterForm.market)
    if (res.code === 0) {
      individualData.value = res.data || []
    }
  } finally {
    loading.value = false
  }
}

const handleSearchSector = async () => {
  loading.value = true
  try {
    const res = await getSectorFundFlowApi(sectorForm.sectorType)
    if (res.code === 0) {
      sectorData.value = res.data || []
    }
  } finally {
    loading.value = false
  }
}

const handleSearchNorth = async () => {
  loading.value = true
  try {
    const res = await getNorthFundFlowApi()
    if (res.code === 0) {
      northData.value = res.data || []
    }
  } finally {
    loading.value = false
  }
}

const formatMoney = (value: number) => {
  if (!value) return '0'
  if (Math.abs(value) >= 100000000) {
    return (value / 100000000).toFixed(2) + '亿'
  }
  if (Math.abs(value) >= 10000) {
    return (value / 10000).toFixed(2) + '万'
  }
  return value.toFixed(2)
}
</script>

<style scoped>
.fund-flow-container {
  padding: 20px;
}
.positive {
  color: #F56C6C;
}
.negative {
  color: #67C23A;
}
</style>
