import {
  b as e,
  a,
  d as t,
  b7 as i,
  g as l,
  i as n,
  e as o,
  aq as c,
  b8 as s,
  b9 as r,
  u as v,
  bi as u,
  aU as d,
  f as p,
  r as f,
  h as m,
  w as b,
  ba as y,
  a2 as h,
  o as k,
  j as g,
  y as C,
  k as I,
  s as x,
  aX as S,
  l as V,
  m as w,
  p as T,
  E as _,
  F as B,
  z as A,
  x as E,
  aW as N,
  n as P,
  aY as j,
  _ as U,
  aB as z,
  as as F,
  bb as K,
  ar as X,
  t as q
} from './index-820a519e.js'
import { i as W } from './validator-a9d8fe4c.js'
import { U as Y, C as D, I as G } from './event-5568c9d8.js'
const H = e({
    modelValue: { type: [Boolean, String, Number], default: !1 },
    disabled: { type: Boolean, default: !1 },
    loading: { type: Boolean, default: !1 },
    size: { type: String, validator: W },
    width: { type: [String, Number], default: '' },
    inlinePrompt: { type: Boolean, default: !1 },
    inactiveActionIcon: { type: a },
    activeActionIcon: { type: a },
    activeIcon: { type: a },
    inactiveIcon: { type: a },
    activeText: { type: String, default: '' },
    inactiveText: { type: String, default: '' },
    activeValue: { type: [Boolean, String, Number], default: !0 },
    inactiveValue: { type: [Boolean, String, Number], default: !1 },
    activeColor: { type: String, default: '' },
    inactiveColor: { type: String, default: '' },
    borderColor: { type: String, default: '' },
    name: { type: String, default: '' },
    validateEvent: { type: Boolean, default: !0 },
    beforeChange: { type: t(Function) },
    id: String,
    tabindex: { type: [String, Number] },
    value: { type: [Boolean, String, Number], default: !1 }
  }),
  J = {
    [Y]: (e) => i(e) || l(e) || n(e),
    [D]: (e) => i(e) || l(e) || n(e),
    [G]: (e) => i(e) || l(e) || n(e)
  },
  L = ['onClick'],
  M = [
    'id',
    'aria-checked',
    'aria-disabled',
    'name',
    'true-value',
    'false-value',
    'disabled',
    'tabindex',
    'onKeydown'
  ],
  O = ['aria-hidden'],
  Q = ['aria-hidden'],
  R = ['aria-hidden'],
  Z = 'ElSwitch',
  $ = o({ name: Z })
