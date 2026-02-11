<script setup lang="tsx">
import { PropType, reactive } from 'vue'
import { Descriptions, DescriptionsSchema } from '@/components/Descriptions'

defineProps({
  currentRow: {
    type: Object as PropType<Nullable<any>>,
    default: () => null
  }
})

const detailSchema = reactive<DescriptionsSchema[]>([
  {
    field: 'user_id',
    label: '操作人编号',
    width: '100px',
    span: 24
  },
  {
    field: 'user.name',
    label: '操作人',
    width: '100px',
    span: 24
  },
  {
    field: 'phone',
    label: '手机号',
    width: '130px',
    span: 24
  },
  {
    field: 'client_ip',
    label: '客户端地址',
    width: '130px',
    span: 24
  },
  {
    field: 'device.mac',
    label: '设备SN',
    span: 24
  },
  {
    field: 'message',
    label: '操作内容',
    span: 24
  },

  {
    field: 'status',
    label: '操作状态',
    width: '100px',
    span: 24
  },
  {
    field: 'browser',
    label: '浏览器',
    width: '150px',
    span: 24
  },
  {
    field: 'system',
    label: '系统',
    width: '150px',
    span: 24
  },
  {
    field: 'process_time',
    label: '总耗时',
    span: 24
  },
  {
    field: 'created_at',
    label: '操作时间',

    span: 24
  }
])
</script>

<template>
  <Descriptions :schema="detailSchema" :data="currentRow || {}" />
</template>
