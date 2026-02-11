<script setup lang="tsx">
import { reactive, ref, unref } from 'vue'
import { getNewsListApi, delNewsListApi, postExportNewsListApi } from '@/api/stock/news'
import { useTable } from '@/hooks/web/useTable'
import { Table, TableColumn } from '@/components/Table'
import { ElButton, ElRow, ElCol, ElTag } from 'element-plus'
import { Search } from '@/components/Search'
import dayjs from 'dayjs'
import { FormSchema } from '@/components/Form'
import { ContentWrap } from '@/components/ContentWrap'
import { useRouter } from 'vue-router'

defineOptions({
  name: 'StockNews'
})

const { push } = useRouter()

const sortInfo = ref<any>({
  prop: 'analyzed_at',
  order: 'desc'
})

const { tableRegister, tableState, tableMethods } = useTable({
  fetchDataApi: async () => {
    const { pageSize, currentPage } = tableState
    const res = await getNewsListApi({
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
    const res = await delNewsListApi(value)
    return res.code === 200
  },
  fetchExportApi: async (headers) => {
    const { pageSize, currentPage } = tableState
    const res = await postExportNewsListApi(
      {
        ...unref(searchParams)
      },
      headers
    )
    return res
  }
})

const { dataList, loading, total, pageSize, currentPage } = tableState
const { getList, delList, exportQueryList } = tableMethods

const priorityMap = { 1: '最高', 2: '高', 3: '中', 4: '低' }
const isSendMap = { 0: '未发送', 1: '已发送' }
const isAnalyzeMap = { 0: '未分析', 1: '已分析' }

const tableColumns = reactive<TableColumn[]>([
  {
    field: 'id',
    label: '编号',
    width: '80px',
    hidden: true
  },
  {
    field: 'date_at',
    label: '新闻日期',
    width: '180px',
    formatter: (row: any) => dayjs(row.date_at).format('YYYY-MM-DD HH:mm:ss'),
    sortable: true
  },
  {
    field: 'name',
    label: '新闻标题',
    minWidth: '250px',
    sortable: true
  },
  {
    field: 'category',
    label: '板块',
    width: '120px',
    sortable: true
  },
  {
    field: 'priority',
    label: '优先级',
    width: '100px',
    sortable: true,
    slots: {
      default: (data: any) => {
        const row = data.row
        return <div>{priorityMap[row.priority] || row.priority}</div>
      }
    }
  },
  {
    field: 'is_send',
    label: '发送状态',
    width: '100px',
    sortable: true,
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <ElTag type={row.is_send === 1 ? 'success' : 'info'}>
            {isSendMap[row.is_send] || row.is_send}
          </ElTag>
        )
      }
    }
  },
  {
    field: 'is_analyze',
    label: '分析状态',
    width: '100px',
    sortable: true,
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <ElTag type={row.is_analyze === 1 ? 'success' : 'warning'}>
            {isAnalyzeMap[row.is_analyze] || row.is_analyze}
          </ElTag>
        )
      }
    }
  },
  {
    field: 'analyzed_at',
    label: '分析时间',
    width: '180px',
    formatter: (row: any) =>
      row.analyzed_at ? dayjs(row.analyzed_at).format('YYYY-MM-DD HH:mm:ss') : '',
    sortable: true
  },
  {
    field: 'data_from',
    label: '数据来源',
    width: '150px',
    sortable: true
  },
  {
    field: 'agent',
    label: '代理',
    width: '120px'
  },
  {
    field: 'tag',
    label: '标签',
    width: '120px'
  },
  {
    field: 'views',
    label: '浏览量',
    width: '100px',
    sortable: true
  },
  {
    field: 'geo_scope',
    label: '全球范围',
    width: '150px'
  },
  {
    field: 'industry_scope',
    label: '行业范围',
    width: '150px'
  },
  {
    field: 'impact_on_business',
    label: '企业影响',
    width: '150px'
  },
  {
    field: 'impact_on_industry',
    label: '行业影响',
    width: '150px'
  },
  {
    field: 'impact_on_market',
    label: '市场影响',
    width: '150px'
  },
  {
    field: 'policy_level',
    label: '政策级别',
    width: '120px'
  },
  {
    field: 'policy_intensity',
    label: '政策力度',
    width: '120px'
  },
  {
    field: 'time_sensitivity',
    label: '时间敏感性',
    width: '150px'
  },
  {
    field: 'market_expectation',
    label: '市场预期',
    width: '150px'
  },
  {
    field: 'eps_impact',
    label: '收益影响',
    width: '120px'
  },
  {
    field: 'primary_sectors',
    label: '受影响板块',
    width: '150px'
  },
  {
    field: 'secondary_sectors',
    label: '间接传导板块',
    width: '150px'
  },
  {
    field: 'style_rotation',
    label: '风格影响',
    width: '150px'
  },
  {
    field: 'has_concept_stocks',
    label: '是否有概念股',
    width: '120px',
    slots: {
      default: (data: any) => {
        const row = data.row
        return <div>{row.has_concept_stocks === 1 ? '是' : '否'}</div>
      }
    }
  },
  {
    field: 'recommendation_level',
    label: '推荐级别',
    width: '120px'
  },
  {
    field: 'confidence_level',
    label: '置信级别',
    width: '120px'
  },
  {
    field: 'confidence_score',
    label: '置信度',
    width: '100px'
  },
  {
    field: 'score',
    label: '评分',
    width: '100px',
    sortable: true
  },
  {
    field: 'risks',
    label: '风险',
    width: '150px'
  },
  {
    field: 'key_points',
    label: '要点',
    minWidth: '200px'
  },
  {
    field: 'summary',
    label: '大纲',
    minWidth: '200px'
  },
  {
    field: 'remark',
    label: 'AI分析',
    minWidth: '200px'
  },
  {
    field: 'url',
    label: '链接',
    width: '200px'
  },
  {
    field: 'action',
    width: '150px',
    label: '操作',
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <>
            <ElButton type="primary" link size="small" onClick={() => editAction(row)}>
              编辑
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
    field: 'name',
    label: '新闻标题',
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
    label: '板块',
    component: 'Input',
    componentProps: {
      clearable: true,
      style: {
        width: '214px'
      }
    }
  },
  {
    field: 'is_send',
    label: '发送状态',
    component: 'Select',
    componentProps: {
      style: {
        width: '214px'
      },
      options: [
        {
          label: '未发送',
          value: 0
        },
        {
          label: '已发送',
          value: 1
        }
      ]
    }
  },
  {
    field: 'is_analyze',
    label: '分析状态',
    component: 'Select',
    componentProps: {
      style: {
        width: '214px'
      },
      options: [
        {
          label: '未分析',
          value: 0
        },
        {
          label: '已分析',
          value: 1
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
          label: '最高',
          value: 1
        },
        {
          label: '高',
          value: 2
        },
        {
          label: '中',
          value: 3
        },
        {
          label: '低',
          value: 4
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
  push(`/stock/news/form?id=${row.id}`)
}

const addAction = () => {
  push('/stock/news/form')
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
  </ContentWrap>
</template>
