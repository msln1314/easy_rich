<template>
  <div class="prediction-panel">
    <!-- 预测控制面板 -->
    <div class="prediction-controls">
      <div class="control-group">
        <label class="control-label">预测天数：</label>
        <select v-model="predictionDays" class="prediction-select" :disabled="predicting">
          <option value="1">1天</option>
          <option value="3">3天</option>
          <option value="7">7天</option>
          <option value="14">14天</option>
          <option value="30">30天</option>
        </select>
      </div>

      <div class="control-group">
        <label class="control-label">历史数据：</label>
        <select v-model="historicalDays" class="prediction-select" :disabled="predicting">
          <option value="30">30天</option>
          <option value="60">60天</option>
          <option value="90">90天</option>
          <option value="120">120天</option>
          <option value="150">150天</option>
          <option value="200">200天</option>
        </select>
      </div>

      <button
        @click="requestPrediction"
        :disabled="predicting || !stockCode"
        class="prediction-button"
        :class="{ loading: predicting }"
      >
        <span v-if="predicting" class="loading-spinner"></span>
        {{ predicting ? '预测中...' : '开始预测' }}
      </button>
    </div>

    <!-- 预测状态显示 -->
    <div v-if="predictionStatus" class="prediction-status">
      <div
        class="status-message"
        :class="{
          success: predictionStatus.type === 'success',
          error: predictionStatus.type === 'error',
          info: predictionStatus.type === 'info'
        }"
      >
        {{ predictionStatus.message }}
      </div>
    </div>

    <!-- 预测结果摘要 -->
    <div v-if="predictionData && !predicting" class="prediction-results">
      <div class="results-header">
        <h3>预测结果</h3>
        <span class="prediction-info">
          基于 {{ predictionData.historical_data_count }} 天历史数据
        </span>
      </div>

      <div class="results-summary">
        <div class="summary-item">
          <span class="label">预测期间：</span>
          <span class="value">{{ formatDateRange() }}</span>
        </div>
        <div class="summary-item">
          <span class="label">预测天数：</span>
          <span class="value">{{ predictionData.predictions.length }} 天</span>
        </div>
        <div class="summary-item">
          <span class="label">价格趋势：</span>
          <span class="value" :class="trendClass">{{ trendText }}</span>
        </div>
      </div>

      <!-- 视图切换按钮 -->
      <div class="view-toggle">
        <button
          @click="displayMode = 'table'"
          :class="{ active: displayMode === 'table' }"
          class="toggle-button"
          >表格视图</button
        >
        <button
          @click="displayMode = 'chart'"
          :class="{ active: displayMode === 'chart' }"
          class="toggle-button"
          >图表视图</button
        >
      </div>

      <!-- 预测数据表格 -->
      <div v-if="displayMode === 'table'" class="prediction-table-container">
        <table class="prediction-table">
          <thead>
            <tr>
              <th>日期</th>
              <th>预测价格</th>
              <th>置信区间</th>
              <th>变化</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(prediction, index) in predictionData.predictions" :key="prediction.date">
              <td>{{ formatDate(prediction.date) }}</td>
              <td class="price">¥{{ prediction.predicted_close.toFixed(2) }}</td>
              <td class="confidence"
                >¥{{ getConfidenceInterval(index).lower_bound.toFixed(2) }} - ¥{{
                  getConfidenceInterval(index).upper_bound.toFixed(2)
                }}</td
              >
              <td class="change" :class="getChangeClass(index)">
                {{ getChangeText(index) }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 预测数据折线图 -->
      <div v-if="displayMode === 'chart'" class="prediction-chart-container">
        <PredictionChart
          :prediction-data="predictionData"
          :historical-data="historicalData"
          :stock-code="stockCode"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import PredictionChart from './PredictionChart.vue'
import { stockPricePredictApi } from '@/api/stock/prediction'
// 定义 props
const props = defineProps({
  stockCode: {
    type: String,
    required: true
  }
})

// 定义 emits
const emit = defineEmits(['prediction-completed', 'prediction-error'])

// 响应式数据
const predictionDays = ref(7)
const historicalDays = ref(120) // 默认120天历史数据
const predicting = ref(false)
const predictionData = ref(null)
const predictionStatus = ref(null)
const displayMode = ref('table') // 'table' 或 'chart'
const historicalData = ref([])

// 计算属性
const trendClass = computed(() => {
  if (!predictionData.value || predictionData.value.predictions.length < 2) {
    return ''
  }

  const firstPrice = predictionData.value.predictions[0].predicted_close
  const lastPrice =
    predictionData.value.predictions[predictionData.value.predictions.length - 1].predicted_close

  if (lastPrice > firstPrice) {
    return 'trend-up'
  } else if (lastPrice < firstPrice) {
    return 'trend-down'
  } else {
    return 'trend-flat'
  }
})

const trendText = computed(() => {
  if (!predictionData.value || predictionData.value.predictions.length < 2) {
    return '无趋势'
  }

  const firstPrice = predictionData.value.predictions[0].predicted_close
  const lastPrice =
    predictionData.value.predictions[predictionData.value.predictions.length - 1].predicted_close
  const changePercent = (((lastPrice - firstPrice) / firstPrice) * 100).toFixed(1)

  if (lastPrice > firstPrice) {
    return `上涨 ${changePercent}%`
  } else if (lastPrice < firstPrice) {
    return `下跌 ${Math.abs(changePercent)}%`
  } else {
    return '持平'
  }
})

// 方法
const requestPrediction = async () => {
  if (!props.stockCode || predicting.value) {
    return
  }

  predicting.value = true
  predictionStatus.value = {
    type: 'info',
    message: '正在获取历史数据并执行预测...'
  }

  try {
    const response = await stockPricePredictApi({
      stock_code: props.stockCode,
      prediction_days: predictionDays.value,
      historical_days: historicalDays.value
    })

    predictionData.value = response.data

    // 使用预测接口返回的历史数据
    if (response.data.historical_data) {
      historicalData.value = response.data.historical_data
    }

    predictionStatus.value = {
      type: 'success',
      message: `预测完成！生成了 ${response.data.predictions.length} 个预测点`
    }

    // 发送预测完成事件
    emit('prediction-completed', response.data)

    // 3秒后清除状态消息
    setTimeout(() => {
      predictionStatus.value = null
    }, 3000)
  } catch (error) {
    console.error('预测请求失败:', error)

    const errorMessage = error.response?.data?.detail || '预测服务暂时不可用，请稍后重试'
    predictionStatus.value = {
      type: 'error',
      message: errorMessage
    }

    // 发送预测错误事件
    emit('prediction-error', error)

    // 5秒后清除错误消息
    setTimeout(() => {
      predictionStatus.value = null
    }, 5000)
  } finally {
    predicting.value = false
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    month: 'short',
    day: 'numeric'
  })
}

