import {
  e,
  aE as a,
  u as s,
  f as t,
  o as l,
  j as r,
  q as o,
  s as n,
  k as i,
  _ as u,
  n as d,
  t as c,
  a8 as p,
  r as m,
  w as v,
  x as f,
  m as h,
  y,
  al as _,
  z as g,
  N as b,
  M as k,
  a1 as j,
  a5 as w,
  l as x,
  F as E,
  da as C,
  af as R,
  Q as V,
  R as S,
  as as $,
  dG as K,
  J as H
} from './index-820a519e.js'
import { E as M } from './el-drawer-45b209ae.js'
import './el-overlay-34b9d092.js'
import { E as N } from './el-divider-9c19755b.js'
import './el-input-5ae17c8f.js'
/* empty css               */ import { E as z, a as A } from './el-select-38080147.js'
import './el-popper-797844d6.js'
import { E as B } from './el-tree-8dac9473.js'
import './el-checkbox-77b6829c.js'
import { u as F } from './dict-451afacd.js'
import { c as J } from './dept-b8a01226.js'
import { e as O } from './tree-ae7cba8b.js'
import { p as U } from './role-0252bcb8.js'
import './use-dialog-2de816dc.js'
import './event-5568c9d8.js'
import './focus-trap-949626e0.js'
import './isNil-1f22f7b0.js'
import './scroll-ac7d0423.js'
import './vnode-06a99f10.js'
import './index-56bc6266.js'
import './strings-ed83d626.js'
import './isEqual-cb9e370d.js'
import './debounce-5bc596c6.js'
import './index-eb31d854.js'
import './validator-a9d8fe4c.js'
import './index-55f4d4a6.js'
import './dict-c8c7fcf4.js'
const D = e({ name: 'ElContainer' })
var L = u(
  e({
    ...D,
    props: { direction: { type: String } },
    setup(e) {
      const u = e,
        d = a(),
        c = s('container'),
        p = t(() => {
          if ('vertical' === u.direction) return !0
          if ('horizontal' === u.direction) return !1
          if (d && d.default) {
            return d.default().some((e) => {
              const a = e.type.name
              return 'ElHeader' === a || 'ElFooter' === a
            })
          }
          return !1
        })
      return (e, a) => (
        l(),
        r(
          'section',
          { class: n([i(c).b(), i(c).is('vertical', i(p))]) },
          [o(e.$slots, 'default')],
          2
        )
      )
    }
  }),
  [
    [
      '__file',
      '/home/runner/work/element-plus/element-plus/packages/components/container/src/container.vue'
    ]
  ]
)
const q = e({ name: 'ElAside' })
var I = u(
  e({
    ...q,
    props: { width: { type: String, default: null } },
    setup(e) {
      const a = e,
        u = s('aside'),
        c = t(() => (a.width ? u.cssVarBlock({ width: a.width }) : {}))
      return (e, a) => (
        l(),
        r('aside', { class: n(i(u).b()), style: d(i(c)) }, [o(e.$slots, 'default')], 6)
      )
    }
  }),
  [
    [
      '__file',
      '/home/runner/work/element-plus/element-plus/packages/components/container/src/aside.vue'
    ]
  ]
)
const T = e({ name: 'ElFooter' })
var G = u(
  e({
    ...T,
    props: { height: { type: String, default: null } },
    setup(e) {
      const a = e,
        u = s('footer'),
        c = t(() => (a.height ? u.cssVarBlock({ height: a.height }) : {}))
      return (e, a) => (
        l(),
        r('footer', { class: n(i(u).b()), style: d(i(c)) }, [o(e.$slots, 'default')], 6)
      )
    }
  }),
  [
    [
      '__file',
      '/home/runner/work/element-plus/element-plus/packages/components/container/src/footer.vue'
    ]
  ]
)
const Q = e({ name: 'ElHeader' })
var W = u(
  e({
    ...Q,
    props: { height: { type: String, default: null } },
    setup(e) {
      const a = e,
        u = s('header'),
        c = t(() => (a.height ? u.cssVarBlock({ height: a.height }) : {}))
      return (e, a) => (
        l(),
        r('header', { class: n(i(u).b()), style: d(i(c)) }, [o(e.$slots, 'default')], 6)
      )
    }
  }),
  [
    [
      '__file',
      '/home/runner/work/element-plus/element-plus/packages/components/container/src/header.vue'
    ]
  ]
)
const X = e({ name: 'ElMain' })
var Z = u(
  e({
    ...X,
    setup(e) {
      const a = s('main')
      return (e, s) => (l(), r('main', { class: n(i(a).b()) }, [o(e.$slots, 'default')], 2))
    }
  }),
  [
    [
      '__file',
      '/home/runner/work/element-plus/element-plus/packages/components/container/src/main.vue'
    ]
  ]
)
const P = c(L, { Aside: I, Footer: G, Header: W, Main: Z }),
  Y = p(I)
