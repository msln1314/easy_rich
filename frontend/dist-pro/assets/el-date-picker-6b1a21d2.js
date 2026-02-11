import { d as e } from './dayjs.min-e5ba30ae.js'
import {
  a9 as a,
  aa as t,
  b2 as l,
  ce as n,
  aZ as o,
  b as r,
  d as s,
  bc as u,
  b6 as i,
  e as d,
  aT as c,
  a_ as v,
  u as p,
  b8 as m,
  ao as f,
  r as h,
  f as y,
  w as b,
  as as g,
  ba as k,
  bz as w,
  cf as D,
  b9 as x,
  k as S,
  aV as M,
  am as C,
  o as P,
  l as _,
  m as V,
  s as $,
  n as O,
  aY as Y,
  E as I,
  p as A,
  F as N,
  j as T,
  y as R,
  q as E,
  z as B,
  a6 as L,
  _ as F,
  aA as j,
  b3 as z,
  cg as W,
  a2 as H,
  a1 as K,
  a5 as U,
  M as q,
  G,
  a0 as Z,
  x as X,
  bk as Q,
  bd as J,
  aD as ee,
  D as ae,
  ch as te,
  aX as le,
  bq as ne,
  aE as oe,
  a4 as re,
  aH as se,
  ci as ue,
  ax as ie,
  ay as de,
  cj as ce,
  N as ve,
  aq as pe,
  L as me
} from './index-820a519e.js'
import { E as fe } from './el-input-5ae17c8f.js'
import { E as he, T as ye } from './el-popper-797844d6.js'
import { d as be } from './debounce-5bc596c6.js'
import { C as ge } from './index-eb31d854.js'
import { i as ke } from './isEqual-cb9e370d.js'
const we = (e) => [...new Set(e)],
  De = (e) => (e || 0 === e ? (Array.isArray(e) ? e : [e]) : [])
var xe = { exports: {} }
xe.exports = (function () {
  var e = {
      LTS: 'h:mm:ss A',
      LT: 'h:mm A',
      L: 'MM/DD/YYYY',
      LL: 'MMMM D, YYYY',
      LLL: 'MMMM D, YYYY h:mm A',
      LLLL: 'dddd, MMMM D, YYYY h:mm A'
    },
    a = /(\[[^[]*\])|([-_:/.,()\s]+)|(A|a|YYYY|YY?|MM?M?M?|Do|DD?|hh?|HH?|mm?|ss?|S{1,3}|z|ZZ?)/g,
    t = /\d\d/,
    l = /\d\d?/,
    n = /\d*[^-_:/,()\s\d]+/,
    o = {},
    r = function (e) {
      return (e = +e) + (e > 68 ? 1900 : 2e3)
    },
    s = function (e) {
      return function (a) {
        this[e] = +a
      }
    },
    u = [
      /[+-]\d\d:?(\d\d)?|Z/,
      function (e) {
        ;(this.zone || (this.zone = {})).offset = (function (e) {
          if (!e) return 0
          if ('Z' === e) return 0
          var a = e.match(/([+-]|\d\d)/g),
            t = 60 * a[1] + (+a[2] || 0)
          return 0 === t ? 0 : '+' === a[0] ? -t : t
        })(e)
      }
    ],
    i = function (e) {
      var a = o[e]
      return a && (a.indexOf ? a : a.s.concat(a.f))
    },
    d = function (e, a) {
      var t,
        l = o.meridiem
      if (l) {
        for (var n = 1; n <= 24; n += 1)
          if (e.indexOf(l(n, 0, a)) > -1) {
            t = n > 12
            break
          }
      } else t = e === (a ? 'pm' : 'PM')
      return t
    },
    c = {
      A: [
        n,
        function (e) {
          this.afternoon = d(e, !1)
        }
      ],
      a: [
        n,
        function (e) {
          this.afternoon = d(e, !0)
        }
      ],
      S: [
        /\d/,
        function (e) {
          this.milliseconds = 100 * +e
        }
      ],
      SS: [
        t,
        function (e) {
          this.milliseconds = 10 * +e
        }
      ],
      SSS: [
        /\d{3}/,
        function (e) {
          this.milliseconds = +e
        }
      ],
      s: [l, s('seconds')],
      ss: [l, s('seconds')],
      m: [l, s('minutes')],
      mm: [l, s('minutes')],
      H: [l, s('hours')],
      h: [l, s('hours')],
      HH: [l, s('hours')],
      hh: [l, s('hours')],
      D: [l, s('day')],
      DD: [t, s('day')],
      Do: [
        n,
        function (e) {
          var a = o.ordinal,
            t = e.match(/\d+/)
          if (((this.day = t[0]), a))
            for (var l = 1; l <= 31; l += 1) a(l).replace(/\[|\]/g, '') === e && (this.day = l)
        }
      ],
      M: [l, s('month')],
      MM: [t, s('month')],
      MMM: [
        n,
        function (e) {
          var a = i('months'),
            t =
              (
                i('monthsShort') ||
                a.map(function (e) {
                  return e.slice(0, 3)
                })
              ).indexOf(e) + 1
          if (t < 1) throw new Error()
          this.month = t % 12 || t
        }
      ],
      MMMM: [
        n,
        function (e) {
          var a = i('months').indexOf(e) + 1
          if (a < 1) throw new Error()
          this.month = a % 12 || a
        }
      ],
      Y: [/[+-]?\d+/, s('year')],
      YY: [
        t,
        function (e) {
          this.year = r(e)
        }
      ],
      YYYY: [/\d{4}/, s('year')],
      Z: u,
      ZZ: u
    }
  function v(t) {
    var l, n
    ;((l = t), (n = o && o.formats))
    for (
      var r = (t = l.replace(/(\[[^\]]+])|(LTS?|l{1,4}|L{1,4})/g, function (a, t, l) {
          var o = l && l.toUpperCase()
          return (
            t ||
            n[l] ||
            e[l] ||
            n[o].replace(/(\[[^\]]+])|(MMMM|MM|DD|dddd)/g, function (e, a, t) {
              return a || t.slice(1)
            })
          )
        })).match(a),
        s = r.length,
        u = 0;
      u < s;
      u += 1
    ) {
      var i = r[u],
        d = c[i],
        v = d && d[0],
        p = d && d[1]
      r[u] = p ? { regex: v, parser: p } : i.replace(/^\[|\]$/g, '')
    }
    return function (e) {
      for (var a = {}, t = 0, l = 0; t < s; t += 1) {
        var n = r[t]
        if ('string' == typeof n) l += n.length
        else {
          var o = n.regex,
            u = n.parser,
            i = e.slice(l),
            d = o.exec(i)[0]
          ;(u.call(a, d), (e = e.replace(d, '')))
        }
      }
      return (
        (function (e) {
          var a = e.afternoon
          if (void 0 !== a) {
            var t = e.hours
            ;(a ? t < 12 && (e.hours += 12) : 12 === t && (e.hours = 0), delete e.afternoon)
          }
        })(a),
        a
      )
    }
  }
  return function (e, a, t) {
    ;((t.p.customParseFormat = !0), e && e.parseTwoDigitYear && (r = e.parseTwoDigitYear))
    var l = a.prototype,
      n = l.parse
    l.parse = function (e) {
      var a = e.date,
        l = e.utc,
        r = e.args
      this.$u = l
      var s = r[1]
      if ('string' == typeof s) {
        var u = !0 === r[2],
          i = !0 === r[3],
          d = u || i,
          c = r[2]
        ;(i && (c = r[2]),
          (o = this.$locale()),
          !u && c && (o = t.Ls[c]),
          (this.$d = (function (e, a, t) {
            try {
              if (['x', 'X'].indexOf(a) > -1) return new Date(('X' === a ? 1e3 : 1) * e)
              var l = v(a)(e),
                n = l.year,
                o = l.month,
                r = l.day,
                s = l.hours,
                u = l.minutes,
                i = l.seconds,
                d = l.milliseconds,
                c = l.zone,
                p = new Date(),
                m = r || (n || o ? 1 : p.getDate()),
                f = n || p.getFullYear(),
                h = 0
              ;(n && !o) || (h = o > 0 ? o - 1 : p.getMonth())
              var y = s || 0,
                b = u || 0,
                g = i || 0,
                k = d || 0
              return c
                ? new Date(Date.UTC(f, h, m, y, b, g, k + 60 * c.offset * 1e3))
                : t
                  ? new Date(Date.UTC(f, h, m, y, b, g, k))
                  : new Date(f, h, m, y, b, g, k)
            } catch (w) {
              return new Date('')
            }
          })(a, s, l)),
          this.init(),
          c && !0 !== c && (this.$L = this.locale(c).$L),
          d && a != this.format(s) && (this.$d = new Date('')),
          (o = {}))
      } else if (s instanceof Array)
        for (var p = s.length, m = 1; m <= p; m += 1) {
          r[1] = s[m - 1]
          var f = t.apply(this, r)
          if (f.isValid()) {
            ;((this.$d = f.$d), (this.$L = f.$L), this.init())
            break
          }
          m === p && (this.$d = new Date(''))
        }
      else n.call(this, e)
    }
  }
})()
const Se = t(xe.exports),
  Me = ['hours', 'minutes', 'seconds'],
  Ce = 'HH:mm:ss',
  Pe = 'YYYY-MM-DD',
  _e = {
    date: Pe,
    dates: Pe,
    week: 'gggg[w]ww',
    year: 'YYYY',
    month: 'YYYY-MM',
    datetime: `${Pe} ${Ce}`,
    monthrange: 'YYYY-MM',
    daterange: Pe,
    datetimerange: `${Pe} ${Ce}`
  },
  Ve = (e, a) => [e > 0 ? e - 1 : void 0, e, e < a ? e + 1 : void 0],
  $e = (e) => Array.from(Array.from({ length: e }).keys()),
  Oe = (e) =>
    e
      .replace(/\W?m{1,2}|\W?ZZ/g, '')
      .replace(/\W?h{1,2}|\W?s{1,3}|\W?a/gi, '')
      .trim(),
  Ye = (e) => e.replace(/\W?D{1,2}|\W?Do|\W?d{1,4}|\W?M{1,4}|\W?Y{2,4}/g, '').trim(),
  Ie = function (e, a) {
    const t = n(e),
      l = n(a)
    return t && l ? e.getTime() === a.getTime() : !t && !l && e === a
  },
  Ae = function (e, a) {
    const t = o(e),
      l = o(a)
    return t && l ? e.length === a.length && e.every((e, t) => Ie(e, a[t])) : !t && !l && Ie(e, a)
  },
  Ne = function (a, t, n) {
    const o = l(t) || 'x' === t ? e(a).locale(n) : e(a, t).locale(n)
    return o.isValid() ? o : void 0
  },
  Te = function (a, t, n) {
    return l(t) ? a : 'x' === t ? +a : e(a).locale(n).format(t)
  },
  Re = (e, a) => {
    var t
    const l = [],
      n = null == a ? void 0 : a()
    for (let o = 0; o < e; o++) l.push(null != (t = null == n ? void 0 : n.includes(o)) && t)
    return l
  },
  Ee = r({
    disabledHours: { type: s(Function) },
    disabledMinutes: { type: s(Function) },
    disabledSeconds: { type: s(Function) }
  }),
  Be = r({
    visible: Boolean,
    actualVisible: { type: Boolean, default: void 0 },
    format: { type: String, default: '' }
  }),
  Le = r({
    id: { type: s([Array, String]) },
    name: { type: s([Array, String]), default: '' },
    popperClass: { type: String, default: '' },
    format: String,
    valueFormat: String,
    type: { type: String, default: '' },
    clearable: { type: Boolean, default: !0 },
    clearIcon: { type: s([String, Object]), default: u },
    editable: { type: Boolean, default: !0 },
    prefixIcon: { type: s([String, Object]), default: '' },
    size: i,
    readonly: { type: Boolean, default: !1 },
    disabled: { type: Boolean, default: !1 },
    placeholder: { type: String, default: '' },
    popperOptions: { type: s(Object), default: () => ({}) },
    modelValue: { type: s([Date, Array, String, Number]), default: '' },
    rangeSeparator: { type: String, default: '-' },
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
    unlinkPanels: Boolean
  }),
  Fe = ['id', 'name', 'placeholder', 'value', 'disabled', 'readonly'],
  je = ['id', 'name', 'placeholder', 'value', 'disabled', 'readonly'],
  ze = d({ name: 'Picker' }),
  We = d({
    ...ze,
    props: Le,
    emits: [
      'update:modelValue',
      'change',
      'focus',
      'blur',
      'calendar-change',
      'panel-change',
      'visible-change',
      'keydown'
    ],
    setup(e, { expose: a, emit: t }) {
      const l = e,
        n = c(),
        { lang: r } = v(),
        s = p('date'),
        u = p('input'),
        i = p('range'),
        { form: d, formItem: F } = m(),
        z = f('ElPopperOptions', {}),
        W = h(),
        H = h(),
        K = h(!1),
        U = h(!1),
        q = h(null)
      let G = !1,
        Z = !1
      const X = y(() => [
          s.b('editor'),
          s.bm('editor', l.type),
          u.e('wrapper'),
          s.is('disabled', ve.value),
          s.is('active', K.value),
          i.b('editor'),
          $e ? i.bm('editor', $e.value) : '',
          n.class
        ]),
        Q = y(() => [u.e('icon'), i.e('close-icon'), De.value ? '' : i.e('close-icon--hidden')])
      b(K, (e) => {
        e
          ? g(() => {
              e && (q.value = l.modelValue)
            })
          : ((Ie.value = null),
            g(() => {
              J(l.modelValue)
            }))
      })
      const J = (e, a) => {
          ;(!a && Ae(e, q.value)) ||
            (t('change', e),
            l.validateEvent && (null == F || F.validate('change').catch((e) => k())))
        },
        ee = (e) => {
          if (!Ae(l.modelValue, e)) {
            let a
            ;(o(e)
              ? (a = e.map((e) => Te(e, l.valueFormat, r.value)))
              : e && (a = Te(e, l.valueFormat, r.value)),
              t('update:modelValue', e ? a : e, r.value))
          }
        },
        ae = y(() => {
          if (H.value) {
            const e = Ve.value ? H.value : H.value.$el
            return Array.from(e.querySelectorAll('input'))
          }
          return []
        }),
        te = (e, a, t) => {
          const l = ae.value
          l.length &&
            (t && 'min' !== t
              ? 'max' === t && (l[1].setSelectionRange(e, a), l[1].focus())
              : (l[0].setSelectionRange(e, a), l[0].focus()))
        },
        le = (e = '', a = !1) => {
          let t
          ;(a || (Z = !0),
            (K.value = a),
            (t = o(e) ? e.map((e) => e.toDate()) : e ? e.toDate() : e),
            (Ie.value = null),
            ee(t))
        },
        ne = () => {
          U.value = !0
        },
        oe = () => {
          t('visible-change', !0)
        },
        re = (e) => {
          ;(null == e ? void 0 : e.key) === j.esc && ue(!0, !0)
        },
        se = () => {
          ;((U.value = !1), (K.value = !1), (Z = !1), t('visible-change', !1))
        },
        ue = (e = !0, a = !1) => {
          Z = a
          const [t, l] = S(ae)
          let n = t
          ;(!e && Ve.value && (n = l), n && n.focus())
        },
        ie = (e) => {
          l.readonly || ve.value || K.value || Z || ((K.value = !0), t('focus', e))
        }
      let de
      const ce = (e) => {
          const a = async () => {
            setTimeout(() => {
              var n
              de === a &&
                (((null == (n = W.value) ? void 0 : n.isFocusInsideContent()) && !G) ||
                  0 !== ae.value.filter((e) => e.contains(document.activeElement)).length ||
                  (Re(),
                  (K.value = !1),
                  t('blur', e),
                  l.validateEvent && (null == F || F.validate('blur').catch((e) => k()))),
                (G = !1))
            }, 0)
          }
          ;((de = a), a())
        },
        ve = y(() => l.disabled || (null == d ? void 0 : d.disabled)),
        pe = y(() => {
          let e
          if (
            (Se.value
              ? Ge.value.getDefaultValue && (e = Ge.value.getDefaultValue())
              : (e = o(l.modelValue)
                  ? l.modelValue.map((e) => Ne(e, l.valueFormat, r.value))
                  : Ne(l.modelValue, l.valueFormat, r.value)),
            Ge.value.getRangeAvailableTime)
          ) {
            const a = Ge.value.getRangeAvailableTime(e)
            ke(a, e) || ((e = a), ee(o(e) ? e.map((e) => e.toDate()) : e.toDate()))
          }
          return (o(e) && e.some((e) => !e) && (e = []), e)
        }),
        me = y(() => {
          if (!Ge.value.panelReady) return ''
          const e = Be(pe.value)
          return o(Ie.value)
            ? [Ie.value[0] || (e && e[0]) || '', Ie.value[1] || (e && e[1]) || '']
            : null !== Ie.value
              ? Ie.value
              : (!be.value && Se.value) || (!K.value && Se.value)
                ? ''
                : e
                  ? ge.value
                    ? e.join(', ')
                    : e
                  : ''
        }),
        ye = y(() => l.type.includes('time')),
        be = y(() => l.type.startsWith('time')),
        ge = y(() => 'dates' === l.type),
        we = y(() => l.prefixIcon || (ye.value ? w : D)),
        De = h(!1),
        xe = (e) => {
          l.readonly ||
            ve.value ||
            (De.value &&
              (e.stopPropagation(),
              ue(!0, !0),
              g(() => {
                Z = !1
              }),
              ee(null),
              J(null, !0),
              (De.value = !1),
              (K.value = !1),
              Ge.value.handleClear && Ge.value.handleClear()))
        },
        Se = y(() => {
          const { modelValue: e } = l
          return !e || (o(e) && !e.filter(Boolean).length)
        }),
        Me = async (e) => {
          var a
          l.readonly ||
            ve.value ||
            (('INPUT' !== (null == (a = e.target) ? void 0 : a.tagName) ||
              ae.value.includes(document.activeElement)) &&
              (K.value = !0))
        },
        Ce = () => {
          l.readonly || ve.value || (!Se.value && l.clearable && (De.value = !0))
        },
        Pe = () => {
          De.value = !1
        },
        _e = (e) => {
          var a
          l.readonly ||
            ve.value ||
            (('INPUT' !== (null == (a = e.touches[0].target) ? void 0 : a.tagName) ||
              ae.value.includes(document.activeElement)) &&
              (K.value = !0))
        },
        Ve = y(() => l.type.includes('range')),
        $e = x(),
        Oe = y(() => {
          var e, a
          return null == (a = null == (e = S(W)) ? void 0 : e.popperRef) ? void 0 : a.contentRef
        }),
        Ye = y(() => {
          var e
          return S(Ve) ? S(H) : null == (e = S(H)) ? void 0 : e.$el
        })
      M(Ye, (e) => {
        const a = S(Oe),
          t = S(Ye)
        ;(a && (e.target === a || e.composedPath().includes(a))) ||
          e.target === t ||
          e.composedPath().includes(t) ||
          (K.value = !1)
      })
      const Ie = h(null),
        Re = () => {
          if (Ie.value) {
            const e = Ee(me.value)
            e && Le(e) && (ee(o(e) ? e.map((e) => e.toDate()) : e.toDate()), (Ie.value = null))
          }
          '' === Ie.value && (ee(null), J(null), (Ie.value = null))
        },
        Ee = (e) => (e ? Ge.value.parseUserInput(e) : null),
        Be = (e) => (e ? Ge.value.formatToString(e) : null),
        Le = (e) => Ge.value.isValidValue(e),
        ze = async (e) => {
          if (l.readonly || ve.value) return
          const { code: a } = e
          if ((t('keydown', e), a !== j.esc))
            if (
              a === j.down &&
              (Ge.value.handleFocusPicker && (e.preventDefault(), e.stopPropagation()),
              !1 === K.value && ((K.value = !0), await g()),
              Ge.value.handleFocusPicker)
            )
              Ge.value.handleFocusPicker()
            else {
              if (a !== j.tab)
                return a === j.enter || a === j.numpadEnter
                  ? ((null === Ie.value || '' === Ie.value || Le(Ee(me.value))) &&
                      (Re(), (K.value = !1)),
                    void e.stopPropagation())
                  : void (Ie.value
                      ? e.stopPropagation()
                      : Ge.value.handleKeydownInput && Ge.value.handleKeydownInput(e))
              G = !0
            }
          else !0 === K.value && ((K.value = !1), e.preventDefault(), e.stopPropagation())
        },
        We = (e) => {
          ;((Ie.value = e), K.value || (K.value = !0))
        },
        He = (e) => {
          const a = e.target
          Ie.value ? (Ie.value = [a.value, Ie.value[1]]) : (Ie.value = [a.value, null])
        },
        Ke = (e) => {
          const a = e.target
          Ie.value ? (Ie.value = [Ie.value[0], a.value]) : (Ie.value = [null, a.value])
        },
        Ue = () => {
          var e
          const a = Ie.value,
            t = Ee(a && a[0]),
            l = S(pe)
          if (t && t.isValid()) {
            Ie.value = [Be(t), (null == (e = me.value) ? void 0 : e[1]) || null]
            const a = [t, l && (l[1] || null)]
            Le(a) && (ee(a), (Ie.value = null))
          }
        },
        qe = () => {
          var e
          const a = S(Ie),
            t = Ee(a && a[1]),
            l = S(pe)
          if (t && t.isValid()) {
            Ie.value = [(null == (e = S(me)) ? void 0 : e[0]) || null, Be(t)]
            const a = [l && l[0], t]
            Le(a) && (ee(a), (Ie.value = null))
          }
        },
        Ge = h({}),
        Ze = (e) => {
          ;((Ge.value[e[0]] = e[1]), (Ge.value.panelReady = !0))
        },
        Xe = (e) => {
          t('calendar-change', e)
        },
        Qe = (e, a, l) => {
          t('panel-change', e, a, l)
        }
      return (
        C('EP_PICKER_BASE', { props: l }),
        a({
          focus: ue,
          handleFocusInput: ie,
          handleBlurInput: ce,
          handleOpen: () => {
            K.value = !0
          },
          handleClose: () => {
            K.value = !1
          },
          onPick: le
        }),
        (e, a) => (
          P(),
          _(
            S(he),
            L(
              {
                ref_key: 'refPopper',
                ref: W,
                visible: K.value,
                effect: 'light',
                pure: '',
                trigger: 'click'
              },
              e.$attrs,
              {
                role: 'dialog',
                teleported: '',
                transition: `${S(s).namespace.value}-zoom-in-top`,
                'popper-class': [`${S(s).namespace.value}-picker__popper`, e.popperClass],
                'popper-options': S(z),
                'fallback-placements': ['bottom', 'top', 'right', 'left'],
                'gpu-acceleration': !1,
                'stop-popper-mouse-event': !1,
                'hide-after': 0,
                persistent: '',
                onBeforeShow: ne,
                onShow: oe,
                onHide: se
              }
            ),
            {
              default: V(() => [
                S(Ve)
                  ? (P(),
                    T(
                      'div',
                      {
                        key: 1,
                        ref_key: 'inputRef',
                        ref: H,
                        class: $(S(X)),
                        style: O(e.$attrs.style),
                        onClick: ie,
                        onMouseenter: Ce,
                        onMouseleave: Pe,
                        onTouchstart: _e,
                        onKeydown: ze
                      },
                      [
                        S(we)
                          ? (P(),
                            _(
                              S(I),
                              {
                                key: 0,
                                class: $([S(u).e('icon'), S(i).e('icon')]),
                                onMousedown: Y(Me, ['prevent']),
                                onTouchstart: _e
                              },
                              { default: V(() => [(P(), _(A(S(we))))]), _: 1 },
                              8,
                              ['class', 'onMousedown']
                            ))
                          : N('v-if', !0),
                        R(
                          'input',
                          {
                            id: e.id && e.id[0],
                            autocomplete: 'off',
                            name: e.name && e.name[0],
                            placeholder: e.startPlaceholder,
                            value: S(me) && S(me)[0],
                            disabled: S(ve),
                            readonly: !e.editable || e.readonly,
                            class: $(S(i).b('input')),
                            onMousedown: Me,
                            onInput: He,
                            onChange: Ue,
                            onFocus: ie,
                            onBlur: ce
                          },
                          null,
                          42,
                          Fe
                        ),
                        E(e.$slots, 'range-separator', {}, () => [
                          R('span', { class: $(S(i).b('separator')) }, B(e.rangeSeparator), 3)
                        ]),
                        R(
                          'input',
                          {
                            id: e.id && e.id[1],
                            autocomplete: 'off',
                            name: e.name && e.name[1],
                            placeholder: e.endPlaceholder,
                            value: S(me) && S(me)[1],
                            disabled: S(ve),
                            readonly: !e.editable || e.readonly,
                            class: $(S(i).b('input')),
                            onMousedown: Me,
                            onFocus: ie,
                            onBlur: ce,
                            onInput: Ke,
                            onChange: qe
                          },
                          null,
                          42,
                          je
                        ),
                        e.clearIcon
                          ? (P(),
                            _(
                              S(I),
                              { key: 1, class: $(S(Q)), onClick: xe },
                              { default: V(() => [(P(), _(A(e.clearIcon)))]), _: 1 },
                              8,
                              ['class']
                            ))
                          : N('v-if', !0)
                      ],
                      38
                    ))
                  : (P(),
                    _(
                      S(fe),
                      {
                        key: 0,
                        id: e.id,
                        ref_key: 'inputRef',
                        ref: H,
                        'container-role': 'combobox',
                        'model-value': S(me),
                        name: e.name,
                        size: S($e),
                        disabled: S(ve),
                        placeholder: e.placeholder,
                        class: $([S(s).b('editor'), S(s).bm('editor', e.type), e.$attrs.class]),
                        style: O(e.$attrs.style),
                        readonly: !e.editable || e.readonly || S(ge) || 'week' === e.type,
                        label: e.label,
                        tabindex: e.tabindex,
                        'validate-event': !1,
                        onInput: We,
                        onFocus: ie,
                        onBlur: ce,
                        onKeydown: ze,
                        onChange: Re,
                        onMousedown: Me,
                        onMouseenter: Ce,
                        onMouseleave: Pe,
                        onTouchstart: _e,
                        onClick: a[0] || (a[0] = Y(() => {}, ['stop']))
                      },
                      {
                        prefix: V(() => [
                          S(we)
                            ? (P(),
                              _(
                                S(I),
                                {
                                  key: 0,
                                  class: $(S(u).e('icon')),
                                  onMousedown: Y(Me, ['prevent']),
                                  onTouchstart: _e
                                },
                                { default: V(() => [(P(), _(A(S(we))))]), _: 1 },
                                8,
                                ['class', 'onMousedown']
                              ))
                            : N('v-if', !0)
                        ]),
                        suffix: V(() => [
                          De.value && e.clearIcon
                            ? (P(),
                              _(
                                S(I),
                                {
                                  key: 0,
                                  class: $(`${S(u).e('icon')} clear-icon`),
                                  onClick: Y(xe, ['stop'])
                                },
                                { default: V(() => [(P(), _(A(e.clearIcon)))]), _: 1 },
                                8,
                                ['class', 'onClick']
                              ))
                            : N('v-if', !0)
                        ]),
                        _: 1
                      },
                      8,
                      [
                        'id',
                        'model-value',
                        'name',
                        'size',
                        'disabled',
                        'placeholder',
                        'class',
                        'style',
                        'readonly',
                        'label',
                        'tabindex',
                        'onKeydown'
                      ]
                    ))
              ]),
              content: V(() => [
                E(e.$slots, 'default', {
                  visible: K.value,
                  actualVisible: U.value,
                  parsedValue: S(pe),
                  format: e.format,
                  unlinkPanels: e.unlinkPanels,
                  type: e.type,
                  defaultValue: e.defaultValue,
                  onPick: le,
                  onSelectRange: te,
                  onSetPickerOption: Ze,
                  onCalendarChange: Xe,
                  onPanelChange: Qe,
                  onKeydown: re,
                  onMousedown: a[1] || (a[1] = Y(() => {}, ['stop']))
                })
              ]),
              _: 3
            },
            16,
            ['visible', 'transition', 'popper-class', 'popper-options']
          )
        )
      )
    }
  })
