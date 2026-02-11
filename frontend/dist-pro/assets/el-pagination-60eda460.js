import {
  b as e,
  a,
  e as t,
  a_ as n,
  f as l,
  o as r,
  j as s,
  z as i,
  l as o,
  m as p,
  p as u,
  k as d,
  E as c,
  _ as g,
  ao as b,
  d as v,
  an as f,
  c as m,
  u as y,
  r as h,
  w as C,
  x,
  a1 as k,
  a5 as P,
  s as z,
  y as S,
  bh as N,
  F as w,
  ci as _,
  dh as E,
  cj as T,
  aX as j,
  i as B,
  ax as A,
  ay as M,
  aq as I,
  am as U,
  ba as q,
  a$ as $,
  t as L,
  b7 as O,
  h as R,
  q as F,
  M as K,
  a6 as H,
  di as J
} from './index-820a519e.js'
import { a as V, E as W } from './el-select-38080147.js'
import { i as X } from './isEqual-cb9e370d.js'
import { E as D } from './el-input-5ae17c8f.js'
import { b as G, u as Q, E as Y } from './el-popper-797844d6.js'
import { d as Z } from './dropdown-394a0a1a.js'
const ee = Symbol('elPaginationKey'),
  ae = e({
    disabled: Boolean,
    currentPage: { type: Number, default: 1 },
    prevText: { type: String },
    prevIcon: { type: a }
  }),
  te = { click: (e) => e instanceof MouseEvent },
  ne = ['disabled', 'aria-label', 'aria-disabled'],
  le = { key: 0 },
  re = t({ name: 'ElPaginationPrev' })
var se = g(
  t({
    ...re,
    props: ae,
    emits: te,
    setup(e) {
      const a = e,
        { t: t } = n(),
        g = l(() => a.disabled || a.currentPage <= 1)
      return (e, a) => (
        r(),
        s(
          'button',
          {
            type: 'button',
            class: 'btn-prev',
            disabled: d(g),
            'aria-label': e.prevText || d(t)('el.pagination.prev'),
            'aria-disabled': d(g),
            onClick: a[0] || (a[0] = (a) => e.$emit('click', a))
          },
          [
            e.prevText
              ? (r(), s('span', le, i(e.prevText), 1))
              : (r(), o(d(c), { key: 1 }, { default: p(() => [(r(), o(u(e.prevIcon)))]), _: 1 }))
          ],
          8,
          ne
        )
      )
    }
  }),
  [
    [
      '__file',
      '/home/runner/work/element-plus/element-plus/packages/components/pagination/src/components/prev.vue'
    ]
  ]
)
const ie = e({
    disabled: Boolean,
    currentPage: { type: Number, default: 1 },
    pageCount: { type: Number, default: 50 },
    nextText: { type: String },
    nextIcon: { type: a }
  }),
  oe = ['disabled', 'aria-label', 'aria-disabled'],
  pe = { key: 0 },
  ue = t({ name: 'ElPaginationNext' })
var de = g(
  t({
    ...ue,
    props: ie,
    emits: ['click'],
    setup(e) {
      const a = e,
        { t: t } = n(),
        g = l(() => a.disabled || a.currentPage === a.pageCount || 0 === a.pageCount)
      return (e, a) => (
        r(),
        s(
          'button',
          {
            type: 'button',
            class: 'btn-next',
            disabled: d(g),
            'aria-label': e.nextText || d(t)('el.pagination.next'),
            'aria-disabled': d(g),
            onClick: a[0] || (a[0] = (a) => e.$emit('click', a))
          },
          [
            e.nextText
              ? (r(), s('span', pe, i(e.nextText), 1))
              : (r(), o(d(c), { key: 1 }, { default: p(() => [(r(), o(u(e.nextIcon)))]), _: 1 }))
          ],
          8,
          oe
        )
      )
    }
  }),
  [
    [
      '__file',
      '/home/runner/work/element-plus/element-plus/packages/components/pagination/src/components/next.vue'
    ]
  ]
)
const ce = () => b(ee, {}),
  ge = e({
    pageSize: { type: Number, required: !0 },
    pageSizes: { type: v(Array), default: () => f([10, 20, 30, 40, 50, 100]) },
    popperClass: { type: String },
    disabled: Boolean,
    size: { type: String, values: m }
  }),
  be = t({ name: 'ElPaginationSizes' })
