<script setup lang="ts">
import { ref, computed, reactive, watch } from 'vue'
import { ElForm, ElFormItem, ElInput, ElButton, ElCheckbox, ElSpace } from 'element-plus'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import { useAuthStoreWithOut } from '@/store/modules/auth'
import { getMenuRoutesApi } from '@/api/system/menu'
import { usePermissionStore } from '@/store/modules/permission'
import { UserLoginType } from '@/api/login/types'
import { useStorage } from '@/hooks/web/useStorage'

defineOptions({ name: 'PwdLogin' })

const emit = defineEmits(['switch-module'])

const authStore = useAuthStoreWithOut()
const permissionStore = usePermissionStore()
const { setStorage } = useStorage()
const router = useRouter()

const formRef = ref()
const loading = ref(false)
const remember = ref(false)

interface FormModel {
  username: string
  password: string
  method: string
}

const model = reactive<FormModel>({
  username: '',
  password: '',
  method: '0'
})

const redirect = ref<string>('')

// 监听路由变化,获取 redirect 参数
watch(
  router,
  (r: any) => {
    redirect.value = r?.query?.redirect as string
  },
  {
    immediate: true
  }
)

// 表单验证规则
const rules = computed(() => ({
  username: [{ required: true, message: '请输入账号', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}))

// 登录
const handleLogin = async () => {
  const valid = await formRef.value?.validate()
  if (!valid) return

  try {
    loading.value = true
    const formData: UserLoginType = {
      username: model.username,
      password: model.password,
      method: model.method
    }
    const res = await authStore.login(formData)

    if (res) {
      ElMessage.success({
        message: '登录成功，正在加载系统...'
      })
      if (!res.data.is_reset_password) {
        router.push({ path: '/reset/password' })
      } else {
        await getMenu()
      }
    }
  } catch (e: any) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

// 获取用户菜单信息
const getMenu = async () => {
  const res = await getMenuRoutesApi()
  if (res) {
    const routers = res.data || []
    setStorage('roleRouters', routers)
    await permissionStore.generateRoutes(routers).catch(() => {})
    permissionStore.getAddRouters.forEach((route) => {
      router.addRoute(route as any)
    })
    permissionStore.setIsAddRouters(true)
    router.push({ path: redirect.value || permissionStore.addRouters[0].path })
  }
}

// 切换到验证码登录
const switchToCodeLogin = () => {
  emit('switch-module', 'code-login')
}

// 切换到注册
const switchToRegister = () => {
  emit('switch-module', 'register')
}
</script>

<template>
  <ElForm
    ref="formRef"
    :model="model"
    :rules="rules"
    size="large"
    :show-label="false"
    class="login-form"
  >
    <ElFormItem prop="username">
      <ElInput v-model="model.username" placeholder="请输入账号" clearable>
        <template #prefix>
          <el-icon><ele-User /></el-icon>
        </template>
      </ElInput>
    </ElFormItem>
    <ElFormItem prop="password">
      <ElInput
        v-model="model.password"
        type="password"
        placeholder="请输入密码"
        show-password
        @keyup.enter="handleLogin"
      >
        <template #prefix>
          <el-icon><ele-Unlock /></el-icon>
        </template>
      </ElInput>
    </ElFormItem>
    <ElSpace direction="vertical" :size="20" class="w-full" fill>
      <div class="flex-y-center justify-between">
        <ElCheckbox v-model="remember">记住我</ElCheckbox>
        <ElButton text type="primary">忘记密码</ElButton>
      </div>
      <ElButton type="primary" size="large" round block :loading="loading" @click="handleLogin">
        登录
      </ElButton>
      <div class="flex-y-center justify-between gap-12px">
        <ElButton class="flex-1" size="default" @click="switchToCodeLogin"> 验证码登录 </ElButton>
        <ElButton class="flex-1" size="default" @click="switchToRegister"> 注册账号 </ElButton>
      </div>
    </ElSpace>
  </ElForm>
</template>

<style scoped>
.w-full {
  width: 100%;
}

.flex-y-center {
  display: flex;
  align-items: center;
}

.justify-between {
  justify-content: space-between;
}

.gap-12px {
  gap: 12px;
}

.login-buttons {
  display: flex;
  gap: 8px;
  justify-content: space-between;
}

.flex-1 {
  flex: 1;
}

.login-form {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
}

:deep(.el-form-item) {
  width: 100%;
  margin-bottom: 20px;
}

:deep(.el-form-item__content) {
  width: 100%;
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

:deep(.el-button--default) {
  border-radius: 8px;
}

:deep(.el-checkbox__label) {
  font-size: 14px;
}
</style>
