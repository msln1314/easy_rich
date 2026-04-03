<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import {
  ElMessage,
  ElRow,
  ElCol,
  ElCard,
  ElButton,
  ElSelect,
  ElOption,
  ElTag,
  ElProgress,
  ElScrollbar,
  ElEmpty,
  ElInput,
  ElRadioGroup,
  ElRadioButton,
  ElDescriptions,
  ElDescriptionsItem
} from 'element-plus'
import { ContentWrap } from '@/components/ContentWrap'
import { agentAnalyze, type AgentAnalyzeRequest, type AgentOpinion } from '@/api/stock/ai'

defineOptions({
  name: 'AIWorkbench'
})

// 状态
const stockCode = ref('')
const query = ref('')
const mode = ref<'quick' | 'standard' | 'full'>('standard')
const loading = ref(false)
const progress = ref(0)
const progressMessage = ref('')

// 分析结果
const analysisResult = ref<any>(null)
const agentOpinions = ref<AgentOpinion[]>([])

// 分析模式描述
const modeDescriptions: Record<string, string> = {
  quick: '快速分析 - 技术面 + 决策',
  standard: '标准分析 - 技术面 + 消息面 + 决策',
  full: '深度分析 - 技术面 + 基本面 + 消息面 + 风控 + 决策'
}

// Agent 名称映射
const agentNames: Record<string, string> = {
  technical: '技术分析',
  fundamental: '基本面分析',
  news: '消息面分析',
  risk: '风险评估',
  decision: '综合决策'
}

// 信号颜色
const getSignalColor = (signal: string) => {
  const colors: Record<string, string> = {
    strong_buy: 'danger',
    buy: 'success',
    hold: 'warning',
    sell: 'info',
    strong_sell: ''
  }
  return colors[signal.toLowerCase()] || 'info'
}

// 信号文本
const getSignalText = (signal: string) => {
  const texts: Record<string, string> = {
    strong_buy: '强烈买入',
    buy: '买入',
    hold: '持有',
    sell: '卖出',
    strong_sell: '强烈卖出'
  }
  return texts[signal.toLowerCase()] || signal
}

// 执行分析
const runAnalysis = async () => {
  if (!stockCode.value) {
    ElMessage.warning('请输入股票代码')
    return
  }

  loading.value = true
  progress.value = 0
  progressMessage.value = '开始分析...'
  analysisResult.value = null
  agentOpinions.value = []

  try {
    const request: AgentAnalyzeRequest = {
      stock_code: stockCode.value,
      query: query.value || undefined,
      mode: mode.value
    }

    // 模拟进度更新
    const progressInterval = setInterval(() => {
      if (progress.value < 90) {
        progress.value += 10
      }
    }, 500)

    const res = await agentAnalyze(request)

    clearInterval(progressInterval)
    progress.value = 100

    if (res.code === 200 && res.data) {
      analysisResult.value = res.data
      agentOpinions.value = res.data.agent_opinions || []
      ElMessage.success('分析完成')
    } else {
      ElMessage.error(res.msg || '分析失败')
    }
  } catch (error: any) {
    ElMessage.error(error.message || '请求失败')
  } finally {
    loading.value = false
    progressMessage.value = ''
  }
}

// 重置
const resetAnalysis = () => {
  stockCode.value = ''
  query.value = ''
  analysisResult.value = null
  agentOpinions.value = []
  progress.value = 0
}
</script>

