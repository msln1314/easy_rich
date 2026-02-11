import {
  a9 as e,
  aa as a,
  b2 as t,
  ce as n,
  aZ as l,
  b as r,
  d as s,
  bc as o,
  b6 as u,
  e as i,
  aT as d,
  a_ as c,
  u as v,
  b8 as p,
  ao as m,
  r as f,
  f as h,
  w as y,
  as as b,
  ba as g,
  bz as k,
  cf as w,
  b9 as D,
  k as M,
  aV as S,
  am as x,
  o as $,
  l as C,
  m as _,
  s as O,
  n as P,
  aY as V,
  E as Y,
  p as A,
  F as I,
  j as T,
  y as N,
  q as L,
  z as R,
  a6 as E,
  _ as F,
  aA as B,
  b3 as W,
  cg as H,
  a2 as z,
  a1 as j,
  a5 as K,
  M as U,
  G as Z,
  a0 as q,
  x as G,
  bk as X,
  bd as J,
  aD as Q,
  D as ee,
  ch as ae,
  aX as te,
  bq as ne,
  aE as le,
  a4 as re,
  aH as se,
  ci as oe,
  ax as ue,
  ay as ie,
  cj as de,
  N as ce,
  aq as ve,
  L as pe,
} from "./index-6b60d190.js";
import { E as me } from "./el-input-38d674e5.js";
import { E as fe, T as he } from "./el-popper-09548d54.js";
import { d as ye } from "./debounce-5c500a3d.js";
import { C as be } from "./index-fdfa028a.js";
import { i as ge } from "./isEqual-b8d86c27.js";
const ke = (e) => [...new Set(e)],
  we = (e) => (e || 0 === e ? (Array.isArray(e) ? e : [e]) : []);
