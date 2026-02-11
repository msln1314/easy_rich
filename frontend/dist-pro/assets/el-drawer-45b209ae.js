import {
  b as e,
  _ as s,
  e as a,
  E as t,
  az as l,
  aB as r,
  f as o,
  r as i,
  u as d,
  a_ as n,
  h as c,
  b1 as f,
  o as u,
  l as p,
  x as m,
  m as b,
  a0 as y,
  y as v,
  a6 as h,
  aY as w,
  s as k,
  j as C,
  q as E,
  z,
  F as R,
  aH as S,
  D as g,
  bZ as I,
  t as $
} from './index-820a519e.js'
import { E as _ } from './el-overlay-34b9d092.js'
import { b as x, c as A, u as L } from './use-dialog-2de816dc.js'
import { E as B } from './focus-trap-949626e0.js'
const j = a({
    name: 'ElDrawer',
    components: { ElOverlay: _, ElFocusTrap: B, ElIcon: t, Close: l },
    inheritAttrs: !1,
    props: e({
      ...x,
      direction: { type: String, default: 'rtl', values: ['ltr', 'rtl', 'ttb', 'btt'] },
      size: { type: [String, Number], default: '30%' },
      withHeader: { type: Boolean, default: !0 },
      modalFade: { type: Boolean, default: !0 }
    }),
    emits: A,
    setup(e, { slots: s }) {
      ;(r(
        {
          scope: 'el-drawer',
          from: 'the title slot',
          replacement: 'the header slot',
          version: '3.0.0',
          ref: 'https://element-plus.org/en-US/component/drawer.html#slots'
        },
        o(() => !!s.title)
      ),
        r(
          {
            scope: 'el-drawer',
            from: 'custom-class',
            replacement: 'class',
            version: '2.3.0',
            ref: 'https://element-plus.org/en-US/component/drawer.html#attributes',
            type: 'Attribute'
          },
          o(() => !!e.customClass)
        ))
      const a = i(),
        t = i(),
        l = d('drawer'),
        { t: f } = n(),
        u = o(() => 'rtl' === e.direction || 'ltr' === e.direction),
        p = o(() => c(e.size))
      return {
        ...L(e, a),
        drawerRef: a,
        focusStartRef: t,
        isHorizontal: u,
        drawerSize: p,
        ns: l,
        t: f
      }
    }
  }),
  H = ['aria-label', 'aria-labelledby', 'aria-describedby'],
  q = ['id'],
  D = ['aria-label'],
  T = ['id']
