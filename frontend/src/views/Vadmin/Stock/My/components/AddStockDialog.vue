<script setup lang="tsx">
import { ref, watch } from 'vue'
import { ElMessage, ElInput, ElButton, ElSelect, ElOption } from 'element-plus'
import { getStockPageApi } from '@/api/stock/base'
import { batchAddStocksToGroupApi } from '@/api/stock/my_stock'
import { Icon } from '@/components/Icon'

defineOptions({
  name: 'AddStockDialog'
})

interface Props {
  groupId: number | null
  visible: boolean
}

interface Emits {
  (e: 'update:visible', value: boolean): void
  (e: 'success'): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const searchKeyword = ref('')
const stockOptions = ref<any[]>([])
const selectedStock = ref<number | null>(null)
const selectedStockList = ref<any[]>([])
const loading = ref(false)
const adding = ref(false)

const handleSearch = async () => {
  if (!searchKeyword.value) {
    ElMessage.warning('请输入股票代码或名称')
    return
  }

  loading.value = true
  try {
    const res = await getStockPageApi({
      keywords: searchKeyword.value
    })
    stockOptions.value = res.data
  } catch (error) {
    console.error('获取股票列表失败', error)
    ElMessage.error('获取股票列表失败')
  } finally {
    loading.value = false
  }
}

const handleAdd = async () => {
  if (!selectedStock.value) {
    ElMessage.warning('请先选择股票')
    return
  }

  adding.value = true
  try {
    const stock = stockOptions.value.find((item: any) => item.id === selectedStock.value)
    if (!stock) {
      ElMessage.error('未找到选中的股票')
      return
    }

    await batchAddStocksToGroupApi({
      group_id: props.groupId,
      stock_ids: [selectedStock.value]
    })

    selectedStockList.value.push(stock)
    ElMessage.success('添加成功')
    selectedStock.value = null
  } catch (error) {
    console.error('添加股票失败', error)
    ElMessage.error('添加股票失败')
  } finally {
    adding.value = false
  }
}

const handleRemove = (stockId: number) => {
  const index = selectedStockList.value.findIndex((item: any) => item.id === stockId)
  if (index > -1) {
    selectedStockList.value.splice(index, 1)
  }
}

const handleConfirm = () => {
  emit('update:visible', false)
  if (selectedStockList.value.length > 0) {
    emit('success')
  }
}

const handleCancel = () => {
  emit('update:visible', false)
}

watch(
  () => props.visible,
  (val) => {
    if (!val) {
      searchKeyword.value = ''
      stockOptions.value = []
      selectedStock.value = null
      selectedStockList.value = []
    }
  }
)
</script>

<template>
  <div class="add-stock-dialog">
    <!-- 搜索区域 -->
    <div class="search-area">
      <el-input
        v-model="searchKeyword"
        placeholder="请输入股票代码或名称"
        clearable
        @keyup.enter="handleSearch"
      >
        <template #suffix>
          <Icon icon="ep:search" size="16" />
        </template>
      </el-input>
      <el-button type="primary" :loading="loading" @click="handleSearch"> 搜索 </el-button>
    </div>

    <!-- 搜索结果 -->
    <div v-if="stockOptions.length > 0" class="search-result">
      <el-select
        v-model="selectedStock"
        placeholder="请选择要添加的股票"
        style="width: 100%"
        filterable
        clearable
      >
        <el-option
          v-for="item in stockOptions"
          :key="item.id"
          :label="`${item.name} (${item.stock_code})`"
          :value="item.id"
        />
      </el-select>
      <el-button
        type="success"
        :loading="adding"
        :disabled="!selectedStock"
        style="width: 100%; margin-top: 10px"
        @click="handleAdd"
      >
        添加
      </el-button>
    </div>

    <!-- 已添加股票列表 -->
    <div v-if="selectedStockList.length > 0" class="added-list">
      <div class="list-title">已添加的股票（{{ selectedStockList.length }}）</div>
      <div class="list-content">
        <div v-for="item in selectedStockList" :key="item.id" class="list-item">
          <span>{{ item.name }} ({{ item.stock_code }})</span>
          <el-button type="danger" size="small" text @click="handleRemove(item.id)">
            移除
          </el-button>
        </div>
      </div>
    </div>

    <!-- 确认按钮 -->
    <div class="dialog-footer">
      <el-button @click="handleCancel">取消</el-button>
      <el-button type="primary" @click="handleConfirm">
        确定（{{ selectedStockList.length }}）
      </el-button>
    </div>
  </div>
</template>

<style scoped lang="scss">
.add-stock-dialog {
  .search-area {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
  }

  .search-result {
    margin-bottom: 20px;
    padding: 15px;
    background: #f5f7fa;
    border-radius: 4px;
  }

  .added-list {
    margin-bottom: 20px;

    .list-title {
      font-weight: 500;
      margin-bottom: 10px;
      color: #303133;
    }

    .list-content {
      max-height: 200px;
      overflow-y: auto;
      border: 1px solid #dcdfe6;
      border-radius: 4px;

      .list-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 8px 12px;
        border-bottom: 1px solid #f0f0f0;

        &:last-child {
          border-bottom: none;
        }
      }
    }
  }

  .dialog-footer {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    border-top: 1px solid #dcdfe6;
    padding-top: 15px;
  }
}
</style>
