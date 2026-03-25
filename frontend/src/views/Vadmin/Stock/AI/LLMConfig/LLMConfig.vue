<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import {
  ElMessage,
  ElCard,
  ElTable,
  ElTableColumn,
  ElButton,
  ElTag,
  ElSwitch,
  ElDialog,
  ElForm,
  ElFormItem,
  ElInput,
  ElSelect,
  ElOption,
  ElInputNumber,
  ElRow,
  ElCol,
  ElTooltip,
  ElMessageBox
} from 'element-plus'
import { ContentWrap } from '@/components/ContentWrap'
import {
  getLLMConfigList,
  getProviders,
  createLLMConfig,
  updateLLMConfig,
  deleteLLMConfig,
  setDefaultLLMConfig,
  toggleLLMConfig,
  testLLMConfig,
  type LLMModelConfig,
  type ProviderInfo,
  type LLMModelConfigCreate
} from '@/api/stock/llmConfig'

defineOptions({
  name: 'LLMConfig'
})

// 状态
const loading = ref(false)
const configList = ref<LLMModelConfig[]>([])
const providers = ref<ProviderInfo[]>([])

// 对话框
const dialogVisible = ref(false)
const dialogTitle = ref('新增模型配置')
const formLoading = ref(false)
const isEdit = ref(false)
const editId = ref<number | null>(null)

// 表单
const formRef = ref()
const formData = reactive<LLMModelConfigCreate & { id?: number }>({
  name: '',
  provider: 'openai',
  model_name: '',
  api_key: '',
  api_base: 'https://api.openai.com/v1',
  max_tokens: 4000,
  temperature: 0.7,
  timeout: 120,
  is_default: false,
  is_enabled: true,
  description: ''
})

// 表单规则
const formRules = {
  name: [{ required: true, message: '请输入配置名称', trigger: 'blur' }],
  provider: [{ required: true, message: '请选择提供商', trigger: 'change' }],
  model_name: [{ required: true, message: '请输入模型名称', trigger: 'blur' }],
  api_key: [{ required: true, message: '请输入API密钥', trigger: 'blur' }],
  api_base: [{ required: true, message: '请输入API地址', trigger: 'blur' }]
}

// 当前选择的提供商信息
const currentProvider = computed(() => {
  return providers.value.find(p => p.value === formData.provider)
})

// 提供商选项
const providerOptions = computed(() => {
  return providers.value.map(p => ({
    value: p.value,
    label: p.label
  }))
})

// 模型选项
const modelOptions = computed(() => {
  return currentProvider.value?.models.map(m => ({
    value: m,
    label: m
  })) || []
})

// 提供商改变时
const handleProviderChange = (provider: string) => {
  const info = providers.value.find(p => p.value === provider)
  if (info) {
    formData.api_base = info.default_api_base
    if (info.models.length > 0) {
      formData.model_name = info.models[0]
    } else {
      formData.model_name = ''
    }
  }
}

// 加载配置列表
const loadConfigList = async () => {
  loading.value = true
  try {
    const res = await getLLMConfigList()
    if (res.code === 200) {
      configList.value = res.data || []
    }
  } catch (error: any) {
    ElMessage.error(error.message || '加载失败')
  } finally {
    loading.value = false
  }
}

// 加载提供商列表
const loadProviders = async () => {
  try {
    const res = await getProviders()
    if (res.code === 200) {
      providers.value = res.data || []
    }
  } catch (error) {
    console.error('加载提供商失败', error)
  }
}

// 新增
const handleAdd = () => {
  isEdit.value = false
  editId.value = null
  dialogTitle.value = '新增模型配置'

  // 重置表单
  Object.assign(formData, {
    name: '',
    provider: 'openai',
    model_name: 'gpt-4',
    api_key: '',
    api_base: 'https://api.openai.com/v1',
    max_tokens: 4000,
    temperature: 0.7,
    timeout: 120,
    is_default: false,
    is_enabled: true,
    description: ''
  })

  dialogVisible.value = true
}

// 编辑
const handleEdit = (row: LLMModelConfig) => {
  isEdit.value = true
  editId.value = row.id
  dialogTitle.value = '编辑模型配置'

  Object.assign(formData, {
    name: row.name,
    provider: row.provider,
    model_name: row.model_name,
    api_key: '', // API Key 不回显
    api_base: row.api_base,
    max_tokens: row.max_tokens,
    temperature: row.temperature,
    timeout: row.timeout,
    is_default: row.is_default,
    is_enabled: row.is_enabled,
    description: row.description || ''
  })

  dialogVisible.value = true
}

