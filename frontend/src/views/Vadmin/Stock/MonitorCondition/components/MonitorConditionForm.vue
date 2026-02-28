<script setup lang="ts">
import { ref, reactive, onMounted, watch } from 'vue'
import {
  ElForm,
  ElFormItem,
  ElInput,
  ElSelect,
  ElOption,
  ElInputNumber,
  ElSwitch
} from 'element-plus'
import { addMonitorConditionApi, putMonitorConditionApi } from '@/api/stock/monitor_condition'

interface Props {
  currentRow?: any
}

const props = withDefaults(defineProps<Props>(), {
  currentRow: null
})

const emit = defineEmits(['success'])

const formRef = ref<InstanceType<typeof ElForm>>()
const formData = reactive({
  name: '',
  condition_content: '',
  tag: '',
  user_id: 1,
  is_active: 1,
  remark: '',
  owner: '',
  reason: '',
  watch_days: 7
})

const rules = {
  name: [{ required: true, message: '请输入监控名称', trigger: 'blur' }],
  condition_content: [{ required: true, message: '请输入监控条件', trigger: 'blur' }]
}

onMounted(() => {
  if (props.currentRow) {
    Object.assign(formData, {
      name: props.currentRow.name || '',
      condition_content: props.currentRow.condition_content || '',
      tag: props.currentRow.tag || '',
      user_id: props.currentRow.user_id || 1,
      is_active: props.currentRow.is_active !== undefined ? props.currentRow.is_active : 1,
      remark: props.currentRow.remark || '',
      owner: props.currentRow.owner || '',
      reason: props.currentRow.reason || '',
      watch_days: props.currentRow.watch_days || 7
    })
  }
})

watch(
  () => props.currentRow,
  (newVal) => {
    if (newVal) {
      Object.assign(formData, {
        name: newVal.name || '',
        condition_content: newVal.condition_content || '',
        tag: newVal.tag || '',
        user_id: newVal.user_id || 1,
        is_active: newVal.is_active !== undefined ? newVal.is_active : 1,
        remark: newVal.remark || '',
        owner: newVal.owner || '',
        reason: newVal.reason || '',
        watch_days: newVal.watch_days || 7
      })
    }
  }
)

const submit = async () => {
  const valid = await formRef.value?.validate()
  if (valid) {
    try {
      if (props.currentRow?.id) {
        await putMonitorConditionApi({
          id: props.currentRow.id,
          ...formData
        })
      } else {
        await addMonitorConditionApi(formData)
      }
      return true
    } catch (error) {
      return false
    }
  }
  return false
}

const resetForm = () => {
  formRef.value?.resetFields()
  Object.assign(formData, {
    name: '',
    condition_content: '',
    tag: '',
    user_id: 1,
    is_active: 1,
    remark: '',
    owner: '',
    reason: '',
    watch_days: 7
  })
}

defineExpose({
  submit,
  resetForm
})
</script>

<template>
  <ElForm ref="formRef" :model="formData" :rules="rules" label-width="120px">
    <ElFormItem label="监控名称" prop="name">
      <ElInput v-model="formData.name" placeholder="请输入监控名称" clearable />
    </ElFormItem>

    <ElFormItem label="监控条件" prop="condition_content">
      <ElInput
        v-model="formData.condition_content"
        type="textarea"
        :rows="4"
        placeholder="请输入监控条件，例如：pe_ratio<20 AND pb_ratio<2 AND change_percent>5"
        clearable
      />
    </ElFormItem>

    <ElFormItem label="标签" prop="tag">
      <ElInput v-model="formData.tag" placeholder="请输入标签，例如：价值投资、成长股" clearable />
    </ElFormItem>

    <ElFormItem label="拥有者" prop="owner">
      <ElInput v-model="formData.owner" placeholder="请输入拥有者" clearable />
    </ElFormItem>

    <ElFormItem label="条件原因" prop="reason">
      <ElInput
        v-model="formData.reason"
        type="textarea"
        :rows="3"
        placeholder="请输入条件原因，例如：低估值、高成长"
        clearable
      />
    </ElFormItem>

    <ElFormItem label="关注天数" prop="watch_days">
      <ElInputNumber v-model="formData.watch_days" :min="1" :max="365" />
    </ElFormItem>

    <ElFormItem label="启用状态" prop="is_active">
      <ElSwitch v-model="formData.is_active" :active-value="1" :inactive-value="0" />
    </ElFormItem>

    <ElFormItem label="备注" prop="remark">
      <ElInput
        v-model="formData.remark"
        type="textarea"
        :rows="3"
        placeholder="请输入备注信息"
        clearable
      />
    </ElFormItem>
  </ElForm>
</template>
