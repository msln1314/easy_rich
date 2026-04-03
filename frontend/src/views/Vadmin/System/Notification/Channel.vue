<template>
  <div class="notification-channel">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>通知渠道配置</span>
          <el-button type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>
            添加渠道
          </el-button>
        </div>
      </template>

      <el-table :data="channels" v-loading="loading">
        <el-table-column prop="channel_name" label="渠道名称" />
        <el-table-column prop="channel_type" label="渠道类型" width="120">
          <template #default="{ row }">
            <el-tag :type="getChannelTagType(row.channel_type)">
              {{ getChannelTypeName(row.channel_type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="配置信息">
          <template #default="{ row }">
            <span v-if="row.channel_type === 'email'">
              {{ row.channel_config?.address || '-' }}
            </span>
            <span v-else-if="row.channel_type === 'wechat'">
              {{ row.channel_config?.push_type || '-' }}
            </span>
            <span v-else>系统通知</span>
          </template>
        </el-table-column>
        <el-table-column prop="verified" label="验证状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.verified ? 'success' : 'warning'">
              {{ row.verified ? '已验证' : '未验证' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="is_enabled" label="状态" width="80">
          <template #default="{ row }">
            <el-switch v-model="row.is_enabled" @change="handleStatusChange(row)" />
          </template>
        </el-table-column>
        <el-table-column label="操作" width="240">
          <template #default="{ row }">
            <el-button
              v-if="!row.verified"
              type="primary"
              link
              @click="handleVerify(row)"
            >
              验证
            </el-button>
            <el-button type="primary" link @click="handleTest(row)">测试</el-button>
            <el-button type="primary" link @click="handleEdit(row)">编辑</el-button>
            <el-button type="danger" link @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 添加/编辑对话框 -->
    <el-dialog v-model="dialogVisible" :title="editingChannel ? '编辑渠道' : '添加渠道'" width="500px">
      <el-form ref="formRef" :model="formData" :rules="formRules" label-width="100px">
        <el-form-item label="渠道类型" prop="channel_type">
          <el-select
            v-model="formData.channel_type"
            placeholder="选择渠道类型"
            :disabled="!!editingChannel"
            @change="handleChannelTypeChange"
          >
            <el-option
              v-for="item in CHANNEL_TYPE_OPTIONS"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="渠道名称" prop="channel_name">
          <el-input v-model="formData.channel_name" placeholder="如: 工作邮箱" />
        </el-form-item>

        <!-- 邮箱配置 -->
        <template v-if="formData.channel_type === 'email'">
          <el-form-item label="邮箱地址" prop="channel_config.address">
            <el-input v-model="formData.channel_config.address" placeholder="user@example.com" />
          </el-form-item>
        </template>

        <!-- 微信推送配置 -->
        <template v-if="formData.channel_type === 'wechat'">
          <el-form-item label="推送类型" prop="channel_config.push_type">
            <el-select v-model="formData.channel_config.push_type" placeholder="选择推送服务">
              <el-option label="Server酱" value="serverchan" />
              <el-option label="WxPusher" value="wxpusher" />
              <el-option label="自定义" value="custom" />
            </el-select>
          </el-form-item>

          <el-form-item
            v-if="formData.channel_config.push_type === 'serverchan'"
            label="SendKey"
            prop="channel_config.sendkey"
          >
            <el-input v-model="formData.channel_config.sendkey" placeholder="Server酱 SendKey" />
          </el-form-item>

          <template v-if="formData.channel_config.push_type === 'wxpusher'">
            <el-form-item label="Token" prop="channel_config.token">
              <el-input v-model="formData.channel_config.token" placeholder="WxPusher AppToken" />
            </el-form-item>
            <el-form-item label="UID" prop="channel_config.uid">
              <el-input v-model="formData.channel_config.uid" placeholder="用户UID" />
            </el-form-item>
          </template>

          <el-form-item
            v-if="formData.channel_config.push_type === 'custom'"
            label="推送URL"
            prop="channel_config.url"
          >
            <el-input v-model="formData.channel_config.url" placeholder="自定义推送URL" />
          </el-form-item>
        </template>
      </el-form>

      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <!-- 验证对话框 -->
    <el-dialog v-model="verifyDialogVisible" title="验证渠道" width="400px">
      <el-form :model="verifyForm" label-width="100px">
        <el-form-item label="验证码">
          <div style="display: flex; gap: 10px;">
            <el-input v-model="verifyForm.code" placeholder="请输入验证码" />
            <el-button @click="sendCode" :loading="sendingCode">
              {{ codeCountdown > 0 ? `${codeCountdown}s` : '发送验证码' }}
            </el-button>
          </div>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="verifyDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitVerify">验证</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import {
  getChannelList,
  createChannel,
  updateChannel,
  deleteChannel,
  testChannel,
  sendVerifyCode,
  verifyChannel,
  CHANNEL_TYPE_OPTIONS,
  type ChannelItem,
  type ChannelForm
} from '@/api/notification'

const loading = ref(false)
const channels = ref<ChannelItem[]>([])
const dialogVisible = ref(false)
const verifyDialogVisible = ref(false)
const editingChannel = ref<ChannelItem | null>(null)
const verifyingChannel = ref<ChannelItem | null>(null)
const sendingCode = ref(false)
const codeCountdown = ref(0)

const formRef = ref()
const formData = reactive<ChannelForm & { channel_config: any }>({
  channel_type: '',
  channel_name: '',
  channel_config: {}
})

const verifyForm = reactive({
  code: ''
})

const formRules = {
  channel_type: [{ required: true, message: '请选择渠道类型', trigger: 'change' }],
  channel_name: [{ required: true, message: '请输入渠道名称', trigger: 'blur' }],
  'channel_config.address': [{ required: true, message: '请输入邮箱地址', trigger: 'blur' }]
}

function getChannelTypeName(type: string) {
  const option = CHANNEL_TYPE_OPTIONS.find(o => o.value === type)
  return option?.label || type
}

function getChannelTagType(type: string) {
  const typeMap: Record<string, string> = {
    email: 'primary',
    wechat: 'success',
    system: 'info'
  }
  return typeMap[type] || 'info'
}

async function loadChannels() {
  loading.value = true
  try {
    const { data } = await getChannelList()
    channels.value = data.data || []
  } catch (error) {
    console.error('加载渠道失败:', error)
  } finally {
    loading.value = false
  }
}

function handleAdd() {
  editingChannel.value = null
  formData.channel_type = ''
  formData.channel_name = ''
  formData.channel_config = {}
  dialogVisible.value = true
}

function handleEdit(row: ChannelItem) {
  editingChannel.value = row
  formData.channel_type = row.channel_type
  formData.channel_name = row.channel_name
  formData.channel_config = { ...row.channel_config }
  dialogVisible.value = true
}

function handleChannelTypeChange() {
  // 重置配置
  if (formData.channel_type === 'email') {
    formData.channel_config = { address: '' }
  } else if (formData.channel_type === 'wechat') {
    formData.channel_config = { push_type: 'serverchan', sendkey: '' }
  } else {
    formData.channel_config = {}
  }
}

async function handleSubmit() {
  await formRef.value?.validate()

  try {
    if (editingChannel.value) {
      await updateChannel(editingChannel.value.id, {
        channel_name: formData.channel_name,
        channel_config: formData.channel_config
      })
      ElMessage.success('更新成功')
    } else {
      await createChannel(formData)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    loadChannels()
  } catch (error: any) {
    ElMessage.error(error.message || '操作失败')
  }
}

async function handleStatusChange(row: ChannelItem) {
  try {
    await updateChannel(row.id, { is_enabled: row.is_enabled })
    ElMessage.success('状态更新成功')
  } catch (error: any) {
    row.is_enabled = !row.is_enabled
    ElMessage.error(error.message || '更新失败')
  }
}

async function handleTest(row: ChannelItem) {
  try {
    const { data } = await testChannel(row.id)
    if (data.code === 20000) {
      ElMessage.success('测试发送成功')
    } else {
      ElMessage.error(data.message || '测试发送失败')
    }
  } catch (error: any) {
    ElMessage.error(error.message || '测试发送失败')
  }
}

function handleVerify(row: ChannelItem) {
  verifyingChannel.value = row
  verifyForm.code = ''
  verifyDialogVisible.value = true
}

async function sendCode() {
  if (!verifyingChannel.value) return

  sendingCode.value = true
  try {
    const { data } = await sendVerifyCode(verifyingChannel.value.id)
    if (data.code === 20000) {
      ElMessage.success('验证码已发送')
      codeCountdown.value = 60
      const timer = setInterval(() => {
        codeCountdown.value--
        if (codeCountdown.value <= 0) {
          clearInterval(timer)
        }
      }, 1000)
    } else {
      ElMessage.error(data.message || '发送失败')
    }
  } catch (error: any) {
    ElMessage.error(error.message || '发送失败')
  } finally {
    sendingCode.value = false
  }
}

async function submitVerify() {
  if (!verifyingChannel.value || !verifyForm.code) {
    ElMessage.warning('请输入验证码')
    return
  }

  try {
    const { data } = await verifyChannel(verifyingChannel.value.id, verifyForm.code)
    if (data.code === 20000) {
      ElMessage.success('验证成功')
      verifyDialogVisible.value = false
      loadChannels()
    } else {
      ElMessage.error(data.message || '验证失败')
    }
  } catch (error: any) {
    ElMessage.error(error.message || '验证失败')
  }
}

async function handleDelete(row: ChannelItem) {
  try {
    await ElMessageBox.confirm('确定要删除此通知渠道吗？', '提示', { type: 'warning' })
    await deleteChannel(row.id)
    ElMessage.success('删除成功')
    loadChannels()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '删除失败')
    }
  }
}

onMounted(() => {
  loadChannels()
})
</script>

<style scoped lang="scss">
.notification-channel {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
}
</style>