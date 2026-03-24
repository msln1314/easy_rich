<script setup lang="ts">
import { ElRow, ElCol, ElCard, ElDescriptions, ElDescriptionsItem, ElTag, ElProgress, ElTable, ElTableColumn, ElEmpty } from 'element-plus'
import { recommendMap } from '@/api/stock/selectionSignal'
import { patternTypeMap } from '@/api/stock/pattern'

const props = defineProps<{
  data: any
  stockCode: string
}>()

const formatValue = (value: any, suffix: string = '') => {
  if (value === null || value === undefined || value === '') return '-'
  if (typeof value === 'number') return value.toFixed(2) + suffix
  return value + suffix
}
</script>

<template>
  <div class="technical-tab">
    <!-- 综合分析 -->
    <ElCard shadow="never" class="analysis-card" v-if="data.technical">
      <template #header>
        <span class="card-title">综合技术分析</span>
      </template>
      <ElRow :gutter="20">
        <ElCol :span="6">
          <div class="score-item">
            <div class="score-label">综合评分</div>
            <div class="score-value">{{ data.technical.score || '-' }}</div>
            <ElProgress
              :percentage="Math.abs(data.technical.score || 0)"
              :stroke-width="10"
              :show-text="false"
              :color="data.technical.score >= 30 ? '#67C23A' : data.technical.score >= 0 ? '#E6A23C' : '#F56C6C'"
            />
          </div>
        </ElCol>
        <ElCol :span="6">
          <div class="score-item">
            <div class="score-label">总体信号</div>
            <ElTag :type="data.technical.overall_signal === 'strong_buy' ? 'danger' : data.technical.overall_signal === 'buy' ? 'warning' : 'info'" size="large">
              {{ data.technical.overall_signal === 'strong_buy' ? '强买入' : data.technical.overall_signal === 'buy' ? '买入' : data.technical.overall_signal === 'sell' ? '卖出' : data.technical.overall_signal === 'strong_sell' ? '强卖出' : '中性' }}
            </ElTag>
          </div>
        </ElCol>
        <ElCol :span="6">
          <div class="signal-item">
            <div class="signal-label">MACD信号</div>
            <ElTag :type="data.technical.macd_signal === 'buy' ? 'success' : data.technical.macd_signal === 'sell' ? 'danger' : 'info'" size="small">
              {{ data.technical.macd_signal === 'buy' ? '金叉' : data.technical.macd_signal === 'sell' ? '死叉' : '无' }}
            </ElTag>
          </div>
        </ElCol>
        <ElCol :span="6">
          <div class="signal-item">
            <div class="signal-label">KDJ信号</div>
            <ElTag :type="data.technical.kdj_signal === 'buy' ? 'success' : data.technical.kdj_signal === 'sell' ? 'danger' : 'info'" size="small">
              {{ data.technical.kdj_signal === 'buy' ? '金叉' : data.technical.kdj_signal === 'sell' ? '死叉' : '无' }}
            </ElTag>
          </div>
        </ElCol>
      </ElRow>

      <ElRow :gutter="20" style="margin-top: 16px">
        <ElCol :span="6">
          <div class="signal-item">
            <div class="signal-label">RSI信号</div>
            <ElTag :type="data.technical.rsi_signal === 'oversold' ? 'success' : data.technical.rsi_signal === 'overbought' ? 'danger' : 'info'" size="small">
              {{ data.technical.rsi_signal === 'oversold' ? '超卖' : data.technical.rsi_signal === 'overbought' ? '超买' : '正常' }}
            </ElTag>
          </div>
        </ElCol>
        <ElCol :span="6">
          <div class="signal-item">
            <div class="signal-label">BOLL信号</div>
            <ElTag :type="data.technical.boll_signal === 'oversold' ? 'success' : data.technical.boll_signal === 'overbought' ? 'danger' : 'info'" size="small">
              {{ data.technical.boll_signal === 'oversold' ? '下轨支撑' : data.technical.boll_signal === 'overbought' ? '上轨压力' : '中轨' }}
            </ElTag>
          </div>
        </ElCol>
        <ElCol :span="6">
          <div class="signal-item">
            <div class="signal-label">均线趋势</div>
            <ElTag :type="data.technical.ma_trend === 'bullish' ? 'success' : data.technical.ma_trend === 'bearish' ? 'danger' : 'info'" size="small">
              {{ data.technical.ma_trend === 'bullish' ? '多头排列' : data.technical.ma_trend === 'bearish' ? '空头排列' : '震荡' }}
            </ElTag>
          </div>
        </ElCol>
        <ElCol :span="6">
          <div class="signal-item">
            <div class="signal-label">成交量信号</div>
            <ElTag :type="data.technical.volume_signal === 'volume_surge' ? 'warning' : 'info'" size="small">
              {{ data.technical.volume_signal === 'volume_surge' ? '放量' : data.technical.volume_signal === 'volume_shrink' ? '缩量' : '正常' }}
            </ElTag>
          </div>
        </ElCol>
      </ElRow>
    </ElCard>

    <!-- 形态识别 -->
    <ElCard shadow="never" class="pattern-card">
      <template #header>
        <span class="card-title">K线形态识别</span>
      </template>
      <ElTable :data="data.patterns || []" stripe size="small" v-if="data.patterns?.length > 0">
        <ElTableColumn prop="pattern_name" label="形态名称" width="150">
          <template #default="{ row }">
            <ElTag :color="patternTypeMap[row.pattern_type]?.color" effect="dark" size="small">
              {{ row.pattern_name }}
            </ElTag>
          </template>
        </ElTableColumn>
        <ElTableColumn prop="signal" label="信号" width="80" align="center">
          <template #default="{ row }">
            <ElTag :type="row.signal === 'buy' ? 'success' : row.signal === 'sell' ? 'danger' : 'info'" size="small">
              {{ row.signal === 'buy' ? '买入' : row.signal === 'sell' ? '卖出' : '观望' }}
            </ElTag>
          </template>
        </ElTableColumn>
        <ElTableColumn prop="confidence" label="置信度" width="100" align="center">
          <template #default="{ row }">
            {{ (row.confidence * 100).toFixed(0) }}%
          </template>
        </ElTableColumn>
        <ElTableColumn prop="price" label="当前价" width="100" align="right">
          <template #default="{ row }">{{ formatValue(row.price) }}</template>
        </ElTableColumn>
        <ElTableColumn prop="target_price" label="目标价" width="100" align="right">
          <template #default="{ row }">
            <span class="text-up">{{ formatValue(row.target_price) }}</span>
          </template>
        </ElTableColumn>
        <ElTableColumn prop="stop_loss" label="止损价" width="100" align="right">
          <template #default="{ row }">
            <span class="text-down">{{ formatValue(row.stop_loss) }}</span>
          </template>
        </ElTableColumn>
        <ElTableColumn prop="description" label="形态描述" />
      </ElTable>
      <ElEmpty v-else description="未检测到K线形态" :image-size="80" />
    </ElCard>
  </div>
</template>

<style lang="scss" scoped>
.technical-tab {
  .analysis-card,
  .pattern-card {
    margin-bottom: 16px;
  }

  .card-title {
    font-size: 15px;
    font-weight: 600;
  }

  .score-item {
    text-align: center;

    .score-label {
      font-size: 14px;
      color: #909399;
      margin-bottom: 8px;
    }

    .score-value {
      font-size: 28px;
      font-weight: 600;
      margin-bottom: 8px;
    }
  }

  .signal-item {
    text-align: center;

    .signal-label {
      font-size: 12px;
      color: #909399;
      margin-bottom: 8px;
    }
  }
}

.text-up {
  color: #f56c6c;
}

.text-down {
  color: #67c23a;
}
</style>