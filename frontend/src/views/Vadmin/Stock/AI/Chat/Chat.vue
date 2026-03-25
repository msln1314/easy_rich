<script setup lang="ts">
import { ref, reactive, nextTick } from 'vue'
import { ElMessage, ElRow, ElCol, ElCard, ElInput, ElButton, ElScrollbar, ElEmpty, ElTag } from 'element-plus'
import { ContentWrap } from '@/components/ContentWrap'
import { aiChat, type ChatRequest } from '@/api/stock/ai'

defineOptions({
  name: 'AIChat'
})

// 状态
const stockCode = ref('')
const stockName = ref('')
const inputMessage = ref('')
const loading = ref(false)
const messages = reactive<Array<{ role: string; content: string; time: string }>>([])

// 发送消息
const handleSend = async () => {
  if (!stockCode.value) {
    ElMessage.warning('请先输入股票代码')
    return
  }
  if (!inputMessage.value.trim()) {
    ElMessage.warning('请输入问题')
    return
  }

  const userMessage = inputMessage.value.trim()
  messages.push({
    role: 'user',
    content: userMessage,
    time: new Date().toLocaleTimeString()
  })

  inputMessage.value = ''
  loading.value = true

  try {
    const request: ChatRequest = {
      stock_code: stockCode.value,
      message: userMessage
    }

    const res = await aiChat(request)
    if (res.code === 200 && res.data) {
      messages.push({
        role: 'assistant',
        content: res.data.message,
        time: new Date().toLocaleTimeString()
      })
    } else {
      ElMessage.error(res.msg || '分析失败')
    }
  } catch (error: any) {
    ElMessage.error(error.message || '请求失败')
  } finally {
    loading.value = false
  }
}

// 快捷问题
const quickQuestions = [
  '分析这只股票的技术面',
  '这只股票的基本面如何？',
  '近期有什么重大消息？',
  '给出投资建议'
]

const handleQuickQuestion = (question: string) => {
  inputMessage.value = question
  handleSend()
}

// 清空对话
const clearChat = () => {
  messages.length = 0
}

// 信号颜色
const getSignalColor = (signal: string) => {
  const colors: Record<string, string> = {
    buy: 'success',
    sell: 'danger',
    hold: 'warning'
  }
  return colors[signal] || 'info'
}
</script>

<template>
  <ContentWrap>
    <ElRow :gutter="20" class="h-[calc(100vh-200px)]">
      <!-- 左侧：股票选择 -->
      <ElCol :span="6">
        <ElCard class="h-full">
          <template #header>
            <div class="flex items-center justify-between">
              <span class="font-bold">股票选择</span>
            </div>
          </template>

          <div class="mb-4">
            <label class="block text-sm text-gray-500 mb-2">股票代码</label>
            <ElInput
              v-model="stockCode"
              placeholder="请输入股票代码，如 000001"
              clearable
            />
          </div>

          <div class="mb-4">
            <label class="block text-sm text-gray-500 mb-2">快捷问题</label>
            <div class="space-y-2">
              <ElButton
                v-for="q in quickQuestions"
                :key="q"
                size="small"
                @click="handleQuickQuestion(q)"
                class="w-full justify-start"
              >
                {{ q }}
              </ElButton>
            </div>
          </div>

          <ElButton type="danger" plain class="w-full" @click="clearChat">
            清空对话
          </ElButton>
        </ElCard>
      </ElCol>

      <!-- 右侧：对话区域 -->
      <ElCol :span="18">
        <ElCard class="h-full flex flex-col">
          <template #header>
            <div class="flex items-center justify-between">
              <span class="font-bold">AI 对话助手</span>
              <ElTag v-if="stockCode" type="primary">{{ stockCode }}</ElTag>
            </div>
          </template>

          <!-- 消息列表 -->
          <ElScrollbar class="flex-1 mb-4" height="calc(100vh - 380px)">
            <div v-if="messages.length === 0" class="flex items-center justify-center h-full">
              <ElEmpty description="开始与 AI 对话吧" />
            </div>
            <div v-else class="space-y-4 p-4">
              <div
                v-for="(msg, index) in messages"
                :key="index"
                :class="[
                  'p-4 rounded-lg',
                  msg.role === 'user' ? 'bg-blue-50 ml-12' : 'bg-gray-50 mr-12'
                ]"
              >
                <div class="flex items-center justify-between mb-2">
                  <span class="font-medium">
                    {{ msg.role === 'user' ? '我' : 'AI 助手' }}
                  </span>
                  <span class="text-xs text-gray-400">{{ msg.time }}</span>
                </div>
                <div class="text-sm whitespace-pre-wrap">{{ msg.content }}</div>
              </div>
            </div>
          </ElScrollbar>

          <!-- 输入区域 -->
          <div class="flex gap-2">
            <ElInput
              v-model="inputMessage"
              type="textarea"
              :rows="2"
              placeholder="输入您的问题..."
              :disabled="loading"
              @keydown.enter.ctrl="handleSend"
            />
            <ElButton type="primary" :loading="loading" @click="handleSend">
              发送
            </ElButton>
          </div>
        </ElCard>
      </ElCol>
    </ElRow>
  </ContentWrap>
</template>

<style scoped>
.h-\[calc\(100vh-200px\)\] {
  min-height: 500px;
}
</style>