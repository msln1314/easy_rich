<script setup lang="tsx">
import { reactive, ref, onMounted, unref } from 'vue'
import {
  getReviewListApi,
  getReviewDetailApi,
  createReviewApi,
  updateReviewApi,
  deleteReviewApi
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
  ElDatePicker,
  ElRadioGroup,
  ElRadioButton
} from 'element-plus'
import { ContentWrap } from '@/components/ContentWrap'
import dayjs from 'dayjs'

defineOptions({
  name: 'ReviewWorkbench'
})

const activeTab = ref('daily')
const dialogVisible = ref(false)
const dialogTitle = ref('新建复盘')
const formRef = ref()
const currentReview = ref<any>(null)

const reviewTypeMap: Record<string, string> = {
  daily: '每日复盘',
  weekly: '每周复盘',
  monthly: '每月复盘',
  adhoc: '不定期复盘'
}

const statusMap: Record<string, { label: string; type: string }> = {
  draft: { label: '草稿', type: 'warning' },
  published: { label: '已发布', type: 'success' }
}

const form = reactive({
  id: null as number | null,
  review_type: 'daily',
  review_date: dayjs().format('YYYY-MM-DD'),
  portfolio_id: null as number | null,
  market_summary: null as any,
  market_analysis: '',
  position_summary: null as any,
  position_analysis: '',
  trade_summary: null as any,
  trade_analysis: '',
  strategy_summary: null as any,
  strategy_analysis: '',
  profit_summary: null as any,
  notes: '',
  next_plan: null as any,
  ai_analysis: '',
  status: 'draft'
})

const formRules = {
  review_type: [{ required: true, message: '请选择复盘类型', trigger: 'change' }],
  review_date: [{ required: true, message: '请选择复盘日期', trigger: 'change' }]
}

const { tableRegister, tableState, tableMethods } = useTable({
  fetchDataApi: async () => {
    const { pageSize, currentPage } = tableState
    const res = await getReviewListApi({
      page: unref(currentPage),
      limit: unref(pageSize),
      review_type: activeTab.value
    })
    return {
      list: res.data || [],
      total: res.count || 0
    }
  },
  fetchDelApi: async (ids) => {
    const res = await deleteReviewApi(ids)
    return res.code === 200
  }
})

const { dataList, loading, total, pageSize, currentPage } = tableState
const { getList, delList } = tableMethods

