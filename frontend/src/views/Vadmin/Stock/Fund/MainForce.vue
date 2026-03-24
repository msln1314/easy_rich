<script setup lang="tsx">
import { ref, onMounted, computed } from 'vue'
import {
  getMainForceOverviewApi,
  getMainForceTrendApi,
  getMainForceFundsApi,
  syncStockMainForceApi
} from '@/api/stock/fund'
import {
  ElCard,
  ElRow,
  ElCol,
  ElTag,
  ElInput,
  ElButton,
  ElEmpty,
  ElProgress,
  ElMessage
} from 'element-plus'
import { ContentWrap } from '@/components/ContentWrap'
import { Table, TableColumn } from '@/components/Table'
import { useTable } from '@/hooks/web/useTable'
import dayjs from 'dayjs'

defineOptions({
  name: 'MainForceAnalysis'
})

const stockCode = ref('')
const overview = ref<any>(null)
const trendData = ref<any[]>([])
const activeTab = ref('all')
const loading = ref(false)
const syncing = ref(false)

const changeTypeOptions = [
  { label: '全部', value: 'all' },
  { label: '增持', value: 'increase' },
  { label: '减持', value: 'decrease' },
  { label: '新进', value: 'new' },
  { label: '退出', value: 'exit' }
]

const { tableRegister, tableState, tableMethods } = useTable({
  fetchDataApi: async () => {
    if (!stockCode.value) {
      return { list: [], total: 0 }
    }
    const { pageSize, currentPage } = tableState
    const changeType = activeTab.value === 'all' ? undefined : activeTab.value
    const res = await getMainForceFundsApi(stockCode.value, {
      page: currentPage,
      limit: pageSize,
      change_type: changeType
    })
    return {
      list: res.data || [],
      total: res.count || 0
    }
  }
})

const { dataList, loading: tableLoading, total, pageSize, currentPage } = tableState
const { getList } = tableMethods

const tableColumns = computed<TableColumn[]>(() => [
  { field: 'fund_code', label: '基金代码', width: '120px' },
  { field: 'fund_name', label: '基金名称', minWidth: '180px', showOverflowTooltip: true },
  {
    field: 'holding_value',
    label: '持仓市值(万)',
    width: '120px',
    slots: {
      default: (data: any) => {
        const val = data.row.holding_value
        return val ? (val / 10000).toFixed(2) + '亿' : '-'
      }
    }
  },
  {
    field: 'holding_ratio',
    label: '占净值比',
    width: '100px',
    slots: {
      default: (data: any) => {
        const val = data.row.holding_ratio
        return val ? val.toFixed(2) + '%' : '-'
      }
    }
  },
  {
    field: 'change_type',
    label: '变动类型',
    width: '80px',
    slots: {
      default: (data: any) => {
        const typeMap: Record<string, { label: string; type: string }> = {
          increase: { label: '增持', type: 'success' },
          decrease: { label: '减持', type: 'danger' },
          new: { label: '新进', type: 'primary' },
          exit: { label: '退出', type: 'info' }
        }
        const info = typeMap[data.row.change_type] || {
          label: data.row.change_type || '-',
          type: 'info'
        }
        return (
          <ElTag type={info.type} size="small">
            {info.label}
          </ElTag>
        )
      }
    }
  },
  {
    field: 'change_value',
    label: '变动市值(万)',
    width: '120px',
    slots: {
      default: (data: any) => {
        const val = data.row.change_value
        if (!val) return '-'
        const color = val > 0 ? '#67C23A' : val < 0 ? '#F56C6C' : '#909399'
        return (
          <span style={{ color }}>
            {val > 0 ? '+' : ''}
            {(val / 10000).toFixed(2)}亿
          </span>
        )
      }
    }
  },
  { field: 'report_date', label: '报告日期', width: '120px' }
])