var De = { exports: {} };
De.exports = (function () {
  var e = 1e3,
    a = 6e4,
    t = 36e5,
    n = "millisecond",
    l = "second",
    r = "minute",
    s = "hour",
    o = "day",
    u = "week",
    i = "month",
    d = "quarter",
    c = "year",
    v = "date",
    p = "Invalid Date",
    m =
      /^(\d{4})[-/]?(\d{1,2})?[-/]?(\d{0,2})[Tt\s]*(\d{1,2})?:?(\d{1,2})?:?(\d{1,2})?[.:]?(\d+)?$/,
    f =
      /\[([^\]]+)]|Y{1,4}|M{1,4}|D{1,2}|d{1,4}|H{1,2}|h{1,2}|a|A|m{1,2}|s{1,2}|Z{1,2}|SSS/g,
    h = {
      name: "en",
      weekdays:
        "Sunday_Monday_Tuesday_Wednesday_Thursday_Friday_Saturday".split("_"),
      months:
        "January_February_March_April_May_June_July_August_September_October_November_December".split(
          "_",
        ),
      ordinal: function (e) {
        var a = ["th", "st", "nd", "rd"],
          t = e % 100;
        return "[" + e + (a[(t - 20) % 10] || a[t] || a[0]) + "]";
      },
    },
    y = function (e, a, t) {
      var n = String(e);
      return !n || n.length >= a ? e : "" + Array(a + 1 - n.length).join(t) + e;
    },
    b = {
      s: y,
      z: function (e) {
        var a = -e.utcOffset(),
          t = Math.abs(a),
          n = Math.floor(t / 60),
          l = t % 60;
        return (a <= 0 ? "+" : "-") + y(n, 2, "0") + ":" + y(l, 2, "0");
      },
      m: function e(a, t) {
        if (a.date() < t.date()) return -e(t, a);
        var n = 12 * (t.year() - a.year()) + (t.month() - a.month()),
          l = a.clone().add(n, i),
          r = t - l < 0,
          s = a.clone().add(n + (r ? -1 : 1), i);
        return +(-(n + (t - l) / (r ? l - s : s - l)) || 0);
      },
      a: function (e) {
        return e < 0 ? Math.ceil(e) || 0 : Math.floor(e);
      },
      p: function (e) {
        return (
          { M: i, y: c, w: u, d: o, D: v, h: s, m: r, s: l, ms: n, Q: d }[e] ||
          String(e || "")
            .toLowerCase()
            .replace(/s$/, "")
        );
      },
      u: function (e) {
        return void 0 === e;
      },
    },
    g = "en",
    k = {};
  k[g] = h;
  var w = function (e) {
      return e instanceof x;
    },
    D = function e(a, t, n) {
      var l;
      if (!a) return g;
      if ("string" == typeof a) {
        var r = a.toLowerCase();
        (k[r] && (l = r), t && ((k[r] = t), (l = r)));
        var s = a.split("-");
        if (!l && s.length > 1) return e(s[0]);
      } else {
        var o = a.name;
        ((k[o] = a), (l = o));
      }
      return (!n && l && (g = l), l || (!n && g));
    },
    M = function (e, a) {
      if (w(e)) return e.clone();
      var t = "object" == typeof a ? a : {};
      return ((t.date = e), (t.args = arguments), new x(t));
    },
    S = b;
  ((S.l = D),
    (S.i = w),
    (S.w = function (e, a) {
      return M(e, { locale: a.$L, utc: a.$u, x: a.$x, $offset: a.$offset });
    }));
  var x = (function () {
      function h(e) {
        ((this.$L = D(e.locale, null, !0)), this.parse(e));
      }
      var y = h.prototype;
      return (
        (y.parse = function (e) {
          ((this.$d = (function (e) {
            var a = e.date,
              t = e.utc;
            if (null === a) return new Date(NaN);
            if (S.u(a)) return new Date();
            if (a instanceof Date) return new Date(a);
            if ("string" == typeof a && !/Z$/i.test(a)) {
              var n = a.match(m);
              if (n) {
                var l = n[2] - 1 || 0,
                  r = (n[7] || "0").substring(0, 3);
                return t
                  ? new Date(
                      Date.UTC(
                        n[1],
                        l,
                        n[3] || 1,
                        n[4] || 0,
                        n[5] || 0,
                        n[6] || 0,
                        r,
                      ),
                    )
                  : new Date(
                      n[1],
                      l,
                      n[3] || 1,
                      n[4] || 0,
                      n[5] || 0,
                      n[6] || 0,
                      r,
                    );
              }
            }
            return new Date(a);
          })(e)),
            (this.$x = e.x || {}),
            this.init());
        }),
        (y.init = function () {
          var e = this.$d;
          ((this.$y = e.getFullYear()),
            (this.$M = e.getMonth()),
            (this.$D = e.getDate()),
            (this.$W = e.getDay()),
            (this.$H = e.getHours()),
            (this.$m = e.getMinutes()),
            (this.$s = e.getSeconds()),
            (this.$ms = e.getMilliseconds()));
        }),
        (y.$utils = function () {
          return S;
        }),
        (y.isValid = function () {
          return !(this.$d.toString() === p);
        }),
        (y.isSame = function (e, a) {
          var t = M(e);
          return this.startOf(a) <= t && t <= this.endOf(a);
        }),
        (y.isAfter = function (e, a) {
          return M(e) < this.startOf(a);
        }),
        (y.isBefore = function (e, a) {
          return this.endOf(a) < M(e);
        }),
        (y.$g = function (e, a, t) {
          return S.u(e) ? this[a] : this.set(t, e);
        }),
        (y.unix = function () {
          return Math.floor(this.valueOf() / 1e3);
        }),
        (y.valueOf = function () {
          return this.$d.getTime();
        }),
        (y.startOf = function (e, a) {
          var t = this,
            n = !!S.u(a) || a,
            d = S.p(e),
            p = function (e, a) {
              var l = S.w(
                t.$u ? Date.UTC(t.$y, a, e) : new Date(t.$y, a, e),
                t,
              );
              return n ? l : l.endOf(o);
            },
            m = function (e, a) {
              return S.w(
                t
                  .toDate()
                  [
                    e
                  ].apply(t.toDate("s"), (n ? [0, 0, 0, 0] : [23, 59, 59, 999]).slice(a)),
                t,
              );
            },
            f = this.$W,
            h = this.$M,
            y = this.$D,
            b = "set" + (this.$u ? "UTC" : "");
          switch (d) {
            case c:
              return n ? p(1, 0) : p(31, 11);
            case i:
              return n ? p(1, h) : p(0, h + 1);
            case u:
              var g = this.$locale().weekStart || 0,
                k = (f < g ? f + 7 : f) - g;
              return p(n ? y - k : y + (6 - k), h);
            case o:
            case v:
              return m(b + "Hours", 0);
            case s:
              return m(b + "Minutes", 1);
            case r:
              return m(b + "Seconds", 2);
            case l:
              return m(b + "Milliseconds", 3);
            default:
              return this.clone();
          }
        }),
        (y.endOf = function (e) {
          return this.startOf(e, !1);
        }),
        (y.$set = function (e, a) {
          var t,
            u = S.p(e),
            d = "set" + (this.$u ? "UTC" : ""),
            p = ((t = {}),
            (t[o] = d + "Date"),
            (t[v] = d + "Date"),
            (t[i] = d + "Month"),
            (t[c] = d + "FullYear"),
            (t[s] = d + "Hours"),
            (t[r] = d + "Minutes"),
            (t[l] = d + "Seconds"),
            (t[n] = d + "Milliseconds"),
            t)[u],
            m = u === o ? this.$D + (a - this.$W) : a;
          if (u === i || u === c) {
            var f = this.clone().set(v, 1);
            (f.$d[p](m),
              f.init(),
              (this.$d = f.set(v, Math.min(this.$D, f.daysInMonth())).$d));
          } else p && this.$d[p](m);
          return (this.init(), this);
        }),
        (y.set = function (e, a) {
          return this.clone().$set(e, a);
        }),
        (y.get = function (e) {
          return this[S.p(e)]();
        }),
        (y.add = function (n, d) {
          var v,
            p = this;
          n = Number(n);
          var m = S.p(d),
            f = function (e) {
              var a = M(p);
              return S.w(a.date(a.date() + Math.round(e * n)), p);
            };
          if (m === i) return this.set(i, this.$M + n);
          if (m === c) return this.set(c, this.$y + n);
          if (m === o) return f(1);
          if (m === u) return f(7);
          var h = ((v = {}), (v[r] = a), (v[s] = t), (v[l] = e), v)[m] || 1,
            y = this.$d.getTime() + n * h;
          return S.w(y, this);
        }),
        (y.subtract = function (e, a) {
          return this.add(-1 * e, a);
        }),
        (y.format = function (e) {
          var a = this,
            t = this.$locale();
          if (!this.isValid()) return t.invalidDate || p;
          var n = e || "YYYY-MM-DDTHH:mm:ssZ",
            l = S.z(this),
            r = this.$H,
            s = this.$m,
            o = this.$M,
            u = t.weekdays,
            i = t.months,
            d = t.meridiem,
            c = function (e, t, l, r) {
              return (e && (e[t] || e(a, n))) || l[t].slice(0, r);
            },
            v = function (e) {
              return S.s(r % 12 || 12, e, "0");
            },
            m =
              d ||
              function (e, a, t) {
                var n = e < 12 ? "AM" : "PM";
                return t ? n.toLowerCase() : n;
              };
          return n.replace(f, function (e, n) {
            return (
              n ||
              (function (e) {
                switch (e) {
                  case "YY":
                    return String(a.$y).slice(-2);
                  case "YYYY":
                    return S.s(a.$y, 4, "0");
                  case "M":
                    return o + 1;
                  case "MM":
                    return S.s(o + 1, 2, "0");
                  case "MMM":
                    return c(t.monthsShort, o, i, 3);
                  case "MMMM":
                    return c(i, o);
                  case "D":
                    return a.$D;
                  case "DD":
                    return S.s(a.$D, 2, "0");
                  case "d":
                    return String(a.$W);
                  case "dd":
                    return c(t.weekdaysMin, a.$W, u, 2);
                  case "ddd":
                    return c(t.weekdaysShort, a.$W, u, 3);
                  case "dddd":
                    return u[a.$W];
                  case "H":
                    return String(r);
                  case "HH":
                    return S.s(r, 2, "0");
                  case "h":
                    return v(1);
                  case "hh":
                    return v(2);
                  case "a":
                    return m(r, s, !0);
                  case "A":
                    return m(r, s, !1);
                  case "m":
                    return String(s);
                  case "mm":
                    return S.s(s, 2, "0");
                  case "s":
                    return String(a.$s);
                  case "ss":
                    return S.s(a.$s, 2, "0");
                  case "SSS":
                    return S.s(a.$ms, 3, "0");
                  case "Z":
                    return l;
                }
                return null;
              })(e) ||
              l.replace(":", "")
            );
          });
        }),
        (y.utcOffset = function () {
          return 15 * -Math.round(this.$d.getTimezoneOffset() / 15);
        }),
        (y.diff = function (n, v, p) {
          var m,
            f = this,
            h = S.p(v),
            y = M(n),
            b = (y.utcOffset() - this.utcOffset()) * a,
            g = this - y,
            k = function () {
              return S.m(f, y);
            };
          switch (h) {
            case c:
              m = k() / 12;
              break;
            case i:
              m = k();
              break;
            case d:
              m = k() / 3;
              break;
            case u:
              m = (g - b) / 6048e5;
              break;
            case o:
              m = (g - b) / 864e5;
              break;
            case s:
              m = g / t;
              break;
            case r:
              m = g / a;
              break;
            case l:
              m = g / e;
              break;
            default:
              m = g;
          }
          return p ? m : S.a(m);
        }),
        (y.daysInMonth = function () {
          return this.endOf(i).$D;
        }),
        (y.$locale = function () {
          return k[this.$L];
        }),
        (y.locale = function (e, a) {
          if (!e) return this.$L;
          var t = this.clone(),
            n = D(e, a, !0);
          return (n && (t.$L = n), t);
        }),
        (y.clone = function () {
          return S.w(this.$d, this);
        }),
        (y.toDate = function () {
          return new Date(this.valueOf());
        }),
        (y.toJSON = function () {
          return this.isValid() ? this.toISOString() : null;
        }),
        (y.toISOString = function () {
          return this.$d.toISOString();
        }),
        (y.toString = function () {
          return this.$d.toUTCString();
        }),
        h
      );
    })(),
    $ = x.prototype;
  return (
    (M.prototype = $),
    [
      ["$ms", n],
      ["$s", l],
      ["$m", r],
      ["$H", s],
      ["$W", o],
      ["$M", i],
      ["$y", c],
      ["$D", v],
    ].forEach(function (e) {
      $[e[1]] = function (a) {
        return this.$g(a, e[0], e[1]);
      };
    }),
    (M.extend = function (e, a) {
      return (e.$i || (e(a, x, M), (e.$i = !0)), M);
    }),
    (M.locale = D),
    (M.isDayjs = w),
    (M.unix = function (e) {
      return M(1e3 * e);
    }),
    (M.en = k[g]),
    (M.Ls = k),
    (M.p = {}),
    M
  );
})();
const Me = a(De.exports);
var Se = { exports: {} };
Se.exports = (function () {
  var e = {
      LTS: "h:mm:ss A",
      LT: "h:mm A",
      L: "MM/DD/YYYY",
      LL: "MMMM D, YYYY",
      LLL: "MMMM D, YYYY h:mm A",
      LLLL: "dddd, MMMM D, YYYY h:mm A",
    },
    a =
      /(\[[^[]*\])|([-_:/.,()\s]+)|(A|a|YYYY|YY?|MM?M?M?|Do|DD?|hh?|HH?|mm?|ss?|S{1,3}|z|ZZ?)/g,
    t = /\d\d/,
    n = /\d\d?/,
    l = /\d*[^-_:/,()\s\d]+/,
    r = {},
    s = function (e) {
      return (e = +e) + (e > 68 ? 1900 : 2e3);
    },
    o = function (e) {
      return function (a) {
        this[e] = +a;
      };
    },
    u = [
      /[+-]\d\d:?(\d\d)?|Z/,
      function (e) {
        (this.zone || (this.zone = {})).offset = (function (e) {
          if (!e) return 0;
          if ("Z" === e) return 0;
          var a = e.match(/([+-]|\d\d)/g),
            t = 60 * a[1] + (+a[2] || 0);
          return 0 === t ? 0 : "+" === a[0] ? -t : t;
        })(e);
      },
    ],
    i = function (e) {
      var a = r[e];
      return a && (a.indexOf ? a : a.s.concat(a.f));
    },
    d = function (e, a) {
      var t,
        n = r.meridiem;
      if (n) {
        for (var l = 1; l <= 24; l += 1)
          if (e.indexOf(n(l, 0, a)) > -1) {
            t = l > 12;
            break;
          }
      } else t = e === (a ? "pm" : "PM");
      return t;
    },
    c = {
      A: [
        l,
        function (e) {
          this.afternoon = d(e, !1);
        },
      ],
      a: [
        l,
        function (e) {
          this.afternoon = d(e, !0);
        },
      ],
      S: [
        /\d/,
        function (e) {
          this.milliseconds = 100 * +e;
        },
      ],
      SS: [
        t,
        function (e) {
          this.milliseconds = 10 * +e;
        },
      ],
      SSS: [
        /\d{3}/,
        function (e) {
          this.milliseconds = +e;
        },
      ],
      s: [n, o("seconds")],
      ss: [n, o("seconds")],
      m: [n, o("minutes")],
      mm: [n, o("minutes")],
      H: [n, o("hours")],
      h: [n, o("hours")],
      HH: [n, o("hours")],
      hh: [n, o("hours")],
      D: [n, o("day")],
      DD: [t, o("day")],
      Do: [
        l,
        function (e) {
          var a = r.ordinal,
            t = e.match(/\d+/);
          if (((this.day = t[0]), a))
            for (var n = 1; n <= 31; n += 1)
              a(n).replace(/\[|\]/g, "") === e && (this.day = n);
        },
      ],
      M: [n, o("month")],
      MM: [t, o("month")],
      MMM: [
        l,
        function (e) {
          var a = i("months"),
            t =
              (
                i("monthsShort") ||
                a.map(function (e) {
                  return e.slice(0, 3);
                })
              ).indexOf(e) + 1;
          if (t < 1) throw new Error();
          this.month = t % 12 || t;
        },
      ],
      MMMM: [
        l,
        function (e) {
          var a = i("months").indexOf(e) + 1;
          if (a < 1) throw new Error();
          this.month = a % 12 || a;
        },
      ],
      Y: [/[+-]?\d+/, o("year")],
      YY: [
        t,
        function (e) {
          this.year = s(e);
        },
      ],
      YYYY: [/\d{4}/, o("year")],
      Z: u,
      ZZ: u,
    };
  function v(t) {
    var n, l;
    ((n = t), (l = r && r.formats));
    for (
      var s = (t = n.replace(
          /(\[[^\]]+])|(LTS?|l{1,4}|L{1,4})/g,
          function (a, t, n) {
            var r = n && n.toUpperCase();
            return (
              t ||
              l[n] ||
              e[n] ||
              l[r].replace(
                /(\[[^\]]+])|(MMMM|MM|DD|dddd)/g,
                function (e, a, t) {
                  return a || t.slice(1);
                },
              )
            );
          },
        )).match(a),
        o = s.length,
        u = 0;
      u < o;
      u += 1
    ) {
      var i = s[u],
        d = c[i],
        v = d && d[0],
        p = d && d[1];
      s[u] = p ? { regex: v, parser: p } : i.replace(/^\[|\]$/g, "");
    }
    return function (e) {
      for (var a = {}, t = 0, n = 0; t < o; t += 1) {
        var l = s[t];
        if ("string" == typeof l) n += l.length;
        else {
          var r = l.regex,
            u = l.parser,
            i = e.slice(n),
            d = r.exec(i)[0];
          (u.call(a, d), (e = e.replace(d, "")));
        }
      }
      return (
        (function (e) {
          var a = e.afternoon;
          if (void 0 !== a) {
            var t = e.hours;
            (a ? t < 12 && (e.hours += 12) : 12 === t && (e.hours = 0),
              delete e.afternoon);
          }
        })(a),
        a
      );
    };
  }
  return function (e, a, t) {
    ((t.p.customParseFormat = !0),
      e && e.parseTwoDigitYear && (s = e.parseTwoDigitYear));
    var n = a.prototype,
      l = n.parse;
    n.parse = function (e) {
      var a = e.date,
        n = e.utc,
        s = e.args;
      this.$u = n;
      var o = s[1];
      if ("string" == typeof o) {
        var u = !0 === s[2],
          i = !0 === s[3],
          d = u || i,
          c = s[2];
        (i && (c = s[2]),
          (r = this.$locale()),
          !u && c && (r = t.Ls[c]),
          (this.$d = (function (e, a, t) {
            try {
              if (["x", "X"].indexOf(a) > -1)
                return new Date(("X" === a ? 1e3 : 1) * e);
              var n = v(a)(e),
                l = n.year,
                r = n.month,
                s = n.day,
                o = n.hours,
                u = n.minutes,
                i = n.seconds,
                d = n.milliseconds,
                c = n.zone,
                p = new Date(),
                m = s || (l || r ? 1 : p.getDate()),
                f = l || p.getFullYear(),
                h = 0;
              (l && !r) || (h = r > 0 ? r - 1 : p.getMonth());
              var y = o || 0,
                b = u || 0,
                g = i || 0,
                k = d || 0;
              return c
                ? new Date(Date.UTC(f, h, m, y, b, g, k + 60 * c.offset * 1e3))
                : t
                  ? new Date(Date.UTC(f, h, m, y, b, g, k))
                  : new Date(f, h, m, y, b, g, k);
            } catch (w) {
              return new Date("");
            }
          })(a, o, n)),
          this.init(),
          c && !0 !== c && (this.$L = this.locale(c).$L),
          d && a != this.format(o) && (this.$d = new Date("")),
          (r = {}));
      } else if (o instanceof Array)
        for (var p = o.length, m = 1; m <= p; m += 1) {
          s[1] = o[m - 1];
          var f = t.apply(this, s);
          if (f.isValid()) {
            ((this.$d = f.$d), (this.$L = f.$L), this.init());
            break;
          }
          m === p && (this.$d = new Date(""));
        }
      else l.call(this, e);
    };
  };
})();
const xe = a(Se.exports),
  $e = ["hours", "minutes", "seconds"],
  Ce = "HH:mm:ss",
  _e = "YYYY-MM-DD",
  Oe = {
    date: _e,
    dates: _e,
    week: "gggg[w]ww",
    year: "YYYY",
    month: "YYYY-MM",
    datetime: `${_e} ${Ce}`,
    monthrange: "YYYY-MM",
    daterange: _e,
    datetimerange: `${_e} ${Ce}`,
  },
  Pe = (e, a) => [e > 0 ? e - 1 : void 0, e, e < a ? e + 1 : void 0],
  Ve = (e) => Array.from(Array.from({ length: e }).keys()),
  Ye = (e) =>
    e
      .replace(/\W?m{1,2}|\W?ZZ/g, "")
      .replace(/\W?h{1,2}|\W?s{1,3}|\W?a/gi, "")
      .trim(),
  Ae = (e) =>
    e.replace(/\W?D{1,2}|\W?Do|\W?d{1,4}|\W?M{1,4}|\W?Y{2,4}/g, "").trim(),
  Ie = function (e, a) {
    const t = n(e),
      l = n(a);
    return t && l ? e.getTime() === a.getTime() : !t && !l && e === a;
  },
  Te = function (e, a) {
    const t = l(e),
      n = l(a);
    return t && n
      ? e.length === a.length && e.every((e, t) => Ie(e, a[t]))
      : !t && !n && Ie(e, a);
  },
  Ne = function (e, a, n) {
    const l = t(a) || "x" === a ? Me(e).locale(n) : Me(e, a).locale(n);
    return l.isValid() ? l : void 0;
  },
  Le = function (e, a, n) {
    return t(a) ? e : "x" === a ? +e : Me(e).locale(n).format(a);
  },
  Re = (e, a) => {
    var t;
    const n = [],
      l = null == a ? void 0 : a();
    for (let r = 0; r < e; r++)
      n.push(null != (t = null == l ? void 0 : l.includes(r)) && t);
    return n;
  },
  Ee = r({
    disabledHours: { type: s(Function) },
    disabledMinutes: { type: s(Function) },
    disabledSeconds: { type: s(Function) },
  }),
  Fe = r({
    visible: Boolean,
    actualVisible: { type: Boolean, default: void 0 },
    format: { type: String, default: "" },
  }),
  Be = r({
    id: { type: s([Array, String]) },
    name: { type: s([Array, String]), default: "" },
    popperClass: { type: String, default: "" },
    format: String,
    valueFormat: String,
    type: { type: String, default: "" },
    clearable: { type: Boolean, default: !0 },
    clearIcon: { type: s([String, Object]), default: o },
    editable: { type: Boolean, default: !0 },
    prefixIcon: { type: s([String, Object]), default: "" },
    size: u,
    readonly: { type: Boolean, default: !1 },
    disabled: { type: Boolean, default: !1 },
    placeholder: { type: String, default: "" },
    popperOptions: { type: s(Object), default: () => ({}) },
    modelValue: { type: s([Date, Array, String, Number]), default: "" },
    rangeSeparator: { type: String, default: "-" },
    startPlaceholder: String,
    endPlaceholder: String,
    defaultValue: { type: s([Date, Array]) },
    defaultTime: { type: s([Date, Array]) },
    isRange: { type: Boolean, default: !1 },
    ...Ee,
    disabledDate: { type: Function },
    cellClassName: { type: Function },
    shortcuts: { type: Array, default: () => [] },
    arrowControl: { type: Boolean, default: !1 },
    label: { type: String, default: void 0 },
    tabindex: { type: s([String, Number]), default: 0 },
    validateEvent: { type: Boolean, default: !0 },
    unlinkPanels: Boolean,
  }),
  We = ["id", "name", "placeholder", "value", "disabled", "readonly"],
  He = ["id", "name", "placeholder", "value", "disabled", "readonly"],
  ze = i({ name: "Picker" }),
  je = i({
    ...ze,
    props: Be,
    emits: [
      "update:modelValue",
      "change",
      "focus",
      "blur",
      "calendar-change",
      "panel-change",
      "visible-change",
      "keydown",
    ],
    setup(e, { expose: a, emit: t }) {
      const n = e,
        r = d(),
        { lang: s } = c(),
        o = v("date"),
        u = v("input"),
        i = v("range"),
        { form: F, formItem: W } = p(),
        H = m("ElPopperOptions", {}),
        z = f(),
        j = f(),
        K = f(!1),
        U = f(!1),
        Z = f(null);
      let q = !1,
        G = !1;
      const X = h(() => [
          o.b("editor"),
          o.bm("editor", n.type),
          u.e("wrapper"),
          o.is("disabled", ve.value),
          o.is("active", K.value),
          i.b("editor"),
          Pe ? i.bm("editor", Pe.value) : "",
          r.class,
        ]),
        J = h(() => [
          u.e("icon"),
          i.e("close-icon"),
          De.value ? "" : i.e("close-icon--hidden"),
        ]);
      y(K, (e) => {
        e
          ? b(() => {
              e && (Z.value = n.modelValue);
            })
          : ((Ae.value = null),
            b(() => {
              Q(n.modelValue);
            }));
      });
      const Q = (e, a) => {
          (!a && Te(e, Z.value)) ||
            (t("change", e),
            n.validateEvent &&
              (null == W || W.validate("change").catch((e) => g())));
        },
        ee = (e) => {
          if (!Te(n.modelValue, e)) {
            let a;
            (l(e)
              ? (a = e.map((e) => Le(e, n.valueFormat, s.value)))
              : e && (a = Le(e, n.valueFormat, s.value)),
              t("update:modelValue", e ? a : e, s.value));
          }
        },
        ae = h(() => {
          if (j.value) {
            const e = Oe.value ? j.value : j.value.$el;
            return Array.from(e.querySelectorAll("input"));
          }
          return [];
        }),
        te = (e, a, t) => {
          const n = ae.value;
          n.length &&
            (t && "min" !== t
              ? "max" === t && (n[1].setSelectionRange(e, a), n[1].focus())
              : (n[0].setSelectionRange(e, a), n[0].focus()));
        },
        ne = (e = "", a = !1) => {
          let t;
          (a || (G = !0),
            (K.value = a),
            (t = l(e) ? e.map((e) => e.toDate()) : e ? e.toDate() : e),
            (Ae.value = null),
            ee(t));
        },
        le = () => {
          U.value = !0;
        },
        re = () => {
          t("visible-change", !0);
        },
        se = (e) => {
          (null == e ? void 0 : e.key) === B.esc && ue(!0, !0);
        },
        oe = () => {
          ((U.value = !1), (K.value = !1), (G = !1), t("visible-change", !1));
        },
        ue = (e = !0, a = !1) => {
          G = a;
          const [t, n] = M(ae);
          let l = t;
          (!e && Oe.value && (l = n), l && l.focus());
        },
        ie = (e) => {
          n.readonly ||
            ve.value ||
            K.value ||
            G ||
            ((K.value = !0), t("focus", e));
        };
      let de;
      const ce = (e) => {
          const a = async () => {
            setTimeout(() => {
              var l;
              de === a &&
                (((null == (l = z.value) ? void 0 : l.isFocusInsideContent()) &&
                  !q) ||
                  0 !==
                    ae.value.filter((e) => e.contains(document.activeElement))
                      .length ||
                  (Ie(),
                  (K.value = !1),
                  t("blur", e),
                  n.validateEvent &&
                    (null == W || W.validate("blur").catch((e) => g()))),
                (q = !1));
            }, 0);
          };
          ((de = a), a());
        },
        ve = h(() => n.disabled || (null == F ? void 0 : F.disabled)),
        pe = h(() => {
          let e;
          if (
            (Se.value
              ? qe.value.getDefaultValue && (e = qe.value.getDefaultValue())
              : (e = l(n.modelValue)
                  ? n.modelValue.map((e) => Ne(e, n.valueFormat, s.value))
                  : Ne(n.modelValue, n.valueFormat, s.value)),
            qe.value.getRangeAvailableTime)
          ) {
            const a = qe.value.getRangeAvailableTime(e);
            ge(a, e) ||
              ((e = a), ee(l(e) ? e.map((e) => e.toDate()) : e.toDate()));
          }
          return (l(e) && e.some((e) => !e) && (e = []), e);
        }),
        he = h(() => {
          if (!qe.value.panelReady) return "";
          const e = Ee(pe.value);
          return l(Ae.value)
            ? [
                Ae.value[0] || (e && e[0]) || "",
                Ae.value[1] || (e && e[1]) || "",
              ]
            : null !== Ae.value
              ? Ae.value
              : (!be.value && Se.value) || (!K.value && Se.value)
                ? ""
                : e
                  ? ke.value
                    ? e.join(", ")
                    : e
                  : "";
        }),
        ye = h(() => n.type.includes("time")),
        be = h(() => n.type.startsWith("time")),
        ke = h(() => "dates" === n.type),
        we = h(() => n.prefixIcon || (ye.value ? k : w)),
        De = f(!1),
        Me = (e) => {
          n.readonly ||
            ve.value ||
            (De.value &&
              (e.stopPropagation(),
              ue(!0, !0),
              b(() => {
                G = !1;
              }),
              ee(null),
              Q(null, !0),
              (De.value = !1),
              (K.value = !1),
              qe.value.handleClear && qe.value.handleClear()));
        },
        Se = h(() => {
          const { modelValue: e } = n;
          return !e || (l(e) && !e.filter(Boolean).length);
        }),
        xe = async (e) => {
          var a;
          n.readonly ||
            ve.value ||
            (("INPUT" !== (null == (a = e.target) ? void 0 : a.tagName) ||
              ae.value.includes(document.activeElement)) &&
              (K.value = !0));
        },
        $e = () => {
          n.readonly ||
            ve.value ||
            (!Se.value && n.clearable && (De.value = !0));
        },
        Ce = () => {
          De.value = !1;
        },
        _e = (e) => {
          var a;
          n.readonly ||
            ve.value ||
            (("INPUT" !==
              (null == (a = e.touches[0].target) ? void 0 : a.tagName) ||
              ae.value.includes(document.activeElement)) &&
              (K.value = !0));
        },
        Oe = h(() => n.type.includes("range")),
        Pe = D(),
        Ve = h(() => {
          var e, a;
          return null == (a = null == (e = M(z)) ? void 0 : e.popperRef)
            ? void 0
            : a.contentRef;
        }),
        Ye = h(() => {
          var e;
          return M(Oe) ? M(j) : null == (e = M(j)) ? void 0 : e.$el;
        });
      S(Ye, (e) => {
        const a = M(Ve),
          t = M(Ye);
        (a && (e.target === a || e.composedPath().includes(a))) ||
          e.target === t ||
          e.composedPath().includes(t) ||
          (K.value = !1);
      });
      const Ae = f(null),
        Ie = () => {
          if (Ae.value) {
            const e = Re(he.value);
            e &&
              Fe(e) &&
              (ee(l(e) ? e.map((e) => e.toDate()) : e.toDate()),
              (Ae.value = null));
          }
          "" === Ae.value && (ee(null), Q(null), (Ae.value = null));
        },
        Re = (e) => (e ? qe.value.parseUserInput(e) : null),
        Ee = (e) => (e ? qe.value.formatToString(e) : null),
        Fe = (e) => qe.value.isValidValue(e),
        Be = async (e) => {
          if (n.readonly || ve.value) return;
          const { code: a } = e;
          if ((t("keydown", e), a !== B.esc))
            if (
              a === B.down &&
              (qe.value.handleFocusPicker &&
                (e.preventDefault(), e.stopPropagation()),
              !1 === K.value && ((K.value = !0), await b()),
              qe.value.handleFocusPicker)
            )
              qe.value.handleFocusPicker();
            else {
              if (a !== B.tab)
                return a === B.enter || a === B.numpadEnter
                  ? ((null === Ae.value ||
                      "" === Ae.value ||
                      Fe(Re(he.value))) &&
                      (Ie(), (K.value = !1)),
                    void e.stopPropagation())
                  : void (Ae.value
                      ? e.stopPropagation()
                      : qe.value.handleKeydownInput &&
                        qe.value.handleKeydownInput(e));
              q = !0;
            }
          else
            !0 === K.value &&
              ((K.value = !1), e.preventDefault(), e.stopPropagation());
        },
        ze = (e) => {
          ((Ae.value = e), K.value || (K.value = !0));
        },
        je = (e) => {
          const a = e.target;
          Ae.value
            ? (Ae.value = [a.value, Ae.value[1]])
            : (Ae.value = [a.value, null]);
        },
        Ke = (e) => {
          const a = e.target;
          Ae.value
            ? (Ae.value = [Ae.value[0], a.value])
            : (Ae.value = [null, a.value]);
        },
        Ue = () => {
          var e;
          const a = Ae.value,
            t = Re(a && a[0]),
            n = M(pe);
          if (t && t.isValid()) {
            Ae.value = [
              Ee(t),
              (null == (e = he.value) ? void 0 : e[1]) || null,
            ];
            const a = [t, n && (n[1] || null)];
            Fe(a) && (ee(a), (Ae.value = null));
          }
        },
        Ze = () => {
          var e;
          const a = M(Ae),
            t = Re(a && a[1]),
            n = M(pe);
          if (t && t.isValid()) {
            Ae.value = [(null == (e = M(he)) ? void 0 : e[0]) || null, Ee(t)];
            const a = [n && n[0], t];
            Fe(a) && (ee(a), (Ae.value = null));
          }
        },
        qe = f({}),
        Ge = (e) => {
          ((qe.value[e[0]] = e[1]), (qe.value.panelReady = !0));
        },
        Xe = (e) => {
          t("calendar-change", e);
        },
        Je = (e, a, n) => {
          t("panel-change", e, a, n);
        };
      return (
        x("EP_PICKER_BASE", { props: n }),
        a({
          focus: ue,
          handleFocusInput: ie,
          handleBlurInput: ce,
          handleOpen: () => {
            K.value = !0;
          },
          handleClose: () => {
            K.value = !1;
          },
          onPick: ne,
        }),
        (e, a) => (
          $(),
          C(
            M(fe),
            E(
              {
                ref_key: "refPopper",
                ref: z,
                visible: K.value,
                effect: "light",
                pure: "",
                trigger: "click",
              },
              e.$attrs,
              {
                role: "dialog",
                teleported: "",
                transition: `${M(o).namespace.value}-zoom-in-top`,
                "popper-class": [
                  `${M(o).namespace.value}-picker__popper`,
                  e.popperClass,
                ],
                "popper-options": M(H),
                "fallback-placements": ["bottom", "top", "right", "left"],
                "gpu-acceleration": !1,
                "stop-popper-mouse-event": !1,
                "hide-after": 0,
                persistent: "",
                onBeforeShow: le,
                onShow: re,
                onHide: oe,
              },
            ),
            {
              default: _(() => [
                M(Oe)
                  ? ($(),
                    T(
                      "div",
                      {
                        key: 1,
                        ref_key: "inputRef",
                        ref: j,
                        class: O(M(X)),
                        style: P(e.$attrs.style),
                        onClick: ie,
                        onMouseenter: $e,
                        onMouseleave: Ce,
                        onTouchstart: _e,
                        onKeydown: Be,
                      },
                      [
                        M(we)
                          ? ($(),
                            C(
                              M(Y),
                              {
                                key: 0,
                                class: O([M(u).e("icon"), M(i).e("icon")]),
                                onMousedown: V(xe, ["prevent"]),
                                onTouchstart: _e,
                              },
                              { default: _(() => [($(), C(A(M(we))))]), _: 1 },
                              8,
                              ["class", "onMousedown"],
                            ))
                          : I("v-if", !0),
                        N(
                          "input",
                          {
                            id: e.id && e.id[0],
                            autocomplete: "off",
                            name: e.name && e.name[0],
                            placeholder: e.startPlaceholder,
                            value: M(he) && M(he)[0],
                            disabled: M(ve),
                            readonly: !e.editable || e.readonly,
                            class: O(M(i).b("input")),
                            onMousedown: xe,
                            onInput: je,
                            onChange: Ue,
                            onFocus: ie,
                            onBlur: ce,
                          },
                          null,
                          42,
                          We,
                        ),
                        L(e.$slots, "range-separator", {}, () => [
                          N(
                            "span",
                            { class: O(M(i).b("separator")) },
                            R(e.rangeSeparator),
                            3,
                          ),
                        ]),
                        N(
                          "input",
                          {
                            id: e.id && e.id[1],
                            autocomplete: "off",
                            name: e.name && e.name[1],
                            placeholder: e.endPlaceholder,
                            value: M(he) && M(he)[1],
                            disabled: M(ve),
                            readonly: !e.editable || e.readonly,
                            class: O(M(i).b("input")),
                            onMousedown: xe,
                            onFocus: ie,
                            onBlur: ce,
                            onInput: Ke,
                            onChange: Ze,
                          },
                          null,
                          42,
                          He,
                        ),
                        e.clearIcon
                          ? ($(),
                            C(
                              M(Y),
                              { key: 1, class: O(M(J)), onClick: Me },
                              {
                                default: _(() => [($(), C(A(e.clearIcon)))]),
                                _: 1,
                              },
                              8,
                              ["class"],
                            ))
                          : I("v-if", !0),
                      ],
                      38,
                    ))
                  : ($(),
                    C(
                      M(me),
                      {
                        key: 0,
                        id: e.id,
                        ref_key: "inputRef",
                        ref: j,
                        "container-role": "combobox",
                        "model-value": M(he),
                        name: e.name,
                        size: M(Pe),
                        disabled: M(ve),
                        placeholder: e.placeholder,
                        class: O([
                          M(o).b("editor"),
                          M(o).bm("editor", e.type),
                          e.$attrs.class,
                        ]),
                        style: P(e.$attrs.style),
                        readonly:
                          !e.editable ||
                          e.readonly ||
                          M(ke) ||
                          "week" === e.type,
                        label: e.label,
                        tabindex: e.tabindex,
                        "validate-event": !1,
                        onInput: ze,
                        onFocus: ie,
                        onBlur: ce,
                        onKeydown: Be,
                        onChange: Ie,
                        onMousedown: xe,
                        onMouseenter: $e,
                        onMouseleave: Ce,
                        onTouchstart: _e,
                        onClick: a[0] || (a[0] = V(() => {}, ["stop"])),
                      },
                      {
                        prefix: _(() => [
                          M(we)
                            ? ($(),
                              C(
                                M(Y),
                                {
                                  key: 0,
                                  class: O(M(u).e("icon")),
                                  onMousedown: V(xe, ["prevent"]),
                                  onTouchstart: _e,
                                },
                                {
                                  default: _(() => [($(), C(A(M(we))))]),
                                  _: 1,
                                },
                                8,
                                ["class", "onMousedown"],
                              ))
                            : I("v-if", !0),
                        ]),
                        suffix: _(() => [
                          De.value && e.clearIcon
                            ? ($(),
                              C(
                                M(Y),
                                {
                                  key: 0,
                                  class: O(`${M(u).e("icon")} clear-icon`),
                                  onClick: V(Me, ["stop"]),
                                },
                                {
                                  default: _(() => [($(), C(A(e.clearIcon)))]),
                                  _: 1,
                                },
                                8,
                                ["class", "onClick"],
                              ))
                            : I("v-if", !0),
                        ]),
                        _: 1,
                      },
                      8,
                      [
                        "id",
                        "model-value",
                        "name",
                        "size",
                        "disabled",
                        "placeholder",
                        "class",
                        "style",
                        "readonly",
                        "label",
                        "tabindex",
                        "onKeydown",
                      ],
                    )),
              ]),
              content: _(() => [
                L(e.$slots, "default", {
                  visible: K.value,
                  actualVisible: U.value,
                  parsedValue: M(pe),
                  format: e.format,
                  unlinkPanels: e.unlinkPanels,
                  type: e.type,
                  defaultValue: e.defaultValue,
                  onPick: ne,
                  onSelectRange: te,
                  onSetPickerOption: Ge,
                  onCalendarChange: Xe,
                  onPanelChange: Je,
                  onKeydown: se,
                  onMousedown: a[1] || (a[1] = V(() => {}, ["stop"])),
                }),
              ]),
              _: 3,
            },
            16,
            ["visible", "transition", "popper-class", "popper-options"],
          )
        )
      );
    },
  });