const formatDateRange = () => {
  if (!predictionData.value || predictionData.value.predictions.length === 0) {
    return ''
  }

  const firstDate = predictionData.value.predictions[0].date
  const lastDate =
    predictionData.value.predictions[predictionData.value.predictions.length - 1].date

  return `${formatDate(firstDate)} - ${formatDate(lastDate)}`
}

const getConfidenceInterval = (index) => {
  if (!predictionData.value || !predictionData.value.confidence_intervals[index]) {
    return { lower_bound: 0, upper_bound: 0 }
  }
  return predictionData.value.confidence_intervals[index]
}

const getChangeText = (index) => {
  if (!predictionData.value) {
    return '-'
  }

  const currentPrice = predictionData.value.predictions[index].predicted_close
  let previousPrice

  if (index === 0) {
    // 预测第一天：与历史数据最后一天的收盘价比较
    if (!historicalData.value || historicalData.value.length === 0) {
      return '-'
    }
    previousPrice = historicalData.value[historicalData.value.length - 1].close
  } else {
    // 预测其他天：与前一天预测价格比较
    previousPrice = predictionData.value.predictions[index - 1].predicted_close
  }

  const change = currentPrice - previousPrice
  const changePercent = ((change / previousPrice) * 100).toFixed(1)

  if (change > 0) {
    return `+${changePercent}%`
  } else if (change < 0) {
    return `${changePercent}%`
  } else {
    return '0.0%'
  }
}

