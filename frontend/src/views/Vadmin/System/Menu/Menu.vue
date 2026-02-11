<script setup lang="tsx">
import { reactive, ref, unref } from 'vue'
import { getMenuListApi, delMenuListApi, addMenuListApi, putMenuListApi } from '@/api/system/menu'
import { useTable } from '@/hooks/web/useTable'
import { useI18n } from '@/hooks/web/useI18n'
import { Table, TableColumn } from '@/components/Table'
import { ElButton, ElSwitch, ElRow, ElCol } from 'element-plus'
import { Icon } from '@/components/Icon'
import { ContentWrap } from '@/components/ContentWrap'
import Write from './components/Write.vue'
import { Dialog } from '@/components/Dialog'
import { useDictStore } from '@/store/modules/dict'
import { selectDictLabel, DictDetail } from '@/utils/dict'

defineOptions({
  name: 'AuthMenu'
})

const { t } = useI18n()

const { tableRegister, tableState, tableMethods } = useTable({
  fetchDataApi: async () => {
    const { pageSize, currentPage } = tableState
    const res = await getMenuListApi({
      page: unref(currentPage),
      limit: unref(pageSize)
    })
    return {
      list: res.data || [],
      total: res.count || 0
    }
  },
  fetchDelApi: async (value) => {
    const res = await delMenuListApi(value)
    return res.code === 200
  }
})

const { dataList, loading } = tableState
const { getList, delList } = tableMethods

let menuTypeOptions = ref<DictDetail[]>([])

const getOptions = async () => {
  const dictStore = useDictStore()
  const dictOptions = await dictStore.getDictObj(['sys_menu_type'])
  menuTypeOptions.value = dictOptions.sys_menu_type
}

getOptions()

const tableColumns = reactive<TableColumn[]>([
  {
    field: 'menu_name',
    label: '菜单名称',
    width: '200px',
    disabled: true,
    hidden: false
  },
  {
    field: 'icon',
    label: '图标',
    width: '120px',
    hidden: true,
    slots: {
      default: (data: any) => {
        const row = data.row
        return <>{row.icon ? <Icon icon={row.icon} /> : ''}</>
      }
    }
  },
  {
    field: 'order',
    label: '排序',
    width: '120px',
    hidden: false
  },
  {
    field: 'menu_type',
    label: '菜单类型',
    width: '120px',
    hidden: false,
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <>
            <span>{selectDictLabel(menuTypeOptions.value, row.menu_type)}</span>
          </>
        )
      }
    }
  },
  {
    field: 'perms',
    label: '权限标识',
    width: '150px',
    hidden: false
  },
  {
    field: 'path',
    label: '路由地址',
    hidden: false
  },
  {
    field: 'component',
    label: '组件路径',
    hidden: false
  },
  {
    field: 'noCache',
    label: '页面缓存',
    width: '120px',
    hidden: false,
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <>
            <ElSwitch model-value={!row.noCache} disabled />
          </>
        )
      }
    }
  },
  {
    field: 'hidden',
    label: '显示状态',
    width: '120px',
    hidden: false,
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <>
            <ElSwitch model-value={!row.hidden} disabled />
          </>
        )
      }
    }
  },
  {
    field: 'status',
    label: '菜单状态',
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
        const update = ['sys.menu.update']
        const add = ['sys.menu.create']
        const del = ['sys.menu.delete']
        return (
          <>
            <ElButton
              type="primary"
              v-hasPermi={update}
              link
              size="small"
              onClick={() => editAction(row)}
            >
              编辑
            </ElButton>
            <ElButton
              type="primary"
              v-hasPermi={add}
              link
              size="small"
              onClick={() => addSonAction(row)}
            >
              添加子菜单
            </ElButton>
            <ElButton
              type="danger"
              v-hasPermi={del}
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
  dialogTitle.value = '添加子菜单'
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
        res.value = await addMenuListApi(formData)
        if (res.value) {
          parentId.value = undefined
          await getList()
          dialogVisible.value = false
        }
      } else if (actionType.value === 'edit') {
        res.value = await putMenuListApi(formData)
        if (res.value) {
          await getList()
          dialogVisible.value = false
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
        <ElButton type="primary" v-hasPermi="['sys.menu.create']" @click="addAction"
          >新增菜单</ElButton
        >
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
