<template>
  <div class="notification-rule-form">
    <el-form ref="formRef" :model="formData" :rules="formRules" label-width="120px">
      <el-form-item label="规则名称" prop="rule_name">
        <el-input v-model="formData.rule_name" placeholder="如: 节前空仓提醒" />
      </el-form-item>

      <el-form-item label="规则类型" prop="rule_type">
        <el-select v-model="formData.rule_type" placeholder="选择规则类型" @change="handleRuleTypeChange">
          <el-option
            v-for="item in RULE_TYPE_OPTIONS"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          >
            <div>
              <span>{{ item.label }}</span>
              <span style="color: #999; font-size: 12px; margin-left: 10px;">{{ item.description }}</span>
            </div>
          </el-option>
        </el-select>
      </el-form-item>

      <el-form-item label="提前天数" prop="condition_config.days_before">
        <el-input-number v-model="formData.condition_config.days_before" :min="1" :max="30" />
        <span style="margin-left: 10px; color: #999;">天时提醒</span>
      </el-form-item>

      <el-form-item label="仅自选股" prop="condition_config.watchlist_only">
        <el-switch v-model="formData.condition_config.watchlist_only" />
        <span style="margin-left: 10px; color: #999;">仅提醒自选股相关事件</span>
      </el-form-item>

      <el-form-item label="指定股票">
        <el-select
          v-model="formData.stock_codes"
          multiple
          filterable
          remote
          :remote-method="searchStock"
          placeholder="输入股票代码或名称搜索（可选）"
        >
          <el-option
            v-for="item in stockOptions"
            :key="item.code"
            :label="`${item.name} (${item.code})`"
            :value="item.code"
          />
        </el-select>
      </el-form-item>

      <el-form-item label="提醒消息" prop="action_config.message">
        <el-input
          v-model="formData.action_config.message"
          type="textarea"
          :rows="2"
          placeholder="自定义提醒消息"
        />
      </el-form-item>

      <el-form-item label="通知渠道" prop="action_config.channels">
        <el-checkbox-group v-model="formData.action_config.channels">
          <el-checkbox label="system">系统通知</el-checkbox>
          <el-checkbox label="email">邮件</el-checkbox>
          <el-checkbox label="wechat">微信推送</el-checkbox>
        </el-checkbox-group>
      </el-form-item>

      <el-form-item label="优先级">
        <el-input-number v-model="formData.priority" :min="0" :max="100" />
        <span style="margin-left: 10px; color: #999;">数值越大优先级越高</span>
      </el-form-item>

      <el-form-item label="有效期">
        <el-date-picker
          v-model="dateRange"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
          @change="handleDateRangeChange"
        />
      </el-form-item>

      <el-form-item label="启用状态">
        <el-switch v-model="formData.is_enabled" />
      </el-form-item>
    </el-form>

    <div class="form-footer">
      <el-button @click="handleCancel">取消</el-button>
      <el-button type="primary" @click="handleSubmit" :loading="submitting">确定</el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, watch, computed } from 'vue'
import { ElMessage } from 'element-plus'
import {
  createNotificationRule,
  updateNotificationRule,
  RULE_TYPE_OPTIONS,
  type NotificationRuleForm,
  type NotificationRuleItem
} from '@/api/notification'

const props = defineProps<{
  editingRule?: NotificationRuleItem | null
}>()

const emit = defineEmits<{
  (e: 'success'): void
  (e: 'cancel'): void
}>()

const formRef = ref()
const submitting = ref(false)
const stockOptions = ref<{ code: string; name: string }[]>([])
const dateRange = ref<string[]>([])

const formData = reactive<NotificationRuleForm & { is_enabled?: boolean }>({
  rule_name: '',
  rule_type: 'holiday',
  condition_config: {
    days_before: 2,
    watchlist_only: true
  },
  action_config: {
    message: '',
    channels: ['system']
  },
  stock_codes: [],
  priority: 0,
  is_enabled: true
})

const formRules = {
  rule_name: [{ required: true, message: '请输入规则名称', trigger: 'blur' }],
  rule_type: [{ required: true, message: '请选择规则类型', trigger: 'change' }]
}

// 默认消息模板
const defaultMessages: Record<string, string> = {
  holiday: '节假日即将到来，建议提前调整仓位',
  earnings: '以下股票即将发布财报，请注意关注',
  dividend: '以下股票即将分红除权，请注意股权登记日',
  unlock: '以下股票即将解禁，注意风险'
}

function handleRuleTypeChange() {
  // 设置默认消息
  if (!formData.action_config.message) {
    formData.action_config.message = defaultMessages[formData.rule_type] || ''
  }
}

function handleDateRangeChange() {
  if (dateRange.value && dateRange.value.length === 2) {
    formData.valid_from = dateRange.value[0]
    formData.valid_to = dateRange.value[1]
  } else {
    formData.valid_from = undefined
    formData.valid_to = undefined
  }
}

async function searchStock(query: string) {
  if (!query) {
    stockOptions.value = []
    return
  }
  // 这里可以调用股票搜索 API
  // 暂时返回模拟数据
  stockOptions.value = [
    { code: '000001', name: '平安银行' },
    { code: '000002', name: '万科A' }
  ].filter(s => s.code.includes(query) || s.name.includes(query))
}

// 编辑模式初始化
watch(() => props.editingRule, (rule) => {
  if (rule) {
    formData.rule_name = rule.rule_name
    formData.rule_type = rule.rule_type as any
    formData.stock_codes = rule.stock_codes || []
    formData.condition_config = { ...rule.condition_config }
    formData.action_config = { ...rule.action_config }
    formData.priority = rule.priority
    formData.is_enabled = rule.is_enabled
    if (rule.valid_from && rule.valid_to) {
      dateRange.value = [rule.valid_from, rule.valid_to]
    }
  }
}, { immediate: true })

async function handleSubmit() {
  await formRef.value?.validate()

  submitting.value = true
  try {
    if (props.editingRule) {
      await updateNotificationRule(props.editingRule.id, formData)
      ElMessage.success('更新成功')
    } else {
      await createNotificationRule(formData)
      ElMessage.success('创建成功')
    }
    emit('success')
  } catch (error: any) {
    ElMessage.error(error.message || '操作失败')
  } finally {
    submitting.value = false
  }
}

function handleCancel() {
  emit('cancel')
}
</script>

<style scoped lang="scss">
.notification-rule-form {
  .form-footer {
    text-align: right;
    padding-top: 20px;
    border-top: 1px solid var(--el-border-color);
  }
}
</style>