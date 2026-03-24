<template>
  <div class="invest-calendar">
    <div class="calendar-header">
      <div class="header-left">
        <el-radio-group v-model="viewType" size="large">
          <el-radio-button label="month">月历</el-radio-button>
          <el-radio-button label="week">周历</el-radio-button>
          <el-radio-button label="timeline">时间线</el-radio-button>
        </el-radio-group>

        <div class="date-nav">
          <el-button @click="navigateDate(-1)" :icon="ArrowLeft" circle />
          <span class="current-date">{{ currentDateDisplay }}</span>
          <el-button @click="navigateDate(1)" :icon="ArrowRight" circle />
          <el-button @click="goToToday" type="primary" size="small">今天</el-button>
        </div>
      </div>

      <div class="header-right">
        <el-checkbox v-model="showWatchlistOnly">仅显示自选股</el-checkbox>
        <el-select
          v-model="selectedEventType"
          placeholder="事件类型"
          clearable
          style="width: 150px"
        >
          <el-option
            v-for="(info, type) in EVENT_TYPE_MAP"
            :key="type"
            :label="info.label"
            :value="type"
          />
        </el-select>
      </div>
    </div>

    <div class="calendar-content" v-loading="loading">
      <CalendarMonth
        v-if="viewType === 'month'"
        :current-date="currentDate"
        :events="events"
        @date-click="handleDateClick"
        @event-click="handleEventClick"
      />

      <div v-else-if="viewType === 'week'" class="coming-soon">
        <el-empty description="周历视图开发中..." />
      </div>

      <div v-else class="coming-soon">
        <el-empty description="时间线视图开发中..." />
      </div>
    </div>

    <el-dialog v-model="showEventDetail" :title="selectedEvent?.title" width="500px">
      <div v-if="selectedEvent" class="event-detail">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="股票"
            >{{ selectedEvent.stock_name }} ({{ selectedEvent.stock_code }})</el-descriptions-item
          >
          <el-descriptions-item label="事件类型">
            <el-tag :color="EVENT_TYPE_MAP[selectedEvent.event_type]?.color" effect="dark">
              {{ EVENT_TYPE_MAP[selectedEvent.event_type]?.label }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="日期">{{ selectedEvent.event_date }}</el-descriptions-item>
          <el-descriptions-item label="详情">{{
            selectedEvent.content || '暂无详情'
          }}</el-descriptions-item>
          <el-descriptions-item v-if="selectedEvent.ai_analysis" label="AI分析">{{
            selectedEvent.ai_analysis
          }}</el-descriptions-item>
          <el-descriptions-item v-if="selectedEvent.ai_suggestion" label="AI建议">{{
            selectedEvent.ai_suggestion
          }}</el-descriptions-item>
        </el-descriptions>
      </div>
      <template #footer>
        <el-button @click="showEventDetail = false">关闭</el-button>
        <el-button type="primary" @click="handleSetReminder">设置提醒</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { ArrowLeft, ArrowRight } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { getEventList } from '@/api/stockCalendar'
import { EVENT_TYPE_MAP } from './types/calendar'
import type { CalendarEvent } from './types/calendar'
import CalendarMonth from './components/CalendarMonth.vue'

const viewType = ref<'month' | 'week' | 'timeline'>('month')
const currentDate = ref(new Date())
const events = ref<CalendarEvent[]>([])
const loading = ref(false)
const showWatchlistOnly = ref(false)
const selectedEventType = ref('')
const selectedEvent = ref<CalendarEvent | null>(null)
const showEventDetail = ref(false)

const currentDateDisplay = computed(() => {
  const year = currentDate.value.getFullYear()
  const month = currentDate.value.getMonth() + 1
  return `${year}年${month}月`
})

function navigateDate(direction: number) {
  const newDate = new Date(currentDate.value)
  if (viewType.value === 'month') {
    newDate.setMonth(newDate.getMonth() + direction)
  } else if (viewType.value === 'week') {
    newDate.setDate(newDate.getDate() + direction * 7)
  }
  currentDate.value = newDate
}

function goToToday() {
  currentDate.value = new Date()
}

async function loadEvents() {
  loading.value = true
  try {
    const year = currentDate.value.getFullYear()
    const month = currentDate.value.getMonth() + 1
    const startDate = `${year}-${String(month).padStart(2, '0')}-01`
    const endDate = new Date(year, month, 0)
    const endDateStr = `${endDate.getFullYear()}-${String(endDate.getMonth() + 1).padStart(
      2,
      '0'
    )}-${String(endDate.getDate()).padStart(2, '0')}`

    const { data } = await getEventList({
      start_date: startDate,
      end_date: endDateStr,
      is_watchlist: showWatchlistOnly.value ? 1 : undefined,
      event_type: selectedEventType.value || undefined,
      page: 1,
      page_size: 100
    })

    events.value = data.data || []
  } catch (error) {
    console.error('加载事件失败:', error)
    ElMessage.error('加载事件失败')
  } finally {
    loading.value = false
  }
}

function handleDateClick(date: Date) {
  currentDate.value = date
  viewType.value = 'week'
}

function handleEventClick(event: CalendarEvent) {
  selectedEvent.value = event
  showEventDetail.value = true
}

function handleSetReminder() {
  ElMessage.info('提醒功能开发中...')
}

watch([showWatchlistOnly, selectedEventType, currentDate], () => {
  loadEvents()
})

onMounted(() => {
  loadEvents()
})
</script>

<style scoped lang="scss">
.invest-calendar {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: var(--el-bg-color);

  .calendar-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px;
    border-bottom: 1px solid var(--el-border-color);

    .header-left {
      display: flex;
      align-items: center;
      gap: 20px;

      .date-nav {
        display: flex;
        align-items: center;
        gap: 8px;

        .current-date {
          font-size: 16px;
          font-weight: 500;
          min-width: 120px;
          text-align: center;
        }
      }
    }

    .header-right {
      display: flex;
      align-items: center;
      gap: 12px;
    }
  }

  .calendar-content {
    flex: 1;
    overflow: auto;

    .coming-soon {
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100%;
    }
  }

  .event-detail {
    padding: 16px 0;
  }
}
</style>