var He = F(We, [
  [
    '__file',
    '/home/runner/work/element-plus/element-plus/packages/components/time-picker/src/common/picker.vue'
  ]
])
const Ke = r({ ...Be, datetimeRole: String, parsedValue: { type: s(Object) } }),
  Ue = ({ getAvailableHours: e, getAvailableMinutes: a, getAvailableSeconds: t }) => {
    const l = {}
    return {
      timePickerOptions: l,
      getAvailableTime: (l, n, o, r) => {
        const s = { hour: e, minute: a, second: t }
        let u = l
        return (
          ['hour', 'minute', 'second'].forEach((e) => {
            if (s[e]) {
              let a
              const t = s[e]
              switch (e) {
                case 'minute':
                  a = t(u.hour(), n, r)
                  break
                case 'second':
                  a = t(u.hour(), u.minute(), n, r)
                  break
                default:
                  a = t(n, r)
              }
              if ((null == a ? void 0 : a.length) && !a.includes(u[e]())) {
                const t = o ? 0 : a.length - 1
                u = u[e](a[t])
              }
            }
          }),
          u
        )
      },
      onSetOption: ([e, a]) => {
        l[e] = a
      }
    }
  },
  qe = (e) => e.map((e, a) => e || a).filter((e) => !0 !== e),
  Ge = (e, a, t) => ({
    getHoursList: (a, t) => Re(24, e && (() => (null == e ? void 0 : e(a, t)))),
    getMinutesList: (e, t, l) => Re(60, a && (() => (null == a ? void 0 : a(e, t, l)))),
    getSecondsList: (e, a, l, n) => Re(60, t && (() => (null == t ? void 0 : t(e, a, l, n))))
  }),
  Ze = (e, a, t) => {
    const { getHoursList: l, getMinutesList: n, getSecondsList: o } = Ge(e, a, t)
    return {
      getAvailableHours: (e, a) => qe(l(e, a)),
      getAvailableMinutes: (e, a, t) => qe(n(e, a, t)),
      getAvailableSeconds: (e, a, t, l) => qe(o(e, a, t, l))
    }
  },
  Xe = (e) => {
    const a = h(e.parsedValue)
    return (
      b(
        () => e.visible,
        (t) => {
          t || (a.value = e.parsedValue)
        }
      ),
      a
    )
  },
  Qe = 100,
  Je = 600,
  ea = {
    beforeMount(e, a) {
      const t = a.value,
        { interval: l = Qe, delay: n = Je } = z(t) ? {} : t
      let o, r
      const s = () => (z(t) ? t() : t.handler()),
        u = () => {
          ;(r && (clearTimeout(r), (r = void 0)), o && (clearInterval(o), (o = void 0)))
        }
      e.addEventListener('mousedown', (e) => {
        0 === e.button &&
          (u(),
          s(),
          document.addEventListener('mouseup', () => u(), { once: !0 }),
          (r = setTimeout(() => {
            o = setInterval(() => {
              s()
            }, l)
          }, n)))
      })
    }
  },
  aa = r({
    role: { type: String, required: !0 },
    spinnerDate: { type: s(Object), required: !0 },
    showSeconds: { type: Boolean, default: !0 },
    arrowControl: Boolean,
    amPmMode: { type: s(String), default: '' },
    ...Ee
  }),
  ta = ['onClick'],
  la = ['onMouseenter']
