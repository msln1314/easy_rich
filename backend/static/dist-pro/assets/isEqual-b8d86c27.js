import {
  aM as e,
  aP as r,
  cE as t,
  cF as n,
  cG as a,
  cH as c,
  bJ as o,
  cI as f,
  cJ as i,
  cK as u,
  cL as s,
  cM as v,
} from "./index-6b60d190.js";
function b(e, r) {
  for (var t = -1, n = null == e ? 0 : e.length; ++t < n; )
    if (r(e[t], t, e)) return !0;
  return !1;
}
var l = 1,
  g = 2;
function p(t, n, a, c, o, f) {
  var i = a & l,
    u = t.length,
    s = n.length;
  if (u != s && !(i && s > u)) return !1;
  var v = f.get(t),
    p = f.get(n);
  if (v && p) return v == n && p == t;
  var j = -1,
    y = !0,
    h = a & g ? new e() : void 0;
  for (f.set(t, n), f.set(n, t); ++j < u; ) {
    var d = t[j],
      w = n[j];
    if (c) var m = i ? c(w, d, j, n, t, f) : c(d, w, j, t, n, f);
    if (void 0 !== m) {
      if (m) continue;
      y = !1;
      break;
    }
    if (h) {
      if (
        !b(n, function (e, t) {
          if (!r(h, t) && (d === e || o(d, e, a, c, f))) return h.push(t);
        })
      ) {
        y = !1;
        break;
      }
    } else if (d !== w && !o(d, w, a, c, f)) {
      y = !1;
      break;
    }
  }
  return (f.delete(t), f.delete(n), y);
}
function j(e) {
  var r = -1,
    t = Array(e.size);
  return (
    e.forEach(function (e, n) {
      t[++r] = [n, e];
    }),
    t
  );
}
function y(e) {
  var r = -1,
    t = Array(e.size);
  return (
    e.forEach(function (e) {
      t[++r] = e;
    }),
    t
  );
}
var h = 1,
  d = 2,
  w = "[object Boolean]",
  m = "[object Date]",
  O = "[object Error]",
  _ = "[object Map]",
  A = "[object Number]",
  E = "[object RegExp]",
  L = "[object Set]",
  k = "[object String]",
  z = "[object Symbol]",
  x = "[object ArrayBuffer]",
  M = "[object DataView]",
  P = t ? t.prototype : void 0,
  S = P ? P.valueOf : void 0;
var B = 1,
  D = Object.prototype.hasOwnProperty;
var J = 1,
  F = "[object Arguments]",
  G = "[object Array]",
  H = "[object Object]",
  I = Object.prototype.hasOwnProperty;
function K(e, r, t, v, b, l) {
  var g = o(e),
    P = o(r),
    K = g ? G : f(e),
    N = P ? G : f(r),
    R = (K = K == F ? H : K) == H,
    V = (N = N == F ? H : N) == H,
    q = K == N;
  if (q && i(e)) {
    if (!i(r)) return !1;
    ((g = !0), (R = !1));
  }
  if (q && !R)
    return (
      l || (l = new u()),
      g || s(e)
        ? p(e, r, t, v, b, l)
        : (function (e, r, t, c, o, f, i) {
            switch (t) {
              case M:
                if (
                  e.byteLength != r.byteLength ||
                  e.byteOffset != r.byteOffset
                )
                  return !1;
                ((e = e.buffer), (r = r.buffer));
              case x:
                return !(
                  e.byteLength != r.byteLength || !f(new a(e), new a(r))
                );
              case w:
              case m:
              case A:
                return n(+e, +r);
              case O:
                return e.name == r.name && e.message == r.message;
              case E:
              case k:
                return e == r + "";
              case _:
                var u = j;
              case L:
                var s = c & h;
                if ((u || (u = y), e.size != r.size && !s)) return !1;
                var v = i.get(e);
                if (v) return v == r;
                ((c |= d), i.set(e, r));
                var b = p(u(e), u(r), c, o, f, i);
                return (i.delete(e), b);
              case z:
                if (S) return S.call(e) == S.call(r);
            }
            return !1;
          })(e, r, K, t, v, b, l)
    );
  if (!(t & J)) {
    var C = R && I.call(e, "__wrapped__"),
      Q = V && I.call(r, "__wrapped__");
    if (C || Q) {
      var T = C ? e.value() : e,
        U = Q ? r.value() : r;
      return (l || (l = new u()), b(T, U, t, v, l));
    }
  }
  return (
    !!q &&
    (l || (l = new u()),
    (function (e, r, t, n, a, o) {
      var f = t & B,
        i = c(e),
        u = i.length;
      if (u != c(r).length && !f) return !1;
      for (var s = u; s--; ) {
        var v = i[s];
        if (!(f ? v in r : D.call(r, v))) return !1;
      }
      var b = o.get(e),
        l = o.get(r);
      if (b && l) return b == r && l == e;
      var g = !0;
      (o.set(e, r), o.set(r, e));
      for (var p = f; ++s < u; ) {
        var j = e[(v = i[s])],
          y = r[v];
        if (n) var h = f ? n(y, j, v, r, e, o) : n(j, y, v, e, r, o);
        if (!(void 0 === h ? j === y || a(j, y, t, n, o) : h)) {
          g = !1;
          break;
        }
        p || (p = "constructor" == v);
      }
      if (g && !p) {
        var d = e.constructor,
          w = r.constructor;
        d == w ||
          !("constructor" in e) ||
          !("constructor" in r) ||
          ("function" == typeof d &&
            d instanceof d &&
            "function" == typeof w &&
            w instanceof w) ||
          (g = !1);
      }
      return (o.delete(e), o.delete(r), g);
    })(e, r, t, v, b, l))
  );
}
function N(e, r, t, n, a) {
  return (
    e === r ||
    (null == e || null == r || (!v(e) && !v(r))
      ? e != e && r != r
      : K(e, r, t, n, N, a))
  );
}
function R(e, r) {
  return N(e, r);
}
export { N as b, R as i, y as s };
