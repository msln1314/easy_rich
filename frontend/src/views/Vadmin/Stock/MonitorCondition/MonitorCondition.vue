<script setup lang="tsx">
import { reactive, ref, unref } from 'vue'
import {
  getMonitorConditionListApi,
  delMonitorConditionApi,
  postExportMonitorConditionApi,
  updateActiveStatusApi
} from '@/api/stock/monitor_condition'
import { useTable } from '@/hooks/web/useTable'
import { Table, TableColumn } from '@/components/Table'
import { ElButton, ElRow, ElCol, ElDialog, ElMessage, ElSwitch } from 'element-plus'
import { Search } from '@/components/Search'
import dayjs from 'dayjs'
import { FormSchema } from '@/components/Form'
import { ContentWrap } from '@/components/ContentWrap'
import { useRouter } from 'vue-router'
import MonitorConditionForm from './components/MonitorConditionForm.vue'

defineOptions({
  name: 'StockMonitorCondition'
})

const { push } = useRouter()

// 表单对话框
const dialogVisible = ref(false)
const dialogTitle = ref('新增条件选股')
const formRef = ref()
const currentRow = ref<any>(null)

const { tableRegister, tableState, tableMethods } = useTable({
  fetchDataApi: async () => {
    const { pageSize, currentPage } = tableState
    const res = await getMonitorConditionListApi({
      page: unref(currentPage),
      limit: unref(pageSize),
      ...unref(searchParams)
    })
    return {
      list: res.data || [],
      total: res.count || 0
    }
  },
  fetchDelApi: async (value) => {
    const res = await delMonitorConditionApi(value)
    return res.code === 200
  },
  fetchExportApi: async (headers) => {
    const { pageSize, currentPage } = tableState
    const res = await postExportMonitorConditionApi(
      {
        ...unref(searchParams)
      },
      headers
    )
    return res
  }
})

const { dataList, loading, total, pageSize, currentPage } = tableState
const { getList, delList, exportQueryList } = tableMethods

const tableColumns = reactive<TableColumn[]>([
  {
    field: 'id',
    label: '编号',
    width: '80px',
    hidden: true
  },
  {
    field: 'name',
    label: '监控名称',
    minWidth: '150px',
    sortable: true
  },
  {
    field: 'condition_content',
    label: '监控条件',
    minWidth: '300px'
  },
  {
    field: 'tag',
    label: '标签',
    width: '120px'
  },
  {
    field: 'owner',
    label: '拥有者',
    width: '120px'
  },
  {
    field: 'reason',
    label: '条件原因',
    minWidth: '200px'
  },
  {
    field: 'watch_days',
    label: '关注天数',
    width: '100px'
  },
  {
    field: 'is_active',
    label: '启用状态',
    width: '100px',
    sortable: true,
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <ElSwitch
            v-model={row.is_active}
            activeValue={1}
            inactiveValue={0}
            onChange={(val: number) => handleStatusChange(row, val === 1)}
          />
        )
      }
    }
  },
  {
    field: 'remark',
    label: '备注',
    minWidth: '200px'
  },
  {
    field: 'created_at',
    label: '创建时间',
    width: '160px',
    formatter: (row: any) => dayjs(row.created_at).format('YYYY-MM-DD HH:mm:ss'),
    sortable: true
  },
  {
    field: 'updated_at',
    label: '更新时间',
    width: '160px',
    formatter: (row: any) => dayjs(row.updated_at).format('YYYY-MM-DD HH:mm:ss'),
    sortable: true
  },
  {
    field: 'action',
    width: '200px',
    label: '操作',
    fixed: 'right',
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <>
            <ElButton type="primary" link size="small" onClick={() => editAction(row)}>
              编辑
            </ElButton>
            <ElButton type="success" link size="small" onClick={() => copyAction(row)}>
              复制
            </ElButton>
            <ElButton
              type="danger"
              loading={delLoading.value}
              link
              size="small"
              onClick={() => delData(row)}
            >
              删除
            </ElButton>
          </>
        )
      }
    }
  }
])

