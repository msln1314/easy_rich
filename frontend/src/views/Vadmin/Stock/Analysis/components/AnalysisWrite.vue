<script setup lang="tsx">
import { reactive, ref, watch, computed } from 'vue'
import { Form, FormSchema } from '@/components/Form'
import { useForm } from '@/hooks/web/useForm'
import { getStockPageApi } from '@/api/stock/base'
import { updateStockAnalysisApi } from '@/api/stock/analysis'

defineOptions({
  name: 'AnalysisWrite'
})

const props = defineProps({
  currentRow: {
    type: Object,
    default: () => null
  }
})

const isUpdate = computed(() => !!props.currentRow?.id)

const stockOptions = ref<any[]>([])
const loading = ref(false)

const { formRegister, formMethods } = useForm()
const { setValues, getElFormExpose } = formMethods

const formSchema = reactive<FormSchema[]>([
  {
    field: 'stock_code',
    label: '股票代码',
    component: 'Select',
    componentProps: {
      clearable: true,
      filterable: true,
      remote: true,
      remoteMethod: async (query: string) => {
        if (!query) {
          stockOptions.value = []
          return
        }
        loading.value = true
        try {
          const res = await getStockPageApi({
            keywords: query
          })
          stockOptions.value = res.data.map((item: any) => ({
            label: item.name,
            value: item.stock_code
          }))
          console.log(stockOptions.value, 'stockOptions')
        } catch (error) {
          console.error('获取股票列表失败', error)
        } finally {
          loading.value = false
        }
      },
      loading: loading,
      options: stockOptions
    },
    formItemProps: {
      rules: [{ required: true, message: '请选择股票代码', trigger: 'change' }]
    }
  },
  {
    field: 'analysis_period',
    label: '分析周期',
    component: 'Select',
    componentProps: {
      clearable: true,
      options: [
        { label: '短线', value: '短线' },
        { label: '中线', value: '中线' },
        { label: '长线', value: '长线' }
      ]
    },
    formItemProps: {
      rules: [{ required: true, message: '请选择分析周期', trigger: 'change' }]
    }
  },
  {
    field: 'analysis_type',
    label: '分析类型',
    component: 'Select',
    componentProps: {
      clearable: true,
      options: [
        {
          label: '技术分析',
          value: '技术分析'
        },
        {
          label: '基本面分析',
          value: '基本面分析'
        },
        {
          label: '消息面分析',
          value: '消息面分析'
        },
        {
          label: '综合分析',
          value: '综合分析'
        }
      ]
    },
    formItemProps: {
      rules: [{ required: true, message: '请选择分析类型', trigger: 'change' }]
    }
  },
  {
    field: 'notes',
    label: '备注',
    component: 'Input',
    componentProps: {
      type: 'textarea',
      rows: 4,
      clearable: true,
      placeholder: '请输入备注信息'
    }
  }
])

const submit = async () => {
  const elForm = await getElFormExpose()
  const valid = await elForm?.validate()
  if (valid) {
    const formData = await formMethods.getFormData()
    // 编辑操作在这里处理
    if (isUpdate.value && props.currentRow) {
      await updateStockAnalysisApi(props.currentRow.id, formData)
    }
    return formData
  }
}

watch(
  () => props.currentRow,
  (val) => {
    if (val) {
      setValues(val)
    }
  },
  {
    immediate: true,
    deep: true
  }
)

defineExpose({
  submit
})
</script>

<template>
  <Form @register="formRegister" :schema="formSchema" />
</template>
