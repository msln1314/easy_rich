<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox, ElDialog } from 'element-plus'
import { ContentWrap } from '@/components/ContentWrap'
import { Refresh, Plus, Delete } from '@element-plus/icons-vue'
import {
  getMonitorStrategyListApi,
  delMonitorStrategyApi,
  updateMonitorStrategyActiveApi
} from '@/api/stock/monitor_strategy'
import StrategyForm from './components/StrategyForm.vue'
import StrategyLog from './components/StrategyLog.vue'

defineOptions({
  name: 'MonitorStrategy'
})

// 数据
const strategies = ref<any[]>([])
const loading = ref(false)
const formDialogVisible = ref(false)
const logDialogVisible = ref(false)
const currentStrategy = ref<any>(null)
const currentStrategyId = ref<number | null>(null)

// 子组件ref
const strategyFormRef = ref()

// 策略类型映射
const strategyTypeMap: Record<string, string> = {
  limit_up: '涨停监听',
  limit_down: '跌停监听',
  open_board: '开板监听',
  turnover: '换手监听',
  breakout: '突破监听',
  rebound: '反弹监听',
  limit_up_break: '涨停破板',
  price_rise: '涨幅监听',
  price_fall: '跌至价位',
  pattern: '形态监控'
}

// 推送方式映射
const notifyMethodMap: Record<string, string> = {
  system: '系统消息',
  email: '邮件',
  sms: '短信',
  wechat: '微信'
}

// 冷却类型映射
const cooldownTypeMap: Record<string, string> = {
  same_day: '同一天只触发一次',
  interval: '按间隔时间'
}

// 推送类型映射
const notifyTypeMap: Record<string, string> = {
  once: '仅一次',
  always: '每次都推送',
  interval: '按间隔推送'
}

// 优先级映射
const priorityMap = { 1: '高', 2: '中', 3: '低' }

// 计算属性
const totalCount = computed(() => strategies.value.length)
const activeCount = computed(() => strategies.value.filter((s) => s.is_active === 1).length)

// 加载策略列表
const loadStrategies = async () => {
  loading.value = true
  try {
    const res = await getMonitorStrategyListApi({})
    strategies.value = res.data || []
  } catch (error) {
    ElMessage.error('加载策略列表失败')
  } finally {
    loading.value = false
  }
}

// 打开新增对话框
const handleAdd = () => {
  currentStrategy.value = null
  formDialogVisible.value = true
}

// 打开编辑对话框
const handleEdit = (strategy: any) => {
  currentStrategy.value = { ...strategy }
  formDialogVisible.value = true
}

// 复制策略
const handleCopy = (strategy: any) => {
  const copyData = {
    ...strategy,
    id: undefined,
    name: strategy.name + ' (副本)',
    trigger_count: 0,
    last_trigger_count: 0,
    last_trigger_time: null
  }
  currentStrategy.value = copyData
  formDialogVisible.value = true
}

