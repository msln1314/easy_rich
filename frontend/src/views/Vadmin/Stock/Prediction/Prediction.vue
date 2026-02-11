<template>
  <div class="stock-data-view">
    <!-- 搜索框 -->
    <div class="header-search">
      <div class="search-container">
        <div class="search-icon">
          <Icon icon="ep:search" size="18" />
        </div>
        <el-input
          ref="searchInputRef"
          v-model="searchKeyword"
          class="search-input"
          placeholder="请输入股票代码或名称，如: 平安银行、000001"
          size="large"
          clearable
          @keyup.enter.prevent="handleSearch"
          @clear="clearSearch"
        />
        <el-button type="primary" :loading="loading" @click="handleSearch" class="search-button">
          搜索
        </el-button>
      </div>
    </div>

    <!-- 股票选择弹框 -->
    <el-dialog
      v-model="showStockSelectDialog"
      title="请选择股票"
      width="600px"
      :close-on-click-modal="false"
    >
      <div v-if="stockOptions.length > 0" class="stock-list">
        <div
          v-for="item in stockOptions"
          :key="item.id"
          class="stock-item"
          :class="{ selected: selectedStock === item.stock_code }"
          @click="handleSelectStock(item.stock_code)"
        >
          <div class="stock-name">{{ item.name }}</div>
          <div class="stock-code">{{ item.stock_code }}</div>
        </div>
      </div>
      <div v-else class="empty-text"> 暂无股票 </div>
      <template #footer>
        <el-button @click="showStockSelectDialog = false">取消</el-button>
      </template>
    </el-dialog>

    <!-- 股票信息展示 -->
    <div v-if="stockInfo" class="stock-info-panel">
      <!-- 股票信息汇总模块 -->
      <div class="module-container">
        <StockInfoSummary :stock-info="stockInfo" />
      </div>
      <!-- K线图模块容器 -->
      <div class="module-container chart-container">
        <KLineChart
          :data="chartData"
          :title="`${stockInfo.name || stockInfo.code} K线图`"
          :loading="chartLoading"
          :show-volume="true"
          height="520px"
          @chart-click="handleChartClick"
        />
      </div>
      <!-- 预测面板模块 -->
      <div class="module-container prediction-container">
        <PredictionPanel
          :stock-code="stockInfo.code"
          @prediction-completed="handlePredictionCompleted"
          @prediction-error="handlePredictionError"
        />
      </div>
    </div>

    <!-- 无数据提示 -->
    <EmptyState
      v-if="!loading && !error && shouldShowNoData"
      :description="getEmptyDescription()"
      :show-retry="searchAttempted"
      @retry="handleRetry"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { ElMessage, ElInput, ElButton, ElSelect, ElOption, ElDialog } from 'element-plus'
import { useRoute } from 'vue-router'
import StockInfoSummary from './components/StockInfoSummary.vue'
import KLineChart from './components/KLineChart.vue'
import EmptyState from './components/EmptyState.vue'
import PredictionPanel from './components/PredictionPanel.vue'
import { getStockPageApi, getStockHistoryApi, getStockInfoApi } from '@/api/stock/base'
import { Icon } from '@/components/Icon'

const route = useRoute()
const stockInfo = ref(null)
const loading = ref(false)
const error = ref(null)
const searchAttempted = ref(false)
const retryCount = ref(0)
const chartData = ref([])
const chartLoading = ref(false)
const predictionData = ref(null)

// 搜索相关
const searchKeyword = ref('')
const stockOptions = ref([])
const selectedStock = ref<string | null>(null)
const showStockSelectDialog = ref(false)

// 计算是否显示搜索框 - 始终显示
const showSearch = computed(() => {
  return true
})

const shouldShowNoData = computed(() => {
  return !stockInfo.value
})

const getEmptyDescription = () => {
  if (!searchAttempted.value) {
    return '请输入股票代码或名称开始查询股票数据'
  }
  const stockCode = selectedStock.value || route.params.code || route.query.code
  return stockCode ? `未找到股票代码 "${stockCode}" 的相关数据` : '未找到符合条件的股票数据'
}

