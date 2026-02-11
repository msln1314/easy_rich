import {
  _ as t,
  aK as e,
  S as n,
  X as o,
  aL as a,
  U as i,
  j as r,
  a2 as s,
  aM as l,
  aN as u,
  b as d,
  u as h,
  aO as p,
  aP as c,
  aQ as f,
  aR as g,
  aS as v,
  h as y,
  a8 as m,
  g as x,
  aT as _,
  s as M,
  K as w,
  a4 as b,
  ac as S,
  aU as I,
  aV as A,
  aW as C,
  aX as T,
  a3 as D,
  aY as L,
  aZ as P,
  a5 as k,
  aD as R,
  a_ as z,
  aJ as O,
  a$ as E,
  aa as V,
  w as Z,
  b0 as N,
  b1 as B,
  b2 as F,
  am as G,
  aj as W,
  b3 as H,
  b4 as U,
  b5 as Y,
  c as X,
  a6 as j,
  b6 as q,
  b7 as K,
  b8 as $,
  b9 as Q,
  ba as J,
  bb as tt,
  bc as et,
  bd as nt,
  be as ot,
  aB as at,
  i as it,
  k as rt,
  bf as st,
  e as lt,
  bg as ut,
  q as dt,
  bh as ht,
  N as pt,
  z as ct,
  x as ft,
  I as gt,
  J as vt,
  bi as yt,
  bj as mt,
  bk as xt,
  P as _t,
  bl as Mt,
  d as wt,
  bm as bt,
  bn as St,
  bo as It,
  bp as At,
  r as Ct,
  bq as Tt,
  br as Dt,
  bs as Lt,
  bt as Pt,
  bu as kt,
  al as Rt,
  bv as zt,
  bw as Ot,
  y as Et,
  p as Vt,
  an as Zt,
  Y as Nt,
  $ as Bt,
  a0 as Ft,
  bx as Gt,
  by as Wt,
  T as Ht,
  bz as Ut,
  bA as Yt,
  af as Xt,
  t as jt,
  bB as qt,
  v as Kt,
  bC as $t,
  E as Qt,
  bD as Jt,
  aF as te,
  ad as ee,
  bE as ne,
  H as oe,
  bF as ae,
  bG as ie,
  bH as re,
  bI as se,
  bJ as le,
  bK as ue,
  bL as de,
  bM as he,
  bN as pe,
  bO as ce,
  bP as fe,
  bQ as ge,
  bR as ve,
  o as ye,
  bS as me,
  bT as xe,
  bU as _e,
  bV as Me,
  bW as we,
  bX as be,
  bY as Se,
  bZ as Ie,
  b_ as Ae,
  b$ as Ce,
  az as Te,
  aA as De,
  c0 as Le,
  aC as Pe,
  aE as ke,
  c1 as Re,
  c2 as ze,
  C as Oe,
  ay as Ee,
  ap as Ve,
  aq as Ze,
  ar as Ne,
  c3 as Be,
  ao as Fe,
  as as Ge,
  l as We,
  at as He,
  au as Ue,
  av as Ye,
  ax as Xe,
  c4 as je,
  aw as qe
} from './echarts-ef988edf.js'
import {
  e as Ke,
  f as $e,
  r as Qe,
  w as Je,
  B as tn,
  dV as en,
  a2 as nn,
  as as on,
  d6 as an,
  aj as rn,
  o as sn,
  j as ln,
  n as un,
  bp as dn,
  dW as hn
} from './index-820a519e.js'
const pn = (function (n) {
  function o() {
    var t = (null !== n && n.apply(this, arguments)) || this
    return ((t.type = o.type), (t.hasSymbolVisual = !0), t)
  }
  return (
    t(o, n),
    (o.prototype.getInitialData = function (t, n) {
      return e(null, this, { useEncodeDefaulter: !0 })
    }),
    (o.prototype.getProgressive = function () {
      var t = this.option.progressive
      return null == t ? (this.option.large ? 5e3 : this.get('progressive')) : t
    }),
    (o.prototype.getProgressiveThreshold = function () {
      var t = this.option.progressiveThreshold
      return null == t ? (this.option.large ? 1e4 : this.get('progressiveThreshold')) : t
    }),
    (o.prototype.brushSelector = function (t, e, n) {
      return n.point(e.getItemLayout(t))
    }),
    (o.prototype.getZLevelKey = function () {
      return this.getData().count() > this.getProgressiveThreshold() ? this.id : ''
    }),
    (o.type = 'series.scatter'),
    (o.dependencies = ['grid', 'polar', 'geo', 'singleAxis', 'calendar']),
    (o.defaultOption = {
      coordinateSystem: 'cartesian2d',
      z: 2,
      legendHoverLink: !0,
      symbolSize: 10,
      large: !1,
      largeThreshold: 2e3,
      itemStyle: { opacity: 0.8 },
      emphasis: { scale: !0 },
      clip: !0,
      select: { itemStyle: { borderColor: '#212121' } },
      universalTransition: { divideShape: 'clone' }
    }),
    o
  )
})(n)
var cn = function () {},
  fn = (function (e) {
    function n(t) {
      var n = e.call(this, t) || this
      return ((n._off = 0), (n.hoverDataIdx = -1), n)
    }
    return (
      t(n, e),
      (n.prototype.getDefaultShape = function () {
        return new cn()
      }),
      (n.prototype.reset = function () {
        ;((this.notClear = !1), (this._off = 0))
      }),
      (n.prototype.buildPath = function (t, e) {
        var n,
          o = e.points,
          a = e.size,
          i = this.symbolProxy,
          r = i.shape,
          s = t.getContext ? t.getContext() : t,
          l = s && a[0] < 4,
          u = this.softClipShape
        if (l) this._ctx = s
        else {
          for (this._ctx = null, n = this._off; n < o.length; ) {
            var d = o[n++],
              h = o[n++]
            isNaN(d) ||
              isNaN(h) ||
              (u && !u.contain(d, h)) ||
              ((r.x = d - a[0] / 2),
              (r.y = h - a[1] / 2),
              (r.width = a[0]),
              (r.height = a[1]),
              i.buildPath(t, r, !0))
          }
          this.incremental && ((this._off = n), (this.notClear = !0))
        }
      }),
      (n.prototype.afterBrush = function () {
        var t,
          e = this.shape,
          n = e.points,
          o = e.size,
          a = this._ctx,
          i = this.softClipShape
        if (a) {
          for (t = this._off; t < n.length; ) {
            var r = n[t++],
              s = n[t++]
            isNaN(r) ||
              isNaN(s) ||
              (i && !i.contain(r, s)) ||
              a.fillRect(r - o[0] / 2, s - o[1] / 2, o[0], o[1])
          }
          this.incremental && ((this._off = t), (this.notClear = !0))
        }
      }),
      (n.prototype.findDataIndex = function (t, e) {
        for (
          var n = this.shape,
            o = n.points,
            a = n.size,
            i = Math.max(a[0], 4),
            r = Math.max(a[1], 4),
            s = o.length / 2 - 1;
          s >= 0;
          s--
        ) {
          var l = 2 * s,
            u = o[l] - i / 2,
            d = o[l + 1] - r / 2
          if (t >= u && e >= d && t <= u + i && e <= d + r) return s
        }
        return -1
      }),
      (n.prototype.contain = function (t, e) {
        var n = this.transformCoordToLocal(t, e),
          o = this.getBoundingRect()
        return (
          (t = n[0]),
          (e = n[1]),
          o.contain(t, e)
            ? (this.hoverDataIdx = this.findDataIndex(t, e)) >= 0
            : ((this.hoverDataIdx = -1), !1)
        )
      }),
      (n.prototype.getBoundingRect = function () {
        var t = this._rect
        if (!t) {
          for (
            var e = this.shape,
              n = e.points,
              a = e.size,
              i = a[0],
              r = a[1],
              s = 1 / 0,
              l = 1 / 0,
              u = -1 / 0,
              d = -1 / 0,
              h = 0;
            h < n.length;
          ) {
            var p = n[h++],
              c = n[h++]
            ;((s = Math.min(p, s)),
              (u = Math.max(p, u)),
              (l = Math.min(c, l)),
              (d = Math.max(c, d)))
          }
          t = this._rect = new o(s - i / 2, l - r / 2, u - s + i, d - l + r)
        }
        return t
      }),
      n
    )
  })(a)
const gn = (function () {
  function t() {
    this.group = new i()
  }
  return (
    (t.prototype.updateData = function (t, e) {
      this._clear()
      var n = this._create()
      ;(n.setShape({ points: t.getLayout('points') }), this._setCommon(n, t, e))
    }),
    (t.prototype.updateLayout = function (t) {
      var e = t.getLayout('points')
      this.group.eachChild(function (t) {
        if (null != t.startIndex) {
          var n = 2 * (t.endIndex - t.startIndex),
            o = 4 * t.startIndex * 2
          e = new Float32Array(e.buffer, o, n)
        }
        ;(t.setShape('points', e), t.reset())
      })
    }),
    (t.prototype.incrementalPrepareUpdate = function (t) {
      this._clear()
    }),
    (t.prototype.incrementalUpdate = function (t, e, n) {
      var o = this._newAdded[0],
        a = e.getLayout('points'),
        i = o && o.shape.points
      if (i && i.length < 2e4) {
        var r = i.length,
          s = new Float32Array(r + a.length)
        ;(s.set(i), s.set(a, r), (o.endIndex = t.end), o.setShape({ points: s }))
      } else {
        this._newAdded = []
        var l = this._create()
        ;((l.startIndex = t.start),
          (l.endIndex = t.end),
          (l.incremental = !0),
          l.setShape({ points: a }),
          this._setCommon(l, e, n))
      }
    }),
    (t.prototype.eachRendered = function (t) {
      this._newAdded[0] && t(this._newAdded[0])
    }),
    (t.prototype._create = function () {
      var t = new fn({ cursor: 'default' })
      return ((t.ignoreCoarsePointer = !0), this.group.add(t), this._newAdded.push(t), t)
    }),
    (t.prototype._setCommon = function (t, e, n) {
      var o = e.hostModel
      n = n || {}
      var a = e.getVisual('symbolSize')
      ;(t.setShape('size', a instanceof Array ? a : [a, a]),
        (t.softClipShape = n.clipShape || null),
        (t.symbolProxy = r(e.getVisual('symbol'), 0, 0, 0, 0)),
        (t.setColor = t.symbolProxy.setColor))
      var i = t.shape.size[0] < 4
      t.useStyle(
        o.getModel('itemStyle').getItemStyle(i ? ['color', 'shadowBlur', 'shadowColor'] : ['color'])
      )
      var l = e.getVisual('style'),
        u = l && l.fill
      u && t.setColor(u)
      var d = s(t)
      ;((d.seriesIndex = o.seriesIndex),
        t.on('mousemove', function (e) {
          d.dataIndex = null
          var n = t.hoverDataIdx
          n >= 0 && (d.dataIndex = n + (t.startIndex || 0))
        }))
    }),
    (t.prototype.remove = function () {
      this._clear()
    }),
    (t.prototype._clear = function () {
      ;((this._newAdded = []), this.group.removeAll())
    }),
    t
  )
})()
const vn = (function (e) {
  function n() {
    var t = (null !== e && e.apply(this, arguments)) || this
    return ((t.type = n.type), t)
  }
  return (
    t(n, e),
    (n.prototype.render = function (t, e, n) {
      var o = t.getData()
      ;(this._updateSymbolDraw(o, t).updateData(o, { clipShape: this._getClipShape(t) }),
        (this._finished = !0))
    }),
    (n.prototype.incrementalPrepareRender = function (t, e, n) {
      var o = t.getData()
      ;(this._updateSymbolDraw(o, t).incrementalPrepareUpdate(o), (this._finished = !1))
    }),
    (n.prototype.incrementalRender = function (t, e, n) {
      ;(this._symbolDraw.incrementalUpdate(t, e.getData(), { clipShape: this._getClipShape(e) }),
        (this._finished = t.end === e.getData().count()))
    }),
    (n.prototype.updateTransform = function (t, e, n) {
      var o = t.getData()
      if ((this.group.dirty(), !this._finished || o.count() > 1e4)) return { update: !0 }
      var a = l('').reset(t, e, n)
      ;(a.progress && a.progress({ start: 0, end: o.count(), count: o.count() }, o),
        this._symbolDraw.updateLayout(o))
    }),
    (n.prototype.eachRendered = function (t) {
      this._symbolDraw && this._symbolDraw.eachRendered(t)
    }),
    (n.prototype._getClipShape = function (t) {
      var e = t.coordinateSystem,
        n = e && e.getArea && e.getArea()
      return t.get('clip', !0) ? n : null
    }),
    (n.prototype._updateSymbolDraw = function (t, e) {
      var n = this._symbolDraw,
        o = e.pipelineContext.large
      return (
        (n && o === this._isLargeDraw) ||
          (n && n.remove(),
          (n = this._symbolDraw = o ? new gn() : new u()),
          (this._isLargeDraw = o),
          this.group.removeAll()),
        this.group.add(n.group),
        n
      )
    }),
    (n.prototype.remove = function (t, e) {
      ;(this._symbolDraw && this._symbolDraw.remove(!0), (this._symbolDraw = null))
    }),
    (n.prototype.dispose = function () {}),
    (n.type = 'scatter'),
    n
  )
})(d)
var yn = c.prototype,
  mn = f.prototype,
  xn = function () {
    ;((this.x1 = 0), (this.y1 = 0), (this.x2 = 0), (this.y2 = 0), (this.percent = 1))
  }
