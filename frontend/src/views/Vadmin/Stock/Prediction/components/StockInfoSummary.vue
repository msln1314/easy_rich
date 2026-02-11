<template>
  <div class="stock-info-summary">
    <!-- 股票基本信息卡片 -->
    <div class="info-card basic-info">
      <div class="card-header">
        <div class="header-content">
          <div class="header-icon">📊</div>
          <h3>股票基本信息</h3>
        </div>
        <div class="card-badge">基础</div>
      </div>
      <div class="card-content">
        <div class="info-grid">
          <div
            class="info-item"
            :class="{
              primary: item.type === 'primary',
              highlight: item.type === 'highlight'
            }"
            v-for="item in basicInfoItems"
            :key="item.key"
          >
            <label>{{ item.label }}</label>
            <span class="info-value" :class="item.changeClass">{{ item.value }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 交易行情信息卡片 -->
    <div class="info-card trading-info">
      <div class="card-header">
        <div class="header-content">
          <div class="header-icon">📈</div>
          <h3>交易行情信息</h3>
        </div>
        <div class="card-badge trading">行情</div>
      </div>
      <div class="card-content">
        <div class="info-grid">
          <div
            class="info-item"
            :class="{
              highlight: item.type === 'highlight',
              extreme: item.type.includes('extreme')
            }"
            v-for="item in tradingInfoItems"
            :key="item.key"
          >
            <label>{{ item.label }}</label>
            <span
              class="info-value"
              :class="{
                high: item.type === 'extreme-high',
                low: item.type === 'extreme-low'
              }"
              >{{ item.value }}</span
            >
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import {
  formatPrice,
  formatChangeAmount,
  formatChangePercent,
  formatVolume,
  formatTurnover,
  formatPercent,
  formatRatio,
  getChangeClass
} from '@/utils/stockUtils'

const props = defineProps({
  stockInfo: {
    type: Object,
    default: () => ({})
  }
})

const basicInfoItems = computed(() => [
  { key: 'code', label: '股票代码', value: props.stockInfo.code || '--', type: 'primary' },
  { key: 'name', label: '股票名称', value: props.stockInfo.name || '--', type: 'primary' },
  { key: 'industry', label: '所属行业', value: props.stockInfo.industry || '--', type: 'normal' },
  { key: 'market', label: '交易市场', value: props.stockInfo.market || '--', type: 'normal' },
  {
    key: 'avg_price',
    label: '均价',
    value: formatPrice(props.stockInfo.avg_price),
    type: 'normal'
  },
  {
    key: 'change_amount',
    label: '涨跌额',
    value: formatChangeAmount(props.stockInfo.change_amount),
    type: 'change',
    changeClass: getChangeClass(props.stockInfo.change_amount)
  },
  {
    key: 'current_price',
    label: '最新价',
    value: formatPrice(props.stockInfo.current_price),
    type: 'highlight'
  },
  {
    key: 'change_percent',
    label: '涨跌幅',
    value: formatChangePercent(props.stockInfo.change_percent),
    type: 'change',
    changeClass: getChangeClass(props.stockInfo.change_percent)
  }
])

const tradingInfoItems = computed(() => [
  { key: 'open', label: '开盘价', value: formatPrice(props.stockInfo.open), type: 'normal' },
  { key: 'high', label: '最高价', value: formatPrice(props.stockInfo.high), type: 'extreme-high' },
  { key: 'low', label: '最低价', value: formatPrice(props.stockInfo.low), type: 'extreme-low' },
  {
    key: 'pre_close',
    label: '昨收价',
    value: formatPrice(props.stockInfo.pre_close),
    type: 'normal'
  },
  {
    key: 'volume',
    label: '成交量(手)',
    value: formatVolume(props.stockInfo.volume),
    type: 'normal'
  },
  {
    key: 'turnover',
    label: '成交额',
    value: formatTurnover(props.stockInfo.turnover),
    type: 'normal'
  },
  {
    key: 'turnover_rate',
    label: '换手率',
    value: formatPercent(props.stockInfo.turnover_rate),
    type: 'highlight'
  },
  {
    key: 'volume_ratio',
    label: '量比',
    value: formatRatio(props.stockInfo.volume_ratio),
    type: 'highlight'
  }
])
</script>