const handleSearch = async () => {
  if (!stockCode.value) return

  loading.value = true
  try {
    const [overviewRes, trendRes] = await Promise.all([
      getMainForceOverviewApi(stockCode.value),
      getMainForceTrendApi(stockCode.value, 8)
    ])
    overview.value = overviewRes.data
    trendData.value = trendRes.data || []
    getList()
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

const handleTabChange = () => {
  currentPage.value = 1
  getList()
}

const formatValue = (val: number | null | undefined, unit = '亿') => {
  if (!val) return '-'
  return (val / 10000).toFixed(2) + unit
}

const getConcentrationColor = (val: number | null | undefined) => {
  if (!val) return '#909399'
  if (val >= 60) return '#F56C6C'
  if (val >= 40) return '#E6A23C'
  return '#67C23A'
}

const handleSync = async () => {
  if (!stockCode.value) {
    ElMessage.warning('请输入股票代码')
    return
  }

  syncing.value = true
  try {
    const res = await syncStockMainForceApi(stockCode.value)
    if (res.data?.success) {
      ElMessage.success(res.data.message || '同步成功')
      await handleSearch()
    } else {
      ElMessage.error(res.data?.message || '同步失败')
    }
  } catch (error) {
    console.error(error)
    ElMessage.error('同步失败')
  } finally {
    syncing.value = false
  }
}

onMounted(() => {
  // 可以从路由参数获取股票代码
})
</script>

<template>
  <ContentWrap>
    <div class="search-bar">
      <ElInput
        v-model="stockCode"
        placeholder="输入股票代码或名称"
        style="width: 300px"
        clearable
        @keyup.enter="handleSearch"
      />
      <ElButton type="primary" @click="handleSearch" :loading="loading">查询</ElButton>
      <ElButton type="success" @click="handleSync" :loading="syncing">同步数据</ElButton>
    </div>

    <template v-if="overview">
      <ElRow :gutter="16" class="overview-cards">
        <ElCol :span="6">
          <ElCard shadow="hover">
            <div class="stat-card">
              <div class="stat-label">持仓基金数</div>
              <div class="stat-value">{{ overview.fund_count || '-' }}</div>
            </div>
          </ElCard>
        </ElCol>
        <ElCol :span="6">
          <ElCard shadow="hover">
            <div class="stat-card">
              <div class="stat-label">持仓市值</div>
              <div class="stat-value">{{ formatValue(overview.holding_value) }}</div>
            </div>
          </ElCard>
        </ElCol>
        <ElCol :span="6">
          <ElCard shadow="hover">
            <div class="stat-card">
              <div class="stat-label">占流通股比</div>
              <div class="stat-value">{{ overview.holding_ratio?.toFixed(2) || '-' }}%</div>
            </div>
          </ElCard>
        </ElCol>
        <ElCol :span="6">
          <ElCard shadow="hover">
            <div class="stat-card">
              <div class="stat-label">较上期变动</div>
              <div
                class="stat-value"
                :style="{ color: (overview.change_value || 0) >= 0 ? '#67C23A' : '#F56C6C' }"
              >
                {{ overview.change_value >= 0 ? '+' : '' }}{{ formatValue(overview.change_value) }}
              </div>
            </div>
          </ElCard>
        </ElCol>
      </ElRow>

      <ElRow :gutter="16" class="analysis-cards">
        <ElCol :span="12">
          <ElCard shadow="hover">
            <template #header>
              <span>筹码集中度</span>
            </template>
            <div class="concentration-section">
              <ElProgress
                :percentage="overview.concentration || 0"
                :color="getConcentrationColor(overview.concentration)"
                :stroke-width="20"
              />
              <div class="concentration-detail">
                <span>TOP10基金占比: {{ overview.top10_ratio?.toFixed(1) || '-' }}%</span>
                <span>TOP20基金占比: {{ overview.top20_ratio?.toFixed(1) || '-' }}%</span>
              </div>
            </div>
          </ElCard>
        </ElCol>
        <ElCol :span="12">
          <ElCard shadow="hover">
            <template #header>
              <span>资金流向</span>
            </template>
            <div class="flow-section">
              <div class="flow-item">
                <ElTag type="success">增持 {{ overview.increase_count || 0 }} 只</ElTag>
              </div>
              <div class="flow-item">
                <ElTag type="danger">减持 {{ overview.decrease_count || 0 }} 只</ElTag>
              </div>
              <div class="flow-item">
                <ElTag type="primary">新进 {{ overview.new_count || 0 }} 只</ElTag>
              </div>
              <div class="flow-item">
                <ElTag type="info">退出 {{ overview.exit_count || 0 }} 只</ElTag>
              </div>
            </div>
          </ElCard>
        </ElCol>
      </ElRow>

      <ElCard shadow="hover" class="fund-list-card">
        <template #header>
          <div class="card-header">
            <span>主力基金排行</span>
            <div class="tab-buttons">
              <ElButton
                v-for="opt in changeTypeOptions"
                :key="opt.value"
                :type="activeTab === opt.value ? 'primary' : 'default'"
                size="small"
                @click="
                  activeTab = opt.value
                  handleTabChange()
                "
              >
                {{ opt.label }}
              </ElButton>
            </div>
          </div>
        </template>
        <Table
          :columns="tableColumns"
          :data="dataList"
          :loading="tableLoading"
          :pagination="{ total, pageSize, currentPage }"
          @register="tableRegister"
          @pageSizeChange="getList"
          @currentPageChange="getList"
        />
      </ElCard>
    </template>

    <ElEmpty v-else-if="!loading" description="请输入股票代码查询主力分析" />
  </ContentWrap>
</template>

<style scoped>
.search-bar {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}

.overview-cards {
  margin-bottom: 16px;
}

.stat-card {
  text-align: center;
  padding: 10px 0;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
}

.analysis-cards {
  margin-bottom: 16px;
}

.concentration-section {
  padding: 10px 0;
}

.concentration-detail {
  display: flex;
  justify-content: space-between;
  margin-top: 16px;
  font-size: 14px;
  color: #606266;
}

.flow-section {
  display: flex;
  justify-content: space-around;
  padding: 20px 0;
}

.flow-item {
  text-align: center;
}

.fund-list-card {
  margin-top: 16px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.tab-buttons {
  display: flex;
  gap: 8px;
}
</style>
