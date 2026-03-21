<template>
  <div class="portfolio-page">
    <div class="portfolio-header">
      <div class="header-left">
        <el-select
          v-model="selectedPortfolioId"
          placeholder="选择组合"
          style="width: 200px"
          @change="handlePortfolioChange"
        >
          <el-option v-for="p in portfolios" :key="p.id" :label="p.name" :value="p.id">
            <span>{{ p.name }}</span>
            <el-tag v-if="p.is_default" size="small" type="success" style="margin-left: 8px"
              >默认</el-tag
            >
          </el-option>
        </el-select>
        <el-button type="primary" @click="showCreateDialog = true">新建组合</el-button>
      </div>
      <div class="header-right">
        <el-button @click="loadPortfolioData" :icon="Refresh">刷新</el-button>
      </div>
    </div>

    <div class="portfolio-content" v-loading="loading">
      <el-tabs v-model="activeTab">
        <el-tab-pane label="持仓概览" name="positions">
          <div class="position-summary">
            <el-row :gutter="16">
              <el-col :span="6">
                <el-card shadow="hover">
                  <el-statistic title="总市值" :value="performance.total_value || 0" :precision="2">
                    <template #suffix>元</template>
                  </el-statistic>
                </el-card>
              </el-col>
              <el-col :span="6">
                <el-card shadow="hover">
                  <el-statistic title="总成本" :value="performance.total_cost || 0" :precision="2">
                    <template #suffix>元</template>
                  </el-statistic>
                </el-card>
              </el-col>
              <el-col :span="6">
                <el-card shadow="hover">
                  <el-statistic
                    title="总盈亏"
                    :value="performance.total_profit || 0"
                    :precision="2"
                  >
                    <template #suffix>元</template>
                  </el-statistic>
                </el-card>
              </el-col>
              <el-col :span="6">
                <el-card shadow="hover">
                  <el-statistic title="收益率" :value="performance.profit_rate || 0" :precision="2">
                    <template #suffix>%</template>
                  </el-statistic>
                </el-card>
              </el-col>
            </el-row>
          </div>

          <div class="position-actions" style="margin: 16px 0">
            <el-button type="primary" @click="showTradeDialog('buy')">买入</el-button>
            <el-button type="danger" @click="showTradeDialog('sell')">卖出</el-button>
          </div>

          <el-table :data="positions" border stripe>
            <el-table-column prop="stock_code" label="股票代码" width="120" />
            <el-table-column prop="stock_name" label="股票名称" width="120" />
            <el-table-column prop="shares" label="持仓股数" width="100" />
            <el-table-column prop="cost_price" label="成本价" width="100">
              <template #default="{ row }">{{ row.cost_price?.toFixed(2) }}</template>
            </el-table-column>
            <el-table-column prop="current_price" label="现价" width="100">
              <template #default="{ row }">{{ row.current_price?.toFixed(2) || '-' }}</template>
            </el-table-column>
            <el-table-column prop="market_value" label="市值" width="120">
              <template #default="{ row }">{{ row.market_value?.toFixed(2) || '-' }}</template>
            </el-table-column>
            <el-table-column prop="profit" label="盈亏" width="120">
              <template #default="{ row }">
                <span :style="{ color: row.profit >= 0 ? '#67C23A' : '#F56C6C' }">
                  {{ row.profit?.toFixed(2) || '-' }}
                </span>
              </template>
            </el-table-column>
            <el-table-column prop="profit_rate" label="收益率" width="100">
              <template #default="{ row }">
                <span :style="{ color: row.profit_rate >= 0 ? '#67C23A' : '#F56C6C' }">
                  {{ row.profit_rate?.toFixed(2) || '-' }}%
                </span>
              </template>
            </el-table-column>
            <el-table-column prop="position_ratio" label="仓位占比" width="100">
              <template #default="{ row }">{{ row.position_ratio?.toFixed(2) || '-' }}%</template>
            </el-table-column>
            <el-table-column label="操作" width="100" fixed="right">
              <template #default="{ row }">
                <el-button type="danger" size="small" link @click="handleDeletePosition(row)"
                  >删除</el-button
                >
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <el-tab-pane label="交易记录" name="trades">
          <el-table :data="trades" border stripe>
            <el-table-column prop="stock_code" label="股票代码" width="120" />
            <el-table-column prop="stock_name" label="股票名称" width="120" />
            <el-table-column prop="trade_type" label="类型" width="80">
              <template #default="{ row }">
                <el-tag
                  :type="
                    row.trade_type === 'buy'
                      ? 'success'
                      : row.trade_type === 'sell'
                      ? 'danger'
                      : 'info'
                  "
                >
                  {{
                    row.trade_type === 'buy' ? '买入' : row.trade_type === 'sell' ? '卖出' : '分红'
                  }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="trade_date" label="日期" width="120" />
            <el-table-column prop="shares" label="股数" width="100" />
            <el-table-column prop="price" label="价格" width="100">
              <template #default="{ row }">{{ row.price?.toFixed(2) }}</template>
            </el-table-column>
            <el-table-column prop="amount" label="金额" width="120">
              <template #default="{ row }">{{ row.amount?.toFixed(2) }}</template>
            </el-table-column>
            <el-table-column prop="commission" label="手续费" width="100">
              <template #default="{ row }">{{ row.commission?.toFixed(2) }}</template>
            </el-table-column>
            <el-table-column prop="remark" label="备注" />
          </el-table>
        </el-tab-pane>

        <el-tab-pane label="风控预警" name="risk">
          <div class="risk-actions" style="margin-bottom: 16px">
            <el-button type="warning" @click="handleRiskCheck">风控检查</el-button>
            <el-button @click="loadRiskAlerts">刷新预警</el-button>
          </div>
          <el-table :data="riskAlerts" border stripe>
            <el-table-column prop="alert_type" label="预警类型" width="120" />
            <el-table-column prop="alert_level" label="级别" width="80">
              <template #default="{ row }">
                <el-tag
                  :type="
                    row.alert_level === 'warning'
                      ? 'warning'
                      : row.alert_level === 'error'
                      ? 'danger'
                      : 'info'
                  "
                >
                  {{ row.alert_level }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="title" label="标题" width="200" />
            <el-table-column prop="content" label="内容" />
            <el-table-column prop="created_at" label="时间" width="180">
              <template #default="{ row }">{{
                row.created_at?.replace('T', ' ').slice(0, 19)
              }}</template>
            </el-table-column>
            <el-table-column label="操作" width="100">
              <template #default="{ row }">
                <el-button
                  v-if="!row.is_handled"
                  type="primary"
                  size="small"
                  link
                  @click="handleAlert(row)"
                  >处理</el-button
                >
                <span v-else style="color: #67c23a">已处理</span>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <el-tab-pane label="收益分析" name="analysis">
          <div class="analysis-section">
            <el-card header="收益归因">
              <el-table :data="attribution.top_winners" border stripe size="small">
                <el-table-column prop="stock_name" label="股票" width="120" />
                <el-table-column prop="profit" label="盈亏" width="100">
                  <template #default="{ row }">
                    <span :style="{ color: row.profit >= 0 ? '#67C23A' : '#F56C6C' }">
                      {{ row.profit?.toFixed(2) }}
                    </span>
                  </template>
                </el-table-column>
                <el-table-column prop="contribution" label="贡献度" width="100">
                  <template #default="{ row }">{{ row.contribution }}%</template>
                </el-table-column>
              </el-table>
            </el-card>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>

    <el-dialog v-model="showCreateDialog" title="新建组合" width="500px">
      <el-form :model="createForm" label-width="100px">
        <el-form-item label="组合名称" required>
          <el-input v-model="createForm.name" placeholder="请输入组合名称" />
        </el-form-item>
        <el-form-item label="组合描述">
          <el-input
            v-model="createForm.description"
            type="textarea"
            rows="3"
            placeholder="请输入组合描述"
          />
        </el-form-item>
        <el-form-item label="单股最大仓位">
          <el-input-number v-model="createForm.max_single_position" :min="5" :max="100" /> %
        </el-form-item>
        <el-form-item label="最大回撤预警">
          <el-input-number v-model="createForm.max_drawdown" :min="5" :max="50" /> %
        </el-form-item>
        <el-form-item label="基准指数">
          <el-select v-model="createForm.benchmark_index" style="width: 100%">
            <el-option label="沪深300" value="000300" />
            <el-option label="上证指数" value="000001" />
            <el-option label="创业板指" value="399006" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCreateDialog = false">取消</el-button>
        <el-button type="primary" @click="handleCreatePortfolio">确定</el-button>
      </template>
    </el-dialog>

    <el-dialog
      v-model="showTradeDialogVisible"
      :title="tradeType === 'buy' ? '买入股票' : '卖出股票'"
      width="500px"
    >
      <el-form :model="tradeForm" label-width="100px">
        <el-form-item label="股票代码" required>
          <el-input v-model="tradeForm.stock_code" placeholder="请输入股票代码" />
        </el-form-item>
        <el-form-item label="股票名称">
          <el-input v-model="tradeForm.stock_name" placeholder="请输入股票名称" />
        </el-form-item>
        <el-form-item label="交易日期" required>
          <el-date-picker
            v-model="tradeForm.trade_date"
            type="date"
            placeholder="选择日期"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="股数" required>
          <el-input-number v-model="tradeForm.shares" :min="1" :step="100" style="width: 100%" />
        </el-form-item>
        <el-form-item label="价格" required>
          <el-input-number
            v-model="tradeForm.price"
            :min="0.01"
            :precision="2"
            :step="0.01"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="手续费">
          <el-input-number
            v-model="tradeForm.commission"
            :min="0"
            :precision="2"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item v-if="tradeType === 'sell'" label="印花税">
          <el-input-number
            v-model="tradeForm.stamp_duty"
            :min="0"
            :precision="2"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="tradeForm.remark" type="textarea" rows="2" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showTradeDialogVisible = false">取消</el-button>
        <el-button :type="tradeType === 'buy' ? 'primary' : 'danger'" @click="handleTrade"
          >确定</el-button
        >
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, watch } from 'vue'
import { Refresh } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  getPortfolioList,
  createPortfolio,
  getPositionList,
  getTradeList,
  recordBuy,
  recordSell,
  deletePosition,
  getPerformance,
  getProfitAttribution,
  getRiskAlerts,
  checkRisk,
  handleAlert as handleAlertApi
} from '@/api/portfolio'
import type { Portfolio, Position, Trade, RiskAlert } from './types/portfolio'