function _n(t) {
  return isNaN(+t.cpx1) || isNaN(+t.cpy1)
}
!(function (e) {
  function n() {
    return (null !== e && e.apply(this, arguments)) || this
  }
  t(n, e)
})(xn)
const Mn = (function (e) {
  function n(t) {
    var n = e.call(this, t) || this
    return ((n.type = 'ec-line'), n)
  }
  return (
    t(n, e),
    (n.prototype.getDefaultStyle = function () {
      return { stroke: '#000', fill: null }
    }),
    (n.prototype.getDefaultShape = function () {
      return new xn()
    }),
    (n.prototype.buildPath = function (t, e) {
      _n(e) ? yn.buildPath.call(this, t, e) : mn.buildPath.call(this, t, e)
    }),
    (n.prototype.pointAt = function (t) {
      return _n(this.shape) ? yn.pointAt.call(this, t) : mn.pointAt.call(this, t)
    }),
    (n.prototype.tangentAt = function (t) {
      var e = this.shape,
        n = _n(e) ? [e.x2 - e.x1, e.y2 - e.y1] : mn.tangentAt.call(this, t)
      return g(n, n)
    }),
    n
  )
})(a)
var wn = ['fromSymbol', 'toSymbol']
function bn(t) {
  return '_' + t + 'Type'
}
function Sn(t, e, n) {
  var o = e.getItemVisual(n, t)
  if (!o || 'none' === o) return o
  var a = e.getItemVisual(n, t + 'Size'),
    i = e.getItemVisual(n, t + 'Rotate'),
    r = e.getItemVisual(n, t + 'Offset'),
    s = e.getItemVisual(n, t + 'KeepAspect'),
    l = T(a)
  return o + l + D(r || 0, l) + (i || '') + (s || '')
}
function In(t, e, n) {
  var o = e.getItemVisual(n, t)
  if (o && 'none' !== o) {
    var a = e.getItemVisual(n, t + 'Size'),
      i = e.getItemVisual(n, t + 'Rotate'),
      s = e.getItemVisual(n, t + 'Offset'),
      l = e.getItemVisual(n, t + 'KeepAspect'),
      u = T(a),
      d = D(s || 0, u),
      h = r(o, -u[0] / 2 + d[0], -u[1] / 2 + d[1], u[0], u[1], null, l)
    return (
      (h.__specifiedRotation = null == i || isNaN(i) ? void 0 : (+i * Math.PI) / 180 || 0),
      (h.name = t),
      h
    )
  }
}
function An(t, e) {
  ;((t.x1 = e[0][0]), (t.y1 = e[0][1]), (t.x2 = e[1][0]), (t.y2 = e[1][1]), (t.percent = 1))
  var n = e[2]
  n ? ((t.cpx1 = n[0]), (t.cpy1 = n[1])) : ((t.cpx1 = NaN), (t.cpy1 = NaN))
}
const Cn = (function (e) {
  function n(t, n, o) {
    var a = e.call(this) || this
    return (a._createLine(t, n, o), a)
  }
  return (
    t(n, e),
    (n.prototype._createLine = function (t, e, n) {
      var o = t.hostModel,
        a = (function (t) {
          var e = new Mn({ name: 'line', subPixelOptimize: !0 })
          return (An(e.shape, t), e)
        })(t.getItemLayout(e))
      ;((a.shape.percent = 0),
        v(a, { shape: { percent: 1 } }, o, e),
        this.add(a),
        y(
          wn,
          function (n) {
            var o = In(n, t, e)
            ;(this.add(o), (this[bn(n)] = Sn(n, t, e)))
          },
          this
        ),
        this._updateCommonStl(t, e, n))
    }),
    (n.prototype.updateData = function (t, e, n) {
      var o = t.hostModel,
        a = this.childOfName('line'),
        i = t.getItemLayout(e),
        r = { shape: {} }
      ;(An(r.shape, i),
        m(a, r, o, e),
        y(
          wn,
          function (n) {
            var o = Sn(n, t, e),
              a = bn(n)
            if (this[a] !== o) {
              this.remove(this.childOfName(n))
              var i = In(n, t, e)
              this.add(i)
            }
            this[a] = o
          },
          this
        ),
        this._updateCommonStl(t, e, n))
    }),
    (n.prototype.getLinePath = function () {
      return this.childAt(0)
    }),
    (n.prototype._updateCommonStl = function (t, e, n) {
      var o = t.hostModel,
        a = this.childOfName('line'),
        i = n && n.emphasisLineStyle,
        r = n && n.blurLineStyle,
        s = n && n.selectLineStyle,
        l = n && n.labelStatesModels,
        u = n && n.emphasisDisabled,
        d = n && n.focus,
        h = n && n.blurScope
      if (!n || t.hasItemOption) {
        var p = t.getItemModel(e),
          c = p.getModel('emphasis')
        ;((i = c.getModel('lineStyle').getLineStyle()),
          (r = p.getModel(['blur', 'lineStyle']).getLineStyle()),
          (s = p.getModel(['select', 'lineStyle']).getLineStyle()),
          (u = c.get('disabled')),
          (d = c.get('focus')),
          (h = c.get('blurScope')),
          (l = x(p)))
      }
      var f = t.getItemVisual(e, 'style'),
        g = f.stroke
      ;(a.useStyle(f),
        (a.style.fill = null),
        (a.style.strokeNoScale = !0),
        (a.ensureState('emphasis').style = i),
        (a.ensureState('blur').style = r),
        (a.ensureState('select').style = s),
        y(
          wn,
          function (t) {
            var e = this.childOfName(t)
            if (e) {
              ;(e.setColor(g), (e.style.opacity = f.opacity))
              for (var n = 0; n < _.length; n++) {
                var o = _[n],
                  i = a.getState(o)
                if (i) {
                  var r = i.style || {},
                    s = e.ensureState(o),
                    l = s.style || (s.style = {})
                  ;(null != r.stroke && (l[e.__isEmptyBrush ? 'stroke' : 'fill'] = r.stroke),
                    null != r.opacity && (l.opacity = r.opacity))
                }
              }
              e.markRedraw()
            }
          },
          this
        ))
      var v = o.getRawValue(e)
      M(this, l, {
        labelDataIndex: e,
        labelFetcher: {
          getFormattedLabel: function (e, n) {
            return o.getFormattedLabel(e, n, t.dataType)
          }
        },
        inheritColor: g || '#000',
        defaultOpacity: f.opacity,
        defaultText: (null == v ? t.getName(e) : isFinite(v) ? w(v) : v) + ''
      })
      var m = this.getTextContent()
      if (m) {
        var I = l.normal
        ;((m.__align = m.style.align),
          (m.__verticalAlign = m.style.verticalAlign),
          (m.__position = I.get('position') || 'middle'))
        var A = I.get('distance')
        ;(b(A) || (A = [A, A]), (m.__labelDistance = A))
      }
      ;(this.setTextConfig({ position: null, local: !0, inside: !1 }), S(this, d, h, u))
    }),
    (n.prototype.highlight = function () {
      I(this)
    }),
    (n.prototype.downplay = function () {
      A(this)
    }),
    (n.prototype.updateLayout = function (t, e) {
      this.setLinePoints(t.getItemLayout(e))
    }),
    (n.prototype.setLinePoints = function (t) {
      var e = this.childOfName('line')
      ;(An(e.shape, t), e.dirty())
    }),
    (n.prototype.beforeUpdate = function () {
      var t = this,
        e = t.childOfName('fromSymbol'),
        n = t.childOfName('toSymbol'),
        o = t.getTextContent()
      if (e || n || (o && !o.ignore)) {
        for (var a = 1, i = this.parent; i; ) (i.scaleX && (a /= i.scaleX), (i = i.parent))
        var r = t.childOfName('line')
        if (this.__dirty || r.__dirty) {
          var s = r.shape.percent,
            l = r.pointAt(0),
            u = r.pointAt(s),
            d = C([], u, l)
          if (
            (g(d, d),
            e && (e.setPosition(l), S(e, 0), (e.scaleX = e.scaleY = a * s), e.markRedraw()),
            n && (n.setPosition(u), S(n, 1), (n.scaleX = n.scaleY = a * s), n.markRedraw()),
            o && !o.ignore)
          ) {
            ;((o.x = o.y = 0), (o.originX = o.originY = 0))
            var h = void 0,
              p = void 0,
              c = o.__labelDistance,
              f = c[0] * a,
              v = c[1] * a,
              y = s / 2,
              m = r.tangentAt(y),
              x = [m[1], -m[0]],
              _ = r.pointAt(y)
            x[1] > 0 && ((x[0] = -x[0]), (x[1] = -x[1]))
            var M = m[0] < 0 ? -1 : 1
            if ('start' !== o.__position && 'end' !== o.__position) {
              var w = -Math.atan2(m[1], m[0])
              ;(u[0] < l[0] && (w = Math.PI + w), (o.rotation = w))
            }
            var b = void 0
            switch (o.__position) {
              case 'insideStartTop':
              case 'insideMiddleTop':
              case 'insideEndTop':
              case 'middle':
                ;((b = -v), (p = 'bottom'))
                break
              case 'insideStartBottom':
              case 'insideMiddleBottom':
              case 'insideEndBottom':
                ;((b = v), (p = 'top'))
                break
              default:
                ;((b = 0), (p = 'middle'))
            }
            switch (o.__position) {
              case 'end':
                ;((o.x = d[0] * f + u[0]),
                  (o.y = d[1] * v + u[1]),
                  (h = d[0] > 0.8 ? 'left' : d[0] < -0.8 ? 'right' : 'center'),
                  (p = d[1] > 0.8 ? 'top' : d[1] < -0.8 ? 'bottom' : 'middle'))
                break
              case 'start':
                ;((o.x = -d[0] * f + l[0]),
                  (o.y = -d[1] * v + l[1]),
                  (h = d[0] > 0.8 ? 'right' : d[0] < -0.8 ? 'left' : 'center'),
                  (p = d[1] > 0.8 ? 'bottom' : d[1] < -0.8 ? 'top' : 'middle'))
                break
              case 'insideStartTop':
              case 'insideStart':
              case 'insideStartBottom':
                ;((o.x = f * M + l[0]),
                  (o.y = l[1] + b),
                  (h = m[0] < 0 ? 'right' : 'left'),
                  (o.originX = -f * M),
                  (o.originY = -b))
                break
              case 'insideMiddleTop':
              case 'insideMiddle':
              case 'insideMiddleBottom':
              case 'middle':
                ;((o.x = _[0]), (o.y = _[1] + b), (h = 'center'), (o.originY = -b))
                break
              case 'insideEndTop':
              case 'insideEnd':
              case 'insideEndBottom':
                ;((o.x = -f * M + u[0]),
                  (o.y = u[1] + b),
                  (h = m[0] >= 0 ? 'right' : 'left'),
                  (o.originX = f * M),
                  (o.originY = -b))
            }
            ;((o.scaleX = o.scaleY = a),
              o.setStyle({ verticalAlign: o.__verticalAlign || p, align: o.__align || h }))
          }
        }
      }
      function S(t, e) {
        var n = t.__specifiedRotation
        if (null == n) {
          var o = r.tangentAt(e)
          t.attr('rotation', ((1 === e ? -1 : 1) * Math.PI) / 2 - Math.atan2(o[1], o[0]))
        } else t.attr('rotation', n)
      }
    }),
    n
  )
})(i)
function Tn(t) {
  var e = t.hostModel,
    n = e.getModel('emphasis')
  return {
    lineStyle: e.getModel('lineStyle').getLineStyle(),
    emphasisLineStyle: n.getModel(['lineStyle']).getLineStyle(),
    blurLineStyle: e.getModel(['blur', 'lineStyle']).getLineStyle(),
    selectLineStyle: e.getModel(['select', 'lineStyle']).getLineStyle(),
    emphasisDisabled: n.get('disabled'),
    blurScope: n.get('blurScope'),
    focus: n.get('focus'),
    labelStatesModels: x(e)
  }
}
function Dn(t) {
  return isNaN(t[0]) || isNaN(t[1])
}
function Ln(t) {
  return t && !Dn(t[0]) && !Dn(t[1])
}
const Pn = (function () {
  function t(t) {
    ;((this.group = new i()), (this._LineCtor = t || Cn))
  }
  return (
    (t.prototype.updateData = function (t) {
      var e = this
      this._progressiveEls = null
      var n = this,
        o = n.group,
        a = n._lineData
      ;((n._lineData = t), a || o.removeAll())
      var i = Tn(t)
      t.diff(a)
        .add(function (n) {
          e._doAdd(t, n, i)
        })
        .update(function (n, o) {
          e._doUpdate(a, t, o, n, i)
        })
        .remove(function (t) {
          o.remove(a.getItemGraphicEl(t))
        })
        .execute()
    }),
    (t.prototype.updateLayout = function () {
      var t = this._lineData
      t &&
        t.eachItemGraphicEl(function (e, n) {
          e.updateLayout(t, n)
        }, this)
    }),
    (t.prototype.incrementalPrepareUpdate = function (t) {
      ;((this._seriesScope = Tn(t)), (this._lineData = null), this.group.removeAll())
    }),
    (t.prototype.incrementalUpdate = function (t, e) {
      function n(t) {
        t.isGroup ||
          (function (t) {
            return t.animators && t.animators.length > 0
          })(t) ||
          ((t.incremental = !0), (t.ensureState('emphasis').hoverLayer = !0))
      }
      this._progressiveEls = []
      for (var o = t.start; o < t.end; o++) {
        if (Ln(e.getItemLayout(o))) {
          var a = new this._LineCtor(e, o, this._seriesScope)
          ;(a.traverse(n),
            this.group.add(a),
            e.setItemGraphicEl(o, a),
            this._progressiveEls.push(a))
        }
      }
    }),
    (t.prototype.remove = function () {
      this.group.removeAll()
    }),
    (t.prototype.eachRendered = function (t) {
      L(this._progressiveEls || this.group, t)
    }),
    (t.prototype._doAdd = function (t, e, n) {
      if (Ln(t.getItemLayout(e))) {
        var o = new this._LineCtor(t, e, n)
        ;(t.setItemGraphicEl(e, o), this.group.add(o))
      }
    }),
    (t.prototype._doUpdate = function (t, e, n, o, a) {
      var i = t.getItemGraphicEl(n)
      Ln(e.getItemLayout(o))
        ? (i ? i.updateData(e, o, a) : (i = new this._LineCtor(e, o, a)),
          e.setItemGraphicEl(o, i),
          this.group.add(i))
        : this.group.remove(i)
    }),
    t
  )
})()
var kn = function () {
  ;((this.angle = 0), (this.width = 10), (this.r = 10), (this.x = 0), (this.y = 0))
}
const Rn = (function (e) {
  function n(t) {
    var n = e.call(this, t) || this
    return ((n.type = 'pointer'), n)
  }
  return (
    t(n, e),
    (n.prototype.getDefaultShape = function () {
      return new kn()
    }),
    (n.prototype.buildPath = function (t, e) {
      var n = Math.cos,
        o = Math.sin,
        a = e.r,
        i = e.width,
        r = e.angle,
        s = e.x - n(r) * i * (i >= a / 3 ? 1 : 2),
        l = e.y - o(r) * i * (i >= a / 3 ? 1 : 2)
      ;((r = e.angle - Math.PI / 2),
        t.moveTo(s, l),
        t.lineTo(e.x + n(r) * i, e.y + o(r) * i),
        t.lineTo(e.x + n(e.angle) * a, e.y + o(e.angle) * a),
        t.lineTo(e.x - n(r) * i, e.y - o(r) * i),
        t.lineTo(s, l))
    }),
    n
  )
})(a)
function zn(t, e) {
  var n = null == t ? '' : t + ''
  return (e && (G(e) ? (n = e.replace('{value}', n)) : W(e) && (n = e(t))), n)
}
const On = (function (e) {
  function n() {
    var t = (null !== e && e.apply(this, arguments)) || this
    return ((t.type = n.type), t)
  }
  return (
    t(n, e),
    (n.prototype.render = function (t, e, n) {
      this.group.removeAll()
      var o = t.get(['axisLine', 'lineStyle', 'color']),
        a = (function (t, e) {
          var n = t.get('center'),
            o = e.getWidth(),
            a = e.getHeight(),
            i = Math.min(o, a)
          return {
            cx: k(n[0], e.getWidth()),
            cy: k(n[1], e.getHeight()),
            r: k(t.get('radius'), i / 2)
          }
        })(t, n)
      ;(this._renderMain(t, e, n, o, a), (this._data = t.getData()))
    }),
    (n.prototype.dispose = function () {}),
    (n.prototype._renderMain = function (t, e, n, o, a) {
      var i = this.group,
        r = t.get('clockwise'),
        s = (-t.get('startAngle') / 180) * Math.PI,
        l = (-t.get('endAngle') / 180) * Math.PI,
        u = t.getModel('axisLine'),
        d = u.get('roundCap') ? H : U,
        h = u.get('show'),
        p = u.getModel('lineStyle'),
        c = p.get('width'),
        f = [s, l]
      P(f, !r)
      for (var g = (l = f[1]) - (s = f[0]), v = s, m = [], x = 0; h && x < o.length; x++) {
        var _ = new d({
          shape: {
            startAngle: v,
            endAngle: (l = s + g * Math.min(Math.max(o[x][0], 0), 1)),
            cx: a.cx,
            cy: a.cy,
            clockwise: r,
            r0: a.r - c,
            r: a.r
          },
          silent: !0
        })
        ;(_.setStyle({ fill: o[x][1] }),
          _.setStyle(p.getLineStyle(['color', 'width'])),
          m.push(_),
          (v = l))
      }
      ;(m.reverse(),
        y(m, function (t) {
          return i.add(t)
        }))
      var M = function (t) {
        if (t <= 0) return o[0][1]
        var e
        for (e = 0; e < o.length; e++)
          if (o[e][0] >= t && (0 === e ? 0 : o[e - 1][0]) < t) return o[e][1]
        return o[e - 1][1]
      }
      ;(this._renderTicks(t, e, n, M, a, s, l, r, c),
        this._renderTitleAndDetail(t, e, n, M, a),
        this._renderAnchor(t, a),
        this._renderPointer(t, e, n, M, a, s, l, r, c))
    }),
    (n.prototype._renderTicks = function (t, e, n, o, a, i, r, s, l) {
      for (
        var u,
          d,
          h = this.group,
          p = a.cx,
          f = a.cy,
          g = a.r,
          v = +t.get('min'),
          y = +t.get('max'),
          m = t.getModel('splitLine'),
          x = t.getModel('axisTick'),
          _ = t.getModel('axisLabel'),
          M = t.get('splitNumber'),
          b = x.get('splitNumber'),
          S = k(m.get('length'), g),
          I = k(x.get('length'), g),
          A = i,
          C = (r - i) / M,
          T = C / b,
          D = m.getModel('lineStyle').getLineStyle(),
          L = x.getModel('lineStyle').getLineStyle(),
          P = m.get('distance'),
          O = 0;
        O <= M;
        O++
      ) {
        if (((u = Math.cos(A)), (d = Math.sin(A)), m.get('show'))) {
          var E = new c({
            shape: {
              x1: u * (g - (V = P ? P + l : l)) + p,
              y1: d * (g - V) + f,
              x2: u * (g - S - V) + p,
              y2: d * (g - S - V) + f
            },
            style: D,
            silent: !0
          })
          ;('auto' === D.stroke && E.setStyle({ stroke: o(O / M) }), h.add(E))
        }
        if (_.get('show')) {
          var V = _.get('distance') + P,
            Z = zn(w((O / M) * (y - v) + v), _.get('formatter')),
            N = o(O / M),
            B = u * (g - S - V) + p,
            F = d * (g - S - V) + f,
            G = _.get('rotate'),
            W = 0
          ;('radial' === G
            ? (W = -A + 2 * Math.PI) > Math.PI / 2 && (W += Math.PI)
            : 'tangential' === G
              ? (W = -A - Math.PI / 2)
              : Y(G) && (W = (G * Math.PI) / 180),
            0 === W
              ? h.add(
                  new R({
                    style: z(
                      _,
                      {
                        text: Z,
                        x: B,
                        y: F,
                        verticalAlign: d < -0.8 ? 'top' : d > 0.8 ? 'bottom' : 'middle',
                        align: u < -0.4 ? 'left' : u > 0.4 ? 'right' : 'center'
                      },
                      { inheritColor: N }
                    ),
                    silent: !0
                  })
                )
              : h.add(
                  new R({
                    style: z(
                      _,
                      { text: Z, x: B, y: F, verticalAlign: 'middle', align: 'center' },
                      { inheritColor: N }
                    ),
                    silent: !0,
                    originX: B,
                    originY: F,
                    rotation: W
                  })
                ))
        }
        if (x.get('show') && O !== M) {
          V = (V = x.get('distance')) ? V + l : l
          for (var H = 0; H <= b; H++) {
            ;((u = Math.cos(A)), (d = Math.sin(A)))
            var U = new c({
              shape: {
                x1: u * (g - V) + p,
                y1: d * (g - V) + f,
                x2: u * (g - I - V) + p,
                y2: d * (g - I - V) + f
              },
              silent: !0,
              style: L
            })
            ;('auto' === L.stroke && U.setStyle({ stroke: o((O + H / b) / M) }), h.add(U), (A += T))
          }
          A -= T
        } else A += C
      }
    }),
    (n.prototype._renderPointer = function (t, e, n, o, a, i, s, l, u) {
      var d = this.group,
        h = this._data,
        p = this._progressEls,
        c = [],
        f = t.get(['pointer', 'show']),
        g = t.getModel('progress'),
        y = g.get('show'),
        x = t.getData(),
        _ = x.mapDimension('value'),
        M = +t.get('min'),
        w = +t.get('max'),
        b = [M, w],
        I = [i, s]
      function A(e, n) {
        var o,
          i = x.getItemModel(e).getModel('pointer'),
          s = k(i.get('width'), a.r),
          l = k(i.get('length'), a.r),
          u = t.get(['pointer', 'icon']),
          d = i.get('offsetCenter'),
          h = k(d[0], a.r),
          p = k(d[1], a.r),
          c = i.get('keepAspect')
        return (
          ((o = u
            ? r(u, h - s / 2, p - l, s, l, null, c)
            : new Rn({ shape: { angle: -Math.PI / 2, width: s, r: l, x: h, y: p } })).rotation = -(
            n +
            Math.PI / 2
          )),
          (o.x = a.cx),
          (o.y = a.cy),
          o
        )
      }
      function C(t, e) {
        var n = g.get('roundCap') ? H : U,
          o = g.get('overlap'),
          r = o ? g.get('width') : u / x.count(),
          s = o ? a.r - r : a.r - (t + 1) * r,
          d = o ? a.r : a.r - t * r,
          h = new n({
            shape: { startAngle: i, endAngle: e, cx: a.cx, cy: a.cy, clockwise: l, r0: s, r: d }
          })
        return (o && (h.z2 = w - (x.get(_, t) % w)), h)
      }
      ;(y || f) &&
        (x
          .diff(h)
          .add(function (e) {
            var n = x.get(_, e)
            if (f) {
              var o = A(e, i)
              ;(v(o, { rotation: -((isNaN(+n) ? I[0] : O(n, b, I, !0)) + Math.PI / 2) }, t),
                d.add(o),
                x.setItemGraphicEl(e, o))
            }
            if (y) {
              var a = C(e, i),
                r = g.get('clip')
              ;(v(a, { shape: { endAngle: O(n, b, I, r) } }, t),
                d.add(a),
                E(t.seriesIndex, x.dataType, e, a),
                (c[e] = a))
            }
          })
          .update(function (e, n) {
            var o = x.get(_, e)
            if (f) {
              var a = h.getItemGraphicEl(n),
                r = a ? a.rotation : i,
                s = A(e, r)
              ;((s.rotation = r),
                m(s, { rotation: -((isNaN(+o) ? I[0] : O(o, b, I, !0)) + Math.PI / 2) }, t),
                d.add(s),
                x.setItemGraphicEl(e, s))
            }
            if (y) {
              var l = p[n],
                u = C(e, l ? l.shape.endAngle : i),
                v = g.get('clip')
              ;(m(u, { shape: { endAngle: O(o, b, I, v) } }, t),
                d.add(u),
                E(t.seriesIndex, x.dataType, e, u),
                (c[e] = u))
            }
          })
          .execute(),
        x.each(function (t) {
          var e = x.getItemModel(t),
            n = e.getModel('emphasis'),
            a = n.get('focus'),
            i = n.get('blurScope'),
            r = n.get('disabled')
          if (f) {
            var s = x.getItemGraphicEl(t),
              l = x.getItemVisual(t, 'style'),
              u = l.fill
            if (s instanceof V) {
              var d = s.style
              s.useStyle(Z({ image: d.image, x: d.x, y: d.y, width: d.width, height: d.height }, l))
            } else (s.useStyle(l), 'pointer' !== s.type && s.setColor(u))
            ;(s.setStyle(e.getModel(['pointer', 'itemStyle']).getItemStyle()),
              'auto' === s.style.fill && s.setStyle('fill', o(O(x.get(_, t), b, [0, 1], !0))),
              (s.z2EmphasisLift = 0),
              N(s, e),
              S(s, a, i, r))
          }
          if (y) {
            var h = c[t]
            ;(h.useStyle(x.getItemVisual(t, 'style')),
              h.setStyle(e.getModel(['progress', 'itemStyle']).getItemStyle()),
              (h.z2EmphasisLift = 0),
              N(h, e),
              S(h, a, i, r))
          }
        }),
        (this._progressEls = c))
    }),
    (n.prototype._renderAnchor = function (t, e) {
      var n = t.getModel('anchor')
      if (n.get('show')) {
        var o = n.get('size'),
          a = n.get('icon'),
          i = n.get('offsetCenter'),
          s = n.get('keepAspect'),
          l = r(a, e.cx - o / 2 + k(i[0], e.r), e.cy - o / 2 + k(i[1], e.r), o, o, null, s)
        ;((l.z2 = n.get('showAbove') ? 1 : 0),
          l.setStyle(n.getModel('itemStyle').getItemStyle()),
          this.group.add(l))
      }
    }),
    (n.prototype._renderTitleAndDetail = function (t, e, n, o, a) {
      var r = this,
        s = t.getData(),
        l = s.mapDimension('value'),
        u = +t.get('min'),
        d = +t.get('max'),
        h = new i(),
        p = [],
        c = [],
        f = t.isAnimationEnabled(),
        g = t.get(['pointer', 'showAbove'])
      ;(s
        .diff(this._data)
        .add(function (t) {
          ;((p[t] = new R({ silent: !0 })), (c[t] = new R({ silent: !0 })))
        })
        .update(function (t, e) {
          ;((p[t] = r._titleEls[e]), (c[t] = r._detailEls[e]))
        })
        .execute(),
        s.each(function (e) {
          var n = s.getItemModel(e),
            r = s.get(l, e),
            v = new i(),
            y = o(O(r, [u, d], [0, 1], !0)),
            m = n.getModel('title')
          if (m.get('show')) {
            var x = m.get('offsetCenter'),
              _ = a.cx + k(x[0], a.r),
              M = a.cy + k(x[1], a.r)
            ;((D = p[e]).attr({
              z2: g ? 0 : 2,
              style: z(
                m,
                { x: _, y: M, text: s.getName(e), align: 'center', verticalAlign: 'middle' },
                { inheritColor: y }
              )
            }),
              v.add(D))
          }
          var w = n.getModel('detail')
          if (w.get('show')) {
            var b = w.get('offsetCenter'),
              S = a.cx + k(b[0], a.r),
              I = a.cy + k(b[1], a.r),
              A = k(w.get('width'), a.r),
              C = k(w.get('height'), a.r),
              T = t.get(['progress', 'show']) ? s.getItemVisual(e, 'style').fill : y,
              D = c[e],
              L = w.get('formatter')
            ;(D.attr({
              z2: g ? 0 : 2,
              style: z(
                w,
                {
                  x: S,
                  y: I,
                  text: zn(r, L),
                  width: isNaN(A) ? null : A,
                  height: isNaN(C) ? null : C,
                  align: 'center',
                  verticalAlign: 'middle'
                },
                { inheritColor: T }
              )
            }),
              B(D, { normal: w }, r, function (t) {
                return zn(t, L)
              }),
              f &&
                F(D, e, s, t, {
                  getFormattedLabel: function (t, e, n, o, a, i) {
                    return zn(i ? i.interpolatedValue : r, L)
                  }
                }),
              v.add(D))
          }
          h.add(v)
        }),
        this.group.add(h),
        (this._titleEls = p),
        (this._detailEls = c))
    }),
    (n.type = 'gauge'),
    n
  )
})(d)
const En = (function (e) {
  function n() {
    var t = (null !== e && e.apply(this, arguments)) || this
    return ((t.type = n.type), (t.visualStyleAccessPath = 'itemStyle'), t)
  }
  return (
    t(n, e),
    (n.prototype.getInitialData = function (t, e) {
      return X(this, ['value'])
    }),
    (n.type = 'series.gauge'),
    (n.defaultOption = {
      z: 2,
      colorBy: 'data',
      center: ['50%', '50%'],
      legendHoverLink: !0,
      radius: '75%',
      startAngle: 225,
      endAngle: -45,
      clockwise: !0,
      min: 0,
      max: 100,
      splitNumber: 10,
      axisLine: { show: !0, roundCap: !1, lineStyle: { color: [[1, '#E6EBF8']], width: 10 } },
      progress: { show: !1, overlap: !0, width: 10, roundCap: !1, clip: !0 },
      splitLine: {
        show: !0,
        length: 10,
        distance: 10,
        lineStyle: { color: '#63677A', width: 3, type: 'solid' }
      },
      axisTick: {
        show: !0,
        splitNumber: 5,
        length: 6,
        distance: 10,
        lineStyle: { color: '#63677A', width: 1, type: 'solid' }
      },
      axisLabel: { show: !0, distance: 15, color: '#464646', fontSize: 12, rotate: 0 },
      pointer: {
        icon: null,
        offsetCenter: [0, 0],
        show: !0,
        showAbove: !0,
        length: '60%',
        width: 6,
        keepAspect: !1
      },
      anchor: {
        show: !1,
        showAbove: !1,
        size: 6,
        icon: 'circle',
        offsetCenter: [0, 0],
        keepAspect: !1,
        itemStyle: { color: '#fff', borderWidth: 0, borderColor: '#5470c6' }
      },
      title: {
        show: !0,
        offsetCenter: [0, '20%'],
        color: '#464646',
        fontSize: 16,
        valueAnimation: !1
      },
      detail: {
        show: !0,
        backgroundColor: 'rgba(0,0,0,0)',
        borderWidth: 0,
        borderColor: '#ccc',
        width: 100,
        height: null,
        padding: [5, 10],
        offsetCenter: [0, '40%'],
        color: '#464646',
        fontSize: 30,
        fontWeight: 'bold',
        lineHeight: 30,
        valueAnimation: !1
      }
    }),
    n
  )
})(n)
const Vn = (function (e) {
  function n(t, n, o) {
    var a = e.call(this) || this
    return (a.add(a.createLine(t, n, o)), a._updateEffectSymbol(t, n), a)
  }
  return (
    t(n, e),
    (n.prototype.createLine = function (t, e, n) {
      return new Cn(t, e, n)
    }),
    (n.prototype._updateEffectSymbol = function (t, e) {
      var n = t.getItemModel(e).getModel('effect'),
        o = n.get('symbolSize'),
        a = n.get('symbol')
      b(o) || (o = [o, o])
      var i = t.getItemVisual(e, 'style'),
        s = n.get('color') || (i && i.stroke),
        l = this.childAt(1)
      ;(this._symbolType !== a &&
        (this.remove(l), ((l = r(a, -0.5, -0.5, 1, 1, s)).z2 = 100), (l.culling = !0), this.add(l)),
        l &&
          (l.setStyle('shadowColor', s),
          l.setStyle(n.getItemStyle(['color'])),
          (l.scaleX = o[0]),
          (l.scaleY = o[1]),
          l.setColor(s),
          (this._symbolType = a),
          (this._symbolScale = o),
          this._updateEffectAnimation(t, n, e)))
    }),
    (n.prototype._updateEffectAnimation = function (t, e, n) {
      var o = this.childAt(1)
      if (o) {
        var a = t.getItemLayout(n),
          i = 1e3 * e.get('period'),
          r = e.get('loop'),
          s = e.get('roundTrip'),
          l = e.get('constantSpeed'),
          u = j(e.get('delay'), function (e) {
            return ((e / t.count()) * i) / 3
          })
        if (
          ((o.ignore = !0),
          this._updateAnimationPoints(o, a),
          l > 0 && (i = (this._getLineLength(o) / l) * 1e3),
          i !== this._period || r !== this._loop || s !== this._roundTrip)
        ) {
          o.stopAnimation()
          var d = void 0
          ;((d = W(u) ? u(n) : u),
            o.__t > 0 && (d = -i * o.__t),
            this._animateSymbol(o, i, d, r, s))
        }
        ;((this._period = i), (this._loop = r), (this._roundTrip = s))
      }
    }),
    (n.prototype._animateSymbol = function (t, e, n, o, a) {
      if (e > 0) {
        t.__t = 0
        var i = this,
          r = t
            .animate('', o)
            .when(a ? 2 * e : e, { __t: a ? 2 : 1 })
            .delay(n)
            .during(function () {
              i._updateSymbolPosition(t)
            })
        ;(o ||
          r.done(function () {
            i.remove(t)
          }),
          r.start())
      }
    }),
    (n.prototype._getLineLength = function (t) {
      return q(t.__p1, t.__cp1) + q(t.__cp1, t.__p2)
    }),
    (n.prototype._updateAnimationPoints = function (t, e) {
      ;((t.__p1 = e[0]),
        (t.__p2 = e[1]),
        (t.__cp1 = e[2] || [(e[0][0] + e[1][0]) / 2, (e[0][1] + e[1][1]) / 2]))
    }),
    (n.prototype.updateData = function (t, e, n) {
      ;(this.childAt(0).updateData(t, e, n), this._updateEffectSymbol(t, e))
    }),
    (n.prototype._updateSymbolPosition = function (t) {
      var e = t.__p1,
        n = t.__p2,
        o = t.__cp1,
        a = t.__t < 1 ? t.__t : 2 - t.__t,
        i = [t.x, t.y],
        r = i.slice(),
        s = K,
        l = $
      ;((i[0] = s(e[0], o[0], n[0], a)), (i[1] = s(e[1], o[1], n[1], a)))
      var u = t.__t < 1 ? l(e[0], o[0], n[0], a) : l(n[0], o[0], e[0], 1 - a),
        d = t.__t < 1 ? l(e[1], o[1], n[1], a) : l(n[1], o[1], e[1], 1 - a)
      ;((t.rotation = -Math.atan2(d, u) - Math.PI / 2),
        ('line' !== this._symbolType &&
          'rect' !== this._symbolType &&
          'roundRect' !== this._symbolType) ||
          (void 0 !== t.__lastT && t.__lastT < t.__t
            ? ((t.scaleY = 1.05 * q(r, i)),
              1 === a && ((i[0] = r[0] + (i[0] - r[0]) / 2), (i[1] = r[1] + (i[1] - r[1]) / 2)))
            : 1 === t.__lastT
              ? (t.scaleY = 2 * q(e, i))
              : (t.scaleY = this._symbolScale[1])),
        (t.__lastT = t.__t),
        (t.ignore = !1),
        (t.x = i[0]),
        (t.y = i[1]))
    }),
    (n.prototype.updateLayout = function (t, e) {
      this.childAt(0).updateLayout(t, e)
      var n = t.getItemModel(e).getModel('effect')
      this._updateEffectAnimation(t, n, e)
    }),
    n
  )
})(i)
const Zn = (function (e) {
  function n(t, n, o) {
    var a = e.call(this) || this
    return (a._createPolyline(t, n, o), a)
  }
  return (
    t(n, e),
    (n.prototype._createPolyline = function (t, e, n) {
      var o = t.getItemLayout(e),
        a = new Q({ shape: { points: o } })
      ;(this.add(a), this._updateCommonStl(t, e, n))
    }),
    (n.prototype.updateData = function (t, e, n) {
      var o = t.hostModel,
        a = this.childAt(0),
        i = { shape: { points: t.getItemLayout(e) } }
      ;(m(a, i, o, e), this._updateCommonStl(t, e, n))
    }),
    (n.prototype._updateCommonStl = function (t, e, n) {
      var o = this.childAt(0),
        a = t.getItemModel(e),
        i = n && n.emphasisLineStyle,
        r = n && n.focus,
        s = n && n.blurScope,
        l = n && n.emphasisDisabled
      if (!n || t.hasItemOption) {
        var u = a.getModel('emphasis')
        ;((i = u.getModel('lineStyle').getLineStyle()),
          (l = u.get('disabled')),
          (r = u.get('focus')),
          (s = u.get('blurScope')))
      }
      ;(o.useStyle(t.getItemVisual(e, 'style')),
        (o.style.fill = null),
        (o.style.strokeNoScale = !0),
        (o.ensureState('emphasis').style = i),
        S(this, r, s, l))
    }),
    (n.prototype.updateLayout = function (t, e) {
      this.childAt(0).setShape('points', t.getItemLayout(e))
    }),
    n
  )
})(i)
const Nn = (function (e) {
  function n() {
    var t = (null !== e && e.apply(this, arguments)) || this
    return ((t._lastFrame = 0), (t._lastFramePercent = 0), t)
  }
  return (
    t(n, e),
    (n.prototype.createLine = function (t, e, n) {
      return new Zn(t, e, n)
    }),
    (n.prototype._updateAnimationPoints = function (t, e) {
      this._points = e
      for (var n = [0], o = 0, a = 1; a < e.length; a++) {
        var i = e[a - 1],
          r = e[a]
        ;((o += q(i, r)), n.push(o))
      }
      if (0 !== o) {
        for (a = 0; a < n.length; a++) n[a] /= o
        ;((this._offsets = n), (this._length = o))
      } else this._length = 0
    }),
    (n.prototype._getLineLength = function () {
      return this._length
    }),
    (n.prototype._updateSymbolPosition = function (t) {
      var e = t.__t < 1 ? t.__t : 2 - t.__t,
        n = this._points,
        o = this._offsets,
        a = n.length
      if (o) {
        var i,
          r = this._lastFrame
        if (e < this._lastFramePercent) {
          for (i = Math.min(r + 1, a - 1); i >= 0 && !(o[i] <= e); i--);
          i = Math.min(i, a - 2)
        } else {
          for (i = r; i < a && !(o[i] > e); i++);
          i = Math.min(i - 1, a - 2)
        }
        var s = (e - o[i]) / (o[i + 1] - o[i]),
          l = n[i],
          u = n[i + 1]
        ;((t.x = l[0] * (1 - s) + s * u[0]), (t.y = l[1] * (1 - s) + s * u[1]))
        var d = t.__t < 1 ? u[0] - l[0] : l[0] - u[0],
          h = t.__t < 1 ? u[1] - l[1] : l[1] - u[1]
        ;((t.rotation = -Math.atan2(h, d) - Math.PI / 2),
          (this._lastFrame = i),
          (this._lastFramePercent = e),
          (t.ignore = !1))
      }
    }),
    n
  )
})(Vn)
var Bn = function () {
    ;((this.polyline = !1), (this.curveness = 0), (this.segs = []))
  },
  Fn = (function (e) {
    function n(t) {
      var n = e.call(this, t) || this
      return ((n._off = 0), (n.hoverDataIdx = -1), n)
    }
    return (
      t(n, e),
      (n.prototype.reset = function () {
        ;((this.notClear = !1), (this._off = 0))
      }),
      (n.prototype.getDefaultStyle = function () {
        return { stroke: '#000', fill: null }
      }),
      (n.prototype.getDefaultShape = function () {
        return new Bn()
      }),
      (n.prototype.buildPath = function (t, e) {
        var n,
          o = e.segs,
          a = e.curveness
        if (e.polyline)
          for (n = this._off; n < o.length; ) {
            var i = o[n++]
            if (i > 0) {
              t.moveTo(o[n++], o[n++])
              for (var r = 1; r < i; r++) t.lineTo(o[n++], o[n++])
            }
          }
        else
          for (n = this._off; n < o.length; ) {
            var s = o[n++],
              l = o[n++],
              u = o[n++],
              d = o[n++]
            if ((t.moveTo(s, l), a > 0)) {
              var h = (s + u) / 2 - (l - d) * a,
                p = (l + d) / 2 - (u - s) * a
              t.quadraticCurveTo(h, p, u, d)
            } else t.lineTo(u, d)
          }
        this.incremental && ((this._off = n), (this.notClear = !0))
      }),
      (n.prototype.findDataIndex = function (t, e) {
        var n = this.shape,
          o = n.segs,
          a = n.curveness,
          i = this.style.lineWidth
        if (n.polyline)
          for (var r = 0, s = 0; s < o.length; ) {
            var l = o[s++]
            if (l > 0)
              for (var u = o[s++], d = o[s++], h = 1; h < l; h++) {
                var p = o[s++],
                  c = o[s++]
                if (J(u, d, p, c, i, t, e)) return r
              }
            r++
          }
        else
          for (r = 0, s = 0; s < o.length; ) {
            ;((u = o[s++]), (d = o[s++]), (p = o[s++]), (c = o[s++]))
            if (a > 0) {
              if (tt(u, d, (u + p) / 2 - (d - c) * a, (d + c) / 2 - (p - u) * a, p, c, i, t, e))
                return r
            } else if (J(u, d, p, c, i, t, e)) return r
            r++
          }
        return -1
      }),
      (n.prototype.contain = function (t, e) {
        var n = this.transformCoordToLocal(t, e),
          o = this.getBoundingRect()
        return (
          (t = n[0]),
          (e = n[1]),
          o.contain(t, e)
            ? (this.hoverDataIdx = this.findDataIndex(t, e)) >= 0
            : ((this.hoverDataIdx = -1), !1)
        )
      }),
      (n.prototype.getBoundingRect = function () {
        var t = this._rect
        if (!t) {
          for (
            var e = this.shape.segs, n = 1 / 0, a = 1 / 0, i = -1 / 0, r = -1 / 0, s = 0;
            s < e.length;
          ) {
            var l = e[s++],
              u = e[s++]
            ;((n = Math.min(l, n)),
              (i = Math.max(l, i)),
              (a = Math.min(u, a)),
              (r = Math.max(u, r)))
          }
          t = this._rect = new o(n, a, i, r)
        }
        return t
      }),
      n
    )
  })(a)
