<script setup lang="tsx">
import { Form, FormSchema } from '@/components/Form'
import { useForm } from '@/hooks/web/useForm'
import { PropType, reactive, watch, ref, onMounted, unref, computed } from 'vue'
import { useValidator } from '@/hooks/web/useValidator'
import { getProductOptionsApi } from '@/api/iot/product'
import { useDictStore } from '@/store/modules/dict'
import { selectDictLabel, DictDetail } from '@/utils/dict'
const { required, isTelephone, isEmail } = useValidator()
// const connectTypeOptions = ref<DictDetail[]>([])
const deviceTagOptions = ref<DictDetail[]>([])
const activeStatusOptions = ref<DictDetail[]>([])
const deviceTypeOptions = ref<DictDetail[]>([])
const areaListOptions = ref<DictDetail[]>([])
const getOptions = async () => {
  const dictStore = useDictStore()
  const dictOptions = await dictStore.getDictObj([
    'active_status',
    'device_tag',
    'device_type',
    'area_list'
  ])
  activeStatusOptions.value = dictOptions.active_status
  deviceTagOptions.value = dictOptions.device_tag
  deviceTypeOptions.value = dictOptions.device_type
  areaListOptions.value = dictOptions.area_list
}

onMounted(async () => {
  await getOptions()
  // console.log(unref(connectTypeOptions))
})

const props = defineProps({
  currentRow: {
    type: Object as PropType<any>,
    default: () => null
  }
})

const formSchema = reactive<FormSchema[]>([
  {
    field: 'ip',
    label: 'IP地址',
    colProps: {
      span: 24
    },
    component: 'Input',
    componentProps: {
      style: {
        width: '100%'
      }
    }
  },
  {
    field: 'mac',
    label: 'Mac地址',
    colProps: {
      span: 24
    },
    component: 'Input',
    componentProps: {
      style: {
        width: '100%'
      }
    }
  },
  {
    field: 'area',
    label: '区域',
    colProps: {
      span: 12
    },
    component: 'Select',
    componentProps: {
      style: {
        width: '100%'
      },
      multiple: false,
      options: areaListOptions
    },
    // optionApi: connectTypeOptions,
    value: []
    // ifshow: (values) => values.is_staff
  },
  {
    field: 'address',
    label: '地址',
    colProps: {
      span: 12
    },
    component: 'Input',
    componentProps: {
      style: {
        width: '100%'
      }
    }
  },
  {
    field: 'product_id',
    label: '产品',
    colProps: {
      span: 12
    },
    component: 'Select',
    componentProps: {
      style: {
        width: '100%'
      },
      checkStrictly: true,
      defaultExpandAll: true
    },
    optionApi: async () => {
      const res = await getProductOptionsApi()
      return res.data
    }
    // value: props.currentRow.group_id
    // ifshow: (values) => values.is_staff
  },
  {
    field: 'device_type',
    label: '设备类型',
    colProps: {
      span: 12
    },
    component: 'Select',
    componentProps: {
      style: {
        width: '100%'
      },
      multiple: false,
      options: deviceTypeOptions
    },
    // optionApi: connectTypeOptions,
    value: []
    // ifshow: (values) => values.is_staff
  },
  {
    field: 'device_tag',
    label: '标签',
    colProps: {
      span: 12
    },
    component: 'Select',
    componentProps: {
      style: {
        width: '100%'
      },
      multiple: false,
      options: deviceTagOptions
    },
    // optionApi: connectTypeOptions,
    value: []
    // ifshow: (values) => values.is_staff
  },
  {
    field: 'is_active',
    label: '是否可用',
    colProps: {
      span: 12
    },
    component: 'RadioGroup',
    // componentProps: {
    //   style: {
    //     width: '100%'
    //   },
    //   multiple: false,
    //   options: activeStatusOptions
    // },
    componentProps: {
      options: [
        {
          label: '可用',
          value: 1
        },
        {
          label: '不可用',
          value: 0
        }
      ]
    },
    // optionApi: connectTypeOptions,
    value: []
    // ifshow: (values) => values.is_staff
  },
  {
    field: 'remark',
    label: '备注',
    colProps: {
      span: 24
    },
    component: 'Input',
    componentProps: {
      style: {
        width: '100%'
      }
    }
  }
])

const rules = reactive({
  ip: [required()],
  mac: [required()],
  is_active: [required()],
  device_type: [required()],
  area: [required()]
  // dept_ids: [required()],
  // telephone: [required(), { validator: isTelephone, trigger: 'blur' }],
  // email: [{ validator: isEmail, trigger: 'blur' }]
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
console.log(formSchema)
defineExpose({
  submit
})
</script>

<template>
  <Form :rules="rules" @register="formRegister" :schema="formSchema" />
</template>
