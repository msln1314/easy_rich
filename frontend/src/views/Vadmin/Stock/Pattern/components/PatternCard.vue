<script setup lang="ts">
import { computed } from 'vue'
import { ElCard, ElTag, ElDescriptions, ElDescriptionsItem, ElButton } from 'element-plus'
import { patternTypeMap, type PatternResult } from '@/api/stock/pattern'

const props = defineProps<{
  pattern: PatternResult
}>()

const patternInfo = computed(() => {
  return patternTypeMap[props.pattern.pattern_type] || {
    name: props.pattern.pattern_name,
    signal: 'hold',
    color: '#909399'
  }
})

const signalType = computed(() => {
  return props.pattern.signal === 'buy' ? 'success' : props.pattern.signal === 'sell' ? 'danger' : 'info'
})

const signalText = computed(() => {
  return props.pattern.signal === 'buy' ? '买入信号' : props.pattern.signal === 'sell' ? '卖出信号' : '观望'
})

const formatValue = (value: number | null | undefined) => {
  if (value === null || value === undefined) return '-'
  return value.toFixed(2)
}

const confidencePercent = computed(() => {
  return (props.pattern.confidence * 100).toFixed(0)
})
</script>

<template>
  <ElCard class="pattern-card" :body-style="{ padding: '16px' }">
    <template #header>
      <div class="card-header">
        <ElTag :color="patternInfo.color" effect="dark">{{ patternInfo.name }}</ElTag>
        <ElTag :type="signalType" size="small">{{ signalText }}</ElTag>
      </div>
    </template>

    <div class="pattern-content">
      <div class="confidence-section">
        <span class="confidence-label">置信度</span>
        <span class="confidence-value">{{ confidencePercent }}%</span>
      </div>

      <ElDescriptions :column="2" size="small" border>
        <ElDescriptionsItem label="当前价格">
          <span class="price">{{ formatValue(pattern.price) }}</span>
        </ElDescriptionsItem>
        <ElDescriptionsItem label="目标价格">
          <span class="target">{{ formatValue(pattern.target_price) }}</span>
        </ElDescriptionsItem>
        <ElDescriptionsItem label="止损价格">
          <span class="stop-loss">{{ formatValue(pattern.stop_loss) }}</span>
        </ElDescriptionsItem>
        <ElDescriptionsItem label="检测时间">
          {{ new Date(pattern.detected_time).toLocaleString() }}
        </ElDescriptionsItem>
      </ElDescriptions>

      <div class="description-section">
        <div class="description-label">形态描述</div>
        <div class="description-text">{{ pattern.description }}</div>
      </div>

      <div class="action-section">
        <ElButton type="primary" size="small" link>查看K线图</ElButton>
        <ElButton type="success" size="small" link>加入监控</ElButton>
      </div>
    </div>
  </ElCard>
</template>

<style lang="scss" scoped>
.pattern-card {
  border: 1px solid #e4e7ed;
  transition: all 0.3s;

  &:hover {
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .pattern-content {
    .confidence-section {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 12px 0;
      border-bottom: 1px solid #ebeef5;
      margin-bottom: 12px;

      .confidence-label {
        font-size: 14px;
        color: #909399;
      }

      .confidence-value {
        font-size: 20px;
        font-weight: 600;
        color: #409eff;
      }
    }

    .price {
      font-weight: 600;
      color: #303133;
    }

    .target {
      color: #67c23a;
      font-weight: 600;
    }

    .stop-loss {
      color: #f56c6c;
      font-weight: 600;
    }

    .description-section {
      margin-top: 12px;
      padding: 12px;
      background: #f5f7fa;
      border-radius: 4px;

      .description-label {
        font-size: 12px;
        color: #909399;
        margin-bottom: 8px;
      }

      .description-text {
        font-size: 14px;
        color: #606266;
        line-height: 1.5;
      }
    }

    .action-section {
      display: flex;
      justify-content: flex-end;
      gap: 12px;
      margin-top: 12px;
      padding-top: 12px;
      border-top: 1px solid #ebeef5;
    }
  }
}
</style>