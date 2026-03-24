<script setup lang="ts">
import { ElRow, ElCol, ElCard, ElDescriptions, ElDescriptionsItem, ElTag, ElTable, ElTableColumn, ElEmpty } from 'element-plus'

defineProps<{
  data: any
}>()

const formatValue = (value: any, suffix: string = '') => {
  if (value === null || value === undefined || value === '') return '-'
  if (typeof value === 'number') return value.toFixed(2) + suffix
  return value + suffix
}

const formatAmount = (value: number | null | undefined) => {
  if (!value && value !== 0) return '-'
  if (value >= 100000000) return (value / 100000000).toFixed(2) + '亿'
  if (value >= 10000) return (value / 10000).toFixed(2) + '万'
  return value.toFixed(2)
}
</script>

<template>
  <div class="fund-tab">
    <ElRow :gutter="16">
      <!-- 资金流向 -->
      <ElCol :span="12">
        <ElCard shadow="never" class="info-card">
          <template #header>
            <span class="card-title">主力资金流向</span>
          </template>
          <ElDescriptions :column="2" border size="small" v-if="data.fund_flow?.main_net_inflow !== undefined">
            <ElDescriptionsItem label="主力净流入">
              <span :class="data.fund_flow.main_net_inflow > 0 ? 'text-up' : 'text-down'">
                {{ formatAmount(data.fund_flow.main_net_inflow) }}
              </span>
            </ElDescriptionsItem>
            <ElDescriptionsItem label="主力净占比">
              <span :class="data.fund_flow.main_net_inflow_ratio > 0 ? 'text-up' : 'text-down'">
                {{ formatValue(data.fund_flow.main_net_inflow_ratio, '%') }}
              </span>
            </ElDescriptionsItem>
            <ElDescriptionsItem label="超大单净流入">
              <span :class="data.fund_flow.super_net_inflow > 0 ? 'text-up' : 'text-down'">
                {{ formatAmount(data.fund_flow.super_net_inflow) }}
              </span>
            </ElDescriptionsItem>
            <ElDescriptionsItem label="大单净流入">
              <span :class="data.fund_flow.big_net_inflow > 0 ? 'text-up' : 'text-down'">
                {{ formatAmount(data.fund_flow.big_net_inflow) }}
              </span>
            </ElDescriptionsItem>
            <ElDescriptionsItem label="中单净流入">{{ formatAmount(data.fund_flow.medium_net_inflow) }}</ElDescriptionsItem>
            <ElDescriptionsItem label="小单净流入">{{ formatAmount(data.fund_flow.small_net_inflow) }}</ElDescriptionsItem>
          </ElDescriptions>
          <ElEmpty v-else description="暂无资金流向数据" :image-size="60" />
        </ElCard>
      </ElCol>

      <!-- 融资融券 -->
      <ElCol :span="12">
        <ElCard shadow="never" class="info-card">
          <template #header>
            <span class="card-title">融资融券</span>
          </template>
          <ElTable :data="data.margin?.data?.slice(0, 5) || []" stripe size="small" v-if="data.margin?.data?.length > 0">
            <ElTableColumn prop="trade_date" label="日期" width="120" />
            <ElTableColumn prop="financing_balance" label="融资余额" align="right">
              <template #default="{ row }">{{ formatAmount(row.financing_balance) }}</template>
            </ElTableColumn>
            <ElTableColumn prop="financing_buy" label="融资买入" align="right">
              <template #default="{ row }">{{ formatAmount(row.financing_buy) }}</template>
            </ElTableColumn>
            <ElTableColumn prop="securities_balance" label="融券余额" align="right">
              <template #default="{ row }">{{ formatAmount(row.securities_balance) }}</template>
            </ElTableColumn>
          </ElTable>
          <ElEmpty v-else description="暂无融资融券数据" :image-size="60" />
        </ElCard>
      </ElCol>
    </ElRow>

    <!-- 股权质押 -->
    <ElCard shadow="never" class="info-card">
      <template #header>
        <span class="card-title">股权质押</span>
      </template>
      <ElTable :data="data.pledge?.data || []" stripe size="small" v-if="data.pledge?.data?.length > 0">
        <ElTableColumn prop="shareholder" label="股东名称" min-width="150" />
        <ElTableColumn prop="pledged_shares" label="质押股数" width="120" align="right">
          <template #default="{ row }">{{ formatAmount(row.pledged_shares) }}</template>
        </ElTableColumn>
        <ElTableColumn prop="pledged_ratio" label="质押比例" width="100" align="right">
          <template #default="{ row }">{{ formatValue(row.pledged_ratio, '%') }}</template>
        </ElTableColumn>
        <ElTableColumn prop="total_shares" label="持股数量" width="120" align="right">
          <template #default="{ row }">{{ formatAmount(row.total_shares) }}</template>
        </ElTableColumn>
        <ElTableColumn prop="update_date" label="更新日期" width="120" />
      </ElTable>
      <ElEmpty v-else description="暂无股权质押数据" :image-size="60" />
    </ElCard>

    <!-- 限售解禁 -->
    <ElCard shadow="never" class="info-card">
      <template #header>
        <span class="card-title">限售解禁计划</span>
      </template>
      <ElTable :data="data.unlock || []" stripe size="small" v-if="data.unlock?.length > 0">
        <ElTableColumn prop="unlock_date" label="解禁日期" width="120" />
        <ElTableColumn prop="unlock_shares" label="解禁股数" width="120" align="right">
          <template #default="{ row }">{{ formatAmount(row.unlock_shares) }}</template>
        </ElTableColumn>
        <ElTableColumn prop="unlock_ratio" label="解禁比例" width="100" align="right">
          <template #default="{ row }">{{ formatValue(row.unlock_ratio, '%') }}</template>
        </ElTableColumn>
        <ElTableColumn prop="unlock_amount" label="解禁市值" width="120" align="right">
          <template #default="{ row }">{{ formatAmount(row.unlock_amount) }}</template>
        </ElTableColumn>
        <ElTableColumn prop="unlock_type" label="解禁类型" width="120" />
      </ElTable>
      <ElEmpty v-else description="暂无解禁计划" :image-size="60" />
    </ElCard>
  </div>
</template>

<style lang="scss" scoped>
.fund-tab {
  .info-card {
    margin-bottom: 16px;
  }

  .card-title {
    font-size: 15px;
    font-weight: 600;
  }
}

.text-up {
  color: #f56c6c;
}

.text-down {
  color: #67c23a;
}
</style>