// 提交表单
const handleSubmit = async () => {
  const valid = await formRef.value?.validate()
  if (!valid) return

  formLoading.value = true
  try {
    if (isEdit.value && editId.value) {
      const updateData: any = { ...formData }
      if (!updateData.api_key) {
        delete updateData.api_key // 不更新空的API Key
      }
      const res = await updateLLMConfig(editId.value, updateData)
      if (res.code === 200) {
        ElMessage.success('更新成功')
        dialogVisible.value = false
        loadConfigList()
      } else {
        ElMessage.error(res.msg || '更新失败')
      }
    } else {
      const res = await createLLMConfig(formData)
      if (res.code === 200) {
        ElMessage.success('创建成功')
        dialogVisible.value = false
        loadConfigList()
      } else {
        ElMessage.error(res.msg || '创建失败')
      }
    }
  } catch (error: any) {
    ElMessage.error(error.message || '操作失败')
  } finally {
    formLoading.value = false
  }
}

// 删除
const handleDelete = async (row: LLMModelConfig) => {
  try {
    await ElMessageBox.confirm(`确定要删除配置 "${row.name}" 吗？`, '提示', {
      type: 'warning'
    })

    const res = await deleteLLMConfig(row.id)
    if (res.code === 200) {
      ElMessage.success('删除成功')
      loadConfigList()
    } else {
      ElMessage.error(res.msg || '删除失败')
    }
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '删除失败')
    }
  }
}

// 设置默认
const handleSetDefault = async (row: LLMModelConfig) => {
  try {
    const res = await setDefaultLLMConfig(row.id)
    if (res.code === 200) {
      ElMessage.success('设置成功')
      loadConfigList()
    } else {
      ElMessage.error(res.msg || '设置失败')
    }
  } catch (error: any) {
    ElMessage.error(error.message || '设置失败')
  }
}

// 启用/禁用
const handleToggle = async (row: LLMModelConfig) => {
  try {
    const res = await toggleLLMConfig(row.id)
    if (res.code === 200) {
      ElMessage.success(res.data?.is_enabled ? '已启用' : '已禁用')
      loadConfigList()
    } else {
      ElMessage.error(res.msg || '操作失败')
    }
  } catch (error: any) {
    ElMessage.error(error.message || '操作失败')
  }
}

// 测试连接
const handleTest = async (row: LLMModelConfig) => {
  ElMessage.info('正在测试连接...')
  try {
    const res = await testLLMConfig(row.id)
    if (res.data?.success) {
      ElMessage.success(res.data.message || '连接成功')
    } else {
      ElMessage.error(res.data?.message || '连接失败')
    }
  } catch (error: any) {
    ElMessage.error(error.message || '测试失败')
  }
}

// 获取提供商标签类型
const getProviderTagType = (provider: string) => {
  const types: Record<string, string> = {
    openai: 'success',
    deepseek: 'primary',
    aliyun: 'warning',
    zhipu: 'info',
    baidu: '',
    tencent: 'success',
    custom: 'info'
  }
  return types[provider] || 'info'
}

// 获取提供商中文名
const getProviderLabel = (provider: string) => {
  const info = providers.value.find(p => p.value === provider)
  return info?.label || provider
}

onMounted(() => {
  loadProviders()
  loadConfigList()
})
</script>

