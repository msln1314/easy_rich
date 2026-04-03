<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import {
  ElCard,
  ElButton,
  ElTable,
  ElTableColumn,
  ElTag,
  ElPagination,
  ElSelect,
  ElOption,
  ElDatePicker,
  ElCheckbox,
  ElRow,
  ElCol,
  ElDialog,
  ElProgress,
  ElMessage
} from 'element-plus'
import { Refresh, Download, Sync } from '@element-plus/icons-vue'
import { ContentWrap } from '@/components/ContentWrap'
import SignalDetail from './components/SignalDetail.vue'
import {
  getSelectionSignals,
  getSignalStatistics,
  getBuySignals,
  syncSignals,
  recommendMap,
  signalValueMap,
  type SelectionSignalItem,
  type SignalStatistics
} from '@/api/stock/selectionSignal'

defineOptions({
  name: 'SelectionSignal'
})

// 加载状态
const loading = ref(false)
const syncing = ref(false)

// 数据
const signals = ref<SelectionSignalItem[]>([])
const statistics = ref<SignalStatistics | null>(null)

// 筛选条件
const filterForm = reactive({
  signal_date: '',
  recommend: '',
  min_score: undefined as number | undefined,
  max_score: undefined as number | undefined,
  ma_signal: undefined as number | undefined,
  macd_signal: undefined as number | undefined,
  kdj_signal: undefined as number | undefined,
  rsi_signal: undefined as number | undefined,
  volume_signal: undefined as number | undefined,
  industry: '',
  stock_name: ''
})

// 分页
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0
})

// 详情弹窗
const detailDialogVisible = ref(false)
const selectedStock = ref<SelectionSignalItem | null>(null)

// 推荐选项
const recommendOptions = [
  { label: '全部', value: '' },
  { label: '强买入', value: 'strong_buy' },
  { label: '买入', value: 'buy' },
  { label: '持有', value: 'hold' },
  { label: '卖出', value: 'sell' },
  { label: '强卖出', value: 'strong_sell' }
]

// 行业列表
const industries = ref<string[]>([])

