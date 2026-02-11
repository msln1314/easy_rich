import {
  ai as e,
  ar as t,
  u as s,
  aJ as n,
  bq as o,
  w as i,
  cg as c,
  cq as d,
  dg as r,
  cp as u,
  aS as l,
  b as a,
  d as h,
  e as p,
  x as f,
  q as _,
  a$ as v
} from './index-820a519e.js'
import { a as y } from './scroll-ac7d0423.js'
import { P as m } from './vnode-06a99f10.js'
/**
 * @vue/shared v3.4.13
 * (c) 2018-present Yuxi (Evan) You and Vue contributors
 * @license MIT
 **/ const g = () => {},
  b = (e) => 'symbol' == typeof e
/**
 * @vue/reactivity v3.4.13
 * (c) 2018-present Yuxi (Evan) You and Vue contributors
 * @license MIT
 **/
let L
class k {
  constructor(e, t, s, n) {
    ;((this.fn = e),
      (this.trigger = t),
      (this.scheduler = s),
      (this.active = !0),
      (this.deps = []),
      (this._dirtyLevel = 2),
      (this._trackId = 0),
      (this._runnings = 0),
      (this._shouldSchedule = !1),
      (this._depsLength = 0),
      (function (e, t) {
        t && t.active && t.effects.push(e)
      })(this, n))
  }
  get dirty() {
    if (1 === this._dirtyLevel) {
      ;(C.push(M), (M = !1))
      for (let e = 0; e < this._depsLength; e++) {
        const t = this.deps[e]
        if (t.computed && (t.computed.value, this._dirtyLevel >= 2)) break
      }
      ;(this._dirtyLevel < 2 && (this._dirtyLevel = 0),
        (function () {
          const e = C.pop()
          M = void 0 === e || e
        })())
    }
    return this._dirtyLevel >= 2
  }
  set dirty(e) {
    this._dirtyLevel = e ? 2 : 0
  }
  run() {
    if (((this._dirtyLevel = 0), !this.active)) return this.fn()
    let e = M,
      t = L
    try {
      return ((M = !0), (L = this), this._runnings++, w(this), this.fn())
    } finally {
      ;(S(this), this._runnings--, (L = t), (M = e))
    }
  }
  stop() {
    var e
    this.active && (w(this), S(this), null == (e = this.onStop) || e.call(this), (this.active = !1))
  }
}
function w(e) {
  ;(e._trackId++, (e._depsLength = 0))
}
function S(e) {
  if (e.deps && e.deps.length > e._depsLength) {
    for (let t = e._depsLength; t < e.deps.length; t++) x(e.deps[t], e)
    e.deps.length = e._depsLength
  }
}
function x(e, t) {
  const s = e.get(t)
  void 0 !== s && t._trackId !== s && (e.delete(t), 0 === e.size && e.cleanup())
}
let M = !0,
  I = 0
