<template>
  <ContentWrap class="factor-manage-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-left">
        <h2>因子库管理</h2>
        <span class="total-count">共 {{ total }} 个因子</span>
      </div>
      <div class="header-actions">
        <ElButton type="primary" @click="handleAddFactor">
          <Icon icon="ep:plus" class="mr-5px" />
          添加因子
        </ElButton>
        <ElButton type="success" @click="handleSyncFromQmt" :loading="syncing">
          <Icon icon="ep:download" class="mr-5px" />
          从QMT同步
        </ElButton>
        <ElButton @click="loadFactors">
          <Icon icon="ep:refresh" class="mr-5px" />
          刷新
        </ElButton>
      </div>
    </div>

    <!-- 筛选区域 -->
    <div class="filter-section">
      <ElSelect
        v-model="filterCategory"
        placeholder="选择分类"
        clearable
        style="width: 150px"
        @change="handleFilterChange"
      >
        <ElOption
          v-for="cat in categories"
          :key="cat.key"
          :label="cat.name"
          :value="cat.key"
        />
      </ElSelect>

      <ElInput
        v-model="filterKeyword"
        placeholder="搜索因子名称/ID"
        clearable
        style="width: 200px"
        @input="handleFilterChange"
      >
        <template #prefix>
          <Icon icon="ep:search" />
        </template>
      </ElInput>
    </div>

    <!-- 因子列表 -->
    <div class="factor-grid" v-loading="loading">
      <div
        class="factor-card"
        v-for="factor in filteredFactors"
        :key="factor.factor_id"
        @click="handleFactorClick(factor)"
      >
        <div class="card-header">
          <span class="factor-id">{{ factor.factor_id }}</span>
          <ElTag :type="getCategoryTagType(factor.category)" size="small">
            {{ getCategoryName(factor.category) }}
          </ElTag>
        </div>

        <div class="factor-name">{{ factor.factor_name }}</div>

        <div class="factor-desc">{{ factor.description || '暂无描述' }}</div>

        <div class="card-footer">
          <div class="formula" v-if="factor.formula">
            <Icon icon="ep:document" class="mr-5px" />
            <span class="formula-text">{{ factor.formula }}</span>
          </div>
          <div class="unit" v-if="factor.unit">
            单位: {{ factor.unit }}
          </div>
        </div>

        <div class="card-actions">
          <ElButton link type="primary" @click.stop="handleViewValues(factor)">
            查看数值
          </ElButton>
          <ElButton link type="primary" @click.stop="handleViewIC(factor)">
            IC分析
          </ElButton>
          <ElButton link type="primary" @click.stop="handleScreen(factor)">
            选股
          </ElButton>
        </div>
      </div>
    </div>

    <ElEmpty v-if="!loading && filteredFactors.length === 0" description="暂无因子数据" />

    <!-- 因子详情弹窗 -->
    <ElDialog
      v-model="detailVisible"
      :title="currentFactor?.factor_name || '因子详情'"
      width="700px"
      destroy-on-close
    >
      <template v-if="currentFactor">
        <ElDescriptions :column="2" border>
          <ElDescriptionsItem label="因子ID">
            <ElTag>{{ currentFactor.factor_id }}</ElTag>
          </ElDescriptionsItem>
          <ElDescriptionsItem label="分类">
            {{ getCategoryName(currentFactor.category) }}
          </ElDescriptionsItem>
          <ElDescriptionsItem label="单位" v-if="currentFactor.unit">
            {{ currentFactor.unit }}
          </ElDescriptionsItem>
          <ElDescriptionsItem label="数据来源" v-if="currentFactor.data_source">
            {{ currentFactor.data_source }}
          </ElDescriptionsItem>
          <ElDescriptionsItem label="更新频率" v-if="currentFactor.update_freq">
            {{ currentFactor.update_freq }}
          </ElDescriptionsItem>
          <ElDescriptionsItem label="状态">
            <ElTag :type="currentFactor.is_active ? 'success' : 'info'">
              {{ currentFactor.is_active ? '启用' : '禁用' }}
            </ElTag>
          </ElDescriptionsItem>
        </ElDescriptions>

        <ElDivider content-position="left">因子描述</ElDivider>
        <p class="detail-text">{{ currentFactor.description || '暂无描述' }}</p>

        <ElDivider content-position="left">计算公式</ElDivider>
        <div class="formula-box">
          <code>{{ currentFactor.formula || '暂无公式' }}</code>
        </div>

        <ElDivider content-position="left" v-if="currentFactor.params?.length">参数配置</ElDivider>
        <ElTable :data="currentFactor.params" v-if="currentFactor.params?.length" size="small">
          <ElTableColumn prop="key" label="参数名" width="120" />
          <ElTableColumn prop="default" label="默认值" width="100" />
          <ElTableColumn label="说明">
            <template #default="{ row }">
              {{ row.desc || row.name || '-' }}
            </template>
          </ElTableColumn>
        </ElTable>
      </template>

      <template #footer>
        <ElButton @click="handleViewValues(currentFactor)">查看数值</ElButton>
        <ElButton type="primary" @click="detailVisible = false">关闭</ElButton>
      </template>
    </ElDialog>

    <!-- 因子值弹窗 -->
    <ElDialog
      v-model="valuesVisible"
      :title="`${currentFactor?.factor_name || ''} - 因子值`"
      width="900px"
      destroy-on-close
    >
      <div class="values-filter">
        <ElInput
          v-model="stockCodesInput"
          placeholder="输入股票代码，多个用逗号分隔"
          style="width: 300px"
        />
        <ElDatePicker
          v-model="valuesDate"
          type="date"
          placeholder="选择日期"
          format="YYYY-MM-DD"
          value-format="YYYYMMDD"
          style="width: 150px"
        />
        <ElButton type="primary" @click="loadFactorValues">查询</ElButton>
      </div>

      <ElTable :data="factorValues" v-loading="valuesLoading" max-height="400">
        <ElTableColumn prop="stock_code" label="股票代码" width="120" />
        <ElTableColumn prop="stock_name" label="股票名称" width="120" />
        <ElTableColumn prop="value" label="因子值" width="120">
          <template #default="{ row }">
            {{ row.value?.toFixed(4) || '-' }}
          </template>
        </ElTableColumn>
        <ElTableColumn prop="rank" label="排名" width="80" />
        <ElTableColumn prop="percentile" label="百分位" width="100">
          <template #default="{ row }">
            {{ row.percentile?.toFixed(2) || '-' }}%
          </template>
        </ElTableColumn>
      </ElTable>
    </ElDialog>

    <!-- 因子选股弹窗 -->
    <ElDialog
      v-model="screenVisible"
      title="因子选股"
      width="800px"
      destroy-on-close
    >
      <ElForm :model="screenForm" label-width="100px">
        <ElFormItem label="筛选条件">
          <div class="screen-conditions">
            <div
              class="condition-item"
              v-for="(cond, index) in screenForm.conditions"
              :key="index"
            >
              <ElSelect v-model="cond.factor_id" placeholder="选择因子" style="width: 150px">
                <ElOption
                  v-for="f in factors"
                  :key="f.factor_id"
                  :label="f.factor_name"
                  :value="f.factor_id"
                />
              </ElSelect>
              <ElSelect v-model="cond.op" placeholder="操作符" style="width: 100px">
                <ElOption label="大于" value="gt" />
                <ElOption label="小于" value="lt" />
                <ElOption label="大于等于" value="ge" />
                <ElOption label="小于等于" value="le" />
                <ElOption label="等于" value="eq" />
              </ElSelect>
              <ElInputNumber v-model="cond.value" placeholder="值" style="width: 120px" />
              <ElButton
                type="danger"
                link
                @click="screenForm.conditions.splice(index, 1)"
                v-if="screenForm.conditions.length > 1"
              >
                <Icon icon="ep:delete" />
              </ElButton>
            </div>
          </div>
          <ElButton type="primary" link @click="addCondition">
            <Icon icon="ep:plus" class="mr-5px" />
            添加条件
          </ElButton>
        </ElFormItem>

        <ElFormItem label="返回数量">
          <ElInputNumber v-model="screenForm.limit" :min="10" :max="500" :step="10" />
        </ElFormItem>
      </ElForm>

      <ElTable :data="screenResults" v-loading="screenLoading" max-height="300">
        <ElTableColumn prop="stock_code" label="股票代码" width="120" />
        <ElTableColumn prop="stock_name" label="股票名称" width="120" />
        <ElTableColumn prop="score" label="综合得分" width="100">
          <template #default="{ row }">
            {{ row.score?.toFixed(2) || '-' }}
          </template>
        </ElTableColumn>
        <ElTableColumn label="因子值">
          <template #default="{ row }">
            <div class="factor-values-cell">
              <ElTag v-for="(value, key) in row.factor_values" :key="key" size="small" class="mr-5px">
                {{ key }}: {{ value?.toFixed(2) }}
              </ElTag>
            </div>
          </template>
        </ElTableColumn>
      </ElTable>

      <template #footer>
        <ElButton @click="screenVisible = false">取消</ElButton>
        <ElButton type="primary" @click="executeScreen" :loading="screenLoading">
          开始选股
        </ElButton>
      </template>
    </ElDialog>
  </ContentWrap>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Icon } from '@/components/Icon'
