<template>
  <div class="stock-ranking">
    <t-card title="个股排行" :bordered="false">
      <!-- 排行类型 Tab -->
      <t-tabs v-model="rankingType" @change="handleRankingTypeChange">
        <t-tab-panel
          v-for="type in rankingTypes"
          :key="type.value"
          :value="type.value"
          :label="type.label"
        />
      </t-tabs>

      <!-- 筛选和搜索 -->
      <div class="filter-bar">
        <t-space>
          <t-input
            v-model="searchKeyword"
            placeholder="搜索股票代码或名称"
            clearable
            style="width: 200px"
            @enter="handleSearch"
          >
            <template #suffix-icon>
              <t-icon name="search" @click="handleSearch" />
            </template>
          </t-input>

          <t-select
            v-model="industry"
            placeholder="选择行业"
            clearable
            style="width: 150px"
            :options="industryOptions"
            @change="handleSearch"
          />

          <t-select
            v-model="market"
            placeholder="选择市场"
            clearable
            style="width: 120px"
            :options="marketOptions"
            @change="handleSearch"
          />

          <t-select
            v-if="rankingType === 'change_percent'"
            v-model="order"
            :options="orderOptions"
            style="width: 100px"
            @change="handleSearch"
          />

          <t-button theme="primary" @click="handleSearch">查询</t-button>
          <t-button @click="handleRefresh">刷新</t-button>
          <t-button @click="handleExport">导出</t-button>
        </t-space>
      </div>

      <!-- 排行表格 -->
      <t-table
        :data="tableData"
        :columns="columns"
        :loading="loading"
        :pagination="pagination"
        row-key="id"
        stripe
        hover
        @page-change="handlePageChange"
      >
        <template #rank="{ row }">
          <t-tag
            v-if="row.rank === 1"
            theme="danger"
            variant="light"
            style="width: 60px; text-align: center"
          >
            🔥 {{ row.rank }}
          </t-tag>
          <t-tag
            v-else-if="row.rank === 2"
            theme="warning"
            variant="light"
            style="width: 60px; text-align: center"
          >
            🥈 {{ row.rank }}
          </t-tag>
          <t-tag
            v-else-if="row.rank === 3"
            theme="success"
            variant="light"
            style="width: 60px; text-align: center"
          >
            🥉 {{ row.rank }}
          </t-tag>
          <span v-else style="width: 60px; text-align: center; display: inline-block">{{
            row.rank
          }}</span>
        </template>

        <template #stockName="{ row }">
          <div style="display: flex; align-items: center; gap: 8px">
            <span>{{ row.stock_name }}</span>
            <t-tag v-if="row.industry" size="small" variant="light">{{ row.industry }}</t-tag>
          </div>
        </template>

        <template #currentPrice="{ row }">
          <span v-if="row.current_price">{{ row.current_price.toFixed(2) }}</span>
          <span v-else>-</span>
        </template>

        <template #changePercent="{ row }">
          <span
            v-if="row.change_percent !== null"
            :style="{
              color: row.change_percent > 0 ? '#e34d59' : row.change_percent < 0 ? '#00a870' : ''
            }"
          >
            {{ row.change_percent > 0 ? '+' : '' }}{{ row.change_percent?.toFixed(2) }}%
          </span>
          <span v-else>-</span>
        </template>

        <template #turnoverRate="{ row }">
          <span v-if="row.turnover_rate !== null">{{ row.turnover_rate.toFixed(2) }}%</span>
          <span v-else>-</span>
        </template>

        <template #amount="{ row }">
          <span v-if="row.amount !== null">{{ formatAmount(row.amount) }}</span>
          <span v-else>-</span>
        </template>

        <template #volumeRatio="{ row }">
          <span v-if="row.volume_ratio !== null">{{ row.volume_ratio.toFixed(2) }}</span>
          <span v-else>-</span>
        </template>

        <template #marketCap="{ row }">
          <span v-if="row.total_market_cap !== null">{{ formatAmount(row.total_market_cap) }}</span>
          <span v-else>-</span>
        </template>

        <template #amplitude="{ row }">
          <span v-if="row.amplitude !== null">{{ row.amplitude.toFixed(2) }}%</span>
          <span v-else>-</span>
        </template>
      </t-table>
    </t-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { MessagePlugin } from 'tdesign-vue-next'
import {
  getStockRankingApi,
  getRankingIndustriesApi,
  getRankingMarketsApi,
  syncRankingDataApi
} from '@/api/stock/base'

// 排行类型
const rankingTypes = [
  { label: '换手率', value: 'turnover' },
  { label: '资金量', value: 'amount' },
  { label: '量比', value: 'volume_ratio' },
  { label: '涨跌幅', value: 'change_percent' },
  { label: '市值', value: 'market_cap' },
  { label: '振幅', value: 'amplitude' }
]

