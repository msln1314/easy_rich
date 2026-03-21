<template>
  <div class="limit-heatmap-card">
    <div class="card-header">
      <div class="header-title">
        <el-icon class="icon"><TrendCharts /></el-icon>
        <span>涨停热力图</span>
      </div>
      <div class="header-stats">
        <span class="stat-item up">涨停 {{ limitUpCount }}</span>
        <span class="stat-item down">跌停 {{ limitDownCount }}</span>
      </div>
    </div>

    <div class="card-content" v-loading="loading">
      <!-- 行业分布 -->
      <div class="industry-section">
        <div class="section-title">行业分布</div>
        <div class="industry-bars">
          <div v-for="item in industryDistribution" :key="item.name" class="industry-bar">
            <span class="industry-name">{{ item.name }}</span>
            <div class="bar-wrapper">
              <div class="bar-fill" :style="{ width: item.percent + '%' }"></div>
            </div>
            <span class="industry-count">{{ item.count }}</span>
          </div>
        </div>
      </div>

      <!-- 时间分布 -->
      <div class="time-section">
        <div class="section-title">分时分布</div>
        <div class="time-grid">
          <div
            v-for="(slot, idx) in timeSlots"
            :key="idx"
            class="time-slot"
            :class="getHeatClass(slot.count)"
          >
            <span class="time-label">{{ slot.label }}</span>
            <span class="time-count">{{ slot.count || '' }}</span>
          </div>
        </div>
      </div>

      <!-- 热点概念 -->
      <div class="concept-section">
        <div class="section-title">热点概念</div>
        <div class="concept-tags">
          <el-tag
            v-for="concept in hotConcepts"
            :key="concept.name"
            :type="concept.count >= 3 ? 'danger' : concept.count >= 2 ? 'warning' : 'info'"
            size="small"
            effect="dark"
            class="concept-tag"
          >
            {{ concept.name }} ({{ concept.count }})
          </el-tag>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { TrendCharts } from '@element-plus/icons-vue'
import { getLimitUpPoolApi } from '/@/api/stock/stockIndex'

interface LimitUpItem {
  stock_code: string
  stock_name: string
  industry?: string
  concept?: string
  limit_up_time?: string
  seal_amount?: number
}

const loading = ref(false)
const limitUpData = ref<LimitUpItem[]>([])
const limitDownCount = ref(0)

// 涨停数量
const limitUpCount = computed(() => limitUpData.value.length)

