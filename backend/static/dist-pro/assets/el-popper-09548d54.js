import {
  bs as e,
  d as t,
  aq as n,
  f as r,
  b3 as o,
  w as a,
  a2 as i,
  aJ as s,
  b7 as l,
  k as p,
  ab as u,
  r as f,
  aj as c,
  bO as d,
  bP as v,
  bQ as m,
  bR as g,
  bS as h,
  b,
  i as y,
  am as w,
  e as x,
  q as O,
  _ as R,
  u as A,
  ao as k,
  o as E,
  j as T,
  s as S,
  n as C,
  aS as j,
  a0 as B,
  bT as M,
  ap as P,
  a1 as F,
  bU as L,
  bV as D,
  x as _,
  bW as I,
  bX as H,
  l as $,
  m as W,
  a6 as q,
  F as N,
  bY as U,
  bo as z,
  t as V,
  aA as K,
  aZ as Z,
  a4 as X,
  aH as Y,
  D as J,
  bZ as Q,
  aV as G,
  bL as ee,
  b_ as te,
  b$ as ne,
  z as re,
} from "./index-6b60d190.js";
import { i as oe } from "./isNil-1f22f7b0.js";
import { E as ae } from "./focus-trap-275966d8.js";
const ie =
    (e, t, { checkForDefaultPrevented: n = !0 } = {}) =>
    (r) => {
      const o = null == e ? void 0 : e(r);
      if (!1 === n || !o) return null == t ? void 0 : t(r);
    },
  se = (e) => (t) => ("mouse" === t.pointerType ? e(t) : void 0);
const le = e({ type: t(Boolean), default: null }),
  pe = e({ type: t(Function) }),
  ue = (e) => {
    const t = `update:${e}`,
      p = `onUpdate:${e}`;
    return {
      useModelToggle: ({
        indicator: u,
        toggleReason: f,
        shouldHideWhenRouteChanges: c,
        shouldProceed: d,
        onShow: v,
        onHide: m,
      }) => {
        const g = n(),
          { emit: h } = g,
          b = g.props,
          y = r(() => o(b[p])),
          w = r(() => null === b[e]),
          x = (e) => {
            !0 !== u.value &&
              ((u.value = !0), f && (f.value = e), o(v) && v(e));
          },
          O = (e) => {
            !1 !== u.value &&
              ((u.value = !1), f && (f.value = e), o(m) && m(e));
          },
          R = (e) => {
            if (!0 === b.disabled || (o(d) && !d())) return;
            const n = y.value && s;
            (n && h(t, !0), (!w.value && n) || x(e));
          },
          A = (e) => {
            if (!0 === b.disabled || !s) return;
            const n = y.value && s;
            (n && h(t, !1), (!w.value && n) || O(e));
          },
          k = (e) => {
            l(e) &&
              (b.disabled && e
                ? y.value && h(t, !1)
                : u.value !== e && (e ? x() : O()));
          };
        return (
          a(() => b[e], k),
          c &&
            void 0 !== g.appContext.config.globalProperties.$route &&
            a(
              () => ({ ...g.proxy.$route }),
              () => {
                c.value && u.value && A();
              },
            ),
          i(() => {
            k(b[e]);
          }),
          {
            hide: A,
            show: R,
            toggle: () => {
              u.value ? A() : R();
            },
            hasUpdateHandler: y,
          }
        );
      },
      useModelToggleProps: { [e]: le, [p]: pe },
      useModelToggleEmits: [t],
    };
  };
ue("modelValue");
var fe = "top",
  ce = "bottom",
  de = "right",
  ve = "left",
  me = "auto",
  ge = [fe, ce, de, ve],
  he = "start",
  be = "end",
  ye = "clippingParents",
  we = "viewport",
  xe = "popper",
  Oe = "reference",
  Re = ge.reduce(function (e, t) {
    return e.concat([t + "-" + he, t + "-" + be]);
  }, []),
  Ae = [].concat(ge, [me]).reduce(function (e, t) {
    return e.concat([t, t + "-" + he, t + "-" + be]);
  }, []),
  ke = [
    "beforeRead",
    "read",
    "afterRead",
    "beforeMain",
    "main",
    "afterMain",
    "beforeWrite",
    "write",
    "afterWrite",
  ];
function Ee(e) {
  return e ? (e.nodeName || "").toLowerCase() : null;
}
function Te(e) {
  if (null == e) return window;
  if ("[object Window]" !== e.toString()) {
    var t = e.ownerDocument;
    return (t && t.defaultView) || window;
  }
  return e;
}
function Se(e) {
  return e instanceof Te(e).Element || e instanceof Element;
}
function Ce(e) {
  return e instanceof Te(e).HTMLElement || e instanceof HTMLElement;
}
function je(e) {
  return (
    "undefined" != typeof ShadowRoot &&
    (e instanceof Te(e).ShadowRoot || e instanceof ShadowRoot)
  );
}
var Be = {
  name: "applyStyles",
  enabled: !0,
  phase: "write",
  fn: function (e) {
    var t = e.state;
    Object.keys(t.elements).forEach(function (e) {
      var n = t.styles[e] || {},
        r = t.attributes[e] || {},
        o = t.elements[e];
      !Ce(o) ||
        !Ee(o) ||
        (Object.assign(o.style, n),
        Object.keys(r).forEach(function (e) {
          var t = r[e];
          !1 === t
            ? o.removeAttribute(e)
            : o.setAttribute(e, !0 === t ? "" : t);
        }));
    });
  },
  effect: function (e) {
    var t = e.state,
      n = {
        popper: {
          position: t.options.strategy,
          left: "0",
          top: "0",
          margin: "0",
        },
        arrow: { position: "absolute" },
        reference: {},
      };
    return (
      Object.assign(t.elements.popper.style, n.popper),
      (t.styles = n),
      t.elements.arrow && Object.assign(t.elements.arrow.style, n.arrow),
      function () {
        Object.keys(t.elements).forEach(function (e) {
          var r = t.elements[e],
            o = t.attributes[e] || {},
            a = Object.keys(
              t.styles.hasOwnProperty(e) ? t.styles[e] : n[e],
            ).reduce(function (e, t) {
              return ((e[t] = ""), e);
            }, {});
          !Ce(r) ||
            !Ee(r) ||
            (Object.assign(r.style, a),
            Object.keys(o).forEach(function (e) {
              r.removeAttribute(e);
            }));
        });
      }
    );
  },
  requires: ["computeStyles"],
};
function Me(e) {
  return e.split("-")[0];
}
var Pe = Math.max,
  Fe = Math.min,
  Le = Math.round;