const rankingType = ref('turnover')
const order = ref('desc')

const orderOptions = [
  { label: '降序', value: 'desc' },
  { label: '升序', value: 'asc' }
]

// 筛选条件
const searchKeyword = ref('')
const industry = ref('')
const market = ref('')

const industryOptions = ref<Array<{ label: string; value: string }>>([])
const marketOptions = ref<Array<{ label: string; value: string }>>([])

// 表格数据
const loading = ref(false)
const tableData = ref<any[]>([])
const pagination = reactive({
  current: 1,
  pageSize: 20,
  total: 0,
  showJumper: true,
  showSizeChanger: true,
  pageSizeOptions: [10, 20, 50, 100]
})

// 表格列
const columns = computed(() => [
  { colKey: 'rank', title: '排名', width: 80, align: 'center' },
  { colKey: 'stock_code', title: '代码', width: 100, align: 'center' },
  { colKey: 'stock_name', title: '名称', width: 200, cell: 'stockName' },
  {
    colKey: 'current_price',
    title: '最新价',
    width: 100,
    align: 'right',
    cell: 'currentPrice'
  },
  {
    colKey: 'change_percent',
    title: '涨跌幅',
    width: 100,
    align: 'right',
    cell: 'changePercent'
  },
  {
    colKey: 'turnover_rate',
    title: '换手率',
    width: 100,
    align: 'right',
    cell: 'turnoverRate'
  },
  {
    colKey: 'amount',
    title: '成交额',
    width: 120,
    align: 'right',
    cell: 'amount'
  },
  {
    colKey: 'volume_ratio',
    title: '量比',
    width: 100,
    align: 'right',
    cell: 'volumeRatio'
  },
  {
    colKey: 'total_market_cap',
    title: '总市值',
    width: 120,
    align: 'right',
    cell: 'marketCap'
  },
  {
    colKey: 'amplitude',
    title: '振幅',
    width: 100,
    align: 'right',
    cell: 'amplitude'
  }
])

// 获取排行数据
const fetchRankingData = async () => {
  loading.value = true
  try {
    const params: any = {
      ranking_type: rankingType.value,
      order: order.value,
      page: pagination.current,
      page_size: pagination.pageSize
    }

    if (searchKeyword.value) {
      params.stock_name = searchKeyword.value
    }

    if (industry.value) {
      params.industry = industry.value
    }

    if (market.value) {
      params.market = market.value
    }

    const res = await getStockRankingApi(params)
    if (res.code === 200 && res.data) {
      tableData.value = res.data.items || []
      pagination.total = res.data.total || 0
    }
  } catch (error) {
    MessagePlugin.error('获取排行数据失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

// 获取行业列表
const fetchIndustries = async () => {
  try {
    const res = await getRankingIndustriesApi()
    if (res.code === 200 && res.data) {
      industryOptions.value = (res.data as string[]).map((item) => ({
        label: item,
        value: item
      }))
    }
  } catch (error) {
    console.error('获取行业列表失败', error)
  }
}

// 获取市场列表
const fetchMarkets = async () => {
  try {
    const res = await getRankingMarketsApi()
    if (res.code === 200 && res.data) {
      marketOptions.value = (res.data as string[]).map((item) => ({
        label: item,
        value: item
      }))
    }
  } catch (error) {
    console.error('获取市场列表失败', error)
  }
}

// 处理排行类型变化
const handleRankingTypeChange = () => {
  pagination.current = 1
  fetchRankingData()
}

// 搜索
const handleSearch = () => {
  pagination.current = 1
  fetchRankingData()
}

// 刷新
const handleRefresh = async () => {
  try {
    const res = await syncRankingDataApi()
    if (res.code === 200) {
      MessagePlugin.success('同步成功')
      fetchRankingData()
    }
  } catch (error) {
    MessagePlugin.error('同步失败')
  }
}

// 导出
const handleExport = () => {
  MessagePlugin.info('导出功能开发中')
}

// 分页变化
const handlePageChange = (pageInfo: any) => {
  pagination.current = pageInfo.current
  pagination.pageSize = pageInfo.pageSize
  fetchRankingData()
}

// 格式化金额
const formatAmount = (amount: number) => {
  if (amount === null || amount === undefined) return '-'
  if (amount >= 100000000) {
    return (amount / 100000000).toFixed(2) + '亿'
  } else if (amount >= 10000) {
    return (amount / 10000).toFixed(2) + '万'
  }
  return amount.toFixed(2)
}

// 初始化
onMounted(() => {
  fetchRankingData()
  fetchIndustries()
  fetchMarkets()
})
</script>

<style scoped lang="less">
.stock-ranking {
  padding: 20px;

  .filter-bar {
    margin-top: 20px;
    margin-bottom: 20px;
  }
}
</style>