var ve = g(
  t({
    ...be,
    props: ge,
    emits: ['page-size-change'],
    setup(e, { emit: a }) {
      const t = e,
        { t: i } = n(),
        u = y('pagination'),
        c = ce(),
        g = h(t.pageSize)
      ;(C(
        () => t.pageSizes,
        (e, n) => {
          if (!X(e, n) && Array.isArray(e)) {
            const n = e.includes(t.pageSize) ? t.pageSize : t.pageSizes[0]
            a('page-size-change', n)
          }
        }
      ),
        C(
          () => t.pageSize,
          (e) => {
            g.value = e
          }
        ))
      const b = l(() => t.pageSizes)
      function v(e) {
        var a
        e !== g.value && ((g.value = e), null == (a = c.handleSizeChange) || a.call(c, Number(e)))
      }
      return (e, a) => (
        r(),
        s(
          'span',
          { class: z(d(u).e('sizes')) },
          [
            x(
              d(W),
              {
                'model-value': g.value,
                disabled: e.disabled,
                'popper-class': e.popperClass,
                size: e.size,
                'validate-event': !1,
                onChange: v
              },
              {
                default: p(() => [
                  (r(!0),
                  s(
                    k,
                    null,
                    P(
                      d(b),
                      (e) => (
                        r(),
                        o(
                          d(V),
                          { key: e, value: e, label: e + d(i)('el.pagination.pagesize') },
                          null,
                          8,
                          ['value', 'label']
                        )
                      )
                    ),
                    128
                  ))
                ]),
                _: 1
              },
              8,
              ['model-value', 'disabled', 'popper-class', 'size']
            )
          ],
          2
        )
      )
    }
  }),
  [
    [
      '__file',
      '/home/runner/work/element-plus/element-plus/packages/components/pagination/src/components/sizes.vue'
    ]
  ]
)
const fe = e({ size: { type: String, values: m } }),
  me = ['disabled'],
  ye = t({ name: 'ElPaginationJumper' })
var he = g(
  t({
    ...ye,
    props: fe,
    setup(e) {
      const { t: a } = n(),
        t = y('pagination'),
        { pageCount: o, disabled: p, currentPage: u, changeEvent: c } = ce(),
        g = h(),
        b = l(() => {
          var e
          return null != (e = g.value) ? e : null == u ? void 0 : u.value
        })
      function v(e) {
        g.value = e ? +e : ''
      }
      function f(e) {
        ;((e = Math.trunc(+e)), null == c || c(e), (g.value = void 0))
      }
      return (e, n) => (
        r(),
        s(
          'span',
          { class: z(d(t).e('jump')), disabled: d(p) },
          [
            S('span', { class: z([d(t).e('goto')]) }, i(d(a)('el.pagination.goto')), 3),
            x(
              d(D),
              {
                size: e.size,
                class: z([d(t).e('editor'), d(t).is('in-pagination')]),
                min: 1,
                max: d(o),
                disabled: d(p),
                'model-value': d(b),
                'validate-event': !1,
                label: d(a)('el.pagination.page'),
                type: 'number',
                'onUpdate:modelValue': v,
                onChange: f
              },
              null,
              8,
              ['size', 'class', 'max', 'disabled', 'model-value', 'label']
            ),
            S(
              'span',
              { class: z([d(t).e('classifier')]) },
              i(d(a)('el.pagination.pageClassifier')),
              3
            )
          ],
          10,
          me
        )
      )
    }
  }),
  [
    [
      '__file',
      '/home/runner/work/element-plus/element-plus/packages/components/pagination/src/components/jumper.vue'
    ]
  ]
)
const Ce = e({ total: { type: Number, default: 1e3 } }),
  xe = ['disabled'],
  ke = t({ name: 'ElPaginationTotal' })
var Pe = g(
  t({
    ...ke,
    props: Ce,
    setup(e) {
      const { t: a } = n(),
        t = y('pagination'),
        { disabled: l } = ce()
      return (e, n) => (
        r(),
        s(
          'span',
          { class: z(d(t).e('total')), disabled: d(l) },
          i(d(a)('el.pagination.total', { total: e.total })),
          11,
          xe
        )
      )
    }
  }),
  [
    [
      '__file',
      '/home/runner/work/element-plus/element-plus/packages/components/pagination/src/components/total.vue'
    ]
  ]
)
const ze = e({
    currentPage: { type: Number, default: 1 },
    pageCount: { type: Number, required: !0 },
    pagerCount: { type: Number, default: 7 },
    disabled: Boolean
  }),
  Se = ['onKeyup'],
  Ne = ['aria-current', 'aria-label', 'tabindex'],
  we = ['tabindex', 'aria-label'],
  _e = ['aria-current', 'aria-label', 'tabindex'],
  Ee = ['tabindex', 'aria-label'],
  Te = ['aria-current', 'aria-label', 'tabindex'],
  je = t({ name: 'ElPaginationPager' })