var na = F(
  d({
    __name: 'basic-time-spinner',
    props: aa,
    emits: ['change', 'select-range', 'set-option'],
    setup(e, { emit: a }) {
      const t = e,
        l = p('time'),
        {
          getHoursList: n,
          getMinutesList: o,
          getSecondsList: r
        } = Ge(t.disabledHours, t.disabledMinutes, t.disabledSeconds)
      let s = !1
      const u = h(),
        i = { hours: h(), minutes: h(), seconds: h() },
        d = y(() => (t.showSeconds ? Me : Me.slice(0, 2))),
        c = y(() => {
          const { spinnerDate: e } = t
          return { hours: e.hour(), minutes: e.minute(), seconds: e.second() }
        }),
        v = y(() => {
          const { hours: e, minutes: a } = S(c)
          return { hours: n(t.role), minutes: o(e, t.role), seconds: r(e, a, t.role) }
        }),
        m = y(() => {
          const { hours: e, minutes: a, seconds: t } = S(c)
          return { hours: Ve(e, 23), minutes: Ve(a, 59), seconds: Ve(t, 59) }
        }),
        f = be((e) => {
          ;((s = !1), D(e))
        }, 200),
        k = (e) => {
          if (!!!t.amPmMode) return ''
          let a = e < 12 ? ' am' : ' pm'
          return ('A' === t.amPmMode && (a = a.toUpperCase()), a)
        },
        w = (e) => {
          let t
          switch (e) {
            case 'hours':
              t = [0, 2]
              break
            case 'minutes':
              t = [3, 5]
              break
            case 'seconds':
              t = [6, 8]
          }
          const [l, n] = t
          ;(a('select-range', l, n), (u.value = e))
        },
        D = (e) => {
          C(e, S(c)[e])
        },
        x = () => {
          ;(D('hours'), D('minutes'), D('seconds'))
        },
        M = (e) => e.querySelector(`.${l.namespace.value}-scrollbar__wrap`),
        C = (e, a) => {
          if (t.arrowControl) return
          const l = S(i[e])
          l && l.$el && (M(l.$el).scrollTop = Math.max(0, a * O(e)))
        },
        O = (e) => {
          const a = S(i[e]),
            t = null == a ? void 0 : a.$el.querySelector('li')
          return (t && Number.parseFloat(W(t, 'height'))) || 0
        },
        Y = () => {
          E(1)
        },
        A = () => {
          E(-1)
        },
        E = (e) => {
          u.value || w('hours')
          const a = u.value,
            t = S(c)[a],
            l = 'hours' === u.value ? 24 : 60,
            n = L(a, t, e, l)
          ;(F(a, n), C(a, n), g(() => w(a)))
        },
        L = (e, a, t, l) => {
          let n = (a + t + l) % l
          const o = S(v)[e]
          for (; o[n] && n !== a; ) n = (n + t + l) % l
          return n
        },
        F = (e, l) => {
          if (S(v)[e][l]) return
          const { hours: n, minutes: o, seconds: r } = S(c)
          let s
          switch (e) {
            case 'hours':
              s = t.spinnerDate.hour(l).minute(o).second(r)
              break
            case 'minutes':
              s = t.spinnerDate.hour(n).minute(l).second(r)
              break
            case 'seconds':
              s = t.spinnerDate.hour(n).minute(o).second(l)
          }
          a('change', s)
        },
        j = (e) => S(i[e]).$el.offsetHeight,
        z = () => {
          const e = (e) => {
            const a = S(i[e])
            a &&
              a.$el &&
              (M(a.$el).onscroll = () => {
                ;((e) => {
                  ;((s = !0), f(e))
                  const a = Math.min(
                    Math.round((M(S(i[e]).$el).scrollTop - (0.5 * j(e) - 10) / O(e) + 3) / O(e)),
                    'hours' === e ? 23 : 59
                  )
                  F(e, a)
                })(e)
              })
          }
          ;(e('hours'), e('minutes'), e('seconds'))
        }
      H(() => {
        g(() => {
          ;(!t.arrowControl && z(), x(), 'start' === t.role && w('hours'))
        })
      })
      return (
        a('set-option', [`${t.role}_scrollDown`, E]),
        a('set-option', [`${t.role}_emitSelectRange`, w]),
        b(
          () => t.spinnerDate,
          () => {
            s || x()
          }
        ),
        (e, a) => (
          P(),
          T(
            'div',
            { class: $([S(l).b('spinner'), { 'has-seconds': e.showSeconds }]) },
            [
              e.arrowControl
                ? N('v-if', !0)
                : (P(!0),
                  T(
                    K,
                    { key: 0 },
                    U(
                      S(d),
                      (a) => (
                        P(),
                        _(
                          S(G),
                          {
                            key: a,
                            ref_for: !0,
                            ref: (e) =>
                              ((e, a) => {
                                i[a].value = e
                              })(e, a),
                            class: $(S(l).be('spinner', 'wrapper')),
                            'wrap-style': 'max-height: inherit;',
                            'view-class': S(l).be('spinner', 'list'),
                            noresize: '',
                            tag: 'ul',
                            onMouseenter: (e) => w(a),
                            onMousemove: (e) => D(a)
                          },
                          {
                            default: V(() => [
                              (P(!0),
                              T(
                                K,
                                null,
                                U(
                                  S(v)[a],
                                  (t, n) => (
                                    P(),
                                    T(
                                      'li',
                                      {
                                        key: n,
                                        class: $([
                                          S(l).be('spinner', 'item'),
                                          S(l).is('active', n === S(c)[a]),
                                          S(l).is('disabled', t)
                                        ]),
                                        onClick: (e) =>
                                          ((e, { value: a, disabled: t }) => {
                                            t || (F(e, a), w(e), C(e, a))
                                          })(a, { value: n, disabled: t })
                                      },
                                      [
                                        'hours' === a
                                          ? (P(),
                                            T(
                                              K,
                                              { key: 0 },
                                              [
                                                q(
                                                  B(
                                                    ('0' + (e.amPmMode ? n % 12 || 12 : n)).slice(
                                                      -2
                                                    )
                                                  ) + B(k(n)),
                                                  1
                                                )
                                              ],
                                              64
                                            ))
                                          : (P(),
                                            T(K, { key: 1 }, [q(B(('0' + n).slice(-2)), 1)], 64))
                                      ],
                                      10,
                                      ta
                                    )
                                  )
                                ),
                                128
                              ))
                            ]),
                            _: 2
                          },
                          1032,
                          ['class', 'view-class', 'onMouseenter', 'onMousemove']
                        )
                      )
                    ),
                    128
                  )),
              e.arrowControl
                ? (P(!0),
                  T(
                    K,
                    { key: 1 },
                    U(
                      S(d),
                      (a) => (
                        P(),
                        T(
                          'div',
                          {
                            key: a,
                            class: $([S(l).be('spinner', 'wrapper'), S(l).is('arrow')]),
                            onMouseenter: (e) => w(a)
                          },
                          [
                            Z(
                              (P(),
                              _(
                                S(I),
                                { class: $(['arrow-up', S(l).be('spinner', 'arrow')]) },
                                { default: V(() => [X(S(Q))]), _: 1 },
                                8,
                                ['class']
                              )),
                              [[S(ea), A]]
                            ),
                            Z(
                              (P(),
                              _(
                                S(I),
                                { class: $(['arrow-down', S(l).be('spinner', 'arrow')]) },
                                { default: V(() => [X(S(J))]), _: 1 },
                                8,
                                ['class']
                              )),
                              [[S(ea), Y]]
                            ),
                            R(
                              'ul',
                              { class: $(S(l).be('spinner', 'list')) },
                              [
                                (P(!0),
                                T(
                                  K,
                                  null,
                                  U(
                                    S(m)[a],
                                    (t, n) => (
                                      P(),
                                      T(
                                        'li',
                                        {
                                          key: n,
                                          class: $([
                                            S(l).be('spinner', 'item'),
                                            S(l).is('active', t === S(c)[a]),
                                            S(l).is('disabled', S(v)[a][t])
                                          ])
                                        },
                                        [
                                          'number' == typeof t
                                            ? (P(),
                                              T(
                                                K,
                                                { key: 0 },
                                                [
                                                  'hours' === a
                                                    ? (P(),
                                                      T(
                                                        K,
                                                        { key: 0 },
                                                        [
                                                          q(
                                                            B(
                                                              (
                                                                '0' +
                                                                (e.amPmMode ? t % 12 || 12 : t)
                                                              ).slice(-2)
                                                            ) + B(k(t)),
                                                            1
                                                          )
                                                        ],
                                                        64
                                                      ))
                                                    : (P(),
                                                      T(
                                                        K,
                                                        { key: 1 },
                                                        [q(B(('0' + t).slice(-2)), 1)],
                                                        64
                                                      ))
                                                ],
                                                64
                                              ))
                                            : N('v-if', !0)
                                        ],
                                        2
                                      )
                                    )
                                  ),
                                  128
                                ))
                              ],
                              2
                            )
                          ],
                          42,
                          la
                        )
                      )
                    ),
                    128
                  ))
                : N('v-if', !0)
            ],
            2
          )
        )
      )
    }
  }),
  [
    [
      '__file',
      '/home/runner/work/element-plus/element-plus/packages/components/time-picker/src/time-picker-com/basic-time-spinner.vue'
    ]
  ]
)
const oa = d({
  __name: 'panel-time-pick',
  props: Ke,
  emits: ['pick', 'select-range', 'set-picker-option'],
  setup(a, { emit: t }) {
    const l = a,
      n = f('EP_PICKER_BASE'),
      {
        arrowControl: o,
        disabledHours: r,
        disabledMinutes: s,
        disabledSeconds: u,
        defaultValue: i
      } = n.props,
      { getAvailableHours: d, getAvailableMinutes: c, getAvailableSeconds: m } = Ze(r, s, u),
      b = p('time'),
      { t: g, lang: k } = v(),
      w = h([0, 2]),
      D = Xe(l),
      x = y(() => (ee(l.actualVisible) ? `${b.namespace.value}-zoom-in-top` : '')),
      M = y(() => l.format.includes('ss')),
      C = y(() => (l.format.includes('A') ? 'A' : l.format.includes('a') ? 'a' : '')),
      O = () => {
        t('pick', D.value, !1)
      },
      Y = (e) => {
        if (!l.visible) return
        const a = F(e).millisecond(0)
        t('pick', a, !0)
      },
      I = (e, a) => {
        ;(t('select-range', e, a), (w.value = [e, a]))
      },
      {
        timePickerOptions: A,
        onSetOption: E,
        getAvailableTime: L
      } = Ue({ getAvailableHours: d, getAvailableMinutes: c, getAvailableSeconds: m }),
      F = (e) => L(e, l.datetimeRole || '', !0)
    return (
      t('set-picker-option', [
        'isValidValue',
        (a) => {
          const t = e(a).locale(k.value),
            l = F(t)
          return t.isSame(l)
        }
      ]),
      t('set-picker-option', ['formatToString', (e) => (e ? e.format(l.format) : null)]),
      t('set-picker-option', [
        'parseUserInput',
        (a) => (a ? e(a, l.format).locale(k.value) : null)
      ]),
      t('set-picker-option', [
        'handleKeydownInput',
        (e) => {
          const a = e.code,
            { left: t, right: l, up: n, down: o } = j
          if ([t, l].includes(a)) {
            return (
              ((e) => {
                const a = [0, 3].concat(M.value ? [6] : []),
                  t = ['hours', 'minutes'].concat(M.value ? ['seconds'] : []),
                  l = (a.indexOf(w.value[0]) + e + a.length) % a.length
                A.start_emitSelectRange(t[l])
              })(a === t ? -1 : 1),
              void e.preventDefault()
            )
          }
          if ([n, o].includes(a)) {
            const t = a === n ? -1 : 1
            return (A.start_scrollDown(t), void e.preventDefault())
          }
        }
      ]),
      t('set-picker-option', ['getRangeAvailableTime', F]),
      t('set-picker-option', ['getDefaultValue', () => e(i).locale(k.value)]),
      (e, a) => (
        P(),
        _(
          ae,
          { name: S(x) },
          {
            default: V(() => [
              e.actualVisible || e.visible
                ? (P(),
                  T(
                    'div',
                    { key: 0, class: $(S(b).b('panel')) },
                    [
                      R(
                        'div',
                        { class: $([S(b).be('panel', 'content'), { 'has-seconds': S(M) }]) },
                        [
                          X(
                            na,
                            {
                              ref: 'spinner',
                              role: e.datetimeRole || 'start',
                              'arrow-control': S(o),
                              'show-seconds': S(M),
                              'am-pm-mode': S(C),
                              'spinner-date': e.parsedValue,
                              'disabled-hours': S(r),
                              'disabled-minutes': S(s),
                              'disabled-seconds': S(u),
                              onChange: Y,
                              onSetOption: S(E),
                              onSelectRange: I
                            },
                            null,
                            8,
                            [
                              'role',
                              'arrow-control',
                              'show-seconds',
                              'am-pm-mode',
                              'spinner-date',
                              'disabled-hours',
                              'disabled-minutes',
                              'disabled-seconds',
                              'onSetOption'
                            ]
                          )
                        ],
                        2
                      ),
                      R(
                        'div',
                        { class: $(S(b).be('panel', 'footer')) },
                        [
                          R(
                            'button',
                            {
                              type: 'button',
                              class: $([S(b).be('panel', 'btn'), 'cancel']),
                              onClick: O
                            },
                            B(S(g)('el.datepicker.cancel')),
                            3
                          ),
                          R(
                            'button',
                            {
                              type: 'button',
                              class: $([S(b).be('panel', 'btn'), 'confirm']),
                              onClick:
                                a[0] ||
                                (a[0] = (e) =>
                                  ((e = !1, a = !1) => {
                                    a || t('pick', l.parsedValue, e)
                                  })())
                            },
                            B(S(g)('el.datepicker.confirm')),
                            3
                          )
                        ],
                        2
                      )
                    ],
                    2
                  ))
                : N('v-if', !0)
            ]),
            _: 1
          },
          8,
          ['name']
        )
      )
    )
  }
})
var ra = F(oa, [
    [
      '__file',
      '/home/runner/work/element-plus/element-plus/packages/components/time-picker/src/time-picker-com/panel-time-pick.vue'
    ]
  ]),
  sa = { exports: {} }
sa.exports = function (e, a, t) {
  var l = a.prototype,
    n = function (e) {
      return e && (e.indexOf ? e : e.s)
    },
    o = function (e, a, t, l, o) {
      var r = e.name ? e : e.$locale(),
        s = n(r[a]),
        u = n(r[t]),
        i =
          s ||
          u.map(function (e) {
            return e.slice(0, l)
          })
      if (!o) return i
      var d = r.weekStart
      return i.map(function (e, a) {
        return i[(a + (d || 0)) % 7]
      })
    },
    r = function () {
      return t.Ls[t.locale()]
    },
    s = function (e, a) {
      return (
        e.formats[a] ||
        e.formats[a.toUpperCase()].replace(/(\[[^\]]+])|(MMMM|MM|DD|dddd)/g, function (e, a, t) {
          return a || t.slice(1)
        })
      )
    },
    u = function () {
      var e = this
      return {
        months: function (a) {
          return a ? a.format('MMMM') : o(e, 'months')
        },
        monthsShort: function (a) {
          return a ? a.format('MMM') : o(e, 'monthsShort', 'months', 3)
        },
        firstDayOfWeek: function () {
          return e.$locale().weekStart || 0
        },
        weekdays: function (a) {
          return a ? a.format('dddd') : o(e, 'weekdays')
        },
        weekdaysMin: function (a) {
          return a ? a.format('dd') : o(e, 'weekdaysMin', 'weekdays', 2)
        },
        weekdaysShort: function (a) {
          return a ? a.format('ddd') : o(e, 'weekdaysShort', 'weekdays', 3)
        },
        longDateFormat: function (a) {
          return s(e.$locale(), a)
        },
        meridiem: this.$locale().meridiem,
        ordinal: this.$locale().ordinal
      }
    }
  ;((l.localeData = function () {
    return u.bind(this)()
  }),
    (t.localeData = function () {
      var e = r()
      return {
        firstDayOfWeek: function () {
          return e.weekStart || 0
        },
        weekdays: function () {
          return t.weekdays()
        },
        weekdaysShort: function () {
          return t.weekdaysShort()
        },
        weekdaysMin: function () {
          return t.weekdaysMin()
        },
        months: function () {
          return t.months()
        },
        monthsShort: function () {
          return t.monthsShort()
        },
        longDateFormat: function (a) {
          return s(e, a)
        },
        meridiem: e.meridiem,
        ordinal: e.ordinal
      }
    }),
    (t.months = function () {
      return o(r(), 'months')
    }),
    (t.monthsShort = function () {
      return o(r(), 'monthsShort', 'months', 3)
    }),
    (t.weekdays = function (e) {
      return o(r(), 'weekdays', null, null, e)
    }),
    (t.weekdaysShort = function (e) {
      return o(r(), 'weekdaysShort', 'weekdays', 3, e)
    }),
    (t.weekdaysMin = function (e) {
      return o(r(), 'weekdaysMin', 'weekdays', 2, e)
    }))
}
const ua = t(sa.exports)
var ia = { exports: {} }
ia.exports = function (e, a) {
  var t = a.prototype,
    l = t.format
  t.format = function (e) {
    var a = this,
      t = this.$locale()
    if (!this.isValid()) return l.bind(this)(e)
    var n = this.$utils(),
      o = (e || 'YYYY-MM-DDTHH:mm:ssZ').replace(
        /\[([^\]]+)]|Q|wo|ww|w|WW|W|zzz|z|gggg|GGGG|Do|X|x|k{1,2}|S/g,
        function (e) {
          switch (e) {
            case 'Q':
              return Math.ceil((a.$M + 1) / 3)
            case 'Do':
              return t.ordinal(a.$D)
            case 'gggg':
              return a.weekYear()
            case 'GGGG':
              return a.isoWeekYear()
            case 'wo':
              return t.ordinal(a.week(), 'W')
            case 'w':
            case 'ww':
              return n.s(a.week(), 'w' === e ? 1 : 2, '0')
            case 'W':
            case 'WW':
              return n.s(a.isoWeek(), 'W' === e ? 1 : 2, '0')
            case 'k':
            case 'kk':
              return n.s(String(0 === a.$H ? 24 : a.$H), 'k' === e ? 1 : 2, '0')
            case 'X':
              return Math.floor(a.$d.getTime() / 1e3)
            case 'x':
              return a.$d.getTime()
            case 'z':
              return '[' + a.offsetName() + ']'
            case 'zzz':
              return '[' + a.offsetName('long') + ']'
            default:
              return e
          }
        }
      )
    return l.bind(this)(o)
  }
}
const da = t(ia.exports)
var ca,
  va,
  pa = { exports: {} }
