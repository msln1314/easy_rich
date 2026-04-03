<template>
  <el-dropdown trigger="click" @command="handleCommand">
    <el-badge :value="unreadCount" :hidden="unreadCount === 0" :max="99">
      <el-icon :size="20" class="bell-icon">
        <Bell />
      </el-icon>
    </el-badge>
    <template #dropdown>
      <div class="notification-dropdown">
        <div class="dropdown-header">
          <span>通知消息</span>
          <el-button v-if="unreadCount > 0" type="primary" link @click="handleReadAll">
            全部已读
          </el-button>
        </div>

        <el-scrollbar max-height="400px">
          <div v-if="loading" class="loading-container">
            <el-icon class="is-loading"><Loading /></el-icon>
          </div>

          <div v-else-if="notifications.length === 0" class="empty-container">
            <el-empty description="暂无通知" :image-size="60" />
          </div>

          <div v-else class="notification-list">
            <div
              v-for="item in notifications"
              :key="item.id"
              class="notification-item"
              :class="{ unread: !item.is_read }"
              @click="handleItemClick(item)"
            >
              <div class="item-title">{{ item.title }}</div>
              <div class="item-content">{{ item.content }}</div>
              <div class="item-time">{{ formatTime(item.created_at) }}</div>
            </div>
          </div>
        </el-scrollbar>

        <div class="dropdown-footer">
          <el-button type="primary" link @click="goToNotificationList">
            查看全部
          </el-button>
        </div>
      </div>
    </template>
  </el-dropdown>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { Bell, Loading } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import {
  getNotificationList,
  getUnreadCount,
  markAsRead,
  markAllAsRead,
  type SystemNotification
} from '@/api/notification'

const router = useRouter()
const loading = ref(false)
const notifications = ref<SystemNotification[]>([])
const unreadCount = ref(0)

let pollingInterval: ReturnType<typeof setInterval> | null = null

async function loadUnreadCount() {
  try {
    const { data } = await getUnreadCount()
    unreadCount.value = data.data?.unread_count || 0
  } catch (error) {
    console.error('加载未读数量失败:', error)
  }
}

async function loadNotifications() {
  loading.value = true
  try {
    const { data } = await getNotificationList({ page: 1, page_size: 10 })
    notifications.value = data.data?.items || []
    unreadCount.value = data.data?.unread_count || 0
  } catch (error) {
    console.error('加载通知失败:', error)
  } finally {
    loading.value = false
  }
}

async function handleItemClick(item: SystemNotification) {
  if (!item.is_read) {
    try {
      await markAsRead(item.id)
      item.is_read = true
      unreadCount.value = Math.max(0, unreadCount.value - 1)
    } catch (error) {
      console.error('标记已读失败:', error)
    }
  }

  if (item.link) {
    router.push(item.link)
  }
}

async function handleReadAll() {
  try {
    await markAllAsRead()
    notifications.value.forEach(n => n.is_read = true)
    unreadCount.value = 0
    ElMessage.success('已全部标记为已读')
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

function handleCommand(command: string) {
  if (command === 'viewAll') {
    goToNotificationList()
  }
}

function goToNotificationList() {
  // 跳转到通知列表页面（如果有的话）
  console.log('跳转到通知列表')
}

function formatTime(time: string): string {
  const date = new Date(time)
  const now = new Date()
  const diff = now.getTime() - date.getTime()

  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)

  if (minutes < 1) return '刚刚'
  if (minutes < 60) return `${minutes}分钟前`
  if (hours < 24) return `${hours}小时前`
  if (days < 30) return `${days}天前`

  return date.toLocaleDateString()
}

onMounted(() => {
  loadUnreadCount()
  loadNotifications()

  // 定时刷新未读数量
  pollingInterval = setInterval(() => {
    loadUnreadCount()
  }, 60000) // 每分钟刷新一次
})

onUnmounted(() => {
  if (pollingInterval) {
    clearInterval(pollingInterval)
  }
})
</script>

<style scoped lang="scss">
.bell-icon {
  cursor: pointer;
  color: var(--el-text-color-regular);

  &:hover {
    color: var(--el-color-primary);
  }
}

.notification-dropdown {
  width: 360px;

  .dropdown-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 16px;
    border-bottom: 1px solid var(--el-border-color);
    font-weight: 500;
  }

  .dropdown-footer {
    text-align: center;
    padding: 12px;
    border-top: 1px solid var(--el-border-color);
  }

  .loading-container,
  .empty-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 200px;
  }

  .notification-list {
    .notification-item {
      padding: 12px 16px;
      cursor: pointer;
      transition: background-color 0.2s;

      &:hover {
        background-color: var(--el-fill-color-light);
      }

      &.unread {
        background-color: var(--el-color-primary-light-9);
      }

      .item-title {
        font-weight: 500;
        margin-bottom: 4px;
      }

      .item-content {
        font-size: 13px;
        color: var(--el-text-color-secondary);
        margin-bottom: 4px;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
      }

      .item-time {
        font-size: 12px;
        color: var(--el-text-color-placeholder);
      }
    }
  }
}
</style>