var Ke = F(je, [
  [
    "__file",
    "/home/runner/work/element-plus/element-plus/packages/components/time-picker/src/common/picker.vue",
  ],
]);
const Ue = r({ ...Fe, datetimeRole: String, parsedValue: { type: s(Object) } }),
  Ze = ({
    getAvailableHours: e,
    getAvailableMinutes: a,
    getAvailableSeconds: t,
  }) => {
    const n = {};
    return {
      timePickerOptions: n,
      getAvailableTime: (n, l, r, s) => {
        const o = { hour: e, minute: a, second: t };
        let u = n;
        return (
          ["hour", "minute", "second"].forEach((e) => {
            if (o[e]) {
              let a;
              const t = o[e];
              switch (e) {
                case "minute":
                  a = t(u.hour(), l, s);
                  break;
                case "second":
                  a = t(u.hour(), u.minute(), l, s);
                  break;
                default:
                  a = t(l, s);
              }
              if ((null == a ? void 0 : a.length) && !a.includes(u[e]())) {
                const t = r ? 0 : a.length - 1;
                u = u[e](a[t]);
              }
            }
          }),
          u
        );
      },
      onSetOption: ([e, a]) => {
        n[e] = a;
      },
    };
  },
  qe = (e) => e.map((e, a) => e || a).filter((e) => !0 !== e),
  Ge = (e, a, t) => ({
    getHoursList: (a, t) => Re(24, e && (() => (null == e ? void 0 : e(a, t)))),
    getMinutesList: (e, t, n) =>
      Re(60, a && (() => (null == a ? void 0 : a(e, t, n)))),
    getSecondsList: (e, a, n, l) =>
      Re(60, t && (() => (null == t ? void 0 : t(e, a, n, l)))),
  }),
  Xe = (e, a, t) => {
    const {
      getHoursList: n,
      getMinutesList: l,
      getSecondsList: r,
    } = Ge(e, a, t);
    return {
      getAvailableHours: (e, a) => qe(n(e, a)),
      getAvailableMinutes: (e, a, t) => qe(l(e, a, t)),
      getAvailableSeconds: (e, a, t, n) => qe(r(e, a, t, n)),
    };
  },
  Je = (e) => {
    const a = f(e.parsedValue);
    return (
      y(
        () => e.visible,
        (t) => {
          t || (a.value = e.parsedValue);
        },
      ),
      a
    );
  },
  Qe = 100,
  ea = 600,
  aa = {
    beforeMount(e, a) {
      const t = a.value,
        { interval: n = Qe, delay: l = ea } = W(t) ? {} : t;
      let r, s;
      const o = () => (W(t) ? t() : t.handler()),
        u = () => {
          (s && (clearTimeout(s), (s = void 0)),
            r && (clearInterval(r), (r = void 0)));
        };
      e.addEventListener("mousedown", (e) => {
        0 === e.button &&
          (u(),
          o(),
          document.addEventListener("mouseup", () => u(), { once: !0 }),
          (s = setTimeout(() => {
            r = setInterval(() => {
              o();
            }, n);
          }, l)));
      });
    },
  },
  ta = r({
    role: { type: String, required: !0 },
    spinnerDate: { type: s(Object), required: !0 },
    showSeconds: { type: Boolean, default: !0 },
    arrowControl: Boolean,
    amPmMode: { type: s(String), default: "" },
    ...Ee,
  }),
  na = ["onClick"],
  la = ["onMouseenter"];
var ra = F(
  i({
    __name: "basic-time-spinner",
    props: ta,
    emits: ["change", "select-range", "set-option"],
    setup(e, { emit: a }) {
      const t = e,
        n = v("time"),
        {
          getHoursList: l,
          getMinutesList: r,
          getSecondsList: s,
        } = Ge(t.disabledHours, t.disabledMinutes, t.disabledSeconds);
      let o = !1;
      const u = f(),
        i = { hours: f(), minutes: f(), seconds: f() },
        d = h(() => (t.showSeconds ? $e : $e.slice(0, 2))),
        c = h(() => {
          const { spinnerDate: e } = t;
          return { hours: e.hour(), minutes: e.minute(), seconds: e.second() };
        }),
        p = h(() => {
          const { hours: e, minutes: a } = M(c);
          return {
            hours: l(t.role),
            minutes: r(e, t.role),
            seconds: s(e, a, t.role),
          };
        }),
        m = h(() => {
          const { hours: e, minutes: a, seconds: t } = M(c);
          return { hours: Pe(e, 23), minutes: Pe(a, 59), seconds: Pe(t, 59) };
        }),
        g = ye((e) => {
          ((o = !1), D(e));
        }, 200),
        k = (e) => {
          if (!!!t.amPmMode) return "";
          let a = e < 12 ? " am" : " pm";
          return ("A" === t.amPmMode && (a = a.toUpperCase()), a);
        },
        w = (e) => {
          let t;
          switch (e) {
            case "hours":
              t = [0, 2];
              break;
            case "minutes":
              t = [3, 5];
              break;
            case "seconds":
              t = [6, 8];
          }
          const [n, l] = t;
          (a("select-range", n, l), (u.value = e));
        },
        D = (e) => {
          P(e, M(c)[e]);
        },
        S = () => {
          (D("hours"), D("minutes"), D("seconds"));
        },
        x = (e) => e.querySelector(`.${n.namespace.value}-scrollbar__wrap`),
        P = (e, a) => {
          if (t.arrowControl) return;
          const n = M(i[e]);
          n && n.$el && (x(n.$el).scrollTop = Math.max(0, a * V(e)));
        },
        V = (e) => {
          const a = M(i[e]),
            t = null == a ? void 0 : a.$el.querySelector("li");
          return (t && Number.parseFloat(H(t, "height"))) || 0;
        },
        A = () => {
          E(1);
        },
        L = () => {
          E(-1);
        },
        E = (e) => {
          u.value || w("hours");
          const a = u.value,
            t = M(c)[a],
            n = "hours" === u.value ? 24 : 60,
            l = F(a, t, e, n);
          (B(a, l), P(a, l), b(() => w(a)));
        },
        F = (e, a, t, n) => {
          let l = (a + t + n) % n;
          const r = M(p)[e];
          for (; r[l] && l !== a; ) l = (l + t + n) % n;
          return l;
        },
        B = (e, n) => {
          if (M(p)[e][n]) return;
          const { hours: l, minutes: r, seconds: s } = M(c);
          let o;
          switch (e) {
            case "hours":
              o = t.spinnerDate.hour(n).minute(r).second(s);
              break;
            case "minutes":
              o = t.spinnerDate.hour(l).minute(n).second(s);
              break;
            case "seconds":
              o = t.spinnerDate.hour(l).minute(r).second(n);
          }
          a("change", o);
        },
        W = (e) => M(i[e]).$el.offsetHeight,
        Q = () => {
          const e = (e) => {
            const a = M(i[e]);
            a &&
              a.$el &&
              (x(a.$el).onscroll = () => {
                ((e) => {
                  ((o = !0), g(e));
                  const a = Math.min(
                    Math.round(
                      (x(M(i[e]).$el).scrollTop -
                        (0.5 * W(e) - 10) / V(e) +
                        3) /
                        V(e),
                    ),
                    "hours" === e ? 23 : 59,
                  );
                  B(e, a);
                })(e);
              });
          };
          (e("hours"), e("minutes"), e("seconds"));
        };
      z(() => {
        b(() => {
          (!t.arrowControl && Q(), S(), "start" === t.role && w("hours"));
        });
      });
      return (
        a("set-option", [`${t.role}_scrollDown`, E]),
        a("set-option", [`${t.role}_emitSelectRange`, w]),
        y(
          () => t.spinnerDate,
          () => {
            o || S();
          },
        ),
        (e, a) => (
          $(),
          T(
            "div",
            { class: O([M(n).b("spinner"), { "has-seconds": e.showSeconds }]) },
            [
              e.arrowControl
                ? I("v-if", !0)
                : ($(!0),
                  T(
                    j,
                    { key: 0 },
                    K(
                      M(d),
                      (a) => (
                        $(),
                        C(
                          M(Z),
                          {
                            key: a,
                            ref_for: !0,
                            ref: (e) =>
                              ((e, a) => {
                                i[a].value = e;
                              })(e, a),
                            class: O(M(n).be("spinner", "wrapper")),
                            "wrap-style": "max-height: inherit;",
                            "view-class": M(n).be("spinner", "list"),
                            noresize: "",
                            tag: "ul",
                            onMouseenter: (e) => w(a),
                            onMousemove: (e) => D(a),
                          },
                          {
                            default: _(() => [
                              ($(!0),
                              T(
                                j,
                                null,
                                K(
                                  M(p)[a],
                                  (t, l) => (
                                    $(),
                                    T(
                                      "li",
                                      {
                                        key: l,
                                        class: O([
                                          M(n).be("spinner", "item"),
                                          M(n).is("active", l === M(c)[a]),
                                          M(n).is("disabled", t),
                                        ]),
                                        onClick: (e) =>
                                          ((e, { value: a, disabled: t }) => {
                                            t || (B(e, a), w(e), P(e, a));
                                          })(a, { value: l, disabled: t }),
                                      },
                                      [
                                        "hours" === a
                                          ? ($(),
                                            T(
                                              j,
                                              { key: 0 },
                                              [
                                                U(
                                                  R(
                                                    (
                                                      "0" +
                                                      (e.amPmMode
                                                        ? l % 12 || 12
                                                        : l)
                                                    ).slice(-2),
                                                  ) + R(k(l)),
                                                  1,
                                                ),
                                              ],
                                              64,
                                            ))
                                          : ($(),
                                            T(
                                              j,
                                              { key: 1 },
                                              [U(R(("0" + l).slice(-2)), 1)],
                                              64,
                                            )),
                                      ],
                                      10,
                                      na,
                                    )
                                  ),
                                ),
                                128,
                              )),
                            ]),
                            _: 2,
                          },
                          1032,
                          [
                            "class",
                            "view-class",
                            "onMouseenter",
                            "onMousemove",
                          ],
                        )
                      ),
                    ),
                    128,
                  )),
              e.arrowControl
                ? ($(!0),
                  T(
                    j,
                    { key: 1 },
                    K(
                      M(d),
                      (a) => (
                        $(),
                        T(
                          "div",
                          {
                            key: a,
                            class: O([
                              M(n).be("spinner", "wrapper"),
                              M(n).is("arrow"),
                            ]),
                            onMouseenter: (e) => w(a),
                          },
                          [
                            q(
                              ($(),
                              C(
                                M(Y),
                                {
                                  class: O([
                                    "arrow-up",
                                    M(n).be("spinner", "arrow"),
                                  ]),
                                },
                                { default: _(() => [G(M(X))]), _: 1 },
                                8,
                                ["class"],
                              )),
                              [[M(aa), L]],
                            ),
                            q(
                              ($(),
                              C(
                                M(Y),
                                {
                                  class: O([
                                    "arrow-down",
                                    M(n).be("spinner", "arrow"),
                                  ]),
                                },
                                { default: _(() => [G(M(J))]), _: 1 },
                                8,
                                ["class"],
                              )),
                              [[M(aa), A]],
                            ),
                            N(
                              "ul",
                              { class: O(M(n).be("spinner", "list")) },
                              [
                                ($(!0),
                                T(
                                  j,
                                  null,
                                  K(
                                    M(m)[a],
                                    (t, l) => (
                                      $(),
                                      T(
                                        "li",
                                        {
                                          key: l,
                                          class: O([
                                            M(n).be("spinner", "item"),
                                            M(n).is("active", t === M(c)[a]),
                                            M(n).is("disabled", M(p)[a][t]),
                                          ]),
                                        },
                                        [
                                          "number" == typeof t
                                            ? ($(),
                                              T(
                                                j,
                                                { key: 0 },
                                                [
                                                  "hours" === a
                                                    ? ($(),
                                                      T(
                                                        j,
                                                        { key: 0 },
                                                        [
                                                          U(
                                                            R(
                                                              (
                                                                "0" +
                                                                (e.amPmMode
                                                                  ? t % 12 || 12
                                                                  : t)
                                                              ).slice(-2),
                                                            ) + R(k(t)),
                                                            1,
                                                          ),
                                                        ],
                                                        64,
                                                      ))
                                                    : ($(),
                                                      T(
                                                        j,
                                                        { key: 1 },
                                                        [
                                                          U(
                                                            R(
                                                              ("0" + t).slice(
                                                                -2,
                                                              ),
                                                            ),
                                                            1,
                                                          ),
                                                        ],
                                                        64,
                                                      )),
                                                ],
                                                64,
                                              ))
                                            : I("v-if", !0),
                                        ],
                                        2,
                                      )
                                    ),
                                  ),
                                  128,
                                )),
                              ],
                              2,
                            ),
                          ],
                          42,
                          la,
                        )
                      ),
                    ),
                    128,
                  ))
                : I("v-if", !0),
            ],
            2,
          )
        )
      );
    },
  }),
  [
    [
      "__file",
      "/home/runner/work/element-plus/element-plus/packages/components/time-picker/src/time-picker-com/basic-time-spinner.vue",
    ],
  ],
);
const sa = i({
  __name: "panel-time-pick",
  props: Ue,
  emits: ["pick", "select-range", "set-picker-option"],
  setup(e, { emit: a }) {
    const t = e,
      n = m("EP_PICKER_BASE"),
      {
        arrowControl: l,
        disabledHours: r,
        disabledMinutes: s,
        disabledSeconds: o,
        defaultValue: u,
      } = n.props,
      {
        getAvailableHours: i,
        getAvailableMinutes: d,
        getAvailableSeconds: p,
      } = Xe(r, s, o),
      y = v("time"),
      { t: b, lang: g } = c(),
      k = f([0, 2]),
      w = Je(t),
      D = h(() =>
        Q(t.actualVisible) ? `${y.namespace.value}-zoom-in-top` : "",
      ),
      S = h(() => t.format.includes("ss")),
      x = h(() =>
        t.format.includes("A") ? "A" : t.format.includes("a") ? "a" : "",
      ),
      P = () => {
        a("pick", w.value, !1);
      },
      V = (e) => {
        if (!t.visible) return;
        const n = F(e).millisecond(0);
        a("pick", n, !0);
      },
      Y = (e, t) => {
        (a("select-range", e, t), (k.value = [e, t]));
      },
      {
        timePickerOptions: A,
        onSetOption: L,
        getAvailableTime: E,
      } = Ze({
        getAvailableHours: i,
        getAvailableMinutes: d,
        getAvailableSeconds: p,
      }),
      F = (e) => E(e, t.datetimeRole || "", !0);
    return (
      a("set-picker-option", [
        "isValidValue",
        (e) => {
          const a = Me(e).locale(g.value),
            t = F(a);
          return a.isSame(t);
        },
      ]),
      a("set-picker-option", [
        "formatToString",
        (e) => (e ? e.format(t.format) : null),
      ]),
      a("set-picker-option", [
        "parseUserInput",
        (e) => (e ? Me(e, t.format).locale(g.value) : null),
      ]),
      a("set-picker-option", [
        "handleKeydownInput",
        (e) => {
          const a = e.code,
            { left: t, right: n, up: l, down: r } = B;
          if ([t, n].includes(a)) {
            return (
              ((e) => {
                const a = [0, 3].concat(S.value ? [6] : []),
                  t = ["hours", "minutes"].concat(S.value ? ["seconds"] : []),
                  n = (a.indexOf(k.value[0]) + e + a.length) % a.length;
                A.start_emitSelectRange(t[n]);
              })(a === t ? -1 : 1),
              void e.preventDefault()
            );
          }
          if ([l, r].includes(a)) {
            const t = a === l ? -1 : 1;
            return (A.start_scrollDown(t), void e.preventDefault());
          }
        },
      ]),
      a("set-picker-option", ["getRangeAvailableTime", F]),
      a("set-picker-option", ["getDefaultValue", () => Me(u).locale(g.value)]),
      (e, n) => (
        $(),
        C(
          ee,
          { name: M(D) },
          {
            default: _(() => [
              e.actualVisible || e.visible
                ? ($(),
                  T(
                    "div",
                    { key: 0, class: O(M(y).b("panel")) },
                    [
                      N(
                        "div",
                        {
                          class: O([
                            M(y).be("panel", "content"),
                            { "has-seconds": M(S) },
                          ]),
                        },
                        [
                          G(
                            ra,
                            {
                              ref: "spinner",
                              role: e.datetimeRole || "start",
                              "arrow-control": M(l),
                              "show-seconds": M(S),
                              "am-pm-mode": M(x),
                              "spinner-date": e.parsedValue,
                              "disabled-hours": M(r),
                              "disabled-minutes": M(s),
                              "disabled-seconds": M(o),
                              onChange: V,
                              onSetOption: M(L),
                              onSelectRange: Y,
                            },
                            null,
                            8,
                            [
                              "role",
                              "arrow-control",
                              "show-seconds",
                              "am-pm-mode",
                              "spinner-date",
                              "disabled-hours",
                              "disabled-minutes",
                              "disabled-seconds",
                              "onSetOption",
                            ],
                          ),
                        ],
                        2,
                      ),
                      N(
                        "div",
                        { class: O(M(y).be("panel", "footer")) },
                        [
                          N(
                            "button",
                            {
                              type: "button",
                              class: O([M(y).be("panel", "btn"), "cancel"]),
                              onClick: P,
                            },
                            R(M(b)("el.datepicker.cancel")),
                            3,
                          ),
                          N(
                            "button",
                            {
                              type: "button",
                              class: O([M(y).be("panel", "btn"), "confirm"]),
                              onClick:
                                n[0] ||
                                (n[0] = (e) =>
                                  ((e = !1, n = !1) => {
                                    n || a("pick", t.parsedValue, e);
                                  })()),
                            },
                            R(M(b)("el.datepicker.confirm")),
                            3,
                          ),
                        ],
                        2,
                      ),
                    ],
                    2,
                  ))
                : I("v-if", !0),
            ]),
            _: 1,
          },
          8,
          ["name"],
        )
      )
    );
  },
});
var oa = F(sa, [
    [
      "__file",
      "/home/runner/work/element-plus/element-plus/packages/components/time-picker/src/time-picker-com/panel-time-pick.vue",
    ],
  ]),
  ua = { exports: {} };
