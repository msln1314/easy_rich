<script setup lang="ts">
import { ref, computed } from 'vue'
import {
  ElCard,
  ElButton,
  ElInput,
  ElRadioGroup,
  ElRadioButton,
  ElEmpty,
  ElTag,
  ElMessage
} from 'element-plus'
import { Search, Refresh } from '@element-plus/icons-vue'
import { ContentWrap } from '@/components/ContentWrap'
import PatternCard from './components/PatternCard.vue'
import {
  detectAllPatterns,
  scanPatterns,
  patternTypeMap,
  patternTypeOptions,
  type PatternResult
} from '@/api/stock/pattern'

defineOptions({
  name: 'PatternRecognition'
})

// 股票代码输入
const stockCode = ref('')
const loading = ref(false)

// 形态筛选
const patternFilter = ref('')

// 检测结果
const results = ref<PatternResult[]>([])

// 检测形态
const handleDetect = async () => {
  if (!stockCode.value.trim()) {
    ElMessage.warning('请输入股票代码')
    return
  }

  loading.value = true
  results.value = []
  try {
    const res = await detectAllPatterns(stockCode.value.trim())
    results.value = res.data?.data || []
    if (results.value.length === 0) {
      ElMessage.info('未检测到任何形态')
    } else {
      ElMessage.success(`检测到 ${results.value.length} 个形态`)
    }
  } catch (error) {
    ElMessage.error('检测失败')
  } finally {
    loading.value = false
  }
}

// 重置
const handleReset = () => {
  stockCode.value = ''
  results.value = []
  patternFilter.value = ''
}

// 筛选后的结果
const filteredResults = computed(() => {
  if (!patternFilter.value) return results.value
  return results.value.filter((r) => r.pattern_type === patternFilter.value)
})

// 获取形态颜色
const getPatternColor = (type: string) => {
  return patternTypeMap[type]?.color || '#909399'
}
</script>

<template>
  <ContentWrap>
    <div class="pattern-container">
      <!-- 输入区域 -->
      <ElCard class="input-card" shadow="never">
        <template #header>
          <span class="card-title">K线形态识别</span>
        </template>
        <div class="input-section">
          <div class="input-row">
            <ElInput
              v-model="stockCode"
              placeholder="请输入股票代码，如：000001"
              style="width: 300px"
              clearable
              @keyup.enter="handleDetect"
            />
            <ElButton type="primary" :icon="Search" :loading="loading" @click="handleDetect">检测形态</ElButton>
            <ElButton :icon="Refresh" @click="handleReset">重置</ElButton>
          </div>
        </div>
      </ElCard>

      <!-- 形态筛选 -->
      <ElCard class="filter-card" shadow="never" v-if="results.length > 0">
        <div class="filter-section">
          <span class="filter-label">形态筛选：</span>
          <ElRadioGroup v-model="patternFilter" size="small">
            <ElRadioButton v-for="opt in patternTypeOptions" :key="opt.value" :label="opt.value">
              {{ opt.label }}
            </ElRadioButton>
          </ElRadioGroup>
        </div>
      </ElCard>

      <!-- 检测结果 -->
      <ElCard class="result-card" shadow="never">
        <template #header>
          <div class="card-header">
            <span class="card-title">检测结果</span>
            <ElTag v-if="results.length > 0" type="info">共 {{ results.length }} 个形态</ElTag>
          </div>
        </template>

        <ElEmpty v-if="!loading && results.length === 0" description="请输入股票代码进行形态检测" />

        <div v-else class="results-grid" v-loading="loading">
          <PatternCard
            v-for="result in filteredResults"
            :key="result.pattern_type + result.detected_time"
            :pattern="result"
          />
        </div>

        <div v-if="results.length > 0 && filteredResults.length === 0" class="no-result">
          <ElEmpty description="该筛选条件下没有形态" />
        </div>
      </ElCard>

      <!-- 形态说明 -->
      <ElCard class="guide-card" shadow="never">
        <template #header>
          <span class="card-title">形态说明</span>
        </template>
        <div class="guide-content">
          <div v-for="(info, type) in patternTypeMap" :key="type" class="guide-item">
            <ElTag :color="info.color" effect="dark" size="small">{{ info.name }}</ElTag>
            <span class="guide-desc">{{ info.description }}</span>
          </div>
        </div>
      </ElCard>
    </div>
  </ContentWrap>
</template>

<style lang="scss" scoped>
.pattern-container {
  .input-card,
  .filter-card,
  .result-card,
  .guide-card {
    margin-bottom: 16px;
  }

  .card-title {
    font-size: 16px;
    font-weight: 600;
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .input-section {
    .input-row {
      display: flex;
      gap: 12px;
      align-items: center;
    }
  }

  .filter-section {
    display: flex;
    align-items: center;
    gap: 12px;

    .filter-label {
      font-size: 14px;
      color: #606266;
    }
  }

  .results-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
    gap: 16px;
  }

  .no-result {
    padding: 20px 0;
  }

  .guide-content {
    display: flex;
    flex-direction: column;
    gap: 12px;

    .guide-item {
      display: flex;
      align-items: flex-start;
      gap: 12px;

      .guide-desc {
        font-size: 14px;
        color: #606266;
        line-height: 1.5;
      }
    }
  }
}
</style>