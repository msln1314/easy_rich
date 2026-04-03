<template>
  <div class="ranking-container">
    <!-- 筛选条件 -->
    <ElCard class="filter-card">
      <ElForm :model="filterForm" inline>
        <ElFormItem label="数据源">
          <ElRadioGroup v-model="dataSource" @change="handleDataSourceChange">
            <ElRadioButton label="realtime">实时排行</ElRadioButton>
            <ElRadioButton label="history">历史排行</ElRadioButton>
          </ElRadioGroup>
        </ElFormItem>
        <ElFormItem label="排行类型">
          <ElSelect v-model="filterForm.rankingType" @change="handleRankingTypeChange">
            <ElOption
              v-for="type in rankingTypeOptions"
              :key="type.value"
              :label="type.label"
              :value="type.value"
            />
          </ElSelect>
        </ElFormItem>
        <ElFormItem v-if="filterForm.rankingType === 'change_percent'" label="排序">
          <ElSelect v-model="filterForm.order" @change="handleSearch">
            <ElOption label="降序" value="desc" />
            <ElOption label="升序" value="asc" />
          </ElSelect>
        </ElFormItem>
        <ElFormItem label="行业">
          <ElSelect
            v-model="filterForm.industry"
            clearable
            placeholder="全部行业"
            @change="handleSearch"
          >
            <ElOption v-for="ind in industries" :key="ind" :label="ind" :value="ind" />
          </ElSelect>
        </ElFormItem>
        <ElFormItem label="市场">
          <ElSelect
            v-model="filterForm.market"
            clearable
            placeholder="全部市场"
            @change="handleSearch"
          >
            <ElOption label="上海" value="SH" />
            <ElOption label="深圳" value="SZ" />
          </ElSelect>
        </ElFormItem>
        <ElFormItem v-if="dataSource === 'history'" label="日期">
          <ElDatePicker
            v-model="filterForm.dataDate"
            type="date"
            placeholder="选择日期"
            value-format="YYYY-MM-DD"
            @change="handleSearch"
          />
        </ElFormItem>
        <ElFormItem>
          <ElButton type="primary" @click="handleSearch">查询</ElButton>
          <ElButton @click="handleRefresh">
            <ElIcon><Refresh /></ElIcon>
            刷新
          </ElButton>
          <ElButton v-if="dataSource === 'history'" type="success" @click="handleSync">
            <ElIcon><Upload /></ElIcon>
            同步数据
          </ElButton>
        </ElFormItem>
      </ElForm>
    </ElCard>

    <!-- 排行表格 -->
    <ElCard class="table-card">
      <template #header>
        <div class="card-header">
          <span>{{ pageTitle }}</span>
          <span class="subtitle">{{ dataSource === 'realtime' ? '实时数据' : '历史数据' }}</span>
        </div>
      </template>

      <ElTable
        :data="tableData"
        stripe
        style="width: 100%"
        v-loading="loading"
        max-height="600"
        @row-click="handleRowClick"
        highlight-current-row
      >
        <ElTableColumn prop="rank" label="排名" width="80" align="center" fixed>
          <template #default="scope">
            <ElTag :type="getRankTagType(scope.row.rank)" size="small">
              {{ scope.row.rank }}
            </ElTag>
          </template>
        </ElTableColumn>
        <ElTableColumn prop="stock_code" label="股票代码" width="110">
          <template #default="scope">
            <ElLink type="primary" @click.stop="handleViewStock(scope.row)">
              {{ scope.row.stock_code }}
            </ElLink>
          </template>
        </ElTableColumn>
        <ElTableColumn prop="stock_name" label="股票名称" width="120" show-overflow-tooltip />
        <ElTableColumn prop="industry" label="行业" width="100" show-overflow-tooltip />
        <ElTableColumn prop="market" label="市场" width="70" align="center">
          <template #default="scope">
            <ElTag size="small" :type="scope.row.market === 'SH' ? 'warning' : 'success'">
              {{ scope.row.market }}
            </ElTag>
          </template>
        </ElTableColumn>
        <ElTableColumn :label="rankingValueLabel" width="130" align="right">
          <template #default="scope">
            {{ formatRankingValue(scope.row) }}
          </template>
        </ElTableColumn>
        <ElTableColumn prop="current_price" label="最新价" width="100" align="right">
          <template #default="scope">
            {{ formatPrice(scope.row.current_price) }}
          </template>
        </ElTableColumn>
        <ElTableColumn prop="change_percent" label="涨跌幅" width="100" align="right">
          <template #default="scope">
            <span :class="getChangeClass(scope.row.change_percent)">
              {{ formatChangePercent(scope.row.change_percent) }}
            </span>
          </template>
        </ElTableColumn>
        <ElTableColumn prop="volume" label="成交量" width="120" align="right">
          <template #default="scope">
            {{ formatNumber(scope.row.volume) }}
          </template>
        </ElTableColumn>
        <ElTableColumn prop="amount" label="成交额" width="120" align="right">
          <template #default="scope">
            {{ formatAmount(scope.row.amount) }}
          </template>
        </ElTableColumn>
        <ElTableColumn prop="turnover_rate" label="换手率" width="90" align="right">
          <template #default="scope">
            {{ formatTurnoverRate(scope.row.turnover_rate) }}
          </template>
        </ElTableColumn>
        <ElTableColumn label="操作" width="120" align="center" fixed="right">
          <template #default="scope">
            <ElButton type="primary" link size="small" @click.stop="handleViewTrend(scope.row)">
              趋势
            </ElButton>
            <ElButton
              v-if="filterForm.rankingType === 'hot'"
              type="info"
              link
              size="small"
              @click.stop="handleViewHotDetail(scope.row)"
            >
              详情
            </ElButton>
          </template>
        </ElTableColumn>
      </ElTable>

      <div class="pagination-container">
        <ElPagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[20, 50, 100, 200]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSearch"
          @current-change="handleSearch"
        />
      </div>
    </ElCard>

    <!-- 趋势弹窗 -->
    <ElDialog
      v-model="trendDialogVisible"
      :title="`${selectedStock?.stock_name} (${selectedStock?.stock_code}) 排行趋势`"
      width="900px"
    >
      <div class="trend-content">
        <ElRadioGroup
          v-model="trendType"
          @change="handleTrendTypeChange"
          style="margin-bottom: 16px"
        >
          <ElRadioButton v-for="type in trendTypeOptions" :key="type.value" :label="type.value">
            {{ type.label }}
          </ElRadioButton>
        </ElRadioGroup>
        <v-chart class="trend-chart" :option="trendChartOption" autoresize />
      </div>
    </ElDialog>

    <!-- 热度详情弹窗 -->
    <ElDialog
      v-model="hotDetailDialogVisible"
      :title="`${selectedStock?.stock_name} (${selectedStock?.stock_code}) 热度详情`"
      width="900px"
    >
      <div class="hot-detail-content">
        <v-chart class="hot-chart" :option="hotChartOption" autoresize />
      </div>
    </ElDialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, reactive } from 'vue'
