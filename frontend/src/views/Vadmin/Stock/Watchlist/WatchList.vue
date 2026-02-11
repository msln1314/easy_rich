<script setup lang="tsx">
import { reactive, ref, unref } from 'vue'
import { getWatchListApi, delWatchListApi, postExportWatchListApi } from '@/api/stock/watch_list'
import { createStockAnalysisApi } from '@/api/stock/analysis'
import { useTable } from '@/hooks/web/useTable'
import { Table, TableColumn } from '@/components/Table'
import { ElButton, ElRow, ElCol, ElDialog, ElMessage } from 'element-plus'
import { Search } from '@/components/Search'
import dayjs from 'dayjs'
import { FormSchema } from '@/components/Form'
import { ContentWrap } from '@/components/ContentWrap'
import { useRouter } from 'vue-router'
import AnalysisWrite from './components/AnalysisWrite.vue'

defineOptions({
  name: 'StockWatchList'
})

const { push } = useRouter()

// 分析对话框
const dialogVisible = ref(false)
const analysisWriteRef = ref()
const currentAnalyzeRow = ref<any>(null)

const sortInfo = ref<any>({})

const { tableRegister, tableState, tableMethods } = useTable({
  fetchDataApi: async () => {
    const { pageSize, currentPage } = tableState
    const res = await getWatchListApi({
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
    const res = await delWatchListApi(value)
    return res.code === 200
  },
  fetchExportApi: async (headers) => {
    const { pageSize, currentPage } = tableState
    const res = await postExportWatchListApi(
      {
        // page: unref(currentPage),
        // limit: unref(pageSize),
        ...unref(searchParams)
      },
      headers
    )
    return res
  }
})

const { dataList, loading, total, pageSize, currentPage } = tableState
const { getList, delList, exportQueryList } = tableMethods

const priorityMap = { 1: '高', 2: '中', 3: '低' }

const tableColumns = reactive<TableColumn[]>([
  {
    field: 'id',
    label: '编号',
    width: '80px',
    hidden: true
  },
  {
    field: 'date_at',
    label: '关注时间',
    width: '120px',
    formatter: (row: any) => dayjs(row.date_at).format('YYYY-MM-DD'),
    sortable: true
  },
  {
    field: 'expire_at',
    label: '到期时间',
    width: '120px',
    formatter: (row: any) => dayjs(row.expire_at).format('YYYY-MM-DD'),
    sortable: true
  },
  {
    field: 'stock_code',
    label: '代码',
    width: '100px',
    sortable: true
  },
  {
    field: 'stock_name',
    label: '名称',
    minWidth: '120px',
    sortable: true
  },
  {
    field: 'follow_bwteen_change_percent',
    label: '关注期间涨幅(%)',
    width: '140px',
    sortable: true
  },
  {
    field: 'follow_bwteen_max_change_percent',
    label: '关注期间最大涨幅(%)',
    width: '160px',
    sortable: true
  },
  {
    field: 'follow_bwteen_min_change_percent',
    label: '关注期间最大跌幅(%)',
    width: '160px'
  },
  {
    field: 'follow_price',
    label: '关注价格',
    width: '100px',
    sortable: true
  },
  {
    field: 'follow_change_percent',
    label: '关注涨跌幅(%)',
    width: '120px',
    sortable: true
  },
  {
    field: 'watch_days',
    label: '关注天数',
    width: '90px',
    sortable: true
  },
  {
    field: 'max_price',
    label: '最高价',
    width: '100px',
    sortable: true
  },
  {
    field: 'min_price',
    label: '最低价',
    width: '100px',
    sortable: true
  },
  {
    field: 'max_change_percent',
    label: '最大涨幅(%)',
    width: '120px',
    sortable: true
  },
  {
    field: 'min_change_percent',
    label: '最大跌幅(%)',
    width: '120px',
    sortable: true
  },
  {
    field: 'follow_remark',
    label: '关注备注',
    minWidth: '150px'
  },
  {
    field: 'follow_reason',
    label: '关注原因',
    minWidth: '150px'
  },
  {
    field: 'category',
    label: '关注分类',
    width: '100px',
    sortable: true
  },
  {
    field: 'priority',
    label: '优先级',
    width: '80px',
    sortable: true,
    slots: {
      default: (data: any) => {
        const row = data.row
        return <div>{priorityMap[row.priority] || row.priority}</div>
      }
    }
  },
  {
    field: 'is_active',
    label: '关注状态',
    width: '90px',
    sortable: true,
    slots: {
      default: (data: any) => {
        const row = data.row
        return <div>{row.is_active === 1 ? '关注中' : '已取消'}</div>
      }
    }
  },
  {
    field: 'tags',
    label: '标签',
    width: '120px'
  },
  {
    field: 'follow_volume',
    label: '关注成交量(手)',
    width: '120px'
  },
  {
    field: 'follow_turnover_rate',
    label: '关注换手率(%)',
    width: '120px'
  },
  {
    field: 'follow_volume_ratio',
    label: '关注量比',
    width: '100px'
  },
  {
    field: 'follow_pe_ratio',
    label: '关注市盈率',
    width: '100px'
  },
  {
    field: 'follow_pb_ratio',
    label: '关注市净率',
    width: '100px'
  },
  {
    field: 'follow_market_cap',
    label: '关注总市值(万元)',
    width: '130px'
  },
  {
    field: 'follow_ma5',
    label: '关注5日均线',
    width: '110px'
  },
  {
    field: 'follow_ma10',
    label: '关注10日均线',
    width: '110px'
  },
  {
    field: 'follow_ma20',
    label: '关注20日均线',
    width: '110px'
  },
  {
    field: 'follow_rsi',
    label: '关注RSI',
    width: '90px'
  },
  {
    field: 'last_follow_price',
    label: '最近关注价格',
    width: '120px'
  },
  {
    field: 'last_follow_change_percent',
    label: '最近关注涨跌幅(%)',
    width: '150px'
  },
  {
    field: 'last_follow_volume',
    label: '最近关注成交量(手)',
    width: '150px'
  },
  {
    field: 'last_follow_turnover_rate',
    label: '最近关注换手率(%)',
    width: '150px'
  },
  {
    field: 'last_follow_volume_ratio',
    label: '最近关注量比',
    width: '130px'
  },
  {
    field: 'last_follow_pe_ratio',
    label: '最近关注市盈率',
    width: '130px'
  },
  {
    field: 'last_follow_pb_ratio',
    label: '最近关注市净率',
    width: '130px'
  },
  {
    field: 'last_follow_market_cap',
    label: '最近关注总市值(万元)',
    width: '160px'
  },
  {
    field: 'max_turnover_rate',
    label: '最大换手率(%)',
    width: '120px'
  },
  {
    field: 'min_turnover_rate',
    label: '最小换手率(%)',
    width: '120px'
  },
  {
    field: 'max_volume_ratio',
    label: '最大量比',
    width: '100px'
  },
  {
    field: 'min_volume_ratio',
    label: '最小量比',
    width: '100px'
  },
  {
    field: 'max_volume',
    label: '最大成交量(手)',
    width: '120px'
  },
  {
    field: 'min_volume',
    label: '最小成交量(手)',
    width: '120px'
  },
  {
    field: 'data_from',
    label: '数据来源',
    width: '150px'
  },
  {
    field: 'is_analyze',
    label: '是否已分析',
    width: '100px',
    slots: {
      default: (data: any) => {
        const row = data.row
        return <div>{row.is_analyze === 1 ? '已分析' : '未分析'}</div>
      }
    }
  },
  {
    field: 'action',
    width: '250px',
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
            <ElButton type="warning" link size="small" onClick={() => analyzeAction(row)}>
              分析
            </ElButton>
            <ElButton type="success" link size="small" onClick={() => predictAction(row)}>
              预测
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

const searchSchema = reactive<FormSchema[]>([
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
    field: 'category',
    label: '关注分类',
    component: 'Input',
    componentProps: {
      clearable: true,
      style: {
        width: '214px'
      }
    }
  },
  {
    field: 'is_active',
    label: '关注状态',
    component: 'Select',
    componentProps: {
      style: {
        width: '214px'
      },
      options: [
        {
          label: '关注中',
          value: 1
        },
        {
          label: '已过期',
          value: 0
        }
      ]
    }
  },
  {
    field: 'priority',
    label: '优先级',
    component: 'Select',
    componentProps: {
      style: {
        width: '214px'
      },
      options: [
        {
          label: '高',
          value: 1
        },
        {
          label: '中',
          value: 2
        },
        {
          label: '低',
          value: 3
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

const editAction = (row: any) => {
  push(`/stock/stock_watchlist/form?id=${row.id}`)
}

const analyzeAction = async (row: any) => {
  currentAnalyzeRow.value = row
  dialogVisible.value = true
}

const handleAnalysisSubmit = async () => {
  try {
    const formData = await analysisWriteRef.value?.submit()
    if (formData) {
      await createStockAnalysisApi({
        stock_code: currentAnalyzeRow.value.stock_code,
        stock_name: currentAnalyzeRow.value.stock_name,
        analysis_period: formData.analysis_period,
        analysis_type: formData.analysis_type,
        notes: formData.notes
      })
      ElMessage.success('分析任务已创建')
      dialogVisible.value = false
    }
  } catch (error: any) {
    console.error('分析失败:', error)
    ElMessage.error(error.response?.data?.detail || '分析失败，请稍后重试')
  }
}

const predictAction = (row: any) => {
  // 跳转到预测页面，并带上股票代码参数
  push(`/stock/prediction?code=${row.stock_code}`)
}

const addAction = () => {
  push('/stock/stock_watchlist/form')
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
</script>

<template>
  <ContentWrap>
    <Search :schema="searchSchema" @reset="resetSearchParams" @search="setSearchParams" />
    <ElRow :gutter="10" :justify="'start'" class="mt-4">
      <ElCol :span="1.5">
        <ElButton type="primary" @click="addAction">新增</ElButton>
      </ElCol>
      <ElCol :span="1.5">
        <ElButton @click="exportQueryList()">导出</ElButton>
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
    <ElDialog v-model="dialogVisible" title="创建股票分析" width="600px">
      <AnalysisWrite :currentRow="currentAnalyzeRow" ref="analysisWriteRef" />
      <template #footer>
        <ElButton @click="dialogVisible = false">取消</ElButton>
        <ElButton type="primary" @click="handleAnalysisSubmit">确定</ElButton>
      </template>
    </ElDialog>
  </ContentWrap>
</template>
