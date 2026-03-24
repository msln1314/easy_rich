<script setup lang="ts">
import { computed } from 'vue'
import { ElSelect, ElOption, ElInputNumber, ElInput } from 'element-plus'
import { conditionFields, operators, type Condition } from '@/api/stock/screener'

const props = defineProps<{
  modelValue: Condition
}>()

const emit = defineEmits<{
  'update:modelValue': [value: Condition]
}>()

const localValue = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

const selectedField = computed(() => {
  return conditionFields.find((f) => f.field === localValue.value.field)
})

const handleFieldChange = (field: string) => {
  emit('update:modelValue', {
    ...localValue.value,
    field
  })
}

const handleOperatorChange = (operator: string) => {
  emit('update:modelValue', {
    ...localValue.value,
    operator: operator as Condition['operator']
  })
}

const handleValueChange = (value: number) => {
  emit('update:modelValue', {
    ...localValue.value,
    value
  })
}

const handleValue2Change = (value2: number) => {
  emit('update:modelValue', {
    ...localValue.value,
    value2
  })
}
</script>

<template>
  <div class="condition-builder">
    <ElSelect
      :model-value="localValue.field"
      @update:model-value="handleFieldChange"
      placeholder="选择字段"
      style="width: 140px"
    >
      <ElOption
        v-for="field in conditionFields"
        :key="field.field"
        :label="field.label"
        :value="field.field"
      />
    </ElSelect>

    <ElSelect
      :model-value="localValue.operator"
      @update:model-value="handleOperatorChange"
      placeholder="选择条件"
      style="width: 120px"
    >
      <ElOption
        v-for="op in operators"
        :key="op.value"
        :label="op.label"
        :value="op.value"
      />
    </ElSelect>

    <ElInputNumber
      v-if="localValue.operator !== 'between'"
      :model-value="localValue.value"
      @update:model-value="handleValueChange"
      placeholder="输入值"
      style="width: 120px"
      :controls="false"
    />

    <template v-else>
      <ElInputNumber
        :model-value="localValue.value"
        @update:model-value="handleValueChange"
        placeholder="最小值"
        style="width: 100px"
        :controls="false"
      />
      <span class="separator">至</span>
      <ElInputNumber
        :model-value="localValue.value2"
        @update:model-value="handleValue2Change"
        placeholder="最大值"
        style="width: 100px"
        :controls="false"
      />
    </template>

    <span v-if="selectedField" class="unit">{{ selectedField.unit }}</span>
  </div>
</template>

<style lang="scss" scoped>
.condition-builder {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;

  .separator {
    color: #909399;
  }

  .unit {
    color: #606266;
    font-size: 14px;
    min-width: 30px;
  }
}
</style>