function De(e, t) {
  void 0 === t && (t = !1);
  var n = e.getBoundingClientRect(),
    r = 1,
    o = 1;
  if (Ce(e) && t) {
    var a = e.offsetHeight,
      i = e.offsetWidth;
    (i > 0 && (r = Le(n.width) / i || 1), a > 0 && (o = Le(n.height) / a || 1));
  }
  return {
    width: n.width / r,
    height: n.height / o,
    top: n.top / o,
    right: n.right / r,
    bottom: n.bottom / o,
    left: n.left / r,
    x: n.left / r,
    y: n.top / o,
  };
}
function _e(e) {
  var t = De(e),
    n = e.offsetWidth,
    r = e.offsetHeight;
  return (
    Math.abs(t.width - n) <= 1 && (n = t.width),
    Math.abs(t.height - r) <= 1 && (r = t.height),
    { x: e.offsetLeft, y: e.offsetTop, width: n, height: r }
  );
}
function Ie(e, t) {
  var n = t.getRootNode && t.getRootNode();
  if (e.contains(t)) return !0;
  if (n && je(n)) {
    var r = t;
    do {
      if (r && e.isSameNode(r)) return !0;
      r = r.parentNode || r.host;
    } while (r);
  }
  return !1;
}
function He(e) {
  return Te(e).getComputedStyle(e);
}
function $e(e) {
  return ["table", "td", "th"].indexOf(Ee(e)) >= 0;
}
function We(e) {
  return ((Se(e) ? e.ownerDocument : e.document) || window.document)
    .documentElement;
}
function qe(e) {
  return "html" === Ee(e)
    ? e
    : e.assignedSlot || e.parentNode || (je(e) ? e.host : null) || We(e);
}
function Ne(e) {
  return Ce(e) && "fixed" !== He(e).position ? e.offsetParent : null;
}
function Ue(e) {
  for (var t = Te(e), n = Ne(e); n && $e(n) && "static" === He(n).position; )
    n = Ne(n);
  return n &&
    ("html" === Ee(n) || ("body" === Ee(n) && "static" === He(n).position))
    ? t
    : n ||
        (function (e) {
          var t = -1 !== navigator.userAgent.toLowerCase().indexOf("firefox");
          if (
            -1 !== navigator.userAgent.indexOf("Trident") &&
            Ce(e) &&
            "fixed" === He(e).position
          )
            return null;
          var n = qe(e);
          for (
            je(n) && (n = n.host);
            Ce(n) && ["html", "body"].indexOf(Ee(n)) < 0;
          ) {
            var r = He(n);
            if (
              "none" !== r.transform ||
              "none" !== r.perspective ||
              "paint" === r.contain ||
              -1 !== ["transform", "perspective"].indexOf(r.willChange) ||
              (t && "filter" === r.willChange) ||
              (t && r.filter && "none" !== r.filter)
            )
              return n;
            n = n.parentNode;
          }
          return null;
        })(e) ||
        t;
}
function ze(e) {
  return ["top", "bottom"].indexOf(e) >= 0 ? "x" : "y";
}
function Ve(e, t, n) {
  return Pe(e, Fe(t, n));
}
function Ke(e) {
  return Object.assign({}, { top: 0, right: 0, bottom: 0, left: 0 }, e);
}
function Ze(e, t) {
  return t.reduce(function (t, n) {
    return ((t[n] = e), t);
  }, {});
}
var Xe = {
  name: "arrow",
  enabled: !0,
  phase: "main",
  fn: function (e) {
    var t,
      n = e.state,
      r = e.name,
      o = e.options,
      a = n.elements.arrow,
      i = n.modifiersData.popperOffsets,
      s = Me(n.placement),
      l = ze(s),
      p = [ve, de].indexOf(s) >= 0 ? "height" : "width";
    if (a && i) {
      var u = (function (e, t) {
          return Ke(
            "number" !=
              typeof (e =
                "function" == typeof e
                  ? e(Object.assign({}, t.rects, { placement: t.placement }))
                  : e)
              ? e
              : Ze(e, ge),
          );
        })(o.padding, n),
        f = _e(a),
        c = "y" === l ? fe : ve,
        d = "y" === l ? ce : de,
        v =
          n.rects.reference[p] +
          n.rects.reference[l] -
          i[l] -
          n.rects.popper[p],
        m = i[l] - n.rects.reference[l],
        g = Ue(a),
        h = g ? ("y" === l ? g.clientHeight || 0 : g.clientWidth || 0) : 0,
        b = v / 2 - m / 2,
        y = u[c],
        w = h - f[p] - u[d],
        x = h / 2 - f[p] / 2 + b,
        O = Ve(y, x, w),
        R = l;
      n.modifiersData[r] = (((t = {})[R] = O), (t.centerOffset = O - x), t);
    }
  },
  effect: function (e) {
    var t = e.state,
      n = e.options.element,
      r = void 0 === n ? "[data-popper-arrow]" : n;
    null != r &&
      (("string" == typeof r && !(r = t.elements.popper.querySelector(r))) ||
        !Ie(t.elements.popper, r) ||
        (t.elements.arrow = r));
  },
  requires: ["popperOffsets"],
  requiresIfExists: ["preventOverflow"],
};
function Ye(e) {
  return e.split("-")[1];
}
var Je = { top: "auto", right: "auto", bottom: "auto", left: "auto" };
function Qe(e) {
  var t,
    n = e.popper,
    r = e.popperRect,
    o = e.placement,
    a = e.variation,
    i = e.offsets,
    s = e.position,
    l = e.gpuAcceleration,
    p = e.adaptive,
    u = e.roundOffsets,
    f = e.isFixed,
    c = i.x,
    d = void 0 === c ? 0 : c,
    v = i.y,
    m = void 0 === v ? 0 : v,
    g = "function" == typeof u ? u({ x: d, y: m }) : { x: d, y: m };
  ((d = g.x), (m = g.y));
  var h = i.hasOwnProperty("x"),
    b = i.hasOwnProperty("y"),
    y = ve,
    w = fe,
    x = window;
  if (p) {
    var O = Ue(n),
      R = "clientHeight",
      A = "clientWidth";
    if (
      (O === Te(n) &&
        "static" !== He((O = We(n))).position &&
        "absolute" === s &&
        ((R = "scrollHeight"), (A = "scrollWidth")),
      o === fe || ((o === ve || o === de) && a === be))
    )
      ((w = ce),
        (m -=
          (f && O === x && x.visualViewport ? x.visualViewport.height : O[R]) -
          r.height),
        (m *= l ? 1 : -1));
    if (o === ve || ((o === fe || o === ce) && a === be))
      ((y = de),
        (d -=
          (f && O === x && x.visualViewport ? x.visualViewport.width : O[A]) -
          r.width),
        (d *= l ? 1 : -1));
  }
  var k,
    E = Object.assign({ position: s }, p && Je),
    T =
      !0 === u
        ? (function (e) {
            var t = e.x,
              n = e.y,
              r = window.devicePixelRatio || 1;
            return { x: Le(t * r) / r || 0, y: Le(n * r) / r || 0 };
          })({ x: d, y: m })
        : { x: d, y: m };
  return (
    (d = T.x),
    (m = T.y),
    l
      ? Object.assign(
          {},
          E,
          (((k = {})[w] = b ? "0" : ""),
          (k[y] = h ? "0" : ""),
          (k.transform =
            (x.devicePixelRatio || 1) <= 1
              ? "translate(" + d + "px, " + m + "px)"
              : "translate3d(" + d + "px, " + m + "px, 0)"),
          k),
        )
      : Object.assign(
          {},
          E,
          (((t = {})[w] = b ? m + "px" : ""),
          (t[y] = h ? d + "px" : ""),
          (t.transform = ""),
          t),
        )
  );
}
var Ge = {
    name: "computeStyles",
    enabled: !0,
    phase: "beforeWrite",
    fn: function (e) {
      var t = e.state,
        n = e.options,
        r = n.gpuAcceleration,
        o = void 0 === r || r,
        a = n.adaptive,
        i = void 0 === a || a,
        s = n.roundOffsets,
        l = void 0 === s || s,
        p = {
          placement: Me(t.placement),
          variation: Ye(t.placement),
          popper: t.elements.popper,
          popperRect: t.rects.popper,
          gpuAcceleration: o,
          isFixed: "fixed" === t.options.strategy,
        };
      (null != t.modifiersData.popperOffsets &&
        (t.styles.popper = Object.assign(
          {},
          t.styles.popper,
          Qe(
            Object.assign({}, p, {
              offsets: t.modifiersData.popperOffsets,
              position: t.options.strategy,
              adaptive: i,
              roundOffsets: l,
            }),
          ),
        )),
        null != t.modifiersData.arrow &&
          (t.styles.arrow = Object.assign(
            {},
            t.styles.arrow,
            Qe(
              Object.assign({}, p, {
                offsets: t.modifiersData.arrow,
                position: "absolute",
                adaptive: !1,
                roundOffsets: l,
              }),
            ),
          )),
        (t.attributes.popper = Object.assign({}, t.attributes.popper, {
          "data-popper-placement": t.placement,
        })));
    },
    data: {},
  },
  et = { passive: !0 };
var tt = {
    name: "eventListeners",
    enabled: !0,
    phase: "write",
    fn: function () {},
    effect: function (e) {
      var t = e.state,
        n = e.instance,
        r = e.options,
        o = r.scroll,
        a = void 0 === o || o,
        i = r.resize,
        s = void 0 === i || i,
        l = Te(t.elements.popper),
        p = [].concat(t.scrollParents.reference, t.scrollParents.popper);
      return (
        a &&
          p.forEach(function (e) {
            e.addEventListener("scroll", n.update, et);
          }),
        s && l.addEventListener("resize", n.update, et),
        function () {
          (a &&
            p.forEach(function (e) {
              e.removeEventListener("scroll", n.update, et);
            }),
            s && l.removeEventListener("resize", n.update, et));
        }
      );
    },
    data: {},
  },
  nt = { left: "right", right: "left", bottom: "top", top: "bottom" };
