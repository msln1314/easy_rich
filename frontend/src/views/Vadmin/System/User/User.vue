<script setup lang="tsx">
import { reactive, ref, unref } from 'vue'
import {
  getUserListApi,
  addUserListApi,
  delUserListApi,
  putUserListApi,
  getUserApi,
  postExportUserQueryListApi
} from '@/api/system/user'
import { useTable } from '@/hooks/web/useTable'
import { useI18n } from '@/hooks/web/useI18n'
import { Table, TableColumn } from '@/components/Table'
import { ElButton, ElSwitch, ElRow, ElCol, ElMessage } from 'element-plus'
import { Search } from '@/components/Search'
import { FormSchema } from '@/components/Form'
import { ContentWrap } from '@/components/ContentWrap'
import Write from './components/Write.vue'
import { Dialog } from '@/components/Dialog'
import { selectDictLabel, DictDetail } from '@/utils/dict'
import { useDictStore } from '@/store/modules/dict'
import Import from './components/Import.vue'
import PasswordSendSMS from './components/PasswordSendSMS.vue'
import PasswordSendEmail from './components/PasswordSendEmail.vue'
import PasswordReset from './components/PasswordReset.vue'
import DeptTree from './components/DeptTree.vue'
defineOptions({
  name: 'AuthUser'
})

const { t } = useI18n()

