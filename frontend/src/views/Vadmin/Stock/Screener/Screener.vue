<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import {
  ElMessage,
  ElCard,
  ElButton,
  ElTable,
  ElTableColumn,
  ElTag,
  ElPagination,
  ElDialog
} from 'element-plus'
import { Refresh, Download, Plus, Delete } from '@element-plus/icons-vue'
import { ContentWrap } from '@/components/ContentWrap'
import QuickScreen from './components/QuickScreen.vue'
import ConditionBuilder from './components/ConditionBuilder.vue'
import {
  screenByCondition,
  screenLimitUp,
  screenLimitDown,
  screenHighTurnover,
  screenLowPE,
  screenVolumeSurge,
  screenSmallCap,
  type Condition,
  type ScreenerResult
} from '@/api/stock/screener'

defineOptions({
  name: 'StockScreener'
})

// 条件列表
const conditions = ref<Condition[]>([])

// 结果数据
const results = ref<ScreenerResult[]>([])
const loading = ref(false)
const totalCount = computed(() => results.value.length)

// 分页
const pagination = reactive({
  page: 1,
  pageSize: 20
})

// 添加条件
const handleAddCondition = () => {
  conditions.value.push({
    field: 'price',
    operator: 'gt',
    value: 0
  })
}

// 删除条件
const handleRemoveCondition = (index: number) => {
  conditions.value.splice(index, 1)
}

// 更新条件
const handleUpdateCondition = (index: number, condition: Condition) => {
  conditions.value[index] = condition
}

// 重置条件
const handleReset = () => {
  conditions.value = []
  results.value = []
}

// 执行选股
const handleScreen = async () => {
  if (conditions.value.length === 0) {
    ElMessage.warning('请至少添加一个筛选条件')
    return
  }

  loading.value = true
  try {
    const res = await screenByCondition(conditions.value, 200)
    results.value = res.data?.data || []
    ElMessage.success(`筛选完成，共找到 ${results.value.length} 只股票`)
  } catch (error) {
    ElMessage.error('选股失败')
  } finally {
    loading.value = false
  }
}

// 快捷选股
const handleQuickScreen = async (type: string) => {
  loading.value = true
  conditions.value = []
  try {
    let res: any
    switch (type) {
      case 'limit_up':
        res = await screenLimitUp(200)
        break
      case 'limit_down':
        res = await screenLimitDown(200)
        break
      case 'high_turnover':
        res = await screenHighTurnover(200)
        break
      case 'low_pe':
        res = await screenLowPE(200)
        break
      case 'volume_surge':
        res = await screenVolumeSurge(200)
        break
      case 'small_cap':
        res = await screenSmallCap(200)
        break
    }
    results.value = res.data?.data || []
    ElMessage.success(`筛选完成，共找到 ${results.value.length} 只股票`)
  } catch (error) {
    ElMessage.error('选股失败')
  } finally {
    loading.value = false
  }
}