ua.exports = function (e, a, t) {
  var n = a.prototype,
    l = function (e) {
      return e && (e.indexOf ? e : e.s);
    },
    r = function (e, a, t, n, r) {
      var s = e.name ? e : e.$locale(),
        o = l(s[a]),
        u = l(s[t]),
        i =
          o ||
          u.map(function (e) {
            return e.slice(0, n);
          });
      if (!r) return i;
      var d = s.weekStart;
      return i.map(function (e, a) {
        return i[(a + (d || 0)) % 7];
      });
    },
    s = function () {
      return t.Ls[t.locale()];
    },
    o = function (e, a) {
      return (
        e.formats[a] ||
        e.formats[a.toUpperCase()].replace(
          /(\[[^\]]+])|(MMMM|MM|DD|dddd)/g,
          function (e, a, t) {
            return a || t.slice(1);
          },
        )
      );
    },
    u = function () {
      var e = this;
      return {
        months: function (a) {
          return a ? a.format("MMMM") : r(e, "months");
        },
        monthsShort: function (a) {
          return a ? a.format("MMM") : r(e, "monthsShort", "months", 3);
        },
        firstDayOfWeek: function () {
          return e.$locale().weekStart || 0;
        },
        weekdays: function (a) {
          return a ? a.format("dddd") : r(e, "weekdays");
        },
        weekdaysMin: function (a) {
          return a ? a.format("dd") : r(e, "weekdaysMin", "weekdays", 2);
        },
        weekdaysShort: function (a) {
          return a ? a.format("ddd") : r(e, "weekdaysShort", "weekdays", 3);
        },
        longDateFormat: function (a) {
          return o(e.$locale(), a);
        },
        meridiem: this.$locale().meridiem,
        ordinal: this.$locale().ordinal,
      };
    };
  ((n.localeData = function () {
    return u.bind(this)();
  }),
    (t.localeData = function () {
      var e = s();
      return {
        firstDayOfWeek: function () {
          return e.weekStart || 0;
        },
        weekdays: function () {
          return t.weekdays();
        },
        weekdaysShort: function () {
          return t.weekdaysShort();
        },
        weekdaysMin: function () {
          return t.weekdaysMin();
        },
        months: function () {
          return t.months();
        },
        monthsShort: function () {
          return t.monthsShort();
        },
        longDateFormat: function (a) {
          return o(e, a);
        },
        meridiem: e.meridiem,
        ordinal: e.ordinal,
      };
    }),
    (t.months = function () {
      return r(s(), "months");
    }),
    (t.monthsShort = function () {
      return r(s(), "monthsShort", "months", 3);
    }),
    (t.weekdays = function (e) {
      return r(s(), "weekdays", null, null, e);
    }),
    (t.weekdaysShort = function (e) {
      return r(s(), "weekdaysShort", "weekdays", 3, e);
    }),
    (t.weekdaysMin = function (e) {
      return r(s(), "weekdaysMin", "weekdays", 2, e);
    }));
};
const ia = a(ua.exports);
var da = { exports: {} };
da.exports = function (e, a) {
  var t = a.prototype,
    n = t.format;
  t.format = function (e) {
    var a = this,
      t = this.$locale();
    if (!this.isValid()) return n.bind(this)(e);
    var l = this.$utils(),
      r = (e || "YYYY-MM-DDTHH:mm:ssZ").replace(
        /\[([^\]]+)]|Q|wo|ww|w|WW|W|zzz|z|gggg|GGGG|Do|X|x|k{1,2}|S/g,
        function (e) {
          switch (e) {
            case "Q":
              return Math.ceil((a.$M + 1) / 3);
            case "Do":
              return t.ordinal(a.$D);
            case "gggg":
              return a.weekYear();
            case "GGGG":
              return a.isoWeekYear();
            case "wo":
              return t.ordinal(a.week(), "W");
            case "w":
            case "ww":
              return l.s(a.week(), "w" === e ? 1 : 2, "0");
            case "W":
            case "WW":
              return l.s(a.isoWeek(), "W" === e ? 1 : 2, "0");
            case "k":
            case "kk":
              return l.s(
                String(0 === a.$H ? 24 : a.$H),
                "k" === e ? 1 : 2,
                "0",
              );
            case "X":
              return Math.floor(a.$d.getTime() / 1e3);
            case "x":
              return a.$d.getTime();
            case "z":
              return "[" + a.offsetName() + "]";
            case "zzz":
              return "[" + a.offsetName("long") + "]";
            default:
              return e;
          }
        },
      );
    return n.bind(this)(r);
  };
};
const ca = a(da.exports);
var va,
  pa,
  ma = { exports: {} };
const fa = a(
  (ma.exports =
    ((va = "week"),
    (pa = "year"),
    function (e, a, t) {
      var n = a.prototype;
      ((n.week = function (e) {
        if ((void 0 === e && (e = null), null !== e))
          return this.add(7 * (e - this.week()), "day");
        var a = this.$locale().yearStart || 1;
        if (11 === this.month() && this.date() > 25) {
          var n = t(this).startOf(pa).add(1, pa).date(a),
            l = t(this).endOf(va);
          if (n.isBefore(l)) return 1;
        }
        var r = t(this)
            .startOf(pa)
            .date(a)
            .startOf(va)
            .subtract(1, "millisecond"),
          s = this.diff(r, va, !0);
        return s < 0 ? t(this).startOf("week").week() : Math.ceil(s);
      }),
        (n.weeks = function (e) {
          return (void 0 === e && (e = null), this.week(e));
        }));
    })),
);
var ha = { exports: {} };
ha.exports = function (e, a) {
  a.prototype.weekYear = function () {
    var e = this.month(),
      a = this.week(),
      t = this.year();
    return 1 === a && 11 === e ? t + 1 : 0 === e && a >= 52 ? t - 1 : t;
  };
};
const ya = a(ha.exports);
var ba = { exports: {} };
ba.exports = function (e, a, t) {
  a.prototype.dayOfYear = function (e) {
    var a =
      Math.round((t(this).startOf("day") - t(this).startOf("year")) / 864e5) +
      1;
    return null == e ? a : this.add(e - a, "day");
  };
};
const ga = a(ba.exports);
var ka = { exports: {} };
ka.exports = function (e, a) {
  a.prototype.isSameOrAfter = function (e, a) {
    return this.isSame(e, a) || this.isAfter(e, a);
  };
};
const wa = a(ka.exports);
var Da = { exports: {} };
const Ma = a(
    (Da.exports = function (e, a) {
      a.prototype.isSameOrBefore = function (e, a) {
        return this.isSame(e, a) || this.isBefore(e, a);
      };
    }),
  ),
  Sa = Symbol(),
  xa = r({ ...Be, type: { type: s(String), default: "date" } }),
  $a = ["date", "dates", "year", "month", "week", "range"],
  Ca = r({
    disabledDate: { type: s(Function) },
    date: { type: s(Object), required: !0 },
    minDate: { type: s(Object) },
    maxDate: { type: s(Object) },
    parsedValue: { type: s([Object, Array]) },
    rangeState: {
      type: s(Object),
      default: () => ({ endDate: null, selecting: !1 }),
    },
  }),
  _a = r({
    type: {
      type: s(String),
      required: !0,
      values: [
        "year",
        "month",
        "date",
        "dates",
        "week",
        "datetime",
        "datetimerange",
        "daterange",
        "monthrange",
      ],
    },
  }),
  Oa = r({ unlinkPanels: Boolean, parsedValue: { type: s(Array) } }),
  Pa = (e) => ({ type: String, values: $a, default: e }),
  Va = r({
    ..._a,
    parsedValue: { type: s([Object, Array]) },
    visible: { type: Boolean },
    format: { type: String, default: "" },
  }),
  Ya = r({
    ...Ca,
    cellClassName: { type: s(Function) },
    showWeekNumber: Boolean,
    selectionMode: Pa("date"),
  }),
  Aa = (e) => {
    if (!l(e)) return !1;
    const [a, t] = e;
    return Me.isDayjs(a) && Me.isDayjs(t) && a.isSameOrBefore(t);
  },
  Ia = (e, { lang: a, unit: t, unlinkPanels: n }) => {
    let r;
    if (l(e)) {
      let [l, r] = e.map((e) => Me(e).locale(a));
      return (n || (r = l.add(1, t)), [l, r]);
    }
    return ((r = e ? Me(e) : Me()), (r = r.locale(a)), [r, r.add(1, t)]);
  };
