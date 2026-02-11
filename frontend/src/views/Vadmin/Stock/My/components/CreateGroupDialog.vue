<script setup lang="tsx">
import { reactive, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { Form, FormSchema } from '@/components/Form'
import { useForm } from '@/hooks/web/useForm'
import { createStockGroupApi } from '@/api/stock/group'

defineOptions({
  name: 'CreateGroupDialog'
})

interface Props {
  visible: boolean
}

interface Emits {
  (e: 'update:visible', value: boolean): void
  (e: 'success'): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const { formRegister, formMethods } = useForm()
const { setValues, getElFormExpose, getFormData } = formMethods

const formSchema = reactive<FormSchema[]>([
  {
    field: 'name',
    label: '分组名称',
    component: 'Input',
    componentProps: {
      placeholder: '请输入分组名称'
    },
    formItemProps: {
      rules: [{ required: true, message: '请输入分组名称', trigger: 'blur' }]
    }
  },
  {
    field: 'remark',
    label: '描述',
    component: 'Input',
    componentProps: {
      type: 'textarea',
      rows: 3,
      placeholder: '请输入描述'
    }
  },
  {
    field: 'order',
    label: '排序',
    component: 'InputNumber',
    componentProps: {
      min: 0
    }
  }
])

const submit = async () => {
  const elForm = await getElFormExpose()
  const valid = await elForm?.validate()
  if (!valid) {
    return false
  }

  const formData = await getFormData()

  try {
    await createStockGroupApi({
      ...formData,
      status: 1
    })
    ElMessage.success('创建成功')
    emit('success')
    handleClose()
    return true
  } catch (error) {
    ElMessage.error('创建失败')
    return false
  }
}

const handleClose = () => {
  setValues({
    name: '',
    remark: '',
    order: 0
  })
  emit('update:visible', false)
}

watch(
  () => props.visible,
  (val) => {
    if (val) {
      setValues({
        name: '',
        remark: '',
        order: 0
      })
    }
  }
)

defineExpose({
  submit
})
</script>

<template>
  <Form @register="formRegister" :schema="formSchema" />
</template>
