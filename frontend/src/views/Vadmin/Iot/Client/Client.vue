<script setup lang="tsx">
import { reactive, ref, unref, onMounted, onBeforeUnmount } from 'vue'
import {
  getClientListApi,
  addClientListApi,
  delClientListApi,
  putClientListApi,
  putClientBindApi,
  putClientUnBindApi,
  getClientApi,
  putPortStatusApi,
  postExportClientQueryListApi
} from '@/api/iot/client'
import { getClientGroupTreeOptionsApi } from '@/api/iot/client_group'
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
  name: 'IotClient'
})

const { t } = useI18n()

const { tableRegister, tableState, tableMethods } = useTable({
  fetchDataApi: async () => {
    const { pageSize, currentPage } = tableState
    const res = await getClientListApi({
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
    const res = await delClientListApi(value)
    return res.code === 200
  },
  fetchExportApi: async (headers) => {
    const { pageSize, currentPage } = tableState
    const res = await postExportClientQueryListApi(
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

const clientTypeOptions = ref<DictDetail[]>([])
const connectTypeOptions = ref<DictDetail[]>([])
const portStatusOptions = ref<DictDetail[]>([])
const groupOptions = ref<DictDetail[]>([])

const getOptions = async () => {
  const dictStore = useDictStore()
  const dictOptions = await dictStore.getDictObj(['client_type', 'connect_type', 'port_status'])
  clientTypeOptions.value = dictOptions.client_type
  connectTypeOptions.value = dictOptions.connect_type
  portStatusOptions.value = dictOptions.port_status
  const res = await getClientGroupTreeOptionsApi()
  groupOptions.value = res.data
  console.log(groupOptions, 'ssssssss')
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
    field: 'id',
    label: '编号',
    width: '100px',
    hidden: true,
    disabled: false
  },
  {
    field: 'sn',
    label: '桩编号',
    hidden: false,
    align: 'center',
    showOverflowTooltip: false,
    // resizable: true,
    minWidth: '220px',
    cellStyle: {
      'background-color': '#f5f7fa',
      color: '#f5f7fa',
      'font-size': '15px'
    }
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
    field: 'name',
    label: '站名称',
    hidden: false,
    resizable: true,
    minWidth: '220px',
    showOverflowTooltip: false
  },
  {
    field: 'client_type',
    label: '充电桩类型',
    hidden: true,
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <>
            <div>{selectDictLabel(unref(clientTypeOptions), row.client_type)}</div>
          </>
        )
      }
    }
  },
  {
    field: 'connect_type',
    label: '连接类型',
    hidden: true,
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <>
            <DictTag type="connect_type" value={row.connect_type} />
          </>
        )
      }
    }
  },

  {
    field: 'port_status',
    label: '端口状态',
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
            <DictTag type="port_status" value={row.port_status} />
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
    field: 'client_tag',
    label: '标签',
    hidden: false
  },
  {
    field: 'port',
    label: '连接信息',
    resizable: true,
    minWidth: '180px',
    showOverflowTooltip: false,
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <>
            <div class="text-truncate">
              {row.connect_type}
              {row.connect_protocol}
              {row.device?.connect_time ? row.device.connect_time : ''}
              <br /> 最近:{row.device?.last_time}
            </div>
          </>
        )
      }
    },
    hidden: false
  },

  {
    field: 'device',
    label: '设备',
    hidden: false,
    resizable: true,
    minWidth: '140px',
    showOverflowTooltip: false,
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <>
            <div>
              {row.port} {row.connect_model}
              <br /> {row.device?.ip}
              <br /> {row.device?.mac}
            </div>
          </>
        )
      }
    }
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
    field: 'bind_status',
    label: '绑定状态',
    hidden: false,
    showOverflowTooltip: false,
    resizable: true,
    minWidth: '120px',
    slots: {
      default: (data: any) => {
        const row = data.row
        console.log(row.bind_time, 'row', data)
        return (
          <>
            <DictTag type="bind_status" value={row.bind_status} />
          </>
        )
      }
    }
  },
  {
    field: 'bind_time',
    label: '绑定时间',
    hidden: true,
    width: '190px'
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
        const update = ['iot.Client.update']
        const bind = ['iot.Client.bind']
        const on_of = ['iot.Client.on_of']
        const del = ['iot.Client.delete']
        return (
          <>
            {(row.port_status == 1 || row.port_status == 0) && row.online_status == 1 && (
              <ElSwitch
                v-hasPermi={on_of}
                size="default"
                active-value={1}
                inactive-value={0}
                active-text="合闸"
                inactive-text="断开"
                inline-prompt
                onClick={async () => await portStatusAction(row)}
                v-model={row.port_status}
              ></ElSwitch>
            )}

            <ElButton
              type="primary"
              v-hasPermi={update}
              link
              size="small"
              onClick={() => editAction(row)}
            >
              编辑
            </ElButton>
            {row.bind_status == 0 && (
              <ElButton
                type="success"
                v-hasPermi={bind}
                link
                size="small"
                onClick={() => bindAction(row)}
              >
                绑定
              </ElButton>
            )}
            {row.bind_status == 1 && (
              <ElButton
                type="danger"
                v-hasPermi={bind}
                link
                size="small"
                onClick={() => unbindAction(row)}
              >
                解绑{row.bind_status == 1}
              </ElButton>
            )}
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
    field: 'name',
    label: '桩编号|站名称',
    component: 'Input',
    componentProps: {
      clearable: false,
      style: {
        width: '214px'
      }
    }
  },
  {
    field: 'keywords',
    label: 'IP|MAC',
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
    field: 'port_status',
    label: '端口状态',
    component: 'Select',
    componentProps: {
      style: {
        width: '180px'
      },
      options: [
        {
          label: '合闸',
          value: 1
        },
        {
          label: '断开',
          value: 0
        },
        {
          label: '未使用',
          value: -1
        }
      ]
    }
  },
  {
    field: 'group_id',
    label: '组',
    colProps: {
      span: 24
    },
    component: 'TreeSelect',
    componentProps: {
      style: {
        width: '100%'
      },
      checkStrictly: true,
      placeholder: '请选择组',
      nodeKey: 'value',
      defaultExpandAll: true,
      data: groupOptions
    }
  },
  // {
  //   field: 'group_id',
  //   label: '分组',
  //   colProps: {
  //     span: 12
  //   },
  //   component: 'TreeSelect',
  //   componentProps: {
  //     style: {
  //       width: '100%'
  //     },
  //     nodeKey: 'value',
  //     checkStrictly: true,
  //     defaultExpandAll: true,
  //     // options: groupOptions
  //     optionApi: async () => {
  //       const res = await getClientGroupTreeOptionsApi()
  //       return res.data
  //     }
  //   }
  //   // value: props.currentRow.group_id
  //   // ifshow: (values) => values.is_staff
  // },
  {
    field: 'bind_status',
    label: '绑定状态',
    component: 'Select',
    componentProps: {
      style: {
        width: '180px'
      },
      options: [
        {
          label: '是',
          value: 1
        },
        {
          label: '否',
          value: 0
        }
      ]
    }
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
  const res = await getClientApi(row.id)
  if (res) {
    dialogTitle.value = '编辑充电桩'
    actionType.value = 'edit'
    currentRow.value = res.data
    dialogVisible.value = true
  }
}

const bindAction = async (row: any) => {
  const res = await getClientApi(row.id)
  if (res) {
    dialogTitle.value = '绑定充电桩'
    actionType.value = 'bind'
    currentRow.value = res.data
    dialogVisible.value = true
  }
}

// const onOfAction = async (row: any) => {
//   const res = await getClientApi(row.id)
//   if (res) {
//     dialogTitle.value = '操作充电桩'
//     actionType.value = 'action'
//     currentRow.value = res.data
//     dialogVisible.value = true
//   }
// }
const unbindAction = async (row: any) => {
  try {
    // 修改状态的二次确认
    await ElMessageBox.confirm('确认要解绑' + row.sn + '"设备吗?')
    ElMessage.success('执行中，请等待....')
    // 发起修改状态
    await putClientUnBindApi({ id: row.id })
    // 刷新列表
    await getList()
    ElMessage.success('解绑成功')
  } catch {
    // 取消后，进行恢复按钮
    ElMessage.error('执行失败')
  }
}

/** 修改端口状态 */
const portStatusAction = async (row: any) => {
  try {
    // 修改状态的二次确认
    const text = row.port_status == 1 ? '合闸' : '断开'
    await ElMessageBox.confirm('确认要"' + text + '""' + row.sn + '"设备吗?')
    ElMessage.success('执行中，请等待....')
    // 发起修改状态
    await putPortStatusApi({ id: row.id, port_status: row.port_status })
    await getList()
    // 刷新列表
    // row.port_status = row.port_status == 1 ? 0 : 1
    ElMessage.success(text + '执行成功')
  } catch {
    // 取消后，进行恢复按钮
    ElMessage.error('执行失败')
    row.port_status = row.port_status == 1 ? 0 : 1
  }
}

const addAction = () => {
  dialogTitle.value = '新增充电桩'
  actionType.value = 'add'
  currentRow.value = undefined
  dialogVisible.value = true
}

// 批量导入用户
const importList = () => {
  dialogTitle.value = '批量导入充电桩'
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
  const form = actionType.value === 'bind' ? unref(bindRef) : unref(writeRef)
  const formData = await form?.submit()
  console.log(formData, 'formData')
  if (formData) {
    console.log(formData, 'formData')
    saveLoading.value = true
    try {
      const res = ref({})
      if (actionType.value === 'add') {
        res.value = await addClientListApi(formData)
        if (res.value) {
          dialogVisible.value = false
          await getList()
          ElMessage.success('添加成功!')
        }
      } else if (actionType.value === 'edit') {
        res.value = await putClientListApi(formData)
        if (res.value) {
          dialogVisible.value = false
          await getList()
          ElMessage.success('编辑成功!')
        }
      } else if (actionType.value === 'bind') {
        res.value = await putClientBindApi(formData)
        if (res.value) {
          dialogVisible.value = false
          await getList()
          ElMessage.success('绑定成功!')
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
      <ElCol :span="1.5" v-hasPermi="['iot.Client.create']">
        <ElButton type="primary" @click="addAction">新增充电桩</ElButton>
      </ElCol>
      <ElCol :span="1.5" v-hasPermi="['iot.Client.import']">
        <ElButton @click="importList">批量导入充电桩</ElButton>
      </ElCol>
      <ElCol :span="1.5" v-hasPermi="['iot.Client.export']">
        <ElButton @click="exportQueryList()">导出筛选充电桩</ElButton>
      </ElCol>
      <!-- <ElCol :span="1.5" v-hasPermi="['iot.Client.reset']">
        <ElButton @click="sendPasswordToEmail">同步充电桩</ElButton>
      </ElCol> -->
      <ElCol :span="1.5" v-hasPermi="['iot.Client.delete']">
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
      :actionType="actionType"
      :current-row="currentRow"
    />
    <Bind v-else-if="actionType === 'bind'" ref="bindRef" :current-row="currentRow" />

    <Import v-else-if="actionType === 'import'" @get-list="getList" />

    <template #footer v-if="actionType === 'add' || actionType === 'edit' || actionType === 'bind'">
      <ElButton type="primary" :loading="saveLoading" @click="save">
        {{ t('exampleDemo.save') }}
      </ElButton>
      <ElButton @click="dialogVisible = false">{{ t('dialogDemo.close') }}</ElButton>
    </template>
  </Dialog>
</template>