var Ta = i({
  name: "ElDatePickerCell",
  props: r({ cell: { type: s(Object) } }),
  setup(e) {
    const a = v("date-table-cell"),
      { slots: t } = m(Sa);
    return () => {
      const { cell: n } = e;
      if (t.default) {
        const e = t
          .default(n)
          .filter(
            (e) =>
              -2 !== e.patchFlag && "Symbol(Comment)" !== e.type.toString(),
          );
        if (e.length) return e;
      }
      return G("div", { class: a.b() }, [
        G("span", { class: a.e("text") }, [null == n ? void 0 : n.text]),
      ]);
    };
  },
});
const Na = ["aria-label", "onMousedown"],
  La = { key: 0, scope: "col" },
  Ra = ["aria-label"],
  Ea = ["aria-current", "aria-selected", "tabindex"],
  Fa = i({
    __name: "basic-date-table",
    props: Ya,
    emits: ["changerange", "pick", "select"],
    setup(e, { expose: a, emit: t }) {
      const n = e,
        l = v("date-table"),
        { t: r, lang: s } = c(),
        o = f(),
        u = f(),
        i = f(),
        d = f(),
        p = f([[], [], [], [], [], []]);
      let m = !1;
      const g = n.date.$locale().weekStart || 7,
        k = n.date
          .locale("en")
          .localeData()
          .weekdaysShort()
          .map((e) => e.toLowerCase()),
        w = h(() => (g > 3 ? 7 - g : -g)),
        D = h(() => {
          const e = n.date.startOf("month");
          return e.subtract(e.day() || 7, "day");
        }),
        S = h(() => k.concat(k).slice(g, g + 7)),
        x = h(() => ae(A.value).some((e) => e.isCurrent)),
        C = h(() => {
          const e = n.date.startOf("month");
          return {
            startOfMonthDay: e.day() || 7,
            dateCountOfMonth: e.daysInMonth(),
            dateCountOfLastMonth: e.subtract(1, "month").daysInMonth(),
          };
        }),
        _ = h(() => ("dates" === n.selectionMode ? we(n.parsedValue) : [])),
        P = (e, { columnIndex: a, rowIndex: t }, l) => {
          const { disabledDate: r, cellClassName: s } = n,
            o = M(_),
            u = ((e, { count: a, rowIndex: t, columnIndex: n }) => {
              const {
                  startOfMonthDay: l,
                  dateCountOfMonth: r,
                  dateCountOfLastMonth: s,
                } = M(C),
                o = M(w);
              if (!(t >= 0 && t <= 1))
                return (
                  a <= r
                    ? (e.text = a)
                    : ((e.text = a - r), (e.type = "next-month")),
                  !0
                );
              {
                const r = l + o < 0 ? 7 + l + o : l + o;
                if (n + 7 * t >= r) return ((e.text = a), !0);
                ((e.text = s - (r - (n % 7)) + 1 + 7 * t),
                  (e.type = "prev-month"));
              }
              return !1;
            })(e, { count: l, rowIndex: t, columnIndex: a }),
            i = e.dayjs.toDate();
          return (
            (e.selected = o.find((a) => a.valueOf() === e.dayjs.valueOf())),
            (e.isSelected = !!e.selected),
            (e.isCurrent = E(e)),
            (e.disabled = null == r ? void 0 : r(i)),
            (e.customClass = null == s ? void 0 : s(i)),
            u
          );
        },
        Y = (e) => {
          if ("week" === n.selectionMode) {
            const [a, t] = n.showWeekNumber ? [1, 7] : [0, 6],
              l = J(e[a + 1]);
            ((e[a].inRange = l),
              (e[a].start = l),
              (e[t].inRange = l),
              (e[t].end = l));
          }
        },
        A = h(() => {
          const {
              minDate: e,
              maxDate: a,
              rangeState: t,
              showWeekNumber: l,
            } = n,
            r = w.value,
            o = p.value,
            u = "day";
          let i = 1;
          if (l)
            for (let n = 0; n < 6; n++)
              o[n][0] ||
                (o[n][0] = {
                  type: "week",
                  text: D.value.add(7 * n + 1, u).week(),
                });
          return (
            ((
              e,
              a,
              {
                columnIndexOffset: t,
                startDate: n,
                nextEndDate: l,
                now: r,
                unit: s,
                relativeDateGetter: o,
                setCellMetadata: u,
                setRowMetadata: i,
              },
            ) => {
              for (let d = 0; d < e.row; d++) {
                const c = a[d];
                for (let a = 0; a < e.column; a++) {
                  let i = c[a + t];
                  i ||
                    (i = {
                      row: d,
                      column: a,
                      type: "normal",
                      inRange: !1,
                      start: !1,
                      end: !1,
                    });
                  const v = o(d * e.column + a);
                  ((i.dayjs = v),
                    (i.date = v.toDate()),
                    (i.timestamp = v.valueOf()),
                    (i.type = "normal"),
                    (i.inRange =
                      !!(
                        n &&
                        v.isSameOrAfter(n, s) &&
                        l &&
                        v.isSameOrBefore(l, s)
                      ) ||
                      !!(
                        n &&
                        v.isSameOrBefore(n, s) &&
                        l &&
                        v.isSameOrAfter(l, s)
                      )),
                    (null == n ? void 0 : n.isSameOrAfter(l))
                      ? ((i.start = !!l && v.isSame(l, s)),
                        (i.end = n && v.isSame(n, s)))
                      : ((i.start = !!n && v.isSame(n, s)),
                        (i.end = !!l && v.isSame(l, s))),
                    v.isSame(r, s) && (i.type = "today"),
                    null == u || u(i, { rowIndex: d, columnIndex: a }),
                    (c[a + t] = i));
                }
                null == i || i(c);
              }
            })({ row: 6, column: 7 }, o, {
              startDate: e,
              columnIndexOffset: l ? 1 : 0,
              nextEndDate: t.endDate || a || (t.selecting && e) || null,
              now: Me().locale(M(s)).startOf(u),
              unit: u,
              relativeDateGetter: (e) => D.value.add(e - r, u),
              setCellMetadata: (...e) => {
                P(...e, i) && (i += 1);
              },
              setRowMetadata: Y,
            }),
            o
          );
        });
      y(
        () => n.date,
        async () => {
          var e, a;
          (null == (e = o.value)
            ? void 0
            : e.contains(document.activeElement)) &&
            (await b(), null == (a = u.value) || a.focus());
        },
      );
      const L = (e = "") => ["normal", "today"].includes(e),
        E = (e) =>
          "date" === n.selectionMode && L(e.type) && F(e, n.parsedValue),
        F = (e, a) =>
          !!a &&
          Me(a)
            .locale(s.value)
            .isSame(n.date.date(Number(e.text)), "day"),
        B = (e) => {
          const a = [];
          return (
            L(e.type) && !e.disabled
              ? (a.push("available"), "today" === e.type && a.push("today"))
              : a.push(e.type),
            E(e) && a.push("current"),
            e.inRange &&
              (L(e.type) || "week" === n.selectionMode) &&
              (a.push("in-range"),
              e.start && a.push("start-date"),
              e.end && a.push("end-date")),
            e.disabled && a.push("disabled"),
            e.selected && a.push("selected"),
            e.customClass && a.push(e.customClass),
            a.join(" ")
          );
        },
        W = (e, a) => {
          const t = 7 * e + (a - (n.showWeekNumber ? 1 : 0)) - w.value;
          return D.value.add(t, "day");
        },
        H = (e) => {
          var a;
          if (!n.rangeState.selecting) return;
          let l = e.target;
          if (
            ("SPAN" === l.tagName &&
              (l = null == (a = l.parentNode) ? void 0 : a.parentNode),
            "DIV" === l.tagName && (l = l.parentNode),
            "TD" !== l.tagName)
          )
            return;
          const r = l.parentNode.rowIndex - 1,
            s = l.cellIndex;
          A.value[r][s].disabled ||
            (r === i.value && s === d.value) ||
            ((i.value = r),
            (d.value = s),
            t("changerange", { selecting: !0, endDate: W(r, s) }));
        },
        z = (e) =>
          (!x.value &&
            1 === (null == e ? void 0 : e.text) &&
            "normal" === e.type) ||
          e.isCurrent,
        U = (e) => {
          m || x.value || "date" !== n.selectionMode || X(e, !0);
        },
        Z = (e) => {
          e.target.closest("td") && (m = !0);
        },
        q = (e) => {
          e.target.closest("td") && (m = !1);
        },
        X = (e, a = !1) => {
          const l = e.target.closest("td");
          if (!l) return;
          const r = l.parentNode.rowIndex - 1,
            s = l.cellIndex,
            o = A.value[r][s];
          if (o.disabled || "week" === o.type) return;
          const u = W(r, s);
          if ("range" === n.selectionMode)
            n.rangeState.selecting && n.minDate
              ? (u >= n.minDate
                  ? t("pick", { minDate: n.minDate, maxDate: u })
                  : t("pick", { minDate: u, maxDate: n.minDate }),
                t("select", !1))
              : (t("pick", { minDate: u, maxDate: null }), t("select", !0));
          else if ("date" === n.selectionMode) t("pick", u, a);
          else if ("week" === n.selectionMode) {
            const e = u.week(),
              a = `${u.year()}w${e}`;
            t("pick", {
              year: u.year(),
              week: e,
              value: a,
              date: u.startOf("week"),
            });
          } else if ("dates" === n.selectionMode) {
            const e = o.selected
              ? we(n.parsedValue).filter(
                  (e) => (null == e ? void 0 : e.valueOf()) !== u.valueOf(),
                )
              : we(n.parsedValue).concat([u]);
            t("pick", e);
          }
        },
        J = (e) => {
          if ("week" !== n.selectionMode) return !1;
          let a = n.date.startOf("day");
          if (
            ("prev-month" === e.type && (a = a.subtract(1, "month")),
            "next-month" === e.type && (a = a.add(1, "month")),
            (a = a.date(Number.parseInt(e.text, 10))),
            n.parsedValue && !Array.isArray(n.parsedValue))
          ) {
            const e = ((n.parsedValue.day() - g + 7) % 7) - 1;
            return n.parsedValue.subtract(e, "day").isSame(a, "day");
          }
          return !1;
        };
      return (
        a({
          focus: async () => {
            var e;
            null == (e = u.value) || e.focus();
          },
        }),
        (e, a) => (
          $(),
          T(
            "table",
            {
              role: "grid",
              "aria-label": M(r)("el.datepicker.dateTablePrompt"),
              cellspacing: "0",
              cellpadding: "0",
              class: O([
                M(l).b(),
                { "is-week-mode": "week" === e.selectionMode },
              ]),
              onClick: X,
              onMousemove: H,
              onMousedown: V(Z, ["prevent"]),
              onMouseup: q,
            },
            [
              N(
                "tbody",
                { ref_key: "tbodyRef", ref: o },
                [
                  N("tr", null, [
                    e.showWeekNumber
                      ? ($(), T("th", La, R(M(r)("el.datepicker.week")), 1))
                      : I("v-if", !0),
                    ($(!0),
                    T(
                      j,
                      null,
                      K(
                        M(S),
                        (e, a) => (
                          $(),
                          T(
                            "th",
                            {
                              key: a,
                              scope: "col",
                              "aria-label": M(r)(
                                "el.datepicker.weeksFull." + e,
                              ),
                            },
                            R(M(r)("el.datepicker.weeks." + e)),
                            9,
                            Ra,
                          )
                        ),
                      ),
                      128,
                    )),
                  ]),
                  ($(!0),
                  T(
                    j,
                    null,
                    K(
                      M(A),
                      (e, a) => (
                        $(),
                        T(
                          "tr",
                          {
                            key: a,
                            class: O([M(l).e("row"), { current: J(e[1]) }]),
                          },
                          [
                            ($(!0),
                            T(
                              j,
                              null,
                              K(
                                e,
                                (e, t) => (
                                  $(),
                                  T(
                                    "td",
                                    {
                                      key: `${a}.${t}`,
                                      ref_for: !0,
                                      ref: (a) => z(e) && (u.value = a),
                                      class: O(B(e)),
                                      "aria-current": e.isCurrent
                                        ? "date"
                                        : void 0,
                                      "aria-selected": e.isCurrent,
                                      tabindex: z(e) ? 0 : -1,
                                      onFocus: U,
                                    },
                                    [G(M(Ta), { cell: e }, null, 8, ["cell"])],
                                    42,
                                    Ea,
                                  )
                                ),
                              ),
                              128,
                            )),
                          ],
                          2,
                        )
                      ),
                    ),
                    128,
                  )),
                ],
                512,
              ),
            ],
            42,
            Na,
          )
        )
      );
    },
  });
var Ba = F(Fa, [
  [
    "__file",
    "/home/runner/work/element-plus/element-plus/packages/components/date-picker/src/date-picker-com/basic-date-table.vue",
  ],
]);
const Wa = r({ ...Ca, selectionMode: Pa("month") }),
  Ha = ["aria-label"],
  za = ["aria-selected", "aria-label", "tabindex", "onKeydown"],
  ja = { class: "cell" },
  Ka = i({
    __name: "basic-month-table",
    props: Wa,
    emits: ["changerange", "pick", "select"],
    setup(e, { expose: a, emit: t }) {
      const n = e,
        l = v("month-table"),
        { t: r, lang: s } = c(),
        o = f(),
        u = f(),
        i = f(
          n.date
            .locale("en")
            .localeData()
            .monthsShort()
            .map((e) => e.toLowerCase()),
        ),
        d = f([[], [], []]),
        p = f(),
        m = f(),
        g = h(() => {
          var e, a;
          const t = d.value,
            l = Me().locale(s.value).startOf("month");
          for (let r = 0; r < 3; r++) {
            const s = t[r];
            for (let t = 0; t < 4; t++) {
              const o =
                s[t] ||
                (s[t] = {
                  row: r,
                  column: t,
                  type: "normal",
                  inRange: !1,
                  start: !1,
                  end: !1,
                  text: -1,
                  disabled: !1,
                });
              o.type = "normal";
              const u = 4 * r + t,
                i = n.date.startOf("year").month(u),
                d =
                  n.rangeState.endDate ||
                  n.maxDate ||
                  (n.rangeState.selecting && n.minDate) ||
                  null;
              ((o.inRange =
                !!(
                  n.minDate &&
                  i.isSameOrAfter(n.minDate, "month") &&
                  d &&
                  i.isSameOrBefore(d, "month")
                ) ||
                !!(
                  n.minDate &&
                  i.isSameOrBefore(n.minDate, "month") &&
                  d &&
                  i.isSameOrAfter(d, "month")
                )),
                (null == (e = n.minDate) ? void 0 : e.isSameOrAfter(d))
                  ? ((o.start = !(!d || !i.isSame(d, "month"))),
                    (o.end = n.minDate && i.isSame(n.minDate, "month")))
                  : ((o.start = !(!n.minDate || !i.isSame(n.minDate, "month"))),
                    (o.end = !(!d || !i.isSame(d, "month")))));
              (l.isSame(i) && (o.type = "today"),
                (o.text = u),
                (o.disabled =
                  (null == (a = n.disabledDate)
                    ? void 0
                    : a.call(n, i.toDate())) || !1));
            }
          }
          return t;
        }),
        k = (e) => {
          const a = {},
            t = n.date.year(),
            l = new Date(),
            r = e.text;
          return (
            (a.disabled =
              !!n.disabledDate &&
              ((e, a, t) => {
                const n = Me().locale(t).startOf("month").month(a).year(e),
                  l = n.daysInMonth();
                return Ve(l).map((e) => n.add(e, "day").toDate());
              })(t, r, s.value).every(n.disabledDate)),
            (a.current =
              we(n.parsedValue).findIndex(
                (e) => Me.isDayjs(e) && e.year() === t && e.month() === r,
              ) >= 0),
            (a.today = l.getFullYear() === t && l.getMonth() === r),
            e.inRange &&
              ((a["in-range"] = !0),
              e.start && (a["start-date"] = !0),
              e.end && (a["end-date"] = !0)),
            a
          );
        },
        w = (e) => {
          const a = n.date.year(),
            t = e.text;
          return (
            we(n.date).findIndex((e) => e.year() === a && e.month() === t) >= 0
          );
        },
        D = (e) => {
          var a;
          if (!n.rangeState.selecting) return;
          let l = e.target;
          if (
            ("A" === l.tagName &&
              (l = null == (a = l.parentNode) ? void 0 : a.parentNode),
            "DIV" === l.tagName && (l = l.parentNode),
            "TD" !== l.tagName)
          )
            return;
          const r = l.parentNode.rowIndex,
            s = l.cellIndex;
          g.value[r][s].disabled ||
            (r === p.value && s === m.value) ||
            ((p.value = r),
            (m.value = s),
            t("changerange", {
              selecting: !0,
              endDate: n.date.startOf("year").month(4 * r + s),
            }));
        },
        S = (e) => {
          var a;
          const l = null == (a = e.target) ? void 0 : a.closest("td");
          if ("TD" !== (null == l ? void 0 : l.tagName)) return;
          if (ne(l, "disabled")) return;
          const r = l.cellIndex,
            s = 4 * l.parentNode.rowIndex + r,
            o = n.date.startOf("year").month(s);
          "range" === n.selectionMode
            ? n.rangeState.selecting
              ? (n.minDate && o >= n.minDate
                  ? t("pick", { minDate: n.minDate, maxDate: o })
                  : t("pick", { minDate: o, maxDate: n.minDate }),
                t("select", !1))
              : (t("pick", { minDate: o, maxDate: null }), t("select", !0))
            : t("pick", s);
        };
      return (
        y(
          () => n.date,
          async () => {
            var e, a;
            (null == (e = o.value)
              ? void 0
              : e.contains(document.activeElement)) &&
              (await b(), null == (a = u.value) || a.focus());
          },
        ),
        a({
          focus: () => {
            var e;
            null == (e = u.value) || e.focus();
          },
        }),
        (e, a) => (
          $(),
          T(
            "table",
            {
              role: "grid",
              "aria-label": M(r)("el.datepicker.monthTablePrompt"),
              class: O(M(l).b()),
              onClick: S,
              onMousemove: D,
            },
            [
              N(
                "tbody",
                { ref_key: "tbodyRef", ref: o },
                [
                  ($(!0),
                  T(
                    j,
                    null,
                    K(
                      M(g),
                      (e, a) => (
                        $(),
                        T("tr", { key: a }, [
                          ($(!0),
                          T(
                            j,
                            null,
                            K(
                              e,
                              (e, a) => (
                                $(),
                                T(
                                  "td",
                                  {
                                    key: a,
                                    ref_for: !0,
                                    ref: (a) => w(e) && (u.value = a),
                                    class: O(k(e)),
                                    "aria-selected": `${w(e)}`,
                                    "aria-label": M(r)(
                                      "el.datepicker.month" + (+e.text + 1),
                                    ),
                                    tabindex: w(e) ? 0 : -1,
                                    onKeydown: [
                                      te(V(S, ["prevent", "stop"]), ["space"]),
                                      te(V(S, ["prevent", "stop"]), ["enter"]),
                                    ],
                                  },
                                  [
                                    N("div", null, [
                                      N(
                                        "span",
                                        ja,
                                        R(
                                          M(r)(
                                            "el.datepicker.months." +
                                              i.value[e.text],
                                          ),
                                        ),
                                        1,
                                      ),
                                    ]),
                                  ],
                                  42,
                                  za,
                                )
                              ),
                            ),
                            128,
                          )),
                        ])
                      ),
                    ),
                    128,
                  )),
                ],
                512,
              ),
            ],
            42,
            Ha,
          )
        )
      );
    },
  });
var Ua = F(Ka, [
  [
    "__file",
    "/home/runner/work/element-plus/element-plus/packages/components/date-picker/src/date-picker-com/basic-month-table.vue",
  ],
]);
const { date: Za, disabledDate: qa, parsedValue: Ga } = Ca,
  Xa = r({ date: Za, disabledDate: qa, parsedValue: Ga }),
  Ja = ["aria-label"],
  Qa = ["aria-selected", "tabindex", "onKeydown"],
  et = { class: "cell" },
  at = { key: 1 },
  tt = i({
    __name: "basic-year-table",
    props: Xa,
    emits: ["pick"],
    setup(e, { expose: a, emit: t }) {
      const n = e,
        l = v("year-table"),
        { t: r, lang: s } = c(),
        o = f(),
        u = f(),
        i = h(() => 10 * Math.floor(n.date.year() / 10)),
        d = (e) => {
          const a = {},
            t = Me().locale(s.value);
          return (
            (a.disabled =
              !!n.disabledDate &&
              ((e, a) => {
                const t = Me(String(e)).locale(a).startOf("year"),
                  n = t.endOf("year").dayOfYear();
                return Ve(n).map((e) => t.add(e, "day").toDate());
              })(e, s.value).every(n.disabledDate)),
            (a.current =
              we(n.parsedValue).findIndex((a) => a.year() === e) >= 0),
            (a.today = t.year() === e),
            a
          );
        },
        p = (e) =>
          (e === i.value &&
            n.date.year() < i.value &&
            n.date.year() > i.value + 9) ||
          we(n.date).findIndex((a) => a.year() === e) >= 0,
        m = (e) => {
          const a = e.target.closest("td");
          if (a && a.textContent) {
            if (ne(a, "disabled")) return;
            const e = a.textContent || a.innerText;
            t("pick", Number(e));
          }
        };
      return (
        y(
          () => n.date,
          async () => {
            var e, a;
            (null == (e = o.value)
              ? void 0
              : e.contains(document.activeElement)) &&
              (await b(), null == (a = u.value) || a.focus());
          },
        ),
        a({
          focus: () => {
            var e;
            null == (e = u.value) || e.focus();
          },
        }),
        (e, a) => (
          $(),
          T(
            "table",
            {
              role: "grid",
              "aria-label": M(r)("el.datepicker.yearTablePrompt"),
              class: O(M(l).b()),
              onClick: m,
            },
            [
              N(
                "tbody",
                { ref_key: "tbodyRef", ref: o },
                [
                  ($(),
                  T(
                    j,
                    null,
                    K(3, (e, a) =>
                      N("tr", { key: a }, [
                        ($(),
                        T(
                          j,
                          null,
                          K(
                            4,
                            (e, t) => (
                              $(),
                              T(
                                j,
                                { key: a + "_" + t },
                                [
                                  4 * a + t < 10
                                    ? ($(),
                                      T(
                                        "td",
                                        {
                                          key: 0,
                                          ref_for: !0,
                                          ref: (e) =>
                                            p(M(i) + 4 * a + t) &&
                                            (u.value = e),
                                          class: O([
                                            "available",
                                            d(M(i) + 4 * a + t),
                                          ]),
                                          "aria-selected": `${p(M(i) + 4 * a + t)}`,
                                          tabindex: p(M(i) + 4 * a + t)
                                            ? 0
                                            : -1,
                                          onKeydown: [
                                            te(V(m, ["prevent", "stop"]), [
                                              "space",
                                            ]),
                                            te(V(m, ["prevent", "stop"]), [
                                              "enter",
                                            ]),
                                          ],
                                        },
                                        [N("span", et, R(M(i) + 4 * a + t), 1)],
                                        42,
                                        Qa,
                                      ))
                                    : ($(), T("td", at)),
                                ],
                                64,
                              )
                            ),
                          ),
                          64,
                        )),
                      ]),
                    ),
                    64,
                  )),
                ],
                512,
              ),
            ],
            10,
            Ja,
          )
        )
      );
    },
  });
