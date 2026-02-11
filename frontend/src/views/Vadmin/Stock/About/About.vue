<template>
  <div class="about-view">
    <div class="about-container">
      <!-- 页面标题 -->
      <div class="page-header">
        <h1 class="page-title">
          <el-icon><InfoFilled /></el-icon>
          关于系统
        </h1>
        <p class="page-subtitle">了解股票数据展示系统的功能特性与技术实现</p>
      </div>

      <!-- 系统简介 -->
      <div class="section-card">
        <h2 class="section-title">系统简介</h2>
        <div class="content-text">
          <p
            >股票数据展示系统是一个基于现代Web技术构建的股票数据分析和预测平台，致力于为用户提供直观、专业的股票数据可视化体验。</p
          >
          <p
            >系统集成了实时数据获取、专业图表展示、智能预测分析等核心功能，帮助用户更好地理解股票市场趋势。</p
          >
        </div>
      </div>

      <!-- 核心功能 -->
      <div class="section-card">
        <h2 class="section-title">核心功能</h2>
        <div class="features-grid">
          <div class="feature-item">
            <div class="feature-icon">📊</div>
            <h3>实时数据展示</h3>
            <p>支持A股市场股票的实时数据查询，包含基本面信息、交易数据等关键指标</p>
          </div>
          <div class="feature-item">
            <div class="feature-icon">📈</div>
            <h3>专业K线图表</h3>
            <p>基于ECharts实现的专业K线图，支持多种技术指标和交互功能</p>
          </div>
          <div class="feature-item">
            <div class="feature-icon">🔮</div>
            <h3>智能预测分析</h3>
            <p>运用时间序列分析算法，为用户提供股票价格走势预测参考</p>
          </div>
        </div>
      </div>

      <!-- 技术架构 -->
      <div class="section-card">
        <h2 class="section-title">技术架构</h2>

        <!-- 架构图示 -->
        <div class="architecture-diagram">
          <div class="arch-layer">
            <div class="layer-title">前端展示层</div>
            <div class="layer-components">
              <div class="component-box">Vue 3 + Composition API</div>
              <div class="component-box">Element Plus UI</div>
              <div class="component-box">ECharts 可视化</div>
            </div>
          </div>
          <div class="arch-arrow">↓</div>
          <div class="arch-layer">
            <div class="layer-title">API 接口层</div>
            <div class="layer-components">
              <div class="component-box">RESTful API</div>
              <div class="component-box">HTTP 通信</div>
              <div class="component-box">响应式数据流</div>
            </div>
          </div>
          <div class="arch-arrow">↓</div>
          <div class="arch-layer">
            <div class="layer-title">业务逻辑层</div>
            <div class="layer-components">
              <div class="component-box">FastAPI 框架</div>
              <div class="component-box">预测算法引擎</div>
              <div class="component-box">数据处理服务</div>
            </div>
          </div>
          <div class="arch-arrow">↓</div>
          <div class="arch-layer">
            <div class="layer-title">数据获取层</div>
            <div class="layer-components">
              <div class="component-box">AKShare 接口</div>
              <div class="component-box">实时数据源</div>
              <div class="component-box">历史数据缓存</div>
            </div>
          </div>
        </div>

        <div class="tech-details">
          <div class="tech-category">
            <h3>🎨 前端技术栈</h3>
            <div class="tech-description">
              <div class="tech-item">
                <span class="tech-tag">Vue 3</span>
                <span class="tech-desc">采用Composition API，提供更好的代码组织和类型支持</span>
              </div>
              <div class="tech-item">
                <span class="tech-tag">Element Plus</span>
                <span class="tech-desc">基于Vue 3的企业级UI组件库，提供丰富的交互组件</span>
              </div>
              <div class="tech-item">
                <span class="tech-tag">ECharts 5</span>
                <span class="tech-desc">专业图表库，支持K线图、折线图等金融图表类型</span>
              </div>
              <div class="tech-item">
                <span class="tech-tag">Vite</span>
                <span class="tech-desc">下一代前端构建工具，提供极速的开发体验</span>
              </div>
              <div class="tech-item">
                <span class="tech-tag">Pinia</span>
                <span class="tech-desc">Vue 3官方推荐的状态管理库，轻量且类型安全</span>
              </div>
            </div>
          </div>

          <div class="tech-category">
            <h3>⚙️ 后端技术栈</h3>
            <div class="tech-description">
              <div class="tech-item">
                <span class="tech-tag">FastAPI</span>
                <span class="tech-desc"
                  >现代Python Web框架，自动生成OpenAPI文档，高性能异步支持</span
                >
              </div>
              <div class="tech-item">
                <span class="tech-tag">Python 3.8+</span>
                <span class="tech-desc">强大的数据处理和科学计算生态系统</span>
              </div>
              <div class="tech-item">
                <span class="tech-tag">AKShare</span>
                <span class="tech-desc">专业金融数据接口，提供A股、港股、美股等市场数据</span>
              </div>
              <div class="tech-item">
                <span class="tech-tag">Pandas</span>
                <span class="tech-desc">数据分析和处理库，高效处理时间序列数据</span>
              </div>
              <div class="tech-item">
                <span class="tech-tag">NumPy</span>
                <span class="tech-desc">科学计算基础库，提供高性能数组计算</span>
              </div>
              <div class="tech-item">
                <span class="tech-tag">Kronos</span>
                <span class="tech-desc">专用时间序列预测模型，集成深度学习与传统统计方法</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 预测算法与模型 -->
      <div class="section-card">
        <h2 class="section-title">预测算法与模型</h2>

        <!-- 算法概述 -->
        <div class="algorithm-overview">
          <div class="algo-intro">
            <h3>🧠 Kronos 预测模型</h3>
            <p class="algo-description">
              系统采用
              <strong>Kronos</strong> 时间序列预测模型，通过分析历史股票价格数据的规律和趋势，
              预测未来的价格走势。该模型专门针对金融数据优化，能够识别价格变化的模式。
            </p>
          </div>
        </div>

        <!-- 工作流程 -->
        <div class="model-architecture">
          <h3>🏗️ 预测工作流程</h3>
          <div class="model-flow">
            <div class="model-step">
              <div class="step-icon">📊</div>
              <div class="step-content">
                <h4>数据准备</h4>
                <p>获取和清理历史股票数据</p>
              </div>
            </div>

            <div class="flow-arrow">→</div>

            <div class="model-step">
              <div class="step-icon">🔍</div>
              <div class="step-content">
                <h4>模式分析</h4>
                <p>识别价格变化的规律和趋势</p>
              </div>
            </div>

            <div class="flow-arrow">→</div>

            <div class="model-step">
              <div class="step-icon">🎯</div>
              <div class="step-content">
                <h4>生成预测</h4>
                <p>预测未来价格和置信区间</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Kronos模型特点 -->
        <div class="algorithm-details">
          <h3>✨ Kronos 模型特点</h3>
          <div class="algo-methods">
            <div class="method-card">
              <div class="method-header">
                <span class="method-icon">🎯</span>
                <h4>智能分析</h4>
              </div>
              <div class="method-content">
                <p>自动识别股票价格的变化模式和趋势</p>
              </div>
            </div>

            <div class="method-card">
              <div class="method-header">
                <span class="method-icon">⚡</span>
                <h4>快速预测</h4>
              </div>
              <div class="method-content">
                <p>基于历史数据快速生成未来价格预测</p>
              </div>
            </div>

            <div class="method-card">
              <div class="method-header">
                <span class="method-icon">🔒</span>
                <h4>置信评估</h4>
              </div>
              <div class="method-content">
                <p>提供预测结果的可信度区间，量化不确定性</p>
              </div>
            </div>
          </div>
        </div>

        <!-- 重要说明 -->
        <div class="algorithm-limitations">
          <h3>⚠️ 预测说明</h3>
          <div class="limitation-notice">
            <div class="notice-content">
              <p>📌 <strong>基于历史数据：</strong>预测结果基于历史价格分析，仅供参考</p>
              <p>📌 <strong>存在不确定性：</strong>股票市场复杂多变，预测结果不保证准确性</p>
              <p>📌 <strong>仅供学习：</strong>本系统仅用于技术学习和数据分析研究</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 使用指南 -->
      <div class="section-card">
        <h2 class="section-title">使用指南</h2>
        <div class="guide-steps">
          <div class="step-item">
            <div class="step-number">1</div>
            <div class="step-content">
              <h4>输入股票代码</h4>
              <p>在搜索框中输入6位股票代码或带市场前缀的代码（如：000001 或 sz.000001）</p>
            </div>
          </div>
          <div class="step-item">
            <div class="step-number">2</div>
            <div class="step-content">
              <h4>查看数据信息</h4>
              <p>系统将展示股票的基本信息、交易数据和专业K线图表</p>
            </div>
          </div>
          <div class="step-item">
            <div class="step-number">3</div>
            <div class="step-content">
              <h4>启用预测功能</h4>
              <p>选择预测天数和历史数据量，获取智能分析预测结果</p>
            </div>
          </div>
          <div class="step-item">
            <div class="step-number">4</div>
            <div class="step-content">
              <h4>分析结果展示</h4>
              <p>在表格视图和图表视图间切换，全方位分析预测数据</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 免责声明 -->
      <div class="section-card disclaimer-card">
        <h2 class="section-title">重要声明</h2>
        <div class="disclaimer-content">
          <div class="warning-notice">
            <el-icon><WarningFilled /></el-icon>
            <span>本系统仅供学习交流使用</span>
          </div>
          <ul class="disclaimer-list">
            <li>所有预测结果基于历史数据分析，不构成投资建议</li>
            <li>股票投资存在风险，过往表现不代表未来收益</li>
            <li>用户应当独立判断并承担投资风险</li>
            <li>系统开发目的为技术学习和数据分析研究</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ElIcon } from 'element-plus'
