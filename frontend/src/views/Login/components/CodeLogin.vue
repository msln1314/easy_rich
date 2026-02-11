<script setup lang="ts">
import { ref, computed, reactive, onUnmounted } from 'vue'
import { ElForm, ElFormItem, ElInput, ElButton, ElSpace } from 'element-plus'
import { ElMessage } from 'element-plus'
import { sendCodeApi } from '@/api/login'
import { useAuthStoreWithOut } from '@/store/modules/auth'
import { UserLoginType } from '@/api/login/types'

defineOptions({ name: 'CodeLogin' })

const emit = defineEmits(['switch-module'])

const authStore = useAuthStoreWithOut()
const formRef = ref()
const loading = ref(false)
const countdown = ref(0)
const timer = ref<any>(null)

interface FormModel {
  account: string
  code: string
}

const model = reactive<FormModel>({
  account: '',
  code: ''
})

// 表单验证规则
const rules = {
  account: [
    {
      required: true,
      message: '请输入手机号或邮箱',
      trigger: 'blur'
    }
  ],
  code: [{ required: true, message: '请输入验证码', trigger: 'blur' }]
}

// 获取验证码
const getCode = async () => {
  if (!model.account) {
    ElMessage.warning('请先输入手机号或邮箱')
    return
  }

  loading.value = true
  try {
    await sendCodeApi({ username: model.account })
    ElMessage.success('验证码已发送')
    startCountdown()
  } catch (e: any) {
    ElMessage.error(e.msg || '验证码发送失败')
  } finally {
    loading.value = false
  }
}

// 开始倒计时
const startCountdown = () => {
  countdown.value = 60
  timer.value = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      clearInterval(timer.value)
    }
  }, 1000)
}

// 获取按钮文本
const btnText = computed(() => {
  return countdown.value > 0 ? `${countdown.value}秒后重试` : '获取验证码'
})

// 登录
const handleLogin = async () => {
  const valid = await formRef.value?.validate()
  if (!valid) return

  try {
    loading.value = true
    const formData: UserLoginType = {
      username: model.account,
      password: model.code,
      method: '1' // 验证码登录
    }
    const res = await authStore.login(formData)

    if (res) {
      ElMessage.success({
        message: '登录成功，正在加载系统...'
      })
      emit('switch-module', 'pwd-login') // 登录成功后返回
    }
  } catch (e: any) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

// 返回密码登录
const backToPwdLogin = () => {
  emit('switch-module', 'pwd-login')
}

// 清理定时器
onUnmounted(() => {
  if (timer.value) {
    clearInterval(timer.value)
  }
})
</script>

<template>
  <ElForm ref="formRef" :model="model" :rules="rules" size="large" :show-label="false">
    <ElFormItem prop="account">
      <ElInput v-model="model.account" placeholder="请输入手机号或邮箱" clearable>
        <template #prefix>
          <el-icon><ele-User /></el-icon>
        </template>
      </ElInput>
    </ElFormItem>
    <ElFormItem prop="code">
      <div class="code-input-wrapper">
        <ElInput
          v-model="model.code"
          placeholder="请输入验证码"
          clearable
          maxlength="6"
          class="code-input"
        />
        <ElButton
          size="large"
          :disabled="countdown > 0"
          :loading="loading"
          class="code-btn"
          @click="getCode"
        >
          {{ btnText }}
        </ElButton>
      </div>
    </ElFormItem>
    <ElSpace direction="vertical" :size="20" fill class="w-full">
      <ElButton type="primary" size="large" round block :loading="loading" @click="handleLogin">
        登录
      </ElButton>
      <ElButton size="large" round block @click="backToPwdLogin"> 返回 </ElButton>
    </ElSpace>
  </ElForm>
</template>

<style scoped>
.w-full {
  width: 100%;
}

.code-input-wrapper {
  display: flex;
  gap: 12px;
  width: 100%;
}

.code-input {
  flex: 1;
}

.code-btn {
  flex-shrink: 0;
  min-width: 120px;
}

:deep(.el-input__wrapper) {
  border-radius: 8px;
  box-shadow: 0 0 0 1px var(--el-border-color) inset;
  transition: all 0.3s;
}

:deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px var(--el-color-primary) inset;
}

:deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 1px var(--el-color-primary) inset;
}

:deep(.el-button--large) {
  height: 44px;
  font-size: 15px;
  font-weight: 500;
}
</style>
