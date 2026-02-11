import {
  e,
  a_ as o,
  ao as s,
  f as l,
  o as t,
  j as a,
  y as r,
  q as n,
  s as i,
  k as c,
  z as d,
  x as u,
  m as f,
  l as p,
  p as m,
  E as g,
  F as h,
  n as v,
  _ as b,
  dr as y,
  aE as k,
  aB as x,
  u as C,
  r as w,
  am as $,
  a0 as _,
  a6 as R,
  ak as A,
  aH as F,
  D as j,
  bZ as E,
  t as I,
  ad as M,
  aT as T,
  cA as D,
  w as L,
  b1 as S,
  M as q,
  G as z,
  as as B
} from './index-820a519e.js'
import { E as O, a as P } from './el-overlay-34b9d092.js'
import { d as H, a as N, b as U, c as G, u as J } from './use-dialog-2de816dc.js'
import { F as K, E as V } from './focus-trap-949626e0.js'
import { c as Z } from './refs-374e9e51.js'
import { u as Q } from './index-2b3f7e71.js'
const W = Symbol('dialogInjectionKey'),
  X = ['aria-label'],
  Y = ['id'],
  ee = e({ name: 'ElDialogContent' })
var oe = b(
  e({
    ...ee,
    props: H,
    emits: N,
    setup(e) {
      const b = e,
        { t: k } = o(),
        { Close: x } = y,
        { dialogRef: C, headerRef: w, bodyId: $, ns: _, style: R } = s(W),
        { focusTrapRef: A } = s(K),
        F = l(() => [
          _.b(),
          _.is('fullscreen', b.fullscreen),
          _.is('draggable', b.draggable),
          _.is('align-center', b.alignCenter),
          { [_.m('center')]: b.center },
          b.customClass
        ]),
        j = Z(A, C),
        E = l(() => b.draggable)
      return (
        Q(C, w, E),
        (e, o) => (
          t(),
          a(
            'div',
            { ref: c(j), class: i(c(F)), style: v(c(R)), tabindex: '-1' },
            [
              r(
                'header',
                { ref_key: 'headerRef', ref: w, class: i(c(_).e('header')) },
                [
                  n(e.$slots, 'header', {}, () => [
                    r('span', { role: 'heading', class: i(c(_).e('title')) }, d(e.title), 3)
                  ]),
                  e.showClose
                    ? (t(),
                      a(
                        'button',
                        {
                          key: 0,
                          'aria-label': c(k)('el.dialog.close'),
                          class: i(c(_).e('headerbtn')),
                          type: 'button',
                          onClick: o[0] || (o[0] = (o) => e.$emit('close'))
                        },
                        [
                          u(
                            c(g),
                            { class: i(c(_).e('close')) },
                            { default: f(() => [(t(), p(m(e.closeIcon || c(x))))]), _: 1 },
                            8,
                            ['class']
                          )
                        ],
                        10,
                        X
                      ))
                    : h('v-if', !0)
                ],
                2
              ),
              r('div', { id: c($), class: i(c(_).e('body')) }, [n(e.$slots, 'default')], 10, Y),
              e.$slots.footer
                ? (t(),
                  a('footer', { key: 0, class: i(c(_).e('footer')) }, [n(e.$slots, 'footer')], 2))
                : h('v-if', !0)
            ],
            6
          )
        )
      )
    }
  }),
  [
    [
      '__file',
      '/home/runner/work/element-plus/element-plus/packages/components/dialog/src/dialog-content.vue'
    ]
  ]
)
const se = ['aria-label', 'aria-labelledby', 'aria-describedby'],
  le = e({ name: 'ElDialog', inheritAttrs: !1 })