const portfolios = ref<Portfolio[]>([])
const selectedPortfolioId = ref<number | null>(null)
const activeTab = ref('positions')
const loading = ref(false)

const positions = ref<Position[]>([])
const trades = ref<Trade[]>([])
const riskAlerts = ref<RiskAlert[]>([])
const performance = ref<any>({})
const attribution = ref<any>({})

const showCreateDialog = ref(false)
const createForm = reactive({
  name: '',
  description: '',
  max_single_position: 20,
  max_drawdown: 15,
  benchmark_index: '000300'
})

const showTradeDialogVisible = ref(false)
const tradeType = ref<'buy' | 'sell'>('buy')
const tradeForm = reactive({
  stock_code: '',
  stock_name: '',
  trade_date: new Date().toISOString().slice(0, 10),
  shares: 100,
  price: 0,
  commission: 0,
  stamp_duty: 0,
  remark: ''
})

async function loadPortfolios() {
  try {
    const { data } = await getPortfolioList()
    portfolios.value = data.data || []
    if (portfolios.value.length > 0 && !selectedPortfolioId.value) {
      const defaultPortfolio = portfolios.value.find((p) => p.is_default)
      selectedPortfolioId.value = defaultPortfolio?.id || portfolios.value[0].id
    }
  } catch (error) {
    console.error('加载组合列表失败:', error)
  }
}

