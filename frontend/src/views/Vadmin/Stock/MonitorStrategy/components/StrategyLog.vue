<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { getMonitorStrategyLogsApi } from '@/api/stock/monitor_strategy'
import { Table, TableColumn } from '@/components/Table'
import { useTable } from '@/hooks/web/useTable'
import dayjs from 'dayjs'
import { ContentWrap } from '@/components/ContentWrap'

defineProps<{
  strategyId?: number | null
}>()

// 策略类型映射
const strategyTypeMap: Record<string, string> = {
  limit_up: '涨停监听',
  limit_down: '跌停监听',
  open_board: '开板监听',
  turnover: '换手监听',
  breakout: '突破监听',
  rebound: '反弹监听'
}

// 推送方式映射
const notifyMethodMap: Record<string, string> = {
  system: '系统消息',
  email: '邮件',
  sms: '短信',
  wechat: '微信'
}

// 推送状态映射
const notifyStatusMap: Record<number, { label: string; type: any }> = {
  0: { label: '待推送', type: 'info' },
  1: { label: '推送成功', type: 'success' },
  2: { label: '推送失败', type: 'danger' }
}

const { tableRegister, tableState, tableMethods } = useTable({
  fetchDataApi: async () => {
    const { pageSize, currentPage } = tableState
    const res = await getMonitorStrategyLogsApi({
      page: unref(currentPage),
      limit: unref(pageSize),
      strategy_id: props.strategyId
    })
    return {
      list: res.data || [],
      total: res.count || 0
    }
  }
})

const { dataList, loading, total, pageSize, currentPage } = tableState
const { getList } = tableMethods

const tableColumns = computed(() => [
  {
    field: 'id',
    label: '编号',
    width: '80px'
  },
  {
    field: 'strategy_name',
    label: '策略名称',
    minWidth: '120px'
  },
  {
    field: 'stock_code',
    label: '股票代码',
    width: '100px'
  },
  {
    field: 'stock_name',
    label: '股票名称',
    width: '120px'
  },
  {
    field: 'strategy_type',
    label: '策略类型',
    width: '100px',
    formatter: (row: any) => strategyTypeMap[row.strategy_type]
  },
  {
    field: 'trigger_time',
    label: '触发时间',
    width: '160px',
    formatter: (row: any) => dayjs(row.trigger_time).format('YYYY-MM-DD HH:mm:ss')
  },
  {
    field: 'trigger_count',
    label: '触发次数',
    width: '100px'
  },
  {
    field: 'trigger_condition',
    label: '触发条件',
    minWidth: '150px'
  },
  {
    field: 'trigger_value',
    label: '触发值',
    width: '100px'
  },
  {
    field: 'trigger_percent',
    label: '触发百分比(%)',
    width: '120px'
  },
  {
    field: 'price',
    label: '价格',
    width: '100px'
  },
  {
    field: 'change_percent',
    label: '涨跌幅(%)',
    width: '100px'
  },
  {
    field: 'volume',
    label: '成交量',
    width: '120px'
  },
  {
    field: 'turnover_rate',
    label: '换手率(%)',
    width: '100px'
  },
  {
    field: 'notify_status',
    label: '推送状态',
    width: '100px',
    slots: { default: 'notifyStatus' }
  },
  {
    field: 'notify_time',
    label: '推送时间',
    width: '160px',
    formatter: (row: any) =>
      row.notify_time ? dayjs(row.notify_time).format('YYYY-MM-DD HH:mm:ss') : '-'
  },
  {
    field: 'notify_method',
    label: '推送方式',
    width: '100px',
    formatter: (row: any) => notifyMethodMap[row.notify_method] || '-'
  },
  {
    field: 'error_message',
    label: '错误信息',
    minWidth: '150px'
  },
  {
    field: 'remark',
    label: '备注',
    minWidth: '150px'
  }
])

onMounted(() => {
  if (props.strategyId) {
    getList()
  }
})
</script>

<template>
  <ContentWrap>
    <Table
      v-model:current-page="currentPage"
      v-model:page-size="pageSize"
      :columns="tableColumns"
      :data="dataList"
      :loading="loading"
      :pagination="{ total }"
      @register="tableRegister"
    >
      <template #notifyStatus="{ row }">
        <el-tag :type="notifyStatusMap[row.notify_status].type">
          {{ notifyStatusMap[row.notify_status].label }}
        </el-tag>
      </template>
    </Table>
  </ContentWrap>
</template>