// 删除策略
const handleDelete = async (strategy: any) => {
  await ElMessageBox.confirm(`确定要删除策略"${strategy.name}"吗？`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })

  try {
    await delMonitorStrategyApi({ ids: [strategy.id] })
    ElMessage.success('删除成功')
    loadStrategies()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 切换启用状态
const handleToggleActive = async (strategy: any) => {
  const newStatus = strategy.is_active === 1 ? 0 : 1
  try {
    await updateMonitorStrategyActiveApi(strategy.id, newStatus)
    ElMessage.success(newStatus === 1 ? '已启用' : '已禁用')
    loadStrategies()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

// 查看日志
const handleViewLog = (strategy: any) => {
  currentStrategyId.value = strategy.id
  logDialogVisible.value = true
}

// 表单提交成功回调
const handleFormSuccess = () => {
  formDialogVisible.value = false
  loadStrategies()
}

// 获取策略类型标签类型
const getStrategyTypeTagType = (type: string) => {
  const map: Record<string, any> = {
    limit_up: 'danger',
    limit_down: 'primary',
    open_board: 'warning',
    turnover: 'success',
    breakout: 'info',
    rebound: 'default'
  }
  return map[type] || 'default'
}

// 获取优先级标签类型
const getPriorityTagType = (priority: number) => {
  const map: Record<number, any> = { 1: 'danger', 2: 'warning', 3: 'info' }
  return map[priority] || 'info'
}

// 格式化时间
const formatTime = (time: string | null) => {
  if (!time) return '-'
  return new Date(time).toLocaleString('zh-CN')
}

onMounted(() => {
  loadStrategies()
})
</script>

<template>
  <ContentWrap>
    <div class="monitor-strategy-container">
      <!-- 头部 -->
      <div class="header-section">
        <div class="header-title">
          <h2>监听策略配置</h2>
          <div class="statistics">
            <el-tag size="large" type="info">总计: {{ totalCount }}</el-tag>
            <el-tag size="large" type="success">启用: {{ activeCount }}</el-tag>
            <el-tag size="large" type="warning">禁用: {{ totalCount - activeCount }}</el-tag>
          </div>
        </div>
        <el-button type="primary" :icon="Plus" @click="handleAdd">新建策略</el-button>
      </div>

      <!-- 策略卡片列表 -->
      <div v-if="loading" class="loading-container">加载中...</div>
      <div v-else-if="strategies.length === 0" class="empty-container">
        <p>暂无策略</p>
        <el-button type="primary" :icon="Plus" @click="handleAdd">新建策略</el-button>
      </div>
      <div v-else class="strategy-cards">
        <div v-for="strategy in strategies" :key="strategy.id" class="strategy-card">
          <!-- 卡片头部 -->
          <div class="card-header">
            <div class="card-title">
              <el-tag :type="getStrategyTypeTagType(strategy.strategy_type)" size="large">
                {{ strategyTypeMap[strategy.strategy_type] }}
              </el-tag>
              <span class="strategy-name">{{ strategy.name }}</span>
              <el-switch
                v-model="strategy.is_active"
                :active-value="1"
                :inactive-value="0"
                @change="handleToggleActive(strategy)"
              />
            </div>
            <div class="card-actions">
              <el-button link type="primary" @click="handleEdit(strategy)">编辑</el-button>
              <el-button link type="primary" @click="handleCopy(strategy)">复制</el-button>
              <el-button link type="primary" @click="handleViewLog(strategy)">日志</el-button>
              <el-button link type="danger" @click="handleDelete(strategy)">删除</el-button>
            </div>
          </div>

          <!-- 卡片内容 -->
          <div class="card-body">
            <div class="info-row">
              <div class="info-item">
                <span class="info-label">股票:</span>
                <span class="info-value">{{ strategy.stock_code }} {{ strategy.stock_name }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">优先级:</span>
                <el-tag :type="getPriorityTagType(strategy.priority)" size="small">
                  {{ priorityMap[strategy.priority] }}
                </el-tag>
              </div>
            </div>

            <div v-if="strategy.condition_content" class="info-row">
              <div class="info-item full-width">
                <span class="info-label">触发条件:</span>
                <span class="info-value">{{ strategy.condition_content }}</span>
              </div>
            </div>

            <div class="info-row">
              <div class="info-item">
                <span class="info-label">冷却时间:</span>
                <span class="info-value">{{ strategy.cooldown_minutes }}分钟</span>
              </div>
              <div class="info-item">
                <span class="info-label">冷却类型:</span>
                <span class="info-value">{{ cooldownTypeMap[strategy.cooldown_type] }}</span>
              </div>
            </div>

            <div class="info-row">
              <div class="info-item">
                <span class="info-label">推送:</span>
                <el-tag v-if="strategy.notify_enabled === 1" type="success" size="small">
                  {{ notifyMethodMap[strategy.notify_method] }}
                </el-tag>
                <el-tag v-else type="info" size="small">禁用</el-tag>
              </div>
              <div class="info-item">
                <span class="info-label">推送条件:</span>
                <span class="info-value">{{ strategy.notify_trigger_count }}次</span>
              </div>
            </div>

            <div class="info-row">
              <div class="info-item">
                <span class="info-label">累计触发:</span>
                <span class="info-value highlight">{{ strategy.trigger_count }}次</span>
              </div>
              <div class="info-item">
                <span class="info-label">最后触发:</span>
                <span class="info-value">{{ formatTime(strategy.last_trigger_time) }}</span>
              </div>
            </div>

            <div v-if="strategy.remark" class="info-row">
              <div class="info-item full-width">
                <span class="info-label">备注:</span>
                <span class="info-value remark">{{ strategy.remark }}</span>
              </div>
            </div>
          </div>

          <!-- 卡片底部 -->
          <div class="card-footer">
            <div class="footer-info">
              <span class="created-time">创建于: {{ formatTime(strategy.create_time) }}</span>
              <span v-if="strategy.tag" class="tag">标签: {{ strategy.tag }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 表单对话框 -->
      <el-dialog
        v-model="formDialogVisible"
        :title="currentStrategy?.id ? '编辑策略' : '新建策略'"
        width="800px"
        destroy-on-close
      >
        <StrategyForm
          ref="strategyFormRef"
          :strategy="currentStrategy"
          @success="handleFormSuccess"
        />
      </el-dialog>

      <!-- 日志对话框 -->
      <el-dialog v-model="logDialogVisible" title="策略触发日志" width="1200px" destroy-on-close>
        <StrategyLog :strategy-id="currentStrategyId" />
      </el-dialog>
    </div>
  </ContentWrap>
</template>

<style lang="scss" scoped>
.monitor-strategy-container {
  .header-section {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;

    .header-title {
      display: flex;
      align-items: center;
      gap: 16px;

      h2 {
        margin: 0;
        font-size: 20px;
        font-weight: 600;
      }

      .statistics {
        display: flex;
        gap: 8px;
      }
    }
  }

  .loading-container,
  .empty-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 300px;
    color: #909399;
  }

  .strategy-cards {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
    gap: 20px;
  }

  .strategy-card {
    border: 1px solid #e4e7ed;
    border-radius: 8px;
    background: #fff;
    transition: all 0.3s;
    overflow: hidden;

    &:hover {
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
      border-color: #409eff;
    }

    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 16px;
      border-bottom: 1px solid #e4e7ed;
      background: #f5f7fa;

      .card-title {
        display: flex;
        align-items: center;
        gap: 8px;
        flex: 1;

        .strategy-name {
          font-size: 16px;
          font-weight: 600;
          color: #303133;
        }
      }

      .card-actions {
        display: flex;
        gap: 8px;
      }
    }

    .card-body {
      padding: 16px;

      .info-row {
        display: flex;
        gap: 24px;
        margin-bottom: 12px;

        &:last-child {
          margin-bottom: 0;
        }

        .info-item {
          display: flex;
          align-items: center;
          gap: 8px;
          flex: 1;

          &.full-width {
            flex: 1;
          }

          .info-label {
            color: #909399;
            font-size: 14px;
            min-width: 70px;
          }

          .info-value {
            color: #303133;
            font-size: 14px;

            &.highlight {
              color: #409eff;
              font-weight: 600;
            }

            &.remark {
              color: #606266;
            }
          }
        }
      }
    }

    .card-footer {
      padding: 12px 16px;
      border-top: 1px solid #e4e7ed;
      background: #f5f7fa;

      .footer-info {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 12px;
        color: #909399;

        .tag {
          background: #ecf5ff;
          color: #409eff;
          padding: 2px 8px;
          border-radius: 4px;
        }
      }
    }
  }
}
</style>