const Gn = (function () {
  function t() {
    this.group = new i()
  }
  return (
    (t.prototype.updateData = function (t) {
      this._clear()
      var e = this._create()
      ;(e.setShape({ segs: t.getLayout('linesPoints') }), this._setCommon(e, t))
    }),
    (t.prototype.incrementalPrepareUpdate = function (t) {
      ;(this.group.removeAll(), this._clear())
    }),
    (t.prototype.incrementalUpdate = function (t, e) {
      var n = this._newAdded[0],
        o = e.getLayout('linesPoints'),
        a = n && n.shape.segs
      if (a && a.length < 2e4) {
        var i = a.length,
          r = new Float32Array(i + o.length)
        ;(r.set(a), r.set(o, i), n.setShape({ segs: r }))
      } else {
        this._newAdded = []
        var s = this._create()
        ;((s.incremental = !0),
          s.setShape({ segs: o }),
          this._setCommon(s, e),
          (s.__startIndex = t.start))
      }
    }),
    (t.prototype.remove = function () {
      this._clear()
    }),
    (t.prototype.eachRendered = function (t) {
      this._newAdded[0] && t(this._newAdded[0])
    }),
    (t.prototype._create = function () {
      var t = new Fn({ cursor: 'default', ignoreCoarsePointer: !0 })
      return (this._newAdded.push(t), this.group.add(t), t)
    }),
    (t.prototype._setCommon = function (t, e, n) {
      var o = e.hostModel
      ;(t.setShape({ polyline: o.get('polyline'), curveness: o.get(['lineStyle', 'curveness']) }),
        t.useStyle(o.getModel('lineStyle').getLineStyle()),
        (t.style.strokeNoScale = !0))
      var a = e.getVisual('style')
      ;(a && a.stroke && t.setStyle('stroke', a.stroke), t.setStyle('fill', null))
      var i = s(t)
      ;((i.seriesIndex = o.seriesIndex),
        t.on('mousemove', function (e) {
          i.dataIndex = null
          var n = t.hoverDataIdx
          n > 0 && (i.dataIndex = n + t.__startIndex)
        }))
    }),
    (t.prototype._clear = function () {
      ;((this._newAdded = []), this.group.removeAll())
    }),
    t
  )
})()
const Wn = {
  seriesType: 'lines',
  plan: et(),
  reset: function (t) {
    var e = t.coordinateSystem
    if (e) {
      var n = t.get('polyline'),
        o = t.pipelineContext.large
      return {
        progress: function (a, i) {
          var r = []
          if (o) {
            var s = void 0,
              l = a.end - a.start
            if (n) {
              for (var u = 0, d = a.start; d < a.end; d++) u += t.getLineCoordsCount(d)
              s = new Float32Array(l + 2 * u)
            } else s = new Float32Array(4 * l)
            var h = 0,
              p = []
            for (d = a.start; d < a.end; d++) {
              var c = t.getLineCoords(d, r)
              n && (s[h++] = c)
              for (var f = 0; f < c; f++)
                ((p = e.dataToPoint(r[f], !1, p)), (s[h++] = p[0]), (s[h++] = p[1]))
            }
            i.setLayout('linesPoints', s)
          } else
            for (d = a.start; d < a.end; d++) {
              var g = i.getItemModel(d),
                v = ((c = t.getLineCoords(d, r)), [])
              if (n) for (var y = 0; y < c; y++) v.push(e.dataToPoint(r[y]))
              else {
                ;((v[0] = e.dataToPoint(r[0])), (v[1] = e.dataToPoint(r[1])))
                var m = g.get(['lineStyle', 'curveness'])
                ;+m &&
                  (v[2] = [
                    (v[0][0] + v[1][0]) / 2 - (v[0][1] - v[1][1]) * m,
                    (v[0][1] + v[1][1]) / 2 - (v[1][0] - v[0][0]) * m
                  ])
              }
              i.setItemLayout(d, v)
            }
        }
      }
    }
  }
}
const Hn = (function (e) {
  function n() {
    var t = (null !== e && e.apply(this, arguments)) || this
    return ((t.type = n.type), t)
  }
  return (
    t(n, e),
    (n.prototype.render = function (t, e, n) {
      var o = t.getData(),
        a = this._updateLineDraw(o, t),
        i = t.get('zlevel'),
        r = t.get(['effect', 'trailLength']),
        s = n.getZr(),
        l = 'svg' === s.painter.getType()
      ;(l || s.painter.getLayer(i).clear(!0),
        null == this._lastZlevel || l || s.configLayer(this._lastZlevel, { motionBlur: !1 }),
        this._showEffect(t) &&
          r > 0 &&
          (l ||
            s.configLayer(i, {
              motionBlur: !0,
              lastFrameAlpha: Math.max(Math.min(r / 10 + 0.9, 1), 0)
            })),
        a.updateData(o))
      var u = t.get('clip', !0) && nt(t.coordinateSystem, !1, t)
      ;(u ? this.group.setClipPath(u) : this.group.removeClipPath(),
        (this._lastZlevel = i),
        (this._finished = !0))
    }),
    (n.prototype.incrementalPrepareRender = function (t, e, n) {
      var o = t.getData()
      ;(this._updateLineDraw(o, t).incrementalPrepareUpdate(o),
        this._clearLayer(n),
        (this._finished = !1))
    }),
    (n.prototype.incrementalRender = function (t, e, n) {
      ;(this._lineDraw.incrementalUpdate(t, e.getData()),
        (this._finished = t.end === e.getData().count()))
    }),
    (n.prototype.eachRendered = function (t) {
      this._lineDraw && this._lineDraw.eachRendered(t)
    }),
    (n.prototype.updateTransform = function (t, e, n) {
      var o = t.getData(),
        a = t.pipelineContext
      if (!this._finished || a.large || a.progressiveRender) return { update: !0 }
      var i = Wn.reset(t, e, n)
      ;(i.progress && i.progress({ start: 0, end: o.count(), count: o.count() }, o),
        this._lineDraw.updateLayout(),
        this._clearLayer(n))
    }),
    (n.prototype._updateLineDraw = function (t, e) {
      var n = this._lineDraw,
        o = this._showEffect(e),
        a = !!e.get('polyline'),
        i = e.pipelineContext.large
      return (
        (n && o === this._hasEffet && a === this._isPolyline && i === this._isLargeDraw) ||
          (n && n.remove(),
          (n = this._lineDraw = i ? new Gn() : new Pn(a ? (o ? Nn : Zn) : o ? Vn : Cn)),
          (this._hasEffet = o),
          (this._isPolyline = a),
          (this._isLargeDraw = i)),
        this.group.add(n.group),
        n
      )
    }),
    (n.prototype._showEffect = function (t) {
      return !!t.get(['effect', 'show'])
    }),
    (n.prototype._clearLayer = function (t) {
      var e = t.getZr()
      'svg' === e.painter.getType() ||
        null == this._lastZlevel ||
        e.painter.getLayer(this._lastZlevel).clear(!0)
    }),
    (n.prototype.remove = function (t, e) {
      ;(this._lineDraw && this._lineDraw.remove(), (this._lineDraw = null), this._clearLayer(e))
    }),
    (n.prototype.dispose = function (t, e) {
      this.remove(t, e)
    }),
    (n.type = 'lines'),
    n
  )
})(d)
var Un = 'undefined' == typeof Uint32Array ? Array : Uint32Array,
  Yn = 'undefined' == typeof Float64Array ? Array : Float64Array
function Xn(t) {
  var e = t.data
  e &&
    e[0] &&
    e[0][0] &&
    e[0][0].coord &&
    (t.data = rt(e, function (t) {
      var e = { coords: [t[0].coord, t[1].coord] }
      return (
        t[0].name && (e.fromName = t[0].name),
        t[1].name && (e.toName = t[1].name),
        st([e, t[0], t[1]])
      )
    }))
}
const jn = (function (e) {
  function n() {
    var t = (null !== e && e.apply(this, arguments)) || this
    return (
      (t.type = n.type),
      (t.visualStyleAccessPath = 'lineStyle'),
      (t.visualDrawType = 'stroke'),
      t
    )
  }
  return (
    t(n, e),
    (n.prototype.init = function (t) {
      ;((t.data = t.data || []), Xn(t))
      var n = this._processFlatCoordsArray(t.data)
      ;((this._flatCoords = n.flatCoords),
        (this._flatCoordsOffset = n.flatCoordsOffset),
        n.flatCoords && (t.data = new Float32Array(n.count)),
        e.prototype.init.apply(this, arguments))
    }),
    (n.prototype.mergeOption = function (t) {
      if ((Xn(t), t.data)) {
        var n = this._processFlatCoordsArray(t.data)
        ;((this._flatCoords = n.flatCoords),
          (this._flatCoordsOffset = n.flatCoordsOffset),
          n.flatCoords && (t.data = new Float32Array(n.count)))
      }
      e.prototype.mergeOption.apply(this, arguments)
    }),
    (n.prototype.appendData = function (t) {
      var e = this._processFlatCoordsArray(t.data)
      ;(e.flatCoords &&
        (this._flatCoords
          ? ((this._flatCoords = ot(this._flatCoords, e.flatCoords)),
            (this._flatCoordsOffset = ot(this._flatCoordsOffset, e.flatCoordsOffset)))
          : ((this._flatCoords = e.flatCoords), (this._flatCoordsOffset = e.flatCoordsOffset)),
        (t.data = new Float32Array(e.count))),
        this.getRawData().appendData(t.data))
    }),
    (n.prototype._getCoordsFromItemModel = function (t) {
      var e = this.getData().getItemModel(t)
      return e.option instanceof Array ? e.option : e.getShallow('coords')
    }),
    (n.prototype.getLineCoordsCount = function (t) {
      return this._flatCoordsOffset
        ? this._flatCoordsOffset[2 * t + 1]
        : this._getCoordsFromItemModel(t).length
    }),
    (n.prototype.getLineCoords = function (t, e) {
      if (this._flatCoordsOffset) {
        for (
          var n = this._flatCoordsOffset[2 * t], o = this._flatCoordsOffset[2 * t + 1], a = 0;
          a < o;
          a++
        )
          ((e[a] = e[a] || []),
            (e[a][0] = this._flatCoords[n + 2 * a]),
            (e[a][1] = this._flatCoords[n + 2 * a + 1]))
        return o
      }
      var i = this._getCoordsFromItemModel(t)
      for (a = 0; a < i.length; a++) ((e[a] = e[a] || []), (e[a][0] = i[a][0]), (e[a][1] = i[a][1]))
      return i.length
    }),
    (n.prototype._processFlatCoordsArray = function (t) {
      var e = 0
      if ((this._flatCoords && (e = this._flatCoords.length), Y(t[0]))) {
        for (var n = t.length, o = new Un(n), a = new Yn(n), i = 0, r = 0, s = 0, l = 0; l < n; ) {
          s++
          var u = t[l++]
          ;((o[r++] = i + e), (o[r++] = u))
          for (var d = 0; d < u; d++) {
            var h = t[l++],
              p = t[l++]
            ;((a[i++] = h), (a[i++] = p))
          }
        }
        return { flatCoordsOffset: new Uint32Array(o.buffer, 0, r), flatCoords: a, count: s }
      }
      return { flatCoordsOffset: null, flatCoords: null, count: t.length }
    }),
    (n.prototype.getInitialData = function (t, e) {
      var n = new at(['value'], this)
      return (
        (n.hasItemOption = !1),
        n.initData(t.data, [], function (t, e, o, a) {
          if (t instanceof Array) return NaN
          n.hasItemOption = !0
          var i = t.value
          return null != i ? (i instanceof Array ? i[a] : i) : void 0
        }),
        n
      )
    }),
    (n.prototype.formatTooltip = function (t, e, n) {
      var o = this.getData().getItemModel(t),
        a = o.get('name')
      if (a) return a
      var i = o.get('fromName'),
        r = o.get('toName'),
        s = []
      return (
        null != i && s.push(i),
        null != r && s.push(r),
        it('nameValue', { name: s.join(' > ') })
      )
    }),
    (n.prototype.preventIncremental = function () {
      return !!this.get(['effect', 'show'])
    }),
    (n.prototype.getProgressive = function () {
      var t = this.option.progressive
      return null == t ? (this.option.large ? 1e4 : this.get('progressive')) : t
    }),
    (n.prototype.getProgressiveThreshold = function () {
      var t = this.option.progressiveThreshold
      return null == t ? (this.option.large ? 2e4 : this.get('progressiveThreshold')) : t
    }),
    (n.prototype.getZLevelKey = function () {
      var t = this.getModel('effect'),
        e = t.get('trailLength')
      return this.getData().count() > this.getProgressiveThreshold()
        ? this.id
        : t.get('show') && e > 0
          ? e + ''
          : ''
    }),
    (n.type = 'series.lines'),
    (n.dependencies = ['grid', 'polar', 'geo', 'calendar']),
    (n.defaultOption = {
      coordinateSystem: 'geo',
      z: 2,
      legendHoverLink: !0,
      xAxisIndex: 0,
      yAxisIndex: 0,
      symbol: ['none', 'none'],
      symbolSize: [10, 10],
      geoIndex: 0,
      effect: {
        show: !1,
        period: 4,
        constantSpeed: 0,
        symbol: 'circle',
        symbolSize: 3,
        loop: !0,
        trailLength: 0.2
      },
      large: !1,
      largeThreshold: 2e3,
      polyline: !1,
      clip: !0,
      label: { show: !1, position: 'end' },
      lineStyle: { opacity: 0.5 }
    }),
    n
  )
})(n)
function qn(t) {
  return (t instanceof Array || (t = [t, t]), t)
}
const Kn = {
  seriesType: 'lines',
  reset: function (t) {
    var e = qn(t.get('symbol')),
      n = qn(t.get('symbolSize')),
      o = t.getData()
    return (
      o.setVisual('fromSymbol', e && e[0]),
      o.setVisual('toSymbol', e && e[1]),
      o.setVisual('fromSymbolSize', n && n[0]),
      o.setVisual('toSymbolSize', n && n[1]),
      {
        dataEach: o.hasItemOption
          ? function (t, e) {
              var n = t.getItemModel(e),
                o = qn(n.getShallow('symbol', !0)),
                a = qn(n.getShallow('symbolSize', !0))
              ;(o[0] && t.setItemVisual(e, 'fromSymbol', o[0]),
                o[1] && t.setItemVisual(e, 'toSymbol', o[1]),
                a[0] && t.setItemVisual(e, 'fromSymbolSize', a[0]),
                a[1] && t.setItemVisual(e, 'toSymbolSize', a[1]))
            }
          : null
      }
    )
  }
}
var $n = ['x', 'y', 'radius', 'angle', 'single'],
  Qn = ['cartesian2d', 'polar', 'singleAxis']
function Jn(t) {
  return t + 'Axis'
}
function to(t, e) {
  var n,
    o = lt(),
    a = [],
    i = lt()
  t.eachComponent({ mainType: 'dataZoom', query: e }, function (t) {
    i.get(t.uid) || s(t)
  })
  do {
    ;((n = !1), t.eachComponent('dataZoom', r))
  } while (n)
  function r(t) {
    !i.get(t.uid) &&
      (function (t) {
        var e = !1
        return (
          t.eachTargetAxis(function (t, n) {
            var a = o.get(t)
            a && a[n] && (e = !0)
          }),
          e
        )
      })(t) &&
      (s(t), (n = !0))
  }
  function s(t) {
    ;(i.set(t.uid, !0),
      a.push(t),
      t.eachTargetAxis(function (t, e) {
        ;(o.get(t) || o.set(t, []))[e] = !0
      }))
  }
  return a
}
function eo(t) {
  var e = t.ecModel,
    n = { infoList: [], infoMap: lt() }
  return (
    t.eachTargetAxis(function (t, o) {
      var a = e.getComponent(Jn(t), o)
      if (a) {
        var i = a.getCoordSysModel()
        if (i) {
          var r = i.uid,
            s = n.infoMap.get(r)
          ;(s || ((s = { model: i, axisModels: [] }), n.infoList.push(s), n.infoMap.set(r, s)),
            s.axisModels.push(a))
        }
      }
    }),
    n
  )
}
var no = (function () {
  function t() {
    ;((this.indexList = []), (this.indexMap = []))
  }
  return (
    (t.prototype.add = function (t) {
      this.indexMap[t] || (this.indexList.push(t), (this.indexMap[t] = !0))
    }),
    t
  )
})()
function oo(t) {
  var e = {}
  return (
    y(['start', 'end', 'startValue', 'endValue', 'throttle'], function (n) {
      t.hasOwnProperty(n) && (e[n] = t[n])
    }),
    e
  )
}
const ao = (function (e) {
  function n() {
    var t = (null !== e && e.apply(this, arguments)) || this
    return (
      (t.type = n.type),
      (t._autoThrottle = !0),
      (t._noTarget = !0),
      (t._rangePropMode = ['percent', 'percent']),
      t
    )
  }
  return (
    t(n, e),
    (n.prototype.init = function (t, e, n) {
      var o = oo(t)
      ;((this.settledOption = o), this.mergeDefaultAndTheme(t, n), this._doInit(o))
    }),
    (n.prototype.mergeOption = function (t) {
      var e = oo(t)
      ;(dt(this.option, t, !0), dt(this.settledOption, e, !0), this._doInit(e))
    }),
    (n.prototype._doInit = function (t) {
      var e = this.option
      ;(this._setDefaultThrottle(t), this._updateRangeUse(t))
      var n = this.settledOption
      ;(y(
        [
          ['start', 'startValue'],
          ['end', 'endValue']
        ],
        function (t, o) {
          'value' === this._rangePropMode[o] && (e[t[0]] = n[t[0]] = null)
        },
        this
      ),
        this._resetTarget())
    }),
    (n.prototype._resetTarget = function () {
      var t = this.get('orient', !0),
        e = (this._targetAxisInfoMap = lt())
      ;(this._fillSpecifiedTargetAxis(e)
        ? (this._orient = t || this._makeAutoOrientByTargetAxis())
        : ((this._orient = t || 'horizontal'), this._fillAutoTargetAxisByOrient(e, this._orient)),
        (this._noTarget = !0),
        e.each(function (t) {
          t.indexList.length && (this._noTarget = !1)
        }, this))
    }),
    (n.prototype._fillSpecifiedTargetAxis = function (t) {
      var e = !1
      return (
        y(
          $n,
          function (n) {
            var o = this.getReferringComponents(Jn(n), ht)
            if (o.specified) {
              e = !0
              var a = new no()
              ;(y(o.models, function (t) {
                a.add(t.componentIndex)
              }),
                t.set(n, a))
            }
          },
          this
        ),
        e
      )
    }),
    (n.prototype._fillAutoTargetAxisByOrient = function (t, e) {
      var n = this.ecModel,
        o = !0
      if (o) {
        var a = 'vertical' === e ? 'y' : 'x'
        i(n.findComponents({ mainType: a + 'Axis' }), a)
      }
      o &&
        i(
          n.findComponents({
            mainType: 'singleAxis',
            filter: function (t) {
              return t.get('orient', !0) === e
            }
          }),
          'single'
        )
      function i(e, n) {
        var a = e[0]
        if (a) {
          var i = new no()
          if ((i.add(a.componentIndex), t.set(n, i), (o = !1), 'x' === n || 'y' === n)) {
            var r = a.getReferringComponents('grid', pt).models[0]
            r &&
              y(e, function (t) {
                a.componentIndex !== t.componentIndex &&
                  r === t.getReferringComponents('grid', pt).models[0] &&
                  i.add(t.componentIndex)
              })
          }
        }
      }
      o &&
        y(
          $n,
          function (e) {
            if (o) {
              var a = n.findComponents({
                mainType: Jn(e),
                filter: function (t) {
                  return 'category' === t.get('type', !0)
                }
              })
              if (a[0]) {
                var i = new no()
                ;(i.add(a[0].componentIndex), t.set(e, i), (o = !1))
              }
            }
          },
          this
        )
    }),
    (n.prototype._makeAutoOrientByTargetAxis = function () {
      var t
      return (
        this.eachTargetAxis(function (e) {
          !t && (t = e)
        }, this),
        'y' === t ? 'vertical' : 'horizontal'
      )
    }),
    (n.prototype._setDefaultThrottle = function (t) {
      if ((t.hasOwnProperty('throttle') && (this._autoThrottle = !1), this._autoThrottle)) {
        var e = this.ecModel.option
        this.option.throttle = e.animation && e.animationDurationUpdate > 0 ? 100 : 20
      }
    }),
    (n.prototype._updateRangeUse = function (t) {
      var e = this._rangePropMode,
        n = this.get('rangeMode')
      y(
        [
          ['start', 'startValue'],
          ['end', 'endValue']
        ],
        function (o, a) {
          var i = null != t[o[0]],
            r = null != t[o[1]]
          i && !r
            ? (e[a] = 'percent')
            : !i && r
              ? (e[a] = 'value')
              : n
                ? (e[a] = n[a])
                : i && (e[a] = 'percent')
        }
      )
    }),
    (n.prototype.noTarget = function () {
      return this._noTarget
    }),
    (n.prototype.getFirstTargetAxisModel = function () {
      var t
      return (
        this.eachTargetAxis(function (e, n) {
          null == t && (t = this.ecModel.getComponent(Jn(e), n))
        }, this),
        t
      )
    }),
    (n.prototype.eachTargetAxis = function (t, e) {
      this._targetAxisInfoMap.each(function (n, o) {
        y(n.indexList, function (n) {
          t.call(e, o, n)
        })
      })
    }),
    (n.prototype.getAxisProxy = function (t, e) {
      var n = this.getAxisModel(t, e)
      if (n) return n.__dzAxisProxy
    }),
    (n.prototype.getAxisModel = function (t, e) {
      var n = this._targetAxisInfoMap.get(t)
      if (n && n.indexMap[e]) return this.ecModel.getComponent(Jn(t), e)
    }),
    (n.prototype.setRawRange = function (t) {
      var e = this.option,
        n = this.settledOption
      ;(y(
        [
          ['start', 'startValue'],
          ['end', 'endValue']
        ],
        function (o) {
          ;(null == t[o[0]] && null == t[o[1]]) ||
            ((e[o[0]] = n[o[0]] = t[o[0]]), (e[o[1]] = n[o[1]] = t[o[1]]))
        },
        this
      ),
        this._updateRangeUse(t))
    }),
    (n.prototype.setCalculatedRange = function (t) {
      var e = this.option
      y(['start', 'startValue', 'end', 'endValue'], function (n) {
        e[n] = t[n]
      })
    }),
    (n.prototype.getPercentRange = function () {
      var t = this.findRepresentativeAxisProxy()
      if (t) return t.getDataPercentWindow()
    }),
    (n.prototype.getValueRange = function (t, e) {
      if (null != t || null != e) return this.getAxisProxy(t, e).getDataValueWindow()
      var n = this.findRepresentativeAxisProxy()
      return n ? n.getDataValueWindow() : void 0
    }),
    (n.prototype.findRepresentativeAxisProxy = function (t) {
      if (t) return t.__dzAxisProxy
      for (var e, n = this._targetAxisInfoMap.keys(), o = 0; o < n.length; o++)
        for (var a = n[o], i = this._targetAxisInfoMap.get(a), r = 0; r < i.indexList.length; r++) {
          var s = this.getAxisProxy(a, i.indexList[r])
          if (s.hostedBy(this)) return s
          e || (e = s)
        }
      return e
    }),
    (n.prototype.getRangePropMode = function () {
      return this._rangePropMode.slice()
    }),
    (n.prototype.getOrient = function () {
      return this._orient
    }),
    (n.type = 'dataZoom'),
    (n.dependencies = [
      'xAxis',
      'yAxis',
      'radiusAxis',
      'angleAxis',
      'singleAxis',
      'series',
      'toolbox'
    ]),
    (n.defaultOption = { z: 4, filterMode: 'filter', start: 0, end: 100 }),
    n
  )
})(ct)
const io = (function (e) {
  function n() {
    var t = (null !== e && e.apply(this, arguments)) || this
    return ((t.type = n.type), t)
  }
  return (t(n, e), (n.type = 'dataZoom.select'), n)
})(ao)
const ro = (function (e) {
  function n() {
    var t = (null !== e && e.apply(this, arguments)) || this
    return ((t.type = n.type), t)
  }
  return (
    t(n, e),
    (n.prototype.render = function (t, e, n, o) {
      ;((this.dataZoomModel = t), (this.ecModel = e), (this.api = n))
    }),
    (n.type = 'dataZoom'),
    n
  )
})(ft)
const so = (function (e) {
  function n() {
    var t = (null !== e && e.apply(this, arguments)) || this
    return ((t.type = n.type), t)
  }
  return (t(n, e), (n.type = 'dataZoom.select'), n)
})(ro)
var lo = y,
  uo = _t
