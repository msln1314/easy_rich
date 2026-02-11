import { _ as e } from './Echart.vue_vue_type_script_setup_true_name_ECharts_lang-3e84099f.js'
import { e as t, o as a, j as r, x as o, k as n, J as i } from './index-820a519e.js'
import './echarts-ef988edf.js'
const l = { class: 'echarts' },
  s = i(
    t({
      __name: 'AgeRatioChart',
      setup(t) {
        let i = [
          { value: 200, name: '10岁以下', percentage: '16%' },
          { value: 110, name: '10 - 18岁', percentage: '8%' },
          { value: 150, name: '18 - 30岁', percentage: '12%' },
          { value: 310, name: '30 - 40岁', percentage: '24%' },
          { value: 250, name: '40 - 60岁', percentage: '20%' },
          { value: 260, name: '60岁以上', percentage: '20%' }
        ]
        const s = ['#F6C95C', '#EF7D33', '#1F9393', '#184EA1', '#81C8EF', '#9270CA'],
          c = {
            color: s,
            tooltip: { show: !0, trigger: 'item', formatter: '{b} <br/>占比：{d}%' },
            legend: {
              orient: 'vertical',
              right: '20px',
              top: '15px',
              itemGap: 15,
              itemWidth: 14,
              formatter: function (e) {
                let t = ''
                return (
                  i.forEach((a) => {
                    a.name === e && (t = ' ' + e + '　 ' + a.percentage)
                  }),
                  t
                )
              },
              textStyle: { color: '#fff' }
            },
            grid: { top: 'bottom', left: 10, bottom: 10 },
            series: [
              {
                zlevel: 1,
                name: '年龄比例',
                type: 'pie',
                selectedMode: 'single',
                radius: [50, 90],
                center: ['35%', '50%'],
                startAngle: 60,
                label: {
                  position: 'inside',
                  show: !0,
                  color: '#fff',
                  formatter: function (e) {
                    return e.data.percentage
                  },
                  rich: { b: { fontSize: 16, lineHeight: 30, color: '#fff' } }
                },
                itemStyle: { shadowColor: 'rgba(0, 0, 0, 0.2)', shadowBlur: 10 },
                data: i.map((e, t) => ({
                  value: e.value,
                  name: e.name,
                  percentage: e.percentage,
                  itemStyle: {
                    borderWidth: 10,
                    shadowBlur: 20,
                    borderColor: s[t],
                    borderRadius: 10
                  }
                }))
              },
              {
                name: '',
                type: 'pie',
                selectedMode: 'single',
                radius: [50, 90],
                center: ['35%', '50%'],
                startAngle: 60,
                data: [
                  {
                    value: 1e3,
                    name: '',
                    label: {
                      show: !0,
                      formatter: '{a|本日总数}',
                      rich: { a: { align: 'center', color: 'rgb(98,137,169)', fontSize: 14 } },
                      position: 'center'
                    }
                  }
                ]
              }
            ]
          }
        return (t, i) => (a(), r('div', l, [o(n(e), { option: c, resize: !1 })]))
      }
    }),
    [['__scopeId', 'data-v-1e26276d']]
  )
export { s as default }
