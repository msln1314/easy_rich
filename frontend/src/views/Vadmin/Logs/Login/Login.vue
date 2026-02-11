<script setup lang="tsx">
import { reactive, ref, unref } from 'vue'
import { getLogLoginListApi } from '@/api/logs/login'
import { useTable } from '@/hooks/web/useTable'
import { useI18n } from '@/hooks/web/useI18n'
import { Table, TableColumn } from '@/components/Table'
import { ElButton, ElSwitch } from 'element-plus'
import { Search } from '@/components/Search'
import { FormSchema } from '@/components/Form'
import { ContentWrap } from '@/components/ContentWrap'
import Detail from './components/Detail.vue'
import { Dialog } from '@/components/Dialog'
import { selectDictLabel, DictDetail } from '@/utils/dict'
import { useDictStore } from '@/store/modules/dict'

defineOptions({
  name: 'SystemRecordLogin'
})

const { t } = useI18n()

const platformOptions = ref<DictDetail[]>([])
const loginMethodOptions = ref<DictDetail[]>([])

const getOptions = async () => {
  const dictStore = useDictStore()
  const dictOptions = await dictStore.getDictObj(['sys_platform', 'sys_login_method'])
  platformOptions.value = dictOptions.sys_platform
  loginMethodOptions.value = dictOptions.sys_login_method
}

getOptions()

const { tableRegister, tableState, tableMethods } = useTable({
  fetchDataApi: async () => {
    const { pageSize, currentPage } = tableState
    const res = await getLogLoginListApi({
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
    label: '编号',
    hidden: false,
    disabled: true,
    width: '120px'
  },
  {
    field: 'username',
    label: '用户名',
    width: '150px',
    hidden: false,
    disabled: true,
    sortable: 'custom'
  },
  {
    field: 'status',
    label: '登录状态',
    hidden: false,
    slots: {
      default: (data: any) => {
        return (
          <>
            <ElSwitch value={data.row.status} size="small" disabled />
          </>
        )
      }
    }
  },
  {
    field: 'platform',
    label: '登录平台',
    width: '150px',
    hidden: false,
    slots: {
      default: (data: any) => {
        return (
          <>
            <div>{selectDictLabel(platformOptions.value, data.row.platform)}</div>
          </>
        )
      }
    }
  },
  {
    field: 'login_method',
    label: '认证方式',
    width: '150px',
    hidden: false,
    slots: {
      default: (data: any) => {
        return (
          <>
            <div>{selectDictLabel(loginMethodOptions.value, data.row.login_method)}</div>
          </>
        )
      }
    }
  },
  {
    field: 'ip',
    label: '登录地址',
    hidden: false,
    disabled: true,
    width: '150px',
    sortable: 'custom'
  },
  {
    field: 'address',
    label: '登录地点',
    hidden: false
  },
  {
    field: 'postal_code',
    label: '邮政编码',
    hidden: true
  },
  {
    field: 'area_code',
    label: '地区区号',
    hidden: true
  },
  {
    field: 'browser',
    label: '浏览器',
    hidden: false
  },
  {
    field: 'system',
    label: '操作系统',
    hidden: false
  },
  {
    field: 'response',
    label: '响应信息',
    hidden: true,
    disabled: true
  },
  {
    field: 'request',
    label: '请求信息',
    hidden: true,
    disabled: true
  },
  {
    field: 'created_at',
    label: '创建时间',
    hidden: false,
    sortable: 'custom'
  },
  {
    field: 'action',
    label: '操作',
    hidden: false,
    width: 100,
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <>
            <ElButton type="primary" link onClick={() => action(row, 'detail')}>
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
    field: 'username',
    label: '用户名',
    component: 'Input',
    componentProps: {
      clearable: false,
      style: {
        width: '214px'
      }
    }
  },
  {
    field: 'platform',
    label: '登录平台',
    component: 'Select',
    componentProps: {
      style: {
        width: '214px'
      },
      options: platformOptions.value
    }
  },
  {
    field: 'ip',
    label: '登录地址',
    component: 'Input',
    componentProps: {
      clearable: false,
      style: {
        width: '214px'
      }
    }
  },
  {
    field: 'address',
    label: '登录地点',
    component: 'Input',
    componentProps: {
      clearable: false,
      style: {
        width: '214px'
      }
    }
  },
  {
    field: 'status',
    label: '登录状态',
    component: 'Select',
    componentProps: {
      style: {
        width: '214px'
      },
      options: [
        {
          label: '登录成功',
          value: true
        },
        {
          label: '登录失败',
          value: false
        }
      ]
    }
  }
])

const searchParams = ref({ order: 'desc', prop: 'id' })
const setSearchParams = (data: any) => {
  currentPage.value = 1
  searchParams.value = data
  getList()
}

const dialogVisible = ref(false)
const dialogTitle = ref('')

const currentRow = ref()
const actionType = ref('')
const sortChange = (column) => {
  console.log(column)
  if (column.order === 'descending') {
    searchParams.value.order = 'desc'
    searchParams.value.prop = column.prop
  } else {
    searchParams.value.order = 'asc'
    searchParams.value.prop = column.prop
  }
  getList()
}
const action = (row: any, type: string) => {
  dialogTitle.value = t('exampleDemo.detail')
  actionType.value = type
  currentRow.value = row
  dialogVisible.value = true
}
</script>

<template>
  <ContentWrap>
    <Search :schema="searchSchema" @reset="setSearchParams" @search="setSearchParams" />
    <Table
      v-model:current-page="currentPage"
      v-model:page-size="pageSize"
      @sort-change="sortChange"
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
@/api/log/login
