import {
  I as a,
  U as e,
  e as s,
  r as t,
  L as l,
  o as i,
  j as o,
  y as d,
  x as n,
  m as r,
  k as u,
  M as p,
  z as m,
  a1 as x
} from './index-820a519e.js'
import { E as c, a as y } from './el-col-beabe3f6.js'
import { E as b } from './el-skeleton-item-e9a083cf.js'
import { E as g, a as v } from './el-radio-group-4cb40939.js'
import { E as f } from './el-date-picker-6b1a21d2.js'
import './el-input-5ae17c8f.js'
import './el-popper-797844d6.js'
import { _ as h } from './Echart.vue_vue_type_script_setup_true_lang-f887d0a9.js'
import './event-5568c9d8.js'
import './dayjs.min-e5ba30ae.js'
import './debounce-5bc596c6.js'
import './index-eb31d854.js'
import './isEqual-cb9e370d.js'
import './isNil-1f22f7b0.js'
import './focus-trap-949626e0.js'
import './echarts-ef988edf.js'
const { t: _ } = a(),
  j = {
    xAxis: {
      data: [
        _('analysis.january'),
        _('analysis.february'),
        _('analysis.march'),
        _('analysis.april'),
        _('analysis.may'),
        _('analysis.june'),
        _('analysis.july'),
        _('analysis.august'),
        _('analysis.september'),
        _('analysis.october'),
        _('analysis.november'),
        _('analysis.december')
      ],
      boundaryGap: !0,
      axisTick: { show: !1 }
    },
    grid: { left: 20, right: 20, bottom: 35, top: 30, containLabel: !0 },
    tooltip: { trigger: 'axis', axisPointer: { type: 'cross' }, padding: [5, 10] },
    yAxis: { type: 'value', axisTick: { show: !1 } },
    legend: { data: ['新增客户'], bottom: -5 },
    series: [
      {
        name: '新增客户',
        smooth: !1,
        symbol: 'circle',
        symbolSize: 8,
        type: 'line',
        data: [100, 120, 161, 134, 105, 160, 165, 114, 163, 185, 118, 123],
        animationDuration: 2800,
        animationEasing: 'quadraticOut',
        itemStyle: { color: 'rgba(79,168,249)' },
        lineStyle: { width: 1, opacity: 1 }
      }
    ]
  },
  w = {
    tooltip: { trigger: 'item', formatter: '{a} <br/>{b} : {c} ({d}%)' },
    series: [
      {
        name: '各楼层销售情况统计',
        type: 'pie',
        radius: '60%',
        center: ['50%', '50%'],
        data: [
          { value: 335, name: '青铜卡' },
          { value: 310, name: '白银卡' },
          { value: 234, name: '黄金卡' },
          { value: 135, name: '钻石卡' }
        ]
      }
    ]
  },
  S = {
    xAxis: {
      data: [
        _('analysis.january'),
        _('analysis.february'),
        _('analysis.march'),
        _('analysis.april'),
        _('analysis.may'),
        _('analysis.june'),
        _('analysis.july'),
        _('analysis.august'),
        _('analysis.september'),
        _('analysis.october'),
        _('analysis.november'),
        _('analysis.december')
      ],
      boundaryGap: !0,
      axisTick: { show: !1 }
    },
    grid: { left: 20, right: 20, bottom: 35, top: 30, containLabel: !0 },
    tooltip: { trigger: 'axis', axisPointer: { type: 'cross' }, padding: [5, 10] },
    yAxis: { type: 'value', axisTick: { show: !1 } },
    legend: { data: ['转换次数', '转换率'], bottom: -5 },
    series: [
      {
        name: '转换次数',
        smooth: !1,
        symbol: 'circle',
        symbolSize: 8,
        type: 'line',
        data: [100, 120, 161, 134, 105, 160, 165, 114, 163, 185, 118, 123],
        animationDuration: 2800,
        animationEasing: 'quadraticOut',
        itemStyle: { color: 'rgba(110,199,30)' },
        lineStyle: { width: 1, opacity: 1 }
      },
      {
        name: '转换率',
        smooth: !1,
        symbol: 'circle',
        symbolSize: 8,
        type: 'line',
        data: [120, 82, 91, 154, 162, 140, 145, 250, 134, 56, 99, 123],
        animationDuration: 2800,
        animationEasing: 'quadraticOut',
        itemStyle: { color: 'rgba(79,168,249)' },
        lineStyle: { width: 1, opacity: 1 }
      }
    ]
  },
  k = {
    xAxis: {
      data: [
        _('analysis.january'),
        _('analysis.february'),
        _('analysis.march'),
        _('analysis.april'),
        _('analysis.may'),
        _('analysis.june'),
        _('analysis.july'),
        _('analysis.august'),
        _('analysis.september'),
        _('analysis.october'),
        _('analysis.november'),
        _('analysis.december')
      ],
      boundaryGap: !0,
      axisTick: { show: !1 }
    },
    grid: { left: 20, right: 20, bottom: 35, top: 30, containLabel: !0 },
    tooltip: { trigger: 'axis', axisPointer: { type: 'cross' }, padding: [5, 10] },
    yAxis: { type: 'value', axisTick: { show: !1 } },
    legend: { data: ['支付成功客户数'], bottom: -5 },
    series: [
      {
        name: '支付成功客户数',
        smooth: !1,
        symbol: 'circle',
        symbolSize: 8,
        type: 'line',
        data: [100, 120, 161, 134, 105, 160, 165, 114, 163, 185, 118, 123],
        animationDuration: 2800,
        animationEasing: 'quadraticOut',
        itemStyle: { color: 'rgba(79,168,249)' },
        lineStyle: { width: 1, opacity: 1 }
      }
    ]
  },
  E = () => e.get({ url: '/analysis/random/number' }),
  T = { class: 'border-1 border-[#e4e7ed] b-solid p-[20px] rounded-[4px]' },
  z = d('div', { class: 'text-[#787a7d] text-[12px]' }, '新增潜客数', -1),
  A = { class: 'text-[#121315] text-[20px] mt-[10px]' },
  D = { class: 'border-1 border-[#e4e7ed] b-solid p-[20px] rounded-[4px]' },
  V = d('div', { class: 'text-[#787a7d] text-[12px]' }, '新增客户数', -1),
  q = { class: 'text-[#121315] text-[20px] mt-[10px]' },
  P = { class: 'border-1 border-[#e4e7ed] b-solid p-[20px] rounded-[4px]' },
  L = d('div', { class: 'text-[#787a7d] text-[12px]' }, '新增会员数', -1),
  O = { class: 'text-[#121315] text-[20px] mt-[10px]' },
  U = { class: 'border-1 border-[#e4e7ed] b-solid p-[20px] rounded-[4px]' },
  G = d('div', { class: 'text-[#787a7d] text-[12px]' }, '支付成功客户数', -1),
  C = { class: 'text-[#121315] text-[20px] mt-[10px]' },
  I = { class: 'border-1 border-[#e4e7ed] b-solid p-[20px] rounded-[4px]' },
  N = d('div', { class: 'text-[#000] text-[12px]' }, '会员分布情况', -1),
  H = { class: 'border-1 border-[#e4e7ed] b-solid p-[20px] rounded-[4px]' },
  J = d('div', { class: 'text-[#000] text-[12px]' }, '新增客户趋势', -1),
  K = { class: 'border-1 border-[#e4e7ed] b-solid p-[20px] rounded-[4px]' },
  M = d('div', { class: 'text-[#000] text-[12px]' }, '客户转会员趋势', -1),
  Q = { class: 'border-1 border-[#e4e7ed] b-solid p-[20px] rounded-[4px]' },
  R = d('div', { class: 'text-[#000] text-[12px]' }, '支付成功客户趋势', -1),
  B = { class: 'border-1 border-[#e4e7ed] b-solid p-[20px] rounded-[4px]' },
  F = d('div', { class: 'text-[#000] text-[12px]' }, '客户转会员趋势', -1),
  W = { class: 'border-1 border-[#e4e7ed] b-solid p-[20px] rounded-[4px]' },
  X = d('div', { class: 'text-[#000] text-[12px]' }, '支付成功客户趋势', -1),
  Y = s({
    __name: 'User',
    setup(a) {
      const e = t(!1),
        s = l(j),
        _ = l(k),
        Y = l(S),
        Z = l(w),
        $ = t(0),
        aa = t(),
        ea = () => {},
        sa = (a) => new Date('2023/01/01').getTime() > a.getTime() || a.getTime() > Date.now(),
        ta = t(0),
        la = t(0),
        ia = t(0),
        oa = t(0),
        da = async () => {
          const a = await E()
          a && (ta.value = a.data)
        },
        na = async () => {
          const a = await E()
          a && (la.value = a.data)
        },
        ra = async () => {
          const a = await E()
          a && (ia.value = a.data)
        },
        ua = async () => {
          const a = await E()
          a && (oa.value = a.data)
        }
      return (
        (async () => {
          ;((e.value = !0), await Promise.all([da(), na(), ra(), ua()]), (e.value = !1))
        })(),
        (a, t) => (
          i(),
          o(
            x,
            null,
            [
              d('div', null, [
                n(
                  u(v),
                  {
                    modelValue: $.value,
                    'onUpdate:modelValue': t[1] || (t[1] = (a) => ($.value = a)),
                    onChange: ea
                  },
                  {
                    default: r(() => [
                      n(u(g), { label: '0' }, { default: r(() => [p('全部')]), _: 1 }),
                      n(u(g), { label: '1' }, { default: r(() => [p('今天')]), _: 1 }),
                      n(u(g), { label: '2' }, { default: r(() => [p('昨天')]), _: 1 }),
                      n(u(g), { label: '3' }, { default: r(() => [p('最近7天')]), _: 1 }),
                      n(u(g), { label: '4' }, { default: r(() => [p('最近30天')]), _: 1 }),
                      n(
                        u(f),
                        {
                          class: 'ml-2',
                          modelValue: aa.value,
                          'onUpdate:modelValue': t[0] || (t[0] = (a) => (aa.value = a)),
                          type: 'daterange',
                          'range-separator': '-',
                          'start-placeholder': '开始时间',
                          'end-placeholder': '结束时间',
                          'disabled-date': sa,
                          'unlink-panels': !0,
                          size: 'default'
                        },
                        null,
                        8,
                        ['modelValue']
                      )
                    ]),
                    _: 1
                  },
                  8,
                  ['modelValue']
                )
              ]),
              n(
                u(y),
                { gutter: 20, class: 'pt-4' },
                {
                  default: r(() => [
                    n(
                      u(c),
                      { xs: 24, sm: 6, class: 'mb-2' },
                      {
                        default: r(() => [
                          n(
                            u(b),
                            { loading: e.value, animated: '', rows: 4 },
                            {
                              default: r(() => [d('div', T, [z, d('div', A, m(ta.value), 1)])]),
                              _: 1
                            },
                            8,
                            ['loading']
                          )
                        ]),
                        _: 1
                      }
                    ),
                    n(
                      u(c),
                      { xs: 24, sm: 6, class: 'mb-2' },
                      {
                        default: r(() => [
                          n(
                            u(b),
                            { loading: e.value, animated: '', rows: 4 },
                            {
                              default: r(() => [d('div', D, [V, d('div', q, m(la.value), 1)])]),
                              _: 1
                            },
                            8,
                            ['loading']
                          )
                        ]),
                        _: 1
                      }
                    ),
                    n(
                      u(c),
                      { xs: 24, sm: 6, class: 'mb-2' },
                      {
                        default: r(() => [
                          n(
                            u(b),
                            { loading: e.value, animated: '', rows: 4 },
                            {
                              default: r(() => [d('div', P, [L, d('div', O, m(ia.value), 1)])]),
                              _: 1
                            },
                            8,
                            ['loading']
                          )
                        ]),
                        _: 1
                      }
                    ),
                    n(
                      u(c),
                      { xs: 24, sm: 6, class: 'mb-2' },
                      {
                        default: r(() => [
                          n(
                            u(b),
                            { loading: e.value, animated: '', rows: 4 },
                            {
                              default: r(() => [d('div', U, [G, d('div', C, m(oa.value), 1)])]),
                              _: 1
                            },
                            8,
                            ['loading']
                          )
                        ]),
                        _: 1
                      }
                    ),
                    n(
                      u(c),
                      { xs: 24, sm: 12, class: 'mb-2' },
                      {
                        default: r(() => [
                          n(
                            u(b),
                            { loading: e.value, animated: '', rows: 4 },
                            {
                              default: r(() => [
                                d('div', I, [
                                  d('div', null, [
                                    N,
                                    n(u(h), { options: Z, height: 230 }, null, 8, ['options'])
                                  ])
                                ])
                              ]),
                              _: 1
                            },
                            8,
                            ['loading']
                          )
                        ]),
                        _: 1
                      }
                    ),
                    n(
                      u(c),
                      { xs: 24, sm: 12, class: 'mb-2' },
                      {
                        default: r(() => [
                          n(
                            u(b),
                            { loading: e.value, animated: '', rows: 4 },
                            {
                              default: r(() => [
                                d('div', H, [
                                  J,
                                  n(u(h), { options: s, height: 230 }, null, 8, ['options'])
                                ])
                              ]),
                              _: 1
                            },
                            8,
                            ['loading']
                          )
                        ]),
                        _: 1
                      }
                    ),
                    n(
                      u(c),
                      { xs: 24, sm: 12, class: 'mb-2' },
                      {
                        default: r(() => [
                          n(
                            u(b),
                            { loading: e.value, animated: '', rows: 4 },
                            {
                              default: r(() => [
                                d('div', K, [
                                  M,
                                  n(u(h), { options: Y, height: 230 }, null, 8, ['options'])
                                ])
                              ]),
                              _: 1
                            },
                            8,
                            ['loading']
                          )
                        ]),
                        _: 1
                      }
                    ),
                    n(
                      u(c),
                      { xs: 24, sm: 12, class: 'mb-2' },
                      {
                        default: r(() => [
                          n(
                            u(b),
                            { loading: e.value, animated: '', rows: 4 },
                            {
                              default: r(() => [
                                d('div', Q, [
                                  R,
                                  n(u(h), { options: _, height: 230 }, null, 8, ['options'])
                                ])
                              ]),
                              _: 1
                            },
                            8,
                            ['loading']
                          )
                        ]),
                        _: 1
                      }
                    ),
                    n(
                      u(c),
                      { xs: 24, sm: 12, class: 'mb-2' },
                      {
                        default: r(() => [
                          n(
                            u(b),
                            { loading: e.value, animated: '', rows: 4 },
                            {
                              default: r(() => [
                                d('div', B, [
                                  F,
                                  n(u(h), { options: Y, height: 230 }, null, 8, ['options'])
                                ])
                              ]),
                              _: 1
                            },
                            8,
                            ['loading']
                          )
                        ]),
                        _: 1
                      }
                    ),
                    n(
                      u(c),
                      { xs: 24, sm: 12, class: 'mb-2' },
                      {
                        default: r(() => [
                          n(
                            u(b),
                            { loading: e.value, animated: '', rows: 4 },
                            {
                              default: r(() => [
                                d('div', W, [
                                  X,
                                  n(u(h), { options: _, height: 230 }, null, 8, ['options'])
                                ])
                              ]),
                              _: 1
                            },
                            8,
                            ['loading']
                          )
                        ]),
                        _: 1
                      }
                    )
                  ]),
                  _: 1
                }
              )
            ],
            64
          )
        )
      )
    }
  })
export { Y as default }