const ho = (function () {
  function t(t, e, n, o) {
    ;((this._dimName = t), (this._axisIndex = e), (this.ecModel = o), (this._dataZoomModel = n))
  }
  return (
    (t.prototype.hostedBy = function (t) {
      return this._dataZoomModel === t
    }),
    (t.prototype.getDataValueWindow = function () {
      return this._valueWindow.slice()
    }),
    (t.prototype.getDataPercentWindow = function () {
      return this._percentWindow.slice()
    }),
    (t.prototype.getTargetSeriesModels = function () {
      var t = []
      return (
        this.ecModel.eachSeries(function (e) {
          if (
            (function (t) {
              var e = t.get('coordinateSystem')
              return ut(Qn, e) >= 0
            })(e)
          ) {
            var n = Jn(this._dimName),
              o = e.getReferringComponents(n, pt).models[0]
            o && this._axisIndex === o.componentIndex && t.push(e)
          }
        }, this),
        t
      )
    }),
    (t.prototype.getAxisModel = function () {
      return this.ecModel.getComponent(this._dimName + 'Axis', this._axisIndex)
    }),
    (t.prototype.getMinMaxSpan = function () {
      return gt(this._minMaxSpan)
    }),
    (t.prototype.calculateDataWindow = function (t) {
      var e,
        n = this._dataExtent,
        o = this.getAxisModel().axis.scale,
        a = this._dataZoomModel.getRangePropMode(),
        i = [0, 100],
        r = [],
        s = []
      ;(lo(['start', 'end'], function (l, u) {
        var d = t[l],
          h = t[l + 'Value']
        ;('percent' === a[u]
          ? (null == d && (d = i[u]), (h = o.parse(O(d, i, n))))
          : ((e = !0), (h = null == h ? n[u] : o.parse(h)), (d = O(h, n, i))),
          (s[u] = null == h || isNaN(h) ? n[u] : h),
          (r[u] = null == d || isNaN(d) ? i[u] : d))
      }),
        uo(s),
        uo(r))
      var l = this._minMaxSpan
      function u(t, e, n, a, i) {
        var r = i ? 'Span' : 'ValueSpan'
        vt(0, t, n, 'all', l['min' + r], l['max' + r])
        for (var s = 0; s < 2; s++) ((e[s] = O(t[s], n, a, !0)), i && (e[s] = o.parse(e[s])))
      }
      return (e ? u(s, r, n, i, !1) : u(r, s, i, n, !0), { valueWindow: s, percentWindow: r })
    }),
    (t.prototype.reset = function (t) {
      if (t === this._dataZoomModel) {
        var e = this.getTargetSeriesModels()
        ;((this._dataExtent = (function (t, e, n) {
          var o = [1 / 0, -1 / 0]
          lo(n, function (t) {
            mt(o, t.getData(), e)
          })
          var a = t.getAxisModel(),
            i = xt(a.axis.scale, a, o).calculate()
          return [i.min, i.max]
        })(this, this._dimName, e)),
          this._updateMinMaxSpan())
        var n = this.calculateDataWindow(t.settledOption)
        ;((this._valueWindow = n.valueWindow),
          (this._percentWindow = n.percentWindow),
          this._setAxisModel())
      }
    }),
    (t.prototype.filterData = function (t, e) {
      if (t === this._dataZoomModel) {
        var n = this._dimName,
          o = this.getTargetSeriesModels(),
          a = t.get('filterMode'),
          i = this._valueWindow
        'none' !== a &&
          lo(o, function (t) {
            var e = t.getData(),
              o = e.mapDimensionsAll(n)
            if (o.length) {
              if ('weakFilter' === a) {
                var r = e.getStore(),
                  s = rt(
                    o,
                    function (t) {
                      return e.getDimensionIndex(t)
                    },
                    e
                  )
                e.filterSelf(function (t) {
                  for (var e, n, a, l = 0; l < o.length; l++) {
                    var u = r.get(s[l], t),
                      d = !isNaN(u),
                      h = u < i[0],
                      p = u > i[1]
                    if (d && !h && !p) return !0
                    ;(d && (a = !0), h && (e = !0), p && (n = !0))
                  }
                  return a && e && n
                })
              } else
                lo(o, function (n) {
                  if ('empty' === a)
                    t.setData(
                      (e = e.map(n, function (t) {
                        return (function (t) {
                          return t >= i[0] && t <= i[1]
                        })(t)
                          ? t
                          : NaN
                      }))
                    )
                  else {
                    var o = {}
                    ;((o[n] = i), e.selectRange(o))
                  }
                })
              lo(o, function (t) {
                e.setApproximateExtent(i, t)
              })
            }
          })
      }
    }),
    (t.prototype._updateMinMaxSpan = function () {
      var t = (this._minMaxSpan = {}),
        e = this._dataZoomModel,
        n = this._dataExtent
      lo(
        ['min', 'max'],
        function (o) {
          var a = e.get(o + 'Span'),
            i = e.get(o + 'ValueSpan')
          ;(null != i && (i = this.getAxisModel().axis.scale.parse(i)),
            null != i
              ? (a = O(n[0] + i, n, [0, 100], !0))
              : null != a && (i = O(a, [0, 100], n, !0) - n[0]),
            (t[o + 'Span'] = a),
            (t[o + 'ValueSpan'] = i))
        },
        this
      )
    }),
    (t.prototype._setAxisModel = function () {
      var t = this.getAxisModel(),
        e = this._percentWindow,
        n = this._valueWindow
      if (e) {
        var o = yt(n, [0, 500])
        o = Math.min(o, 20)
        var a = t.axis.scale.rawExtentInfo
        ;(0 !== e[0] && a.setDeterminedMinMax('min', +n[0].toFixed(o)),
          100 !== e[1] && a.setDeterminedMinMax('max', +n[1].toFixed(o)),
          a.freeze())
      }
    }),
    t
  )
})()
const po = {
  getTargetSeries: function (t) {
    function e(e) {
      t.eachComponent('dataZoom', function (n) {
        n.eachTargetAxis(function (o, a) {
          var i = t.getComponent(Jn(o), a)
          e(o, a, i, n)
        })
      })
    }
    e(function (t, e, n, o) {
      n.__dzAxisProxy = null
    })
    var n = []
    e(function (e, o, a, i) {
      a.__dzAxisProxy || ((a.__dzAxisProxy = new ho(e, o, i, t)), n.push(a.__dzAxisProxy))
    })
    var o = lt()
    return (
      y(n, function (t) {
        y(t.getTargetSeriesModels(), function (t) {
          o.set(t.uid, t)
        })
      }),
      o
    )
  },
  overallReset: function (t, e) {
    ;(t.eachComponent('dataZoom', function (t) {
      ;(t.eachTargetAxis(function (e, n) {
        t.getAxisProxy(e, n).reset(t)
      }),
        t.eachTargetAxis(function (n, o) {
          t.getAxisProxy(n, o).filterData(t, e)
        }))
    }),
      t.eachComponent('dataZoom', function (t) {
        var e = t.findRepresentativeAxisProxy()
        if (e) {
          var n = e.getDataPercentWindow(),
            o = e.getDataValueWindow()
          t.setCalculatedRange({ start: n[0], end: n[1], startValue: o[0], endValue: o[1] })
        }
      }))
  }
}
var co = !1
function fo(t) {
  co ||
    ((co = !0),
    t.registerProcessor(t.PRIORITY.PROCESSOR.FILTER, po),
    (function (t) {
      t.registerAction('dataZoom', function (t, e) {
        var n = to(e, t)
        y(n, function (e) {
          e.setRawRange({
            start: t.start,
            end: t.end,
            startValue: t.startValue,
            endValue: t.endValue
          })
        })
      })
    })(t),
    t.registerSubTypeDefaulter('dataZoom', function () {
      return 'slider'
    }))
}
function go(t) {
  ;(t.registerComponentModel(io), t.registerComponentView(so), fo(t))
}
var vo = function () {},
  yo = {}
function mo(t, e) {
  yo[t] = e
}
function xo(t) {
  return yo[t]
}
const _o = (function (e) {
  function n() {
    var t = (null !== e && e.apply(this, arguments)) || this
    return ((t.type = n.type), t)
  }
  return (
    t(n, e),
    (n.prototype.optionUpdated = function () {
      e.prototype.optionUpdated.apply(this, arguments)
      var t = this.ecModel
      y(this.option.feature, function (e, n) {
        var o = xo(n)
        o &&
          (o.getDefaultOption && (o.defaultOption = o.getDefaultOption(t)), dt(e, o.defaultOption))
      })
    }),
    (n.type = 'toolbox'),
    (n.layoutMode = { type: 'box', ignoreSize: !0 }),
    (n.defaultOption = {
      show: !0,
      z: 6,
      orient: 'horizontal',
      left: 'right',
      top: 'top',
      backgroundColor: 'transparent',
      borderColor: '#ccc',
      borderRadius: 0,
      borderWidth: 0,
      padding: 5,
      itemSize: 15,
      itemGap: 8,
      showTitle: !0,
      iconStyle: { borderColor: '#666', color: 'none' },
      emphasis: { iconStyle: { borderColor: '#3E98C5' } },
      tooltip: { show: !1, position: 'bottom' }
    }),
    n
  )
})(ct)
const Mo = (function (e) {
  function n() {
    return (null !== e && e.apply(this, arguments)) || this
  }
  return (
    t(n, e),
    (n.prototype.render = function (t, e, n, o) {
      var a = this.group
      if ((a.removeAll(), t.get('show'))) {
        var i = +t.get('itemSize'),
          r = 'vertical' === t.get('orient'),
          s = t.get('feature') || {},
          l = this._features || (this._features = {}),
          u = []
        ;(y(s, function (t, e) {
          u.push(e)
        }),
          new Mt(this._featureNames || [], u).add(d).update(d).remove(wt(d, null)).execute(),
          (this._featureNames = u),
          Tt(a, t, n),
          a.add(Dt(a.getBoundingRect(), t)),
          r ||
            a.eachChild(function (t) {
              var e = t.__title,
                o = t.ensureState('emphasis'),
                r = o.textConfig || (o.textConfig = {}),
                s = t.getTextContent(),
                l = s && s.ensureState('emphasis')
              if (l && !W(l) && e) {
                var u = l.style || (l.style = {}),
                  d = Lt(e, R.makeFont(u)),
                  h = t.x + a.x,
                  p = !1
                t.y + a.y + i + d.height > n.getHeight() && ((r.position = 'top'), (p = !0))
                var c = p ? -5 - d.height : i + 10
                h + d.width / 2 > n.getWidth()
                  ? ((r.position = ['100%', c]), (u.align = 'right'))
                  : h - d.width / 2 < 0 && ((r.position = [0, c]), (u.align = 'left'))
              }
            }))
      }
      function d(d, h) {
        var p,
          c = u[d],
          f = u[h],
          g = s[c],
          v = new bt(g, t, t.ecModel)
        if ((o && null != o.newTitle && o.featureName === c && (g.title = o.newTitle), c && !f)) {
          if (
            (function (t) {
              return 0 === t.indexOf('my')
            })(c)
          )
            p = { onclick: v.option.onclick, featureName: c }
          else {
            var m = xo(c)
            if (!m) return
            p = new m()
          }
          l[c] = p
        } else if (!(p = l[f])) return
        ;((p.uid = St('toolbox-feature')), (p.model = v), (p.ecModel = e), (p.api = n))
        var x = p instanceof vo
        c || !f
          ? !v.get('show') || (x && p.unusable)
            ? x && p.remove && p.remove(e, n)
            : (!(function (o, s, l) {
                var u,
                  d,
                  h = o.getModel('iconStyle'),
                  p = o.getModel(['emphasis', 'iconStyle']),
                  c = s instanceof vo && s.getIcons ? s.getIcons() : o.get('icon'),
                  f = o.get('title') || {}
                G(c) ? ((u = {})[l] = c) : (u = c)
                G(f) ? ((d = {})[l] = f) : (d = f)
                var g = (o.iconPaths = {})
                y(u, function (l, u) {
                  var c = It(l, {}, { x: -i / 2, y: -i / 2, width: i, height: i })
                  ;(c.setStyle(h.getItemStyle()),
                    (c.ensureState('emphasis').style = p.getItemStyle()))
                  var f = new R({
                    style: {
                      text: d[u],
                      align: p.get('textAlign'),
                      borderRadius: p.get('textBorderRadius'),
                      padding: p.get('textPadding'),
                      fill: null
                    },
                    ignore: !0
                  })
                  ;(c.setTextContent(f),
                    At({
                      el: c,
                      componentModel: t,
                      itemName: u,
                      formatterParamsExtra: { title: d[u] }
                    }),
                    (c.__title = d[u]),
                    c
                      .on('mouseover', function () {
                        var e = p.getItemStyle(),
                          o = r
                            ? null == t.get('right') && 'right' !== t.get('left')
                              ? 'right'
                              : 'left'
                            : null == t.get('bottom') && 'bottom' !== t.get('top')
                              ? 'bottom'
                              : 'top'
                        ;(f.setStyle({
                          fill: p.get('textFill') || e.fill || e.stroke || '#000',
                          backgroundColor: p.get('textBackgroundColor')
                        }),
                          c.setTextConfig({ position: p.get('textPosition') || o }),
                          (f.ignore = !t.get('showTitle')),
                          n.enterEmphasis(this))
                      })
                      .on('mouseout', function () {
                        ;('emphasis' !== o.get(['iconStatus', u]) && n.leaveEmphasis(this),
                          f.hide())
                      }),
                    ('emphasis' === o.get(['iconStatus', u]) ? I : A)(c),
                    a.add(c),
                    c.on('click', Ct(s.onclick, s, e, n, u)),
                    (g[u] = c))
                })
              })(v, p, c),
              (v.setIconStatus = function (t, e) {
                var n = this.option,
                  o = this.iconPaths
                ;((n.iconStatus = n.iconStatus || {}),
                  (n.iconStatus[t] = e),
                  o[t] && ('emphasis' === e ? I : A)(o[t]))
              }),
              p instanceof vo && p.render && p.render(v, e, n, o))
          : x && p.dispose && p.dispose(e, n)
      }
    }),
    (n.prototype.updateView = function (t, e, n, o) {
      y(this._features, function (t) {
        t instanceof vo && t.updateView && t.updateView(t.model, e, n, o)
      })
    }),
    (n.prototype.remove = function (t, e) {
      ;(y(this._features, function (n) {
        n instanceof vo && n.remove && n.remove(t, e)
      }),
        this.group.removeAll())
    }),
    (n.prototype.dispose = function (t, e) {
      y(this._features, function (n) {
        n instanceof vo && n.dispose && n.dispose(t, e)
      })
    }),
    (n.type = 'toolbox'),
    n
  )
})(ft)
const wo = (function (e) {
  function n() {
    return (null !== e && e.apply(this, arguments)) || this
  }
  return (
    t(n, e),
    (n.prototype.onclick = function (t, e) {
      var n = this.model,
        o = n.get('name') || t.get('title.0.text') || 'echarts',
        a = 'svg' === e.getZr().painter.getType(),
        i = a ? 'svg' : n.get('type', !0) || 'png',
        r = e.getConnectedDataURL({
          type: i,
          backgroundColor: n.get('backgroundColor', !0) || t.get('backgroundColor') || '#fff',
          connectedBackgroundColor: n.get('connectedBackgroundColor'),
          excludeComponents: n.get('excludeComponents'),
          pixelRatio: n.get('pixelRatio')
        }),
        s = Pt.browser
      if (W(MouseEvent) && (s.newEdge || (!s.ie && !s.edge))) {
        var l = document.createElement('a')
        ;((l.download = o + '.' + i), (l.target = '_blank'), (l.href = r))
        var u = new MouseEvent('click', { view: document.defaultView, bubbles: !0, cancelable: !1 })
        l.dispatchEvent(u)
      } else if (window.navigator.msSaveOrOpenBlob || a) {
        var d = r.split(','),
          h = d[0].indexOf('base64') > -1,
          p = a ? decodeURIComponent(d[1]) : d[1]
        h && (p = window.atob(p))
        var c = o + '.' + i
        if (window.navigator.msSaveOrOpenBlob) {
          for (var f = p.length, g = new Uint8Array(f); f--; ) g[f] = p.charCodeAt(f)
          var v = new Blob([g])
          window.navigator.msSaveOrOpenBlob(v, c)
        } else {
          var y = document.createElement('iframe')
          document.body.appendChild(y)
          var m = y.contentWindow,
            x = m.document
          ;(x.open('image/svg+xml', 'replace'),
            x.write(p),
            x.close(),
            m.focus(),
            x.execCommand('SaveAs', !0, c),
            document.body.removeChild(y))
        }
      } else {
        var _ = n.get('lang'),
          M =
            '<body style="margin:0;"><img src="' +
            r +
            '" style="max-width:100%;" title="' +
            ((_ && _[0]) || '') +
            '" /></body>',
          w = window.open()
        ;(w.document.write(M), (w.document.title = o))
      }
    }),
    (n.getDefaultOption = function (t) {
      return {
        show: !0,
        icon: 'M4.7,22.9L29.3,45.5L54.7,23.4M4.6,43.6L4.6,58L53.8,58L53.8,43.6M29.2,45.1L29.2,0',
        title: t.getLocaleModel().get(['toolbox', 'saveAsImage', 'title']),
        type: 'png',
        connectedBackgroundColor: '#fff',
        name: '',
        excludeComponents: ['toolbox'],
        lang: t.getLocaleModel().get(['toolbox', 'saveAsImage', 'lang'])
      }
    }),
    n
  )
})(vo)
var bo = '__ec_magicType_stack__',
  So = [['line', 'bar'], ['stack']],
  Io = (function (e) {
    function n() {
      return (null !== e && e.apply(this, arguments)) || this
    }
    return (
      t(n, e),
      (n.prototype.getIcons = function () {
        var t = this.model,
          e = t.get('icon'),
          n = {}
        return (
          y(t.get('type'), function (t) {
            e[t] && (n[t] = e[t])
          }),
          n
        )
      }),
      (n.getDefaultOption = function (t) {
        return {
          show: !0,
          type: [],
          icon: {
            line: 'M4.1,28.9h7.1l9.3-22l7.4,38l9.7-19.7l3,12.8h14.9M4.1,58h51.4',
            bar: 'M6.7,22.9h10V48h-10V22.9zM24.9,13h10v35h-10V13zM43.2,2h10v46h-10V2zM3.1,58h53.7',
            stack:
              'M8.2,38.4l-8.4,4.1l30.6,15.3L60,42.5l-8.1-4.1l-21.5,11L8.2,38.4z M51.9,30l-8.1,4.2l-13.4,6.9l-13.9-6.9L8.2,30l-8.4,4.2l8.4,4.2l22.2,11l21.5-11l8.1-4.2L51.9,30z M51.9,21.7l-8.1,4.2L35.7,30l-5.3,2.8L24.9,30l-8.4-4.1l-8.3-4.2l-8.4,4.2L8.2,30l8.3,4.2l13.9,6.9l13.4-6.9l8.1-4.2l8.1-4.1L51.9,21.7zM30.4,2.2L-0.2,17.5l8.4,4.1l8.3,4.2l8.4,4.2l5.5,2.7l5.3-2.7l8.1-4.2l8.1-4.2l8.1-4.1L30.4,2.2z'
          },
          title: t.getLocaleModel().get(['toolbox', 'magicType', 'title']),
          option: {},
          seriesIndex: {}
        }
      }),
      (n.prototype.onclick = function (t, e, n) {
        var o = this.model,
          a = o.get(['seriesIndex', n])
        if (Ao[n]) {
          var i,
            r = { series: [] }
          ;(y(So, function (t) {
            ut(t, n) >= 0 &&
              y(t, function (t) {
                o.setIconStatus(t, 'normal')
              })
          }),
            o.setIconStatus(n, 'emphasis'),
            t.eachComponent(
              { mainType: 'series', query: null == a ? null : { seriesIndex: a } },
              function (t) {
                var e = t.subType,
                  a = t.id,
                  i = Ao[n](e, a, t, o)
                i && (Rt(i, t.option), r.series.push(i))
                var s = t.coordinateSystem
                if (s && 'cartesian2d' === s.type && ('line' === n || 'bar' === n)) {
                  var l = s.getAxesByScale('ordinal')[0]
                  if (l) {
                    var u = l.dim + 'Axis',
                      d = t.getReferringComponents(u, pt).models[0].componentIndex
                    r[u] = r[u] || []
                    for (var h = 0; h <= d; h++) r[u][d] = r[u][d] || {}
                    r[u][d].boundaryGap = 'bar' === n
                  }
                }
              }
            ))
          var s = n
          ;('stack' === n &&
            ((i = dt({ stack: o.option.title.tiled, tiled: o.option.title.stack }, o.option.title)),
            'emphasis' !== o.get(['iconStatus', n]) && (s = 'tiled')),
            e.dispatchAction({
              type: 'changeMagicType',
              currentType: s,
              newOption: r,
              newTitle: i,
              featureName: 'magicType'
            }))
        }
      }),
      n
    )
  })(vo),
  Ao = {
    line: function (t, e, n, o) {
      if ('bar' === t)
        return dt(
          {
            id: e,
            type: 'line',
            data: n.get('data'),
            stack: n.get('stack'),
            markPoint: n.get('markPoint'),
            markLine: n.get('markLine')
          },
          o.get(['option', 'line']) || {},
          !0
        )
    },
    bar: function (t, e, n, o) {
      if ('line' === t)
        return dt(
          {
            id: e,
            type: 'bar',
            data: n.get('data'),
            stack: n.get('stack'),
            markPoint: n.get('markPoint'),
            markLine: n.get('markLine')
          },
          o.get(['option', 'bar']) || {},
          !0
        )
    },
    stack: function (t, e, n, o) {
      var a = n.get('stack') === bo
      if ('line' === t || 'bar' === t)
        return (
          o.setIconStatus('stack', a ? 'normal' : 'emphasis'),
          dt({ id: e, stack: a ? '' : bo }, o.get(['option', 'stack']) || {}, !0)
        )
    }
  }
kt(
  { type: 'changeMagicType', event: 'magicTypeChanged', update: 'prepareAndUpdate' },
  function (t, e) {
    e.mergeOption(t.newOption)
  }
)
const Co = Io
var To = new Array(60).join('-'),
  Do = '\t'
function Lo(t) {
  return t.replace(/^\s\s*/, '').replace(/\s\s*$/, '')
}
var Po = new RegExp('[' + Do + ']+', 'g')
function ko(t, e) {
  var n = t.split(new RegExp('\n*' + To + '\n*', 'g')),
    o = { series: [] }
  return (
    y(n, function (t, n) {
      if (
        (function (t) {
          if (t.slice(0, t.indexOf('\n')).indexOf(Do) >= 0) return !0
        })(t)
      ) {
        var a = (function (t) {
            for (
              var e = t.split(/\n+/g),
                n = Lo(e.shift()).split(Po),
                o = [],
                a = rt(n, function (t) {
                  return { name: t, data: [] }
                }),
                i = 0;
              i < e.length;
              i++
            ) {
              var r = Lo(e[i]).split(Po)
              o.push(r.shift())
              for (var s = 0; s < r.length; s++) a[s] && (a[s].data[i] = r[s])
            }
            return { series: a, categories: o }
          })(t),
          i = e[n],
          r = i.axisDim + 'Axis'
        i &&
          ((o[r] = o[r] || []),
          (o[r][i.axisIndex] = { data: a.categories }),
          (o.series = o.series.concat(a.series)))
      } else {
        a = (function (t) {
          for (var e = t.split(/\n+/g), n = Lo(e.shift()), o = [], a = 0; a < e.length; a++) {
            var i = Lo(e[a])
            if (i) {
              var r = i.split(Po),
                s = '',
                l = void 0,
                u = !1
              isNaN(r[0])
                ? ((u = !0),
                  (s = r[0]),
                  (r = r.slice(1)),
                  (o[a] = { name: s, value: [] }),
                  (l = o[a].value))
                : (l = o[a] = [])
              for (var d = 0; d < r.length; d++) l.push(+r[d])
              1 === l.length && (u ? (o[a].value = l[0]) : (o[a] = l[0]))
            }
          }
          return { name: n, data: o }
        })(t)
        o.series.push(a)
      }
    }),
    o
  )
}
var Ro = (function (e) {
  function n() {
    return (null !== e && e.apply(this, arguments)) || this
  }
  return (
    t(n, e),
    (n.prototype.onclick = function (t, e) {
      setTimeout(function () {
        e.dispatchAction({ type: 'hideTip' })
      })
      var n = e.getDom(),
        o = this.model
      this._dom && n.removeChild(this._dom)
      var a = document.createElement('div')
      ;((a.style.cssText = 'position:absolute;top:0;bottom:0;left:0;right:0;padding:5px'),
        (a.style.backgroundColor = o.get('backgroundColor') || '#fff'))
      var i = document.createElement('h4'),
        r = o.get('lang') || []
      ;((i.innerHTML = r[0] || o.get('title')),
        (i.style.cssText = 'margin:10px 20px'),
        (i.style.color = o.get('textColor')))
      var s = document.createElement('div'),
        l = document.createElement('textarea')
      s.style.cssText = 'overflow:auto'
      var u = o.get('optionToContent'),
        d = o.get('contentToOption'),
        h = (function (t) {
          var e,
            n,
            o,
            a = (function (t) {
              var e = {},
                n = [],
                o = []
              return (
                t.eachRawSeries(function (t) {
                  var a = t.coordinateSystem
                  if (!a || ('cartesian2d' !== a.type && 'polar' !== a.type)) n.push(t)
                  else {
                    var i = a.getBaseAxis()
                    if ('category' === i.type) {
                      var r = i.dim + '_' + i.index
                      ;(e[r] ||
                        ((e[r] = { categoryAxis: i, valueAxis: a.getOtherAxis(i), series: [] }),
                        o.push({ axisDim: i.dim, axisIndex: i.index })),
                        e[r].series.push(t))
                    } else n.push(t)
                  }
                }),
                { seriesGroupByCategoryAxis: e, other: n, meta: o }
              )
            })(t)
          return {
            value: Et(
              [
                ((n = a.seriesGroupByCategoryAxis),
                (o = []),
                y(n, function (t, e) {
                  var n = t.categoryAxis,
                    a = t.valueAxis.dim,
                    i = [' '].concat(
                      rt(t.series, function (t) {
                        return t.name
                      })
                    ),
                    r = [n.model.getCategories()]
                  y(t.series, function (t) {
                    var e = t.getRawData()
                    r.push(
                      t.getRawData().mapArray(e.mapDimension(a), function (t) {
                        return t
                      })
                    )
                  })
                  for (var s = [i.join(Do)], l = 0; l < r[0].length; l++) {
                    for (var u = [], d = 0; d < r.length; d++) u.push(r[d][l])
                    s.push(u.join(Do))
                  }
                  o.push(s.join('\n'))
                }),
                o.join('\n\n' + To + '\n\n')),
                ((e = a.other),
                rt(e, function (t) {
                  var e = t.getRawData(),
                    n = [t.name],
                    o = []
                  return (
                    e.each(e.dimensions, function () {
                      for (
                        var t = arguments.length, a = arguments[t - 1], i = e.getName(a), r = 0;
                        r < t - 1;
                        r++
                      )
                        o[r] = arguments[r]
                      n.push((i ? i + Do : '') + o.join(Do))
                    }),
                    n.join('\n')
                  )
                }).join('\n\n' + To + '\n\n'))
              ],
              function (t) {
                return !!t.replace(/[\n\t\s]/g, '')
              }
            ).join('\n\n' + To + '\n\n'),
            meta: a.meta
          }
        })(t)
      if (W(u)) {
        var p = u(e.getOption())
        G(p) ? (s.innerHTML = p) : zt(p) && s.appendChild(p)
      } else {
        l.readOnly = o.get('readOnly')
        var c = l.style
        ;((c.cssText =
          'display:block;width:100%;height:100%;font-family:monospace;font-size:14px;line-height:1.6rem;resize:none;box-sizing:border-box;outline:none'),
          (c.color = o.get('textColor')),
          (c.borderColor = o.get('textareaBorderColor')),
          (c.backgroundColor = o.get('textareaColor')),
          (l.value = h.value),
          s.appendChild(l))
      }
      var f = h.meta,
        g = document.createElement('div')
      g.style.cssText = 'position:absolute;bottom:5px;left:0;right:0'
      var v =
          'float:right;margin-right:20px;border:none;cursor:pointer;padding:2px 5px;font-size:12px;border-radius:3px',
        m = document.createElement('div'),
        x = document.createElement('div')
      ;((v += ';background-color:' + o.get('buttonColor')),
        (v += ';color:' + o.get('buttonTextColor')))
      var _ = this
      function M() {
        ;(n.removeChild(a), (_._dom = null))
      }
      ;(Ot(m, 'click', M),
        Ot(x, 'click', function () {
          if ((null == d && null != u) || (null != d && null == u)) M()
          else {
            var t
            try {
              t = W(d) ? d(s, e.getOption()) : ko(l.value, f)
            } catch (n) {
              throw (M(), new Error('Data view format error ' + n))
            }
            ;(t && e.dispatchAction({ type: 'changeDataView', newOption: t }), M())
          }
        }),
        (m.innerHTML = r[1]),
        (x.innerHTML = r[2]),
        (x.style.cssText = m.style.cssText = v),
        !o.get('readOnly') && g.appendChild(x),
        g.appendChild(m),
        a.appendChild(i),
        a.appendChild(s),
        a.appendChild(g),
        (s.style.height = n.clientHeight - 80 + 'px'),
        n.appendChild(a),
        (this._dom = a))
    }),
    (n.prototype.remove = function (t, e) {
      this._dom && e.getDom().removeChild(this._dom)
    }),
    (n.prototype.dispose = function (t, e) {
      this.remove(t, e)
    }),
    (n.getDefaultOption = function (t) {
      return {
        show: !0,
        readOnly: !1,
        optionToContent: null,
        contentToOption: null,
        icon: 'M17.5,17.3H33 M17.5,17.3H33 M45.4,29.5h-28 M11.5,2v56H51V14.8L38.4,2H11.5z M38.4,2.2v12.7H51 M45.4,41.7h-28',
        title: t.getLocaleModel().get(['toolbox', 'dataView', 'title']),
        lang: t.getLocaleModel().get(['toolbox', 'dataView', 'lang']),
        backgroundColor: '#fff',
        textColor: '#000',
        textareaColor: '#fff',
        textareaBorderColor: '#333',
        buttonColor: '#c23531',
        buttonTextColor: '#fff'
      }
    }),
    n
  )
})(vo)
function zo(t, e) {
  return rt(t, function (t, n) {
    var o = e && e[n]
    if (Vt(o) && !b(o)) {
      ;(Vt(t) && !b(t)) || (t = { value: t })
      var a = null != o.name && null == t.name
      return ((t = Rt(t, o)), a && delete t.name, t)
    }
    return t
  })
}
kt(
  { type: 'changeDataView', event: 'dataViewChanged', update: 'prepareAndUpdate' },
  function (t, e) {
    var n = []
    ;(y(t.newOption.series, function (t) {
      var o = e.getSeriesByName(t.name)[0]
      if (o) {
        var a = o.get('data')
        n.push({ name: t.name, data: zo(t.data, a) })
      } else n.push(Z({ type: 'scatter' }, t))
    }),
      e.mergeOption(Rt({ series: n }, t.newOption)))
  }
)
const Oo = Ro
var Eo = y,
  Vo = Zt()