async function loadPortfolioData() {
  if (!selectedPortfolioId.value) return

  loading.value = true
  try {
    const [posRes, tradeRes, perfRes, attrRes] = await Promise.all([
      getPositionList(selectedPortfolioId.value),
      getTradeList(selectedPortfolioId.value),
      getPerformance(selectedPortfolioId.value),
      getProfitAttribution(selectedPortfolioId.value)
    ])

    positions.value = posRes.data.data || []
    trades.value = tradeRes.data.data || []
    performance.value = perfRes.data.data || {}
    attribution.value = attrRes.data.data || {}
  } catch (error) {
    console.error('加载数据失败:', error)
    ElMessage.error('加载数据失败')
  } finally {
    loading.value = false
  }
}

async function loadRiskAlerts() {
  if (!selectedPortfolioId.value) return
  try {
    const { data } = await getRiskAlerts(selectedPortfolioId.value)
    riskAlerts.value = data.data || []
  } catch (error) {
    console.error('加载预警失败:', error)
  }
}

function handlePortfolioChange() {
  loadPortfolioData()
  loadRiskAlerts()
}

async function handleCreatePortfolio() {
  if (!createForm.name) {
    ElMessage.warning('请输入组合名称')
    return
  }

  try {
    await createPortfolio(createForm)
    ElMessage.success('创建成功')
    showCreateDialog.value = false
    loadPortfolios()
  } catch (error) {
    ElMessage.error('创建失败')
  }
}