function rt(e) {
  return e.replace(/left|right|bottom|top/g, function (e) {
    return nt[e];
  });
}
var ot = { start: "end", end: "start" };
function at(e) {
  return e.replace(/start|end/g, function (e) {
    return ot[e];
  });
}
function it(e) {
  var t = Te(e);
  return { scrollLeft: t.pageXOffset, scrollTop: t.pageYOffset };
}
function st(e) {
  return De(We(e)).left + it(e).scrollLeft;
}
function lt(e) {
  var t = He(e),
    n = t.overflow,
    r = t.overflowX,
    o = t.overflowY;
  return /auto|scroll|overlay|hidden/.test(n + o + r);
}
function pt(e) {
  return ["html", "body", "#document"].indexOf(Ee(e)) >= 0
    ? e.ownerDocument.body
    : Ce(e) && lt(e)
      ? e
      : pt(qe(e));
}
function ut(e, t) {
  var n;
  void 0 === t && (t = []);
  var r = pt(e),
    o = r === (null == (n = e.ownerDocument) ? void 0 : n.body),
    a = Te(r),
    i = o ? [a].concat(a.visualViewport || [], lt(r) ? r : []) : r,
    s = t.concat(i);
  return o ? s : s.concat(ut(qe(i)));
}
function ft(e) {
  return Object.assign({}, e, {
    left: e.x,
    top: e.y,
    right: e.x + e.width,
    bottom: e.y + e.height,
  });
}
function ct(e, t) {
  return t === we
    ? ft(
        (function (e) {
          var t = Te(e),
            n = We(e),
            r = t.visualViewport,
            o = n.clientWidth,
            a = n.clientHeight,
            i = 0,
            s = 0;
          return (
            r &&
              ((o = r.width),
              (a = r.height),
              /^((?!chrome|android).)*safari/i.test(navigator.userAgent) ||
                ((i = r.offsetLeft), (s = r.offsetTop))),
            { width: o, height: a, x: i + st(e), y: s }
          );
        })(e),
      )
    : Se(t)
      ? (function (e) {
          var t = De(e);
          return (
            (t.top = t.top + e.clientTop),
            (t.left = t.left + e.clientLeft),
            (t.bottom = t.top + e.clientHeight),
            (t.right = t.left + e.clientWidth),
            (t.width = e.clientWidth),
            (t.height = e.clientHeight),
            (t.x = t.left),
            (t.y = t.top),
            t
          );
        })(t)
      : ft(
          (function (e) {
            var t,
              n = We(e),
              r = it(e),
              o = null == (t = e.ownerDocument) ? void 0 : t.body,
              a = Pe(
                n.scrollWidth,
                n.clientWidth,
                o ? o.scrollWidth : 0,
                o ? o.clientWidth : 0,
              ),
              i = Pe(
                n.scrollHeight,
                n.clientHeight,
                o ? o.scrollHeight : 0,
                o ? o.clientHeight : 0,
              ),
              s = -r.scrollLeft + st(e),
              l = -r.scrollTop;
            return (
              "rtl" === He(o || n).direction &&
                (s += Pe(n.clientWidth, o ? o.clientWidth : 0) - a),
              { width: a, height: i, x: s, y: l }
            );
          })(We(e)),
        );
}
function dt(e, t, n) {
  var r =
      "clippingParents" === t
        ? (function (e) {
            var t = ut(qe(e)),
              n =
                ["absolute", "fixed"].indexOf(He(e).position) >= 0 && Ce(e)
                  ? Ue(e)
                  : e;
            return Se(n)
              ? t.filter(function (e) {
                  return Se(e) && Ie(e, n) && "body" !== Ee(e);
                })
              : [];
          })(e)
        : [].concat(t),
    o = [].concat(r, [n]),
    a = o[0],
    i = o.reduce(
      function (t, n) {
        var r = ct(e, n);
        return (
          (t.top = Pe(r.top, t.top)),
          (t.right = Fe(r.right, t.right)),
          (t.bottom = Fe(r.bottom, t.bottom)),
          (t.left = Pe(r.left, t.left)),
          t
        );
      },
      ct(e, a),
    );
  return (
    (i.width = i.right - i.left),
    (i.height = i.bottom - i.top),
    (i.x = i.left),
    (i.y = i.top),
    i
  );
}
function vt(e) {
  var t,
    n = e.reference,
    r = e.element,
    o = e.placement,
    a = o ? Me(o) : null,
    i = o ? Ye(o) : null,
    s = n.x + n.width / 2 - r.width / 2,
    l = n.y + n.height / 2 - r.height / 2;
  switch (a) {
    case fe:
      t = { x: s, y: n.y - r.height };
      break;
    case ce:
      t = { x: s, y: n.y + n.height };
      break;
    case de:
      t = { x: n.x + n.width, y: l };
      break;
    case ve:
      t = { x: n.x - r.width, y: l };
      break;
    default:
      t = { x: n.x, y: n.y };
  }
  var p = a ? ze(a) : null;
  if (null != p) {
    var u = "y" === p ? "height" : "width";
    switch (i) {
      case he:
        t[p] = t[p] - (n[u] / 2 - r[u] / 2);
        break;
      case be:
        t[p] = t[p] + (n[u] / 2 - r[u] / 2);
    }
  }
  return t;
}
function mt(e, t) {
  void 0 === t && (t = {});
  var n = t,
    r = n.placement,
    o = void 0 === r ? e.placement : r,
    a = n.boundary,
    i = void 0 === a ? ye : a,
    s = n.rootBoundary,
    l = void 0 === s ? we : s,
    p = n.elementContext,
    u = void 0 === p ? xe : p,
    f = n.altBoundary,
    c = void 0 !== f && f,
    d = n.padding,
    v = void 0 === d ? 0 : d,
    m = Ke("number" != typeof v ? v : Ze(v, ge)),
    g = u === xe ? Oe : xe,
    h = e.rects.popper,
    b = e.elements[c ? g : u],
    y = dt(Se(b) ? b : b.contextElement || We(e.elements.popper), i, l),
    w = De(e.elements.reference),
    x = vt({ reference: w, element: h, strategy: "absolute", placement: o }),
    O = ft(Object.assign({}, h, x)),
    R = u === xe ? O : w,
    A = {
      top: y.top - R.top + m.top,
      bottom: R.bottom - y.bottom + m.bottom,
      left: y.left - R.left + m.left,
      right: R.right - y.right + m.right,
    },
    k = e.modifiersData.offset;
  if (u === xe && k) {
    var E = k[o];
    Object.keys(A).forEach(function (e) {
      var t = [de, ce].indexOf(e) >= 0 ? 1 : -1,
        n = [fe, ce].indexOf(e) >= 0 ? "y" : "x";
      A[e] += E[n] * t;
    });
  }
  return A;
}
var gt = {
  name: "flip",
  enabled: !0,
  phase: "main",
  fn: function (e) {
    var t = e.state,
      n = e.options,
      r = e.name;
    if (!t.modifiersData[r]._skip) {
      for (
        var o = n.mainAxis,
          a = void 0 === o || o,
          i = n.altAxis,
          s = void 0 === i || i,
          l = n.fallbackPlacements,
          p = n.padding,
          u = n.boundary,
          f = n.rootBoundary,
          c = n.altBoundary,
          d = n.flipVariations,
          v = void 0 === d || d,
          m = n.allowedAutoPlacements,
          g = t.options.placement,
          h = Me(g),
          b =
            l ||
            (h === g || !v
              ? [rt(g)]
              : (function (e) {
                  if (Me(e) === me) return [];
                  var t = rt(e);
                  return [at(e), t, at(t)];
                })(g)),
          y = [g].concat(b).reduce(function (e, n) {
            return e.concat(
              Me(n) === me
                ? (function (e, t) {
                    void 0 === t && (t = {});
                    var n = t,
                      r = n.placement,
                      o = n.boundary,
                      a = n.rootBoundary,
                      i = n.padding,
                      s = n.flipVariations,
                      l = n.allowedAutoPlacements,
                      p = void 0 === l ? Ae : l,
                      u = Ye(r),
                      f = u
                        ? s
                          ? Re
                          : Re.filter(function (e) {
                              return Ye(e) === u;
                            })
                        : ge,
                      c = f.filter(function (e) {
                        return p.indexOf(e) >= 0;
                      });
                    0 === c.length && (c = f);
                    var d = c.reduce(function (t, n) {
                      return (
                        (t[n] = mt(e, {
                          placement: n,
                          boundary: o,
                          rootBoundary: a,
                          padding: i,
                        })[Me(n)]),
                        t
                      );
                    }, {});
                    return Object.keys(d).sort(function (e, t) {
                      return d[e] - d[t];
                    });
                  })(t, {
                    placement: n,
                    boundary: u,
                    rootBoundary: f,
                    padding: p,
                    flipVariations: v,
                    allowedAutoPlacements: m,
                  })
                : n,
            );
          }, []),
          w = t.rects.reference,
          x = t.rects.popper,
          O = new Map(),
          R = !0,
          A = y[0],
          k = 0;
        k < y.length;
        k++
      ) {
        var E = y[k],
          T = Me(E),
          S = Ye(E) === he,
          C = [fe, ce].indexOf(T) >= 0,
          j = C ? "width" : "height",
          B = mt(t, {
            placement: E,
            boundary: u,
            rootBoundary: f,
            altBoundary: c,
            padding: p,
          }),
          M = C ? (S ? de : ve) : S ? ce : fe;
        w[j] > x[j] && (M = rt(M));
        var P = rt(M),
          F = [];
        if (
          (a && F.push(B[T] <= 0),
          s && F.push(B[M] <= 0, B[P] <= 0),
          F.every(function (e) {
            return e;
          }))
        ) {
          ((A = E), (R = !1));
          break;
        }
        O.set(E, F);
      }
      if (R)
        for (
          var L = function (e) {
              var t = y.find(function (t) {
                var n = O.get(t);
                if (n)
                  return n.slice(0, e).every(function (e) {
                    return e;
                  });
              });
              if (t) return ((A = t), "break");
            },
            D = v ? 3 : 1;
          D > 0;
          D--
        ) {
          if ("break" === L(D)) break;
        }
      t.placement !== A &&
        ((t.modifiersData[r]._skip = !0), (t.placement = A), (t.reset = !0));
    }
  },
  requiresIfExists: ["offset"],
  data: { _skip: !1 },
};
function ht(e, t, n) {
  return (
    void 0 === n && (n = { x: 0, y: 0 }),
    {
      top: e.top - t.height - n.y,
      right: e.right - t.width + n.x,
      bottom: e.bottom - t.height + n.y,
      left: e.left - t.width - n.x,
    }
  );
}
function bt(e) {
  return [fe, de, ce, ve].some(function (t) {
    return e[t] >= 0;
  });
}
var yt = {
  name: "hide",
  enabled: !0,
  phase: "main",
  requiresIfExists: ["preventOverflow"],
  fn: function (e) {
    var t = e.state,
      n = e.name,
      r = t.rects.reference,
      o = t.rects.popper,
      a = t.modifiersData.preventOverflow,
      i = mt(t, { elementContext: "reference" }),
      s = mt(t, { altBoundary: !0 }),
      l = ht(i, r),
      p = ht(s, o, a),
      u = bt(l),
      f = bt(p);
    ((t.modifiersData[n] = {
      referenceClippingOffsets: l,
      popperEscapeOffsets: p,
      isReferenceHidden: u,
      hasPopperEscaped: f,
    }),
      (t.attributes.popper = Object.assign({}, t.attributes.popper, {
        "data-popper-reference-hidden": u,
        "data-popper-escaped": f,
      })));
  },
};
var wt = {
  name: "offset",
  enabled: !0,
  phase: "main",
  requires: ["popperOffsets"],
  fn: function (e) {
    var t = e.state,
      n = e.options,
      r = e.name,
      o = n.offset,
      a = void 0 === o ? [0, 0] : o,
      i = Ae.reduce(function (e, n) {
        return (
          (e[n] = (function (e, t, n) {
            var r = Me(e),
              o = [ve, fe].indexOf(r) >= 0 ? -1 : 1,
              a =
                "function" == typeof n
                  ? n(Object.assign({}, t, { placement: e }))
                  : n,
              i = a[0],
              s = a[1];
            return (
              (i = i || 0),
              (s = (s || 0) * o),
              [ve, de].indexOf(r) >= 0 ? { x: s, y: i } : { x: i, y: s }
            );
          })(n, t.rects, a)),
          e
        );
      }, {}),
      s = i[t.placement],
      l = s.x,
      p = s.y;
    (null != t.modifiersData.popperOffsets &&
      ((t.modifiersData.popperOffsets.x += l),
      (t.modifiersData.popperOffsets.y += p)),
      (t.modifiersData[r] = i));
  },
};
var xt = {
  name: "popperOffsets",
  enabled: !0,
  phase: "read",
  fn: function (e) {
    var t = e.state,
      n = e.name;
    t.modifiersData[n] = vt({
      reference: t.rects.reference,
      element: t.rects.popper,
      strategy: "absolute",
      placement: t.placement,
    });
  },
  data: {},
};
var Ot = {
  name: "preventOverflow",
  enabled: !0,
  phase: "main",
  fn: function (e) {
    var t = e.state,
      n = e.options,
      r = e.name,
      o = n.mainAxis,
      a = void 0 === o || o,
      i = n.altAxis,
      s = void 0 !== i && i,
      l = n.boundary,
      p = n.rootBoundary,
      u = n.altBoundary,
      f = n.padding,
      c = n.tether,
      d = void 0 === c || c,
      v = n.tetherOffset,
      m = void 0 === v ? 0 : v,
      g = mt(t, { boundary: l, rootBoundary: p, padding: f, altBoundary: u }),
      h = Me(t.placement),
      b = Ye(t.placement),
      y = !b,
      w = ze(h),
      x = (function (e) {
        return "x" === e ? "y" : "x";
      })(w),
      O = t.modifiersData.popperOffsets,
      R = t.rects.reference,
      A = t.rects.popper,
      k =
        "function" == typeof m
          ? m(Object.assign({}, t.rects, { placement: t.placement }))
          : m,
      E =
        "number" == typeof k
          ? { mainAxis: k, altAxis: k }
          : Object.assign({ mainAxis: 0, altAxis: 0 }, k),
      T = t.modifiersData.offset ? t.modifiersData.offset[t.placement] : null,
      S = { x: 0, y: 0 };
    if (O) {
      if (a) {
        var C,
          j = "y" === w ? fe : ve,
          B = "y" === w ? ce : de,
          M = "y" === w ? "height" : "width",
          P = O[w],
          F = P + g[j],
          L = P - g[B],
          D = d ? -A[M] / 2 : 0,
          _ = b === he ? R[M] : A[M],
          I = b === he ? -A[M] : -R[M],
          H = t.elements.arrow,
          $ = d && H ? _e(H) : { width: 0, height: 0 },
          W = t.modifiersData["arrow#persistent"]
            ? t.modifiersData["arrow#persistent"].padding
            : { top: 0, right: 0, bottom: 0, left: 0 },
          q = W[j],
          N = W[B],
          U = Ve(0, R[M], $[M]),
          z = y ? R[M] / 2 - D - U - q - E.mainAxis : _ - U - q - E.mainAxis,
          V = y ? -R[M] / 2 + D + U + N + E.mainAxis : I + U + N + E.mainAxis,
          K = t.elements.arrow && Ue(t.elements.arrow),
          Z = K ? ("y" === w ? K.clientTop || 0 : K.clientLeft || 0) : 0,
          X = null != (C = null == T ? void 0 : T[w]) ? C : 0,
          Y = P + V - X,
          J = Ve(d ? Fe(F, P + z - X - Z) : F, P, d ? Pe(L, Y) : L);
        ((O[w] = J), (S[w] = J - P));
      }
      if (s) {
        var Q,
          G = "x" === w ? fe : ve,
          ee = "x" === w ? ce : de,
          te = O[x],
          ne = "y" === x ? "height" : "width",
          re = te + g[G],
          oe = te - g[ee],
          ae = -1 !== [fe, ve].indexOf(h),
          ie = null != (Q = null == T ? void 0 : T[x]) ? Q : 0,
          se = ae ? re : te - R[ne] - A[ne] - ie + E.altAxis,
          le = ae ? te + R[ne] + A[ne] - ie - E.altAxis : oe,
          pe =
            d && ae
              ? (function (e, t, n) {
                  var r = Ve(e, t, n);
                  return r > n ? n : r;
                })(se, te, le)
              : Ve(d ? se : re, te, d ? le : oe);
        ((O[x] = pe), (S[x] = pe - te));
      }
      t.modifiersData[r] = S;
    }
  },
  requiresIfExists: ["offset"],
};
function Rt(e, t, n) {
  void 0 === n && (n = !1);
  var r = Ce(t),
    o =
      Ce(t) &&
      (function (e) {
        var t = e.getBoundingClientRect(),
          n = Le(t.width) / e.offsetWidth || 1,
          r = Le(t.height) / e.offsetHeight || 1;
        return 1 !== n || 1 !== r;
      })(t),
    a = We(t),
    i = De(e, o),
    s = { scrollLeft: 0, scrollTop: 0 },
    l = { x: 0, y: 0 };
  return (
    (r || (!r && !n)) &&
      (("body" !== Ee(t) || lt(a)) &&
        (s = (function (e) {
          return e !== Te(e) && Ce(e)
            ? (function (e) {
                return { scrollLeft: e.scrollLeft, scrollTop: e.scrollTop };
              })(e)
            : it(e);
        })(t)),
      Ce(t)
        ? (((l = De(t, !0)).x += t.clientLeft), (l.y += t.clientTop))
        : a && (l.x = st(a))),
    {
      x: i.left + s.scrollLeft - l.x,
      y: i.top + s.scrollTop - l.y,
      width: i.width,
      height: i.height,
    }
  );
}
function At(e) {
  var t = new Map(),
    n = new Set(),
    r = [];
  function o(e) {
    (n.add(e.name),
      []
        .concat(e.requires || [], e.requiresIfExists || [])
        .forEach(function (e) {
          if (!n.has(e)) {
            var r = t.get(e);
            r && o(r);
          }
        }),
      r.push(e));
  }
  return (
    e.forEach(function (e) {
      t.set(e.name, e);
    }),
    e.forEach(function (e) {
      n.has(e.name) || o(e);
    }),
    r
  );
}
function kt(e) {
  var t;
  return function () {
    return (
      t ||
        (t = new Promise(function (n) {
          Promise.resolve().then(function () {
            ((t = void 0), n(e()));
          });
        })),
      t
    );
  };
}
var Et = { placement: "bottom", modifiers: [], strategy: "absolute" };
function Tt() {
  for (var e = arguments.length, t = new Array(e), n = 0; n < e; n++)
    t[n] = arguments[n];
  return !t.some(function (e) {
    return !(e && "function" == typeof e.getBoundingClientRect);
  });
}
function St(e) {
  void 0 === e && (e = {});
  var t = e,
    n = t.defaultModifiers,
    r = void 0 === n ? [] : n,
    o = t.defaultOptions,
    a = void 0 === o ? Et : o;
  return function (e, t, n) {
    void 0 === n && (n = a);
    var o = {
        placement: "bottom",
        orderedModifiers: [],
        options: Object.assign({}, Et, a),
        modifiersData: {},
        elements: { reference: e, popper: t },
        attributes: {},
        styles: {},
      },
      i = [],
      s = !1,
      l = {
        state: o,
        setOptions: function (n) {
          var s = "function" == typeof n ? n(o.options) : n;
          (p(),
            (o.options = Object.assign({}, a, o.options, s)),
            (o.scrollParents = {
              reference: Se(e)
                ? ut(e)
                : e.contextElement
                  ? ut(e.contextElement)
                  : [],
              popper: ut(t),
            }));
          var u = (function (e) {
            var t = At(e);
            return ke.reduce(function (e, n) {
              return e.concat(
                t.filter(function (e) {
                  return e.phase === n;
                }),
              );
            }, []);
          })(
            (function (e) {
              var t = e.reduce(function (e, t) {
                var n = e[t.name];
                return (
                  (e[t.name] = n
                    ? Object.assign({}, n, t, {
                        options: Object.assign({}, n.options, t.options),
                        data: Object.assign({}, n.data, t.data),
                      })
                    : t),
                  e
                );
              }, {});
              return Object.keys(t).map(function (e) {
                return t[e];
              });
            })([].concat(r, o.options.modifiers)),
          );
          return (
            (o.orderedModifiers = u.filter(function (e) {
              return e.enabled;
            })),
            o.orderedModifiers.forEach(function (e) {
              var t = e.name,
                n = e.options,
                r = void 0 === n ? {} : n,
                a = e.effect;
              if ("function" == typeof a) {
                var s = a({ state: o, name: t, instance: l, options: r }),
                  p = function () {};
                i.push(s || p);
              }
            }),
            l.update()
          );
        },
        forceUpdate: function () {
          if (!s) {
            var e = o.elements,
              t = e.reference,
              n = e.popper;
            if (Tt(t, n)) {
              ((o.rects = {
                reference: Rt(t, Ue(n), "fixed" === o.options.strategy),
                popper: _e(n),
              }),
                (o.reset = !1),
                (o.placement = o.options.placement),
                o.orderedModifiers.forEach(function (e) {
                  return (o.modifiersData[e.name] = Object.assign({}, e.data));
                }));
              for (var r = 0; r < o.orderedModifiers.length; r++)
                if (!0 !== o.reset) {
                  var a = o.orderedModifiers[r],
                    i = a.fn,
                    p = a.options,
                    u = void 0 === p ? {} : p,
                    f = a.name;
                  "function" == typeof i &&
                    (o =
                      i({ state: o, options: u, name: f, instance: l }) || o);
                } else ((o.reset = !1), (r = -1));
            }
          }
        },
        update: kt(function () {
          return new Promise(function (e) {
            (l.forceUpdate(), e(o));
          });
        }),
        destroy: function () {
          (p(), (s = !0));
        },
      };
    if (!Tt(e, t)) return l;
    function p() {
      (i.forEach(function (e) {
        return e();
      }),
        (i = []));
    }
    return (
      l.setOptions(n).then(function (e) {
        !s && n.onFirstUpdate && n.onFirstUpdate(e);
      }),
      l
    );
  };
}
(St(), St({ defaultModifiers: [tt, xt, Ge, Be] }));
var Ct = St({ defaultModifiers: [tt, xt, Ge, Be, wt, gt, Ot, Xe, yt] });
const jt = (e, t, n = {}) => {
  const o = {
      name: "updateState",
      enabled: !0,
      phase: "write",
      fn: ({ state: e }) => {
        const t = (function (e) {
          const t = Object.keys(e.elements),
            n = d(t.map((t) => [t, e.styles[t] || {}])),
            r = d(t.map((t) => [t, e.attributes[t]]));
          return { styles: n, attributes: r };
        })(e);
        Object.assign(l.value, t);
      },
      requires: ["computeStyles"],
    },
    i = r(() => {
      const {
        onFirstUpdate: e,
        placement: t,
        strategy: r,
        modifiers: a,
      } = p(n);
      return {
        onFirstUpdate: e,
        placement: t || "bottom",
        strategy: r || "absolute",
        modifiers: [...(a || []), o, { name: "applyStyles", enabled: !1 }],
      };
    }),
    s = u(),
    l = f({
      styles: {
        popper: { position: p(i).strategy, left: "0", top: "0" },
        arrow: { position: "absolute" },
      },
      attributes: {},
    }),
    v = () => {
      s.value && (s.value.destroy(), (s.value = void 0));
    };
  return (
    a(
      i,
      (e) => {
        const t = p(s);
        t && t.setOptions(e);
      },
      { deep: !0 },
    ),
    a([e, t], ([e, t]) => {
      (v(), e && t && (s.value = Ct(e, t, p(i))));
    }),
    c(() => {
      v();
    }),
    {
      state: r(() => {
        var e;
        return { ...((null == (e = p(s)) ? void 0 : e.state) || {}) };
      }),
      styles: r(() => p(l).styles),
      attributes: r(() => p(l).attributes),
      update: () => {
        var e;
        return null == (e = p(s)) ? void 0 : e.update();
      },
      forceUpdate: () => {
        var e;
        return null == (e = p(s)) ? void 0 : e.forceUpdate();
      },
      instanceRef: r(() => p(s)),
    }
  );
};
function Bt() {
  let e;
  const t = () => window.clearTimeout(e);
  return (
    v(() => t()),
    {
      registerTimeout: (n, r) => {
        (t(), (e = window.setTimeout(n, r)));
      },
      cancelTimeout: t,
    }
  );
}
let Mt;
const Pt = () => {
    const e = g(),
      t = h(),
      n = r(() => `${e.value}-popper-container-${t.prefix}`),
      o = r(() => `#${n.value}`);
    return { id: n, selector: o };
  },
  Ft = () => {
    const { id: e, selector: t } = Pt();
    return (
      m(() => {
        s &&
          (Mt ||
            document.body.querySelector(t.value) ||
            (Mt = ((e) => {
              const t = document.createElement("div");
              return ((t.id = e), document.body.appendChild(t), t);
            })(e.value)));
      }),
      { id: e, selector: t }
    );
  },
  Lt = b({
    showAfter: { type: Number, default: 0 },
    hideAfter: { type: Number, default: 200 },
    autoClose: { type: Number, default: 0 },
  }),
  Dt = ({ showAfter: e, hideAfter: t, autoClose: n, open: r, close: o }) => {
    const { registerTimeout: a } = Bt(),
      { registerTimeout: i, cancelTimeout: s } = Bt();
    return {
      onOpen: (t) => {
        a(() => {
          r(t);
          const e = p(n);
          y(e) &&
            e > 0 &&
            i(() => {
              o(t);
            }, e);
        }, p(e));
      },
      onClose: (e) => {
        (s(),
          a(() => {
            o(e);
          }, p(t)));
      },
    };
  },
  _t = Symbol("elForwardRef"),
  It = Symbol("popper"),
  Ht = Symbol("popperContent"),
  $t = b({
    role: {
      type: String,
      values: [
        "dialog",
        "grid",
        "group",
        "listbox",
        "menu",
        "navigation",
        "tooltip",
        "tree",
      ],
      default: "tooltip",
    },
  }),
  Wt = x({ name: "ElPopper", inheritAttrs: !1 });
