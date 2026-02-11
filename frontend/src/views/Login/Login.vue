<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElCard } from 'element-plus'
import PwdLogin from './components/PwdLogin.vue'
import CodeLogin from './components/CodeLogin.vue'
import Register from './components/Register.vue'
import { WaveBg } from '@/components/WaveBg'
import { getPaletteColorByNumber, mixColor } from '@sa/color'
import { useAppStoreWithOut } from '@/store/modules/app'
import { useDesign } from '@/hooks/web/useDesign'

defineOptions({ name: 'LoginPage' })

const { getPrefixCls } = useDesign()
console.log(getPrefixCls('login'))
const prefixCls = getPrefixCls('login')

const appStore = useAppStoreWithOut()
const activeModule = ref<'pwd-login' | 'code-login' | 'register'>('pwd-login')

// 从 store 获取主题色
const themeColor = computed(() => appStore.getTheme.elColorPrimary || '#409eff')

// 从 store 获取系统标题
const systemTitle = computed(() => appStore.getTitle || '系统管理平台')

// 从 store 获取 logo 图片
const logoImage = computed(() => appStore.getLogoImage || '')

// 从 store 获取页脚内容
const footerContent = computed(() => appStore.getFooterContent || '')

// 从 store 获取 ICP 备案号
const icpNumber = computed(() => appStore.getIcpNumber || '')

// 从 store 获取暗黑模式
const isDark = computed(() => appStore.getIsDark || false)

// 根据模块切换组件
const activeComponent = computed(() => {
  switch (activeModule.value) {
    case 'pwd-login':
      return PwdLogin
    case 'code-login':
      return CodeLogin
    case 'register':
      return Register
    default:
      return PwdLogin
  }
})

// 切换模块
const handleModuleSwitch = (module: 'pwd-login' | 'code-login' | 'register') => {
  activeModule.value = module
}

// 计算背景主题色
const bgThemeColor = computed(() => {
  const color = themeColor.value
  return isDark.value ? getPaletteColorByNumber(color, 600) : color
})

// 计算背景色
const bgColor = computed(() => {
  const COLOR_WHITE = '#ffffff'
  const ratio = isDark.value ? 0.5 : 0.2
  return mixColor(COLOR_WHITE, themeColor.value, ratio)
})

// 当前模块标题
const moduleTitle = computed(() => {
  switch (activeModule.value) {
    case 'pwd-login':
      return '账号密码登录'
    case 'code-login':
      return '验证码登录'
    case 'register':
      return '注册账号'
    default:
      return '账号密码登录'
  }
})
</script>

<template>
  <div :class="`${prefixCls}-container`" :style="{ backgroundColor: bgColor }">
    <WaveBg :theme-color="bgThemeColor" />
    <ElCard :class="`${prefixCls}-card`">
      <div :class="`${prefixCls}-content`">
        <header :class="`${prefixCls}-header`">
          <div :class="`${prefixCls}-logo-area`">
            <div v-if="logoImage" :class="`${prefixCls}-logo-image-wrapper`">
              <img :src="logoImage" alt="logo" :class="`${prefixCls}-logo-image`" />
            </div>
            <div v-else :class="`${prefixCls}-logo-wrapper`">
              <svg
                :class="`${prefixCls}-logo`"
                viewBox="0 0 64 64"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <circle cx="32" cy="32" r="32" :fill="`url(#logo-gradient-${activeModule})`" />
                <path d="M32 20L40 28L32 36L24 28L32 20Z" fill="white" fill-opacity="0.9" />
                <path d="M32 28L40 36L32 44L24 36L32 28Z" fill="white" fill-opacity="0.7" />
                <defs>
                  <linearGradient
                    :id="`logo-gradient-${activeModule}`"
                    x1="0"
                    y1="0"
                    x2="64"
                    y2="64"
                    gradientUnits="userSpaceOnUse"
                  >
                    <stop :stop-color="themeColor" />
                    <stop offset="1" :stop-color="getPaletteColorByNumber(themeColor, 600)" />
                  </linearGradient>
                </defs>
              </svg>
            </div>
            <div :class="`${prefixCls}-title-area`">
              <h3 :class="`${prefixCls}-title`">{{ systemTitle }}</h3>
              <p :class="`${prefixCls}-subtitle`">欢迎登录</p>
            </div>
          </div>
        </header>
        <main :class="`${prefixCls}-main`">
          <h3 :class="`${prefixCls}-module-title`">{{ moduleTitle }}</h3>
          <div :class="`${prefixCls}-form-wrapper`">
            <component :is="activeComponent" @switch-module="handleModuleSwitch" />
          </div>
        </main>
      </div>
    </ElCard>
    <footer v-if="footerContent || icpNumber" :class="`${prefixCls}-footer`">
      <p v-if="footerContent">{{ footerContent }}</p>
      <p v-if="icpNumber">{{ icpNumber }}</p>
    </footer>
  </div>
</template>

<style scoped>
.v-login-container {
  position: relative;
  width: 100%;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

.v-login-card {
  position: relative;
  z-index: 10;
  border-radius: 16px;
  width: auto;
  box-shadow: 0 8px 32px rgba(99, 102, 241, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.95);
}

.v-login-content {
  width: 420px;
  padding: 20px;
}

@media (max-width: 640px) {
  .v-login-content {
    width: 320px;
    padding: 16px;
  }
}

.v-login-header {
  padding-bottom: 28px;
}

.v-login-logo-area {
  display: flex;
  align-items: center;
  gap: 16px;
}

.v-login-logo-wrapper {
  width: 64px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 16px;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

@media (max-width: 640px) {
  .v-login-logo-wrapper {
    width: 52px;
    height: 52px;
  }
}

.v-login-logo {
  width: 40px;
  height: 40px;
}

@media (max-width: 640px) {
  .v-login-logo {
    width: 32px;
    height: 32px;
  }
}

.v-login-logo-image-wrapper {
  width: 64px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 16px;
  overflow: hidden;
}

.v-login-logo-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.v-login-title-area {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.v-login-title {
  font-size: 26px;
  font-weight: 600;
  color: var(--el-color-primary);
  margin: 0;
  line-height: 1.2;
}

@media (max-width: 640px) {
  .v-login-title {
    font-size: 22px;
  }
}

.v-login-subtitle {
  font-size: 14px;
  color: var(--el-text-color-secondary);
  margin: 0;
  font-weight: 400;
}

.v-login-main {
  padding-top: 20px;
}

.v-login-module-title {
  font-size: 18px;
  font-weight: 500;
  color: var(--el-text-color-primary);
  margin: 0 0 24px 0;
  text-align: center;
}

.v-login-form-wrapper {
  padding-top: 8px;
}

.v-login-footer {
  position: fixed;
  bottom: 20px;
  left: 0;
  right: 0;
  text-align: center;
  font-size: 14px;
  color: var(--el-text-color-secondary);
  z-index: 10;
}

.v-login-footer p {
  margin: 4px 0;
}
</style>
