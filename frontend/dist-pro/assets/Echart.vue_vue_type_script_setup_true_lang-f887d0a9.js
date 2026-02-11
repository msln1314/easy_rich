import {
  _ as t,
  M as e,
  C as a,
  Z as i,
  s as n,
  g as o,
  a as r,
  b as s,
  c as l,
  d as u,
  m as d,
  e as c,
  f as h,
  h as p,
  i as f,
  j as m,
  S as g,
  k as y,
  u as v,
  l as x,
  n as w,
  o as b,
  p as S,
  q as M,
  r as _,
  t as I,
  v as C,
  w as D,
  x as E,
  y as T,
  z as A,
  A as P,
  B as L,
  D as R,
  E as k,
  F as O,
  G as W,
  H as z,
  I as B,
  J as N,
  K as F,
  L as G,
  N as Y,
  O as V,
  P as X,
  Q as H,
  R as j,
  T as q,
  U,
  V as Z,
  W as $,
  X as J,
  Y as K,
  $ as Q,
  a0 as tt,
  a1 as et,
  a2 as at,
  a3 as it,
  a4 as nt,
  a5 as ot,
  a6 as rt,
  a7 as st,
  a8 as lt,
  a9 as ut,
  aa as dt,
  ab as ct,
  ac as ht,
  ad as pt,
  ae as ft,
  af as mt,
  ag as gt,
  ah as yt,
  ai as vt,
  aj as xt,
  ak as wt,
  al as bt,
  am as St,
  an as Mt,
  ao as _t,
  ap as It,
  aq as Ct,
  ar as Dt,
  as as Et,
  at as Tt,
  au as At,
  av as Pt,
  aw as Lt,
  ax as Rt,
  ay as kt,
  az as Ot,
  aA as Wt,
  aB as zt,
  aC as Bt,
  aD as Nt,
  aE as Ft,
  aF as Gt,
  aG as Yt,
  aH as Vt,
  aI as Xt,
  aJ as Ht
} from './echarts-ef988edf.js'
import {
  e as jt,
  ad as qt,
  B as Ut,
  f as Zt,
  k as $t,
  r as Jt,
  d5 as Kt,
  w as Qt,
  a2 as te,
  aj as ee,
  d6 as ae,
  o as ie,
  j as ne,
  s as oe,
  n as re,
  H as se
} from './index-820a519e.js'
import { d as le } from './debounce-5bc596c6.js'
const ue = (function (s) {
  function l() {
    var t = (null !== s && s.apply(this, arguments)) || this
    return ((t.type = l.type), t)
  }
  return (
    t(l, s),
    (l.prototype.render = function (t, a, i, n) {
      if (!n || 'mapToggleSelect' !== n.type || n.from !== this.uid) {
        var o = this.group
        if ((o.removeAll(), !t.getHostGeoModel())) {
          if (
            (this._mapDraw && n && 'geoRoam' === n.type && this._mapDraw.resetForLabelLayout(),
            n && 'geoRoam' === n.type && 'series' === n.componentType && n.seriesId === t.id)
          )
            (r = this._mapDraw) && o.add(r.group)
          else if (t.needsDrawMap) {
            var r = this._mapDraw || new e(i)
            ;(o.add(r.group), r.draw(t, a, i, this, n), (this._mapDraw = r))
          } else (this._mapDraw && this._mapDraw.remove(), (this._mapDraw = null))
          t.get('showLegendSymbol') && a.getComponent('legend') && this._renderSymbols(t, a, i)
        }
      }
    }),
    (l.prototype.remove = function () {
      ;(this._mapDraw && this._mapDraw.remove(), (this._mapDraw = null), this.group.removeAll())
    }),
    (l.prototype.dispose = function () {
      ;(this._mapDraw && this._mapDraw.remove(), (this._mapDraw = null))
    }),
    (l.prototype._renderSymbols = function (t, e, s) {
      var l = t.originalData,
        u = this.group
      l.each(l.mapDimension('value'), function (e, s) {
        if (!isNaN(e)) {
          var d = l.getItemLayout(s)
          if (d && d.point) {
            var c = d.point,
              h = d.offset,
              p = new a({
                style: { fill: t.getData().getVisual('style').fill },
                shape: { cx: c[0] + 9 * h, cy: c[1], r: 3 },
                silent: !0,
                z2: 8 + (h ? 0 : i + 1)
              })
            if (!h) {
              var f = t.mainSeries.getData(),
                m = l.getName(s),
                g = f.indexOfName(m),
                y = l.getItemModel(s),
                v = y.getModel('label'),
                x = f.getItemGraphicEl(g)
              ;(n(p, o(y), {
                labelFetcher: {
                  getFormattedLabel: function (e, a) {
                    return t.getFormattedLabel(g, a)
                  }
                },
                defaultText: m
              }),
                (p.disableLabelAnimation = !0),
                v.get('position') || p.setTextConfig({ position: 'bottom' }),
                (x.onHoverStateChange = function (t) {
                  r(p, t)
                }))
            }
            u.add(p)
          }
        }
      })
    }),
    (l.type = 'map'),
    l
  )
})(s)
const de = (function (e) {
  function a() {
    var t = (null !== e && e.apply(this, arguments)) || this
    return (
      (t.type = a.type),
      (t.needsDrawMap = !1),
      (t.seriesGroup = []),
      (t.getTooltipPosition = function (t) {
        if (null != t) {
          var e = this.getData().getName(t),
            a = this.coordinateSystem,
            i = a.getRegion(e)
          return i && a.dataToPoint(i.getCenter())
        }
      }),
      t
    )
  }
  return (
    t(a, e),
    (a.prototype.getInitialData = function (t) {
      for (
        var e = l(this, { coordDimensions: ['value'], encodeDefaulter: u(d, this) }),
          a = c(),
          i = [],
          n = 0,
          o = e.count();
        n < o;
        n++
      ) {
        var r = e.getName(n)
        a.set(r, !0)
      }
      var s = h.load(this.getMapType(), this.option.nameMap, this.option.nameProperty)
      return (
        p(s.regions, function (t) {
          var e = t.name
          a.get(e) || i.push(e)
        }),
        e.appendValues([], i),
        e
      )
    }),
    (a.prototype.getHostGeoModel = function () {
      var t = this.option.geoIndex
      return null != t ? this.ecModel.getComponent('geo', t) : null
    }),
    (a.prototype.getMapType = function () {
      return (this.getHostGeoModel() || this).option.map
    }),
    (a.prototype.getRawValue = function (t) {
      var e = this.getData()
      return e.get(e.mapDimension('value'), t)
    }),
    (a.prototype.getRegionModel = function (t) {
      var e = this.getData()
      return e.getItemModel(e.indexOfName(t))
    }),
    (a.prototype.formatTooltip = function (t, e, a) {
      for (
        var i = this.getData(),
          n = this.getRawValue(t),
          o = i.getName(t),
          r = this.seriesGroup,
          s = [],
          l = 0;
        l < r.length;
        l++
      ) {
        var u = r[l].originalData.indexOfName(o),
          d = i.mapDimension('value')
        isNaN(r[l].originalData.get(d, u)) || s.push(r[l].name)
      }
      return f('section', {
        header: s.join(', '),
        noHeader: !s.length,
        blocks: [f('nameValue', { name: o, value: n })]
      })
    }),
    (a.prototype.setZoom = function (t) {
      this.option.zoom = t
    }),
    (a.prototype.setCenter = function (t) {
      this.option.center = t
    }),
    (a.prototype.getLegendIcon = function (t) {
      var e = t.icon || 'roundRect',
        a = m(e, 0, 0, t.itemWidth, t.itemHeight, t.itemStyle.fill)
      return (
        a.setStyle(t.itemStyle),
        (a.style.stroke = 'none'),
        e.indexOf('empty') > -1 &&
          ((a.style.stroke = a.style.fill), (a.style.fill = '#fff'), (a.style.lineWidth = 2)),
        a
      )
    }),
    (a.type = 'series.map'),
    (a.dependencies = ['geo']),
    (a.layoutMode = 'box'),
    (a.defaultOption = {
      z: 2,
      coordinateSystem: 'geo',
      map: '',
      left: 'center',
      top: 'center',
      aspectScale: null,
      showLegendSymbol: !0,
      boundingCoords: null,
      center: null,
      zoom: 1,
      scaleLimit: null,
      selectedMode: !0,
      label: { show: !1, color: '#000' },
      itemStyle: { borderWidth: 0.5, borderColor: '#444', areaColor: '#eee' },
      emphasis: {
        label: { show: !0, color: 'rgb(100,0,0)' },
        itemStyle: { areaColor: 'rgba(255,215,0,0.8)' }
      },
      select: {
        label: { show: !0, color: 'rgb(100,0,0)' },
        itemStyle: { color: 'rgba(255,215,0,0.8)' }
      },
      nameProperty: 'name'
    }),
    a
  )
})(g)
function ce(t) {
  var e = {}
  ;(t.eachSeriesByType('map', function (t) {
    var a = t.getHostGeoModel(),
      i = a ? 'o' + a.id : 'i' + t.getMapType()
    ;(e[i] = e[i] || []).push(t)
  }),
    p(e, function (t, e) {
      for (
        var a,
          i,
          n,
          o =
            ((a = y(t, function (t) {
              return t.getData()
            })),
            (i = t[0].get('mapValueCalculation')),
            (n = {}),
            p(a, function (t) {
              t.each(t.mapDimension('value'), function (e, a) {
                var i = 'ec-' + t.getName(a)
                ;((n[i] = n[i] || []), isNaN(e) || n[i].push(e))
              })
            }),
            a[0].map(a[0].mapDimension('value'), function (t, e) {
              for (
                var o = 'ec-' + a[0].getName(e),
                  r = 0,
                  s = 1 / 0,
                  l = -1 / 0,
                  u = n[o].length,
                  d = 0;
                d < u;
                d++
              )
                ((s = Math.min(s, n[o][d])), (l = Math.max(l, n[o][d])), (r += n[o][d]))
              return 0 === u ? NaN : 'min' === i ? s : 'max' === i ? l : 'average' === i ? r / u : r
            })),
          r = 0;
        r < t.length;
        r++
      )
        t[r].originalData = t[r].getData()
      for (r = 0; r < t.length; r++)
        ((t[r].seriesGroup = t),
          (t[r].needsDrawMap = 0 === r && !t[r].getHostGeoModel()),
          t[r].setData(o.cloneShallow()),
          (t[r].mainSeries = t[0]))
    }))
}
function he(t) {
  var e = {}
  t.eachSeriesByType('map', function (a) {
    var i = a.getMapType()
    if (!a.getHostGeoModel() && !e[i]) {
      var n = {}
      p(a.seriesGroup, function (e) {
        var a = e.coordinateSystem,
          i = e.originalData
        e.get('showLegendSymbol') &&
          t.getComponent('legend') &&
          i.each(i.mapDimension('value'), function (t, e) {
            var o = i.getName(e),
              r = a.getRegion(o)
            if (r && !isNaN(t)) {
              var s = n[o] || 0,
                l = a.dataToPoint(r.getCenter())
              ;((n[o] = s + 1), i.setItemLayout(e, { point: l, offset: s }))
            }
          })
      })
      var o = a.getData()
      ;(o.each(function (t) {
        var e = o.getName(t),
          a = o.getItemLayout(t) || {}
        ;((a.showLabel = !n[e]), o.setItemLayout(t, a))
      }),
        (e[i] = !0))
    }
  })
}
function pe(t) {
  ;(!(function (t) {
    if (t.parallel) return
    var e = !1
    ;(p(t.series, function (t) {
      t && 'parallel' === t.type && (e = !0)
    }),
      e && (t.parallel = [{}]))
  })(t),
    (function (t) {
      var e = b(t.parallelAxis)
      p(e, function (e) {
        if (S(e)) {
          var a = e.parallelIndex || 0,
            i = b(t.parallel)[a]
          i && i.parallelAxisDefault && M(e, i.parallelAxisDefault, !1)
        }
      })
    })(t))
}
var fe = (function (e) {
    function a() {
      var t = (null !== e && e.apply(this, arguments)) || this
      return ((t.type = a.type), t)
    }
    return (
      t(a, e),
      (a.prototype.render = function (t, e, a) {
        ;((this._model = t),
          (this._api = a),
          this._handlers ||
            ((this._handlers = {}),
            p(
              me,
              function (t, e) {
                a.getZr().on(e, (this._handlers[e] = _(t, this)))
              },
              this
            )),
          I(this, '_throttledDispatchExpand', t.get('axisExpandRate'), 'fixRate'))
      }),
      (a.prototype.dispose = function (t, e) {
        ;(C(this, '_throttledDispatchExpand'),
          p(this._handlers, function (t, a) {
            e.getZr().off(a, t)
          }),
          (this._handlers = null))
      }),
      (a.prototype._throttledDispatchExpand = function (t) {
        this._dispatchExpand(t)
      }),
      (a.prototype._dispatchExpand = function (t) {
        t && this._api.dispatchAction(D({ type: 'parallelAxisExpand' }, t))
      }),
      (a.type = 'parallel'),
      a
    )
  })(E),
  me = {
    mousedown: function (t) {
      ge(this, 'click') && (this._mouseDownPoint = [t.offsetX, t.offsetY])
    },
    mouseup: function (t) {
      var e = this._mouseDownPoint
      if (ge(this, 'click') && e) {
        var a = [t.offsetX, t.offsetY]
        if (Math.pow(e[0] - a[0], 2) + Math.pow(e[1] - a[1], 2) > 5) return
        var i = this._model.coordinateSystem.getSlidedAxisExpandWindow([t.offsetX, t.offsetY])
        'none' !== i.behavior && this._dispatchExpand({ axisExpandWindow: i.axisExpandWindow })
      }
      this._mouseDownPoint = null
    },
    mousemove: function (t) {
      if (!this._mouseDownPoint && ge(this, 'mousemove')) {
        var e = this._model,
          a = e.coordinateSystem.getSlidedAxisExpandWindow([t.offsetX, t.offsetY]),
          i = a.behavior
        ;('jump' === i &&
          this._throttledDispatchExpand.debounceNextCall(e.get('axisExpandDebounce')),
          this._throttledDispatchExpand(
            'none' === i
              ? null
              : {
                  axisExpandWindow: a.axisExpandWindow,
                  animation: 'jump' === i ? null : { duration: 0 }
                }
          ))
      }
    }
  }
