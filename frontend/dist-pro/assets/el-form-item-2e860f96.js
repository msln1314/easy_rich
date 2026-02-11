import {
  bJ as e,
  bK as r,
  b as t,
  c as n,
  d as a,
  aZ as i,
  g as s,
  b7 as l,
  r as u,
  f as o,
  e as f,
  b9 as d,
  u as c,
  w as p,
  ba as v,
  am as g,
  L as h,
  bw as y,
  bn as m,
  o as b,
  j as w,
  q,
  s as F,
  k as O,
  _ as x,
  b3 as j,
  ao as E,
  bo as A,
  ar as P,
  a2 as k,
  aj as S,
  aw as R,
  at as $,
  x as _,
  a1 as M,
  as as W,
  aE as B,
  bL as I,
  bM as V,
  h as z,
  bN as L,
  m as N,
  l as C,
  p as D,
  n as T,
  M as J,
  z as Z,
  F as G,
  y as K,
  T as U,
  t as Y,
  a8 as H
} from './index-820a519e.js'
function Q() {
  if (!arguments.length) return []
  var r = arguments[0]
  return e(r) ? r : [r]
}
function X(e) {
  return r(e, 4)
}
const ee = t({ size: { type: String, values: n }, disabled: Boolean }),
  re = t({
    ...ee,
    model: Object,
    rules: { type: a(Object) },
    labelPosition: { type: String, values: ['left', 'right', 'top'], default: 'right' },
    requireAsteriskPosition: { type: String, values: ['left', 'right'], default: 'left' },
    labelWidth: { type: [String, Number], default: '' },
    labelSuffix: { type: String, default: '' },
    inline: Boolean,
    inlineMessage: Boolean,
    statusIcon: Boolean,
    showMessage: { type: Boolean, default: !0 },
    validateOnRuleChange: { type: Boolean, default: !0 },
    hideRequiredAsterisk: Boolean,
    scrollToError: Boolean,
    scrollIntoViewOptions: { type: [Object, Boolean] }
  }),
  te = { validate: (e, r, t) => (i(e) || s(e)) && l(r) && s(t) }
function ne() {
  const e = u([]),
    r = o(() => {
      if (!e.value.length) return '0'
      const r = Math.max(...e.value)
      return r ? `${r}px` : ''
    })
  function t(t) {
    const n = e.value.indexOf(t)
    return (-1 === n && r.value, n)
  }
  return {
    autoLabelWidth: r,
    registerLabelWidth: function (r, n) {
      if (r && n) {
        const a = t(n)
        e.value.splice(a, 1, r)
      } else r && e.value.push(r)
    },
    deregisterLabelWidth: function (r) {
      const n = t(r)
      n > -1 && e.value.splice(n, 1)
    }
  }
}
const ae = (e, r) => {
    const t = Q(r)
    return t.length > 0 ? e.filter((e) => e.prop && t.includes(e.prop)) : e
  },
  ie = f({ name: 'ElForm' })
var se = x(
  f({
    ...ie,
    props: re,
    emits: te,
    setup(e, { expose: r, emit: t }) {
      const n = e,
        a = [],
        i = d(),
        s = c('form'),
        l = o(() => {
          const { labelPosition: e, inline: r } = n
          return [s.b(), s.m(i.value || 'default'), { [s.m(`label-${e}`)]: e, [s.m('inline')]: r }]
        }),
        u = (e = []) => {
          n.model && ae(a, e).forEach((e) => e.resetField())
        },
        f = (e = []) => {
          ae(a, e).forEach((e) => e.clearValidate())
        },
        x = o(() => !!n.model),
        E = async (e) => P(void 0, e),
        A = async (e = []) => {
          if (!x.value) return !1
          const r = ((e) => {
            if (0 === a.length) return []
            const r = ae(a, e)
            return r.length ? r : []
          })(e)
          if (0 === r.length) return !0
          let t = {}
          for (const a of r)
            try {
              await a.validate('')
            } catch (n) {
              t = { ...t, ...n }
            }
          return 0 === Object.keys(t).length || Promise.reject(t)
        },
        P = async (e = [], r) => {
          const t = !j(r)
          try {
            const t = await A(e)
            return (!0 === t && (null == r || r(t)), t)
          } catch (a) {
            if (a instanceof Error) throw a
            const e = a
            return (
              n.scrollToError && k(Object.keys(e)[0]),
              null == r || r(!1, e),
              t && Promise.reject(e)
            )
          }
        },
        k = (e) => {
          var r
          const t = ae(a, e)[0]
          t && (null == (r = t.$el) || r.scrollIntoView(n.scrollIntoViewOptions))
        }
      return (
        p(
          () => n.rules,
          () => {
            n.validateOnRuleChange && E().catch((e) => v())
          },
          { deep: !0 }
        ),
        g(
          m,
          h({
            ...y(n),
            emit: t,
            resetFields: u,
            clearValidate: f,
            validateField: P,
            addField: (e) => {
              a.push(e)
            },
            removeField: (e) => {
              e.prop && a.splice(a.indexOf(e), 1)
            },
            ...ne()
          })
        ),
        r({ validate: E, validateField: P, resetFields: u, clearValidate: f, scrollToField: k }),
        (e, r) => (b(), w('form', { class: F(O(l)) }, [q(e.$slots, 'default')], 2))
      )
    }
  }),
  [['__file', '/home/runner/work/element-plus/element-plus/packages/components/form/src/form.vue']]
)
function le() {
  return (
    (le = Object.assign
      ? Object.assign.bind()
      : function (e) {
          for (var r = 1; r < arguments.length; r++) {
            var t = arguments[r]
            for (var n in t) Object.prototype.hasOwnProperty.call(t, n) && (e[n] = t[n])
          }
          return e
        }),
    le.apply(this, arguments)
  )
}
function ue(e) {
  return (ue = Object.setPrototypeOf
    ? Object.getPrototypeOf.bind()
    : function (e) {
        return e.__proto__ || Object.getPrototypeOf(e)
      })(e)
}
function oe(e, r) {
  return (oe = Object.setPrototypeOf
    ? Object.setPrototypeOf.bind()
    : function (e, r) {
        return ((e.__proto__ = r), e)
      })(e, r)
}
function fe(e, r, t) {
  return (fe = (function () {
    if ('undefined' == typeof Reflect || !Reflect.construct) return !1
    if (Reflect.construct.sham) return !1
    if ('function' == typeof Proxy) return !0
    try {
      return (Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], function () {})), !0)
    } catch (e) {
      return !1
    }
  })()
    ? Reflect.construct.bind()
    : function (e, r, t) {
        var n = [null]
        n.push.apply(n, r)
        var a = new (Function.bind.apply(e, n))()
        return (t && oe(a, t.prototype), a)
      }).apply(null, arguments)
}
function de(e) {
  var r = 'function' == typeof Map ? new Map() : void 0
  return (
    (de = function (e) {
      if (null === e || ((t = e), -1 === Function.toString.call(t).indexOf('[native code]')))
        return e
      var t
      if ('function' != typeof e)
        throw new TypeError('Super expression must either be null or a function')
      if (void 0 !== r) {
        if (r.has(e)) return r.get(e)
        r.set(e, n)
      }
      function n() {
        return fe(e, arguments, ue(this).constructor)
      }
      return (
        (n.prototype = Object.create(e.prototype, {
          constructor: { value: n, enumerable: !1, writable: !0, configurable: !0 }
        })),
        oe(n, e)
      )
    }),
    de(e)
  )
}
var ce = /%[sdj%]/g,
  pe = function () {}