var nt = F(tt, [
  [
    "__file",
    "/home/runner/work/element-plus/element-plus/packages/components/date-picker/src/date-picker-com/basic-year-table.vue",
  ],
]);
const lt = ["onClick"],
  rt = ["aria-label"],
  st = ["aria-label"],
  ot = ["aria-label"],
  ut = ["aria-label"],
  it = i({
    __name: "panel-date-pick",
    props: Va,
    emits: ["pick", "set-picker-option", "panel-change"],
    setup(e, { emit: a }) {
      const t = e,
        n = v("picker-panel"),
        r = v("date-picker"),
        s = d(),
        o = le(),
        { t: u, lang: i } = c(),
        p = m("EP_PICKER_BASE"),
        g = m(he),
        {
          shortcuts: k,
          disabledDate: w,
          cellClassName: D,
          defaultTime: S,
          arrowControl: x,
        } = p.props,
        P = re(p.props, "defaultValue"),
        V = f(),
        A = f(Me().locale(i.value)),
        E = f(!1),
        F = h(() => Me(S).locale(i.value)),
        H = h(() => A.value.month()),
        z = h(() => A.value.year()),
        Z = f([]),
        X = f(null),
        J = f(null),
        Q = (e) => !(Z.value.length > 0) || (Z.value, t.format, !0),
        ee = (e) =>
          !S || Ne.value || E.value
            ? $e.value
              ? e.millisecond(0)
              : e.startOf("day")
            : F.value.year(e.year()).month(e.month()).date(e.date()),
        ae = (e, ...t) => {
          if (e)
            if (l(e)) {
              const n = e.map(ee);
              a("pick", n, ...t);
            } else a("pick", ee(e), ...t);
          else a("pick", e, ...t);
          ((X.value = null), (J.value = null), (E.value = !1));
        },
        ne = (e, a) => {
          if ("date" === ge.value) {
            let n = t.parsedValue
              ? t.parsedValue.year(e.year()).month(e.month()).date(e.date())
              : e;
            (Q() ||
              (n = Z.value[0][0]
                .year(e.year())
                .month(e.month())
                .date(e.date())),
              (A.value = n),
              ae(n, $e.value || a));
          } else
            "week" === ge.value
              ? ae(e.date)
              : "dates" === ge.value && ae(e, !0);
        },
        ve = (e) => {
          const a = e ? "add" : "subtract";
          ((A.value = A.value[a](1, "month")), qe("month"));
        },
        pe = (e) => {
          const a = A.value,
            t = e ? "add" : "subtract";
          ((A.value = "year" === fe.value ? a[t](10, "year") : a[t](1, "year")),
            qe("year"));
        },
        fe = f("date"),
        ye = h(() => {
          const e = u("el.datepicker.year");
          if ("year" === fe.value) {
            const a = 10 * Math.floor(z.value / 10);
            return e ? `${a} ${e} - ${a + 9} ${e}` : `${a} - ${a + 9}`;
          }
          return `${z.value} ${e}`;
        }),
        ge = h(() => {
          const { type: e } = t;
          return ["week", "month", "year", "dates"].includes(e) ? e : "date";
        }),
        ke = h(() => ("date" === ge.value ? fe.value : ge.value)),
        we = h(() => !!k.length),
        De = async (e) => {
          ((A.value = A.value.startOf("month").month(e)),
            "month" === ge.value
              ? ae(A.value, !1)
              : ((fe.value = "date"),
                ["month", "year", "date", "week"].includes(ge.value) &&
                  (ae(A.value, !0), await b(), Ke())),
            qe("month"));
        },
        Se = async (e) => {
          ("year" === ge.value
            ? ((A.value = A.value.startOf("year").year(e)), ae(A.value, !1))
            : ((A.value = A.value.year(e)),
              (fe.value = "month"),
              ["month", "year", "date", "week"].includes(ge.value) &&
                (ae(A.value, !0), await b(), Ke())),
            qe("year"));
        },
        xe = async (e) => {
          ((fe.value = e), await b(), Ke());
        },
        $e = h(() => "datetime" === t.type || "datetimerange" === t.type),
        Ce = h(() => $e.value || "dates" === ge.value),
        _e = h(
          () =>
            !!w &&
            (!t.parsedValue ||
              (l(t.parsedValue)
                ? w(t.parsedValue[0].toDate())
                : w(t.parsedValue.toDate()))),
        ),
        Oe = () => {
          if ("dates" === ge.value) ae(t.parsedValue);
          else {
            let e = t.parsedValue;
            if (!e) {
              const a = Me(S).locale(i.value),
                t = je();
              e = a.year(t.year()).month(t.month()).date(t.date());
            }
            ((A.value = e), ae(e));
          }
        },
        Pe = h(() => !!w && w(Me().locale(i.value).toDate())),
        Ve = () => {
          const e = Me().locale(i.value).toDate();
          ((E.value = !0),
            (w && w(e)) ||
              !Q() ||
              ((A.value = Me().locale(i.value)), ae(A.value)));
        },
        Ie = h(() => Ae(t.format)),
        Te = h(() => Ye(t.format)),
        Ne = h(() =>
          J.value
            ? J.value
            : t.parsedValue || P.value
              ? (t.parsedValue || A.value).format(Ie.value)
              : void 0,
        ),
        Le = h(() =>
          X.value
            ? X.value
            : t.parsedValue || P.value
              ? (t.parsedValue || A.value).format(Te.value)
              : void 0,
        ),
        Re = f(!1),
        Ee = () => {
          Re.value = !0;
        },
        Fe = () => {
          Re.value = !1;
        },
        Be = (e) => ({
          hour: e.hour(),
          minute: e.minute(),
          second: e.second(),
          year: e.year(),
          month: e.month(),
          date: e.date(),
        }),
        We = (e, a, n) => {
          const { hour: l, minute: r, second: s } = Be(e),
            o = t.parsedValue ? t.parsedValue.hour(l).minute(r).second(s) : e;
          ((A.value = o), ae(A.value, !0), n || (Re.value = a));
        },
        He = (e) => {
          const a = Me(e, Ie.value).locale(i.value);
          if (a.isValid() && Q()) {
            const { year: e, month: t, date: n } = Be(A.value);
            ((A.value = a.year(e).month(t).date(n)),
              (J.value = null),
              (Re.value = !1),
              ae(A.value, !0));
          }
        },
        ze = (e) => {
          const a = Me(e, Te.value).locale(i.value);
          if (a.isValid()) {
            if (w && w(a.toDate())) return;
            const { hour: e, minute: t, second: n } = Be(A.value);
            ((A.value = a.hour(e).minute(t).second(n)),
              (X.value = null),
              ae(A.value, !0));
          }
        },
        je = () => {
          const e = Me(P.value).locale(i.value);
          if (!P.value) {
            const e = F.value;
            return Me()
              .hour(e.hour())
              .minute(e.minute())
              .second(e.second())
              .locale(i.value);
          }
          return e;
        },
        Ke = async () => {
          var e;
          ["week", "month", "year", "date"].includes(ge.value) &&
            (null == (e = V.value) || e.focus(),
            "week" === ge.value && Ze(B.down));
        },
        Ue = (e) => {
          const { code: a } = e;
          ([
            B.up,
            B.down,
            B.left,
            B.right,
            B.home,
            B.end,
            B.pageUp,
            B.pageDown,
          ].includes(a) && (Ze(a), e.stopPropagation(), e.preventDefault()),
            [B.enter, B.space, B.numpadEnter].includes(a) &&
              null === X.value &&
              null === J.value &&
              (e.preventDefault(), ae(A.value, !1)));
        },
        Ze = (e) => {
          var t;
          const {
              up: n,
              down: l,
              left: r,
              right: s,
              home: o,
              end: u,
              pageUp: d,
              pageDown: c,
            } = B,
            v = {
              year: {
                [n]: -4,
                [l]: 4,
                [r]: -1,
                [s]: 1,
                offset: (e, a) => e.setFullYear(e.getFullYear() + a),
              },
              month: {
                [n]: -4,
                [l]: 4,
                [r]: -1,
                [s]: 1,
                offset: (e, a) => e.setMonth(e.getMonth() + a),
              },
              week: {
                [n]: -1,
                [l]: 1,
                [r]: -1,
                [s]: 1,
                offset: (e, a) => e.setDate(e.getDate() + 7 * a),
              },
              date: {
                [n]: -7,
                [l]: 7,
                [r]: -1,
                [s]: 1,
                [o]: (e) => -e.getDay(),
                [u]: (e) => 6 - e.getDay(),
                [d]: (e) =>
                  -new Date(e.getFullYear(), e.getMonth(), 0).getDate(),
                [c]: (e) =>
                  new Date(e.getFullYear(), e.getMonth() + 1, 0).getDate(),
                offset: (e, a) => e.setDate(e.getDate() + a),
              },
            },
            p = A.value.toDate();
          for (; Math.abs(A.value.diff(p, "year", !0)) < 1; ) {
            const n = v[ke.value];
            if (!n) return;
            if (
              (n.offset(p, W(n[e]) ? n[e](p) : null != (t = n[e]) ? t : 0),
              w && w(p))
            )
              break;
            const l = Me(p).locale(i.value);
            ((A.value = l), a("pick", l, !0));
            break;
          }
        },
        qe = (e) => {
          a("panel-change", A.value.toDate(), e, fe.value);
        };
      return (
        y(
          () => ge.value,
          (e) => {
            ["month", "year"].includes(e)
              ? (fe.value = e)
              : (fe.value = "date");
          },
          { immediate: !0 },
        ),
        y(
          () => fe.value,
          () => {
            null == g || g.updatePopper();
          },
        ),
        y(
          () => P.value,
          (e) => {
            e && (A.value = je());
          },
          { immediate: !0 },
        ),
        y(
          () => t.parsedValue,
          (e) => {
            if (e) {
              if ("dates" === ge.value) return;
              if (Array.isArray(e)) return;
              A.value = e;
            } else A.value = je();
          },
          { immediate: !0 },
        ),
        a("set-picker-option", [
          "isValidValue",
          (e) => Me.isDayjs(e) && e.isValid() && (!w || !w(e.toDate())),
        ]),
        a("set-picker-option", [
          "formatToString",
          (e) =>
            "dates" === ge.value
              ? e.map((e) => e.format(t.format))
              : e.format(t.format),
        ]),
        a("set-picker-option", [
          "parseUserInput",
          (e) => Me(e, t.format).locale(i.value),
        ]),
        a("set-picker-option", ["handleFocusPicker", Ke]),
        (e, t) => (
          $(),
          T(
            "div",
            {
              class: O([
                M(n).b(),
                M(r).b(),
                { "has-sidebar": e.$slots.sidebar || M(we), "has-time": M($e) },
              ]),
            },
            [
              N(
                "div",
                { class: O(M(n).e("body-wrapper")) },
                [
                  L(e.$slots, "sidebar", { class: O(M(n).e("sidebar")) }),
                  M(we)
                    ? ($(),
                      T(
                        "div",
                        { key: 0, class: O(M(n).e("sidebar")) },
                        [
                          ($(!0),
                          T(
                            j,
                            null,
                            K(
                              M(k),
                              (e, t) => (
                                $(),
                                T(
                                  "button",
                                  {
                                    key: t,
                                    type: "button",
                                    class: O(M(n).e("shortcut")),
                                    onClick: (t) =>
                                      ((e) => {
                                        const t = W(e.value)
                                          ? e.value()
                                          : e.value;
                                        t
                                          ? ae(Me(t).locale(i.value))
                                          : e.onClick &&
                                            e.onClick({
                                              attrs: s,
                                              slots: o,
                                              emit: a,
                                            });
                                      })(e),
                                  },
                                  R(e.text),
                                  11,
                                  lt,
                                )
                              ),
                            ),
                            128,
                          )),
                        ],
                        2,
                      ))
                    : I("v-if", !0),
                  N(
                    "div",
                    { class: O(M(n).e("body")) },
                    [
                      M($e)
                        ? ($(),
                          T(
                            "div",
                            { key: 0, class: O(M(r).e("time-header")) },
                            [
                              N(
                                "span",
                                { class: O(M(r).e("editor-wrap")) },
                                [
                                  G(
                                    M(me),
                                    {
                                      placeholder: M(u)(
                                        "el.datepicker.selectDate",
                                      ),
                                      "model-value": M(Le),
                                      size: "small",
                                      "validate-event": !1,
                                      onInput:
                                        t[0] || (t[0] = (e) => (X.value = e)),
                                      onChange: ze,
                                    },
                                    null,
                                    8,
                                    ["placeholder", "model-value"],
                                  ),
                                ],
                                2,
                              ),
                              q(
                                ($(),
                                T(
                                  "span",
                                  { class: O(M(r).e("editor-wrap")) },
                                  [
                                    G(
                                      M(me),
                                      {
                                        placeholder: M(u)(
                                          "el.datepicker.selectTime",
                                        ),
                                        "model-value": M(Ne),
                                        size: "small",
                                        "validate-event": !1,
                                        onFocus: Ee,
                                        onInput:
                                          t[1] || (t[1] = (e) => (J.value = e)),
                                        onChange: He,
                                      },
                                      null,
                                      8,
                                      ["placeholder", "model-value"],
                                    ),
                                    G(
                                      M(oa),
                                      {
                                        visible: Re.value,
                                        format: M(Ie),
                                        "time-arrow-control": M(x),
                                        "parsed-value": A.value,
                                        onPick: We,
                                      },
                                      null,
                                      8,
                                      [
                                        "visible",
                                        "format",
                                        "time-arrow-control",
                                        "parsed-value",
                                      ],
                                    ),
                                  ],
                                  2,
                                )),
                                [[M(be), Fe]],
                              ),
                            ],
                            2,
                          ))
                        : I("v-if", !0),
                      q(
                        N(
                          "div",
                          {
                            class: O([
                              M(r).e("header"),
                              ("year" === fe.value || "month" === fe.value) &&
                                M(r).e("header--bordered"),
                            ]),
                          },
                          [
                            N(
                              "span",
                              { class: O(M(r).e("prev-btn")) },
                              [
                                N(
                                  "button",
                                  {
                                    type: "button",
                                    "aria-label": M(u)(
                                      "el.datepicker.prevYear",
                                    ),
                                    class: O([
                                      "d-arrow-left",
                                      M(n).e("icon-btn"),
                                    ]),
                                    onClick: t[2] || (t[2] = (e) => pe(!1)),
                                  },
                                  [
                                    G(M(Y), null, {
                                      default: _(() => [G(M(oe))]),
                                      _: 1,
                                    }),
                                  ],
                                  10,
                                  rt,
                                ),
                                q(
                                  N(
                                    "button",
                                    {
                                      type: "button",
                                      "aria-label": M(u)(
                                        "el.datepicker.prevMonth",
                                      ),
                                      class: O([
                                        M(n).e("icon-btn"),
                                        "arrow-left",
                                      ]),
                                      onClick: t[3] || (t[3] = (e) => ve(!1)),
                                    },
                                    [
                                      G(M(Y), null, {
                                        default: _(() => [G(M(ue))]),
                                        _: 1,
                                      }),
                                    ],
                                    10,
                                    st,
                                  ),
                                  [[se, "date" === fe.value]],
                                ),
                              ],
                              2,
                            ),
                            N(
                              "span",
                              {
                                role: "button",
                                class: O(M(r).e("header-label")),
                                "aria-live": "polite",
                                tabindex: "0",
                                onKeydown:
                                  t[4] ||
                                  (t[4] = te((e) => xe("year"), ["enter"])),
                                onClick: t[5] || (t[5] = (e) => xe("year")),
                              },
                              R(M(ye)),
                              35,
                            ),
                            q(
                              N(
                                "span",
                                {
                                  role: "button",
                                  "aria-live": "polite",
                                  tabindex: "0",
                                  class: O([
                                    M(r).e("header-label"),
                                    { active: "month" === fe.value },
                                  ]),
                                  onKeydown:
                                    t[6] ||
                                    (t[6] = te((e) => xe("month"), ["enter"])),
                                  onClick: t[7] || (t[7] = (e) => xe("month")),
                                },
                                R(M(u)(`el.datepicker.month${M(H) + 1}`)),
                                35,
                              ),
                              [[se, "date" === fe.value]],
                            ),
                            N(
                              "span",
                              { class: O(M(r).e("next-btn")) },
                              [
                                q(
                                  N(
                                    "button",
                                    {
                                      type: "button",
                                      "aria-label": M(u)(
                                        "el.datepicker.nextMonth",
                                      ),
                                      class: O([
                                        M(n).e("icon-btn"),
                                        "arrow-right",
                                      ]),
                                      onClick: t[8] || (t[8] = (e) => ve(!0)),
                                    },
                                    [
                                      G(M(Y), null, {
                                        default: _(() => [G(M(ie))]),
                                        _: 1,
                                      }),
                                    ],
                                    10,
                                    ot,
                                  ),
                                  [[se, "date" === fe.value]],
                                ),
                                N(
                                  "button",
                                  {
                                    type: "button",
                                    "aria-label": M(u)(
                                      "el.datepicker.nextYear",
                                    ),
                                    class: O([
                                      M(n).e("icon-btn"),
                                      "d-arrow-right",
                                    ]),
                                    onClick: t[9] || (t[9] = (e) => pe(!0)),
                                  },
                                  [
                                    G(M(Y), null, {
                                      default: _(() => [G(M(de))]),
                                      _: 1,
                                    }),
                                  ],
                                  10,
                                  ut,
                                ),
                              ],
                              2,
                            ),
                          ],
                          2,
                        ),
                        [[se, "time" !== fe.value]],
                      ),
                      N(
                        "div",
                        { class: O(M(n).e("content")), onKeydown: Ue },
                        [
                          "date" === fe.value
                            ? ($(),
                              C(
                                Ba,
                                {
                                  key: 0,
                                  ref_key: "currentViewRef",
                                  ref: V,
                                  "selection-mode": M(ge),
                                  date: A.value,
                                  "parsed-value": e.parsedValue,
                                  "disabled-date": M(w),
                                  "cell-class-name": M(D),
                                  onPick: ne,
                                },
                                null,
                                8,
                                [
                                  "selection-mode",
                                  "date",
                                  "parsed-value",
                                  "disabled-date",
                                  "cell-class-name",
                                ],
                              ))
                            : I("v-if", !0),
                          "year" === fe.value
                            ? ($(),
                              C(
                                nt,
                                {
                                  key: 1,
                                  ref_key: "currentViewRef",
                                  ref: V,
                                  date: A.value,
                                  "disabled-date": M(w),
                                  "parsed-value": e.parsedValue,
                                  onPick: Se,
                                },
                                null,
                                8,
                                ["date", "disabled-date", "parsed-value"],
                              ))
                            : I("v-if", !0),
                          "month" === fe.value
                            ? ($(),
                              C(
                                Ua,
                                {
                                  key: 2,
                                  ref_key: "currentViewRef",
                                  ref: V,
                                  date: A.value,
                                  "parsed-value": e.parsedValue,
                                  "disabled-date": M(w),
                                  onPick: De,
                                },
                                null,
                                8,
                                ["date", "parsed-value", "disabled-date"],
                              ))
                            : I("v-if", !0),
                        ],
                        34,
                      ),
                    ],
                    2,
                  ),
                ],
                2,
              ),
              q(
                N(
                  "div",
                  { class: O(M(n).e("footer")) },
                  [
                    q(
                      G(
                        M(ce),
                        {
                          text: "",
                          size: "small",
                          class: O(M(n).e("link-btn")),
                          disabled: M(Pe),
                          onClick: Ve,
                        },
                        {
                          default: _(() => [
                            U(R(M(u)("el.datepicker.now")), 1),
                          ]),
                          _: 1,
                        },
                        8,
                        ["class", "disabled"],
                      ),
                      [[se, "dates" !== M(ge)]],
                    ),
                    G(
                      M(ce),
                      {
                        plain: "",
                        size: "small",
                        class: O(M(n).e("link-btn")),
                        disabled: M(_e),
                        onClick: Oe,
                      },
                      {
                        default: _(() => [
                          U(R(M(u)("el.datepicker.confirm")), 1),
                        ]),
                        _: 1,
                      },
                      8,
                      ["class", "disabled"],
                    ),
                  ],
                  2,
                ),
                [[se, M(Ce) && "date" === fe.value]],
              ),
            ],
            2,
          )
        )
      );
    },
  });
