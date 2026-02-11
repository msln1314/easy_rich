<script setup lang="tsx">
import { reactive, ref, unref, onMounted, onBeforeUnmount } from 'vue'
import {
  getDeviceListApi,
  addDeviceListApi,
  delDeviceListApi,
  putDeviceListApi,
  putDeviceBindApi,
  putDeviceUnBindApi,
  getDeviceApi,
  putPortStatusApi,
  postExportDeviceQueryListApi
} from '@/api/iot/device'
import { getProductOptionsApi } from '@/api/iot/product'
import { useTable } from '@/hooks/web/useTable'
import { useI18n } from '@/hooks/web/useI18n'
import { Table, TableColumn } from '@/components/Table'
import {
  ElButton,
  ElSwitch,
  ElRow,
  ElCol,
  ElMessage,
  ElMessageBox,
  ElTag,
  ElDivider
} from 'element-plus'
import { Search } from '@/components/Search'
import { FormSchema } from '@/components/Form'
import { ContentWrap } from '@/components/ContentWrap'
import Write from './components/Write.vue'
import { Dialog } from '@/components/Dialog'
import { selectDictLabel, DictDetail } from '@/utils/dict'
import { useDictStore } from '@/store/modules/dict'
import Import from './components/Import.vue'
import Bind from './components/Bind.vue'
import GroupTree from './components/GroupTree.vue'
import DictTag from '@/components/DictTag/src/DictTag.vue'

defineOptions({
  name: 'IotDevice'
})

const { t } = useI18n()

