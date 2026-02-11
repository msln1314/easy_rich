import {
  as as e,
  aA as n,
  _ as o,
  e as t,
  N as a,
  E as s,
  dc as l,
  dd as r,
  f as i,
  r as c,
  L as u,
  de as d,
  bL as p,
  w as f,
  a2 as m,
  aj as v,
  bw as g,
  b1 as y,
  o as b,
  l as h,
  m as C,
  a0 as E,
  x,
  y as w,
  s as B,
  n as k,
  aY as M,
  j as T,
  p as I,
  F as S,
  z,
  aX as R,
  q as _,
  M as A,
  aH as L,
  D as j,
  aJ as P,
  g as V,
  ag as $,
  df as O,
  bg as H,
  ap as D,
  aD as K,
  b3 as q,
  bX as F
} from './index-820a519e.js'
import { E as U } from './el-input-5ae17c8f.js'
import { E as X, u as J, a as N } from './el-overlay-34b9d092.js'
import { o as W } from './useForm-c59a8d29.js'
import { E as Y } from './focus-trap-949626e0.js'
import { i as Z } from './validator-a9d8fe4c.js'
import { u as G } from './index-2b3f7e71.js'
const Q = '_trap-focus-children',
  ee = [],
  ne = (e) => {
    if (0 === ee.length) return
    const o = ee[ee.length - 1][Q]
    if (o.length > 0 && e.code === n.tab) {
      if (1 === o.length)
        return (e.preventDefault(), void (document.activeElement !== o[0] && o[0].focus()))
      const n = e.shiftKey,
        t = e.target === o[0],
        a = e.target === o[o.length - 1]
      ;(t && n && (e.preventDefault(), o[o.length - 1].focus()),
        a && !n && (e.preventDefault(), o[0].focus()))
    }
  },
  oe = t({
    name: 'ElMessageBox',
    directives: {
      TrapFocus: {
        beforeMount(e) {
          ;((e[Q] = W(e)), ee.push(e), ee.length <= 1 && document.addEventListener('keydown', ne))
        },
        updated(n) {
          e(() => {
            n[Q] = W(n)
          })
        },
        unmounted() {
          ;(ee.shift(), 0 === ee.length && document.removeEventListener('keydown', ne))
        }
      }
    },
    components: { ElButton: a, ElFocusTrap: Y, ElInput: U, ElOverlay: X, ElIcon: s, ...l },
    inheritAttrs: !1,
    props: {
      buttonSize: { type: String, validator: Z },
      modal: { type: Boolean, default: !0 },
      lockScroll: { type: Boolean, default: !0 },
      showClose: { type: Boolean, default: !0 },
      closeOnClickModal: { type: Boolean, default: !0 },
      closeOnPressEscape: { type: Boolean, default: !0 },
      closeOnHashChange: { type: Boolean, default: !0 },
      center: Boolean,
      draggable: Boolean,
      roundButton: { default: !1, type: Boolean },
      container: { type: String, default: 'body' },
      boxType: { type: String, default: '' }
    },
    emits: ['vanish', 'action'],
    setup(n, { emit: o }) {
      const {
          locale: t,
          zIndex: a,
          ns: s,
          size: l
        } = r(
          'message-box',
          i(() => n.buttonSize)
        ),
        { t: y } = t,
        { nextZIndex: b } = a,
        h = c(!1),
        C = u({
          autofocus: !0,
          beforeClose: null,
          callback: null,
          cancelButtonText: '',
          cancelButtonClass: '',
          confirmButtonText: '',
          confirmButtonClass: '',
          customClass: '',
          customStyle: {},
          dangerouslyUseHTMLString: !1,
          distinguishCancelAndClose: !1,
          icon: '',
          inputPattern: null,
          inputPlaceholder: '',
          inputType: 'text',
          inputValue: null,
          inputValidator: null,
          inputErrorMessage: '',
          message: null,
          modalFade: !0,
          modalClass: '',
          showCancelButton: !1,
          showConfirmButton: !0,
          type: '',
          title: void 0,
          showInput: !1,
          action: '',
          confirmButtonLoading: !1,
          cancelButtonLoading: !1,
          confirmButtonDisabled: !1,
          editorErrorMessage: '',
          validateError: !1,
          zIndex: b()
        }),
        E = i(() => {
          const e = C.type
          return { [s.bm('icon', e)]: e && d[e] }
        }),
        x = p(),
        w = p(),
        B = i(() => C.icon || d[C.type] || ''),
        k = i(() => !!C.message),
        M = c(),
        T = c(),
        I = c(),
        S = c(),
        z = c(),
        R = i(() => C.confirmButtonClass)
      ;(f(
        () => C.inputValue,
        async (o) => {
          ;(await e(), 'prompt' === n.boxType && null !== o && V())
        },
        { immediate: !0 }
      ),
        f(
          () => h.value,
          (o) => {
            var t, a
            ;(o &&
              ('prompt' !== n.boxType &&
                (C.autofocus
                  ? (I.value = null != (a = null == (t = z.value) ? void 0 : t.$el) ? a : M.value)
                  : (I.value = M.value)),
              (C.zIndex = b())),
              'prompt' === n.boxType &&
                (o
                  ? e().then(() => {
                      var e
                      S.value &&
                        S.value.$el &&
                        (C.autofocus
                          ? (I.value = null != (e = $()) ? e : M.value)
                          : (I.value = M.value))
                    })
                  : ((C.editorErrorMessage = ''), (C.validateError = !1))))
          }
        ))
      const _ = i(() => n.draggable)
      function A() {
        h.value &&
          ((h.value = !1),
          e(() => {
            C.action && o('action', C.action)
          }))
      }
      ;(G(M, T, _),
        m(async () => {
          ;(await e(), n.closeOnHashChange && window.addEventListener('hashchange', A))
        }),
        v(() => {
          n.closeOnHashChange && window.removeEventListener('hashchange', A)
        }))
      const L = () => {
          n.closeOnClickModal && P(C.distinguishCancelAndClose ? 'close' : 'cancel')
        },
        j = N(L),
        P = (e) => {
          var o
          ;('prompt' !== n.boxType || 'confirm' !== e || V()) &&
            ((C.action = e),
            C.beforeClose ? null == (o = C.beforeClose) || o.call(C, e, C, A) : A())
        },
        V = () => {
          if ('prompt' === n.boxType) {
            const e = C.inputPattern
            if (e && !e.test(C.inputValue || ''))
              return (
                (C.editorErrorMessage = C.inputErrorMessage || y('el.messagebox.error')),
                (C.validateError = !0),
                !1
              )
            const n = C.inputValidator
            if ('function' == typeof n) {
              const e = n(C.inputValue)
              if (!1 === e)
                return (
                  (C.editorErrorMessage = C.inputErrorMessage || y('el.messagebox.error')),
                  (C.validateError = !0),
                  !1
                )
              if ('string' == typeof e)
                return ((C.editorErrorMessage = e), (C.validateError = !0), !1)
            }
          }
          return ((C.editorErrorMessage = ''), (C.validateError = !1), !0)
        },
        $ = () => {
          const e = S.value.$refs
          return e.input || e.textarea
        },
        O = () => {
          P('close')
        }
      return (
        n.lockScroll && J(h),
        {
          ...g(C),
          ns: s,
          overlayEvent: j,
          visible: h,
          hasMessage: k,
          typeClass: E,
          contentId: x,
          inputId: w,
          btnSize: l,
          iconComponent: B,
          confirmButtonClasses: R,
          rootRef: M,
          focusStartRef: I,
          headerRef: T,
          inputRef: S,
          confirmRef: z,
          doClose: A,
          handleClose: O,
          onCloseRequested: () => {
            n.closeOnPressEscape && O()
          },
          handleWrapperClick: L,
          handleInputEnter: (e) => {
            if ('textarea' !== C.inputType) return (e.preventDefault(), P('confirm'))
          },
          handleAction: P,
          t: y
        }
      )
    }
  }),
  te = ['aria-label', 'aria-describedby'],
  ae = ['aria-label'],
  se = ['id']
