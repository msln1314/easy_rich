<template>
  <div class="hot-news">
    <!-- 顶部固定导航 -->
    <div class="top-nav">
      <div class="nav-content">
        <div class="logo">
          <el-icon class="logo-icon"><TrendCharts /></el-icon>
          <span class="logo-text">热门头条</span>
        </div>
        <div class="nav-actions">
          <el-button type="primary" size="small" :loading="refreshing" @click="refreshAll">
            <el-icon><Refresh /></el-icon>
            刷新
          </el-button>
        </div>
      </div>
    </div>

    <!-- 主 Tab：更多、关注、最热、实时 -->
    <div class="main-tabs">
      <div class="tabs-wrapper">
        <!-- 更多按钮 -->
        <el-popover
          placement="bottom"
          :width="280"
          trigger="click"
          :visible="showMorePopover"
          @update:visible="showMorePopover = $event"
        >
          <template #reference>
            <div class="main-tab more-tab" :class="{ active: isCategoryActive }">
              <span>更多</span>
              <el-icon><ArrowDown /></el-icon>
            </div>
          </template>
          <div class="more-categories">
            <div
              v-for="cat in moreCategories"
              :key="cat.key"
              class="category-item"
              :class="{ active: activeCategory === cat.key }"
              @click="selectCategory(cat.key)"
            >
              <el-icon><component :is="cat.icon" /></el-icon>
              <span>{{ cat.label }}</span>
              <span class="category-count">{{ getCategoryCount(cat.key) }}</span>
            </div>
          </div>
        </el-popover>

        <!-- 关注 -->
        <div
          class="main-tab"
          :class="{ active: activeTab === 'focus' }"
          @click="switchTab('focus')"
        >
          <el-icon><Star /></el-icon>
          <span>关注</span>
          <span v-if="focusCount > 0" class="tab-badge">{{ focusCount }}</span>
        </div>

        <!-- 最热 -->
        <div
          class="main-tab"
          :class="{ active: activeTab === 'hottest' }"
          @click="switchTab('hottest')"
        >
          <el-icon><Flag /></el-icon>
          <span>最热</span>
          <span class="tab-count">{{ getCategoryCount('hottest') }}</span>
        </div>

        <!-- 实时 -->
        <div
          class="main-tab"
          :class="{ active: activeTab === 'realtime' }"
          @click="switchTab('realtime')"
        >
          <el-icon><Lightning /></el-icon>
          <span>实时</span>
          <span class="tab-count">{{ getCategoryCount('realtime') }}</span>
        </div>
      </div>
    </div>

    <!-- 内容区域：多卡片 Grid 布局 -->
    <div class="content-area">
      <div class="cards-grid">
        <div
          v-for="source in currentSources"
          :key="source.id"
          class="source-card"
          :style="{ backgroundColor: getColorValue(source.color, 0.1) }"
        >
          <div class="card-header">
            <div class="header-left">
              <div class="source-avatar" :style="{ backgroundColor: getColorValue(source.color) }">
                {{ source.name.charAt(0) }}
              </div>
              <div class="source-info">
                <div class="source-title">
                  {{ source.name }}
                  <span v-if="source.title" class="source-subtitle">{{ source.title }}</span>
                </div>
                <div class="update-info">
                  <el-icon v-if="loadingMap[source.id]" class="is-loading"><Loading /></el-icon>
                  <span v-else>{{ getUpdateTimeText(sourcesData[source.id]) }}</span>
                </div>
              </div>
            </div>
            <div class="header-actions">
              <el-icon
                class="focus-icon"
                :class="{ focused: isFocused(source.id) }"
                @click.stop="toggleFocus(source.id)"
              >
                <StarFilled v-if="isFocused(source.id)" />
                <Star v-else />
              </el-icon>
              <el-button
                :loading="loadingMap[source.id]"
                circle
                size="small"
                @click="refreshSource(source.id)"
              >
                <el-icon><Refresh /></el-icon>
              </el-button>
            </div>
          </div>

          <!-- 新闻列表 -->
          <div class="news-list" :class="{ realtime: source.type === 'realtime' }">
            <div v-if="getSourceItems(source.id).length > 0">
              <!-- 实时列表样式 -->
              <template v-if="source.type === 'realtime'">
                <a
                  v-for="item in getSourceItems(source.id)"
                  :key="item.id"
                  :href="item.url"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="news-item realtime-item"
                >
                  <span v-if="item.pub_date" class="item-time">{{
                    formatTime(item.pub_date)
                  }}</span>
                  <span class="item-title">{{ item.title }}</span>
                </a>
              </template>
              <!-- 最热列表样式 -->
              <template v-else>
                <a
                  v-for="(item, index) in getSourceItems(source.id)"
                  :key="item.id"
                  :href="item.url"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="news-item hottest-item"
                >
                  <span class="item-rank" :class="getRankClass(index + 1)">{{ index + 1 }}</span>
                  <div class="item-content">
                    <span class="item-title">{{ item.title }}</span>
                    <span v-if="item.extra && item.extra.info" class="item-info">{{
                      item.extra.info
                    }}</span>
                  </div>
                </a>
              </template>
            </div>
            <div v-else-if="getServerError(source.id)" class="empty-state small">
              <el-icon :size="32"><WarningFilled /></el-icon>
              <p>{{ getServerError(source.id) }}</p>
            </div>
            <div v-else class="empty-state small">
              <el-icon :size="32" class="is-loading"><Loading /></el-icon>
              <p>加载中...</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 空状态：关注 -->
      <div v-if="activeTab === 'focus' && currentSources.length === 0" class="empty-focus">
        <el-icon :size="64"><Star /></el-icon>
        <h3>还没有关注任何数据源</h3>
        <p>点击数据源卡片右上角的 ⭐ 图标添加关注</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import {
  TrendCharts,
  Refresh,
  Loading,
  WarningFilled,
  ChromeFilled,
  Monitor,
  Star,
  StarFilled,
  ArrowDown,
  Flag,
  Lightning
} from '@element-plus/icons-vue'
import { getHotNewsSourcesApi, getHotNewsApi } from '/@/api/stock/hotNews'

