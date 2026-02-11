<script setup lang="tsx">
import { Form, FormSchema } from '@/components/Form'
import { useForm } from '@/hooks/web/useForm'
import { PropType, reactive, watch } from 'vue'
import { useValidator } from '@/hooks/web/useValidator'

const { required } = useValidator()

const props = defineProps({
  currentRow: {
    type: Object as PropType<any>,
    default: () => null
  }
})

const formSchema = reactive<FormSchema[]>([
  {
    field: 'stock_code',
    label: '股票代码',
    colProps: {
      span: 12
    },
    component: 'Input',
    componentProps: {
      disabled: true,
      style: {
        width: '100%'
      }
    }
  },
  {
    field: 'stock_name',
    label: '股票名称',
    colProps: {
      span: 12
    },
    component: 'Input',
    componentProps: {
      disabled: true,
      style: {
        width: '100%'
      }
    }
  },
  {
    field: 'analysis_period',
    label: '分析周期',
    colProps: {
      span: 12
    },
    component: 'Select',
    componentProps: {
      style: {
        width: '100%'
      },
      options: [
        {
          label: '短线',
          value: '短线'
        },
        {
          label: '中线',
          value: '中线'
        },
        {
          label: '长线',
          value: '长线'
        }
      ]
    },
    value: '短线'
  },
  {
    field: 'analysis_type',
    label: '分析类型',
    colProps: {
      span: 12
    },
    component: 'Select',
    componentProps: {
      style: {
        width: '100%'
      },
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
    value: '技术分析'
  },
  {
    field: 'notes',
    label: '备注',
    colProps: {
      span: 24
    },
    component: 'Input',
    componentProps: {
      type: 'textarea',
      rows: 4,
      placeholder: '请输入备注信息',
      style: {
        width: '100%'
      }
    }
  }
])

const rules = reactive({
  analysis_period: [required()],
  analysis_type: [required()]
})

const { formRegister, formMethods } = useForm()
const { setValues, getFormData, getElFormExpose } = formMethods

const submit = async () => {
  const elForm = await getElFormExpose()
  const valid = await elForm?.validate()
  if (valid) {
    const formData = await getFormData()
    return formData
  }
}

watch(
  () => props.currentRow,
  (currentRow) => {
    if (!currentRow) return
    setValues({
      stock_code: currentRow.stock_code,
      stock_name: currentRow.stock_name
    })
  },
  {
    deep: true,
    immediate: true
  }
)

defineExpose({
  submit
})
</script>

<template>
  <Form :rules="rules" @register="formRegister" :schema="formSchema" />
</template>
