<script setup lang="ts">
import {
  ElRow,
  ElCol,
  ElCard,
  ElDescriptions,
  ElDescriptionsItem,
  ElTag,
  ElTable,
  ElTableColumn
} from 'element-plus'

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
  <div class="overview-tab">
    <ElRow :gutter="16">
      <!-- 基本信息 -->
      <ElCol :span="12">
        <ElCard shadow="never" class="info-card">
          <template #header>
            <span class="card-title">基本信息</span>
          </template>
          <ElDescriptions :column="2" border size="small" v-if="data.basic_info">
            <ElDescriptionsItem label="股票代码">{{ data.basic_info.code }}</ElDescriptionsItem>
            <ElDescriptionsItem label="股票名称">{{ data.basic_info.name }}</ElDescriptionsItem>
            <ElDescriptionsItem label="所属行业">{{
              data.basic_info.industry || '-'
            }}</ElDescriptionsItem>
            <ElDescriptionsItem label="上市日期">{{
              data.basic_info.listing_date || '-'
            }}</ElDescriptionsItem>
            <ElDescriptionsItem label="总市值">{{
              formatAmount(data.basic_info.total_market_value)
            }}</ElDescriptionsItem>
            <ElDescriptionsItem label="流通市值">{{
              formatAmount(data.basic_info.circulating_market_value)
            }}</ElDescriptionsItem>
            <ElDescriptionsItem label="总股本"
              >{{ formatAmount(data.basic_info.total_share) }}股</ElDescriptionsItem
            >
            <ElDescriptionsItem label="流通股"
              >{{ formatAmount(data.basic_info.circulating_share) }}股</ElDescriptionsItem
            >
          </ElDescriptions>
          <div v-else class="no-data">暂无基本信息</div>
        </ElCard>
      </ElCol>

      <!-- 行情数据 -->
      <ElCol :span="12">
        <ElCard shadow="never" class="info-card">
          <template #header>
            <span class="card-title">行情数据</span>
          </template>
          <ElDescriptions :column="2" border size="small" v-if="data.quote">
            <ElDescriptionsItem label="最新价">
              <span
                :class="
                  data.quote.change_percent > 0
                    ? 'text-up'
                    : data.quote.change_percent < 0
                    ? 'text-down'
                    : ''
                "
              >
                {{ formatValue(data.quote.price) }}
              </span>
            </ElDescriptionsItem>
            <ElDescriptionsItem label="涨跌幅">
              <span
                :class="
                  data.quote.change_percent > 0
                    ? 'text-up'
                    : data.quote.change_percent < 0
                    ? 'text-down'
                    : ''
                "
              >
                {{ formatValue(data.quote.change_percent, '%') }}
              </span>
            </ElDescriptionsItem>
            <ElDescriptionsItem label="今开">{{ formatValue(data.quote.open) }}</ElDescriptionsItem>
            <ElDescriptionsItem label="昨收">{{
              formatValue(data.quote.pre_close || data.quote.previous_close)
            }}</ElDescriptionsItem>
            <ElDescriptionsItem label="最高">
              <span class="text-up">{{ formatValue(data.quote.high) }}</span>
            </ElDescriptionsItem>
            <ElDescriptionsItem label="最低">
              <span class="text-down">{{ formatValue(data.quote.low) }}</span>
            </ElDescriptionsItem>
            <ElDescriptionsItem label="成交量">{{
              formatAmount(data.quote.volume)
            }}</ElDescriptionsItem>
            <ElDescriptionsItem label="成交额">{{
              formatAmount(data.quote.amount)
            }}</ElDescriptionsItem>
            <ElDescriptionsItem label="换手率">{{
              formatValue(data.quote.turnover_rate, '%')
            }}</ElDescriptionsItem>
            <ElDescriptionsItem label="市盈率">{{
              formatValue(data.quote.pe_ratio)
            }}</ElDescriptionsItem>
            <ElDescriptionsItem label="市净率">{{
              formatValue(data.quote.pb_ratio)
            }}</ElDescriptionsItem>
            <ElDescriptionsItem label="总市值">{{
              formatAmount(data.quote.market_cap)
            }}</ElDescriptionsItem>
          </ElDescriptions>
          <div v-else class="no-data">暂无行情数据</div>
        </ElCard>
      </ElCol>
    </ElRow>

    <!-- 板块概念 -->
    <ElCard shadow="never" class="sector-card">
      <template #header>
        <span class="card-title">板块概念</span>
      </template>
      <div v-if="data.sectors?.sectors?.length > 0" class="sector-tags">
        <ElTag
          v-for="sector in data.sectors.sectors"
          :key="sector.name"
          :type="sector.type === 'industry' ? 'primary' : 'success'"
          class="sector-tag"
        >
          {{ sector.name }}
        </ElTag>
      </div>
      <div v-else class="no-data">暂无板块信息</div>
    </ElCard>

    <!-- 资金流向 -->
    <ElCard shadow="never" class="fund-card">
      <template #header>
        <span class="card-title">资金流向</span>
      </template>
      <ElDescriptions
        :column="4"
        border
        size="small"
        v-if="data.fund_flow?.main_net_inflow !== undefined"
      >
        <ElDescriptionsItem label="主力净流入">
          <span :class="data.fund_flow.main_net_inflow > 0 ? 'text-up' : 'text-down'">
            {{ formatAmount(data.fund_flow.main_net_inflow) }}
          </span>
        </ElDescriptionsItem>
        <ElDescriptionsItem label="主力净占比">{{
          formatValue(data.fund_flow.main_net_inflow_ratio, '%')
        }}</ElDescriptionsItem>
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
        <ElDescriptionsItem label="中单净流入">{{
          formatAmount(data.fund_flow.medium_net_inflow)
        }}</ElDescriptionsItem>
        <ElDescriptionsItem label="小单净流入">{{
          formatAmount(data.fund_flow.small_net_inflow)
        }}</ElDescriptionsItem>
      </ElDescriptions>
      <div v-else class="no-data">暂无资金流向数据</div>
    </ElCard>
  </div>
</template>

<style lang="scss" scoped>
.overview-tab {
  .info-card,
  .sector-card,
  .fund-card {
    margin-bottom: 16px;
  }

  .card-title {
    font-size: 15px;
    font-weight: 600;
  }

  .sector-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;

    .sector-tag {
      margin-bottom: 4px;
    }
  }

  .no-data {
    text-align: center;
    color: #909399;
    padding: 20px 0;
  }
}

.text-up {
  color: #f56c6c;
}

.text-down {
  color: #67c23a;
}
</style>