function Zo(t) {
  var e = Vo(t)
  return (e.snapshots || (e.snapshots = [{}]), e.snapshots)
}
var No = (function (e) {
  function n() {
    return (null !== e && e.apply(this, arguments)) || this
  }
  return (
    t(n, e),
    (n.prototype.onclick = function (t, e) {
      ;(!(function (t) {
        Vo(t).snapshots = null
      })(t),
        e.dispatchAction({ type: 'restore', from: this.uid }))
    }),
    (n.getDefaultOption = function (t) {
      return {
        show: !0,
        icon: 'M3.8,33.4 M47,18.9h9.8V8.7 M56.3,20.1 C52.1,9,40.5,0.6,26.8,2.1C12.6,3.7,1.6,16.2,2.1,30.6 M13,41.1H3.1v10.2 M3.7,39.9c4.2,11.1,15.8,19.5,29.5,18 c14.2-1.6,25.2-14.1,24.7-28.5',
        title: t.getLocaleModel().get(['toolbox', 'restore', 'title'])
      }
    }),
    n
  )
})(vo)
kt({ type: 'restore', event: 'restore', update: 'prepareAndUpdate' }, function (t, e) {
  e.resetOption('recreate')
})
const Bo = No
var Fo = ['grid', 'xAxis', 'yAxis', 'geo', 'graph', 'polar', 'radiusAxis', 'angleAxis', 'bmap'],
  Go = (function () {
    function t(t, e, n) {
      var o = this
      this._targetInfoList = []
      var a = Ho(e, t)
      y(Uo, function (t, e) {
        ;(!n || !n.include || ut(n.include, e) >= 0) && t(a, o._targetInfoList)
      })
    }
    return (
      (t.prototype.setOutputRanges = function (t, e) {
        return (
          this.matchOutputRanges(t, e, function (t, e, n) {
            if (((t.coordRanges || (t.coordRanges = [])).push(e), !t.coordRange)) {
              t.coordRange = e
              var o = jo[t.brushType](0, n, e)
              t.__rangeOffset = {
                offset: Ko[t.brushType](o.values, t.range, [1, 1]),
                xyMinMax: o.xyMinMax
              }
            }
          }),
          t
        )
      }),
      (t.prototype.matchOutputRanges = function (t, e, n) {
        y(
          t,
          function (t) {
            var o = this.findTargetInfo(t, e)
            o &&
              !0 !== o &&
              y(o.coordSyses, function (o) {
                var a = jo[t.brushType](1, o, t.range, !0)
                n(t, a.values, o, e)
              })
          },
          this
        )
      }),
      (t.prototype.setInputRanges = function (t, e) {
        y(
          t,
          function (t) {
            var n,
              o,
              a,
              i,
              r,
              s = this.findTargetInfo(t, e)
            if (((t.range = t.range || []), s && !0 !== s)) {
              t.panelId = s.panelId
              var l = jo[t.brushType](0, s.coordSys, t.coordRange),
                u = t.__rangeOffset
              t.range = u
                ? Ko[t.brushType](
                    l.values,
                    u.offset,
                    ((n = l.xyMinMax),
                    (o = u.xyMinMax),
                    (a = Qo(n)),
                    (i = Qo(o)),
                    (r = [a[0] / i[0], a[1] / i[1]]),
                    isNaN(r[0]) && (r[0] = 1),
                    isNaN(r[1]) && (r[1] = 1),
                    r)
                  )
                : l.values
            }
          },
          this
        )
      }),
      (t.prototype.makePanelOpts = function (t, e) {
        return rt(this._targetInfoList, function (n) {
          var o = n.getPanelRect()
          return {
            panelId: n.panelId,
            defaultBrushType: e ? e(n) : null,
            clipPath: Nt(o),
            isTargetByCursor: Bt(o, t, n.coordSysModel),
            getLinearBrushOtherExtent: Ft(o)
          }
        })
      }),
      (t.prototype.controlSeries = function (t, e, n) {
        var o = this.findTargetInfo(t, n)
        return !0 === o || (o && ut(o.coordSyses, e.coordinateSystem) >= 0)
      }),
      (t.prototype.findTargetInfo = function (t, e) {
        for (var n = this._targetInfoList, o = Ho(e, t), a = 0; a < n.length; a++) {
          var i = n[a],
            r = t.panelId
          if (r) {
            if (i.panelId === r) return i
          } else for (var s = 0; s < Yo.length; s++) if (Yo[s](o, i)) return i
        }
        return !0
      }),
      t
    )
  })()
function Wo(t) {
  return (t[0] > t[1] && t.reverse(), t)
}
function Ho(t, e) {
  return Gt(t, e, { includeMainTypes: Fo })
}
var Uo = {
    grid: function (t, e) {
      var n = t.xAxisModels,
        o = t.yAxisModels,
        a = t.gridModels,
        i = lt(),
        r = {},
        s = {}
      ;(n || o || a) &&
        (y(n, function (t) {
          var e = t.axis.grid.model
          ;(i.set(e.id, e), (r[e.id] = !0))
        }),
        y(o, function (t) {
          var e = t.axis.grid.model
          ;(i.set(e.id, e), (s[e.id] = !0))
        }),
        y(a, function (t) {
          ;(i.set(t.id, t), (r[t.id] = !0), (s[t.id] = !0))
        }),
        i.each(function (t) {
          var a = t.coordinateSystem,
            i = []
          ;(y(a.getCartesians(), function (t, e) {
            ;(ut(n, t.getAxis('x').model) >= 0 || ut(o, t.getAxis('y').model) >= 0) && i.push(t)
          }),
            e.push({
              panelId: 'grid--' + t.id,
              gridModel: t,
              coordSysModel: t,
              coordSys: i[0],
              coordSyses: i,
              getPanelRect: Xo.grid,
              xAxisDeclared: r[t.id],
              yAxisDeclared: s[t.id]
            }))
        }))
    },
    geo: function (t, e) {
      y(t.geoModels, function (t) {
        var n = t.coordinateSystem
        e.push({
          panelId: 'geo--' + t.id,
          geoModel: t,
          coordSysModel: t,
          coordSys: n,
          coordSyses: [n],
          getPanelRect: Xo.geo
        })
      })
    }
  },
  Yo = [
    function (t, e) {
      var n = t.xAxisModel,
        o = t.yAxisModel,
        a = t.gridModel
      return (
        !a && n && (a = n.axis.grid.model),
        !a && o && (a = o.axis.grid.model),
        a && a === e.gridModel
      )
    },
    function (t, e) {
      var n = t.geoModel
      return n && n === e.geoModel
    }
  ],
  Xo = {
    grid: function () {
      return this.coordSys.master.getRect().clone()
    },
    geo: function () {
      var t = this.coordSys,
        e = t.getBoundingRect().clone()
      return (e.applyTransform(Wt(t)), e)
    }
  },
  jo = {
    lineX: wt(qo, 0),
    lineY: wt(qo, 1),
    rect: function (t, e, n, o) {
      var a = t ? e.pointToData([n[0][0], n[1][0]], o) : e.dataToPoint([n[0][0], n[1][0]], o),
        i = t ? e.pointToData([n[0][1], n[1][1]], o) : e.dataToPoint([n[0][1], n[1][1]], o),
        r = [Wo([a[0], i[0]]), Wo([a[1], i[1]])]
      return { values: r, xyMinMax: r }
    },
    polygon: function (t, e, n, o) {
      var a = [
        [1 / 0, -1 / 0],
        [1 / 0, -1 / 0]
      ]
      return {
        values: rt(n, function (n) {
          var i = t ? e.pointToData(n, o) : e.dataToPoint(n, o)
          return (
            (a[0][0] = Math.min(a[0][0], i[0])),
            (a[1][0] = Math.min(a[1][0], i[1])),
            (a[0][1] = Math.max(a[0][1], i[0])),
            (a[1][1] = Math.max(a[1][1], i[1])),
            i
          )
        }),
        xyMinMax: a
      }
    }
  }
function qo(t, e, n, o) {
  var a = n.getAxis(['x', 'y'][t]),
    i = Wo(
      rt([0, 1], function (t) {
        return e ? a.coordToData(a.toLocalCoord(o[t]), !0) : a.toGlobalCoord(a.dataToCoord(o[t]))
      })
    ),
    r = []
  return ((r[t] = i), (r[1 - t] = [NaN, NaN]), { values: i, xyMinMax: r })
}
var Ko = {
  lineX: wt($o, 0),
  lineY: wt($o, 1),
  rect: function (t, e, n) {
    return [
      [t[0][0] - n[0] * e[0][0], t[0][1] - n[0] * e[0][1]],
      [t[1][0] - n[1] * e[1][0], t[1][1] - n[1] * e[1][1]]
    ]
  },
  polygon: function (t, e, n) {
    return rt(t, function (t, o) {
      return [t[0] - n[0] * e[o][0], t[1] - n[1] * e[o][1]]
    })
  }
}
function $o(t, e, n, o) {
  return [e[0] - o[t] * n[0], e[1] - o[t] * n[1]]
}
function Qo(t) {
  return t ? [t[0][1] - t[0][0], t[1][1] - t[1][0]] : [NaN, NaN]
}
const Jo = Go
var ta = y,
  ea = Yt('toolbox-dataZoom_'),
  na = (function (e) {
    function n() {
      return (null !== e && e.apply(this, arguments)) || this
    }
    return (
      t(n, e),
      (n.prototype.render = function (t, e, n, o) {
        ;(this._brushController ||
          ((this._brushController = new Ht(n.getZr())),
          this._brushController.on('brush', Ct(this._onBrush, this)).mount()),
          (function (t, e, n, o, a) {
            var i = n._isZoomActive
            o &&
              'takeGlobalCursor' === o.type &&
              (i = 'dataZoomSelect' === o.key && o.dataZoomSelectActive)
            ;((n._isZoomActive = i), t.setIconStatus('zoom', i ? 'emphasis' : 'normal'))
            var r = new Jo(aa(t), e, { include: ['grid'] }),
              s = r.makePanelOpts(a, function (t) {
                return t.xAxisDeclared && !t.yAxisDeclared
                  ? 'lineX'
                  : !t.xAxisDeclared && t.yAxisDeclared
                    ? 'lineY'
                    : 'rect'
              })
            n._brushController
              .setPanels(s)
              .enableBrush(
                !(!i || !s.length) && {
                  brushType: 'auto',
                  brushStyle: t.getModel('brushStyle').getItemStyle()
                }
              )
          })(t, e, this, o, n),
          (function (t, e) {
            t.setIconStatus(
              'back',
              (function (t) {
                return Zo(t).length
              })(e) > 1
                ? 'emphasis'
                : 'normal'
            )
          })(t, e))
      }),
      (n.prototype.onclick = function (t, e, n) {
        oa[n].call(this)
      }),
      (n.prototype.remove = function (t, e) {
        this._brushController && this._brushController.unmount()
      }),
      (n.prototype.dispose = function (t, e) {
        this._brushController && this._brushController.dispose()
      }),
      (n.prototype._onBrush = function (t) {
        var e = t.areas
        if (t.isEnd && e.length) {
          var n = {},
            o = this.ecModel
          ;(this._brushController.updateCovers([]),
            new Jo(aa(this.model), o, { include: ['grid'] }).matchOutputRanges(
              e,
              o,
              function (t, e, n) {
                if ('cartesian2d' === n.type) {
                  var o = t.brushType
                  'rect' === o
                    ? (a('x', n, e[0]), a('y', n, e[1]))
                    : a({ lineX: 'x', lineY: 'y' }[o], n, e)
                }
              }
            ),
            (function (t, e) {
              var n = Zo(t)
              ;(Eo(e, function (e, o) {
                for (var a = n.length - 1; a >= 0 && !n[a][o]; a--);
                if (a < 0) {
                  var i = t.queryComponents({ mainType: 'dataZoom', subType: 'select', id: o })[0]
                  if (i) {
                    var r = i.getPercentRange()
                    n[0][o] = { dataZoomId: o, start: r[0], end: r[1] }
                  }
                }
              }),
                n.push(e))
            })(o, n),
            this._dispatchZoomAction(n))
        }
        function a(t, e, a) {
          var i = e.getAxis(t),
            r = i.model,
            s = (function (t, e, n) {
              var o
              return (
                n.eachComponent({ mainType: 'dataZoom', subType: 'select' }, function (n) {
                  n.getAxisModel(t, e.componentIndex) && (o = n)
                }),
                o
              )
            })(t, r, o),
            l = s.findRepresentativeAxisProxy(r).getMinMaxSpan()
          ;((null == l.minValueSpan && null == l.maxValueSpan) ||
            (a = vt(0, a.slice(), i.scale.getExtent(), 0, l.minValueSpan, l.maxValueSpan)),
            s && (n[s.id] = { dataZoomId: s.id, startValue: a[0], endValue: a[1] }))
        }
      }),
      (n.prototype._dispatchZoomAction = function (t) {
        var e = []
        ;(ta(t, function (t, n) {
          e.push(gt(t))
        }),
          e.length && this.api.dispatchAction({ type: 'dataZoom', from: this.uid, batch: e }))
      }),
      (n.getDefaultOption = function (t) {
        return {
          show: !0,
          filterMode: 'filter',
          icon: {
            zoom: 'M0,13.5h26.9 M13.5,26.9V0 M32.1,13.5H58V58H13.5 V32.1',
            back: 'M22,1.4L9.9,13.5l12.3,12.3 M10.3,13.5H54.9v44.6 H10.3v-26'
          },
          title: t.getLocaleModel().get(['toolbox', 'dataZoom', 'title']),
          brushStyle: { borderWidth: 0, color: 'rgba(210,219,238,0.2)' }
        }
      }),
      n
    )
  })(vo),
  oa = {
    zoom: function () {
      var t = !this._isZoomActive
      this.api.dispatchAction({
        type: 'takeGlobalCursor',
        key: 'dataZoomSelect',
        dataZoomSelectActive: t
      })
    },
    back: function () {
      this._dispatchZoomAction(
        (function (t) {
          var e = Zo(t),
            n = e[e.length - 1]
          e.length > 1 && e.pop()
          var o = {}
          return (
            Eo(n, function (t, n) {
              for (var a = e.length - 1; a >= 0; a--)
                if ((t = e[a][n])) {
                  o[n] = t
                  break
                }
            }),
            o
          )
        })(this.ecModel)
      )
    }
  }
function aa(t) {
  var e = {
    xAxisIndex: t.get('xAxisIndex', !0),
    yAxisIndex: t.get('yAxisIndex', !0),
    xAxisId: t.get('xAxisId', !0),
    yAxisId: t.get('yAxisId', !0)
  }
  return (
    null == e.xAxisIndex && null == e.xAxisId && (e.xAxisIndex = 'all'),
    null == e.yAxisIndex && null == e.yAxisId && (e.yAxisIndex = 'all'),
    e
  )
}
Ut('dataZoom', function (t) {
  var e = t.getComponent('toolbox', 0),
    n = ['feature', 'dataZoom']
  if (e && null != e.get(n)) {
    var o = e.getModel(n),
      a = [],
      i = aa(o),
      r = Gt(t, i)
    return (
      ta(r.xAxisModels, function (t) {
        return s(t, 'xAxis', 'xAxisIndex')
      }),
      ta(r.yAxisModels, function (t) {
        return s(t, 'yAxis', 'yAxisIndex')
      }),
      a
    )
  }
  function s(t, e, n) {
    var i = t.componentIndex,
      r = {
        type: 'select',
        $fromToolbox: !0,
        filterMode: o.get('filterMode', !0) || 'filter',
        id: ea + e + i
      }
    ;((r[n] = i), a.push(r))
  }
})
const ia = na
const ra = (function (e) {
  function n() {
    var t = (null !== e && e.apply(this, arguments)) || this
    return ((t.type = n.type), t)
  }
  return (
    t(n, e),
    (n.type = 'dataZoom.inside'),
    (n.defaultOption = Xt(ao.defaultOption, {
      disabled: !1,
      zoomLock: !1,
      zoomOnMouseWheel: !0,
      moveOnMouseMove: !0,
      moveOnMouseWheel: !1,
      preventDefaultMouseMove: !0
    })),
    n
  )
})(ao)
var sa = Zt()
function la(t, e) {
  if (e) {
    t.removeKey(e.model.uid)
    var n = e.controller
    n && n.dispose()
  }
}
function ua(t, e) {
  t.isDisposed() ||
    t.dispatchAction({
      type: 'dataZoom',
      animation: { easing: 'cubicOut', duration: 100 },
      batch: e
    })
}
function da(t, e, n, o) {
  return t.coordinateSystem.containPoint([n, o])
}
function ha(t) {
  t.registerProcessor(t.PRIORITY.PROCESSOR.FILTER, function (t, e) {
    var n = sa(e),
      o = n.coordSysRecordMap || (n.coordSysRecordMap = lt())
    ;(o.each(function (t) {
      t.dataZoomInfoMap = null
    }),
      t.eachComponent({ mainType: 'dataZoom', subType: 'inside' }, function (t) {
        var n = eo(t)
        y(n.infoList, function (n) {
          var a = n.model.uid,
            i =
              o.get(a) ||
              o.set(
                a,
                (function (t, e) {
                  var n = {
                      model: e,
                      containsPoint: wt(da, e),
                      dispatchAction: wt(ua, t),
                      dataZoomInfoMap: null,
                      controller: null
                    },
                    o = (n.controller = new qt(t.getZr()))
                  return (
                    y(['pan', 'zoom', 'scrollMove'], function (t) {
                      o.on(t, function (e) {
                        var o = []
                        ;(n.dataZoomInfoMap.each(function (a) {
                          if (e.isAvailableBehavior(a.model.option)) {
                            var i = (a.getRange || {})[t],
                              r = i && i(a.dzReferCoordSysInfo, n.model.mainType, n.controller, e)
                            !a.model.get('disabled', !0) &&
                              r &&
                              o.push({ dataZoomId: a.model.id, start: r[0], end: r[1] })
                          }
                        }),
                          o.length && n.dispatchAction(o))
                      })
                    }),
                    n
                  )
                })(e, n.model)
              )
          ;(i.dataZoomInfoMap || (i.dataZoomInfoMap = lt())).set(t.uid, {
            dzReferCoordSysInfo: n,
            model: t,
            getRange: null
          })
        })
      }),
      o.each(function (t) {
        var e,
          n = t.controller,
          a = t.dataZoomInfoMap
        if (a) {
          var i = a.keys()[0]
          null != i && (e = a.get(i))
        }
        if (e) {
          var r = (function (t) {
            var e,
              n = 'type_',
              o = { type_true: 2, type_move: 1, type_false: 0, type_undefined: -1 },
              a = !0
            return (
              t.each(function (t) {
                var i = t.model,
                  r = !i.get('disabled', !0) && (!i.get('zoomLock', !0) || 'move')
                ;(o[n + r] > o[n + e] && (e = r), (a = a && i.get('preventDefaultMouseMove', !0)))
              }),
              {
                controlType: e,
                opt: {
                  zoomOnMouseWheel: !0,
                  moveOnMouseMove: !0,
                  moveOnMouseWheel: !0,
                  preventDefaultMouseMove: !!a
                }
              }
            )
          })(a)
          ;(n.enable(r.controlType, r.opt),
            n.setPointerChecker(t.containsPoint),
            jt(t, 'dispatchAction', e.model.get('throttle', !0), 'fixRate'))
        } else la(o, t)
      }))
  })
}
var pa = (function (e) {
    function n() {
      var t = (null !== e && e.apply(this, arguments)) || this
      return ((t.type = 'dataZoom.inside'), t)
    }
    return (
      t(n, e),
      (n.prototype.render = function (t, n, o) {
        ;(e.prototype.render.apply(this, arguments),
          t.noTarget()
            ? this._clear()
            : ((this.range = t.getPercentRange()),
              (function (t, e, n) {
                sa(t).coordSysRecordMap.each(function (t) {
                  var o = t.dataZoomInfoMap.get(e.uid)
                  o && (o.getRange = n)
                })
              })(o, t, {
                pan: Ct(ca.pan, this),
                zoom: Ct(ca.zoom, this),
                scrollMove: Ct(ca.scrollMove, this)
              })))
      }),
      (n.prototype.dispose = function () {
        ;(this._clear(), e.prototype.dispose.apply(this, arguments))
      }),
      (n.prototype._clear = function () {
        ;(!(function (t, e) {
          for (var n = sa(t).coordSysRecordMap, o = n.keys(), a = 0; a < o.length; a++) {
            var i = o[a],
              r = n.get(i),
              s = r.dataZoomInfoMap
            if (s) {
              var l = e.uid
              s.get(l) && (s.removeKey(l), s.keys().length || la(n, r))
            }
          }
        })(this.api, this.dataZoomModel),
          (this.range = null))
      }),
      (n.type = 'dataZoom.inside'),
      n
    )
  })(ro),
  ca = {
    zoom: function (t, e, n, o) {
      var a = this.range,
        i = a.slice(),
        r = t.axisModels[0]
      if (r) {
        var s = ga[e](null, [o.originX, o.originY], r, n, t),
          l =
            ((s.signal > 0 ? s.pixelStart + s.pixelLength - s.pixel : s.pixel - s.pixelStart) /
              s.pixelLength) *
              (i[1] - i[0]) +
            i[0],
          u = Math.max(1 / o.scale, 0)
        ;((i[0] = (i[0] - l) * u + l), (i[1] = (i[1] - l) * u + l))
        var d = this.dataZoomModel.findRepresentativeAxisProxy().getMinMaxSpan()
        return (
          vt(0, i, [0, 100], 0, d.minSpan, d.maxSpan),
          (this.range = i),
          a[0] !== i[0] || a[1] !== i[1] ? i : void 0
        )
      }
    },
    pan: fa(function (t, e, n, o, a, i) {
      var r = ga[o]([i.oldX, i.oldY], [i.newX, i.newY], e, a, n)
      return (r.signal * (t[1] - t[0]) * r.pixel) / r.pixelLength
    }),
    scrollMove: fa(function (t, e, n, o, a, i) {
      return (
        ga[o]([0, 0], [i.scrollDelta, i.scrollDelta], e, a, n).signal *
        (t[1] - t[0]) *
        i.scrollDelta
      )
    })
  }
function fa(t) {
  return function (e, n, o, a) {
    var i = this.range,
      r = i.slice(),
      s = e.axisModels[0]
    if (s) {
      var l = t(r, s, e, n, o, a)
      return (
        vt(l, r, [0, 100], 'all'),
        (this.range = r),
        i[0] !== r[0] || i[1] !== r[1] ? r : void 0
      )
    }
  }
}
var ga = {
  grid: function (t, e, n, o, a) {
    var i = n.axis,
      r = {},
      s = a.model.coordinateSystem.getRect()
    return (
      (t = t || [0, 0]),
      'x' === i.dim
        ? ((r.pixel = e[0] - t[0]),
          (r.pixelLength = s.width),
          (r.pixelStart = s.x),
          (r.signal = i.inverse ? 1 : -1))
        : ((r.pixel = e[1] - t[1]),
          (r.pixelLength = s.height),
          (r.pixelStart = s.y),
          (r.signal = i.inverse ? -1 : 1)),
      r
    )
  },
  polar: function (t, e, n, o, a) {
    var i = n.axis,
      r = {},
      s = a.model.coordinateSystem,
      l = s.getRadiusAxis().getExtent(),
      u = s.getAngleAxis().getExtent()
    return (
      (t = t ? s.pointToCoord(t) : [0, 0]),
      (e = s.pointToCoord(e)),
      'radiusAxis' === n.mainType
        ? ((r.pixel = e[0] - t[0]),
          (r.pixelLength = l[1] - l[0]),
          (r.pixelStart = l[0]),
          (r.signal = i.inverse ? 1 : -1))
        : ((r.pixel = e[1] - t[1]),
          (r.pixelLength = u[1] - u[0]),
          (r.pixelStart = u[0]),
          (r.signal = i.inverse ? -1 : 1)),
      r
    )
  },
  singleAxis: function (t, e, n, o, a) {
    var i = n.axis,
      r = a.model.coordinateSystem.getRect(),
      s = {}
    return (
      (t = t || [0, 0]),
      'horizontal' === i.orient
        ? ((s.pixel = e[0] - t[0]),
          (s.pixelLength = r.width),
          (s.pixelStart = r.x),
          (s.signal = i.inverse ? 1 : -1))
        : ((s.pixel = e[1] - t[1]),
          (s.pixelLength = r.height),
          (s.pixelStart = r.y),
          (s.signal = i.inverse ? -1 : 1)),
      s
    )
  }
}
const va = pa
function ya(t) {
  ;(fo(t), t.registerComponentModel(ra), t.registerComponentView(va), ha(t))
}
const ma = (function (e) {
  function n() {
    var t = (null !== e && e.apply(this, arguments)) || this
    return ((t.type = n.type), t)
  }
  return (
    t(n, e),
    (n.type = 'dataZoom.slider'),
    (n.layoutMode = 'box'),
    (n.defaultOption = Xt(ao.defaultOption, {
      show: !0,
      right: 'ph',
      top: 'ph',
      width: 'ph',
      height: 'ph',
      left: null,
      bottom: null,
      borderColor: '#d2dbee',
      borderRadius: 3,
      backgroundColor: 'rgba(47,69,84,0)',
      dataBackground: {
        lineStyle: { color: '#d2dbee', width: 0.5 },
        areaStyle: { color: '#d2dbee', opacity: 0.2 }
      },
      selectedDataBackground: {
        lineStyle: { color: '#8fb0f7', width: 0.5 },
        areaStyle: { color: '#8fb0f7', opacity: 0.2 }
      },
      fillerColor: 'rgba(135,175,274,0.2)',
      handleIcon:
        'path://M-9.35,34.56V42m0-40V9.5m-2,0h4a2,2,0,0,1,2,2v21a2,2,0,0,1-2,2h-4a2,2,0,0,1-2-2v-21A2,2,0,0,1-11.35,9.5Z',
      handleSize: '100%',
      handleStyle: { color: '#fff', borderColor: '#ACB8D1' },
      moveHandleSize: 7,
      moveHandleIcon:
        'path://M-320.9-50L-320.9-50c18.1,0,27.1,9,27.1,27.1V85.7c0,18.1-9,27.1-27.1,27.1l0,0c-18.1,0-27.1-9-27.1-27.1V-22.9C-348-41-339-50-320.9-50z M-212.3-50L-212.3-50c18.1,0,27.1,9,27.1,27.1V85.7c0,18.1-9,27.1-27.1,27.1l0,0c-18.1,0-27.1-9-27.1-27.1V-22.9C-239.4-41-230.4-50-212.3-50z M-103.7-50L-103.7-50c18.1,0,27.1,9,27.1,27.1V85.7c0,18.1-9,27.1-27.1,27.1l0,0c-18.1,0-27.1-9-27.1-27.1V-22.9C-130.9-41-121.8-50-103.7-50z',
      moveHandleStyle: { color: '#D2DBEE', opacity: 0.7 },
      showDetail: !0,
      showDataShadow: 'auto',
      realtime: !0,
      zoomLock: !1,
      textStyle: { color: '#6E7079' },
      brushSelect: !0,
      brushStyle: { color: 'rgba(135,175,274,0.15)' },
      emphasis: { handleStyle: { borderColor: '#8FB0F7' }, moveHandleStyle: { color: '#8FB0F7' } }
    })),
    n
  )
})(ao)
var xa = ee,
  _a = 'horizontal',
  Ma = 'vertical',
  wa = ['line', 'bar', 'candlestick', 'scatter'],
  ba = { easing: 'cubicOut', duration: 100, delay: 0 }
