<template>
  <div class="sentiment-card">
    <div class="card-header">
      <div class="header-title">
        <el-icon class="icon"><DataAnalysis /></el-icon>
        <span>市场情绪</span>
      </div>
    </div>

    <div class="card-content" v-loading="loading">
      <div class="sentiment-score">
        <div class="score-circle" :class="sentimentClass">
          <div class="score-value">{{ sentiment.score?.toFixed(0) || '-' }}</div>
          <div class="score-label">情绪评分</div>
        </div>
        <div class="sentiment-level" :class="sentimentClass">
          {{ sentiment.level || '计算中' }}
        </div>
      </div>

      <div class="stats-grid">
        <div class="stat-item">
          <div class="stat-value up">{{ sentiment.zt_count || 0 }}</div>
          <div class="stat-label">涨停家数</div>
        </div>
        <div class="stat-item">
          <div class="stat-value down">{{ sentiment.dt_count || 0 }}</div>
          <div class="stat-label">跌停家数</div>
        </div>
        <div class="stat-item">
          <div class="stat-value hot">{{ sentiment.max_continuous || 0 }}板</div>
          <div class="stat-label">最高连板</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">{{ (sentiment.zt_dt_ratio * 100)?.toFixed(0) || 50 }}%</div>
          <div class="stat-label">涨跌停比</div>
        </div>
      </div>

      <!-- 连板TOP 5 -->
      <div class="continuous-top5" v-if="continuousTop5.length > 0">
        <div class="top5-title">连板TOP 5</div>
        <div class="top5-list">
          <div v-for="(item, idx) in continuousTop5" :key="item.stock_code" class="top5-item">
            <div class="item-rank" :class="getRankClass(idx + 1)">{{ idx + 1 }}</div>
            <div class="item-info">
              <span class="item-name">{{ item.stock_name }}</span>
              <span class="item-code">{{ item.stock_code }}</span>
            </div>
            <div class="item-days" :class="getDaysClass(item.continuous_days)">
              {{ item.continuous_days || '-' }}板
            </div>
          </div>
        </div>
      </div>

      <div class="continuous-bar" v-if="continuousList.length > 0">
        <div class="bar-title">连板分布</div>
        <div class="bar-content">
          <div
            v-for="item in continuousList"
            :key="item.days"
            class="bar-item"
            :style="{ width: item.percent + '%' }"
          >
            <span class="days">{{ item.days }}板</span>
            <span class="count">{{ item.count }}</span>
          </div>
        </div>
      </div>

      <div class="sentiment-hint">
        <span v-if="sentiment.score >= 70">
          <el-icon><CaretTop /></el-icon>
          市场情绪亢奋，注意追高风险
        </span>
        <span v-else-if="sentiment.score >= 50">
          <el-icon><Minus /></el-icon>
          市场情绪温和，可适当参与
        </span>
        <span v-else>
          <el-icon><CaretBottom /></el-icon>
          市场情绪低迷，谨慎操作
        </span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { DataAnalysis, CaretTop, CaretBottom, Minus } from '@element-plus/icons-vue'
import { getMarketSentimentApi, getLimitUpPoolApi } from '/@/api/stock/stockIndex'
import type { MarketSentiment, LimitUpPoolItem } from '/@/api/stock/stockIndex'

const loading = ref(false)
const sentiment = ref<Partial<MarketSentiment>>({
  zt_count: 0,
  dt_count: 0,
  max_continuous: 0,
  continuous_stats: {},
  zt_dt_ratio: 0.5,
  sentiment_score: 50,
  sentiment_level: '计算中'
})

const limitUpList = ref<LimitUpPoolItem[]>([])

const sentimentClass = computed(() => {
  const score = sentiment.value.sentiment_score || 50
  if (score >= 70) return 'hot'
  if (score >= 50) return 'warm'
  return 'cold'
})

const continuousList = computed(() => {
  const stats = sentiment.value.continuous_stats || {}
  const total = Object.values(stats).reduce((a, b) => a + b, 0)
  if (total === 0) return []

  return Object.entries(stats)
    .map(([days, count]) => ({
      days: Number(days),
      count,
      percent: (count / total) * 100
    }))
    .sort((a, b) => b.days - a.days)
    .slice(0, 5)
})

const continuousTop5 = computed(() => {
  return limitUpList.value
    .filter((item) => item.continuous_days && item.continuous_days >= 2)
    .sort((a, b) => (b.continuous_days || 0) - (a.continuous_days || 0))
    .slice(0, 5)
})

function getRankClass(rank: number): string {
  if (rank === 1) return 'gold'
  if (rank === 2) return 'silver'
  if (rank === 3) return 'bronze'
  return ''
}

function getDaysClass(days: number | undefined): string {
  if (!days) return ''
  if (days >= 5) return 'high'
  if (days >= 3) return 'medium'
  return 'low'
}