function ve(e) {
  if (!e || !e.length) return null
  var r = {}
  return (
    e.forEach(function (e) {
      var t = e.field
      ;((r[t] = r[t] || []), r[t].push(e))
    }),
    r
  )
}
function ge(e) {
  for (var r = arguments.length, t = new Array(r > 1 ? r - 1 : 0), n = 1; n < r; n++)
    t[n - 1] = arguments[n]
  var a = 0,
    i = t.length
  return 'function' == typeof e
    ? e.apply(null, t)
    : 'string' == typeof e
      ? e.replace(ce, function (e) {
          if ('%%' === e) return '%'
          if (a >= i) return e
          switch (e) {
            case '%s':
              return String(t[a++])
            case '%d':
              return Number(t[a++])
            case '%j':
              try {
                return JSON.stringify(t[a++])
              } catch (r) {
                return '[Circular]'
              }
              break
            default:
              return e
          }
        })
      : e
}
function he(e, r) {
  return (
    null == e ||
    !('array' !== r || !Array.isArray(e) || e.length) ||
    !(
      !(function (e) {
        return (
          'string' === e ||
          'url' === e ||
          'hex' === e ||
          'email' === e ||
          'date' === e ||
          'pattern' === e
        )
      })(r) ||
      'string' != typeof e ||
      e
    )
  )
}
function ye(e, r, t) {
  var n = 0,
    a = e.length
  !(function i(s) {
    if (s && s.length) t(s)
    else {
      var l = n
      ;((n += 1), l < a ? r(e[l], i) : t([]))
    }
  })([])
}
'undefined' != typeof process && process.env
var me = (function (e) {
  var r, t
  function n(r, t) {
    var n
    return (((n = e.call(this, 'Async Validation Error') || this).errors = r), (n.fields = t), n)
  }
  return (
    (t = e),
    ((r = n).prototype = Object.create(t.prototype)),
    (r.prototype.constructor = r),
    oe(r, t),
    n
  )
})(de(Error))
function be(e, r, t, n, a) {
  if (r.first) {
    var i = new Promise(function (r, i) {
      var s = (function (e) {
        var r = []
        return (
          Object.keys(e).forEach(function (t) {
            r.push.apply(r, e[t] || [])
          }),
          r
        )
      })(e)
      ye(s, t, function (e) {
        return (n(e), e.length ? i(new me(e, ve(e))) : r(a))
      })
    })
    return (
      i.catch(function (e) {
        return e
      }),
      i
    )
  }
  var s = !0 === r.firstFields ? Object.keys(e) : r.firstFields || [],
    l = Object.keys(e),
    u = l.length,
    o = 0,
    f = [],
    d = new Promise(function (r, i) {
      var d = function (e) {
        if ((f.push.apply(f, e), ++o === u)) return (n(f), f.length ? i(new me(f, ve(f))) : r(a))
      }
      ;(l.length || (n(f), r(a)),
        l.forEach(function (r) {
          var n = e[r]
          ;-1 !== s.indexOf(r)
            ? ye(n, t, d)
            : (function (e, r, t) {
                var n = [],
                  a = 0,
                  i = e.length
                function s(e) {
                  ;(n.push.apply(n, e || []), ++a === i && t(n))
                }
                e.forEach(function (e) {
                  r(e, s)
                })
              })(n, t, d)
        }))
    })
  return (
    d.catch(function (e) {
      return e
    }),
    d
  )
}
function we(e, r) {
  return function (t) {
    var n, a
    return (
      (n = e.fullFields
        ? (function (e, r) {
            for (var t = e, n = 0; n < r.length; n++) {
              if (null == t) return t
              t = t[r[n]]
            }
            return t
          })(r, e.fullFields)
        : r[t.field || e.fullField]),
      (a = t) && void 0 !== a.message
        ? ((t.field = t.field || e.fullField), (t.fieldValue = n), t)
        : {
            message: 'function' == typeof t ? t() : t,
            fieldValue: n,
            field: t.field || e.fullField
          }
    )
  }
}
function qe(e, r) {
  if (r)
    for (var t in r)
      if (r.hasOwnProperty(t)) {
        var n = r[t]
        'object' == typeof n && 'object' == typeof e[t] ? (e[t] = le({}, e[t], n)) : (e[t] = n)
      }
  return e
}
var Fe,
  Oe = function (e, r, t, n, a, i) {
    !e.required ||
      (t.hasOwnProperty(e.field) && !he(r, i || e.type)) ||
      n.push(ge(a.messages.required, e.fullField))
  },
  xe =
    /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]+\.)+[a-zA-Z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]{2,}))$/,
  je = /^#?([a-f0-9]{6}|[a-f0-9]{3})$/i,
  Ee = {
    integer: function (e) {
      return Ee.number(e) && parseInt(e, 10) === e
    },
    float: function (e) {
      return Ee.number(e) && !Ee.integer(e)
    },
    array: function (e) {
      return Array.isArray(e)
    },
    regexp: function (e) {
      if (e instanceof RegExp) return !0
      try {
        return !!new RegExp(e)
      } catch (r) {
        return !1
      }
    },
    date: function (e) {
      return (
        'function' == typeof e.getTime &&
        'function' == typeof e.getMonth &&
        'function' == typeof e.getYear &&
        !isNaN(e.getTime())
      )
    },
    number: function (e) {
      return !isNaN(e) && 'number' == typeof e
    },
    object: function (e) {
      return 'object' == typeof e && !Ee.array(e)
    },
    method: function (e) {
      return 'function' == typeof e
    },
    email: function (e) {
      return 'string' == typeof e && e.length <= 320 && !!e.match(xe)
    },
    url: function (e) {
      return (
        'string' == typeof e &&
        e.length <= 2048 &&
        !!e.match(
          (function () {
            if (Fe) return Fe
            var e = '[a-fA-F\\d:]',
              r = function (r) {
                return r && r.includeBoundaries
                  ? '(?:(?<=\\s|^)(?=' + e + ')|(?<=' + e + ')(?=\\s|$))'
                  : ''
              },
              t =
                '(?:25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]\\d|\\d)(?:\\.(?:25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]\\d|\\d)){3}',
              n = '[a-fA-F\\d]{1,4}',
              a = (
                '\n(?:\n(?:' +
                n +
                ':){7}(?:' +
                n +
                '|:)|                                    // 1:2:3:4:5:6:7::  1:2:3:4:5:6:7:8\n(?:' +
                n +
                ':){6}(?:' +
                t +
                '|:' +
                n +
                '|:)|                             // 1:2:3:4:5:6::    1:2:3:4:5:6::8   1:2:3:4:5:6::8  1:2:3:4:5:6::1.2.3.4\n(?:' +
                n +
                ':){5}(?::' +
                t +
                '|(?::' +
                n +
                '){1,2}|:)|                   // 1:2:3:4:5::      1:2:3:4:5::7:8   1:2:3:4:5::8    1:2:3:4:5::7:1.2.3.4\n(?:' +
                n +
                ':){4}(?:(?::' +
                n +
                '){0,1}:' +
                t +
                '|(?::' +
                n +
                '){1,3}|:)| // 1:2:3:4::        1:2:3:4::6:7:8   1:2:3:4::8      1:2:3:4::6:7:1.2.3.4\n(?:' +
                n +
                ':){3}(?:(?::' +
                n +
                '){0,2}:' +
                t +
                '|(?::' +
                n +
                '){1,4}|:)| // 1:2:3::          1:2:3::5:6:7:8   1:2:3::8        1:2:3::5:6:7:1.2.3.4\n(?:' +
                n +
                ':){2}(?:(?::' +
                n +
                '){0,3}:' +
                t +
                '|(?::' +
                n +
                '){1,5}|:)| // 1:2::            1:2::4:5:6:7:8   1:2::8          1:2::4:5:6:7:1.2.3.4\n(?:' +
                n +
                ':){1}(?:(?::' +
                n +
                '){0,4}:' +
                t +
                '|(?::' +
                n +
                '){1,6}|:)| // 1::              1::3:4:5:6:7:8   1::8            1::3:4:5:6:7:1.2.3.4\n(?::(?:(?::' +
                n +
                '){0,5}:' +
                t +
                '|(?::' +
                n +
                '){1,7}|:))             // ::2:3:4:5:6:7:8  ::2:3:4:5:6:7:8  ::8             ::1.2.3.4\n)(?:%[0-9a-zA-Z]{1,})?                                             // %eth0            %1\n'
              )
                .replace(/\s*\/\/.*$/gm, '')
                .replace(/\n/g, '')
                .trim(),
              i = new RegExp('(?:^' + t + '$)|(?:^' + a + '$)'),
              s = new RegExp('^' + t + '$'),
              l = new RegExp('^' + a + '$'),
              u = function (e) {
                return e && e.exact
                  ? i
                  : new RegExp('(?:' + r(e) + t + r(e) + ')|(?:' + r(e) + a + r(e) + ')', 'g')
              }
            ;((u.v4 = function (e) {
              return e && e.exact ? s : new RegExp('' + r(e) + t + r(e), 'g')
            }),
              (u.v6 = function (e) {
                return e && e.exact ? l : new RegExp('' + r(e) + a + r(e), 'g')
              }))
            var o = u.v4().source,
              f = u.v6().source
            return (Fe = new RegExp(
              '(?:^(?:(?:(?:[a-z]+:)?//)|www\\.)(?:\\S+(?::\\S*)?@)?(?:localhost|' +
                o +
                '|' +
                f +
                '|(?:(?:[a-z\\u00a1-\\uffff0-9][-_]*)*[a-z\\u00a1-\\uffff0-9]+)(?:\\.(?:[a-z\\u00a1-\\uffff0-9]-*)*[a-z\\u00a1-\\uffff0-9]+)*(?:\\.(?:[a-z\\u00a1-\\uffff]{2,})))(?::\\d{2,5})?(?:[/?#][^\\s"]*)?$)',
              'i'
            ))
          })()
        )
      )
    },
    hex: function (e) {
      return 'string' == typeof e && !!e.match(je)
    }
  },
  Ae = 'enum',
  Pe = {
    required: Oe,
    whitespace: function (e, r, t, n, a) {
      ;(/^\s+$/.test(r) || '' === r) && n.push(ge(a.messages.whitespace, e.fullField))
    },
    type: function (e, r, t, n, a) {
      if (e.required && void 0 === r) Oe(e, r, t, n, a)
      else {
        var i = e.type
        ;[
          'integer',
          'float',
          'array',
          'regexp',
          'object',
          'method',
          'email',
          'number',
          'date',
          'url',
          'hex'
        ].indexOf(i) > -1
          ? Ee[i](r) || n.push(ge(a.messages.types[i], e.fullField, e.type))
          : i && typeof r !== e.type && n.push(ge(a.messages.types[i], e.fullField, e.type))
      }
    },
    range: function (e, r, t, n, a) {
      var i = 'number' == typeof e.len,
        s = 'number' == typeof e.min,
        l = 'number' == typeof e.max,
        u = r,
        o = null,
        f = 'number' == typeof r,
        d = 'string' == typeof r,
        c = Array.isArray(r)
      if ((f ? (o = 'number') : d ? (o = 'string') : c && (o = 'array'), !o)) return !1
      ;(c && (u = r.length),
        d && (u = r.replace(/[\uD800-\uDBFF][\uDC00-\uDFFF]/g, '_').length),
        i
          ? u !== e.len && n.push(ge(a.messages[o].len, e.fullField, e.len))
          : s && !l && u < e.min
            ? n.push(ge(a.messages[o].min, e.fullField, e.min))
            : l && !s && u > e.max
              ? n.push(ge(a.messages[o].max, e.fullField, e.max))
              : s &&
                l &&
                (u < e.min || u > e.max) &&
                n.push(ge(a.messages[o].range, e.fullField, e.min, e.max)))
    },
    enum: function (e, r, t, n, a) {
      ;((e[Ae] = Array.isArray(e[Ae]) ? e[Ae] : []),
        -1 === e[Ae].indexOf(r) && n.push(ge(a.messages[Ae], e.fullField, e[Ae].join(', '))))
    },
    pattern: function (e, r, t, n, a) {
      if (e.pattern)
        if (e.pattern instanceof RegExp)
          ((e.pattern.lastIndex = 0),
            e.pattern.test(r) || n.push(ge(a.messages.pattern.mismatch, e.fullField, r, e.pattern)))
        else if ('string' == typeof e.pattern) {
          new RegExp(e.pattern).test(r) ||
            n.push(ge(a.messages.pattern.mismatch, e.fullField, r, e.pattern))
        }
    }
  },
  ke = function (e, r, t, n, a) {
    var i = e.type,
      s = []
    if (e.required || (!e.required && n.hasOwnProperty(e.field))) {
      if (he(r, i) && !e.required) return t()
      ;(Pe.required(e, r, n, s, a, i), he(r, i) || Pe.type(e, r, n, s, a))
    }
    t(s)
  },
  Se = {
    string: function (e, r, t, n, a) {
      var i = []
      if (e.required || (!e.required && n.hasOwnProperty(e.field))) {
        if (he(r, 'string') && !e.required) return t()
        ;(Pe.required(e, r, n, i, a, 'string'),
          he(r, 'string') ||
            (Pe.type(e, r, n, i, a),
            Pe.range(e, r, n, i, a),
            Pe.pattern(e, r, n, i, a),
            !0 === e.whitespace && Pe.whitespace(e, r, n, i, a)))
      }
      t(i)
    },
    method: function (e, r, t, n, a) {
      var i = []
      if (e.required || (!e.required && n.hasOwnProperty(e.field))) {
        if (he(r) && !e.required) return t()
        ;(Pe.required(e, r, n, i, a), void 0 !== r && Pe.type(e, r, n, i, a))
      }
      t(i)
    },
    number: function (e, r, t, n, a) {
      var i = []
      if (e.required || (!e.required && n.hasOwnProperty(e.field))) {
        if (('' === r && (r = void 0), he(r) && !e.required)) return t()
        ;(Pe.required(e, r, n, i, a),
          void 0 !== r && (Pe.type(e, r, n, i, a), Pe.range(e, r, n, i, a)))
      }
      t(i)
    },
    boolean: function (e, r, t, n, a) {
      var i = []
      if (e.required || (!e.required && n.hasOwnProperty(e.field))) {
        if (he(r) && !e.required) return t()
        ;(Pe.required(e, r, n, i, a), void 0 !== r && Pe.type(e, r, n, i, a))
      }
      t(i)
    },
    regexp: function (e, r, t, n, a) {
      var i = []
      if (e.required || (!e.required && n.hasOwnProperty(e.field))) {
        if (he(r) && !e.required) return t()
        ;(Pe.required(e, r, n, i, a), he(r) || Pe.type(e, r, n, i, a))
      }
      t(i)
    },
    integer: function (e, r, t, n, a) {
      var i = []
      if (e.required || (!e.required && n.hasOwnProperty(e.field))) {
        if (he(r) && !e.required) return t()
        ;(Pe.required(e, r, n, i, a),
          void 0 !== r && (Pe.type(e, r, n, i, a), Pe.range(e, r, n, i, a)))
      }
      t(i)
    },
    float: function (e, r, t, n, a) {
      var i = []
      if (e.required || (!e.required && n.hasOwnProperty(e.field))) {
        if (he(r) && !e.required) return t()
        ;(Pe.required(e, r, n, i, a),
          void 0 !== r && (Pe.type(e, r, n, i, a), Pe.range(e, r, n, i, a)))
      }
      t(i)
    },
    array: function (e, r, t, n, a) {
      var i = []
      if (e.required || (!e.required && n.hasOwnProperty(e.field))) {
        if (null == r && !e.required) return t()
        ;(Pe.required(e, r, n, i, a, 'array'),
          null != r && (Pe.type(e, r, n, i, a), Pe.range(e, r, n, i, a)))
      }
      t(i)
    },
    object: function (e, r, t, n, a) {
      var i = []
      if (e.required || (!e.required && n.hasOwnProperty(e.field))) {
        if (he(r) && !e.required) return t()
        ;(Pe.required(e, r, n, i, a), void 0 !== r && Pe.type(e, r, n, i, a))
      }
      t(i)
    },
    enum: function (e, r, t, n, a) {
      var i = []
      if (e.required || (!e.required && n.hasOwnProperty(e.field))) {
        if (he(r) && !e.required) return t()
        ;(Pe.required(e, r, n, i, a), void 0 !== r && Pe.enum(e, r, n, i, a))
      }
      t(i)
    },
    pattern: function (e, r, t, n, a) {
      var i = []
      if (e.required || (!e.required && n.hasOwnProperty(e.field))) {
        if (he(r, 'string') && !e.required) return t()
        ;(Pe.required(e, r, n, i, a), he(r, 'string') || Pe.pattern(e, r, n, i, a))
      }
      t(i)
    },
    date: function (e, r, t, n, a) {
      var i = []
      if (e.required || (!e.required && n.hasOwnProperty(e.field))) {
        if (he(r, 'date') && !e.required) return t()
        var s
        if ((Pe.required(e, r, n, i, a), !he(r, 'date')))
          ((s = r instanceof Date ? r : new Date(r)),
            Pe.type(e, s, n, i, a),
            s && Pe.range(e, s.getTime(), n, i, a))
      }
      t(i)
    },
    url: ke,
    hex: ke,
    email: ke,
    required: function (e, r, t, n, a) {
      var i = [],
        s = Array.isArray(r) ? 'array' : typeof r
      ;(Pe.required(e, r, n, i, a, s), t(i))
    },
    any: function (e, r, t, n, a) {
      var i = []
      if (e.required || (!e.required && n.hasOwnProperty(e.field))) {
        if (he(r) && !e.required) return t()
        Pe.required(e, r, n, i, a)
      }
      t(i)
    }
  }