var qt = R(
  x({
    ...Wt,
    props: $t,
    setup(e, { expose: t }) {
      const n = e,
        o = {
          triggerRef: f(),
          popperInstanceRef: f(),
          contentRef: f(),
          referenceRef: f(),
          role: r(() => n.role),
        };
      return (t(o), w(It, o), (e, t) => O(e.$slots, "default"));
    },
  }),
  [
    [
      "__file",
      "/home/runner/work/element-plus/element-plus/packages/components/popper/src/popper.vue",
    ],
  ],
);
const Nt = b({ arrowOffset: { type: Number, default: 5 } }),
  Ut = x({ name: "ElPopperArrow", inheritAttrs: !1 });
var zt = R(
  x({
    ...Ut,
    props: Nt,
    setup(e, { expose: t }) {
      const n = e,
        r = A("popper"),
        { arrowOffset: o, arrowRef: i, arrowStyle: s } = k(Ht, void 0);
      return (
        a(
          () => n.arrowOffset,
          (e) => {
            o.value = e;
          },
        ),
        c(() => {
          i.value = void 0;
        }),
        t({ arrowRef: i }),
        (e, t) => (
          E(),
          T(
            "span",
            {
              ref_key: "arrowRef",
              ref: i,
              class: S(p(r).e("arrow")),
              style: C(p(s)),
              "data-popper-arrow": "",
            },
            null,
            6,
          )
        )
      );
    },
  }),
  [
    [
      "__file",
      "/home/runner/work/element-plus/element-plus/packages/components/popper/src/arrow.vue",
    ],
  ],
);
const Vt = x({
  name: "ElOnlyChild",
  setup(e, { slots: t, attrs: n }) {
    var r;
    const o = k(_t),
      a =
        ((i = null != (r = null == o ? void 0 : o.setForwardRef) ? r : j),
        {
          mounted(e) {
            i(e);
          },
          updated(e) {
            i(e);
          },
          unmounted() {
            i(null);
          },
        });
    var i;
    return () => {
      var e;
      const r = null == (e = t.default) ? void 0 : e.call(t, n);
      if (!r) return null;
      if (r.length > 1) return null;
      const o = Kt(r);
      return o ? B(M(o, n), [[a]]) : null;
    };
  },
});
function Kt(e) {
  if (!e) return null;
  const t = e;
  for (const n of t) {
    if (P(n))
      switch (n.type) {
        case D:
          continue;
        case L:
        case "svg":
          return Zt(n);
        case F:
          return Kt(n.children);
        default:
          return n;
      }
    return Zt(n);
  }
  return null;
}
function Zt(e) {
  const t = A("only-child");
  return _("span", { class: t.e("content") }, [e]);
}
const Xt = b({
    virtualRef: { type: t(Object) },
    virtualTriggering: Boolean,
    onMouseenter: { type: t(Function) },
    onMouseleave: { type: t(Function) },
    onClick: { type: t(Function) },
    onKeydown: { type: t(Function) },
    onFocus: { type: t(Function) },
    onBlur: { type: t(Function) },
    onContextmenu: { type: t(Function) },
    id: String,
    open: Boolean,
  }),
  Yt = x({ name: "ElPopperTrigger", inheritAttrs: !1 });