// 行业分布
const industryDistribution = computed(() => {
  const industryMap: Record<string, number> = {}
  limitUpData.value.forEach((item) => {
    const industry = item.industry || '其他'
    industryMap[industry] = (industryMap[industry] || 0) + 1
  })

  const result = Object.entries(industryMap)
    .map(([name, count]) => ({
      name,
      count,
      percent: limitUpCount.value > 0 ? (count / limitUpCount.value) * 100 : 0
    }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 6)

  return result
})

// 时间分时分布
const timeSlots = computed(() => {
  const slots = [
    { label: '09:30', start: '09:30', end: '09:59', count: 0 },
    { label: '10:00', start: '10:00', end: '10:29', count: 0 },
    { label: '10:30', start: '10:30', end: '10:59', count: 0 },
    { label: '11:00', start: '11:00', end: '11:29', count: 0 },
    { label: '13:00', start: '13:00', end: '13:29', count: 0 },
    { label: '13:30', start: '13:30', end: '13:59', count: 0 },
    { label: '14:00', start: '14:00', end: '14:29', count: 0 },
    { label: '14:30', start: '14:30', end: '15:00', count: 0 }
  ]

  limitUpData.value.forEach((item) => {
    const time = item.limit_up_time
    if (time) {
      const hour = time.substring(0, 5)
      for (const slot of slots) {
        if (hour >= slot.start && hour < slot.end) {
          slot.count++
          break
        }
      }
    }
  })

  return slots
})

// 热点概念
const hotConcepts = computed(() => {
  const conceptMap: Record<string, number> = {}
  limitUpData.value.forEach((item) => {
    if (item.concept) {
      const concepts = item.concept.split(/[,，、]/)
      concepts.forEach((c) => {
        const trimmed = c.trim()
        if (trimmed) {
          conceptMap[trimmed] = (conceptMap[trimmed] || 0) + 1
        }
      })
    }
  })

  return Object.entries(conceptMap)
    .map(([name, count]) => ({ name, count }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 8)
})

function getHeatClass(count: number): string {
  if (count >= 10) return 'heat-high'
  if (count >= 5) return 'heat-medium'
  if (count >= 2) return 'heat-low'
  if (count >= 1) return 'heat-minimal'
  return 'heat-none'
}

async function fetchData() {
  loading.value = true
  try {
    const res = await getLimitUpPoolApi()
    if (res.data) {
      limitUpData.value = res.data.limit_up_list || []
      limitDownCount.value = res.data.limit_down_count || 0
    }
  } catch (error) {
    console.error('获取涨停池数据失败:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchData()
})

defineExpose({
  refresh: fetchData
})
</script>

<style scoped lang="scss">
.limit-heatmap-card {
  background: linear-gradient(145deg, #151c2c 0%, #1a2234 100%);
  border-radius: 10px;
  padding: 14px;
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;

  .header-title {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 14px;
    font-weight: 600;
    color: #fff;

    .icon {
      color: #f43f5e;
      font-size: 16px;
    }
  }

  .header-stats {
    display: flex;
    gap: 12px;

    .stat-item {
      font-size: 12px;
      font-weight: 500;

      &.up {
        color: #f43f5e;
      }
      &.down {
        color: #22c55e;
      }
    }
  }
}

.card-content {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.section-title {
  font-size: 11px;
  color: #64748b;
  margin-bottom: 8px;
  font-weight: 500;
}

// 行业分布
.industry-section {
  .industry-bars {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }

  .industry-bar {
    display: flex;
    align-items: center;
    gap: 8px;

    .industry-name {
      width: 60px;
      font-size: 11px;
      color: #94a3b8;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }

    .bar-wrapper {
      flex: 1;
      height: 6px;
      background: rgba(255, 255, 255, 0.05);
      border-radius: 3px;
      overflow: hidden;

      .bar-fill {
        height: 100%;
        background: linear-gradient(90deg, #f43f5e, #fb7185);
        border-radius: 3px;
        transition: width 0.3s;
      }
    }

    .industry-count {
      width: 24px;
      font-size: 11px;
      font-weight: 600;
      color: #f43f5e;
      text-align: right;
    }
  }
}

// 时间分布
.time-section {
  .time-grid {
    display: grid;
    grid-template-columns: repeat(8, 1fr);
    gap: 4px;
  }

  .time-slot {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 6px 2px;
    border-radius: 4px;
    background: rgba(255, 255, 255, 0.03);

    .time-label {
      font-size: 9px;
      color: #64748b;
      margin-bottom: 2px;
    }

    .time-count {
      font-size: 12px;
      font-weight: 600;
      color: #fff;
    }

    &.heat-high {
      background: rgba(244, 63, 94, 0.4);
      .time-count {
        color: #f43f5e;
      }
    }
    &.heat-medium {
      background: rgba(244, 63, 94, 0.25);
      .time-count {
        color: #fb7185;
      }
    }
    &.heat-low {
      background: rgba(244, 63, 94, 0.15);
      .time-count {
        color: #fda4af;
      }
    }
    &.heat-minimal {
      background: rgba(244, 63, 94, 0.08);
      .time-count {
        color: #fecdd3;
      }
    }
    &.heat-none {
      .time-count {
        color: #475569;
      }
    }
  }
}

// 热点概念
.concept-section {
  .concept-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
  }

  .concept-tag {
    font-size: 10px;
  }
}
</style>
