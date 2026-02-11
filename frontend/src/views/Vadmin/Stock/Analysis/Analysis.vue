<script setup lang="tsx">
import { reactive, ref, unref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  getStockAnalysisListApi,
  deleteStockAnalysisApi,
  getStockAnalysisDetailApi,
  verifyAnalysisApi,
  createStockAnalysisApi
} from '@/api/stock/analysis'
import { useTable } from '@/hooks/web/useTable'
import { Table, TableColumn } from '@/components/Table'
import { ElButton, ElRow, ElCol, ElMessage, ElDialog } from 'element-plus'
import { Search } from '@/components/Search'
import dayjs from 'dayjs'
import { ContentWrap } from '@/components/ContentWrap'
import AnalysisWrite from './components/AnalysisWrite.vue'
import AnalysisVerify from './components/AnalysisVerify.vue'

defineOptions({
  name: 'StockAnalysis'
})

const route = useRoute()
const router = useRouter()

// 表单对话框
const dialogVisible = ref(false)
const dialogTitle = ref('新增股票分析')
const formRef = ref()
const currentRow = ref<any>(null)

// 验证弹框
const verifyDialogVisible = ref(false)
const analysisVerifyRef = ref()
const verifyCurrentRow = ref<any>(null)

const sortInfo = ref<any>({})

