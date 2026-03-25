<!-- frontend/src/views/Vadmin/Stock/Drawdown/components/DrawdownAnalysis.vue -->
<script setup lang="ts">
import { computed } from 'vue'
import { ElCard, ElStatistic, ElRow, ElCol, ElTable, ElTableColumn, ElTag } from 'element-plus'
import type { DrawdownAnalysisResult } from '@/api/stock/drawdown'

const props = defineProps<{
  result: DrawdownAnalysisResult
}>()

// 表格数据
const tableData = computed(() => props.result.drawdown_points.slice(0, 10))
</script>

<template>
  <ElCard header="回撤概览">
    <ElRow :gutter="20" class="mb-4">
      <ElCol :span="4">
        <ElStatistic title="最大回撤" :value="result.max_drawdown" suffix="%" />
      </ElCol>
      <ElCol :span="4">
        <ElStatistic title="平均回撤" :value="result.avg_drawdown" suffix="%" />
      </ElCol>
      <ElCol :span="4">
        <ElStatistic title="最大持续天数" :value="result.max_drawdown_duration" suffix="天" />
      </ElCol>
      <ElCol :span="4">
        <ElStatistic title="平均恢复天数" :value="result.avg_recovery_days" suffix="天" />
      </ElCol>
    </ElRow>

    <ElRow :gutter="20" class="mb-4">
      <ElCol :span="2">
        <ElTag>5%+: {{ result.drawdown_5p_count }}次</ElTag>
      </ElCol>
      <ElCol :span="2">
        <ElTag type="warning">10%+: {{ result.drawdown_10p_count }}次</ElTag>
      </ElCol>
      <ElCol :span="2">
        <ElTag type="danger">20%+: {{ result.drawdown_20p_count }}次</ElTag>
      </ElCol>
      <ElCol :span="2">
        <ElTag type="danger" effect="dark">30%+: {{ result.drawdown_30p_count }}次</ElTag>
      </ElCol>
    </ElRow>

    <!-- 回撤记录表 -->
    <ElTable :data="tableData" stripe max-height="300">
      <ElTableColumn prop="peak_date" label="峰值日期" width="120" />
      <ElTableColumn prop="peak_price" label="峰值价格" width="100" />
      <ElTableColumn prop="trough_date" label="谷值日期" width="120" />
      <ElTableColumn prop="trough_price" label="谷值价格" width="100" />
      <ElTableColumn prop="drawdown_percent" label="回撤幅度" width="100">
        <template #default="{ row }">
          <ElTag type="danger">-{{ row.drawdown_percent.toFixed(2) }}%</ElTag>
        </template>
      </ElTableColumn>
      <ElTableColumn prop="duration_days" label="持续天数" width="100" />
      <ElTableColumn prop="recovery_days" label="恢复天数" width="100">
        <template #default="{ row }">
          {{ row.recovery_days ?? '-' }}
        </template>
      </ElTableColumn>
    </ElTable>
  </ElCard>
</template>