function ge(t, e) {
  var a = t._model
  return a.get('axisExpandable') && a.get('axisExpandTriggerOn') === e
}
const ye = fe
const ve = (function (e) {
  function a() {
    var t = (null !== e && e.apply(this, arguments)) || this
    return ((t.type = a.type), t)
  }
  return (
    t(a, e),
    (a.prototype.init = function () {
      ;(e.prototype.init.apply(this, arguments), this.mergeOption({}))
    }),
    (a.prototype.mergeOption = function (t) {
      var e = this.option
      ;(t && M(e, t, !0), this._initDimensions())
    }),
    (a.prototype.contains = function (t, e) {
      var a = t.get('parallelIndex')
      return null != a && e.getComponent('parallel', a) === this
    }),
    (a.prototype.setAxisExpand = function (t) {
      p(
        [
          'axisExpandable',
          'axisExpandCenter',
          'axisExpandCount',
          'axisExpandWidth',
          'axisExpandWindow'
        ],
        function (e) {
          t.hasOwnProperty(e) && (this.option[e] = t[e])
        },
        this
      )
    }),
    (a.prototype._initDimensions = function () {
      var t = (this.dimensions = []),
        e = (this.parallelAxisIndex = []),
        a = T(
          this.ecModel.queryComponents({ mainType: 'parallelAxis' }),
          function (t) {
            return (t.get('parallelIndex') || 0) === this.componentIndex
          },
          this
        )
      p(a, function (a) {
        ;(t.push('dim' + a.get('dim')), e.push(a.componentIndex))
      })
    }),
    (a.type = 'parallel'),
    (a.dependencies = ['parallelAxis']),
    (a.layoutMode = 'box'),
    (a.defaultOption = {
      z: 0,
      left: 80,
      top: 60,
      right: 80,
      bottom: 60,
      layout: 'horizontal',
      axisExpandable: !1,
      axisExpandCenter: null,
      axisExpandCount: 0,
      axisExpandWidth: 50,
      axisExpandRate: 17,
      axisExpandDebounce: 50,
      axisExpandSlideTriggerArea: [-0.15, 0.05, 0.4],
      axisExpandTriggerOn: 'click',
      parallelAxisDefault: null
    }),
    a
  )
})(A)
const xe = (function (e) {
  function a(t, a, i, n, o) {
    var r = e.call(this, t, a, i) || this
    return ((r.type = n || 'value'), (r.axisIndex = o), r)
  }
  return (
    t(a, e),
    (a.prototype.isHorizontal = function () {
      return 'horizontal' !== this.coordinateSystem.getModel().get('layout')
    }),
    a
  )
})(P)
var we = p,
  be = Math.min,
  Se = Math.max,
  Me = Math.floor,
  _e = Math.ceil,
  Ie = F,
  Ce = Math.PI