import { InfoFilled, WarningFilled } from '@element-plus/icons-vue'
</script>

<style scoped>
.about-view {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

.about-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.page-header {
  text-align: center;
  padding: 40px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  color: white;
  margin-bottom: 8px;
}

.page-title {
  font-size: 32px;
  font-weight: 700;
  margin: 0 0 12px 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

.page-subtitle {
  font-size: 16px;
  margin: 0;
  opacity: 0.9;
  font-weight: 400;
}

.section-card {
  background: white;
  border-radius: 12px;
  padding: 32px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid #f0f0f0;
  transition: all 0.3s ease;
}

.section-card:hover {
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
  transform: translateY(-2px);
}

.section-title {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 20px 0;
  border-bottom: 2px solid #409eff;
  padding-bottom: 8px;
  display: inline-block;
}

.content-text {
  line-height: 1.8;
  color: #606266;
  font-size: 16px;
}

.content-text p {
  margin: 0 0 16px 0;
}

.content-text strong {
  color: #409eff;
  font-weight: 600;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
  margin-top: 8px;
}

.feature-item {
  padding: 24px;
  background: linear-gradient(135deg, #f8f9ff 0%, #f0f4ff 100%);
  border-radius: 8px;
  border: 1px solid #e6f0ff;
  text-align: center;
  transition: all 0.3s ease;
}

.feature-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(64, 158, 255, 0.15);
}

.feature-icon {
  font-size: 32px;
  margin-bottom: 12px;
}

.feature-item h3 {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 8px 0;
}

.feature-item p {
  font-size: 14px;
  color: #606266;
  line-height: 1.6;
  margin: 0;
}

.tech-stack {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 32px;
  margin-top: 8px;
}

.tech-category h3 {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 16px 0;
}

.tech-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

/* 架构图样式 */
.architecture-diagram {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  margin: 24px 0;
  padding: 20px;
  background: linear-gradient(135deg, #f8f9ff 0%, #f0f4ff 100%);
  border-radius: 8px;
  border: 1px solid #e6f0ff;
}

.arch-layer {
  text-align: center;
  min-width: 300px;
}

.layer-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 8px;
  padding: 8px 16px;
  background: #409eff;
  color: white;
  border-radius: 20px;
  display: inline-block;
}

.layer-components {
  display: flex;
  justify-content: center;
  gap: 8px;
  flex-wrap: wrap;
}

.component-box {
  background: white;
  padding: 8px 12px;
  border-radius: 6px;
  font-size: 12px;
  color: #409eff;
  border: 1px solid #409eff;
  font-weight: 500;
}

.arch-arrow {
  font-size: 20px;
  color: #409eff;
  font-weight: bold;
}

/* 技术详情样式 */
.tech-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
  gap: 32px;
  margin-top: 32px;
}

.tech-description {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.tech-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}

.tech-item:last-child {
  border-bottom: none;
}

.tech-tag {
  background: linear-gradient(135deg, #409eff 0%, #79bbff 100%);
  color: white;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
  min-width: 80px;
  text-align: center;
}

.tech-desc {
  font-size: 13px;
  color: #606266;
  line-height: 1.5;
}

/* 算法概述样式 */
.algorithm-overview {
  margin-bottom: 32px;
}

.algo-intro h3 {
  font-size: 18px;
  color: #303133;
  margin: 0 0 12px 0;
}

.algo-description {
  font-size: 15px;
  line-height: 1.7;
  color: #606266;
  margin: 0;
  padding: 16px;
  background: linear-gradient(135deg, #f8f9ff 0%, #f0f4ff 100%);
  border-radius: 8px;
  border-left: 4px solid #409eff;
}

/* 模型架构样式 */
.model-architecture {
  margin-bottom: 32px;
}

.model-flow {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  margin: 20px 0;
  flex-wrap: wrap;
}

.model-step {
  background: white;
  border: 2px solid #409eff;
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  min-width: 200px;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.1);
}

.step-icon {
  font-size: 24px;
  margin-bottom: 8px;
}

.step-content h4 {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 12px 0;
}

.step-content p {
  font-size: 13px;
  color: #606266;
  margin: 0;
  line-height: 1.4;
}

.flow-arrow {
  font-size: 24px;
  color: #409eff;
  font-weight: bold;
}

/* 算法详解样式 */
.algorithm-details {
  margin-bottom: 32px;
}

.algo-methods {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
  margin-top: 16px;
}

.method-card {
  background: white;
  border: 1px solid #e6f0ff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.method-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 20px rgba(64, 158, 255, 0.15);
}

.method-header {
  background: linear-gradient(135deg, #409eff 0%, #79bbff 100%);
  color: white;
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.method-icon {
  font-size: 20px;
}

.method-header h4 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
}

.method-content {
  padding: 16px;
}

.method-content p {
  margin: 0 0 8px 0;
  font-size: 13px;
  line-height: 1.5;
  color: #606266;
}

.method-content strong {
  color: #409eff;
}

/* 模型特性样式 */
.model-features {
  margin-bottom: 32px;
}

.features-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-top: 16px;
}

.feature-point {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
  background: linear-gradient(135deg, #f8f9ff 0%, #f0f4ff 100%);
  border-radius: 8px;
  border: 1px solid #e6f0ff;
}

.feature-bullet {
  font-size: 16px;
  flex-shrink: 0;
}

.feature-text {
  font-size: 14px;
  line-height: 1.6;
  color: #606266;
}

.feature-text strong {
  color: #409eff;
}

/* 算法局限性样式 */
.algorithm-limitations {
  margin-bottom: 32px;
}

.limitation-notice {
  background: linear-gradient(135deg, #fff7e6 0%, #fef1e6 100%);
  border: 1px solid #ffd591;
  border-radius: 8px;
  padding: 20px;
  margin-top: 16px;
}

.notice-content p {
  margin: 0 0 12px 0;
  font-size: 14px;
  line-height: 1.6;
  color: #d46b08;
}

.notice-content p:last-child {
  margin-bottom: 0;
}

/* 数据流程样式 */
.data-source-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.data-flow {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  flex-wrap: wrap;
}

.data-step {
  background: linear-gradient(135deg, #f8f9ff 0%, #f0f4ff 100%);
  border: 2px solid #409eff;
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  min-width: 180px;
}

.data-icon {
  font-size: 24px;
  margin-bottom: 8px;
}

.data-step h4 {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 8px 0;
}

.data-step p {
  font-size: 13px;
  color: #606266;
  margin: 0;
  line-height: 1.4;
}

.data-arrow {
  font-size: 20px;
  color: #409eff;
  font-weight: bold;
}

.data-details {
  background: #fafafa;
  border-radius: 8px;
  padding: 20px;
}

.data-details h4 {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 12px 0;
}

.data-details ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.data-details li {
  padding: 6px 0;
  font-size: 14px;
  color: #606266;
  line-height: 1.5;
  border-bottom: 1px solid #f0f0f0;
}

.data-details li:last-child {
  border-bottom: none;
}

.data-details strong {
  color: #409eff;
}

/* Kronos模型优势样式 */
.kronos-advantages {
  margin-bottom: 32px;
}

.advantages-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
  margin-top: 16px;
}

.advantage-card {
  background: white;
  border: 2px solid #409eff;
  border-radius: 12px;
  padding: 24px;
  text-align: center;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.1);
}

.advantage-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 8px 24px rgba(64, 158, 255, 0.2);
  border-color: #79bbff;
}

.advantage-icon {
  font-size: 32px;
  margin-bottom: 16px;
  display: block;
}

.advantage-card h4 {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 12px 0;
}

.advantage-card p {
  font-size: 14px;
  color: #606266;
  line-height: 1.6;
  margin: 0;
}

.guide-steps {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-top: 8px;
}

.step-item {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 20px;
  background: #fafafa;
  border-radius: 8px;
  border-left: 4px solid #409eff;
}

.step-number {
  background: #409eff;
  color: white;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 14px;
  flex-shrink: 0;
}

.step-content h4 {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 8px 0;
}

.step-content p {
  font-size: 14px;
  color: #606266;
  line-height: 1.6;
  margin: 0;
}

.disclaimer-card {
  background: linear-gradient(135deg, #fff7e6 0%, #fef1e6 100%);
  border: 1px solid #ffd591;
}

.disclaimer-card .section-title {
  border-bottom-color: #fa8c16;
  color: #ad4e00;
}

.warning-notice {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: #ad4e00;
  margin-bottom: 16px;
}

.disclaimer-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.disclaimer-list li {
  padding: 8px 0;
  color: #d46b08;
  font-size: 14px;
  line-height: 1.6;
  position: relative;
  padding-left: 20px;
}

.disclaimer-list li:before {
  content: '•';
  position: absolute;
  left: 0;
  color: #fa8c16;
  font-weight: bold;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .about-view {
    padding: 12px;
  }

  .page-header {
    padding: 24px 16px;
  }

  .page-title {
    font-size: 24px;
  }

  .page-subtitle {
    font-size: 14px;
  }

  .section-card {
    padding: 20px;
  }

  .section-title {
    font-size: 20px;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }

  .tech-details {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .tech-item {
    flex-direction: column;
    gap: 8px;
  }

  .architecture-diagram {
    padding: 12px;
  }

  .layer-components {
    flex-direction: column;
    gap: 6px;
  }

  .model-flow {
    flex-direction: column;
  }

  .flow-arrow {
    transform: rotate(90deg);
  }

  .model-step {
    min-width: auto;
    width: 100%;
  }

  .algo-methods {
    grid-template-columns: 1fr;
  }

  .advantages-grid {
    grid-template-columns: 1fr;
  }

  .data-flow {
    flex-direction: column;
  }

  .data-arrow {
    transform: rotate(90deg);
  }

  .data-step {
    min-width: auto;
    width: 100%;
  }

  .step-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
}
</style>
