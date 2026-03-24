<script setup lang="tsx">
import { reactive, ref, onMounted, unref } from 'vue'
import {
  getExperienceListApi,
  getExperienceDetailApi,
  createExperienceApi,
  updateExperienceApi,
  deleteExperienceApi
} from '@/api/stock/review'
import { useTable } from '@/hooks/web/useTable'
import { Table, TableColumn } from '@/components/Table'
import {
  ElButton,
  ElMessage,
  ElTag,
  ElDialog,
  ElForm,
  ElFormItem,
  ElInput,
  ElSelect,
  ElOption,
  ElCard,
  ElRow,
  ElCol,
  ElEmpty
} from 'element-plus'
import { ContentWrap } from '@/components/ContentWrap'
import dayjs from 'dayjs'

defineOptions({
  name: 'ExperienceLibrary'
})

const viewMode = ref<'list' | 'card'>('card')
const dialogVisible = ref(false)
const dialogTitle = ref('新建心得')
const formRef = ref()
const searchKeyword = ref('')

const categoryOptions = [
  { label: '交易心得', value: 'trading' },
  { label: '策略总结', value: 'strategy' },
  { label: '风险教训', value: 'risk' },
  { label: '市场感悟', value: 'market' },
  { label: '其他', value: 'other' }
]

const importanceOptions = [
  { label: '重要', value: 'important' },
  { label: '普通', value: 'normal' },
  { label: '参考', value: 'reference' }
]

const moodOptions = [
  { label: '开心', value: 'happy' },
  { label: '平静', value: 'calm' },
  { label: '沮丧', value: 'frustrated' },
  { label: '后悔', value: 'regret' },
  { label: '兴奋', value: 'excited' }
]

const form = reactive({
  id: null as number | null,
  title: '',
  content: '',
  category: '',
  tags: [] as string[],
  related_stocks: [] as string[],
  related_trades: [] as number[],
  related_review_id: null as number | null,
  mood: '',
  importance: 'normal'
})

const formRules = {
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  content: [{ required: true, message: '请输入内容', trigger: 'blur' }]
}

const { tableRegister, tableState, tableMethods } = useTable({
  fetchDataApi: async () => {
    const { pageSize, currentPage } = tableState
    const params: any = {
      page: unref(currentPage),
      limit: unref(pageSize)
    }
    if (searchKeyword.value) {
      params.keyword = searchKeyword.value
    }
    const res = await getExperienceListApi(params)
    return {
      list: res.data || [],
      total: res.count || 0
    }
  },
  fetchDelApi: async (ids) => {
    const res = await deleteExperienceApi(ids)
    return res.code === 200
  }
})

const { dataList, loading, total, pageSize, currentPage } = tableState
const { getList, delList } = tableMethods

const getCategoryLabel = (value: string) => {
  return categoryOptions.find((item) => item.value === value)?.label || value
}

const getImportanceType = (value: string) => {
  const map: Record<string, string> = {
    important: 'danger',
    normal: 'info',
    reference: 'success'
  }
  return map[value] || 'info'
}