function De(t, e) {
  return be(Se(t, e[0]), e[1])
}
function Ee(t, e) {
  var a = e.layoutLength / (e.axisCount - 1)
  return { position: a * t, axisNameAvailableWidth: a, axisLabelShow: !0 }
}
function Te(t, e) {
  var a,
    i,
    n = e.layoutLength,
    o = e.axisExpandWidth,
    r = e.axisCount,
    s = e.axisCollapseWidth,
    l = e.winInnerIndices,
    u = s,
    d = !1
  return (
    t < l[0]
      ? ((a = t * s), (i = s))
      : t <= l[1]
        ? ((a = e.axisExpandWindow0Pos + t * o - e.axisExpandWindow[0]), (u = o), (d = !0))
        : ((a = n - (r - 1 - t) * s), (i = s)),
    { position: a, axisNameAvailableWidth: u, axisLabelShow: d, nameTruncateMaxWidth: i }
  )
}
const Ae = (function () {
  function t(t, e, a) {
    ;((this.type = 'parallel'),
      (this._axesMap = c()),
      (this._axesLayout = {}),
      (this.dimensions = t.dimensions),
      (this._model = t),
      this._init(t, e, a))
  }
  return (
    (t.prototype._init = function (t, e, a) {
      var i = t.dimensions,
        n = t.parallelAxisIndex
      we(
        i,
        function (t, a) {
          var i = n[a],
            o = e.getComponent('parallelAxis', i),
            r = this._axesMap.set(t, new xe(t, L(o), [0, 0], o.get('type'), i)),
            s = 'category' === r.type
          ;((r.onBand = s && o.get('boundaryGap')),
            (r.inverse = o.get('inverse')),
            (o.axis = r),
            (r.model = o),
            (r.coordinateSystem = o.coordinateSystem = this))
        },
        this
      )
    }),
    (t.prototype.update = function (t, e) {
      this._updateAxesFromSeries(this._model, t)
    }),
    (t.prototype.containPoint = function (t) {
      var e = this._makeLayoutInfo(),
        a = e.axisBase,
        i = e.layoutBase,
        n = e.pixelDimIndex,
        o = t[1 - n],
        r = t[n]
      return o >= a && o <= a + e.axisLength && r >= i && r <= i + e.layoutLength
    }),
    (t.prototype.getModel = function () {
      return this._model
    }),
    (t.prototype._updateAxesFromSeries = function (t, e) {
      e.eachSeries(function (a) {
        if (t.contains(a, e)) {
          var i = a.getData()
          we(
            this.dimensions,
            function (t) {
              var e = this._axesMap.get(t)
              ;(e.scale.unionExtentFromData(i, i.mapDimension(t)), R(e.scale, e.model))
            },
            this
          )
        }
      }, this)
    }),
    (t.prototype.resize = function (t, e) {
      ;((this._rect = k(t.getBoxLayoutParams(), { width: e.getWidth(), height: e.getHeight() })),
        this._layoutAxes())
    }),
    (t.prototype.getRect = function () {
      return this._rect
    }),
    (t.prototype._makeLayoutInfo = function () {
      var t,
        e = this._model,
        a = this._rect,
        i = ['x', 'y'],
        n = ['width', 'height'],
        o = e.get('layout'),
        r = 'horizontal' === o ? 0 : 1,
        s = a[n[r]],
        l = [0, s],
        u = this.dimensions.length,
        d = De(e.get('axisExpandWidth'), l),
        c = De(e.get('axisExpandCount') || 0, [0, u]),
        h = e.get('axisExpandable') && u > 3 && u > c && c > 1 && d > 0 && s > 0,
        p = e.get('axisExpandWindow')
      p
        ? ((t = De(p[1] - p[0], l)), (p[1] = p[0] + t))
        : ((t = De(d * (c - 1), l)),
          ((p = [d * (e.get('axisExpandCenter') || Me(u / 2)) - t / 2])[1] = p[0] + t))
      var f = (s - t) / (u - c)
      f < 3 && (f = 0)
      var m = [Me(Ie(p[0] / d, 1)) + 1, _e(Ie(p[1] / d, 1)) - 1],
        g = (f / d) * p[0]
      return {
        layout: o,
        pixelDimIndex: r,
        layoutBase: a[i[r]],
        layoutLength: s,
        axisBase: a[i[1 - r]],
        axisLength: a[n[1 - r]],
        axisExpandable: h,
        axisExpandWidth: d,
        axisCollapseWidth: f,
        axisExpandWindow: p,
        axisCount: u,
        winInnerIndices: m,
        axisExpandWindow0Pos: g
      }
    }),
    (t.prototype._layoutAxes = function () {
      var t = this._rect,
        e = this._axesMap,
        a = this.dimensions,
        i = this._makeLayoutInfo(),
        n = i.layout
      ;(e.each(function (t) {
        var e = [0, i.axisLength],
          a = t.inverse ? 1 : 0
        t.setExtent(e[a], e[1 - a])
      }),
        we(
          a,
          function (e, a) {
            var o = (i.axisExpandable ? Te : Ee)(a, i),
              r = {
                horizontal: { x: o.position, y: i.axisLength },
                vertical: { x: 0, y: o.position }
              },
              s = { horizontal: Ce / 2, vertical: 0 },
              l = [r[n].x + t.x, r[n].y + t.y],
              u = s[n],
              d = G()
            ;(O(d, d, u),
              W(d, d, l),
              (this._axesLayout[e] = {
                position: l,
                rotation: u,
                transform: d,
                axisNameAvailableWidth: o.axisNameAvailableWidth,
                axisLabelShow: o.axisLabelShow,
                nameTruncateMaxWidth: o.nameTruncateMaxWidth,
                tickDirection: 1,
                labelDirection: 1
              }))
          },
          this
        ))
    }),
    (t.prototype.getAxis = function (t) {
      return this._axesMap.get(t)
    }),
    (t.prototype.dataToPoint = function (t, e) {
      return this.axisCoordToPoint(this._axesMap.get(e).dataToCoord(t), e)
    }),
    (t.prototype.eachActiveState = function (t, e, a, i) {
      ;(null == a && (a = 0), null == i && (i = t.count()))
      var n = this._axesMap,
        o = this.dimensions,
        r = [],
        s = []
      p(o, function (e) {
        ;(r.push(t.mapDimension(e)), s.push(n.get(e).model))
      })
      for (var l = this.hasAxisBrushed(), u = a; u < i; u++) {
        var d = void 0
        if (l) {
          d = 'active'
          for (var c = t.getValues(r, u), h = 0, f = o.length; h < f; h++) {
            if ('inactive' === s[h].getActiveState(c[h])) {
              d = 'inactive'
              break
            }
          }
        } else d = 'normal'
        e(d, u)
      }
    }),
    (t.prototype.hasAxisBrushed = function () {
      for (var t = this.dimensions, e = this._axesMap, a = !1, i = 0, n = t.length; i < n; i++)
        'normal' !== e.get(t[i]).model.getActiveState() && (a = !0)
      return a
    }),
    (t.prototype.axisCoordToPoint = function (t, e) {
      var a = this._axesLayout[e]
      return z([t, 0], a.transform)
    }),
    (t.prototype.getAxisLayout = function (t) {
      return B(this._axesLayout[t])
    }),
    (t.prototype.getSlidedAxisExpandWindow = function (t) {
      var e = this._makeLayoutInfo(),
        a = e.pixelDimIndex,
        i = e.axisExpandWindow.slice(),
        n = i[1] - i[0],
        o = [0, e.axisExpandWidth * (e.axisCount - 1)]
      if (!this.containPoint(t)) return { behavior: 'none', axisExpandWindow: i }
      var r,
        s = t[a] - e.layoutBase - e.axisExpandWindow0Pos,
        l = 'slide',
        u = e.axisCollapseWidth,
        d = this._model.get('axisExpandSlideTriggerArea'),
        c = null != d[0]
      if (u)
        (c && u && s < n * d[0]
          ? ((l = 'jump'), (r = s - n * d[2]))
          : c && u && s > n * (1 - d[0])
            ? ((l = 'jump'), (r = s - n * (1 - d[2])))
            : (r = s - n * d[1]) >= 0 && (r = s - n * (1 - d[1])) <= 0 && (r = 0),
          (r *= e.axisExpandWidth / u) ? N(r, i, o, 'all') : (l = 'none'))
      else {
        var h = i[1] - i[0]
        ;(((i = [Se(0, (o[1] * s) / h - h / 2)])[1] = be(o[1], i[0] + h)), (i[0] = i[1] - h))
      }
      return { axisExpandWindow: i, behavior: l }
    }),
    t
  )
})()
const Pe = {
  create: function (t, e) {
    var a = []
    return (
      t.eachComponent('parallel', function (i, n) {
        var o = new Ae(i, t, e)
        ;((o.name = 'parallel_' + n),
          o.resize(i, e),
          (i.coordinateSystem = o),
          (o.model = i),
          a.push(o))
      }),
      t.eachSeries(function (t) {
        if ('parallel' === t.get('coordinateSystem')) {
          var e = t.getReferringComponents('parallel', Y).models[0]
          t.coordinateSystem = e.coordinateSystem
        }
      }),
      a
    )
  }
}
var Le = (function (e) {
  function a() {
    var t = (null !== e && e.apply(this, arguments)) || this
    return ((t.type = a.type), (t.activeIntervals = []), t)
  }
  return (
    t(a, e),
    (a.prototype.getAreaSelectStyle = function () {
      return V([
        ['fill', 'color'],
        ['lineWidth', 'borderWidth'],
        ['stroke', 'borderColor'],
        ['width', 'width'],
        ['opacity', 'opacity']
      ])(this.getModel('areaSelectStyle'))
    }),
    (a.prototype.setActiveIntervals = function (t) {
      var e = (this.activeIntervals = B(t))
      if (e) for (var a = e.length - 1; a >= 0; a--) X(e[a])
    }),
    (a.prototype.getActiveState = function (t) {
      var e = this.activeIntervals
      if (!e.length) return 'normal'
      if (null == t || isNaN(+t)) return 'inactive'
      if (1 === e.length) {
        var a = e[0]
        if (a[0] <= t && t <= a[1]) return 'active'
      } else
        for (var i = 0, n = e.length; i < n; i++) if (e[i][0] <= t && t <= e[i][1]) return 'active'
      return 'inactive'
    }),
    a
  )
})(A)
H(Le, j)
const Re = Le
var ke = ['axisLine', 'axisTickLabel', 'axisName']
const Oe = (function (e) {
  function a() {
    var t = (null !== e && e.apply(this, arguments)) || this
    return ((t.type = a.type), t)
  }
  return (
    t(a, e),
    (a.prototype.init = function (t, a) {
      ;(e.prototype.init.apply(this, arguments),
        (this._brushController = new q(a.getZr())).on('brush', _(this._onBrush, this)))
    }),
    (a.prototype.render = function (t, e, a, i) {
      if (
        !(function (t, e, a) {
          return (
            a &&
            'axisAreaSelect' === a.type &&
            e.findComponents({ mainType: 'parallelAxis', query: a })[0] === t
          )
        })(t, e, i)
      ) {
        ;((this.axisModel = t), (this.api = a), this.group.removeAll())
        var n = this._axisGroup
        if (((this._axisGroup = new U()), this.group.add(this._axisGroup), t.get('show'))) {
          var o = (function (t, e) {
              return e.getComponent('parallel', t.get('parallelIndex'))
            })(t, e),
            r = o.coordinateSystem,
            s = t.getAreaSelectStyle(),
            l = s.width,
            u = t.axis.dim,
            d = r.getAxisLayout(u),
            c = D({ strokeContainThreshold: l }, d),
            h = new Z(t, c)
          ;(p(ke, h.add, h),
            this._axisGroup.add(h.getGroup()),
            this._refreshBrushController(c, s, t, o, l, a),
            $(n, this._axisGroup, t))
        }
      }
    }),
    (a.prototype._refreshBrushController = function (t, e, a, i, n, o) {
      var r = a.axis.getExtent(),
        s = r[1] - r[0],
        l = Math.min(30, 0.1 * Math.abs(s)),
        u = J.create({ x: r[0], y: -n / 2, width: s, height: n })
      ;((u.x -= l),
        (u.width += 2 * l),
        this._brushController
          .mount({ enableGlobalPan: !0, rotation: t.rotation, x: t.position[0], y: t.position[1] })
          .setPanels([
            {
              panelId: 'pl',
              clipPath: K(u),
              isTargetByCursor: Q(u, o, i),
              getLinearBrushOtherExtent: tt(u, 0)
            }
          ])
          .enableBrush({ brushType: 'lineX', brushStyle: e, removeOnClick: !0 })
          .updateCovers(
            (function (t) {
              var e = t.axis
              return y(t.activeIntervals, function (t) {
                return {
                  brushType: 'lineX',
                  panelId: 'pl',
                  range: [e.dataToCoord(t[0], !0), e.dataToCoord(t[1], !0)]
                }
              })
            })(a)
          ))
    }),
    (a.prototype._onBrush = function (t) {
      var e = t.areas,
        a = this.axisModel,
        i = a.axis,
        n = y(e, function (t) {
          return [i.coordToData(t.range[0], !0), i.coordToData(t.range[1], !0)]
        })
      ;(!a.option.realtime === t.isEnd || t.removeOnClick) &&
        this.api.dispatchAction({ type: 'axisAreaSelect', parallelAxisId: a.id, intervals: n })
    }),
    (a.prototype.dispose = function () {
      this._brushController.dispose()
    }),
    (a.type = 'parallelAxis'),
    a
  )
})(E)
var We = { type: 'axisAreaSelect', event: 'axisAreaSelected' }
var ze = {
  type: 'value',
  areaSelectStyle: {
    width: 20,
    borderWidth: 1,
    borderColor: 'rgba(160,197,232)',
    color: 'rgba(160,197,232)',
    opacity: 0.3
  },
  realtime: !0,
  z: 10
}
var Be = ['itemStyle', 'borderWidth'],
  Ne = [
    { xy: 'x', wh: 'width', index: 0, posDesc: ['left', 'right'] },
    { xy: 'y', wh: 'height', index: 1, posDesc: ['top', 'bottom'] }
  ],
  Fe = new a()
