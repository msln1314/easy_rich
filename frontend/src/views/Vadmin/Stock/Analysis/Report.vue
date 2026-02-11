<script setup lang="tsx">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getStockAnalysisDetailApi } from '@/api/stock/analysis'
import { ElMessage, ElButton } from 'element-plus'
import { ContentWrap } from '@/components/ContentWrap'
import AnalysisReport from './components/AnalysisReport.vue'
import html2canvas from 'html2canvas'

defineOptions({
  name: 'AnalysisReportView'
})

const route = useRoute()
const router = useRouter()
const analysisData = ref<any>(null)
const loading = ref(false)
const reportRef = ref<HTMLElement | null>(null)
const generating = ref(false)

// 加载数据
const loadData = async () => {
  const id = route.query.id as string
  if (!id) {
    ElMessage.error('缺少分析ID')
    router.back()
    return
  }

  loading.value = true
  try {
    const res = await getStockAnalysisDetailApi(Number(id))
    analysisData.value = res.data
  } catch (error) {
    ElMessage.error('加载数据失败')
    router.back()
  } finally {
    loading.value = false
  }
}

// 返回列表
const goBack = () => {
  router.back()
}

// 生成图片
const generateImage = async () => {
  if (!reportRef.value) {
    ElMessage.error('未找到报表内容')
    return
  }

  generating.value = true
  try {
    ElMessage.info('正在生成图片，请稍候...')

    // 等待 DOM 完全渲染
    await new Promise((resolve) => setTimeout(resolve, 100))

    const element = reportRef.value

    // 滚动到顶部确保完整渲染
    window.scrollTo(0, 0)

    // 获取实际的宽高
    const width = element.scrollWidth
    const height = element.scrollHeight

    console.log('元素尺寸:', { width, height })

    const canvas = await html2canvas(element, {
      scale: 2,
      useCORS: true,
      backgroundColor: '#ffffff',
      logging: true,
      width: width,
      height: height,
      windowWidth: window.innerWidth,
      windowHeight: window.innerHeight,
      scrollX: 0,
      scrollY: 0,
      allowTaint: true,
      foreignObjectRendering: false,
      imageTimeout: 15000,
      removeContainer: false,
      onclone: (clonedDoc) => {
        // 确保 clone 的元素有正确的尺寸
        const clonedElement = clonedDoc.querySelector('.analysis-report') as HTMLElement
        if (clonedElement) {
          clonedElement.style.height = 'auto'
          clonedElement.style.minHeight = '100%'
          clonedElement.style.width = '100%'
        }
      }
    })

    console.log('Canvas 尺寸:', { width: canvas.width, height: canvas.height })

    // 转换为图片并下载
    const blob: Blob = await new Promise((resolve) => {
      canvas.toBlob((blob: Blob | null) => resolve(blob!), 'image/png', 1.0)
    })

    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `股票分析报表_${analysisData.value?.stock_code}_${new Date().getTime()}.png`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)

    ElMessage.success('图片生成成功')
  } catch (error) {
    console.error('生成图片失败:', error)
    ElMessage.error('生成图片失败，请重试')
  } finally {
    generating.value = false
  }
}

onMounted(() => {
  loadData()
})
</script>

<template>
  <ContentWrap>
    <div class="header-actions">
      <ElButton @click="goBack">返回列表</ElButton>
      <ElButton type="primary" :loading="generating" @click="generateImage">
        <span v-if="!generating">📷</span>
        {{ generating ? '生成中...' : '生成图片' }}
      </ElButton>
    </div>
    <div ref="reportRef" class="report-container">
      <AnalysisReport v-if="analysisData && !loading" :analysisData="analysisData" />
    </div>
  </ContentWrap>
</template>

<style scoped lang="scss">
.header-actions {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}

.report-container {
  background: white;
  padding: 20px;
  min-height: 100%;
  display: block;
}
</style>
