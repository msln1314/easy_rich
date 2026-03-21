<template>
  <div class="global-index-card">
    <div class="card-header">
      <div class="header-title">
        <el-icon class="icon"><Promotion /></el-icon>
        <span>全球指数</span>
      </div>
      <el-tag type="info" size="small" effect="dark">延迟</el-tag>
    </div>

    <div class="card-content" v-loading="loading">
      <div class="region-section" v-for="region in regions" :key="region.name">
        <div class="region-title">{{ region.name }}</div>
        <div class="index-grid">
          <div v-for="idx in region.indices" :key="idx.index_code" class="index-item">
            <div class="index-name">{{ getIndexShortName(idx.index_name) }}</div>
            <div class="index-price">{{ formatPrice(idx.price) }}</div>
            <div class="index-change" :class="getChangeClass(idx.change_percent)">
              {{ formatChange(idx.change_percent) }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Promotion } from '@element-plus/icons-vue'
import { getGlobalIndicesApi } from '/@/api/stock/stockIndex'
import type { GlobalIndexItem } from '/@/api/stock/stockIndex'

const loading = ref(false)
const allIndices = ref<GlobalIndexItem[]>([])

const regions = computed(() => {
  const usNames = ['道琼斯', '纳斯达克', '标普500', 'DJI', 'NASDAQ', 'S&P']
  const asiaNames = ['日经', '恒生', '韩国', 'Nikkei', 'Hang Seng', 'KOSPI']
  const euNames = ['富时', 'DAX', 'CAC', 'FTSE', '英国', '德国', '法国']

  const usIndices = allIndices.value
    .filter((i) => usNames.some((n) => i.index_name?.includes(n)))
    .slice(0, 3)
  const asiaIndices = allIndices.value
    .filter((i) => asiaNames.some((n) => i.index_name?.includes(n)))
    .slice(0, 3)
  const euIndices = allIndices.value
    .filter((i) => euNames.some((n) => i.index_name?.includes(n)))
    .slice(0, 3)

  return [
    { name: '美股', indices: usIndices.length > 0 ? usIndices : getDefaultUS() },
    { name: '亚太', indices: asiaIndices.length > 0 ? asiaIndices : getDefaultAsia() },
    { name: '欧洲', indices: euIndices.length > 0 ? euIndices : getDefaultEU() }
  ]
})

function getDefaultUS() {
  return [
    {
      index_code: 'DJI',
      index_name: '道琼斯',
      price: null,
      change: null,
      change_percent: null,
      update_time: ''
    },
    {
      index_code: 'IXIC',
      index_name: '纳斯达克',
      price: null,
      change: null,
      change_percent: null,
      update_time: ''
    },
    {
      index_code: 'SPX',
      index_name: '标普500',
      price: null,
      change: null,
      change_percent: null,
      update_time: ''
    }
  ]
}

function getDefaultAsia() {
  return [
    {
      index_code: 'N225',
      index_name: '日经225',
      price: null,
      change: null,
      change_percent: null,
      update_time: ''
    },
    {
      index_code: 'HSI',
      index_name: '恒生指数',
      price: null,
      change: null,
      change_percent: null,
      update_time: ''
    },
    {
      index_code: 'KS11',
      index_name: '韩国综指',
      price: null,
      change: null,
      change_percent: null,
      update_time: ''
    }
  ]
}

function getDefaultEU() {
  return [
    {
      index_code: 'FTSE',
      index_name: '英国富时',
      price: null,
      change: null,
      change_percent: null,
      update_time: ''
    },
    {
      index_code: 'DAX',
      index_name: '德国DAX',
      price: null,
      change: null,
      change_percent: null,
      update_time: ''
    },
    {
      index_code: 'CAC',
      index_name: '法国CAC',
      price: null,
      change: null,
      change_percent: null,
      update_time: ''
    }
  ]
}

function getIndexShortName(name: string): string {
  if (!name) return '-'
  const shortNames: Record<string, string> = {
    道琼斯: '道指',
    纳斯达克: '纳指',
    标普500: '标普',
    日经225: '日经',
    恒生指数: '恒指',
    韩国综指: '韩综',
    英国富时: '富时',
    法国CAC: 'CAC'
  }
  return shortNames[name] || name.slice(0, 4)
}

function formatPrice(price: number | null | undefined): string {
  if (price === null || price === undefined) return '-'
  return price.toFixed(2)
}

function formatChange(value: number | null | undefined): string {
  if (value === null || value === undefined) return '-'
  const prefix = value > 0 ? '+' : ''
  return prefix + value.toFixed(2) + '%'
}

function getChangeClass(value: number | null | undefined): string {
  if (value === null || value === undefined || value === 0) return ''
  return value > 0 ? 'up' : 'down'
}

async function fetchData() {
  loading.value = true
  try {
    const res = await getGlobalIndicesApi()
    if (res.data && res.data.data) {
      allIndices.value = res.data.data
    }
  } catch (error) {
    console.error('获取全球指数失败:', error)
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
.global-index-card {
  background: linear-gradient(145deg, #151c2c 0%, #1a2234 100%);
  border-radius: 12px;
  padding: 14px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;

  .header-title {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 14px;
    font-weight: 600;
    color: #fff;

    .icon {
      color: #3b82f6;
    }
  }
}

.region-section {
  margin-bottom: 10px;

  &:last-child {
    margin-bottom: 0;
  }

  .region-title {
    font-size: 11px;
    color: #64748b;
    margin-bottom: 6px;
    padding-left: 2px;
  }

  .index-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 6px;
  }
}

.index-item {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 6px;
  padding: 8px;
  text-align: center;

  .index-name {
    font-size: 10px;
    color: #94a3b8;
    margin-bottom: 4px;
  }

  .index-price {
    font-size: 13px;
    font-weight: 600;
    color: #fff;
    font-family: 'DIN Alternate', sans-serif;
  }

  .index-change {
    font-size: 10px;
    font-weight: 500;
    margin-top: 2px;

    &.up {
      color: #f43f5e;
    }

    &.down {
      color: #22c55e;
    }
  }
}
</style>