function Ge(t, e, a, i) {
  var n = t.getItemLayout(e),
    o = a.get('symbolRepeat'),
    r = a.get('symbolClip'),
    s = a.get('symbolPosition') || 'start',
    l = ((a.get('symbolRotate') || 0) * Math.PI) / 180 || 0,
    u = a.get('symbolPatternSize') || 2,
    d = a.isAnimationEnabled(),
    c = {
      dataIndex: e,
      layout: n,
      itemModel: a,
      symbolType: t.getItemVisual(e, 'symbol') || 'circle',
      style: t.getItemVisual(e, 'style'),
      symbolClip: r,
      symbolRepeat: o,
      symbolRepeatDirection: a.get('symbolRepeatDirection'),
      symbolPatternSize: u,
      rotation: l,
      animationModel: d ? a : null,
      hoverScale: d && a.get(['emphasis', 'scale']),
      z2: a.getShallow('z', !0) || 0
    }
  ;(!(function (t, e, a, i, n) {
    var o,
      r = i.valueDim,
      s = t.get('symbolBoundingData'),
      l = i.coordSys.getOtherAxis(i.coordSys.getBaseAxis()),
      u = l.toGlobalCoord(l.dataToCoord(0)),
      d = 1 - +(a[r.wh] <= 0)
    if (nt(s)) {
      var c = [Ye(l, s[0]) - u, Ye(l, s[1]) - u]
      ;(c[1] < c[0] && c.reverse(), (o = c[d]))
    } else o = null != s ? Ye(l, s) - u : e ? i.coordSysExtent[r.index][d] - u : a[r.wh]
    ;((n.boundingLength = o), e && (n.repeatCutLength = a[r.wh]))
    n.pxSign = o > 0 ? 1 : -1
  })(a, o, n, i, c),
    (function (t, e, a, i, n, o, r, s, l, u) {
      var d,
        c = l.valueDim,
        h = l.categoryDim,
        p = Math.abs(a[h.wh]),
        f = t.getItemVisual(e, 'symbolSize')
      d = nt(f) ? f.slice() : null == f ? ['100%', '100%'] : [f, f]
      ;((d[h.index] = ot(d[h.index], p)),
        (d[c.index] = ot(d[c.index], i ? p : Math.abs(o))),
        (u.symbolSize = d))
      var m = (u.symbolScale = [d[0] / s, d[1] / s])
      m[c.index] *= (l.isHorizontal ? -1 : 1) * r
    })(t, e, n, o, 0, c.boundingLength, c.pxSign, u, i, c),
    (function (t, e, a, i, n) {
      var o = t.get(Be) || 0
      o &&
        (Fe.attr({ scaleX: e[0], scaleY: e[1], rotation: a }),
        Fe.updateTransform(),
        (o /= Fe.getLineScale()),
        (o *= e[i.valueDim.index]))
      n.valueLineWidth = o || 0
    })(a, c.symbolScale, l, i, c))
  var h = c.symbolSize,
    p = it(a.get('symbolOffset'), h)
  return (
    (function (t, e, a, i, n, o, r, s, l, u, d, c) {
      var h = d.categoryDim,
        p = d.valueDim,
        f = c.pxSign,
        m = Math.max(e[p.index] + s, 0),
        g = m
      if (i) {
        var y = Math.abs(l),
          v = rt(t.get('symbolMargin'), '15%') + '',
          x = !1
        v.lastIndexOf('!') === v.length - 1 && ((x = !0), (v = v.slice(0, v.length - 1)))
        var w = ot(v, e[p.index]),
          b = Math.max(m + 2 * w, 0),
          S = x ? 0 : 2 * w,
          M = st(i),
          _ = M ? i : ia((y + S) / b)
        ;((b = m + 2 * (w = (y - _ * m) / 2 / (x ? _ : Math.max(_ - 1, 1)))),
          (S = x ? 0 : 2 * w),
          M || 'fixed' === i || (_ = u ? ia((Math.abs(u) + S) / b) : 0),
          (g = _ * b - S),
          (c.repeatTimes = _),
          (c.symbolMargin = w))
      }
      var I = f * (g / 2),
        C = (c.pathPosition = [])
      ;((C[h.index] = a[h.wh] / 2),
        (C[p.index] = 'start' === r ? I : 'end' === r ? l - I : l / 2),
        o && ((C[0] += o[0]), (C[1] += o[1])))
      var E = (c.bundlePosition = [])
      ;((E[h.index] = a[h.xy]), (E[p.index] = a[p.xy]))
      var T = (c.barRectShape = D({}, a))
      ;((T[p.wh] = f * Math.max(Math.abs(a[p.wh]), Math.abs(C[p.index] + I))), (T[h.wh] = a[h.wh]))
      var A = (c.clipShape = {})
      ;((A[h.xy] = -a[h.xy]), (A[h.wh] = d.ecSize[h.wh]), (A[p.xy] = 0), (A[p.wh] = a[p.wh]))
    })(a, h, n, o, 0, p, s, c.valueLineWidth, c.boundingLength, c.repeatCutLength, i, c),
    c
  )
}
function Ye(t, e) {
  return t.toGlobalCoord(t.dataToCoord(t.scale.parse(e)))
}
function Ve(t) {
  var e = t.symbolPatternSize,
    a = m(t.symbolType, -e / 2, -e / 2, e, e)
  return (a.attr({ culling: !0 }), 'image' !== a.type && a.setStyle({ strokeNoScale: !0 }), a)
}
function Xe(t, e, a, i) {
  var n = t.__pictorialBundle,
    o = a.symbolSize,
    r = a.valueLineWidth,
    s = a.pathPosition,
    l = e.valueDim,
    u = a.repeatTimes || 0,
    d = 0,
    c = o[e.valueDim.index] + r + 2 * a.symbolMargin
  for (
    ta(t, function (t) {
      ;((t.__pictorialAnimationIndex = d),
        (t.__pictorialRepeatTimes = u),
        d < u
          ? ea(t, null, f(d), a, i)
          : ea(t, null, { scaleX: 0, scaleY: 0 }, a, i, function () {
              n.remove(t)
            }),
        d++)
    });
    d < u;
    d++
  ) {
    var h = Ve(a)
    ;((h.__pictorialAnimationIndex = d), (h.__pictorialRepeatTimes = u), n.add(h))
    var p = f(d)
    ea(
      h,
      { x: p.x, y: p.y, scaleX: 0, scaleY: 0 },
      { scaleX: p.scaleX, scaleY: p.scaleY, rotation: p.rotation },
      a,
      i
    )
  }
  function f(t) {
    var e = s.slice(),
      i = a.pxSign,
      n = t
    return (
      ('start' === a.symbolRepeatDirection ? i > 0 : i < 0) && (n = u - 1 - t),
      (e[l.index] = c * (n - u / 2 + 0.5) + s[l.index]),
      { x: e[0], y: e[1], scaleX: a.symbolScale[0], scaleY: a.symbolScale[1], rotation: a.rotation }
    )
  }
}
function He(t, e, a, i) {
  var n = t.__pictorialBundle,
    o = t.__pictorialMainPath
  o
    ? ea(
        o,
        null,
        {
          x: a.pathPosition[0],
          y: a.pathPosition[1],
          scaleX: a.symbolScale[0],
          scaleY: a.symbolScale[1],
          rotation: a.rotation
        },
        a,
        i
      )
    : ((o = t.__pictorialMainPath = Ve(a)),
      n.add(o),
      ea(
        o,
        { x: a.pathPosition[0], y: a.pathPosition[1], scaleX: 0, scaleY: 0, rotation: a.rotation },
        { scaleX: a.symbolScale[0], scaleY: a.symbolScale[1] },
        a,
        i
      ))
}
function je(t, e, a) {
  var i = D({}, e.barRectShape),
    n = t.__pictorialBarRect
  n
    ? ea(n, null, { shape: i }, e, a)
    : (((n = t.__pictorialBarRect =
        new pt({
          z2: 2,
          shape: i,
          silent: !0,
          style: { stroke: 'transparent', fill: 'transparent', lineWidth: 0 }
        })).disableMorphing = !0),
      t.add(n))
}
function qe(t, e, a, i) {
  if (a.symbolClip) {
    var n = t.__pictorialClipPath,
      o = D({}, a.clipShape),
      r = e.valueDim,
      s = a.animationModel,
      l = a.dataIndex
    if (n) lt(n, { shape: o }, s, l)
    else {
      ;((o[r.wh] = 0),
        (n = new pt({ shape: o })),
        t.__pictorialBundle.setClipPath(n),
        (t.__pictorialClipPath = n))
      var u = {}
      ;((u[r.wh] = a.clipShape[r.wh]), ft[i ? 'updateProps' : 'initProps'](n, { shape: u }, s, l))
    }
  }
}
function Ue(t, e) {
  var a = t.getItemModel(e)
  return ((a.getAnimationDelayParams = Ze), (a.isAnimationEnabled = $e), a)
}
function Ze(t) {
  return { index: t.__pictorialAnimationIndex, count: t.__pictorialRepeatTimes }
}
function $e() {
  return this.parentModel.isAnimationEnabled() && !!this.getShallow('animation')
}
function Je(t, e, a, i) {
  var n = new U(),
    o = new U()
  return (
    n.add(o),
    (n.__pictorialBundle = o),
    (o.x = a.bundlePosition[0]),
    (o.y = a.bundlePosition[1]),
    a.symbolRepeat ? Xe(n, e, a) : He(n, 0, a),
    je(n, a, i),
    qe(n, e, a, i),
    (n.__pictorialShapeStr = Qe(t, a)),
    (n.__pictorialSymbolMeta = a),
    n
  )
}
function Ke(t, e, a, i) {
  var n = i.__pictorialBarRect
  n && n.removeTextContent()
  var o = []
  ;(ta(i, function (t) {
    o.push(t)
  }),
    i.__pictorialMainPath && o.push(i.__pictorialMainPath),
    i.__pictorialClipPath && (a = null),
    p(o, function (t) {
      ut(t, { scaleX: 0, scaleY: 0 }, a, e, function () {
        i.parent && i.parent.remove(i)
      })
    }),
    t.setItemGraphicEl(e, null))
}
function Qe(t, e) {
  return [t.getItemVisual(e.dataIndex, 'symbol') || 'none', !!e.symbolRepeat, !!e.symbolClip].join(
    ':'
  )
}
function ta(t, e, a) {
  p(t.__pictorialBundle.children(), function (i) {
    i !== t.__pictorialBarRect && e.call(a, i)
  })
}
function ea(t, e, a, i, n, o) {
  ;(e && t.attr(e),
    i.symbolClip && !n
      ? a && t.attr(a)
      : a && ft[n ? 'updateProps' : 'initProps'](t, a, i.animationModel, i.dataIndex, o))
}
function aa(t, e, a) {
  var i = a.dataIndex,
    r = a.itemModel,
    s = r.getModel('emphasis'),
    l = s.getModel('itemStyle').getItemStyle(),
    u = r.getModel(['blur', 'itemStyle']).getItemStyle(),
    d = r.getModel(['select', 'itemStyle']).getItemStyle(),
    c = r.getShallow('cursor'),
    h = s.get('focus'),
    p = s.get('blurScope'),
    f = s.get('scale')
  ta(t, function (t) {
    if (t instanceof dt) {
      var e = t.style
      t.useStyle(D({ image: e.image, x: e.x, y: e.y, width: e.width, height: e.height }, a.style))
    } else t.useStyle(a.style)
    var i = t.ensureState('emphasis')
    ;((i.style = l),
      f && ((i.scaleX = 1.1 * t.scaleX), (i.scaleY = 1.1 * t.scaleY)),
      (t.ensureState('blur').style = u),
      (t.ensureState('select').style = d),
      c && (t.cursor = c),
      (t.z2 = a.z2))
  })
  var m = e.valueDim.posDesc[+(a.boundingLength > 0)],
    g = t.__pictorialBarRect
  ;(n(g, o(r), {
    labelFetcher: e.seriesModel,
    labelDataIndex: i,
    defaultText: ct(e.seriesModel.getData(), i),
    inheritColor: a.style.fill,
    defaultOpacity: a.style.opacity,
    defaultOutsidePosition: m
  }),
    ht(t, h, p, s.get('disabled')))
}
function ia(t) {
  var e = Math.round(t)
  return Math.abs(t - e) < 1e-4 ? e : Math.ceil(t)
}
const na = (function (e) {
  function a() {
    var t = (null !== e && e.apply(this, arguments)) || this
    return ((t.type = a.type), t)
  }
  return (
    t(a, e),
    (a.prototype.render = function (t, e, a) {
      var i = this.group,
        n = t.getData(),
        o = this._data,
        r = t.coordinateSystem,
        s = r.getBaseAxis().isHorizontal(),
        l = r.master.getRect(),
        u = {
          ecSize: { width: a.getWidth(), height: a.getHeight() },
          seriesModel: t,
          coordSys: r,
          coordSysExtent: [
            [l.x, l.x + l.width],
            [l.y, l.y + l.height]
          ],
          isHorizontal: s,
          valueDim: Ne[+s],
          categoryDim: Ne[1 - +s]
        }
      return (
        n
          .diff(o)
          .add(function (t) {
            if (n.hasValue(t)) {
              var e = Ue(n, t),
                a = Ge(n, t, e, u),
                o = Je(n, u, a)
              ;(n.setItemGraphicEl(t, o), i.add(o), aa(o, u, a))
            }
          })
          .update(function (t, e) {
            var a = o.getItemGraphicEl(e)
            if (n.hasValue(t)) {
              var r = Ue(n, t),
                s = Ge(n, t, r, u),
                l = Qe(n, s)
              ;(a &&
                l !== a.__pictorialShapeStr &&
                (i.remove(a), n.setItemGraphicEl(t, null), (a = null)),
                a
                  ? (function (t, e, a) {
                      var i = a.animationModel,
                        n = a.dataIndex,
                        o = t.__pictorialBundle
                      ;(lt(o, { x: a.bundlePosition[0], y: a.bundlePosition[1] }, i, n),
                        a.symbolRepeat ? Xe(t, e, a, !0) : He(t, e, a, !0))
                      ;(je(t, a, !0), qe(t, e, a, !0))
                    })(a, u, s)
                  : (a = Je(n, u, s, !0)),
                n.setItemGraphicEl(t, a),
                (a.__pictorialSymbolMeta = s),
                i.add(a),
                aa(a, u, s))
            } else i.remove(a)
          })
          .remove(function (t) {
            var e = o.getItemGraphicEl(t)
            e && Ke(o, t, e.__pictorialSymbolMeta.animationModel, e)
          })
          .execute(),
        (this._data = n),
        this.group
      )
    }),
    (a.prototype.remove = function (t, e) {
      var a = this.group,
        i = this._data
      t.get('animation')
        ? i &&
          i.eachItemGraphicEl(function (e) {
            Ke(i, at(e).dataIndex, t, e)
          })
        : a.removeAll()
    }),
    (a.type = 'pictorialBar'),
    a
  )
})(s)
const oa = (function (e) {
  function a() {
    var t = (null !== e && e.apply(this, arguments)) || this
    return ((t.type = a.type), (t.hasSymbolVisual = !0), (t.defaultSymbol = 'roundRect'), t)
  }
  return (
    t(a, e),
    (a.prototype.getInitialData = function (t) {
      return ((t.stack = null), e.prototype.getInitialData.apply(this, arguments))
    }),
    (a.type = 'series.pictorialBar'),
    (a.dependencies = ['grid']),
    (a.defaultOption = mt(gt.defaultOption, {
      symbol: 'circle',
      symbolSize: null,
      symbolRotate: null,
      symbolPosition: null,
      symbolOffset: null,
      symbolMargin: null,
      symbolRepeat: !1,
      symbolRepeatDirection: 'end',
      symbolClip: !1,
      symbolBoundingData: null,
      symbolPatternSize: 400,
      barGap: '-100%',
      progressive: 0,
      emphasis: { scale: !1 },
      select: { itemStyle: { borderColor: '#212121' } }
    })),
    a
  )
})(gt)
var ra = { label: { enabled: !0 }, decal: { show: !1 } },
  sa = Mt(),
  la = {}