const ma = t(
  (pa.exports =
    ((ca = 'week'),
    (va = 'year'),
    function (e, a, t) {
      var l = a.prototype
      ;((l.week = function (e) {
        if ((void 0 === e && (e = null), null !== e)) return this.add(7 * (e - this.week()), 'day')
        var a = this.$locale().yearStart || 1
        if (11 === this.month() && this.date() > 25) {
          var l = t(this).startOf(va).add(1, va).date(a),
            n = t(this).endOf(ca)
          if (l.isBefore(n)) return 1
        }
        var o = t(this).startOf(va).date(a).startOf(ca).subtract(1, 'millisecond'),
          r = this.diff(o, ca, !0)
        return r < 0 ? t(this).startOf('week').week() : Math.ceil(r)
      }),
        (l.weeks = function (e) {
          return (void 0 === e && (e = null), this.week(e))
        }))
    }))
)
var fa = { exports: {} }
fa.exports = function (e, a) {
  a.prototype.weekYear = function () {
    var e = this.month(),
      a = this.week(),
      t = this.year()
    return 1 === a && 11 === e ? t + 1 : 0 === e && a >= 52 ? t - 1 : t
  }
}
const ha = t(fa.exports)
var ya = { exports: {} }
ya.exports = function (e, a, t) {
  a.prototype.dayOfYear = function (e) {
    var a = Math.round((t(this).startOf('day') - t(this).startOf('year')) / 864e5) + 1
    return null == e ? a : this.add(e - a, 'day')
  }
}
const ba = t(ya.exports)
var ga = { exports: {} }
ga.exports = function (e, a) {
  a.prototype.isSameOrAfter = function (e, a) {
    return this.isSame(e, a) || this.isAfter(e, a)
  }
}
const ka = t(ga.exports)
var wa = { exports: {} }
const Da = t(
    (wa.exports = function (e, a) {
      a.prototype.isSameOrBefore = function (e, a) {
        return this.isSame(e, a) || this.isBefore(e, a)
      }
    })
  ),
  xa = Symbol(),
  Sa = r({ ...Le, type: { type: s(String), default: 'date' } }),
  Ma = ['date', 'dates', 'year', 'month', 'week', 'range'],
  Ca = r({
    disabledDate: { type: s(Function) },
    date: { type: s(Object), required: !0 },
    minDate: { type: s(Object) },
    maxDate: { type: s(Object) },
    parsedValue: { type: s([Object, Array]) },
    rangeState: { type: s(Object), default: () => ({ endDate: null, selecting: !1 }) }
  }),
  Pa = r({
    type: {
      type: s(String),
      required: !0,
      values: [
        'year',
        'month',
        'date',
        'dates',
        'week',
        'datetime',
        'datetimerange',
        'daterange',
        'monthrange'
      ]
    }
  }),
  _a = r({ unlinkPanels: Boolean, parsedValue: { type: s(Array) } }),
  Va = (e) => ({ type: String, values: Ma, default: e }),
  $a = r({
    ...Pa,
    parsedValue: { type: s([Object, Array]) },
    visible: { type: Boolean },
    format: { type: String, default: '' }
  }),
  Oa = r({
    ...Ca,
    cellClassName: { type: s(Function) },
    showWeekNumber: Boolean,
    selectionMode: Va('date')
  }),
  Ya = (a) => {
    if (!o(a)) return !1
    const [t, l] = a
    return e.isDayjs(t) && e.isDayjs(l) && t.isSameOrBefore(l)
  },
  Ia = (a, { lang: t, unit: l, unlinkPanels: n }) => {
    let r
    if (o(a)) {
      let [o, r] = a.map((a) => e(a).locale(t))
      return (n || (r = o.add(1, l)), [o, r])
    }
    return ((r = a ? e(a) : e()), (r = r.locale(t)), [r, r.add(1, l)])
  }
var Aa = d({
  name: 'ElDatePickerCell',
  props: r({ cell: { type: s(Object) } }),
  setup(e) {
    const a = p('date-table-cell'),
      { slots: t } = f(xa)
    return () => {
      const { cell: l } = e
      if (t.default) {
        const e = t
          .default(l)
          .filter((e) => -2 !== e.patchFlag && 'Symbol(Comment)' !== e.type.toString())
        if (e.length) return e
      }
      return X('div', { class: a.b() }, [
        X('span', { class: a.e('text') }, [null == l ? void 0 : l.text])
      ])
    }
  }
})
const Na = ['aria-label', 'onMousedown'],
  Ta = { key: 0, scope: 'col' },
  Ra = ['aria-label'],
  Ea = ['aria-current', 'aria-selected', 'tabindex'],
  Ba = d({
    __name: 'basic-date-table',
    props: Oa,
    emits: ['changerange', 'pick', 'select'],
    setup(a, { expose: t, emit: l }) {
      const n = a,
        o = p('date-table'),
        { t: r, lang: s } = v(),
        u = h(),
        i = h(),
        d = h(),
        c = h(),
        m = h([[], [], [], [], [], []])
      let f = !1
      const k = n.date.$locale().weekStart || 7,
        w = n.date
          .locale('en')
          .localeData()
          .weekdaysShort()
          .map((e) => e.toLowerCase()),
        D = y(() => (k > 3 ? 7 - k : -k)),
        x = y(() => {
          const e = n.date.startOf('month')
          return e.subtract(e.day() || 7, 'day')
        }),
        M = y(() => w.concat(w).slice(k, k + 7)),
        C = y(() => te(A.value).some((e) => e.isCurrent)),
        _ = y(() => {
          const e = n.date.startOf('month')
          return {
            startOfMonthDay: e.day() || 7,
            dateCountOfMonth: e.daysInMonth(),
            dateCountOfLastMonth: e.subtract(1, 'month').daysInMonth()
          }
        }),
        V = y(() => ('dates' === n.selectionMode ? De(n.parsedValue) : [])),
        O = (e, { columnIndex: a, rowIndex: t }, l) => {
          const { disabledDate: o, cellClassName: r } = n,
            s = S(V),
            u = ((e, { count: a, rowIndex: t, columnIndex: l }) => {
              const { startOfMonthDay: n, dateCountOfMonth: o, dateCountOfLastMonth: r } = S(_),
                s = S(D)
              if (!(t >= 0 && t <= 1))
                return (a <= o ? (e.text = a) : ((e.text = a - o), (e.type = 'next-month')), !0)
              {
                const o = n + s < 0 ? 7 + n + s : n + s
                if (l + 7 * t >= o) return ((e.text = a), !0)
                ;((e.text = r - (o - (l % 7)) + 1 + 7 * t), (e.type = 'prev-month'))
              }
              return !1
            })(e, { count: l, rowIndex: t, columnIndex: a }),
            i = e.dayjs.toDate()
          return (
            (e.selected = s.find((a) => a.valueOf() === e.dayjs.valueOf())),
            (e.isSelected = !!e.selected),
            (e.isCurrent = L(e)),
            (e.disabled = null == o ? void 0 : o(i)),
            (e.customClass = null == r ? void 0 : r(i)),
            u
          )
        },
        I = (e) => {
          if ('week' === n.selectionMode) {
            const [a, t] = n.showWeekNumber ? [1, 7] : [0, 6],
              l = J(e[a + 1])
            ;((e[a].inRange = l), (e[a].start = l), (e[t].inRange = l), (e[t].end = l))
          }
        },
        A = y(() => {
          const { minDate: a, maxDate: t, rangeState: l, showWeekNumber: o } = n,
            r = D.value,
            u = m.value,
            i = 'day'
          let d = 1
          if (o)
            for (let e = 0; e < 6; e++)
              u[e][0] || (u[e][0] = { type: 'week', text: x.value.add(7 * e + 1, i).week() })
          return (
            ((
              e,
              a,
              {
                columnIndexOffset: t,
                startDate: l,
                nextEndDate: n,
                now: o,
                unit: r,
                relativeDateGetter: s,
                setCellMetadata: u,
                setRowMetadata: i
              }
            ) => {
              for (let d = 0; d < e.row; d++) {
                const c = a[d]
                for (let a = 0; a < e.column; a++) {
                  let i = c[a + t]
                  i || (i = { row: d, column: a, type: 'normal', inRange: !1, start: !1, end: !1 })
                  const v = s(d * e.column + a)
                  ;((i.dayjs = v),
                    (i.date = v.toDate()),
                    (i.timestamp = v.valueOf()),
                    (i.type = 'normal'),
                    (i.inRange =
                      !!(l && v.isSameOrAfter(l, r) && n && v.isSameOrBefore(n, r)) ||
                      !!(l && v.isSameOrBefore(l, r) && n && v.isSameOrAfter(n, r))),
                    (null == l ? void 0 : l.isSameOrAfter(n))
                      ? ((i.start = !!n && v.isSame(n, r)), (i.end = l && v.isSame(l, r)))
                      : ((i.start = !!l && v.isSame(l, r)), (i.end = !!n && v.isSame(n, r))),
                    v.isSame(o, r) && (i.type = 'today'),
                    null == u || u(i, { rowIndex: d, columnIndex: a }),
                    (c[a + t] = i))
                }
                null == i || i(c)
              }
            })({ row: 6, column: 7 }, u, {
              startDate: a,
              columnIndexOffset: o ? 1 : 0,
              nextEndDate: l.endDate || t || (l.selecting && a) || null,
              now: e().locale(S(s)).startOf(i),
              unit: i,
              relativeDateGetter: (e) => x.value.add(e - r, i),
              setCellMetadata: (...e) => {
                O(...e, d) && (d += 1)
              },
              setRowMetadata: I
            }),
            u
          )
        })
      b(
        () => n.date,
        async () => {
          var e, a
          ;(null == (e = u.value) ? void 0 : e.contains(document.activeElement)) &&
            (await g(), null == (a = i.value) || a.focus())
        }
      )
      const E = (e = '') => ['normal', 'today'].includes(e),
        L = (e) => 'date' === n.selectionMode && E(e.type) && F(e, n.parsedValue),
        F = (a, t) =>
          !!t &&
          e(t)
            .locale(s.value)
            .isSame(n.date.date(Number(a.text)), 'day'),
        j = (e) => {
          const a = []
          return (
            E(e.type) && !e.disabled
              ? (a.push('available'), 'today' === e.type && a.push('today'))
              : a.push(e.type),
            L(e) && a.push('current'),
            e.inRange &&
              (E(e.type) || 'week' === n.selectionMode) &&
              (a.push('in-range'), e.start && a.push('start-date'), e.end && a.push('end-date')),
            e.disabled && a.push('disabled'),
            e.selected && a.push('selected'),
            e.customClass && a.push(e.customClass),
            a.join(' ')
          )
        },
        z = (e, a) => {
          const t = 7 * e + (a - (n.showWeekNumber ? 1 : 0)) - D.value
          return x.value.add(t, 'day')
        },
        W = (e) => {
          var a
          if (!n.rangeState.selecting) return
          let t = e.target
          if (
            ('SPAN' === t.tagName && (t = null == (a = t.parentNode) ? void 0 : a.parentNode),
            'DIV' === t.tagName && (t = t.parentNode),
            'TD' !== t.tagName)
          )
            return
          const o = t.parentNode.rowIndex - 1,
            r = t.cellIndex
          A.value[o][r].disabled ||
            (o === d.value && r === c.value) ||
            ((d.value = o), (c.value = r), l('changerange', { selecting: !0, endDate: z(o, r) }))
        },
        H = (e) =>
          (!C.value && 1 === (null == e ? void 0 : e.text) && 'normal' === e.type) || e.isCurrent,
        q = (e) => {
          f || C.value || 'date' !== n.selectionMode || Q(e, !0)
        },
        G = (e) => {
          e.target.closest('td') && (f = !0)
        },
        Z = (e) => {
          e.target.closest('td') && (f = !1)
        },
        Q = (e, a = !1) => {
          const t = e.target.closest('td')
          if (!t) return
          const o = t.parentNode.rowIndex - 1,
            r = t.cellIndex,
            s = A.value[o][r]
          if (s.disabled || 'week' === s.type) return
          const u = z(o, r)
          if ('range' === n.selectionMode)
            n.rangeState.selecting && n.minDate
              ? (u >= n.minDate
                  ? l('pick', { minDate: n.minDate, maxDate: u })
                  : l('pick', { minDate: u, maxDate: n.minDate }),
                l('select', !1))
              : (l('pick', { minDate: u, maxDate: null }), l('select', !0))
          else if ('date' === n.selectionMode) l('pick', u, a)
          else if ('week' === n.selectionMode) {
            const e = u.week(),
              a = `${u.year()}w${e}`
            l('pick', { year: u.year(), week: e, value: a, date: u.startOf('week') })
          } else if ('dates' === n.selectionMode) {
            const e = s.selected
              ? De(n.parsedValue).filter((e) => (null == e ? void 0 : e.valueOf()) !== u.valueOf())
              : De(n.parsedValue).concat([u])
            l('pick', e)
          }
        },
        J = (e) => {
          if ('week' !== n.selectionMode) return !1
          let a = n.date.startOf('day')
          if (
            ('prev-month' === e.type && (a = a.subtract(1, 'month')),
            'next-month' === e.type && (a = a.add(1, 'month')),
            (a = a.date(Number.parseInt(e.text, 10))),
            n.parsedValue && !Array.isArray(n.parsedValue))
          ) {
            const e = ((n.parsedValue.day() - k + 7) % 7) - 1
            return n.parsedValue.subtract(e, 'day').isSame(a, 'day')
          }
          return !1
        }
      return (
        t({
          focus: async () => {
            var e
            null == (e = i.value) || e.focus()
          }
        }),
        (e, a) => (
          P(),
          T(
            'table',
            {
              role: 'grid',
              'aria-label': S(r)('el.datepicker.dateTablePrompt'),
              cellspacing: '0',
              cellpadding: '0',
              class: $([S(o).b(), { 'is-week-mode': 'week' === e.selectionMode }]),
              onClick: Q,
              onMousemove: W,
              onMousedown: Y(G, ['prevent']),
              onMouseup: Z
            },
            [
              R(
                'tbody',
                { ref_key: 'tbodyRef', ref: u },
                [
                  R('tr', null, [
                    e.showWeekNumber
                      ? (P(), T('th', Ta, B(S(r)('el.datepicker.week')), 1))
                      : N('v-if', !0),
                    (P(!0),
                    T(
                      K,
                      null,
                      U(
                        S(M),
                        (e, a) => (
                          P(),
                          T(
                            'th',
                            {
                              key: a,
                              scope: 'col',
                              'aria-label': S(r)('el.datepicker.weeksFull.' + e)
                            },
                            B(S(r)('el.datepicker.weeks.' + e)),
                            9,
                            Ra
                          )
                        )
                      ),
                      128
                    ))
                  ]),
                  (P(!0),
                  T(
                    K,
                    null,
                    U(
                      S(A),
                      (e, a) => (
                        P(),
                        T(
                          'tr',
                          { key: a, class: $([S(o).e('row'), { current: J(e[1]) }]) },
                          [
                            (P(!0),
                            T(
                              K,
                              null,
                              U(
                                e,
                                (e, t) => (
                                  P(),
                                  T(
                                    'td',
                                    {
                                      key: `${a}.${t}`,
                                      ref_for: !0,
                                      ref: (a) => H(e) && (i.value = a),
                                      class: $(j(e)),
                                      'aria-current': e.isCurrent ? 'date' : void 0,
                                      'aria-selected': e.isCurrent,
                                      tabindex: H(e) ? 0 : -1,
                                      onFocus: q
                                    },
                                    [X(S(Aa), { cell: e }, null, 8, ['cell'])],
                                    42,
                                    Ea
                                  )
                                )
                              ),
                              128
                            ))
                          ],
                          2
                        )
                      )
                    ),
                    128
                  ))
                ],
                512
              )
            ],
            42,
            Na
          )
        )
      )
    }
  })