const { tableRegister, tableState, tableMethods } = useTable({
  fetchDataApi: async () => {
    const { pageSize, currentPage } = tableState
    const res = await getStockAnalysisListApi({
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
    const res = await deleteStockAnalysisApi(value)
    return res.code === 200
  }
})

const { dataList, loading, total, pageSize, currentPage } = tableState
const { getList, delList } = tableMethods

const tableColumns = reactive<TableColumn[]>([
  {
    field: 'id',
    label: '编号',
    width: '80px',
    hidden: true
  },
  {
    field: 'analysis_date',
    label: '分析日期',
    width: '120px',
    formatter: (row: any) => row.analysis_date && dayjs(row.analysis_date).format('YYYY-MM-DD'),
    sortable: true
  },
  {
    field: 'stock_code',
    label: '股票代码',
    width: '100px',
    sortable: true
  },
  {
    field: 'stock_name',
    label: '股票名称',
    width: '120px',
    sortable: true
  },
  {
    field: 'stock_industry',
    label: '行业',
    width: '100px',
    sortable: true,
    hidden: true
  },
  {
    field: 'analysis_period',
    label: '分析周期',
    width: '80px',
    sortable: true,
    slots: {
      default: (data: any) => {
        const row = data.row
        const period = row.analysis_period
        let color = '#909399'
        if (period === '短线') {
          color = '#ff4d4f'
        } else if (period === '中线') {
          color = '#faad14'
        } else if (period === '长线') {
          color = '#52c41a'
        }
        return <span style={{ color, fontWeight: 500 }}>{period}</span>
      }
    }
  },
  {
    field: 'analysis_type',
    label: '分析类型',
    width: '100px',
    sortable: true,
    hidden: true
  },
  {
    field: 'analysis_result',
    label: '分析结果',
    width: '80px',
    sortable: true,
    slots: {
      default: (data: any) => {
        const row = data.row
        const result = row.analysis_result
        let color = '#909399'
        let bgColor = '#f5f5f5'
        if (result === '看涨') {
          color = '#ff4d4f'
          bgColor = '#fff1f0'
        } else if (result === '看跌') {
          color = '#52c41a'
          bgColor = '#f6ffed'
        } else if (result === '中性') {
          color = '#1890ff'
          bgColor = '#e6f7ff'
        }
        return (
          <span
            style={{
              color,
              backgroundColor: bgColor,
              padding: '4px 8px',
              borderRadius: '4px',
              fontSize: '12px',
              fontWeight: 500
            }}
          >
            {result}
          </span>
        )
      }
    }
  },
  {
    field: 'analysis_price',
    label: '分析价格',
    width: '100px',
    sortable: true
  },
  {
    field: 'stop_price',
    label: '止损价',
    width: '90px',
    sortable: true
  },
  {
    field: 'target_price',
    label: '目标价',
    width: '90px',
    sortable: true
  },
  {
    field: 'confidence_value',
    label: '置信值',
    width: '80px',
    sortable: true
  },
  {
    field: 'action_position',
    label: '仓位',
    width: '80px'
  },
  {
    field: 'hold_type',
    label: '持有类型',
    width: '80px'
  },
  {
    field: 'risk_level',
    label: '风险等级',
    width: '80px',
    sortable: true
  },
  {
    field: 'operation_direction',
    label: '操作建议',
    width: '90px',
    slots: {
      default: (data: any) => {
        const row = data.row
        const direction = row.operation_direction
        let color = '#909399'
        let bgColor = '#f5f5f5'
        if (direction === '买入') {
          color = '#ff4d4f'
          bgColor = '#fff1f0'
        } else if (direction === '观望') {
          color = '#faad14'
          bgColor = '#fffbe6'
        } else if (direction === '卖出') {
          color = '#52c41a'
          bgColor = '#f6ffed'
        }
        return (
          <span
            style={{
              color,
              backgroundColor: bgColor,
              padding: '4px 8px',
              borderRadius: '4px',
              fontSize: '12px'
            }}
          >
            {direction}
          </span>
        )
      }
    }
  },
  {
    field: 'ma5',
    label: '5日均线',
    width: '90px'
  },
  {
    field: 'ma10',
    label: '10日均线',
    width: '90px'
  },
  {
    field: 'ma20',
    label: '20日均线',
    width: '90px'
  },
  {
    field: 'rsi',
    label: 'RSI',
    width: '70px'
  },
  {
    field: 'macd',
    label: 'MACD',
    width: '80px'
  },
  {
    field: 'support',
    label: '支撑位',
    width: '80px'
  },
  {
    field: 'resistance',
    label: '压力位',
    width: '80px'
  },
  {
    field: 'tags',
    label: '标签',
    width: '120px'
  },
  {
    field: 'is_valid',
    label: '状态',
    width: '70px',
    sortable: true,
    slots: {
      default: (data: any) => {
        const row = data.row
        const isValid = row.is_valid === 1
        const color = isValid ? '#52c41a' : '#ff4d4f'
        const bgColor = isValid ? '#f6ffed' : '#fff1f0'
        return (
          <span
            style={{
              color,
              backgroundColor: bgColor,
              padding: '4px 8px',
              borderRadius: '4px',
              fontSize: '12px'
            }}
          >
            {isValid ? '有效' : '无效'}
          </span>
        )
      }
    }
  },
  {
    field: 'is_verified',
    label: '验证',
    width: '70px',
    sortable: true,
    slots: {
      default: (data: any) => {
        const row = data.row
        const isVerified = row.is_verified === 1
        const color = isVerified ? '#1890ff' : '#909399'
        const bgColor = isVerified ? '#e6f7ff' : '#f5f5f5'
        return (
          <span
            style={{
              color,
              backgroundColor: bgColor,
              padding: '4px 8px',
              borderRadius: '4px',
              fontSize: '12px'
            }}
          >
            {isVerified ? '已验证' : '未验证'}
          </span>
        )
      }
    }
  },
  {
    field: 'is_send',
    label: '发送',
    width: '70px',
    sortable: true,
    slots: {
      default: (data: any) => {
        const row = data.row
        const isSend = row.is_send === 1
        const color = isSend ? '#722ed1' : '#909399'
        const bgColor = isSend ? '#f9f0ff' : '#f5f5f5'
        return (
          <span
            style={{
              color,
              backgroundColor: bgColor,
              padding: '4px 8px',
              borderRadius: '4px',
              fontSize: '12px'
            }}
          >
            {isSend ? '已发送' : '未发送'}
          </span>
        )
      }
    }
  },
  {
    field: 'score',
    label: '评分',
    width: '60px'
  },
  {
    field: 'analyzer',
    label: '分析师',
    width: '90px',
    hidden: true
  },
  {
    field: 'notes',
    label: '备注',
    minWidth: '150px',
    showOverflowTooltip: true
  },
  {
    field: 'action',
    width: '220px',
    label: '操作',
    fixed: 'right',
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <>
            <ElButton type="primary" link size="small" onClick={() => editAction(row)}>
              编辑
            </ElButton>
            <ElButton type="success" link size="small" onClick={() => verifyAction(row)}>
              验证
            </ElButton>
            <ElButton type="info" link size="small" onClick={() => reportAction(row)}>
              查看报表
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

const searchSchema = reactive([
  {
    field: 'stock_code',
    label: '股票代码',
    component: 'Input',
    componentProps: {
      clearable: true,
      style: {
        width: '214px'
      }
    }
  },
  {
    field: 'stock_name',
    label: '股票名称',
    component: 'Input',
    componentProps: {
      clearable: true,
      style: {
        width: '214px'
      }
    }
  },
  {
    field: 'stock_industry',
    label: '股票行业',
    component: 'Input',
    componentProps: {
      clearable: true,
      style: {
        width: '214px'
      }
    }
  },
  {
    field: 'analysis_type',
    label: '分析类型',
    component: 'Select',
    componentProps: {
      clearable: true,
      style: {
        width: '214px'
      },
      options: [
        { label: '技术分析', value: '技术分析' },
        { label: '基本面分析', value: '基本面分析' },
        { label: '消息面分析', value: '消息面分析' },
        { label: '综合分析', value: '综合分析' }
      ]
    }
  },
  {
    field: 'analysis_result',
    label: '分析结果',
    component: 'Select',
    componentProps: {
      clearable: true,
      style: {
        width: '214px'
      },
      options: [
        {
          label: '看涨',
          value: '看涨'
        },
        {
          label: '看跌',
          value: '看跌'
        },
        {
          label: '中性',
          value: '中性'
        }
      ]
    }
  },
  {
    field: 'analysis_period',
    label: '分析周期',
    component: 'Select',
    componentProps: {
      clearable: true,
      style: {
        width: '214px'
      },
      options: [
        { label: '短线', value: '短线' },
        { label: '中线', value: '中线' },
        { label: '长线', value: '长线' }
      ]
    }
  },
  {
    field: 'risk_level',
    label: '风险等级',
    component: 'Select',
    componentProps: {
      clearable: true,
      style: {
        width: '214px'
      },
      options: [
        { label: '低', value: 'low' },
        { label: '中', value: 'medium' },
        { label: '高', value: 'high' }
      ]
    }
  },
  {
    field: 'is_valid',
    label: '状态',
    component: 'Select',
    componentProps: {
      clearable: true,
      style: {
        width: '214px'
      },
      options: [
        {
          label: '有效',
          value: 1
        },
        {
          label: '无效',
          value: 0
        }
      ]
    }
  },
  {
    field: 'is_verified',
    label: '验证状态',
    component: 'Select',
    componentProps: {
      clearable: true,
      style: {
        width: '214px'
      },
      options: [
        { label: '已验证', value: 1 },
        { label: '未验证', value: 0 }
      ]
    }
  }
])

const searchParams = ref<any>({})
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

const editAction = async (row: any) => {
  try {
    const res = await getStockAnalysisDetailApi(row.id)
    currentRow.value = res.data
    dialogTitle.value = '编辑股票分析'
    dialogVisible.value = true
  } catch (error) {
    ElMessage.error('获取数据失败')
  }
}

const addAction = () => {
  currentRow.value = null
  dialogTitle.value = '新增股票分析'
  dialogVisible.value = true
}

// 验证操作
const verifyAction = async (row: any) => {
  try {
    // const res = await getStockAnalysisDetailApi(row.id)
    verifyCurrentRow.value = row
    verifyDialogVisible.value = true
  } catch (error) {
    ElMessage.error('获取数据失败')
  }
}

// 查看报表操作 - 跳转到独立页面
const reportAction = (row: any) => {
  router.push({
    path: '/stock/analysis_report',
    query: { id: row.id }
  })
}

// 新增/编辑表单提交
const handleFormSubmit = async () => {
  try {
    const formData = await formRef.value?.submit()
    if (formData) {
      if (currentRow.value) {
        // 编辑操作，在子组件中处理
        ElMessage.success('操作成功')
      } else {
        // 新增操作
        await createStockAnalysisApi(formData)
        ElMessage.success('创建成功')
      }
      dialogVisible.value = false
      getList()
    }
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '操作失败')
  }
}

// 验证表单提交
const handleVerifySubmit = async () => {
  try {
    const formData = await analysisVerifyRef.value?.submit()
    console.log('formData', formData)
    if (formData) {
      await verifyAnalysisApi(verifyCurrentRow.value.id, {
        verification_result: formData.verification_result
      })
      ElMessage.success('验证成功')
      verifyDialogVisible.value = false
      getList()
    }
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '验证失败')
  }
}

const handleSortChange = (sort: any) => {
  if (sort.prop) {
    sortInfo.value = {
      prop: sort.prop,
      order: sort.order === 'ascending' ? 'asc' : 'desc'
    }
    getList()
  } else {
    sortInfo.value = {}
  }
}

// 检查是否从路由传入id用于编辑
onMounted(async () => {
  const id = route.query.id as string
  if (id) {
    await editAction({ id: Number(id) })
  }
})
</script>

<template>
  <ContentWrap>
    <Search :schema="searchSchema" @reset="resetSearchParams" @search="setSearchParams" />
    <ElRow :gutter="10" :justify="'start'" class="mt-4">
      <ElCol :span="1.5">
        <ElButton type="primary" @click="addAction">新增</ElButton>
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
      :showAction="true"
      :loading="loading"
      :pagination="{
        total
      }"
      @register="tableRegister"
      @refresh="getList"
      @sort-change="handleSortChange"
    />
    <ElDialog v-model="dialogVisible" :title="dialogTitle" width="600px">
      <AnalysisWrite :currentRow="currentRow" ref="formRef" />
      <template #footer>
        <ElButton @click="dialogVisible = false">取消</ElButton>
        <ElButton type="primary" @click="handleFormSubmit">确定</ElButton>
      </template>
    </ElDialog>
    <ElDialog v-model="verifyDialogVisible" title="验证分析" width="600px">
      <AnalysisVerify :currentRow="verifyCurrentRow" ref="analysisVerifyRef" />
      <template #footer>
        <ElButton @click="verifyDialogVisible = false">取消</ElButton>
        <ElButton type="primary" @click="handleVerifySubmit">确定</ElButton>
      </template>
    </ElDialog>
  </ContentWrap>
</template>