var Be = g(
  t({
    ...je,
    props: ze,
    emits: ['change'],
    setup(e, { emit: a }) {
      const t = e,
        p = y('pager'),
        u = y('icon'),
        { t: c } = n(),
        g = h(!1),
        b = h(!1),
        v = h(!1),
        f = h(!1),
        m = h(!1),
        C = h(!1),
        x = l(() => {
          const e = t.pagerCount,
            a = (e - 1) / 2,
            n = Number(t.currentPage),
            l = Number(t.pageCount)
          let r = !1,
            s = !1
          l > e && (n > e - a && (r = !0), n < l - a && (s = !0))
          const i = []
          if (r && !s) {
            for (let a = l - (e - 2); a < l; a++) i.push(a)
          } else if (!r && s) for (let t = 2; t < e; t++) i.push(t)
          else if (r && s) {
            const a = Math.floor(e / 2) - 1
            for (let e = n - a; e <= n + a; e++) i.push(e)
          } else for (let t = 2; t < l; t++) i.push(t)
          return i
        }),
        S = l(() => ['more', 'btn-quickprev', u.b(), p.is('disabled', t.disabled)]),
        B = l(() => ['more', 'btn-quicknext', u.b(), p.is('disabled', t.disabled)]),
        A = l(() => (t.disabled ? -1 : 0))
      function M(e = !1) {
        t.disabled || (e ? (v.value = !0) : (f.value = !0))
      }
      function I(e = !1) {
        e ? (m.value = !0) : (C.value = !0)
      }
      function U(e) {
        const n = e.target
        if ('li' === n.tagName.toLowerCase() && Array.from(n.classList).includes('number')) {
          const e = Number(n.textContent)
          e !== t.currentPage && a('change', e)
        } else 'li' === n.tagName.toLowerCase() && Array.from(n.classList).includes('more') && q(e)
      }
      function q(e) {
        const n = e.target
        if ('ul' === n.tagName.toLowerCase() || t.disabled) return
        let l = Number(n.textContent)
        const r = t.pageCount,
          s = t.currentPage,
          i = t.pagerCount - 2
        ;(n.className.includes('more') &&
          (n.className.includes('quickprev')
            ? (l = s - i)
            : n.className.includes('quicknext') && (l = s + i)),
          Number.isNaN(+l) || (l < 1 && (l = 1), l > r && (l = r)),
          l !== s && a('change', l))
      }
      return (
        N(() => {
          const e = (t.pagerCount - 1) / 2
          ;((g.value = !1),
            (b.value = !1),
            t.pageCount > t.pagerCount &&
              (t.currentPage > t.pagerCount - e && (g.value = !0),
              t.currentPage < t.pageCount - e && (b.value = !0)))
        }),
        (e, a) => (
          r(),
          s(
            'ul',
            { class: z(d(p).b()), onClick: q, onKeyup: j(U, ['enter']) },
            [
              e.pageCount > 0
                ? (r(),
                  s(
                    'li',
                    {
                      key: 0,
                      class: z([
                        [d(p).is('active', 1 === e.currentPage), d(p).is('disabled', e.disabled)],
                        'number'
                      ]),
                      'aria-current': 1 === e.currentPage,
                      'aria-label': d(c)('el.pagination.currentPage', { pager: 1 }),
                      tabindex: d(A)
                    },
                    ' 1 ',
                    10,
                    Ne
                  ))
                : w('v-if', !0),
              g.value
                ? (r(),
                  s(
                    'li',
                    {
                      key: 1,
                      class: z(d(S)),
                      tabindex: d(A),
                      'aria-label': d(c)('el.pagination.prevPages', { pager: e.pagerCount - 2 }),
                      onMouseenter: a[0] || (a[0] = (e) => M(!0)),
                      onMouseleave: a[1] || (a[1] = (e) => (v.value = !1)),
                      onFocus: a[2] || (a[2] = (e) => I(!0)),
                      onBlur: a[3] || (a[3] = (e) => (m.value = !1))
                    },
                    [
                      (!v.value && !m.value) || e.disabled
                        ? (r(), o(d(E), { key: 1 }))
                        : (r(), o(d(_), { key: 0 }))
                    ],
                    42,
                    we
                  ))
                : w('v-if', !0),
              (r(!0),
              s(
                k,
                null,
                P(
                  d(x),
                  (a) => (
                    r(),
                    s(
                      'li',
                      {
                        key: a,
                        class: z([
                          [d(p).is('active', e.currentPage === a), d(p).is('disabled', e.disabled)],
                          'number'
                        ]),
                        'aria-current': e.currentPage === a,
                        'aria-label': d(c)('el.pagination.currentPage', { pager: a }),
                        tabindex: d(A)
                      },
                      i(a),
                      11,
                      _e
                    )
                  )
                ),
                128
              )),
              b.value
                ? (r(),
                  s(
                    'li',
                    {
                      key: 2,
                      class: z(d(B)),
                      tabindex: d(A),
                      'aria-label': d(c)('el.pagination.nextPages', { pager: e.pagerCount - 2 }),
                      onMouseenter: a[4] || (a[4] = (e) => M()),
                      onMouseleave: a[5] || (a[5] = (e) => (f.value = !1)),
                      onFocus: a[6] || (a[6] = (e) => I()),
                      onBlur: a[7] || (a[7] = (e) => (C.value = !1))
                    },
                    [
                      (!f.value && !C.value) || e.disabled
                        ? (r(), o(d(E), { key: 1 }))
                        : (r(), o(d(T), { key: 0 }))
                    ],
                    42,
                    Ee
                  ))
                : w('v-if', !0),
              e.pageCount > 1
                ? (r(),
                  s(
                    'li',
                    {
                      key: 3,
                      class: z([
                        [
                          d(p).is('active', e.currentPage === e.pageCount),
                          d(p).is('disabled', e.disabled)
                        ],
                        'number'
                      ]),
                      'aria-current': e.currentPage === e.pageCount,
                      'aria-label': d(c)('el.pagination.currentPage', { pager: e.pageCount }),
                      tabindex: d(A)
                    },
                    i(e.pageCount),
                    11,
                    Te
                  ))
                : w('v-if', !0)
            ],
            42,
            Se
          )
        )
      )
    }
  }),
  [
    [
      '__file',
      '/home/runner/work/element-plus/element-plus/packages/components/pagination/src/components/pager.vue'
    ]
  ]
)
const Ae = (e) => 'number' != typeof e,
  Me = e({
    pageSize: Number,
    defaultPageSize: Number,
    total: Number,
    pageCount: Number,
    pagerCount: {
      type: Number,
      validator: (e) => B(e) && Math.trunc(e) === e && e > 4 && e < 22 && e % 2 == 1,
      default: 7
    },
    currentPage: Number,
    defaultCurrentPage: Number,
    layout: {
      type: String,
      default: ['prev', 'pager', 'next', 'jumper', '->', 'total'].join(', ')
    },
    pageSizes: { type: v(Array), default: () => f([10, 20, 30, 40, 50, 100]) },
    popperClass: { type: String, default: '' },
    prevText: { type: String, default: '' },
    prevIcon: { type: a, default: () => A },
    nextText: { type: String, default: '' },
    nextIcon: { type: a, default: () => M },
    small: Boolean,
    background: Boolean,
    disabled: Boolean,
    hideOnSinglePage: Boolean
  }),
  Ie = 'ElPagination'
