<script setup lang="ts">
import { ref, computed, reactive } from 'vue'
import { ElForm, ElFormItem, ElInput, ElButton, ElSpace } from 'element-plus'
import { ElMessage } from 'element-plus'
import { sendCodeApi, registerApi } from '@/api/login'

defineOptions({ name: 'Register' })

const emit = defineEmits(['switch-module'])

const formRef = ref()
const loading = ref(false)

interface FormModel {
  username: string // 手机号或邮箱
  code: string
  password: string
  confirmPassword: string
}

const model = reactive<FormModel>({
  username: '',
  code: '',
  password: '',
  confirmPassword: ''
})

// 表单验证规则
const rules = computed(() => ({
  username: [
    { required: true, message: '请输入手机号或邮箱', trigger: 'blur' },
    {
      validator: (rule: any, value: any, callback: any) => {
        const phonePattern = /^1[3-9]\d{9}$/
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
        if (!phonePattern.test(value) && !emailPattern.test(value)) {
          callback(new Error('请输入正确的手机号或邮箱'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ],
  code: [{ required: true, message: '请输入验证码', trigger: 'blur' }],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    {
      validator: (rule: any, value: any, callback: any) => {
        if (value !== model.password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}))

// 获取验证码
const getCode = async () => {
  if (!model.username) {
    ElMessage.warning('请先输入手机号或邮箱')
    return
  }

  const phonePattern = /^1[3-9]\d{9}$/
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!phonePattern.test(model.username) && !emailPattern.test(model.username)) {
    ElMessage.error('请输入正确的手机号或邮箱')
    return
  }

  loading.value = true
  try {
    await sendCodeApi({ username: model.username })
    ElMessage.success('验证码已发送')
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

// 注册
const handleRegister = async () => {
  const valid = await formRef.value?.validate()
  if (!valid) return

  try {
    loading.value = true
    const res = await registerApi({
      username: model.username,
      code: model.code,
      password: model.password
    })
    console.log(res)
    // 只有在响应成功时才显示注册成功
    ElMessage.success('注册成功')
    emit('switch-module', 'pwd-login')
  } catch (e) {
    console.error(e)
    // 错误已经在 axios 拦截器中处理，这里不需要额外处理
  } finally {
    loading.value = false
  }
}

// 返回登录
const backToLogin = () => {
  emit('switch-module', 'pwd-login')
}
</script>

<template>
  <ElForm ref="formRef" :model="model" :rules="rules" size="large" :show-label="false">
    <ElFormItem prop="username">
      <ElInput v-model="model.username" placeholder="请输入手机号或邮箱" clearable>
        <template #prefix>
          <el-icon><ele-Phone /></el-icon>
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
        <ElButton size="large" :loading="loading" class="code-btn" @click="getCode">
          获取验证码
        </ElButton>
      </div>
    </ElFormItem>
    <ElFormItem prop="password">
      <ElInput v-model="model.password" type="password" placeholder="请输入密码" show-password>
        <template #prefix>
          <el-icon><ele-Lock /></el-icon>
        </template>
      </ElInput>
    </ElFormItem>
    <ElFormItem prop="confirmPassword">
      <ElInput
        v-model="model.confirmPassword"
        type="password"
        placeholder="请确认密码"
        show-password
        @keyup.enter="handleRegister"
      >
        <template #prefix>
          <el-icon><ele-Lock /></el-icon>
        </template>
      </ElInput>
    </ElFormItem>
    <ElSpace direction="vertical" :size="20" fill class="w-full">
      <ElButton type="primary" size="large" round block :loading="loading" @click="handleRegister">
        注册
      </ElButton>
      <ElButton size="large" round block @click="backToLogin"> 返回登录 </ElButton>
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
