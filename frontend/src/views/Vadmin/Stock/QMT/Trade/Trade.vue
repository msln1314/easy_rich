<!-- frontend/src/views/Vadmin/Stock/QMT/Trade/Trade.vue -->
<template>
  <div class="qmt-trade">
    <el-row :gutter="20">
      <!-- 左侧：下单表单 -->
      <el-col :span="8">
        <el-card class="order-form-card">
          <template #header>
            <div class="card-header">
              <span>下单</span>
              <el-tag :type="qmtStatus === 'connected' ? 'success' : 'warning'" size="small">
                {{ qmtStatus === 'connected' ? '已连接' : '模拟模式' }}
              </el-tag>
            </div>
          </template>

          <el-form :model="orderForm" label-width="80px" :rules="orderRules" ref="orderFormRef">
            <el-form-item label="股票代码" prop="stock_code">
              <el-input v-model="orderForm.stock_code" placeholder="请输入股票代码" />
            </el-form-item>

            <el-form-item label="方向" prop="direction">
              <el-radio-group v-model="orderForm.direction">
                <el-radio-button value="buy">买入</el-radio-button>
                <el-radio-button value="sell">卖出</el-radio-button>
              </el-radio-group>
            </el-form-item>

            <el-form-item label="订单类型" prop="order_type">
              <el-select v-model="orderForm.order_type" style="width: 100%">
                <el-option label="限价单" value="limit" />
                <el-option label="市价单" value="market" />
              </el-select>
            </el-form-item>

            <el-form-item label="价格" prop="price" v-if="orderForm.order_type === 'limit'">
              <el-input-number v-model="orderForm.price" :precision="2" :min="0" style="width: 100%" />
            </el-form-item>

            <el-form-item label="数量" prop="quantity">
              <el-input-number v-model="orderForm.quantity" :min="100" :step="100" style="width: 100%" />
            </el-form-item>

            <el-form-item>
              <el-button type="primary" @click="handlePlaceOrder" :loading="submitting">
                {{ orderForm.direction === 'buy' ? '买入' : '卖出' }}
              </el-button>
              <el-button @click="resetForm">重置</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>

      <!-- 右侧：委托列表 -->
      <el-col :span="16">
        <el-card class="order-list-card">
          <template #header>
            <div class="card-header">
              <span>委托列表</span>
              <el-button type="primary" size="small" @click="refreshOrders">刷新</el-button>
            </div>
          </template>

          <el-table :data="orders" v-loading="loading" stripe>
            <el-table-column prop="order_id" label="委托ID" width="100" />
            <el-table-column prop="stock_code" label="股票代码" width="100" />
            <el-table-column prop="stock_name" label="股票名称" width="100" />
            <el-table-column prop="direction" label="方向" width="80">
              <template #default="{ row }">
                <el-tag :type="row.direction === 'buy' ? 'danger' : 'success'" size="small">
                  {{ row.direction === 'buy' ? '买入' : '卖出' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="price" label="价格" width="100" />
            <el-table-column prop="quantity" label="数量" width="100" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)" size="small">
                  {{ getStatusText(row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="filled_quantity" label="已成交" width="100" />
            <el-table-column label="操作" fixed="right" width="100">
              <template #default="{ row }">
                <el-button
                  v-if="row.status === 'pending'"
                  type="danger"
                  size="small"
                  @click="handleCancelOrder(row.order_id)"
                >
                  撤单
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { placeOrderApi, cancelOrderApi, getOrdersApi, getQMTHealthApi } from '@/api/stock/qmt'

// 状态
const loading = ref(false)
const submitting = ref(false)
const qmtStatus = ref<'connected' | 'mock'>('mock')
const orders = ref<any[]>([])

// 表单
const orderFormRef = ref<FormInstance>()
const orderForm = reactive({
  stock_code: '',
  direction: 'buy' as 'buy' | 'sell',
  price: 0,
  quantity: 100,
  order_type: 'limit' as 'limit' | 'market'
})

const orderRules: FormRules = {
  stock_code: [{ required: true, message: '请输入股票代码', trigger: 'blur' }],
  direction: [{ required: true, message: '请选择方向', trigger: 'change' }],
  quantity: [{ required: true, message: '请输入数量', trigger: 'blur' }]
}

// 方法
const checkQMTStatus = async () => {
  try {
    const { data } = await getQMTHealthApi()
    qmtStatus.value = data.qmt?.connected ? 'connected' : 'mock'
  } catch (e) {
    qmtStatus.value = 'mock'
  }
}

const refreshOrders = async () => {
  loading.value = true
  try {
    const { data } = await getOrdersApi()
    orders.value = data?.orders || []
  } catch (e: any) {
    ElMessage.error(e.message || '获取委托列表失败')
  } finally {
    loading.value = false
  }
}

const handlePlaceOrder = async () => {
  await orderFormRef.value?.validate()

  submitting.value = true
  try {
    await placeOrderApi(orderForm)
    ElMessage.success('下单成功')
    resetForm()
    refreshOrders()
  } catch (e: any) {
    ElMessage.error(e.message || '下单失败')
  } finally {
    submitting.value = false
  }
}

const handleCancelOrder = async (orderId: string) => {
  await ElMessageBox.confirm('确定要撤销该委托吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })

  try {
    await cancelOrderApi(orderId)
    ElMessage.success('撤单成功')
    refreshOrders()
  } catch (e: any) {
    ElMessage.error(e.message || '撤单失败')
  }
}

const resetForm = () => {
  orderFormRef.value?.resetFields()
  orderForm.price = 0
  orderForm.quantity = 100
}

const getStatusType = (status: string) => {
  const map: Record<string, string> = {
    pending: 'warning',
    partial: 'info',
    filled: 'success',
    cancelled: 'info',
    rejected: 'danger'
  }
  return map[status] || 'info'
}

const getStatusText = (status: string) => {
  const map: Record<string, string> = {
    pending: '待成交',
    partial: '部分成交',
    filled: '已成交',
    cancelled: '已撤单',
    rejected: '已拒绝'
  }
  return map[status] || status
}

// 生命周期
onMounted(() => {
  checkQMTStatus()
  refreshOrders()
})
</script>

<style scoped>
.qmt-trade {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.order-form-card,
.order-list-card {
  height: calc(100vh - 200px);
  overflow: auto;
}
</style>