var dt = F(it, [
  [
    "__file",
    "/home/runner/work/element-plus/element-plus/packages/components/date-picker/src/date-picker-com/panel-date-pick.vue",
  ],
]);
const ct = r({ ..._a, ...Oa }),
  vt = (
    e,
    {
      defaultValue: a,
      leftDate: t,
      rightDate: n,
      unit: r,
      onParsedValueChanged: s,
    },
  ) => {
    const { emit: o } = ve(),
      { pickerNs: u } = m(Sa),
      i = v("date-range-picker"),
      { t: p, lang: h } = c(),
      b = ((e) => {
        const { emit: a } = ve(),
          t = d(),
          n = le();
        return (l) => {
          const r = W(l.value) ? l.value() : l.value;
          r
            ? a("pick", [Me(r[0]).locale(e.value), Me(r[1]).locale(e.value)])
            : l.onClick && l.onClick({ attrs: t, slots: n, emit: a });
        };
      })(h),
      g = f(),
      k = f(),
      w = f({ endDate: null, selecting: !1 }),
      D = () => {
        const [l, s] = Ia(M(a), {
          lang: M(h),
          unit: r,
          unlinkPanels: e.unlinkPanels,
        });
        ((g.value = void 0), (k.value = void 0), (t.value = l), (n.value = s));
      };
    return (
      y(
        a,
        (e) => {
          e && D();
        },
        { immediate: !0 },
      ),
      y(
        () => e.parsedValue,
        (e) => {
          if (l(e) && 2 === e.length) {
            const [a, n] = e;
            ((g.value = a), (t.value = a), (k.value = n), s(M(g), M(k)));
          } else D();
        },
        { immediate: !0 },
      ),
      {
        minDate: g,
        maxDate: k,
        rangeState: w,
        lang: h,
        ppNs: u,
        drpNs: i,
        handleChangeRange: (e) => {
          w.value = e;
        },
        handleRangeConfirm: (e = !1) => {
          const a = M(g),
            t = M(k);
          Aa([a, t]) && o("pick", [a, t], e);
        },
        handleShortcutClick: b,
        onSelect: (e) => {
          ((w.value.selecting = e), e || (w.value.endDate = null));
        },
        t: p,
      }
    );
  },
  pt = ["onClick"],
  mt = ["disabled"],
  ft = ["disabled"],
  ht = ["disabled"],
  yt = ["disabled"],
  bt = "month",
  gt = i({
    __name: "panel-date-range",
    props: ct,
    emits: ["pick", "set-picker-option", "calendar-change", "panel-change"],
    setup(e, { emit: a }) {
      const t = e,
        n = m("EP_PICKER_BASE"),
        {
          disabledDate: r,
          cellClassName: s,
          format: o,
          defaultTime: u,
          arrowControl: i,
          clearable: d,
        } = n.props,
        v = re(n.props, "shortcuts"),
        p = re(n.props, "defaultValue"),
        { lang: y } = c(),
        b = f(Me().locale(y.value)),
        g = f(Me().locale(y.value).add(1, bt)),
        {
          minDate: k,
          maxDate: w,
          rangeState: D,
          ppNs: S,
          drpNs: x,
          handleChangeRange: P,
          handleRangeConfirm: V,
          handleShortcutClick: A,
          onSelect: E,
          t: F,
        } = vt(t, {
          defaultValue: p,
          leftDate: b,
          rightDate: g,
          unit: bt,
          onParsedValueChanged: function (e, a) {
            if (t.unlinkPanels && a) {
              const t = (null == e ? void 0 : e.year()) || 0,
                n = (null == e ? void 0 : e.month()) || 0,
                l = a.year(),
                r = a.month();
              g.value = t === l && n === r ? a.add(1, bt) : a;
            } else
              ((g.value = b.value.add(1, bt)),
                a &&
                  (g.value = g.value
                    .hour(a.hour())
                    .minute(a.minute())
                    .second(a.second())));
          },
        }),
        B = f({ min: null, max: null }),
        W = f({ min: null, max: null }),
        H = h(
          () =>
            `${b.value.year()} ${F("el.datepicker.year")} ${F(`el.datepicker.month${b.value.month() + 1}`)}`,
        ),
        z = h(
          () =>
            `${g.value.year()} ${F("el.datepicker.year")} ${F(`el.datepicker.month${g.value.month() + 1}`)}`,
        ),
        Z = h(() => b.value.year()),
        X = h(() => b.value.month()),
        J = h(() => g.value.year()),
        Q = h(() => g.value.month()),
        ee = h(() => !!v.value.length),
        ae = h(() =>
          null !== B.value.min
            ? B.value.min
            : k.value
              ? k.value.format(ve.value)
              : "",
        ),
        te = h(() =>
          null !== B.value.max
            ? B.value.max
            : w.value || k.value
              ? (w.value || k.value).format(ve.value)
              : "",
        ),
        ne = h(() =>
          null !== W.value.min
            ? W.value.min
            : k.value
              ? k.value.format(se.value)
              : "",
        ),
        le = h(() =>
          null !== W.value.max
            ? W.value.max
            : w.value || k.value
              ? (w.value || k.value).format(se.value)
              : "",
        ),
        se = h(() => Ae(o)),
        ve = h(() => Ye(o)),
        pe = () => {
          ((b.value = b.value.subtract(1, "year")),
            t.unlinkPanels || (g.value = b.value.add(1, "month")),
            Se("year"));
        },
        fe = () => {
          ((b.value = b.value.subtract(1, "month")),
            t.unlinkPanels || (g.value = b.value.add(1, "month")),
            Se("month"));
        },
        he = () => {
          (t.unlinkPanels
            ? (g.value = g.value.add(1, "year"))
            : ((b.value = b.value.add(1, "year")),
              (g.value = b.value.add(1, "month"))),
            Se("year"));
        },
        ye = () => {
          (t.unlinkPanels
            ? (g.value = g.value.add(1, "month"))
            : ((b.value = b.value.add(1, "month")),
              (g.value = b.value.add(1, "month"))),
            Se("month"));
        },
        ge = () => {
          ((b.value = b.value.add(1, "year")), Se("year"));
        },
        ke = () => {
          ((b.value = b.value.add(1, "month")), Se("month"));
        },
        we = () => {
          ((g.value = g.value.subtract(1, "year")), Se("year"));
        },
        De = () => {
          ((g.value = g.value.subtract(1, "month")), Se("month"));
        },
        Se = (e) => {
          a("panel-change", [b.value.toDate(), g.value.toDate()], e);
        },
        xe = h(() => {
          const e = (X.value + 1) % 12,
            a = X.value + 1 >= 12 ? 1 : 0;
          return (
            t.unlinkPanels &&
            new Date(Z.value + a, e) < new Date(J.value, Q.value)
          );
        }),
        $e = h(
          () =>
            t.unlinkPanels &&
            12 * J.value + Q.value - (12 * Z.value + X.value + 1) >= 12,
        ),
        Ce = h(
          () =>
            !(
              k.value &&
              w.value &&
              !D.value.selecting &&
              Aa([k.value, w.value])
            ),
        ),
        _e = h(() => "datetime" === t.type || "datetimerange" === t.type),
        Oe = (e, a) => {
          if (e) {
            if (u) {
              return Me(u[a] || u)
                .locale(y.value)
                .year(e.year())
                .month(e.month())
                .date(e.date());
            }
            return e;
          }
        },
        Pe = (e, t = !0) => {
          const n = e.minDate,
            l = e.maxDate,
            r = Oe(n, 0),
            s = Oe(l, 1);
          (w.value === s && k.value === r) ||
            (a("calendar-change", [n.toDate(), l && l.toDate()]),
            (w.value = s),
            (k.value = r),
            t && !_e.value && V());
        },
        Ve = f(!1),
        Ie = f(!1),
        Te = () => {
          Ve.value = !1;
        },
        Ne = () => {
          Ie.value = !1;
        },
        Le = (e, a) => {
          B.value[a] = e;
          const n = Me(e, ve.value).locale(y.value);
          if (n.isValid()) {
            if (r && r(n.toDate())) return;
            "min" === a
              ? ((b.value = n),
                (k.value = (k.value || b.value)
                  .year(n.year())
                  .month(n.month())
                  .date(n.date())),
                t.unlinkPanels ||
                  (w.value && !w.value.isBefore(k.value)) ||
                  ((g.value = n.add(1, "month")),
                  (w.value = k.value.add(1, "month"))))
              : ((g.value = n),
                (w.value = (w.value || g.value)
                  .year(n.year())
                  .month(n.month())
                  .date(n.date())),
                t.unlinkPanels ||
                  (k.value && !k.value.isAfter(w.value)) ||
                  ((b.value = n.subtract(1, "month")),
                  (k.value = w.value.subtract(1, "month"))));
          }
        },
        Re = (e, a) => {
          B.value[a] = null;
        },
        Ee = (e, a) => {
          W.value[a] = e;
          const t = Me(e, se.value).locale(y.value);
          t.isValid() &&
            ("min" === a
              ? ((Ve.value = !0),
                (k.value = (k.value || b.value)
                  .hour(t.hour())
                  .minute(t.minute())
                  .second(t.second())),
                (w.value && !w.value.isBefore(k.value)) || (w.value = k.value))
              : ((Ie.value = !0),
                (w.value = (w.value || g.value)
                  .hour(t.hour())
                  .minute(t.minute())
                  .second(t.second())),
                (g.value = w.value),
                w.value && w.value.isBefore(k.value) && (k.value = w.value)));
        },
        Fe = (e, a) => {
          ((W.value[a] = null),
            "min" === a
              ? ((b.value = k.value), (Ve.value = !1))
              : ((g.value = w.value), (Ie.value = !1)));
        },
        Be = (e, a, t) => {
          W.value.min ||
            (e &&
              ((b.value = e),
              (k.value = (k.value || b.value)
                .hour(e.hour())
                .minute(e.minute())
                .second(e.second()))),
            t || (Ve.value = a),
            (w.value && !w.value.isBefore(k.value)) ||
              ((w.value = k.value), (g.value = e)));
        },
        We = (e, a, t) => {
          W.value.max ||
            (e &&
              ((g.value = e),
              (w.value = (w.value || g.value)
                .hour(e.hour())
                .minute(e.minute())
                .second(e.second()))),
            t || (Ie.value = a),
            w.value && w.value.isBefore(k.value) && (k.value = w.value));
        },
        He = () => {
          ((b.value = Ia(M(p), {
            lang: M(y),
            unit: "month",
            unlinkPanels: t.unlinkPanels,
          })[0]),
            (g.value = b.value.add(1, "month")),
            a("pick", null));
        };
      return (
        a("set-picker-option", ["isValidValue", Aa]),
        a("set-picker-option", [
          "parseUserInput",
          (e) =>
            l(e)
              ? e.map((e) => Me(e, o).locale(y.value))
              : Me(e, o).locale(y.value),
        ]),
        a("set-picker-option", [
          "formatToString",
          (e) => (l(e) ? e.map((e) => e.format(o)) : e.format(o)),
        ]),
        a("set-picker-option", ["handleClear", He]),
        (e, a) => (
          $(),
          T(
            "div",
            {
              class: O([
                M(S).b(),
                M(x).b(),
                { "has-sidebar": e.$slots.sidebar || M(ee), "has-time": M(_e) },
              ]),
            },
            [
              N(
                "div",
                { class: O(M(S).e("body-wrapper")) },
                [
                  L(e.$slots, "sidebar", { class: O(M(S).e("sidebar")) }),
                  M(ee)
                    ? ($(),
                      T(
                        "div",
                        { key: 0, class: O(M(S).e("sidebar")) },
                        [
                          ($(!0),
                          T(
                            j,
                            null,
                            K(
                              M(v),
                              (e, a) => (
                                $(),
                                T(
                                  "button",
                                  {
                                    key: a,
                                    type: "button",
                                    class: O(M(S).e("shortcut")),
                                    onClick: (a) => M(A)(e),
                                  },
                                  R(e.text),
                                  11,
                                  pt,
                                )
                              ),
                            ),
                            128,
                          )),
                        ],
                        2,
                      ))
                    : I("v-if", !0),
                  N(
                    "div",
                    { class: O(M(S).e("body")) },
                    [
                      M(_e)
                        ? ($(),
                          T(
                            "div",
                            { key: 0, class: O(M(x).e("time-header")) },
                            [
                              N(
                                "span",
                                { class: O(M(x).e("editors-wrap")) },
                                [
                                  N(
                                    "span",
                                    { class: O(M(x).e("time-picker-wrap")) },
                                    [
                                      G(
                                        M(me),
                                        {
                                          size: "small",
                                          disabled: M(D).selecting,
                                          placeholder: M(F)(
                                            "el.datepicker.startDate",
                                          ),
                                          class: O(M(x).e("editor")),
                                          "model-value": M(ae),
                                          "validate-event": !1,
                                          onInput:
                                            a[0] ||
                                            (a[0] = (e) => Le(e, "min")),
                                          onChange:
                                            a[1] ||
                                            (a[1] = (e) => Re(0, "min")),
                                        },
                                        null,
                                        8,
                                        [
                                          "disabled",
                                          "placeholder",
                                          "class",
                                          "model-value",
                                        ],
                                      ),
                                    ],
                                    2,
                                  ),
                                  q(
                                    ($(),
                                    T(
                                      "span",
                                      { class: O(M(x).e("time-picker-wrap")) },
                                      [
                                        G(
                                          M(me),
                                          {
                                            size: "small",
                                            class: O(M(x).e("editor")),
                                            disabled: M(D).selecting,
                                            placeholder: M(F)(
                                              "el.datepicker.startTime",
                                            ),
                                            "model-value": M(ne),
                                            "validate-event": !1,
                                            onFocus:
                                              a[2] ||
                                              (a[2] = (e) => (Ve.value = !0)),
                                            onInput:
                                              a[3] ||
                                              (a[3] = (e) => Ee(e, "min")),
                                            onChange:
                                              a[4] ||
                                              (a[4] = (e) => Fe(0, "min")),
                                          },
                                          null,
                                          8,
                                          [
                                            "class",
                                            "disabled",
                                            "placeholder",
                                            "model-value",
                                          ],
                                        ),
                                        G(
                                          M(oa),
                                          {
                                            visible: Ve.value,
                                            format: M(se),
                                            "datetime-role": "start",
                                            "time-arrow-control": M(i),
                                            "parsed-value": b.value,
                                            onPick: Be,
                                          },
                                          null,
                                          8,
                                          [
                                            "visible",
                                            "format",
                                            "time-arrow-control",
                                            "parsed-value",
                                          ],
                                        ),
                                      ],
                                      2,
                                    )),
                                    [[M(be), Te]],
                                  ),
                                ],
                                2,
                              ),
                              N("span", null, [
                                G(M(Y), null, {
                                  default: _(() => [G(M(ie))]),
                                  _: 1,
                                }),
                              ]),
                              N(
                                "span",
                                {
                                  class: O([
                                    M(x).e("editors-wrap"),
                                    "is-right",
                                  ]),
                                },
                                [
                                  N(
                                    "span",
                                    { class: O(M(x).e("time-picker-wrap")) },
                                    [
                                      G(
                                        M(me),
                                        {
                                          size: "small",
                                          class: O(M(x).e("editor")),
                                          disabled: M(D).selecting,
                                          placeholder: M(F)(
                                            "el.datepicker.endDate",
                                          ),
                                          "model-value": M(te),
                                          readonly: !M(k),
                                          "validate-event": !1,
                                          onInput:
                                            a[5] ||
                                            (a[5] = (e) => Le(e, "max")),
                                          onChange:
                                            a[6] ||
                                            (a[6] = (e) => Re(0, "max")),
                                        },
                                        null,
                                        8,
                                        [
                                          "class",
                                          "disabled",
                                          "placeholder",
                                          "model-value",
                                          "readonly",
                                        ],
                                      ),
                                    ],
                                    2,
                                  ),
                                  q(
                                    ($(),
                                    T(
                                      "span",
                                      { class: O(M(x).e("time-picker-wrap")) },
                                      [
                                        G(
                                          M(me),
                                          {
                                            size: "small",
                                            class: O(M(x).e("editor")),
                                            disabled: M(D).selecting,
                                            placeholder: M(F)(
                                              "el.datepicker.endTime",
                                            ),
                                            "model-value": M(le),
                                            readonly: !M(k),
                                            "validate-event": !1,
                                            onFocus:
                                              a[7] ||
                                              (a[7] = (e) =>
                                                M(k) && (Ie.value = !0)),
                                            onInput:
                                              a[8] ||
                                              (a[8] = (e) => Ee(e, "max")),
                                            onChange:
                                              a[9] ||
                                              (a[9] = (e) => Fe(0, "max")),
                                          },
                                          null,
                                          8,
                                          [
                                            "class",
                                            "disabled",
                                            "placeholder",
                                            "model-value",
                                            "readonly",
                                          ],
                                        ),
                                        G(
                                          M(oa),
                                          {
                                            "datetime-role": "end",
                                            visible: Ie.value,
                                            format: M(se),
                                            "time-arrow-control": M(i),
                                            "parsed-value": g.value,
                                            onPick: We,
                                          },
                                          null,
                                          8,
                                          [
                                            "visible",
                                            "format",
                                            "time-arrow-control",
                                            "parsed-value",
                                          ],
                                        ),
                                      ],
                                      2,
                                    )),
                                    [[M(be), Ne]],
                                  ),
                                ],
                                2,
                              ),
                            ],
                            2,
                          ))
                        : I("v-if", !0),
                      N(
                        "div",
                        {
                          class: O([
                            [M(S).e("content"), M(x).e("content")],
                            "is-left",
                          ]),
                        },
                        [
                          N(
                            "div",
                            { class: O(M(x).e("header")) },
                            [
                              N(
                                "button",
                                {
                                  type: "button",
                                  class: O([
                                    M(S).e("icon-btn"),
                                    "d-arrow-left",
                                  ]),
                                  onClick: pe,
                                },
                                [
                                  G(M(Y), null, {
                                    default: _(() => [G(M(oe))]),
                                    _: 1,
                                  }),
                                ],
                                2,
                              ),
                              N(
                                "button",
                                {
                                  type: "button",
                                  class: O([M(S).e("icon-btn"), "arrow-left"]),
                                  onClick: fe,
                                },
                                [
                                  G(M(Y), null, {
                                    default: _(() => [G(M(ue))]),
                                    _: 1,
                                  }),
                                ],
                                2,
                              ),
                              e.unlinkPanels
                                ? ($(),
                                  T(
                                    "button",
                                    {
                                      key: 0,
                                      type: "button",
                                      disabled: !M($e),
                                      class: O([
                                        [
                                          M(S).e("icon-btn"),
                                          { "is-disabled": !M($e) },
                                        ],
                                        "d-arrow-right",
                                      ]),
                                      onClick: ge,
                                    },
                                    [
                                      G(M(Y), null, {
                                        default: _(() => [G(M(de))]),
                                        _: 1,
                                      }),
                                    ],
                                    10,
                                    mt,
                                  ))
                                : I("v-if", !0),
                              e.unlinkPanels
                                ? ($(),
                                  T(
                                    "button",
                                    {
                                      key: 1,
                                      type: "button",
                                      disabled: !M(xe),
                                      class: O([
                                        [
                                          M(S).e("icon-btn"),
                                          { "is-disabled": !M(xe) },
                                        ],
                                        "arrow-right",
                                      ]),
                                      onClick: ke,
                                    },
                                    [
                                      G(M(Y), null, {
                                        default: _(() => [G(M(ie))]),
                                        _: 1,
                                      }),
                                    ],
                                    10,
                                    ft,
                                  ))
                                : I("v-if", !0),
                              N("div", null, R(M(H)), 1),
                            ],
                            2,
                          ),
                          G(
                            Ba,
                            {
                              "selection-mode": "range",
                              date: b.value,
                              "min-date": M(k),
                              "max-date": M(w),
                              "range-state": M(D),
                              "disabled-date": M(r),
                              "cell-class-name": M(s),
                              onChangerange: M(P),
                              onPick: Pe,
                              onSelect: M(E),
                            },
                            null,
                            8,
                            [
                              "date",
                              "min-date",
                              "max-date",
                              "range-state",
                              "disabled-date",
                              "cell-class-name",
                              "onChangerange",
                              "onSelect",
                            ],
                          ),
                        ],
                        2,
                      ),
                      N(
                        "div",
                        {
                          class: O([
                            [M(S).e("content"), M(x).e("content")],
                            "is-right",
                          ]),
                        },
                        [
                          N(
                            "div",
                            { class: O(M(x).e("header")) },
                            [
                              e.unlinkPanels
                                ? ($(),
                                  T(
                                    "button",
                                    {
                                      key: 0,
                                      type: "button",
                                      disabled: !M($e),
                                      class: O([
                                        [
                                          M(S).e("icon-btn"),
                                          { "is-disabled": !M($e) },
                                        ],
                                        "d-arrow-left",
                                      ]),
                                      onClick: we,
                                    },
                                    [
                                      G(M(Y), null, {
                                        default: _(() => [G(M(oe))]),
                                        _: 1,
                                      }),
                                    ],
                                    10,
                                    ht,
                                  ))
                                : I("v-if", !0),
                              e.unlinkPanels
                                ? ($(),
                                  T(
                                    "button",
                                    {
                                      key: 1,
                                      type: "button",
                                      disabled: !M(xe),
                                      class: O([
                                        [
                                          M(S).e("icon-btn"),
                                          { "is-disabled": !M(xe) },
                                        ],
                                        "arrow-left",
                                      ]),
                                      onClick: De,
                                    },
                                    [
                                      G(M(Y), null, {
                                        default: _(() => [G(M(ue))]),
                                        _: 1,
                                      }),
                                    ],
                                    10,
                                    yt,
                                  ))
                                : I("v-if", !0),
                              N(
                                "button",
                                {
                                  type: "button",
                                  class: O([
                                    M(S).e("icon-btn"),
                                    "d-arrow-right",
                                  ]),
                                  onClick: he,
                                },
                                [
                                  G(M(Y), null, {
                                    default: _(() => [G(M(de))]),
                                    _: 1,
                                  }),
                                ],
                                2,
                              ),
                              N(
                                "button",
                                {
                                  type: "button",
                                  class: O([M(S).e("icon-btn"), "arrow-right"]),
                                  onClick: ye,
                                },
                                [
                                  G(M(Y), null, {
                                    default: _(() => [G(M(ie))]),
                                    _: 1,
                                  }),
                                ],
                                2,
                              ),
                              N("div", null, R(M(z)), 1),
                            ],
                            2,
                          ),
                          G(
                            Ba,
                            {
                              "selection-mode": "range",
                              date: g.value,
                              "min-date": M(k),
                              "max-date": M(w),
                              "range-state": M(D),
                              "disabled-date": M(r),
                              "cell-class-name": M(s),
                              onChangerange: M(P),
                              onPick: Pe,
                              onSelect: M(E),
                            },
                            null,
                            8,
                            [
                              "date",
                              "min-date",
                              "max-date",
                              "range-state",
                              "disabled-date",
                              "cell-class-name",
                              "onChangerange",
                              "onSelect",
                            ],
                          ),
                        ],
                        2,
                      ),
                    ],
                    2,
                  ),
                ],
                2,
              ),
              M(_e)
                ? ($(),
                  T(
                    "div",
                    { key: 0, class: O(M(S).e("footer")) },
                    [
                      M(d)
                        ? ($(),
                          C(
                            M(ce),
                            {
                              key: 0,
                              text: "",
                              size: "small",
                              class: O(M(S).e("link-btn")),
                              onClick: He,
                            },
                            {
                              default: _(() => [
                                U(R(M(F)("el.datepicker.clear")), 1),
                              ]),
                              _: 1,
                            },
                            8,
                            ["class"],
                          ))
                        : I("v-if", !0),
                      G(
                        M(ce),
                        {
                          plain: "",
                          size: "small",
                          class: O(M(S).e("link-btn")),
                          disabled: M(Ce),
                          onClick: a[10] || (a[10] = (e) => M(V)(!1)),
                        },
                        {
                          default: _(() => [
                            U(R(M(F)("el.datepicker.confirm")), 1),
                          ]),
                          _: 1,
                        },
                        8,
                        ["class", "disabled"],
                      ),
                    ],
                    2,
                  ))
                : I("v-if", !0),
            ],
            2,
          )
        )
      );
    },
  });