// 导出数据
const handleExport = () => {
  if (results.value.length === 0) {
    ElMessage.warning('暂无数据可导出')
    return
  }

  const headers = ['股票代码', '股票名称', '价格', '涨跌幅', '匹配得分', '匹配原因']
  const rows = results.value.map((item) => [
    item.stock_code,
    item.stock_name,
    item.price?.toFixed(2) || '-',
    item.change_percent?.toFixed(2) + '%' || '-',
    item.match_score.toFixed(0),
    item.match_reasons.join('; ')
  ])

  const csvContent = [headers.join(','), ...rows.map((r) => r.join(','))].join('\n')
  const blob = new Blob(['\ufeff' + csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.download = `选股结果_${new Date().toISOString().split('T')[0]}.csv`
  link.click()

  ElMessage.success('导出成功')
}

// 格式化涨跌幅
const formatChangePercent = (value: number | null) => {
  if (value === null || value === undefined) return '-'
  const prefix = value > 0 ? '+' : ''
  return `${prefix}${value.toFixed(2)}%`
}

// 获取涨跌幅样式
const getChangeClass = (value: number | null) => {
  if (value === null || value === undefined) return ''
  return value > 0 ? 'text-up' : value < 0 ? 'text-down' : ''
}

// 分页数据
const pagedResults = computed(() => {
  const start = (pagination.page - 1) * pagination.pageSize
  const end = start + pagination.pageSize
  return results.value.slice(start, end)
})
</script>

<template>
  <ContentWrap>
    <div class="screener-container">
      <!-- 快捷选股 -->
      <QuickScreen @select="handleQuickScreen" :loading="loading" />

      <!-- 条件选股 -->
      <ElCard class="condition-card" shadow="never">
        <template #header>
          <div class="card-header">
            <span class="title">条件筛选</span>
            <div class="actions">
              <ElButton type="primary" :icon="Plus" @click="handleAddCondition">添加条件</ElButton>
              <ElButton :icon="Refresh" @click="handleReset">重置</ElButton>
              <ElButton type="success" :loading="loading" @click="handleScreen">开始选股</ElButton>
            </div>
          </div>
        </template>

        <div v-if="conditions.length === 0" class="empty-conditions">
          <span>点击"添加条件"开始设置筛选条件</span>
        </div>

        <div v-else class="conditions-list">
          <div v-for="(condition, index) in conditions" :key="index" class="condition-item">
            <ConditionBuilder
              :model-value="condition"
              @update:model-value="(val) => handleUpdateCondition(index, val)"
            />
            <ElButton
              type="danger"
              :icon="Delete"
              circle
              size="small"
              @click="handleRemoveCondition(index)"
            />
          </div>
        </div>
      </ElCard>

      <!-- 结果展示 -->
      <ElCard class="result-card" shadow="never">
        <template #header>
          <div class="card-header">
            <span class="title">筛选结果 (共 {{ totalCount }} 只股票)</span>
            <ElButton type="primary" :icon="Download" @click="handleExport">导出CSV</ElButton>
          </div>
        </template>

        <ElTable :data="pagedResults" stripe v-loading="loading" max-height="500">
          <ElTableColumn prop="stock_code" label="股票代码" width="100" />
          <ElTableColumn prop="stock_name" label="股票名称" width="120" />
          <ElTableColumn prop="price" label="最新价" width="100" align="right">
            <template #default="{ row }">
              {{ row.price?.toFixed(2) || '-' }}
            </template>
          </ElTableColumn>
          <ElTableColumn prop="change_percent" label="涨跌幅" width="100" align="right">
            <template #default="{ row }">
              <span :class="getChangeClass(row.change_percent)">
                {{ formatChangePercent(row.change_percent) }}
              </span>
            </template>
          </ElTableColumn>
          <ElTableColumn prop="match_score" label="匹配得分" width="100" align="center">
            <template #default="{ row }">
              <ElTag
                :type="
                  row.match_score >= 80 ? 'success' : row.match_score >= 60 ? 'warning' : 'info'
                "
              >
                {{ row.match_score.toFixed(0) }}
              </ElTag>
            </template>
          </ElTableColumn>
          <ElTableColumn prop="match_reasons" label="匹配原因">
            <template #default="{ row }">
              {{ row.match_reasons?.join('; ') || '-' }}
            </template>
          </ElTableColumn>
        </ElTable>

        <div class="pagination-wrapper">
          <ElPagination
            v-model:current-page="pagination.page"
            v-model:page-size="pagination.pageSize"
            :page-sizes="[20, 50, 100, 200]"
            :total="totalCount"
            layout="total, sizes, prev, pager, next"
          />
        </div>
      </ElCard>
    </div>
  </ContentWrap>
</template>

<style lang="scss" scoped>
.screener-container {
  .condition-card {
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

  .empty-conditions {
    text-align: center;
    color: #909399;
    padding: 20px 0;
  }

  .conditions-list {
    display: flex;
    flex-direction: column;
    gap: 12px;

    .condition-item {
      display: flex;
      align-items: center;
      gap: 12px;
    }
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
</style>
