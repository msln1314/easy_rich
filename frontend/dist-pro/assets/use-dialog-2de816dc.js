import {
  b as e,
  a as o,
  d as l,
  b7 as a,
  aq as n,
  bY as t,
  bL as s,
  r as u,
  ds as c,
  f as r,
  h as d,
  w as p,
  as as i,
  a2 as f,
  dt as y,
  du as v,
  aJ as m
} from './index-820a519e.js'
import { U as C } from './event-5568c9d8.js'
import { u as b } from './el-overlay-34b9d092.js'
const B = e({
    center: Boolean,
    alignCenter: Boolean,
    closeIcon: { type: o },
    customClass: { type: String, default: '' },
    draggable: Boolean,
    fullscreen: Boolean,
    showClose: { type: Boolean, default: !0 },
    title: { type: String, default: '' }
  }),
  g = { close: () => !0 },
  D = e({
    ...B,
    appendToBody: Boolean,
    beforeClose: { type: l(Function) },
    destroyOnClose: Boolean,
    closeOnClickModal: { type: Boolean, default: !0 },
    closeOnPressEscape: { type: Boolean, default: !0 },
    lockScroll: { type: Boolean, default: !0 },
    modal: { type: Boolean, default: !0 },
    openDelay: { type: Number, default: 0 },
    closeDelay: { type: Number, default: 0 },
    top: { type: String },
    modelValue: Boolean,
    modalClass: String,
    width: { type: [String, Number] },
    zIndex: { type: Number },
    trapFocus: { type: Boolean, default: !1 }
  }),
  x = {
    open: () => !0,
    opened: () => !0,
    close: () => !0,
    closed: () => !0,
    [C]: (e) => a(e),
    openAutoFocus: () => !0,
    closeAutoFocus: () => !0
  },
  F = (e, o) => {
    const l = n().emit,
      { nextZIndex: a } = t()
    let B = ''
    const g = s(),
      D = s(),
      x = u(!1),
      F = u(!1),
      I = u(!1),
      S = u(e.zIndex || a())
    let h, O
    const w = c('namespace', y),
      A = r(() => {
        const o = {},
          l = `--${w.value}-dialog`
        return (
          e.fullscreen ||
            (e.top && (o[`${l}-margin-top`] = e.top), e.width && (o[`${l}-width`] = d(e.width))),
          o
        )
      }),
      k = r(() => (e.alignCenter ? { display: 'flex' } : {}))
    function z() {
      ;(null == O || O(),
        null == h || h(),
        e.openDelay && e.openDelay > 0 ? ({ stop: h } = v(() => E(), e.openDelay)) : E())
    }
    function N() {
      ;(null == h || h(),
        null == O || O(),
        e.closeDelay && e.closeDelay > 0 ? ({ stop: O } = v(() => L(), e.closeDelay)) : L())
    }
    function j() {
      e.beforeClose
        ? e.beforeClose(function (e) {
            e || ((F.value = !0), (x.value = !1))
          })
        : N()
    }
    function E() {
      m && (x.value = !0)
    }
    function L() {
      x.value = !1
    }
    return (
      e.lockScroll && b(x),
      p(
        () => e.modelValue,
        (n) => {
          n
            ? ((F.value = !1),
              z(),
              (I.value = !0),
              (S.value = e.zIndex ? S.value++ : a()),
              i(() => {
                ;(l('open'), o.value && (o.value.scrollTop = 0))
              }))
            : x.value && N()
        }
      ),
      p(
        () => e.fullscreen,
        (e) => {
          o.value &&
            (e
              ? ((B = o.value.style.transform), (o.value.style.transform = ''))
              : (o.value.style.transform = B))
        }
      ),
      f(() => {
        e.modelValue && ((x.value = !0), (I.value = !0), z())
      }),
      {
        afterEnter: function () {
          l('opened')
        },
        afterLeave: function () {
          ;(l('closed'), l(C, !1), e.destroyOnClose && (I.value = !1))
        },
        beforeLeave: function () {
          l('close')
        },
        handleClose: j,
        onModalClick: function () {
          e.closeOnClickModal && j()
        },
        close: N,
        doClose: L,
        onOpenAutoFocus: function () {
          l('openAutoFocus')
        },
        onCloseAutoFocus: function () {
          l('closeAutoFocus')
        },
        onCloseRequested: function () {
          e.closeOnPressEscape && j()
        },
        onFocusoutPrevented: function (e) {
          var o
          'pointer' === (null == (o = e.detail) ? void 0 : o.focusReason) && e.preventDefault()
        },
        titleId: g,
        bodyId: D,
        closed: F,
        style: A,
        overlayDialogStyle: k,
        rendered: I,
        visible: x,
        zIndex: S
      }
    )
  }
export { g as a, D as b, x as c, B as d, F as u }
