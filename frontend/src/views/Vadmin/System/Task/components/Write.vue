<script setup lang="tsx">
import { Form, FormSchema } from '@/components/Form'
import { useForm } from '@/hooks/web/useForm'
import { PropType, reactive, watch } from 'vue'
import { useValidator } from '@/hooks/web/useValidator'
import { useDictStore } from '@/store/modules/dict'
import { getTaskGroupOptionsApi } from '@/api/system/task'

const { required } = useValidator()

const props = defineProps({
  currentRow: {
    type: Object as PropType<any>,
    default: () => null
  }
})

const formSchema = reactive<FormSchema[]>([
  {
    field: 'name',
    label: '任务名称',
    component: 'Input',
    colProps: {
      span: 12
    },
    componentProps: {
      style: {
        width: '100%'
      }
    },
    formItemProps: {
      rules: [required()]
    }
  },
  {
    field: 'task_group_id',
    label: '任务分组',
    colProps: {
      span: 12
    },
    component: 'Select',
    componentProps: {
      style: {
        width: '100%'
      },
      allowCreate: true,
      filterable: true,
      defaultFirstOption: true,
      placeholder: '请选择任务分组，支持直接输入添加'
    },
    optionApi: async () => {
      const res = await getTaskGroupOptionsApi()
      const options = res.data.map((item) => ({ label: item.name, value: item.id }))
      return options
    }
  },
  {
    field: 'job_class',
    label: '调用目标',
    component: 'Input',
    colProps: {
      span: 24
    },
    componentProps: {
      style: {
        width: '100%'
      },
      placeholder:
        'schedule.Test("kinit", 1314, True)；参数仅支持字符串，整数，浮点数，布尔类型。约定使用apps.module_task目录下模块'
    },
    labelMessage: 'schedule.Test("kinit", 1314, True)<br/>参数仅支持字符串，整数，浮点数，布尔类型',
    formItemProps: {
      rules: [required()]
    }
  },
  {
    field: 'trigger',
    label: '触发器类型',
    colProps: {
      span: 12
    },
    component: 'RadioGroup',
    componentProps: {
      style: {
        width: '100%'
      }
    },
    value: 'cron',
    formItemProps: {
      rules: [required()]
    },
    optionApi: async () => {
      const dictStore = useDictStore()
      const dictOptions = await dictStore.getDictObj(['system_task_trigger'])
      return dictOptions.system_task_trigger
    }
  },
  {
    field: 'executor',
    label: '执行器',
    component: 'Select',
    colProps: {
      span: 12
    },
    componentProps: {
      style: {
        width: '100%'
      },
      placeholder: '请选择执行器'
    },
    formItemProps: {
      rules: [required()]
    },
    optionApi: async () => {
      const dictStore = useDictStore()
      const dictOptions = await dictStore.getDictObj(['system_task_executor'])
      return dictOptions.system_task_executor || [{ label: 'default', value: 'default' }]
    }
  },
  {
    field: 'trigger_args',
    label: 'Cron 表达式',
    component: 'Input',
    colProps: {
      span: 24
    },
    componentProps: {
      style: {
        width: '100%'
      },
      placeholder: 'cron 表达式，六位或七位，分别表示秒、分钟、小时、天、月、星期几、年(可选)'
    },
    ifshow: (values) => values.trigger === 'cron',
    formItemProps: {
      rules: [required()]
    }
  },
  {
    field: 'trigger_args',
    label: 'Interval 表达式',
    component: 'Input',
    colProps: {
      span: 24
    },
    componentProps: {
      style: {
        width: '100%'
      },
      placeholder:
        'interval 表达式，五位，分别为：秒 分 时 天 周，例如：10 * * * * 表示每隔 10 秒执行一次任务。'
    },
    ifshow: (values) => values.trigger === 'interval',
    formItemProps: {
      rules: [required()]
    }
  },
  {
    field: 'trigger_args',
    label: 'Date 表达式',
    component: 'DatePicker',
    colProps: {
      span: 24
    },
    componentProps: {
      style: {
        width: '100%'
      },
      type: 'datetime',
      format: 'YYYY-MM-DD HH:mm:ss',
      valueFormat: 'YYYY-MM-DD HH:mm:ss',
      placeholder: '请选择执行时间'
    },
    ifshow: (values) => values.trigger === 'date',
    formItemProps: {
      rules: [required()]
    }
  },
  {
    field: 'start_date',
    label: '开始时间',
    colProps: {
      span: 12
    },
    component: 'DatePicker',
    componentProps: {
      style: {
        width: '100%'
      },
      type: 'datetime',
      format: 'YYYY-MM-DD HH:mm:ss',
      valueFormat: 'YYYY-MM-DD HH:mm:ss'
    },
    ifshow: (values) => values.trigger !== 'date'
  },
  {
    field: 'end_date',
    label: '结束时间',
    colProps: {
      span: 12
    },
    component: 'DatePicker',
    componentProps: {
      style: {
        width: '100%'
      },
      type: 'datetime',
      format: 'YYYY-MM-DD HH:mm:ss',
      valueFormat: 'YYYY-MM-DD HH:mm:ss'
    },
    ifshow: (values) => values.trigger !== 'date'
  },
  {
    field: 'args',
    label: '位置参数',
    component: 'Input',
    colProps: {
      span: 12
    },
    componentProps: {
      style: {
        width: '100%'
      },
      type: 'textarea',
      rows: '2',
      placeholder: '位置参数，如：param1,param2'
    }
  },
  {
    field: 'kwargs',
    label: '关键字参数',
    component: 'Input',
    colProps: {
      span: 12
    },
    componentProps: {
      style: {
        width: '100%'
      },
      type: 'textarea',
      rows: '2',
      placeholder: '关键字参数，如：{"key1": "value1"}'
    }
  },
  {
    field: 'coalesce',
    label: '合并运行',
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
          label: '是',
          value: true
        },
        {
          label: '否',
          value: false
        }
      ]
    },
    value: false
  },
  {
    field: 'max_instances',
    label: '最大实例数',
    component: 'InputNumber',
    colProps: {
      span: 12
    },
    componentProps: {
      style: {
        width: '100%'
      },
      min: 1,
      max: 100,
      placeholder: '允许的最大并发执行实例数'
    },
    value: 1,
    formItemProps: {
      rules: [required()]
    }
  },
  {
    field: 'status',
    label: '任务状态',
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
          label: '启用',
          value: true
        },
        {
          label: '禁用',
          value: false
        }
      ]
    },
    value: true,
    formItemProps: {
      rules: [required()]
    }
  },
  {
    field: 'jobstore',
    label: '存储器',
    colProps: {
      span: 12
    },
    component: 'Input',
    componentProps: {
      style: {
        width: '100%'
      },
      placeholder: '请选择存储器'
    },
    labelMessage:
      '创建或更新任务完成后，如果任务状态与设置的不符，请尝试刷新数据或查看调度日志，<br/>任务状态可能会有延迟(几秒)',
    value: 'default'
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
  <Form @register="formRegister" :schema="formSchema" />
</template>