var kt = F(gt, [
  [
    "__file",
    "/home/runner/work/element-plus/element-plus/packages/components/date-picker/src/date-picker-com/panel-date-range.vue",
  ],
]);
const wt = r({ ...Oa }),
  Dt = ["onClick"],
  Mt = ["disabled"],
  St = ["disabled"],
  xt = "year",
  $t = i({ name: "DatePickerMonthRange" }),
  Ct = i({
    ...$t,
    props: wt,
    emits: ["pick", "set-picker-option"],
    setup(e, { emit: a }) {
      const t = e,
        { lang: n } = c(),
        l = m("EP_PICKER_BASE"),
        { shortcuts: r, disabledDate: s, format: o } = l.props,
        u = re(l.props, "defaultValue"),
        i = f(Me().locale(n.value)),
        d = f(Me().locale(n.value).add(1, xt)),
        {
          minDate: v,
          maxDate: p,
          rangeState: y,
          ppNs: b,
          drpNs: g,
          handleChangeRange: k,
          handleRangeConfirm: w,
          handleShortcutClick: D,
          onSelect: S,
        } = vt(t, {
          defaultValue: u,
          leftDate: i,
          rightDate: d,
          unit: xt,
          onParsedValueChanged: function (e, a) {
            if (t.unlinkPanels && a) {
              const t = (null == e ? void 0 : e.year()) || 0,
                n = a.year();
              d.value = t === n ? a.add(1, xt) : a;
            } else d.value = i.value.add(1, xt);
          },
        }),
        x = h(() => !!r.length),
        {
          leftPrevYear: C,
          rightNextYear: P,
          leftNextYear: V,
          rightPrevYear: A,
          leftLabel: E,
          rightLabel: F,
          leftYear: B,
          rightYear: W,
        } = (({ unlinkPanels: e, leftDate: a, rightDate: t }) => {
          const { t: n } = c();
          return {
            leftPrevYear: () => {
              ((a.value = a.value.subtract(1, "year")),
                e.value || (t.value = t.value.subtract(1, "year")));
            },
            rightNextYear: () => {
              (e.value || (a.value = a.value.add(1, "year")),
                (t.value = t.value.add(1, "year")));
            },
            leftNextYear: () => {
              a.value = a.value.add(1, "year");
            },
            rightPrevYear: () => {
              t.value = t.value.subtract(1, "year");
            },
            leftLabel: h(() => `${a.value.year()} ${n("el.datepicker.year")}`),
            rightLabel: h(() => `${t.value.year()} ${n("el.datepicker.year")}`),
            leftYear: h(() => a.value.year()),
            rightYear: h(() =>
              t.value.year() === a.value.year()
                ? a.value.year() + 1
                : t.value.year(),
            ),
          };
        })({ unlinkPanels: re(t, "unlinkPanels"), leftDate: i, rightDate: d }),
        H = h(() => t.unlinkPanels && W.value > B.value + 1),
        z = (e, a = !0) => {
          const t = e.minDate,
            n = e.maxDate;
          (p.value === n && v.value === t) ||
            ((p.value = n), (v.value = t), a && w());
        };
      return (
        a("set-picker-option", [
          "formatToString",
          (e) => e.map((e) => e.format(o)),
        ]),
        (e, a) => (
          $(),
          T(
            "div",
            {
              class: O([
                M(b).b(),
                M(g).b(),
                { "has-sidebar": Boolean(e.$slots.sidebar) || M(x) },
              ]),
            },
            [
              N(
                "div",
                { class: O(M(b).e("body-wrapper")) },
                [
                  L(e.$slots, "sidebar", { class: O(M(b).e("sidebar")) }),
                  M(x)
                    ? ($(),
                      T(
                        "div",
                        { key: 0, class: O(M(b).e("sidebar")) },
                        [
                          ($(!0),
                          T(
                            j,
                            null,
                            K(
                              M(r),
                              (e, a) => (
                                $(),
                                T(
                                  "button",
                                  {
                                    key: a,
                                    type: "button",
                                    class: O(M(b).e("shortcut")),
                                    onClick: (a) => M(D)(e),
                                  },
                                  R(e.text),
                                  11,
                                  Dt,
                                )
                              ),
                            ),
                            128,
                          )),
                        ],
                        2,
                      ))
                    : I("v-if", !0),
                  N(
                    "div",
                    { class: O(M(b).e("body")) },
                    [
                      N(
                        "div",
                        {
                          class: O([
                            [M(b).e("content"), M(g).e("content")],
                            "is-left",
                          ]),
                        },
                        [
                          N(
                            "div",
                            { class: O(M(g).e("header")) },
                            [
                              N(
                                "button",
                                {
                                  type: "button",
                                  class: O([
                                    M(b).e("icon-btn"),
                                    "d-arrow-left",
                                  ]),
                                  onClick:
                                    a[0] ||
                                    (a[0] = (...e) => M(C) && M(C)(...e)),
                                },
                                [
                                  G(M(Y), null, {
                                    default: _(() => [G(M(oe))]),
                                    _: 1,
                                  }),
                                ],
                                2,
                              ),
                              e.unlinkPanels
                                ? ($(),
                                  T(
                                    "button",
                                    {
                                      key: 0,
                                      type: "button",
                                      disabled: !M(H),
                                      class: O([
                                        [
                                          M(b).e("icon-btn"),
                                          { [M(b).is("disabled")]: !M(H) },
                                        ],
                                        "d-arrow-right",
                                      ]),
                                      onClick:
                                        a[1] ||
                                        (a[1] = (...e) => M(V) && M(V)(...e)),
                                    },
                                    [
                                      G(M(Y), null, {
                                        default: _(() => [G(M(de))]),
                                        _: 1,
                                      }),
                                    ],
                                    10,
                                    Mt,
                                  ))
                                : I("v-if", !0),
                              N("div", null, R(M(E)), 1),
                            ],
                            2,
                          ),
                          G(
                            Ua,
                            {
                              "selection-mode": "range",
                              date: i.value,
                              "min-date": M(v),
                              "max-date": M(p),
                              "range-state": M(y),
                              "disabled-date": M(s),
                              onChangerange: M(k),
                              onPick: z,
                              onSelect: M(S),
                            },
                            null,
                            8,
                            [
                              "date",
                              "min-date",
                              "max-date",
                              "range-state",
                              "disabled-date",
                              "onChangerange",
                              "onSelect",
                            ],
                          ),
                        ],
                        2,
                      ),
                      N(
                        "div",
                        {
                          class: O([
                            [M(b).e("content"), M(g).e("content")],
                            "is-right",
                          ]),
                        },
                        [
                          N(
                            "div",
                            { class: O(M(g).e("header")) },
                            [
                              e.unlinkPanels
                                ? ($(),
                                  T(
                                    "button",
                                    {
                                      key: 0,
                                      type: "button",
                                      disabled: !M(H),
                                      class: O([
                                        [
                                          M(b).e("icon-btn"),
                                          { "is-disabled": !M(H) },
                                        ],
                                        "d-arrow-left",
                                      ]),
                                      onClick:
                                        a[2] ||
                                        (a[2] = (...e) => M(A) && M(A)(...e)),
                                    },
                                    [
                                      G(M(Y), null, {
                                        default: _(() => [G(M(oe))]),
                                        _: 1,
                                      }),
                                    ],
                                    10,
                                    St,
                                  ))
                                : I("v-if", !0),
                              N(
                                "button",
                                {
                                  type: "button",
                                  class: O([
                                    M(b).e("icon-btn"),
                                    "d-arrow-right",
                                  ]),
                                  onClick:
                                    a[3] ||
                                    (a[3] = (...e) => M(P) && M(P)(...e)),
                                },
                                [
                                  G(M(Y), null, {
                                    default: _(() => [G(M(de))]),
                                    _: 1,
                                  }),
                                ],
                                2,
                              ),
                              N("div", null, R(M(F)), 1),
                            ],
                            2,
                          ),
                          G(
                            Ua,
                            {
                              "selection-mode": "range",
                              date: d.value,
                              "min-date": M(v),
                              "max-date": M(p),
                              "range-state": M(y),
                              "disabled-date": M(s),
                              onChangerange: M(k),
                              onPick: z,
                              onSelect: M(S),
                            },
                            null,
                            8,
                            [
                              "date",
                              "min-date",
                              "max-date",
                              "range-state",
                              "disabled-date",
                              "onChangerange",
                              "onSelect",
                            ],
                          ),
                        ],
                        2,
                      ),
                    ],
                    2,
                  ),
                ],
                2,
              ),
            ],
            2,
          )
        )
      );
    },
  });
var _t = F(Ct, [
  [
    "__file",
    "/home/runner/work/element-plus/element-plus/packages/components/date-picker/src/date-picker-com/panel-month-range.vue",
  ],
]);
(Me.extend(ia),
  Me.extend(ca),
  Me.extend(xe),
  Me.extend(fa),
  Me.extend(ya),
  Me.extend(ga),
  Me.extend(wa),
  Me.extend(Ma));
const Ot = i({
  name: "ElDatePicker",
  install: null,
  props: xa,
  emits: ["update:modelValue"],
  setup(e, { expose: a, emit: t, slots: n }) {
    const l = v("picker-panel");
    (x("ElPopperOptions", pe(re(e, "popperOptions"))),
      x(Sa, { slots: n, pickerNs: l }));
    const r = f();
    a({
      focus: (e = !0) => {
        var a;
        null == (a = r.value) || a.focus(e);
      },
      handleOpen: () => {
        var e;
        null == (e = r.value) || e.handleOpen();
      },
      handleClose: () => {
        var e;
        null == (e = r.value) || e.handleClose();
      },
    });
    const s = (e) => {
      t("update:modelValue", e);
    };
    return () => {
      var a;
      const t = null != (a = e.format) ? a : Oe[e.type] || _e,
        l = (function (e) {
          switch (e) {
            case "daterange":
            case "datetimerange":
              return kt;
            case "monthrange":
              return _t;
            default:
              return dt;
          }
        })(e.type);
      return G(
        Ke,
        E(e, { format: t, type: e.type, ref: r, "onUpdate:modelValue": s }),
        {
          default: (e) => G(l, e, null),
          "range-separator": n["range-separator"],
        },
      );
    };
  },
});
Ot.install = (e) => {
  e.component(Ot.name, Ot);
};
const Pt = Ot;
export {
  Ke as C,
  Ce as D,
  Pt as E,
  ra as T,
  Ze as a,
  Xe as b,
  xe as c,
  Me as d,
  Be as e,
  oa as f,
  ke as g,
  we as h,
  Fe as t,
  Je as u,
  aa as v,
};
