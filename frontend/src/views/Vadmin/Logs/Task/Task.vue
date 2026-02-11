<script setup lang="tsx">
import { reactive, ref, unref } from 'vue'
import { useTable } from '@/hooks/web/useTable'
import { useI18n } from '@/hooks/web/useI18n'
import { Table, TableColumn } from '@/components/Table'
import { ElButton } from 'element-plus'
import { Search } from '@/components/Search'
import { FormSchema } from '@/components/Form'
import { ContentWrap } from '@/components/ContentWrap'
import Detail from './components/Detail.vue'
import { Dialog } from '@/components/Dialog'
import { selectDictLabel, DictDetail } from '@/utils/dict'
import { useDictStore } from '@/store/modules/dict'
import { useRouter } from 'vue-router'
import { getTaskRecordListApi } from '@/api/logs/task'

defineOptions({
  name: 'SystemRecordTask'
})

const { t } = useI18n()
const { currentRoute } = useRouter()

const job_id = currentRoute.value.query.job_id

const { tableRegister, tableState, tableMethods } = useTable({
  immediate: false,
  fetchDataApi: async () => {
    const { pageSize, currentPage } = tableState
    const res = await getTaskRecordListApi({
      page: unref(currentPage),
      limit: unref(pageSize),
      ...unref(searchParams)
    })
    return {
      list: res.data || [],
      total: res.count || 0
    }
  }
})

const { dataList, loading, total, pageSize, currentPage } = tableState
const { getList } = tableMethods

const tableColumns = reactive<TableColumn[]>([
  {
    field: 'id',
    label: '日志ID',
    hidden: false,
    disabled: true,
    width: '100px'
  },
  {
    field: 'job_name',
    label: '任务名称',
    hidden: false,
    disabled: true
  },
  {
    field: 'job_group',
    label: '任务分组',
    hidden: false,
    span: 2
  },
  {
    field: 'job_executor',
    label: '任务执行器',
    hidden: false
  },
  {
    field: 'invoke_target',
    label: '调用目标',
    hidden: false,
    span: 24
  },
  {
    field: 'job_args',
    label: '位置参数',
    hidden: false,
    width: '150px'
  },
  {
    field: 'job_kwargs',
    label: '关键字参数',
    hidden: false,
    width: '150px'
  },
  {
    field: 'job_trigger',
    label: '任务触发器',
    hidden: false,
    width: '180px'
  },
  {
    field: 'status',
    label: '任务状态',
    hidden: false,
    width: '100px',
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <>
            <div>{row.status ? '成功' : '失败'}</div>
          </>
        )
      }
    }
  },
  {
    field: 'job_message',
    label: '日志信息',
    hidden: false,
    span: 24
  },
  {
    field: 'exception_info',
    label: '异常信息',
    hidden: true,
    span: 24
  },
  {
    field: 'create_time',
    label: '创建时间',
    hidden: false,
    width: '180px'
  },
  {
    field: 'action',
    width: '100px',
    label: '操作',
    hidden: false,
    disabled: true,
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <>
            <ElButton type="primary" link size="small" onClick={() => view(row)}>
              详情
            </ElButton>
          </>
        )
      }
    }
  }
])

const searchSchema = reactive<FormSchema[]>([
  {
    field: 'job_id',
    label: '任务ID',
    component: 'Input',
    componentProps: {
      clearable: true,
      style: {
        width: '240px'
      }
    },
    value: job_id
  },
  {
    field: 'job_name',
    label: '任务名称',
    component: 'Input',
    componentProps: {
      clearable: true
    }
  }
])

const searchParams = ref({})
const setSearchParams = (data: any) => {
  currentPage.value = 1
  searchParams.value = data
  getList()
}

const dialogVisible = ref(false)
const dialogTitle = ref('')

const currentRow = ref()
const actionType = ref('')

const view = (row) => {
  dialogTitle.value = t('exampleDemo.detail')
  actionType.value = 'detail'
  currentRow.value = row
  dialogVisible.value = true
}

if (job_id) {
  searchParams.value = { job_id: job_id }
  getList()
} else {
  getList()
}
</script>

<template>
  <ContentWrap>
    <Search :schema="searchSchema" @reset="setSearchParams" @search="setSearchParams" />
    <Table
      v-model:current-page="currentPage"
      v-model:page-size="pageSize"
      showAction
      :columns="tableColumns"
      node-key="id"
      :data="dataList"
      :loading="loading"
      :pagination="{
        total
      }"
      @register="tableRegister"
      @refresh="getList"
    />
  </ContentWrap>

  <Dialog v-model="dialogVisible" :title="dialogTitle" width="800px">
    <Detail v-if="actionType === 'detail'" :current-row="currentRow" />

    <template #footer>
      <ElButton @click="dialogVisible = false">{{ t('dialogDemo.close') }}</ElButton>
    </template>
  </Dialog>
</template>