<style scoped>
.stock-info-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 20px;
}

/* 手机端适配 */
@media (max-width: 768px) {
  .stock-info-summary {
    grid-template-columns: 1fr;
    gap: 16px;
    padding: 0 8px;
  }
}

/* 卡片样式 */
.info-card {
  position: relative;
  border: 1px solid #e4e7ed;
  border-radius: 20px;
  background: #fff;
  transition: all 0.3s ease;
  overflow: hidden;
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.06);
}

.info-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  opacity: 0;
  transition: all 0.3s ease;
}

.info-card:hover {
  border-color: #409eff;
  box-shadow: 0 8px 32px rgba(64, 158, 255, 0.12);
  transform: translateY(-4px);
}

.info-card:hover::before {
  opacity: 1;
}

.basic-info::before {
  background: linear-gradient(90deg, #667eea, #764ba2);
}

.trading-info::before {
  background: linear-gradient(90deg, #f093fb, #f5576c);
}

/* 卡片头部 */
.card-header {
  padding: 24px 28px 20px;
  border-bottom: 1px solid #f0f2f5;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.9), rgba(250, 250, 250, 0.5));
}

/* 手机端卡片头部优化 */
@media (max-width: 768px) {
  .card-header {
    padding: 16px 20px 14px;
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }

  .header-content {
    width: 100%;
    justify-content: space-between;
  }

  .card-badge {
    align-self: flex-end;
  }
}

.header-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.header-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: linear-gradient(135deg, #409eff, #79bbff);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
}

.header-content h3 {
  margin: 0;
  font-size: 20px;
  font-weight: 700;
  color: #303133;
}

/* 手机端头部图标和标题优化 */
@media (max-width: 768px) {
  .header-icon {
    width: 40px;
    height: 40px;
    font-size: 20px;
    border-radius: 10px;
  }

  .header-content h3 {
    font-size: 18px;
  }

  .header-content {
    gap: 12px;
  }
}

@media (max-width: 480px) {
  .header-icon {
    width: 36px;
    height: 36px;
    font-size: 18px;
    border-radius: 8px;
  }

  .header-content h3 {
    font-size: 16px;
  }

  .header-content {
    gap: 10px;
  }
}

.card-badge {
  padding: 6px 12px;
  border-radius: 20px;
  background: linear-gradient(135deg, #409eff, #79bbff);
  color: white;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  box-shadow: 0 2px 8px rgba(64, 158, 255, 0.3);
}

.card-badge.trading {
  background: linear-gradient(135deg, #f093fb, #f5576c);
  box-shadow: 0 2px 8px rgba(240, 147, 251, 0.3);
}

.card-content {
  padding: 24px 28px;
}

/* 手机端卡片内容优化 */
@media (max-width: 768px) {
  .card-content {
    padding: 16px 20px;
  }
}

@media (max-width: 480px) {
  .card-content {
    padding: 12px 16px;
  }
}

/* 信息网格 */
.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 16px;
}

/* 平板端适配 */
@media (max-width: 1024px) {
  .info-grid {
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 14px;
  }
}

/* 手机端适配 */
@media (max-width: 768px) {
  .info-grid {
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 12px;
  }
}

@media (max-width: 480px) {
  .info-grid {
    grid-template-columns: 1fr 1fr;
    gap: 10px;
  }
}

/* 信息项样式 */
.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 18px 20px;
  border-radius: 12px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.9), rgba(250, 250, 250, 0.6));
  border: 1px solid #f0f2f5;
  transition: all 0.3s ease;
  position: relative;
}

/* 手机端信息项优化 */
@media (max-width: 768px) {
  .info-item {
    padding: 14px 16px;
    border-radius: 10px;
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
    min-height: auto;
  }
}