<template>
  <ContentWrap>
    <ElCard>
      <template #header>
        <div class="flex items-center justify-between">
          <span class="font-bold text-lg">大模型配置管理</span>
          <ElButton type="primary" @click="handleAdd">新增配置</ElButton>
        </div>
      </template>

      <ElTable :data="configList" v-loading="loading" stripe>
        <ElTableColumn prop="name" label="配置名称" width="150" />
        <ElTableColumn prop="provider" label="提供商" width="120">
          <template #default="{ row }">
            <ElTag :type="getProviderTagType(row.provider)" size="small">
              {{ getProviderLabel(row.provider) }}
            </ElTag>
          </template>
        </ElTableColumn>
        <ElTableColumn prop="model_name" label="模型名称" width="150" />
        <ElTableColumn prop="api_base" label="API地址" min-width="200" show-overflow-tooltip />
        <ElTableColumn prop="api_key_masked" label="API Key" width="150" />
        <ElTableColumn prop="max_tokens" label="最大Token" width="100" />
        <ElTableColumn prop="temperature" label="温度" width="80" />
        <ElTableColumn prop="is_default" label="默认" width="80" align="center">
          <template #default="{ row }">
            <ElTag v-if="row.is_default" type="success" size="small">默认</ElTag>
            <span v-else>-</span>
          </template>
        </ElTableColumn>
        <ElTableColumn prop="is_enabled" label="状态" width="100" align="center">
          <template #default="{ row }">
            <ElSwitch
              :model-value="row.is_enabled"
              @change="handleToggle(row)"
              active-text="启用"
              inactive-text="禁用"
            />
          </template>
        </ElTableColumn>
        <ElTableColumn label="操作" width="220" fixed="right">
          <template #default="{ row }">
            <ElButton size="small" @click="handleTest(row)">测试</ElButton>
            <ElButton size="small" @click="handleEdit(row)">编辑</ElButton>
            <ElButton
              size="small"
              type="success"
              @click="handleSetDefault(row)"
              :disabled="row.is_default"
            >
              设为默认
            </ElButton>
            <ElButton size="small" type="danger" @click="handleDelete(row)">删除</ElButton>
          </template>
        </ElTableColumn>
      </ElTable>
    </ElCard>

    <!-- 新增/编辑对话框 -->
    <ElDialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="600px"
      :close-on-click-modal="false"
    >
      <ElForm
        ref="formRef"
        :model="formData"
        :rules="formRules"
        label-width="100px"
      >
        <ElRow :gutter="20">
          <ElCol :span="12">
            <ElFormItem label="配置名称" prop="name">
              <ElInput v-model="formData.name" placeholder="请输入配置名称" />
            </ElFormItem>
          </ElCol>
          <ElCol :span="12">
            <ElFormItem label="提供商" prop="provider">
              <ElSelect
                v-model="formData.provider"
                placeholder="请选择提供商"
                @change="handleProviderChange"
                style="width: 100%"
              >
                <ElOption
                  v-for="item in providerOptions"
                  :key="item.value"
                  :value="item.value"
                  :label="item.label"
                />
              </ElSelect>
            </ElFormItem>
          </ElCol>
        </ElRow>

        <ElRow :gutter="20">
          <ElCol :span="12">
            <ElFormItem label="模型名称" prop="model_name">
              <ElSelect
                v-model="formData.model_name"
                placeholder="请选择或输入模型名称"
                filterable
                allow-create
                style="width: 100%"
              >
                <ElOption
                  v-for="item in modelOptions"
                  :key="item.value"
                  :value="item.value"
                  :label="item.label"
                />
              </ElSelect>
            </ElFormItem>
          </ElCol>
          <ElCol :span="12">
            <ElFormItem label="API密钥" prop="api_key">
              <ElInput
                v-model="formData.api_key"
                type="password"
                placeholder="请输入API密钥"
                show-password
              />
            </ElFormItem>
          </ElCol>
        </ElRow>

        <ElFormItem label="API地址" prop="api_base">
          <ElInput v-model="formData.api_base" placeholder="请输入API基础地址" />
        </ElFormItem>

        <ElRow :gutter="20">
          <ElCol :span="8">
            <ElFormItem label="最大Token">
              <ElInputNumber v-model="formData.max_tokens" :min="100" :max="32000" :step="100" style="width: 100%" />
            </ElFormItem>
          </ElCol>
          <ElCol :span="8">
            <ElFormItem label="温度参数">
              <ElInputNumber v-model="formData.temperature" :min="0" :max="2" :step="0.1" :precision="1" style="width: 100%" />
            </ElFormItem>
          </ElCol>
          <ElCol :span="8">
            <ElFormItem label="超时时间">
              <ElInputNumber v-model="formData.timeout" :min="10" :max="600" :step="10" style="width: 100%" />
            </ElFormItem>
          </ElCol>
        </ElRow>

        <ElRow :gutter="20">
          <ElCol :span="12">
            <ElFormItem label="设为默认">
              <ElSwitch v-model="formData.is_default" />
            </ElFormItem>
          </ElCol>
          <ElCol :span="12">
            <ElFormItem label="启用状态">
              <ElSwitch v-model="formData.is_enabled" />
            </ElFormItem>
          </ElCol>
        </ElRow>

        <ElFormItem label="描述">
          <ElInput
            v-model="formData.description"
            type="textarea"
            :rows="2"
            placeholder="可选：配置描述"
          />
        </ElFormItem>
      </ElForm>

      <template #footer>
        <ElButton @click="dialogVisible = false">取消</ElButton>
        <ElButton type="primary" :loading="formLoading" @click="handleSubmit">确定</ElButton>
      </template>
    </ElDialog>
  </ContentWrap>
</template>

<style scoped>
</style>