<script setup lang="tsx">
import { reactive, ref, onMounted, unref } from 'vue'
import {
  getRuleListApi,
  getRuleDetailApi,
  createRuleApi,
  updateRuleApi,
  updateRuleActiveApi,
  deleteRuleApi,
  getViolationListApi
} from '@/api/stock/review'
import { useTable } from '@/hooks/web/useTable'
import { Table, TableColumn } from '@/components/Table'
import {
  ElButton,
  ElMessage,
  ElTag,
  ElTabs,
  ElTabPane,
  ElDialog,
  ElForm,
  ElFormItem,
  ElInput,
  ElSelect,
  ElOption,
  ElSwitch,
  ElRadioGroup,
  ElRadioButton,
  ElTimeline,
  ElTimelineItem,
  ElEmpty,
  ElCard
} from 'element-plus'
import { ContentWrap } from '@/components/ContentWrap'
import dayjs from 'dayjs'

defineOptions({
  name: 'RiskRules'
})

const activeTab = ref('trap')
const dialogVisible = ref(false)
const dialogTitle = ref('新建规则')
const formRef = ref()
const violationDialogVisible = ref(false)
const violations = ref<any[]>([])

const severityOptions = [
  { label: '严重', value: 'critical' },
  { label: '重要', value: 'major' },
  { label: '一般', value: 'minor' }
]

const categoryOptions = [
  { label: '交易纪律', value: 'trading' },
  { label: '风险控制', value: 'risk' },
  { label: '仓位管理', value: 'position' },
  { label: '选股规则', value: 'selection' },
  { label: '其他', value: 'other' }
]

const form = reactive({
  id: null as number | null,
  rule_type: 'trap',
  category: '',
  name: '',
  description: '',
  severity: 'minor',
  check_timing: [] as string[],
  check_condition: null as any,
  is_active: 1
})

const formRules = {
  rule_type: [{ required: true, message: '请选择规则类型', trigger: 'change' }],
  name: [{ required: true, message: '请输入规则名称', trigger: 'blur' }]
}

const { tableRegister, tableState, tableMethods } = useTable({
  fetchDataApi: async () => {
    const { pageSize, currentPage } = tableState
    const res = await getRuleListApi({
      page: unref(currentPage),
      limit: unref(pageSize),
      rule_type: activeTab.value
    })
    return {
      list: res.data || [],
      total: res.count || 0
    }
  },
  fetchDelApi: async (ids) => {
    const res = await deleteRuleApi(ids)
    return res.code === 200
  }
})

const { dataList, loading, total, pageSize, currentPage } = tableState
const { getList, delList } = tableMethods

const getCategoryLabel = (value: string) => {
  return categoryOptions.find((item) => item.value === value)?.label || value
}

const getSeverityType = (value: string) => {
  const map: Record<string, string> = {
    critical: 'danger',
    major: 'warning',
    minor: 'info'
  }
  return map[value] || 'info'
}

const tableColumns = reactive<TableColumn[]>([
  { field: 'id', label: 'ID', width: '80px' },
  { field: 'name', label: '规则名称', minWidth: '200px', showOverflowTooltip: true },
  {
    field: 'category',
    label: '分类',
    width: '100px',
    slots: {
      default: (data: any) => {
        const row = data.row
        return row.category ? (
          <ElTag size="small" type="info">
            {getCategoryLabel(row.category)}
          </ElTag>
        ) : null
      }
    }
  },
  {
    field: 'severity',
    label: '严重程度',
    width: '100px',
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <ElTag size="small" type={getSeverityType(row.severity)}>
            {severityOptions.find((item) => item.value === row.severity)?.label || row.severity}
          </ElTag>
        )
      }
    }
  },
  { field: 'description', label: '描述', minWidth: '200px', showOverflowTooltip: true },
  {
    field: 'is_active',
    label: '状态',
    width: '100px',
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <ElSwitch
            modelValue={row.is_active === 1}
            activeText="启用"
            inactiveText="禁用"
            onChange={() => handleToggleActive(row)}
          />
        )
      }
    }
  },
  { field: 'created_at', label: '创建时间', width: '160px' },
  {
    field: 'action',
    label: '操作',
    width: '220px',
    fixed: 'right',
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <>
            <ElButton type="primary" link onClick={() => openEditDialog(row)}>
              编辑
            </ElButton>
            <ElButton type="warning" link onClick={() => handleViewViolations(row)}>
              违规记录
            </ElButton>
            <ElButton type="danger" link onClick={() => handleDelete(row)}>
              删除
            </ElButton>
          </>
        )
      }
    }
  }
])

const handleTabChange = () => {
  currentPage.value = 1
  getList()
}

