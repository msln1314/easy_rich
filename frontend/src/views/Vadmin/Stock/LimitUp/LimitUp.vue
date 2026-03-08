<template>
  <div class="limit-up-container">
    <el-card class="filter-card">
      <el-form :model="filterForm" inline>
        <el-form-item label="日期">
          <el-date-picker
            v-model="filterForm.date"
            type="date"
            placeholder="选择日期"
            value-format="YYYYMMDD"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleStatistics">查看统计</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-row :gutter="20" v-if="statistics">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-value positive">{{ statistics.limit_up_count }}</div>
          <div class="stat-label">涨停家数</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-value negative">{{ statistics.limit_down_count }}</div>
          <div class="stat-label">跌停家数</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-value warning">{{ statistics.>
          <divstrong_count }}</div">强势涨停 class="stat-label </el-col>
</el-card>
     </div>
              <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-value">{{ statistics.broken_rate }}%</div>
          <div class="stat-label">炸板率</div>
        </el-card>
      </el-col>
    </el-row>

    <el-tabs v-model="activeTab" type="border-card" style="margin-top: 20px;">
      <el-tab-pane label="涨停板" name="zt">
        <el-table :data="ztData" stripe v-loading="loading" max-height="500">
          <el-table-column prop="代码" label="股票代码" width="120" />
          <el-table-column prop="名称" label="股票名称" width="120" />
          <el-table-column prop="涨跌幅" label="涨跌幅" width="100">
            <template #default="{ row }">
              <span class="positive">{{ row['涨跌幅']?.toFixed(2) }}%</span>
            </template>
          </el-table-column>
          <el-table-column prop="首次封板时间" label="首次封板" width="120" />
          <el-table-column prop="最后封板时间" label="最后封板" width="120" />
          <el-table-column prop="封板金额" label="封单金额" width="150">
            <template #default="{ row }">
              {{ formatMoney(row['封板金额']) }}
            </template>
          </el-table-column>
          <el-table-column prop="炸板次数" label="炸板次数" width="100" />
          <el-table-column prop="所属行业" label="所属行业" width="120" />
        </el-table>
      </el-tab-pane>

      <el-tab-pane label="跌停板" name="dt">
        <el-table :data="dtData" stripe v-loading="loading" max-height="500">
          <el-table-column prop="代码" label="股票代码" width="120" />
          <el-table-column prop="名称" label="股票名称" width="120" />
          <el-table-column prop="涨跌幅" label="涨跌幅" width="100">
            <template #default="{ row }">
              <span class="negative">{{ row['涨跌幅']?.toFixed(2) }}%</span>
            </template>
          </el-table-column>
          <el-table-column prop="首次封板时间" label="首次封板" width="120" />
        </el-table>
      </el-tab-pane>

      <el-tab-pane label="强势涨停" name="strong">
        <el-table :data="strongData" stripe v-loading="loading" max-height="500">
          <el-table-column prop="代码" label="股票代码" width="120" />
          <el-table-column prop="名称" label="股票名称" width="120" />
          <el-table-column prop="涨跌幅" label="涨跌幅" width="100">
            <template #default="{ row }">
              <span class="positive">{{ row['涨跌幅']?.toFixed(2) }}%</span>
            </template>
          </el-table-column>
          <el-table-column prop="首次封板时间" label="首次封板" width="120" />
          <el-table-column prop="封板金额" label="封单金额" width="150">
            <template #default="{ row }">
              {{ formatMoney(row['封板金额']) }}
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>

      <el-tab-pane label="炸板股票" name="broken">
        <el-table :data="brokenData" stripe v-loading="loading" max-height="500">
          <el-table-column prop="代码" label="股票代码" width="120" />
          <el-table-column prop="名称" label="股票名称" width="120" />
          <el-table-column prop="涨跌幅" label="涨跌幅" width="100" />
          <el-table-column prop="炸板次数" label="炸板次数" width="100" />
        </el-table>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import {
  getZtPoolApi,
  getZtPoolSubApi,
  getZtPoolStrongApi,
  getZtPoolZbgcApi,
  getLimitUpStatisticsApi
} from '@/api/stock/limitUp'

const activeTab = ref('zt')
const loading = ref(false)

const filterForm = reactive({
  date: ''
})

const statistics = ref<any>(null)
const ztData = ref<any[]>([])
const dtData = ref<any[]>([])
const strongData = ref<any[]>([])
const brokenData = ref<any[]>([])

const loadData = async () => {
  loading.value = true
  try {
    const [ztRes, dtRes, strongRes, brokenRes] = await Promise.all([
      getZtPoolApi(filterForm.date),
      getZtPoolSubApi(filterForm.date),
      getZtPoolStrongApi(filterForm.date),
      getZtPoolZbgcApi(filterForm.date)
    ])
    if (ztRes.code === 0) ztData.value = ztRes.data || []
    if (dtRes.code === 0) dtData.value = dtRes.data || []
    if (strongRes.code === 0) strongData.value = strongRes.data || []
    if (brokenRes.code === 0) brokenData.value = brokenRes.data || []
  } finally {
    loading.value = false
  }
}

const handleStatistics = async () => {
  const res = await getLimitUpStatisticsApi(filterForm.date)
  if (res.code === 0) {
    statistics.value = res.data
  }
  await loadData()
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

onMounted(() => {
  handleStatistics()
})
</script>

<style scoped>
.limit-up-container {
  padding: 20px;
}
.filter-card {
  margin-bottom: 20px;
}
.stat-card {
  text-align: center;
}
.stat-value {
  font-size: 32px;
  font-weight: bold;
}
.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 10px;
}
.positive {
  color: #F56C6C;
}
.negative {
  color: #67C23A;
}
.warning {
  color: #E6A23C;
}
</style>