import { useRouter } from 'vue-router'
import {
  ElMessage,
  ElMessageBox,
  ElCard,
  ElForm,
  ElFormItem,
  ElRadioGroup,
  ElRadioButton,
  ElSelect,
  ElOption,
  ElDatePicker,
  ElButton,
  ElIcon,
  ElTable,
  ElTableColumn,
  ElTag,
  ElLink,
  ElPagination,
  ElDialog
} from 'element-plus'
import { Refresh, Upload } from '@element-plus/icons-vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart, BarChart } from 'echarts/charts'
import {
  GridComponent,
  TooltipComponent,
  DataZoomComponent,
  LegendComponent
} from 'echarts/components'
import {
  getDailyRanking,
  getRealtimeRanking,
  getHotRanking,
  getRankingTrend,
  syncDailyRanking,
  getIndustries,
  getHotDetail
} from '@/api/stock/dailyRanking'

use([
  CanvasRenderer,
  LineChart,
  BarChart,
  GridComponent,
  TooltipComponent,
  DataZoomComponent,
  LegendComponent
])

const router = useRouter()

// 排行类型选项
const rankingTypeOptions = computed(() => {
  if (dataSource.value === 'realtime') {
    return [
      { label: '换手率', value: 'turnover' },
      { label: '成交量', value: 'volume' },
      { label: '成交额', value: 'amount' },
      { label: '涨跌幅', value: 'change_percent' }
    ]
  }
  return [
    { label: '换手率', value: 'turnover' },
    { label: '成交量', value: 'volume' },
    { label: '成交额', value: 'amount' },
    { label: '涨跌幅', value: 'change_percent' },
    { label: '热度', value: 'hot' }
  ]
})

// 趋势类型选项
const trendTypeOptions = [
  { label: '换手率', value: 'turnover' },
  { label: '成交量', value: 'volume' },
  { label: '成交额', value: 'amount' },
  { label: '热度', value: 'hot' }
]

// 筛选表单
const filterForm = reactive({
  rankingType: 'turnover',
  order: 'desc',
  industry: '',
  market: '',
  dataDate: ''
})

// 数据源
const dataSource = ref<'realtime' | 'history'>('realtime')

// 表格数据
const tableData = ref<any[]>([])
const loading = ref(false)
const industries = ref<string[]>([])

// 分页
const pagination = reactive({
  page: 1,
  pageSize: 50,
  total: 0
})

