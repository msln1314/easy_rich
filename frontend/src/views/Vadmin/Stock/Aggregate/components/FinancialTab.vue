<script setup lang="ts">
import { ElCard, ElTable, ElTableColumn, ElEmpty } from 'element-plus'

defineProps<{
  data: any
}>()

const formatValue = (value: any, suffix: string = '') => {
  if (value === null || value === undefined || value === '') return '-'
  if (typeof value === 'number') return value.toFixed(2) + suffix
  return value + suffix
}
</script>

<template>
  <div class="financial-tab">
    <ElCard shadow="never" class="info-card">
      <template #header>
        <span class="card-title">财务指标</span>
      </template>
      <ElTable :data="data.financial?.data || []" stripe size="small" v-if="data.financial?.data?.length > 0">
        <ElTableColumn prop="report_date" label="报告日期" width="120" fixed />
        <ElTableColumn prop="roe" label="ROE(%)" width="100" align="right">
          <template #default="{ row }">
            <span :class="row.roe > 15 ? 'text-up' : ''">{{ formatValue(row.roe) }}</span>
          </template>
        </ElTableColumn>
        <ElTableColumn prop="roa" label="ROA(%)" width="100" align="right">
          <template #default="{ row }">{{ formatValue(row.roa) }}</template>
        </ElTableColumn>
        <ElTableColumn prop="gross_margin" label="毛利率(%)" width="100" align="right">
          <template #default="{ row }">{{ formatValue(row.gross_margin) }}</template>
        </ElTableColumn>
        <ElTableColumn prop="net_margin" label="净利率(%)" width="100" align="right">
          <template #default="{ row }">{{ formatValue(row.net_margin) }}</template>
        </ElTableColumn>
        <ElTableColumn prop="debt_ratio" label="资产负债率(%)" width="120" align="right">
          <template #default="{ row }">
            <span :class="row.debt_ratio > 70 ? 'text-down' : ''">{{ formatValue(row.debt_ratio) }}</span>
          </template>
        </ElTableColumn>
        <ElTableColumn prop="current_ratio" label="流动比率" width="100" align="right">
          <template #default="{ row }">{{ formatValue(row.current_ratio) }}</template>
        </ElTableColumn>
        <ElTableColumn prop="quick_ratio" label="速动比率" width="100" align="right">
          <template #default="{ row }">{{ formatValue(row.quick_ratio) }}</template>
        </ElTableColumn>
        <ElTableColumn prop="eps" label="每股收益" width="100" align="right">
          <template #default="{ row }">{{ formatValue(row.eps) }}</template>
        </ElTableColumn>
        <ElTableColumn prop="bvps" label="每股净资产" width="100" align="right">
          <template #default="{ row }">{{ formatValue(row.bvps) }}</template>
        </ElTableColumn>
      </ElTable>
      <ElEmpty v-else description="暂无财务数据" :image-size="80" />
    </ElCard>

    <!-- 财务指标说明 -->
    <ElCard shadow="never" class="info-card">
      <template #header>
        <span class="card-title">指标说明</span>
      </template>
      <div class="indicator-desc">
        <ElRow :gutter="20">
          <ElCol :span="8">
            <div class="desc-item">
              <h4>盈利能力</h4>
              <ul>
                <li><strong>ROE</strong>: 净资产收益率，衡量股东权益收益水平，一般高于15%为优秀</li>
                <li><strong>ROA</strong>: 总资产净利率，衡量资产利用效率</li>
                <li><strong>毛利率</strong>: 反映产品竞争力，越高越好</li>
                <li><strong>净利率</strong>: 反映最终盈利能力，越高越好</li>
              </ul>
            </div>
          </ElCol>
          <ElCol :span="8">
            <div class="desc-item">
              <h4>偿债能力</h4>
              <ul>
                <li><strong>资产负债率</strong>: 一般低于70%较为安全</li>
                <li><strong>流动比率</strong>: 一般大于2较好</li>
                <li><strong>速动比率</strong>: 一般大于1较好</li>
              </ul>
            </div>
          </ElCol>
          <ElCol :span="8">
            <div class="desc-item">
              <h4>每股指标</h4>
              <ul>
                <li><strong>每股收益(EPS)</strong>: 公司盈利能力的关键指标</li>
                <li><strong>每股净资产</strong>: 每股股票代表的净资产价值</li>
              </ul>
            </div>
          </ElCol>
        </ElRow>
      </div>
    </ElCard>
  </div>
</template>

<script lang="ts">
import { ElRow, ElCol } from 'element-plus'
</script>

<style lang="scss" scoped>
.financial-tab {
  .info-card {
    margin-bottom: 16px;
  }

  .card-title {
    font-size: 15px;
    font-weight: 600;
  }

  .indicator-desc {
    .desc-item {
      h4 {
        margin: 0 0 12px 0;
        font-size: 14px;
        font-weight: 600;
        color: #303133;
      }

      ul {
        margin: 0;
        padding-left: 16px;

        li {
          font-size: 12px;
          color: #606266;
          line-height: 1.8;

          strong {
            color: #409eff;
          }
        }
      }
    }
  }
}

.text-up {
  color: #f56c6c;
}

.text-down {
  color: #67c23a;
}
</style>