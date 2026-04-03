<!-- frontend/src/views/Vadmin/Stock/Drawdown/Drawdown.vue -->
<script setup lang="ts">
import { ref } from 'vue'
import {
  ElMessage,
  ElCard,
  ElInput,
  ElButton,
  ElSelect,
  ElOption,
  ElRow,
  ElCol
} from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import { ContentWrap } from '@/components/ContentWrap'
import { analyzeDrawdown } from '@/api/stock/drawdown'
import type { DrawdownAnalysisResult } from '@/api/stock/drawdown'
import DrawdownAnalysis from './components/DrawdownAnalysis.vue'
import PullbackSignal from './components/PullbackSignal.vue'
import PositionMonitor from './components/PositionMonitor.vue'

defineOptions({
  name: 'DrawdownAnalysis'
})

// 股票代码
const stockCode = ref('')
const loading = ref(false)

// 时间范围选项
const timeRange = ref('1y')
const timeRangeOptions = [
  { label: '近半年', value: '6m' },
  { label: '近一年', value: '1y' },
  { label: '近两年', value: '2y' },
  { label: '近三年', value: '3y' }
]

// 分析结果
const analysisResult = ref<DrawdownAnalysisResult | null>(null)

// 执行分析
const handleAnalyze = async () => {
  if (!stockCode.value) {
    ElMessage.warning('请输入股票代码')
    return
  }

  loading.value = true
  try {
    const res = await analyzeDrawdown({
      stock_code: stockCode.value
    })
    if (res.code === 200) {
      analysisResult.value = res.data
      ElMessage.success('分析完成')
    } else {
      ElMessage.error(res.msg || '分析失败')
    }
  } catch (error) {
    ElMessage.error('分析失败')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <ContentWrap>
    <ElCard>
      <template #header>
        <div class="flex items-center justify-between">
          <span class="font-bold text-lg">回撤分析</span>
        </div>
      </template>

      <!-- 搜索栏 -->
      <ElRow :gutter="20" class="mb-4">
        <ElCol :span="6">
          <ElInput
            v-model="stockCode"
            placeholder="请输入股票代码"
            clearable
            @keyup.enter="handleAnalyze"
          />
        </ElCol>
        <ElCol :span="4">
          <ElSelect v-model="timeRange" style="width: 100%">
            <ElOption
              v-for="item in timeRangeOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </ElSelect>
        </ElCol>
        <ElCol :span="4">
          <ElButton type="primary" :icon="Search" :loading="loading" @click="handleAnalyze">
            分析
          </ElButton>
        </ElCol>
      </ElRow>

      <!-- 分析结果 -->
      <template v-if="analysisResult">
        <DrawdownAnalysis :result="analysisResult" class="mb-4" />
        <PullbackSignal :stock-code="stockCode" class="mb-4" />
        <PositionMonitor :stock-code="stockCode" />
      </template>

      <!-- 空状态 -->
      <div v-else class="text-center text-gray-400 py-20"> 请输入股票代码开始分析 </div>
    </ElCard>
  </ContentWrap>
</template>