var le = o(oe, [
  [
    'render',
    function (e, n, o, t, a, s) {
      const l = y('el-icon'),
        r = y('close'),
        i = y('el-input'),
        c = y('el-button'),
        u = y('el-focus-trap'),
        d = y('el-overlay')
      return (
        b(),
        h(
          j,
          {
            name: 'fade-in-linear',
            onAfterLeave: n[11] || (n[11] = (n) => e.$emit('vanish')),
            persisted: ''
          },
          {
            default: C(() => [
              E(
                x(
                  d,
                  {
                    'z-index': e.zIndex,
                    'overlay-class': [e.ns.is('message-box'), e.modalClass],
                    mask: e.modal
                  },
                  {
                    default: C(() => [
                      w(
                        'div',
                        {
                          role: 'dialog',
                          'aria-label': e.title,
                          'aria-modal': 'true',
                          'aria-describedby': e.showInput ? void 0 : e.contentId,
                          class: B(`${e.ns.namespace.value}-overlay-message-box`),
                          onClick:
                            n[8] ||
                            (n[8] = (...n) =>
                              e.overlayEvent.onClick && e.overlayEvent.onClick(...n)),
                          onMousedown:
                            n[9] ||
                            (n[9] = (...n) =>
                              e.overlayEvent.onMousedown && e.overlayEvent.onMousedown(...n)),
                          onMouseup:
                            n[10] ||
                            (n[10] = (...n) =>
                              e.overlayEvent.onMouseup && e.overlayEvent.onMouseup(...n))
                        },
                        [
                          x(
                            u,
                            {
                              loop: '',
                              trapped: e.visible,
                              'focus-trap-el': e.rootRef,
                              'focus-start-el': e.focusStartRef,
                              onReleaseRequested: e.onCloseRequested
                            },
                            {
                              default: C(() => [
                                w(
                                  'div',
                                  {
                                    ref: 'rootRef',
                                    class: B([
                                      e.ns.b(),
                                      e.customClass,
                                      e.ns.is('draggable', e.draggable),
                                      { [e.ns.m('center')]: e.center }
                                    ]),
                                    style: k(e.customStyle),
                                    tabindex: '-1',
                                    onClick: n[7] || (n[7] = M(() => {}, ['stop']))
                                  },
                                  [
                                    null !== e.title && void 0 !== e.title
                                      ? (b(),
                                        T(
                                          'div',
                                          { key: 0, ref: 'headerRef', class: B(e.ns.e('header')) },
                                          [
                                            w(
                                              'div',
                                              { class: B(e.ns.e('title')) },
                                              [
                                                e.iconComponent && e.center
                                                  ? (b(),
                                                    h(
                                                      l,
                                                      {
                                                        key: 0,
                                                        class: B([e.ns.e('status'), e.typeClass])
                                                      },
                                                      {
                                                        default: C(() => [
                                                          (b(), h(I(e.iconComponent)))
                                                        ]),
                                                        _: 1
                                                      },
                                                      8,
                                                      ['class']
                                                    ))
                                                  : S('v-if', !0),
                                                w('span', null, z(e.title), 1)
                                              ],
                                              2
                                            ),
                                            e.showClose
                                              ? (b(),
                                                T(
                                                  'button',
                                                  {
                                                    key: 0,
                                                    type: 'button',
                                                    class: B(e.ns.e('headerbtn')),
                                                    'aria-label': e.t('el.messagebox.close'),
                                                    onClick:
                                                      n[0] ||
                                                      (n[0] = (n) =>
                                                        e.handleAction(
                                                          e.distinguishCancelAndClose
                                                            ? 'close'
                                                            : 'cancel'
                                                        )),
                                                    onKeydown:
                                                      n[1] ||
                                                      (n[1] = R(
                                                        M(
                                                          (n) =>
                                                            e.handleAction(
                                                              e.distinguishCancelAndClose
                                                                ? 'close'
                                                                : 'cancel'
                                                            ),
                                                          ['prevent']
                                                        ),
                                                        ['enter']
                                                      ))
                                                  },
                                                  [
                                                    x(
                                                      l,
                                                      { class: B(e.ns.e('close')) },
                                                      { default: C(() => [x(r)]), _: 1 },
                                                      8,
                                                      ['class']
                                                    )
                                                  ],
                                                  42,
                                                  ae
                                                ))
                                              : S('v-if', !0)
                                          ],
                                          2
                                        ))
                                      : S('v-if', !0),
                                    w(
                                      'div',
                                      { id: e.contentId, class: B(e.ns.e('content')) },
                                      [
                                        w(
                                          'div',
                                          { class: B(e.ns.e('container')) },
                                          [
                                            e.iconComponent && !e.center && e.hasMessage
                                              ? (b(),
                                                h(
                                                  l,
                                                  {
                                                    key: 0,
                                                    class: B([e.ns.e('status'), e.typeClass])
                                                  },
                                                  {
                                                    default: C(() => [
                                                      (b(), h(I(e.iconComponent)))
                                                    ]),
                                                    _: 1
                                                  },
                                                  8,
                                                  ['class']
                                                ))
                                              : S('v-if', !0),
                                            e.hasMessage
                                              ? (b(),
                                                T(
                                                  'div',
                                                  { key: 1, class: B(e.ns.e('message')) },
                                                  [
                                                    _(e.$slots, 'default', {}, () => [
                                                      e.dangerouslyUseHTMLString
                                                        ? (b(),
                                                          h(
                                                            I(e.showInput ? 'label' : 'p'),
                                                            {
                                                              key: 1,
                                                              for: e.showInput ? e.inputId : void 0,
                                                              innerHTML: e.message
                                                            },
                                                            null,
                                                            8,
                                                            ['for', 'innerHTML']
                                                          ))
                                                        : (b(),
                                                          h(
                                                            I(e.showInput ? 'label' : 'p'),
                                                            {
                                                              key: 0,
                                                              for: e.showInput ? e.inputId : void 0
                                                            },
                                                            {
                                                              default: C(() => [
                                                                A(
                                                                  z(
                                                                    e.dangerouslyUseHTMLString
                                                                      ? ''
                                                                      : e.message
                                                                  ),
                                                                  1
                                                                )
                                                              ]),
                                                              _: 1
                                                            },
                                                            8,
                                                            ['for']
                                                          ))
                                                    ])
                                                  ],
                                                  2
                                                ))
                                              : S('v-if', !0)
                                          ],
                                          2
                                        ),
                                        E(
                                          w(
                                            'div',
                                            { class: B(e.ns.e('input')) },
                                            [
                                              x(
                                                i,
                                                {
                                                  id: e.inputId,
                                                  ref: 'inputRef',
                                                  modelValue: e.inputValue,
                                                  'onUpdate:modelValue':
                                                    n[2] || (n[2] = (n) => (e.inputValue = n)),
                                                  type: e.inputType,
                                                  placeholder: e.inputPlaceholder,
                                                  'aria-invalid': e.validateError,
                                                  class: B({ invalid: e.validateError }),
                                                  onKeydown: R(e.handleInputEnter, ['enter'])
                                                },
                                                null,
                                                8,
                                                [
                                                  'id',
                                                  'modelValue',
                                                  'type',
                                                  'placeholder',
                                                  'aria-invalid',
                                                  'class',
                                                  'onKeydown'
                                                ]
                                              ),
                                              w(
                                                'div',
                                                {
                                                  class: B(e.ns.e('errormsg')),
                                                  style: k({
                                                    visibility: e.editorErrorMessage
                                                      ? 'visible'
                                                      : 'hidden'
                                                  })
                                                },
                                                z(e.editorErrorMessage),
                                                7
                                              )
                                            ],
                                            2
                                          ),
                                          [[L, e.showInput]]
                                        )
                                      ],
                                      10,
                                      se
                                    ),
                                    w(
                                      'div',
                                      { class: B(e.ns.e('btns')) },
                                      [
                                        e.showCancelButton
                                          ? (b(),
                                            h(
                                              c,
                                              {
                                                key: 0,
                                                loading: e.cancelButtonLoading,
                                                class: B([e.cancelButtonClass]),
                                                round: e.roundButton,
                                                size: e.btnSize,
                                                onClick:
                                                  n[3] || (n[3] = (n) => e.handleAction('cancel')),
                                                onKeydown:
                                                  n[4] ||
                                                  (n[4] = R(
                                                    M((n) => e.handleAction('cancel'), ['prevent']),
                                                    ['enter']
                                                  ))
                                              },
                                              {
                                                default: C(() => [
                                                  A(
                                                    z(
                                                      e.cancelButtonText ||
                                                        e.t('el.messagebox.cancel')
                                                    ),
                                                    1
                                                  )
                                                ]),
                                                _: 1
                                              },
                                              8,
                                              ['loading', 'class', 'round', 'size']
                                            ))
                                          : S('v-if', !0),
                                        E(
                                          x(
                                            c,
                                            {
                                              ref: 'confirmRef',
                                              type: 'primary',
                                              loading: e.confirmButtonLoading,
                                              class: B([e.confirmButtonClasses]),
                                              round: e.roundButton,
                                              disabled: e.confirmButtonDisabled,
                                              size: e.btnSize,
                                              onClick:
                                                n[5] || (n[5] = (n) => e.handleAction('confirm')),
                                              onKeydown:
                                                n[6] ||
                                                (n[6] = R(
                                                  M((n) => e.handleAction('confirm'), ['prevent']),
                                                  ['enter']
                                                ))
                                            },
                                            {
                                              default: C(() => [
                                                A(
                                                  z(
                                                    e.confirmButtonText ||
                                                      e.t('el.messagebox.confirm')
                                                  ),
                                                  1
                                                )
                                              ]),
                                              _: 1
                                            },
                                            8,
                                            ['loading', 'class', 'round', 'disabled', 'size']
                                          ),
                                          [[L, e.showConfirmButton]]
                                        )
                                      ],
                                      2
                                    )
                                  ],
                                  6
                                )
                              ]),
                              _: 3
                            },
                            8,
                            ['trapped', 'focus-trap-el', 'focus-start-el', 'onReleaseRequested']
                          )
                        ],
                        42,
                        te
                      )
                    ]),
                    _: 3
                  },
                  8,
                  ['z-index', 'overlay-class', 'mask']
                ),
                [[L, e.visible]]
              )
            ]),
            _: 3
          }
        )
      )
    }
  ],
  [
    '__file',
    '/home/runner/work/element-plus/element-plus/packages/components/message-box/src/index.vue'
  ]
])
const re = new Map(),
  ie = (e, n, o = null) => {
    const t = x(
      le,
      e,
      q(e.message) || $(e.message) ? { default: q(e.message) ? e.message : () => e.message } : null
    )
    return (
      (t.appContext = o),
      O(t, n),
      ((e) => {
        let n = document.body
        return (
          e.appendTo &&
            (V(e.appendTo) && (n = document.querySelector(e.appendTo)),
            F(e.appendTo) && (n = e.appendTo),
            F(n) || (n = document.body)),
          n
        )
      })(e).appendChild(n.firstElementChild),
      t.component
    )
  },
  ce = (e, n) => {
    const o = document.createElement('div')
    ;((e.onVanish = () => {
      ;(O(null, o), re.delete(a))
    }),
      (e.onAction = (n) => {
        const o = re.get(a)
        let s
        ;((s = e.showInput ? { value: a.inputValue, action: n } : n),
          e.callback
            ? e.callback(s, t.proxy)
            : 'cancel' === n || 'close' === n
              ? e.distinguishCancelAndClose && 'cancel' !== n
                ? o.reject('close')
                : o.reject('cancel')
              : o.resolve(s))
      }))
    const t = ie(e, o, n),
      a = t.proxy
    for (const s in e) H(e, s) && !H(a.$props, s) && (a[s] = e[s])
    return ((a.visible = !0), a)
  }
