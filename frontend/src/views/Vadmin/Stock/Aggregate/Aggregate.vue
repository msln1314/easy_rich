<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import {
  ElCard,
  ElInput,
  ElButton,
  ElTabs,
  ElTabPane,
  ElTag,
  ElRow,
  ElCol,
  ElDescriptions,
  ElDescriptionsItem,
  ElProgress,
  ElEmpty,
  ElMessage,
  ElSkeleton
} from 'element-plus'
import { Search, Refresh, Star, Bell } from '@element-plus/icons-vue'
import { ContentWrap } from '@/components/ContentWrap'
import OverviewTab from './components/OverviewTab.vue'
import TechnicalTab from './components/TechnicalTab.vue'
import FundTab from './components/FundTab.vue'
import InfoTab from './components/InfoTab.vue'
import FinancialTab from './components/FinancialTab.vue'
import { getStockFullData } from '@/api/stock/aggregate'

defineOptions({
  name: 'StockAggregate'
})

// 股票代码
const stockCode = ref('')

// 加载状态
const loading = ref(false)

// 数据
const aggregateData = ref<any>(null)

// 当前Tab
const activeTab = ref('overview')

// 搜索股票
const handleSearch = async () => {
  if (!stockCode.value.trim()) {
    ElMessage.warning('请输入股票代码')
    return
  }

  loading.value = true
  aggregateData.value = null

  try {
    const res = await getStockFullData(stockCode.value.trim())
    aggregateData.value = res.data || null

    if (aggregateData.value) {
      ElMessage.success('数据加载成功')
    }
  } catch (error) {
    ElMessage.error('获取数据失败')
  } finally {
    loading.value = false
  }
}

// 重置
const handleReset = () => {
  stockCode.value = ''
  aggregateData.value = null
}

// 格式化金额
const formatAmount = (value: number | null | undefined) => {
  if (!value && value !== 0) return '-'
  if (value >= 100000000) return (value / 100000000).toFixed(2) + '亿'
  if (value >= 10000) return (value / 10000).toFixed(2) + '万'
  return value.toFixed(2)
}

// 格式化涨跌幅
const formatChangePercent = (value: number | null | undefined) => {
  if (value === null || value === undefined) return '-'
  const prefix = value > 0 ? '+' : ''
  return `${prefix}${value.toFixed(2)}%`
}

// 获取涨跌幅样式
const getChangeClass = (value: number | null | undefined) => {
  if (value === null || value === undefined) return ''
  return value > 0 ? 'text-up' : value < 0 ? 'text-down' : ''
}

// 键盘回车搜索
const handleKeyup = (e: KeyboardEvent) => {
  if (e.key === 'Enter') {
    handleSearch()
  }
}

// 初始化时如果有路由参数则自动搜索
onMounted(() => {
  // 可以从路由参数获取股票代码
  const urlParams = new URLSearchParams(window.location.search)
  const code = urlParams.get('code')
  if (code) {
    stockCode.value = code
    handleSearch()
  }
})
</script>