<template>
  <ContentWrap>
    <ElRow :gutter="20">
      <!-- 左侧：配置面板 -->
      <ElCol :span="6">
        <ElCard>
          <template #header>
            <span class="font-bold">分析配置</span>
          </template>

          <div class="mb-4">
            <label class="block text-sm text-gray-500 mb-2">股票代码</label>
            <ElInput v-model="stockCode" placeholder="请输入股票代码" :disabled="loading" />
          </div>

          <div class="mb-4">
            <label class="block text-sm text-gray-500 mb-2">分析模式</label>
            <ElRadioGroup v-model="mode" :disabled="loading">
              <ElRadioButton value="quick">快速</ElRadioButton>
              <ElRadioButton value="standard">标准</ElRadioButton>
              <ElRadioButton value="full">深度</ElRadioButton>
            </ElRadioGroup>
            <div class="text-xs text-gray-400 mt-2">{{ modeDescriptions[mode] }}</div>
          </div>

          <div class="mb-4">
            <label class="block text-sm text-gray-500 mb-2">自定义问题（可选）</label>
            <ElInput
              v-model="query"
              type="textarea"
              :rows="3"
              placeholder="输入您想了解的问题..."
              :disabled="loading"
            />
          </div>

          <div class="flex gap-2">
            <ElButton type="primary" :loading="loading" @click="runAnalysis" class="flex-1">
              开始分析
            </ElButton>
            <ElButton @click="resetAnalysis" :disabled="loading"> 重置 </ElButton>
          </div>

          <!-- 进度条 -->
          <div v-if="loading" class="mt-4">
            <ElProgress :percentage="progress" :stroke-width="10" />
            <div class="text-sm text-gray-500 mt-2 text-center">{{ progressMessage }}</div>
          </div>
        </ElCard>
      </ElCol>

      <!-- 右侧：分析结果 -->
      <ElCol :span="18">
        <!-- 无结果时 -->
        <ElCard v-if="!analysisResult" class="h-[calc(100vh-260px)]">
          <div class="flex items-center justify-center h-full">
            <ElEmpty description="配置分析参数，点击开始分析" />
          </div>
        </ElCard>

        <!-- 有结果时 -->
        <template v-else>
          <!-- 综合结论 -->
          <ElCard class="mb-4">
            <template #header>
              <div class="flex items-center justify-between">
                <span class="font-bold">综合研判</span>
                <ElTag :type="getSignalColor(analysisResult.signal)" size="large">
                  {{ getSignalText(analysisResult.signal) }}
                </ElTag>
              </div>
            </template>

            <ElDescriptions :column="3" border>
              <ElDescriptionsItem label="股票代码">{{
                analysisResult.stock_code
              }}</ElDescriptionsItem>
              <ElDescriptionsItem label="股票名称">{{
                analysisResult.stock_name
              }}</ElDescriptionsItem>
              <ElDescriptionsItem label="分析时间">{{
                analysisResult.analysis_time
              }}</ElDescriptionsItem>
              <ElDescriptionsItem label="置信度">
                <ElProgress :percentage="analysisResult.confidence * 100" :stroke-width="15" />
              </ElDescriptionsItem>
              <ElDescriptionsItem label="信号" :span="2">
                <ElTag :type="getSignalColor(analysisResult.signal)">
                  {{ getSignalText(analysisResult.signal) }}
                </ElTag>
              </ElDescriptionsItem>
            </ElDescriptions>

            <div class="mt-4">
              <div class="font-medium mb-2">分析摘要</div>
              <div class="text-gray-600 bg-gray-50 p-4 rounded-lg">
                {{ analysisResult.summary }}
              </div>
            </div>
          </ElCard>

          <!-- Agent 观点 -->
          <ElCard>
            <template #header>
              <span class="font-bold">各 Agent 观点</span>
            </template>

            <ElRow :gutter="16">
              <ElCol
                v-for="opinion in agentOpinions"
                :key="opinion.agent_name"
                :span="12"
                class="mb-4"
              >
                <ElCard shadow="hover">
                  <template #header>
                    <div class="flex items-center justify-between">
                      <span>{{ agentNames[opinion.agent_type] || opinion.agent_name }}</span>
                      <ElTag :type="getSignalColor(opinion.signal)" size="small">
                        {{ getSignalText(opinion.signal) }}
                      </ElTag>
                    </div>
                  </template>

                  <div class="mb-2">
                    <span class="text-sm text-gray-500">置信度：</span>
                    <ElProgress
                      :percentage="opinion.confidence * 100"
                      :stroke-width="8"
                      class="inline-block w-32"
                    />
                  </div>

                  <ElScrollbar height="150px">
                    <div class="text-sm text-gray-600 whitespace-pre-wrap">
                      {{ opinion.reasoning }}
                    </div>
                  </ElScrollbar>
                </ElCard>
              </ElCol>
            </ElRow>
          </ElCard>
        </template>
      </ElCol>
    </ElRow>
  </ContentWrap>
</template>

<style scoped>
.h-\[calc\(100vh-260px\)\] {
  min-height: 400px;
}
</style>