const ee = q(
  U(
    o({
      ...$,
      props: H,
      emits: J,
      setup(e, { expose: a, emit: t }) {
        const l = e,
          n = c(),
          { formItem: o } = s(),
          U = r(),
          q = v('switch')
        ;[
          ['"value"', '"model-value" or "v-model"', 'value'],
          ['"active-color"', 'CSS var `--el-switch-on-color`', 'activeColor'],
          ['"inactive-color"', 'CSS var `--el-switch-off-color`', 'inactiveColor'],
          ['"border-color"', 'CSS var `--el-switch-border-color`', 'borderColor']
        ].forEach((e) => {
          z(
            {
              from: e[0],
              replacement: e[1],
              scope: Z,
              version: '2.3.0',
              ref: 'https://element-plus.org/en-US/component/switch.html#attributes',
              type: 'Attribute'
            },
            p(() => {
              var a
              return !!(null == (a = n.vnode.props) ? void 0 : a[e[2]])
            })
          )
        })
        const { inputId: W } = u(l, { formItemContext: o }),
          H = d(p(() => l.loading)),
          J = f(!1 !== l.modelValue),
          $ = f(),
          ee = f(),
          ae = p(() => [q.b(), q.m(U.value), q.is('disabled', H.value), q.is('checked', oe.value)]),
          te = p(() => [q.e('label'), q.em('label', 'left'), q.is('active', !oe.value)]),
          ie = p(() => [q.e('label'), q.em('label', 'right'), q.is('active', oe.value)]),
          le = p(() => ({ width: m(l.width) }))
        ;(b(
          () => l.modelValue,
          () => {
            J.value = !0
          }
        ),
          b(
            () => l.value,
            () => {
              J.value = !1
            }
          ))
        const ne = p(() => (J.value ? l.modelValue : l.value)),
          oe = p(() => ne.value === l.activeValue)
        ;([l.activeValue, l.inactiveValue].includes(ne.value) ||
          (t(Y, l.inactiveValue), t(D, l.inactiveValue), t(G, l.inactiveValue)),
          b(oe, (e) => {
            var a
            ;(($.value.checked = e),
              l.validateEvent &&
                (null == (a = null == o ? void 0 : o.validate) ||
                  a.call(o, 'change').catch((e) => y())))
          }))
        const ce = () => {
            const e = oe.value ? l.inactiveValue : l.activeValue
            ;(t(Y, e),
              t(D, e),
              t(G, e),
              F(() => {
                $.value.checked = oe.value
              }))
          },
          se = () => {
            if (H.value) return
            const { beforeChange: e } = l
            if (!e) return void ce()
            const a = e()
            ;([K(a), i(a)].includes(!0) ||
              X(Z, 'beforeChange must return type `Promise<boolean>` or `boolean`'),
              K(a)
                ? a
                    .then((e) => {
                      e && ce()
                    })
                    .catch((e) => {})
                : a && ce())
          },
          re = p(() =>
            q.cssVarBlock({
              ...(l.activeColor ? { 'on-color': l.activeColor } : null),
              ...(l.inactiveColor ? { 'off-color': l.inactiveColor } : null),
              ...(l.borderColor ? { 'border-color': l.borderColor } : null)
            })
          )
        return (
          h(() => {
            $.value.checked = oe.value
          }),
          a({
            focus: () => {
              var e, a
              null == (a = null == (e = $.value) ? void 0 : e.focus) || a.call(e)
            },
            checked: oe
          }),
          (e, a) => (
            k(),
            g(
              'div',
              { class: x(I(ae)), style: P(I(re)), onClick: j(se, ['prevent']) },
              [
                C(
                  'input',
                  {
                    id: I(W),
                    ref_key: 'input',
                    ref: $,
                    class: x(I(q).e('input')),
                    type: 'checkbox',
                    role: 'switch',
                    'aria-checked': I(oe),
                    'aria-disabled': I(H),
                    name: e.name,
                    'true-value': e.activeValue,
                    'false-value': e.inactiveValue,
                    disabled: I(H),
                    tabindex: e.tabindex,
                    onChange: ce,
                    onKeydown: S(se, ['enter'])
                  },
                  null,
                  42,
                  M
                ),
                e.inlinePrompt || (!e.inactiveIcon && !e.inactiveText)
                  ? B('v-if', !0)
                  : (k(),
                    g(
                      'span',
                      { key: 0, class: x(I(te)) },
                      [
                        e.inactiveIcon
                          ? (k(),
                            V(
                              I(_),
                              { key: 0 },
                              { default: w(() => [(k(), V(T(e.inactiveIcon)))]), _: 1 }
                            ))
                          : B('v-if', !0),
                        !e.inactiveIcon && e.inactiveText
                          ? (k(),
                            g('span', { key: 1, 'aria-hidden': I(oe) }, A(e.inactiveText), 9, O))
                          : B('v-if', !0)
                      ],
                      2
                    )),
                C(
                  'span',
                  { ref_key: 'core', ref: ee, class: x(I(q).e('core')), style: P(I(le)) },
                  [
                    e.inlinePrompt
                      ? (k(),
                        g(
                          'div',
                          { key: 0, class: x(I(q).e('inner')) },
                          [
                            e.activeIcon || e.inactiveIcon
                              ? (k(),
                                V(
                                  I(_),
                                  { key: 0, class: x(I(q).is('icon')) },
                                  {
                                    default: w(() => [
                                      (k(), V(T(I(oe) ? e.activeIcon : e.inactiveIcon)))
                                    ]),
                                    _: 1
                                  },
                                  8,
                                  ['class']
                                ))
                              : e.activeText || e.inactiveText
                                ? (k(),
                                  g(
                                    'span',
                                    { key: 1, class: x(I(q).is('text')), 'aria-hidden': !I(oe) },
                                    A(I(oe) ? e.activeText : e.inactiveText),
                                    11,
                                    Q
                                  ))
                                : B('v-if', !0)
                          ],
                          2
                        ))
                      : B('v-if', !0),
                    C(
                      'div',
                      { class: x(I(q).e('action')) },
                      [
                        e.loading
                          ? (k(),
                            V(
                              I(_),
                              { key: 0, class: x(I(q).is('loading')) },
                              { default: w(() => [E(I(N))]), _: 1 },
                              8,
                              ['class']
                            ))
                          : e.activeActionIcon && I(oe)
                            ? (k(),
                              V(
                                I(_),
                                { key: 1 },
                                { default: w(() => [(k(), V(T(e.activeActionIcon)))]), _: 1 }
                              ))
                            : e.inactiveActionIcon && !I(oe)
                              ? (k(),
                                V(
                                  I(_),
                                  { key: 2 },
                                  { default: w(() => [(k(), V(T(e.inactiveActionIcon)))]), _: 1 }
                                ))
                              : B('v-if', !0)
                      ],
                      2
                    )
                  ],
                  6
                ),
                e.inlinePrompt || (!e.activeIcon && !e.activeText)
                  ? B('v-if', !0)
                  : (k(),
                    g(
                      'span',
                      { key: 1, class: x(I(ie)) },
                      [
                        e.activeIcon
                          ? (k(),
                            V(
                              I(_),
                              { key: 0 },
                              { default: w(() => [(k(), V(T(e.activeIcon)))]), _: 1 }
                            ))
                          : B('v-if', !0),
                        !e.activeIcon && e.activeText
                          ? (k(),
                            g('span', { key: 1, 'aria-hidden': !I(oe) }, A(e.activeText), 9, R))
                          : B('v-if', !0)
                      ],
                      2
                    ))
              ],
              14,
              L
            )
          )
        )
      }
    }),
    [
      [
        '__file',
        '/home/runner/work/element-plus/element-plus/packages/components/switch/src/switch.vue'
      ]
    ]
  )
)
export { ee as E }