const C = []
const E = []
function j(e, t, s) {
  I++
  for (const n of e.keys())
    if (e.get(n) === n._trackId) {
      if (n._dirtyLevel < t) {
        const e = n._dirtyLevel
        ;((n._dirtyLevel = t), 0 === e && ((n._shouldSchedule = !0), n.trigger()))
      }
      n.scheduler &&
        n._shouldSchedule &&
        (!n._runnings || n.allowRecurse) &&
        ((n._shouldSchedule = !1), E.push(n.scheduler))
    }
  !(function () {
    for (I--; !I && E.length; ) E.shift()()
  })()
}
function z(e) {
  const t = e && e.__v_raw
  return t ? z(t) : e
}
new Set(
  Object.getOwnPropertyNames(Symbol)
    .filter((e) => 'arguments' !== e && 'caller' !== e)
    .map((e) => Symbol[e])
    .filter(b)
)
class O {
  constructor(e, t, s, n) {
    ;((this._setter = t),
      (this.dep = void 0),
      (this.__v_isRef = !0),
      (this.__v_isReadonly = !1),
      (this.effect = new k(
        () => e(this._value),
        () => R(this, 1)
      )),
      (this.effect.computed = this),
      (this.effect.active = this._cacheable = !n),
      (this.__v_isReadonly = s))
  }
  get value() {
    const e = z(this)
    var t, s, n
    return (
      (e._cacheable && !e.effect.dirty) ||
        ((t = e._value), (s = e._value = e.effect.run()), Object.is(t, s) || R(e, 2)),
      (n = e),
      M &&
        L &&
        ((n = z(n)),
        (function (e, t, s) {
          if (t.get(e) !== e._trackId) {
            t.set(e, e._trackId)
            const s = e.deps[e._depsLength]
            s !== t ? (s && x(s, e), (e.deps[e._depsLength++] = t)) : e._depsLength++
          }
        })(
          L,
          n.dep ||
            (n.dep = ((e, t) => {
              const s = new Map()
              return ((s.cleanup = e), (s.computed = t), s)
            })(() => (n.dep = void 0), n instanceof O ? n : void 0))
        )),
      e._value
    )
  }
  set value(e) {
    this._setter(e)
  }
  get _dirty() {
    return this.effect.dirty
  }
  set _dirty(e) {
    this.effect.dirty = e
  }
}
function R(e, t = 2, s) {
  const n = (e = z(e)).dep
  n && j(n, t)
}
const P = (l, a = {}) => {
    e(l) || t('[useLockscreen]', 'You need to pass a ref param to this function')
    const h = a.ns || s('popup'),
      p = (function (e, t, s = !1) {
        let n, o
        const i = 'function' == typeof e
        return (i ? ((n = e), (o = g)) : ((n = e.get), (o = e.set)), new O(n, o, i || !o, s))
      })(() => h.bm('parent', 'hidden'))
    if (!n || o(document.body, p.value)) return
    let f = 0,
      _ = !1,
      v = '0'
    const m = () => {
      setTimeout(() => {
        ;(u(null == document ? void 0 : document.body, p.value),
          _ && document && (document.body.style.width = v))
      }, 200)
    }
    ;(i(l, (e) => {
      if (!e) return void m()
      ;((_ = !o(document.body, p.value)),
        _ && (v = document.body.style.width),
        (f = y(h.namespace.value)))
      const t = document.documentElement.clientHeight < document.body.scrollHeight,
        s = c(document.body, 'overflowY')
      ;(f > 0 && (t || 'scroll' === s) && _ && (document.body.style.width = `calc(100% - ${f}px)`),
        d(document.body, p.value))
    }),
      r(() => m()))
  },
  T = (e) => {
    if (!e) return { onClick: l, onMousedown: l, onMouseup: l }
    let t = !1,
      s = !1
    return {
      onClick: (n) => {
        ;(t && s && e(n), (t = s = !1))
      },
      onMousedown: (e) => {
        t = e.target === e.currentTarget
      },
      onMouseup: (e) => {
        s = e.target === e.currentTarget
      }
    }
  },
  q = a({
    mask: { type: Boolean, default: !0 },
    customMaskEvent: { type: Boolean, default: !1 },
    overlayClass: { type: h([String, Array, Object]) },
    zIndex: { type: h([String, Number]) }
  })
const Y = p({
  name: 'ElOverlay',
  props: q,
  emits: { click: (e) => e instanceof MouseEvent },
  setup(e, { slots: t, emit: n }) {
    const o = s('overlay'),
      {
        onClick: i,
        onMousedown: c,
        onMouseup: d
      } = T(
        e.customMaskEvent
          ? void 0
          : (e) => {
              n('click', e)
            }
      )
    return () =>
      e.mask
        ? f(
            'div',
            {
              class: [o.b(), e.overlayClass],
              style: { zIndex: e.zIndex },
              onClick: i,
              onMousedown: c,
              onMouseup: d
            },
            [_(t, 'default')],
            m.STYLE | m.CLASS | m.PROPS,
            ['onClick', 'onMouseup', 'onMousedown']
          )
        : v(
            'div',
            {
              class: e.overlayClass,
              style: {
                zIndex: e.zIndex,
                position: 'fixed',
                top: '0px',
                right: '0px',
                bottom: '0px',
                left: '0px'
              }
            },
            [_(t, 'default')]
          )
  }
})
export { Y as E, T as a, P as u }