function ua(t, e) {
  var a = t.getModel('aria')
  if (a.get('enabled')) {
    var i = B(ra)
    ;(M(i.label, t.getLocaleModel().get('aria'), !1),
      M(a.option, i, !1),
      (function () {
        if (a.getModel('decal').get('show')) {
          var e = c()
          ;(t.eachSeries(function (t) {
            if (!t.isColorBySeries()) {
              var a = e.get(t.type)
              ;(a || ((a = {}), e.set(t.type, a)), (sa(t).scope = a))
            }
          }),
            t.eachRawSeries(function (e) {
              if (!t.isSeriesFiltered(e))
                if (xt(e.enableAriaDecal)) e.enableAriaDecal()
                else {
                  var a = e.getData()
                  if (e.isColorBySeries()) {
                    var i = wt(e.ecModel, e.name, la, t.getSeriesCount()),
                      n = a.getVisual('decal')
                    a.setVisual('decal', u(n, i))
                  } else {
                    var o = e.getRawData(),
                      r = {},
                      s = sa(e).scope
                    a.each(function (t) {
                      var e = a.getRawIndex(t)
                      r[e] = t
                    })
                    var l = o.count()
                    o.each(function (t) {
                      var i = r[t],
                        n = o.getName(t) || t + '',
                        d = wt(e.ecModel, n, s, l),
                        c = a.getItemVisual(i, 'decal')
                      a.setItemVisual(i, 'decal', u(c, d))
                    })
                  }
                }
              function u(t, e) {
                var a = t ? D(D({}, e), t) : e
                return ((a.dirty = !0), a)
              }
            }))
        }
      })(),
      (function () {
        var i = t.getLocaleModel().get('aria'),
          o = a.getModel('label')
        if (((o.option = bt(o.option, i)), !o.get('enabled'))) return
        var r = e.getZr().dom
        if (o.get('description')) return void r.setAttribute('aria-label', o.get('description'))
        var s,
          l = t.getSeriesCount(),
          u = o.get(['data', 'maxCount']) || 10,
          d = o.get(['series', 'maxCount']) || 10,
          c = Math.min(l, d)
        if (l < 1) return
        var h = (function () {
          var e = t.get('title')
          e && e.length && (e = e[0])
          return e && e.text
        })()
        s = h
          ? n(o.get(['general', 'withTitle']), { title: h })
          : o.get(['general', 'withoutTitle'])
        var p = []
        ;((s += n(
          l > 1 ? o.get(['series', 'multiple', 'prefix']) : o.get(['series', 'single', 'prefix']),
          { seriesCount: l }
        )),
          t.eachSeries(function (e, a) {
            if (a < c) {
              var i = void 0,
                r = e.get('name') ? 'withName' : 'withoutName'
              i = n(
                (i = l > 1 ? o.get(['series', 'multiple', r]) : o.get(['series', 'single', r])),
                {
                  seriesId: e.seriesIndex,
                  seriesName: e.get('name'),
                  seriesType:
                    ((x = e.subType),
                    t.getLocaleModel().get(['series', 'typeNames'])[x] || '自定义图')
                }
              )
              var s = e.getData()
              if (s.count() > u) i += n(o.get(['data', 'partialData']), { displayCnt: u })
              else i += o.get(['data', 'allData'])
              for (
                var d = o.get(['data', 'separator', 'middle']),
                  h = o.get(['data', 'separator', 'end']),
                  f = [],
                  m = 0;
                m < s.count();
                m++
              )
                if (m < u) {
                  var g = s.getName(m),
                    y = s.getValues(m),
                    v = o.get(['data', g ? 'withName' : 'withoutName'])
                  f.push(n(v, { name: g, value: y.join(d) }))
                }
              ;((i += f.join(d) + h), p.push(i))
            }
            var x
          }))
        var f = o.getModel(['series', 'multiple', 'separator']),
          m = f.get('middle'),
          g = f.get('end')
        ;((s += p.join(m) + g), r.setAttribute('aria-label', s))
      })())
  }
  function n(t, e) {
    if (!St(t)) return t
    var a = t
    return (
      p(e, function (t, e) {
        a = a.replace(new RegExp('\\{\\s*' + e + '\\s*\\}', 'g'), t)
      }),
      a
    )
  }
}
function da(t) {
  if (t && t.aria) {
    var e = t.aria
    ;(null != e.show && (e.enabled = e.show),
      (e.label = e.label || {}),
      p(['description', 'general', 'series', 'data'], function (t) {
        null != e[t] && (e.label[t] = e[t])
      }))
  }
}
;(v([
  _t,
  It,
  Ct,
  Dt,
  Et,
  function (t) {
    ;(t.registerPreprocessor(da), t.registerVisual(t.PRIORITY.VISUAL.ARIA, ua))
  },
  function (t) {
    ;(t.registerComponentView(ye),
      t.registerComponentModel(ve),
      t.registerCoordinateSystem('parallel', Pe),
      t.registerPreprocessor(pe),
      t.registerComponentModel(Re),
      t.registerComponentView(Oe),
      et(t, 'parallel', Re, ze),
      (function (t) {
        ;(t.registerAction(We, function (t, e) {
          e.eachComponent({ mainType: 'parallelAxis', query: t }, function (e) {
            e.axis.model.setActiveIntervals(t.intervals)
          })
        }),
          t.registerAction('parallelAxisExpand', function (t, e) {
            e.eachComponent({ mainType: 'parallel', query: t }, function (e) {
              e.setAxisExpand(t)
            })
          }))
      })(t))
  },
  Tt,
  At,
  Pt,
  function (t) {
    ;(v(x),
      t.registerChartView(ue),
      t.registerSeriesModel(de),
      t.registerLayout(he),
      t.registerProcessor(t.PRIORITY.PROCESSOR.STATISTIC, ce),
      w('map', t.registerAction))
  },
  Lt,
  function (t) {
    ;(t.registerChartView(na),
      t.registerSeriesModel(oa),
      t.registerLayout(t.PRIORITY.VISUAL.LAYOUT, u(yt, 'pictorialBar')),
      t.registerLayout(t.PRIORITY.VISUAL.PROGRESSIVE_LAYOUT, vt('pictorialBar')))
  },
  Rt
]),
  Ot({
    type: 'series.wordCloud',
    visualStyleAccessPath: 'textStyle',
    visualStyleMapper: function (t) {
      return { fill: t.get('color') }
    },
    visualDrawType: 'fill',
    optionUpdated: function () {
      var t = this.option
      t.gridSize = Math.max(Math.floor(t.gridSize), 4)
    },
    getInitialData: function (t, e) {
      var a = Wt(t.data, { coordDimensions: ['value'] }),
        i = new zt(a, this)
      return (i.initData(t.data), i)
    },
    defaultOption: {
      maskImage: null,
      shape: 'circle',
      keepAspect: !1,
      left: 'center',
      top: 'center',
      width: '70%',
      height: '80%',
      sizeRange: [12, 60],
      rotationRange: [-90, 90],
      rotationStep: 45,
      gridSize: 8,
      drawOutOfBound: !1,
      shrinkToFit: !1,
      textStyle: { fontWeight: 'normal' }
    }
  }),
  Bt({
    type: 'wordCloud',
    render: function (t, e, a) {
      var i = this.group
      i.removeAll()
      var n = t.getData(),
        o = t.get('gridSize')
      ;((t.layoutInstance.ondraw = function (e, a, r, s) {
        var l = n.getItemModel(r),
          u = l.getModel('textStyle'),
          d = new Nt({
            style: Ft(u),
            scaleX: 1 / s.info.mu,
            scaleY: 1 / s.info.mu,
            x: (s.gx + s.info.gw / 2) * o,
            y: (s.gy + s.info.gh / 2) * o,
            rotation: s.rot
          })
        ;(d.setStyle({
          x: s.info.fillTextOffsetX,
          y: s.info.fillTextOffsetY + 0.5 * a,
          text: e,
          verticalAlign: 'middle',
          fill: n.getItemVisual(r, 'style').fill,
          fontSize: a
        }),
          i.add(d),
          n.setItemGraphicEl(r, d),
          (d.ensureState('emphasis').style = Ft(l.getModel(['emphasis', 'textStyle']), {
            state: 'emphasis'
          })),
          (d.ensureState('blur').style = Ft(l.getModel(['blur', 'textStyle']), { state: 'blur' })),
          Gt(d, l.get(['emphasis', 'focus']), l.get(['emphasis', 'blurScope'])),
          (d.stateTransition = {
            duration: t.get('animation') ? t.get(['stateAnimation', 'duration']) : 0,
            easing: t.get(['stateAnimation', 'easing'])
          }),
          (d.__highDownDispatcher = !0))
      }),
        (this._model = t))
    },
    remove: function () {
      ;(this.group.removeAll(), this._model.layoutInstance.dispose())
    },
    dispose: function () {
      this._model.layoutInstance.dispose()
    }
  }),
  /*!
   * wordcloud2.js
   * http://timdream.org/wordcloud2.js/
   *
   * Copyright 2011 - 2019 Tim Guan-tin Chien and contributors.
   * Released under the MIT license
   */
  window.setImmediate ||
    (window.setImmediate =
      window.msSetImmediate ||
      window.webkitSetImmediate ||
      window.mozSetImmediate ||
      window.oSetImmediate ||
      (function () {
        if (!window.postMessage || !window.addEventListener) return null
        var t = [void 0],
          e = 'zero-timeout-message'
        return (
          window.addEventListener(
            'message',
            function (a) {
              if ('string' == typeof a.data && a.data.substr(0, 20) === e) {
                a.stopImmediatePropagation()
                var i = parseInt(a.data.substr(20), 36)
                t[i] && (t[i](), (t[i] = void 0))
              }
            },
            !0
          ),
          (window.clearImmediate = function (e) {
            t[e] && (t[e] = void 0)
          }),
          function (a) {
            var i = t.length
            return (t.push(a), window.postMessage(e + i.toString(36), '*'), i)
          }
        )
      })() ||
      function (t) {
        window.setTimeout(t, 0)
      }),
  window.clearImmediate ||
    (window.clearImmediate =
      window.msClearImmediate ||
      window.webkitClearImmediate ||
      window.mozClearImmediate ||
      window.oClearImmediate ||
      function (t) {
        window.clearTimeout(t)
      }))