interface NewsItem {
  id: string
  title: string
  url: string
  pub_date?: number
  extra?: {
    hover?: string
    info?: string
  }
}

interface SourceData {
  status: string
  source_id: string
  source_name: string
  updated_time: number
  items: NewsItem[]
  message?: string
}

interface NewsSource {
  id: string
  name: string
  title: string
  color: string
  type: string
  column: string
  available: boolean
}

// 分类定义
const moreCategories = [
  { key: 'finance', label: '财经', icon: TrendCharts },
  { key: 'china', label: '国内', icon: ChromeFilled },
  { key: 'tech', label: '科技', icon: Monitor }
]

// 数据
const activeTab = ref('hottest')
const activeCategory = ref('')
const activeSourceId = ref('')
const allSources = ref<NewsSource[]>([])
const sourcesData = reactive<Record<string, SourceData>>({})
const loadingMap = reactive<Record<string, boolean>>({})
const refreshing = ref(false)
const showMorePopover = ref(false)
const focusSources = ref<string[]>([])

// 从 localStorage 加载关注列表
const FOCUS_KEY = 'hot_news_focus_sources'
function loadFocusSources() {
  try {
    const saved = localStorage.getItem(FOCUS_KEY)
    if (saved) {
      focusSources.value = JSON.parse(saved)
    }
  } catch (e) {
    console.error('加载关注列表失败:', e)
  }
}

function saveFocusSources() {
  try {
    localStorage.setItem(FOCUS_KEY, JSON.stringify(focusSources.value))
  } catch (e) {
    console.error('保存关注列表失败:', e)
  }
}

function isFocused(sourceId: string): boolean {
  return focusSources.value.includes(sourceId)
}

function toggleFocus(sourceId: string) {
  const index = focusSources.value.indexOf(sourceId)
  if (index > -1) {
    focusSources.value.splice(index, 1)
    ElMessage.success('已取消关注')
  } else {
    focusSources.value.push(sourceId)
    ElMessage.success('已添加关注')
  }
  saveFocusSources()
}

const focusCount = computed(() => focusSources.value.length)

const isCategoryActive = computed(() => {
  return activeCategory.value && ['finance', 'china', 'tech'].includes(activeCategory.value)
})

// 当前显示的数据源
const currentSources = computed(() => {
  // 如果选择了分类（更多菜单）
  if (activeCategory.value) {
    return allSources.value.filter((s) => s.column === activeCategory.value)
  }
  // 关注 Tab
  if (activeTab.value === 'focus') {
    return allSources.value.filter((s) => focusSources.value.includes(s.id))
  }
  // 最热 Tab
  if (activeTab.value === 'hottest') {
    return allSources.value.filter((s) => s.type === 'hottest')
  }
  // 实时 Tab
  if (activeTab.value === 'realtime') {
    return allSources.value.filter((s) => s.type === 'realtime')
  }
  return []
})

// 当前选中的数据源
const currentSource = computed(() => {
  return allSources.value.find((s) => s.id === activeSourceId.value)
})