function ue(e, n = null) {
  if (!P) return Promise.reject()
  let o
  return (
    V(e) || $(e) ? (e = { message: e }) : (o = e.callback),
    new Promise((t, a) => {
      const s = ce(e, null != n ? n : ue._context)
      re.set(s, { options: e, callback: o, resolve: t, reject: a })
    })
  )
}
const de = {
  alert: { closeOnPressEscape: !1, closeOnClickModal: !1 },
  confirm: { showCancelButton: !0 },
  prompt: { showCancelButton: !0, showInput: !0 }
}
;(['alert', 'confirm', 'prompt'].forEach((e) => {
  ue[e] = (function (e) {
    return (n, o, t, a) => {
      let s = ''
      return (
        D(o) ? ((t = o), (s = '')) : (s = K(o) ? '' : o),
        ue(Object.assign({ title: s, message: n, type: '', ...de[e] }, t, { boxType: e }), a)
      )
    }
  })(e)
}),
  (ue.close = () => {
    ;(re.forEach((e, n) => {
      n.doClose()
    }),
      re.clear())
  }),
  (ue._context = null))
const pe = ue
pe.install = (e) => {
  ;((pe._context = e._context),
    (e.config.globalProperties.$msgbox = pe),
    (e.config.globalProperties.$messageBox = pe),
    (e.config.globalProperties.$alert = pe.alert),
    (e.config.globalProperties.$confirm = pe.confirm),
    (e.config.globalProperties.$prompt = pe.prompt))
}
const fe = pe
export { fe as E }