function Re() {
  return {
    default: 'Validation error on field %s',
    required: '%s is required',
    enum: '%s must be one of %s',
    whitespace: '%s cannot be empty',
    date: {
      format: '%s date %s is invalid for format %s',
      parse: '%s date could not be parsed, %s is invalid ',
      invalid: '%s date %s is invalid'
    },
    types: {
      string: '%s is not a %s',
      method: '%s is not a %s (function)',
      array: '%s is not an %s',
      object: '%s is not an %s',
      number: '%s is not a %s',
      date: '%s is not a %s',
      boolean: '%s is not a %s',
      integer: '%s is not an %s',
      float: '%s is not a %s',
      regexp: '%s is not a valid %s',
      email: '%s is not a valid %s',
      url: '%s is not a valid %s',
      hex: '%s is not a valid %s'
    },
    string: {
      len: '%s must be exactly %s characters',
      min: '%s must be at least %s characters',
      max: '%s cannot be longer than %s characters',
      range: '%s must be between %s and %s characters'
    },
    number: {
      len: '%s must equal %s',
      min: '%s cannot be less than %s',
      max: '%s cannot be greater than %s',
      range: '%s must be between %s and %s'
    },
    array: {
      len: '%s must be exactly %s in length',
      min: '%s cannot be less than %s in length',
      max: '%s cannot be greater than %s in length',
      range: '%s must be between %s and %s in length'
    },
    pattern: { mismatch: '%s value %s does not match pattern %s' },
    clone: function () {
      var e = JSON.parse(JSON.stringify(this))
      return ((e.clone = this.clone), e)
    }
  }
}
var $e = Re(),
  _e = (function () {
    function e(e) {
      ;((this.rules = null), (this._messages = $e), this.define(e))
    }
    var r = e.prototype
    return (
      (r.define = function (e) {
        var r = this
        if (!e) throw new Error('Cannot configure a schema with no rules')
        if ('object' != typeof e || Array.isArray(e)) throw new Error('Rules must be an object')
        ;((this.rules = {}),
          Object.keys(e).forEach(function (t) {
            var n = e[t]
            r.rules[t] = Array.isArray(n) ? n : [n]
          }))
      }),
      (r.messages = function (e) {
        return (e && (this._messages = qe(Re(), e)), this._messages)
      }),
      (r.validate = function (r, t, n) {
        var a = this
        ;(void 0 === t && (t = {}), void 0 === n && (n = function () {}))
        var i = r,
          s = t,
          l = n
        if (
          ('function' == typeof s && ((l = s), (s = {})),
          !this.rules || 0 === Object.keys(this.rules).length)
        )
          return (l && l(null, i), Promise.resolve(i))
        if (s.messages) {
          var u = this.messages()
          ;(u === $e && (u = Re()), qe(u, s.messages), (s.messages = u))
        } else s.messages = this.messages()
        var o = {}
        ;(s.keys || Object.keys(this.rules)).forEach(function (e) {
          var t = a.rules[e],
            n = i[e]
          t.forEach(function (t) {
            var s = t
            ;('function' == typeof s.transform &&
              (i === r && (i = le({}, i)), (n = i[e] = s.transform(n))),
              ((s = 'function' == typeof s ? { validator: s } : le({}, s)).validator =
                a.getValidationMethod(s)),
              s.validator &&
                ((s.field = e),
                (s.fullField = s.fullField || e),
                (s.type = a.getType(s)),
                (o[e] = o[e] || []),
                o[e].push({ rule: s, value: n, source: i, field: e })))
          })
        })
        var f = {}
        return be(
          o,
          s,
          function (r, t) {
            var n,
              a = r.rule,
              l = !(
                ('object' !== a.type && 'array' !== a.type) ||
                ('object' != typeof a.fields && 'object' != typeof a.defaultField)
              )
            function u(e, r) {
              return le({}, r, {
                fullField: a.fullField + '.' + e,
                fullFields: a.fullFields ? [].concat(a.fullFields, [e]) : [e]
              })
            }
            function o(n) {
              void 0 === n && (n = [])
              var o = Array.isArray(n) ? n : [n]
              ;(!s.suppressWarning && o.length && e.warning('async-validator:', o),
                o.length && void 0 !== a.message && (o = [].concat(a.message)))
              var d = o.map(we(a, i))
              if (s.first && d.length) return ((f[a.field] = 1), t(d))
              if (l) {
                if (a.required && !r.value)
                  return (
                    void 0 !== a.message
                      ? (d = [].concat(a.message).map(we(a, i)))
                      : s.error && (d = [s.error(a, ge(s.messages.required, a.field))]),
                    t(d)
                  )
                var c = {}
                ;(a.defaultField &&
                  Object.keys(r.value).map(function (e) {
                    c[e] = a.defaultField
                  }),
                  (c = le({}, c, r.rule.fields)))
                var p = {}
                Object.keys(c).forEach(function (e) {
                  var r = c[e],
                    t = Array.isArray(r) ? r : [r]
                  p[e] = t.map(u.bind(null, e))
                })
                var v = new e(p)
                ;(v.messages(s.messages),
                  r.rule.options &&
                    ((r.rule.options.messages = s.messages), (r.rule.options.error = s.error)),
                  v.validate(r.value, r.rule.options || s, function (e) {
                    var r = []
                    ;(d && d.length && r.push.apply(r, d),
                      e && e.length && r.push.apply(r, e),
                      t(r.length ? r : null))
                  }))
              } else t(d)
            }
            if (
              ((l = l && (a.required || (!a.required && r.value))),
              (a.field = r.field),
              a.asyncValidator)
            )
              n = a.asyncValidator(a, r.value, o, r.source, s)
            else if (a.validator) {
              try {
                n = a.validator(a, r.value, o, r.source, s)
              } catch (d) {
                ;(console.error,
                  s.suppressValidatorError ||
                    setTimeout(function () {
                      throw d
                    }, 0),
                  o(d.message))
              }
              !0 === n
                ? o()
                : !1 === n
                  ? o(
                      'function' == typeof a.message
                        ? a.message(a.fullField || a.field)
                        : a.message || (a.fullField || a.field) + ' fails'
                    )
                  : n instanceof Array
                    ? o(n)
                    : n instanceof Error && o(n.message)
            }
            n &&
              n.then &&
              n.then(
                function () {
                  return o()
                },
                function (e) {
                  return o(e)
                }
              )
          },
          function (e) {
            !(function (e) {
              for (var r, t, n = [], a = {}, s = 0; s < e.length; s++)
                ((r = e[s]),
                  (t = void 0),
                  Array.isArray(r) ? (n = (t = n).concat.apply(t, r)) : n.push(r))
              n.length ? ((a = ve(n)), l(n, a)) : l(null, i)
            })(e)
          },
          i
        )
      }),
      (r.getType = function (e) {
        if (
          (void 0 === e.type && e.pattern instanceof RegExp && (e.type = 'pattern'),
          'function' != typeof e.validator && e.type && !Se.hasOwnProperty(e.type))
        )
          throw new Error(ge('Unknown rule type %s', e.type))
        return e.type || 'string'
      }),
      (r.getValidationMethod = function (e) {
        if ('function' == typeof e.validator) return e.validator
        var r = Object.keys(e),
          t = r.indexOf('message')
        return (
          -1 !== t && r.splice(t, 1),
          1 === r.length && 'required' === r[0] ? Se.required : Se[this.getType(e)] || void 0
        )
      }),
      e
    )
  })()