const Ue = L(
    t({
      name: Ie,
      props: Me,
      emits: {
        'update:current-page': (e) => B(e),
        'update:page-size': (e) => B(e),
        'size-change': (e) => B(e),
        'current-change': (e) => B(e),
        'prev-click': (e) => B(e),
        'next-click': (e) => B(e)
      },
      setup(e, { emit: a, slots: t }) {
        const { t: r } = n(),
          s = y('pagination'),
          i = I().vnode.props || {},
          o = 'onUpdate:currentPage' in i || 'onUpdate:current-page' in i || 'onCurrentChange' in i,
          p = 'onUpdate:pageSize' in i || 'onUpdate:page-size' in i || 'onSizeChange' in i,
          u = l(() => {
            if (Ae(e.total) && Ae(e.pageCount)) return !1
            if (!Ae(e.currentPage) && !o) return !1
            if (e.layout.includes('sizes'))
              if (Ae(e.pageCount)) {
                if (!Ae(e.total) && !Ae(e.pageSize) && !p) return !1
              } else if (!p) return !1
            return !0
          }),
          d = h(Ae(e.defaultPageSize) ? 10 : e.defaultPageSize),
          c = h(Ae(e.defaultCurrentPage) ? 1 : e.defaultCurrentPage),
          g = l({
            get: () => (Ae(e.pageSize) ? d.value : e.pageSize),
            set(t) {
              ;(Ae(e.pageSize) && (d.value = t),
                p && (a('update:page-size', t), a('size-change', t)))
            }
          }),
          b = l(() => {
            let a = 0
            return (
              Ae(e.pageCount)
                ? Ae(e.total) || (a = Math.max(1, Math.ceil(e.total / g.value)))
                : (a = e.pageCount),
              a
            )
          }),
          v = l({
            get: () => (Ae(e.currentPage) ? c.value : e.currentPage),
            set(t) {
              let n = t
              ;(t < 1 ? (n = 1) : t > b.value && (n = b.value),
                Ae(e.currentPage) && (c.value = n),
                o && (a('update:current-page', n), a('current-change', n)))
            }
          })
        function f(e) {
          v.value = e
        }
        function m() {
          e.disabled || ((v.value -= 1), a('prev-click', v.value))
        }
        function x() {
          e.disabled || ((v.value += 1), a('next-click', v.value))
        }
        function k(e, a) {
          e && (e.props || (e.props = {}), (e.props.class = [e.props.class, a].join(' ')))
        }
        return (
          C(b, (e) => {
            v.value > e && (v.value = e)
          }),
          U(ee, {
            pageCount: b,
            disabled: l(() => e.disabled),
            currentPage: v,
            changeEvent: f,
            handleSizeChange: function (e) {
              g.value = e
              const a = b.value
              v.value > a && (v.value = a)
            }
          }),
          () => {
            var a, n
            if (!u.value) return (q(Ie, r('el.pagination.deprecationWarning')), null)
            if (!e.layout) return null
            if (e.hideOnSinglePage && b.value <= 1) return null
            const l = [],
              i = [],
              o = $('div', { class: s.e('rightwrapper') }, i),
              p = {
                prev: $(se, {
                  disabled: e.disabled,
                  currentPage: v.value,
                  prevText: e.prevText,
                  prevIcon: e.prevIcon,
                  onClick: m
                }),
                jumper: $(he, { size: e.small ? 'small' : 'default' }),
                pager: $(Be, {
                  currentPage: v.value,
                  pageCount: b.value,
                  pagerCount: e.pagerCount,
                  onChange: f,
                  disabled: e.disabled
                }),
                next: $(de, {
                  disabled: e.disabled,
                  currentPage: v.value,
                  pageCount: b.value,
                  nextText: e.nextText,
                  nextIcon: e.nextIcon,
                  onClick: x
                }),
                sizes: $(ve, {
                  pageSize: g.value,
                  pageSizes: e.pageSizes,
                  popperClass: e.popperClass,
                  disabled: e.disabled,
                  size: e.small ? 'small' : 'default'
                }),
                slot:
                  null != (n = null == (a = null == t ? void 0 : t.default) ? void 0 : a.call(t))
                    ? n
                    : null,
                total: $(Pe, { total: Ae(e.total) ? 0 : e.total })
              },
              d = e.layout.split(',').map((e) => e.trim())
            let c = !1
            return (
              d.forEach((e) => {
                '->' !== e ? (c ? i.push(p[e]) : l.push(p[e])) : (c = !0)
              }),
              k(l[0], s.is('first')),
              k(l[l.length - 1], s.is('last')),
              c &&
                i.length > 0 &&
                (k(i[0], s.is('first')), k(i[i.length - 1], s.is('last')), l.push(o)),
              $(
                'div',
                { class: [s.b(), s.is('background', e.background), { [s.m('small')]: e.small }] },
                l
              )
            )
          }
        )
      }
    })
  ),
  qe = e({
    trigger: G.trigger,
    placement: Z.placement,
    disabled: G.disabled,
    visible: Q.visible,
    transition: Q.transition,
    popperOptions: Z.popperOptions,
    tabindex: Z.tabindex,
    content: Q.content,
    popperStyle: Q.popperStyle,
    popperClass: Q.popperClass,
    enterable: { ...Q.enterable, default: !0 },
    effect: { ...Q.effect, default: 'light' },
    teleported: Q.teleported,
    title: String,
    width: { type: [String, Number], default: 150 },
    offset: { type: Number, default: void 0 },
    showAfter: { type: Number, default: 0 },
    hideAfter: { type: Number, default: 200 },
    autoClose: { type: Number, default: 0 },
    showArrow: { type: Boolean, default: !0 },
    persistent: { type: Boolean, default: !0 },
    'onUpdate:visible': { type: Function }
  }),
  $e = {
    'update:visible': (e) => O(e),
    'before-enter': () => !0,
    'before-leave': () => !0,
    'after-enter': () => !0,
    'after-leave': () => !0
  },
  Le = t({ name: 'ElPopover' }),
  Oe = t({
    ...Le,
    props: qe,
    emits: $e,
    setup(e, { expose: a, emit: t }) {
      const n = e,
        u = l(() => n['onUpdate:visible']),
        c = y('popover'),
        g = h(),
        b = l(() => {
          var e
          return null == (e = d(g)) ? void 0 : e.popperRef
        }),
        v = l(() => [{ width: R(n.width) }, n.popperStyle]),
        f = l(() => [c.b(), n.popperClass, { [c.m('plain')]: !!n.content }]),
        m = l(() => n.transition === `${c.namespace.value}-fade-in-linear`),
        C = () => {
          t('before-enter')
        },
        x = () => {
          t('before-leave')
        },
        k = () => {
          t('after-enter')
        },
        P = () => {
          ;(t('update:visible', !1), t('after-leave'))
        }
      return (
        a({
          popperRef: b,
          hide: () => {
            var e
            null == (e = g.value) || e.hide()
          }
        }),
        (e, a) => (
          r(),
          o(
            d(Y),
            H({ ref_key: 'tooltipRef', ref: g }, e.$attrs, {
              trigger: e.trigger,
              placement: e.placement,
              disabled: e.disabled,
              visible: e.visible,
              transition: e.transition,
              'popper-options': e.popperOptions,
              tabindex: e.tabindex,
              content: e.content,
              offset: e.offset,
              'show-after': e.showAfter,
              'hide-after': e.hideAfter,
              'auto-close': e.autoClose,
              'show-arrow': e.showArrow,
              'aria-label': e.title,
              effect: e.effect,
              enterable: e.enterable,
              'popper-class': d(f),
              'popper-style': d(v),
              teleported: e.teleported,
              persistent: e.persistent,
              'gpu-acceleration': d(m),
              'onUpdate:visible': d(u),
              onBeforeShow: C,
              onBeforeHide: x,
              onShow: k,
              onHide: P
            }),
            {
              content: p(() => [
                e.title
                  ? (r(),
                    s('div', { key: 0, class: z(d(c).e('title')), role: 'title' }, i(e.title), 3))
                  : w('v-if', !0),
                F(e.$slots, 'default', {}, () => [K(i(e.content), 1)])
              ]),
              default: p(() => [
                e.$slots.reference ? F(e.$slots, 'reference', { key: 0 }) : w('v-if', !0)
              ]),
              _: 3
            },
            16,
            [
              'trigger',
              'placement',
              'disabled',
              'visible',
              'transition',
              'popper-options',
              'tabindex',
              'content',
              'offset',
              'show-after',
              'hide-after',
              'auto-close',
              'show-arrow',
              'aria-label',
              'effect',
              'enterable',
              'popper-class',
              'popper-style',
              'teleported',
              'persistent',
              'gpu-acceleration',
              'onUpdate:visible'
            ]
          )
        )
      )
    }
  })
const Re = (e, a) => {
  const t = a.arg || a.value,
    n = null == t ? void 0 : t.popperRef
  n && (n.triggerRef = e)
}
const Fe = L(
  g(Oe, [
    [
      '__file',
      '/home/runner/work/element-plus/element-plus/packages/components/popover/src/popover.vue'
    ]
  ]),
  {
    directive: J(
      {
        mounted(e, a) {
          Re(e, a)
        },
        updated(e, a) {
          Re(e, a)
        }
      },
      'popover'
    )
  }
)
export { Fe as E, Ue as a }