var Jt = R(
  x({
    ...Yt,
    props: Xt,
    setup(e, { expose: t }) {
      const n = e,
        { role: o, triggerRef: s } = k(It, void 0);
      var l;
      ((l = s),
        w(_t, {
          setForwardRef: (e) => {
            l.value = e;
          },
        }));
      const u = r(() => (d.value ? n.id : void 0)),
        f = r(() => {
          if (o && "tooltip" === o.value) return n.open && n.id ? n.id : void 0;
        }),
        d = r(() => {
          if (o && "tooltip" !== o.value) return o.value;
        }),
        v = r(() => (d.value ? `${n.open}` : void 0));
      let m;
      return (
        i(() => {
          (a(
            () => n.virtualRef,
            (e) => {
              e && (s.value = I(e));
            },
            { immediate: !0 },
          ),
            a(
              s,
              (e, t) => {
                (null == m || m(),
                  (m = void 0),
                  H(e) &&
                    ([
                      "onMouseenter",
                      "onMouseleave",
                      "onClick",
                      "onKeydown",
                      "onFocus",
                      "onBlur",
                      "onContextmenu",
                    ].forEach((r) => {
                      var o;
                      const a = n[r];
                      a &&
                        (e.addEventListener(r.slice(2).toLowerCase(), a),
                        null ==
                          (o = null == t ? void 0 : t.removeEventListener) ||
                          o.call(t, r.slice(2).toLowerCase(), a));
                    }),
                    (m = a(
                      [u, f, d, v],
                      (t) => {
                        [
                          "aria-controls",
                          "aria-describedby",
                          "aria-haspopup",
                          "aria-expanded",
                        ].forEach((n, r) => {
                          oe(t[r])
                            ? e.removeAttribute(n)
                            : e.setAttribute(n, t[r]);
                        });
                      },
                      { immediate: !0 },
                    ))),
                  H(t) &&
                    [
                      "aria-controls",
                      "aria-describedby",
                      "aria-haspopup",
                      "aria-expanded",
                    ].forEach((e) => t.removeAttribute(e)));
              },
              { immediate: !0 },
            ));
        }),
        c(() => {
          (null == m || m(), (m = void 0));
        }),
        t({ triggerRef: s }),
        (e, t) =>
          e.virtualTriggering
            ? N("v-if", !0)
            : (E(),
              $(
                p(Vt),
                q({ key: 0 }, e.$attrs, {
                  "aria-controls": p(u),
                  "aria-describedby": p(f),
                  "aria-expanded": p(v),
                  "aria-haspopup": p(d),
                }),
                { default: W(() => [O(e.$slots, "default")]), _: 3 },
                16,
                [
                  "aria-controls",
                  "aria-describedby",
                  "aria-expanded",
                  "aria-haspopup",
                ],
              ))
      );
    },
  }),
  [
    [
      "__file",
      "/home/runner/work/element-plus/element-plus/packages/components/popper/src/trigger.vue",
    ],
  ],
);
const Qt = b({
    boundariesPadding: { type: Number, default: 0 },
    fallbackPlacements: { type: t(Array), default: void 0 },
    gpuAcceleration: { type: Boolean, default: !0 },
    offset: { type: Number, default: 12 },
    placement: { type: String, values: Ae, default: "bottom" },
    popperOptions: { type: t(Object), default: () => ({}) },
    strategy: {
      type: String,
      values: ["fixed", "absolute"],
      default: "absolute",
    },
  }),
  Gt = b({
    ...Qt,
    id: String,
    style: { type: t([String, Array, Object]) },
    className: { type: t([String, Array, Object]) },
    effect: { type: String, default: "dark" },
    visible: Boolean,
    enterable: { type: Boolean, default: !0 },
    pure: Boolean,
    focusOnShow: { type: Boolean, default: !1 },
    trapping: { type: Boolean, default: !1 },
    popperClass: { type: t([String, Array, Object]) },
    popperStyle: { type: t([String, Array, Object]) },
    referenceEl: { type: t(Object) },
    triggerTargetEl: { type: t(Object) },
    stopPopperMouseEvent: { type: Boolean, default: !0 },
    ariaLabel: { type: String, default: void 0 },
    virtualTriggering: Boolean,
    zIndex: Number,
  }),
  en = {
    mouseenter: (e) => e instanceof MouseEvent,
    mouseleave: (e) => e instanceof MouseEvent,
    focus: () => !0,
    blur: () => !0,
    close: () => !0,
  },
  tn = (e, t = []) => {
    const { placement: n, strategy: r, popperOptions: o } = e,
      a = { placement: n, strategy: r, ...o, modifiers: [...nn(e), ...t] };
    return (
      (function (e, t) {
        t && (e.modifiers = [...e.modifiers, ...(null != t ? t : [])]);
      })(a, null == o ? void 0 : o.modifiers),
      a
    );
  };
