<template>
  <div class="empty-state">
    <el-empty :description="description || '暂无数据'">
      <el-button v-if="showRetry" type="primary" @click="$emit('retry')"> 重新查询 </el-button>
    </el-empty>
  </div>
</template>

<script setup>
import { ElEmpty, ElButton } from 'element-plus'

defineProps({
  description: {
    type: String,
    default: ''
  },
  showRetry: {
    type: Boolean,
    default: false
  }
})

defineEmits(['retry'])
</script>

<style scoped>
.empty-state {
  padding: 40px 20px;
  text-align: center;
}
</style>
