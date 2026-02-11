import {
  e as a,
  A as e,
  r as s,
  a2 as t,
  aj as r,
  o as n,
  j as i,
  y as c,
  k as l,
  z as d,
  x as m,
  Q as o,
  R as v,
  J as h
} from './index-820a519e.js'
import S from './AgeRatioChart-bd6010e4.js'
import p from './AnnualUseChart-17ca3b99.js'
import A from './ChinaMapChart-7aa26904.js'
import u from './HotPlateChart-e4b37ce4.js'
import f from './MaleFemaleRatioChart-480fb646.js'
import g from './OverNext30Chart-a2ceee7e.js'
import C from './PlatformSourceChart-29c538c5.js'
import x from './RealTimeAccessChart-4fdb407c.js'
import { d as j } from './dayjs.min-e5ba30ae.js'
import './Echart.vue_vue_type_script_setup_true_name_ECharts_lang-3e84099f.js'
import './echarts-ef988edf.js'
const Y =
    'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEQAAAAHCAYAAACx3+twAAAAAXNSR0IArs4c6QAAAZ9JREFUSEvNlb9LHFEQxz/fE4MXsJEUVhaCndcKqSxVUspZHeS0zIGChYIEXcXGxuLQgzSiohD8Ucr5BwRBWxvRzkJSCXqFsuqOuIrE7O5bDQfxtW/m+2bmzWdGVqWIUUFkSTrGKRny6uXgbxPboIFrZhHjgBwaBxh5feX0Txubp4VG1hB9ib6PF8v4fNMoV5EYZshhrAM5x/s+YoxJyhKWZBcmYDvkEOsoRTDDGD3xgrZGH0GYWIsjqHMyFFSg+qIohlhgAjENNDj8Dwno1wgnkaLMk+Uy/NhiSmGrGAV5nMfZPf+o7ZHlggqkCBrVMKneqKCt0IZYRXQ7gjKMOZqY0gD+i8JU6CbgJ9Dq8K8hhlViOc7GPIoozMPd8ZCXF+34SIv/d4QWaSVgqQ4IbQMdb0UolvknhLZRiuB7RmiOZq4ovxWhxCFov2imRrkOCG0iul6B0HcNcPePCA2pxFY9EEreCk/qtksXxkfnoAo40xeOYwPa4APXfEaODfTgeMuRBvkdGZY/+IRPZ8qghBv24zZQuDQ82oG2FA1fHnv3y0m/CFsHcS4AAAAASUVORK5CYII=',
  E = (a) => (o('data-v-a8fbfd36'), (a = a()), v(), a),
  R = { class: 'dataScreen-container' },
  w = { class: 'dataScreen-header' },
  I = { class: 'header-lf' },
  M = E(() =>
    c(
      'div',
      { class: 'header-ct' },
      [
        c('div', { class: 'header-ct-title' }, [
          c('span', null, '智慧旅游可视化大数据展示平台'),
          c('div', { class: 'header-ct-warning' }, '平台高峰预警信息（2条）')
        ])
      ],
      -1
    )
  ),
  b = { class: 'header-ri' },
  k = E(() => c('span', { class: 'header-download' }, '统计报告', -1)),
  D = { class: 'header-time' },
  H = { class: 'dataScreen-main' },
  Z = { class: 'dataScreen-lf' },
  q = { class: 'dataScreen-top' },
  G = E(() =>
    c(
      'div',
      { class: 'dataScreen-main-title' },
      [c('span', null, '实时游客统计'), c('img', { src: Y, alt: '' })],
      -1
    )
  ),
  F = { class: 'dataScreen-main-chart' },
  y = { class: 'dataScreen-center' },
  Q = E(() =>
    c(
      'div',
      { class: 'dataScreen-main-title' },
      [c('span', null, '男女比例'), c('img', { src: Y, alt: '' })],
      -1
    )
  ),
  U = { class: 'dataScreen-main-chart' },
  _ = { class: 'dataScreen-bottom' },
  B = E(() =>
    c(
      'div',
      { class: 'dataScreen-main-title' },
      [c('span', null, '年龄比例'), c('img', { src: Y, alt: '' })],
      -1
    )
  ),
  O = { class: 'dataScreen-main-chart' },
  P = { class: 'dataScreen-ct' },
  V = { class: 'dataScreen-map' },
  X = E(() => c('div', { class: 'dataScreen-map-title' }, '景区实时客流量', -1)),
  z = { class: 'dataScreen-cb' },
  K = E(() =>
    c(
      'div',
      { class: 'dataScreen-main-title' },
      [c('span', null, '未来30天游客量趋势图'), c('img', { src: Y, alt: '' })],
      -1
    )
  ),
  N = { class: 'dataScreen-main-chart' },
  W = { class: 'dataScreen-rg' },
  J = { class: 'dataScreen-top' },
  L = E(() =>
    c(
      'div',
      { class: 'dataScreen-main-title' },
      [c('span', null, '热门景区排行'), c('img', { src: Y, alt: '' })],
      -1
    )
  ),
  T = { class: 'dataScreen-main-chart' },
  $ = { class: 'dataScreen-center' },
  aa = E(() =>
    c(
      'div',
      { class: 'dataScreen-main-title' },
      [c('span', null, '年度游客量对比'), c('img', { src: Y, alt: '' })],
      -1
    )
  ),
  ea = { class: 'dataScreen-main-chart' },
  sa = { class: 'dataScreen-bottom' },
  ta = E(() =>
    c(
      'div',
      { class: 'dataScreen-main-title' },
      [c('span', null, '预约渠道数据统计'), c('img', { src: Y, alt: '' })],
      -1
    )
  ),
  ra = { class: 'dataScreen-main-chart' },
  na = h(
    a({
      __name: 'index',
      setup(a) {
        const o = e(),
          v = s(null)
        t(() => {
          ;(v.value &&
            ((v.value.style.transform = `scale(${Y()}) translate(-50%, -50%)`),
            (v.value.style.width = '1920px'),
            (v.value.style.height = '1080px')),
            window.addEventListener('resize', h))
        })
        const h = () => {
            v.value && (v.value.style.transform = `scale(${Y()}) translate(-50%, -50%)`)
          },
          Y = (a = 1920, e = 1080) => {
            let s = window.innerWidth / a,
              t = window.innerHeight / e
            return s < t ? s : t
          }
        let E = null,
          na = s(j().format('YYYY年MM月DD HH:mm:ss'))
        return (
          (E = setInterval(() => {
            na.value = j().format('YYYY年MM月DD HH:mm:ss')
          }, 1e3)),
          r(() => {
            ;(window.removeEventListener('resize', h), clearInterval(E))
          }),
          (a, e) => (
            n(),
            i('div', R, [
              c(
                'div',
                { class: 'dataScreen-content', ref_key: 'dataScreenRef', ref: v },
                [
                  c('div', w, [
                    c('div', I, [
                      c(
                        'span',
                        {
                          class: 'header-screening',
                          onClick: e[0] || (e[0] = (a) => l(o).push('/index'))
                        },
                        '首页'
                      )
                    ]),
                    M,
                    c('div', b, [k, c('span', D, '当前时间：' + d(l(na)), 1)])
                  ]),
                  c('div', H, [
                    c('div', Z, [
                      c('div', q, [G, c('div', F, [m(x)])]),
                      c('div', y, [Q, c('div', U, [m(f)])]),
                      c('div', _, [B, c('div', O, [m(S)])])
                    ]),
                    c('div', P, [c('div', V, [X, m(A)]), c('div', z, [K, c('div', N, [m(g)])])]),
                    c('div', W, [
                      c('div', J, [L, c('div', T, [m(u)])]),
                      c('div', $, [aa, c('div', ea, [m(p)])]),
                      c('div', sa, [ta, c('div', ra, [m(C)])])
                    ])
                  ])
                ],
                512
              )
            ])
          )
        )
      }
    }),
    [['__scopeId', 'data-v-a8fbfd36']]
  )
export { na as default }