const openCreateDialog = () => {
  dialogTitle.value = '新建规则'
  resetForm()
  form.rule_type = activeTab.value
  dialogVisible.value = true
}

const openEditDialog = async (row: any) => {
  dialogTitle.value = '编辑规则'
  const res = await getRuleDetailApi(row.id)
  if (res.data) {
    Object.assign(form, res.data)
    dialogVisible.value = true
  }
}

const resetForm = () => {
  Object.assign(form, {
    id: null,
    rule_type: activeTab.value,
    category: '',
    name: '',
    description: '',
    severity: 'minor',
    check_timing: [],
    check_condition: null,
    is_active: 1
  })
}

const handleSubmit = async () => {
  await formRef.value?.validate()
  try {
    if (form.id) {
      await updateRuleApi(form.id, form)
      ElMessage.success('更新成功')
    } else {
      await createRuleApi(form)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    getList()
  } catch (error) {
    console.error(error)
  }
}

const handleDelete = async (row: any) => {
  await delList(false, [row.id])
}

const handleToggleActive = async (row: any) => {
  const newStatus = row.is_active === 1 ? 0 : 1
  await updateRuleActiveApi(row.id, newStatus)
  ElMessage.success(newStatus === 1 ? '已启用' : '已禁用')
  getList()
}

const handleViewViolations = async (row: any) => {
  const res = await getViolationListApi({ rule_id: row.id })
  violations.value = res.data || []
  violationDialogVisible.value = true
}

onMounted(() => {
  getList()
})
</script>

<template>
  <ContentWrap>
    <ElTabs v-model="activeTab" @tab-change="handleTabChange">
      <ElTabPane label="雷区（负面清单）" name="trap" />
      <ElTabPane label="基线（正面清单）" name="baseline" />
    </ElTabs>

    <div class="toolbar">
      <ElButton type="primary" @click="openCreateDialog">新建规则</ElButton>
    </div>

    <Table
      :columns="tableColumns"
      :data="dataList"
      :loading="loading"
      :pagination="{
        total,
        pageSize,
        currentPage
      }"
      @register="tableRegister"
      @pageSizeChange="getList"
      @currentPageChange="getList"
    />

    <ElDialog v-model="dialogVisible" :title="dialogTitle" width="600px" destroy-on-close>
      <ElForm ref="formRef" :model="form" :rules="formRules" label-width="100px">
        <ElFormItem label="规则类型" prop="rule_type">
          <ElRadioGroup v-model="form.rule_type">
            <ElRadioButton label="trap">雷区（负面清单）</ElRadioButton>
            <ElRadioButton label="baseline">基线（正面清单）</ElRadioButton>
          </ElRadioGroup>
        </ElFormItem>
        <ElFormItem label="规则名称" prop="name">
          <ElInput
            v-model="form.name"
            placeholder="请输入规则名称"
            maxlength="200"
            show-word-limit
          />
        </ElFormItem>
        <ElFormItem label="分类">
          <ElSelect v-model="form.category" placeholder="选择分类" clearable style="width: 200px">
            <ElOption
              v-for="item in categoryOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </ElSelect>
        </ElFormItem>
        <ElFormItem label="严重程度">
          <ElSelect v-model="form.severity" placeholder="选择严重程度" style="width: 200px">
            <ElOption
              v-for="item in severityOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </ElSelect>
        </ElFormItem>
        <ElFormItem label="规则描述">
          <ElInput
            v-model="form.description"
            type="textarea"
            :rows="4"
            placeholder="请输入规则描述..."
          />
        </ElFormItem>
        <ElFormItem label="是否启用">
          <ElSwitch v-model="form.is_active" :active-value="1" :inactive-value="0" />
        </ElFormItem>
      </ElForm>
      <template #footer>
        <ElButton @click="dialogVisible = false">取消</ElButton>
        <ElButton type="primary" @click="handleSubmit">确定</ElButton>
      </template>
    </ElDialog>

    <ElDialog v-model="violationDialogVisible" title="违规记录" width="600px">
      <div v-if="violations.length === 0">
        <ElEmpty description="暂无违规记录" />
      </div>
      <ElTimeline v-else>
        <ElTimelineItem
          v-for="item in violations"
          :key="item.id"
          :timestamp="dayjs(item.violation_time).format('YYYY-MM-DD HH:mm:ss')"
          placement="top"
        >
          <ElCard>
            <div v-if="item.related_stock_code">
              <strong>股票代码:</strong> {{ item.related_stock_code }}
            </div>
            <div v-if="item.user_note"> <strong>备注:</strong> {{ item.user_note }} </div>
          </ElCard>
        </ElTimelineItem>
      </ElTimeline>
    </ElDialog>
  </ContentWrap>
</template>

<style scoped>
.toolbar {
  margin-bottom: 16px;
}
</style>