function Sa(t) {
  return 'vertical' === t ? 'ns-resize' : 'ew-resize'
}
const Ia = (function (e) {
  function n() {
    var t = (null !== e && e.apply(this, arguments)) || this
    return ((t.type = n.type), (t._displayables = {}), t)
  }
  return (
    t(n, e),
    (n.prototype.init = function (t, e) {
      ;((this.api = e),
        (this._onBrush = Ct(this._onBrush, this)),
        (this._onBrushEnd = Ct(this._onBrushEnd, this)))
    }),
    (n.prototype.render = function (t, n, o, a) {
      if (
        (e.prototype.render.apply(this, arguments),
        jt(this, '_dispatchZoomAction', t.get('throttle'), 'fixRate'),
        (this._orient = t.getOrient()),
        !1 !== t.get('show'))
      ) {
        if (t.noTarget()) return (this._clear(), void this.group.removeAll())
        ;((a && 'dataZoom' === a.type && a.from === this.uid) || this._buildView(),
          this._updateView())
      } else this.group.removeAll()
    }),
    (n.prototype.dispose = function () {
      ;(this._clear(), e.prototype.dispose.apply(this, arguments))
    }),
    (n.prototype._clear = function () {
      Kt(this, '_dispatchZoomAction')
      var t = this.api.getZr()
      ;(t.off('mousemove', this._onBrush), t.off('mouseup', this._onBrushEnd))
    }),
    (n.prototype._buildView = function () {
      var t = this.group
      ;(t.removeAll(),
        (this._brushing = !1),
        (this._displayables.brushRect = null),
        this._resetLocation(),
        this._resetInterval())
      var e = (this._displayables.sliderGroup = new i())
      ;(this._renderBackground(),
        this._renderHandle(),
        this._renderDataShadow(),
        t.add(e),
        this._positionGroup())
    }),
    (n.prototype._resetLocation = function () {
      var t = this.dataZoomModel,
        e = this.api,
        n = t.get('brushSelect') ? 7 : 0,
        o = this._findCoordRect(),
        a = { width: e.getWidth(), height: e.getHeight() },
        i =
          this._orient === _a
            ? {
                right: a.width - o.x - o.width,
                top: a.height - 30 - 7 - n,
                width: o.width,
                height: 30
              }
            : { right: 7, top: o.y, width: 30, height: o.height },
        r = $t(t.option)
      y(['right', 'top', 'width', 'height'], function (t) {
        'ph' === r[t] && (r[t] = i[t])
      })
      var s = Qt(r, a)
      ;((this._location = { x: s.x, y: s.y }),
        (this._size = [s.width, s.height]),
        this._orient === Ma && this._size.reverse())
    }),
    (n.prototype._positionGroup = function () {
      var t = this.group,
        e = this._location,
        n = this._orient,
        o = this.dataZoomModel.getFirstTargetAxisModel(),
        a = o && o.get('inverse'),
        i = this._displayables.sliderGroup,
        r = (this._dataShadowInfo || {}).otherAxisInverse
      i.attr(
        n !== _a || a
          ? n === _a && a
            ? { scaleY: r ? 1 : -1, scaleX: -1 }
            : n !== Ma || a
              ? { scaleY: r ? -1 : 1, scaleX: -1, rotation: Math.PI / 2 }
              : { scaleY: r ? -1 : 1, scaleX: 1, rotation: Math.PI / 2 }
          : { scaleY: r ? 1 : -1, scaleX: 1 }
      )
      var s = t.getBoundingRect([i])
      ;((t.x = e.x - s.x), (t.y = e.y - s.y), t.markRedraw())
    }),
    (n.prototype._getViewExtent = function () {
      return [0, this._size[0]]
    }),
    (n.prototype._renderBackground = function () {
      var t = this.dataZoomModel,
        e = this._size,
        n = this._displayables.sliderGroup,
        o = t.get('brushSelect')
      n.add(
        new xa({
          silent: !0,
          shape: { x: 0, y: 0, width: e[0], height: e[1] },
          style: { fill: t.get('backgroundColor') },
          z2: -40
        })
      )
      var a = new xa({
          shape: { x: 0, y: 0, width: e[0], height: e[1] },
          style: { fill: 'transparent' },
          z2: 0,
          onclick: Ct(this._onClickPanel, this)
        }),
        i = this.api.getZr()
      ;(o
        ? (a.on('mousedown', this._onBrushStart, this),
          (a.cursor = 'crosshair'),
          i.on('mousemove', this._onBrush),
          i.on('mouseup', this._onBrushEnd))
        : (i.off('mousemove', this._onBrush), i.off('mouseup', this._onBrushEnd)),
        n.add(a))
    }),
    (n.prototype._renderDataShadow = function () {
      var t = (this._dataShadowInfo = this._prepareDataShadowInfo())
      if (((this._displayables.dataShadowSegs = []), t)) {
        var e = this._size,
          n = this._shadowSize || [],
          o = t.series,
          a = o.getRawData(),
          r = o.getShadowDim && o.getShadowDim(),
          s = r && a.getDimensionInfo(r) ? o.getShadowDim() : t.otherDim
        if (null != s) {
          var l = this._shadowPolygonPts,
            u = this._shadowPolylinePts
          if (a !== this._shadowData || s !== this._shadowDim || e[0] !== n[0] || e[1] !== n[1]) {
            var d = a.getDataExtent(s),
              h = 0.3 * (d[1] - d[0])
            d = [d[0] - h, d[1] + h]
            var p,
              c = [0, e[1]],
              f = [0, e[0]],
              g = [
                [e[0], 0],
                [0, 0]
              ],
              v = [],
              y = f[1] / (a.count() - 1),
              m = 0,
              x = Math.round(a.count() / e[0])
            ;(a.each([s], function (t, e) {
              if (x > 0 && e % x) m += y
              else {
                var n = null == t || isNaN(t) || '' === t,
                  o = n ? 0 : O(t, d, c, !0)
                ;(n && !p && e
                  ? (g.push([g[g.length - 1][0], 0]), v.push([v[v.length - 1][0], 0]))
                  : !n && p && (g.push([m, 0]), v.push([m, 0])),
                  g.push([m, o]),
                  v.push([m, o]),
                  (m += y),
                  (p = n))
              }
            }),
              (l = this._shadowPolygonPts = g),
              (u = this._shadowPolylinePts = v))
          }
          ;((this._shadowData = a), (this._shadowDim = s), (this._shadowSize = [e[0], e[1]]))
          for (var _, M, w, b, S, I = this.dataZoomModel, A = 0; A < 3; A++) {
            var C =
              ((_ = 1 === A),
              (M = void 0),
              (w = void 0),
              (b = void 0),
              (S = void 0),
              (M = I.getModel(_ ? 'selectedDataBackground' : 'dataBackground')),
              (w = new i()),
              (b = new re({
                shape: { points: l },
                segmentIgnoreThreshold: 1,
                style: M.getModel('areaStyle').getAreaStyle(),
                silent: !0,
                z2: -20
              })),
              (S = new Q({
                shape: { points: u },
                segmentIgnoreThreshold: 1,
                style: M.getModel('lineStyle').getLineStyle(),
                silent: !0,
                z2: -19
              })),
              w.add(b),
              w.add(S),
              w)
            ;(this._displayables.sliderGroup.add(C), this._displayables.dataShadowSegs.push(C))
          }
        }
      }
    }),
    (n.prototype._prepareDataShadowInfo = function () {
      var t = this.dataZoomModel,
        e = t.get('showDataShadow')
      if (!1 !== e) {
        var n,
          o = this.ecModel
        return (
          t.eachTargetAxis(function (a, i) {
            var r = t.getAxisProxy(a, i).getTargetSeriesModels()
            y(
              r,
              function (t) {
                if (!(n || (!0 !== e && ut(wa, t.get('type')) < 0))) {
                  var r,
                    s = o.getComponent(Jn(a), i).axis,
                    l = { x: 'y', y: 'x', radius: 'angle', angle: 'radius' }[a],
                    u = t.coordinateSystem
                  ;(null != l && u.getOtherAxis && (r = u.getOtherAxis(s).inverse),
                    (l = t.getData().mapDimension(l)),
                    (n = { thisAxis: s, series: t, thisDim: a, otherDim: l, otherAxisInverse: r }))
                }
              },
              this
            )
          }, this),
          n
        )
      }
    }),
    (n.prototype._renderHandle = function () {
      var t = this.group,
        e = this._displayables,
        n = (e.handles = [null, null]),
        o = (e.handleLabels = [null, null]),
        a = this._displayables.sliderGroup,
        i = this._size,
        s = this.dataZoomModel,
        l = this.api,
        u = s.get('borderRadius') || 0,
        d = s.get('brushSelect'),
        h = (e.filler = new xa({
          silent: d,
          style: { fill: s.get('fillerColor') },
          textConfig: { position: 'inside' }
        }))
      ;(a.add(h),
        a.add(
          new xa({
            silent: !0,
            subPixelOptimize: !0,
            shape: { x: 0, y: 0, width: i[0], height: i[1], r: u },
            style: {
              stroke: s.get('dataBackgroundColor') || s.get('borderColor'),
              lineWidth: 1,
              fill: 'rgba(0,0,0,0)'
            }
          })
        ),
        y(
          [0, 1],
          function (e) {
            var i = s.get('handleIcon')
            !Jt[i] && i.indexOf('path://') < 0 && i.indexOf('image://') < 0 && (i = 'path://' + i)
            var l = r(i, -1, 0, 2, 2, null, !0)
            l.attr({
              cursor: Sa(this._orient),
              draggable: !0,
              drift: Ct(this._onDragMove, this, e),
              ondragend: Ct(this._onDragEnd, this),
              onmouseover: Ct(this._showDataInfo, this, !0),
              onmouseout: Ct(this._showDataInfo, this, !1),
              z2: 5
            })
            var u = l.getBoundingRect(),
              d = s.get('handleSize')
            ;((this._handleHeight = k(d, this._size[1])),
              (this._handleWidth = (u.width / u.height) * this._handleHeight),
              l.setStyle(s.getModel('handleStyle').getItemStyle()),
              (l.style.strokeNoScale = !0),
              (l.rectHover = !0),
              (l.ensureState('emphasis').style = s
                .getModel(['emphasis', 'handleStyle'])
                .getItemStyle()),
              te(l))
            var h = s.get('handleColor')
            ;(null != h && (l.style.fill = h), a.add((n[e] = l)))
            var p = s.getModel('textStyle')
            t.add(
              (o[e] = new R({
                silent: !0,
                invisible: !0,
                style: z(p, {
                  x: 0,
                  y: 0,
                  text: '',
                  verticalAlign: 'middle',
                  align: 'center',
                  fill: p.getTextColor(),
                  font: p.getFont()
                }),
                z2: 10
              }))
            )
          },
          this
        ))
      var p = h
      if (d) {
        var c = k(s.get('moveHandleSize'), i[1]),
          f = (e.moveHandle = new ee({
            style: s.getModel('moveHandleStyle').getItemStyle(),
            silent: !0,
            shape: { r: [0, 0, 2, 2], y: i[1] - 0.5, height: c }
          })),
          g = 0.8 * c,
          v = (e.moveHandleIcon = r(s.get('moveHandleIcon'), -g / 2, -g / 2, g, g, '#fff', !0))
        ;((v.silent = !0),
          (v.y = i[1] + c / 2 - 0.5),
          (f.ensureState('emphasis').style = s
            .getModel(['emphasis', 'moveHandleStyle'])
            .getItemStyle()))
        var m = Math.min(i[1] / 2, Math.max(c, 10))
        ;((p = e.moveZone = new ee({ invisible: !0, shape: { y: i[1] - m, height: c + m } }))
          .on('mouseover', function () {
            l.enterEmphasis(f)
          })
          .on('mouseout', function () {
            l.leaveEmphasis(f)
          }),
          a.add(f),
          a.add(v),
          a.add(p))
      }
      p.attr({
        draggable: !0,
        cursor: Sa(this._orient),
        drift: Ct(this._onDragMove, this, 'all'),
        ondragstart: Ct(this._showDataInfo, this, !0),
        ondragend: Ct(this._onDragEnd, this),
        onmouseover: Ct(this._showDataInfo, this, !0),
        onmouseout: Ct(this._showDataInfo, this, !1)
      })
    }),
    (n.prototype._resetInterval = function () {
      var t = (this._range = this.dataZoomModel.getPercentRange()),
        e = this._getViewExtent()
      this._handleEnds = [O(t[0], [0, 100], e, !0), O(t[1], [0, 100], e, !0)]
    }),
    (n.prototype._updateInterval = function (t, e) {
      var n = this.dataZoomModel,
        o = this._handleEnds,
        a = this._getViewExtent(),
        i = n.findRepresentativeAxisProxy().getMinMaxSpan(),
        r = [0, 100]
      vt(
        e,
        o,
        a,
        n.get('zoomLock') ? 'all' : t,
        null != i.minSpan ? O(i.minSpan, r, a, !0) : null,
        null != i.maxSpan ? O(i.maxSpan, r, a, !0) : null
      )
      var s = this._range,
        l = (this._range = _t([O(o[0], a, r, !0), O(o[1], a, r, !0)]))
      return !s || s[0] !== l[0] || s[1] !== l[1]
    }),
    (n.prototype._updateView = function (t) {
      var e = this._displayables,
        n = this._handleEnds,
        o = _t(n.slice()),
        a = this._size
      ;(y(
        [0, 1],
        function (t) {
          var o = e.handles[t],
            i = this._handleHeight
          o.attr({ scaleX: i / 2, scaleY: i / 2, x: n[t] + (t ? -1 : 1), y: a[1] / 2 - i / 2 })
        },
        this
      ),
        e.filler.setShape({ x: o[0], y: 0, width: o[1] - o[0], height: a[1] }))
      var i = { x: o[0], width: o[1] - o[0] }
      e.moveHandle &&
        (e.moveHandle.setShape(i),
        e.moveZone.setShape(i),
        e.moveZone.getBoundingRect(),
        e.moveHandleIcon && e.moveHandleIcon.attr('x', i.x + i.width / 2))
      for (var r = e.dataShadowSegs, s = [0, o[0], o[1], a[0]], l = 0; l < r.length; l++) {
        var u = r[l],
          d = u.getClipPath()
        ;(d || ((d = new ee()), u.setClipPath(d)),
          d.setShape({ x: s[l], y: 0, width: s[l + 1] - s[l], height: a[1] }))
      }
      this._updateDataInfo(t)
    }),
    (n.prototype._updateDataInfo = function (t) {
      var e = this.dataZoomModel,
        n = this._displayables,
        o = n.handleLabels,
        a = this._orient,
        i = ['', '']
      if (e.get('showDetail')) {
        var r = e.findRepresentativeAxisProxy()
        if (r) {
          var s = r.getAxisModel().axis,
            l = this._range,
            u = t
              ? r.calculateDataWindow({ start: l[0], end: l[1] }).valueWindow
              : r.getDataValueWindow()
          i = [this._formatLabel(u[0], s), this._formatLabel(u[1], s)]
        }
      }
      var d = _t(this._handleEnds.slice())
      function h(t) {
        var e = Wt(n.handles[t].parent, this.group),
          r = ne(0 === t ? 'right' : 'left', e),
          s = this._handleWidth / 2 + 5,
          l = oe([d[t] + (0 === t ? -s : s), this._size[1] / 2], e)
        o[t].setStyle({
          x: l[0],
          y: l[1],
          verticalAlign: a === _a ? 'middle' : r,
          align: a === _a ? r : 'center',
          text: i[t]
        })
      }
      ;(h.call(this, 0), h.call(this, 1))
    }),
    (n.prototype._formatLabel = function (t, e) {
      var n = this.dataZoomModel,
        o = n.get('labelFormatter'),
        a = n.get('labelPrecision')
      ;(null != a && 'auto' !== a) || (a = e.getPixelPrecision())
      var i =
        null == t || isNaN(t)
          ? ''
          : 'category' === e.type || 'time' === e.type
            ? e.scale.getLabel({ value: Math.round(t) })
            : t.toFixed(Math.min(a, 20))
      return W(o) ? o(t, i) : G(o) ? o.replace('{value}', i) : i
    }),
    (n.prototype._showDataInfo = function (t) {
      t = this._dragging || t
      var e = this._displayables,
        n = e.handleLabels
      ;(n[0].attr('invisible', !t),
        n[1].attr('invisible', !t),
        e.moveHandle && this.api[t ? 'enterEmphasis' : 'leaveEmphasis'](e.moveHandle, 1))
    }),
    (n.prototype._onDragMove = function (t, e, n, o) {
      ;((this._dragging = !0), ae(o.event))
      var a = this._displayables.sliderGroup.getLocalTransform(),
        i = oe([e, n], a, !0),
        r = this._updateInterval(t, i[0]),
        s = this.dataZoomModel.get('realtime')
      ;(this._updateView(!s), r && s && this._dispatchZoomAction(!0))
    }),
    (n.prototype._onDragEnd = function () {
      ;((this._dragging = !1),
        this._showDataInfo(!1),
        !this.dataZoomModel.get('realtime') && this._dispatchZoomAction(!1))
    }),
    (n.prototype._onClickPanel = function (t) {
      var e = this._size,
        n = this._displayables.sliderGroup.transformCoordToLocal(t.offsetX, t.offsetY)
      if (!(n[0] < 0 || n[0] > e[0] || n[1] < 0 || n[1] > e[1])) {
        var o = this._handleEnds,
          a = (o[0] + o[1]) / 2,
          i = this._updateInterval('all', n[0] - a)
        ;(this._updateView(), i && this._dispatchZoomAction(!1))
      }
    }),
    (n.prototype._onBrushStart = function (t) {
      var e = t.offsetX,
        n = t.offsetY
      ;((this._brushStart = new ie(e, n)),
        (this._brushing = !0),
        (this._brushStartTime = +new Date()))
    }),
    (n.prototype._onBrushEnd = function (t) {
      if (this._brushing) {
        var e = this._displayables.brushRect
        if (((this._brushing = !1), e)) {
          e.attr('ignore', !0)
          var n = e.shape
          if (!(+new Date() - this._brushStartTime < 200 && Math.abs(n.width) < 5)) {
            var o = this._getViewExtent(),
              a = [0, 100]
            ;((this._range = _t([O(n.x, o, a, !0), O(n.x + n.width, o, a, !0)])),
              (this._handleEnds = [n.x, n.x + n.width]),
              this._updateView(),
              this._dispatchZoomAction(!1))
          }
        }
      }
    }),
    (n.prototype._onBrush = function (t) {
      this._brushing && (ae(t.event), this._updateBrushRect(t.offsetX, t.offsetY))
    }),
    (n.prototype._updateBrushRect = function (t, e) {
      var n = this._displayables,
        o = this.dataZoomModel,
        a = n.brushRect
      ;(a ||
        ((a = n.brushRect = new xa({ silent: !0, style: o.getModel('brushStyle').getItemStyle() })),
        n.sliderGroup.add(a)),
        a.attr('ignore', !1))
      var i = this._brushStart,
        r = this._displayables.sliderGroup,
        s = r.transformCoordToLocal(t, e),
        l = r.transformCoordToLocal(i.x, i.y),
        u = this._size
      ;((s[0] = Math.max(Math.min(u[0], s[0]), 0)),
        a.setShape({ x: l[0], y: 0, width: s[0] - l[0], height: u[1] }))
    }),
    (n.prototype._dispatchZoomAction = function (t) {
      var e = this._range
      this.api.dispatchAction({
        type: 'dataZoom',
        from: this.uid,
        dataZoomId: this.dataZoomModel.id,
        animation: t ? ba : null,
        start: e[0],
        end: e[1]
      })
    }),
    (n.prototype._findCoordRect = function () {
      var t,
        e = eo(this.dataZoomModel).infoList
      if (!t && e.length) {
        var n = e[0].model.coordinateSystem
        t = n.getRect && n.getRect()
      }
      if (!t) {
        var o = this.api.getWidth(),
          a = this.api.getHeight()
        t = { x: 0.2 * o, y: 0.2 * a, width: 0.6 * o, height: 0.6 * a }
      }
      return t
    }),
    (n.type = 'dataZoom.slider'),
    n
  )
})(ro)
function Aa(t) {
  ;(t.registerComponentModel(ma), t.registerComponentView(Ia), fo(t))
}
var Ca = {
    value: 'eq',
    '<': 'lt',
    '<=': 'lte',
    '>': 'gt',
    '>=': 'gte',
    '=': 'eq',
    '!=': 'ne',
    '<>': 'ne'
  },
  Ta = (function () {
    function t(t) {
      if (null == (this._condVal = G(t) ? new RegExp(t) : ce(t) ? t : null)) {
        se('')
      }
    }
    return (
      (t.prototype.evaluate = function (t) {
        var e = typeof t
        return G(e) ? this._condVal.test(t) : !!Y(e) && this._condVal.test(t + '')
      }),
      t
    )
  })(),
  Da = (function () {
    function t() {}
    return (
      (t.prototype.evaluate = function () {
        return this.value
      }),
      t
    )
  })(),
  La = (function () {
    function t() {}
    return (
      (t.prototype.evaluate = function () {
        for (var t = this.children, e = 0; e < t.length; e++) if (!t[e].evaluate()) return !1
        return !0
      }),
      t
    )
  })(),
  Pa = (function () {
    function t() {}
    return (
      (t.prototype.evaluate = function () {
        for (var t = this.children, e = 0; e < t.length; e++) if (t[e].evaluate()) return !0
        return !1
      }),
      t
    )
  })(),
  ka = (function () {
    function t() {}
    return (
      (t.prototype.evaluate = function () {
        return !this.child.evaluate()
      }),
      t
    )
  })(),
  Ra = (function () {
    function t() {}
    return (
      (t.prototype.evaluate = function () {
        for (
          var t = !!this.valueParser,
            e = (0, this.getValue)(this.valueGetterParam),
            n = t ? this.valueParser(e) : null,
            o = 0;
          o < this.subCondList.length;
          o++
        )
          if (!this.subCondList[o].evaluate(t ? n : e)) return !1
        return !0
      }),
      t
    )
  })()
function za(t, e) {
  if (!0 === t || !1 === t) {
    var n = new Da()
    return ((n.value = t), n)
  }
  return (
    Ea(t) || se(''),
    t.and
      ? Oa('and', t, e)
      : t.or
        ? Oa('or', t, e)
        : t.not
          ? (function (t, e) {
              var n = t.not,
                o = ''
              Ea(n) || se(o)
              var a = new ka()
              ;((a.child = za(n, e)), a.child || se(o))
              return a
            })(t, e)
          : (function (t, e) {
              for (
                var n = '',
                  o = e.prepareGetValue(t),
                  a = [],
                  i = le(t),
                  r = t.parser,
                  s = r ? ue(r) : null,
                  l = 0;
                l < i.length;
                l++
              ) {
                var u = i[l]
                if ('parser' !== u && !e.valueGetterAttrMap.get(u)) {
                  var d = de(Ca, u) ? Ca[u] : u,
                    h = t[u],
                    p = s ? s(h) : h,
                    c = he(d, p) || ('reg' === d && new Ta(p))
                  ;(c || se(n), a.push(c))
                }
              }
              a.length || se(n)
              var f = new Ra()
              return (
                (f.valueGetterParam = o),
                (f.valueParser = s),
                (f.getValue = e.getValue),
                (f.subCondList = a),
                f
              )
            })(t, e)
  )
}
function Oa(t, e, n) {
  var o = e[t]
  ;(b(o) || se(''), o.length || se(''))
  var a = 'and' === t ? new La() : new Pa()
  return (
    (a.children = rt(o, function (t) {
      return za(t, n)
    })),
    a.children.length || se(''),
    a
  )
}
function Ea(t) {
  return Vt(t) && !pe(t)
}
var Va = (function () {
  function t(t, e) {
    this._cond = za(t, e)
  }
  return (
    (t.prototype.evaluate = function () {
      return this._cond.evaluate()
    }),
    t
  )
})()
var Za = {
    type: 'echarts:filter',
    transform: function (t) {
      for (
        var e,
          n,
          o,
          a = t.upstream,
          i =
            ((n = t.config),
            (o = {
              valueGetterAttrMap: lt({ dimension: !0 }),
              prepareGetValue: function (t) {
                var e = t.dimension
                de(t, 'dimension') || se('')
                var n = a.getDimensionInfo(e)
                return (n || se(''), { dimIdx: n.index })
              },
              getValue: function (t) {
                return a.retrieveValueFromItem(e, t.dimIdx)
              }
            }),
            new Va(n, o)),
          r = [],
          s = 0,
          l = a.count();
        s < l;
        s++
      )
        ((e = a.getRawDataItem(s)), i.evaluate() && r.push(e))
      return { data: r }
    }
  },
  Na = {
    type: 'echarts:sort',
    transform: function (t) {
      var e = t.upstream,
        n = t.config,
        o = '',
        a = ye(n)
      a.length || se(o)
      var i = []
      y(a, function (t) {
        var n = t.dimension,
          a = t.order,
          r = t.parser,
          s = t.incomparable
        if (
          (null == n && se(o),
          'asc' !== a && 'desc' !== a && se(o),
          s && 'min' !== s && 'max' !== s)
        ) {
          se('')
        }
        if ('asc' !== a && 'desc' !== a) {
          se('')
        }
        var l = e.getDimensionInfo(n)
        l || se(o)
        var u = r ? ue(r) : null
        ;(r && !u && se(o), i.push({ dimIdx: l.index, parser: u, comparator: new fe(a, s) }))
      })
      var r = e.sourceFormat
      r !== ge && r !== ve && se(o)
      for (var s = [], l = 0, u = e.count(); l < u; l++) s.push(e.getRawDataItem(l))
      return (
        s.sort(function (t, n) {
          for (var o = 0; o < i.length; o++) {
            var a = i[o],
              r = e.retrieveValueFromItem(t, a.dimIdx),
              s = e.retrieveValueFromItem(n, a.dimIdx)
            a.parser && ((r = a.parser(r)), (s = a.parser(s)))
            var l = a.comparator.evaluate(r, s)
            if (0 !== l) return l
          }
          return 0
        }),
        { data: s }
      )
    }
  }