// 当前数据源的数据
const currentSourceData = computed(() => {
  if (!activeSourceId.value) return null
  return sourcesData[activeSourceId.value] || null
})

// 当前数据源的新闻条目
const currentSourceItems = computed(() => {
  const data = currentSourceData.value
  if (data && data.items && data.items.length > 0) {
    return data.items
  }
  return []
})

// 当前数据源的错误信息
const currentSourceError = computed(() => {
  const data = currentSourceData.value
  if (data && data.status === 'error') {
    return data.message || '加载失败'
  }
  return ''
})

// 颜色映射
const colorMap: Record<string, string> = {
  blue: '#409eff',
  red: '#f56c6c',
  green: '#67c23a',
  orange: '#e6a23c',
  gray: '#909399',
  indigo: '#5470c6',
  emerald: '#10b981',
  teal: '#14b8a6',
  slate: '#64748b',
  yellow: '#fbbf24'
}

function getColorValue(color: string, opacity?: number): string {
  const hex = colorMap[color] || '#409eff'
  if (opacity !== undefined) {
    const r = parseInt(hex.slice(1, 3), 16)
    const g = parseInt(hex.slice(3, 5), 16)
    const b = parseInt(hex.slice(5, 7), 16)
    return `rgba(${r}, ${g}, ${b}, ${opacity})`
  }
  return hex
}

function getCategoryCount(category: string): number {
  if (category === 'hottest') {
    return allSources.value.filter((s) => s.type === 'hottest').length
  }
  if (category === 'realtime') {
    return allSources.value.filter((s) => s.type === 'realtime').length
  }
  return allSources.value.filter((s) => s.column === category).length
}

function formatTime(timestamp: number): string {
  if (!timestamp) return ''
  const date = new Date(timestamp)
  return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}

function getUpdateTimeText(data: SourceData | null): string {
  if (!data) return '加载中...'
  if (data.status === 'error') return '获取失败'
  if (!data.updated_time) return '加载中...'

  const date = new Date(data.updated_time * 1000)
  const now = new Date()
  const diff = now.getTime() - date.getTime()

  if (diff < 60000) return '刚刚更新'
  if (diff < 3600000) return Math.floor(diff / 60000) + '分钟前'
  return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}

function getRankClass(rank: number): string {
  if (rank === 1) return 'rank-1'
  if (rank === 2) return 'rank-2'
  if (rank === 3) return 'rank-3'
  return ''
}

// 获取指定数据源的新闻条目
function getSourceItems(sourceId: string): NewsItem[] {
  const data = sourcesData[sourceId]
  if (data && data.items && data.items.length > 0) {
    return data.items
  }
  return []
}

// 获取服务器错误信息
function getServerError(sourceId: string): string {
  const data = sourcesData[sourceId]
  if (data && data.status === 'error') {
    return data.message || '加载失败'
  }
  return ''
}

// 切换主 Tab
function switchTab(tab: string) {
  activeTab.value = tab
  activeCategory.value = ''
  showMorePopover.value = false
  // 切换后选中第一个数据源
  selectFirstSource()
}

// 选择更多分类
function selectCategory(category: string) {
  activeCategory.value = category
  activeTab.value = ''
  showMorePopover.value = false
  // 切换后选中第一个数据源
  selectFirstSource()
}

// 选中第一个数据源
function selectFirstSource() {
  if (currentSources.value.length > 0) {
    activeSourceId.value = currentSources.value[0].id
    // 加载数据
    loadCurrentSources()
  } else {
    activeSourceId.value = ''
  }
}

// 切换数据源
function switchSource(sourceId: string) {
  activeSourceId.value = sourceId
  // 如果该数据源还没加载，立即加载
  if (!sourcesData[sourceId]) {
    loadSourceData(sourceId)
  }
}

// 加载单个数据源
async function loadSourceData(sourceId: string) {
  loadingMap[sourceId] = true
  try {
    const res = await getHotNewsApi(sourceId)
    if (res.data) {
      sourcesData[sourceId] = res.data
    }
  } catch (error) {
    console.error(`获取 ${sourceId} 失败:`, error)
    sourcesData[sourceId] = {
      status: 'error',
      source_id: sourceId,
      source_name: sourceId,
      updated_time: Math.floor(Date.now() / 1000),
      items: [],
      message: '获取失败'
    }
  } finally {
    loadingMap[sourceId] = false
  }
}

// 分批并发加载数据源
function loadCurrentSources() {
  const sourceIds = currentSources.value.map((s) => s.id)
  const batchSize = 5

  for (let i = 0; i < sourceIds.length; i += batchSize) {
    const batch = sourceIds.slice(i, i + batchSize)
    batch.forEach((id) => {
      if (!sourcesData[id]) {
        loadSourceData(id)
      }
    })
  }
}