<template>
  <ContentWrap>
    <div class="aggregate-container">
      <!-- 搜索区域 -->
      <ElCard class="search-card" shadow="never">
        <div class="search-section">
          <ElInput
            v-model="stockCode"
            placeholder="请输入股票代码，如：000001、600519"
            style="width: 300px"
            clearable
            @keyup="handleKeyup"
          >
            <template #prefix>
              <Search />
            </template>
          </ElInput>
          <ElButton type="primary" :loading="loading" @click="handleSearch">查询</ElButton>
          <ElButton :icon="Refresh" @click="handleReset">重置</ElButton>
        </div>
      </ElCard>

      <!-- 数据展示区域 -->
      <template v-if="aggregateData">
        <!-- 头部信息卡片 -->
        <ElCard class="header-card" shadow="never">
          <div class="stock-header">
            <div class="stock-info">
              <h2 class="stock-name">
                {{ aggregateData.basic_info?.name || '-' }}
                <ElTag v-if="aggregateData.quote" :type="aggregateData.quote.change_percent > 0 ? 'danger' : 'success'" size="large">
                  {{ aggregateData.quote.change_percent > 0 ? '涨' : '跌' }}
                </ElTag>
              </h2>
              <div class="stock-code">{{ stockCode }}</div>
            </div>

            <div class="price-info" v-if="aggregateData.quote">
              <div class="current-price" :class="getChangeClass(aggregateData.quote.change_percent)">
                {{ aggregateData.quote.price?.toFixed(2) || '-' }}
              </div>
              <div class="change-info">
                <span :class="getChangeClass(aggregateData.quote.change_percent)">
                  {{ formatChangePercent(aggregateData.quote.change_percent) }}
                </span>
                <span class="change-amount" :class="getChangeClass(aggregateData.quote.change)">
                  {{ aggregateData.quote.change > 0 ? '+' : '' }}{{ aggregateData.quote.change?.toFixed(2) || '-' }}
                </span>
              </div>
            </div>

            <div class="quick-info">
              <div class="info-item">
                <span class="label">今开</span>
                <span class="value">{{ aggregateData.quote?.open?.toFixed(2) || '-' }}</span>
              </div>
              <div class="info-item">
                <span class="label">最高</span>
                <span class="value text-up">{{ aggregateData.quote?.high?.toFixed(2) || '-' }}</span>
              </div>
              <div class="info-item">
                <span class="label">最低</span>
                <span class="value text-down">{{ aggregateData.quote?.low?.toFixed(2) || '-' }}</span>
              </div>
              <div class="info-item">
                <span class="label">成交量</span>
                <span class="value">{{ formatAmount(aggregateData.quote?.volume) }}</span>
              </div>
              <div class="info-item">
                <span class="label">成交额</span>
                <span class="value">{{ formatAmount(aggregateData.quote?.amount) }}</span>
              </div>
              <div class="info-item">
                <span class="label">换手率</span>
                <span class="value">{{ aggregateData.quote?.turnover_rate?.toFixed(2) || '-' }}%</span>
              </div>
            </div>

            <div class="action-buttons">
              <ElButton type="warning" :icon="Star" plain>加入自选</ElButton>
              <ElButton type="info" :icon="Bell" plain>设置提醒</ElButton>
            </div>
          </div>

          <!-- 摘要信息 -->
          <div class="summary-section" v-if="aggregateData.summary">
            <ElRow :gutter="16">
              <ElCol :span="4">
                <div class="summary-item">
                  <span class="summary-value">{{ aggregateData.summary.signal_count }}</span>
                  <span class="summary-label">技术信号</span>
                </div>
              </ElCol>
              <ElCol :span="4">
                <div class="summary-item">
                  <span class="summary-value">{{ aggregateData.summary.pattern_count }}</span>
                  <span class="summary-label">识别形态</span>
                </div>
              </ElCol>
              <ElCol :span="4">
                <div class="summary-item">
                  <span class="summary-value">{{ aggregateData.reports?.length || 0 }}</span>
                  <span class="summary-label">研报数量</span>
                </div>
              </ElCol>
              <ElCol :span="4">
                <div class="summary-item">
                  <span class="summary-value">{{ aggregateData.notices?.length || 0 }}</span>
                  <span class="summary-label">公告数量</span>
                </div>
              </ElCol>
              <ElCol :span="4">
                <div class="summary-item">
                  <span class="summary-value">{{ aggregateData.sectors?.sectors?.length || 0 }}</span>
                  <span class="summary-label">板块概念</span>
                </div>
              </ElCol>
              <ElCol :span="4">
                <div class="summary-item">
                  <span class="summary-value">{{ aggregateData.rating?.data?.length || 0 }}</span>
                  <span class="summary-label">机构评级</span>
                </div>
              </ElCol>
            </ElRow>
          </div>
        </ElCard>

        <!-- 详细信息Tab -->
        <ElCard class="content-card" shadow="never">
          <ElTabs v-model="activeTab" type="border-card">
            <ElTabPane label="概览" name="overview">
              <OverviewTab :data="aggregateData" />
            </ElTabPane>
            <ElTabPane label="技术分析" name="technical">
              <TechnicalTab :data="aggregateData" :stock-code="stockCode" />
            </ElTabPane>
            <ElTabPane label="资金面" name="fund">
              <FundTab :data="aggregateData" />
            </ElTabPane>
            <ElTabPane label="资讯公告" name="info">
              <InfoTab :data="aggregateData" />
            </ElTabPane>
            <ElTabPane label="财务数据" name="financial">
              <FinancialTab :data="aggregateData" />
            </ElTabPane>
          </ElTabs>
        </ElCard>
      </template>

      <!-- 空状态 -->
      <ElCard v-else-if="!loading" class="empty-card" shadow="never">
        <ElEmpty description="请输入股票代码进行查询" />
      </ElCard>

      <!-- 加载中 -->
      <ElCard v-if="loading" class="loading-card" shadow="never">
        <ElSkeleton :rows="10" animated />
      </ElCard>
    </div>
  </ContentWrap>
</template>

<style lang="scss" scoped>
.aggregate-container {
  .search-card {
    margin-bottom: 16px;

    .search-section {
      display: flex;
      gap: 12px;
      align-items: center;
    }
  }

  .header-card {
    margin-bottom: 16px;

    .stock-header {
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 20px;

      .stock-info {
        .stock-name {
          margin: 0 0 8px 0;
          font-size: 24px;
          font-weight: 600;
          display: flex;
          align-items: center;
          gap: 12px;
        }

        .stock-code {
          font-size: 14px;
          color: #909399;
        }
      }

      .price-info {
        text-align: center;

        .current-price {
          font-size: 36px;
          font-weight: 700;
        }

        .change-info {
          display: flex;
          gap: 16px;
          justify-content: center;
          margin-top: 8px;

          .change-amount {
            font-size: 14px;
          }
        }
      }

      .quick-info {
        display: flex;
        gap: 24px;
        flex-wrap: wrap;

        .info-item {
          display: flex;
          flex-direction: column;
          align-items: center;

          .label {
            font-size: 12px;
            color: #909399;
          }

          .value {
            font-size: 16px;
            font-weight: 600;
            margin-top: 4px;
          }
        }
      }

      .action-buttons {
        display: flex;
        gap: 12px;
      }
    }

    .summary-section {
      margin-top: 24px;
      padding-top: 16px;
      border-top: 1px solid #ebeef5;

      .summary-item {
        text-align: center;

        .summary-value {
          font-size: 24px;
          font-weight: 600;
          color: #409eff;
        }

        .summary-label {
          font-size: 12px;
          color: #909399;
          display: block;
          margin-top: 4px;
        }
      }
    }
  }

  .content-card {
    :deep(.el-tabs__content) {
      padding: 16px;
    }
  }

  .empty-card,
  .loading-card {
    min-height: 400px;
  }
}

.text-up {
  color: #f56c6c;
}

.text-down {
  color: #67c23a;
}
</style>