const F = $(
  s(j, [
    [
      'render',
      function (e, s, a, t, l, r) {
        const o = f('close'),
          i = f('el-icon'),
          d = f('el-focus-trap'),
          n = f('el-overlay')
        return (
          u(),
          p(
            I,
            { to: 'body', disabled: !e.appendToBody },
            [
              m(
                g,
                {
                  name: e.ns.b('fade'),
                  onAfterEnter: e.afterEnter,
                  onAfterLeave: e.afterLeave,
                  onBeforeLeave: e.beforeLeave,
                  persisted: ''
                },
                {
                  default: b(() => [
                    y(
                      m(
                        n,
                        {
                          mask: e.modal,
                          'overlay-class': e.modalClass,
                          'z-index': e.zIndex,
                          onClick: e.onModalClick
                        },
                        {
                          default: b(() => [
                            m(
                              d,
                              {
                                loop: '',
                                trapped: e.visible,
                                'focus-trap-el': e.drawerRef,
                                'focus-start-el': e.focusStartRef,
                                onReleaseRequested: e.onCloseRequested
                              },
                              {
                                default: b(() => [
                                  v(
                                    'div',
                                    h(
                                      {
                                        ref: 'drawerRef',
                                        'aria-modal': 'true',
                                        'aria-label': e.title || void 0,
                                        'aria-labelledby': e.title ? void 0 : e.titleId,
                                        'aria-describedby': e.bodyId
                                      },
                                      e.$attrs,
                                      {
                                        class: [
                                          e.ns.b(),
                                          e.direction,
                                          e.visible && 'open',
                                          e.customClass
                                        ],
                                        style: e.isHorizontal
                                          ? 'width: ' + e.drawerSize
                                          : 'height: ' + e.drawerSize,
                                        role: 'dialog',
                                        onClick: s[1] || (s[1] = w(() => {}, ['stop']))
                                      }
                                    ),
                                    [
                                      v(
                                        'span',
                                        {
                                          ref: 'focusStartRef',
                                          class: k(e.ns.e('sr-focus')),
                                          tabindex: '-1'
                                        },
                                        null,
                                        2
                                      ),
                                      e.withHeader
                                        ? (u(),
                                          C(
                                            'header',
                                            { key: 0, class: k(e.ns.e('header')) },
                                            [
                                              e.$slots.title
                                                ? E(e.$slots, 'title', { key: 1 }, () => [
                                                    R(' DEPRECATED SLOT ')
                                                  ])
                                                : E(
                                                    e.$slots,
                                                    'header',
                                                    {
                                                      key: 0,
                                                      close: e.handleClose,
                                                      titleId: e.titleId,
                                                      titleClass: e.ns.e('title')
                                                    },
                                                    () => [
                                                      e.$slots.title
                                                        ? R('v-if', !0)
                                                        : (u(),
                                                          C(
                                                            'span',
                                                            {
                                                              key: 0,
                                                              id: e.titleId,
                                                              role: 'heading',
                                                              class: k(e.ns.e('title'))
                                                            },
                                                            z(e.title),
                                                            11,
                                                            q
                                                          ))
                                                    ]
                                                  ),
                                              e.showClose
                                                ? (u(),
                                                  C(
                                                    'button',
                                                    {
                                                      key: 2,
                                                      'aria-label': e.t('el.drawer.close'),
                                                      class: k(e.ns.e('close-btn')),
                                                      type: 'button',
                                                      onClick:
                                                        s[0] ||
                                                        (s[0] = (...s) =>
                                                          e.handleClose && e.handleClose(...s))
                                                    },
                                                    [
                                                      m(
                                                        i,
                                                        { class: k(e.ns.e('close')) },
                                                        { default: b(() => [m(o)]), _: 1 },
                                                        8,
                                                        ['class']
                                                      )
                                                    ],
                                                    10,
                                                    D
                                                  ))
                                                : R('v-if', !0)
                                            ],
                                            2
                                          ))
                                        : R('v-if', !0),
                                      e.rendered
                                        ? (u(),
                                          C(
                                            'div',
                                            { key: 1, id: e.bodyId, class: k(e.ns.e('body')) },
                                            [E(e.$slots, 'default')],
                                            10,
                                            T
                                          ))
                                        : R('v-if', !0),
                                      e.$slots.footer
                                        ? (u(),
                                          C(
                                            'div',
                                            { key: 2, class: k(e.ns.e('footer')) },
                                            [E(e.$slots, 'footer')],
                                            2
                                          ))
                                        : R('v-if', !0)
                                    ],
                                    16,
                                    H
                                  )
                                ]),
                                _: 3
                              },
                              8,
                              ['trapped', 'focus-trap-el', 'focus-start-el', 'onReleaseRequested']
                            )
                          ]),
                          _: 3
                        },
                        8,
                        ['mask', 'overlay-class', 'z-index', 'onClick']
                      ),
                      [[S, e.visible]]
                    )
                  ]),
                  _: 3
                },
                8,
                ['name', 'onAfterEnter', 'onAfterLeave', 'onBeforeLeave']
              )
            ],
            8,
            ['disabled']
          )
        )
      }
    ],
    [
      '__file',
      '/home/runner/work/element-plus/element-plus/packages/components/drawer/src/drawer.vue'
    ]
  ])
)
export { F as E }