// 刷新单个数据源
async function refreshSource(sourceId: string) {
  delete sourcesData[sourceId]
  await loadSourceData(sourceId)
  ElMessage.success('刷新成功')
}

// 刷新全部
async function refreshAll() {
  refreshing.value = true
  currentSources.value.forEach((s) => {
    delete sourcesData[s.id]
  })
  const sourceIds = currentSources.value.map((s) => s.id)

  try {
    await Promise.allSettled(sourceIds.map((id) => loadSourceData(id)))
    ElMessage.success('刷新完成')
  } finally {
    refreshing.value = false
  }
}

// 初始化
onMounted(async () => {
  loadFocusSources()

  try {
    // 加载所有数据源列表
    const res = await getHotNewsSourcesApi()
    if (res.data && res.data.sources) {
      allSources.value = res.data.sources.filter((s: NewsSource) => s.available)
    }

    // 默认选中第一个最热数据源并加载数据
    selectFirstSource()
  } catch (error) {
    console.error('初始化失败:', error)
    ElMessage.error('加载数据源失败')
  }
})
</script>

<style scoped lang="scss">
.hot-news {
  min-height: 100vh;
  background: #f5f7fa;
  display: flex;
  flex-direction: column;
}

// 顶部导航
.top-nav {
  position: sticky;
  top: 0;
  z-index: 100;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  box-shadow: 0 2px 12px rgba(102, 126, 234, 0.3);

  .nav-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 12px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .logo {
    display: flex;
    align-items: center;
    gap: 10px;
    color: white;

    .logo-icon {
      font-size: 24px;
    }

    .logo-text {
      font-size: 20px;
      font-weight: 600;
    }
  }
}

// 主 Tab
.main-tabs {
  background: white;
  border-bottom: 1px solid #eee;
  position: sticky;
  top: 48px;
  z-index: 99;

  .tabs-wrapper {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    padding: 0 20px;
    gap: 4px;
  }

  .main-tab {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 14px 20px;
    cursor: pointer;
    color: #666;
    font-size: 15px;
    border-bottom: 3px solid transparent;
    transition: all 0.2s;

    &:hover {
      color: #667eea;
      background: #f8f9ff;
    }

    &.active {
      color: #667eea;
      font-weight: 600;
      border-bottom-color: #667eea;
    }

    .tab-count {
      font-size: 12px;
      background: #f0f0f0;
      padding: 1px 6px;
      border-radius: 10px;
      color: #999;
    }

    .tab-badge {
      font-size: 11px;
      background: #667eea;
      color: white;
      padding: 1px 6px;
      border-radius: 10px;
      min-width: 18px;
      text-align: center;
    }

    &.active .tab-count {
      background: #667eea;
      color: white;
    }

    &.more-tab {
      .el-icon {
        transition: transform 0.2s;
      }
    }
  }
}

// 更多分类弹窗
.more-categories {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;

  .category-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 16px 12px;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.2s;

    &:hover {
      background: #f5f7fa;
    }

    &.active {
      background: #667eea;
      color: white;

      .category-count {
        background: rgba(255, 255, 255, 0.3);
        color: white;
      }
    }

    .el-icon {
      font-size: 24px;
      margin-bottom: 6px;
    }

    span {
      font-size: 13px;
    }

    .category-count {
      font-size: 11px;
      background: #f0f0f0;
      padding: 1px 6px;
      border-radius: 10px;
      color: #999;
      margin-top: 4px;
    }
  }
}

// 数据源导航
.source-nav {
  background: white;
  border-bottom: 1px solid #eee;
  overflow-x: auto;
  position: sticky;
  top: 97px;
  z-index: 98;

  &::-webkit-scrollbar {
    display: none;
  }

  .source-tabs {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    padding: 10px 20px;
    gap: 8px;
  }

  .source-tab {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 8px 14px;
    background: #f5f7fa;
    border-radius: 20px;
    cursor: pointer;
    white-space: nowrap;
    transition: all 0.2s;

    &:hover {
      background: #e8ecf3;
    }

    &.active {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;

      .source-badge {
        background: rgba(255, 255, 255, 0.2) !important;
        color: white !important;
      }

      .focus-icon {
        color: rgba(255, 255, 255, 0.7);

        &.focused {
          color: #ffd700;
        }
      }
    }

    .source-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
    }

    .source-name {
      font-size: 13px;
      font-weight: 500;
    }

    .source-badge {
      font-size: 10px;
      padding: 1px 5px;
      border-radius: 4px;
    }

    .focus-icon {
      font-size: 14px;
      color: #ccc;
      transition: all 0.2s;

      &:hover {
        color: #ffd700;
      }

      &.focused {
        color: #ffd700;
      }
    }
  }
}