var ca = (function () {
    var t = document.createElement('canvas')
    if (!t || !t.getContext) return !1
    var e = t.getContext('2d')
    return (
      !!e && !!e.getImageData && !!e.fillText && !!Array.prototype.some && !!Array.prototype.push
    )
  })(),
  ha = (function () {
    if (ca) {
      for (var t, e, a = document.createElement('canvas').getContext('2d'), i = 20; i; ) {
        if (
          ((a.font = i.toString(10) + 'px sans-serif'),
          a.measureText('Ｗ').width === t && a.measureText('m').width === e)
        )
          return i + 1
        ;((t = a.measureText('Ｗ').width), (e = a.measureText('m').width), i--)
      }
      return 0
    }
  })(),
  pa = function (t) {
    for (var e, a, i = t.length; i; )
      ((e = Math.floor(Math.random() * i)), (a = t[--i]), (t[i] = t[e]), (t[e] = a))
    return t
  },
  fa = {},
  ma = function (t, e) {
    if (ca) {
      var a = Math.floor(Math.random() * Date.now())
      ;(Array.isArray(t) || (t = [t]),
        t.forEach(function (e, a) {
          if ('string' == typeof e) {
            if (((t[a] = document.getElementById(e)), !t[a]))
              throw new Error('The element id specified is not found.')
          } else if (!e.tagName && !e.appendChild)
            throw new Error('You must pass valid HTML elements, or ID of the element.')
        }))
      var i = {
        list: [],
        fontFamily:
          '"Trebuchet MS", "Heiti TC", "微軟正黑體", "Arial Unicode MS", "Droid Fallback Sans", sans-serif',
        fontWeight: 'normal',
        color: 'random-dark',
        minSize: 0,
        weightFactor: 1,
        clearCanvas: !0,
        backgroundColor: '#fff',
        gridSize: 8,
        drawOutOfBound: !1,
        shrinkToFit: !1,
        origin: null,
        drawMask: !1,
        maskColor: 'rgba(255,0,0,0.3)',
        maskGapWidth: 0.3,
        layoutAnimation: !0,
        wait: 0,
        abortThreshold: 0,
        abort: function () {},
        minRotation: -Math.PI / 2,
        maxRotation: Math.PI / 2,
        rotationStep: 0.1,
        shuffle: !0,
        rotateRatio: 0.1,
        shape: 'circle',
        ellipticity: 0.65,
        classes: null,
        hover: null,
        click: null
      }
      if (e) for (var n in e) n in i && (i[n] = e[n])
      if ('function' != typeof i.weightFactor) {
        var o = i.weightFactor
        i.weightFactor = function (t) {
          return t * o
        }
      }
      if ('function' != typeof i.shape)
        switch (i.shape) {
          case 'circle':
          default:
            i.shape = 'circle'
            break
          case 'cardioid':
            i.shape = function (t) {
              return 1 - Math.sin(t)
            }
            break
          case 'diamond':
            i.shape = function (t) {
              var e = t % ((2 * Math.PI) / 4)
              return 1 / (Math.cos(e) + Math.sin(e))
            }
            break
          case 'square':
            i.shape = function (t) {
              return Math.min(1 / Math.abs(Math.cos(t)), 1 / Math.abs(Math.sin(t)))
            }
            break
          case 'triangle-forward':
            i.shape = function (t) {
              var e = t % ((2 * Math.PI) / 3)
              return 1 / (Math.cos(e) + Math.sqrt(3) * Math.sin(e))
            }
            break
          case 'triangle':
          case 'triangle-upright':
            i.shape = function (t) {
              var e = (t + (3 * Math.PI) / 2) % ((2 * Math.PI) / 3)
              return 1 / (Math.cos(e) + Math.sqrt(3) * Math.sin(e))
            }
            break
          case 'pentagon':
            i.shape = function (t) {
              var e = (t + 0.955) % ((2 * Math.PI) / 5)
              return 1 / (Math.cos(e) + 0.726543 * Math.sin(e))
            }
            break
          case 'star':
            i.shape = function (t) {
              var e = (t + 0.955) % ((2 * Math.PI) / 10)
              return ((t + 0.955) % ((2 * Math.PI) / 5)) - (2 * Math.PI) / 10 >= 0
                ? 1 /
                    (Math.cos((2 * Math.PI) / 10 - e) + 3.07768 * Math.sin((2 * Math.PI) / 10 - e))
                : 1 / (Math.cos(e) + 3.07768 * Math.sin(e))
            }
        }
      i.gridSize = Math.max(Math.floor(i.gridSize), 4)
      var r,
        s,
        l,
        u,
        d,
        c,
        h,
        p,
        f = i.gridSize,
        m = f - i.maskGapWidth,
        g = Math.abs(i.maxRotation - i.minRotation),
        y = Math.min(i.maxRotation, i.minRotation),
        v = i.rotationStep
      switch (i.color) {
        case 'random-dark':
          h = function () {
            return L(10, 50)
          }
          break
        case 'random-light':
          h = function () {
            return L(50, 90)
          }
          break
        default:
          'function' == typeof i.color && (h = i.color)
      }
      'function' == typeof i.fontWeight && (p = i.fontWeight)
      var x = null
      'function' == typeof i.classes && (x = i.classes)
      var w,
        b = !1,
        S = [],
        M = function (t) {
          var e,
            a,
            i = t.currentTarget,
            n = i.getBoundingClientRect()
          t.touches
            ? ((e = t.touches[0].clientX), (a = t.touches[0].clientY))
            : ((e = t.clientX), (a = t.clientY))
          var o = e - n.left,
            r = a - n.top,
            s = Math.floor((o * (i.width / n.width || 1)) / f),
            l = Math.floor((r * (i.height / n.height || 1)) / f)
          return S[s] ? S[s][l] : null
        },
        _ = function (t) {
          var e = M(t)
          w !== e && ((w = e), e ? i.hover(e.item, e.dimension, t) : i.hover(void 0, void 0, t))
        },
        I = function (t) {
          var e = M(t)
          e && (i.click(e.item, e.dimension, t), t.preventDefault())
        },
        C = [],
        D = function (t) {
          if (C[t]) return C[t]
          var e = 8 * t,
            a = e,
            n = []
          for (0 === t && n.push([u[0], u[1], 0]); a--; ) {
            var o = 1
            ;('circle' !== i.shape && (o = i.shape((a / e) * 2 * Math.PI)),
              n.push([
                u[0] + t * o * Math.cos((-a / e) * 2 * Math.PI),
                u[1] + t * o * Math.sin((-a / e) * 2 * Math.PI) * i.ellipticity,
                (a / e) * 2 * Math.PI
              ]))
          }
          return ((C[t] = n), n)
        },
        E = function () {
          return i.abortThreshold > 0 && new Date().getTime() - c > i.abortThreshold
        },
        T = function (e, a, i, n, o) {
          if (!(e >= s || a >= l || e < 0 || a < 0)) {
            if (((r[e][a] = !1), i)) t[0].getContext('2d').fillRect(e * f, a * f, m, m)
            b && (S[e][a] = { item: o, dimension: n })
          }
        },
        A = function e(a, n) {
          if (n > 20) return null
          var o, u, c
          Array.isArray(a)
            ? ((o = a[0]), (u = a[1]))
            : ((o = a.word), (u = a.weight), (c = a.attributes))
          var m =
              0 === i.rotateRatio || Math.random() > i.rotateRatio
                ? 0
                : 0 === g
                  ? y
                  : y + Math.round((Math.random() * g) / v) * v,
            w = (function (t) {
              if (Array.isArray(t)) {
                var e = t.slice()
                return (e.splice(0, 2), e)
              }
              return []
            })(a),
            S = (function (t, e, a, n) {
              var o = i.weightFactor(e)
              if (o <= i.minSize) return !1
              var r,
                s = 1
              ;(o < ha &&
                (s = (function () {
                  for (var t = 2; t * o < ha; ) t += 2
                  return t
                })()),
                (r = p ? p(t, e, o, n) : i.fontWeight))
              var l = document.createElement('canvas'),
                u = l.getContext('2d', { willReadFrequently: !0 })
              u.font = r + ' ' + (o * s).toString(10) + 'px ' + i.fontFamily
              var d = u.measureText(t).width / s,
                c = Math.max(o * s, u.measureText('m').width, u.measureText('Ｗ').width) / s,
                h = d + 2 * c,
                m = 3 * c,
                g = Math.ceil(h / f),
                y = Math.ceil(m / f)
              ;((h = g * f), (m = y * f))
              var v = -d / 2,
                x = 0.4 * -c,
                w = Math.ceil((h * Math.abs(Math.sin(a)) + m * Math.abs(Math.cos(a))) / f),
                b = Math.ceil((h * Math.abs(Math.cos(a)) + m * Math.abs(Math.sin(a))) / f),
                S = b * f,
                M = w * f
              ;(l.setAttribute('width', S),
                l.setAttribute('height', M),
                u.scale(1 / s, 1 / s),
                u.translate((S * s) / 2, (M * s) / 2),
                u.rotate(-a),
                (u.font = r + ' ' + (o * s).toString(10) + 'px ' + i.fontFamily),
                (u.fillStyle = '#000'),
                (u.textBaseline = 'middle'),
                u.fillText(t, v * s, (x + 0.5 * o) * s))
              var _ = u.getImageData(0, 0, S, M).data
              if (E()) return !1
              for (var I, C, D, T = [], A = b, P = [w / 2, b / 2, w / 2, b / 2]; A--; )
                for (I = w; I--; ) {
                  D = f
                  t: for (; D--; )
                    for (C = f; C--; )
                      if (_[4 * ((I * f + D) * S + (A * f + C)) + 3]) {
                        ;(T.push([A, I]),
                          A < P[3] && (P[3] = A),
                          A > P[1] && (P[1] = A),
                          I < P[0] && (P[0] = I),
                          I > P[2] && (P[2] = I))
                        break t
                      }
                }
              return {
                mu: s,
                occupied: T,
                bounds: P,
                gw: b,
                gh: w,
                fillTextOffsetX: v,
                fillTextOffsetY: x,
                fillTextWidth: d,
                fillTextHeight: c,
                fontSize: o
              }
            })(o, u, m, w)
          if (!S) return !1
          if (E()) return !1
          if (!i.drawOutOfBound && !i.shrinkToFit) {
            var M = S.bounds
            if (M[1] - M[3] + 1 > s || M[2] - M[0] + 1 > l) return !1
          }
          for (
            var _ = d + 1,
              I = function (e) {
                var n = Math.floor(e[0] - S.gw / 2),
                  g = Math.floor(e[1] - S.gh / 2)
                ;(S.gw, S.gh)
                return (
                  !!(function (t, e, a, n, o) {
                    for (var u = o.length; u--; ) {
                      var d = t + o[u][0],
                        c = e + o[u][1]
                      if (d >= s || c >= l || d < 0 || c < 0) {
                        if (!i.drawOutOfBound) return !1
                      } else if (!r[d][c]) return !1
                    }
                    return !0
                  })(n, g, 0, 0, S.occupied) &&
                  ((function (e, a, n, o, r, s, l, u, d, c) {
                    var m,
                      g,
                      y,
                      v = n.fontSize
                    ;((m = h ? h(o, r, v, s, l, c) : i.color),
                      (g = p ? p(o, r, v, c) : i.fontWeight),
                      (y = x ? x(o, r, v, c) : i.classes),
                      t.forEach(function (t) {
                        if (t.getContext) {
                          var r = t.getContext('2d'),
                            s = n.mu
                          ;(r.save(),
                            r.scale(1 / s, 1 / s),
                            (r.font = g + ' ' + (v * s).toString(10) + 'px ' + i.fontFamily),
                            (r.fillStyle = m),
                            r.translate((e + n.gw / 2) * f * s, (a + n.gh / 2) * f * s),
                            0 !== u && r.rotate(-u),
                            (r.textBaseline = 'middle'),
                            r.fillText(o, n.fillTextOffsetX * s, (n.fillTextOffsetY + 0.5 * v) * s),
                            r.restore())
                        } else {
                          var l = document.createElement('span'),
                            c = ''
                          ;((c = 'rotate(' + (-u / Math.PI) * 180 + 'deg) '),
                            1 !== n.mu &&
                              (c +=
                                'translateX(-' +
                                n.fillTextWidth / 4 +
                                'px) scale(' +
                                1 / n.mu +
                                ')'))
                          var h = {
                            position: 'absolute',
                            display: 'block',
                            font: g + ' ' + v * n.mu + 'px ' + i.fontFamily,
                            left: (e + n.gw / 2) * f + n.fillTextOffsetX + 'px',
                            top: (a + n.gh / 2) * f + n.fillTextOffsetY + 'px',
                            width: n.fillTextWidth + 'px',
                            height: n.fillTextHeight + 'px',
                            lineHeight: v + 'px',
                            whiteSpace: 'nowrap',
                            transform: c,
                            webkitTransform: c,
                            msTransform: c,
                            transformOrigin: '50% 40%',
                            webkitTransformOrigin: '50% 40%',
                            msTransformOrigin: '50% 40%'
                          }
                          for (var p in (m && (h.color = m), (l.textContent = o), h))
                            l.style[p] = h[p]
                          if (d) for (var x in d) l.setAttribute(x, d[x])
                          ;(y && (l.className += y), t.appendChild(l))
                        }
                      }))
                  })(n, g, S, o, u, d - _, e[2], m, c, w),
                  (function (e, a, n, o, r, u) {
                    var d,
                      c,
                      h = r.occupied,
                      p = i.drawMask
                    if (
                      (p && ((d = t[0].getContext('2d')).save(), (d.fillStyle = i.maskColor)), b)
                    ) {
                      var m = r.bounds
                      c = {
                        x: (e + m[3]) * f,
                        y: (a + m[0]) * f,
                        w: (m[1] - m[3] + 1) * f,
                        h: (m[2] - m[0] + 1) * f
                      }
                    }
                    for (var g = h.length; g--; ) {
                      var y = e + h[g][0],
                        v = a + h[g][1]
                      y >= s || v >= l || y < 0 || v < 0 || T(y, v, p, c, u)
                    }
                    p && d.restore()
                  })(n, g, 0, 0, S, a),
                  { gx: n, gy: g, rot: m, info: S })
                )
              };
            _--;
          ) {
            var C = D(d - _)
            i.shuffle && ((C = [].concat(C)), pa(C))
            for (var A = 0; A < C.length; A++) {
              var P = I(C[A])
              if (P) return P
            }
          }
          return i.shrinkToFit
            ? (Array.isArray(a) ? (a[1] = (3 * a[1]) / 4) : (a.weight = (3 * a.weight) / 4),
              e(a, n + 1))
            : null
        },
        P = function (e, a, i) {
          if (a)
            return !t.some(function (t) {
              var a = new CustomEvent(e, { detail: i || {} })
              return !t.dispatchEvent(a)
            }, this)
          t.forEach(function (t) {
            var a = new CustomEvent(e, { detail: i || {} })
            t.dispatchEvent(a)
          }, this)
        }
      !(function () {
        var e = t[0]
        if (e.getContext) ((s = Math.ceil(e.width / f)), (l = Math.ceil(e.height / f)))
        else {
          var n = e.getBoundingClientRect()
          ;((s = Math.ceil(n.width / f)), (l = Math.ceil(n.height / f)))
        }
        if (P('wordcloudstart', !0)) {
          var o, h, p, m, g
          if (
            ((u = i.origin ? [i.origin[0] / f, i.origin[1] / f] : [s / 2, l / 2]),
            (d = Math.floor(Math.sqrt(s * s + l * l))),
            (r = []),
            !e.getContext || i.clearCanvas)
          )
            for (
              t.forEach(function (t) {
                if (t.getContext) {
                  var e = t.getContext('2d')
                  ;((e.fillStyle = i.backgroundColor),
                    e.clearRect(0, 0, s * (f + 1), l * (f + 1)),
                    e.fillRect(0, 0, s * (f + 1), l * (f + 1)))
                } else
                  ((t.textContent = ''),
                    (t.style.backgroundColor = i.backgroundColor),
                    (t.style.position = 'relative'))
              }),
                o = s;
              o--;
            )
              for (r[o] = [], h = l; h--; ) r[o][h] = !0
          else {
            var y = document.createElement('canvas').getContext('2d')
            ;((y.fillStyle = i.backgroundColor), y.fillRect(0, 0, 1, 1))
            var v,
              x,
              M = y.getImageData(0, 0, 1, 1).data,
              C = e.getContext('2d').getImageData(0, 0, s * f, l * f).data
            for (o = s; o--; )
              for (r[o] = [], h = l; h--; ) {
                x = f
                t: for (; x--; )
                  for (v = f; v--; )
                    for (p = 4; p--; )
                      if (C[4 * ((h * f + x) * s * f + (o * f + v)) + p] !== M[p]) {
                        r[o][h] = !1
                        break t
                      }
                !1 !== r[o][h] && (r[o][h] = !0)
              }
            C = y = M = void 0
          }
          if (i.hover || i.click) {
            for (b = !0, o = s + 1; o--; ) S[o] = []
            ;(i.hover && e.addEventListener('mousemove', _),
              i.click &&
                (e.addEventListener('click', I),
                e.addEventListener('touchstart', I),
                e.addEventListener('touchend', function (t) {
                  t.preventDefault()
                }),
                (e.style.webkitTapHighlightColor = 'rgba(0, 0, 0, 0)')),
              e.addEventListener('wordcloudstart', function t() {
                ;(e.removeEventListener('wordcloudstart', t),
                  e.removeEventListener('mousemove', _),
                  e.removeEventListener('click', I),
                  (w = void 0))
              }))
          }
          p = 0
          var D = !0
          i.layoutAnimation
            ? 0 !== i.wait
              ? ((m = window.setTimeout), (g = window.clearTimeout))
              : ((m = window.setImmediate), (g = window.clearImmediate))
            : ((m = function (t) {
                t()
              }),
              (g = function () {
                D = !1
              }))
          var T = function (e, a) {
              t.forEach(function (t) {
                t.removeEventListener(e, a)
              }, this)
            },
            L = function t() {
              ;(T('wordcloudstart', t), g(fa[a]))
            }
          ;(!(function (e, a) {
            t.forEach(function (t) {
              t.addEventListener(e, a)
            }, this)
          })('wordcloudstart', L),
            (fa[a] = (i.layoutAnimation ? m : setTimeout)(function t() {
              if (D) {
                if (p >= i.list.length)
                  return (
                    g(fa[a]),
                    P('wordcloudstop', !1),
                    T('wordcloudstart', L),
                    void delete fa[a]
                  )
                c = new Date().getTime()
                var e = A(i.list[p], 0),
                  n = !P('wordclouddrawn', !0, { item: i.list[p], drawn: e })
                if (E() || n)
                  return (
                    g(fa[a]),
                    i.abort(),
                    P('wordcloudabort', !1),
                    P('wordcloudstop', !1),
                    void T('wordcloudstart', L)
                  )
                ;(p++, (fa[a] = m(t, i.wait)))
              }
            }, i.wait)))
        }
      })()
    }
    function L(t, e) {
      return (
        'hsl(' +
        (360 * Math.random()).toFixed() +
        ',' +
        (30 * Math.random() + 70).toFixed() +
        '%,' +
        (Math.random() * (e - t) + t).toFixed() +
        '%)'
      )
    }
  }