;((_e.register = function (e, r) {
  if ('function' != typeof r)
    throw new Error('Cannot register a validator by type, validator is not a function')
  Se[e] = r
}),
  (_e.warning = pe),
  (_e.messages = $e),
  (_e.validators = Se))
const Me = t({
    label: String,
    labelWidth: { type: [String, Number], default: '' },
    prop: { type: a([String, Array]) },
    required: { type: Boolean, default: void 0 },
    rules: { type: a([Object, Array]) },
    error: String,
    validateStatus: { type: String, values: ['', 'error', 'validating', 'success'] },
    for: String,
    inlineMessage: { type: [String, Boolean], default: '' },
    showMessage: { type: Boolean, default: !0 },
    size: { type: String, values: n }
  }),
  We = 'ElLabelWrap'
var Be = f({
  name: We,
  props: { isAutoWidth: Boolean, updateAll: Boolean },
  setup(e, { slots: r }) {
    const t = E(m, void 0),
      n = E(A)
    n || P(We, 'usage: <el-form-item><label-wrap /></el-form-item>')
    const a = c('form'),
      i = u(),
      s = u(0),
      l = (n = 'update') => {
        W(() => {
          r.default &&
            e.isAutoWidth &&
            ('update' === n
              ? (s.value = (() => {
                  var e
                  if (null == (e = i.value) ? void 0 : e.firstElementChild) {
                    const e = window.getComputedStyle(i.value.firstElementChild).width
                    return Math.ceil(Number.parseFloat(e))
                  }
                  return 0
                })())
              : 'remove' === n && (null == t || t.deregisterLabelWidth(s.value)))
        })
      },
      f = () => l('update')
    return (
      k(() => {
        f()
      }),
      S(() => {
        l('remove')
      }),
      R(() => f()),
      p(s, (r, n) => {
        e.updateAll && (null == t || t.registerLabelWidth(r, n))
      }),
      $(
        o(() => {
          var e, r
          return null != (r = null == (e = i.value) ? void 0 : e.firstElementChild) ? r : null
        }),
        f
      ),
      () => {
        var l, u
        if (!r) return null
        const { isAutoWidth: o } = e
        if (o) {
          const e = null == t ? void 0 : t.autoLabelWidth,
            u = {}
          if ((null == n ? void 0 : n.hasLabel) && e && 'auto' !== e) {
            const r = Math.max(0, Number.parseInt(e, 10) - s.value),
              n = 'left' === t.labelPosition ? 'marginRight' : 'marginLeft'
            r && (u[n] = `${r}px`)
          }
          return _('div', { ref: i, class: [a.be('item', 'label-wrap')], style: u }, [
            null == (l = r.default) ? void 0 : l.call(r)
          ])
        }
        return _(M, { ref: i }, [null == (u = r.default) ? void 0 : u.call(r)])
      }
    )
  }
})
const Ie = ['role', 'aria-labelledby'],
  Ve = f({ name: 'ElFormItem' })
