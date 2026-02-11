<script setup lang="tsx">
import { reactive, watch } from 'vue'
import { Form, FormSchema } from '@/components/Form'
import { useForm } from '@/hooks/web/useForm'

const props = defineProps({
  currentRow: {
    type: Object,
    default: () => null
  }
})

const formSchema = reactive<FormSchema[]>([
  {
    field: 'verification_result',
    label: '验证结果',
    component: 'RadioGroup',
    componentProps: {
      options: [
        { label: '正确', value: '正确' },
        { label: '错误', value: '错误' },
        { label: '部分正确', value: '部分正确' }
      ]
    },
    value: '正确'
  }
])

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
  (val) => {
    if (val) {
      setValues({
        verification_result: '正确'
      })
    }
  },
  {
    immediate: true
  }
)

defineExpose({
  submit
})
</script>

<template>
  <Form @register="formRegister" :schema="formSchema" />
</template>
