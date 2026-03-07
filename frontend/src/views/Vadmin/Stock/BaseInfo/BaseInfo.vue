<script setup lang="tsx">
import { reactive, ref, unref } from 'vue'
import {
  getStockPageApi,
  getStockDetailApi,
  createStockApi,
  updateStockApi,
  deleteStockApi,
  exportStockApi
} from '@/api/stock/base'
import { useTable } from '@/hooks/web/useTable'
import { Table, TableColumn } from '@/components/Table'
import { ElButton, ElRow, ElCol, ElMessage } from 'element-plus'
import { Search } from '@/components/Search'
import { FormSchema } from '@/components/Form'
import { ContentWrap } from '@/components/ContentWrap'
import { Dialog } from '@/components/Dialog'
import Write from './components/Write.vue'

defineOptions({
  name: 'StockBaseInfo'
})

const sortInfo = ref<any>({})

const { tableRegister, tableState, tableMethods } = useTable({
  fetchDataApi: async () => {
    const { pageSize, currentPage } = tableState
    const res = await getStockPageApi({
      page: unref(currentPage),
      limit: unref(pageSize),
      ...unref(searchParams),
      ...unref(sortInfo)
    })
    return {
      list: res.data || [],
      total: res.count || 0
    }
  },
  fetchDelApi: async (value) => {
    const res = await deleteStockApi(value)
    return res.code === 200
  },
  fetchExportApi: async (headers) => {
    const { pageSize, currentPage } = tableState
    const res = await exportStockApi(
      {
        page: unref(currentPage),
        limit: unref(pageSize),
        ...unref(searchParams)
      },
      headers
    )
    return res
  }
})

const { dataList, loading, total, pageSize, currentPage } = tableState
const { getList, delList, exportQueryList } = tableMethods

const marketOptions = [
  { label: '上海', value: '上海' },
  { label: '深圳', value: '深圳' },
  { label: '北京', value: '北京' },
  { label: '创业板', value: '创业板' },
  { label: '科创板', value: '科创板' }
]

const hsOptions = [
  { label: '是', value: '是' },
  { label: '否', value: '否' }
]

const statusOptions = [
  { label: '上市', value: '上市' },
  { label: '退市', value: '退市' },
  { label: '暂停上市', value: '暂停上市' }
]

const tableColumns = reactive<TableColumn[]>([
  {
    field: 'selection',
    type: 'selection',
    disabled: true
  },
  {
    field: 'id',
    label: '编号',
    width: '80px',
    hidden: true
  },
  {
    field: 'full_code',
    label: 'TS代码',
    width: '120px'
  },
  {
    field: 'stock_code',
    label: '股票代码',
    width: '100px'
  },
  {
    field: 'stock_name',
    label: '股票名称',
    minWidth: '120px'
  },
  {
    field: 'area',
    label: '地域',
    width: '100px'
  },
  {
    field: 'industry',
    label: '所属行业',
    width: '120px'
  },
  {
    field: 'cnspell',
    label: '拼音缩写',
    width: '100px'
  },
  {
    field: 'market',
    label: '市场类型',
    width: '90px'
  },
  {
    field: 'list_date',
    label: '上市日期',
    width: '110px'
  },
  {
    field: 'is_hs',
    label: '沪深港通',
    width: '90px'
  },
  {
    field: 'status',
    label: '上市状态',
    width: '90px'
  },
  {
    field: 'action',
    width: '150px',
    label: '操作',
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <>
            <ElButton type="primary" link size="small" onClick={() => editAction(row)}>
              编辑
            </ElButton>
            <ElButton
              type="danger"
              link
              size="small"
              loading={delLoading.value}
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
    field: 'keywords',
    label: '关键词',
    component: 'Input',
    componentProps: {
      clearable: true,
      style: {
        width: '200px'
      }
    }
  },
  {
    field: 'stock_code',
    label: '代码',
    component: 'Input',
    componentProps: {
      clearable: true,
      style: {
        width: '150px'
      }
    }
  },
  {
    field: 'name',
    label: '名称',
    component: 'Input',
    componentProps: {
      clearable: true,
      style: {
        width: '150px'
      }
    }
  },
  {
    field: 'area',
    label: '地域',
    component: 'Input',
    componentProps: {
      clearable: true,
      style: {
        width: '120px'
      }
    }
  },
  {
    field: 'industry',
    label: '行业',
    component: 'Input',
    componentProps: {
      clearable: true,
      style: {
        width: '150px'
      }
    }
  },
  {
    field: 'market',
    label: '市场',
    component: 'Select',
    componentProps: {
      clearable: true,
      style: {
        width: '120px'
      },
      options: marketOptions
    }
  },
  {
    field: 'is_hs',
    label: '沪深港通',
    component: 'Select',
    componentProps: {
      clearable: true,
      style: {
        width: '100px'
      },
      options: hsOptions
    }
  },
  {
    field: 'status',
    label: '状态',
    component: 'Select',
    componentProps: {
      clearable: true,
      style: {
        width: '100px'
      },
      options: statusOptions
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

const dialogVisible = ref(false)
const dialogTitle = ref('')
const currentRow = ref()
const actionType = ref('')

const writeRef = ref<ComponentRef<any>>()
const saveLoading = ref(false)

const addAction = () => {
  dialogTitle.value = '新增股票'
  actionType.value = 'add'
  currentRow.value = undefined
  dialogVisible.value = true
}

const editAction = async (row: any) => {
  const res = await getStockDetailApi(row.id)
  if (res) {
    dialogTitle.value = '编辑股票'
    actionType.value = 'edit'
    currentRow.value = res.data
    dialogVisible.value = true
  }
}

const save = async () => {
  const write = unref(writeRef)
  const formData = await write?.submit()
  if (formData) {
    saveLoading.value = true
    try {
      const res = ref({})
      if (actionType.value === 'add') {
        res.value = await createStockApi(formData)
        if (res.value) {
          dialogVisible.value = false
          await getList()
          ElMessage.success('添加成功!')
        }
      } else if (actionType.value === 'edit') {
        res.value = await updateStockApi(formData)
        if (res.value) {
          dialogVisible.value = false
          await getList()
          ElMessage.success('编辑成功!')
        }
      }
    } finally {
      saveLoading.value = false
    }
  }
}
</script>

<template>
  <ContentWrap>
    <Search :schema="searchSchema" @reset="resetSearchParams" @search="setSearchParams" />
    <ElRow :gutter="10" :justify="'start'" class="mt-10px">
      <ElCol :span="1.5">
        <ElButton type="primary" @click="addAction">新增股票</ElButton>
      </ElCol>
      <ElCol :span="1.5">
        <ElButton @click="exportQueryList()">导出数据</ElButton>
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
      :loading="loading"
      :pagination="{
        total
      }"
      @register="tableRegister"
      @refresh="getList"
    />
  </ContentWrap>

  <Dialog v-model="dialogVisible" :title="dialogTitle" :width="700">
    <Write
      v-if="actionType === 'add' || actionType === 'edit'"
      ref="writeRef"
      :current-row="currentRow"
    />

    <template #footer v-if="actionType === 'add' || actionType === 'edit'">
      <ElButton type="primary" :loading="saveLoading" @click="save"> 保存 </ElButton>
      <ElButton @click="dialogVisible = false">关闭</ElButton>
    </template>
  </Dialog>
</template>