var La = F(Ba, [
  [
    '__file',
    '/home/runner/work/element-plus/element-plus/packages/components/date-picker/src/date-picker-com/basic-date-table.vue'
  ]
])
const Fa = r({ ...Ca, selectionMode: Va('month') }),
  ja = ['aria-label'],
  za = ['aria-selected', 'aria-label', 'tabindex', 'onKeydown'],
  Wa = { class: 'cell' },
  Ha = d({
    __name: 'basic-month-table',
    props: Fa,
    emits: ['changerange', 'pick', 'select'],
    setup(a, { expose: t, emit: l }) {
      const n = a,
        o = p('month-table'),
        { t: r, lang: s } = v(),
        u = h(),
        i = h(),
        d = h(
          n.date
            .locale('en')
            .localeData()
            .monthsShort()
            .map((e) => e.toLowerCase())
        ),
        c = h([[], [], []]),
        m = h(),
        f = h(),
        k = y(() => {
          var a, t
          const l = c.value,
            o = e().locale(s.value).startOf('month')
          for (let e = 0; e < 3; e++) {
            const r = l[e]
            for (let l = 0; l < 4; l++) {
              const s =
                r[l] ||
                (r[l] = {
                  row: e,
                  column: l,
                  type: 'normal',
                  inRange: !1,
                  start: !1,
                  end: !1,
                  text: -1,
                  disabled: !1
                })
              s.type = 'normal'
              const u = 4 * e + l,
                i = n.date.startOf('year').month(u),
                d =
                  n.rangeState.endDate || n.maxDate || (n.rangeState.selecting && n.minDate) || null
              ;((s.inRange =
                !!(
                  n.minDate &&
                  i.isSameOrAfter(n.minDate, 'month') &&
                  d &&
                  i.isSameOrBefore(d, 'month')
                ) ||
                !!(
                  n.minDate &&
                  i.isSameOrBefore(n.minDate, 'month') &&
                  d &&
                  i.isSameOrAfter(d, 'month')
                )),
                (null == (a = n.minDate) ? void 0 : a.isSameOrAfter(d))
                  ? ((s.start = !(!d || !i.isSame(d, 'month'))),
                    (s.end = n.minDate && i.isSame(n.minDate, 'month')))
                  : ((s.start = !(!n.minDate || !i.isSame(n.minDate, 'month'))),
                    (s.end = !(!d || !i.isSame(d, 'month')))))
              ;(o.isSame(i) && (s.type = 'today'),
                (s.text = u),
                (s.disabled =
                  (null == (t = n.disabledDate) ? void 0 : t.call(n, i.toDate())) || !1))
            }
          }
          return l
        }),
        w = (a) => {
          const t = {},
            l = n.date.year(),
            o = new Date(),
            r = a.text
          return (
            (t.disabled =
              !!n.disabledDate &&
              ((a, t, l) => {
                const n = e().locale(l).startOf('month').month(t).year(a),
                  o = n.daysInMonth()
                return $e(o).map((e) => n.add(e, 'day').toDate())
              })(l, r, s.value).every(n.disabledDate)),
            (t.current =
              De(n.parsedValue).findIndex(
                (a) => e.isDayjs(a) && a.year() === l && a.month() === r
              ) >= 0),
            (t.today = o.getFullYear() === l && o.getMonth() === r),
            a.inRange &&
              ((t['in-range'] = !0),
              a.start && (t['start-date'] = !0),
              a.end && (t['end-date'] = !0)),
            t
          )
        },
        D = (e) => {
          const a = n.date.year(),
            t = e.text
          return De(n.date).findIndex((e) => e.year() === a && e.month() === t) >= 0
        },
        x = (e) => {
          var a
          if (!n.rangeState.selecting) return
          let t = e.target
          if (
            ('A' === t.tagName && (t = null == (a = t.parentNode) ? void 0 : a.parentNode),
            'DIV' === t.tagName && (t = t.parentNode),
            'TD' !== t.tagName)
          )
            return
          const o = t.parentNode.rowIndex,
            r = t.cellIndex
          k.value[o][r].disabled ||
            (o === m.value && r === f.value) ||
            ((m.value = o),
            (f.value = r),
            l('changerange', { selecting: !0, endDate: n.date.startOf('year').month(4 * o + r) }))
        },
        M = (e) => {
          var a
          const t = null == (a = e.target) ? void 0 : a.closest('td')
          if ('TD' !== (null == t ? void 0 : t.tagName)) return
          if (ne(t, 'disabled')) return
          const o = t.cellIndex,
            r = 4 * t.parentNode.rowIndex + o,
            s = n.date.startOf('year').month(r)
          'range' === n.selectionMode
            ? n.rangeState.selecting
              ? (n.minDate && s >= n.minDate
                  ? l('pick', { minDate: n.minDate, maxDate: s })
                  : l('pick', { minDate: s, maxDate: n.minDate }),
                l('select', !1))
              : (l('pick', { minDate: s, maxDate: null }), l('select', !0))
            : l('pick', r)
        }
      return (
        b(
          () => n.date,
          async () => {
            var e, a
            ;(null == (e = u.value) ? void 0 : e.contains(document.activeElement)) &&
              (await g(), null == (a = i.value) || a.focus())
          }
        ),
        t({
          focus: () => {
            var e
            null == (e = i.value) || e.focus()
          }
        }),
        (e, a) => (
          P(),
          T(
            'table',
            {
              role: 'grid',
              'aria-label': S(r)('el.datepicker.monthTablePrompt'),
              class: $(S(o).b()),
              onClick: M,
              onMousemove: x
            },
            [
              R(
                'tbody',
                { ref_key: 'tbodyRef', ref: u },
                [
                  (P(!0),
                  T(
                    K,
                    null,
                    U(
                      S(k),
                      (e, a) => (
                        P(),
                        T('tr', { key: a }, [
                          (P(!0),
                          T(
                            K,
                            null,
                            U(
                              e,
                              (e, a) => (
                                P(),
                                T(
                                  'td',
                                  {
                                    key: a,
                                    ref_for: !0,
                                    ref: (a) => D(e) && (i.value = a),
                                    class: $(w(e)),
                                    'aria-selected': `${D(e)}`,
                                    'aria-label': S(r)('el.datepicker.month' + (+e.text + 1)),
                                    tabindex: D(e) ? 0 : -1,
                                    onKeydown: [
                                      le(Y(M, ['prevent', 'stop']), ['space']),
                                      le(Y(M, ['prevent', 'stop']), ['enter'])
                                    ]
                                  },
                                  [
                                    R('div', null, [
                                      R(
                                        'span',
                                        Wa,
                                        B(S(r)('el.datepicker.months.' + d.value[e.text])),
                                        1
                                      )
                                    ])
                                  ],
                                  42,
                                  za
                                )
                              )
                            ),
                            128
                          ))
                        ])
                      )
                    ),
                    128
                  ))
                ],
                512
              )
            ],
            42,
            ja
          )
        )
      )
    }
  })
var Ka = F(Ha, [
  [
    '__file',
    '/home/runner/work/element-plus/element-plus/packages/components/date-picker/src/date-picker-com/basic-month-table.vue'
  ]
])
const { date: Ua, disabledDate: qa, parsedValue: Ga } = Ca,
  Za = r({ date: Ua, disabledDate: qa, parsedValue: Ga }),
  Xa = ['aria-label'],
  Qa = ['aria-selected', 'tabindex', 'onKeydown'],
  Ja = { class: 'cell' },
  et = { key: 1 },
  at = d({
    __name: 'basic-year-table',
    props: Za,
    emits: ['pick'],
    setup(a, { expose: t, emit: l }) {
      const n = a,
        o = p('year-table'),
        { t: r, lang: s } = v(),
        u = h(),
        i = h(),
        d = y(() => 10 * Math.floor(n.date.year() / 10)),
        c = (a) => {
          const t = {},
            l = e().locale(s.value)
          return (
            (t.disabled =
              !!n.disabledDate &&
              ((a, t) => {
                const l = e(String(a)).locale(t).startOf('year'),
                  n = l.endOf('year').dayOfYear()
                return $e(n).map((e) => l.add(e, 'day').toDate())
              })(a, s.value).every(n.disabledDate)),
            (t.current = De(n.parsedValue).findIndex((e) => e.year() === a) >= 0),
            (t.today = l.year() === a),
            t
          )
        },
        m = (e) =>
          (e === d.value && n.date.year() < d.value && n.date.year() > d.value + 9) ||
          De(n.date).findIndex((a) => a.year() === e) >= 0,
        f = (e) => {
          const a = e.target.closest('td')
          if (a && a.textContent) {
            if (ne(a, 'disabled')) return
            const e = a.textContent || a.innerText
            l('pick', Number(e))
          }
        }
      return (
        b(
          () => n.date,
          async () => {
            var e, a
            ;(null == (e = u.value) ? void 0 : e.contains(document.activeElement)) &&
              (await g(), null == (a = i.value) || a.focus())
          }
        ),
        t({
          focus: () => {
            var e
            null == (e = i.value) || e.focus()
          }
        }),
        (e, a) => (
          P(),
          T(
            'table',
            {
              role: 'grid',
              'aria-label': S(r)('el.datepicker.yearTablePrompt'),
              class: $(S(o).b()),
              onClick: f
            },
            [
              R(
                'tbody',
                { ref_key: 'tbodyRef', ref: u },
                [
                  (P(),
                  T(
                    K,
                    null,
                    U(3, (e, a) =>
                      R('tr', { key: a }, [
                        (P(),
                        T(
                          K,
                          null,
                          U(
                            4,
                            (e, t) => (
                              P(),
                              T(
                                K,
                                { key: a + '_' + t },
                                [
                                  4 * a + t < 10
                                    ? (P(),
                                      T(
                                        'td',
                                        {
                                          key: 0,
                                          ref_for: !0,
                                          ref: (e) => m(S(d) + 4 * a + t) && (i.value = e),
                                          class: $(['available', c(S(d) + 4 * a + t)]),
                                          'aria-selected': `${m(S(d) + 4 * a + t)}`,
                                          tabindex: m(S(d) + 4 * a + t) ? 0 : -1,
                                          onKeydown: [
                                            le(Y(f, ['prevent', 'stop']), ['space']),
                                            le(Y(f, ['prevent', 'stop']), ['enter'])
                                          ]
                                        },
                                        [R('span', Ja, B(S(d) + 4 * a + t), 1)],
                                        42,
                                        Qa
                                      ))
                                    : (P(), T('td', et))
                                ],
                                64
                              )
                            )
                          ),
                          64
                        ))
                      ])
                    ),
                    64
                  ))
                ],
                512
              )
            ],
            10,
            Xa
          )
        )
      )
    }
  })