const tableColumns = reactive<TableColumn[]>([
  { field: 'id', label: 'ID', width: '80px' },
  { field: 'title', label: '标题', minWidth: '200px', showOverflowTooltip: true },
  {
    field: 'category',
    label: '分类',
    width: '100px',
    slots: {
      default: (data: any) => {
        const row = data.row
        return row.category ? <ElTag size="small">{getCategoryLabel(row.category)}</ElTag> : null
      }
    }
  },
  {
    field: 'importance',
    label: '重要程度',
    width: '100px',
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <ElTag size="small" type={getImportanceType(row.importance)}>
            {importanceOptions.find((item) => item.value === row.importance)?.label ||
              row.importance}
          </ElTag>
        )
      }
    }
  },
  {
    field: 'mood',
    label: '心情',
    width: '80px',
    slots: {
      default: (data: any) => {
        const row = data.row
        return row.mood
          ? moodOptions.find((item) => item.value === row.mood)?.label || row.mood
          : null
      }
    }
  },
  { field: 'view_count', label: '查看次数', width: '100px' },
  { field: 'created_at', label: '创建时间', width: '160px' },
  {
    field: 'action',
    label: '操作',
    width: '150px',
    fixed: 'right',
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <>
            <ElButton type="primary" link onClick={() => openEditDialog(row)}>
              编辑
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

const openCreateDialog = () => {
  dialogTitle.value = '新建心得'
  resetForm()
  dialogVisible.value = true
}

const openEditDialog = async (row: any) => {
  dialogTitle.value = '编辑心得'
  const res = await getExperienceDetailApi(row.id)
  if (res.data) {
    Object.assign(form, res.data)
    dialogVisible.value = true
  }
}

const resetForm = () => {
  Object.assign(form, {
    id: null,
    title: '',
    content: '',
    category: '',
    tags: [],
    related_stocks: [],
    related_trades: [],
    related_review_id: null,
    mood: '',
    importance: 'normal'
  })
}

const handleSubmit = async () => {
  await formRef.value?.validate()
  try {
    if (form.id) {
      await updateExperienceApi(form.id, form)
      ElMessage.success('更新成功')
    } else {
      await createExperienceApi(form)
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

const handleSearch = () => {
  currentPage.value = 1
  getList()
}

onMounted(() => {
  getList()
})
</script>

<template>
  <ContentWrap>
    <div class="toolbar">
      <div class="toolbar-left">
        <ElInput
          v-model="searchKeyword"
          placeholder="搜索心得..."
          style="width: 300px"
          clearable
          @keyup.enter="handleSearch"
          @clear="handleSearch"
        />
        <ElButton type="primary" @click="handleSearch">搜索</ElButton>
      </div>
      <div class="toolbar-right">
        <ElButton :type="viewMode === 'list' ? 'primary' : 'default'" @click="viewMode = 'list'">
          列表
        </ElButton>
        <ElButton :type="viewMode === 'card' ? 'primary' : 'default'" @click="viewMode = 'card'">
          卡片
        </ElButton>
        <ElButton type="primary" @click="openCreateDialog">新建心得</ElButton>
      </div>
    </div>

    <template v-if="viewMode === 'list'">
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
    </template>

    <template v-else>
      <div v-if="dataList.length === 0 && !loading" class="empty-state">
        <ElEmpty description="暂无心得记录" />
      </div>
      <ElRow v-else :gutter="16" class="card-grid">
        <ElCol v-for="item in dataList" :key="item.id" :span="8">
          <ElCard class="experience-card" shadow="hover" @click="openEditDialog(item)">
            <template #header>
              <div class="card-header">
                <span class="title">{{ item.title }}</span>
                <ElTag v-if="item.category" size="small" type="info">
                  {{ getCategoryLabel(item.category) }}
                </ElTag>
              </div>
            </template>
            <div class="card-content">{{ item.content }}</div>
            <div class="card-footer">
              <span class="date">{{ dayjs(item.created_at).format('YYYY-MM-DD') }}</span>
              <span class="views">查看: {{ item.view_count }}</span>
            </div>
          </ElCard>
        </ElCol>
      </ElRow>
    </template>

    <ElDialog v-model="dialogVisible" :title="dialogTitle" width="700px" destroy-on-close>
      <ElForm ref="formRef" :model="form" :rules="formRules" label-width="100px">
        <ElFormItem label="标题" prop="title">
          <ElInput v-model="form.title" placeholder="请输入标题" maxlength="200" show-word-limit />
        </ElFormItem>
        <ElFormItem label="内容" prop="content">
          <ElInput
            v-model="form.content"
            type="textarea"
            :rows="6"
            placeholder="请输入心得内容..."
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
        <ElFormItem label="重要程度">
          <ElSelect v-model="form.importance" placeholder="选择重要程度" style="width: 200px">
            <ElOption
              v-for="item in importanceOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </ElSelect>
        </ElFormItem>
        <ElFormItem label="心情">
          <ElSelect v-model="form.mood" placeholder="选择心情" clearable style="width: 200px">
            <ElOption
              v-for="item in moodOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </ElSelect>
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
.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.toolbar-left {
  display: flex;
  gap: 8px;
}

.toolbar-right {
  display: flex;
  gap: 8px;
}

.card-grid {
  margin-top: 16px;
}

.experience-card {
  cursor: pointer;
  margin-bottom: 16px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header .title {
  font-weight: 600;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex: 1;
  margin-right: 8px;
}

.card-content {
  color: #666;
  font-size: 14px;
  line-height: 1.6;
  height: 66px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #eee;
  font-size: 12px;
  color: #999;
}

.empty-state {
  padding: 60px 0;
}
</style>
