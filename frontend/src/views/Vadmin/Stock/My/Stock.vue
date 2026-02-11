<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox, ElTag, ElDialog } from 'element-plus'
import { ContentWrap } from '@/components/ContentWrap'
import { Search } from '@element-plus/icons-vue'
import {
  getMyStocksApi,
  removeStockFromGroupApi,
  getStockCountByGroupApi
} from '@/api/stock/my_stock'
import { getStockGroupTreeApi, deleteStockGroupApi } from '@/api/stock/group'
import AddStockDialog from './components/AddStockDialog.vue'
import CreateGroupDialog from './components/CreateGroupDialog.vue'

defineOptions({
  name: 'MyStock'
})

// 数据
const stocks = ref<any[]>([])
const groups = ref<any[]>([])
const groupCounts = ref<any[]>([])
const currentGroupId = ref<number | null>(null)
const loading = ref(false)
const groupLoading = ref(false)
const stockDialogVisible = ref(false)
const groupDialogVisible = ref(false)

// 子组件ref
const addStockRef = ref()
const createGroupRef = ref()

// 计算属性
const currentGroupName = computed(() => {
  if (currentGroupId.value === null) return '全部自选股'
  const group = findGroupById(groups.value, currentGroupId.value)
  return group ? group.name : '未知分组'
})

const totalCount = computed(() => {
  return stocks.value.length
})

// 递归查找分组
const findGroupById = (groups: any[], id: number): any => {
  for (const group of groups) {
    if (group.id === id) return group
    if (group.children && group.children.length > 0) {
      const found = findGroupById(group.children, id)
      if (found) return found
    }
  }
  return null
}

// 加载分组列表
const loadGroups = async () => {
  groupLoading.value = true
  try {
    const res = await getStockGroupTreeApi({})
    groups.value = res.data || []
    await loadGroupCounts()
  } catch (error) {
    ElMessage.error('加载分组失败')
  } finally {
    groupLoading.value = false
  }
}

// 加载各分组股票数量
const loadGroupCounts = async () => {
  try {
    const res = await getStockCountByGroupApi({})
    groupCounts.value = res.data || []
  } catch (error) {
    console.error('加载分组统计失败', error)
  }
}

// 获取分组的股票数量
const getGroupStockCount = (groupId: number) => {
  const item = groupCounts.value.find((item: any) => item.group_id === groupId)
  return item ? item.stock_count : 0
}

// 加载自选股列表
const loadStocks = async () => {
  loading.value = true
  try {
    const params: any = {}
    if (currentGroupId.value !== null) {
      params.group_id = currentGroupId.value
    }
    const res = await getMyStocksApi(params)
    stocks.value = res.data || []
  } catch (error) {
    ElMessage.error('加载自选股失败')
  } finally {
    loading.value = false
  }
}

// 选择分组
const selectGroup = (groupId: number | null) => {
  currentGroupId.value = groupId
  loadStocks()
}

// 移除股票
const handleRemoveStock = async (stockId: number) => {
  await ElMessageBox.confirm('确定要移除这只股票吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })

  try {
    await removeStockFromGroupApi({
      stock_id: stockId,
      group_id: currentGroupId.value
    })
    ElMessage.success('移除成功')
    loadStocks()
    loadGroupCounts()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('移除失败')
    }
  }
}

