<script setup lang="ts">
import { ElCard, ElButton } from 'element-plus'

defineProps<{
  loading: boolean
}>()

const emit = defineEmits<{
  select: [type: string]
}>()

const quickButtons = [
  { type: 'limit_up', label: '涨停股', color: '#F56C6C' },
  { type: 'limit_down', label: '跌停股', color: '#67C23A' },
  { type: 'high_turnover', label: '高换手', color: '#E6A23C' },
  { type: 'low_pe', label: '低估值', color: '#409EFF' },
  { type: 'volume_surge', label: '放量股', color: '#909399' },
  { type: 'small_cap', label: '小市值', color: '#B37FEB' }
]

const handleSelect = (type: string) => {
  emit('select', type)
}
</script>

<template>
  <ElCard class="quick-screen-card" shadow="never">
    <template #header>
      <span class="title">快捷选股</span>
    </template>
    <div class="quick-buttons">
      <ElButton
        v-for="btn in quickButtons"
        :key="btn.type"
        :loading="loading"
        @click="handleSelect(btn.type)"
        :style="{ borderColor: btn.color, color: btn.color }"
      >
        {{ btn.label }}
      </ElButton>
    </div>
  </ElCard>
</template>

<style lang="scss" scoped>
.quick-screen-card {
  margin-bottom: 16px;

  .title {
    font-size: 16px;
    font-weight: 600;
  }

  .quick-buttons {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
  }
}
</style>
