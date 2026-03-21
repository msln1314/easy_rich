<template>
  <div class="sector-hot-card">
    <div class="card-header">
      <div class="header-title">
        <el-icon class="icon"><TrendCharts /></el-icon>
        <span>板块热度</span>
      </div>
      <div class="header-tabs">
        <span
          class="tab"
          :class="{ active: sectorType === 'industry' }"
          @click="switchSector('industry')"
          >行业</span
        >
        <span
          class="tab"
          :class="{ active: sectorType === 'concept' }"
          @click="switchSector('concept')"
          >概念</span
        >
      </div>
    </div>

    <div class="card-content" v-loading="loading">
      <div class="sector-list">
        <div v-for="(item, idx) in sectors" :key="item.board_code || idx" class="sector-item">
          <div class="rank" :class="getRankClass(idx + 1)">{{ idx + 1 }}</div>
          <div class="sector-info">
            <span class="name">{{ item.board_name || item.name }}</span>
          </div>
          <div class="sector-data">
            <span class="change" :class="item.change_percent >= 0 ? 'up' : 'down'">
              {{ formatChange(item.change_percent) }}
            </span>
            <div class="up-down">
              <span class="up">{{ item.up_count || 0 }}</span>
              <span class="divider">/</span>
              <span class="down">{{ item.down_count || 0 }}</span>
            </div>
          </div>
        </div>
        <div v-if="sectors.length === 0 && !loading" class="empty-text"> 暂无板块数据 </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { TrendCharts } from '@element-plus/icons-vue'
import { getSectorHotApi } from '/@/api/stock/stockIndex'
import type { SectorHotItem } from '/@/api/stock/stockIndex'

const loading = ref(false)
const sectorType = ref<'industry' | 'concept'>('industry')
const sectors = ref<SectorHotItem[]>([])

function formatChange(value: number | null | undefined): string {
  if (value === null || value === undefined) return '-'
  const prefix = value > 0 ? '+' : ''
  return `${prefix}${value.toFixed(2)}%`
}

function getRankClass(rank: number): string {
  if (rank === 1) return 'gold'
  if (rank === 2) return 'silver'
  if (rank === 3) return 'bronze'
  return ''
}

async function fetchData() {
  loading.value = true
  try {
    const res = await getSectorHotApi(sectorType.value, 10)
    if (res.data && res.data.sectors) {
      sectors.value = res.data.sectors
    }
  } catch (error) {
    console.error('获取板块数据失败:', error)
  } finally {
    loading.value = false
  }
}

function switchSector(type: 'industry' | 'concept') {
  sectorType.value = type
  fetchData()
}

onMounted(() => {
  fetchData()
})

defineExpose({
  refresh: fetchData
})
</script>

<style scoped lang="scss">
.sector-hot-card {
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
  margin-bottom: 12px;

  .header-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 15px;
    font-weight: 600;
    color: #fff;

    .icon {
      color: #3b82f6;
    }
  }

  .header-tabs {
    display: flex;
    gap: 8px;

    .tab {
      padding: 4px 12px;
      border-radius: 12px;
      font-size: 12px;
      cursor: pointer;
      background: rgba(255, 255, 255, 0.05);
      color: #94a3b8;
      transition: all 0.2s;

      &:hover {
        background: rgba(255, 255, 255, 0.1);
      }

      &.active {
        background: rgba(59, 130, 246, 0.2);
        color: #3b82f6;
      }
    }
  }
}

.sector-list {
  max-height: 280px;
  overflow-y: auto;

  .sector-item {
    display: flex;
    align-items: center;
    padding: 8px;
    border-radius: 6px;
    transition: background 0.2s;

    &:hover {
      background: rgba(255, 255, 255, 0.03);
    }

    .rank {
      width: 22px;
      height: 22px;
      border-radius: 4px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 12px;
      font-weight: 600;
      background: rgba(255, 255, 255, 0.05);
      color: #94a3b8;
      margin-right: 10px;

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

    .sector-info {
      flex: 1;
      min-width: 0;

      .name {
        font-size: 13px;
        font-weight: 500;
        color: #fff;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }
    }

    .sector-data {
      display: flex;
      align-items: center;
      gap: 12px;

      .change {
        font-size: 13px;
        font-weight: 500;
        min-width: 65px;
        text-align: right;

        &.up {
          color: #f43f5e;
        }
        &.down {
          color: #22c55e;
        }
      }

      .up-down {
        font-size: 11px;
        min-width: 50px;
        text-align: right;

        .up {
          color: #f43f5e;
        }
        .down {
          color: #22c55e;
        }
        .divider {
          color: #64748b;
          margin: 0 2px;
        }
      }
    }
  }

  .empty-text {
    text-align: center;
    color: #64748b;
    padding: 40px 0;
    font-size: 13px;
  }
}
</style>
