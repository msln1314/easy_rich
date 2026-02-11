import {
  cC as e,
  cT as t,
  c7 as l,
  cF as n,
  aQ as o,
  cK as r,
  cU as a,
  cV as s,
  c5 as i,
  bu as u,
  c9 as d,
  cW as c,
  bJ as h,
  cX as p,
  cY as f,
  cZ as v,
  cJ as m,
  cL as g,
  aR as y,
  c_ as b,
  c$ as w,
  d0 as x,
  d1 as C,
  c8 as S,
  d2 as E,
  d3 as R,
  d4 as N,
  aK as k,
  aa as O,
  bg as L,
  ar as H,
  b7 as W,
  aZ as A,
  ap as M,
  aq as F,
  r as T,
  k as $,
  f as B,
  w as I,
  bw as K,
  u as j,
  as as z,
  ai as D,
  aJ as P,
  _ as V,
  e as _,
  G as Y,
  E as q,
  bd as X,
  bk as G,
  a_ as U,
  b1 as Q,
  Z,
  o as J,
  l as ee,
  m as te,
  j as le,
  y as ne,
  s as oe,
  x as re,
  a1 as ae,
  a5 as se,
  M as ie,
  z as ue,
  a0 as de,
  bQ as ce,
  a2 as he,
  aw as pe,
  aG as fe,
  ao as ve,
  cq as me,
  bX as ge,
  bq as ye,
  cp as be,
  a$ as we,
  bY as xe,
  bh as Ce,
  by as Se,
  at as Ee,
  b9 as Re,
  b6 as Ne,
  i as ke,
  am as Oe,
  q as Le,
  n as He,
  F as We,
  aH as Ae,
  bN as Me,
  ay as Fe,
  aW as Te,
  bV as $e,
  aD as Be,
  aj as Ie,
  g as Ke,
  t as je,
  a8 as ze
} from './index-820a519e.js'
import { d as De, y as Pe, E as Ve } from './el-popper-797844d6.js'
import { b as _e } from './isEqual-cb9e370d.js'
import { h as Ye, E as qe } from './el-checkbox-77b6829c.js'
import { d as Xe } from './debounce-5bc596c6.js'
import { C as Ge } from './index-eb31d854.js'
var Ue = 1,
  Qe = 2
function Ze(t) {
  return t == t && !e(t)
}
function Je(e, t) {
  return function (l) {
    return null != l && l[e] === t && (void 0 !== t || e in Object(l))
  }
}
function et(e) {
  var t = (function (e) {
    for (var t = a(e), l = t.length; l--; ) {
      var n = t[l],
        o = e[n]
      t[l] = [n, o, Ze(o)]
    }
    return t
  })(e)
  return 1 == t.length && t[0][2]
    ? Je(t[0][0], t[0][1])
    : function (l) {
        return (
          l === e ||
          (function (e, t, l, n) {
            var o = l.length,
              a = o,
              s = !n
            if (null == e) return !a
            for (e = Object(e); o--; ) {
              var i = l[o]
              if (s && i[2] ? i[1] !== e[i[0]] : !(i[0] in e)) return !1
            }
            for (; ++o < a; ) {
              var u = (i = l[o])[0],
                d = e[u],
                c = i[1]
              if (s && i[2]) {
                if (void 0 === d && !(u in e)) return !1
              } else {
                var h = new r()
                if (n) var p = n(d, c, u, e, t, h)
                if (!(void 0 === p ? _e(c, d, Ue | Qe, n, h) : p)) return !1
              }
            }
            return !0
          })(l, e, t)
        )
      }
}
var tt,
  lt = 1,
  nt = 2
function ot(e) {
  return s(e)
    ? ((t = i(e)),
      function (e) {
        return null == e ? void 0 : e[t]
      })
    : (function (e) {
        return function (t) {
          return d(t, e)
        }
      })(e)
  var t
}
function rt(e) {
  return 'function' == typeof e
    ? e
    : null == e
      ? c
      : 'object' == typeof e
        ? h(e)
          ? ((t = e[0]),
            (l = e[1]),
            s(t) && Ze(l)
              ? Je(i(t), l)
              : function (e) {
                  var n = u(e, t)
                  return void 0 === n && n === l ? Ye(e, t) : _e(l, n, lt | nt)
                })
          : et(e)
        : ot(e)
  var t, l
}
const at = function (e, t, l) {
  for (var n = -1, o = Object(e), r = l(e), a = r.length; a--; ) {
    var s = r[tt ? a : ++n]
    if (!1 === t(o[s], s, o)) break
  }
  return e
}
var st = (function (e, l) {
  return function (n, o) {
    if (null == n) return n
    if (!t(n)) return e(n, o)
    for (
      var r = n.length, a = l ? r : -1, s = Object(n);
      (l ? a-- : ++a < r) && !1 !== o(s[a], a, s);
    );
    return n
  }
})(function (e, t) {
  return e && at(e, t, a)
})
const it = st
function ut(e, t, l) {
  ;((void 0 !== l && !n(e[t], l)) || (void 0 === l && !(t in e))) && p(e, t, l)
}
function dt(e, t) {
  if (('constructor' !== t || 'function' != typeof e[t]) && '__proto__' != t) return e[t]
}
function ct(t, l, n, o, r, a, s) {
  var i = dt(t, n),
    u = dt(l, n),
    d = s.get(u)
  if (d) ut(t, n, d)
  else {
    var c,
      p = a ? a(i, u, n + '', t, l, s) : void 0,
      N = void 0 === p
    if (N) {
      var k = h(u),
        O = !k && m(u),
        L = !k && !O && g(u)
      ;((p = u),
        k || O || L
          ? h(i)
            ? (p = i)
            : y(i)
              ? (p = b(i))
              : O
                ? ((N = !1), (p = w(u, !0)))
                : L
                  ? ((N = !1), (p = x(u, !0)))
                  : (p = [])
          : C(u) || S(u)
            ? ((p = i), S(i) ? (p = f((c = i), v(c))) : (e(i) && !E(i)) || (p = R(u)))
            : (N = !1))
    }
    ;(N && (s.set(u, p), r(p, u, o, a, s), s.delete(u)), ut(t, n, p))
  }
}
function ht(t, l, n, o, a) {
  t !== l &&
    at(
      l,
      function (s, i) {
        if ((a || (a = new r()), e(s))) ct(t, l, i, n, ht, o, a)
        else {
          var u = o ? o(dt(t, i), s, i + '', t, l, a) : void 0
          ;(void 0 === u && (u = s), ut(t, i, u))
        }
      },
      v
    )
}
function pt(e, l) {
  var n = -1,
    o = t(e) ? Array(e.length) : []
  return (
    it(e, function (e, t, r) {
      o[++n] = l(e, t, r)
    }),
    o
  )
}
function ft(e, t) {
  return k(
    (function (e, t) {
      return (h(e) ? N : pt)(e, rt(t))
    })(e, t),
    1
  )
}
var vt
const mt =
  ((vt = function (e, t, l) {
    ht(e, t, l)
  }),
  o(function (o, r) {
    var a = -1,
      s = r.length,
      i = s > 1 ? r[s - 1] : void 0,
      u = s > 2 ? r[2] : void 0
    for (
      i = vt.length > 3 && 'function' == typeof i ? (s--, i) : void 0,
        u &&
          (function (o, r, a) {
            if (!e(a)) return !1
            var s = typeof r
            return (
              !!('number' == s ? t(a) && l(r, a.length) : 'string' == s && (r in a)) && n(a[r], o)
            )
          })(r[0], r[1], u) &&
          ((i = s < 3 ? void 0 : i), (s = 1)),
        o = Object(o);
      ++a < s;
    ) {
      var d = r[a]
      d && vt(o, d, a, i)
    }
    return o
  }))
var gt,
  yt,
  bt,
  wt,
  xt,
  Ct,
  St,
  Et,
  Rt,
  Nt,
  kt,
  Ot,
  Lt,
  Ht,
  Wt,
  At = !1
function Mt() {
  if (!At) {
    At = !0
    var e = navigator.userAgent,
      t =
        /(?:MSIE.(\d+\.\d+))|(?:(?:Firefox|GranParadiso|Iceweasel).(\d+\.\d+))|(?:Opera(?:.+Version.|.)(\d+\.\d+))|(?:AppleWebKit.(\d+(?:\.\d+)?))|(?:Trident\/\d+\.\d+.*rv:(\d+\.\d+))/.exec(
          e
        ),
      l = /(Mac OS X)|(Windows)|(Linux)/.exec(e)
    if (
      ((Ot = /\b(iPhone|iP[ao]d)/.exec(e)),
      (Lt = /\b(iP[ao]d)/.exec(e)),
      (Nt = /Android/i.exec(e)),
      (Ht = /FBAN\/\w+;/i.exec(e)),
      (Wt = /Mobile/i.exec(e)),
      (kt = !!/Win64/.exec(e)),
      t)
    ) {
      ;(gt = t[1] ? parseFloat(t[1]) : t[5] ? parseFloat(t[5]) : NaN) &&
        document &&
        document.documentMode &&
        (gt = document.documentMode)
      var n = /(?:Trident\/(\d+.\d+))/.exec(e)
      ;((Ct = n ? parseFloat(n[1]) + 4 : gt),
        (yt = t[2] ? parseFloat(t[2]) : NaN),
        (bt = t[3] ? parseFloat(t[3]) : NaN),
        (wt = t[4] ? parseFloat(t[4]) : NaN)
          ? ((t = /(?:Chrome\/(\d+\.\d+))/.exec(e)), (xt = t && t[1] ? parseFloat(t[1]) : NaN))
          : (xt = NaN))
    } else gt = yt = bt = xt = wt = NaN
    if (l) {
      if (l[1]) {
        var o = /(?:Mac OS X (\d+(?:[._]\d+)?))/.exec(e)
        St = !o || parseFloat(o[1].replace('_', '.'))
      } else St = !1
      ;((Et = !!l[2]), (Rt = !!l[3]))
    } else St = Et = Rt = !1
  }
}
var Ft,
  Tt = {
    ie: function () {
      return Mt() || gt
    },
    ieCompatibilityMode: function () {
      return Mt() || Ct > gt
    },
    ie64: function () {
      return Tt.ie() && kt
    },
    firefox: function () {
      return Mt() || yt
    },
    opera: function () {
      return Mt() || bt
    },
    webkit: function () {
      return Mt() || wt
    },
    safari: function () {
      return Tt.webkit()
    },
    chrome: function () {
      return Mt() || xt
    },
    windows: function () {
      return Mt() || Et
    },
    osx: function () {
      return Mt() || St
    },
    linux: function () {
      return Mt() || Rt
    },
    iphone: function () {
      return Mt() || Ot
    },
    mobile: function () {
      return Mt() || Ot || Lt || Nt || Wt
    },
    nativeApp: function () {
      return Mt() || Ht
    },
    android: function () {
      return Mt() || Nt
    },
    ipad: function () {
      return Mt() || Lt
    }
  },
  $t = Tt,
  Bt = !!(typeof window < 'u' && window.document && window.document.createElement),
  It = {
    canUseDOM: Bt,
    canUseWorkers: typeof Worker < 'u',
    canUseEventListeners: Bt && !(!window.addEventListener && !window.attachEvent),
    canUseViewport: Bt && !!window.screen,
    isInWorker: !Bt
  }
It.canUseDOM &&
  (Ft =
    document.implementation &&
    document.implementation.hasFeature &&
    !0 !== document.implementation.hasFeature('', ''))
var Kt = function (e, t) {
  if (!It.canUseDOM || (t && !('addEventListener' in document))) return !1
  var l = 'on' + e,
    n = l in document
  if (!n) {
    var o = document.createElement('div')
    ;(o.setAttribute(l, 'return;'), (n = 'function' == typeof o[l]))
  }
  return (
    !n && Ft && 'wheel' === e && (n = document.implementation.hasFeature('Events.wheel', '3.0')),
    n
  )
}
function jt(e) {
  var t = 0,
    l = 0,
    n = 0,
    o = 0
  return (
    'detail' in e && (l = e.detail),
    'wheelDelta' in e && (l = -e.wheelDelta / 120),
    'wheelDeltaY' in e && (l = -e.wheelDeltaY / 120),
    'wheelDeltaX' in e && (t = -e.wheelDeltaX / 120),
    'axis' in e && e.axis === e.HORIZONTAL_AXIS && ((t = l), (l = 0)),
    (n = 10 * t),
    (o = 10 * l),
    'deltaY' in e && (o = e.deltaY),
    'deltaX' in e && (n = e.deltaX),
    (n || o) &&
      e.deltaMode &&
      (1 == e.deltaMode ? ((n *= 40), (o *= 40)) : ((n *= 800), (o *= 800))),
    n && !t && (t = n < 1 ? -1 : 1),
    o && !l && (l = o < 1 ? -1 : 1),
    { spinX: t, spinY: l, pixelX: n, pixelY: o }
  )
}
jt.getEventType = function () {
  return $t.firefox() ? 'DOMMouseScroll' : Kt('wheel') ? 'wheel' : 'mousewheel'
}
var zt = jt
/**
 * Checks if an event is supported in the current execution environment.
 *
 * NOTE: This will not work correctly for non-generic events such as `change`,
 * `reset`, `load`, `error`, and `select`.
 *
 * Borrows from Modernizr.
 *
 * @param {string} eventNameSuffix Event name, e.g. "click".
 * @param {?boolean} capture Check if the capture phase is supported.
 * @return {boolean} True if the event is supported.
 * @internal
 * @license Modernizr 3.0.0pre (Custom Build) | MIT
 */ const Dt = {
  beforeMount(e, t) {
    !(function (e, t) {
      if (e && e.addEventListener) {
        const l = function (e) {
          const l = zt(e)
          t && Reflect.apply(t, this, [e, l])
        }
        e.addEventListener('wheel', l, { passive: !0 })
      }
    })(e, t.value)
  }
}
/*!
 * escape-html
 * Copyright(c) 2012-2013 TJ Holowaychuk
 * Copyright(c) 2015 Andreas Lubbe
 * Copyright(c) 2015 Tiancheng "Timothy" Gu
 * MIT Licensed
 */
