<script setup lang="tsx">
import { Form, FormSchema } from '@/components/Form'
import { useForm } from '@/hooks/web/useForm'
import { PropType, reactive, watch } from 'vue'
import { useValidator } from '@/hooks/web/useValidator'
import { propTypes } from '@/utils/propTypes'
import { getClientGroupTreeOptionsApi } from '@/api/iot/client_group'

const { required } = useValidator()

const props = defineProps({
  currentRow: {
    type: Object as PropType<any>,
    default: () => null
  },
  parentId: propTypes.number.def(undefined)
})

const formSchema = reactive<FormSchema[]>([
  {
    field: 'parent_id',
    label: '上级组',
    colProps: {
      span: 24
    },
    component: 'TreeSelect',
    componentProps: {
      style: {
        width: '100%'
      },
      checkStrictly: true,
      placeholder: '请选择上级组',
      nodeKey: 'value',
      defaultExpandAll: true
    },
    optionApi: async () => {
      const res = await getClientGroupTreeOptionsApi()
      return res.data
    },
    value: props.parentId
  },
  {
    field: 'name',
    label: '分组名称',
    component: 'Input',
    colProps: {
      span: 12
    }
  },

  {
    field: 'remak',
    label: '描述',
    component: 'Input',
    colProps: {
      span: 12
    }
  },
  {
    field: 'order',
    label: '显示排序',
    component: 'InputNumber',
    colProps: {
      span: 12
    },
    componentProps: {
      style: {
        width: '100%'
      }
    }
  },
  {
    field: 'status',
    label: '是否启用',
    colProps: {
      span: 12
    },
    component: 'RadioGroup',
    componentProps: {
      style: {
        width: '100%'
      },
      options: [
        {
          label: '正常',
          value: true
        },
        {
          label: '停用',
          value: false
        }
      ]
    },
    value: false
  }
])

const rules = reactive({
  name: [required()],
  status: [required()],
  order: [required()]
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
    setValues(currentRow)
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
  <Form :rules="rules" @register="formRegister" :schema="formSchema" :labelWidth="100" />
</template>