var tt = F(at, [
  [
    '__file',
    '/home/runner/work/element-plus/element-plus/packages/components/date-picker/src/date-picker-com/basic-year-table.vue'
  ]
])
const lt = ['onClick'],
  nt = ['aria-label'],
  ot = ['aria-label'],
  rt = ['aria-label'],
  st = ['aria-label'],
  ut = d({
    __name: 'panel-date-pick',
    props: $a,
    emits: ['pick', 'set-picker-option', 'panel-change'],
    setup(a, { emit: t }) {
      const l = a,
        n = p('picker-panel'),
        r = p('date-picker'),
        s = c(),
        u = oe(),
        { t: i, lang: d } = v(),
        m = f('EP_PICKER_BASE'),
        k = f(ye),
        {
          shortcuts: w,
          disabledDate: D,
          cellClassName: x,
          defaultTime: M,
          arrowControl: C
        } = m.props,
        O = re(m.props, 'defaultValue'),
        Y = h(),
        A = h(e().locale(d.value)),
        L = h(!1),
        F = y(() => e(M).locale(d.value)),
        W = y(() => A.value.month()),
        H = y(() => A.value.year()),
        G = h([]),
        Q = h(null),
        J = h(null),
        ee = (e) => !(G.value.length > 0) || (G.value, l.format, !0),
        ae = (e) =>
          !M || Te.value || L.value
            ? Ce.value
              ? e.millisecond(0)
              : e.startOf('day')
            : F.value.year(e.year()).month(e.month()).date(e.date()),
        te = (e, ...a) => {
          if (e)
            if (o(e)) {
              const l = e.map(ae)
              t('pick', l, ...a)
            } else t('pick', ae(e), ...a)
          else t('pick', e, ...a)
          ;((Q.value = null), (J.value = null), (L.value = !1))
        },
        ne = (e, a) => {
          if ('date' === ke.value) {
            let t = l.parsedValue ? l.parsedValue.year(e.year()).month(e.month()).date(e.date()) : e
            ;(ee() || (t = G.value[0][0].year(e.year()).month(e.month()).date(e.date())),
              (A.value = t),
              te(t, Ce.value || a))
          } else 'week' === ke.value ? te(e.date) : 'dates' === ke.value && te(e, !0)
        },
        pe = (e) => {
          const a = e ? 'add' : 'subtract'
          ;((A.value = A.value[a](1, 'month')), Ge('month'))
        },
        me = (e) => {
          const a = A.value,
            t = e ? 'add' : 'subtract'
          ;((A.value = 'year' === he.value ? a[t](10, 'year') : a[t](1, 'year')), Ge('year'))
        },
        he = h('date'),
        be = y(() => {
          const e = i('el.datepicker.year')
          if ('year' === he.value) {
            const a = 10 * Math.floor(H.value / 10)
            return e ? `${a} ${e} - ${a + 9} ${e}` : `${a} - ${a + 9}`
          }
          return `${H.value} ${e}`
        }),
        ke = y(() => {
          const { type: e } = l
          return ['week', 'month', 'year', 'dates'].includes(e) ? e : 'date'
        }),
        we = y(() => ('date' === ke.value ? he.value : ke.value)),
        De = y(() => !!w.length),
        xe = async (e) => {
          ;((A.value = A.value.startOf('month').month(e)),
            'month' === ke.value
              ? te(A.value, !1)
              : ((he.value = 'date'),
                ['month', 'year', 'date', 'week'].includes(ke.value) &&
                  (te(A.value, !0), await g(), Ke())),
            Ge('month'))
        },
        Se = async (e) => {
          ;('year' === ke.value
            ? ((A.value = A.value.startOf('year').year(e)), te(A.value, !1))
            : ((A.value = A.value.year(e)),
              (he.value = 'month'),
              ['month', 'year', 'date', 'week'].includes(ke.value) &&
                (te(A.value, !0), await g(), Ke())),
            Ge('year'))
        },
        Me = async (e) => {
          ;((he.value = e), await g(), Ke())
        },
        Ce = y(() => 'datetime' === l.type || 'datetimerange' === l.type),
        Pe = y(() => Ce.value || 'dates' === ke.value),
        _e = y(
          () =>
            !!D &&
            (!l.parsedValue ||
              (o(l.parsedValue) ? D(l.parsedValue[0].toDate()) : D(l.parsedValue.toDate())))
        ),
        Ve = () => {
          if ('dates' === ke.value) te(l.parsedValue)
          else {
            let a = l.parsedValue
            if (!a) {
              const t = e(M).locale(d.value),
                l = He()
              a = t.year(l.year()).month(l.month()).date(l.date())
            }
            ;((A.value = a), te(a))
          }
        },
        $e = y(() => !!D && D(e().locale(d.value).toDate())),
        Ie = () => {
          const a = e().locale(d.value).toDate()
          ;((L.value = !0), (D && D(a)) || !ee() || ((A.value = e().locale(d.value)), te(A.value)))
        },
        Ae = y(() => Ye(l.format)),
        Ne = y(() => Oe(l.format)),
        Te = y(() =>
          J.value
            ? J.value
            : l.parsedValue || O.value
              ? (l.parsedValue || A.value).format(Ae.value)
              : void 0
        ),
        Re = y(() =>
          Q.value
            ? Q.value
            : l.parsedValue || O.value
              ? (l.parsedValue || A.value).format(Ne.value)
              : void 0
        ),
        Ee = h(!1),
        Be = () => {
          Ee.value = !0
        },
        Le = () => {
          Ee.value = !1
        },
        Fe = (e) => ({
          hour: e.hour(),
          minute: e.minute(),
          second: e.second(),
          year: e.year(),
          month: e.month(),
          date: e.date()
        }),
        je = (e, a, t) => {
          const { hour: n, minute: o, second: r } = Fe(e),
            s = l.parsedValue ? l.parsedValue.hour(n).minute(o).second(r) : e
          ;((A.value = s), te(A.value, !0), t || (Ee.value = a))
        },
        ze = (a) => {
          const t = e(a, Ae.value).locale(d.value)
          if (t.isValid() && ee()) {
            const { year: e, month: a, date: l } = Fe(A.value)
            ;((A.value = t.year(e).month(a).date(l)),
              (J.value = null),
              (Ee.value = !1),
              te(A.value, !0))
          }
        },
        We = (a) => {
          const t = e(a, Ne.value).locale(d.value)
          if (t.isValid()) {
            if (D && D(t.toDate())) return
            const { hour: e, minute: a, second: l } = Fe(A.value)
            ;((A.value = t.hour(e).minute(a).second(l)), (Q.value = null), te(A.value, !0))
          }
        },
        He = () => {
          const a = e(O.value).locale(d.value)
          if (!O.value) {
            const a = F.value
            return e().hour(a.hour()).minute(a.minute()).second(a.second()).locale(d.value)
          }
          return a
        },
        Ke = async () => {
          var e
          ;['week', 'month', 'year', 'date'].includes(ke.value) &&
            (null == (e = Y.value) || e.focus(), 'week' === ke.value && qe(j.down))
        },
        Ue = (e) => {
          const { code: a } = e
          ;([j.up, j.down, j.left, j.right, j.home, j.end, j.pageUp, j.pageDown].includes(a) &&
            (qe(a), e.stopPropagation(), e.preventDefault()),
            [j.enter, j.space, j.numpadEnter].includes(a) &&
              null === Q.value &&
              null === J.value &&
              (e.preventDefault(), te(A.value, !1)))
        },
        qe = (a) => {
          var l
          const { up: n, down: o, left: r, right: s, home: u, end: i, pageUp: c, pageDown: v } = j,
            p = {
              year: {
                [n]: -4,
                [o]: 4,
                [r]: -1,
                [s]: 1,
                offset: (e, a) => e.setFullYear(e.getFullYear() + a)
              },
              month: {
                [n]: -4,
                [o]: 4,
                [r]: -1,
                [s]: 1,
                offset: (e, a) => e.setMonth(e.getMonth() + a)
              },
              week: {
                [n]: -1,
                [o]: 1,
                [r]: -1,
                [s]: 1,
                offset: (e, a) => e.setDate(e.getDate() + 7 * a)
              },
              date: {
                [n]: -7,
                [o]: 7,
                [r]: -1,
                [s]: 1,
                [u]: (e) => -e.getDay(),
                [i]: (e) => 6 - e.getDay(),
                [c]: (e) => -new Date(e.getFullYear(), e.getMonth(), 0).getDate(),
                [v]: (e) => new Date(e.getFullYear(), e.getMonth() + 1, 0).getDate(),
                offset: (e, a) => e.setDate(e.getDate() + a)
              }
            },
            m = A.value.toDate()
          for (; Math.abs(A.value.diff(m, 'year', !0)) < 1; ) {
            const n = p[we.value]
            if (!n) return
            if ((n.offset(m, z(n[a]) ? n[a](m) : null != (l = n[a]) ? l : 0), D && D(m))) break
            const o = e(m).locale(d.value)
            ;((A.value = o), t('pick', o, !0))
            break
          }
        },
        Ge = (e) => {
          t('panel-change', A.value.toDate(), e, he.value)
        }
      return (
        b(
          () => ke.value,
          (e) => {
            ;['month', 'year'].includes(e) ? (he.value = e) : (he.value = 'date')
          },
          { immediate: !0 }
        ),
        b(
          () => he.value,
          () => {
            null == k || k.updatePopper()
          }
        ),
        b(
          () => O.value,
          (e) => {
            e && (A.value = He())
          },
          { immediate: !0 }
        ),
        b(
          () => l.parsedValue,
          (e) => {
            if (e) {
              if ('dates' === ke.value) return
              if (Array.isArray(e)) return
              A.value = e
            } else A.value = He()
          },
          { immediate: !0 }
        ),
        t('set-picker-option', [
          'isValidValue',
          (a) => e.isDayjs(a) && a.isValid() && (!D || !D(a.toDate()))
        ]),
        t('set-picker-option', [
          'formatToString',
          (e) => ('dates' === ke.value ? e.map((e) => e.format(l.format)) : e.format(l.format))
        ]),
        t('set-picker-option', ['parseUserInput', (a) => e(a, l.format).locale(d.value)]),
        t('set-picker-option', ['handleFocusPicker', Ke]),
        (a, l) => (
          P(),
          T(
            'div',
            {
              class: $([
                S(n).b(),
                S(r).b(),
                { 'has-sidebar': a.$slots.sidebar || S(De), 'has-time': S(Ce) }
              ])
            },
            [
              R(
                'div',
                { class: $(S(n).e('body-wrapper')) },
                [
                  E(a.$slots, 'sidebar', { class: $(S(n).e('sidebar')) }),
                  S(De)
                    ? (P(),
                      T(
                        'div',
                        { key: 0, class: $(S(n).e('sidebar')) },
                        [
                          (P(!0),
                          T(
                            K,
                            null,
                            U(
                              S(w),
                              (a, l) => (
                                P(),
                                T(
                                  'button',
                                  {
                                    key: l,
                                    type: 'button',
                                    class: $(S(n).e('shortcut')),
                                    onClick: (l) =>
                                      ((a) => {
                                        const l = z(a.value) ? a.value() : a.value
                                        l
                                          ? te(e(l).locale(d.value))
                                          : a.onClick && a.onClick({ attrs: s, slots: u, emit: t })
                                      })(a)
                                  },
                                  B(a.text),
                                  11,
                                  lt
                                )
                              )
                            ),
                            128
                          ))
                        ],
                        2
                      ))
                    : N('v-if', !0),
                  R(
                    'div',
                    { class: $(S(n).e('body')) },
                    [
                      S(Ce)
                        ? (P(),
                          T(
                            'div',
                            { key: 0, class: $(S(r).e('time-header')) },
                            [
                              R(
                                'span',
                                { class: $(S(r).e('editor-wrap')) },
                                [
                                  X(
                                    S(fe),
                                    {
                                      placeholder: S(i)('el.datepicker.selectDate'),
                                      'model-value': S(Re),
                                      size: 'small',
                                      'validate-event': !1,
                                      onInput: l[0] || (l[0] = (e) => (Q.value = e)),
                                      onChange: We
                                    },
                                    null,
                                    8,
                                    ['placeholder', 'model-value']
                                  )
                                ],
                                2
                              ),
                              Z(
                                (P(),
                                T(
                                  'span',
                                  { class: $(S(r).e('editor-wrap')) },
                                  [
                                    X(
                                      S(fe),
                                      {
                                        placeholder: S(i)('el.datepicker.selectTime'),
                                        'model-value': S(Te),
                                        size: 'small',
                                        'validate-event': !1,
                                        onFocus: Be,
                                        onInput: l[1] || (l[1] = (e) => (J.value = e)),
                                        onChange: ze
                                      },
                                      null,
                                      8,
                                      ['placeholder', 'model-value']
                                    ),
                                    X(
                                      S(ra),
                                      {
                                        visible: Ee.value,
                                        format: S(Ae),
                                        'time-arrow-control': S(C),
                                        'parsed-value': A.value,
                                        onPick: je
                                      },
                                      null,
                                      8,
                                      ['visible', 'format', 'time-arrow-control', 'parsed-value']
                                    )
                                  ],
                                  2
                                )),
                                [[S(ge), Le]]
                              )
                            ],
                            2
                          ))
                        : N('v-if', !0),
                      Z(
                        R(
                          'div',
                          {
                            class: $([
                              S(r).e('header'),
                              ('year' === he.value || 'month' === he.value) &&
                                S(r).e('header--bordered')
                            ])
                          },
                          [
                            R(
                              'span',
                              { class: $(S(r).e('prev-btn')) },
                              [
                                R(
                                  'button',
                                  {
                                    type: 'button',
                                    'aria-label': S(i)('el.datepicker.prevYear'),
                                    class: $(['d-arrow-left', S(n).e('icon-btn')]),
                                    onClick: l[2] || (l[2] = (e) => me(!1))
                                  },
                                  [X(S(I), null, { default: V(() => [X(S(ue))]), _: 1 })],
                                  10,
                                  nt
                                ),
                                Z(
                                  R(
                                    'button',
                                    {
                                      type: 'button',
                                      'aria-label': S(i)('el.datepicker.prevMonth'),
                                      class: $([S(n).e('icon-btn'), 'arrow-left']),
                                      onClick: l[3] || (l[3] = (e) => pe(!1))
                                    },
                                    [X(S(I), null, { default: V(() => [X(S(ie))]), _: 1 })],
                                    10,
                                    ot
                                  ),
                                  [[se, 'date' === he.value]]
                                )
                              ],
                              2
                            ),
                            R(
                              'span',
                              {
                                role: 'button',
                                class: $(S(r).e('header-label')),
                                'aria-live': 'polite',
                                tabindex: '0',
                                onKeydown: l[4] || (l[4] = le((e) => Me('year'), ['enter'])),
                                onClick: l[5] || (l[5] = (e) => Me('year'))
                              },
                              B(S(be)),
                              35
                            ),
                            Z(
                              R(
                                'span',
                                {
                                  role: 'button',
                                  'aria-live': 'polite',
                                  tabindex: '0',
                                  class: $([
                                    S(r).e('header-label'),
                                    { active: 'month' === he.value }
                                  ]),
                                  onKeydown: l[6] || (l[6] = le((e) => Me('month'), ['enter'])),
                                  onClick: l[7] || (l[7] = (e) => Me('month'))
                                },
                                B(S(i)(`el.datepicker.month${S(W) + 1}`)),
                                35
                              ),
                              [[se, 'date' === he.value]]
                            ),
                            R(
                              'span',
                              { class: $(S(r).e('next-btn')) },
                              [
                                Z(
                                  R(
                                    'button',
                                    {
                                      type: 'button',
                                      'aria-label': S(i)('el.datepicker.nextMonth'),
                                      class: $([S(n).e('icon-btn'), 'arrow-right']),
                                      onClick: l[8] || (l[8] = (e) => pe(!0))
                                    },
                                    [X(S(I), null, { default: V(() => [X(S(de))]), _: 1 })],
                                    10,
                                    rt
                                  ),
                                  [[se, 'date' === he.value]]
                                ),
                                R(
                                  'button',
                                  {
                                    type: 'button',
                                    'aria-label': S(i)('el.datepicker.nextYear'),
                                    class: $([S(n).e('icon-btn'), 'd-arrow-right']),
                                    onClick: l[9] || (l[9] = (e) => me(!0))
                                  },
                                  [X(S(I), null, { default: V(() => [X(S(ce))]), _: 1 })],
                                  10,
                                  st
                                )
                              ],
                              2
                            )
                          ],
                          2
                        ),
                        [[se, 'time' !== he.value]]
                      ),
                      R(
                        'div',
                        { class: $(S(n).e('content')), onKeydown: Ue },
                        [
                          'date' === he.value
                            ? (P(),
                              _(
                                La,
                                {
                                  key: 0,
                                  ref_key: 'currentViewRef',
                                  ref: Y,
                                  'selection-mode': S(ke),
                                  date: A.value,
                                  'parsed-value': a.parsedValue,
                                  'disabled-date': S(D),
                                  'cell-class-name': S(x),
                                  onPick: ne
                                },
                                null,
                                8,
                                [
                                  'selection-mode',
                                  'date',
                                  'parsed-value',
                                  'disabled-date',
                                  'cell-class-name'
                                ]
                              ))
                            : N('v-if', !0),
                          'year' === he.value
                            ? (P(),
                              _(
                                tt,
                                {
                                  key: 1,
                                  ref_key: 'currentViewRef',
                                  ref: Y,
                                  date: A.value,
                                  'disabled-date': S(D),
                                  'parsed-value': a.parsedValue,
                                  onPick: Se
                                },
                                null,
                                8,
                                ['date', 'disabled-date', 'parsed-value']
                              ))
                            : N('v-if', !0),
                          'month' === he.value
                            ? (P(),
                              _(
                                Ka,
                                {
                                  key: 2,
                                  ref_key: 'currentViewRef',
                                  ref: Y,
                                  date: A.value,
                                  'parsed-value': a.parsedValue,
                                  'disabled-date': S(D),
                                  onPick: xe
                                },
                                null,
                                8,
                                ['date', 'parsed-value', 'disabled-date']
                              ))
                            : N('v-if', !0)
                        ],
                        34
                      )
                    ],
                    2
                  )
                ],
                2
              ),
              Z(
                R(
                  'div',
                  { class: $(S(n).e('footer')) },
                  [
                    Z(
                      X(
                        S(ve),
                        {
                          text: '',
                          size: 'small',
                          class: $(S(n).e('link-btn')),
                          disabled: S($e),
                          onClick: Ie
                        },
                        { default: V(() => [q(B(S(i)('el.datepicker.now')), 1)]), _: 1 },
                        8,
                        ['class', 'disabled']
                      ),
                      [[se, 'dates' !== S(ke)]]
                    ),
                    X(
                      S(ve),
                      {
                        plain: '',
                        size: 'small',
                        class: $(S(n).e('link-btn')),
                        disabled: S(_e),
                        onClick: Ve
                      },
                      { default: V(() => [q(B(S(i)('el.datepicker.confirm')), 1)]), _: 1 },
                      8,
                      ['class', 'disabled']
                    )
                  ],
                  2
                ),
                [[se, S(Pe) && 'date' === he.value]]
              )
            ],
            2
          )
        )
      )
    }
  })