var Ba = me.CMD
function Fa(t, e) {
  return Math.abs(t - e) < 1e-5
}
function Ga(t) {
  var e,
    n,
    o,
    a,
    i,
    r,
    s,
    l,
    u,
    d,
    h,
    p,
    c,
    f,
    g,
    v,
    y,
    m,
    x,
    _,
    M,
    w,
    b,
    S,
    I = t.data,
    A = t.len(),
    C = [],
    T = 0,
    D = 0,
    L = 0,
    P = 0
  function k(t, n) {
    ;(e && e.length > 2 && C.push(e), (e = [t, n]))
  }
  function R(t, n, o, a) {
    ;(Fa(t, o) && Fa(n, a)) || e.push(t, n, o, a, o, a)
  }
  for (var z = 0; z < A; ) {
    var O = I[z++],
      E = 1 === z
    switch (
      (E &&
        ((L = T = I[z]),
        (P = D = I[z + 1]),
        (O !== Ba.L && O !== Ba.C && O !== Ba.Q) || (e = [L, P])),
      O)
    ) {
      case Ba.M:
        ;((T = L = I[z++]), (D = P = I[z++]), k(L, P))
        break
      case Ba.L:
        ;(R(T, D, (n = I[z++]), (o = I[z++])), (T = n), (D = o))
        break
      case Ba.C:
        e.push(I[z++], I[z++], I[z++], I[z++], (T = I[z++]), (D = I[z++]))
        break
      case Ba.Q:
        ;((n = I[z++]),
          (o = I[z++]),
          (a = I[z++]),
          (i = I[z++]),
          e.push(
            T + (2 / 3) * (n - T),
            D + (2 / 3) * (o - D),
            a + (2 / 3) * (n - a),
            i + (2 / 3) * (o - i),
            a,
            i
          ),
          (T = a),
          (D = i))
        break
      case Ba.A:
        var V = I[z++],
          Z = I[z++],
          N = I[z++],
          B = I[z++],
          F = I[z++],
          G = I[z++] + F
        z += 1
        var W = !I[z++]
        ;((n = Math.cos(F) * N + V),
          (o = Math.sin(F) * B + Z),
          E ? k((L = n), (P = o)) : R(T, D, n, o),
          (T = Math.cos(G) * N + V),
          (D = Math.sin(G) * B + Z))
        for (var H = ((W ? -1 : 1) * Math.PI) / 2, U = F; W ? U > G : U < G; U += H) {
          var Y = W ? Math.max(U + H, G) : Math.min(U + H, G)
          ;((r = U),
            (s = Y),
            (l = V),
            (u = Z),
            (d = N),
            (h = B),
            (p = void 0),
            (c = void 0),
            (f = void 0),
            (g = void 0),
            (v = void 0),
            (y = void 0),
            (m = void 0),
            (x = void 0),
            (_ = void 0),
            (M = void 0),
            (w = void 0),
            (b = void 0),
            (S = void 0),
            (p = Math.abs(s - r)),
            (c = (4 * Math.tan(p / 4)) / 3),
            (f = s < r ? -1 : 1),
            (g = Math.cos(r)),
            (v = Math.sin(r)),
            (y = Math.cos(s)),
            (m = Math.sin(s)),
            (x = g * d + l),
            (_ = v * h + u),
            (M = y * d + l),
            (w = m * h + u),
            (b = d * c * f),
            (S = h * c * f),
            e.push(x - b * v, _ + S * g, M + b * m, w - S * y, M, w))
        }
        break
      case Ba.R:
        ;((L = T = I[z++]),
          (P = D = I[z++]),
          (n = L + I[z++]),
          (o = P + I[z++]),
          k(n, P),
          R(n, P, n, o),
          R(n, o, L, o),
          R(L, o, L, P),
          R(L, P, n, P))
        break
      case Ba.Z:
        ;(e && R(T, D, L, P), (T = L), (D = P))
    }
  }
  return (e && e.length > 2 && C.push(e), C)
}
function Wa(t, e, n, o, a, i, r, s, l, u) {
  if (Fa(t, n) && Fa(e, o) && Fa(a, r) && Fa(i, s)) l.push(r, s)
  else {
    var d = 2 / u,
      h = d * d,
      p = r - t,
      c = s - e,
      f = Math.sqrt(p * p + c * c)
    ;((p /= f), (c /= f))
    var g = n - t,
      v = o - e,
      y = a - r,
      m = i - s,
      x = g * g + v * v,
      _ = y * y + m * m
    if (x < h && _ < h) l.push(r, s)
    else {
      var M = p * g + c * v,
        w = -p * y - c * m
      if (x - M * M < h && M >= 0 && _ - w * w < h && w >= 0) l.push(r, s)
      else {
        var b = [],
          S = []
        ;(xe(t, n, a, r, 0.5, b),
          xe(e, o, i, s, 0.5, S),
          Wa(b[0], S[0], b[1], S[1], b[2], S[2], b[3], S[3], l, u),
          Wa(b[4], S[4], b[5], S[5], b[6], S[6], b[7], S[7], l, u))
      }
    }
  }
}
function Ha(t, e, n) {
  var o = t[e],
    a = t[1 - e],
    i = Math.abs(o / a),
    r = Math.ceil(Math.sqrt(i * n)),
    s = Math.floor(n / r)
  0 === s && ((s = 1), (r = n))
  for (var l = [], u = 0; u < r; u++) l.push(s)
  var d = n - r * s
  if (d > 0) for (u = 0; u < d; u++) l[u % r] += 1
  return l
}
function Ua(t, e, n) {
  for (
    var o = t.r0,
      a = t.r,
      i = t.startAngle,
      r = t.endAngle,
      s = Math.abs(r - i),
      l = s * a,
      u = a - o,
      d = l > Math.abs(u),
      h = Ha([l, u], d ? 0 : 1, e),
      p = (d ? s : u) / h.length,
      c = 0;
    c < h.length;
    c++
  )
    for (var f = (d ? u : s) / h[c], g = 0; g < h[c]; g++) {
      var v = {}
      ;(d
        ? ((v.startAngle = i + p * c),
          (v.endAngle = i + p * (c + 1)),
          (v.r0 = o + f * g),
          (v.r = o + f * (g + 1)))
        : ((v.startAngle = i + f * g),
          (v.endAngle = i + f * (g + 1)),
          (v.r0 = o + p * c),
          (v.r = o + p * (c + 1))),
        (v.clockwise = t.clockwise),
        (v.cx = t.cx),
        (v.cy = t.cy),
        n.push(v))
    }
}
function Ya(t, e, n, o) {
  return t * o - n * e
}
function Xa(t, e, n, o, a, i, r, s) {
  var l = n - t,
    u = o - e,
    d = r - a,
    h = s - i,
    p = Ya(d, h, l, u)
  if (Math.abs(p) < 1e-6) return null
  var c = Ya(t - a, e - i, d, h) / p
  return c < 0 || c > 1 ? null : new ie(c * l + t, c * u + e)
}
function ja(t, e, n) {
  var o = new ie()
  ;(ie.sub(o, n, e), o.normalize())
  var a = new ie()
  return (ie.sub(a, t, e), a.dot(o))
}
function qa(t, e) {
  var n = t[t.length - 1]
  ;(n && n[0] === e[0] && n[1] === e[1]) || t.push(e)
}
function Ka(t) {
  var e = t.points,
    n = [],
    a = []
  _e(e, n, a)
  var i = new o(n[0], n[1], a[0] - n[0], a[1] - n[1]),
    r = i.width,
    s = i.height,
    l = i.x,
    u = i.y,
    d = new ie(),
    h = new ie()
  return (
    r > s
      ? ((d.x = h.x = l + r / 2), (d.y = u), (h.y = u + s))
      : ((d.y = h.y = u + s / 2), (d.x = l), (h.x = l + r)),
    (function (t, e, n) {
      for (var o = t.length, a = [], i = 0; i < o; i++) {
        var r = t[i],
          s = t[(i + 1) % o],
          l = Xa(r[0], r[1], s[0], s[1], e.x, e.y, n.x, n.y)
        l && a.push({ projPt: ja(l, e, n), pt: l, idx: i })
      }
      if (a.length < 2) return [{ points: t }, { points: t }]
      a.sort(function (t, e) {
        return t.projPt - e.projPt
      })
      var u = a[0],
        d = a[a.length - 1]
      if (d.idx < u.idx) {
        var h = u
        ;((u = d), (d = h))
      }
      var p = [u.pt.x, u.pt.y],
        c = [d.pt.x, d.pt.y],
        f = [p],
        g = [c]
      for (i = u.idx + 1; i <= d.idx; i++) qa(f, t[i].slice())
      for (qa(f, c), qa(f, p), i = d.idx + 1; i <= u.idx + o; i++) qa(g, t[i % o].slice())
      return (qa(g, p), qa(g, c), [{ points: f }, { points: g }])
    })(e, d, h)
  )
}
function $a(t, e, n, o) {
  if (1 === n) o.push(e)
  else {
    var a = Math.floor(n / 2),
      i = t(e)
    ;($a(t, i[0], a, o), $a(t, i[1], n - a, o))
  }
  return o
}
function Qa(t, e) {
  var n,
    o = [],
    a = t.shape
  switch (t.type) {
    case 'rect':
      ;(!(function (t, e, n) {
        for (
          var o = t.width,
            a = t.height,
            i = o > a,
            r = Ha([o, a], i ? 0 : 1, e),
            s = i ? 'width' : 'height',
            l = i ? 'height' : 'width',
            u = i ? 'x' : 'y',
            d = i ? 'y' : 'x',
            h = t[s] / r.length,
            p = 0;
          p < r.length;
          p++
        )
          for (var c = t[l] / r[p], f = 0; f < r[p]; f++) {
            var g = {}
            ;((g[u] = p * h),
              (g[d] = f * c),
              (g[s] = h),
              (g[l] = c),
              (g.x += t.x),
              (g.y += t.y),
              n.push(g))
          }
      })(a, e, o),
        (n = ee))
      break
    case 'sector':
      ;(Ua(a, e, o), (n = U))
      break
    case 'circle':
      ;(Ua({ r0: 0, r: a.r, startAngle: 0, endAngle: 2 * Math.PI, cx: a.cx, cy: a.cy }, e, o),
        (n = U))
      break
    default:
      var i = t.getComputedTransform(),
        r = i ? Math.sqrt(Math.max(i[0] * i[0] + i[1] * i[1], i[2] * i[2] + i[3] * i[3])) : 1,
        s = rt(
          (function (t, e) {
            var n = Ga(t),
              o = []
            e = e || 1
            for (var a = 0; a < n.length; a++) {
              var i = n[a],
                r = [],
                s = i[0],
                l = i[1]
              r.push(s, l)
              for (var u = 2; u < i.length; ) {
                var d = i[u++],
                  h = i[u++],
                  p = i[u++],
                  c = i[u++],
                  f = i[u++],
                  g = i[u++]
                ;(Wa(s, l, d, h, p, c, f, g, r, e), (s = f), (l = g))
              }
              o.push(r)
            }
            return o
          })(t.getUpdatedPathProxy(), r),
          function (t) {
            return (function (t) {
              for (var e = [], n = 0; n < t.length; ) e.push([t[n++], t[n++]])
              return e
            })(t)
          }
        ),
        l = s.length
      if (0 === l) $a(Ka, { points: s[0] }, e, o)
      else if (l === e) for (var u = 0; u < l; u++) o.push({ points: s[u] })
      else {
        var d = 0,
          h = rt(s, function (t) {
            var e = [],
              n = []
            _e(t, e, n)
            var o = (n[1] - e[1]) * (n[0] - e[0])
            return ((d += o), { poly: t, area: o })
          })
        h.sort(function (t, e) {
          return e.area - t.area
        })
        var p = e
        for (u = 0; u < l; u++) {
          var c = h[u]
          if (p <= 0) break
          var f = u === l - 1 ? p : Math.ceil((c.area / d) * e)
          f < 0 || ($a(Ka, { points: c.poly }, f, o), (p -= f))
        }
      }
      n = re
  }
  if (!n)
    return (function (t, e) {
      for (var n = [], o = 0; o < e; o++) n.push(Me(t))
      return n
    })(t, e)
  var g,
    v,
    y = []
  for (u = 0; u < o.length; u++) {
    var m = new n()
    ;(m.setShape(o[u]),
      (g = t),
      (v = m).setStyle(g.style),
      (v.z = g.z),
      (v.z2 = g.z2),
      (v.zlevel = g.zlevel),
      y.push(m))
  }
  return y
}
function Ja(t, e) {
  var n = t.length,
    o = e.length
  if (n === o) return [t, e]
  for (
    var a = [],
      i = [],
      r = n < o ? t : e,
      s = Math.min(n, o),
      l = Math.abs(o - n) / 6,
      u = (s - 2) / 6,
      d = Math.ceil(l / u) + 1,
      h = [r[0], r[1]],
      p = l,
      c = 2;
    c < s;
  ) {
    var f = r[c - 2],
      g = r[c - 1],
      v = r[c++],
      y = r[c++],
      m = r[c++],
      x = r[c++],
      _ = r[c++],
      M = r[c++]
    if (p <= 0) h.push(v, y, m, x, _, M)
    else {
      for (var w = Math.min(p, d - 1) + 1, b = 1; b <= w; b++) {
        var S = b / w
        ;(xe(f, v, m, _, S, a),
          xe(g, y, x, M, S, i),
          (f = a[3]),
          (g = i[3]),
          h.push(a[1], i[1], a[2], i[2], f, g),
          (v = a[5]),
          (y = i[5]),
          (m = a[6]),
          (x = i[6]))
      }
      p -= w - 1
    }
  }
  return r === t ? [h, e] : [t, h]
}
function ti(t, e) {
  for (var n = t.length, o = t[n - 2], a = t[n - 1], i = [], r = 0; r < e.length; )
    ((i[r++] = o), (i[r++] = a))
  return i
}
function ei(t) {
  for (var e = 0, n = 0, o = 0, a = t.length, i = 0, r = a - 2; i < a; r = i, i += 2) {
    var s = t[r],
      l = t[r + 1],
      u = t[i],
      d = t[i + 1],
      h = s * d - u * l
    ;((e += h), (n += (s + u) * h), (o += (l + d) * h))
  }
  return 0 === e ? [t[0] || 0, t[1] || 0] : [n / e / 3, o / e / 3, e]
}
function ni(t, e, n, o) {
  for (var a = (t.length - 2) / 6, i = 1 / 0, r = 0, s = t.length, l = s - 2, u = 0; u < a; u++) {
    for (var d = 6 * u, h = 0, p = 0; p < s; p += 2) {
      var c = 0 === p ? d : ((d + p - 2) % l) + 2,
        f = t[c] - n[0],
        g = t[c + 1] - n[1],
        v = e[p] - o[0] - f,
        y = e[p + 1] - o[1] - g
      h += v * v + y * y
    }
    h < i && ((i = h), (r = u))
  }
  return r
}
function oi(t) {
  for (var e = [], n = t.length, o = 0; o < n; o += 2)
    ((e[o] = t[n - o - 2]), (e[o + 1] = t[n - o - 1]))
  return e
}
function ai(t) {
  return t.__isCombineMorphing
}
var ii = '__mOriginal_'
function ri(t, e, n) {
  var o = ii + e,
    a = t[o] || t[e]
  t[o] || (t[o] = t[e])
  var i = n.replace,
    r = n.after,
    s = n.before
  t[e] = function () {
    var t,
      e = arguments
    return (
      s && s.apply(this, e),
      (t = i ? i.apply(this, e) : a.apply(this, e)),
      r && r.apply(this, e),
      t
    )
  }
}
function si(t, e) {
  var n = ii + e
  t[n] && ((t[e] = t[n]), (t[n] = null))
}
function li(t, e) {
  for (var n = 0; n < t.length; n++)
    for (var o = t[n], a = 0; a < o.length; ) {
      var i = o[a],
        r = o[a + 1]
      ;((o[a++] = e[0] * i + e[2] * r + e[4]), (o[a++] = e[1] * i + e[3] * r + e[5]))
    }
}
function ui(t, e) {
  var n = t.getUpdatedPathProxy(),
    o = e.getUpdatedPathProxy(),
    a = (function (t, e) {
      for (var n, o, a, i = [], r = [], s = 0; s < Math.max(t.length, e.length); s++) {
        var l = t[s],
          u = e[s],
          d = void 0,
          h = void 0
        ;(l
          ? u
            ? ((o = d = (n = Ja(l, u))[0]), (a = h = n[1]))
            : ((h = ti(a || l, l)), (d = l))
          : ((d = ti(o || u, u)), (h = u)),
          i.push(d),
          r.push(h))
      }
      return [i, r]
    })(Ga(n), Ga(o)),
    i = a[0],
    r = a[1],
    s = t.getComputedTransform(),
    l = e.getComputedTransform()
  ;(s && li(i, s),
    l && li(r, l),
    ri(e, 'updateTransform', {
      replace: function () {
        this.transform = null
      }
    }),
    (e.transform = null))
  var u = (function (t, e, n, o) {
      for (var a, i = [], r = 0; r < t.length; r++) {
        var s = t[r],
          l = e[r],
          u = ei(s),
          d = ei(l)
        null == a && (a = u[2] < 0 != d[2] < 0)
        var h = [],
          p = [],
          c = 0,
          f = 1 / 0,
          g = [],
          v = s.length
        a && (s = oi(s))
        for (var y = 6 * ni(s, l, u, d), m = v - 2, x = 0; x < m; x += 2) {
          var _ = ((y + x) % m) + 2
          ;((h[x + 2] = s[_] - u[0]), (h[x + 3] = s[_ + 1] - u[1]))
        }
        if (((h[0] = s[y] - u[0]), (h[1] = s[y + 1] - u[1]), n > 0))
          for (var M = o / n, w = -o / 2; w <= o / 2; w += M) {
            var b = Math.sin(w),
              S = Math.cos(w),
              I = 0
            for (x = 0; x < s.length; x += 2) {
              var A = h[x],
                C = h[x + 1],
                T = l[x] - d[0],
                D = l[x + 1] - d[1],
                L = T * S - D * b,
                P = T * b + D * S
              ;((g[x] = L), (g[x + 1] = P))
              var k = L - A,
                R = P - C
              I += k * k + R * R
            }
            if (I < f) {
              ;((f = I), (c = w))
              for (var z = 0; z < g.length; z++) p[z] = g[z]
            }
          }
        else for (var O = 0; O < v; O += 2) ((p[O] = l[O] - d[0]), (p[O + 1] = l[O + 1] - d[1]))
        i.push({ from: h, to: p, fromCp: u, toCp: d, rotation: -c })
      }
      return i
    })(i, r, 10, Math.PI),
    d = []
  ri(e, 'buildPath', {
    replace: function (t) {
      for (var n = e.__morphT, o = 1 - n, a = [], i = 0; i < u.length; i++) {
        var r = u[i],
          s = r.from,
          l = r.to,
          h = r.rotation * n,
          p = r.fromCp,
          c = r.toCp,
          f = Math.sin(h),
          g = Math.cos(h)
        be(a, p, c, n)
        for (var v = 0; v < s.length; v += 2) {
          var y = s[v],
            m = s[v + 1],
            x = y * o + (b = l[v]) * n,
            _ = m * o + (S = l[v + 1]) * n
          ;((d[v] = x * g - _ * f + a[0]), (d[v + 1] = x * f + _ * g + a[1]))
        }
        var M = d[0],
          w = d[1]
        t.moveTo(M, w)
        for (v = 2; v < s.length; ) {
          var b = d[v++],
            S = d[v++],
            I = d[v++],
            A = d[v++],
            C = d[v++],
            T = d[v++]
          ;(M === b && w === S && I === C && A === T
            ? t.lineTo(C, T)
            : t.bezierCurveTo(b, S, I, A, C, T),
            (M = C),
            (w = T))
        }
      }
    }
  })
}
function di(t, e, n) {
  if (!t || !e) return e
  var o = n.done,
    a = n.during
  return (
    ui(t, e),
    (e.__morphT = 0),
    e.animateTo(
      { __morphT: 1 },
      Rt(
        {
          during: function (t) {
            ;(e.dirtyShape(), a && a(t))
          },
          done: function () {
            ;(si(e, 'buildPath'),
              si(e, 'updateTransform'),
              (e.__morphT = -1),
              e.createPathProxy(),
              e.dirtyShape(),
              o && o())
          }
        },
        n
      )
    ),
    e
  )
}
function hi(t, e, n, o, a, i) {
  ;((t = a === n ? 0 : Math.round((32767 * (t - n)) / (a - n))),
    (e = i === o ? 0 : Math.round((32767 * (e - o)) / (i - o))))
  for (var r, s = 0, l = 32768; l > 0; l /= 2) {
    var u = 0,
      d = 0
    ;((t & l) > 0 && (u = 1),
      (e & l) > 0 && (d = 1),
      (s += l * l * ((3 * u) ^ d)),
      0 === d && (1 === u && ((t = l - 1 - t), (e = l - 1 - e)), (r = t), (t = e), (e = r)))
  }
  return s
}
function pi(t) {
  var e = 1 / 0,
    n = 1 / 0,
    o = -1 / 0,
    a = -1 / 0,
    i = rt(t, function (t) {
      var i = t.getBoundingRect(),
        r = t.getComputedTransform(),
        s = i.x + i.width / 2 + (r ? r[4] : 0),
        l = i.y + i.height / 2 + (r ? r[5] : 0)
      return (
        (e = Math.min(s, e)),
        (n = Math.min(l, n)),
        (o = Math.max(s, o)),
        (a = Math.max(l, a)),
        [s, l]
      )
    })
  return rt(i, function (i, r) {
    return { cp: i, z: hi(i[0], i[1], e, n, o, a), path: t[r] }
  })
    .sort(function (t, e) {
      return t.z - e.z
    })
    .map(function (t) {
      return t.path
    })
}
function ci(t) {
  return Qa(t.path, t.count)
}
function fi(t) {
  return b(t[0])
}
function gi(t, e) {
  for (var n = [], o = t.length, a = 0; a < o; a++) n.push({ one: t[a], many: [] })
  for (a = 0; a < e.length; a++) {
    var i = e[a].length,
      r = void 0
    for (r = 0; r < i; r++) n[r % o].many.push(e[a][r])
  }
  var s = 0
  for (a = o - 1; a >= 0; a--)
    if (!n[a].many.length) {
      var l = n[s].many
      if (l.length <= 1) {
        if (!s) return n
        s = 0
      }
      i = l.length
      var u = Math.ceil(i / 2)
      ;((n[a].many = l.slice(u, i)), (n[s].many = l.slice(0, u)), s++)
    }
  return n
}
var vi = {
  clone: function (t) {
    for (
      var e = [], n = 1 - Math.pow(1 - t.path.style.opacity, 1 / t.count), o = 0;
      o < t.count;
      o++
    ) {
      var a = Me(t.path)
      ;(a.setStyle('opacity', n), e.push(a))
    }
    return e
  },
  split: null
}
function yi(t, e, n, o, i, r) {
  if (t.length && e.length) {
    var s = Se('update', o, i)
    if (s && s.duration > 0) {
      var l,
        u,
        d = o.getModel('universalTransition').get('delay'),
        h = Object.assign({ setToFinal: !0 }, s)
      ;(fi(t) && ((l = t), (u = e)), fi(e) && ((l = e), (u = t)))
      for (
        var p = l ? l === t : t.length > e.length,
          c = l ? gi(u, l) : gi(p ? e : t, [p ? t : e]),
          f = 0,
          g = 0;
        g < c.length;
        g++
      )
        f += c[g].many.length
      var v = 0
      for (g = 0; g < c.length; g++) (y(c[g], p, v, f), (v += c[g].many.length))
    }
  }
  function y(t, e, o, i, s) {
    var l = t.many,
      u = t.one
    if (1 !== l.length || s)
      for (
        var p = Rt(
            {
              dividePath: vi[n],
              individualDelay:
                d &&
                function (t, e, n, a) {
                  return d(t + o, i)
                }
            },
            h
          ),
          c = e
            ? (function (t, e, n) {
                var o = []
                !(function t(e) {
                  for (var n = 0; n < e.length; n++) {
                    var i = e[n]
                    ai(i) ? t(i.childrenRef()) : i instanceof a && o.push(i)
                  }
                })(t)
                var i = o.length
                if (!i) return { fromIndividuals: [], toIndividuals: [], count: 0 }
                var r = (n.dividePath || ci)({ path: e, count: i })
                if (r.length !== i) return { fromIndividuals: [], toIndividuals: [], count: 0 }
                ;((o = pi(o)), (r = pi(r)))
                for (
                  var s = n.done, l = n.during, u = n.individualDelay, d = new we(), h = 0;
                  h < i;
                  h++
                ) {
                  var p = o[h],
                    c = r[h]
                  ;((c.parent = e), c.copyTransform(d), u || ui(p, c))
                }
                function f(t) {
                  for (var e = 0; e < r.length; e++) r[e].addSelfToZr(t)
                }
                function g() {
                  ;((e.__isCombineMorphing = !1),
                    (e.__morphT = -1),
                    (e.childrenRef = null),
                    si(e, 'addSelfToZr'),
                    si(e, 'removeSelfFromZr'))
                }
                ;((e.__isCombineMorphing = !0),
                  (e.childrenRef = function () {
                    return r
                  }),
                  ri(e, 'addSelfToZr', {
                    after: function (t) {
                      f(t)
                    }
                  }),
                  ri(e, 'removeSelfFromZr', {
                    after: function (t) {
                      for (var e = 0; e < r.length; e++) r[e].removeSelfFromZr(t)
                    }
                  }))
                var v = r.length
                if (u) {
                  var y = v,
                    m = function () {
                      0 == --y && (g(), s && s())
                    }
                  for (h = 0; h < v; h++) {
                    var x = u ? Rt({ delay: (n.delay || 0) + u(h, v, o[h], r[h]), done: m }, n) : n
                    di(o[h], r[h], x)
                  }
                } else
                  ((e.__morphT = 0),
                    e.animateTo(
                      { __morphT: 1 },
                      Rt(
                        {
                          during: function (t) {
                            for (var n = 0; n < v; n++) {
                              var o = r[n]
                              ;((o.__morphT = e.__morphT), o.dirtyShape())
                            }
                            l && l(t)
                          },
                          done: function () {
                            g()
                            for (var e = 0; e < t.length; e++) si(t[e], 'updateTransform')
                            s && s()
                          }
                        },
                        n
                      )
                    ))
                return (e.__zr && f(e.__zr), { fromIndividuals: o, toIndividuals: r, count: v })
              })(l, u, p)
            : (function (t, e, n) {
                var o = e.length,
                  i = [],
                  r = n.dividePath || ci
                if (ai(t)) {
                  !(function t(e) {
                    for (var n = 0; n < e.length; n++) {
                      var o = e[n]
                      ai(o) ? t(o.childrenRef()) : o instanceof a && i.push(o)
                    }
                  })(t.childrenRef())
                  var s = i.length
                  if (s < o) for (var l = 0, u = s; u < o; u++) i.push(Me(i[l++ % s]))
                  i.length = o
                } else {
                  i = r({ path: t, count: o })
                  var d = t.getComputedTransform()
                  for (u = 0; u < i.length; u++) i[u].setLocalTransform(d)
                  if (i.length !== o) return { fromIndividuals: [], toIndividuals: [], count: 0 }
                }
                ;((i = pi(i)), (e = pi(e)))
                var h = n.individualDelay
                for (u = 0; u < o; u++) {
                  var p = h ? Rt({ delay: (n.delay || 0) + h(u, o, i[u], e[u]) }, n) : n
                  di(i[u], e[u], p)
                }
                return { fromIndividuals: i, toIndividuals: e, count: e.length }
              })(u, l, p),
          f = c.fromIndividuals,
          g = c.toIndividuals,
          v = f.length,
          m = 0;
        m < v;
        m++
      ) {
        x = d ? Rt({ delay: d(m, v) }, h) : h
        r(f[m], g[m], e ? l[m] : t.one, e ? t.one : l[m], x)
      }
    else {
      var x,
        _ = e ? l[0] : u,
        M = e ? u : l[0]
      if (ai(_)) y({ many: [_], one: M }, !0, o, i, !0)
      else (di(_, M, (x = d ? Rt({ delay: d(o, i) }, h) : h)), r(_, M, _, M, x))
    }
  }
}
function mi(t) {
  if (!t) return []
  if (b(t)) {
    for (var e = [], n = 0; n < t.length; n++) e.push(mi(t[n]))
    return e
  }
  var o = []
  return (
    t.traverse(function (t) {
      t instanceof a && !t.disableMorphing && !t.invisible && !t.ignore && o.push(t)
    }),
    o
  )
}
var xi = 1e4,
  _i = Zt()