const tableColumns = reactive<TableColumn[]>([
  { field: 'id', label: 'ID', width: '80px' },
  { field: 'review_date', label: '复盘日期', width: '120px' },
  {
    field: 'review_type',
    label: '复盘类型',
    width: '100px',
    slots: {
      default: (data: any) => {
        const row = data.row
        return <ElTag>{reviewTypeMap[row.review_type] || row.review_type}</ElTag>
      }
    }
  },
  { field: 'market_analysis', label: '市场分析', showOverflowTooltip: true, minWidth: '200px' },
  { field: 'notes', label: '心得记录', showOverflowTooltip: true, minWidth: '200px' },
  {
    field: 'status',
    label: '状态',
    width: '100px',
    slots: {
      default: (data: any) => {
        const row = data.row
        const statusInfo = statusMap[row.status] || { label: row.status, type: 'info' }
        return <ElTag type={statusInfo.type}>{statusInfo.label}</ElTag>
      }
    }
  },
  { field: 'created_at', label: '创建时间', width: '160px' },
  {
    field: 'action',
    label: '操作',
    width: '180px',
    fixed: 'right',
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <>
            <ElButton type="primary" link onClick={() => openEditDialog(row)}>
              编辑
            </ElButton>
            {row.status === 'draft' && (
              <ElButton type="success" link onClick={() => handlePublish(row)}>
                发布
              </ElButton>
            )}
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
  dialogTitle.value = '新建复盘'
  resetForm()
  form.review_type = activeTab.value
  dialogVisible.value = true
}

const openEditDialog = async (row: any) => {
  dialogTitle.value = '编辑复盘'
  const res = await getReviewDetailApi(row.id)
  if (res.data) {
    Object.assign(form, {
      ...res.data,
      review_date: dayjs(res.data.review_date).format('YYYY-MM-DD')
    })
    currentReview.value = res.data
    dialogVisible.value = true
  }
}

const resetForm = () => {
  Object.assign(form, {
    id: null,
    review_type: activeTab.value,
    review_date: dayjs().format('YYYY-MM-DD'),
    portfolio_id: null,
    market_summary: null,
    market_analysis: '',
    position_summary: null,
    position_analysis: '',
    trade_summary: null,
    trade_analysis: '',
    strategy_summary: null,
    strategy_analysis: '',
    profit_summary: null,
    notes: '',
    next_plan: null,
    ai_analysis: '',
    status: 'draft'
  })
  currentReview.value = null
}

const handleSubmit = async () => {
  await formRef.value?.validate()
  try {
    const submitData = { ...form }
    if (form.id) {
      await updateReviewApi(form.id, submitData)
      ElMessage.success('更新成功')
    } else {
      await createReviewApi(submitData)
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

const handlePublish = async (row: any) => {
  await updateReviewApi(row.id, { status: 'published' })
  ElMessage.success('发布成功')
  getList()
}

onMounted(() => {
  getList()
})
</script>

<template>
  <ContentWrap>
    <ElTabs v-model="activeTab" @tab-change="handleTabChange">
      <ElTabPane label="每日复盘" name="daily" />
      <ElTabPane label="每周复盘" name="weekly" />
      <ElTabPane label="每月复盘" name="monthly" />
      <ElTabPane label="不定期复盘" name="adhoc" />
    </ElTabs>

    <div class="mb-4">
      <ElButton type="primary" @click="openCreateDialog">新建复盘</ElButton>
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

    <ElDialog v-model="dialogVisible" :title="dialogTitle" width="800px" destroy-on-close>
      <ElForm ref="formRef" :model="form" :rules="formRules" label-width="100px">
        <ElFormItem label="复盘类型" prop="review_type">
          <ElRadioGroup v-model="form.review_type">
            <ElRadioButton label="daily">每日复盘</ElRadioButton>
            <ElRadioButton label="weekly">每周复盘</ElRadioButton>
            <ElRadioButton label="monthly">每月复盘</ElRadioButton>
            <ElRadioButton label="adhoc">不定期复盘</ElRadioButton>
          </ElRadioGroup>
        </ElFormItem>
        <ElFormItem label="复盘日期" prop="review_date">
          <ElDatePicker
            v-model="form.review_date"
            type="date"
            placeholder="选择日期"
            value-format="YYYY-MM-DD"
            style="width: 200px"
          />
        </ElFormItem>
        <ElFormItem label="市场分析">
          <ElInput
            v-model="form.market_analysis"
            type="textarea"
            :rows="4"
            placeholder="请输入市场分析..."
          />
        </ElFormItem>
        <ElFormItem label="持仓分析">
          <ElInput
            v-model="form.position_analysis"
            type="textarea"
            :rows="4"
            placeholder="请输入持仓分析..."
          />
        </ElFormItem>
        <ElFormItem label="交易分析">
          <ElInput
            v-model="form.trade_analysis"
            type="textarea"
            :rows="4"
            placeholder="请输入交易分析..."
          />
        </ElFormItem>
        <ElFormItem label="策略分析">
          <ElInput
            v-model="form.strategy_analysis"
            type="textarea"
            :rows="4"
            placeholder="请输入策略分析..."
          />
        </ElFormItem>
        <ElFormItem label="心得记录">
          <ElInput v-model="form.notes" type="textarea" :rows="4" placeholder="请输入心得记录..." />
        </ElFormItem>
        <ElFormItem label="状态">
          <ElRadioGroup v-model="form.status">
            <ElRadioButton label="draft">草稿</ElRadioButton>
            <ElRadioButton label="published">发布</ElRadioButton>
          </ElRadioGroup>
        </ElFormItem>
      </ElForm>
      <template #footer>
        <ElButton @click="dialogVisible = false">取消</ElButton>
        <ElButton type="primary" @click="handleSubmit">确定</ElButton>
      </template>
    </ElDialog>
  </ContentWrap>
</template>

<style scoped>
.mb-4 {
  margin-bottom: 16px;
}
</style>