if (((ma.isSupported = ca), (ma.minFontSize = ha), !ma.isSupported))
  throw new Error('Sorry your browser not support wordCloud')
;(Yt(function (t, e) {
  t.eachSeriesByType('wordCloud', function (a) {
    var i = k(a.getBoxLayoutParams(), { width: e.getWidth(), height: e.getHeight() }),
      n = a.get('keepAspect'),
      o = a.get('maskImage'),
      r = o ? o.width / o.height : 1
    n &&
      (function (t, e) {
        var a = t.width,
          i = t.height
        a > i * e
          ? ((t.x += (a - i * e) / 2), (t.width = i * e))
          : ((t.y += (i - a / e) / 2), (t.height = a / e))
      })(i, r)
    var s = a.getData(),
      l = document.createElement('canvas')
    ;((l.width = i.width), (l.height = i.height))
    var u = l.getContext('2d')
    if (o)
      try {
        ;(u.drawImage(o, 0, 0, l.width, l.height),
          (function (t) {
            for (
              var e = t.getContext('2d'),
                a = e.getImageData(0, 0, t.width, t.height),
                i = e.createImageData(a),
                n = 0,
                o = 0,
                r = 0;
              r < a.data.length;
              r += 4
            )
              a.data[r + 3] > 128 && ((n += l = a.data[r] + a.data[r + 1] + a.data[r + 2]), ++o)
            var s = n / o
            for (r = 0; r < a.data.length; r += 4) {
              var l = a.data[r] + a.data[r + 1] + a.data[r + 2]
              a.data[r + 3] < 128 || l > s
                ? ((i.data[r] = 0), (i.data[r + 1] = 0), (i.data[r + 2] = 0), (i.data[r + 3] = 0))
                : ((i.data[r] = 255),
                  (i.data[r + 1] = 255),
                  (i.data[r + 2] = 255),
                  (i.data[r + 3] = 255))
            }
            e.putImageData(i, 0, 0)
          })(l))
      } catch (g) {}
    var d = a.get('sizeRange'),
      c = a.get('rotationRange'),
      h = s.getDataExtent('value'),
      p = Math.PI / 180,
      f = a.get('gridSize')
    function m(t) {
      var e = t.detail.item
      t.detail.drawn &&
        a.layoutInstance.ondraw &&
        ((t.detail.drawn.gx += i.x / f),
        (t.detail.drawn.gy += i.y / f),
        a.layoutInstance.ondraw(e[0], e[1], e[2], t.detail.drawn))
    }
    ;(ma(l, {
      list: s
        .mapArray('value', function (t, e) {
          var a = s.getItemModel(e)
          return [s.getName(e), a.get('textStyle.fontSize', !0) || Ht(t, h, d), e]
        })
        .sort(function (t, e) {
          return e[1] - t[1]
        }),
      fontFamily:
        a.get('textStyle.fontFamily') ||
        a.get('emphasis.textStyle.fontFamily') ||
        t.get('textStyle.fontFamily'),
      fontWeight:
        a.get('textStyle.fontWeight') ||
        a.get('emphasis.textStyle.fontWeight') ||
        t.get('textStyle.fontWeight'),
      gridSize: f,
      ellipticity: i.height / i.width,
      minRotation: c[0] * p,
      maxRotation: c[1] * p,
      clearCanvas: !o,
      rotateRatio: 1,
      rotationStep: a.get('rotationStep') * p,
      drawOutOfBound: a.get('drawOutOfBound'),
      shrinkToFit: a.get('shrinkToFit'),
      layoutAnimation: a.get('layoutAnimation'),
      shuffle: !1,
      shape: a.get('shape')
    }),
      l.addEventListener('wordclouddrawn', m),
      a.layoutInstance && a.layoutInstance.dispose(),
      (a.layoutInstance = {
        ondraw: null,
        dispose: function () {
          ;(l.removeEventListener('wordclouddrawn', m),
            l.addEventListener('wordclouddrawn', function (t) {
              t.preventDefault()
            }))
        }
      }))
  })
}),
  Vt(function (t) {
    var e = (t || {}).series
    !nt(e) && (e = e ? [e] : [])
    var a = ['shadowColor', 'shadowBlur', 'shadowOffsetX', 'shadowOffsetY']
    function i(t) {
      t &&
        p(a, function (e) {
          t.hasOwnProperty(e) && (t['text' + Xt(e)] = t[e])
        })
    }
    p(e, function (t) {
      if (t && 'wordCloud' === t.type) {
        var e = t.textStyle || {}
        ;(i(e.normal), i(e.emphasis))
      }
    })
  }))