function Mi(t) {
  var e = []
  return (
    y(t, function (t) {
      var n = t.data
      if (!(n.count() > xi))
        for (
          var o = n.getIndices(),
            a = (function (t) {
              for (var e = t.dimensions, n = 0; n < e.length; n++) {
                var o = t.getDimensionInfo(e[n])
                if (o && 0 === o.otherDims.itemGroupId) return e[n]
              }
            })(n),
            i = 0;
          i < o.length;
          i++
        )
          e.push({
            dataGroupId: t.dataGroupId,
            data: n,
            dim: t.dim || a,
            divide: t.divide,
            dataIndex: i
          })
    }),
    e
  )
}
function wi(t, e, n) {
  t.traverse(function (t) {
    t instanceof a && v(t, { style: { opacity: 0 } }, e, { dataIndex: n, isFrom: !0 })
  })
}
function bi(t) {
  if (t.parent) {
    var e = t.getComputedTransform()
    ;(t.setLocalTransform(e), t.parent.remove(t))
  }
}
function Si(t) {
  ;(t.stopAnimation(),
    t.isGroup &&
      t.traverse(function (t) {
        t.stopAnimation()
      }))
}
function Ii(t, e, n) {
  var o = Mi(t),
    i = Mi(e)
  function r(t, e, n, o, a) {
    ;(n || t) && e.animateFrom({ style: n && n !== t ? Z(Z({}, n.style), t.style) : t.style }, a)
  }
  function s(t) {
    for (var e = 0; e < t.length; e++) if (t[e].dim) return t[e].dim
  }
  var l = s(o),
    u = s(i),
    d = !1
  function h(t, e) {
    return function (n) {
      var o = n.data,
        a = n.dataIndex
      if (e) return o.getId(a)
      var i = n.dataGroupId,
        r = t ? l || u : u || l,
        s = r && o.getDimensionInfo(r),
        d = s && s.ordinalMeta
      if (s) {
        var h = o.get(s.name, a)
        return (d && d.categories[h]) || h + ''
      }
      var p = o.getRawDataItem(a)
      return p && p.groupId ? p.groupId + '' : i || o.getId(a)
    }
  }
  var p = (function (t, e) {
      var n = t.length
      if (n !== e.length) return !1
      for (var o = 0; o < n; o++) {
        var a = t[o],
          i = e[o]
        if (a.data.getId(a.dataIndex) !== i.data.getId(i.dataIndex)) return !1
      }
      return !0
    })(o, i),
    c = {}
  if (!p)
    for (var f = 0; f < i.length; f++) {
      var g = i[f],
        v = g.data.getItemGraphicEl(g.dataIndex)
      v && (c[v.id] = !0)
    }
  function m(t, e) {
    var n = o[e],
      a = i[t],
      s = a.data.hostModel,
      l = n.data.getItemGraphicEl(n.dataIndex),
      u = a.data.getItemGraphicEl(a.dataIndex)
    l !== u
      ? (l && c[l.id]) ||
        (u &&
          (Si(u), l ? (Si(l), bi(l), (d = !0), yi(mi(l), mi(u), a.divide, s, t, r)) : wi(u, s, t)))
      : u &&
        (function (t, e, n) {
          var o = Se('update', n, e)
          o &&
            t.traverse(function (t) {
              if (t instanceof Ae) {
                var e = Ce(t)
                e && t.animateFrom({ style: e }, o)
              }
            })
        })(u, a.dataIndex, s)
  }
  ;(new Mt(o, i, h(!0, p), h(!1, p), null, 'multiple')
    .update(m)
    .updateManyToOne(function (t, e) {
      var n = i[t],
        a = n.data,
        s = a.hostModel,
        l = a.getItemGraphicEl(n.dataIndex),
        u = Et(
          rt(e, function (t) {
            return o[t].data.getItemGraphicEl(o[t].dataIndex)
          }),
          function (t) {
            return t && t !== l && !c[t.id]
          }
        )
      l &&
        (Si(l),
        u.length
          ? (y(u, function (t) {
              ;(Si(t), bi(t))
            }),
            (d = !0),
            yi(mi(u), mi(l), n.divide, s, t, r))
          : wi(l, s, n.dataIndex))
    })
    .updateOneToMany(function (t, e) {
      var n = o[e],
        a = n.data.getItemGraphicEl(n.dataIndex)
      if (!a || !c[a.id]) {
        var s = Et(
            rt(t, function (t) {
              return i[t].data.getItemGraphicEl(i[t].dataIndex)
            }),
            function (t) {
              return t && t !== a
            }
          ),
          l = i[t[0]].data.hostModel
        s.length &&
          (y(s, function (t) {
            return Si(t)
          }),
          a
            ? (Si(a), bi(a), (d = !0), yi(mi(a), mi(s), n.divide, l, t[0], r))
            : y(s, function (e) {
                return wi(e, l, t[0])
              }))
      }
    })
    .updateManyToMany(function (t, e) {
      new Mt(
        e,
        t,
        function (t) {
          return o[t].data.getId(o[t].dataIndex)
        },
        function (t) {
          return i[t].data.getId(i[t].dataIndex)
        }
      )
        .update(function (n, o) {
          m(t[n], e[o])
        })
        .execute()
    })
    .execute(),
    d &&
      y(e, function (t) {
        var e = t.data.hostModel,
          o = e && n.getViewOfSeriesModel(e),
          i = Se('update', e, 0)
        o &&
          e.isAnimationEnabled() &&
          i &&
          i.duration > 0 &&
          o.group.traverse(function (t) {
            t instanceof a && !t.animators.length && t.animateFrom({ style: { opacity: 0 } }, i)
          })
      }))
}
function Ai(t) {
  var e = t.getModel('universalTransition').get('seriesKey')
  return e || t.id
}
function Ci(t) {
  return b(t) ? t.sort().join(',') : t
}
function Ti(t) {
  if (t.hostModel) return t.hostModel.getModel('universalTransition').get('divideShape')
}
function Di(t, e) {
  for (var n = 0; n < t.length; n++) {
    if (
      (null != e.seriesIndex && e.seriesIndex === t[n].seriesIndex) ||
      (null != e.seriesId && e.seriesId === t[n].id)
    )
      return n
  }
}
Te({
  type: 'series.liquidFill',
  optionUpdated: function () {
    var t = this.option
    t.gridSize = Math.max(Math.floor(t.gridSize), 4)
  },
  getInitialData: function (t, e) {
    var n = De(t.data, { coordDimensions: ['value'] }),
      o = new at(n, this)
    return (o.initData(t.data), o)
  },
  defaultOption: {
    color: ['#294D99', '#156ACF', '#1598ED', '#45BDFF'],
    center: ['50%', '50%'],
    radius: '50%',
    amplitude: '8%',
    waveLength: '80%',
    phase: 'auto',
    period: 'auto',
    direction: 'right',
    shape: 'circle',
    waveAnimation: !0,
    animationEasing: 'linear',
    animationEasingUpdate: 'linear',
    animationDuration: 2e3,
    animationDurationUpdate: 1e3,
    outline: {
      show: !0,
      borderDistance: 8,
      itemStyle: {
        color: 'none',
        borderColor: '#294D99',
        borderWidth: 8,
        shadowBlur: 20,
        shadowColor: 'rgba(0, 0, 0, 0.25)'
      }
    },
    backgroundStyle: { color: '#E3F7FF' },
    itemStyle: { opacity: 0.95, shadowBlur: 50, shadowColor: 'rgba(0, 0, 0, 0.4)' },
    label: {
      show: !0,
      color: '#294D99',
      insideColor: '#fff',
      fontSize: 50,
      fontWeight: 'bold',
      align: 'center',
      baseline: 'middle',
      position: 'inside'
    },
    emphasis: { itemStyle: { opacity: 0.8 } }
  }
})
const Li = Le({
  type: 'ec-liquid-fill',
  shape: {
    waveLength: 0,
    radius: 0,
    radiusY: 0,
    cx: 0,
    cy: 0,
    waterLevel: 0,
    amplitude: 0,
    phase: 0,
    inverse: !1
  },
  buildPath: function (t, e) {
    null == e.radiusY && (e.radiusY = e.radius)
    for (
      var n = Math.max(2 * Math.ceil(((2 * e.radius) / e.waveLength) * 4), 8);
      e.phase < 2 * -Math.PI;
    )
      e.phase += 2 * Math.PI
    for (; e.phase > 0; ) e.phase -= 2 * Math.PI
    var o = (e.phase / Math.PI / 2) * e.waveLength,
      a = e.cx - e.radius + o - 2 * e.radius
    t.moveTo(a, e.waterLevel)
    for (var i = 0, r = 0; r < n; ++r) {
      var s = r % 4,
        l = Pi((r * e.waveLength) / 4, s, e.waveLength, e.amplitude)
      ;(t.bezierCurveTo(
        l[0][0] + a,
        -l[0][1] + e.waterLevel,
        l[1][0] + a,
        -l[1][1] + e.waterLevel,
        l[2][0] + a,
        -l[2][1] + e.waterLevel
      ),
        r === n - 1 && (i = l[2][0]))
    }
    ;(e.inverse
      ? (t.lineTo(i + a, e.cy - e.radiusY),
        t.lineTo(a, e.cy - e.radiusY),
        t.lineTo(a, e.waterLevel))
      : (t.lineTo(i + a, e.cy + e.radiusY),
        t.lineTo(a, e.cy + e.radiusY),
        t.lineTo(a, e.waterLevel)),
      t.closePath())
  }
})
function Pi(t, e, n, o) {
  return 0 === e
    ? [
        [t + (0.5 * n) / Math.PI / 2, o / 2],
        [t + (0.5 * n) / Math.PI, o],
        [t + n / 4, o]
      ]
    : 1 === e
      ? [
          [t + ((0.5 * n) / Math.PI / 2) * (Math.PI - 2), o],
          [t + ((0.5 * n) / Math.PI / 2) * (Math.PI - 1), o / 2],
          [t + n / 4, 0]
        ]
      : 2 === e
        ? [
            [t + (0.5 * n) / Math.PI / 2, -o / 2],
            [t + (0.5 * n) / Math.PI, -o],
            [t + n / 4, -o]
          ]
        : [
            [t + ((0.5 * n) / Math.PI / 2) * (Math.PI - 2), -o],
            [t + ((0.5 * n) / Math.PI / 2) * (Math.PI - 1), -o / 2],
            [t + n / 4, 0]
          ]
}
var ki = k
function Ri(t) {
  return t && 0 === t.indexOf('path://')
}
;(Pe({
  type: 'liquidFill',
  render: function (t, e, n) {
    var a = this,
      s = this.group
    s.removeAll()
    var l = t.getData(),
      u = l.getItemModel(0),
      d = u.get('center'),
      h = u.get('radius'),
      p = n.getWidth(),
      c = n.getHeight(),
      f = Math.min(p, c),
      g = 0,
      y = 0,
      x = t.get('outline.show')
    x &&
      ((g = t.get('outline.borderDistance')), (y = ki(t.get('outline.itemStyle.borderWidth'), f)))
    var _,
      M,
      w,
      b = ki(d[0], p),
      S = ki(d[1], c),
      I = !1,
      A = t.get('shape')
    ;('container' === A
      ? ((I = !0),
        (M = [(_ = [p / 2, c / 2])[0] - y / 2, _[1] - y / 2]),
        (w = [ki(g, p), ki(g, c)]),
        (h = [Math.max(M[0] - w[0], 0), Math.max(M[1] - w[1], 0)]))
      : ((M = (_ = ki(h, f) / 2) - y / 2), (w = ki(g, f)), (h = Math.max(M - w, 0))),
    x) && ((z().style.lineWidth = y), s.add(z()))
    var C = I ? 0 : b - h,
      T = I ? 0 : S - h,
      D = null
    s.add(
      (function () {
        var e = k(h)
        ;(e.setStyle(t.getModel('backgroundStyle').getItemStyle()),
          (e.style.fill = null),
          (e.z2 = 5))
        var n = k(h)
        ;(n.setStyle(t.getModel('backgroundStyle').getItemStyle()), (n.style.stroke = null))
        var o = new i()
        return (o.add(e), o.add(n), o)
      })()
    )
    var L = this._data,
      P = []
    function k(t, e) {
      if (A) {
        if (Ri(A)) {
          var n = ze(A.slice(7), {}),
            a = n.getBoundingRect(),
            i = a.width,
            s = a.height
          i > s ? ((s *= (2 * t) / i), (i = 2 * t)) : ((i *= (2 * t) / s), (s = 2 * t))
          var l = e ? 0 : b - i / 2,
            u = e ? 0 : S - s / 2
          return (
            (n = ze(A.slice(7), {}, new o(l, u, i, s))),
            e && ((n.x = -i / 2), (n.y = -s / 2)),
            n
          )
        }
        if (I) {
          var d = e ? -t[0] : b - t[0],
            h = e ? -t[1] : S - t[1]
          return r('rect', d, h, 2 * t[0], 2 * t[1])
        }
        h = e ? -t : S - t
        return (
          'pin' === A ? (h += t) : 'arrow' === A && (h -= t),
          r(A, (d = e ? -t : b - t), h, 2 * t, 2 * t)
        )
      }
      return new Oe({ shape: { cx: e ? 0 : b, cy: e ? 0 : S, r: t } })
    }
    function z() {
      var e = k(_)
      return ((e.style.fill = null), e.setStyle(t.getModel('outline.itemStyle').getItemStyle()), e)
    }
    function O(e, n, o) {
      var a = I ? h[0] : h,
        i = I ? c / 2 : h,
        r = l.getItemModel(e),
        s = r.getModel('itemStyle'),
        u = r.get('phase'),
        d = ki(r.get('amplitude'), 2 * i),
        p = ki(r.get('waveLength'), 2 * a),
        f = i - l.get('value', e) * i * 2
      u = o ? o.shape.phase : 'auto' === u ? (e * Math.PI) / 4 : u
      var g = s.getItemStyle()
      if (!g.fill) {
        var v = t.get('color'),
          y = e % v.length
        g.fill = v[y]
      }
      var m = new Li({
        shape: {
          waveLength: p,
          radius: a,
          radiusY: i,
          cx: 2 * a,
          cy: 0,
          waterLevel: f,
          amplitude: d,
          phase: u,
          inverse: n
        },
        style: g,
        x: b,
        y: S
      })
      m.shape._waterLevel = f
      var x = r.getModel('emphasis.itemStyle').getItemStyle()
      ;((x.lineWidth = 0), (m.ensureState('emphasis').style = x), te(m))
      var _ = k(h, !0)
      return (_.setStyle({ fill: 'white' }), m.setClipPath(_), m)
    }
    function E(t, e, n) {
      var o = l.getItemModel(t),
        a = o.get('period'),
        i = o.get('direction'),
        r = l.get('value', t),
        s = o.get('phase')
      s = n ? n.shape.phase : 'auto' === s ? (t * Math.PI) / 4 : s
      var u,
        d,
        h = 0
      'auto' === a
        ? ((u = 5e3), (h = 0 === (d = l.count()) ? u : u * (0.2 + ((d - t) / d) * 0.8)))
        : (h = 'function' == typeof a ? a(r, t) : a)
      var p = 0
      ;('right' === i || null == i
        ? (p = Math.PI)
        : 'left' === i
          ? (p = -Math.PI)
          : 'none' === i && (p = 0),
        'none' !== i &&
          o.get('waveAnimation') &&
          e
            .animate('shape', !0)
            .when(0, { phase: s })
            .when(h / 2, { phase: p + s })
            .when(h, { phase: 2 * p + s })
            .during(function () {
              D && D.dirty(!0)
            })
            .start())
    }
    ;(l
      .diff(L)
      .add(function (e) {
        var n = O(e, !1),
          o = n.shape.waterLevel
        ;((n.shape.waterLevel = I ? c / 2 : h),
          v(n, { shape: { waterLevel: o } }, t),
          (n.z2 = 2),
          E(e, n, null),
          s.add(n),
          l.setItemGraphicEl(e, n),
          P.push(n))
      })
      .update(function (e, n) {
        for (
          var o = L.getItemGraphicEl(n),
            i = O(e, !1, o),
            r = {},
            u = ['amplitude', 'cx', 'cy', 'phase', 'radius', 'radiusY', 'waterLevel', 'waveLength'],
            d = 0;
          d < u.length;
          ++d
        ) {
          var h = u[d]
          i.shape.hasOwnProperty(h) && (r[h] = i.shape[h])
        }
        var p = {},
          f = ['fill', 'opacity', 'shadowBlur', 'shadowColor']
        for (d = 0; d < f.length; ++d) {
          h = f[d]
          i.style.hasOwnProperty(h) && (p[h] = i.style[h])
        }
        ;(I && (r.radiusY = c / 2),
          m(o, { shape: r, x: i.x, y: i.y }, t),
          t.isUniversalTransitionEnabled && t.isUniversalTransitionEnabled()
            ? m(o, { style: p }, t)
            : o.useStyle(p))
        var g = o.getClipPath(),
          v = i.getClipPath()
        ;(o.setClipPath(i.getClipPath()),
          (o.shape.inverse = i.inverse),
          g && v && a._shape === A && !Ri(A) && m(v, { shape: g.shape }, t, { isFrom: !0 }),
          E(e, o, o),
          s.add(o),
          l.setItemGraphicEl(e, o),
          P.push(o))
      })
      .remove(function (t) {
        var e = L.getItemGraphicEl(t)
        s.remove(e)
      })
      .execute(),
      u.get('label.show') &&
        s.add(
          (function (e) {
            var n = u.getModel('label')
            function o() {
              var e = t.getFormattedLabel(0, 'normal'),
                n = 100 * l.get('value', 0),
                o = l.getName(0) || t.name
              return (isNaN(n) || (o = n.toFixed(0) + '%'), null == e ? o : e)
            }
            var a = {
                z2: 10,
                shape: { x: C, y: T, width: 2 * (I ? h[0] : h), height: 2 * (I ? h[1] : h) },
                style: { fill: 'transparent' },
                textConfig: { position: n.get('position') || 'inside' },
                silent: !0
              },
              r = {
                style: {
                  text: o(),
                  textAlign: n.get('align'),
                  textVerticalAlign: n.get('baseline')
                }
              }
            Object.assign(r.style, ke(n))
            var s = new ee(a),
              d = new ee(a)
            ;((d.disableLabelAnimation = !0), (s.disableLabelAnimation = !0))
            var p = new R(r),
              c = new R(r)
            ;(s.setTextContent(p), d.setTextContent(c))
            var f = n.get('insideColor')
            c.style.fill = f
            var g = new i()
            ;(g.add(s), g.add(d))
            var v = k(h, !0)
            return (
              (D = new Re({ shape: { paths: e }, x: b, y: S })).setClipPath(v),
              d.setClipPath(D),
              g
            )
          })(P)
        ),
      (this._shape = A),
      (this._data = l))
  },
  dispose: function () {}
}),
  h([
    Ve,
    Ze,
    Ne,
    Be,
    function (t) {
      ;(t.registerTransform(Za), t.registerTransform(Na))
    },
    Fe,
    Ge,
    We,
    function (t) {
      ;(t.registerComponentModel(_o),
        t.registerComponentView(Mo),
        mo('saveAsImage', wo),
        mo('magicType', Co),
        mo('dataView', Oo),
        mo('dataZoom', ia),
        mo('restore', Bo),
        h(go))
    },
    function (t) {
      ;(h(ya), h(Aa))
    },
    He,
    Ue,
    function (t) {
      ;(t.registerChartView(Hn),
        t.registerSeriesModel(jn),
        t.registerLayout(Wn),
        t.registerVisual(Kn))
    },
    Ye,
    function (t) {
      ;(h(p), t.registerSeriesModel(pn), t.registerChartView(vn), t.registerLayout(l('scatter')))
    },
    Xe,
    function (t) {
      ;(t.registerChartView(On), t.registerSeriesModel(En))
    },
    je,
    function (t) {
      ;(t.registerUpdateLifecycle('series:beforeupdate', function (t, e, n) {
        y(ye(n.seriesTransition), function (t) {
          y(ye(t.to), function (t) {
            for (var e = n.updatedSeries, o = 0; o < e.length; o++)
              ((null != t.seriesIndex && t.seriesIndex === e[o].seriesIndex) ||
                (null != t.seriesId && t.seriesId === e[o].id)) &&
                (e[o][Ie] = !0)
          })
        })
      }),
        t.registerUpdateLifecycle('series:transition', function (t, e, n) {
          var o = _i(e)
          if (o.oldSeries && n.updatedSeries && n.optionChanged) {
            var a = n.seriesTransition
            if (a)
              y(ye(a), function (t) {
                !(function (t, e, n, o) {
                  var a = [],
                    i = []
                  ;(y(ye(t.from), function (t) {
                    var n = Di(e.oldSeries, t)
                    n >= 0 &&
                      a.push({
                        dataGroupId: e.oldDataGroupIds[n],
                        data: e.oldData[n],
                        divide: Ti(e.oldData[n]),
                        dim: t.dimension
                      })
                  }),
                    y(ye(t.to), function (t) {
                      var o = Di(n.updatedSeries, t)
                      if (o >= 0) {
                        var a = n.updatedSeries[o].getData()
                        i.push({
                          dataGroupId: e.oldDataGroupIds[o],
                          data: a,
                          divide: Ti(a),
                          dim: t.dimension
                        })
                      }
                    }),
                    a.length > 0 && i.length > 0 && Ii(a, i, o))
                })(t, o, n, e)
              })
            else {
              var i = (function (t, e) {
                var n = lt(),
                  o = lt(),
                  a = lt()
                return (
                  y(t.oldSeries, function (e, n) {
                    var i = t.oldDataGroupIds[n],
                      r = t.oldData[n],
                      s = Ai(e),
                      l = Ci(s)
                    ;(o.set(l, { dataGroupId: i, data: r }),
                      b(s) &&
                        y(s, function (t) {
                          a.set(t, { key: l, dataGroupId: i, data: r })
                        }))
                  }),
                  y(e.updatedSeries, function (t) {
                    if (t.isUniversalTransitionEnabled() && t.isAnimationEnabled()) {
                      var e = t.get('dataGroupId'),
                        i = t.getData(),
                        r = Ai(t),
                        s = Ci(r),
                        l = o.get(s)
                      if (l)
                        n.set(s, {
                          oldSeries: [
                            { dataGroupId: l.dataGroupId, divide: Ti(l.data), data: l.data }
                          ],
                          newSeries: [{ dataGroupId: e, divide: Ti(i), data: i }]
                        })
                      else if (b(r)) {
                        var u = []
                        ;(y(r, function (t) {
                          var e = o.get(t)
                          e.data &&
                            u.push({ dataGroupId: e.dataGroupId, divide: Ti(e.data), data: e.data })
                        }),
                          u.length &&
                            n.set(s, {
                              oldSeries: u,
                              newSeries: [{ dataGroupId: e, data: i, divide: Ti(i) }]
                            }))
                      } else {
                        var d = a.get(r)
                        if (d) {
                          var h = n.get(d.key)
                          ;(h ||
                            ((h = {
                              oldSeries: [
                                { dataGroupId: d.dataGroupId, data: d.data, divide: Ti(d.data) }
                              ],
                              newSeries: []
                            }),
                            n.set(d.key, h)),
                            h.newSeries.push({ dataGroupId: e, data: i, divide: Ti(i) }))
                        }
                      }
                    }
                  }),
                  n
                )
              })(o, n)
              y(i.keys(), function (t) {
                var n = i.get(t)
                Ii(n.oldSeries, n.newSeries, e)
              })
            }
            y(n.updatedSeries, function (t) {
              t[Ie] && (t[Ie] = !1)
            })
          }
          for (
            var r = t.getSeries(),
              s = (o.oldSeries = []),
              l = (o.oldDataGroupIds = []),
              u = (o.oldData = []),
              d = 0;
            d < r.length;
            d++
          ) {
            var h = r[d].getData()
            h.count() < xi && (s.push(r[d]), l.push(r[d].get('dataGroupId')), u.push(h))
          }
        }))
    },
    qe
  ]))
const zi = Ke({
  __name: 'Echart',
  props: {
    option: {},
    renderer: { default: 'canvas' },
    resize: { type: Boolean, default: !0 },
    theme: {},
    width: {},
    height: {},
    onClick: {}
  },
  setup(t, { expose: e }) {
    const n = t,
      o = $e(() =>
        n.width || n.height
          ? { height: n.height + 'px', width: n.width + 'px' }
          : { height: '100%', width: '100%' }
      ),
      a = Qe(),
      i = Qe(),
      r = () => {
        i.value && i.value.setOption(n.option, { notMerge: !0 })
      }
    Je(n, () => {
      r()
    })
    const s = (t) => n.onClick && n.onClick(t),
      l = () => {
        i.value && n.resize && i.value.resize({ animation: { duration: 300 } })
      },
      u = hn(l, 300, { maxWait: 800 }),
      d = tn(),
      { screenfull: h, collapse: p, tagsView: c, footer: f } = en(d)
    return (
      Je(
        () => [h, p, c, f],
        () => {
          u()
        },
        { deep: !0 }
      ),
      nn(() => {
        ;(on(() => {
          a.value &&
            ((i.value = Ee.getInstanceByDom(a.value)),
            i.value ||
              ((i.value = dn(Ee.init(a.value, n.theme, { renderer: n.renderer }))),
              i.value.on('click', s),
              r()))
        }),
          window.addEventListener('resize', u))
      }),
      an(() => {
        i.value && i.value.resize()
      }),
      rn(() => {
        var t
        ;(null == (t = i.value) || t.dispose(), window.removeEventListener('resize', u))
      }),
      e({ getInstance: () => i.value, resize: l, draw: r }),
      (t, e) => (
        sn(),
        ln('div', { id: 'echarts', ref_key: 'chartRef', ref: a, style: un(o.value) }, null, 4)
      )
    )
  }
})
export { zi as _ }
