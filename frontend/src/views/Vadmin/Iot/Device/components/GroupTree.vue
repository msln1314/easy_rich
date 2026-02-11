<template>
  <div class="head-container">
    <el-input v-model="ClientGroupName" class="mb-20px" clearable placeholder="请输入分组名称">
      <template #prefix>
        <Icon icon="ep:search" />
      </template>
    </el-input>
  </div>
  <div class="head-container">
    <el-tree
      ref="treeRef"
      :data="ClientGroupList"
      :expand-on-click-node="false"
      :filter-node-method="filterNode"
      :props="defaultProps"
      default-expand-all
      highlight-current
      node-key="id"
      @node-click="handleNodeClick"
    />
  </div>
</template>

<script lang="ts" setup>
import { ElTree, ElInput } from 'element-plus'
import { Icon } from '@/components/Icon'
import { reactive, ref, unref, onMounted } from 'vue'
import { getClientGroupTreeOptionsApi } from '@/api/iot/client_group'
// import { defaultProps, handleTree } from '@/utils/tree'

defineOptions({ name: 'IotClientGroupTree' })

const ClientGroupName = ref('')
const ClientGroupList = ref<Tree[]>([]) // 树形结构
const treeRef = ref<InstanceType<typeof ElTree>>()

/** 获得部门树 */
const getTree = async () => {
  const res = await getClientGroupTreeOptionsApi()
  ClientGroupList.value = res.data
  // console.log(ClientGroupList, 'ClientGroup')
  // ClientGroupList.value = []
  // ClientGroupList.value.push(...handleTree(res))
}

/** 基于名字过滤 */
const filterNode = (name: string, data: Tree) => {
  if (!name) return true
  return data.label.includes(name)
}

/** 处理部门被点击 */
const handleNodeClick = async (row: { [key: string]: any }) => {
  emits('node-click', row)
}
const emits = defineEmits(['node-click'])

/** 初始化 */
onMounted(async () => {
  await getTree()
})
</script>
@/api/iot/client_group