var it = F(ut, [
  [
    '__file',
    '/home/runner/work/element-plus/element-plus/packages/components/date-picker/src/date-picker-com/panel-date-pick.vue'
  ]
])
const dt = r({ ...Pa, ..._a }),
  ct = (a, { defaultValue: t, leftDate: l, rightDate: n, unit: r, onParsedValueChanged: s }) => {
    const { emit: u } = pe(),
      { pickerNs: i } = f(xa),
      d = p('date-range-picker'),
      { t: m, lang: y } = v(),
      g = ((a) => {
        const { emit: t } = pe(),
          l = c(),
          n = oe()
        return (o) => {
          const r = z(o.value) ? o.value() : o.value
          r
            ? t('pick', [e(r[0]).locale(a.value), e(r[1]).locale(a.value)])
            : o.onClick && o.onClick({ attrs: l, slots: n, emit: t })
        }
      })(y),
      k = h(),
      w = h(),
      D = h({ endDate: null, selecting: !1 }),
      x = () => {
        const [e, o] = Ia(S(t), { lang: S(y), unit: r, unlinkPanels: a.unlinkPanels })
        ;((k.value = void 0), (w.value = void 0), (l.value = e), (n.value = o))
      }
    return (
      b(
        t,
        (e) => {
          e && x()
        },
        { immediate: !0 }
      ),
      b(
        () => a.parsedValue,
        (e) => {
          if (o(e) && 2 === e.length) {
            const [a, t] = e
            ;((k.value = a), (l.value = a), (w.value = t), s(S(k), S(w)))
          } else x()
        },
        { immediate: !0 }
      ),
      {
        minDate: k,
        maxDate: w,
        rangeState: D,
        lang: y,
        ppNs: i,
        drpNs: d,
        handleChangeRange: (e) => {
          D.value = e
        },
        handleRangeConfirm: (e = !1) => {
          const a = S(k),
            t = S(w)
          Ya([a, t]) && u('pick', [a, t], e)
        },
        handleShortcutClick: g,
        onSelect: (e) => {
          ;((D.value.selecting = e), e || (D.value.endDate = null))
        },
        t: m
      }
    )
  },
  vt = ['onClick'],
  pt = ['disabled'],
  mt = ['disabled'],
  ft = ['disabled'],
  ht = ['disabled'],
  yt = 'month',
  bt = d({
    __name: 'panel-date-range',
    props: dt,
    emits: ['pick', 'set-picker-option', 'calendar-change', 'panel-change'],
    setup(a, { emit: t }) {
      const l = a,
        n = f('EP_PICKER_BASE'),
        {
          disabledDate: r,
          cellClassName: s,
          format: u,
          defaultTime: i,
          arrowControl: d,
          clearable: c
        } = n.props,
        p = re(n.props, 'shortcuts'),
        m = re(n.props, 'defaultValue'),
        { lang: b } = v(),
        g = h(e().locale(b.value)),
        k = h(e().locale(b.value).add(1, yt)),
        {
          minDate: w,
          maxDate: D,
          rangeState: x,
          ppNs: M,
          drpNs: C,
          handleChangeRange: O,
          handleRangeConfirm: Y,
          handleShortcutClick: A,
          onSelect: L,
          t: F
        } = ct(l, {
          defaultValue: m,
          leftDate: g,
          rightDate: k,
          unit: yt,
          onParsedValueChanged: function (e, a) {
            if (l.unlinkPanels && a) {
              const t = (null == e ? void 0 : e.year()) || 0,
                l = (null == e ? void 0 : e.month()) || 0,
                n = a.year(),
                o = a.month()
              k.value = t === n && l === o ? a.add(1, yt) : a
            } else
              ((k.value = g.value.add(1, yt)),
                a && (k.value = k.value.hour(a.hour()).minute(a.minute()).second(a.second())))
          }
        }),
        j = h({ min: null, max: null }),
        z = h({ min: null, max: null }),
        W = y(
          () =>
            `${g.value.year()} ${F('el.datepicker.year')} ${F(`el.datepicker.month${g.value.month() + 1}`)}`
        ),
        H = y(
          () =>
            `${k.value.year()} ${F('el.datepicker.year')} ${F(`el.datepicker.month${k.value.month() + 1}`)}`
        ),
        G = y(() => g.value.year()),
        Q = y(() => g.value.month()),
        J = y(() => k.value.year()),
        ee = y(() => k.value.month()),
        ae = y(() => !!p.value.length),
        te = y(() =>
          null !== j.value.min ? j.value.min : w.value ? w.value.format(pe.value) : ''
        ),
        le = y(() =>
          null !== j.value.max
            ? j.value.max
            : D.value || w.value
              ? (D.value || w.value).format(pe.value)
              : ''
        ),
        ne = y(() =>
          null !== z.value.min ? z.value.min : w.value ? w.value.format(se.value) : ''
        ),
        oe = y(() =>
          null !== z.value.max
            ? z.value.max
            : D.value || w.value
              ? (D.value || w.value).format(se.value)
              : ''
        ),
        se = y(() => Ye(u)),
        pe = y(() => Oe(u)),
        me = () => {
          ;((g.value = g.value.subtract(1, 'year')),
            l.unlinkPanels || (k.value = g.value.add(1, 'month')),
            Se('year'))
        },
        he = () => {
          ;((g.value = g.value.subtract(1, 'month')),
            l.unlinkPanels || (k.value = g.value.add(1, 'month')),
            Se('month'))
        },
        ye = () => {
          ;(l.unlinkPanels
            ? (k.value = k.value.add(1, 'year'))
            : ((g.value = g.value.add(1, 'year')), (k.value = g.value.add(1, 'month'))),
            Se('year'))
        },
        be = () => {
          ;(l.unlinkPanels
            ? (k.value = k.value.add(1, 'month'))
            : ((g.value = g.value.add(1, 'month')), (k.value = g.value.add(1, 'month'))),
            Se('month'))
        },
        ke = () => {
          ;((g.value = g.value.add(1, 'year')), Se('year'))
        },
        we = () => {
          ;((g.value = g.value.add(1, 'month')), Se('month'))
        },
        De = () => {
          ;((k.value = k.value.subtract(1, 'year')), Se('year'))
        },
        xe = () => {
          ;((k.value = k.value.subtract(1, 'month')), Se('month'))
        },
        Se = (e) => {
          t('panel-change', [g.value.toDate(), k.value.toDate()], e)
        },
        Me = y(() => {
          const e = (Q.value + 1) % 12,
            a = Q.value + 1 >= 12 ? 1 : 0
          return l.unlinkPanels && new Date(G.value + a, e) < new Date(J.value, ee.value)
        }),
        Ce = y(
          () => l.unlinkPanels && 12 * J.value + ee.value - (12 * G.value + Q.value + 1) >= 12
        ),
        Pe = y(() => !(w.value && D.value && !x.value.selecting && Ya([w.value, D.value]))),
        _e = y(() => 'datetime' === l.type || 'datetimerange' === l.type),
        Ve = (a, t) => {
          if (a) {
            if (i) {
              return e(i[t] || i)
                .locale(b.value)
                .year(a.year())
                .month(a.month())
                .date(a.date())
            }
            return a
          }
        },
        $e = (e, a = !0) => {
          const l = e.minDate,
            n = e.maxDate,
            o = Ve(l, 0),
            r = Ve(n, 1)
          ;(D.value === r && w.value === o) ||
            (t('calendar-change', [l.toDate(), n && n.toDate()]),
            (D.value = r),
            (w.value = o),
            a && !_e.value && Y())
        },
        Ie = h(!1),
        Ae = h(!1),
        Ne = () => {
          Ie.value = !1
        },
        Te = () => {
          Ae.value = !1
        },
        Re = (a, t) => {
          j.value[t] = a
          const n = e(a, pe.value).locale(b.value)
          if (n.isValid()) {
            if (r && r(n.toDate())) return
            'min' === t
              ? ((g.value = n),
                (w.value = (w.value || g.value).year(n.year()).month(n.month()).date(n.date())),
                l.unlinkPanels ||
                  (D.value && !D.value.isBefore(w.value)) ||
                  ((k.value = n.add(1, 'month')), (D.value = w.value.add(1, 'month'))))
              : ((k.value = n),
                (D.value = (D.value || k.value).year(n.year()).month(n.month()).date(n.date())),
                l.unlinkPanels ||
                  (w.value && !w.value.isAfter(D.value)) ||
                  ((g.value = n.subtract(1, 'month')), (w.value = D.value.subtract(1, 'month'))))
          }
        },
        Ee = (e, a) => {
          j.value[a] = null
        },
        Be = (a, t) => {
          z.value[t] = a
          const l = e(a, se.value).locale(b.value)
          l.isValid() &&
            ('min' === t
              ? ((Ie.value = !0),
                (w.value = (w.value || g.value)
                  .hour(l.hour())
                  .minute(l.minute())
                  .second(l.second())),
                (D.value && !D.value.isBefore(w.value)) || (D.value = w.value))
              : ((Ae.value = !0),
                (D.value = (D.value || k.value)
                  .hour(l.hour())
                  .minute(l.minute())
                  .second(l.second())),
                (k.value = D.value),
                D.value && D.value.isBefore(w.value) && (w.value = D.value)))
        },
        Le = (e, a) => {
          ;((z.value[a] = null),
            'min' === a
              ? ((g.value = w.value), (Ie.value = !1))
              : ((k.value = D.value), (Ae.value = !1)))
        },
        Fe = (e, a, t) => {
          z.value.min ||
            (e &&
              ((g.value = e),
              (w.value = (w.value || g.value)
                .hour(e.hour())
                .minute(e.minute())
                .second(e.second()))),
            t || (Ie.value = a),
            (D.value && !D.value.isBefore(w.value)) || ((D.value = w.value), (k.value = e)))
        },
        je = (e, a, t) => {
          z.value.max ||
            (e &&
              ((k.value = e),
              (D.value = (D.value || k.value)
                .hour(e.hour())
                .minute(e.minute())
                .second(e.second()))),
            t || (Ae.value = a),
            D.value && D.value.isBefore(w.value) && (w.value = D.value))
        },
        ze = () => {
          ;((g.value = Ia(S(m), { lang: S(b), unit: 'month', unlinkPanels: l.unlinkPanels })[0]),
            (k.value = g.value.add(1, 'month')),
            t('pick', null))
        }
      return (
        t('set-picker-option', ['isValidValue', Ya]),
        t('set-picker-option', [
          'parseUserInput',
          (a) => (o(a) ? a.map((a) => e(a, u).locale(b.value)) : e(a, u).locale(b.value))
        ]),
        t('set-picker-option', [
          'formatToString',
          (e) => (o(e) ? e.map((e) => e.format(u)) : e.format(u))
        ]),
        t('set-picker-option', ['handleClear', ze]),
        (e, a) => (
          P(),
          T(
            'div',
            {
              class: $([
                S(M).b(),
                S(C).b(),
                { 'has-sidebar': e.$slots.sidebar || S(ae), 'has-time': S(_e) }
              ])
            },
            [
              R(
                'div',
                { class: $(S(M).e('body-wrapper')) },
                [
                  E(e.$slots, 'sidebar', { class: $(S(M).e('sidebar')) }),
                  S(ae)
                    ? (P(),
                      T(
                        'div',
                        { key: 0, class: $(S(M).e('sidebar')) },
                        [
                          (P(!0),
                          T(
                            K,
                            null,
                            U(
                              S(p),
                              (e, a) => (
                                P(),
                                T(
                                  'button',
                                  {
                                    key: a,
                                    type: 'button',
                                    class: $(S(M).e('shortcut')),
                                    onClick: (a) => S(A)(e)
                                  },
                                  B(e.text),
                                  11,
                                  vt
                                )
                              )
                            ),
                            128
                          ))
                        ],
                        2
                      ))
                    : N('v-if', !0),
                  R(
                    'div',
                    { class: $(S(M).e('body')) },
                    [
                      S(_e)
                        ? (P(),
                          T(
                            'div',
                            { key: 0, class: $(S(C).e('time-header')) },
                            [
                              R(
                                'span',
                                { class: $(S(C).e('editors-wrap')) },
                                [
                                  R(
                                    'span',
                                    { class: $(S(C).e('time-picker-wrap')) },
                                    [
                                      X(
                                        S(fe),
                                        {
                                          size: 'small',
                                          disabled: S(x).selecting,
                                          placeholder: S(F)('el.datepicker.startDate'),
                                          class: $(S(C).e('editor')),
                                          'model-value': S(te),
                                          'validate-event': !1,
                                          onInput: a[0] || (a[0] = (e) => Re(e, 'min')),
                                          onChange: a[1] || (a[1] = (e) => Ee(0, 'min'))
                                        },
                                        null,
                                        8,
                                        ['disabled', 'placeholder', 'class', 'model-value']
                                      )
                                    ],
                                    2
                                  ),
                                  Z(
                                    (P(),
                                    T(
                                      'span',
                                      { class: $(S(C).e('time-picker-wrap')) },
                                      [
                                        X(
                                          S(fe),
                                          {
                                            size: 'small',
                                            class: $(S(C).e('editor')),
                                            disabled: S(x).selecting,
                                            placeholder: S(F)('el.datepicker.startTime'),
                                            'model-value': S(ne),
                                            'validate-event': !1,
                                            onFocus: a[2] || (a[2] = (e) => (Ie.value = !0)),
                                            onInput: a[3] || (a[3] = (e) => Be(e, 'min')),
                                            onChange: a[4] || (a[4] = (e) => Le(0, 'min'))
                                          },
                                          null,
                                          8,
                                          ['class', 'disabled', 'placeholder', 'model-value']
                                        ),
                                        X(
                                          S(ra),
                                          {
                                            visible: Ie.value,
                                            format: S(se),
                                            'datetime-role': 'start',
                                            'time-arrow-control': S(d),
                                            'parsed-value': g.value,
                                            onPick: Fe
                                          },
                                          null,
                                          8,
                                          [
                                            'visible',
                                            'format',
                                            'time-arrow-control',
                                            'parsed-value'
                                          ]
                                        )
                                      ],
                                      2
                                    )),
                                    [[S(ge), Ne]]
                                  )
                                ],
                                2
                              ),
                              R('span', null, [
                                X(S(I), null, { default: V(() => [X(S(de))]), _: 1 })
                              ]),
                              R(
                                'span',
                                { class: $([S(C).e('editors-wrap'), 'is-right']) },
                                [
                                  R(
                                    'span',
                                    { class: $(S(C).e('time-picker-wrap')) },
                                    [
                                      X(
                                        S(fe),
                                        {
                                          size: 'small',
                                          class: $(S(C).e('editor')),
                                          disabled: S(x).selecting,
                                          placeholder: S(F)('el.datepicker.endDate'),
                                          'model-value': S(le),
                                          readonly: !S(w),
                                          'validate-event': !1,
                                          onInput: a[5] || (a[5] = (e) => Re(e, 'max')),
                                          onChange: a[6] || (a[6] = (e) => Ee(0, 'max'))
                                        },
                                        null,
                                        8,
                                        [
                                          'class',
                                          'disabled',
                                          'placeholder',
                                          'model-value',
                                          'readonly'
                                        ]
                                      )
                                    ],
                                    2
                                  ),
                                  Z(
                                    (P(),
                                    T(
                                      'span',
                                      { class: $(S(C).e('time-picker-wrap')) },
                                      [
                                        X(
                                          S(fe),
                                          {
                                            size: 'small',
                                            class: $(S(C).e('editor')),
                                            disabled: S(x).selecting,
                                            placeholder: S(F)('el.datepicker.endTime'),
                                            'model-value': S(oe),
                                            readonly: !S(w),
                                            'validate-event': !1,
                                            onFocus:
                                              a[7] || (a[7] = (e) => S(w) && (Ae.value = !0)),
                                            onInput: a[8] || (a[8] = (e) => Be(e, 'max')),
                                            onChange: a[9] || (a[9] = (e) => Le(0, 'max'))
                                          },
                                          null,
                                          8,
                                          [
                                            'class',
                                            'disabled',
                                            'placeholder',
                                            'model-value',
                                            'readonly'
                                          ]
                                        ),
                                        X(
                                          S(ra),
                                          {
                                            'datetime-role': 'end',
                                            visible: Ae.value,
                                            format: S(se),
                                            'time-arrow-control': S(d),
                                            'parsed-value': k.value,
                                            onPick: je
                                          },
                                          null,
                                          8,
                                          [
                                            'visible',
                                            'format',
                                            'time-arrow-control',
                                            'parsed-value'
                                          ]
                                        )
                                      ],
                                      2
                                    )),
                                    [[S(ge), Te]]
                                  )
                                ],
                                2
                              )
                            ],
                            2
                          ))
                        : N('v-if', !0),
                      R(
                        'div',
                        { class: $([[S(M).e('content'), S(C).e('content')], 'is-left']) },
                        [
                          R(
                            'div',
                            { class: $(S(C).e('header')) },
                            [
                              R(
                                'button',
                                {
                                  type: 'button',
                                  class: $([S(M).e('icon-btn'), 'd-arrow-left']),
                                  onClick: me
                                },
                                [X(S(I), null, { default: V(() => [X(S(ue))]), _: 1 })],
                                2
                              ),
                              R(
                                'button',
                                {
                                  type: 'button',
                                  class: $([S(M).e('icon-btn'), 'arrow-left']),
                                  onClick: he
                                },
                                [X(S(I), null, { default: V(() => [X(S(ie))]), _: 1 })],
                                2
                              ),
                              e.unlinkPanels
                                ? (P(),
                                  T(
                                    'button',
                                    {
                                      key: 0,
                                      type: 'button',
                                      disabled: !S(Ce),
                                      class: $([
                                        [S(M).e('icon-btn'), { 'is-disabled': !S(Ce) }],
                                        'd-arrow-right'
                                      ]),
                                      onClick: ke
                                    },
                                    [X(S(I), null, { default: V(() => [X(S(ce))]), _: 1 })],
                                    10,
                                    pt
                                  ))
                                : N('v-if', !0),
                              e.unlinkPanels
                                ? (P(),
                                  T(
                                    'button',
                                    {
                                      key: 1,
                                      type: 'button',
                                      disabled: !S(Me),
                                      class: $([
                                        [S(M).e('icon-btn'), { 'is-disabled': !S(Me) }],
                                        'arrow-right'
                                      ]),
                                      onClick: we
                                    },
                                    [X(S(I), null, { default: V(() => [X(S(de))]), _: 1 })],
                                    10,
                                    mt
                                  ))
                                : N('v-if', !0),
                              R('div', null, B(S(W)), 1)
                            ],
                            2
                          ),
                          X(
                            La,
                            {
                              'selection-mode': 'range',
                              date: g.value,
                              'min-date': S(w),
                              'max-date': S(D),
                              'range-state': S(x),
                              'disabled-date': S(r),
                              'cell-class-name': S(s),
                              onChangerange: S(O),
                              onPick: $e,
                              onSelect: S(L)
                            },
                            null,
                            8,
                            [
                              'date',
                              'min-date',
                              'max-date',
                              'range-state',
                              'disabled-date',
                              'cell-class-name',
                              'onChangerange',
                              'onSelect'
                            ]
                          )
                        ],
                        2
                      ),
                      R(
                        'div',
                        { class: $([[S(M).e('content'), S(C).e('content')], 'is-right']) },
                        [
                          R(
                            'div',
                            { class: $(S(C).e('header')) },
                            [
                              e.unlinkPanels
                                ? (P(),
                                  T(
                                    'button',
                                    {
                                      key: 0,
                                      type: 'button',
                                      disabled: !S(Ce),
                                      class: $([
                                        [S(M).e('icon-btn'), { 'is-disabled': !S(Ce) }],
                                        'd-arrow-left'
                                      ]),
                                      onClick: De
                                    },
                                    [X(S(I), null, { default: V(() => [X(S(ue))]), _: 1 })],
                                    10,
                                    ft
                                  ))
                                : N('v-if', !0),
                              e.unlinkPanels
                                ? (P(),
                                  T(
                                    'button',
                                    {
                                      key: 1,
                                      type: 'button',
                                      disabled: !S(Me),
                                      class: $([
                                        [S(M).e('icon-btn'), { 'is-disabled': !S(Me) }],
                                        'arrow-left'
                                      ]),
                                      onClick: xe
                                    },
                                    [X(S(I), null, { default: V(() => [X(S(ie))]), _: 1 })],
                                    10,
                                    ht
                                  ))
                                : N('v-if', !0),
                              R(
                                'button',
                                {
                                  type: 'button',
                                  class: $([S(M).e('icon-btn'), 'd-arrow-right']),
                                  onClick: ye
                                },
                                [X(S(I), null, { default: V(() => [X(S(ce))]), _: 1 })],
                                2
                              ),
                              R(
                                'button',
                                {
                                  type: 'button',
                                  class: $([S(M).e('icon-btn'), 'arrow-right']),
                                  onClick: be
                                },
                                [X(S(I), null, { default: V(() => [X(S(de))]), _: 1 })],
                                2
                              ),
                              R('div', null, B(S(H)), 1)
                            ],
                            2
                          ),
                          X(
                            La,
                            {
                              'selection-mode': 'range',
                              date: k.value,
                              'min-date': S(w),
                              'max-date': S(D),
                              'range-state': S(x),
                              'disabled-date': S(r),
                              'cell-class-name': S(s),
                              onChangerange: S(O),
                              onPick: $e,
                              onSelect: S(L)
                            },
                            null,
                            8,
                            [
                              'date',
                              'min-date',
                              'max-date',
                              'range-state',
                              'disabled-date',
                              'cell-class-name',
                              'onChangerange',
                              'onSelect'
                            ]
                          )
                        ],
                        2
                      )
                    ],
                    2
                  )
                ],
                2
              ),
              S(_e)
                ? (P(),
                  T(
                    'div',
                    { key: 0, class: $(S(M).e('footer')) },
                    [
                      S(c)
                        ? (P(),
                          _(
                            S(ve),
                            {
                              key: 0,
                              text: '',
                              size: 'small',
                              class: $(S(M).e('link-btn')),
                              onClick: ze
                            },
                            { default: V(() => [q(B(S(F)('el.datepicker.clear')), 1)]), _: 1 },
                            8,
                            ['class']
                          ))
                        : N('v-if', !0),
                      X(
                        S(ve),
                        {
                          plain: '',
                          size: 'small',
                          class: $(S(M).e('link-btn')),
                          disabled: S(Pe),
                          onClick: a[10] || (a[10] = (e) => S(Y)(!1))
                        },
                        { default: V(() => [q(B(S(F)('el.datepicker.confirm')), 1)]), _: 1 },
                        8,
                        ['class', 'disabled']
                      )
                    ],
                    2
                  ))
                : N('v-if', !0)
            ],
            2
          )
        )
      )
    }
  })
