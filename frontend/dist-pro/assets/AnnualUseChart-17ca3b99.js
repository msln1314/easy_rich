import { _ as a } from './Echart.vue_vue_type_script_setup_true_name_ECharts_lang-3e84099f.js'
import { e, o, j as t, x as l, k as r, J as s } from './index-820a519e.js'
import './echarts-ef988edf.js'
const n = { class: 'echarts' },
  i = s(
    e({
      __name: 'AnnualUseChart',
      setup(e) {
        const s = ['rgba(254, 219, 101,0.1)', 'rgba(0, 122, 254,0.1)', 'rgba(255, 75, 122, 0.1)'],
          i = [
            {
              label: new Date().getFullYear() - 2 + '年',
              value: ['184', '90', '120', '0', '30', '100', '80', '40', '20', '510', '350', '180']
            },
            {
              label: new Date().getFullYear() - 1 + '年',
              value: [
                '118',
                '509',
                '366',
                '162',
                '380',
                '123',
                '321',
                '158',
                '352',
                '474',
                '154',
                '22'
              ]
            },
            {
              label: new Date().getFullYear() + '年',
              value: ['548', '259', '113', '90', '69', '512', '23', '49', '28', '420', '313', '156']
            }
          ],
          c = {
            data: i,
            unit: i.map((a) => a.label),
            columns: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
            colors: ['#FFA600', '#007AFE', '#FF4B7A']
          },
          d = {
            tooltip: {
              trigger: 'axis',
              axisPointer: { type: 'none' },
              borderWidth: 0,
              padding: 0,
              backgroundColor: 'transparent',
              formatter: (a) => {
                let e = ''
                a.forEach((a) => {
                  e += `\n          <div class="year-item">\n            <span class="year-dot" style="background-color: ${a.color};"></span>\n            <span class="year-name">${a.seriesName}</span>\n            <span class="year-value">${a.data >= 1e4 ? (a.data / 1e4).toFixed(2) + 'w' : a.data}</span>\n          </div>\n          `
                })
                return `\n                    <div class="annual-tooltip">\n                      <span class="annual-month">${a[0].dataIndex + 1}月</span>\n                      <div class="annual-list">\n                        ${e}\n                      </div>\n                    </div>\n                  `
              }
            },
            legend: {
              right: '2%',
              top: '0%',
              itemWidth: 15,
              itemHeight: 6,
              align: 'auto',
              icon: 'rect',
              itemGap: 15,
              textStyle: { color: '#ebebf0' }
            },
            grid: { top: '20%', left: '40', right: '4%', bottom: '15%' },
            xAxis: [
              {
                name: '(月份)',
                type: 'category',
                boundaryGap: !1,
                axisLine: { show: !0, lineStyle: { color: '#233653' } },
                axisLabel: {
                  color: '#7ec7ff',
                  padding: 0,
                  fontSize: 12,
                  formatter: function (a) {
                    return a
                  }
                },
                splitLine: { show: !1, lineStyle: { color: '#192a44' } },
                axisTick: { show: !1 },
                data: c.columns
              }
            ],
            yAxis: {
              name: '(人数)',
              nameTextStyle: { color: '#D6DFEA', fontSize: 12, padding: [0, 30, 0, 0] },
              minInterval: 1,
              splitNumber: 5,
              splitLine: { show: !1, lineStyle: { color: '#192a44' } },
              axisLine: { show: !0, lineStyle: { color: '#233653' } },
              axisLabel: { show: !0, color: '#B9D6D6', padding: 0 },
              axisTick: { show: !1 }
            },
            series: c.data.map((a, e) => ({
              name: a.label,
              type: 'line',
              symbol: 'circle',
              showSymbol: !1,
              smooth: !0,
              lineStyle: { width: 1, color: c.colors[e], borderColor: c.colors[e] },
              itemStyle: { color: c.colors[e], borderColor: '#646ace', borderWidth: 2 },
              tooltip: { show: !0 },
              areaStyle: {
                color: {
                  type: 'linear',
                  x: 0,
                  y: 0,
                  x2: 0,
                  y2: 1,
                  colorStops: [
                    { offset: 0, color: c.colors[e] },
                    { offset: 1, color: s[e] }
                  ],
                  global: !1
                },
                shadowColor: 'rgba(25,163,223, 0.3)',
                shadowBlur: 20
              },
              data: a.value
            }))
          }
        return (e, s) => (o(), t('div', n, [l(r(a), { option: d, resize: !1 })]))
      }
    }),
    [['__scopeId', 'data-v-3df43777']]
  )
export { i as default }