const getChangeClass = (index) => {
  if (!predictionData.value) {
    return ''
  }

  const currentPrice = predictionData.value.predictions[index].predicted_close
  let previousPrice

  if (index === 0) {
    // 预测第一天：与历史数据最后一天的收盘价比较
    if (!historicalData.value || historicalData.value.length === 0) {
      return ''
    }
    previousPrice = historicalData.value[historicalData.value.length - 1].close
  } else {
    // 预测其他天：与前一天预测价格比较
    previousPrice = predictionData.value.predictions[index - 1].predicted_close
  }

  if (currentPrice > previousPrice) {
    return 'positive'
  } else if (currentPrice < previousPrice) {
    return 'negative'
  } else {
    return 'neutral'
  }
}

// 监听股票代码变化，清除之前的预测结果
watch(
  () => props.stockCode,
  () => {
    predictionData.value = null
    predictionStatus.value = null
    historicalData.value = []
  }
)
</script>

<style scoped>
.prediction-panel {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.prediction-controls {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 15px;
  flex-wrap: wrap;
}

.control-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.control-label {
  font-weight: 500;
  color: #333;
  white-space: nowrap;
}

.prediction-select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
  font-size: 14px;
  min-width: 80px;
}

.prediction-select:disabled {
  background: #f5f5f5;
  color: #999;
}

.prediction-button {
  padding: 10px 20px;
  background: #1890ff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s;
}

.prediction-button:hover:not(:disabled) {
  background: #40a9ff;
}

.prediction-button:disabled {
  background: #d9d9d9;
  cursor: not-allowed;
}

.prediction-button.loading {
  background: #1890ff;
}

.loading-spinner {
  width: 14px;
  height: 14px;
  border: 2px solid transparent;
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.prediction-status {
  margin-bottom: 15px;
}

.status-message {
  padding: 10px 15px;
  border-radius: 4px;
  font-size: 14px;
}

.status-message.success {
  background: #f6ffed;
  border: 1px solid #b7eb8f;
  color: #52c41a;
}

.status-message.error {
  background: #fff2f0;
  border: 1px solid #ffccc7;
  color: #ff4d4f;
}

.status-message.info {
  background: #e6f7ff;
  border: 1px solid #91d5ff;
  color: #1890ff;
}

.prediction-results {
  border-top: 1px solid #f0f0f0;
  padding-top: 20px;
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.results-header h3 {
  margin: 0;
  color: #333;
  font-size: 16px;
}

.prediction-info {
  font-size: 12px;
  color: #666;
}

.results-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-bottom: 20px;
  padding: 15px;
  background: #fafafa;
  border-radius: 4px;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.summary-item .label {
  font-weight: 500;
  color: #666;
}

.summary-item .value {
  font-weight: 600;
  color: #333;
}

.trend-up {
  color: #52c41a;
}

.trend-down {
  color: #ff4d4f;
}

.trend-flat {
  color: #666;
}

.view-toggle {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
  padding: 4px;
  background: #f5f5f5;
  border-radius: 6px;
  width: fit-content;
}

.toggle-button {
  padding: 8px 16px;
  background: transparent;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  color: #666;
  transition: all 0.2s;
}

.toggle-button:hover {
  background: #e6f7ff;
  color: #1890ff;
}

.toggle-button.active {
  background: #1890ff;
  color: white;
  font-weight: 500;
}

.prediction-chart-container {
  margin-top: 16px;
}

.prediction-table-container {
  overflow-x: auto;
}

.prediction-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.prediction-table th,
.prediction-table td {
  padding: 12px 8px;
  text-align: left;
  border-bottom: 1px solid #f0f0f0;
}

.prediction-table th {
  background: #fafafa;
  font-weight: 600;
  color: #333;
}

.prediction-table .price {
  font-weight: 600;
  color: #333;
}

.prediction-table .confidence {
  font-size: 12px;
  color: #666;
}

.prediction-table .change {
  font-weight: 500;
}

.prediction-table .change.positive {
  color: #ff4d4f;
}

.prediction-table .change.negative {
  color: #52c41a;
}

.prediction-table .change.neutral {
  color: #666;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .prediction-controls {
    flex-direction: column;
    align-items: stretch;
  }

  .control-group {
    justify-content: space-between;
  }

  .results-summary {
    grid-template-columns: 1fr;
  }

  .prediction-table {
    font-size: 12px;
  }

  .prediction-table th,
  .prediction-table td {
    padding: 8px 4px;
  }
}
</style>