function nn(e) {
  const { offset: t, gpuAcceleration: n, fallbackPlacements: r } = e;
  return [
    { name: "offset", options: { offset: [0, null != t ? t : 12] } },
    {
      name: "preventOverflow",
      options: { padding: { top: 2, bottom: 2, left: 5, right: 5 } },
    },
    { name: "flip", options: { padding: 5, fallbackPlacements: r } },
    { name: "computeStyles", options: { gpuAcceleration: n } },
  ];
}
const rn = (e) => {
    const {
        popperInstanceRef: t,
        contentRef: n,
        triggerRef: o,
        role: l,
      } = k(It, void 0),
      u = f(),
      c = f(),
      d = r(() => ({ name: "eventListeners", enabled: !!e.visible })),
      v = r(() => {
        var e;
        const t = p(u),
          n = null != (e = p(c)) ? e : 0;
        return {
          name: "arrow",
          enabled: ((r = t), !(void 0 === r)),
          options: { element: t, padding: n },
        };
        var r;
      }),
      m = r(() => ({
        onFirstUpdate: () => {
          w();
        },
        ...tn(e, [p(v), p(d)]),
      })),
      g = r(
        () =>
          ((e) => {
            if (s) return I(e);
          })(e.referenceEl) || p(o),
      ),
      {
        attributes: h,
        state: b,
        styles: y,
        update: w,
        forceUpdate: x,
        instanceRef: O,
      } = jt(g, n, m);
    return (
      a(O, (e) => (t.value = e)),
      i(() => {
        a(
          () => {
            var e;
            return null == (e = p(g)) ? void 0 : e.getBoundingClientRect();
          },
          () => {
            w();
          },
        );
      }),
      {
        attributes: h,
        arrowRef: u,
        contentRef: n,
        instanceRef: O,
        state: b,
        styles: y,
        role: l,
        forceUpdate: x,
        update: w,
      }
    );
  },
  on = x({ name: "ElPopperContent" });