var gt = F(bt, [
  [
    '__file',
    '/home/runner/work/element-plus/element-plus/packages/components/date-picker/src/date-picker-com/panel-date-range.vue'
  ]
])
const kt = r({ ..._a }),
  wt = ['onClick'],
  Dt = ['disabled'],
  xt = ['disabled'],
  St = 'year',
  Mt = d({ name: 'DatePickerMonthRange' }),
  Ct = d({
    ...Mt,
    props: kt,
    emits: ['pick', 'set-picker-option'],
    setup(a, { emit: t }) {
      const l = a,
        { lang: n } = v(),
        o = f('EP_PICKER_BASE'),
        { shortcuts: r, disabledDate: s, format: u } = o.props,
        i = re(o.props, 'defaultValue'),
        d = h(e().locale(n.value)),
        c = h(e().locale(n.value).add(1, St)),
        {
          minDate: p,
          maxDate: m,
          rangeState: b,
          ppNs: g,
          drpNs: k,
          handleChangeRange: w,
          handleRangeConfirm: D,
          handleShortcutClick: x,
          onSelect: M
        } = ct(l, {
          defaultValue: i,
          leftDate: d,
          rightDate: c,
          unit: St,
          onParsedValueChanged: function (e, a) {
            if (l.unlinkPanels && a) {
              const t = (null == e ? void 0 : e.year()) || 0,
                l = a.year()
              c.value = t === l ? a.add(1, St) : a
            } else c.value = d.value.add(1, St)
          }
        }),
        C = y(() => !!r.length),
        {
          leftPrevYear: _,
          rightNextYear: O,
          leftNextYear: Y,
          rightPrevYear: A,
          leftLabel: L,
          rightLabel: F,
          leftYear: j,
          rightYear: z
        } = (({ unlinkPanels: e, leftDate: a, rightDate: t }) => {
          const { t: l } = v()
          return {
            leftPrevYear: () => {
              ;((a.value = a.value.subtract(1, 'year')),
                e.value || (t.value = t.value.subtract(1, 'year')))
            },
            rightNextYear: () => {
              ;(e.value || (a.value = a.value.add(1, 'year')), (t.value = t.value.add(1, 'year')))
            },
            leftNextYear: () => {
              a.value = a.value.add(1, 'year')
            },
            rightPrevYear: () => {
              t.value = t.value.subtract(1, 'year')
            },
            leftLabel: y(() => `${a.value.year()} ${l('el.datepicker.year')}`),
            rightLabel: y(() => `${t.value.year()} ${l('el.datepicker.year')}`),
            leftYear: y(() => a.value.year()),
            rightYear: y(() =>
              t.value.year() === a.value.year() ? a.value.year() + 1 : t.value.year()
            )
          }
        })({ unlinkPanels: re(l, 'unlinkPanels'), leftDate: d, rightDate: c }),
        W = y(() => l.unlinkPanels && z.value > j.value + 1),
        H = (e, a = !0) => {
          const t = e.minDate,
            l = e.maxDate
          ;(m.value === l && p.value === t) || ((m.value = l), (p.value = t), a && D())
        }
      return (
        t('set-picker-option', ['formatToString', (e) => e.map((e) => e.format(u))]),
        (e, a) => (
          P(),
          T(
            'div',
            {
              class: $([S(g).b(), S(k).b(), { 'has-sidebar': Boolean(e.$slots.sidebar) || S(C) }])
            },
            [
              R(
                'div',
                { class: $(S(g).e('body-wrapper')) },
                [
                  E(e.$slots, 'sidebar', { class: $(S(g).e('sidebar')) }),
                  S(C)
                    ? (P(),
                      T(
                        'div',
                        { key: 0, class: $(S(g).e('sidebar')) },
                        [
                          (P(!0),
                          T(
                            K,
                            null,
                            U(
                              S(r),
                              (e, a) => (
                                P(),
                                T(
                                  'button',
                                  {
                                    key: a,
                                    type: 'button',
                                    class: $(S(g).e('shortcut')),
                                    onClick: (a) => S(x)(e)
                                  },
                                  B(e.text),
                                  11,
                                  wt
                                )
                              )
                            ),
                            128
                          ))
                        ],
                        2
                      ))
                    : N('v-if', !0),
                  R(
                    'div',
                    { class: $(S(g).e('body')) },
                    [
                      R(
                        'div',
                        { class: $([[S(g).e('content'), S(k).e('content')], 'is-left']) },
                        [
                          R(
                            'div',
                            { class: $(S(k).e('header')) },
                            [
                              R(
                                'button',
                                {
                                  type: 'button',
                                  class: $([S(g).e('icon-btn'), 'd-arrow-left']),
                                  onClick: a[0] || (a[0] = (...e) => S(_) && S(_)(...e))
                                },
                                [X(S(I), null, { default: V(() => [X(S(ue))]), _: 1 })],
                                2
                              ),
                              e.unlinkPanels
                                ? (P(),
                                  T(
                                    'button',
                                    {
                                      key: 0,
                                      type: 'button',
                                      disabled: !S(W),
                                      class: $([
                                        [S(g).e('icon-btn'), { [S(g).is('disabled')]: !S(W) }],
                                        'd-arrow-right'
                                      ]),
                                      onClick: a[1] || (a[1] = (...e) => S(Y) && S(Y)(...e))
                                    },
                                    [X(S(I), null, { default: V(() => [X(S(ce))]), _: 1 })],
                                    10,
                                    Dt
                                  ))
                                : N('v-if', !0),
                              R('div', null, B(S(L)), 1)
                            ],
                            2
                          ),
                          X(
                            Ka,
                            {
                              'selection-mode': 'range',
                              date: d.value,
                              'min-date': S(p),
                              'max-date': S(m),
                              'range-state': S(b),
                              'disabled-date': S(s),
                              onChangerange: S(w),
                              onPick: H,
                              onSelect: S(M)
                            },
                            null,
                            8,
                            [
                              'date',
                              'min-date',
                              'max-date',
                              'range-state',
                              'disabled-date',
                              'onChangerange',
                              'onSelect'
                            ]
                          )
                        ],
                        2
                      ),
                      R(
                        'div',
                        { class: $([[S(g).e('content'), S(k).e('content')], 'is-right']) },
                        [
                          R(
                            'div',
                            { class: $(S(k).e('header')) },
                            [
                              e.unlinkPanels
                                ? (P(),
                                  T(
                                    'button',
                                    {
                                      key: 0,
                                      type: 'button',
                                      disabled: !S(W),
                                      class: $([
                                        [S(g).e('icon-btn'), { 'is-disabled': !S(W) }],
                                        'd-arrow-left'
                                      ]),
                                      onClick: a[2] || (a[2] = (...e) => S(A) && S(A)(...e))
                                    },
                                    [X(S(I), null, { default: V(() => [X(S(ue))]), _: 1 })],
                                    10,
                                    xt
                                  ))
                                : N('v-if', !0),
                              R(
                                'button',
                                {
                                  type: 'button',
                                  class: $([S(g).e('icon-btn'), 'd-arrow-right']),
                                  onClick: a[3] || (a[3] = (...e) => S(O) && S(O)(...e))
                                },
                                [X(S(I), null, { default: V(() => [X(S(ce))]), _: 1 })],
                                2
                              ),
                              R('div', null, B(S(F)), 1)
                            ],
                            2
                          ),
                          X(
                            Ka,
                            {
                              'selection-mode': 'range',
                              date: c.value,
                              'min-date': S(p),
                              'max-date': S(m),
                              'range-state': S(b),
                              'disabled-date': S(s),
                              onChangerange: S(w),
                              onPick: H,
                              onSelect: S(M)
                            },
                            null,
                            8,
                            [
                              'date',
                              'min-date',
                              'max-date',
                              'range-state',
                              'disabled-date',
                              'onChangerange',
                              'onSelect'
                            ]
                          )
                        ],
                        2
                      )
                    ],
                    2
                  )
                ],
                2
              )
            ],
            2
          )
        )
      )
    }
  })
var Pt = F(Ct, [
  [
    '__file',
    '/home/runner/work/element-plus/element-plus/packages/components/date-picker/src/date-picker-com/panel-month-range.vue'
  ]
])
;(e.extend(ua),
  e.extend(da),
  e.extend(Se),
  e.extend(ma),
  e.extend(ha),
  e.extend(ba),
  e.extend(ka),
  e.extend(Da))
const _t = d({
  name: 'ElDatePicker',
  install: null,
  props: Sa,
  emits: ['update:modelValue'],
  setup(e, { expose: a, emit: t, slots: l }) {
    const n = p('picker-panel')
    ;(C('ElPopperOptions', me(re(e, 'popperOptions'))), C(xa, { slots: l, pickerNs: n }))
    const o = h()
    a({
      focus: (e = !0) => {
        var a
        null == (a = o.value) || a.focus(e)
      },
      handleOpen: () => {
        var e
        null == (e = o.value) || e.handleOpen()
      },
      handleClose: () => {
        var e
        null == (e = o.value) || e.handleClose()
      }
    })
    const r = (e) => {
      t('update:modelValue', e)
    }
    return () => {
      var a
      const t = null != (a = e.format) ? a : _e[e.type] || Pe,
        n = (function (e) {
          switch (e) {
            case 'daterange':
            case 'datetimerange':
              return gt
            case 'monthrange':
              return Pt
            default:
              return it
          }
        })(e.type)
      return X(He, L(e, { format: t, type: e.type, ref: o, 'onUpdate:modelValue': r }), {
        default: (e) => X(n, e, null),
        'range-separator': l['range-separator']
      })
    }
  }
})
_t.install = (e) => {
  e.component(_t.name, _t)
}
const Vt = _t
export {
  He as C,
  Ce as D,
  Vt as E,
  na as T,
  Ue as a,
  Ze as b,
  Se as c,
  Le as d,
  ra as e,
  we as f,
  De as g,
  Be as t,
  Xe as u,
  ea as v
}