@media (max-width: 480px) {
  .info-item {
    padding: 12px 14px;
    border-radius: 8px;
    gap: 6px;
  }
}

.info-item:hover {
  background: linear-gradient(135deg, rgba(255, 255, 255, 1), rgba(250, 250, 250, 0.8));
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border-color: #409eff;
}

/* 特殊项目样式 */
.info-item.primary {
  background: linear-gradient(135deg, rgba(64, 158, 255, 0.08), rgba(64, 158, 255, 0.03));
  border: 1px solid rgba(64, 158, 255, 0.2);
}

.info-item.primary::before {
  background: #409eff;
}

.info-item.highlight {
  background: linear-gradient(135deg, rgba(64, 158, 255, 0.12), rgba(64, 158, 255, 0.06));
  border: 2px solid rgba(64, 158, 255, 0.3);
}

.info-item.highlight::before {
  background: linear-gradient(180deg, #409eff, #79bbff);
  width: 4px;
}

.info-item.extreme::after {
  content: '';
  position: absolute;
  right: 8px;
  top: 8px;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #409eff;
  animation: blink 2s infinite;
}

/* 标签样式 */
.info-item label {
  font-size: 14px;
  color: #606266;
  font-weight: 600;
  display: flex;
  align-items: center;
  position: relative;
}

/* 手机端标签优化 */
@media (max-width: 768px) {
  .info-item label {
    font-size: 13px;
    margin-bottom: 2px;
  }
}

@media (max-width: 480px) {
  .info-item label {
    font-size: 12px;
  }
}

.info-item label::before {
  content: '';
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #409eff;
  margin-right: 10px;
  transition: all 0.3s ease;
}

.info-item:hover label::before {
  background: #79bbff;
  transform: scale(1.2);
}

/* 数值样式 */
.info-value {
  font-size: 15px;
  color: #303133;
  font-weight: 700;
  text-align: right;
  letter-spacing: 0.3px;
  transition: all 0.3s ease;
}

/* 手机端数值优化 */
@media (max-width: 768px) {
  .info-value {
    font-size: 14px;
    text-align: left;
    width: 100%;
  }
}

@media (max-width: 480px) {
  .info-value {
    font-size: 13px;
  }
}

/* 特殊数值样式 */
.info-value.high {
  color: #f56c6c;
  font-weight: 800;
  background: linear-gradient(135deg, rgba(245, 108, 108, 0.1), rgba(245, 108, 108, 0.05));
  padding: 4px 8px;
  border-radius: 6px;
}

.info-value.low {
  color: #67c23a;
  font-weight: 800;
  background: linear-gradient(135deg, rgba(103, 194, 58, 0.1), rgba(103, 194, 58, 0.05));
  padding: 4px 8px;
  border-radius: 6px;
}

/* 涨跌状态样式 */
.price-up,
.price-down,
.price-neutral {
  font-weight: 800;
  border-radius: 8px;
  padding: 6px 12px;
}

.price-up {
  color: #f56c6c;
  background: linear-gradient(135deg, rgba(245, 108, 108, 0.15), rgba(245, 108, 108, 0.08));
  border: 1px solid rgba(245, 108, 108, 0.3);
}

.price-up::before {
  content: '↗ ';
}

.price-down {
  color: #67c23a;
  background: linear-gradient(135deg, rgba(103, 194, 58, 0.15), rgba(103, 194, 58, 0.08));
  border: 1px solid rgba(103, 194, 58, 0.3);
}

.price-down::before {
  content: '↘ ';
}

.price-neutral {
  color: #909399;
  background: linear-gradient(135deg, rgba(144, 147, 153, 0.1), rgba(144, 147, 153, 0.05));
  border: 1px solid rgba(144, 147, 153, 0.2);
}

.price-neutral::before {
  content: '→ ';
}

@keyframes blink {
  0%,
  50% {
    opacity: 1;
  }
  51%,
  100% {
    opacity: 0.3;
  }
}
</style>
