<template>
  <div class="factor-selection-container">
    <el-card class="filter-card">
      <el-form :model="filterForm" inline>
        <el-form-item label="股票代码列表">
          <el-input
            v-model="filterForm.stocks"
            type="textarea"
            :rows="3"
            placeholder="输入股票代码,逗号分隔,例如: 000001,000002,600000"
            style="width: 400px;"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleCalculate">计算因子</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card v-if="factorResults.length > 0">
      <template #header>
        <div class="card-header">
          <span>因子计算结果</span>
          <el-button type="primary" size="small" @click="handleExport">导出</el-button>
        </div>
      </template>
      <el-table :data="factorResults" stripe v-loading="loading" max-height="600">
        <el-table-column prop="stock_code" label="股票代码" width="120" />
        <el-table-column prop="value_score" label="价值得分" width="100">
          <template #default="{ row }">
            <el-tag :type="getScoreTagType(row.value_score)">{{ row.value_score?.toFixed(1) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="growth_score" label="成长得分" width="100">
          <template #default="{ row }">
            <el-tag :type="getScoreTagType(row.growth_score)">{{ row.growth_score?.toFixed(1) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="quality_score" label="质量得分" width="100">
          <template #default="{ row }">
            <el-tag :type="getScoreTagType(row.quality_score)">{{ row.quality_score?.toFixed(1) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="momentum_score" label="动量得分" width="100">
          <template #default="{ row }">
            <el-tag :type="getScoreTagType(row.momentum_score)">{{ row.momentum_score?.toFixed(1) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="composite_score" label="综合得分" width="120">
          <template #default="{ row }">
            <el-tag :type="getScoreTagType(row.composite_score)" size="large">
              {{ row.composite_score?.toFixed(1) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120">
          <template #default="{ row }">
            <el-button type="primary" link @click="handleViewDetail(row)">详情</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="detailVisible" title="因子详情" width="600px">
      <el-descriptions v-if="currentDetail" :column="2" border>
        <el-descriptions-item label="股票代码">{{ currentDetail.stock_code }}</el-descriptions-item>
        <el-descriptions-item label="综合得分">
          <el-tag :type="getScoreTagType(currentDetail.composite_score)">
            {{ currentDetail.composite_score?.toFixed(1) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="PE">{{ currentDetail.pe }}</el-descriptions-item>
        <el-descriptions-item label="PB">{{ currentDetail.pb }}</el-descriptions-item>
        <el-descriptions-item label="ROE">{{ currentDetail.roe }}</el-descriptions-item>
        <el-descriptions-item label="营收增长">{{ currentDetail.revenue_growth }}%</el-descriptions-item>
        <el-descriptions-item label="净利润增长">{{ currentDetail.profit_growth }}%</el-descriptions-item>
        <el-descriptions-item label="20日涨幅">{{ currentDetail.change_20d }}%</el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { batchCalculateFactorApi } from '@/api/stock/factor'

const loading = ref(false)
const filterForm = reactive({
  stocks: '000001,000002,600000,600036'
})

const factorResults = ref<any[]>([])
const detailVisible = ref(false)
const currentDetail = ref<any>(null)

const handleCalculate = async () => {
  if (!filterForm.stocks) {
    ElMessage.warning('请输入股票代码')
    return
  }
  loading.value = true
  try {
    const stockList = filterForm.stocks.split(',').map(s => s.trim()).filter(s => s)
    const res = await batchCalculateFactorApi(stockList)
    if (res.code === 0) {
      factorResults.value = (res.data || []).sort((a: any, b: any) => 
        (b.composite_score || 0) - (a.composite_score || 0)
      )
    }
  } finally {
    loading.value = false
  }
}

const handleViewDetail = (row: any) => {
  currentDetail.value = row
  detailVisible.value = true
}

const handleExport = () => {
  ElMessage.info('导出功能开发中')
}

const getScoreTagType = (score: number) => {
  if (!score) return 'info'
  if (score >= 80) return 'success'
  if (score >= 60) return 'warning'
  return 'danger'
}
</script>

<style scoped>
.factor-selection-container {
  padding: 20px;
}
.filter-card {
  margin-bottom: 20px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
