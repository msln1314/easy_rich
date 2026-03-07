<script setup lang="ts">
import { ref, reactive, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { addMonitorStrategyApi, putMonitorStrategyApi } from '@/api/stock/monitor_strategy'
import { Form, FormSchema } from '@/components/Form'
import { useForm } from '@/hooks/web/useForm'

defineProps<{
  strategy?: any
}>()

const emit = defineEmits(['success'])

const strategyTypeOptions = [
  { label: '涨停监听', value: 'limit_up' },
  { label: '跌停监听', value: 'limit_down' },
  { label: '开板监听', value: 'open_board' },
  { label: '换手监听', value: 'turnover' },
  { label: '突破监听', value: 'breakout' },
  { label: '反弹监听', value: 'rebound' },
  { label: '涨停破板', value: 'limit_up_break' },
  { label: '涨幅监听', value: 'price_rise' },
  { label: '跌至价位', value: 'price_fall' },
  { label: '形态监控', value: 'pattern' }
]

const priorityOptions = [
  { label: '高', value: 1 },
  { label: '中', value: 2 },
  { label: '低', value: 3 }
]

const cooldownTypeOptions = [
  { label: '同一天只触发一次', value: 'same_day' },
  { label: '按间隔时间触发', value: 'interval' }
]

const notifyMethodOptions = [
  { label: '系统消息', value: 'system' },
  { label: '邮件', value: 'email' },
  { label: '短信', value: 'sms' },
  { label: '微信', value: 'wechat' }
]

const notifyTypeOptions = [
  { label: '仅一次', value: 'once' },
  { label: '每次都推送', value: 'always' },
  { label: '按间隔推送', value: 'interval' }
]

const formSchema = reactive<FormSchema[]>([
  {
    field: 'name',
    label: '策略名称',
    component: 'Input',
    colProps: { span: 24 },
    componentProps: {
      placeholder: '请输入策略名称',
      maxlength: 100
    },
    formItemProps: {
      rules: [{ required: true, message: '请输入策略名称', trigger: 'blur' }]
    }
  },
  {
    field: 'stock_code',
    label: '股票代码',
    component: 'Input',
    colProps: { span: 12 },
    componentProps: {
      placeholder: '请输入股票代码，如000001',
      maxlength: 10
    },
    formItemProps: {
      rules: [{ required: true, message: '请输入股票代码', trigger: 'blur' }]
    }
  },
  {
    field: 'stock_name',
    label: '股票名称',
    component: 'Input',
    colProps: { span: 12 },
    componentProps: {
      placeholder: '请输入股票名称',
      maxlength: 50
    }
  },
  {
    field: 'strategy_type',
    label: '策略类型',
    component: 'Select',
    colProps: { span: 12 },
    componentProps: {
      placeholder: '请选择策略类型',
      options: strategyTypeOptions
    },
    formItemProps: {
      rules: [{ required: true, message: '请选择策略类型', trigger: 'change' }]
    }
  },
  {
    field: 'tag',
    label: '标签',
    component: 'Input',
    colProps: { span: 12 },
    componentProps: {
      placeholder: '请输入标签',
      maxlength: 50
    }
  },
  {
    field: 'condition_content',
    label: '触发条件',
    component: 'Input',
    colProps: { span: 24 },
    componentProps: {
      type: 'textarea',
      placeholder: '请输入触发条件，如换手率>5等',
      rows: 3,
      maxlength: 500
    }
  },
  {
    field: 'trigger_value_min',
    label: '触发值最小值',
    component: 'InputNumber',
    colProps: { span: 12 },
    componentProps: {
      placeholder: '如换手率5表示>5%',
      precision: 2,
      min: 0
    }
  },
  {
    field: 'trigger_value_max',
    label: '触发值最大值',
    component: 'InputNumber',
    colProps: { span: 12 },
    componentProps: {
      placeholder: '如换手率10表示<10%',
      precision: 2,
      min: 0
    }
  },
  {
    field: 'trigger_percent_min',
    label: '触发百分比最小值',
    component: 'InputNumber',
    colProps: { span: 12 },
    componentProps: {
      placeholder: '如涨幅5表示>5%',
      precision: 2,
      min: 0
    }
  },
  {
    field: 'trigger_percent_max',
    label: '触发百分比最大值',
    component: 'InputNumber',
    colProps: { span: 12 },
    componentProps: {
      placeholder: '如涨幅10表示<10%',
      precision: 2,
      min: 0
    }
  },
  {
    field: 'cooldown_minutes',
    label: '冷却时间(分钟)',
    component: 'InputNumber',
    colProps: { span: 12 },
    componentProps: {
      placeholder: '触发后多久再次触发',
      min: 1,
      max: 1440
    },
    formItemProps: {
      rules: [{ required: true, message: '请输入冷却时间', trigger: 'blur' }]
    }
  },
  {
    field: 'cooldown_type',
    label: '冷却类型',
    component: 'Select',
    colProps: { span: 12 },
    componentProps: {
      placeholder: '请选择冷却类型',
      options: cooldownTypeOptions
    },
    formItemProps: {
      rules: [{ required: true, message: '请选择冷却类型', trigger: 'change' }]
    }
  },
  {
    field: 'priority',
    label: '优先级',
    component: 'Select',
    colProps: { span: 12 },
    componentProps: {
      placeholder: '请选择优先级',
      options: priorityOptions
    },
    formItemProps: {
      rules: [{ required: true, message: '请选择优先级', trigger: 'change' }]
    }
  },
  {
    field: 'is_active',
    label: '启用状态',
    component: 'Switch',
    colProps: { span: 12 },
    componentProps: {
      activeValue: 1,
      inactiveValue: 0,
      activeText: '启用',
      inactiveText: '禁用'
    }
  },
  {
    field: 'notify_enabled',
    label: '启用推送',
    component: 'Switch',
    colProps: { span: 12 },
    componentProps: {
      activeValue: 1,
      inactiveValue: 0,
      activeText: '启用',
      inactiveText: '禁用'
    }
  },
  {
    field: 'notify_method',
    label: '推送方式',
    component: 'Select',
    colProps: { span: 12 },
    componentProps: {
      placeholder: '请选择推送方式',
      options: notifyMethodOptions
    },
    formItemProps: {
      rules: [{ required: true, message: '请选择推送方式', trigger: 'change' }]
    }
  },
  {
    field: 'notify_trigger_count',
    label: '推送触发次数',
    component: 'InputNumber',
    colProps: { span: 12 },
    componentProps: {
      placeholder: '累计触发次数达到此值时才推送',
      min: 1,
      max: 100
    },
    formItemProps: {
      rules: [{ required: true, message: '请输入推送触发次数', trigger: 'blur' }]
    }
  },
  {
    field: 'notify_type',
    label: '推送类型',
    component: 'Select',
    colProps: { span: 12 },
    componentProps: {
      placeholder: '请选择推送类型',
      options: notifyTypeOptions
    },
    formItemProps: {
      rules: [{ required: true, message: '请选择推送类型', trigger: 'change' }]
    }
  },
  {
    field: 'strategy_config',
    label: '策略配置(JSON)',
    component: 'Input',
    colProps: { span: 24 },
    componentProps: {
      type: 'textarea',
      placeholder: '请输入策略特定配置，JSON格式，如：{"threshold": 9.9, "direction": "up"}',
      rows: 3
    }
  },
  {
    field: 'reason',
    label: '监听原因',
    component: 'Input',
    colProps: { span: 24 },
    componentProps: {
      type: 'textarea',
      placeholder: '请输入监听原因',
      rows: 2,
      maxlength: 255
    }
  },
  {
    field: 'remark',
    label: '备注',
    component: 'Input',
    colProps: { span: 24 },
    componentProps: {
      type: 'textarea',
      placeholder: '请输入备注',
      rows: 2
    }
  }
])

const { register, formRef, methods } = useForm()

const formLoading = ref(false)

// 监听策略变化，填充表单
watch(
  () => props.strategy,
  (val) => {
    if (val) {
      methods.setValues(val)
    } else {
      methods.setValues({
        name: '',
        stock_code: '',
        stock_name: '',
        strategy_type: '',
        tag: '',
        condition_content: '',
        trigger_value_min: null,
        trigger_value_max: null,
        trigger_percent_min: null,
        trigger_percent_max: null,
        cooldown_minutes: 60,
        cooldown_type: 'same_day',
        priority: 3,
        is_active: 1,
        notify_enabled: 1,
        notify_method: 'system',
        notify_trigger_count: 1,
        notify_type: 'once',
        strategy_config: '',
        reason: '',
        remark: ''
      })
    }
  },
  { immediate: true }
)

// 提交表单
const handleSubmit = async () => {
  const formEl = formRef.value
  if (!formEl) return

  await formEl.validate(async (valid) => {
    if (!valid) return

    formLoading.value = true
    try {
      const values = methods.getValues()

      // 处理 JSON 配置
      if (values.strategy_config) {
        try {
          JSON.parse(values.strategy_config)
        } catch (e) {
          ElMessage.error('策略配置格式错误，请输入有效的JSON格式')
          formLoading.value = false
          return
        }
      }

      if (props.strategy?.id) {
        await putMonitorStrategyApi(values, props.strategy.id)
        ElMessage.success('更新成功')
      } else {
        await addMonitorStrategyApi(values)
        ElMessage.success('创建成功')
      }
      emit('success')
    } catch (error) {
      ElMessage.error('操作失败')
    } finally {
      formLoading.value = false
    }
  })
}
</script>

<template>
  <div class="strategy-form-container">
    <Form
      :schema="formSchema"
      :is-col="true"
      :register="register"
      label-width="140px"
      label-position="right"
    />
    <div class="form-actions">
      <el-button @click="$emit('success')">取消</el-button>
      <el-button type="primary" :loading="formLoading" @click="handleSubmit">提交</el-button>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.strategy-form-container {
  .form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 12px;
    margin-top: 24px;
    padding-top: 24px;
    border-top: 1px solid #e4e7ed;
  }
}
</style>
