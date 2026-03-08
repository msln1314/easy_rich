<template>
  <div class="daily-ranking-container">
    <el-card class="filter-card">
      <el-form :model="filterForm" inline>
        <el-form-item label="排行类型">
          <el-select v-model="filterForm.rankingType" @change="handleRankingTypeChange">
            <el-option label="换手率排行" value="turnover" />
            <el-option label="成交量排行" value="volume" />
            <el-option label="成交额排行" value="amount" />
            <el-option label="涨跌幅排行" value="change_percent" />
            <el-option label="热度排行" value="hot" />
          </el-select>
        </el-form-item>
        <el-form-item label="行业">
          <el-select v-model="filterForm.industry" clearable placeholder="全部行业" @change="handleSearch">
            <el-option v-for="ind in industries" :key="ind" :label="ind" :value="ind" />
          </el-select>
        </el-form-item>
        <el-form-item label="市场">
          <el-select v-model="filterForm.market" clearable placeholder="全部市场" @change="handleSearch">
            <el-option label="上海" value="SH" />
            <el-option label="深圳" value="SZ" />
          </el-select>
        </el-form-item>
        <el-form-item label="日期">
          <el-date-picker
            v-model="filterForm.dataDate"
            type="date"
            placeholder="选择日期"
            value-format="YYYY-MM-DD"
            @change="handleSearch"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="handleSync">同步数据</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="ranking-card">
      <template #header>
        <div class="card-header">
          <span>{{ rankingTypeLabel }}排行</span>
          <el-radio-group v-model="dataSource" size="small" @change="handleDataSourceChange">
            <el-radio-button label="realtime">实时</el-radio-button>
            <el-radio-button label="history">历史</el-radio-button>
          </el-radio-group>
        </div>
      </template>

      <el-table
        :data="tableData"
        stripe
        style="width: 100%"
        v-loading="loading"
        max-height="600"
      >
        <el-table-column prop="rank" label="排名" width="80" align="center">
          <template #default="{ row }">
            <el-tag :type="getRankTagType(row.rank)" size="small">
              {{ row.rank }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="stockCode" label="股票代码" width="100">
          <template #default="{ row }">
            <el-link type="primary" @click="handleViewStock(row)">
              {{ row.stockCode }}
            </el-link>
          </template>
        </el-table-column>
        <el-table-column prop="stockName" label="股票名称" width="120" />
        <el-table-column prop="industry" label="行业" width="100" />
        <el-table-column :label="rankingValueLabel" width="120" align="right">
          <template #default="{ row }">
            {{ formatRankingValue(row) }}
          </template>
        </el-table-column>
        <el-table-column prop="currentPrice" label="最新价" width="100" align="right">
          <template #default="{ row }">
            {{ row.currentPrice?.toFixed(2) || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="changePercent" label="涨跌幅" width="100" align="right">
          <template #default="{ row }">
            <span :class="getChangeClass(row.changePercent)">
              {{ row.changePercent?.toFixed(2) || '-' }}%
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="volume" label="成交量" width="120" align="right">
          <template #default="{ row }">
            {{ formatNumber(row.volume) }} 手
          </template>
        </el-table-column>
        <el-table-column prop="turnoverRate" label="换手率" width="100" align="right">
          <template #default="{ row }">
            {{ row.turnoverRate?.toFixed(2) || '-' }}%
          </template>
        </el-table-column>
        <el-table-column label="操作" width="100" align="center">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="handleViewTrend(row)">
              趋势
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-container">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[20, 50, 100]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSearch"
          @current-change="handleSearch"
        />
      </div>
    </el-card>

    <!-- 趋势弹窗 -->
    <el-dialog
      v-model="trendDialogVisible"
      :title="`${selectedStock?.stockName} (${selectedStock?.stockCode}) 排行趋势`"
      width="800px"
    >
      <div class="trend-content">
        <el-radio-group v-model="trendType" @change="handleTrendTypeChange" style="margin-bottom: 16px;">
          <el-radio-button label="turnover">换手率</el-radio-button>
          <el-radio-button label="volume">成交量</el-radio-button>
          <el-radio-button label="amount">成交额</el-radio-button>
          <el-radio-button label="hot">热度</el-radio-button>
        </el-radio-group>
        <v-chart class="trend-chart" :option="trendChartOption" autoresize />
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, DataZoomComponent } from 'echarts/components'
import {
  getDailyRanking,
  getRealtimeRanking,
  getHotRanking,
  getRankingTrend,
  syncDailyRanking,
  getIndustries,
} from '/@/api/stock/dailyRanking'

use([CanvasRenderer, LineChart, GridComponent, TooltipComponent, DataZoomComponent])

const router = useRouter()

// 筛选表单
const filterForm = ref({
  rankingType: 'turnover',
  industry: '',
  market: '',
  dataDate: '',
})

// 数据源：实时或历史
const dataSource = ref('realtime')

// 表格数据
const tableData = ref([])
const loading = ref(false)
const industries = ref<string[]>([])

// 分页
const pagination = ref({
  page: 1,
  pageSize: 50,
  total: 0,
})

// 趋势弹窗
const trendDialogVisible = ref(false)
const selectedStock = ref<RankingItem | null>(null)
const trendType = ref('turnover')
const trendData = ref<Array<{ date: string; rank: number; value: number }>>([])

// 排行类型标签映射
const rankingTypeLabelMap: Record<string, string> = {
  turnover: '换手率',
  volume: '成交量',
  amount: '成交额',
  change_percent: '涨跌幅',
  hot: '热度',
}

const rankingTypeLabel = computed(() => rankingTypeLabelMap[filterForm.value.rankingType] || '排行')

// 排行数值标签映射
const rankingValueLabel = computed(() => {
  const map: Record<string, string> = {
    turnover: '换手率',
    volume: '成交量',
    amount: '成交额',
    change_percent: '涨跌幅',
    hot: '热度值',
  }
  return map[filterForm.value.rankingType] || '排行值'
})

// 图表配置
const trendChartOption = computed(() => ({
  tooltip: {
    trigger: 'axis',
    formatter: (params) => {
      const p = params[0]
      return `${p.name}<br/>排名: ${p.data[1]}`
    },
  },
  grid: {
    left: '10%',
    right: '10%',
    bottom: '15%',
  },
  xAxis: {
    type: 'category',
    data: trendData.value.map((item) => item.date),
  },
  yAxis: {
    type: 'value',
    inverse: true,
    name: '排名',
    min: 1,
    max: (val) => Math.max(val.max, 100),
  },
  dataZoom: [
    {
      type: 'slider',
      start: 0,
      end: 100,
    },
  ],
  series: [
    {
      data: trendData.value.map((item) => [item.date, item.rank]),
      type: 'line',
      smooth: true,
      lineStyle: {
        width: 2,
      },
      areaStyle: {
        opacity: 0.1,
      },
    },
  ],
}))

// 获取排行标签样式
function getRankTagType(rank: number): string {
  if (rank <= 3) return 'danger'
  if (rank <= 10) return 'warning'
  return 'info'
}

// 获取涨跌幅样式
function getChangeClass(changePercent: number): string {
  if (!changePercent) return ''
  return changePercent > 0 ? 'text-up' : changePercent < 0 ? 'text-down' : ''
}

// 格式化排行数值
function formatRankingValue(row: RankingItem): string {
  const { rankingType } = filterForm.value
  if (rankingType === 'turnover' || rankingType === 'change_percent') {
    return `${(row.turnoverRate || row.changePercent || 0).toFixed(2)}%`
  }
  if (rankingType === 'amount') {
    return formatNumber(row.amount)
  }
  if (rankingType === 'volume') {
    return formatNumber(row.volume)
  }
  return '-'
}

// 格式化数字
function formatNumber(num: number): string {
  if (!num) return '0'
  if (num >= 100000000) return (num / 100000000).toFixed(2) + '亿'
  if (num >= 10000) return (num / 10000).toFixed(2) + '万'
  return num.toFixed(0)
}

// 获取行业列表
async function fetchIndustries() {
  try {
    const res = await getIndustries(filterForm.value.rankingType)
    industries.value = res.data || []
  } catch (error) {
    console.error('获取行业列表失败:', error)
  }
}

// 获取表格数据
async function fetchData() {
  loading.value = true
  try {
    const params = {
      rankingType: filterForm.value.rankingType,
      industry: filterForm.value.industry || undefined,
      market: filterForm.value.market || undefined,
      dataDate: filterForm.value.dataDate || undefined,
      page: pagination.value.page,
      pageSize: pagination.value.pageSize,
    }

    let res
    if (dataSource.value === 'realtime') {
      if (filterForm.value.rankingType === 'hot') {
        res = await getHotRanking({ ...params, limit: pagination.value.pageSize })
      } else {
        res = await getRealtimeRanking({ ...params, limit: pagination.value.pageSize })
      }
    } else {
      res = await getDailyRanking(params)
    }

    if (res.data?.items) {
      tableData.value = res.data.items
      pagination.value.total = res.data.total || 0
    } else if (Array.isArray(res.data)) {
      tableData.value = res.data
      pagination.value.total = res.data.length
    } else {
      tableData.value = []
      pagination.value.total = 0
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
  pagination.value.page = 1
  fetchData()
}

// 排行类型变化
function handleRankingTypeChange() {
  filterForm.value.industry = ''
  fetchIndustries()
  handleSearch()
}

// 数据源变化
function handleDataSourceChange() {
  pagination.value.page = 1
  fetchData()
}

// 同步数据
async function handleSync() {
  try {
    await ElMessageBox.confirm('确认同步今日排行数据？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    const res = await syncDailyRanking({
      dataDate: filterForm.value.dataDate || undefined,
    })
    if (res.code === ResultEnum.SUCCESS) {
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

// 查看股票
function handleViewStock(row: RankingItem) {
  router.push({
    path: '/stock/analysis',
    query: { code: row.stockCode },
  })
}

// 查看趋势
async function handleViewTrend(row: RankingItem) {
  selectedStock.value = row
  trendDialogVisible.value = true
  await fetchTrendData(row.stockCode)
}

// 获取趋势数据
async function fetchTrendData(stockCode: string) {
  try {
    const res = await getRankingTrend({
      stockCode,
      rankingType: trendType.value,
      startDate: undefined,
      endDate: undefined,
    })
    if (res.data?.trendData) {
      trendData.value = res.data.trendData.map((item) => ({
        date: item.dataDate,
        rank: item.rank,
        value: item.rankingValue || 0,
      }))
    }
  } catch (error) {
    console.error('获取趋势数据失败:', error)
  }
}

// 趋势类型变化
async function handleTrendTypeChange() {
  if (selectedStock.value) {
    await fetchTrendData(selectedStock.value.stockCode)
  }
}

// 初始化
onMounted(() => {
  fetchIndustries()
  fetchData()
})
</script>

<style scoped lang="scss">
.daily-ranking-container {
  padding: 16px;

  .filter-card {
    margin-bottom: 16px;
  }

  .ranking-card {
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
  }

  .pagination-container {
    margin-top: 16px;
    display: flex;
    justify-content: flex-end;
  }

  .trend-content {
    .trend-chart {
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
</style>