const searchSchema = reactive<FormSchema[]>([
  {
    field: 'name',
    label: '监控名称',
    component: 'Input',
    componentProps: {
      clearable: true,
      style: {
        width: '214px'
      }
    }
  },
  {
    field: 'tag',
    label: '标签',
    component: 'Input',
    componentProps: {
      clearable: true,
      style: {
        width: '214px'
      }
    }
  },
  {
    field: 'owner',
    label: '拥有者',
    component: 'Input',
    componentProps: {
      clearable: true,
      style: {
        width: '214px'
      }
    }
  },
  {
    field: 'reason',
    label: '条件原因',
    component: 'Input',
    componentProps: {
      clearable: true,
      style: {
        width: '214px'
      }
    }
  },
  {
    field: 'is_active',
    label: '启用状态',
    component: 'Select',
    componentProps: {
      style: {
        width: '214px'
      },
      options: [
        {
          label: '启用',
          value: 1
        },
        {
          label: '禁用',
          value: 0
        }
      ]
    }
  }
])

const searchParams = ref({})
const setSearchParams = (data: any) => {
  currentPage.value = 1
  searchParams.value = data
  getList()
}

const resetSearchParams = () => {
  currentPage.value = 1
  searchParams.value = {}
  getList()
}

const delLoading = ref(false)

const delData = async (row?: any) => {
  delLoading.value = true
  if (row) {
    await delList(true, [row.id]).finally(() => {
      delLoading.value = false
    })
  } else {
    await delList(true).finally(() => {
      delLoading.value = false
    })
  }
}

const editAction = (row: any) => {
  currentRow.value = row
  dialogTitle.value = '编辑条件选股'
  dialogVisible.value = true
}

const copyAction = (row: any) => {
  currentRow.value = { ...row, id: undefined }
  dialogTitle.value = '复制条件选股'
  dialogVisible.value = true
}

const handleStatusChange = async (row: any, value: boolean) => {
  try {
    await updateActiveStatusApi({ id: row.id, is_active: value ? 1 : 0 })
    // ElMessage.success(value ? '已启用' : '已禁用')
    getList()
  } catch (error: any) {
    ElMessage.error('操作失败')
    getList()
  }
}

const addAction = () => {
  currentRow.value = null
  dialogTitle.value = '新增条件选股'
  dialogVisible.value = true
}

const handleSubmit = async () => {
  try {
    const formData = await formRef.value?.submit()
    if (formData) {
      ElMessage.success(dialogTitle.value === '编辑条件选股' ? '编辑成功' : '新增成功')
      dialogVisible.value = false
      getList()
    }
  } catch (error: any) {
    console.error('提交失败:', error)
    ElMessage.error(error.response?.data?.detail || '操作失败，请稍后重试')
  }
}
</script>

<template>
  <ContentWrap>
    <Search :schema="searchSchema" @reset="resetSearchParams" @search="setSearchParams" />
    <ElRow :gutter="10" :justify="'start'" class="mt-4">
      <ElCol :span="1.5">
        <ElButton type="primary" @click="addAction">新增</ElButton>
      </ElCol>
      <ElCol :span="1.5">
        <ElButton @click="exportQueryList()">导出</ElButton>
      </ElCol>
      <ElCol :span="1.5">
        <ElButton type="danger" @click="delData(null)">批量删除</ElButton>
      </ElCol>
    </ElRow>
    <Table
      v-model:current-page="currentPage"
      v-model:page-size="pageSize"
      :columns="tableColumns"
      :data="dataList"
      :showAction="true"
      :loading="loading"
      :pagination="{
        total
      }"
      @register="tableRegister"
      @refresh="getList"
    />
    <ElDialog v-model="dialogVisible" :title="dialogTitle" width="800px" destroy-on-close>
      <MonitorConditionForm :currentRow="currentRow" ref="formRef" />
      <template #footer>
        <ElButton @click="dialogVisible = false">取消</ElButton>
        <ElButton type="primary" @click="handleSubmit">确定</ElButton>
      </template>
    </ElDialog>
  </ContentWrap>
</template>
