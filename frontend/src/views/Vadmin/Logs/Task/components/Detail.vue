<script setup lang="tsx">
import { PropType, reactive } from 'vue'
import { Descriptions, DescriptionsSchema } from '@/components/Descriptions'
import 'vue3-json-viewer/dist/index.css'

defineProps({
  currentRow: {
    type: Object as PropType<Nullable<any>>,
    default: () => null
  }
})

const detailSchema = reactive<DescriptionsSchema[]>([
  {
    field: 'id',
    label: '日志ID',
    width: '200px',
    span: 12
  },
  {
    field: 'job_id',
    label: '任务ID',
    span: 12
  },
  {
    field: 'job_name',
    label: '任务名称',
    span: 24
  },
  {
    field: 'job_group',
    label: '任务分组',
    span: 12
  },
  {
    field: 'job_executor',
    label: '任务执行器',
    span: 12
  },
  {
    field: 'invoke_target',
    label: '调用目标',
    span: 24
  },
  {
    field: 'job_args',
    label: '位置参数',
    span: 12
  },
  {
    field: 'job_kwargs',
    label: '关键字参数',
    span: 12
  },
  {
    field: 'job_trigger',
    label: '任务触发器',
    span: 24
  },
  {
    field: 'status',
    label: '任务状态',
    span: 12,
    slots: {
      default: (data: any) => {
        return (
          <>
            <div>{data.status ? '成功' : '失败'}</div>
          </>
        )
      }
    }
  },
  {
    field: 'create_time',
    label: '创建时间',
    span: 12
  },
  {
    field: 'job_message',
    label: '日志信息',
    span: 24
  },
  {
    field: 'exception_info',
    label: '异常信息',
    span: 24
  }
])
</script>

<template>
  <Descriptions :schema="detailSchema" :data="currentRow || {}" />
</template>