const ga = jt({
  __name: 'Echart',
  props: {
    options: { type: Object, required: !0 },
    width: qt.oneOfType([Number, String]).def(''),
    height: qt.oneOfType([Number, String]).def('500px')
  },
  setup(t) {
    const e = t,
      { getPrefixCls: a, variables: i } = se(),
      n = a('echart'),
      o = Ut(),
      r = Zt(() => o.getIsDark),
      s = Zt(() => !!$t(r) || 'auto'),
      l = Zt(() => Object.assign(e.options, { darkMode: $t(s) })),
      u = Jt()
    let d = null
    const c = Jt(),
      h = Zt(() => ({
        width: Kt(e.width) ? e.width : `${e.width}px`,
        height: Kt(e.height) ? e.height : `${e.height}px`
      }))
    Qt(
      () => l.value,
      (t) => {
        d && (null == d || d.setOption(t))
      },
      { deep: !0 }
    )
    const p = le(() => {
        d && d.resize()
      }, 100),
      f = async (t) => {
        'width' === t.propertyName && p()
      }
    return (
      te(() => {
        ;($t(u) && e.options && ((d = kt.init($t(u))), null == d || d.setOption($t(l))),
          window.addEventListener('resize', p),
          (c.value = document.getElementsByClassName(`${i.namespace}-layout-content`)[0]),
          $t(c) && $t(c).addEventListener('transitionend', f))
      }),
      ee(() => {
        ;(window.removeEventListener('resize', p),
          $t(c) && $t(c).removeEventListener('transitionend', f))
      }),
      ae(() => {
        d && d.resize()
      }),
      (t, e) => (
        ie(),
        ne(
          'div',
          { ref_key: 'elRef', ref: u, class: oe([t.$attrs.class, $t(n)]), style: re(h.value) },
          null,
          6
        )
      )
    )
  }
})
export { ga as _ }
