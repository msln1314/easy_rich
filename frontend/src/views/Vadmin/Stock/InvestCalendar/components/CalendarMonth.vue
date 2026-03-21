<template>
  <div class="calendar-month">
    <div class="weekday-header">
      <div v-for="day in weekdays" :key="day" class="weekday-cell">{{ day }}</div>
    </div>

    <div class="date-grid">
      <div
        v-for="(cell, index) in calendarCells"
        :key="index"
        class="date-cell"
        :class="{
          'other-month': !cell.isCurrentMonth,
          'is-today': cell.isToday,
          'has-events': cell.events.length > 0
        }"
        @click="handleCellClick(cell)"
      >
        <div class="date-number">{{ cell.date }}</div>
        <div class="event-dots">
          <span
            v-for="(event, i) in cell.events.slice(0, 3)"
            :key="i"
            class="event-dot"
            :style="{ backgroundColor: getEventColor(event.event_type) }"
          ></span>
          <span v-if="cell.events.length > 3" class="more-dots">+{{ cell.events.length - 3 }}</span>
        </div>
        <div class="event-list" v-if="cell.events.length > 0">
          <div
            v-for="event in cell.events.slice(0, 2)"
            :key="event.id"
            class="event-item"
            :style="{ borderLeftColor: getEventColor(event.event_type) }"
            @click.stop="handleEventClick(event)"
          >
            <span class="event-stock">{{ event.stock_name || event.stock_code }}</span>
            <span class="event-title">{{ event.title }}</span>
          </div>
          <div v-if="cell.events.length > 2" class="more-events">
            还有 {{ cell.events.length - 2 }} 个事件
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { CalendarEvent, EventType } from '../types/calendar'
import { EVENT_TYPE_MAP } from '../types/calendar'

const props = defineProps<{
  currentDate: Date
  events: CalendarEvent[]
}>()

const emit = defineEmits<{
  (e: 'date-click', date: Date): void
  (e: 'event-click', event: CalendarEvent): void
}>()

const weekdays = ['日', '一', '二', '三', '四', '五', '六']

interface CalendarCell {
  date: number
  fullDate: Date
  isCurrentMonth: boolean
  isToday: boolean
  events: CalendarEvent[]
}

const calendarCells = computed(() => {
  const year = props.currentDate.getFullYear()
  const month = props.currentDate.getMonth()

  const firstDay = new Date(year, month, 1)
  const lastDay = new Date(year, month + 1, 0)

  const today = new Date()
  today.setHours(0, 0, 0, 0)

  const cells: CalendarCell[] = []

  const firstDayWeek = firstDay.getDay()
  for (let i = firstDayWeek - 1; i >= 0; i--) {
    const date = new Date(year, month, -i)
    cells.push({
      date: date.getDate(),
      fullDate: date,
      isCurrentMonth: false,
      isToday: date.getTime() === today.getTime(),
      events: getEventsForDate(date)
    })
  }

  for (let i = 1; i <= lastDay.getDate(); i++) {
    const date = new Date(year, month, i)
    cells.push({
      date: i,
      fullDate: date,
      isCurrentMonth: true,
      isToday: date.getTime() === today.getTime(),
      events: getEventsForDate(date)
    })
  }

  const remaining = 42 - cells.length
  for (let i = 1; i <= remaining; i++) {
    const date = new Date(year, month + 1, i)
    cells.push({
      date: i,
      fullDate: date,
      isCurrentMonth: false,
      isToday: date.getTime() === today.getTime(),
      events: getEventsForDate(date)
    })
  }

  return cells
})

function getEventsForDate(date: Date): CalendarEvent[] {
  const dateStr = formatDate(date)
  return props.events.filter((event) => event.event_date === dateStr)
}

function formatDate(date: Date): string {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

function getEventColor(type: EventType): string {
  return EVENT_TYPE_MAP[type]?.color || '#909399'
}

function handleCellClick(cell: CalendarCell) {
  emit('date-click', cell.fullDate)
}

function handleEventClick(event: CalendarEvent) {
  emit('event-click', event)
}
</script>

<style scoped lang="scss">
.calendar-month {
  height: 100%;
  display: flex;
  flex-direction: column;

  .weekday-header {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    background: var(--el-fill-color-light);
    border-bottom: 1px solid var(--el-border-color);

    .weekday-cell {
      padding: 12px;
      text-align: center;
      font-weight: 500;
      color: var(--el-text-color-secondary);
    }
  }

  .date-grid {
    flex: 1;
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    grid-template-rows: repeat(6, 1fr);

    .date-cell {
      min-height: 100px;
      padding: 8px;
      border-right: 1px solid var(--el-border-color-lighter);
      border-bottom: 1px solid var(--el-border-color-lighter);
      cursor: pointer;
      transition: background-color 0.2s;

      &:hover {
        background-color: var(--el-fill-color-light);
      }

      &.other-month {
        background-color: var(--el-fill-color-lighter);
        .date-number {
          color: var(--el-text-color-placeholder);
        }
      }

      &.is-today {
        background-color: var(--el-color-primary-light-9);
        .date-number {
          background-color: var(--el-color-primary);
          color: white;
          border-radius: 50%;
          width: 28px;
          height: 28px;
          display: flex;
          align-items: center;
          justify-content: center;
        }
      }

      .date-number {
        font-size: 14px;
        font-weight: 500;
        margin-bottom: 4px;
      }

      .event-dots {
        display: flex;
        gap: 4px;
        margin-bottom: 4px;

        .event-dot {
          width: 6px;
          height: 6px;
          border-radius: 50%;
        }

        .more-dots {
          font-size: 10px;
          color: var(--el-text-color-secondary);
        }
      }

      .event-list {
        .event-item {
          font-size: 12px;
          padding: 2px 6px;
          border-left: 3px solid;
          background: var(--el-fill-color-lighter);
          margin-bottom: 2px;
          overflow: hidden;
          cursor: pointer;

          &:hover {
            background: var(--el-fill-color);
          }

          .event-stock {
            color: var(--el-text-color-secondary);
            margin-right: 4px;
          }

          .event-title {
            color: var(--el-text-color-primary);
          }
        }

        .more-events {
          font-size: 11px;
          color: var(--el-color-primary);
          padding: 2px 6px;
        }
      }
    }
  }
}
</style>