p(G)
const ee = p(W),
  ae = p(Z),
  se = (e) => (V('data-v-159700c0'), (e = e()), S(), e),
  te = { class: 'auth-manage-main-view' },
  le = { class: 'flex justify-between pt-[20px] pb-[20px]' },
  re = se(() => y('span', null, '权限管理', -1)),
  oe = { class: 'h-12 flex justify-between mt-3 mr-3 ml-5' },
  ne = { class: 'mt-1 text-[#909399]' },
  ie = { class: 'border-r-1 border-r-[#f0f0f0] b-r-solid h-[100%] p-[20px] box-border' },
  ue = se(() =>
    y(
      'div',
      { class: 'flex items-center' },
      [y('div', { class: 'yxt-divider' }), y('span', null, '数据权限')],
      -1
    )
  ),
  de = { class: 'ml-4 mt-3' },
  ce = { key: 0, class: 'mt-3 max-h-[65vh] b-1 b-solid b-[#e5e7eb] p-10px overflow-auto' },
  pe = se(() =>
    y(
      'div',
      { class: 'flex items-center' },
      [y('div', { class: 'yxt-divider' }), y('span', null, '菜单权限')],
      -1
    )
  ),
  me = { class: 'mt-5 max-h-[70vh] b-1 b-solid b-[#e5e7eb] p-10px overflow-auto box-border' },
  ve = H(
    e({
      __name: 'AuthManage',
      props: { currentRow: { type: Object, default: () => null } },
      emits: ['getList'],
      setup(e, { expose: a, emit: s }) {
        const t = e,
          o = m({})
        v(
          () => t.currentRow,
          (e) => {
            e && (o.value = JSON.parse(JSON.stringify(e)))
          },
          { deep: !0, immediate: !0 }
        )
        const n = m(!1),
          u = m(),
          d = { children: 'children', label: 'label' }
        let c = m([])
        const p = m()
        let V = m([])
        const S = m(),
          H = m(!1),
          D = async () => {
            var e, a, t
            if (H.value) return
            if (C(o.value.data_range)) return void R.error('数据范围选择项不能为空！')
            H.value = !0
            const l = [
              ...((null == (e = i(S)) ? void 0 : e.getCheckedKeys()) || []),
              ...((null == (a = i(S)) ? void 0 : a.getHalfCheckedKeys()) || [])
            ]
            ;((o.value.menu_ids = l),
              (o.value.dept_ids = null == (t = i(p)) ? void 0 : t.getCheckedKeys()))
            try {
              ;(await U(o.value)) && ((H.value = !1), R.success('保存成功'), L(), s('getList'))
            } finally {
              H.value = !1
            }
          },
          L = () => {
            var e, a
            ;((n.value = !1),
              (o.value = {}),
              null == (e = i(S)) || e.setCheckedKeys([]),
              null == (a = i(p)) || a.setCheckedKeys([]))
          }
        return (
          (async () => {
            const e = F(),
              a = await e.getDictObj(['sys_vadmin_data_range'])
            u.value = a.sys_vadmin_data_range
          })(),
          a({
            openDrawer: () => {
              ;((n.value = !0),
                (async () => {
                  var e
                  const a = await K()
                  if (a && ((V.value = a.data), await $(), t.currentRow)) {
                    const s = t.currentRow.menus.map((e) => e.id),
                      l = []
                    O(a.data, (e) => {
                      s.includes(e.value) && l.push(e.value)
                    })
                    for (const a of l) null == (e = i(S)) || e.setChecked(a, !0, !1)
                  }
                })(),
                (async () => {
                  var e
                  const a = await J()
                  if (a && ((c.value = a.data), await $(), t.currentRow)) {
                    const s = t.currentRow.depts.map((e) => e.id),
                      l = []
                    O(a.data, (e) => {
                      s.includes(e.value) && l.push(e.value)
                    })
                    for (const a of l) null == (e = i(p)) || e.setChecked(a, !0, !1)
                  }
                })())
            }
          }),
          (e, a) => (
            l(),
            r('div', te, [
              f(
                i(M),
                {
                  modelValue: n.value,
                  'onUpdate:modelValue': a[1] || (a[1] = (e) => (n.value = e)),
                  'with-header': !1,
                  size: 1e3,
                  'before-close': L
                },
                {
                  default: h(() => [
                    f(i(P), null, {
                      default: h(() => [
                        f(i(ee), null, {
                          default: h(() => [
                            y('div', le, [
                              re,
                              y('span', { onClick: L, class: 'flex cursor-pointer' }, [
                                f(i(_), { icon: 'iconamoon:close-thin', size: 23 })
                              ])
                            ])
                          ]),
                          _: 1
                        }),
                        f(i(N)),
                        y('div', oe, [
                          y('div', ne, [y('span', null, '角色名称：' + g(o.value.name), 1)]),
                          f(
                            i(b),
                            { type: 'primary', loading: H.value, onClick: D },
                            { default: h(() => [k('保存')]), _: 1 },
                            8,
                            ['loading']
                          )
                        ]),
                        f(i(N)),
                        f(i(P), null, {
                          default: h(() => [
                            f(
                              i(Y),
                              { width: '450px' },
                              {
                                default: h(() => [
                                  y('div', ie, [
                                    y('div', null, [
                                      ue,
                                      y('div', de, [
                                        f(
                                          i(z),
                                          {
                                            modelValue: o.value.data_range,
                                            'onUpdate:modelValue':
                                              a[0] || (a[0] = (e) => (o.value.data_range = e)),
                                            placeholder: '请选择数据范围'
                                          },
                                          {
                                            default: h(() => [
                                              (l(!0),
                                              r(
                                                j,
                                                null,
                                                w(
                                                  u.value,
                                                  (e) => (
                                                    l(),
                                                    x(
                                                      i(A),
                                                      {
                                                        key: e.value,
                                                        label: e.label,
                                                        value: e.value
                                                      },
                                                      null,
                                                      8,
                                                      ['label', 'value']
                                                    )
                                                  )
                                                ),
                                                128
                                              ))
                                            ]),
                                            _: 1
                                          },
                                          8,
                                          ['modelValue']
                                        ),
                                        '4' === o.value.data_range
                                          ? (l(),
                                            r('div', ce, [
                                              f(
                                                i(B),
                                                {
                                                  ref_key: 'deptTreeRef',
                                                  ref: p,
                                                  data: i(c),
                                                  'show-checkbox': '',
                                                  'node-key': 'value',
                                                  props: d,
                                                  'default-expand-all': !0,
                                                  'check-strictly': !0
                                                },
                                                null,
                                                8,
                                                ['data']
                                              )
                                            ]))
                                          : E('', !0)
                                      ])
                                    ])
                                  ])
                                ]),
                                _: 1
                              }
                            ),
                            f(i(ae), null, {
                              default: h(() => [
                                pe,
                                y('div', me, [
                                  f(
                                    i(B),
                                    {
                                      ref_key: 'menuTreeRef',
                                      ref: S,
                                      data: i(V),
                                      'show-checkbox': '',
                                      'node-key': 'value',
                                      props: d,
                                      'default-expand-all': !0,
                                      'check-strictly': !1
                                    },
                                    null,
                                    8,
                                    ['data']
                                  )
                                ])
                              ]),
                              _: 1
                            })
                          ]),
                          _: 1
                        })
                      ]),
                      _: 1
                    }),
                    f(i(N))
                  ]),
                  _: 1
                },
                8,
                ['modelValue']
              )
            ])
          )
        )
      }
    }),
    [['__scopeId', 'data-v-159700c0']]
  )
export { ve as default }