const { tableRegister, tableState, tableMethods } = useTable({
  fetchDataApi: async () => {
    const { pageSize, currentPage } = tableState
    const res = await getDeviceListApi({
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
    const res = await delDeviceListApi(value)
    return res.code === 200
  },
  fetchExportApi: async (headers) => {
    const { pageSize, currentPage } = tableState
    const res = await postExportDeviceQueryListApi(
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
const { getList, delList, getSelections, exportQueryList } = tableMethods

const deviceTypeOptions = ref<DictDetail[]>([])
const deviceTagOptions = ref<DictDetail[]>([])

const productOptions = ref<DictDetail[]>([])

const getOptions = async () => {
  const dictStore = useDictStore()
  const dictOptions = await dictStore.getDictObj(['Device_type', 'device_tag', 'port_status'])
  deviceTypeOptions.value = dictOptions.Device_type
  deviceTagOptions.value = dictOptions.connect_type

  const res = await getProductOptionsApi()
  productOptions.value = res.data
  console.log(productOptions, 'ssssssss')
}
// 用于存储定时器 ID
const intervalId = ref(null)
onMounted(() => {
  // 在页面加载完成后，启动定时器
  intervalId.value = setInterval(getList, 50000) // 每60秒刷新一次
})

onBeforeUnmount(() => {
  // 在组件销毁前清除定时器，避免内存泄漏
  clearInterval(intervalId.value)
})

onMounted(async () => {
  await getOptions()
})

const textTyle = () => {
  return {
    'background-color': '#000000',
    color: 'red',
    'font-size': '38px'
  }
}

const tableColumns = reactive<TableColumn[]>([
  {
    field: 'selection',
    type: 'selection',
    hidden: false,
    disabled: true
  },
  {
    field: 'ip',
    label: 'IP地址',
    width: '100px',
    hidden: false,
    disabled: false
  },
  {
    field: 'mac',
    label: 'MAC地址',
    hidden: false,
    align: 'center',
    showOverflowTooltip: false,
    // resizable: true,
    minWidth: '220px'

    // slots: {
    //   default: (data: any) => {
    //     const row = data.row
    //     return (
    //       <>
    //         <ElTag>{row.sn}</ElTag>
    //       </>
    //     )
    //   }
    // }
    // disabled: true
  },

  {
    field: 'device_type',
    label: '客户端类型',
    hidden: true,
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <>
            <div>{selectDictLabel(unref(deviceTypeOptions), row.device_type)}</div>
          </>
        )
      }
    }
  },
  {
    field: 'device_tag',
    label: '设备标记',
    hidden: true,
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <>
            <DictTag type="device_tag" value={row.device_tag} />
          </>
        )
      }
    }
  },

  {
    field: 'online_status',
    label: '在线状态',
    hidden: false,
    showOverflowTooltip: false,
    minWidth: '120px',
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <>
            <DictTag type="online_status" value={row.online_status} />
            <ElDivider direction="vertical" />
            {row.last_time}
          </>
        )
      }
    }
  },
  {
    field: 'address',
    label: '位置',
    hidden: false,
    showOverflowTooltip: false,
    disabled: true
  },
  {
    field: 'area',
    label: '单位',
    hidden: false,
    disabled: true
  },

  {
    field: 'is_active',
    label: '是否可用',
    hidden: true,
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <>
            <DictTag type="active_status" value={row.is_active} />
          </>
        )
      }
    }
  },

  {
    field: 'ccid',
    label: 'ccid',
    width: '220px',
    hidden: true
  },

  {
    field: 'phone',
    label: 'phone',
    width: '100px',
    hidden: false
  },
  {
    field: 'created_at',
    label: '创建时间',
    width: '190px',
    hidden: true
  },
  {
    field: 'remark',
    label: '备注',
    width: '100px',
    hidden: false,
    showOverflowTooltip: false,
    resizable: true
    // nullable: true
  },
  // {
  //   field: 'last_time',
  //   label: '通信时间',
  //   width: '190px',
  //   hidden: true
  // },
  {
    field: 'action',
    width: '180px',
    label: '操作',
    showOverflowTooltip: false,
    hidden: false,
    slots: {
      default: (data: any) => {
        const row = data.row
        const update = ['iot.device.update']
        const del = ['iot.Device.delete']
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

const searchSchema = reactive<FormSchema[]>([
  {
    field: 'ip',
    label: 'IP',
    component: 'Input',
    componentProps: {
      clearable: false,
      style: {
        width: '214px'
      }
    },
    formItemProps: {
      labelWidth: '80px'
    }
  },
  {
    field: 'mac',
    label: 'MAC',
    component: 'Input',
    componentProps: {
      clearable: false,
      style: {
        width: '214px'
      }
    },
    formItemProps: {
      labelWidth: '80px'
    }
  },
  {
    field: 'ccid',
    label: 'CCID',
    component: 'Input',
    componentProps: {
      clearable: false,
      style: {
        width: '214px'
      }
    },
    formItemProps: {
      labelWidth: '80px'
    }
  },
  {
    field: 'is_active',
    label: '状态',
    component: 'Select',
    componentProps: {
      style: {
        width: '180px'
      },
      options: [
        {
          label: '正常',
          value: true
        },
        {
          label: '停用',
          value: false
        }
      ]
    }
  },

  {
    field: 'product_id',
    label: '产品',
    colProps: {
      span: 12
    },
    component: 'Select',
    componentProps: {
      style: {
        width: '100%'
      },
      nodeKey: 'value',
      checkStrictly: true,
      defaultExpandAll: true,
      options: productOptions
    }
    // value: props.currentRow.group_id
    // ifshow: (values) => values.is_staff
  },

  {
    field: 'online_status',
    label: '在线状态',
    component: 'Select',
    componentProps: {
      style: {
        width: '180px'
      },
      options: [
        {
          label: '在线',
          value: '1'
        },
        {
          label: '离线',
          value: '0'
        },
        {
          label: '空',
          value: '-1'
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

const dialogVisible = ref(false)
const dialogTitle = ref('')

const currentRow = ref()
const actionType = ref('')

const writeRef = ref<ComponentRef<typeof Write>>()
const bindRef = ref<ComponentRef<typeof Bind>>()

const saveLoading = ref(false)

const editAction = async (row: any) => {
  const res = await getDeviceApi(row.id)
  if (res) {
    dialogTitle.value = '编辑设备'
    actionType.value = 'edit'
    currentRow.value = res.data
    dialogVisible.value = true
  }
}

// const onOfAction = async (row: any) => {
//   const res = await getDeviceApi(row.id)
//   if (res) {
//     dialogTitle.value = '操作客户端'
//     actionType.value = 'action'
//     currentRow.value = res.data
//     dialogVisible.value = true
//   }
// }

const addAction = () => {
  dialogTitle.value = '新增设备'
  actionType.value = 'add'
  currentRow.value = undefined
  dialogVisible.value = true
}

// 批量导入用户
const importList = () => {
  dialogTitle.value = '批量导入设备'
  actionType.value = 'import'
  currentRow.value = undefined
  dialogVisible.value = true
}

const selections = ref([] as any[])

/** 处理部门被点击 */
// const handleGroupNodeClick = async (row) => {
//   // console.log(row, 'row')
//   searchParams.value.group_id = row.value
//   await getList()
// }

const save = async () => {
  console.log(111111111)
  console.log(writeRef, 'writeRef')
  const form = unref(writeRef)
  const formData = await form?.submit()
  console.log(formData, 'formData')
  if (formData) {
    console.log(formData, 'formData')
    saveLoading.value = true
    try {
      const res = ref({})
      if (actionType.value === 'add') {
        res.value = await addDeviceListApi(formData)
        if (res.value) {
          dialogVisible.value = false
          await getList()
          ElMessage.success('添加成功!')
        }
      } else if (actionType.value === 'edit') {
        res.value = await putDeviceListApi(formData)
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
    <ElRow :gutter="10" :justify="'start'">
      <ElCol :span="1.5" v-hasPermi="['iot.device.create']">
        <ElButton type="primary" @click="addAction">新增设备</ElButton>
      </ElCol>
      <ElCol :span="1.5" v-hasPermi="['iot.device.import']">
        <ElButton @click="importList">批量导入设备</ElButton>
      </ElCol>
      <ElCol :span="1.5" v-hasPermi="['iot.device.export']">
        <ElButton @click="exportQueryList()">导出筛选设备</ElButton>
      </ElCol>
      <!-- <ElCol :span="1.5" v-hasPermi="['iot.Device.reset']">
        <ElButton @click="sendPasswordToEmail">同步客户端</ElButton>
      </ElCol> -->
      <ElCol :span="1.5" v-hasPermi="['iot.device.delete']">
        <ElButton type="danger" @click="delData(null)">批量删除</ElButton>
      </ElCol>
    </ElRow>
    <Table
      v-model:current-page="currentPage"
      v-model:page-size="pageSize"
      showAction
      :columns="tableColumns"
      default-expand-all
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
  <Dialog v-model="dialogVisible" :title="dialogTitle" :height="600" :width="700">
    <Write
      v-if="actionType === 'add' || actionType === 'edit'"
      ref="writeRef"
      :current-row="currentRow"
    />

    <Import v-else-if="actionType === 'import'" @get-list="getList" />

    <template #footer v-if="actionType === 'add' || actionType === 'edit' || actionType === 'bind'">
      <ElButton type="primary" :loading="saveLoading" @click="save">
        {{ t('exampleDemo.save') }}
      </ElButton>
      <ElButton @click="dialogVisible = false">{{ t('dialogDemo.close') }}</ElButton>
    </template>
  </Dialog>
</template>
