<script setup lang="ts">
import { ElRow, ElCol, ElCard, ElTable, ElTableColumn, ElTag, ElLink, ElEmpty } from 'element-plus'

defineProps<{
  data: any
}>()

const formatDate = (date: string) => {
  if (!date) return '-'
  return date.substring(0, 10)
}
</script>

<template>
  <div class="info-tab">
    <ElRow :gutter="16">
      <!-- 公告 -->
      <ElCol :span="12">
        <ElCard shadow="never" class="info-card">
          <template #header>
            <span class="card-title">公司公告</span>
          </template>
          <ElTable
            :data="data.notices || []"
            stripe
            size="small"
            max-height="400"
            v-if="data.notices?.length > 0"
          >
            <ElTableColumn prop="date" label="日期" width="100">
              <template #default="{ row }">{{ formatDate(row.date) }}</template>
            </ElTableColumn>
            <ElTableColumn prop="type" label="类型" width="100">
              <template #default="{ row }">
                <ElTag size="small">{{ row.type || '公告' }}</ElTag>
              </template>
            </ElTableColumn>
            <ElTableColumn prop="title" label="标题" min-width="200">
              <template #default="{ row }">
                <ElLink type="primary" :href="row.url" target="_blank">{{ row.title }}</ElLink>
              </template>
            </ElTableColumn>
          </ElTable>
          <ElEmpty v-else description="暂无公告数据" :image-size="60" />
        </ElCard>
      </ElCol>

      <!-- 研报 -->
      <ElCol :span="12">
        <ElCard shadow="never" class="info-card">
          <template #header>
            <span class="card-title">研究报告</span>
          </template>
          <ElTable
            :data="data.reports || []"
            stripe
            size="small"
            max-height="400"
            v-if="data.reports?.length > 0"
          >
            <ElTableColumn prop="date" label="日期" width="100">
              <template #default="{ row }">{{ formatDate(row.date) }}</template>
            </ElTableColumn>
            <ElTableColumn prop="org_name" label="机构" width="120" show-overflow-tooltip />
            <ElTableColumn prop="rating" label="评级" width="80">
              <template #default="{ row }">
                <ElTag
                  v-if="row.rating"
                  :type="
                    row.rating.includes('买入')
                      ? 'success'
                      : row.rating.includes('卖出')
                      ? 'danger'
                      : 'info'
                  "
                  size="small"
                >
                  {{ row.rating }}
                </ElTag>
                <span v-else>-</span>
              </template>
            </ElTableColumn>
            <ElTableColumn prop="title" label="报告标题" min-width="200" show-overflow-tooltip />
          </ElTable>
          <ElEmpty v-else description="暂无研报数据" :image-size="60" />
        </ElCard>
      </ElCol>
    </ElRow>

    <!-- 机构评级 -->
    <ElCard shadow="never" class="info-card">
      <template #header>
        <span class="card-title">机构评级</span>
      </template>
      <ElTable
        :data="data.rating?.data || []"
        stripe
        size="small"
        v-if="data.rating?.data?.length > 0"
      >
        <ElTableColumn prop="report_date" label="评级日期" width="120" />
        <ElTableColumn prop="org_name" label="机构名称" min-width="150" />
        <ElTableColumn prop="rating" label="评级" width="100">
          <template #default="{ row }">
            <ElTag
              :type="
                row.rating?.includes('买入')
                  ? 'success'
                  : row.rating?.includes('卖出')
                  ? 'danger'
                  : 'warning'
              "
              size="small"
            >
              {{ row.rating || '-' }}
            </ElTag>
          </template>
        </ElTableColumn>
        <ElTableColumn prop="rating_change" label="评级变动" width="100">
          <template #default="{ row }">
            <ElTag v-if="row.rating_change?.includes('上调')" type="success" size="small">{{
              row.rating_change
            }}</ElTag>
            <ElTag v-else-if="row.rating_change?.includes('下调')" type="danger" size="small">{{
              row.rating_change
            }}</ElTag>
            <span v-else>{{ row.rating_change || '-' }}</span>
          </template>
        </ElTableColumn>
        <ElTableColumn prop="target_price" label="目标价" width="100" align="right">
          <template #default="{ row }">{{ row.target_price?.toFixed(2) || '-' }}</template>
        </ElTableColumn>
      </ElTable>
      <ElEmpty v-else description="暂无机构评级数据" :image-size="60" />
    </ElCard>
  </div>
</template>

<style lang="scss" scoped>
.info-tab {
  .info-card {
    margin-bottom: 16px;
  }

  .card-title {
    font-size: 15px;
    font-weight: 600;
  }
}
</style>