var Pt = /["'&<>]/
const Vt = O(function (e) {
    var t,
      l = '' + e,
      n = Pt.exec(l)
    if (!n) return l
    var o = '',
      r = 0,
      a = 0
    for (r = n.index; r < l.length; r++) {
      switch (l.charCodeAt(r)) {
        case 34:
          t = '&quot;'
          break
        case 38:
          t = '&amp;'
          break
        case 39:
          t = '&#39;'
          break
        case 60:
          t = '&lt;'
          break
        case 62:
          t = '&gt;'
          break
        default:
          continue
      }
      ;(a !== r && (o += l.substring(a, r)), (a = r + 1), (o += t))
    }
    return a !== r ? o + l.substring(a, r) : o
  }),
  _t = function (e) {
    var t
    return null == (t = e.target) ? void 0 : t.closest('td')
  },
  Yt = function (e, t, l, n, o) {
    if (!t && !n && (!o || (Array.isArray(o) && !o.length))) return e
    l = 'string' == typeof l ? ('descending' === l ? -1 : 1) : l && l < 0 ? -1 : 1
    const r = n
      ? null
      : function (l, n) {
          return o
            ? (Array.isArray(o) || (o = [o]),
              o.map((t) => ('string' == typeof t ? u(l, t) : t(l, n, e))))
            : ('$key' !== t && M(l) && '$value' in l && (l = l.$value), [M(l) ? u(l, t) : l])
        }
    return e
      .map((e, t) => ({ value: e, index: t, key: r ? r(e, t) : null }))
      .sort((e, t) => {
        let o = (function (e, t) {
          if (n) return n(e.value, t.value)
          for (let l = 0, n = e.key.length; l < n; l++) {
            if (e.key[l] < t.key[l]) return -1
            if (e.key[l] > t.key[l]) return 1
          }
          return 0
        })(e, t)
        return (o || (o = e.index - t.index), o * +l)
      })
      .map((e) => e.value)
  },
  qt = function (e, t) {
    let l = null
    return (
      e.columns.forEach((e) => {
        e.id === t && (l = e)
      }),
      l
    )
  },
  Xt = function (e, t) {
    let l = null
    for (let n = 0; n < e.columns.length; n++) {
      const o = e.columns[n]
      if (o.columnKey === t) {
        l = o
        break
      }
    }
    return (l || H('ElTable', `No column matching with column-key: ${t}`), l)
  },
  Gt = function (e, t, l) {
    const n = (t.className || '').match(new RegExp(`${l}-table_[^\\s]+`, 'gm'))
    return n ? qt(e, n[0]) : null
  },
  Ut = (e, t) => {
    if (!e) throw new Error('Row is required when get row identity')
    if ('string' == typeof t) {
      if (!t.includes('.')) return `${e[t]}`
      const l = t.split('.')
      let n = e
      for (const e of l) n = n[e]
      return `${n}`
    }
    if ('function' == typeof t) return t.call(null, e)
  },
  Qt = function (e, t) {
    const l = {}
    return (
      (e || []).forEach((e, n) => {
        l[Ut(e, t)] = { row: e, index: n }
      }),
      l
    )
  }
function Zt(e) {
  return (
    '' === e || (void 0 !== e && ((e = Number.parseInt(e, 10)), Number.isNaN(e) && (e = ''))),
    e
  )
}
function Jt(e) {
  return ('' === e || (void 0 !== e && ((e = Zt(e)), Number.isNaN(e) && (e = 80))), e)
}
function el(e, t, l) {
  let n = !1
  const o = e.indexOf(t),
    r = -1 !== o,
    a = (a) => {
      ;('add' === a ? e.push(t) : e.splice(o, 1),
        (n = !0),
        A(t.children) &&
          t.children.forEach((t) => {
            el(e, t, null != l ? l : !r)
          }))
    }
  return (W(l) ? (l && !r ? a('add') : !l && r && a('remove')) : a(r ? 'remove' : 'add'), n)
}
function tl(e, t, l = 'children', n = 'hasChildren') {
  const o = (e) => !(Array.isArray(e) && e.length)
  function r(e, a, s) {
    ;(t(e, a, s),
      a.forEach((e) => {
        if (e[n]) return void t(e, null, s + 1)
        const a = e[l]
        o(a) || r(e, a, s + 1)
      }))
  }
  e.forEach((e) => {
    if (e[n]) return void t(e, null, 0)
    const a = e[l]
    o(a) || r(e, a, 0)
  })
}
let ll
function nl(e) {
  return e.children ? ft(e.children, nl) : [e]
}
function ol(e, t) {
  return e + t.colSpan
}
const rl = (e, t, l, n) => {
    let o = 0,
      r = e
    const a = l.states.columns.value
    if (n) {
      const t = nl(n[e])
      ;((o = a.slice(0, a.indexOf(t[0])).reduce(ol, 0)), (r = o + t.reduce(ol, 0) - 1))
    } else o = e
    let s
    switch (t) {
      case 'left':
        r < l.states.fixedLeafColumnsLength.value && (s = 'left')
        break
      case 'right':
        o >= a.length - l.states.rightFixedLeafColumnsLength.value && (s = 'right')
        break
      default:
        r < l.states.fixedLeafColumnsLength.value
          ? (s = 'left')
          : o >= a.length - l.states.rightFixedLeafColumnsLength.value && (s = 'right')
    }
    return s ? { direction: s, start: o, after: r } : {}
  },
  al = (e, t, l, n, o, r = 0) => {
    const a = [],
      { direction: s, start: i, after: u } = rl(t, l, n, o)
    if (s) {
      const t = 'left' === s
      ;(a.push(`${e}-fixed-column--${s}`),
        t && u + r === n.states.fixedLeafColumnsLength.value - 1
          ? a.push('is-last-column')
          : t ||
            i - r != n.states.columns.value.length - n.states.rightFixedLeafColumnsLength.value ||
            a.push('is-first-column'))
    }
    return a
  }
function sl(e, t) {
  return e + (null === t.realWidth || Number.isNaN(t.realWidth) ? Number(t.width) : t.realWidth)
}
const il = (e, t, l, n) => {
    const { direction: o, start: r = 0, after: a = 0 } = rl(e, t, l, n)
    if (!o) return
    const s = {},
      i = 'left' === o,
      u = l.states.columns.value
    return (
      i
        ? (s.left = u.slice(0, r).reduce(sl, 0))
        : (s.right = u
            .slice(a + 1)
            .reverse()
            .reduce(sl, 0)),
      s
    )
  },
  ul = (e, t) => {
    e && (Number.isNaN(e[t]) || (e[t] = `${e[t]}px`))
  }
const dl = (e, t) => {
    const l = t.sortingColumn
    return l && 'string' != typeof l.sortable
      ? Yt(e, t.sortProp, t.sortOrder, l.sortMethod, l.sortBy)
      : e
  },
  cl = (e) => {
    const t = []
    return (
      e.forEach((e) => {
        e.children && e.children.length > 0 ? t.push.apply(t, cl(e.children)) : t.push(e)
      }),
      t
    )
  }
function hl() {
  var e
  const t = F(),
    { size: l } = K(null == (e = t.proxy) ? void 0 : e.$props),
    n = T(null),
    o = T([]),
    r = T([]),
    a = T(!1),
    s = T([]),
    i = T([]),
    u = T([]),
    d = T([]),
    c = T([]),
    h = T([]),
    p = T([]),
    f = T([]),
    v = T(0),
    m = T(0),
    g = T(0),
    y = T(!1),
    b = T([]),
    w = T(!1),
    x = T(!1),
    C = T(null),
    S = T({}),
    E = T(null),
    R = T(null),
    N = T(null),
    k = T(null),
    O = T(null)
  I(o, () => t.state && A(!1), { deep: !0 })
  const H = (e) => {
      var t
      null == (t = e.children) ||
        t.forEach((t) => {
          ;((t.fixed = e.fixed), H(t))
        })
    },
    W = () => {
      ;(s.value.forEach((e) => {
        H(e)
      }),
        (d.value = s.value.filter((e) => !0 === e.fixed || 'left' === e.fixed)),
        (c.value = s.value.filter((e) => 'right' === e.fixed)),
        d.value.length > 0 &&
          s.value[0] &&
          'selection' === s.value[0].type &&
          !s.value[0].fixed &&
          ((s.value[0].fixed = !0), d.value.unshift(s.value[0])))
      const e = s.value.filter((e) => !e.fixed)
      i.value = [].concat(d.value).concat(e).concat(c.value)
      const t = cl(e),
        l = cl(d.value),
        n = cl(c.value)
      ;((v.value = t.length),
        (m.value = l.length),
        (g.value = n.length),
        (u.value = [].concat(l).concat(t).concat(n)),
        (a.value = d.value.length > 0 || c.value.length > 0))
    },
    A = (e, l = !1) => {
      ;(e && W(), l ? t.state.doLayout() : t.state.debouncedUpdateLayout())
    },
    M = (e) => {
      var l
      if (!t || !t.store) return 0
      const { treeData: n } = t.store.states
      let o = 0
      const r = null == (l = n.value[e]) ? void 0 : l.children
      return (
        r &&
          ((o += r.length),
          r.forEach((e) => {
            o += M(e)
          })),
        o
      )
    },
    j = (e, t, l) => {
      ;(R.value && R.value !== e && (R.value.order = null),
        (R.value = e),
        (N.value = t),
        (k.value = l))
    },
    z = () => {
      let e = $(r)
      ;(Object.keys(S.value).forEach((t) => {
        const l = S.value[t]
        if (!l || 0 === l.length) return
        const n = qt({ columns: u.value }, t)
        n &&
          n.filterMethod &&
          (e = e.filter((e) => l.some((t) => n.filterMethod.call(null, t, e, n))))
      }),
        (E.value = e))
    },
    D = () => {
      o.value = dl(E.value, { sortingColumn: R.value, sortProp: N.value, sortOrder: k.value })
    },
    {
      setExpandRowKeys: P,
      toggleRowExpansion: V,
      updateExpandRows: _,
      states: Y,
      isRowExpanded: q
    } = (function (e) {
      const t = F(),
        l = T(!1),
        n = T([])
      return {
        updateExpandRows: () => {
          const t = e.data.value || [],
            o = e.rowKey.value
          if (l.value) n.value = t.slice()
          else if (o) {
            const e = Qt(n.value, o)
            n.value = t.reduce((t, l) => {
              const n = Ut(l, o)
              return (e[n] && t.push(l), t)
            }, [])
          } else n.value = []
        },
        toggleRowExpansion: (e, l) => {
          el(n.value, e, l) && t.emit('expand-change', e, n.value.slice())
        },
        setExpandRowKeys: (l) => {
          t.store.assertRowKey()
          const o = e.data.value || [],
            r = e.rowKey.value,
            a = Qt(o, r)
          n.value = l.reduce((e, t) => {
            const l = a[t]
            return (l && e.push(l.row), e)
          }, [])
        },
        isRowExpanded: (t) => {
          const l = e.rowKey.value
          return l ? !!Qt(n.value, l)[Ut(t, l)] : n.value.includes(t)
        },
        states: { expandRows: n, defaultExpandAll: l }
      }
    })({ data: o, rowKey: n }),
    {
      updateTreeExpandKeys: X,
      toggleTreeExpansion: G,
      updateTreeData: U,
      loadOrToggle: Q,
      states: Z
    } = (function (e) {
      const t = T([]),
        l = T({}),
        n = T(16),
        o = T(!1),
        r = T({}),
        a = T('hasChildren'),
        s = T('children'),
        i = F(),
        u = B(() => {
          if (!e.rowKey.value) return {}
          const t = e.data.value || []
          return c(t)
        }),
        d = B(() => {
          const t = e.rowKey.value,
            l = Object.keys(r.value),
            n = {}
          return l.length
            ? (l.forEach((e) => {
                if (r.value[e].length) {
                  const l = { children: [] }
                  ;(r.value[e].forEach((e) => {
                    const o = Ut(e, t)
                    ;(l.children.push(o), e[a.value] && !n[o] && (n[o] = { children: [] }))
                  }),
                    (n[e] = l))
                }
              }),
              n)
            : n
        }),
        c = (t) => {
          const l = e.rowKey.value,
            n = {}
          return (
            tl(
              t,
              (e, t, r) => {
                const a = Ut(e, l)
                Array.isArray(t)
                  ? (n[a] = { children: t.map((e) => Ut(e, l)), level: r })
                  : o.value && (n[a] = { children: [], lazy: !0, level: r })
              },
              s.value,
              a.value
            ),
            n
          )
        },
        h = (
          e = !1,
          n = ((e) => (null == (e = i.store) ? void 0 : e.states.defaultExpandAll.value))()
        ) => {
          var r
          const a = u.value,
            s = d.value,
            c = Object.keys(a),
            h = {}
          if (c.length) {
            const r = $(l),
              i = [],
              u = (l, o) => {
                if (e)
                  return t.value
                    ? n || t.value.includes(o)
                    : !(!n && !(null == l ? void 0 : l.expanded))
                {
                  const e = n || (t.value && t.value.includes(o))
                  return !(!(null == l ? void 0 : l.expanded) && !e)
                }
              }
            c.forEach((e) => {
              const t = r[e],
                l = { ...a[e] }
              if (((l.expanded = u(t, e)), l.lazy)) {
                const { loaded: n = !1, loading: o = !1 } = t || {}
                ;((l.loaded = !!n), (l.loading = !!o), i.push(e))
              }
              h[e] = l
            })
            const d = Object.keys(s)
            o.value &&
              d.length &&
              i.length &&
              d.forEach((e) => {
                const t = r[e],
                  l = s[e].children
                if (i.includes(e)) {
                  if (0 !== h[e].children.length)
                    throw new Error('[ElTable]children must be an empty array.')
                  h[e].children = l
                } else {
                  const { loaded: n = !1, loading: o = !1 } = t || {}
                  h[e] = {
                    lazy: !0,
                    loaded: !!n,
                    loading: !!o,
                    expanded: u(t, e),
                    children: l,
                    level: ''
                  }
                }
              })
          }
          ;((l.value = h), null == (r = i.store) || r.updateTableScrollY())
        }
      ;(I(
        () => t.value,
        () => {
          h(!0)
        }
      ),
        I(
          () => u.value,
          () => {
            h()
          }
        ),
        I(
          () => d.value,
          () => {
            h()
          }
        ))
      const p = (t, n) => {
          i.store.assertRowKey()
          const o = e.rowKey.value,
            r = Ut(t, o),
            a = r && l.value[r]
          if (r && a && 'expanded' in a) {
            const e = a.expanded
            ;((n = void 0 === n ? !a.expanded : n),
              (l.value[r].expanded = n),
              e !== n && i.emit('expand-change', t, n),
              i.store.updateTableScrollY())
          }
        },
        f = (e, t, n) => {
          const { load: o } = i.props
          o &&
            !l.value[t].loaded &&
            ((l.value[t].loading = !0),
            o(e, n, (n) => {
              if (!Array.isArray(n)) throw new TypeError('[ElTable] data must be an array')
              ;((l.value[t].loading = !1),
                (l.value[t].loaded = !0),
                (l.value[t].expanded = !0),
                n.length && (r.value[t] = n),
                i.emit('expand-change', e, !0))
            }))
        }
      return {
        loadData: f,
        loadOrToggle: (t) => {
          i.store.assertRowKey()
          const n = e.rowKey.value,
            r = Ut(t, n),
            a = l.value[r]
          o.value && a && 'loaded' in a && !a.loaded ? f(t, r, a) : p(t, void 0)
        },
        toggleTreeExpansion: p,
        updateTreeExpandKeys: (e) => {
          ;((t.value = e), h())
        },
        updateTreeData: h,
        normalize: c,
        states: {
          expandRowKeys: t,
          treeData: l,
          indent: n,
          lazy: o,
          lazyTreeNodeMap: r,
          lazyColumnIdentifier: a,
          childrenColumnName: s
        }
      }
    })({ data: o, rowKey: n }),
    {
      updateCurrentRowData: J,
      updateCurrentRow: ee,
      setCurrentRowKey: te,
      states: le
    } = (function (e) {
      const t = F(),
        l = T(null),
        n = T(null),
        o = () => {
          l.value = null
        },
        r = (l) => {
          const { data: o, rowKey: r } = e
          let a = null
          ;(r.value && (a = ($(o) || []).find((e) => Ut(e, r.value) === l)),
            (n.value = a),
            t.emit('current-change', n.value, null))
        }
      return {
        setCurrentRowKey: (e) => {
          ;(t.store.assertRowKey(), (l.value = e), r(e))
        },
        restoreCurrentRowKey: o,
        setCurrentRowByKey: r,
        updateCurrentRow: (e) => {
          const l = n.value
          if (e && e !== l) return ((n.value = e), void t.emit('current-change', n.value, l))
          !e && l && ((n.value = null), t.emit('current-change', null, l))
        },
        updateCurrentRowData: () => {
          const a = e.rowKey.value,
            s = e.data.value || [],
            i = n.value
          if (!s.includes(i) && i) {
            if (a) {
              const e = Ut(i, a)
              r(e)
            } else n.value = null
            null === n.value && t.emit('current-change', null, i)
          } else l.value && (r(l.value), o())
        },
        states: { _currentRowKey: l, currentRow: n }
      }
    })({ data: o, rowKey: n })
  return {
    assertRowKey: () => {
      if (!n.value) throw new Error('[ElTable] prop row-key is required')
    },
    updateColumns: W,
    scheduleLayout: A,
    isSelected: (e) => b.value.includes(e),
    clearSelection: () => {
      y.value = !1
      b.value.length && ((b.value = []), t.emit('selection-change', []))
    },
    cleanSelection: () => {
      let e
      if (n.value) {
        e = []
        const t = Qt(b.value, n.value),
          l = Qt(o.value, n.value)
        for (const n in t) L(t, n) && !l[n] && e.push(t[n].row)
      } else e = b.value.filter((e) => !o.value.includes(e))
      if (e.length) {
        const l = b.value.filter((t) => !e.includes(t))
        ;((b.value = l), t.emit('selection-change', l.slice()))
      }
    },
    getSelectionRows: () => (b.value || []).slice(),
    toggleRowSelection: (e, l = void 0, n = !0) => {
      if (el(b.value, e, l)) {
        const l = (b.value || []).slice()
        ;(n && t.emit('select', l, e), t.emit('selection-change', l))
      }
    },
    _toggleAllSelection: () => {
      var e, l
      const n = x.value ? !y.value : !(y.value || b.value.length)
      y.value = n
      let r = !1,
        a = 0
      const s =
        null == (l = null == (e = null == t ? void 0 : t.store) ? void 0 : e.states)
          ? void 0
          : l.rowKey.value
      ;(o.value.forEach((e, t) => {
        const l = t + a
        ;(C.value
          ? C.value.call(null, e, l) && el(b.value, e, n) && (r = !0)
          : el(b.value, e, n) && (r = !0),
          (a += M(Ut(e, s))))
      }),
        r && t.emit('selection-change', b.value ? b.value.slice() : []),
        t.emit('select-all', b.value))
    },
    toggleAllSelection: null,
    updateSelectionByRowKey: () => {
      const e = Qt(b.value, n.value)
      o.value.forEach((t) => {
        const l = Ut(t, n.value),
          o = e[l]
        o && (b.value[o.index] = t)
      })
    },
    updateAllSelected: () => {
      var e, l, r
      if (0 === (null == (e = o.value) ? void 0 : e.length)) return void (y.value = !1)
      let a
      n.value && (a = Qt(b.value, n.value))
      let s = !0,
        i = 0,
        u = 0
      for (let c = 0, h = (o.value || []).length; c < h; c++) {
        const e =
            null == (r = null == (l = null == t ? void 0 : t.store) ? void 0 : l.states)
              ? void 0
              : r.rowKey.value,
          h = c + u,
          p = o.value[c],
          f = C.value && C.value.call(null, p, h)
        if (((d = p), a ? a[Ut(d, n.value)] : b.value.includes(d))) i++
        else if (!C.value || f) {
          s = !1
          break
        }
        u += M(Ut(p, e))
      }
      var d
      ;(0 === i && (s = !1), (y.value = s))
    },
    updateFilters: (e, t) => {
      Array.isArray(e) || (e = [e])
      const l = {}
      return (
        e.forEach((e) => {
          ;((S.value[e.id] = t), (l[e.columnKey || e.id] = t))
        }),
        l
      )
    },
    updateCurrentRow: ee,
    updateSort: j,
    execFilter: z,
    execSort: D,
    execQuery: (e = void 0) => {
      ;((e && e.filter) || z(), D())
    },
    clearFilter: (e) => {
      const { tableHeaderRef: l } = t.refs
      if (!l) return
      const n = Object.assign({}, l.filterPanels),
        o = Object.keys(n)
      if (o.length)
        if (('string' == typeof e && (e = [e]), Array.isArray(e))) {
          const l = e.map((e) => Xt({ columns: u.value }, e))
          ;(o.forEach((e) => {
            const t = l.find((t) => t.id === e)
            t && (t.filteredValue = [])
          }),
            t.store.commit('filterChange', { column: l, values: [], silent: !0, multi: !0 }))
        } else
          (o.forEach((e) => {
            const t = u.value.find((t) => t.id === e)
            t && (t.filteredValue = [])
          }),
            (S.value = {}),
            t.store.commit('filterChange', { column: {}, values: [], silent: !0 }))
    },
    clearSort: () => {
      R.value && (j(null, null, null), t.store.commit('changeSortCondition', { silent: !0 }))
    },
    toggleRowExpansion: V,
    setExpandRowKeysAdapter: (e) => {
      ;(P(e), X(e))
    },
    setCurrentRowKey: te,
    toggleRowExpansionAdapter: (e, t) => {
      u.value.some(({ type: e }) => 'expand' === e) ? V(e, t) : G(e, t)
    },
    isRowExpanded: q,
    updateExpandRows: _,
    updateCurrentRowData: J,
    loadOrToggle: Q,
    updateTreeData: U,
    states: {
      tableSize: l,
      rowKey: n,
      data: o,
      _data: r,
      isComplex: a,
      _columns: s,
      originColumns: i,
      columns: u,
      fixedColumns: d,
      rightFixedColumns: c,
      leafColumns: h,
      fixedLeafColumns: p,
      rightFixedLeafColumns: f,
      updateOrderFns: [],
      leafColumnsLength: v,
      fixedLeafColumnsLength: m,
      rightFixedLeafColumnsLength: g,
      isAllSelected: y,
      selection: b,
      reserveSelection: w,
      selectOnIndeterminate: x,
      selectable: C,
      filters: S,
      filteredData: E,
      sortingColumn: R,
      sortProp: N,
      sortOrder: k,
      hoverRow: O,
      ...Y,
      ...Z,
      ...le
    }
  }
}
function pl(e, t) {
  return e.map((e) => {
    var l
    return e.id === t.id
      ? t
      : ((null == (l = e.children) ? void 0 : l.length) && (e.children = pl(e.children, t)), e)
  })
}
function fl(e) {
  ;(e.forEach((e) => {
    var t, l
    ;((e.no = null == (t = e.getColumnIndex) ? void 0 : t.call(e)),
      (null == (l = e.children) ? void 0 : l.length) && fl(e.children))
  }),
    e.sort((e, t) => e.no - t.no))
}
const vl = {
  rowKey: 'rowKey',
  defaultExpandAll: 'defaultExpandAll',
  selectOnIndeterminate: 'selectOnIndeterminate',
  indent: 'indent',
  lazy: 'lazy',
  data: 'data',
  'treeProps.hasChildren': { key: 'lazyColumnIdentifier', default: 'hasChildren' },
  'treeProps.children': { key: 'childrenColumnName', default: 'children' }
}
function ml(e, t) {
  if (!e) throw new Error('Table is required.')
  const l = (function () {
    const e = F(),
      t = hl()
    return {
      ns: j('table'),
      ...t,
      mutations: {
        setData(t, l) {
          const n = $(t._data) !== l
          ;((t.data.value = l),
            (t._data.value = l),
            e.store.execQuery(),
            e.store.updateCurrentRowData(),
            e.store.updateExpandRows(),
            e.store.updateTreeData(e.store.states.defaultExpandAll.value),
            $(t.reserveSelection)
              ? (e.store.assertRowKey(), e.store.updateSelectionByRowKey())
              : n
                ? e.store.clearSelection()
                : e.store.cleanSelection(),
            e.store.updateAllSelected(),
            e.$ready && e.store.scheduleLayout())
        },
        insertColumn(t, l, n, o) {
          const r = $(t._columns)
          let a = []
          ;(n
            ? (n && !n.children && (n.children = []), n.children.push(l), (a = pl(r, n)))
            : (r.push(l), (a = r)),
            fl(a),
            (t._columns.value = a),
            t.updateOrderFns.push(o),
            'selection' === l.type &&
              ((t.selectable.value = l.selectable),
              (t.reserveSelection.value = l.reserveSelection)),
            e.$ready && (e.store.updateColumns(), e.store.scheduleLayout()))
        },
        updateColumnOrder(t, l) {
          var n
          ;(null == (n = l.getColumnIndex) ? void 0 : n.call(l)) !== l.no &&
            (fl(t._columns.value), e.$ready && e.store.updateColumns())
        },
        removeColumn(t, l, n, o) {
          const r = $(t._columns) || []
          if (n)
            (n.children.splice(
              n.children.findIndex((e) => e.id === l.id),
              1
            ),
              z(() => {
                var e
                0 === (null == (e = n.children) ? void 0 : e.length) && delete n.children
              }),
              (t._columns.value = pl(r, n)))
          else {
            const e = r.indexOf(l)
            e > -1 && (r.splice(e, 1), (t._columns.value = r))
          }
          const a = t.updateOrderFns.indexOf(o)
          ;(a > -1 && t.updateOrderFns.splice(a, 1),
            e.$ready && (e.store.updateColumns(), e.store.scheduleLayout()))
        },
        sort(t, l) {
          const { prop: n, order: o, init: r } = l
          if (n) {
            const l = $(t.columns).find((e) => e.property === n)
            l &&
              ((l.order = o),
              e.store.updateSort(l, n, o),
              e.store.commit('changeSortCondition', { init: r }))
          }
        },
        changeSortCondition(t, l) {
          const { sortingColumn: n, sortProp: o, sortOrder: r } = t,
            a = $(n),
            s = $(o),
            i = $(r)
          ;(null === i && ((t.sortingColumn.value = null), (t.sortProp.value = null)),
            e.store.execQuery({ filter: !0 }),
            (l && (l.silent || l.init)) || e.emit('sort-change', { column: a, prop: s, order: i }),
            e.store.updateTableScrollY())
        },
        filterChange(t, l) {
          const { column: n, values: o, silent: r } = l,
            a = e.store.updateFilters(n, o)
          ;(e.store.execQuery(), r || e.emit('filter-change', a), e.store.updateTableScrollY())
        },
        toggleAllSelection() {
          e.store.toggleAllSelection()
        },
        rowSelectedChanged(t, l) {
          ;(e.store.toggleRowSelection(l), e.store.updateAllSelected())
        },
        setHoverRow(e, t) {
          e.hoverRow.value = t
        },
        setCurrentRow(t, l) {
          e.store.updateCurrentRow(l)
        }
      },
      commit: function (t, ...l) {
        const n = e.store.mutations
        if (!n[t]) throw new Error(`Action not found: ${t}`)
        n[t].apply(e, [e.store.states].concat(l))
      },
      updateTableScrollY: function () {
        z(() => e.layout.updateScrollY.apply(e.layout))
      }
    }
  })()
  return (
    (l.toggleAllSelection = Xe(l._toggleAllSelection, 10)),
    Object.keys(vl).forEach((e) => {
      gl(yl(t, e), e, l)
    }),
    (function (e, t) {
      Object.keys(vl).forEach((l) => {
        I(
          () => yl(t, l),
          (t) => {
            gl(t, l, e)
          }
        )
      })
    })(l, t),
    l
  )
}
function gl(e, t, l) {
  let n = e,
    o = vl[t]
  ;('object' == typeof vl[t] && ((o = o.key), (n = n || vl[t].default)), (l.states[o].value = n))
}
function yl(e, t) {
  if (t.includes('.')) {
    const l = t.split('.')
    let n = e
    return (
      l.forEach((e) => {
        n = n[e]
      }),
      n
    )
  }
  return e[t]
}
class bl {
  constructor(e) {
    ;((this.observers = []),
      (this.table = null),
      (this.store = null),
      (this.columns = []),
      (this.fit = !0),
      (this.showHeader = !0),
      (this.height = T(null)),
      (this.scrollX = T(!1)),
      (this.scrollY = T(!1)),
      (this.bodyWidth = T(null)),
      (this.fixedWidth = T(null)),
      (this.rightFixedWidth = T(null)),
      (this.gutterWidth = 0))
    for (const t in e) L(e, t) && (D(this[t]) ? (this[t].value = e[t]) : (this[t] = e[t]))
    if (!this.table) throw new Error('Table is required for Table Layout')
    if (!this.store) throw new Error('Store is required for Table Layout')
  }
  updateScrollY() {
    if (null === this.height.value) return !1
    const e = this.table.refs.scrollBarRef
    if (this.table.vnode.el && (null == e ? void 0 : e.wrapRef)) {
      let t = !0
      const l = this.scrollY.value
      return (
        (t = e.wrapRef.scrollHeight > e.wrapRef.clientHeight),
        (this.scrollY.value = t),
        l !== t
      )
    }
    return !1
  }
  setHeight(e, t = 'height') {
    if (!P) return
    const l = this.table.vnode.el
    var n
    if (
      ((e =
        'number' == typeof (n = e)
          ? n
          : 'string' == typeof n
            ? /^\d+(?:px)?$/.test(n)
              ? Number.parseInt(n, 10)
              : n
            : null),
      (this.height.value = Number(e)),
      !l && (e || 0 === e))
    )
      return z(() => this.setHeight(e, t))
    'number' == typeof e
      ? ((l.style[t] = `${e}px`), this.updateElsHeight())
      : 'string' == typeof e && ((l.style[t] = e), this.updateElsHeight())
  }
  setMaxHeight(e) {
    this.setHeight(e, 'max-height')
  }
  getFlattenColumns() {
    const e = []
    return (
      this.table.store.states.columns.value.forEach((t) => {
        t.isColumnGroup ? e.push.apply(e, t.columns) : e.push(t)
      }),
      e
    )
  }
  updateElsHeight() {
    ;(this.updateScrollY(), this.notifyObservers('scrollable'))
  }
  headerDisplayNone(e) {
    if (!e) return !0
    let t = e
    for (; 'DIV' !== t.tagName; ) {
      if ('none' === getComputedStyle(t).display) return !0
      t = t.parentElement
    }
    return !1
  }
  updateColumnsWidth() {
    if (!P) return
    const e = this.fit,
      t = this.table.vnode.el.clientWidth
    let l = 0
    const n = this.getFlattenColumns(),
      o = n.filter((e) => 'number' != typeof e.width)
    if (
      (n.forEach((e) => {
        'number' == typeof e.width && e.realWidth && (e.realWidth = null)
      }),
      o.length > 0 && e)
    ) {
      if (
        (n.forEach((e) => {
          l += Number(e.width || e.minWidth || 80)
        }),
        l <= t)
      ) {
        this.scrollX.value = !1
        const e = t - l
        if (1 === o.length) o[0].realWidth = Number(o[0].minWidth || 80) + e
        else {
          const t = e / o.reduce((e, t) => e + Number(t.minWidth || 80), 0)
          let l = 0
          ;(o.forEach((e, n) => {
            if (0 === n) return
            const o = Math.floor(Number(e.minWidth || 80) * t)
            ;((l += o), (e.realWidth = Number(e.minWidth || 80) + o))
          }),
            (o[0].realWidth = Number(o[0].minWidth || 80) + e - l))
        }
      } else
        ((this.scrollX.value = !0),
          o.forEach((e) => {
            e.realWidth = Number(e.minWidth)
          }))
      ;((this.bodyWidth.value = Math.max(l, t)),
        (this.table.state.resizeState.value.width = this.bodyWidth.value))
    } else
      (n.forEach((e) => {
        ;(e.width || e.minWidth
          ? (e.realWidth = Number(e.width || e.minWidth))
          : (e.realWidth = 80),
          (l += e.realWidth))
      }),
        (this.scrollX.value = l > t),
        (this.bodyWidth.value = l))
    const r = this.store.states.fixedColumns.value
    if (r.length > 0) {
      let e = 0
      ;(r.forEach((t) => {
        e += Number(t.realWidth || t.width)
      }),
        (this.fixedWidth.value = e))
    }
    const a = this.store.states.rightFixedColumns.value
    if (a.length > 0) {
      let e = 0
      ;(a.forEach((t) => {
        e += Number(t.realWidth || t.width)
      }),
        (this.rightFixedWidth.value = e))
    }
    this.notifyObservers('columns')
  }
  addObserver(e) {
    this.observers.push(e)
  }
  removeObserver(e) {
    const t = this.observers.indexOf(e)
    ;-1 !== t && this.observers.splice(t, 1)
  }
  notifyObservers(e) {
    this.observers.forEach((t) => {
      var l, n
      switch (e) {
        case 'columns':
          null == (l = t.state) || l.onColumnsChange(this)
          break
        case 'scrollable':
          null == (n = t.state) || n.onScrollableChange(this)
          break
        default:
          throw new Error(`Table Layout don't have event ${e}.`)
      }
    })
  }
}
const { CheckboxGroup: wl } = qe,
  xl = _({
    name: 'ElTableFilterPanel',
    components: {
      ElCheckbox: qe,
      ElCheckboxGroup: wl,
      ElScrollbar: Y,
      ElTooltip: Ve,
      ElIcon: q,
      ArrowDown: X,
      ArrowUp: G
    },
    directives: { ClickOutside: Ge },
    props: {
      placement: { type: String, default: 'bottom-start' },
      store: { type: Object },
      column: { type: Object },
      upDataColumn: { type: Function }
    },
    setup(e) {
      const t = F(),
        { t: l } = U(),
        n = j('table-filter'),
        o = null == t ? void 0 : t.parent
      o.filterPanels.value[e.column.id] || (o.filterPanels.value[e.column.id] = t)
      const r = T(!1),
        a = T(null),
        s = B(() => e.column && e.column.filters),
        i = B({
          get: () => {
            var t
            return ((null == (t = e.column) ? void 0 : t.filteredValue) || [])[0]
          },
          set: (e) => {
            u.value && (null != e ? u.value.splice(0, 1, e) : u.value.splice(0, 1))
          }
        }),
        u = B({
          get: () => (e.column && e.column.filteredValue) || [],
          set(t) {
            e.column && e.upDataColumn('filteredValue', t)
          }
        }),
        d = B(() => !e.column || e.column.filterMultiple),
        c = () => {
          r.value = !1
        },
        h = (t) => {
          ;(e.store.commit('filterChange', { column: e.column, values: t }),
            e.store.updateAllSelected())
        }
      I(
        r,
        (t) => {
          e.column && e.upDataColumn('filterOpened', t)
        },
        { immediate: !0 }
      )
      const p = B(() => {
        var e, t
        return null == (t = null == (e = a.value) ? void 0 : e.popperRef) ? void 0 : t.contentRef
      })
      return {
        tooltipVisible: r,
        multiple: d,
        filteredValue: u,
        filterValue: i,
        filters: s,
        handleConfirm: () => {
          ;(h(u.value), c())
        },
        handleReset: () => {
          ;((u.value = []), h(u.value), c())
        },
        handleSelect: (e) => {
          ;((i.value = e), h(null != e ? u.value : []), c())
        },
        isActive: (e) => e.value === i.value,
        t: l,
        ns: n,
        showFilterPanel: (e) => {
          ;(e.stopPropagation(), (r.value = !r.value))
        },
        hideFilterPanel: () => {
          r.value = !1
        },
        popperPaneRef: p,
        tooltip: a
      }
    }
  }),
  Cl = { key: 0 },
  Sl = ['disabled'],
  El = ['label', 'onClick']
var Rl = V(xl, [
  [
    'render',
    function (e, t, l, n, o, r) {
      const a = Q('el-checkbox'),
        s = Q('el-checkbox-group'),
        i = Q('el-scrollbar'),
        u = Q('arrow-up'),
        d = Q('arrow-down'),
        c = Q('el-icon'),
        h = Q('el-tooltip'),
        p = Z('click-outside')
      return (
        J(),
        ee(
          h,
          {
            ref: 'tooltip',
            visible: e.tooltipVisible,
            offset: 0,
            placement: e.placement,
            'show-arrow': !1,
            'stop-popper-mouse-event': !1,
            teleported: '',
            effect: 'light',
            pure: '',
            'popper-class': e.ns.b(),
            persistent: ''
          },
          {
            content: te(() => [
              e.multiple
                ? (J(),
                  le('div', Cl, [
                    ne(
                      'div',
                      { class: oe(e.ns.e('content')) },
                      [
                        re(
                          i,
                          { 'wrap-class': e.ns.e('wrap') },
                          {
                            default: te(() => [
                              re(
                                s,
                                {
                                  modelValue: e.filteredValue,
                                  'onUpdate:modelValue':
                                    t[0] || (t[0] = (t) => (e.filteredValue = t)),
                                  class: oe(e.ns.e('checkbox-group'))
                                },
                                {
                                  default: te(() => [
                                    (J(!0),
                                    le(
                                      ae,
                                      null,
                                      se(
                                        e.filters,
                                        (e) => (
                                          J(),
                                          ee(
                                            a,
                                            { key: e.value, label: e.value },
                                            { default: te(() => [ie(ue(e.text), 1)]), _: 2 },
                                            1032,
                                            ['label']
                                          )
                                        )
                                      ),
                                      128
                                    ))
                                  ]),
                                  _: 1
                                },
                                8,
                                ['modelValue', 'class']
                              )
                            ]),
                            _: 1
                          },
                          8,
                          ['wrap-class']
                        )
                      ],
                      2
                    ),
                    ne(
                      'div',
                      { class: oe(e.ns.e('bottom')) },
                      [
                        ne(
                          'button',
                          {
                            class: oe({ [e.ns.is('disabled')]: 0 === e.filteredValue.length }),
                            disabled: 0 === e.filteredValue.length,
                            type: 'button',
                            onClick:
                              t[1] || (t[1] = (...t) => e.handleConfirm && e.handleConfirm(...t))
                          },
                          ue(e.t('el.table.confirmFilter')),
                          11,
                          Sl
                        ),
                        ne(
                          'button',
                          {
                            type: 'button',
                            onClick: t[2] || (t[2] = (...t) => e.handleReset && e.handleReset(...t))
                          },
                          ue(e.t('el.table.resetFilter')),
                          1
                        )
                      ],
                      2
                    )
                  ]))
                : (J(),
                  le(
                    'ul',
                    { key: 1, class: oe(e.ns.e('list')) },
                    [
                      ne(
                        'li',
                        {
                          class: oe([
                            e.ns.e('list-item'),
                            {
                              [e.ns.is('active')]:
                                void 0 === e.filterValue || null === e.filterValue
                            }
                          ]),
                          onClick: t[3] || (t[3] = (t) => e.handleSelect(null))
                        },
                        ue(e.t('el.table.clearFilter')),
                        3
                      ),
                      (J(!0),
                      le(
                        ae,
                        null,
                        se(
                          e.filters,
                          (t) => (
                            J(),
                            le(
                              'li',
                              {
                                key: t.value,
                                class: oe([e.ns.e('list-item'), e.ns.is('active', e.isActive(t))]),
                                label: t.value,
                                onClick: (l) => e.handleSelect(t.value)
                              },
                              ue(t.text),
                              11,
                              El
                            )
                          )
                        ),
                        128
                      ))
                    ],
                    2
                  ))
            ]),
            default: te(() => [
              de(
                (J(),
                le(
                  'span',
                  {
                    class: oe([
                      `${e.ns.namespace.value}-table__column-filter-trigger`,
                      `${e.ns.namespace.value}-none-outline`
                    ]),
                    onClick: t[4] || (t[4] = (...t) => e.showFilterPanel && e.showFilterPanel(...t))
                  },
                  [
                    re(c, null, {
                      default: te(() => [
                        e.column.filterOpened ? (J(), ee(u, { key: 0 })) : (J(), ee(d, { key: 1 }))
                      ]),
                      _: 1
                    })
                  ],
                  2
                )),
                [[p, e.hideFilterPanel, e.popperPaneRef]]
              )
            ]),
            _: 1
          },
          8,
          ['visible', 'placement', 'popper-class']
        )
      )
    }
  ],
  [
    '__file',
    '/home/runner/work/element-plus/element-plus/packages/components/table/src/filter-panel.vue'
  ]
])
function Nl(e) {
  const t = F()
  ;(ce(() => {
    l.value.addObserver(t)
  }),
    he(() => {
      ;(n(l.value), o(l.value))
    }),
    pe(() => {
      ;(n(l.value), o(l.value))
    }),
    fe(() => {
      l.value.removeObserver(t)
    }))
  const l = B(() => {
      const t = e.layout
      if (!t) throw new Error('Can not find table layout.')
      return t
    }),
    n = (t) => {
      var l
      const n = (null == (l = e.vnode.el) ? void 0 : l.querySelectorAll('colgroup > col')) || []
      if (!n.length) return
      const o = t.getFlattenColumns(),
        r = {}
      o.forEach((e) => {
        r[e.id] = e
      })
      for (let e = 0, a = n.length; e < a; e++) {
        const t = n[e],
          l = t.getAttribute('name'),
          o = r[l]
        o && t.setAttribute('width', o.realWidth || o.width)
      }
    },
    o = (t) => {
      var l, n
      const o =
        (null == (l = e.vnode.el) ? void 0 : l.querySelectorAll('colgroup > col[name=gutter]')) ||
        []
      for (let e = 0, a = o.length; e < a; e++) {
        o[e].setAttribute('width', t.scrollY.value ? t.gutterWidth : '0')
      }
      const r = (null == (n = e.vnode.el) ? void 0 : n.querySelectorAll('th.gutter')) || []
      for (let e = 0, a = r.length; e < a; e++) {
        const l = r[e]
        ;((l.style.width = t.scrollY.value ? `${t.gutterWidth}px` : '0'),
          (l.style.display = t.scrollY.value ? '' : 'none'))
      }
    }
  return { tableLayout: l.value, onColumnsChange: n, onScrollableChange: o }
}
const kl = Symbol('ElTable')
const Ol = (e) => {
  const t = []
  return (
    e.forEach((e) => {
      e.children ? (t.push(e), t.push.apply(t, Ol(e.children))) : t.push(e)
    }),
    t
  )
}
function Ll(e) {
  const t = ve(kl),
    l = B(() =>
      ((e) => {
        let t = 1
        const l = (e, n) => {
          if ((n && ((e.level = n.level + 1), t < e.level && (t = e.level)), e.children)) {
            let t = 0
            ;(e.children.forEach((n) => {
              ;(l(n, e), (t += n.colSpan))
            }),
              (e.colSpan = t))
          } else e.colSpan = 1
        }
        e.forEach((e) => {
          ;((e.level = 1), l(e, void 0))
        })
        const n = []
        for (let o = 0; o < t; o++) n.push([])
        return (
          Ol(e).forEach((e) => {
            ;(e.children
              ? ((e.rowSpan = 1), e.children.forEach((e) => (e.isSubColumn = !0)))
              : (e.rowSpan = t - e.level + 1),
              n[e.level - 1].push(e))
          }),
          n
        )
      })(e.store.states.originColumns.value)
    )
  return {
    isGroup: B(() => {
      const e = l.value.length > 1
      return (e && t && (t.state.isGroup.value = !0), e)
    }),
    toggleAllSelection: (e) => {
      ;(e.stopPropagation(), null == t || t.store.commit('toggleAllSelection'))
    },
    columnRows: l
  }
}
var Hl = _({
  name: 'ElTableHeader',
  components: { ElCheckbox: qe },
  props: {
    fixed: { type: String, default: '' },
    store: { required: !0, type: Object },
    border: Boolean,
    defaultSort: { type: Object, default: () => ({ prop: '', order: '' }) }
  },
  setup(e, { emit: t }) {
    const l = F(),
      n = ve(kl),
      o = j('table'),
      r = T({}),
      { onColumnsChange: a, onScrollableChange: s } = Nl(n)
    he(async () => {
      ;(await z(), await z())
      const { prop: t, order: l } = e.defaultSort
      null == n || n.store.commit('sort', { prop: t, order: l, init: !0 })
    })
    const {
        handleHeaderClick: i,
        handleHeaderContextMenu: u,
        handleMouseDown: d,
        handleMouseMove: c,
        handleMouseOut: h,
        handleSortClick: p,
        handleFilterClick: f
      } = (function (e, t) {
        const l = F(),
          n = ve(kl),
          o = (e) => {
            e.stopPropagation()
          },
          r = T(null),
          a = T(!1),
          s = T({}),
          i = (t, l, o) => {
            var r
            t.stopPropagation()
            const a =
                l.order === o
                  ? null
                  : o ||
                    (({ order: e, sortOrders: t }) => {
                      if ('' === e) return t[0]
                      const l = t.indexOf(e || null)
                      return t[l > t.length - 2 ? 0 : l + 1]
                    })(l),
              s = null == (r = t.target) ? void 0 : r.closest('th')
            if (s && ye(s, 'noclick')) return void be(s, 'noclick')
            if (!l.sortable) return
            const i = e.store.states
            let u,
              d = i.sortProp.value
            const c = i.sortingColumn.value
            ;((c !== l || (c === l && null === c.order)) &&
              (c && (c.order = null), (i.sortingColumn.value = l), (d = l.property)),
              (u = l.order = a || null),
              (i.sortProp.value = d),
              (i.sortOrder.value = u),
              null == n || n.store.commit('changeSortCondition'))
          }
        return {
          handleHeaderClick: (e, t) => {
            ;(!t.filters && t.sortable ? i(e, t, !1) : t.filterable && !t.sortable && o(e),
              null == n || n.emit('header-click', t, e))
          },
          handleHeaderContextMenu: (e, t) => {
            null == n || n.emit('header-contextmenu', t, e)
          },
          handleMouseDown: (o, i) => {
            if (P && !(i.children && i.children.length > 0) && r.value && e.border) {
              a.value = !0
              const u = n
              t('set-drag-visible', !0)
              const d = (null == u ? void 0 : u.vnode.el).getBoundingClientRect().left,
                c = l.vnode.el.querySelector(`th.${i.id}`),
                h = c.getBoundingClientRect(),
                p = h.left - d + 30
              ;(me(c, 'noclick'),
                (s.value = {
                  startMouseLeft: o.clientX,
                  startLeft: h.right - d,
                  startColumnLeft: h.left - d,
                  tableLeft: d
                }))
              const f = null == u ? void 0 : u.refs.resizeProxy
              ;((f.style.left = `${s.value.startLeft}px`),
                (document.onselectstart = function () {
                  return !1
                }),
                (document.ondragstart = function () {
                  return !1
                }))
              const v = (e) => {
                  const t = e.clientX - s.value.startMouseLeft,
                    l = s.value.startLeft + t
                  f.style.left = `${Math.max(p, l)}px`
                },
                m = () => {
                  if (a.value) {
                    const { startColumnLeft: l, startLeft: n } = s.value,
                      d = Number.parseInt(f.style.left, 10) - l
                    ;((i.width = i.realWidth = d),
                      null == u || u.emit('header-dragend', i.width, n - l, i, o),
                      requestAnimationFrame(() => {
                        e.store.scheduleLayout(!1, !0)
                      }),
                      (document.body.style.cursor = ''),
                      (a.value = !1),
                      (r.value = null),
                      (s.value = {}),
                      t('set-drag-visible', !1))
                  }
                  ;(document.removeEventListener('mousemove', v),
                    document.removeEventListener('mouseup', m),
                    (document.onselectstart = null),
                    (document.ondragstart = null),
                    setTimeout(() => {
                      be(c, 'noclick')
                    }, 0))
                }
              ;(document.addEventListener('mousemove', v), document.addEventListener('mouseup', m))
            }
          },
          handleMouseMove: (t, l) => {
            if (l.children && l.children.length > 0) return
            const n = t.target
            if (!ge(n)) return
            const o = null == n ? void 0 : n.closest('th')
            if (l && l.resizable && !a.value && e.border) {
              const e = o.getBoundingClientRect(),
                n = document.body.style
              e.width > 12 && e.right - t.pageX < 8
                ? ((n.cursor = 'col-resize'),
                  ye(o, 'is-sortable') && (o.style.cursor = 'col-resize'),
                  (r.value = l))
                : a.value ||
                  ((n.cursor = ''),
                  ye(o, 'is-sortable') && (o.style.cursor = 'pointer'),
                  (r.value = null))
            }
          },
          handleMouseOut: () => {
            P && (document.body.style.cursor = '')
          },
          handleSortClick: i,
          handleFilterClick: o
        }
      })(e, t),
      {
        getHeaderRowStyle: v,
        getHeaderRowClass: m,
        getHeaderCellStyle: g,
        getHeaderCellClass: y
      } = (function (e) {
        const t = ve(kl),
          l = j('table')
        return {
          getHeaderRowStyle: (e) => {
            const l = null == t ? void 0 : t.props.headerRowStyle
            return 'function' == typeof l ? l.call(null, { rowIndex: e }) : l
          },
          getHeaderRowClass: (e) => {
            const l = [],
              n = null == t ? void 0 : t.props.headerRowClassName
            return (
              'string' == typeof n
                ? l.push(n)
                : 'function' == typeof n && l.push(n.call(null, { rowIndex: e })),
              l.join(' ')
            )
          },
          getHeaderCellStyle: (l, n, o, r) => {
            var a
            let s = null != (a = null == t ? void 0 : t.props.headerCellStyle) ? a : {}
            'function' == typeof s &&
              (s = s.call(null, { rowIndex: l, columnIndex: n, row: o, column: r }))
            const i = il(n, r.fixed, e.store, o)
            return (ul(i, 'left'), ul(i, 'right'), Object.assign({}, s, i))
          },
          getHeaderCellClass: (n, o, r, a) => {
            const s = al(l.b(), o, a.fixed, e.store, r),
              i = [a.id, a.order, a.headerAlign, a.className, a.labelClassName, ...s]
            ;(a.children || i.push('is-leaf'), a.sortable && i.push('is-sortable'))
            const u = null == t ? void 0 : t.props.headerCellClassName
            return (
              'string' == typeof u
                ? i.push(u)
                : 'function' == typeof u &&
                  i.push(u.call(null, { rowIndex: n, columnIndex: o, row: r, column: a })),
              i.push(l.e('cell')),
              i.filter((e) => Boolean(e)).join(' ')
            )
          }
        }
      })(e),
      { isGroup: b, toggleAllSelection: w, columnRows: x } = Ll(e)
    return (
      (l.state = { onColumnsChange: a, onScrollableChange: s }),
      (l.filterPanels = r),
      {
        ns: o,
        filterPanels: r,
        onColumnsChange: a,
        onScrollableChange: s,
        columnRows: x,
        getHeaderRowClass: m,
        getHeaderRowStyle: v,
        getHeaderCellClass: y,
        getHeaderCellStyle: g,
        handleHeaderClick: i,
        handleHeaderContextMenu: u,
        handleMouseDown: d,
        handleMouseMove: c,
        handleMouseOut: h,
        handleSortClick: p,
        handleFilterClick: f,
        isGroup: b,
        toggleAllSelection: w
      }
    )
  },
  render() {
    const {
      ns: e,
      isGroup: t,
      columnRows: l,
      getHeaderCellStyle: n,
      getHeaderCellClass: o,
      getHeaderRowClass: r,
      getHeaderRowStyle: a,
      handleHeaderClick: s,
      handleHeaderContextMenu: i,
      handleMouseDown: u,
      handleMouseMove: d,
      handleSortClick: c,
      handleMouseOut: h,
      store: p,
      $parent: f
    } = this
    let v = 1
    return we(
      'thead',
      { class: { [e.is('group')]: t } },
      l.map((e, t) =>
        we(
          'tr',
          { class: r(t), key: t, style: a(t) },
          e.map(
            (l, r) => (
              l.rowSpan > v && (v = l.rowSpan),
              we(
                'th',
                {
                  class: o(t, r, e, l),
                  colspan: l.colSpan,
                  key: `${l.id}-thead`,
                  rowspan: l.rowSpan,
                  style: n(t, r, e, l),
                  onClick: (e) => s(e, l),
                  onContextmenu: (e) => i(e, l),
                  onMousedown: (e) => u(e, l),
                  onMousemove: (e) => d(e, l),
                  onMouseout: h
                },
                [
                  we(
                    'div',
                    {
                      class: [
                        'cell',
                        l.filteredValue && l.filteredValue.length > 0 ? 'highlight' : ''
                      ]
                    },
                    [
                      l.renderHeader
                        ? l.renderHeader({ column: l, $index: r, store: p, _self: f })
                        : l.label,
                      l.sortable &&
                        we('span', { onClick: (e) => c(e, l), class: 'caret-wrapper' }, [
                          we('i', {
                            onClick: (e) => c(e, l, 'ascending'),
                            class: 'sort-caret ascending'
                          }),
                          we('i', {
                            onClick: (e) => c(e, l, 'descending'),
                            class: 'sort-caret descending'
                          })
                        ]),
                      l.filterable &&
                        we(Rl, {
                          store: p,
                          placement: l.filterPlacement || 'bottom-start',
                          column: l,
                          upDataColumn: (e, t) => {
                            l[e] = t
                          }
                        })
                    ]
                  )
                ]
              )
            )
          )
        )
      )
    )
  }
})
function Wl(e) {
  const t = ve(kl),
    l = T(''),
    n = T(we('div')),
    { nextZIndex: o } = xe(),
    r = (l, n, o) => {
      var r
      const a = t,
        s = _t(l)
      let i
      const u = null == (r = null == a ? void 0 : a.vnode.el) ? void 0 : r.dataset.prefix
      ;(s &&
        ((i = Gt({ columns: e.store.states.columns.value }, s, u)),
        i && (null == a || a.emit(`cell-${o}`, n, i, s, l))),
        null == a || a.emit(`row-${o}`, n, i, l))
    },
    a = Xe((t) => {
      e.store.commit('setHoverRow', t)
    }, 30),
    s = Xe(() => {
      e.store.commit('setHoverRow', null)
    }, 30)
  return {
    handleDoubleClick: (e, t) => {
      r(e, t, 'dblclick')
    },
    handleClick: (t, l) => {
      ;(e.store.commit('setCurrentRow', l), r(t, l, 'click'))
    },
    handleContextMenu: (e, t) => {
      r(e, t, 'contextmenu')
    },
    handleMouseEnter: a,
    handleMouseLeave: s,
    handleCellMouseEnter: (l, n, r) => {
      var a
      const s = t,
        i = _t(l),
        u = null == (a = null == s ? void 0 : s.vnode.el) ? void 0 : a.dataset.prefix
      if (i) {
        const t = Gt({ columns: e.store.states.columns.value }, i, u),
          o = (s.hoverState = { cell: i, column: t, row: n })
        null == s || s.emit('cell-mouse-enter', o.row, o.column, o.cell, l)
      }
      if (!r) return
      const d = l.target.querySelector('.cell')
      if (!ye(d, `${u}-tooltip`) || !d.childNodes.length) return
      const c = document.createRange()
      ;(c.setStart(d, 0), c.setEnd(d, d.childNodes.length))
      let h = c.getBoundingClientRect().width,
        p = c.getBoundingClientRect().height
      h - Math.floor(h) < 0.001 && (h = Math.floor(h))
      p - Math.floor(p) < 0.001 && (p = Math.floor(p))
      const {
          top: f,
          left: v,
          right: m,
          bottom: g
        } = ((e) => {
          const t = window.getComputedStyle(e, null)
          return {
            left: Number.parseInt(t.paddingLeft, 10) || 0,
            right: Number.parseInt(t.paddingRight, 10) || 0,
            top: Number.parseInt(t.paddingTop, 10) || 0,
            bottom: Number.parseInt(t.paddingBottom, 10) || 0
          }
        })(d),
        y = f + g
      ;(h + (v + m) > d.offsetWidth || p + y > d.offsetHeight || d.scrollWidth > d.offsetWidth) &&
        (function (e, t, l, n, o) {
          o = mt({ enterable: !0, showArrow: !0 }, o)
          const r = null == e ? void 0 : e.dataset.prefix,
            a = null == e ? void 0 : e.querySelector(`.${r}-scrollbar__wrap`)
          function s() {
            i && i.update()
          }
          ;(null == ll || ll(),
            (ll = () => {
              try {
                ;(i && i.destroy(),
                  c && (null == e || e.removeChild(c)),
                  t.removeEventListener('mouseenter', u),
                  t.removeEventListener('mouseleave', d),
                  null == a || a.removeEventListener('scroll', ll),
                  (ll = void 0))
              } catch (l) {}
            }))
          let i = null,
            u = s,
            d = ll
          o.enterable &&
            ({ onOpen: u, onClose: d } = De({
              showAfter: o.showAfter,
              hideAfter: o.hideAfter,
              open: s,
              close: ll
            }))
          const c = (function () {
            const t = 'light' === o.effect,
              a = document.createElement('div')
            return (
              (a.className = [`${r}-popper`, t ? 'is-light' : 'is-dark', o.popperClass || ''].join(
                ' '
              )),
              (l = Vt(l)),
              (a.innerHTML = l),
              (a.style.zIndex = String(n())),
              null == e || e.appendChild(a),
              a
            )
          })()
          ;((c.onmouseenter = u), (c.onmouseleave = d))
          const h = []
          if (
            (o.offset && h.push({ name: 'offset', options: { offset: [0, o.offset] } }),
            o.showArrow)
          ) {
            const e = c.appendChild(
              (function () {
                const e = document.createElement('div')
                return ((e.className = `${r}-popper__arrow`), e)
              })()
            )
            h.push({ name: 'arrow', options: { element: e, padding: 10 } })
          }
          const p = o.popperOptions || {}
          ;((i = Pe(t, c, {
            placement: o.placement || 'top',
            strategy: 'fixed',
            ...p,
            modifiers: p.modifiers ? h.concat(p.modifiers) : h
          })),
            t.addEventListener('mouseenter', u),
            t.addEventListener('mouseleave', d),
            null == a || a.addEventListener('scroll', ll))
        })(null == t ? void 0 : t.refs.tableWrapper, i, i.innerText || i.textContent, o, r)
    },
    handleCellMouseLeave: (e) => {
      if (!_t(e)) return
      const l = null == t ? void 0 : t.hoverState
      null == t ||
        t.emit(
          'cell-mouse-leave',
          null == l ? void 0 : l.row,
          null == l ? void 0 : l.column,
          null == l ? void 0 : l.cell,
          e
        )
    },
    tooltipContent: l,
    tooltipTrigger: n
  }
}
function Al(e) {
  const t = ve(kl),
    l = j('table'),
    {
      handleDoubleClick: n,
      handleClick: o,
      handleContextMenu: r,
      handleMouseEnter: a,
      handleMouseLeave: s,
      handleCellMouseEnter: i,
      handleCellMouseLeave: u,
      tooltipContent: d,
      tooltipTrigger: c
    } = Wl(e),
    {
      getRowStyle: h,
      getRowClass: p,
      getCellStyle: f,
      getCellClass: v,
      getSpan: m,
      getColspanRealWidth: g
    } = (function (e) {
      const t = ve(kl),
        l = j('table')
      return {
        getRowStyle: (e, l) => {
          const n = null == t ? void 0 : t.props.rowStyle
          return 'function' == typeof n ? n.call(null, { row: e, rowIndex: l }) : n || null
        },
        getRowClass: (n, o) => {
          const r = [l.e('row')]
          ;((null == t ? void 0 : t.props.highlightCurrentRow) &&
            n === e.store.states.currentRow.value &&
            r.push('current-row'),
            e.stripe && o % 2 == 1 && r.push(l.em('row', 'striped')))
          const a = null == t ? void 0 : t.props.rowClassName
          return (
            'string' == typeof a
              ? r.push(a)
              : 'function' == typeof a && r.push(a.call(null, { row: n, rowIndex: o })),
            r
          )
        },
        getCellStyle: (l, n, o, r) => {
          const a = null == t ? void 0 : t.props.cellStyle
          let s = null != a ? a : {}
          'function' == typeof a &&
            (s = a.call(null, { rowIndex: l, columnIndex: n, row: o, column: r }))
          const i = il(n, null == e ? void 0 : e.fixed, e.store)
          return (ul(i, 'left'), ul(i, 'right'), Object.assign({}, s, i))
        },
        getCellClass: (n, o, r, a, s) => {
          const i = al(l.b(), o, null == e ? void 0 : e.fixed, e.store, void 0, s),
            u = [a.id, a.align, a.className, ...i],
            d = null == t ? void 0 : t.props.cellClassName
          return (
            'string' == typeof d
              ? u.push(d)
              : 'function' == typeof d &&
                u.push(d.call(null, { rowIndex: n, columnIndex: o, row: r, column: a })),
            u.push(l.e('cell')),
            u.filter((e) => Boolean(e)).join(' ')
          )
        },
        getSpan: (e, l, n, o) => {
          let r = 1,
            a = 1
          const s = null == t ? void 0 : t.props.spanMethod
          if ('function' == typeof s) {
            const t = s({ row: e, column: l, rowIndex: n, columnIndex: o })
            Array.isArray(t)
              ? ((r = t[0]), (a = t[1]))
              : 'object' == typeof t && ((r = t.rowspan), (a = t.colspan))
          }
          return { rowspan: r, colspan: a }
        },
        getColspanRealWidth: (e, t, l) => {
          if (t < 1) return e[l].realWidth
          const n = e.map(({ realWidth: e, width: t }) => e || t).slice(l, l + t)
          return Number(n.reduce((e, t) => Number(e) + Number(t), -1))
        }
      }
    })(e),
    y = B(() => e.store.states.columns.value.findIndex(({ type: e }) => 'default' === e)),
    b = (e, l) => {
      const n = t.props.rowKey
      return n ? Ut(e, n) : l
    },
    w = (d, c, w, C = !1) => {
      const { tooltipEffect: S, tooltipOptions: E, store: R } = e,
        { indent: N, columns: k } = R.states,
        O = p(d, c)
      let L = !0
      w && (O.push(l.em('row', `level-${w.level}`)), (L = w.display))
      return we(
        'tr',
        {
          style: [L ? null : { display: 'none' }, h(d, c)],
          class: O,
          key: b(d, c),
          onDblclick: (e) => n(e, d),
          onClick: (e) => o(e, d),
          onContextmenu: (e) => r(e, d),
          onMouseenter: () => a(c),
          onMouseleave: s
        },
        k.value.map((l, n) => {
          const { rowspan: o, colspan: r } = m(d, l, c, n)
          if (!o || !r) return null
          const a = { ...l }
          a.realWidth = g(k.value, r, n)
          const s = {
            store: e.store,
            _self: e.context || t,
            column: a,
            row: d,
            $index: c,
            cellIndex: n,
            expanded: C
          }
          n === y.value &&
            w &&
            ((s.treeNode = { indent: w.level * N.value, level: w.level }),
            'boolean' == typeof w.expanded &&
              ((s.treeNode.expanded = w.expanded),
              'loading' in w && (s.treeNode.loading = w.loading),
              'noLazyChildren' in w && (s.treeNode.noLazyChildren = w.noLazyChildren)))
          const h = `${c},${n}`,
            p = a.columnKey || a.rawColumnKey || '',
            b = x(n, l, s),
            R = l.showOverflowTooltip && mt({ effect: S }, E, l.showOverflowTooltip)
          return we(
            'td',
            {
              style: f(c, n, d, l),
              class: v(c, n, d, l, r - 1),
              key: `${p}${h}`,
              rowspan: o,
              colspan: r,
              onMouseenter: (e) => i(e, d, R),
              onMouseleave: u
            },
            [b]
          )
        })
      )
    },
    x = (e, t, l) => t.renderCell(l)
  return {
    wrappedRowRender: (n, o) => {
      const r = e.store,
        { isRowExpanded: a, assertRowKey: s } = r,
        { treeData: i, lazyTreeNodeMap: u, childrenColumnName: d, rowKey: c } = r.states,
        h = r.states.columns.value
      if (h.some(({ type: e }) => 'expand' === e)) {
        const e = a(n),
          s = w(n, o, void 0, e),
          i = t.renderExpanded
        return e
          ? i
            ? [
                [
                  s,
                  we('tr', { key: `expanded-row__${s.key}` }, [
                    we(
                      'td',
                      { colspan: h.length, class: `${l.e('cell')} ${l.e('expanded-cell')}` },
                      [i({ row: n, $index: o, store: r, expanded: e })]
                    )
                  ])
                ]
              ]
            : s
          : [[s]]
      }
      if (Object.keys(i.value).length) {
        s()
        const e = Ut(n, c.value)
        let t = i.value[e],
          l = null
        t &&
          ((l = { expanded: t.expanded, level: t.level, display: !0 }),
          'boolean' == typeof t.lazy &&
            ('boolean' == typeof t.loaded &&
              t.loaded &&
              (l.noLazyChildren = !(t.children && t.children.length)),
            (l.loading = t.loading)))
        const r = [w(n, o, l)]
        if (t) {
          let l = 0
          const a = (e, n) => {
            e &&
              e.length &&
              n &&
              e.forEach((e) => {
                const s = {
                    display: n.display && n.expanded,
                    level: n.level + 1,
                    expanded: !1,
                    noLazyChildren: !1,
                    loading: !1
                  },
                  h = Ut(e, c.value)
                if (null == h) throw new Error('For nested data item, row-key is required.')
                if (
                  ((t = { ...i.value[h] }),
                  t &&
                    ((s.expanded = t.expanded),
                    (t.level = t.level || s.level),
                    (t.display = !(!t.expanded || !s.display)),
                    'boolean' == typeof t.lazy &&
                      ('boolean' == typeof t.loaded &&
                        t.loaded &&
                        (s.noLazyChildren = !(t.children && t.children.length)),
                      (s.loading = t.loading))),
                  l++,
                  r.push(w(e, o + l, s)),
                  t)
                ) {
                  const l = u.value[h] || e[d.value]
                  a(l, t)
                }
              })
          }
          t.display = !0
          const s = u.value[e] || n[d.value]
          a(s, t)
        }
        return r
      }
      return w(n, o, void 0)
    },
    tooltipContent: d,
    tooltipTrigger: c
  }
}
var Ml = _({
  name: 'ElTableBody',
  props: {
    store: { required: !0, type: Object },
    stripe: Boolean,
    tooltipEffect: String,
    tooltipOptions: { type: Object },
    context: { default: () => ({}), type: Object },
    rowClassName: [String, Function],
    rowStyle: [Object, Function],
    fixed: { type: String, default: '' },
    highlight: Boolean
  },
  setup(e) {
    const t = F(),
      l = ve(kl),
      n = j('table'),
      { wrappedRowRender: o, tooltipContent: r, tooltipTrigger: a } = Al(e),
      { onColumnsChange: s, onScrollableChange: i } = Nl(l)
    return (
      I(e.store.states.hoverRow, (l, o) => {
        if (!e.store.states.isComplex.value || !P) return
        let r = window.requestAnimationFrame
        ;(r || (r = (e) => window.setTimeout(e, 16)),
          r(() => {
            const e = null == t ? void 0 : t.vnode.el,
              r = Array.from((null == e ? void 0 : e.children) || []).filter((e) =>
                null == e ? void 0 : e.classList.contains(`${n.e('row')}`)
              ),
              a = r[o],
              s = r[l]
            ;(a && be(a, 'hover-row'), s && me(s, 'hover-row'))
          }))
      }),
      fe(() => {
        var e
        null == (e = ll) || e()
      }),
      {
        ns: n,
        onColumnsChange: s,
        onScrollableChange: i,
        wrappedRowRender: o,
        tooltipContent: r,
        tooltipTrigger: a
      }
    )
  },
  render() {
    const { wrappedRowRender: e, store: t } = this,
      l = t.states.data.value || []
    return we('tbody', {}, [l.reduce((t, l) => t.concat(e(l, t.length)), [])])
  }
})
function Fl(e) {
  const t = 'auto' === e.tableLayout
  let l = e.columns || []
  t && l.every((e) => void 0 === e.width) && (l = [])
  return we(
    'colgroup',
    {},
    l.map((l) =>
      we(
        'col',
        ((l) => {
          const n = { key: `${e.tableLayout}_${l.id}`, style: {}, name: void 0 }
          return (t ? (n.style = { width: `${l.width}px` }) : (n.name = l.id), n)
        })(l)
      )
    )
  )
}
function Tl(e) {
  const { columns: t } = (function () {
      const e = ve(kl),
        t = null == e ? void 0 : e.store
      return {
        leftFixedLeafCount: B(() => t.states.fixedLeafColumnsLength.value),
        rightFixedLeafCount: B(() => t.states.rightFixedColumns.value.length),
        columnsCount: B(() => t.states.columns.value.length),
        leftFixedCount: B(() => t.states.fixedColumns.value.length),
        rightFixedCount: B(() => t.states.rightFixedColumns.value.length),
        columns: t.states.columns
      }
    })(),
    l = j('table')
  return {
    getCellClasses: (t, n) => {
      const o = t[n],
        r = [l.e('cell'), o.id, o.align, o.labelClassName, ...al(l.b(), n, o.fixed, e.store)]
      return (o.className && r.push(o.className), o.children || r.push(l.is('leaf')), r)
    },
    getCellStyles: (t, l) => {
      const n = il(l, t.fixed, e.store)
      return (ul(n, 'left'), ul(n, 'right'), n)
    },
    columns: t
  }
}
Fl.props = ['columns', 'tableLayout']
var $l = _({
  name: 'ElTableFooter',
  props: {
    fixed: { type: String, default: '' },
    store: { required: !0, type: Object },
    summaryMethod: Function,
    sumText: String,
    border: Boolean,
    defaultSort: { type: Object, default: () => ({ prop: '', order: '' }) }
  },
  setup(e) {
    const { getCellClasses: t, getCellStyles: l, columns: n } = Tl(e)
    return { ns: j('table'), getCellClasses: t, getCellStyles: l, columns: n }
  },
  render() {
    const {
        columns: e,
        getCellStyles: t,
        getCellClasses: l,
        summaryMethod: n,
        sumText: o,
        ns: r
      } = this,
      a = this.store.states.data.value
    let s = []
    return (
      n
        ? (s = n({ columns: e, data: a }))
        : e.forEach((e, t) => {
            if (0 === t) return void (s[t] = o)
            const l = a.map((t) => Number(t[e.property])),
              n = []
            let r = !0
            l.forEach((e) => {
              if (!Number.isNaN(+e)) {
                r = !1
                const t = `${e}`.split('.')[1]
                n.push(t ? t.length : 0)
              }
            })
            const i = Math.max.apply(null, n)
            s[t] = r
              ? ''
              : l.reduce((e, t) => {
                  const l = Number(t)
                  return Number.isNaN(+l) ? e : Number.parseFloat((e + t).toFixed(Math.min(i, 20)))
                }, 0)
          }),
      we('table', { class: r.e('footer'), cellspacing: '0', cellpadding: '0', border: '0' }, [
        Fl({ columns: e }),
        we('tbody', [
          we('tr', {}, [
            ...e.map((n, o) =>
              we(
                'td',
                { key: o, colspan: n.colSpan, rowspan: n.rowSpan, class: l(e, o), style: t(n, o) },
                [we('div', { class: ['cell', n.labelClassName] }, [s[o]])]
              )
            )
          ])
        ])
      ])
    )
  }
})
function Bl(e, t, l, n) {
  const o = T(!1),
    r = T(null),
    a = T(!1),
    s = T({ width: null, height: null, headerHeight: null }),
    i = T(!1),
    u = T(),
    d = T(0),
    c = T(0),
    h = T(0),
    p = T(0),
    f = T(0)
  ;(Ce(() => {
    t.setHeight(e.height)
  }),
    Ce(() => {
      t.setMaxHeight(e.maxHeight)
    }),
    I(
      () => [e.currentRowKey, l.states.rowKey],
      ([e, t]) => {
        $(t) && $(e) && l.setCurrentRowKey(`${e}`)
      },
      { immediate: !0 }
    ),
    I(
      () => e.data,
      (e) => {
        n.store.commit('setData', e)
      },
      { immediate: !0, deep: !0 }
    ),
    Ce(() => {
      e.expandRowKeys && l.setExpandRowKeysAdapter(e.expandRowKeys)
    }))
  const v = B(
      () =>
        e.height ||
        e.maxHeight ||
        l.states.fixedColumns.value.length > 0 ||
        l.states.rightFixedColumns.value.length > 0
    ),
    m = B(() => ({ width: t.bodyWidth.value ? `${t.bodyWidth.value}px` : '' })),
    g = () => {
      ;(v.value && t.updateElsHeight(), t.updateColumnsWidth(), requestAnimationFrame(b))
    }
  he(async () => {
    ;(await z(), l.updateColumns(), w(), requestAnimationFrame(g))
    const t = n.vnode.el,
      o = n.refs.headerWrapper
    ;(e.flexible && t && t.parentElement && (t.parentElement.style.minWidth = '0'),
      (s.value = {
        width: (u.value = t.offsetWidth),
        height: t.offsetHeight,
        headerHeight: e.showHeader && o ? o.offsetHeight : null
      }),
      l.states.columns.value.forEach((e) => {
        e.filteredValue &&
          e.filteredValue.length &&
          n.store.commit('filterChange', { column: e, values: e.filteredValue, silent: !0 })
      }),
      (n.$ready = !0))
  })
  const y = (e) => {
      const { tableWrapper: l } = n.refs
      ;((e, l) => {
        if (!e) return
        const n = Array.from(e.classList).filter((e) => !e.startsWith('is-scrolling-'))
        ;(n.push(t.scrollX.value ? l : 'is-scrolling-none'), (e.className = n.join(' ')))
      })(l, e)
    },
    b = function () {
      if (!n.refs.scrollBarRef) return
      if (!t.scrollX.value) {
        const e = 'is-scrolling-none'
        return void (
          ((e) => {
            const { tableWrapper: t } = n.refs
            return !(!t || !t.classList.contains(e))
          })(e) || y(e)
        )
      }
      const e = n.refs.scrollBarRef.wrapRef
      if (!e) return
      const { scrollLeft: l, offsetWidth: o, scrollWidth: r } = e,
        { headerWrapper: a, footerWrapper: s } = n.refs
      ;(a && (a.scrollLeft = l), s && (s.scrollLeft = l))
      y(
        l >= r - o - 1
          ? 'is-scrolling-right'
          : 0 === l
            ? 'is-scrolling-left'
            : 'is-scrolling-middle'
      )
    },
    w = () => {
      n.refs.scrollBarRef &&
        (n.refs.scrollBarRef.wrapRef &&
          Se(n.refs.scrollBarRef.wrapRef, 'scroll', b, { passive: !0 }),
        e.fit ? Ee(n.vnode.el, x) : Se(window, 'resize', x),
        Ee(n.refs.bodyWrapper, () => {
          var e, t
          ;(x(), null == (t = null == (e = n.refs) ? void 0 : e.scrollBarRef) || t.update())
        }))
    },
    x = () => {
      var t, l, o, r
      const a = n.vnode.el
      if (!n.$ready || !a) return
      let i = !1
      const { width: m, height: y, headerHeight: b } = s.value,
        w = (u.value = a.offsetWidth)
      m !== w && (i = !0)
      const x = a.offsetHeight
      ;(e.height || v.value) && y !== x && (i = !0)
      const C =
        'fixed' === e.tableLayout
          ? n.refs.headerWrapper
          : null == (t = n.refs.tableHeaderRef)
            ? void 0
            : t.$el
      ;(e.showHeader && (null == C ? void 0 : C.offsetHeight) !== b && (i = !0),
        (d.value = (null == (l = n.refs.tableWrapper) ? void 0 : l.scrollHeight) || 0),
        (h.value = (null == C ? void 0 : C.scrollHeight) || 0),
        (p.value = (null == (o = n.refs.footerWrapper) ? void 0 : o.offsetHeight) || 0),
        (f.value = (null == (r = n.refs.appendWrapper) ? void 0 : r.offsetHeight) || 0),
        (c.value = d.value - h.value - p.value - f.value),
        i &&
          ((s.value = {
            width: w,
            height: x,
            headerHeight: (e.showHeader && (null == C ? void 0 : C.offsetHeight)) || 0
          }),
          g()))
    },
    C = Re(),
    S = B(() => {
      const { bodyWidth: e, scrollY: l, gutterWidth: n } = t
      return e.value ? e.value - (l.value ? n : 0) + 'px' : ''
    }),
    E = B(() => (e.maxHeight ? 'fixed' : e.tableLayout)),
    R = B(() => {
      if (e.data && e.data.length) return null
      let t = '100%'
      e.height && c.value && (t = `${c.value}px`)
      const l = u.value
      return { width: l ? `${l}px` : '', height: t }
    }),
    N = B(() =>
      e.height
        ? { height: Number.isNaN(Number(e.height)) ? e.height : `${e.height}px` }
        : e.maxHeight
          ? { maxHeight: Number.isNaN(Number(e.maxHeight)) ? e.maxHeight : `${e.maxHeight}px` }
          : {}
    ),
    k = B(() =>
      e.height
        ? { height: '100%' }
        : e.maxHeight
          ? Number.isNaN(Number(e.maxHeight))
            ? { maxHeight: `calc(${e.maxHeight} - ${h.value + p.value}px)` }
            : { maxHeight: e.maxHeight - h.value - p.value + 'px' }
          : {}
    )
  return {
    isHidden: o,
    renderExpanded: r,
    setDragVisible: (e) => {
      a.value = e
    },
    isGroup: i,
    handleMouseLeave: () => {
      ;(n.store.commit('setHoverRow', null), n.hoverState && (n.hoverState = null))
    },
    handleHeaderFooterMousewheel: (e, t) => {
      const { pixelX: l, pixelY: o } = t
      Math.abs(l) >= Math.abs(o) && (n.refs.bodyWrapper.scrollLeft += t.pixelX / 5)
    },
    tableSize: C,
    emptyBlockStyle: R,
    handleFixedMousewheel: (e, t) => {
      const l = n.refs.bodyWrapper
      if (Math.abs(t.spinY) > 0) {
        const n = l.scrollTop
        ;(t.pixelY < 0 && 0 !== n && e.preventDefault(),
          t.pixelY > 0 && l.scrollHeight - l.clientHeight > n && e.preventDefault(),
          (l.scrollTop += Math.ceil(t.pixelY / 5)))
      } else l.scrollLeft += Math.ceil(t.pixelX / 5)
    },
    resizeProxyVisible: a,
    bodyWidth: S,
    resizeState: s,
    doLayout: g,
    tableBodyStyles: m,
    tableLayout: E,
    scrollbarViewStyle: { display: 'inline-block', verticalAlign: 'middle' },
    tableInnerStyle: N,
    scrollbarStyle: k
  }
}
function Il(e) {
  const t = T()
  ;(he(() => {
    ;(() => {
      const l = e.vnode.el.querySelector('.hidden-columns'),
        n = e.store.states.updateOrderFns
      ;((t.value = new MutationObserver(() => {
        n.forEach((e) => e())
      })),
        t.value.observe(l, { childList: !0, subtree: !0 }))
    })()
  }),
    fe(() => {
      var e
      null == (e = t.value) || e.disconnect()
    }))
}
var Kl = {
  data: { type: Array, default: () => [] },
  size: Ne,
  width: [String, Number],
  height: [String, Number],
  maxHeight: [String, Number],
  fit: { type: Boolean, default: !0 },
  stripe: Boolean,
  border: Boolean,
  rowKey: [String, Function],
  showHeader: { type: Boolean, default: !0 },
  showSummary: Boolean,
  sumText: String,
  summaryMethod: Function,
  rowClassName: [String, Function],
  rowStyle: [Object, Function],
  cellClassName: [String, Function],
  cellStyle: [Object, Function],
  headerRowClassName: [String, Function],
  headerRowStyle: [Object, Function],
  headerCellClassName: [String, Function],
  headerCellStyle: [Object, Function],
  highlightCurrentRow: Boolean,
  currentRowKey: [String, Number],
  emptyText: String,
  expandRowKeys: Array,
  defaultExpandAll: Boolean,
  defaultSort: Object,
  tooltipEffect: String,
  tooltipOptions: Object,
  spanMethod: Function,
  selectOnIndeterminate: { type: Boolean, default: !0 },
  indent: { type: Number, default: 16 },
  treeProps: {
    type: Object,
    default: () => ({ hasChildren: 'hasChildren', children: 'children' })
  },
  lazy: Boolean,
  load: Function,
  style: { type: Object, default: () => ({}) },
  className: { type: String, default: '' },
  tableLayout: { type: String, default: 'fixed' },
  scrollbarAlwaysOn: { type: Boolean, default: !1 },
  flexible: Boolean,
  showOverflowTooltip: [Boolean, Object]
}
let jl = 1
const zl = _({
    name: 'ElTable',
    directives: { Mousewheel: Dt },
    components: { TableHeader: Hl, TableBody: Ml, TableFooter: $l, ElScrollbar: Y, hColgroup: Fl },
    props: Kl,
    emits: [
      'select',
      'select-all',
      'selection-change',
      'cell-mouse-enter',
      'cell-mouse-leave',
      'cell-contextmenu',
      'cell-click',
      'cell-dblclick',
      'row-click',
      'row-contextmenu',
      'row-dblclick',
      'header-click',
      'header-contextmenu',
      'sort-change',
      'filter-change',
      'current-change',
      'header-dragend',
      'expand-change'
    ],
    setup(e) {
      const { t: t } = U(),
        l = j('table'),
        n = F()
      Oe(kl, n)
      const o = ml(n, e)
      n.store = o
      const r = new bl({ store: n.store, table: n, fit: e.fit, showHeader: e.showHeader })
      n.layout = r
      const a = B(() => 0 === (o.states.data.value || []).length),
        {
          setCurrentRow: s,
          getSelectionRows: i,
          toggleRowSelection: u,
          clearSelection: d,
          clearFilter: c,
          toggleAllSelection: h,
          toggleRowExpansion: p,
          clearSort: f,
          sort: v
        } = (function (e) {
          return {
            setCurrentRow: (t) => {
              e.commit('setCurrentRow', t)
            },
            getSelectionRows: () => e.getSelectionRows(),
            toggleRowSelection: (t, l) => {
              ;(e.toggleRowSelection(t, l, !1), e.updateAllSelected())
            },
            clearSelection: () => {
              e.clearSelection()
            },
            clearFilter: (t) => {
              e.clearFilter(t)
            },
            toggleAllSelection: () => {
              e.commit('toggleAllSelection')
            },
            toggleRowExpansion: (t, l) => {
              e.toggleRowExpansionAdapter(t, l)
            },
            clearSort: () => {
              e.clearSort()
            },
            sort: (t, l) => {
              e.commit('sort', { prop: t, order: l })
            }
          }
        })(o),
        {
          isHidden: m,
          renderExpanded: g,
          setDragVisible: y,
          isGroup: b,
          handleMouseLeave: w,
          handleHeaderFooterMousewheel: x,
          tableSize: C,
          emptyBlockStyle: S,
          handleFixedMousewheel: E,
          resizeProxyVisible: R,
          bodyWidth: N,
          resizeState: k,
          doLayout: O,
          tableBodyStyles: L,
          tableLayout: H,
          scrollbarViewStyle: W,
          tableInnerStyle: A,
          scrollbarStyle: M
        } = Bl(e, r, o, n),
        {
          scrollBarRef: $,
          scrollTo: I,
          setScrollLeft: K,
          setScrollTop: z
        } = (() => {
          const e = T(),
            t = (t, l) => {
              const n = e.value
              n && ke(l) && ['Top', 'Left'].includes(t) && n[`setScroll${t}`](l)
            }
          return {
            scrollBarRef: e,
            scrollTo: (t, l) => {
              const n = e.value
              n && n.scrollTo(t, l)
            },
            setScrollTop: (e) => t('Top', e),
            setScrollLeft: (e) => t('Left', e)
          }
        })(),
        D = Xe(O, 50),
        P = `${l.namespace.value}-table_${jl++}`
      ;((n.tableId = P),
        (n.state = { isGroup: b, resizeState: k, doLayout: O, debouncedUpdateLayout: D }))
      const V = B(() => e.sumText || t('el.table.sumText')),
        _ = B(() => e.emptyText || t('el.table.emptyText'))
      return (
        Il(n),
        {
          ns: l,
          layout: r,
          store: o,
          handleHeaderFooterMousewheel: x,
          handleMouseLeave: w,
          tableId: P,
          tableSize: C,
          isHidden: m,
          isEmpty: a,
          renderExpanded: g,
          resizeProxyVisible: R,
          resizeState: k,
          isGroup: b,
          bodyWidth: N,
          tableBodyStyles: L,
          emptyBlockStyle: S,
          debouncedUpdateLayout: D,
          handleFixedMousewheel: E,
          setCurrentRow: s,
          getSelectionRows: i,
          toggleRowSelection: u,
          clearSelection: d,
          clearFilter: c,
          toggleAllSelection: h,
          toggleRowExpansion: p,
          clearSort: f,
          doLayout: O,
          sort: v,
          t: t,
          setDragVisible: y,
          context: n,
          computedSumText: V,
          computedEmptyText: _,
          tableLayout: H,
          scrollbarViewStyle: W,
          tableInnerStyle: A,
          scrollbarStyle: M,
          scrollBarRef: $,
          scrollTo: I,
          setScrollLeft: K,
          setScrollTop: z
        }
      )
    }
  }),
  Dl = ['data-prefix'],
  Pl = { ref: 'hiddenColumns', class: 'hidden-columns' }
var Vl = V(zl, [
  [
    'render',
    function (e, t, l, n, o, r) {
      const a = Q('hColgroup'),
        s = Q('table-header'),
        i = Q('table-body'),
        u = Q('el-scrollbar'),
        d = Q('table-footer'),
        c = Z('mousewheel')
      return (
        J(),
        le(
          'div',
          {
            ref: 'tableWrapper',
            class: oe([
              {
                [e.ns.m('fit')]: e.fit,
                [e.ns.m('striped')]: e.stripe,
                [e.ns.m('border')]: e.border || e.isGroup,
                [e.ns.m('hidden')]: e.isHidden,
                [e.ns.m('group')]: e.isGroup,
                [e.ns.m('fluid-height')]: e.maxHeight,
                [e.ns.m('scrollable-x')]: e.layout.scrollX.value,
                [e.ns.m('scrollable-y')]: e.layout.scrollY.value,
                [e.ns.m('enable-row-hover')]: !e.store.states.isComplex.value,
                [e.ns.m('enable-row-transition')]:
                  0 !== (e.store.states.data.value || []).length &&
                  (e.store.states.data.value || []).length < 100,
                'has-footer': e.showSummary
              },
              e.ns.m(e.tableSize),
              e.className,
              e.ns.b(),
              e.ns.m(`layout-${e.tableLayout}`)
            ]),
            style: He(e.style),
            'data-prefix': e.ns.namespace.value,
            onMouseleave: t[0] || (t[0] = (...t) => e.handleMouseLeave && e.handleMouseLeave(...t))
          },
          [
            ne(
              'div',
              { class: oe(e.ns.e('inner-wrapper')), style: He(e.tableInnerStyle) },
              [
                ne('div', Pl, [Le(e.$slots, 'default')], 512),
                e.showHeader && 'fixed' === e.tableLayout
                  ? de(
                      (J(),
                      le(
                        'div',
                        { key: 0, ref: 'headerWrapper', class: oe(e.ns.e('header-wrapper')) },
                        [
                          ne(
                            'table',
                            {
                              ref: 'tableHeader',
                              class: oe(e.ns.e('header')),
                              style: He(e.tableBodyStyles),
                              border: '0',
                              cellpadding: '0',
                              cellspacing: '0'
                            },
                            [
                              re(
                                a,
                                {
                                  columns: e.store.states.columns.value,
                                  'table-layout': e.tableLayout
                                },
                                null,
                                8,
                                ['columns', 'table-layout']
                              ),
                              re(
                                s,
                                {
                                  ref: 'tableHeaderRef',
                                  border: e.border,
                                  'default-sort': e.defaultSort,
                                  store: e.store,
                                  onSetDragVisible: e.setDragVisible
                                },
                                null,
                                8,
                                ['border', 'default-sort', 'store', 'onSetDragVisible']
                              )
                            ],
                            6
                          )
                        ],
                        2
                      )),
                      [[c, e.handleHeaderFooterMousewheel]]
                    )
                  : We('v-if', !0),
                ne(
                  'div',
                  { ref: 'bodyWrapper', class: oe(e.ns.e('body-wrapper')) },
                  [
                    re(
                      u,
                      {
                        ref: 'scrollBarRef',
                        'view-style': e.scrollbarViewStyle,
                        'wrap-style': e.scrollbarStyle,
                        always: e.scrollbarAlwaysOn
                      },
                      {
                        default: te(() => [
                          ne(
                            'table',
                            {
                              ref: 'tableBody',
                              class: oe(e.ns.e('body')),
                              cellspacing: '0',
                              cellpadding: '0',
                              border: '0',
                              style: He({ width: e.bodyWidth, tableLayout: e.tableLayout })
                            },
                            [
                              re(
                                a,
                                {
                                  columns: e.store.states.columns.value,
                                  'table-layout': e.tableLayout
                                },
                                null,
                                8,
                                ['columns', 'table-layout']
                              ),
                              e.showHeader && 'auto' === e.tableLayout
                                ? (J(),
                                  ee(
                                    s,
                                    {
                                      key: 0,
                                      ref: 'tableHeaderRef',
                                      border: e.border,
                                      'default-sort': e.defaultSort,
                                      store: e.store,
                                      onSetDragVisible: e.setDragVisible
                                    },
                                    null,
                                    8,
                                    ['border', 'default-sort', 'store', 'onSetDragVisible']
                                  ))
                                : We('v-if', !0),
                              re(
                                i,
                                {
                                  context: e.context,
                                  highlight: e.highlightCurrentRow,
                                  'row-class-name': e.rowClassName,
                                  'tooltip-effect': e.tooltipEffect,
                                  'tooltip-options': e.tooltipOptions,
                                  'row-style': e.rowStyle,
                                  store: e.store,
                                  stripe: e.stripe
                                },
                                null,
                                8,
                                [
                                  'context',
                                  'highlight',
                                  'row-class-name',
                                  'tooltip-effect',
                                  'tooltip-options',
                                  'row-style',
                                  'store',
                                  'stripe'
                                ]
                              )
                            ],
                            6
                          ),
                          e.isEmpty
                            ? (J(),
                              le(
                                'div',
                                {
                                  key: 0,
                                  ref: 'emptyBlock',
                                  style: He(e.emptyBlockStyle),
                                  class: oe(e.ns.e('empty-block'))
                                },
                                [
                                  ne(
                                    'span',
                                    { class: oe(e.ns.e('empty-text')) },
                                    [
                                      Le(e.$slots, 'empty', {}, () => [
                                        ie(ue(e.computedEmptyText), 1)
                                      ])
                                    ],
                                    2
                                  )
                                ],
                                6
                              ))
                            : We('v-if', !0),
                          e.$slots.append
                            ? (J(),
                              le(
                                'div',
                                {
                                  key: 1,
                                  ref: 'appendWrapper',
                                  class: oe(e.ns.e('append-wrapper'))
                                },
                                [Le(e.$slots, 'append')],
                                2
                              ))
                            : We('v-if', !0)
                        ]),
                        _: 3
                      },
                      8,
                      ['view-style', 'wrap-style', 'always']
                    )
                  ],
                  2
                ),
                e.showSummary
                  ? de(
                      (J(),
                      le(
                        'div',
                        { key: 1, ref: 'footerWrapper', class: oe(e.ns.e('footer-wrapper')) },
                        [
                          re(
                            d,
                            {
                              border: e.border,
                              'default-sort': e.defaultSort,
                              store: e.store,
                              style: He(e.tableBodyStyles),
                              'sum-text': e.computedSumText,
                              'summary-method': e.summaryMethod
                            },
                            null,
                            8,
                            [
                              'border',
                              'default-sort',
                              'store',
                              'style',
                              'sum-text',
                              'summary-method'
                            ]
                          )
                        ],
                        2
                      )),
                      [
                        [Ae, !e.isEmpty],
                        [c, e.handleHeaderFooterMousewheel]
                      ]
                    )
                  : We('v-if', !0),
                e.border || e.isGroup
                  ? (J(), le('div', { key: 2, class: oe(e.ns.e('border-left-patch')) }, null, 2))
                  : We('v-if', !0)
              ],
              6
            ),
            de(
              ne('div', { ref: 'resizeProxy', class: oe(e.ns.e('column-resize-proxy')) }, null, 2),
              [[Ae, e.resizeProxyVisible]]
            )
          ],
          46,
          Dl
        )
      )
    }
  ],
  ['__file', '/home/runner/work/element-plus/element-plus/packages/components/table/src/table.vue']
])
const _l = { selection: 'table-column--selection', expand: 'table__expand-column' },
  Yl = {
    default: { order: '' },
    selection: { width: 48, minWidth: 48, realWidth: 48, order: '' },
    expand: { width: 48, minWidth: 48, realWidth: 48, order: '' },
    index: { width: 48, minWidth: 48, realWidth: 48, order: '' }
  },
  ql = {
    selection: {
      renderHeader: ({ store: e }) =>
        we(qe, {
          disabled: e.states.data.value && 0 === e.states.data.value.length,
          size: e.states.tableSize.value,
          indeterminate: e.states.selection.value.length > 0 && !e.states.isAllSelected.value,
          'onUpdate:modelValue': e.toggleAllSelection,
          modelValue: e.states.isAllSelected.value
        }),
      renderCell: ({ row: e, column: t, store: l, $index: n }) =>
        we(qe, {
          disabled: !!t.selectable && !t.selectable.call(null, e, n),
          size: l.states.tableSize.value,
          onChange: () => {
            l.commit('rowSelectedChanged', e)
          },
          onClick: (e) => e.stopPropagation(),
          modelValue: l.isSelected(e)
        }),
      sortable: !1,
      resizable: !1
    },
    index: {
      renderHeader: ({ column: e }) => e.label || '#',
      renderCell({ column: e, $index: t }) {
        let l = t + 1
        const n = e.index
        return (
          'number' == typeof n ? (l = t + n) : 'function' == typeof n && (l = n(t)),
          we('div', {}, [l])
        )
      },
      sortable: !1
    },
    expand: {
      renderHeader: ({ column: e }) => e.label || '',
      renderCell({ row: e, store: t, expanded: l }) {
        const { ns: n } = t,
          o = [n.e('expand-icon')]
        l && o.push(n.em('expand-icon', 'expanded'))
        return we(
          'div',
          {
            class: o,
            onClick: function (l) {
              ;(l.stopPropagation(), t.toggleRowExpansion(e))
            }
          },
          { default: () => [we(q, null, { default: () => [we(Fe)] })] }
        )
      },
      sortable: !1,
      resizable: !1
    }
  }
function Xl({ row: e, column: t, $index: l }) {
  var n
  const o = t.property,
    r = o && Me(e, o).value
  return t && t.formatter
    ? t.formatter(e, t, r, l)
    : (null == (n = null == r ? void 0 : r.toString) ? void 0 : n.call(r)) || ''
}
function Gl(e, t) {
  return e.reduce((e, t) => ((e[t] = t), e), t)
}
function Ul(e, t, l) {
  const n = F(),
    o = T(''),
    r = T(!1),
    a = T(),
    s = T(),
    i = j('table')
  ;(Ce(() => {
    ;((a.value = e.align ? `is-${e.align}` : null), a.value)
  }),
    Ce(() => {
      ;((s.value = e.headerAlign ? `is-${e.headerAlign}` : a.value), s.value)
    }))
  const u = B(() => {
      let e = n.vnode.vParent || n.parent
      for (; e && !e.tableId && !e.columnId; ) e = e.vnode.vParent || e.parent
      return e
    }),
    d = B(() => {
      const { store: e } = n.parent
      if (!e) return !1
      const { treeData: t } = e.states,
        l = t.value
      return l && Object.keys(l).length > 0
    }),
    c = T(Zt(e.width)),
    h = T(Jt(e.minWidth))
  return {
    columnId: o,
    realAlign: a,
    isSubColumn: r,
    realHeaderAlign: s,
    columnOrTableParent: u,
    setColumnWidth: (e) => (
      c.value && (e.width = c.value),
      h.value && (e.minWidth = h.value),
      !c.value && h.value && (e.width = void 0),
      e.minWidth || (e.minWidth = 80),
      (e.realWidth = Number(void 0 === e.width ? e.minWidth : e.width)),
      e
    ),
    setColumnForcedProps: (e) => {
      const t = e.type,
        l = ql[t] || {}
      Object.keys(l).forEach((t) => {
        const n = l[t]
        'className' !== t && void 0 !== n && (e[t] = n)
      })
      const n = ((e) => _l[e] || '')(t)
      if (n) {
        const t = `${$(i.namespace)}-${n}`
        e.className = e.className ? `${e.className} ${t}` : t
      }
      return e
    },
    setColumnRenders: (o) => {
      e.renderHeader ||
        ('selection' !== o.type &&
          (o.renderHeader = (e) => {
            n.columnConfig.value.label
            const l = t.header
            return l ? l(e) : o.label
          }))
      let r = o.renderCell
      return (
        'expand' === o.type
          ? ((o.renderCell = (e) => we('div', { class: 'cell' }, [r(e)])),
            (l.value.renderExpanded = (e) => (t.default ? t.default(e) : t.default)))
          : ((r = r || Xl),
            (o.renderCell = (e) => {
              let a = null
              if (t.default) {
                const l = t.default(e)
                a = l.some((e) => e.type !== $e) ? l : r(e)
              } else a = r(e)
              const { columns: s } = l.value.store.states,
                u = s.value.findIndex((e) => 'default' === e.type),
                c = (function ({ row: e, treeNode: t, store: l }, n = !1) {
                  const { ns: o } = l
                  if (!t) return n ? [we('span', { class: o.e('placeholder') })] : null
                  const r = [],
                    a = function (n) {
                      ;(n.stopPropagation(), t.loading || l.loadOrToggle(e))
                    }
                  if (
                    (t.indent &&
                      r.push(
                        we('span', {
                          class: o.e('indent'),
                          style: { 'padding-left': `${t.indent}px` }
                        })
                      ),
                    'boolean' != typeof t.expanded || t.noLazyChildren)
                  )
                    r.push(we('span', { class: o.e('placeholder') }))
                  else {
                    const e = [
                      o.e('expand-icon'),
                      t.expanded ? o.em('expand-icon', 'expanded') : ''
                    ]
                    let l = Fe
                    ;(t.loading && (l = Te),
                      r.push(
                        we(
                          'div',
                          { class: e, onClick: a },
                          {
                            default: () => [
                              we(
                                q,
                                { class: { [o.is('loading')]: t.loading } },
                                { default: () => [we(l)] }
                              )
                            ]
                          }
                        )
                      ))
                  }
                  return r
                })(e, d.value && e.cellIndex === u),
                h = { class: 'cell', style: {} }
              return (
                o.showOverflowTooltip &&
                  ((h.class = `${h.class} ${$(i.namespace)}-tooltip`),
                  (h.style = { width: (e.column.realWidth || Number(e.column.width)) - 1 + 'px' })),
                ((e) => {
                  function t(e) {
                    var t
                    'ElTableColumn' ===
                      (null == (t = null == e ? void 0 : e.type) ? void 0 : t.name) &&
                      (e.vParent = n)
                  }
                  Array.isArray(e) ? e.forEach((e) => t(e)) : t(e)
                })(a),
                we('div', h, [c, a])
              )
            })),
        o
      )
    },
    getPropsData: (...t) =>
      t.reduce(
        (t, l) => (
          Array.isArray(l) &&
            l.forEach((l) => {
              t[l] = e[l]
            }),
          t
        ),
        {}
      ),
    getColumnElIndex: (e, t) => Array.prototype.indexOf.call(e, t),
    updateColumnOrder: () => {
      l.value.store.commit('updateColumnOrder', n.columnConfig.value)
    }
  }
}
var Ql = {
  type: { type: String, default: 'default' },
  label: String,
  className: String,
  labelClassName: String,
  property: String,
  prop: String,
  width: { type: [String, Number], default: '' },
  minWidth: { type: [String, Number], default: '' },
  renderHeader: Function,
  sortable: { type: [Boolean, String], default: !1 },
  sortMethod: Function,
  sortBy: [String, Function, Array],
  resizable: { type: Boolean, default: !0 },
  columnKey: String,
  align: String,
  headerAlign: String,
  showOverflowTooltip: { type: [Boolean, Object], default: void 0 },
  fixed: [Boolean, String],
  formatter: Function,
  selectable: Function,
  reserveSelection: Boolean,
  filterMethod: Function,
  filteredValue: Array,
  filters: Array,
  filterPlacement: String,
  filterMultiple: { type: Boolean, default: !0 },
  index: [Number, Function],
  sortOrders: {
    type: Array,
    default: () => ['ascending', 'descending', null],
    validator: (e) => e.every((e) => ['ascending', 'descending', null].includes(e))
  }
}
let Zl = 1
var Jl = _({
  name: 'ElTableColumn',
  components: { ElCheckbox: qe },
  props: Ql,
  setup(e, { slots: t }) {
    const l = F(),
      n = T({}),
      o = B(() => {
        let e = l.parent
        for (; e && !e.tableId; ) e = e.parent
        return e
      }),
      { registerNormalWatchers: r, registerComplexWatchers: a } = (function (e, t) {
        const l = F()
        return {
          registerComplexWatchers: () => {
            const n = { realWidth: 'width', realMinWidth: 'minWidth' },
              o = Gl(['fixed'], n)
            Object.keys(o).forEach((o) => {
              const r = n[o]
              L(t, r) &&
                I(
                  () => t[r],
                  (t) => {
                    let n = t
                    ;('width' === r && 'realWidth' === o && (n = Zt(t)),
                      'minWidth' === r && 'realMinWidth' === o && (n = Jt(t)),
                      (l.columnConfig.value[r] = n),
                      (l.columnConfig.value[o] = n))
                    const a = 'fixed' === r
                    e.value.store.scheduleLayout(a)
                  }
                )
            })
          },
          registerNormalWatchers: () => {
            const e = { property: 'prop', align: 'realAlign', headerAlign: 'realHeaderAlign' },
              n = Gl(
                [
                  'label',
                  'filters',
                  'filterMultiple',
                  'filteredValue',
                  'sortable',
                  'index',
                  'formatter',
                  'className',
                  'labelClassName',
                  'showOverflowTooltip'
                ],
                e
              )
            Object.keys(n).forEach((n) => {
              const o = e[n]
              L(t, o) &&
                I(
                  () => t[o],
                  (e) => {
                    l.columnConfig.value[n] = e
                  }
                )
            })
          }
        }
      })(o, e),
      {
        columnId: s,
        isSubColumn: i,
        realHeaderAlign: u,
        columnOrTableParent: d,
        setColumnWidth: c,
        setColumnForcedProps: h,
        setColumnRenders: p,
        getPropsData: f,
        getColumnElIndex: v,
        realAlign: m,
        updateColumnOrder: g
      } = Ul(e, t, o),
      y = d.value
    ;((s.value = `${y.tableId || y.columnId}_column_${Zl++}`),
      ce(() => {
        i.value = o.value !== y
        const t = e.type || 'default',
          d = '' === e.sortable || e.sortable,
          v = Be(e.showOverflowTooltip) ? y.props.showOverflowTooltip : e.showOverflowTooltip,
          g = {
            ...Yl[t],
            id: s.value,
            type: t,
            property: e.prop || e.property,
            align: m,
            headerAlign: u,
            showOverflowTooltip: v,
            filterable: e.filters || e.filterMethod,
            filteredValue: [],
            filterPlacement: '',
            isColumnGroup: !1,
            isSubColumn: !1,
            filterOpened: !1,
            sortable: d,
            index: e.index,
            rawColumnKey: l.vnode.key
          }
        let b = f(
          [
            'columnKey',
            'label',
            'className',
            'labelClassName',
            'type',
            'renderHeader',
            'formatter',
            'fixed',
            'resizable'
          ],
          ['sortMethod', 'sortBy', 'sortOrders'],
          ['selectable', 'reserveSelection'],
          [
            'filterMethod',
            'filters',
            'filterMultiple',
            'filterOpened',
            'filteredValue',
            'filterPlacement'
          ]
        )
        b = (function (e, t) {
          const l = {}
          let n
          for (n in e) l[n] = e[n]
          for (n in t)
            if (L(t, n)) {
              const e = t[n]
              void 0 !== e && (l[n] = e)
            }
          return l
        })(g, b)
        ;((b = (function (...e) {
          return 0 === e.length
            ? (e) => e
            : 1 === e.length
              ? e[0]
              : e.reduce(
                  (e, t) =>
                    (...l) =>
                      e(t(...l))
                )
        })(
          p,
          c,
          h
        )(b)),
          (n.value = b),
          r(),
          a())
      }),
      he(() => {
        var e
        const t = d.value,
          r = i.value
            ? t.vnode.el.children
            : null == (e = t.refs.hiddenColumns)
              ? void 0
              : e.children,
          a = () => v(r || [], l.vnode.el)
        n.value.getColumnIndex = a
        a() > -1 &&
          o.value.store.commit('insertColumn', n.value, i.value ? t.columnConfig.value : null, g)
      }),
      Ie(() => {
        o.value.store.commit('removeColumn', n.value, i.value ? y.columnConfig.value : null, g)
      }),
      (l.columnId = s.value),
      (l.columnConfig = n))
  },
  render() {
    var e, t, l
    try {
      const n =
          null == (t = (e = this.$slots).default)
            ? void 0
            : t.call(e, { row: {}, column: {}, $index: -1 }),
        o = []
      if (Array.isArray(n))
        for (const e of n)
          'ElTableColumn' === (null == (l = e.type) ? void 0 : l.name) || 2 & e.shapeFlag
            ? o.push(e)
            : e.type === ae &&
              Array.isArray(e.children) &&
              e.children.forEach((e) => {
                1024 === (null == e ? void 0 : e.patchFlag) ||
                  Ke(null == e ? void 0 : e.children) ||
                  o.push(e)
              })
      return we('div', o)
    } catch (n) {
      return we('div', [])
    }
  }
})
const en = je(Vl, { TableColumn: Jl }),
  tn = ze(Jl)
export { tn as E, en as a }