var an = R(
  x({
    ...on,
    props: Gt,
    emits: en,
    setup(e, { expose: t, emit: n }) {
      const o = e,
        {
          focusStartRef: s,
          trapped: l,
          onFocusAfterReleased: u,
          onFocusAfterTrapped: d,
          onFocusInTrap: v,
          onFocusoutPrevented: m,
          onReleaseRequested: g,
        } = ((e, t) => {
          const n = f(!1),
            r = f();
          return {
            focusStartRef: r,
            trapped: n,
            onFocusAfterReleased: (e) => {
              var n;
              "pointer" !== (null == (n = e.detail) ? void 0 : n.focusReason) &&
                ((r.value = "first"), t("blur"));
            },
            onFocusAfterTrapped: () => {
              t("focus");
            },
            onFocusInTrap: (t) => {
              e.visible &&
                !n.value &&
                (t.target && (r.value = t.target), (n.value = !0));
            },
            onFocusoutPrevented: (t) => {
              e.trapping ||
                ("pointer" === t.detail.focusReason && t.preventDefault(),
                (n.value = !1));
            },
            onReleaseRequested: () => {
              ((n.value = !1), t("close"));
            },
          };
        })(o, n),
        {
          attributes: h,
          arrowRef: b,
          contentRef: y,
          styles: x,
          instanceRef: R,
          role: S,
          update: C,
        } = rn(o),
        {
          ariaModal: B,
          arrowStyle: M,
          contentAttrs: P,
          contentClass: F,
          contentStyle: L,
          updateZIndex: D,
        } = ((e, { attributes: t, styles: n, role: o }) => {
          const { nextZIndex: a } = U(),
            i = A("popper"),
            s = r(() => p(t).popper),
            l = f(e.zIndex || a()),
            u = r(() => [
              i.b(),
              i.is("pure", e.pure),
              i.is(e.effect),
              e.popperClass,
            ]),
            c = r(() => [{ zIndex: p(l) }, p(n).popper, e.popperStyle || {}]);
          return {
            ariaModal: r(() => ("dialog" === o.value ? "false" : void 0)),
            arrowStyle: r(() => p(n).arrow || {}),
            contentAttrs: s,
            contentClass: u,
            contentStyle: c,
            contentZIndex: l,
            updateZIndex: () => {
              l.value = e.zIndex || a();
            },
          };
        })(o, { styles: x, attributes: h, role: S }),
        I = k(z, void 0),
        $ = f();
      let N;
      (w(Ht, { arrowStyle: M, arrowRef: b, arrowOffset: $ }),
        I &&
          (I.addInputId || I.removeInputId) &&
          w(z, { ...I, addInputId: j, removeInputId: j }));
      const V = (e = !0) => {
          (C(), e && D());
        },
        K = () => {
          (V(!1),
            o.visible && o.focusOnShow
              ? (l.value = !0)
              : !1 === o.visible && (l.value = !1));
        };
      return (
        i(() => {
          (a(
            () => o.triggerTargetEl,
            (e, t) => {
              (null == N || N(), (N = void 0));
              const n = p(e || y.value),
                r = p(t || y.value);
              (H(n) &&
                (N = a(
                  [S, () => o.ariaLabel, B, () => o.id],
                  (e) => {
                    ["role", "aria-label", "aria-modal", "id"].forEach(
                      (t, r) => {
                        oe(e[r])
                          ? n.removeAttribute(t)
                          : n.setAttribute(t, e[r]);
                      },
                    );
                  },
                  { immediate: !0 },
                )),
                r !== n &&
                  H(r) &&
                  ["role", "aria-label", "aria-modal", "id"].forEach((e) => {
                    r.removeAttribute(e);
                  }));
            },
            { immediate: !0 },
          ),
            a(() => o.visible, K, { immediate: !0 }));
        }),
        c(() => {
          (null == N || N(), (N = void 0));
        }),
        t({
          popperContentRef: y,
          popperInstanceRef: R,
          updatePopper: V,
          contentStyle: L,
        }),
        (e, t) => (
          E(),
          T(
            "div",
            q({ ref_key: "contentRef", ref: y }, p(P), {
              style: p(L),
              class: p(F),
              tabindex: "-1",
              onMouseenter: t[0] || (t[0] = (t) => e.$emit("mouseenter", t)),
              onMouseleave: t[1] || (t[1] = (t) => e.$emit("mouseleave", t)),
            }),
            [
              _(
                p(ae),
                {
                  trapped: p(l),
                  "trap-on-focus-in": !0,
                  "focus-trap-el": p(y),
                  "focus-start-el": p(s),
                  onFocusAfterTrapped: p(d),
                  onFocusAfterReleased: p(u),
                  onFocusin: p(v),
                  onFocusoutPrevented: p(m),
                  onReleaseRequested: p(g),
                },
                { default: W(() => [O(e.$slots, "default")]), _: 3 },
                8,
                [
                  "trapped",
                  "focus-trap-el",
                  "focus-start-el",
                  "onFocusAfterTrapped",
                  "onFocusAfterReleased",
                  "onFocusin",
                  "onFocusoutPrevented",
                  "onReleaseRequested",
                ],
              ),
            ],
            16,
          )
        )
      );
    },
  }),
  [
    [
      "__file",
      "/home/runner/work/element-plus/element-plus/packages/components/popper/src/content.vue",
    ],
  ],
);
const sn = V(qt),
  ln = Symbol("elTooltip"),
  pn = b({
    ...Lt,
    ...Gt,
    appendTo: { type: t([String, Object]) },
    content: { type: String, default: "" },
    rawContent: { type: Boolean, default: !1 },
    persistent: Boolean,
    ariaLabel: String,
    visible: { type: t(Boolean), default: null },
    transition: String,
    teleported: { type: Boolean, default: !0 },
    disabled: Boolean,
  }),
  un = b({
    ...Xt,
    disabled: Boolean,
    trigger: { type: t([String, Array]), default: "hover" },
    triggerKeys: { type: t(Array), default: () => [K.enter, K.space] },
  }),
  {
    useModelToggleProps: fn,
    useModelToggleEmits: cn,
    useModelToggle: dn,
  } = ue("visible"),
  vn = b({
    ...$t,
    ...fn,
    ...pn,
    ...un,
    ...Nt,
    showArrow: { type: Boolean, default: !0 },
  }),
  mn = [...cn, "before-show", "before-hide", "show", "hide", "open", "close"],
  gn = (e, t, n) => (r) => {
    ((e, t) => (Z(e) ? e.includes(t) : e === t))(p(e), t) && n(r);
  },
  hn = x({ name: "ElTooltipTrigger" });
var bn = R(
  x({
    ...hn,
    props: un,
    setup(e, { expose: t }) {
      const n = e,
        r = A("tooltip"),
        {
          controlled: o,
          id: a,
          open: i,
          onOpen: s,
          onClose: l,
          onToggle: u,
        } = k(ln, void 0),
        c = f(null),
        d = () => {
          if (p(o) || n.disabled) return !0;
        },
        v = X(n, "trigger"),
        m = ie(d, gn(v, "hover", s)),
        g = ie(d, gn(v, "hover", l)),
        h = ie(
          d,
          gn(v, "click", (e) => {
            0 === e.button && u(e);
          }),
        ),
        b = ie(d, gn(v, "focus", s)),
        y = ie(d, gn(v, "focus", l)),
        w = ie(
          d,
          gn(v, "contextmenu", (e) => {
            (e.preventDefault(), u(e));
          }),
        ),
        x = ie(d, (e) => {
          const { code: t } = e;
          n.triggerKeys.includes(t) && (e.preventDefault(), u(e));
        });
      return (
        t({ triggerRef: c }),
        (e, t) => (
          E(),
          $(
            p(Jt),
            {
              id: p(a),
              "virtual-ref": e.virtualRef,
              open: p(i),
              "virtual-triggering": e.virtualTriggering,
              class: S(p(r).e("trigger")),
              onBlur: p(y),
              onClick: p(h),
              onContextmenu: p(w),
              onFocus: p(b),
              onMouseenter: p(m),
              onMouseleave: p(g),
              onKeydown: p(x),
            },
            { default: W(() => [O(e.$slots, "default")]), _: 3 },
            8,
            [
              "id",
              "virtual-ref",
              "open",
              "virtual-triggering",
              "class",
              "onBlur",
              "onClick",
              "onContextmenu",
              "onFocus",
              "onMouseenter",
              "onMouseleave",
              "onKeydown",
            ],
          )
        )
      );
    },
  }),
  [
    [
      "__file",
      "/home/runner/work/element-plus/element-plus/packages/components/tooltip/src/trigger.vue",
    ],
  ],
);
const yn = x({ name: "ElTooltipContent", inheritAttrs: !1 });
var wn = R(
  x({
    ...yn,
    props: pn,
    setup(e, { expose: t }) {
      const n = e,
        { selector: o } = Pt(),
        i = A("tooltip"),
        s = f(null),
        l = f(!1),
        {
          controlled: u,
          id: d,
          open: v,
          trigger: m,
          onClose: g,
          onOpen: h,
          onShow: b,
          onHide: y,
          onBeforeShow: w,
          onBeforeHide: x,
        } = k(ln, void 0),
        R = r(() => n.transition || `${i.namespace.value}-fade-in-linear`),
        T = r(() => n.persistent);
      c(() => {
        l.value = !0;
      });
      const S = r(() => !!p(T) || p(v)),
        C = r(() => !n.disabled && p(v)),
        j = r(() => n.appendTo || o.value),
        M = r(() => {
          var e;
          return null != (e = n.style) ? e : {};
        }),
        P = r(() => !p(v)),
        F = () => {
          y();
        },
        L = () => {
          if (p(u)) return !0;
        },
        D = ie(L, () => {
          n.enterable && "hover" === p(m) && h();
        }),
        I = ie(L, () => {
          "hover" === p(m) && g();
        }),
        H = () => {
          var e, t;
          (null == (t = null == (e = s.value) ? void 0 : e.updatePopper) ||
            t.call(e),
            null == w || w());
        },
        U = () => {
          null == x || x();
        },
        z = () => {
          (b(),
            (K = G(
              r(() => {
                var e;
                return null == (e = s.value) ? void 0 : e.popperContentRef;
              }),
              () => {
                if (p(u)) return;
                "hover" !== p(m) && g();
              },
            )));
        },
        V = () => {
          n.virtualTriggering || g();
        };
      let K;
      return (
        a(
          () => p(v),
          (e) => {
            e || null == K || K();
          },
          { flush: "post" },
        ),
        a(
          () => n.content,
          () => {
            var e, t;
            null == (t = null == (e = s.value) ? void 0 : e.updatePopper) ||
              t.call(e);
          },
        ),
        t({ contentRef: s }),
        (e, t) => (
          E(),
          $(
            Q,
            { disabled: !e.teleported, to: p(j) },
            [
              _(
                J,
                {
                  name: p(R),
                  onAfterLeave: F,
                  onBeforeEnter: H,
                  onAfterEnter: z,
                  onBeforeLeave: U,
                },
                {
                  default: W(() => [
                    p(S)
                      ? B(
                          (E(),
                          $(
                            p(an),
                            q(
                              {
                                key: 0,
                                id: p(d),
                                ref_key: "contentRef",
                                ref: s,
                              },
                              e.$attrs,
                              {
                                "aria-label": e.ariaLabel,
                                "aria-hidden": p(P),
                                "boundaries-padding": e.boundariesPadding,
                                "fallback-placements": e.fallbackPlacements,
                                "gpu-acceleration": e.gpuAcceleration,
                                offset: e.offset,
                                placement: e.placement,
                                "popper-options": e.popperOptions,
                                strategy: e.strategy,
                                effect: e.effect,
                                enterable: e.enterable,
                                pure: e.pure,
                                "popper-class": e.popperClass,
                                "popper-style": [e.popperStyle, p(M)],
                                "reference-el": e.referenceEl,
                                "trigger-target-el": e.triggerTargetEl,
                                visible: p(C),
                                "z-index": e.zIndex,
                                onMouseenter: p(D),
                                onMouseleave: p(I),
                                onBlur: V,
                                onClose: p(g),
                              },
                            ),
                            {
                              default: W(() => [
                                l.value
                                  ? N("v-if", !0)
                                  : O(e.$slots, "default", { key: 0 }),
                              ]),
                              _: 3,
                            },
                            16,
                            [
                              "id",
                              "aria-label",
                              "aria-hidden",
                              "boundaries-padding",
                              "fallback-placements",
                              "gpu-acceleration",
                              "offset",
                              "placement",
                              "popper-options",
                              "strategy",
                              "effect",
                              "enterable",
                              "pure",
                              "popper-class",
                              "popper-style",
                              "reference-el",
                              "trigger-target-el",
                              "visible",
                              "z-index",
                              "onMouseenter",
                              "onMouseleave",
                              "onClose",
                            ],
                          )),
                          [[Y, p(C)]],
                        )
                      : N("v-if", !0),
                  ]),
                  _: 3,
                },
                8,
                ["name"],
              ),
            ],
            8,
            ["disabled", "to"],
          )
        )
      );
    },
  }),
  [
    [
      "__file",
      "/home/runner/work/element-plus/element-plus/packages/components/tooltip/src/content.vue",
    ],
  ],
);
const xn = ["innerHTML"],
  On = { key: 1 },
  Rn = x({ name: "ElTooltip" });