// 删除分组
const handleDeleteGroup = async (group: any) => {
  const count = getGroupStockCount(group.id)
  await ElMessageBox.confirm(
    `确定要删除分组"${group.name}"吗？该分组下的 ${count} 只股票也将被移除。`,
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  )

  try {
    await deleteStockGroupApi([group.id])
    ElMessage.success('删除成功')
    if (currentGroupId.value === group.id) {
      currentGroupId.value = null
    }
    loadGroups()
    loadStocks()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 打开添加股票对话框
const openStockDialog = () => {
  if (!currentGroupId.value) {
    ElMessage.warning('请先选择分组')
    return
  }
  stockDialogVisible.value = true
}

// 添加股票成功回调
const handleAddStockSuccess = () => {
  loadStocks()
  loadGroupCounts()
}

// 获取涨跌颜色
const getChangeColor = (change: number | null) => {
  if (change === null || change === undefined) return '#6b7280'
  return change > 0 ? '#ef4444' : change < 0 ? '#3b82f6' : '#6b7280'
}

// 格式化涨跌幅
const formatChangePercent = (change: number | null) => {
  if (change === null || change === undefined) return '-'
  const prefix = change > 0 ? '+' : ''
  return prefix + change.toFixed(2) + '%'
}

// 格式化市值
const formatMarketCap = (cap: number | null) => {
  if (cap === null || cap === undefined) return '-'
  if (cap >= 100000000) return (cap / 100000000).toFixed(2) + '亿'
  if (cap >= 10000) return (cap / 10000).toFixed(2) + '万'
  return cap.toFixed(2)
}

onMounted(() => {
  loadGroups()
  loadStocks()
})
</script>

<template>
  <ContentWrap>
    <div class="my-stock-container">
      <!-- 左侧分组列表 -->
      <div class="group-panel">
        <div class="panel-header">
          <h3 class="panel-title">我的分组</h3>
          <el-button type="primary" size="small" @click="groupDialogVisible = true">
            新建分组
          </el-button>
        </div>
        <div class="panel-body">
          <div
            class="group-item all"
            :class="{ active: currentGroupId === null }"
            @click="selectGroup(null)"
          >
            <div class="group-content">
              <div class="group-info">
                <span class="group-name">全部自选股</span>
                <el-tag size="small" type="primary" round>
                  {{ totalCount }}
                </el-tag>
              </div>
            </div>
          </div>
          <!-- 分组树递归渲染 -->
          <template v-for="group in groups" :key="group.id">
            <div class="group-item">
              <div
                class="group-content"
                :class="{ active: currentGroupId === group.id }"
                @click="selectGroup(group.id)"
              >
                <div class="group-info">
                  <span class="group-name">{{ group.name }}</span>
                  <el-tag size="small" type="info" round>
                    {{ getGroupStockCount(group.id) }}
                  </el-tag>
                </div>
                <el-tag v-if="group.status === 0" size="small" type="warning">禁用</el-tag>
                <div class="group-actions">
                  <span class="action-btn delete-btn" @click.stop="handleDeleteGroup(group)">
                    删除
                  </span>
                </div>
              </div>
              <div v-if="group.children && group.children.length > 0" class="group-children">
                <template v-for="child in group.children" :key="child.id">
                  <div class="group-item">
                    <div
                      class="group-content"
                      :class="{ active: currentGroupId === child.id }"
                      @click="selectGroup(child.id)"
                    >
                      <div class="group-info">
                        <span class="group-name">{{ child.name }}</span>
                        <el-tag size="small" type="info" round>
                          {{ getGroupStockCount(child.id) }}
                        </el-tag>
                      </div>
                      <el-tag v-if="child.status === 0" size="small" type="warning">禁用</el-tag>
                      <div class="group-actions">
                        <span class="action-btn delete-btn" @click.stop="handleDeleteGroup(child)">
                          删除
                        </span>
                      </div>
                    </div>
                  </div>
                </template>
              </div>
            </div>
          </template>
        </div>
      </div>

      <!-- 右侧股票列表 -->
      <div class="stock-panel">
        <div class="panel-header">
          <h3 class="panel-title"> {{ currentGroupName }} ({{ stocks.length }}) </h3>
          <el-button type="primary" size="small" @click="openStockDialog">
            <el-icon style="margin-right: 4px"><Search /></el-icon>
            添加股票
          </el-button>
        </div>
        <div class="panel-body">
          <div v-if="loading" class="loading-container">加载中...</div>
          <div v-else-if="stocks.length === 0" class="empty-container">
            <p>暂无股票</p>
            <el-button type="primary" size="small" @click="openStockDialog"> 添加股票 </el-button>
          </div>
          <div v-else class="stock-list">
            <div v-for="stock in stocks" :key="stock.id" class="stock-item">
              <div class="stock-main">
                <div class="stock-info">
                  <span class="stock-name">{{ stock.stock_name || '-' }}</span>
                  <span class="stock-code">{{ stock.stock_code }}</span>
                  <el-tag
                    v-if="stock.group_name"
                    size="small"
                    type="success"
                    style="margin-left: 8px"
                  >
                    {{ stock.group_name }}
                  </el-tag>
                </div>
                <div class="stock-price">
                  <span class="current-price">
                    {{ stock.current_price ? stock.current_price.toFixed(2) : '-' }}
                  </span>
                  <span
                    class="change-percent"
                    :style="{ color: getChangeColor(stock.change_percent) }"
                  >
                    {{ formatChangePercent(stock.change_percent) }}
                  </span>
                </div>
              </div>
              <div class="stock-details">
                <div class="detail-item">
                  <span class="detail-label">当前价</span>
                  <span class="detail-value">
                    {{ stock.current_price ? stock.current_price.toFixed(2) : '-' }}
                  </span>
                </div>
                <div class="detail-item">
                  <span class="detail-label">涨跌幅</span>
                  <span
                    class="detail-value"
                    :style="{ color: getChangeColor(stock.change_percent) }"
                  >
                    {{ formatChangePercent(stock.change_percent) }}
                  </span>
                </div>
                <div class="detail-item">
                  <span class="detail-label">成交量</span>
                  <span class="detail-value">
                    {{ stock.volume ? (stock.volume / 10000).toFixed(2) + '万手' : '-' }}
                  </span>
                </div>
                <div class="detail-item">
                  <span class="detail-label">成交额</span>
                  <span class="detail-value">
                    {{ stock.amount ? formatMarketCap(stock.amount) : '-' }}
                  </span>
                </div>
                <div class="detail-item">
                  <span class="detail-label">市盈率</span>
                  <span class="detail-value">
                    {{ stock.pe_ratio ? stock.pe_ratio.toFixed(2) : '-' }}
                  </span>
                </div>
                <div class="detail-item">
                  <span class="detail-label">总市值</span>
                  <span class="detail-value">
                    {{ stock.total_market_cap ? formatMarketCap(stock.total_market_cap) : '-' }}
                  </span>
                </div>
              </div>
              <div v-if="stock.follow_remark" class="stock-remark">
                <span class="remark-label">备注：</span>
                <span class="remark-text">{{ stock.follow_remark }}</span>
              </div>
              <div class="stock-actions">
                <el-button
                  type="danger"
                  size="small"
                  text
                  @click="handleRemoveStock(stock.stock_id)"
                >
                  移除
                </el-button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </ContentWrap>

  <!-- 添加股票对话框 -->
  <ElDialog v-model="stockDialogVisible" title="添加股票" width="600px">
    <AddStockDialog
      ref="addStockRef"
      :group-id="currentGroupId"
      :visible="stockDialogVisible"
      @update:visible="stockDialogVisible = $event"
      @success="handleAddStockSuccess"
    />
  </ElDialog>

  <!-- 新建分组对话框 -->
  <ElDialog v-model="groupDialogVisible" title="新建分组" width="500px">
    <CreateGroupDialog
      ref="createGroupRef"
      :visible="groupDialogVisible"
      @update:visible="groupDialogVisible = $event"
      @success="loadGroups"
    />
    <template #footer>
      <el-button @click="groupDialogVisible = false">取消</el-button>
      <el-button type="primary" @click="createGroupRef?.submit()">确定</el-button>
    </template>
  </ElDialog>
</template>

<style scoped lang="scss">
.my-stock-container {
  display: flex;
  gap: 20px;
  height: calc(100vh - 200px);
  min-height: 600px;

  .group-panel,
  .stock-panel {
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    overflow: hidden;
  }

  .group-panel {
    width: 280px;
    flex-shrink: 0;
    display: flex;
    flex-direction: column;
  }

  .stock-panel {
    flex: 1;
    display: flex;
    flex-direction: column;
  }

  .panel-header {
    padding: 16px 20px;
    border-bottom: 1px solid #e5e7eb;
    display: flex;
    justify-content: space-between;
    align-items: center;

    .panel-title {
      margin: 0;
      font-size: 16px;
      font-weight: 600;
      color: #1f2937;
    }
  }

  .panel-body {
    flex: 1;
    overflow-y: auto;
    padding: 12px;
  }

  .group-item {
    &.all .group-content.active {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
    }

    .group-content {
      padding: 12px 16px;
      border-radius: 8px;
      margin-bottom: 8px;
      cursor: pointer;
      transition: all 0.3s;
      border: 1px solid #e5e7eb;

      &:hover {
        border-color: #667eea;
        background: #f0f9ff;
      }

      &.active {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-color: #667eea;

        .group-name {
          color: white;
        }
      }

      .group-info {
        display: flex;
        justify-content: space-between;
        align-items: center;
      }

      .group-name {
        font-size: 14px;
        font-weight: 600;
        color: #1f2937;
      }
    }

    .group-children {
      margin-left: 20px;
      margin-top: 8px;
    }
  }

  .group-actions {
    margin-top: 8px;
    display: flex;
    gap: 8px;
    justify-content: flex-end;

    .action-btn {
      font-size: 12px;
      cursor: pointer;
      padding: 4px 8px;
      border-radius: 4px;
      transition: all 0.3s;

      &:hover {
        background: rgba(255, 255, 255, 0.2);
      }

      &.delete-btn {
        color: #ef4444;
      }
    }
  }

  .loading-container,
  .empty-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 300px;
    color: #9ca3af;
  }

  .stock-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 16px;
  }

  .stock-item {
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 16px;
    transition: all 0.3s;
    background: white;

    &:hover {
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
      border-color: #667eea;
    }

    .stock-main {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 12px;
      padding-bottom: 12px;
      border-bottom: 1px solid #f3f4f6;
    }

    .stock-info {
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .stock-name {
      font-size: 16px;
      font-weight: 700;
      color: #1f2937;
    }

    .stock-code {
      font-size: 13px;
      color: #6b7280;
    }

    .stock-price {
      text-align: right;
    }

    .current-price {
      font-size: 20px;
      font-weight: 700;
      color: #1f2937;
      display: block;
    }

    .change-percent {
      font-size: 14px;
      font-weight: 600;
    }

    .stock-details {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 8px;
      margin-bottom: 12px;
    }

    .detail-item {
      display: flex;
      flex-direction: column;
      gap: 2px;
    }

    .detail-label {
      font-size: 12px;
      color: #9ca3af;
    }

    .detail-value {
      font-size: 13px;
      font-weight: 500;
      color: #1f2937;
    }

    .stock-remark {
      padding: 8px 12px;
      background: #f9fafb;
      border-radius: 6px;
      margin-bottom: 12px;
      font-size: 13px;
      line-height: 1.5;

      .remark-label {
        color: #6b7280;
        font-weight: 500;
      }

      .remark-text {
        color: #374151;
      }
    }

    .stock-actions {
      display: flex;
      justify-content: flex-end;
    }
  }
}
</style>