// 搜索股票（模糊查询）
const handleSearch = async () => {
  if (!searchKeyword.value) {
    ElMessage.warning('请输入股票代码或名称')
    return
  }

  loading.value = true
  error.value = null
  searchAttempted.value = true
  stockOptions.value = []
  selectedStock.value = null

  // 清除之前的预测数据
  predictionData.value = null
  stockInfo.value = null
  chartData.value = []

  try {
    const res = await getStockPageApi({
      keywords: searchKeyword.value
    })
    stockOptions.value = res.data || []

    if (stockOptions.value.length === 0) {
      ElMessage.warning('未找到匹配的股票')
    } else if (stockOptions.value.length === 1) {
      // 只有一个结果，直接设置为当前股票代码
      const stock = stockOptions.value[0]
      selectedStock.value = stock.stock_code
      searchKeyword.value = stock.stock_code
    } else {
      // 多个结果，弹出选择框
      showStockSelectDialog.value = true
    }
  } catch (err) {
    error.value = err
    ElMessage.error('搜索失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

// 从弹框中选择股票
const handleSelectStock = (stockCode) => {
  selectedStock.value = stockCode
  showStockSelectDialog.value = false
}

// 加载股票数据
const loadStockData = async (stockCode) => {
  if (!stockCode) return

  loading.value = true
  try {
    // 获取K线数据
    await fetchChartData(stockCode)

    // 通过接口查询股票信息
    const res = await getStockInfoApi({ stock_code: stockCode })
    if (res.data) {
      stockInfo.value = res.data.data
      console.log('股票信息:', stockInfo.value)
    }
  } catch (err) {
    ElMessage.error('加载股票数据失败')
  } finally {
    loading.value = false
  }
}

// 获取K线数据
const fetchChartData = async (stockCode) => {
  if (!stockCode) return

  chartLoading.value = true
  try {
    // 获取最近30天的数据
    const endDate = new Date().toISOString().split('T')[0]
    const startDate = new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]

    const response = await getStockHistoryApi({
      stock_code: stockCode,
      start_date: startDate,
      end_date: endDate
    })

    const data = response.data.data || []
    console.log('K线数据:', data)
    console.log('K线数据第一条:', data[0])
    chartData.value = data
  } catch (error) {
    console.error('获取K线数据失败:', error)
    ElMessage.warning('K线数据加载失败，请稍后重试')
    chartData.value = []
  } finally {
    chartLoading.value = false
  }
}

// 处理图表点击事件
const handleChartClick = (params) => {
  console.log('图表点击事件:', params)
}

// 处理预测完成事件
const handlePredictionCompleted = (data) => {
  console.log('预测完成:', data)
  predictionData.value = data
  ElMessage.success(`预测完成！生成了 ${data.predictions.length} 个预测点`)
}

// 处理预测错误事件
const handlePredictionError = (error) => {
  console.error('预测错误:', error)
  predictionData.value = null

  const errorMessage = error.response?.data?.detail || '预测失败，请稍后重试'
  ElMessage.error(errorMessage)
}

const searchInputRef = ref(null)

const handleRetry = () => {
  retryCount.value++
  error.value = null
  handleSearch()
}

// 清空搜索
const clearSearch = () => {
  searchKeyword.value = ''
  stockOptions.value = []
  selectedStock.value = null
  stockInfo.value = null
  chartData.value = []
  predictionData.value = null
  searchAttempted.value = false
}

// 监听路由参数变化（兼容旧版URL）
watch(
  () => [route.params.code, route.query.code],
  ([paramsCode, queryCode]) => {
    const stockCode = paramsCode || queryCode
    if (stockCode) {
      searchKeyword.value = stockCode
      handleSearch().then(() => {
        selectedStock.value = stockCode
      })
    }
  },
  { immediate: true }
)

// 监听 selectedStock 变化，加载股票数据
watch(selectedStock, (newStockCode) => {
  if (newStockCode) {
    loadStockData(newStockCode)
  }
})
</script>

<style scoped>
.stock-data-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0;
  min-height: calc(100vh - 70px);
}

.header-search {
  max-width: 800px;
  margin: 20px auto;
  padding: 0 20px;
  width: 100%;
  display: block;
}

.search-container {
  display: flex;
  align-items: center;
  gap: 12px;
  background: white;
  border-radius: 12px;
  padding: 8px 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.search-container:hover {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.12);
  transform: translateY(-1px);
}

.search-container:focus-within {
  box-shadow: 0 4px 20px rgba(64, 158, 255, 0.15);
  border-color: #409eff;
}

.search-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  color: #909399;
  font-size: 18px;
  flex-shrink: 0;
}

.search-input {
  flex: 1;
}

.search-input :deep(.el-input__wrapper) {
  box-shadow: none !important;
  padding: 8px 0;
  background: transparent !important;
}

.search-input :deep(.el-input__inner) {
  font-size: 15px;
  color: #303133;
}

.search-input :deep(.el-input__inner)::placeholder {
  color: #c0c4cc;
}

.search-button {
  height: 40px;
  padding: 0 28px;
  border-radius: 8px;
  font-weight: 500;
  font-size: 15px;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.search-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
}

.search-button:active {
  transform: translateY(0);
}

.stock-list {
  max-height: 400px;
  overflow-y: auto;
}

.stock-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #e4e7ed;
  margin-bottom: 8px;
}

.stock-item:hover {
  background: #f5f7fa;
  border-color: #409eff;
}

.stock-item.selected {
  background: #ecf5ff;
  border-color: #409eff;
}

.stock-name {
  font-size: 15px;
  font-weight: 500;
  color: #303133;
}

.stock-code {
  font-size: 14px;
  color: #909399;
}

.empty-text {
  text-align: center;
  padding: 40px 0;
  color: #909399;
  font-size: 14px;
}

.stock-selection {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.selection-title {
  font-size: 16px;
  font-weight: 500;
  color: #303133;
  margin-bottom: 15px;
}

.stock-select {
  width: 100%;
}

/* 手机端股票数据视图优化 */
@media (max-width: 768px) {
  .stock-data-view {
    max-width: 100%;
    padding: 0;
  }

  .header-search {
    margin: 15px auto;
    padding: 0 15px;
  }

  .search-container {
    padding: 6px 12px;
    gap: 8px;
  }

  .search-icon {
    font-size: 16px;
  }

  .search-input :deep(.el-input__inner) {
    font-size: 14px;
  }

  .search-button {
    height: 36px;
    padding: 0 20px;
    font-size: 14px;
  }

  .stock-selection {
    margin: 15px;
    padding: 15px;
  }

  .selection-title {
    font-size: 14px;
  }
}

.stock-info-panel {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding: 0;
  margin-top: 20px;
}

/* 手机端股票信息面板优化 */
@media (max-width: 768px) {
  .stock-info-panel {
    gap: 16px;
    margin-top: 12px;
  }
}

@media (max-width: 480px) {
  .stock-info-panel {
    gap: 12px;
    margin-top: 8px;
  }
}

.module-container {
  width: 100%;
  transition: all 0.3s ease;
}

.module-container:hover {
  transform: translateY(-2px);
}

.prediction-container {
  margin-top: 8px;
}

.chart-container {
  margin-top: 8px;
}
</style>
