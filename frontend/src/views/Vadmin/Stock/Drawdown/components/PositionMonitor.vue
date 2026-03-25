<!-- frontend/src/views/Vadmin/Stock/Drawdown/components/PositionMonitor.vue -->
<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage, ElCard, ElForm, ElFormItem, ElInputNumber, ElDatePicker, ElButton, ElRow, ElCol, ElTag, ElAlert } from 'element-plus'
import { monitorPosition, type PositionMonitor as PositionMonitorType } from '@/api/stock/drawdown'

const props = defineProps<{
  stockCode: string
}>()

const form = ref({
  costPrice: null as number | null,
  positionDate: null as Date | null
})

const monitorData = ref<PositionMonitorType | null>(null)
const loading = ref(false)

const handleMonitor = async () => {
  if (!props.stockCode || !form.value.costPrice || !form.value.positionDate) {
    return
  }

  loading.value = true
  try {
    const res = await monitorPosition({
      stock_code: props.stockCode,
      cost_price: form.value.costPrice,
      position_date: form.value.positionDate.toISOString().split('T')[0]
    })
    if (res.code === 200) {
      monitorData.value = res.data
    }
  } catch (error) {
    console.error(error)
    ElMessage.error('持仓监控失败')
  } finally {
    loading.value = false
  }
}

const getAlertType = (level: string) => {
  if (level === '警告') return 'error'
  if (level === '注意') return 'warning'
  return 'success'
}
</script>

<template>
  <ElCard header="持仓监控">
    <ElForm :inline="true" class="mb-4">
      <ElFormItem label="成本价">
        <ElInputNumber v-model="form.costPrice" :min="0" :precision="2" />
      </ElFormItem>
      <ElFormItem label="买入日期">
        <ElDatePicker v-model="form.positionDate" type="date" />
      </ElFormItem>
      <ElFormItem>
        <ElButton type="primary" :loading="loading" @click="handleMonitor">监控</ElButton>
      </ElFormItem>
    </ElForm>

    <template v-if="monitorData">
      <ElAlert
        v-if="monitorData.alert_level !== '正常'"
        :title="`${monitorData.alert_level}：从最高点回撤 ${monitorData.drawdown_from_high}%`"
        :type="getAlertType(monitorData.alert_level)"
        show-icon
        class="mb-4"
      />

      <ElRow :gutter="20">
        <ElCol :span="4">
          <div class="text-gray-500">当前价</div>
          <div class="text-xl font-bold">{{ monitorData.current_price }}</div>
        </ElCol>
        <ElCol :span="4">
          <div class="text-gray-500">盈亏</div>
          <ElTag :type="monitorData.profit_percent >= 0 ? 'success' : 'danger'" size="large">
            {{ monitorData.profit_percent >= 0 ? '+' : '' }}{{ monitorData.profit_percent }}%
          </ElTag>
        </ElCol>
        <ElCol :span="4">
          <div class="text-gray-500">最高价</div>
          <div class="text-xl">{{ monitorData.highest_price }}</div>
        </ElCol>
        <ElCol :span="4">
          <div class="text-gray-500">从高点回撤</div>
          <ElTag type="warning">{{ monitorData.drawdown_from_high }}%</ElTag>
        </ElCol>
        <ElCol :span="4">
          <div class="text-gray-500">建议止盈价</div>
          <div class="text-xl font-bold text-primary">{{ monitorData.suggested_stop_profit }}</div>
        </ElCol>
      </ElRow>
    </template>
  </ElCard>
</template>