<script setup lang="tsx">
import { Form, FormSchema } from '@/components/Form'
import { useForm } from '@/hooks/web/useForm'
import { PropType, reactive, watch, ref, onMounted, unref, computed } from 'vue'
import { useValidator } from '@/hooks/web/useValidator'
import { getDeviceOptionsApi } from '@/api/iot/device'
import { getClientGroupTreeOptionsApi } from '@/api/iot/client_group'
import { useDictStore } from '@/store/modules/dict'
import { selectDictLabel, DictDetail } from '@/utils/dict'
const { required, isTelephone, isEmail } = useValidator()
const connectTypeOptions = ref<DictDetail[]>([])
const connectPortOptions = ref<DictDetail[]>([])
const connectProtocolOptions = ref<DictDetail[]>([])
const deviceOptions = ref<DictDetail[]>([])
const connectModelOptions = ref<DictDetail[]>([])
const getOptions = async () => {
  const dictStore = useDictStore()
  const dictOptions = await dictStore.getDictObj([
    'connect_type',
    'connect_port',
    'connect_protocol',
    'connect_model'
  ])
  console.log('connect_type', dictOptions.connect_port)
  connectTypeOptions.value = dictOptions.connect_type
  connectPortOptions.value = dictOptions.connect_port
  connectProtocolOptions.value = dictOptions.connect_protocol
  connectModelOptions.value = dictOptions.connect_model
}

onMounted(async () => {
  await getOptions()
  console.log(unref(connectTypeOptions))
})

const props = defineProps({
  currentRow: {
    type: Object as PropType<any>,
    default: () => null
  }
})

const formSchema = reactive<FormSchema[]>([
  {
    field: 'name',
    label: '名称',
    colProps: {
      span: 24
    },
    component: 'Input',
    componentProps: {
      style: {
        width: '100%'
      },
      placeholder: '请输入名称',
      readonly: true,
      disabled: true
    }
  },
  {
    field: 'sn',
    label: '桩号',
    colProps: {
      span: 24
    },
    component: 'Input',
    componentProps: {
      style: {
        width: '100%'
      },
      // readonly: true
      readonly: true,
      disabled: true
    }
  },

  {
    field: 'device_id',
    label: '设备',
    colProps: {
      span: 16
    },
    component: 'SelectV2',
    componentProps: {
      style: {
        width: '100%'
      },
      placeholder: '请输入设备MAC搜索',

      multiple: false,
      clearable: true,
      remote: true,
      filterable: true,
      options: deviceOptions,
      remoteMethod: async (query) => {
        console.log(query)
        const params = { keywords: query, page: 1, limit: 20, device_type: '4g_io' }
        const res = await getDeviceOptionsApi(params)
        const options = res.data.map((item) => {
          return { label: `${item.ip} ${item.mac}`, value: item.id }
        })
        deviceOptions.value = options
        return options
      },
      props: { label: 'ip', value: 'id' }
    },

    // optionApi: async () => {
    //   const res = await getDeviceOptionsApi()
    //   const options = res.data.map((item) => {
    //     return { label: `${item.ip} ${item.mac}`, value: item.id }
    //   })
    //   return options
    // },
    value: []
    // ifshow: (values) => values.is_staff
  },
  {
    field: 'port',
    label: '连接端口',
    colProps: {
      span: 8
    },
    component: 'Select',
    componentProps: {
      style: {
        width: '100%'
      },
      multiple: false,
      options: connectPortOptions
    },

    value: []
    // ifshow: (values) => values.is_staff
  },
  {
    field: 'connect_model',
    label: '连接模式',
    colProps: {
      span: 12
    },
    component: 'Select',
    componentProps: {
      style: {
        width: '100%'
      },
      multiple: false,
      options: connectModelOptions
    },
    value: []
  },
  {
    field: 'connect_type',
    label: '连接类型',
    colProps: {
      span: 12
    },
    component: 'Select',
    componentProps: {
      style: {
        width: '100%'
      },
      multiple: false,
      options: connectTypeOptions
    },
    // optionApi: connectTypeOptions,
    value: []
    // ifshow: (values) => values.is_staff
  },

  {
    field: 'connect_protocol',
    label: '连接协议',
    colProps: {
      span: 12
    },
    component: 'Select',
    componentProps: {
      style: {
        width: '100%'
      },
      multiple: false,
      options: connectProtocolOptions
    },

    value: []
    // ifshow: (values) => values.is_staff
  }
])

const rules = reactive({
  name: [required()],
  sn: [required()],
  port: [required()],
  device_id: [required()],
  connect_type: [required()],
  connect_protocol: [required()],
  connect_model: [required()]
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
