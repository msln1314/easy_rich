<script setup lang="tsx">
import { reactive, ref, unref } from 'vue'
import {
  getClientGroupListApi,
  delClientGroupListApi,
  addClientGroupListApi,
  putClientGroupListApi
} from '@/api/iot/client_group'
import { useTable } from '@/hooks/web/useTable'
import { useI18n } from '@/hooks/web/useI18n'
import { Table, TableColumn } from '@/components/Table'
import { ElButton, ElSwitch, ElRow, ElCol, ElMessage } from 'element-plus'
import { ContentWrap } from '@/components/ContentWrap'
import Write from './components/Write.vue'
import { Dialog } from '@/components/Dialog'

defineOptions({
  name: 'IotClientGroup'
})

const { t } = useI18n()

const { tableRegister, tableState, tableMethods } = useTable({
  fetchDataApi: async () => {
    const { pageSize, currentPage } = tableState
    const res = await getClientGroupListApi({
      page: unref(currentPage),
      limit: unref(pageSize)
    })
    return {
      list: res.data || [],
      total: res.count || 0
    }
  },
  fetchDelApi: async (value) => {
    const res = await delClientGroupListApi(value)
    return res.code === 200
  }
})

const { dataList, loading } = tableState
const { getList, delList } = tableMethods

const tableColumns = reactive<TableColumn[]>([
  {
    field: 'name',
    label: '分组名称',
    disabled: true,
    hidden: false
  },

  {
    field: 'remark',
    label: '描述',
    hidden: false
  },
  {
    field: 'order',
    label: '排序',
    width: '120px',
    hidden: false
  },
  {
    field: 'status',
    label: '状态',
    width: '120px',
    hidden: false,
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <>
            <ElSwitch model-value={row.status} disabled />
          </>
        )
      }
    }
  },
  {
    field: 'action',
    width: '200px',
    label: '操作',
    hidden: false,
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <>
            <ElButton type="primary" link size="small" onClick={() => editAction(row)}>
              编辑
            </ElButton>
            <ElButton type="primary" link size="small" onClick={() => addSonAction(row)}>
              添加子组
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

const delLoading = ref(false)

const delData = async (row: any) => {
  delLoading.value = true
  await delList(true, [row.id]).finally(() => {
    delLoading.value = false
  })
}

const dialogVisible = ref(false)
const dialogTitle = ref('')

const currentRow = ref()
const parentId = ref(undefined)
const actionType = ref('')

const writeRef = ref<ComponentRef<typeof Write>>()

const saveLoading = ref(false)

const editAction = (row: any) => {
  dialogTitle.value = '编辑'
  actionType.value = 'edit'
  currentRow.value = row
  dialogVisible.value = true
}

const addAction = () => {
  dialogTitle.value = '新增'
  actionType.value = 'add'
  currentRow.value = undefined
  dialogVisible.value = true
}

const addSonAction = (row: any) => {
  dialogTitle.value = '添加子部门'
  actionType.value = 'addSon'
  parentId.value = row.id
  currentRow.value = undefined
  dialogVisible.value = true
}

const save = async () => {
  const write = unref(writeRef)
  const formData = await write?.submit()
  if (formData) {
    saveLoading.value = true
    try {
      const res = ref({})
      if (actionType.value === 'add' || actionType.value === 'addSon') {
        res.value = await addClientGroupListApi(formData)
        if (res.value) {
          parentId.value = undefined
          dialogVisible.value = false
          getList()
          ElMessage.success('添加成功!')
        }
      } else if (actionType.value === 'edit') {
        res.value = await putClientGroupListApi(formData)
        if (res.value) {
          dialogVisible.value = false
          getList()
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
    <ElRow :gutter="10" :justify="'start'">
      <ElCol :span="1.5">
        <ElButton type="primary" @click="addAction">新增分组</ElButton>
      </ElCol>
    </ElRow>
    <Table
      :columns="tableColumns"
      showAction
      default-expand-all
      node-key="id"
      :data="dataList"
      :loading="loading"
      @register="tableRegister"
      @refresh="getList"
    />
  </ContentWrap>

  <Dialog v-model="dialogVisible" :title="dialogTitle">
    <Write ref="writeRef" :current-row="currentRow" :parent-id="parentId" />

    <template #footer>
      <ElButton v-if="actionType !== 'detail'" type="primary" :loading="saveLoading" @click="save">
        {{ t('exampleDemo.save') }}
      </ElButton>
      <ElButton @click="dialogVisible = false">{{ t('dialogDemo.close') }}</ElButton>
    </template>
  </Dialog>
</template>