import { ContentWrap } from '@/components/ContentWrap'
import request from '@/axios'

// 数据状态
const loading = ref(false)
const syncing = ref(false)
const factors = ref<any[]>([])
const total = ref(0)
const categories = ref<any[]>([])

// 筛选
const filterCategory = ref('')
const filterKeyword = ref('')

// 详情弹窗
const detailVisible = ref(false)
const currentFactor = ref<any>(null)

// 因子值弹窗
const valuesVisible = ref(false)
const valuesLoading = ref(false)
const factorValues = ref<any[]>([])
const stockCodesInput = ref('000001.SZ,600519.SH')
const valuesDate = ref('')

// 选股弹窗
const screenVisible = ref(false)
const screenLoading = ref(false)
const screenResults = ref<any[]>([])
const screenForm = ref({
  conditions: [{ factor_id: '', op: 'gt', value: 0 }],
  date: '',
  limit: 50
})

// 筛选后的因子列表
const filteredFactors = computed(() => {
  let result = factors.value

  if (filterCategory.value) {
    result = result.filter(f => f.category === filterCategory.value)
  }

  if (filterKeyword.value) {
    const keyword = filterKeyword.value.toLowerCase()
    result = result.filter(f =>
      f.factor_name.toLowerCase().includes(keyword) ||
      f.factor_id.toLowerCase().includes(keyword) ||
      (f.description && f.description.toLowerCase().includes(keyword))
    )
  }

  return result
})