// 趋势弹窗
const trendDialogVisible = ref(false)
const selectedStock = ref<any>(null)
const trendType = ref('turnover')
const trendData = ref<Array<{ date: string; rank: number; value: number }>>([])

// 热度详情弹窗
const hotDetailDialogVisible = ref(false)
const hotDetailData = ref<any>(null)

// 页面标题
const pageTitle = computed(() => {
  const map: Record<string, string> = {
    turnover: '换手率',
    volume: '成交量',
    amount: '成交额',
    change_percent: '涨跌幅',
    hot: '热度'
  }
  return `${map[filterForm.rankingType]}排行`
})

// 排行数值标签
const rankingValueLabel = computed(() => {
  const map: Record<string, string> = {
    turnover: '换手率(%)',
    volume: '成交量(手)',
    amount: '成交额(元)',
    change_percent: '涨跌幅(%)',
    hot: '热度值'
  }
  return map[filterForm.rankingType] || '排行值'
})

// 图表配置
const trendChartOption = computed(() => ({
  tooltip: {
    trigger: 'axis',
    formatter: (params: any) => {
      const p = params[0]
      return `${p.name}<br/>排名: ${p.data[1]}`
    }
  },
  grid: {
    left: '10%',
    right: '10%',
    bottom: '15%'
  },
  xAxis: {
    type: 'category',
    data: trendData.value.map((item) => item.date)
  },
  yAxis: {
    type: 'value',
    inverse: true,
    name: '排名',
    min: 1,
    max: (val: any) => Math.max(val.max, 100)
  },
  dataZoom: [
    {
      type: 'slider',
      start: 0,
      end: 100
    }
  ],
  series: [
    {
      data: trendData.value.map((item) => [item.date, item.rank]),
      type: 'line',
      smooth: true,
      lineStyle: {
        width: 2
      },
      areaStyle: {
        opacity: 0.1
      }
    }
  ]
}))

// 热度详情图表配置
const hotChartOption = computed(() => {
  if (!hotDetailData.value?.trend_data) return {}
  const data = hotDetailData.value.trend_data
  return {
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: ['排名', '热度值', '浏览量'],
      bottom: 0
    },
    grid: {
      left: '10%',
      right: '10%',
      bottom: '15%'
    },
    xAxis: {
      type: 'category',
      data: data.map((item: any) => item.data_date)
    },
    yAxis: [
      {
        type: 'value',
        inverse: true,
        name: '排名',
        position: 'left'
      },
      {
        type: 'value',
        name: '数值',
        position: 'right'
      }
    ],
    series: [
      {
        name: '排名',
        type: 'line',
        data: data.map((item: any) => item.rank),
        yAxisIndex: 0,
        smooth: true
      },
      {
        name: '热度值',
        type: 'bar',
        data: data.map((item: any) => item.hot_value || 0),
        yAxisIndex: 1
      }
    ]
  }
})

// 获取排行标签样式
function getRankTagType(rank: number): string {
  if (rank === 1) return 'danger'
  if (rank === 2) return 'warning'
  if (rank === 3) return 'success'
  return 'info'
}

// 获取涨跌幅样式
function getChangeClass(changePercent: number): string {
  if (!changePercent && changePercent !== 0) return ''
  return changePercent > 0 ? 'text-up' : changePercent < 0 ? 'text-down' : ''
}

// 格式化涨跌幅
function formatChangePercent(value: number): string {
  if (!value && value !== 0) return '-'
  const prefix = value > 0 ? '+' : ''
  return `${prefix}${value.toFixed(2)}%`
}

// 格式化排行数值
function formatRankingValue(row: any): string {
  const { rankingType } = filterForm
  if (rankingType === 'turnover' || rankingType === 'change_percent') {
    return `${(row.turnover_rate || row.change_percent || 0).toFixed(2)}%`
  }
  if (rankingType === 'amount') {
    return formatAmount(row.amount)
  }
  if (rankingType === 'volume') {
    return formatNumber(row.volume)
  }
  if (rankingType === 'hot') {
    return row.hot_value?.toFixed(0) || '-'
  }
  return '-'
}

// 格式化数字（成交量）
function formatNumber(num: number): string {
  if (!num && num !== 0) return '-'
  if (num >= 100000000) return (num / 100000000).toFixed(2) + '亿'
  if (num >= 10000) return (num / 10000).toFixed(2) + '万'
  return num.toFixed(0)
}

// 格式化金额
function formatAmount(amount: number): string {
  if (!amount && amount !== 0) return '-'
  if (amount >= 100000000) return (amount / 100000000).toFixed(2) + '亿'
  if (amount >= 10000) return (amount / 10000).toFixed(2) + '万'
  return amount.toFixed(2)
}

// 格式化价格
function formatPrice(price: number): string {
  if (!price && price !== 0) return '-'
  return price.toFixed(2)
}