var ze = x(
  f({
    ...Ve,
    props: Me,
    setup(e, { expose: r }) {
      const t = e,
        n = B(),
        a = E(m, void 0),
        i = E(A, void 0),
        f = d(void 0, { formItem: !1 }),
        v = c('form-item'),
        x = I().value,
        P = u([]),
        R = u(''),
        $ = V(R, 100),
        M = u(''),
        Y = u()
      let H,
        ee = !1
      const re = o(() => {
          if ('top' === (null == a ? void 0 : a.labelPosition)) return {}
          const e = z(t.labelWidth || (null == a ? void 0 : a.labelWidth) || '')
          return e ? { width: e } : {}
        }),
        te = o(() => {
          if ('top' === (null == a ? void 0 : a.labelPosition) || (null == a ? void 0 : a.inline))
            return {}
          if (!t.label && !t.labelWidth && fe) return {}
          const e = z(t.labelWidth || (null == a ? void 0 : a.labelWidth) || '')
          return t.label || n.label ? {} : { marginLeft: e }
        }),
        ne = o(() => [
          v.b(),
          v.m(f.value),
          v.is('error', 'error' === R.value),
          v.is('validating', 'validating' === R.value),
          v.is('success', 'success' === R.value),
          v.is('required', ve.value || t.required),
          v.is('no-asterisk', null == a ? void 0 : a.hideRequiredAsterisk),
          'right' === (null == a ? void 0 : a.requireAsteriskPosition)
            ? 'asterisk-right'
            : 'asterisk-left',
          { [v.m('feedback')]: null == a ? void 0 : a.statusIcon }
        ]),
        ae = o(() =>
          l(t.inlineMessage) ? t.inlineMessage : (null == a ? void 0 : a.inlineMessage) || !1
        ),
        ie = o(() => [v.e('error'), { [v.em('error', 'inline')]: ae.value }]),
        se = o(() => (t.prop ? (s(t.prop) ? t.prop : t.prop.join('.')) : '')),
        le = o(() => !(!t.label && !n.label)),
        ue = o(() => (t.for || 1 === P.value.length ? P.value[0] : void 0)),
        oe = o(() => !ue.value && le.value),
        fe = !!i,
        de = o(() => {
          const e = null == a ? void 0 : a.model
          if (e && t.prop) return L(e, t.prop).value
        }),
        ce = o(() => {
          const { required: e } = t,
            r = []
          t.rules && r.push(...Q(t.rules))
          const n = null == a ? void 0 : a.rules
          if (n && t.prop) {
            const e = L(n, t.prop).value
            e && r.push(...Q(e))
          }
          if (void 0 !== e) {
            const t = r.map((e, r) => [e, r]).filter(([e]) => Object.keys(e).includes('required'))
            if (t.length > 0)
              for (const [n, a] of t) n.required !== e && (r[a] = { ...n, required: e })
            else r.push({ required: e })
          }
          return r
        }),
        pe = o(() => ce.value.length > 0),
        ve = o(() => ce.value.some((e) => e.required)),
        ge = o(() => {
          var e
          return (
            'error' === $.value &&
            t.showMessage &&
            (null == (e = null == a ? void 0 : a.showMessage) || e)
          )
        }),
        he = o(() => `${t.label || ''}${(null == a ? void 0 : a.labelSuffix) || ''}`),
        ye = (e) => {
          R.value = e
        },
        me = async (e) => {
          const r = se.value
          return new _e({ [r]: e })
            .validate({ [r]: de.value }, { firstFields: !0 })
            .then(() => (ye('success'), null == a || a.emit('validate', t.prop, !0, ''), !0))
            .catch(
              (e) => (
                ((e) => {
                  var r, n
                  const { errors: i, fields: s } = e
                  ;(ye('error'),
                    (M.value = i
                      ? null != (n = null == (r = null == i ? void 0 : i[0]) ? void 0 : r.message)
                        ? n
                        : `${t.prop} is required`
                      : ''),
                    null == a || a.emit('validate', t.prop, !1, M.value))
                })(e),
                Promise.reject(e)
              )
            )
        },
        be = async (e, r) => {
          if (ee || !t.prop) return !1
          const n = j(r)
          if (!pe.value) return (null == r || r(!1), !1)
          const a = ((e) =>
            ce.value
              .filter(
                (r) =>
                  !r.trigger ||
                  !e ||
                  (Array.isArray(r.trigger) ? r.trigger.includes(e) : r.trigger === e)
              )
              .map(({ trigger: e, ...r }) => r))(e)
          return 0 === a.length
            ? (null == r || r(!0), !0)
            : (ye('validating'),
              me(a)
                .then(() => (null == r || r(!0), !0))
                .catch((e) => {
                  const { fields: t } = e
                  return (null == r || r(!1, t), !n && Promise.reject(t))
                }))
        },
        we = () => {
          ;(ye(''), (M.value = ''), (ee = !1))
        },
        qe = async () => {
          const e = null == a ? void 0 : a.model
          if (!e || !t.prop) return
          const r = L(e, t.prop)
          ;((ee = !0), (r.value = X(H)), await W(), we(), (ee = !1))
        }
      ;(p(
        () => t.error,
        (e) => {
          ;((M.value = e || ''), ye(e ? 'error' : ''))
        },
        { immediate: !0 }
      ),
        p(
          () => t.validateStatus,
          (e) => ye(e || '')
        ))
      const Fe = h({
        ...y(t),
        $el: Y,
        size: f,
        validateState: R,
        labelId: x,
        inputIds: P,
        isGroup: oe,
        hasLabel: le,
        addInputId: (e) => {
          P.value.includes(e) || P.value.push(e)
        },
        removeInputId: (e) => {
          P.value = P.value.filter((r) => r !== e)
        },
        resetField: qe,
        clearValidate: we,
        validate: be
      })
      return (
        g(A, Fe),
        k(() => {
          t.prop && (null == a || a.addField(Fe), (H = X(de.value)))
        }),
        S(() => {
          null == a || a.removeField(Fe)
        }),
        r({
          size: f,
          validateMessage: M,
          validateState: R,
          validate: be,
          clearValidate: we,
          resetField: qe
        }),
        (e, r) => {
          var t
          return (
            b(),
            w(
              'div',
              {
                ref_key: 'formItemRef',
                ref: Y,
                class: F(O(ne)),
                role: O(oe) ? 'group' : void 0,
                'aria-labelledby': O(oe) ? O(x) : void 0
              },
              [
                _(
                  O(Be),
                  {
                    'is-auto-width': 'auto' === O(re).width,
                    'update-all': 'auto' === (null == (t = O(a)) ? void 0 : t.labelWidth)
                  },
                  {
                    default: N(() => [
                      O(le)
                        ? (b(),
                          C(
                            D(O(ue) ? 'label' : 'div'),
                            {
                              key: 0,
                              id: O(x),
                              for: O(ue),
                              class: F(O(v).e('label')),
                              style: T(O(re))
                            },
                            {
                              default: N(() => [
                                q(e.$slots, 'label', { label: O(he) }, () => [J(Z(O(he)), 1)])
                              ]),
                              _: 3
                            },
                            8,
                            ['id', 'for', 'class', 'style']
                          ))
                        : G('v-if', !0)
                    ]),
                    _: 3
                  },
                  8,
                  ['is-auto-width', 'update-all']
                ),
                K(
                  'div',
                  { class: F(O(v).e('content')), style: T(O(te)) },
                  [
                    q(e.$slots, 'default'),
                    _(
                      U,
                      { name: `${O(v).namespace.value}-zoom-in-top` },
                      {
                        default: N(() => [
                          O(ge)
                            ? q(e.$slots, 'error', { key: 0, error: M.value }, () => [
                                K('div', { class: F(O(ie)) }, Z(M.value), 3)
                              ])
                            : G('v-if', !0)
                        ]),
                        _: 3
                      },
                      8,
                      ['name']
                    )
                  ],
                  6
                )
              ],
              10,
              Ie
            )
          )
        }
      )
    }
  }),
  [
    [
      '__file',
      '/home/runner/work/element-plus/element-plus/packages/components/form/src/form-item.vue'
    ]
  ]
)
const Le = Y(se, { FormItem: ze }),
  Ne = H(ze)
export { Le as E, Ne as a }