const te = I(
    b(
      e({
        ...le,
        props: U,
        emits: G,
        setup(e, { expose: o }) {
          const s = e,
            a = k()
          ;(x(
            {
              scope: 'el-dialog',
              from: 'the title slot',
              replacement: 'the header slot',
              version: '3.0.0',
              ref: 'https://element-plus.org/en-US/component/dialog.html#slots'
            },
            l(() => !!a.title)
          ),
            x(
              {
                scope: 'el-dialog',
                from: 'custom-class',
                replacement: 'class',
                version: '2.3.0',
                ref: 'https://element-plus.org/en-US/component/dialog.html#attributes',
                type: 'Attribute'
              },
              l(() => !!s.customClass)
            ))
          const d = C('dialog'),
            m = w(),
            g = w(),
            b = w(),
            {
              visible: y,
              titleId: I,
              bodyId: M,
              style: T,
              overlayDialogStyle: D,
              rendered: L,
              zIndex: S,
              afterEnter: q,
              afterLeave: z,
              beforeLeave: B,
              handleClose: H,
              onModalClick: N,
              onOpenAutoFocus: U,
              onCloseAutoFocus: G,
              onCloseRequested: K,
              onFocusoutPrevented: Z
            } = J(s, m)
          $(W, { dialogRef: m, headerRef: g, bodyId: M, ns: d, rendered: L, style: T })
          const Q = P(N),
            X = l(() => s.draggable && !s.fullscreen)
          return (
            o({ visible: y, dialogContentRef: b }),
            (e, o) => (
              t(),
              p(
                E,
                { to: 'body', disabled: !e.appendToBody },
                [
                  u(
                    j,
                    {
                      name: 'dialog-fade',
                      onAfterEnter: c(q),
                      onAfterLeave: c(z),
                      onBeforeLeave: c(B),
                      persisted: ''
                    },
                    {
                      default: f(() => [
                        _(
                          u(
                            c(O),
                            {
                              'custom-mask-event': '',
                              mask: e.modal,
                              'overlay-class': e.modalClass,
                              'z-index': c(S)
                            },
                            {
                              default: f(() => [
                                r(
                                  'div',
                                  {
                                    role: 'dialog',
                                    'aria-modal': 'true',
                                    'aria-label': e.title || void 0,
                                    'aria-labelledby': e.title ? void 0 : c(I),
                                    'aria-describedby': c(M),
                                    class: i(`${c(d).namespace.value}-overlay-dialog`),
                                    style: v(c(D)),
                                    onClick:
                                      o[0] || (o[0] = (...e) => c(Q).onClick && c(Q).onClick(...e)),
                                    onMousedown:
                                      o[1] ||
                                      (o[1] = (...e) => c(Q).onMousedown && c(Q).onMousedown(...e)),
                                    onMouseup:
                                      o[2] ||
                                      (o[2] = (...e) => c(Q).onMouseup && c(Q).onMouseup(...e))
                                  },
                                  [
                                    u(
                                      c(V),
                                      {
                                        loop: '',
                                        trapped: c(y),
                                        'focus-start-el': 'container',
                                        onFocusAfterTrapped: c(U),
                                        onFocusAfterReleased: c(G),
                                        onFocusoutPrevented: c(Z),
                                        onReleaseRequested: c(K)
                                      },
                                      {
                                        default: f(() => [
                                          c(L)
                                            ? (t(),
                                              p(
                                                oe,
                                                R(
                                                  { key: 0, ref_key: 'dialogContentRef', ref: b },
                                                  e.$attrs,
                                                  {
                                                    'custom-class': e.customClass,
                                                    center: e.center,
                                                    'align-center': e.alignCenter,
                                                    'close-icon': e.closeIcon,
                                                    draggable: c(X),
                                                    fullscreen: e.fullscreen,
                                                    'show-close': e.showClose,
                                                    title: e.title,
                                                    onClose: c(H)
                                                  }
                                                ),
                                                A(
                                                  {
                                                    header: f(() => [
                                                      e.$slots.title
                                                        ? n(e.$slots, 'title', { key: 1 })
                                                        : n(e.$slots, 'header', {
                                                            key: 0,
                                                            close: c(H),
                                                            titleId: c(I),
                                                            titleClass: c(d).e('title')
                                                          })
                                                    ]),
                                                    default: f(() => [n(e.$slots, 'default')]),
                                                    _: 2
                                                  },
                                                  [
                                                    e.$slots.footer
                                                      ? {
                                                          name: 'footer',
                                                          fn: f(() => [n(e.$slots, 'footer')])
                                                        }
                                                      : void 0
                                                  ]
                                                ),
                                                1040,
                                                [
                                                  'custom-class',
                                                  'center',
                                                  'align-center',
                                                  'close-icon',
                                                  'draggable',
                                                  'fullscreen',
                                                  'show-close',
                                                  'title',
                                                  'onClose'
                                                ]
                                              ))
                                            : h('v-if', !0)
                                        ]),
                                        _: 3
                                      },
                                      8,
                                      [
                                        'trapped',
                                        'onFocusAfterTrapped',
                                        'onFocusAfterReleased',
                                        'onFocusoutPrevented',
                                        'onReleaseRequested'
                                      ]
                                    )
                                  ],
                                  46,
                                  se
                                )
                              ]),
                              _: 3
                            },
                            8,
                            ['mask', 'overlay-class', 'z-index']
                          ),
                          [[F, c(y)]]
                        )
                      ]),
                      _: 3
                    },
                    8,
                    ['onAfterEnter', 'onAfterLeave', 'onBeforeLeave']
                  )
                ],
                8,
                ['disabled']
              )
            )
          )
        }
      }),
      [
        [
          '__file',
          '/home/runner/work/element-plus/element-plus/packages/components/dialog/src/dialog.vue'
        ]
      ]
    )
  ),
  ae = { class: 'flex justify-between items-center h-54px pl-15px pr-15px relative' },
  re = {
    class:
      'h-54px flex justify-between items-center absolute top-[50%] right-15px translate-y-[-50%]'
  },
  ne = e({
    __name: 'Dialog',
    props: {
      modelValue: M.bool.def(!1),
      title: M.string.def('Dialog'),
      fullscreen: M.bool.def(!0),
      top: M.string.def('8vh'),
      height: M.oneOfType([String, Number]).def('500px'),
      width: M.oneOfType([String, Number]).def('700px')
    },
    setup(e) {
      const o = e,
        s = k(),
        a = l(() => {
          const e = ['fullscreen', 'title', 'height', 'top', 'width'],
            s = { ...T(), ...o }
          for (const o in s) -1 !== e.indexOf(o) && delete s[o]
          return s
        }),
        i = w(!1),
        m = () => {
          i.value = !c(i)
        },
        g = w(D(o.height) ? `${o.height}px` : o.height)
      L(
        () => i.value,
        async (e) => {
          if ((await B(), e)) {
            const e = document.documentElement.offsetHeight
            g.value = e - 55 - 60 - (s.footer ? 63 : 0) + 'px'
          } else g.value = D(o.height) ? `${o.height}px` : o.height
        },
        { immediate: !0 }
      )
      const b = l(() => ({ height: c(g) }))
      return (o, l) => {
        const g = S('Icon')
        return (
          t(),
          p(
            c(te),
            R(a.value, {
              fullscreen: i.value,
              'destroy-on-close': '',
              'lock-scroll': '',
              draggable: '',
              top: e.top,
              width: e.width,
              'close-on-click-modal': !1,
              'show-close': !1
            }),
            A(
              {
                header: f(({ close: s }) => [
                  r('div', ae, [
                    n(o.$slots, 'title', {}, () => [q(d(e.title), 1)]),
                    r('div', re, [
                      e.fullscreen
                        ? (t(),
                          p(
                            g,
                            {
                              key: 0,
                              class: 'cursor-pointer is-hover !h-54px mr-10px',
                              icon: i.value
                                ? 'radix-icons:exit-full-screen'
                                : 'radix-icons:enter-full-screen',
                              color: 'var(--el-color-info)',
                              'hover-color': 'var(--el-color-primary)',
                              onClick: m
                            },
                            null,
                            8,
                            ['icon']
                          ))
                        : h('', !0),
                      u(
                        g,
                        {
                          class: 'cursor-pointer is-hover !h-54px',
                          icon: 'ep:close',
                          'hover-color': 'var(--el-color-primary)',
                          color: 'var(--el-color-info)',
                          onClick: s
                        },
                        null,
                        8,
                        ['onClick']
                      )
                    ])
                  ])
                ]),
                default: f(() => [
                  u(
                    c(z),
                    { style: v(b.value) },
                    { default: f(() => [n(o.$slots, 'default')]), _: 3 },
                    8,
                    ['style']
                  )
                ]),
                _: 2
              },
              [
                c(s).footer
                  ? { name: 'footer', fn: f(() => [n(o.$slots, 'footer')]), key: '0' }
                  : void 0
              ]
            ),
            1040,
            ['fullscreen', 'top', 'width']
          )
        )
      }
    }
  })
export { ne as _ }