// 获取统计数据
const fetchStatistics = async () => {
  try {
    const res = await getSignalStatistics(filterForm.signal_date || undefined)
    statistics.value = res.data || null
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
}

// 获取信号列表
const fetchSignals = async () => {
  loading.value = true
  try {
    const params: any = {
      page: pagination.page,
      page_size: pagination.pageSize
    }

    if (filterForm.signal_date) params.signal_date = filterForm.signal_date
    if (filterForm.recommend) params.recommend = filterForm.recommend
    if (filterForm.min_score !== undefined) params.min_score = filterForm.min_score
    if (filterForm.max_score !== undefined) params.max_score = filterForm.max_score
    if (filterForm.ma_signal !== undefined) params.ma_signal = filterForm.ma_signal
    if (filterForm.macd_signal !== undefined) params.macd_signal = filterForm.macd_signal
    if (filterForm.kdj_signal !== undefined) params.kdj_signal = filterForm.kdj_signal
    if (filterForm.rsi_signal !== undefined) params.rsi_signal = filterForm.rsi_signal
    if (filterForm.volume_signal !== undefined) params.volume_signal = filterForm.volume_signal
    if (filterForm.industry) params.industry = filterForm.industry
    if (filterForm.stock_name) params.stock_name = filterForm.stock_name

    const res = await getSelectionSignals(params)
    signals.value = res.data?.items || []
    pagination.total = res.data?.total || 0
  } catch (error) {
    ElMessage.error('获取信号列表失败')
  } finally {
    loading.value = false
  }
}

// 同步信号
const handleSync = async () => {
  syncing.value = true
  try {
    const res = await syncSignals(500)
    if (res.data?.is_success) {
      ElMessage.success(res.data.message || '同步成功')
      fetchStatistics()
      fetchSignals()
    } else {
      ElMessage.error(res.data?.message || '同步失败')
    }
  } catch (error) {
    ElMessage.error('同步失败')
  } finally {
    syncing.value = false
  }
}

// 筛选买入信号
const handleFilterBuy = async () => {
  filterForm.recommend = ''
  loading.value = true
  try {
    const res = await getBuySignals({
      signal_date: filterForm.signal_date || undefined,
      min_score: 50,
      limit: 100
    })
    signals.value = res.data || []
    pagination.total = signals.value.length
  } catch (error) {
    ElMessage.error('获取买入信号失败')
  } finally {
    loading.value = false
  }
}

// 重置筛选
const handleReset = () => {
  Object.assign(filterForm, {
    signal_date: '',
    recommend: '',
    min_score: undefined,
    max_score: undefined,
    ma_signal: undefined,
    macd_signal: undefined,
    kdj_signal: undefined,
    rsi_signal: undefined,
    volume_signal: undefined,
    industry: '',
    stock_name: ''
  })
  pagination.page = 1
  fetchSignals()
}

// 查看详情
const handleViewDetail = (row: SelectionSignalItem) => {
  selectedStock.value = row
  detailDialogVisible.value = true
}

// 格式化信号值
const formatSignal = (value: number | undefined) => {
  if (value === undefined || value === null) return '-'
  const map = signalValueMap[value]
  return map ? map.icon : '-'
}

// 获取信号颜色
const getSignalColor = (value: number | undefined) => {
  if (value === undefined || value === null) return '#909399'
  const map = signalValueMap[value]
  return map ? map.color : '#909399'
}

// 导出
const handleExport = () => {
  if (signals.value.length === 0) {
    ElMessage.warning('暂无数据可导出')
    return
  }

  const headers = [
    '排名',
    '代码',
    '名称',
    '价格',
    '涨跌幅',
    '评分',
    '推荐',
    '均线',
    'MACD',
    'KDJ',
    'RSI',
    '行业'
  ]
  const rows = signals.value.map((item) => [
    item.score_rank,
    item.stock_code,
    item.stock_name,
    item.current_price?.toFixed(2) || '-',
    item.change_percent?.toFixed(2) + '%' || '-',
    item.total_score?.toFixed(0) || '-',
    recommendMap[item.recommend]?.label || item.recommend,
    item.ma_signal === 1 ? '金叉' : item.ma_signal === -1 ? '死叉' : '-',
    item.macd_signal === 1 ? '金叉' : item.macd_signal === -1 ? '死叉' : '-',
    item.kdj_signal === 1 ? '金叉' : item.kdj_signal === -1 ? '死叉' : '-',
    item.rsi_signal === 1 ? '超卖' : item.rsi_signal === -1 ? '超买' : '-',
    item.industry || '-'
  ])

  const csvContent = [headers.join(','), ...rows.map((r) => r.join(','))].join('\n')
  const blob = new Blob(['\ufeff' + csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.download = `选股信号_${filterForm.signal_date || new Date().toISOString().split('T')[0]}.csv`
  link.click()
  ElMessage.success('导出成功')
}

// 分页变化
const handlePageChange = () => {
  fetchSignals()
}

// 初始化
onMounted(() => {
  fetchStatistics()
  fetchSignals()
})
</script>

<template>
  <ContentWrap>
    <div class="selection-signal-container">
      <!-- 统计概览 -->
      <ElCard class="statistics-card" shadow="never">
        <template #header>
          <div class="card-header">
            <span class="title">信号统计</span>
            <ElButton type="primary" :icon="Sync" :loading="syncing" @click="handleSync"
              >同步信号</ElButton
            >
          </div>
        </template>
        <ElRow :gutter="20" v-if="statistics">
          <ElCol :span="4">
            <div class="stat-item">
              <div class="stat-value">{{ statistics.total }}</div>
              <div class="stat-label">总数</div>
            </div>
          </ElCol>
          <ElCol :span="4">
            <div class="stat-item">
              <div class="stat-value text-danger">{{
                statistics.recommend_stats?.strong_buy || 0
              }}</div>
              <div class="stat-label">强买入</div>
            </div>
          </ElCol>
          <ElCol :span="4">
            <div class="stat-item">
              <div class="stat-value text-warning">{{ statistics.recommend_stats?.buy || 0 }}</div>
              <div class="stat-label">买入</div>
            </div>
          </ElCol>
          <ElCol :span="4">
            <div class="stat-item">
              <div class="stat-value text-info">{{ statistics.recommend_stats?.hold || 0 }}</div>
              <div class="stat-label">持有</div>
            </div>
          </ElCol>
          <ElCol :span="4">
            <div class="stat-item">
              <div class="stat-value text-success">{{ statistics.recommend_stats?.sell || 0 }}</div>
              <div class="stat-label">卖出</div>
            </div>
          </ElCol>
          <ElCol :span="4">
            <div class="stat-item">
              <div class="stat-value text-primary">{{
                statistics.recommend_stats?.strong_sell || 0
              }}</div>
              <div class="stat-label">强卖出</div>
            </div>
          </ElCol>
        </ElRow>
      </ElCard>

      <!-- 筛选条件 -->
      <ElCard class="filter-card" shadow="never">
        <template #header>
          <div class="card-header">
            <span class="title">筛选条件</span>
            <div class="actions">
              <ElButton type="success" @click="handleFilterBuy">买入信号</ElButton>
              <ElButton :icon="Refresh" @click="handleReset">重置</ElButton>
              <ElButton type="primary" @click="fetchSignals">查询</ElButton>
            </div>
          </div>
        </template>
        <ElRow :gutter="16">
          <ElCol :span="4">
            <ElDatePicker
              v-model="filterForm.signal_date"
              type="date"
              placeholder="信号日期"
              value-format="YYYY-MM-DD"
              style="width: 100%"
            />
          </ElCol>
          <ElCol :span="4">
            <ElSelect
              v-model="filterForm.recommend"
              placeholder="推荐信号"
              clearable
              style="width: 100%"
            >
              <ElOption
                v-for="opt in recommendOptions"
                :key="opt.value"
                :label="opt.label"
                :value="opt.value"
              />
            </ElSelect>
          </ElCol>
          <ElCol :span="4">
            <ElSelect
              v-model="filterForm.industry"
              placeholder="行业筛选"
              clearable
              filterable
              style="width: 100%"
            >
              <ElOption v-for="ind in industries" :key="ind" :label="ind" :value="ind" />
            </ElSelect>
          </ElCol>
          <ElCol :span="8">
            <div class="checkbox-group">
              <ElCheckbox v-model="filterForm.macd_signal" :true-label="1" :false-label="undefined"
                >MACD金叉</ElCheckbox
              >
              <ElCheckbox v-model="filterForm.kdj_signal" :true-label="1" :false-label="undefined"
                >KDJ金叉</ElCheckbox
              >
              <ElCheckbox v-model="filterForm.ma_signal" :true-label="1" :false-label="undefined"
                >均线金叉</ElCheckbox
              >
              <ElCheckbox
                v-model="filterForm.volume_signal"
                :true-label="1"
                :false-label="undefined"
                >放量</ElCheckbox
              >
            </div>
          </ElCol>
        </ElRow>
      </ElCard>

      <!-- 信号列表 -->
      <ElCard class="table-card" shadow="never">
        <template #header>
          <div class="card-header">
            <span class="title">信号列表 (共 {{ pagination.total }} 条)</span>
            <ElButton type="primary" :icon="Download" @click="handleExport">导出</ElButton>
          </div>
        </template>

        <ElTable
          :data="signals"
          stripe
          v-loading="loading"
          max-height="500"
          @row-click="handleViewDetail"
          highlight-current-row
        >
          <ElTableColumn prop="score_rank" label="排名" width="70" align="center" fixed />
          <ElTableColumn prop="stock_code" label="代码" width="100" />
          <ElTableColumn prop="stock_name" label="名称" width="100" />
          <ElTableColumn prop="current_price" label="价格" width="80" align="right">
            <template #default="{ row }">{{ row.current_price?.toFixed(2) || '-' }}</template>
          </ElTableColumn>
          <ElTableColumn prop="change_percent" label="涨跌幅" width="90" align="right">
            <template #default="{ row }">
              <span
                :class="
                  row.change_percent > 0 ? 'text-up' : row.change_percent < 0 ? 'text-down' : ''
                "
              >
                {{ row.change_percent?.toFixed(2) || '-' }}%
              </span>
            </template>
          </ElTableColumn>
          <ElTableColumn prop="total_score" label="评分" width="70" align="center" sortable>
            <template #default="{ row }">
              <ElProgress
                :percentage="row.total_score || 0"
                :stroke-width="8"
                :show-text="false"
                :color="
                  row.total_score >= 60 ? '#67C23A' : row.total_score >= 40 ? '#E6A23C' : '#909399'
                "
              />
              <span>{{ row.total_score?.toFixed(0) || '-' }}</span>
            </template>
          </ElTableColumn>
          <ElTableColumn prop="recommend" label="推荐" width="80" align="center">
            <template #default="{ row }">
              <ElTag
                v-if="recommendMap[row.recommend]"
                :type="recommendMap[row.recommend].type"
                size="small"
              >
                {{ recommendMap[row.recommend].label }}
              </ElTag>
              <span v-else>-</span>
            </template>
          </ElTableColumn>
          <ElTableColumn prop="ma_signal" label="均线" width="60" align="center">
            <template #default="{ row }">
              <span :style="{ color: getSignalColor(row.ma_signal) }">{{
                formatSignal(row.ma_signal)
              }}</span>
            </template>
          </ElTableColumn>
          <ElTableColumn prop="macd_signal" label="MACD" width="60" align="center">
            <template #default="{ row }">
              <span :style="{ color: getSignalColor(row.macd_signal) }">{{
                formatSignal(row.macd_signal)
              }}</span>
            </template>
          </ElTableColumn>
          <ElTableColumn prop="kdj_signal" label="KDJ" width="60" align="center">
            <template #default="{ row }">
              <span :style="{ color: getSignalColor(row.kdj_signal) }">{{
                formatSignal(row.kdj_signal)
              }}</span>
            </template>
          </ElTableColumn>
          <ElTableColumn prop="rsi_signal" label="RSI" width="60" align="center">
            <template #default="{ row }">
              <span :style="{ color: getSignalColor(row.rsi_signal) }">{{
                formatSignal(row.rsi_signal)
              }}</span>
            </template>
          </ElTableColumn>
          <ElTableColumn prop="industry" label="行业" width="100" />
        </ElTable>

        <div class="pagination-wrapper">
          <ElPagination
            v-model:current-page="pagination.page"
            v-model:page-size="pagination.pageSize"
            :page-sizes="[20, 50, 100]"
            :total="pagination.total"
            layout="total, sizes, prev, pager, next"
            @size-change="handlePageChange"
            @current-change="handlePageChange"
          />
        </div>
      </ElCard>

      <!-- 详情弹窗 -->
      <ElDialog v-model="detailDialogVisible" title="信号详情" width="800px" destroy-on-close>
        <SignalDetail v-if="selectedStock" :stock="selectedStock" />
      </ElDialog>
    </div>
  </ContentWrap>
</template>

<style lang="scss" scoped>
.selection-signal-container {
  .statistics-card {
    margin-bottom: 16px;
  }

  .filter-card {
    margin-bottom: 16px;
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;

    .title {
      font-size: 16px;
      font-weight: 600;
    }

    .actions {
      display: flex;
      gap: 8px;
    }
  }

  .stat-item {
    text-align: center;
    padding: 12px 0;

    .stat-value {
      font-size: 24px;
      font-weight: 600;
      color: #303133;
    }

    .stat-label {
      font-size: 14px;
      color: #909399;
      margin-top: 4px;
    }
  }

  .checkbox-group {
    display: flex;
    gap: 12px;
    align-items: center;
    height: 32px;
  }

  .pagination-wrapper {
    margin-top: 16px;
    display: flex;
    justify-content: flex-end;
  }
}

.text-up {
  color: #f56c6c;
}

.text-down {
  color: #67c23a;
}

.text-danger {
  color: #f56c6c;
}

.text-warning {
  color: #e6a23c;
}

.text-info {
  color: #909399;
}

.text-success {
  color: #67c23a;
}

.text-primary {
  color: #409eff;
}

:deep(.el-table__row) {
  cursor: pointer;
}
</style>