// 内容区域
.content-area {
  flex: 1;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
  padding: 20px;
}

// 卡片 Grid 布局
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 20px;
}

// 数据源卡片
.source-card {
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  height: 520px;

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 16px;

    .header-left {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .source-avatar {
      width: 36px;
      height: 36px;
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-size: 16px;
      font-weight: 600;
    }

    .source-info {
      .source-title {
        font-size: 15px;
        font-weight: 600;
        color: #1a1a1a;
        display: flex;
        align-items: center;
        gap: 6px;
      }

      .source-subtitle {
        font-size: 11px;
        font-weight: normal;
        color: #666;
        background: rgba(0, 0, 0, 0.05);
        padding: 1px 5px;
        border-radius: 4px;
      }

      .update-info {
        font-size: 11px;
        color: #999;
        margin-top: 2px;
        display: flex;
        align-items: center;
        gap: 4px;
      }
    }

    .header-actions {
      display: flex;
      align-items: center;
      gap: 8px;

      .focus-icon {
        font-size: 18px;
        color: #ccc;
        cursor: pointer;
        transition: all 0.2s;

        &:hover {
          color: #ffd700;
        }

        &.focused {
          color: #ffd700;
        }
      }
    }
  }
}

// 新闻列表
.news-list {
  flex: 1;
  overflow-y: auto;
  background: rgba(255, 255, 255, 0.7);
  border-radius: 12px;
  margin: 0 12px 12px;

  .news-item {
    display: flex;
    align-items: flex-start;
    padding: 10px 12px;
    border-bottom: 1px solid #f5f5f5;
    text-decoration: none;
    color: inherit;
    transition: background 0.2s;

    &:hover {
      background: rgba(0, 0, 0, 0.03);
    }
  }

  // 实时样式
  .realtime-item {
    align-items: center;

    .item-time {
      flex-shrink: 0;
      width: 42px;
      font-size: 11px;
      color: #999;
      margin-right: 8px;
    }

    .item-title {
      flex: 1;
      font-size: 13px;
      line-height: 1.5;
      color: #333;
    }
  }

  // 最热样式
  .hottest-item {
    .item-rank {
      flex-shrink: 0;
      width: 20px;
      height: 20px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 11px;
      font-weight: 600;
      border-radius: 4px;
      background: #f0f0f0;
      color: #666;
      margin-right: 10px;

      &.rank-1 {
        background: linear-gradient(135deg, #ff6b6b, #ee5a5a);
        color: white;
      }

      &.rank-2 {
        background: linear-gradient(135deg, #ffa726, #ff9800);
        color: white;
      }

      &.rank-3 {
        background: linear-gradient(135deg, #ffd54f, #ffca28);
        color: white;
      }
    }

    .item-content {
      flex: 1;

      .item-title {
        font-size: 13px;
        line-height: 1.5;
        color: #333;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
      }

      .item-info {
        display: inline-block;
        font-size: 10px;
        color: #999;
        margin-top: 3px;
        padding: 1px 4px;
        background: #f5f5f5;
        border-radius: 3px;
      }
    }
  }
}

// 空状态
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: #999;

  &.small {
    padding: 40px 20px;

    p {
      font-size: 12px;
    }
  }

  p {
    margin-top: 12px;
    font-size: 14px;
  }
}

// 空关注状态
.empty-focus {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  color: #999;
  text-align: center;

  h3 {
    margin-top: 20px;
    font-size: 18px;
    color: #666;
  }

  p {
    margin-top: 8px;
    font-size: 14px;
  }
}

// 响应式
@media (max-width: 768px) {
  .main-tabs .tabs-wrapper {
    padding: 0 10px;
    overflow-x: auto;

    &::-webkit-scrollbar {
      display: none;
    }
  }

  .main-tab {
    padding: 12px 14px;
    font-size: 14px;
  }

  .content-area {
    padding: 12px;
  }

  .cards-grid {
    grid-template-columns: 1fr;
  }

  .source-card {
    height: auto;
    min-height: 400px;
  }

  .source-card .card-header {
    padding: 10px 12px;
  }

  .news-list {
    margin: 0 8px 8px;

    .news-item {
      padding: 8px 10px;
    }
  }

  .more-categories {
    grid-template-columns: repeat(3, 1fr);

    .category-item {
      padding: 12px 8px;

      .el-icon {
        font-size: 20px;
      }

      span {
        font-size: 12px;
      }
    }
  }
}
</style>
