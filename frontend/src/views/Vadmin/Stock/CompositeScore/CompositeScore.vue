<template>
  <div class="composite-score-container">
    <el-card class="filter-card">
      <el-form :model="filterForm" inline>
        <el-form-item label="股票代码">
          <el-input
            v-model="filterForm.stock"
            placeholder="输入股票代码"
            clearable
            @keyup.enter="handleSearch"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button type="success" @click="handleBatchSearch">批量查询</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-row :gutter="20">
      <el-col :span="24" v-if="currentScore">
        <el-card class="score-card">
          <template #header>
            <div class="card-header">
              <span>{{ currentScore.stock_code }} - 综合评分</span>
              <el-tag :type="getRecommendationType(currentScore.recommendation)" size="large">
                {{ currentScore.recommendation }}
              </el-tag>
            </div>
          </template>
          <el-row :gutter="20">
            <el-col :span="6">
              <div class="score-item">
                <div class="score-value" :style="{ color: getScoreColor(currentScore.composite_score) }">
                  {{ currentScore.composite_score }}
                </div>
                <div class="score-label">综合评分</div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="score-item">
                <div class="score-value">{{ currentScore.value_score }}</div>
                <div class="score-label">价值得分</div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="score-item">
                <div class="score-value">{{ currentScore.growth_score }}</div>
                <div class="score-label">成长得分</div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="score-item">
                <div class="score-value">{{ currentScore.quality_score }}</div>
                <div class="score-label">质量得分</div>
              </div>
            </el-col>
          </el-row>
          <el-row :gutter="20" style="margin-top: 20px;">
            <el-col :span="6">
              <div class="score-item">
                <div class="score-value">{{ currentScore.momentum_score }}</div>
                <div class="score-label">动量得分</div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="score-item">
                <div class="score-value">{{ currentScore.fund_score }}</div>
                <div class="score-label">资金得分</div>
              </div>
            </el-col>
          </el-row>
        </el-card>
      </el-col>
    </el-row>

    <el-card class="table-card" v-if="batchScores.length > 0">
      <template #header>
        <span>批量评分结果</span>
      </template>
      <el-table :data="batchScores" stripe v-loading="loading">
        <el-table-column prop="stock_code" label="股票代码" width="120" />
        <el-table-column prop="composite_score" label="综合评分" width="120">
          <template #default="{ row }">
            <el-tag :type="getScoreTagType(row.composite_score)">
              {{ row.composite_score }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="recommendation" label="建议" width="120">
          <template #default="{ row }">
            <el-tag :type="getRecommendationType(row.recommendation)">
              {{ row.recommendation }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { getCompositeScoreApi, batchCompositeScoreApi } from '@/api/stock/composite'

const loading = ref(false)
const filterForm = reactive({
  stock: ''
})

const currentScore = ref<any>(null)
const batchScores = ref<any[]>([])

const handleSearch = async () => {
  if (!filterForm.stock) {
    ElMessage.warning('请输入股票代码')
    return
  }
  loading.value = true
  try {
    const res = await getCompositeScoreApi(filterForm.stock)
    if (res.code === 0) {
      currentScore.value = res.data
    }
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

const handleBatchSearch = async () => {
  const stocks = '000001,000002,600000,600036'
  loading.value = true
  try {
    const res = await batchCompositeScoreApi(stocks)
    if (res.code === 0) {
      batchScores.value = res.data || []
    }
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

const getScoreColor = (score: number) => {
  if (score >= 80) return '#67C23A'
  if (score >= 70) return '#E6A23C'
  if (score >= 55) return '#909399'
  return '#F56C6C'
}

const getScoreTagType = (score: number) => {
  if (score >= 80) return 'success'
  if (score >= 70) return 'warning'
  if (score >= 55) return 'info'
  return 'danger'
}

const getRecommendationType = (recommendation: string) => {
  switch (recommendation) {
    case '强烈买入':
      return 'success'
    case '买入':
      return 'success'
    case '持有':
      return 'info'
    case '观望':
      return 'warning'
    case '卖出':
      return 'danger'
    default:
      return 'info'
  }
}
</script>

<style scoped>
.composite-score-container {
  padding: 20px;
}
.filter-card {
  margin-bottom: 20px;
}
.score-card {
  margin-bottom: 20px;
}
.score-item {
  text-align: center;
  padding: 20px;
}
.score-value {
  font-size: 36px;
  font-weight: bold;
  color: #409EFF;
}
.score-label {
  font-size: 14px;
  color: #909399;
  margin-top: 10px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
