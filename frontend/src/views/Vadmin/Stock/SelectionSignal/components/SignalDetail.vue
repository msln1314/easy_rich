<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElRow, ElCol, ElCard, ElTag, ElProgress, ElDescriptions, ElDescriptionsItem } from 'element-plus'
import { getStockSignalDetail, recommendMap, type SelectionSignalItem } from '@/api/stock/selectionSignal'

const props = defineProps<{
  stock: SelectionSignalItem
}>()

const loading = ref(false)
const detail = ref<any>(null)

const fetchDetail = async () => {
  loading.value = true
  try {
    const res = await getStockSignalDetail(props.stock.stock_code, props.stock.signal_date)
    detail.value = res.data || null
  } catch (error) {
    console.error('获取详情失败:', error)
  } finally {
    loading.value = false
  }
}

const formatValue = (value: number | undefined | null, suffix: string = '') => {
  if (value === undefined || value === null) return '-'
  return value.toFixed(2) + suffix
}

onMounted(() => {
  fetchDetail()
})
</script>

<template>
  <div class="signal-detail" v-loading="loading">
    <!-- 基本信息 -->
    <ElCard shadow="never" class="info-card">
      <ElRow :gutter="20">
        <ElCol :span="6">
          <div class="info-item">
            <div class="label">股票代码</div>
            <div class="value">{{ stock.stock_code }}</div>
          </div>
        </ElCol>
        <ElCol :span="6">
          <div class="info-item">
            <div class="label">股票名称</div>
            <div class="value">{{ stock.stock_name }}</div>
          </div>
        </ElCol>
        <ElCol :span="6">
          <div class="info-item">
            <div class="label">当前价格</div>
            <div class="value">{{ stock.current_price?.toFixed(2) || '-' }}</div>
          </div>
        </ElCol>
        <ElCol :span="6">
          <div class="info-item">
            <div class="label">涨跌幅</div>
            <div class="value" :class="stock.change_percent > 0 ? 'text-up' : stock.change_percent < 0 ? 'text-down' : ''">
              {{ stock.change_percent?.toFixed(2) || '-' }}%
            </div>
          </div>
        </ElCol>
      </ElRow>
    </ElCard>

    <!-- 评分信息 -->
    <ElCard shadow="never" class="score-card">
      <template #header>
        <span class="card-title">评分分析</span>
      </template>
      <ElRow :gutter="20">
        <ElCol :span="6">
          <div class="score-item">
            <div class="score-label">综合评分</div>
            <div class="score-value">{{ stock.total_score?.toFixed(0) || '-' }}</div>
            <ElProgress
              :percentage="stock.total_score || 0"
              :stroke-width="10"
              :show-text="false"
              :color="stock.total_score >= 60 ? '#67C23A' : stock.total_score >= 40 ? '#E6A23C' : '#F56C6C'"
            />
          </div>
        </ElCol>
        <ElCol :span="6">
          <div class="score-item">
            <div class="score-label">推荐信号</div>
            <div class="score-value">
              <ElTag v-if="recommendMap[stock.recommend]" :type="recommendMap[stock.recommend].type" size="large">
                {{ recommendMap[stock.recommend].label }}
              </ElTag>
            </div>
          </div>
        </ElCol>
        <ElCol :span="6">
          <div class="score-item">
            <div class="score-label">信号强度</div>
            <div class="score-value">{{ stock.signal_strength || '-' }}级</div>
          </div>
        </ElCol>
        <ElCol :span="6">
          <div class="score-item">
            <div class="score-label">置信度</div>
            <div class="score-value">{{ (stock.confidence * 100)?.toFixed(0) || '-' }}%</div>
          </div>
        </ElCol>
      </ElRow>
    </ElCard>

    <!-- 技术指标 -->
    <ElCard shadow="never" class="indicator-card" v-if="detail">
      <template #header>
        <span class="card-title">技术指标</span>
      </template>
      <ElDescriptions :column="4" border>
        <ElDescriptionsItem label="MA5">{{ formatValue(detail.ma5) }}</ElDescriptionsItem>
        <ElDescriptionsItem label="MA10">{{ formatValue(detail.ma10) }}</ElDescriptionsItem>
        <ElDescriptionsItem label="MA20">{{ formatValue(detail.ma20) }}</ElDescriptionsItem>
        <ElDescriptionsItem label="均线信号">
          <ElTag v-if="detail.ma_signal === 1" type="success" size="small">金叉</ElTag>
          <ElTag v-else-if="detail.ma_signal === -1" type="danger" size="small">死叉</ElTag>
          <span v-else>-</span>
        </ElDescriptionsItem>

        <ElDescriptionsItem label="DIF">{{ formatValue(detail.dif) }}</ElDescriptionsItem>
        <ElDescriptionsItem label="DEA">{{ formatValue(detail.dea) }}</ElDescriptionsItem>
        <ElDescriptionsItem label="MACD">{{ formatValue(detail.macd) }}</ElDescriptionsItem>
        <ElDescriptionsItem label="MACD信号">
          <ElTag v-if="detail.macd_signal === 1" type="success" size="small">金叉</ElTag>
          <ElTag v-else-if="detail.macd_signal === -1" type="danger" size="small">死叉</ElTag>
          <span v-else>-</span>
        </ElDescriptionsItem>

        <ElDescriptionsItem label="K值">{{ formatValue(detail.k_value) }}</ElDescriptionsItem>
        <ElDescriptionsItem label="D值">{{ formatValue(detail.d_value) }}</ElDescriptionsItem>
        <ElDescriptionsItem label="J值">{{ formatValue(detail.j_value) }}</ElDescriptionsItem>
        <ElDescriptionsItem label="KDJ信号">
          <ElTag v-if="detail.kdj_signal === 1" type="success" size="small">金叉</ElTag>
          <ElTag v-else-if="detail.kdj_signal === -1" type="danger" size="small">死叉</ElTag>
          <span v-else>-</span>
        </ElDescriptionsItem>

        <ElDescriptionsItem label="RSI">{{ formatValue(detail.rsi_value) }}</ElDescriptionsItem>
        <ElDescriptionsItem label="RSI信号">
          <ElTag v-if="detail.rsi_signal === 1" type="success" size="small">超卖</ElTag>
          <ElTag v-else-if="detail.rsi_signal === -1" type="danger" size="small">超买</ElTag>
          <span v-else>-</span>
        </ElDescriptionsItem>
        <ElDescriptionsItem label="成交量信号">
          <ElTag v-if="detail.volume_signal === 1" type="success" size="small">放量</ElTag>
          <ElTag v-else-if="detail.volume_signal === -1" type="warning" size="small">缩量</ElTag>
          <span v-else>-</span>
        </ElDescriptionsItem>
        <ElDescriptionsItem label="波动率">{{ formatValue(detail.volatility, '%') }}</ElDescriptionsItem>
      </ElDescriptions>
    </ElCard>

    <!-- 分项评分 -->
    <ElCard shadow="never" class="sub-score-card" v-if="detail">
      <template #header>
        <span class="card-title">分项评分</span>
      </template>
      <ElRow :gutter="16">
        <ElCol :span="6" v-for="(score, key) in {
          macd_score: 'MACD评分',
          kdj_score: 'KDJ评分',
          rsi_score: 'RSI评分',
          ma_score: '均线评分',
          volume_score: '成交量评分',
          trend_score: '趋势评分',
          potential_score: '潜力评分'
        }" :key="key">
          <div class="sub-score-item">
            <div class="sub-score-label">{{ score }}</div>
            <ElProgress
              :percentage="(detail[key] || 0) / 25 * 100"
              :stroke-width="8"
              :show-text="true"
              :format="() => detail[key]?.toFixed(0) || '0'"
              :color="detail[key] >= 15 ? '#67C23A' : detail[key] >= 10 ? '#E6A23C' : '#909399'"
            />
          </div>
        </ElCol>
      </ElRow>
    </ElCard>
  </div>
</template>

<style lang="scss" scoped>
.signal-detail {
  .info-card,
  .score-card,
  .indicator-card,
  .sub-score-card {
    margin-bottom: 16px;
  }

  .card-title {
    font-size: 15px;
    font-weight: 600;
  }

  .info-item {
    text-align: center;

    .label {
      font-size: 12px;
      color: #909399;
      margin-bottom: 8px;
    }

    .value {
      font-size: 18px;
      font-weight: 600;
      color: #303133;
    }
  }

  .score-item {
    text-align: center;

    .score-label {
      font-size: 14px;
      color: #909399;
      margin-bottom: 8px;
    }

    .score-value {
      font-size: 24px;
      font-weight: 600;
      color: #303133;
      margin-bottom: 8px;
    }
  }

  .sub-score-item {
    margin-bottom: 16px;

    .sub-score-label {
      font-size: 12px;
      color: #606266;
      margin-bottom: 8px;
    }
  }
}

.text-up {
  color: #f56c6c !important;
}

.text-down {
  color: #67c23a !important;
}
</style>