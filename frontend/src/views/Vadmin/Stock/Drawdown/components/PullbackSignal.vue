<!-- frontend/src/views/Vadmin/Stock/Drawdown/components/PullbackSignal.vue -->
<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { ElMessage, ElCard, ElProgress, ElTag, ElEmpty } from 'element-plus'
import { getPullbackSignals, type PullbackSignal } from '@/api/stock/drawdown'

const props = defineProps<{
  stockCode: string
}>()

const signals = ref<PullbackSignal[]>([])
const loading = ref(false)

const loadSignals = async () => {
  if (!props.stockCode) return
  loading.value = true
  try {
    const res = await getPullbackSignals(props.stockCode)
    if (res.code === 200) {
      signals.value = res.data || []
    }
  } catch (error) {
    console.error(error)
    ElMessage.error('获取买点信号失败')
  } finally {
    loading.value = false
  }
}

watch(() => props.stockCode, loadSignals)
onMounted(loadSignals)

const getStrengthType = (strength: number) => {
  if (strength >= 70) return 'success'
  if (strength >= 50) return 'warning'
  return 'info'
}
</script>

<template>
  <ElCard header="回调买点信号">
    <template v-if="signals.length > 0">
      <div v-for="signal in signals" :key="signal.signal_date" class="mb-4 p-4 border rounded">
        <div class="flex items-center justify-between mb-2">
          <span>信号强度</span>
          <ElTag :type="getStrengthType(signal.signal_strength)">
            {{ signal.signal_strength >= 70 ? '强买点' : signal.signal_strength >= 50 ? '中等买点' : '观望' }}
          </ElTag>
        </div>
        <ElProgress
          :percentage="signal.signal_strength"
          :status="getStrengthType(signal.signal_strength)"
          class="mb-2"
        />
        <div class="grid grid-cols-3 gap-4 text-sm">
          <div>
            <span class="text-gray-500">当前回调:</span>
            <ElTag type="danger" class="ml-1">{{ signal.current_drawdown.toFixed(2) }}%</ElTag>
          </div>
          <div>
            <span class="text-gray-500">支撑位:</span>
            <span class="ml-1 font-bold">{{ signal.support_price }}</span>
          </div>
          <div>
            <span class="text-gray-500">建议止损:</span>
            <span class="ml-1">{{ signal.stop_loss_price }}</span>
          </div>
        </div>
        <div class="mt-2 text-sm text-gray-600">{{ signal.reasoning }}</div>
      </div>
    </template>
    <ElEmpty v-else description="暂无买点信号" />
  </ElCard>
</template>