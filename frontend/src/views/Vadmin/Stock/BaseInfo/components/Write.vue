<script setup lang="tsx">
import { Form, FormSchema } from '@/components/Form'
import { useForm } from '@/hooks/web/useForm'
import { PropType, reactive, watch } from 'vue'

const props = defineProps({
  currentRow: {
    type: Object as PropType<any>,
    default: () => null
  }
})

const { formRegister, formMethods } = useForm()
const { setValues, getFormData } = formMethods

const formSchema = reactive<FormSchema[]>([
  {
    field: 'full_code',
    label: 'TS股票代码',
    colProps: {
      span: 12
    },
    component: 'Input',
    componentProps: {
      placeholder: '例如: 000001.SZ'
    }
  },
  {
    field: 'stock_code',
    label: '股票代码',
    colProps: {
      span: 12
    },
    component: 'Input',
    componentProps: {
      placeholder: '例如: 000001'
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
      placeholder: '例如: 平安银行'
    }
  },
  {
    field: 'cnspell',
    label: '拼音缩写',
    colProps: {
      span: 12
    },
    component: 'Input',
    componentProps: {
      placeholder: '例如: payh'
    }
  },
  {
    field: 'area',
    label: '地域',
    colProps: {
      span: 12
    },
    component: 'Input',
    componentProps: {
      placeholder: '例如: 深圳'
    }
  },
  {
    field: 'industry',
    label: '所属行业',
    colProps: {
      span: 12
    },
    component: 'Input',
    componentProps: {
      placeholder: '例如: 银行'
    }
  },
  {
    field: 'market',
    label: '市场类型',
    colProps: {
      span: 12
    },
    component: 'Select',
    componentProps: {
      placeholder: '请选择市场类型',
      options: [
        { label: '上海', value: '上海' },
        { label: '深圳', value: '深圳' },
        { label: '北京', value: '北京' },
        { label: '创业板', value: '创业板' },
        { label: '科创板', value: '科创板' }
      ]
    }
  },
  {
    field: 'is_hs',
    label: '沪深港通',
    colProps: {
      span: 12
    },
    component: 'Select',
    componentProps: {
      placeholder: '请选择',
      options: [
        { label: '是', value: '是' },
        { label: '否', value: '否' }
      ]
    }
  },
  {
    field: 'list_date',
    label: '上市日期',
    colProps: {
      span: 12
    },
    component: 'DatePicker',
    componentProps: {
      type: 'date',
      placeholder: '请选择上市日期',
      format: 'YYYY-MM-DD',
      valueFormat: 'YYYY-MM-DD'
    }
  },
  {
    field: 'act_name',
    label: '实际控制人',
    colProps: {
      span: 12
    },
    component: 'Input',
    componentProps: {
      placeholder: '实际控制人名称'
    }
  },
  {
    field: 'act_ent_type',
    label: '控制人类型',
    colProps: {
      span: 12
    },
    component: 'Input',
    componentProps: {
      placeholder: '实际控制人企业类型'
    }
  },
  {
    field: 'status',
    label: '上市状态',
    colProps: {
      span: 12
    },
    component: 'Select',
    componentProps: {
      placeholder: '请选择上市状态',
      options: [
        { label: '上市', value: '上市' },
        { label: '退市', value: '退市' },
        { label: '暂停上市', value: '暂停上市' }
      ]
    }
  }
])

watch(
  () => props.currentRow,
  (val) => {
    if (val) {
      setValues(val)
    }
  },
  {
    deep: true,
    immediate: true
  }
)

defineExpose({
  submit: async () => {
    const formData = await getFormData()
    return formData
  }
})
</script>

<template>
  <Form :schema="formSchema" :register="formRegister" />
</template>