function showTradeDialog(type: 'buy' | 'sell') {
  tradeType.value = type
  tradeForm.stock_code = ''
  tradeForm.stock_name = ''
  tradeForm.trade_date = new Date().toISOString().slice(0, 10)
  tradeForm.shares = 100
  tradeForm.price = 0
  tradeForm.commission = 0
  tradeForm.stamp_duty = 0
  tradeForm.remark = ''
  showTradeDialogVisible.value = true
}

async function handleTrade() {
  if (
    !selectedPortfolioId.value ||
    !tradeForm.stock_code ||
    !tradeForm.trade_date ||
    tradeForm.shares <= 0 ||
    tradeForm.price <= 0
  ) {
    ElMessage.warning('请填写完整信息')
    return
  }

  try {
    const data = {
      ...tradeForm,
      trade_date:
        typeof tradeForm.trade_date === 'string'
          ? tradeForm.trade_date
          : new Date(tradeForm.trade_date).toISOString().slice(0, 10)
    }

    if (tradeType.value === 'buy') {
      await recordBuy(selectedPortfolioId.value, data)
    } else {
      await recordSell(selectedPortfolioId.value, data)
    }

    ElMessage.success('操作成功')
    showTradeDialogVisible.value = false
    loadPortfolioData()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

async function handleDeletePosition(row: Position) {
  try {
    await ElMessageBox.confirm('确定删除该持仓?', '提示', { type: 'warning' })
    await deletePosition(selectedPortfolioId.value!, row.stock_code)
    ElMessage.success('删除成功')
    loadPortfolioData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

async function handleRiskCheck() {
  if (!selectedPortfolioId.value) return
  try {
    await checkRisk(selectedPortfolioId.value)
    ElMessage.success('风控检查完成')
    loadRiskAlerts()
  } catch (error) {
    ElMessage.error('风控检查失败')
  }
}

async function handleAlert(row: RiskAlert) {
  try {
    await handleAlertApi(row.id)
    ElMessage.success('处理成功')
    loadRiskAlerts()
  } catch (error) {
    ElMessage.error('处理失败')
  }
}

watch(selectedPortfolioId, () => {
  if (selectedPortfolioId.value) {
    loadPortfolioData()
    loadRiskAlerts()
  }
})

onMounted(() => {
  loadPortfolios()
})
</script>

<style scoped lang="scss">
.portfolio-page {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: var(--el-bg-color);

  .portfolio-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px;
    border-bottom: 1px solid var(--el-border-color);

    .header-left {
      display: flex;
      align-items: center;
      gap: 12px;
    }
  }

  .portfolio-content {
    flex: 1;
    overflow: auto;
    padding: 16px;
  }

  .position-summary {
    margin-bottom: 16px;
  }
}
</style>