const { tableRegister, tableState, tableMethods } = useTable({
  fetchDataApi: async () => {
    const { pageSize, currentPage } = tableState
    const res = await getUserListApi({
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
    const res = await delUserListApi(value)
    return res.code === 200
  },
  fetchExportApi: async (headers) => {
    const { pageSize, currentPage } = tableState
    const res = await postExportUserQueryListApi(
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

const genderOptions = ref<DictDetail[]>([])

const getOptions = async () => {
  const dictStore = useDictStore()
  const dictOptions = await dictStore.getDictObj(['sys_gender'])
  genderOptions.value = dictOptions.sys_gender || []
}

getOptions()

const tableColumns = reactive<TableColumn[]>([
  {
    field: 'selection',
    type: 'selection',
    hidden: false,
    disabled: true
  },
  {
    field: 'id',
    label: '用户编号',
    width: '100px',
    hidden: true,
    disabled: false
  },
  {
    field: 'name',
    label: '姓名',
    hidden: false,
    disabled: true
  },
  {
    field: 'nickname',
    label: '昵称',
    hidden: false
  },
  {
    field: 'phone',
    label: '手机号',
    hidden: false,
    disabled: true
  },
  {
    field: 'email',
    label: '邮箱',
    hidden: false,
    disabled: true
  },
  {
    field: 'gender',
    label: '性别',
    hidden: true,
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <>
            <div>{selectDictLabel(unref(genderOptions), row.gender)}</div>
          </>
        )
      }
    }
  },
  {
    field: 'roles',
    label: '角色',
    hidden: false,
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <>
            <div class="text-truncate">{row.roles.map((item) => item.name).join()}</div>
          </>
        )
      }
    }
  },
  {
    field: 'dept',
    label: '部门',
    hidden: false,
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <>
            <div class="text-truncate">{row.dept?.name}</div>
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
            <ElSwitch model-value={row.is_active} disabled />
          </>
        )
      }
    }
  },
  {
    field: 'is_staff',
    label: '工作人员',
    hidden: false,
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <>
            <ElSwitch model-value={row.is_staff} disabled />
          </>
        )
      }
    }
  },
  {
    field: 'is_admin',
    label: '管理人员',
    hidden: false,
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <>
            <ElSwitch model-value={row.is_admin} disabled />
          </>
        )
      }
    }
  },
  {
    field: 'last_login',
    label: '最近登录时间',
    hidden: false,
    width: '190px'
  },
  {
    field: 'created_at',
    label: '创建时间',
    width: '190px',
    hidden: true
  },
  {
    field: 'action',
    width: '150px',
    label: '操作',
    hidden: false,
    slots: {
      default: (data: any) => {
        const row = data.row
        const update = ['sys.user.update']
        const del = ['sys.user.delete']
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
    field: 'name',
    label: '姓名',
    component: 'Input',
    componentProps: {
      clearable: false,
      style: {
        width: '214px'
      }
    },
    formItemProps: {
      labelWidth: '47px'
    }
  },
  {
    field: 'phone',
    label: '手机号',
    component: 'Input',
    componentProps: {
      clearable: false,
      style: {
        width: '214px'
      }
    }
  },
  {
    field: 'is_active',
    label: '状态',
    component: 'Select',
    componentProps: {
      style: {
        width: '214px'
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
    field: 'is_staff',
    label: '工作人员',
    component: 'Select',
    componentProps: {
      style: {
        width: '214px'
      },
      options: [
        {
          label: '是',
          value: true
        },
        {
          label: '否',
          value: false
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

const saveLoading = ref(false)

const editAction = async (row: any) => {
  const res = await getUserApi(row.id)
  if (res) {
    dialogTitle.value = '编辑用户'
    res.data.role_ids = res.data.roles.map((item: any) => item.id)
    // res.data.iot_group_ids = res.data.iot_groups.map((item: any) => item.id)
    actionType.value = 'edit'
    currentRow.value = res.data
    dialogVisible.value = true
  }
}

const addAction = () => {
  dialogTitle.value = '新增用户'
  actionType.value = 'add'
  currentRow.value = undefined
  dialogVisible.value = true
}

// 批量导入用户
const importList = () => {
  dialogTitle.value = '批量导入用户'
  actionType.value = 'import'
  currentRow.value = undefined
  dialogVisible.value = true
}

const selections = ref([] as any[])

// 批量发送密码至短信
const sendPasswordToSMS = async () => {
  selections.value = await getSelections()
  if (selections.value.length > 0) {
    dialogTitle.value = '重置密码并发送短信'
    actionType.value = 'sms'
    currentRow.value = undefined
    dialogVisible.value = true
  } else {
    return ElMessage.warning('请先选择数据')
  }
}

// 批量发送密码至邮件
const sendPasswordToEmail = async () => {
  selections.value = await getSelections()
  if (selections.value.length > 0) {
    dialogTitle.value = '重置密码并发送邮件'
    actionType.value = 'email'
    currentRow.value = undefined
    dialogVisible.value = true
  } else {
    return ElMessage.warning('请先选择数据')
  }
}

// 批量重置密码
const restPassword = async () => {
  selections.value = await getSelections()
  if (selections.value.length > 0) {
    dialogTitle.value = '重置密码'
    actionType.value = 'reset_password'
    currentRow.value = undefined
    dialogVisible.value = true
  } else {
    return ElMessage.warning('请先选择数据')
  }
}

/** 处理部门被点击 */
const handleDeptNodeClick = async (row) => {
  // console.log(row, 'row')
  searchParams.value.dept_id = row.value
  await getList()
}

const save = async () => {
  const write = unref(writeRef)
  const formData = await write?.submit()
  if (formData) {
    saveLoading.value = true
    try {
      const res = ref({})
      if (actionType.value === 'add') {
        res.value = await addUserListApi(formData)
        if (res.value) {
          dialogVisible.value = false
          await getList()
          ElMessage.success('添加成功!')
        }
      } else if (actionType.value === 'edit') {
        res.value = await putUserListApi(formData)
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
  <el-row :gutter="20">
    <!-- 左侧部门树 -->
    <el-col :span="4" :xs="24">
      <ContentWrap class="h-1/1 -mr-15px">
        <DeptTree @node-click="handleDeptNodeClick" />
      </ContentWrap>
    </el-col>

    <el-col :span="20" :xs="24">
      <ContentWrap>
        <Search :schema="searchSchema" @reset="resetSearchParams" @search="setSearchParams" />
        <ElRow :gutter="10" :justify="'start'">
          <ElCol :span="1.5" v-hasPermi="['sys.user.create']">
            <ElButton type="primary" @click="addAction">新增用户</ElButton>
          </ElCol>
          <ElCol :span="1.5" v-hasPermi="['sys.user.import']">
            <ElButton @click="importList">批量导入用户</ElButton>
          </ElCol>
          <ElCol :span="1.5" v-hasPermi="['sys.user.export']">
            <ElButton @click="exportQueryList()">导出筛选用户</ElButton>
          </ElCol>
          <ElCol :span="1.5" v-hasPermi="['sys.user.reset']">
            <ElButton @click="sendPasswordToSMS">重置密码通知短信</ElButton>
          </ElCol>
          <ElCol :span="1.5" v-hasPermi="['sys.user.reset']">
            <ElButton @click="sendPasswordToEmail">重置密码通知邮件</ElButton>
          </ElCol>
          <ElCol :span="1.5" v-hasPermi="['sys.user.reset']">
            <ElButton @click="restPassword">重置密码</ElButton>
          </ElCol>
          <ElCol :span="1.5" v-hasPermi="['sys.user.delete']">
            <ElButton type="danger" @click="delData(null)">批量删除</ElButton>
          </ElCol>
        </ElRow>
        <Table
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :columns="tableColumns"
          default-expand-all
          node-key="id"
          :data="dataList"
          :showAction="true"
          :loading="loading"
          :pagination="{
            total
          }"
          @register="tableRegister"
          @refresh="getList"
        />
      </ContentWrap>
    </el-col>
  </el-row>
  <Dialog
    v-model="dialogVisible"
    :title="dialogTitle"
    :height="600"
    :width="actionType === 'sms' || actionType === 'email' ? '1000px' : '700px'"
  >
    <Write
      v-if="actionType === 'add' || actionType === 'edit'"
      ref="writeRef"
      :current-row="currentRow"
    />

    <Import v-else-if="actionType === 'import'" @get-list="getList" />

    <PasswordSendSMS
      v-else-if="actionType === 'sms'"
      :selections="selections"
      @get-list="getList"
    />

    <PasswordSendEmail
      v-else-if="actionType === 'email'"
      :selections="selections"
      @get-list="getList"
    />

    <PasswordReset
      v-else-if="actionType === 'reset_password'"
      :selections="selections"
      @get-list="getList"
    />

    <template #footer v-if="actionType === 'add' || actionType === 'edit'">
      <ElButton type="primary" :loading="saveLoading" @click="save">
        {{ t('exampleDemo.save') }}
      </ElButton>
      <ElButton @click="dialogVisible = false">{{ t('dialogDemo.close') }}</ElButton>
    </template>
  </Dialog>
</template>