// 格式化换手率
function formatTurnoverRate(rate: number): string {
  if (!rate && rate !== 0) return '-'
  return rate.toFixed(2) + '%'
}

// 获取行业列表
async function fetchIndustries() {
  try {
    const res = await getIndustries(filterForm.rankingType)
    industries.value = res.data || []
  } catch (error) {
    console.error('获取行业列表失败:', error)
  }
}

// 获取表格数据
async function fetchData() {
  loading.value = true
  try {
    const params: any = {
      rankingType: filterForm.rankingType,
      industry: filterForm.industry || undefined,
      market: filterForm.market || undefined,
      dataDate: filterForm.dataDate || undefined,
      page: pagination.page,
      pageSize: pagination.pageSize
    }

    let res: any
    if (dataSource.value === 'realtime') {
      if (filterForm.rankingType === 'hot') {
        // 实时模式不支持热度排行
        filterForm.rankingType = 'turnover'
        params.rankingType = 'turnover'
      }
      res = await getRealtimeRanking({ ...params, limit: pagination.pageSize })
    } else {
      if (filterForm.rankingType === 'hot') {
        res = await getHotRanking({ ...params })
      } else {
        res = await getDailyRanking(params)
      }
    }

    if (res.data?.items) {
      tableData.value = res.data.items
      pagination.total = res.data.total || 0
    } else if (Array.isArray(res.data)) {
      tableData.value = res.data
      pagination.total = res.data.length
    } else {
      tableData.value = []
      pagination.total = 0
    }
  } catch (error) {
    console.error('获取排行数据失败:', error)
    ElMessage.error('获取排行数据失败')
  } finally {
    loading.value = false
  }
}

// 查询
function handleSearch() {
  pagination.page = 1
  fetchData()
}

// 排行类型变化
function handleRankingTypeChange() {
  filterForm.industry = ''
  fetchIndustries()
  handleSearch()
}

// 数据源变化
function handleDataSourceChange() {
  pagination.page = 1
  // 重置排行类型
  filterForm.rankingType = 'turnover'
  fetchIndustries()
  fetchData()
}

// 刷新
function handleRefresh() {
  fetchData()
  ElMessage.success('刷新成功')
}

// 同步数据
async function handleSync() {
  try {
    await ElMessageBox.confirm('确认同步今日排行数据？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    const res = await syncDailyRanking({
      dataDate: filterForm.dataDate || undefined
    })
    if (res.code === 200) {
      ElMessage.success('同步成功')
      fetchData()
    } else {
      ElMessage.error(res.message || '同步失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('同步失败')
    }
  }
}

// 点击行
function handleRowClick(row: any) {
  // 可以添加点击行的事件
}

// 查看股票
function handleViewStock(row: any) {
  router.push({
    path: '/stock/analysis',
    query: { code: row.stock_code }
  })
}

// 查看趋势
async function handleViewTrend(row: any) {
  selectedStock.value = row
  trendType.value = filterForm.rankingType
  trendDialogVisible.value = true
  await fetchTrendData(row.stock_code)
}

// 获取趋势数据
async function fetchTrendData(stockCode: string) {
  try {
    const res = await getRankingTrend({
      stockCode,
      rankingType: trendType.value as any
    })
    if (res.data?.trendData) {
      trendData.value = res.data.trendData.map((item: any) => ({
        date: item.data_date,
        rank: item.rank,
        value: item.ranking_value || 0
      }))
    }
  } catch (error) {
    console.error('获取趋势数据失败:', error)
  }
}

// 趋势类型变化
async function handleTrendTypeChange() {
  if (selectedStock.value) {
    await fetchTrendData(selectedStock.value.stock_code)
  }
}

// 查看热度详情
async function handleViewHotDetail(row: any) {
  selectedStock.value = row
  hotDetailDialogVisible.value = true
  try {
    const res = await getHotDetail(row.stock_code, 30)
    hotDetailData.value = res.data
  } catch (error) {
    console.error('获取热度详情失败:', error)
  }
}

// 初始化
onMounted(() => {
  fetchIndustries()
  fetchData()
})
</script>

<style scoped lang="scss">
.ranking-container {
  padding: 16px;

  .filter-card {
    margin-bottom: 16px;
  }

  .table-card {
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;

      .subtitle {
        font-size: 12px;
        color: #909399;
      }
    }
  }

  .pagination-container {
    margin-top: 16px;
    display: flex;
    justify-content: flex-end;
  }

  .trend-content,
  .hot-detail-content {
    .trend-chart,
    .hot-chart {
      height: 400px;
    }
  }
}

.text-up {
  color: #f56c6c;
}

.text-down {
  color: #67c23a;
}

:deep(.el-table__row) {
  cursor: pointer;
}
</style>