// 获取分类名称
function getCategoryName(category: string): string {
  const cat = categories.value.find(c => c.key === category)
  return cat?.name || category
}

// 获取分类标签类型
function getCategoryTagType(category: string): '' | 'success' | 'warning' | 'info' | 'danger' {
  const typeMap: Record<string, '' | 'success' | 'warning' | 'info' | 'danger'> = {
    trend: '',
    momentum: 'success',
    volatility: 'warning',
    volume: 'info',
    value: 'danger',
    growth: 'success',
    quality: 'warning',
    sentiment: 'info',
    custom: ''
  }
  return typeMap[category] || ''
}

// 加载因子分类
async function loadCategories() {
  try {
    const res = await request.get('/api/v1/factor/categories')
    categories.value = res.data || []
  } catch (error) {
    console.error('加载分类失败:', error)
  }
}

// 加载因子列表
async function loadFactors() {
  loading.value = true
  try {
    const res = await request.get('/api/v1/factor/definitions')
    factors.value = res.factors || []
    total.value = res.total || 0
  } catch (error) {
    console.error('加载因子失败:', error)
    ElMessage.error('加载因子失败')
  } finally {
    loading.value = false
  }
}

// 筛选变化
function handleFilterChange() {
  // 使用 computed 自动过滤
}

// 点击因子卡片
function handleFactorClick(factor: any) {
  currentFactor.value = factor
  detailVisible.value = true
}

// 添加因子
function handleAddFactor() {
  ElMessage.info('添加自定义因子功能开发中')
}

// 从QMT同步因子
async function handleSyncFromQmt() {
  syncing.value = true
  try {
    const res = await request.post('/api/v1/factor/sync')
    ElMessage.success(res.message || `同步成功，新增 ${res.synced} 个因子`)
    await loadFactors()
  } catch (error: any) {
    ElMessage.error(error?.message || '同步失败')
  } finally {
    syncing.value = false
  }
}

// 查看因子值
function handleViewValues(factor: any) {
  currentFactor.value = factor
  valuesVisible.value = true
  detailVisible.value = false
}