async function fetchData() {
  loading.value = true
  try {
    const [sentimentRes, limitUpRes] = await Promise.all([
      getMarketSentimentApi(),
      getLimitUpPoolApi()
    ])

    if (sentimentRes.data) {
      sentiment.value = sentimentRes.data
    }

    if (limitUpRes.data && limitUpRes.data.limit_up_list) {
      limitUpList.value = limitUpRes.data.limit_up_list
    }
  } catch (error) {
    console.error('获取市场情绪失败:', error)
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
.sentiment-card {
  background: linear-gradient(145deg, #151c2c 0%, #1a2234 100%);
  border-radius: 12px;
  padding: 16px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;

  .header-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 15px;
    font-weight: 600;
    color: #fff;

    .icon {
      color: #8b5cf6;
    }
  }
}

.sentiment-score {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 16px;

  .score-circle {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border: 3px solid;

    &.hot {
      border-color: #f43f5e;
      background: rgba(244, 63, 94, 0.1);
      .score-value {
        color: #f43f5e;
      }
    }

    &.warm {
      border-color: #f59e0b;
      background: rgba(245, 158, 11, 0.1);
      .score-value {
        color: #f59e0b;
      }
    }

    &.cold {
      border-color: #22c55e;
      background: rgba(34, 197, 94, 0.1);
      .score-value {
        color: #22c55e;
      }
    }

    .score-value {
      font-size: 28px;
      font-weight: 700;
      font-family: 'DIN Alternate', sans-serif;
    }

    .score-label {
      font-size: 10px;
      color: #64748b;
    }
  }

  .sentiment-level {
    margin-top: 8px;
    font-size: 14px;
    font-weight: 600;

    &.hot {
      color: #f43f5e;
    }
    &.warm {
      color: #f59e0b;
    }
    &.cold {
      color: #22c55e;
    }
  }
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
  margin-bottom: 16px;

  .stat-item {
    text-align: center;
    padding: 8px;
    background: rgba(0, 0, 0, 0.2);
    border-radius: 6px;

    .stat-value {
      font-size: 16px;
      font-weight: 700;
      font-family: 'DIN Alternate', sans-serif;

      &.up {
        color: #f43f5e;
      }
      &.down {
        color: #22c55e;
      }
      &.hot {
        color: #fb923c;
      }
    }

    .stat-label {
      font-size: 10px;
      color: #64748b;
      margin-top: 2px;
    }
  }
}

// 连板TOP 5
.continuous-top5 {
  margin-bottom: 12px;

  .top5-title {
    font-size: 12px;
    color: #64748b;
    margin-bottom: 8px;
    font-weight: 500;
  }

  .top5-list {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }

  .top5-item {
    display: flex;
    align-items: center;
    padding: 6px 8px;
    background: rgba(0, 0, 0, 0.2);
    border-radius: 6px;

    .item-rank {
      width: 18px;
      height: 18px;
      border-radius: 4px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 10px;
      font-weight: 600;
      background: rgba(255, 255, 255, 0.05);
      color: #94a3b8;
      margin-right: 8px;

      &.gold {
        background: linear-gradient(135deg, #ffd700 0%, #ffaa00 100%);
        color: #000;
      }

      &.silver {
        background: linear-gradient(135deg, #c0c0c0 0%, #a0a0a0 100%);
        color: #000;
      }

      &.bronze {
        background: linear-gradient(135deg, #cd7f32 0%, #b87333 100%);
        color: #fff;
      }
    }

    .item-info {
      flex: 1;
      min-width: 0;

      .item-name {
        display: block;
        font-size: 12px;
        font-weight: 500;
        color: #fff;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      .item-code {
        font-size: 10px;
        color: #64748b;
      }
    }

    .item-days {
      font-size: 12px;
      font-weight: 700;
      padding: 2px 8px;
      border-radius: 4px;

      &.high {
        background: rgba(244, 63, 94, 0.2);
        color: #f43f5e;
      }

      &.medium {
        background: rgba(251, 146, 60, 0.2);
        color: #fb923c;
      }

      &.low {
        background: rgba(245, 158, 11, 0.2);
        color: #f59e0b;
      }
    }
  }
}

.continuous-bar {
  margin-bottom: 12px;

  .bar-title {
    font-size: 12px;
    color: #64748b;
    margin-bottom: 6px;
  }

  .bar-content {
    display: flex;
    gap: 4px;
    height: 24px;

    .bar-item {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      background: rgba(244, 63, 94, 0.2);
      border-radius: 4px;
      min-width: 30px;

      .days {
        font-size: 10px;
        color: #f43f5e;
        font-weight: 600;
      }

      .count {
        font-size: 9px;
        color: #94a3b8;
      }
    }
  }
}

.sentiment-hint {
  text-align: center;
  padding: 10px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 6px;
  font-size: 12px;
  color: #94a3b8;

  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}
</style>
