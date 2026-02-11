import {
  b as e,
  dv as t,
  a as o,
  dw as n,
  e as s,
  a_ as a,
  u as l,
  r as p,
  f as r,
  h as c,
  o as i,
  l as f,
  m as u,
  y as m,
  s as d,
  k as y,
  E as x,
  n as v,
  p as B,
  F as T,
  M as h,
  z as g,
  x as k,
  N as _,
  q as S,
  a6 as b,
  _ as E,
  t as w
} from './index-820a519e.js'
import { u as C, E as $ } from './el-popper-797844d6.js'
const z = e({
    title: String,
    confirmButtonText: String,
    cancelButtonText: String,
    confirmButtonType: { type: String, values: t, default: 'primary' },
    cancelButtonType: { type: String, values: t, default: 'text' },
    icon: { type: o, default: () => n },
    iconColor: { type: String, default: '#f90' },
    hideIcon: { type: Boolean, default: !1 },
    hideAfter: { type: Number, default: 200 },
    teleported: C.teleported,
    persistent: C.persistent,
    width: { type: [String, Number], default: 150 }
  }),
  M = { confirm: (e) => e instanceof MouseEvent, cancel: (e) => e instanceof MouseEvent },
  N = s({ name: 'ElPopconfirm' })
const j = w(
  E(
    s({
      ...N,
      props: z,
      emits: M,
      setup(e, { emit: t }) {
        const o = e,
          { t: n } = a(),
          s = l('popconfirm'),
          E = p(),
          w = () => {
            var e, t
            null == (t = null == (e = E.value) ? void 0 : e.onClose) || t.call(e)
          },
          C = r(() => ({ width: c(o.width) })),
          z = (e) => {
            ;(t('confirm', e), w())
          },
          M = (e) => {
            ;(t('cancel', e), w())
          },
          N = r(() => o.confirmButtonText || n('el.popconfirm.confirmButtonText')),
          j = r(() => o.cancelButtonText || n('el.popconfirm.cancelButtonText'))
        return (e, t) => (
          i(),
          f(
            y($),
            b({ ref_key: 'tooltipRef', ref: E, trigger: 'click', effect: 'light' }, e.$attrs, {
              'popper-class': `${y(s).namespace.value}-popover`,
              'popper-style': y(C),
              teleported: e.teleported,
              'fallback-placements': ['bottom', 'top', 'right', 'left'],
              'hide-after': e.hideAfter,
              persistent: e.persistent
            }),
            {
              content: u(() => [
                m(
                  'div',
                  { class: d(y(s).b()) },
                  [
                    m(
                      'div',
                      { class: d(y(s).e('main')) },
                      [
                        !e.hideIcon && e.icon
                          ? (i(),
                            f(
                              y(x),
                              {
                                key: 0,
                                class: d(y(s).e('icon')),
                                style: v({ color: e.iconColor })
                              },
                              { default: u(() => [(i(), f(B(e.icon)))]), _: 1 },
                              8,
                              ['class', 'style']
                            ))
                          : T('v-if', !0),
                        h(' ' + g(e.title), 1)
                      ],
                      2
                    ),
                    m(
                      'div',
                      { class: d(y(s).e('action')) },
                      [
                        k(
                          y(_),
                          {
                            size: 'small',
                            type: 'text' === e.cancelButtonType ? '' : e.cancelButtonType,
                            text: 'text' === e.cancelButtonType,
                            onClick: M
                          },
                          { default: u(() => [h(g(y(j)), 1)]), _: 1 },
                          8,
                          ['type', 'text']
                        ),
                        k(
                          y(_),
                          {
                            size: 'small',
                            type: 'text' === e.confirmButtonType ? '' : e.confirmButtonType,
                            text: 'text' === e.confirmButtonType,
                            onClick: z
                          },
                          { default: u(() => [h(g(y(N)), 1)]), _: 1 },
                          8,
                          ['type', 'text']
                        )
                      ],
                      2
                    )
                  ],
                  2
                )
              ]),
              default: u(() => [
                e.$slots.reference ? S(e.$slots, 'reference', { key: 0 }) : T('v-if', !0)
              ]),
              _: 3
            },
            16,
            ['popper-class', 'popper-style', 'teleported', 'hide-after', 'persistent']
          )
        )
      }
    }),
    [
      [
        '__file',
        '/home/runner/work/element-plus/element-plus/packages/components/popconfirm/src/popconfirm.vue'
      ]
    ]
  )
)
export { j as E }