// 加载因子值
async function loadFactorValues() {
  if (!currentFactor.value || !stockCodesInput.value) {
    ElMessage.warning('请输入股票代码')
    return
  }

  valuesLoading.value = true
  try {
    const stockCodes = stockCodesInput.value.split(',').map(s => s.trim())
    const res = await request.get(`/api/v1/factor/values/${currentFactor.value.factor_id}`, {
      params: {
        stock_codes: stockCodes,
        date: valuesDate.value || undefined
      }
    })
    factorValues.value = res.values || []
  } catch (error) {
    console.error('加载因子值失败:', error)
    ElMessage.error('加载因子值失败')
  } finally {
    valuesLoading.value = false
  }
}

// 查看IC
function handleViewIC(factor: any) {
  ElMessage.info('IC分析功能开发中')
}

// 因子选股
function handleScreen(factor: any) {
  if (factor) {
    screenForm.value.conditions = [{ factor_id: factor.factor_id, op: 'gt', value: 0 }]
  }
  screenVisible.value = true
}

// 添加筛选条件
function addCondition() {
  screenForm.value.conditions.push({ factor_id: '', op: 'gt', value: 0 })
}

// 执行选股
async function executeScreen() {
  const conditions = screenForm.value.conditions.filter(c => c.factor_id)
  if (conditions.length === 0) {
    ElMessage.warning('请至少添加一个筛选条件')
    return
  }

  screenLoading.value = true
  try {
    const res = await request.post('/api/v1/factor/screen', {
      factors: conditions,
      date: screenForm.value.date || undefined,
      limit: screenForm.value.limit
    })
    screenResults.value = res.stocks || []
    ElMessage.success(`筛选出 ${screenResults.value.length} 只股票`)
  } catch (error) {
    console.error('因子选股失败:', error)
    ElMessage.error('因子选股失败')
  } finally {
    screenLoading.value = false
  }
}

onMounted(() => {
  loadCategories()
  loadFactors()
})
</script>

<style scoped lang="scss">
.factor-manage-page {
  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;

    .header-left {
      display: flex;
      align-items: center;
      gap: 15px;

      h2 {
        margin: 0;
        font-size: 20px;
        font-weight: 600;
      }

      .total-count {
        color: var(--el-text-color-secondary);
        font-size: 14px;
      }
    }

    .header-actions {
      display: flex;
      gap: 10px;
    }
  }

  .filter-section {
    display: flex;
    gap: 15px;
    margin-bottom: 20px;
  }

  .factor-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 16px;
  }

  .factor-card {
    background: var(--el-bg-color);
    border: 1px solid var(--el-border-color-lighter);
    border-radius: 8px;
    padding: 16px;
    cursor: pointer;
    transition: all 0.3s;

    &:hover {
      border-color: var(--el-color-primary-light-5);
      box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    }

    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;

      .factor-id {
        font-family: monospace;
        font-size: 13px;
        color: var(--el-color-primary);
        font-weight: 500;
      }
    }

    .factor-name {
      font-size: 16px;
      font-weight: 600;
      margin-bottom: 8px;
      color: var(--el-text-color-primary);
    }

    .factor-desc {
      font-size: 13px;
      color: var(--el-text-color-secondary);
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
      margin-bottom: 12px;
      min-height: 36px;
    }

    .card-footer {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 12px;
      font-size: 12px;
      color: var(--el-text-color-regular);

      .formula {
        display: flex;
        align-items: center;
        background: var(--el-fill-color-light);
        padding: 4px 8px;
        border-radius: 4px;
        max-width: 100%;

        .formula-text {
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
          font-family: monospace;
        }
      }
    }

    .card-actions {
      display: flex;
      gap: 10px;
      padding-top: 12px;
      border-top: 1px solid var(--el-border-color-lighter);
    }
  }
}

.detail-text {
  color: var(--el-text-color-regular);
  line-height: 1.6;
}

.formula-box {
  background: var(--el-fill-color-light);
  padding: 12px;
  border-radius: 4px;
  font-family: monospace;

  code {
    color: var(--el-color-primary);
  }
}

.values-filter {
  display: flex;
  gap: 10px;
  margin-bottom: 16px;
}

.screen-conditions {
  display: flex;
  flex-direction: column;
  gap: 10px;

  .condition-item {
    display: flex;
    gap: 10px;
    align-items: center;
  }
}

.factor-values-cell {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}
</style>