const An = V(
  R(
    x({
      ...Rn,
      props: vn,
      emits: mn,
      setup(e, { expose: t, emit: n }) {
        const o = e;
        Ft();
        const i = ee(),
          s = f(),
          u = f(),
          c = () => {
            var e;
            const t = p(s);
            t && (null == (e = t.popperInstanceRef) || e.update());
          },
          d = f(!1),
          v = f(),
          {
            show: m,
            hide: g,
            hasUpdateHandler: h,
          } = dn({ indicator: d, toggleReason: v }),
          { onOpen: b, onClose: y } = Dt({
            showAfter: X(o, "showAfter"),
            hideAfter: X(o, "hideAfter"),
            autoClose: X(o, "autoClose"),
            open: m,
            close: g,
          }),
          x = r(() => l(o.visible) && !h.value);
        (w(ln, {
          controlled: x,
          id: i,
          open: te(d),
          trigger: X(o, "trigger"),
          onOpen: (e) => {
            b(e);
          },
          onClose: (e) => {
            y(e);
          },
          onToggle: (e) => {
            p(d) ? y(e) : b(e);
          },
          onShow: () => {
            n("show", v.value);
          },
          onHide: () => {
            n("hide", v.value);
          },
          onBeforeShow: () => {
            n("before-show", v.value);
          },
          onBeforeHide: () => {
            n("before-hide", v.value);
          },
          updatePopper: c,
        }),
          a(
            () => o.disabled,
            (e) => {
              e && d.value && (d.value = !1);
            },
          ));
        return (
          ne(() => d.value && g()),
          t({
            popperRef: s,
            contentRef: u,
            isFocusInsideContent: (e) => {
              var t, n;
              const r =
                  null == (n = null == (t = u.value) ? void 0 : t.contentRef)
                    ? void 0
                    : n.popperContentRef,
                o =
                  (null == e ? void 0 : e.relatedTarget) ||
                  document.activeElement;
              return r && r.contains(o);
            },
            updatePopper: c,
            onOpen: b,
            onClose: y,
            hide: g,
          }),
          (e, t) => (
            E(),
            $(
              p(sn),
              { ref_key: "popperRef", ref: s, role: e.role },
              {
                default: W(() => [
                  _(
                    bn,
                    {
                      disabled: e.disabled,
                      trigger: e.trigger,
                      "trigger-keys": e.triggerKeys,
                      "virtual-ref": e.virtualRef,
                      "virtual-triggering": e.virtualTriggering,
                    },
                    {
                      default: W(() => [
                        e.$slots.default
                          ? O(e.$slots, "default", { key: 0 })
                          : N("v-if", !0),
                      ]),
                      _: 3,
                    },
                    8,
                    [
                      "disabled",
                      "trigger",
                      "trigger-keys",
                      "virtual-ref",
                      "virtual-triggering",
                    ],
                  ),
                  _(
                    wn,
                    {
                      ref_key: "contentRef",
                      ref: u,
                      "aria-label": e.ariaLabel,
                      "boundaries-padding": e.boundariesPadding,
                      content: e.content,
                      disabled: e.disabled,
                      effect: e.effect,
                      enterable: e.enterable,
                      "fallback-placements": e.fallbackPlacements,
                      "hide-after": e.hideAfter,
                      "gpu-acceleration": e.gpuAcceleration,
                      offset: e.offset,
                      persistent: e.persistent,
                      "popper-class": e.popperClass,
                      "popper-style": e.popperStyle,
                      placement: e.placement,
                      "popper-options": e.popperOptions,
                      pure: e.pure,
                      "raw-content": e.rawContent,
                      "reference-el": e.referenceEl,
                      "trigger-target-el": e.triggerTargetEl,
                      "show-after": e.showAfter,
                      strategy: e.strategy,
                      teleported: e.teleported,
                      transition: e.transition,
                      "virtual-triggering": e.virtualTriggering,
                      "z-index": e.zIndex,
                      "append-to": e.appendTo,
                    },
                    {
                      default: W(() => [
                        O(e.$slots, "content", {}, () => [
                          e.rawContent
                            ? (E(),
                              T(
                                "span",
                                { key: 0, innerHTML: e.content },
                                null,
                                8,
                                xn,
                              ))
                            : (E(), T("span", On, re(e.content), 1)),
                        ]),
                        e.showArrow
                          ? (E(),
                            $(
                              p(zt),
                              { key: 0, "arrow-offset": e.arrowOffset },
                              null,
                              8,
                              ["arrow-offset"],
                            ))
                          : N("v-if", !0),
                      ]),
                      _: 3,
                    },
                    8,
                    [
                      "aria-label",
                      "boundaries-padding",
                      "content",
                      "disabled",
                      "effect",
                      "enterable",
                      "fallback-placements",
                      "hide-after",
                      "gpu-acceleration",
                      "offset",
                      "persistent",
                      "popper-class",
                      "popper-style",
                      "placement",
                      "popper-options",
                      "pure",
                      "raw-content",
                      "reference-el",
                      "trigger-target-el",
                      "show-after",
                      "strategy",
                      "teleported",
                      "transition",
                      "virtual-triggering",
                      "z-index",
                      "append-to",
                    ],
                  ),
                ]),
                _: 3,
              },
              8,
              ["role"],
            )
          )
        );
      },
    }),
    [
      [
        "__file",
        "/home/runner/work/element-plus/element-plus/packages/components/tooltip/src/tooltip.vue",
      ],
    ],
  ),
);
export {
  An as E,
  Vt as O,
  ln as T,
  Ae as a,
  un as b,
  ie as c,
  Dt as d,
  pn as u,
  se as w,
  Ct as y,
};
