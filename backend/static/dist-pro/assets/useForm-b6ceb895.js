import {
  aJ as e,
  aK as t,
  aL as l,
  aM as a,
  aN as n,
  aO as o,
  aP as s,
  aQ as r,
  aR as i,
  b as u,
  d as c,
  aS as d,
  g as p,
  ap as h,
  e as v,
  aT as f,
  aU as m,
  u as g,
  r as b,
  f as y,
  aV as k,
  a2 as w,
  o as x,
  l as S,
  m as C,
  y as V,
  s as N,
  k as T,
  n as E,
  x as M,
  G as I,
  j as O,
  E as A,
  aW as _,
  a1 as P,
  a5 as L,
  q as $,
  M as B,
  z as D,
  a6 as j,
  aX as R,
  aY as z,
  ak as F,
  _ as K,
  as as H,
  aZ as W,
  ar as U,
  t as q,
  a_ as Y,
  ao as G,
  F as X,
  aA as Z,
  am as Q,
  a$ as J,
  b0 as ee,
  ay as te,
  b1 as le,
  aq as ae,
  b2 as ne,
  b3 as oe,
  aD as se,
  L as re,
  w as ie,
  b4 as ue,
  b5 as ce,
  b6 as de,
  b7 as pe,
  b8 as he,
  b9 as ve,
  ba as fe,
  bb as me,
  at as ge,
  a0 as be,
  bc as ye,
  bd as ke,
  be as we,
  ai as xe,
  aH as Se,
  bf as Ce,
  ab as Ve,
  h as Ne,
  bg as Te,
  bh as Ee,
  bi as Me,
  N as Ie,
  az as Oe,
  i as Ae,
  aw as _e,
  bj as Pe,
  bk as Le,
  aC as $e,
  an as Be,
  bl as De,
  a as je,
  bm as Re,
  bn as ze,
  bo as Fe,
  bp as Ke,
  p as He,
  bq as We,
  br as Ue,
  bs as qe,
  bt as Ye,
  aj as Ge,
  bu as Xe,
  bv as Ze,
  bw as Qe,
  Z as Je,
  a7 as et,
  bx as tt,
  by as lt,
  bz as at,
  aE as nt,
  bA as ot,
  ax as st,
  ad as rt,
  H as it,
  J as ut,
  bB as ct,
  a9 as dt,
  aa as pt,
  bC as ht,
  I as vt,
  bD as ft,
  bE as mt,
  bF as gt,
  bG as bt,
  ag as yt,
  al as kt,
} from "./index-6b60d190.js";
import { E as wt, a as xt } from "./el-form-item-ce18addb.js";
import { a as St, E as Ct } from "./el-col-b8aa0d1a.js";
import "./el-tooltip-4ed993c7.js";
import { u as Vt, E as Nt, a as Tt } from "./el-popper-09548d54.js";
import { u as Et, E as Mt, i as It, a as Ot } from "./el-input-38d674e5.js";
/* empty css               */ import {
  E as At,
  a as _t,
  p as Pt,
  b as Lt,
} from "./el-checkbox-4903f610.js";
/* empty css                          */ import {
  t as $t,
  u as Bt,
  b as Dt,
  T as jt,
  d as Rt,
  a as zt,
  c as Ft,
  e as Kt,
  f as Ht,
  D as Wt,
  C as Ut,
  g as qt,
  h as Yt,
  v as Gt,
  E as Xt,
} from "./el-date-picker-91f17f23.js";
import { b as Zt, a as Qt, E as Jt } from "./el-radio-group-0c46635e.js";
import { E as el, a as tl, s as ll, b as al } from "./el-select-8805ff65.js";
import { E as nl } from "./el-switch-5507f2ea.js";
import { E as ol } from "./el-divider-2dd0a1ee.js";
import { _ as sl } from "./el-tree-84af12f2.js";
import { E as rl } from "./el-progress-31e0b945.js";
import { _ as il } from "./style.css_vue_type_style_index_0_src_true_lang-d8fdefc2.js";
import { U as ul, I as cl, C as dl } from "./event-5568c9d8.js";
import { d as pl } from "./debounce-5c500a3d.js";
import { i as hl } from "./isNil-1f22f7b0.js";
import { c as vl, e as fl } from "./strings-00317668.js";
import { s as ml, i as gl } from "./isEqual-b8d86c27.js";
import { s as bl } from "./scroll-6dba6951.js";
import { t as yl, E as kl } from "./index-b7c1540b.js";
import { C as wl } from "./index-fdfa028a.js";
import { i as xl } from "./validator-f032316f.js";
const Sl = (e) =>
    Array.from(
      e.querySelectorAll(
        'a[href],button:not([disabled]),button:not([hidden]),:not([tabindex="-1"]),input:not([disabled]),input:not([type="hidden"]),select:not([disabled]),textarea:not([disabled])',
      ),
    ).filter(
      (e) =>
        Cl(e) &&
        ((e) =>
          "fixed" !== getComputedStyle(e).position && null !== e.offsetParent)(
          e,
        ),
    ),
  Cl = (e) => {
    if (
      e.tabIndex > 0 ||
      (0 === e.tabIndex && null !== e.getAttribute("tabIndex"))
    )
      return !0;
    if (e.disabled) return !1;
    switch (e.nodeName) {
      case "A":
        return !!e.href && "ignore" !== e.rel;
      case "INPUT":
        return !("hidden" === e.type || "file" === e.type);
      case "BUTTON":
      case "SELECT":
      case "TEXTAREA":
        return !0;
      default:
        return !1;
    }
  },
  Vl = function (e, t, ...l) {
    let a;
    a =
      t.includes("mouse") || t.includes("click")
        ? "MouseEvents"
        : t.includes("key")
          ? "KeyboardEvent"
          : "HTMLEvents";
    const n = document.createEvent(a);
    return (n.initEvent(t, ...l), e.dispatchEvent(n), e);
  },
  Nl = (e) => !e.getAttribute("aria-owns"),
  Tl = (e, t, l) => {
    const { parentNode: a } = e;
    if (!a) return null;
    const n = a.querySelectorAll(l);
    return n[Array.prototype.indexOf.call(n, e) + t] || null;
  },
  El = (e) => {
    e && (e.focus(), !Nl(e) && e.click());
  },
  Ml = (t, l) => {
    if (!e || !t || !l) return !1;
    const a = t.getBoundingClientRect();
    let n;
    return (
      (n =
        l instanceof Element
          ? l.getBoundingClientRect()
          : {
              top: 0,
              right: window.innerWidth,
              bottom: window.innerHeight,
              left: 0,
            }),
      a.top < n.bottom &&
        a.bottom > n.top &&
        a.right > n.left &&
        a.left < n.right
    );
  },
  Il = (e) => {
    let t, l;
    return (
      "touchend" === e.type
        ? ((l = e.changedTouches[0].clientY), (t = e.changedTouches[0].clientX))
        : e.type.startsWith("touch")
          ? ((l = e.touches[0].clientY), (t = e.touches[0].clientX))
          : ((l = e.clientY), (t = e.clientX)),
      { clientX: t, clientY: l }
    );
  };
const Ol =
  l && 1 / ml(new l([, -0]))[1] == 1 / 0
    ? function (e) {
        return new l(e);
      }
    : function () {};
const Al = r(function (e) {
    return (function (e, t, l) {
      var r = -1,
        i = n,
        u = e.length,
        c = !0,
        d = [],
        p = d;
      if (l) ((c = !1), (i = o));
      else if (u >= 200) {
        var h = t ? null : Ol(e);
        if (h) return ml(h);
        ((c = !1), (i = s), (p = new a()));
      } else p = t ? [] : d;
      e: for (; ++r < u; ) {
        var v = e[r],
          f = t ? t(v) : v;
        if (((v = l || 0 !== v ? v : 0), c && f == f)) {
          for (var m = p.length; m--; ) if (p[m] === f) continue e;
          (t && p.push(f), d.push(v));
        } else i(p, f, l) || (p !== d && p.push(f), d.push(v));
      }
      return d;
    })(t(e, 1, i, !0));
  }),
  _l = (t) => (e ? window.requestAnimationFrame(t) : setTimeout(t, 16)),
  Pl = (t) => (e ? window.cancelAnimationFrame(t) : clearTimeout(t)),
  Ll = () => Math.floor(1e4 * Math.random()),
  $l = u({
    valueKey: { type: String, default: "value" },
    modelValue: { type: [String, Number], default: "" },
    debounce: { type: Number, default: 300 },
    placement: {
      type: c(String),
      values: [
        "top",
        "top-start",
        "top-end",
        "bottom",
        "bottom-start",
        "bottom-end",
      ],
      default: "bottom-start",
    },
    fetchSuggestions: { type: c([Function, Array]), default: d },
    popperClass: { type: String, default: "" },
    triggerOnFocus: { type: Boolean, default: !0 },
    selectWhenUnmatched: { type: Boolean, default: !1 },
    hideLoading: { type: Boolean, default: !1 },
    label: { type: String },
    teleported: Vt.teleported,
    highlightFirstItem: { type: Boolean, default: !1 },
    fitInputWidth: { type: Boolean, default: !1 },
    clearable: { type: Boolean, default: !1 },
    disabled: { type: Boolean, default: !1 },
    name: String,
  }),
  Bl = {
    [ul]: (e) => p(e),
    [cl]: (e) => p(e),
    [dl]: (e) => p(e),
    focus: (e) => e instanceof FocusEvent,
    blur: (e) => e instanceof FocusEvent,
    clear: () => !0,
    select: (e) => h(e),
  },
  Dl = ["aria-expanded", "aria-owns"],
  jl = { key: 0 },
  Rl = ["id", "aria-selected", "onClick"],
  zl = "ElAutocomplete",
  Fl = v({ name: zl, inheritAttrs: !1 });
const Kl = q(
    K(
      v({
        ...Fl,
        props: $l,
        emits: Bl,
        setup(e, { expose: t, emit: l }) {
          const a = e,
            n = Et(),
            o = f(),
            s = m(),
            r = g("autocomplete"),
            i = b(),
            u = b(),
            c = b(),
            d = b();
          let p = !1,
            h = !1;
          const v = b([]),
            K = b(-1),
            q = b(""),
            Y = b(!1),
            G = b(!1),
            X = b(!1),
            Z = y(() => r.b(String(Ll()))),
            Q = y(() => o.style),
            J = y(() => (v.value.length > 0 || X.value) && Y.value),
            ee = y(() => !a.hideLoading && X.value),
            te = y(() =>
              i.value ? Array.from(i.value.$el.querySelectorAll("input")) : [],
            ),
            le = async () => {
              (await H(),
                J.value && (q.value = `${i.value.$el.offsetWidth}px`));
            },
            ae = () => {
              K.value = -1;
            },
            ne = pl(async (e) => {
              if (G.value) return;
              const t = (e) => {
                ((X.value = !1),
                  G.value ||
                    (W(e)
                      ? ((v.value = e),
                        (K.value = a.highlightFirstItem ? 0 : -1))
                      : U(zl, "autocomplete suggestions must be an array")));
              };
              if (((X.value = !0), W(a.fetchSuggestions)))
                t(a.fetchSuggestions);
              else {
                const l = await a.fetchSuggestions(e, t);
                W(l) && t(l);
              }
            }, a.debounce),
            oe = (e) => {
              const t = !!e;
              if (
                (l(cl, e),
                l(ul, e),
                (G.value = !1),
                Y.value || (Y.value = t),
                !a.triggerOnFocus && !e)
              )
                return ((G.value = !0), void (v.value = []));
              ne(e);
            },
            se = (e) => {
              var t;
              s.value ||
                (("INPUT" !== (null == (t = e.target) ? void 0 : t.tagName) ||
                  te.value.includes(document.activeElement)) &&
                  (Y.value = !0));
            },
            re = (e) => {
              l(dl, e);
            },
            ie = (e) => {
              h
                ? (h = !1)
                : ((Y.value = !0),
                  l("focus", e),
                  a.triggerOnFocus && !p && ne(String(a.modelValue)));
            },
            ue = (e) => {
              setTimeout(() => {
                var t;
                (null == (t = c.value) ? void 0 : t.isFocusInsideContent())
                  ? (h = !0)
                  : (Y.value && he(), l("blur", e));
              });
            },
            ce = () => {
              ((Y.value = !1), l(ul, ""), l("clear"));
            },
            de = async () => {
              J.value && K.value >= 0 && K.value < v.value.length
                ? ve(v.value[K.value])
                : a.selectWhenUnmatched &&
                  (l("select", { value: a.modelValue }),
                  (v.value = []),
                  (K.value = -1));
            },
            pe = (e) => {
              J.value && (e.preventDefault(), e.stopPropagation(), he());
            },
            he = () => {
              Y.value = !1;
            },
            ve = async (e) => {
              (l(cl, e[a.valueKey]),
                l(ul, e[a.valueKey]),
                l("select", e),
                (v.value = []),
                (K.value = -1));
            },
            fe = (e) => {
              if (!J.value || X.value) return;
              if (e < 0) return void (K.value = -1);
              e >= v.value.length && (e = v.value.length - 1);
              const t = u.value.querySelector(`.${r.be("suggestion", "wrap")}`),
                l = t.querySelectorAll(`.${r.be("suggestion", "list")} li`)[e],
                a = t.scrollTop,
                { offsetTop: n, scrollHeight: o } = l;
              (n + o > a + t.clientHeight && (t.scrollTop += o),
                n < a && (t.scrollTop -= o),
                (K.value = e),
                i.value.ref.setAttribute(
                  "aria-activedescendant",
                  `${Z.value}-item-${K.value}`,
                ));
            };
          return (
            k(d, () => {
              J.value && he();
            }),
            w(() => {
              (i.value.ref.setAttribute("role", "textbox"),
                i.value.ref.setAttribute("aria-autocomplete", "list"),
                i.value.ref.setAttribute("aria-controls", "id"),
                i.value.ref.setAttribute(
                  "aria-activedescendant",
                  `${Z.value}-item-${K.value}`,
                ),
                (p = i.value.ref.hasAttribute("readonly")));
            }),
            t({
              highlightedIndex: K,
              activated: Y,
              loading: X,
              inputRef: i,
              popperRef: c,
              suggestions: v,
              handleSelect: ve,
              handleKeyEnter: de,
              focus: () => {
                var e;
                null == (e = i.value) || e.focus();
              },
              blur: () => {
                var e;
                null == (e = i.value) || e.blur();
              },
              close: he,
              highlight: fe,
            }),
            (e, t) => (
              x(),
              S(
                T(Nt),
                {
                  ref_key: "popperRef",
                  ref: c,
                  visible: T(J),
                  placement: e.placement,
                  "fallback-placements": ["bottom-start", "top-start"],
                  "popper-class": [T(r).e("popper"), e.popperClass],
                  teleported: e.teleported,
                  "gpu-acceleration": !1,
                  pure: "",
                  "manual-mode": "",
                  effect: "light",
                  trigger: "click",
                  transition: `${T(r).namespace.value}-zoom-in-top`,
                  persistent: "",
                  role: "listbox",
                  onBeforeShow: le,
                  onHide: ae,
                },
                {
                  content: C(() => [
                    V(
                      "div",
                      {
                        ref_key: "regionRef",
                        ref: u,
                        class: N([
                          T(r).b("suggestion"),
                          T(r).is("loading", T(ee)),
                        ]),
                        style: E({
                          [e.fitInputWidth ? "width" : "minWidth"]: q.value,
                          outline: "none",
                        }),
                        role: "region",
                      },
                      [
                        M(
                          T(I),
                          {
                            id: T(Z),
                            tag: "ul",
                            "wrap-class": T(r).be("suggestion", "wrap"),
                            "view-class": T(r).be("suggestion", "list"),
                            role: "listbox",
                          },
                          {
                            default: C(() => [
                              T(ee)
                                ? (x(),
                                  O("li", jl, [
                                    M(
                                      T(A),
                                      { class: N(T(r).is("loading")) },
                                      { default: C(() => [M(T(_))]), _: 1 },
                                      8,
                                      ["class"],
                                    ),
                                  ]))
                                : (x(!0),
                                  O(
                                    P,
                                    { key: 1 },
                                    L(
                                      v.value,
                                      (t, l) => (
                                        x(),
                                        O(
                                          "li",
                                          {
                                            id: `${T(Z)}-item-${l}`,
                                            key: l,
                                            class: N({
                                              highlighted: K.value === l,
                                            }),
                                            role: "option",
                                            "aria-selected": K.value === l,
                                            onClick: (e) => ve(t),
                                          },
                                          [
                                            $(
                                              e.$slots,
                                              "default",
                                              { item: t },
                                              () => [B(D(t[e.valueKey]), 1)],
                                            ),
                                          ],
                                          10,
                                          Rl,
                                        )
                                      ),
                                    ),
                                    128,
                                  )),
                            ]),
                            _: 3,
                          },
                          8,
                          ["id", "wrap-class", "view-class"],
                        ),
                      ],
                      6,
                    ),
                  ]),
                  default: C(() => [
                    V(
                      "div",
                      {
                        ref_key: "listboxRef",
                        ref: d,
                        class: N([T(r).b(), e.$attrs.class]),
                        style: E(T(Q)),
                        role: "combobox",
                        "aria-haspopup": "listbox",
                        "aria-expanded": T(J),
                        "aria-owns": T(Z),
                      },
                      [
                        M(
                          T(Mt),
                          j({ ref_key: "inputRef", ref: i }, T(n), {
                            clearable: e.clearable,
                            disabled: T(s),
                            name: e.name,
                            "model-value": e.modelValue,
                            onInput: oe,
                            onChange: re,
                            onFocus: ie,
                            onBlur: ue,
                            onClear: ce,
                            onKeydown: [
                              t[0] ||
                                (t[0] = R(
                                  z((e) => fe(K.value - 1), ["prevent"]),
                                  ["up"],
                                )),
                              t[1] ||
                                (t[1] = R(
                                  z((e) => fe(K.value + 1), ["prevent"]),
                                  ["down"],
                                )),
                              R(de, ["enter"]),
                              R(he, ["tab"]),
                              R(pe, ["esc"]),
                            ],
                            onMousedown: se,
                          }),
                          F({ _: 2 }, [
                            e.$slots.prepend
                              ? {
                                  name: "prepend",
                                  fn: C(() => [$(e.$slots, "prepend")]),
                                }
                              : void 0,
                            e.$slots.append
                              ? {
                                  name: "append",
                                  fn: C(() => [$(e.$slots, "append")]),
                                }
                              : void 0,
                            e.$slots.prefix
                              ? {
                                  name: "prefix",
                                  fn: C(() => [$(e.$slots, "prefix")]),
                                }
                              : void 0,
                            e.$slots.suffix
                              ? {
                                  name: "suffix",
                                  fn: C(() => [$(e.$slots, "suffix")]),
                                }
                              : void 0,
                          ]),
                          1040,
                          [
                            "clearable",
                            "disabled",
                            "name",
                            "model-value",
                            "onKeydown",
                          ],
                        ),
                      ],
                      14,
                      Dl,
                    ),
                  ]),
                  _: 3,
                },
                8,
                [
                  "visible",
                  "placement",
                  "popper-class",
                  "teleported",
                  "transition",
                ],
              )
            )
          );
        },
      }),
      [
        [
          "__file",
          "/home/runner/work/element-plus/element-plus/packages/components/autocomplete/src/autocomplete.vue",
        ],
      ],
    ),
  ),
  Hl = u({ ...$t, parsedValue: { type: c(Array) } }),
  Wl = ["disabled"];
var Ul = K(
  v({
    __name: "panel-time-range",
    props: Hl,
    emits: ["pick", "select-range", "set-picker-option"],
    setup(e, { emit: t }) {
      const l = e,
        a = (e, t) => {
          const l = [];
          for (let a = e; a <= t; a++) l.push(a);
          return l;
        },
        { t: n, lang: o } = Y(),
        s = g("time"),
        r = g("picker"),
        i = G("EP_PICKER_BASE"),
        {
          arrowControl: u,
          disabledHours: c,
          disabledMinutes: d,
          disabledSeconds: p,
          defaultValue: h,
        } = i.props,
        v = y(() => [
          s.be("range-picker", "body"),
          s.be("panel", "content"),
          s.is("arrow", u),
          S.value ? "has-seconds" : "",
        ]),
        f = y(() => [
          s.be("range-picker", "body"),
          s.be("panel", "content"),
          s.is("arrow", u),
          S.value ? "has-seconds" : "",
        ]),
        m = y(() => l.parsedValue[0]),
        k = y(() => l.parsedValue[1]),
        w = Bt(l),
        S = y(() => l.format.includes("ss")),
        C = y(() =>
          l.format.includes("A") ? "A" : l.format.includes("a") ? "a" : "",
        ),
        E = (e) => {
          A(e.millisecond(0), k.value);
        },
        I = (e) => {
          A(m.value, e.millisecond(0));
        },
        A = (e, l) => {
          t("pick", [e, l], !0);
        },
        _ = y(() => m.value > k.value),
        P = b([0, 2]),
        L = (e, l) => {
          (t("select-range", e, l, "min"), (P.value = [e, l]));
        },
        $ = y(() => (S.value ? 11 : 8)),
        B = (e, l) => {
          t("select-range", e, l, "max");
          const a = T($);
          P.value = [e + a, l + a];
        },
        j = (e, t) => {
          const l = c ? c(e) : [],
            n = "start" === e,
            o = (t || (n ? k.value : m.value)).hour(),
            s = n ? a(o + 1, 23) : a(0, o - 1);
          return Al(l, s);
        },
        R = (e, t, l) => {
          const n = d ? d(e, t) : [],
            o = "start" === t,
            s = l || (o ? k.value : m.value);
          if (e !== s.hour()) return n;
          const r = s.minute(),
            i = o ? a(r + 1, 59) : a(0, r - 1);
          return Al(n, i);
        },
        z = (e, t, l, n) => {
          const o = p ? p(e, t, l) : [],
            s = "start" === l,
            r = n || (s ? k.value : m.value),
            i = r.hour(),
            u = r.minute();
          if (e !== i || t !== u) return o;
          const c = r.second(),
            d = s ? a(c + 1, 59) : a(0, c - 1);
          return Al(o, d);
        },
        F = ([e, t]) => [Q(e, "start", !0, t), Q(t, "end", !1, e)],
        {
          getAvailableHours: K,
          getAvailableMinutes: H,
          getAvailableSeconds: U,
        } = Dt(j, R, z),
        {
          timePickerOptions: q,
          getAvailableTime: Q,
          onSetOption: J,
        } = zt({
          getAvailableHours: K,
          getAvailableMinutes: H,
          getAvailableSeconds: U,
        });
      return (
        t("set-picker-option", [
          "formatToString",
          (e) =>
            e
              ? W(e)
                ? e.map((e) => e.format(l.format))
                : e.format(l.format)
              : null,
        ]),
        t("set-picker-option", [
          "parseUserInput",
          (e) =>
            e
              ? W(e)
                ? e.map((e) => Rt(e, l.format).locale(o.value))
                : Rt(e, l.format).locale(o.value)
              : null,
        ]),
        t("set-picker-option", [
          "isValidValue",
          (e) => {
            const t = e.map((e) => Rt(e).locale(o.value)),
              l = F(t);
            return t[0].isSame(l[0]) && t[1].isSame(l[1]);
          },
        ]),
        t("set-picker-option", [
          "handleKeydownInput",
          (e) => {
            const t = e.code,
              { left: l, right: a, up: n, down: o } = Z;
            if ([l, a].includes(t)) {
              return (
                ((e) => {
                  const t = S.value ? [0, 3, 6, 11, 14, 17] : [0, 3, 8, 11],
                    l = ["hours", "minutes"].concat(S.value ? ["seconds"] : []),
                    a = (t.indexOf(P.value[0]) + e + t.length) % t.length,
                    n = t.length / 2;
                  a < n
                    ? q.start_emitSelectRange(l[a])
                    : q.end_emitSelectRange(l[a - n]);
                })(t === l ? -1 : 1),
                void e.preventDefault()
              );
            }
            if ([n, o].includes(t)) {
              const l = t === n ? -1 : 1,
                a = P.value[0] < $.value ? "start" : "end";
              return (q[`${a}_scrollDown`](l), void e.preventDefault());
            }
          },
        ]),
        t("set-picker-option", [
          "getDefaultValue",
          () => {
            if (W(h)) return h.map((e) => Rt(e).locale(o.value));
            const e = Rt(h).locale(o.value);
            return [e, e.add(60, "m")];
          },
        ]),
        t("set-picker-option", ["getRangeAvailableTime", F]),
        (e, l) =>
          e.actualVisible
            ? (x(),
              O(
                "div",
                { key: 0, class: N([T(s).b("range-picker"), T(r).b("panel")]) },
                [
                  V(
                    "div",
                    { class: N(T(s).be("range-picker", "content")) },
                    [
                      V(
                        "div",
                        { class: N(T(s).be("range-picker", "cell")) },
                        [
                          V(
                            "div",
                            { class: N(T(s).be("range-picker", "header")) },
                            D(T(n)("el.datepicker.startTime")),
                            3,
                          ),
                          V(
                            "div",
                            { class: N(T(v)) },
                            [
                              M(
                                jt,
                                {
                                  ref: "minSpinner",
                                  role: "start",
                                  "show-seconds": T(S),
                                  "am-pm-mode": T(C),
                                  "arrow-control": T(u),
                                  "spinner-date": T(m),
                                  "disabled-hours": j,
                                  "disabled-minutes": R,
                                  "disabled-seconds": z,
                                  onChange: E,
                                  onSetOption: T(J),
                                  onSelectRange: L,
                                },
                                null,
                                8,
                                [
                                  "show-seconds",
                                  "am-pm-mode",
                                  "arrow-control",
                                  "spinner-date",
                                  "onSetOption",
                                ],
                              ),
                            ],
                            2,
                          ),
                        ],
                        2,
                      ),
                      V(
                        "div",
                        { class: N(T(s).be("range-picker", "cell")) },
                        [
                          V(
                            "div",
                            { class: N(T(s).be("range-picker", "header")) },
                            D(T(n)("el.datepicker.endTime")),
                            3,
                          ),
                          V(
                            "div",
                            { class: N(T(f)) },
                            [
                              M(
                                jt,
                                {
                                  ref: "maxSpinner",
                                  role: "end",
                                  "show-seconds": T(S),
                                  "am-pm-mode": T(C),
                                  "arrow-control": T(u),
                                  "spinner-date": T(k),
                                  "disabled-hours": j,
                                  "disabled-minutes": R,
                                  "disabled-seconds": z,
                                  onChange: I,
                                  onSetOption: T(J),
                                  onSelectRange: B,
                                },
                                null,
                                8,
                                [
                                  "show-seconds",
                                  "am-pm-mode",
                                  "arrow-control",
                                  "spinner-date",
                                  "onSetOption",
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
                  V(
                    "div",
                    { class: N(T(s).be("panel", "footer")) },
                    [
                      V(
                        "button",
                        {
                          type: "button",
                          class: N([T(s).be("panel", "btn"), "cancel"]),
                          onClick:
                            l[0] ||
                            (l[0] = (e) => {
                              t("pick", w.value, !1);
                            }),
                        },
                        D(T(n)("el.datepicker.cancel")),
                        3,
                      ),
                      V(
                        "button",
                        {
                          type: "button",
                          class: N([T(s).be("panel", "btn"), "confirm"]),
                          disabled: T(_),
                          onClick:
                            l[1] ||
                            (l[1] = (e) =>
                              ((e = !1) => {
                                t("pick", [m.value, k.value], e);
                              })()),
                        },
                        D(T(n)("el.datepicker.confirm")),
                        11,
                        Wl,
                      ),
                    ],
                    2,
                  ),
                ],
                2,
              ))
            : X("v-if", !0)
      );
    },
  }),
  [
    [
      "__file",
      "/home/runner/work/element-plus/element-plus/packages/components/time-picker/src/time-picker-com/panel-time-range.vue",
    ],
  ],
);
Rt.extend(Ft);
var ql = v({
  name: "ElTimePicker",
  install: null,
  props: { ...Kt, isRange: { type: Boolean, default: !1 } },
  emits: ["update:modelValue"],
  setup(e, t) {
    const l = b(),
      [a, n] = e.isRange ? ["timerange", Ul] : ["time", Ht],
      o = (e) => t.emit("update:modelValue", e);
    return (
      Q("ElPopperOptions", e.popperOptions),
      t.expose({
        focus: (e) => {
          var t;
          null == (t = l.value) || t.handleFocusInput(e);
        },
        blur: (e) => {
          var t;
          null == (t = l.value) || t.handleBlurInput(e);
        },
        handleOpen: () => {
          var e;
          null == (e = l.value) || e.handleOpen();
        },
        handleClose: () => {
          var e;
          null == (e = l.value) || e.handleClose();
        },
      }),
      () => {
        var t;
        const s = null != (t = e.format) ? t : Wt;
        return M(
          Ut,
          j(e, { ref: l, type: a, format: s, "onUpdate:modelValue": o }),
          { default: (e) => M(n, e, null) },
        );
      }
    );
  },
});
const Yl = ql;
Yl.install = (e) => {
  e.component(Yl.name, Yl);
};
const Gl = Yl;
var Xl = v({
  name: "NodeContent",
  setup: () => ({ ns: g("cascader-node") }),
  render() {
    const { ns: e } = this,
      { node: t, panel: l } = this.$parent,
      { data: a, label: n } = t,
      { renderLabelFn: o } = l;
    return J("span", { class: e.e("label") }, o ? o({ node: t, data: a }) : n);
  },
});
const Zl = Symbol(),
  Ql = v({
    name: "ElCascaderNode",
    components: {
      ElCheckbox: At,
      ElRadio: Zt,
      NodeContent: Xl,
      ElIcon: A,
      Check: ee,
      Loading: _,
      ArrowRight: te,
    },
    props: { node: { type: Object, required: !0 }, menuId: String },
    emits: ["expand"],
    setup(e, { emit: t }) {
      const l = G(Zl),
        a = g("cascader-node"),
        n = y(() => l.isHoverMenu),
        o = y(() => l.config.multiple),
        s = y(() => l.config.checkStrictly),
        r = y(() => {
          var e;
          return null == (e = l.checkedNodes[0]) ? void 0 : e.uid;
        }),
        i = y(() => e.node.isDisabled),
        u = y(() => e.node.isLeaf),
        c = y(() => (s.value && !u.value) || !i.value),
        d = y(() => h(l.expandingNode)),
        p = y(() => s.value && l.checkedNodes.some(h)),
        h = (t) => {
          var l;
          const { level: a, uid: n } = e.node;
          return (
            (null == (l = null == t ? void 0 : t.pathNodes[a - 1])
              ? void 0
              : l.uid) === n
          );
        },
        v = () => {
          d.value || l.expandNode(e.node);
        },
        f = (t) => {
          const { node: a } = e;
          t !== a.checked && l.handleCheckChange(a, t);
        },
        m = () => {
          l.lazyLoad(e.node, () => {
            u.value || v();
          });
        },
        b = () => {
          const { node: t } = e;
          c.value && !t.loading && (t.loaded ? v() : m());
        },
        k = (t) => {
          e.node.loaded ? (f(t), !s.value && v()) : m();
        };
      return {
        panel: l,
        isHoverMenu: n,
        multiple: o,
        checkStrictly: s,
        checkedNodeId: r,
        isDisabled: i,
        isLeaf: u,
        expandable: c,
        inExpandingPath: d,
        inCheckedPath: p,
        ns: a,
        handleHoverExpand: (e) => {
          n.value && (b(), !u.value && t("expand", e));
        },
        handleExpand: b,
        handleClick: () => {
          (n.value && !u.value) ||
            (!u.value || i.value || s.value || o.value ? b() : k(!0));
        },
        handleCheck: k,
        handleSelectCheck: (t) => {
          s.value ? (f(t), e.node.loaded && v()) : k(t);
        },
      };
    },
  }),
  Jl = ["id", "aria-haspopup", "aria-owns", "aria-expanded", "tabindex"],
  ea = V("span", null, null, -1);
const ta = v({
  name: "ElCascaderMenu",
  components: {
    Loading: _,
    ElIcon: A,
    ElScrollbar: I,
    ElCascaderNode: K(Ql, [
      [
        "render",
        function (e, t, l, a, n, o) {
          const s = le("el-checkbox"),
            r = le("el-radio"),
            i = le("check"),
            u = le("el-icon"),
            c = le("node-content"),
            d = le("loading"),
            p = le("arrow-right");
          return (
            x(),
            O(
              "li",
              {
                id: `${e.menuId}-${e.node.uid}`,
                role: "menuitem",
                "aria-haspopup": !e.isLeaf,
                "aria-owns": e.isLeaf ? null : e.menuId,
                "aria-expanded": e.inExpandingPath,
                tabindex: e.expandable ? -1 : void 0,
                class: N([
                  e.ns.b(),
                  e.ns.is("selectable", e.checkStrictly),
                  e.ns.is("active", e.node.checked),
                  e.ns.is("disabled", !e.expandable),
                  e.inExpandingPath && "in-active-path",
                  e.inCheckedPath && "in-checked-path",
                ]),
                onMouseenter:
                  t[2] ||
                  (t[2] = (...t) =>
                    e.handleHoverExpand && e.handleHoverExpand(...t)),
                onFocus:
                  t[3] ||
                  (t[3] = (...t) =>
                    e.handleHoverExpand && e.handleHoverExpand(...t)),
                onClick:
                  t[4] ||
                  (t[4] = (...t) => e.handleClick && e.handleClick(...t)),
              },
              [
                X(" prefix "),
                e.multiple
                  ? (x(),
                    S(
                      s,
                      {
                        key: 0,
                        "model-value": e.node.checked,
                        indeterminate: e.node.indeterminate,
                        disabled: e.isDisabled,
                        onClick: t[0] || (t[0] = z(() => {}, ["stop"])),
                        "onUpdate:modelValue": e.handleSelectCheck,
                      },
                      null,
                      8,
                      [
                        "model-value",
                        "indeterminate",
                        "disabled",
                        "onUpdate:modelValue",
                      ],
                    ))
                  : e.checkStrictly
                    ? (x(),
                      S(
                        r,
                        {
                          key: 1,
                          "model-value": e.checkedNodeId,
                          label: e.node.uid,
                          disabled: e.isDisabled,
                          "onUpdate:modelValue": e.handleSelectCheck,
                          onClick: t[1] || (t[1] = z(() => {}, ["stop"])),
                        },
                        {
                          default: C(() => [
                            X(
                              "\n        Add an empty element to avoid render label,\n        do not use empty fragment here for https://github.com/vuejs/vue-next/pull/2485\n      ",
                            ),
                            ea,
                          ]),
                          _: 1,
                        },
                        8,
                        [
                          "model-value",
                          "label",
                          "disabled",
                          "onUpdate:modelValue",
                        ],
                      ))
                    : e.isLeaf && e.node.checked
                      ? (x(),
                        S(
                          u,
                          { key: 2, class: N(e.ns.e("prefix")) },
                          { default: C(() => [M(i)]), _: 1 },
                          8,
                          ["class"],
                        ))
                      : X("v-if", !0),
                X(" content "),
                M(c),
                X(" postfix "),
                e.isLeaf
                  ? X("v-if", !0)
                  : (x(),
                    O(
                      P,
                      { key: 3 },
                      [
                        e.node.loading
                          ? (x(),
                            S(
                              u,
                              {
                                key: 0,
                                class: N([
                                  e.ns.is("loading"),
                                  e.ns.e("postfix"),
                                ]),
                              },
                              { default: C(() => [M(d)]), _: 1 },
                              8,
                              ["class"],
                            ))
                          : (x(),
                            S(
                              u,
                              {
                                key: 1,
                                class: N(["arrow-right", e.ns.e("postfix")]),
                              },
                              { default: C(() => [M(p)]), _: 1 },
                              8,
                              ["class"],
                            )),
                      ],
                      64,
                    )),
              ],
              42,
              Jl,
            )
          );
        },
      ],
      [
        "__file",
        "/home/runner/work/element-plus/element-plus/packages/components/cascader-panel/src/node.vue",
      ],
    ]),
  },
  props: {
    nodes: { type: Array, required: !0 },
    index: { type: Number, required: !0 },
  },
  setup(e) {
    const t = ae(),
      l = g("cascader-menu"),
      { t: a } = Y(),
      n = Ll();
    let o = null,
      s = null;
    const r = G(Zl),
      i = b(null),
      u = y(() => !e.nodes.length),
      c = y(() => !r.initialLoaded),
      d = y(() => `cascader-menu-${n}-${e.index}`),
      p = () => {
        s && (clearTimeout(s), (s = null));
      },
      h = () => {
        i.value && ((i.value.innerHTML = ""), p());
      };
    return {
      ns: l,
      panel: r,
      hoverZone: i,
      isEmpty: u,
      isLoading: c,
      menuId: d,
      t: a,
      handleExpand: (e) => {
        o = e.target;
      },
      handleMouseMove: (e) => {
        if (r.isHoverMenu && o && i.value)
          if (o.contains(e.target)) {
            p();
            const l = t.vnode.el,
              { left: a } = l.getBoundingClientRect(),
              { offsetWidth: n, offsetHeight: s } = l,
              r = e.clientX - a,
              u = o.offsetTop,
              c = u + o.offsetHeight;
            i.value.innerHTML = `\n          <path style="pointer-events: auto;" fill="transparent" d="M${r} ${u} L${n} 0 V${u} Z" />\n          <path style="pointer-events: auto;" fill="transparent" d="M${r} ${c} L${n} ${s} V${c} Z" />\n        `;
          } else s || (s = window.setTimeout(h, r.config.hoverThreshold));
      },
      clearHoverZone: h,
    };
  },
});
var la = K(ta, [
  [
    "render",
    function (e, t, l, a, n, o) {
      const s = le("el-cascader-node"),
        r = le("loading"),
        i = le("el-icon"),
        u = le("el-scrollbar");
      return (
        x(),
        S(
          u,
          {
            key: e.menuId,
            tag: "ul",
            role: "menu",
            class: N(e.ns.b()),
            "wrap-class": e.ns.e("wrap"),
            "view-class": [e.ns.e("list"), e.ns.is("empty", e.isEmpty)],
            onMousemove: e.handleMouseMove,
            onMouseleave: e.clearHoverZone,
          },
          {
            default: C(() => {
              var t;
              return [
                (x(!0),
                O(
                  P,
                  null,
                  L(
                    e.nodes,
                    (t) => (
                      x(),
                      S(
                        s,
                        {
                          key: t.uid,
                          node: t,
                          "menu-id": e.menuId,
                          onExpand: e.handleExpand,
                        },
                        null,
                        8,
                        ["node", "menu-id", "onExpand"],
                      )
                    ),
                  ),
                  128,
                )),
                e.isLoading
                  ? (x(),
                    O(
                      "div",
                      { key: 0, class: N(e.ns.e("empty-text")) },
                      [
                        M(
                          i,
                          { size: "14", class: N(e.ns.is("loading")) },
                          { default: C(() => [M(r)]), _: 1 },
                          8,
                          ["class"],
                        ),
                        B(" " + D(e.t("el.cascader.loading")), 1),
                      ],
                      2,
                    ))
                  : e.isEmpty
                    ? (x(),
                      O(
                        "div",
                        { key: 1, class: N(e.ns.e("empty-text")) },
                        D(e.t("el.cascader.noData")),
                        3,
                      ))
                    : (null == (t = e.panel) ? void 0 : t.isHoverMenu)
                      ? (x(),
                        O(
                          "svg",
                          {
                            key: 2,
                            ref: "hoverZone",
                            class: N(e.ns.e("hover-zone")),
                          },
                          null,
                          2,
                        ))
                      : X("v-if", !0),
              ];
            }),
            _: 1,
          },
          8,
          ["class", "wrap-class", "view-class", "onMousemove", "onMouseleave"],
        )
      );
    },
  ],
  [
    "__file",
    "/home/runner/work/element-plus/element-plus/packages/components/cascader-panel/src/menu.vue",
  ],
]);
let aa = 0;
class na {
  constructor(e, t, l, a = !1) {
    ((this.data = e),
      (this.config = t),
      (this.parent = l),
      (this.root = a),
      (this.uid = aa++),
      (this.checked = !1),
      (this.indeterminate = !1),
      (this.loading = !1));
    const { value: n, label: o, children: s } = t,
      r = e[s],
      i = ((e) => {
        const t = [e];
        let { parent: l } = e;
        for (; l; ) (t.unshift(l), (l = l.parent));
        return t;
      })(this);
    ((this.level = a ? 0 : l ? l.level + 1 : 1),
      (this.value = e[n]),
      (this.label = e[o]),
      (this.pathNodes = i),
      (this.pathValues = i.map((e) => e.value)),
      (this.pathLabels = i.map((e) => e.label)),
      (this.childrenData = r),
      (this.children = (r || []).map((e) => new na(e, t, this))),
      (this.loaded = !t.lazy || this.isLeaf || !ne(r)));
  }
  get isDisabled() {
    const { data: e, parent: t, config: l } = this,
      { disabled: a, checkStrictly: n } = l;
    return (
      (oe(a) ? a(e, this) : !!e[a]) ||
      (!n && (null == t ? void 0 : t.isDisabled))
    );
  }
  get isLeaf() {
    const { data: e, config: t, childrenData: l, loaded: a } = this,
      { lazy: n, leaf: o } = t,
      s = oe(o) ? o(e, this) : e[o];
    return se(s) ? !(n && !a) && !(Array.isArray(l) && l.length) : !!s;
  }
  get valueByOption() {
    return this.config.emitPath ? this.pathValues : this.value;
  }
  appendChild(e) {
    const { childrenData: t, children: l } = this,
      a = new na(e, this.config, this);
    return (
      Array.isArray(t) ? t.push(e) : (this.childrenData = [e]),
      l.push(a),
      a
    );
  }
  calcText(e, t) {
    const l = e ? this.pathLabels.join(t) : this.label;
    return ((this.text = l), l);
  }
  broadcast(e, ...t) {
    const l = `onParent${vl(e)}`;
    this.children.forEach((a) => {
      a && (a.broadcast(e, ...t), a[l] && a[l](...t));
    });
  }
  emit(e, ...t) {
    const { parent: l } = this,
      a = `onChild${vl(e)}`;
    l && (l[a] && l[a](...t), l.emit(e, ...t));
  }
  onParentCheck(e) {
    this.isDisabled || this.setCheckState(e);
  }
  onChildCheck() {
    const { children: e } = this,
      t = e.filter((e) => !e.isDisabled),
      l = !!t.length && t.every((e) => e.checked);
    this.setCheckState(l);
  }
  setCheckState(e) {
    const t = this.children.length,
      l = this.children.reduce(
        (e, t) => e + (t.checked ? 1 : t.indeterminate ? 0.5 : 0),
        0,
      );
    ((this.checked =
      this.loaded &&
      this.children
        .filter((e) => !e.isDisabled)
        .every((e) => e.loaded && e.checked) &&
      e),
      (this.indeterminate = this.loaded && l !== t && l > 0));
  }
  doCheck(e) {
    if (this.checked === e) return;
    const { checkStrictly: t, multiple: l } = this.config;
    t || !l
      ? (this.checked = e)
      : (this.broadcast("check", e), this.setCheckState(e), this.emit("check"));
  }
}
const oa = (e, t) =>
  e.reduce(
    (e, l) => (
      l.isLeaf
        ? e.push(l)
        : (!t && e.push(l), (e = e.concat(oa(l.children, t)))),
      e
    ),
    [],
  );
class sa {
  constructor(e, t) {
    this.config = t;
    const l = (e || []).map((e) => new na(e, this.config));
    ((this.nodes = l),
      (this.allNodes = oa(l, !1)),
      (this.leafNodes = oa(l, !0)));
  }
  getNodes() {
    return this.nodes;
  }
  getFlattedNodes(e) {
    return e ? this.leafNodes : this.allNodes;
  }
  appendNode(e, t) {
    const l = t ? t.appendChild(e) : new na(e, this.config);
    (t || this.nodes.push(l),
      this.allNodes.push(l),
      l.isLeaf && this.leafNodes.push(l));
  }
  appendNodes(e, t) {
    e.forEach((e) => this.appendNode(e, t));
  }
  getNodeByValue(e, t = !1) {
    if (!e && 0 !== e) return null;
    return (
      this.getFlattedNodes(t).find(
        (t) => gl(t.value, e) || gl(t.pathValues, e),
      ) || null
    );
  }
  getSameNode(e) {
    if (!e) return null;
    return (
      this.getFlattedNodes(!1).find(
        ({ value: t, level: l }) => gl(e.value, t) && e.level === l,
      ) || null
    );
  }
}
const ra = u({
    modelValue: { type: c([Number, String, Array]) },
    options: { type: c(Array), default: () => [] },
    props: { type: c(Object), default: () => ({}) },
  }),
  ia = {
    expandTrigger: "click",
    multiple: !1,
    checkStrictly: !1,
    emitPath: !0,
    lazy: !1,
    lazyLoad: d,
    value: "value",
    label: "label",
    children: "children",
    leaf: "leaf",
    disabled: "disabled",
    hoverThreshold: 500,
  },
  ua = (e) => {
    if (!e) return 0;
    const t = e.id.split("-");
    return Number(t[t.length - 2]);
  },
  ca = v({
    name: "ElCascaderPanel",
    components: { ElCascaderMenu: la },
    props: {
      ...ra,
      border: { type: Boolean, default: !0 },
      renderLabel: Function,
    },
    emits: [ul, dl, "close", "expand-change"],
    setup(l, { emit: a, slots: n }) {
      let o = !1;
      const s = g("cascader"),
        r = ((e) => y(() => ({ ...ia, ...e.props })))(l);
      let i = null;
      const u = b(!0),
        c = b([]),
        d = b(null),
        p = b([]),
        h = b(null),
        v = b([]),
        f = y(() => "hover" === r.value.expandTrigger),
        m = y(() => l.renderLabel || n.default),
        k = (e, t) => {
          const l = r.value;
          (e = e || new na({}, l, void 0, !0)).loading = !0;
          l.lazyLoad(e, (l) => {
            const a = e,
              n = a.root ? null : a;
            (l && (null == i || i.appendNodes(l, n)),
              (a.loading = !1),
              (a.loaded = !0),
              (a.childrenData = a.childrenData || []),
              t && t(l));
          });
        },
        x = (e, t) => {
          var l;
          const { level: n } = e,
            o = p.value.slice(0, n);
          let s;
          (e.isLeaf ? (s = e.pathNodes[n - 2]) : ((s = e), o.push(e.children)),
            (null == (l = h.value) ? void 0 : l.uid) !==
              (null == s ? void 0 : s.uid) &&
              ((h.value = e),
              (p.value = o),
              !t &&
                a("expand-change", (null == e ? void 0 : e.pathValues) || [])));
        },
        S = (e, t, l = !0) => {
          const { checkStrictly: n, multiple: s } = r.value,
            i = v.value[0];
          ((o = !0),
            !s && (null == i || i.doCheck(!1)),
            e.doCheck(t),
            T(),
            l && !s && !n && a("close"),
            !l && !s && !n && C(e));
        },
        C = (e) => {
          e && ((e = e.parent), C(e), e && x(e));
        },
        V = (e) => (null == i ? void 0 : i.getFlattedNodes(e)),
        N = (e) => {
          var t;
          return null == (t = V(e))
            ? void 0
            : t.filter((e) => !1 !== e.checked);
        },
        T = () => {
          var e;
          const { checkStrictly: t, multiple: l } = r.value,
            a = ((e, t) => {
              const l = t.slice(0),
                a = l.map((e) => e.uid),
                n = e.reduce((e, t) => {
                  const n = a.indexOf(t.uid);
                  return (
                    n > -1 && (e.push(t), l.splice(n, 1), a.splice(n, 1)),
                    e
                  );
                }, []);
              return (n.push(...l), n);
            })(v.value, N(!t)),
            n = a.map((e) => e.valueByOption);
          ((v.value = a), (d.value = l ? n : null != (e = n[0]) ? e : null));
        },
        E = (e = !1, a = !1) => {
          const { modelValue: n } = l,
            { lazy: s, multiple: c, checkStrictly: p } = r.value,
            h = !p;
          var v;
          if (u.value && !o && (a || !gl(n, d.value)))
            if (s && !e) {
              const e = qt(null != (v = Yt(n)) && v.length ? t(v, 1 / 0) : [])
                .map((e) => (null == i ? void 0 : i.getNodeByValue(e)))
                .filter((e) => !!e && !e.loaded && !e.loading);
              e.length
                ? e.forEach((e) => {
                    k(e, () => E(!1, a));
                  })
                : E(!0, a);
            } else {
              const e = c ? Yt(n) : [n],
                t = qt(
                  e.map((e) => (null == i ? void 0 : i.getNodeByValue(e, h))),
                );
              (M(t, a), (d.value = ce(n)));
            }
        },
        M = (e, t = !0) => {
          const { checkStrictly: a } = r.value,
            n = v.value,
            o = e.filter((e) => !!e && (a || e.isLeaf)),
            s = null == i ? void 0 : i.getSameNode(h.value),
            u = (t && s) || o[0];
          (u ? u.pathNodes.forEach((e) => x(e, !0)) : (h.value = null),
            n.forEach((e) => e.doCheck(!1)),
            l.props.multiple
              ? re(o).forEach((e) => e.doCheck(!0))
              : o.forEach((e) => e.doCheck(!0)),
            (v.value = o),
            H(I));
        },
        I = () => {
          e &&
            c.value.forEach((e) => {
              const t = null == e ? void 0 : e.$el;
              if (t) {
                const e = t.querySelector(
                    `.${s.namespace.value}-scrollbar__wrap`,
                  ),
                  l =
                    t.querySelector(`.${s.b("node")}.${s.is("active")}`) ||
                    t.querySelector(`.${s.b("node")}.in-active-path`);
                bl(e, l);
              }
            });
        };
      return (
        Q(
          Zl,
          re({
            config: r,
            expandingNode: h,
            checkedNodes: v,
            isHoverMenu: f,
            initialLoaded: u,
            renderLabelFn: m,
            lazyLoad: k,
            expandNode: x,
            handleCheckChange: S,
          }),
        ),
        ie(
          [r, () => l.options],
          () => {
            const { options: e } = l,
              t = r.value;
            ((o = !1),
              (i = new sa(e, t)),
              (p.value = [i.getNodes()]),
              t.lazy && ne(l.options)
                ? ((u.value = !1),
                  k(void 0, (e) => {
                    (e && ((i = new sa(e, t)), (p.value = [i.getNodes()])),
                      (u.value = !0),
                      E(!1, !0));
                  }))
                : E(!1, !0));
          },
          { deep: !0, immediate: !0 },
        ),
        ie(
          () => l.modelValue,
          () => {
            ((o = !1), E());
          },
          { deep: !0 },
        ),
        ie(
          () => d.value,
          (e) => {
            gl(e, l.modelValue) || (a(ul, e), a(dl, e));
          },
        ),
        ue(() => (c.value = [])),
        w(() => !ne(l.modelValue) && E()),
        {
          ns: s,
          menuList: c,
          menus: p,
          checkedNodes: v,
          handleKeyDown: (e) => {
            const t = e.target,
              { code: l } = e;
            switch (l) {
              case Z.up:
              case Z.down: {
                e.preventDefault();
                const a = l === Z.up ? -1 : 1;
                El(Tl(t, a, `.${s.b("node")}[tabindex="-1"]`));
                break;
              }
              case Z.left: {
                e.preventDefault();
                const l = c.value[ua(t) - 1],
                  a =
                    null == l
                      ? void 0
                      : l.$el.querySelector(
                          `.${s.b("node")}[aria-expanded="true"]`,
                        );
                El(a);
                break;
              }
              case Z.right: {
                e.preventDefault();
                const l = c.value[ua(t) + 1],
                  a =
                    null == l
                      ? void 0
                      : l.$el.querySelector(`.${s.b("node")}[tabindex="-1"]`);
                El(a);
                break;
              }
              case Z.enter:
                ((e) => {
                  if (!e) return;
                  const t = e.querySelector("input");
                  t ? t.click() : Nl(e) && e.click();
                })(t);
            }
          },
          handleCheckChange: S,
          getFlattedNodes: V,
          getCheckedNodes: N,
          clearCheckedNodes: () => {
            (v.value.forEach((e) => e.doCheck(!1)),
              T(),
              (p.value = p.value.slice(0, 1)),
              (h.value = null),
              a("expand-change", []));
          },
          calculateCheckedValue: T,
          scrollToExpandingNode: I,
        }
      );
    },
  });
var da = K(ca, [
  [
    "render",
    function (e, t, l, a, n, o) {
      const s = le("el-cascader-menu");
      return (
        x(),
        O(
          "div",
          {
            class: N([e.ns.b("panel"), e.ns.is("bordered", e.border)]),
            onKeydown:
              t[0] ||
              (t[0] = (...t) => e.handleKeyDown && e.handleKeyDown(...t)),
          },
          [
            (x(!0),
            O(
              P,
              null,
              L(
                e.menus,
                (t, l) => (
                  x(),
                  S(
                    s,
                    {
                      key: l,
                      ref_for: !0,
                      ref: (t) => (e.menuList[l] = t),
                      index: l,
                      nodes: [...t],
                    },
                    null,
                    8,
                    ["index", "nodes"],
                  )
                ),
              ),
              128,
            )),
          ],
          34,
        )
      );
    },
  ],
  [
    "__file",
    "/home/runner/work/element-plus/element-plus/packages/components/cascader-panel/src/index.vue",
  ],
]);
da.install = (e) => {
  e.component(da.name, da);
};
const pa = da,
  ha = u({
    ...ra,
    size: de,
    placeholder: String,
    disabled: Boolean,
    clearable: Boolean,
    filterable: Boolean,
    filterMethod: { type: c(Function), default: (e, t) => e.text.includes(t) },
    separator: { type: String, default: " / " },
    showAllLevels: { type: Boolean, default: !0 },
    collapseTags: Boolean,
    collapseTagsTooltip: { type: Boolean, default: !1 },
    debounce: { type: Number, default: 300 },
    beforeFilter: { type: c(Function), default: () => !0 },
    popperClass: { type: String, default: "" },
    teleported: Vt.teleported,
    tagType: { ...yl.type, default: "info" },
    validateEvent: { type: Boolean, default: !0 },
  }),
  va = {
    [ul]: (e) => !!e || null === e,
    [dl]: (e) => !!e || null === e,
    focus: (e) => e instanceof FocusEvent,
    blur: (e) => e instanceof FocusEvent,
    visibleChange: (e) => pe(e),
    expandChange: (e) => !!e,
    removeTag: (e) => !!e,
  },
  fa = { key: 0 },
  ma = ["placeholder", "onKeydown"],
  ga = ["onClick"],
  ba = v({ name: "ElCascader" }),
  ya = v({
    ...ba,
    props: ha,
    emits: va,
    setup(t, { expose: l, emit: a }) {
      const n = t,
        o = {
          modifiers: [
            {
              name: "arrowPosition",
              enabled: !0,
              phase: "main",
              fn: ({ state: e }) => {
                const { modifiersData: t, placement: l } = e;
                ["right", "left", "bottom", "top"].includes(l) ||
                  (t.arrow.x = 35);
              },
              requires: ["arrow"],
            },
          ],
        },
        s = f();
      let r = 0,
        i = 0;
      const u = g("cascader"),
        c = g("input"),
        { t: d } = Y(),
        { form: p, formItem: h } = he(),
        v = b(null),
        m = b(null),
        k = b(null),
        _ = b(null),
        B = b(null),
        j = b(!1),
        F = b(!1),
        K = b(!1),
        W = b(!1),
        U = b(""),
        q = b(""),
        G = b([]),
        Q = b([]),
        J = b([]),
        te = b(!1),
        le = y(() => s.style),
        ae = y(() => n.disabled || (null == p ? void 0 : p.disabled)),
        ne = y(() => n.placeholder || d("el.cascader.placeholder")),
        oe = y(() =>
          q.value || G.value.length > 0 || te.value ? "" : ne.value,
        ),
        se = ve(),
        re = y(() => (["small"].includes(se.value) ? "small" : "default")),
        ue = y(() => !!n.props.multiple),
        de = y(() => !n.filterable || ue.value),
        pe = y(() => (ue.value ? q.value : U.value)),
        Ve = y(() => {
          var e;
          return (null == (e = _.value) ? void 0 : e.checkedNodes) || [];
        }),
        Ne = y(
          () =>
            !(!n.clearable || ae.value || K.value || !F.value) &&
            !!Ve.value.length,
        ),
        Te = y(() => {
          const { showAllLevels: e, separator: t } = n,
            l = Ve.value;
          return l.length ? (ue.value ? "" : l[0].calcText(e, t)) : "";
        }),
        Ee = y({
          get: () => ce(n.modelValue),
          set(e) {
            (a(ul, e),
              a(dl, e),
              n.validateEvent &&
                (null == h || h.validate("change").catch((e) => fe())));
          },
        }),
        Me = y(() => [
          u.b(),
          u.m(se.value),
          u.is("disabled", ae.value),
          s.class,
        ]),
        Ie = y(() => [
          c.e("icon"),
          "icon-arrow-down",
          u.is("reverse", j.value),
        ]),
        Oe = y(() => u.is("focus", j.value || W.value)),
        Ae = y(() => {
          var e, t;
          return null == (t = null == (e = v.value) ? void 0 : e.popperRef)
            ? void 0
            : t.contentRef;
        }),
        _e = (e) => {
          var t, l, o;
          ae.value ||
            ((e = null != e ? e : !j.value) !== j.value &&
              ((j.value = e),
              null == (l = null == (t = m.value) ? void 0 : t.input) ||
                l.setAttribute("aria-expanded", `${e}`),
              e
                ? (Pe(),
                  H(null == (o = _.value) ? void 0 : o.scrollToExpandingNode))
                : n.filterable && We(),
              a("visibleChange", e)));
        },
        Pe = () => {
          H(() => {
            var e;
            null == (e = v.value) || e.updatePopper();
          });
        },
        Le = () => {
          K.value = !1;
        },
        $e = (e) => {
          const { showAllLevels: t, separator: l } = n;
          return {
            node: e,
            key: e.uid,
            text: e.calcText(t, l),
            hitState: !1,
            closable: !ae.value && !e.isDisabled,
            isCollapseTag: !1,
          };
        },
        Be = (e) => {
          var t;
          const l = e.node;
          (l.doCheck(!1),
            null == (t = _.value) || t.calculateCheckedValue(),
            a("removeTag", l.valueByOption));
        },
        De = () => {
          var e, t;
          const { filterMethod: l, showAllLevels: a, separator: o } = n,
            s =
              null ==
              (t =
                null == (e = _.value)
                  ? void 0
                  : e.getFlattedNodes(!n.props.checkStrictly))
                ? void 0
                : t.filter(
                    (e) => !e.isDisabled && (e.calcText(a, o), l(e, pe.value)),
                  );
          (ue.value &&
            (G.value.forEach((e) => {
              e.hitState = !1;
            }),
            Q.value.forEach((e) => {
              e.hitState = !1;
            })),
            (K.value = !0),
            (J.value = s),
            Pe());
        },
        je = () => {
          var e;
          let t;
          ((t =
            K.value && B.value
              ? B.value.$el.querySelector(`.${u.e("suggestion-item")}`)
              : null == (e = _.value)
                ? void 0
                : e.$el.querySelector(`.${u.b("node")}[tabindex="-1"]`)),
            t && (t.focus(), !K.value && t.click()));
        },
        Re = () => {
          var t, l;
          const a = null == (t = m.value) ? void 0 : t.input,
            n = k.value,
            o = null == (l = B.value) ? void 0 : l.$el;
          if (e && a) {
            if (o) {
              o.querySelector(`.${u.e("suggestion-list")}`).style.minWidth =
                `${a.offsetWidth}px`;
            }
            if (n) {
              const { offsetHeight: e } = n,
                t = G.value.length > 0 ? `${Math.max(e + 6, r)}px` : `${r}px`;
              ((a.style.height = t), Pe());
            }
          }
        },
        ze = (e) => {
          (Pe(), a("expandChange", e));
        },
        Fe = (e) => {
          var t;
          const l = null == (t = e.target) ? void 0 : t.value;
          if ("compositionend" === e.type) ((te.value = !1), H(() => Ze(l)));
          else {
            const e = l[l.length - 1] || "";
            te.value = !It(e);
          }
        },
        Ke = (e) => {
          if (!te.value)
            switch (e.code) {
              case Z.enter:
                _e();
                break;
              case Z.down:
                (_e(!0), H(je), e.preventDefault());
                break;
              case Z.esc:
                !0 === j.value &&
                  (e.preventDefault(), e.stopPropagation(), _e(!1));
                break;
              case Z.tab:
                _e(!1);
            }
        },
        He = () => {
          var e;
          (null == (e = _.value) || e.clearCheckedNodes(),
            !j.value && n.filterable && We(),
            _e(!1));
        },
        We = () => {
          const { value: e } = Te;
          ((U.value = e), (q.value = e));
        },
        Ue = (e) => {
          const t = e.target,
            { code: l } = e;
          switch (l) {
            case Z.up:
            case Z.down: {
              const e = l === Z.up ? -1 : 1;
              El(Tl(t, e, `.${u.e("suggestion-item")}[tabindex="-1"]`));
              break;
            }
            case Z.enter:
              t.click();
          }
        },
        qe = () => {
          const e = G.value,
            t = e[e.length - 1];
          ((i = q.value ? 0 : i + 1),
            !t ||
              !i ||
              (n.collapseTags && e.length > 1) ||
              (t.hitState ? Be(t) : (t.hitState = !0)));
        },
        Ye = (e) => {
          const t = e.target,
            l = u.e("search-input");
          (t.className === l && (W.value = !0), a("focus", e));
        },
        Ge = (e) => {
          ((W.value = !1), a("blur", e));
        },
        Xe = pl(() => {
          const { value: e } = pe;
          if (!e) return;
          const t = n.beforeFilter(e);
          me(t) ? t.then(De).catch(() => {}) : !1 !== t ? De() : Le();
        }, n.debounce),
        Ze = (e, t) => {
          (!j.value && _e(!0),
            (null == t ? void 0 : t.isComposing) || (e ? Xe() : Le()));
        },
        Qe = (e) =>
          Number.parseFloat(Ce(c.cssVarName("input-height"), e).value) - 2;
      return (
        ie(K, Pe),
        ie([Ve, ae], () => {
          if (!ue.value) return;
          const e = Ve.value,
            t = [],
            l = [];
          if ((e.forEach((e) => l.push($e(e))), (Q.value = l), e.length)) {
            const [l, ...a] = e,
              o = a.length;
            (t.push($e(l)),
              o &&
                (n.collapseTags
                  ? t.push({
                      key: -1,
                      text: `+ ${o}`,
                      closable: !1,
                      isCollapseTag: !0,
                    })
                  : a.forEach((e) => t.push($e(e)))));
          }
          G.value = t;
        }),
        ie(G, () => {
          H(() => Re());
        }),
        ie(se, async () => {
          await H();
          const e = m.value.input;
          ((r = Qe(e) || r), Re());
        }),
        ie(Te, We, { immediate: !0 }),
        w(() => {
          const e = m.value.input,
            t = Qe(e);
          ((r = e.offsetHeight || t), ge(e, Re));
        }),
        l({
          getCheckedNodes: (e) => {
            var t;
            return null == (t = _.value) ? void 0 : t.getCheckedNodes(e);
          },
          cascaderPanelRef: _,
          togglePopperVisible: _e,
          contentRef: Ae,
        }),
        (e, t) => (
          x(),
          S(
            T(Nt),
            {
              ref_key: "tooltipRef",
              ref: v,
              visible: j.value,
              teleported: e.teleported,
              "popper-class": [T(u).e("dropdown"), e.popperClass],
              "popper-options": o,
              "fallback-placements": [
                "bottom-start",
                "bottom",
                "top-start",
                "top",
                "right",
                "left",
              ],
              "stop-popper-mouse-event": !1,
              "gpu-acceleration": !1,
              placement: "bottom-start",
              transition: `${T(u).namespace.value}-zoom-in-top`,
              effect: "light",
              pure: "",
              persistent: "",
              onHide: Le,
            },
            {
              default: C(() => [
                be(
                  (x(),
                  O(
                    "div",
                    {
                      class: N(T(Me)),
                      style: E(T(le)),
                      onClick: t[5] || (t[5] = () => _e(!T(de) || void 0)),
                      onKeydown: Ke,
                      onMouseenter: t[6] || (t[6] = (e) => (F.value = !0)),
                      onMouseleave: t[7] || (t[7] = (e) => (F.value = !1)),
                    },
                    [
                      M(
                        T(Mt),
                        {
                          ref_key: "input",
                          ref: m,
                          modelValue: U.value,
                          "onUpdate:modelValue":
                            t[1] || (t[1] = (e) => (U.value = e)),
                          placeholder: T(oe),
                          readonly: T(de),
                          disabled: T(ae),
                          "validate-event": !1,
                          size: T(se),
                          class: N(T(Oe)),
                          tabindex:
                            T(ue) && e.filterable && !T(ae) ? -1 : void 0,
                          onCompositionstart: Fe,
                          onCompositionupdate: Fe,
                          onCompositionend: Fe,
                          onFocus: Ye,
                          onBlur: Ge,
                          onInput: Ze,
                        },
                        {
                          suffix: C(() => [
                            T(Ne)
                              ? (x(),
                                S(
                                  T(A),
                                  {
                                    key: "clear",
                                    class: N([
                                      T(c).e("icon"),
                                      "icon-circle-close",
                                    ]),
                                    onClick: z(He, ["stop"]),
                                  },
                                  { default: C(() => [M(T(ye))]), _: 1 },
                                  8,
                                  ["class", "onClick"],
                                ))
                              : (x(),
                                S(
                                  T(A),
                                  {
                                    key: "arrow-down",
                                    class: N(T(Ie)),
                                    onClick:
                                      t[0] || (t[0] = z((e) => _e(), ["stop"])),
                                  },
                                  { default: C(() => [M(T(ke))]), _: 1 },
                                  8,
                                  ["class"],
                                )),
                          ]),
                          _: 1,
                        },
                        8,
                        [
                          "modelValue",
                          "placeholder",
                          "readonly",
                          "disabled",
                          "size",
                          "class",
                          "tabindex",
                        ],
                      ),
                      T(ue)
                        ? (x(),
                          O(
                            "div",
                            {
                              key: 0,
                              ref_key: "tagWrapper",
                              ref: k,
                              class: N(T(u).e("tags")),
                            },
                            [
                              (x(!0),
                              O(
                                P,
                                null,
                                L(
                                  G.value,
                                  (t) => (
                                    x(),
                                    S(
                                      T(kl),
                                      {
                                        key: t.key,
                                        type: e.tagType,
                                        size: T(re),
                                        hit: t.hitState,
                                        closable: t.closable,
                                        "disable-transitions": "",
                                        onClose: (e) => Be(t),
                                      },
                                      {
                                        default: C(() => [
                                          !1 === t.isCollapseTag
                                            ? (x(), O("span", fa, D(t.text), 1))
                                            : (x(),
                                              S(
                                                T(Nt),
                                                {
                                                  key: 1,
                                                  disabled:
                                                    j.value ||
                                                    !e.collapseTagsTooltip,
                                                  "fallback-placements": [
                                                    "bottom",
                                                    "top",
                                                    "right",
                                                    "left",
                                                  ],
                                                  placement: "bottom",
                                                  effect: "light",
                                                },
                                                {
                                                  default: C(() => [
                                                    V(
                                                      "span",
                                                      null,
                                                      D(t.text),
                                                      1,
                                                    ),
                                                  ]),
                                                  content: C(() => [
                                                    V(
                                                      "div",
                                                      {
                                                        class: N(
                                                          T(u).e(
                                                            "collapse-tags",
                                                          ),
                                                        ),
                                                      },
                                                      [
                                                        (x(!0),
                                                        O(
                                                          P,
                                                          null,
                                                          L(
                                                            Q.value.slice(1),
                                                            (t, l) => (
                                                              x(),
                                                              O(
                                                                "div",
                                                                {
                                                                  key: l,
                                                                  class: N(
                                                                    T(u).e(
                                                                      "collapse-tag",
                                                                    ),
                                                                  ),
                                                                },
                                                                [
                                                                  (x(),
                                                                  S(
                                                                    T(kl),
                                                                    {
                                                                      key: t.key,
                                                                      class:
                                                                        "in-tooltip",
                                                                      type: e.tagType,
                                                                      size: T(
                                                                        re,
                                                                      ),
                                                                      hit: t.hitState,
                                                                      closable:
                                                                        t.closable,
                                                                      "disable-transitions":
                                                                        "",
                                                                      onClose: (
                                                                        e,
                                                                      ) =>
                                                                        Be(t),
                                                                    },
                                                                    {
                                                                      default:
                                                                        C(
                                                                          () => [
                                                                            V(
                                                                              "span",
                                                                              null,
                                                                              D(
                                                                                t.text,
                                                                              ),
                                                                              1,
                                                                            ),
                                                                          ],
                                                                        ),
                                                                      _: 2,
                                                                    },
                                                                    1032,
                                                                    [
                                                                      "type",
                                                                      "size",
                                                                      "hit",
                                                                      "closable",
                                                                      "onClose",
                                                                    ],
                                                                  )),
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
                                                  ]),
                                                  _: 2,
                                                },
                                                1032,
                                                ["disabled"],
                                              )),
                                        ]),
                                        _: 2,
                                      },
                                      1032,
                                      [
                                        "type",
                                        "size",
                                        "hit",
                                        "closable",
                                        "onClose",
                                      ],
                                    )
                                  ),
                                ),
                                128,
                              )),
                              e.filterable && !T(ae)
                                ? be(
                                    (x(),
                                    O(
                                      "input",
                                      {
                                        key: 0,
                                        "onUpdate:modelValue":
                                          t[2] || (t[2] = (e) => (q.value = e)),
                                        type: "text",
                                        class: N(T(u).e("search-input")),
                                        placeholder: T(Te) ? "" : T(ne),
                                        onInput:
                                          t[3] ||
                                          (t[3] = (e) => Ze(q.value, e)),
                                        onClick:
                                          t[4] ||
                                          (t[4] = z((e) => _e(!0), ["stop"])),
                                        onKeydown: R(qe, ["delete"]),
                                        onCompositionstart: Fe,
                                        onCompositionupdate: Fe,
                                        onCompositionend: Fe,
                                        onFocus: Ye,
                                        onBlur: Ge,
                                      },
                                      null,
                                      42,
                                      ma,
                                    )),
                                    [[we, q.value]],
                                  )
                                : X("v-if", !0),
                            ],
                            2,
                          ))
                        : X("v-if", !0),
                    ],
                    38,
                  )),
                  [[T(wl), () => _e(!1), T(Ae)]],
                ),
              ]),
              content: C(() => [
                be(
                  M(
                    T(pa),
                    {
                      ref_key: "cascaderPanelRef",
                      ref: _,
                      modelValue: T(Ee),
                      "onUpdate:modelValue":
                        t[8] ||
                        (t[8] = (e) => (xe(Ee) ? (Ee.value = e) : null)),
                      options: e.options,
                      props: n.props,
                      border: !1,
                      "render-label": e.$slots.default,
                      onExpandChange: ze,
                      onClose:
                        t[9] || (t[9] = (t) => e.$nextTick(() => _e(!1))),
                    },
                    null,
                    8,
                    ["modelValue", "options", "props", "render-label"],
                  ),
                  [[Se, !K.value]],
                ),
                e.filterable
                  ? be(
                      (x(),
                      S(
                        T(I),
                        {
                          key: 0,
                          ref_key: "suggestionPanel",
                          ref: B,
                          tag: "ul",
                          class: N(T(u).e("suggestion-panel")),
                          "view-class": T(u).e("suggestion-list"),
                          onKeydown: Ue,
                        },
                        {
                          default: C(() => [
                            J.value.length
                              ? (x(!0),
                                O(
                                  P,
                                  { key: 0 },
                                  L(
                                    J.value,
                                    (e) => (
                                      x(),
                                      O(
                                        "li",
                                        {
                                          key: e.uid,
                                          class: N([
                                            T(u).e("suggestion-item"),
                                            T(u).is("checked", e.checked),
                                          ]),
                                          tabindex: -1,
                                          onClick: (t) =>
                                            ((e) => {
                                              var t, l;
                                              const { checked: a } = e;
                                              ue.value
                                                ? null == (t = _.value) ||
                                                  t.handleCheckChange(e, !a, !1)
                                                : (!a &&
                                                    (null == (l = _.value) ||
                                                      l.handleCheckChange(
                                                        e,
                                                        !0,
                                                        !1,
                                                      )),
                                                  _e(!1));
                                            })(e),
                                        },
                                        [
                                          V("span", null, D(e.text), 1),
                                          e.checked
                                            ? (x(),
                                              S(
                                                T(A),
                                                { key: 0 },
                                                {
                                                  default: C(() => [M(T(ee))]),
                                                  _: 1,
                                                },
                                              ))
                                            : X("v-if", !0),
                                        ],
                                        10,
                                        ga,
                                      )
                                    ),
                                  ),
                                  128,
                                ))
                              : $(e.$slots, "empty", { key: 1 }, () => [
                                  V(
                                    "li",
                                    { class: N(T(u).e("empty-text")) },
                                    D(T(d)("el.cascader.noMatch")),
                                    3,
                                  ),
                                ]),
                          ]),
                          _: 3,
                        },
                        8,
                        ["class", "view-class"],
                      )),
                      [[Se, K.value]],
                    )
                  : X("v-if", !0),
              ]),
              _: 3,
            },
            8,
            ["visible", "teleported", "popper-class", "transition"],
          )
        )
      );
    },
  });
var ka = K(ya, [
  [
    "__file",
    "/home/runner/work/element-plus/element-plus/packages/components/cascader/src/cascader.vue",
  ],
]);
ka.install = (e) => {
  e.component(ka.name, ka);
};
const wa = ka,
  xa = u({
    color: { type: c(Object), required: !0 },
    vertical: { type: Boolean, default: !1 },
  });
let Sa = !1;
function Ca(t, l) {
  if (!e) return;
  const a = function (e) {
      var t;
      null == (t = l.drag) || t.call(l, e);
    },
    n = function (e) {
      var t;
      (document.removeEventListener("mousemove", a),
        document.removeEventListener("mouseup", n),
        document.removeEventListener("touchmove", a),
        document.removeEventListener("touchend", n),
        (document.onselectstart = null),
        (document.ondragstart = null),
        (Sa = !1),
        null == (t = l.end) || t.call(l, e));
    },
    o = function (e) {
      var t;
      Sa ||
        (e.preventDefault(),
        (document.onselectstart = () => !1),
        (document.ondragstart = () => !1),
        document.addEventListener("mousemove", a),
        document.addEventListener("mouseup", n),
        document.addEventListener("touchmove", a),
        document.addEventListener("touchend", n),
        (Sa = !0),
        null == (t = l.start) || t.call(l, e));
    };
  (t.addEventListener("mousedown", o), t.addEventListener("touchstart", o));
}
const Va = (e, { bar: t, thumb: l, handleDrag: a }) => {
    const n = ae(),
      o = g("color-alpha-slider"),
      s = b(0),
      r = b(0),
      i = b();
    function u() {
      ((s.value = (function () {
        if (!l.value) return 0;
        if (e.vertical) return 0;
        const t = n.vnode.el,
          a = e.color.get("alpha");
        return t
          ? Math.round((a * (t.offsetWidth - l.value.offsetWidth / 2)) / 100)
          : 0;
      })()),
        (r.value = (function () {
          if (!l.value) return 0;
          const t = n.vnode.el;
          if (!e.vertical) return 0;
          const a = e.color.get("alpha");
          return t
            ? Math.round(
                (a * (t.offsetHeight - l.value.offsetHeight / 2)) / 100,
              )
            : 0;
        })()),
        (i.value = (function () {
          if (e.color && e.color.value) {
            const { r: t, g: l, b: a } = e.color.toRgb();
            return `linear-gradient(to right, rgba(${t}, ${l}, ${a}, 0) 0%, rgba(${t}, ${l}, ${a}, 1) 100%)`;
          }
          return "";
        })()));
    }
    (w(() => {
      if (!t.value || !l.value) return;
      const e = {
        drag: (e) => {
          a(e);
        },
        end: (e) => {
          a(e);
        },
      };
      (Ca(t.value, e), Ca(l.value, e), u());
    }),
      ie(
        () => e.color.get("alpha"),
        () => u(),
      ),
      ie(
        () => e.color.value,
        () => u(),
      ));
    const c = y(() => [o.b(), o.is("vertical", e.vertical)]),
      d = y(() => o.e("bar")),
      p = y(() => o.e("thumb"));
    return {
      rootKls: c,
      barKls: d,
      barStyle: y(() => ({ background: i.value })),
      thumbKls: p,
      thumbStyle: y(() => ({ left: Ne(s.value), top: Ne(r.value) })),
      update: u,
    };
  },
  Na = v({ name: "ElColorAlphaSlider" });
var Ta = K(
  v({
    ...Na,
    props: xa,
    setup(e, { expose: t }) {
      const l = e,
        {
          bar: a,
          thumb: n,
          handleDrag: o,
          handleClick: s,
        } = ((e) => {
          const t = ae(),
            l = Ve(),
            a = Ve();
          function n(n) {
            if (!a.value || !l.value) return;
            const o = t.vnode.el.getBoundingClientRect(),
              { clientX: s, clientY: r } = Il(n);
            if (e.vertical) {
              let t = r - o.top;
              ((t = Math.max(l.value.offsetHeight / 2, t)),
                (t = Math.min(t, o.height - l.value.offsetHeight / 2)),
                e.color.set(
                  "alpha",
                  Math.round(
                    ((t - l.value.offsetHeight / 2) /
                      (o.height - l.value.offsetHeight)) *
                      100,
                  ),
                ));
            } else {
              let t = s - o.left;
              ((t = Math.max(l.value.offsetWidth / 2, t)),
                (t = Math.min(t, o.width - l.value.offsetWidth / 2)),
                e.color.set(
                  "alpha",
                  Math.round(
                    ((t - l.value.offsetWidth / 2) /
                      (o.width - l.value.offsetWidth)) *
                      100,
                  ),
                ));
            }
          }
          return {
            thumb: l,
            bar: a,
            handleDrag: n,
            handleClick: function (e) {
              e.target !== l.value && n(e);
            },
          };
        })(l),
        {
          rootKls: r,
          barKls: i,
          barStyle: u,
          thumbKls: c,
          thumbStyle: d,
          update: p,
        } = Va(l, { bar: a, thumb: n, handleDrag: o });
      return (
        t({ update: p, bar: a, thumb: n }),
        (e, t) => (
          x(),
          O(
            "div",
            { class: N(T(r)) },
            [
              V(
                "div",
                {
                  ref_key: "bar",
                  ref: a,
                  class: N(T(i)),
                  style: E(T(u)),
                  onClick: t[0] || (t[0] = (...e) => T(s) && T(s)(...e)),
                },
                null,
                6,
              ),
              V(
                "div",
                { ref_key: "thumb", ref: n, class: N(T(c)), style: E(T(d)) },
                null,
                6,
              ),
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
      "/home/runner/work/element-plus/element-plus/packages/components/color-picker/src/components/alpha-slider.vue",
    ],
  ],
);
var Ea = K(
  v({
    name: "ElColorHueSlider",
    props: { color: { type: Object, required: !0 }, vertical: Boolean },
    setup(e) {
      const t = g("color-hue-slider"),
        l = ae(),
        a = b(),
        n = b(),
        o = b(0),
        s = b(0),
        r = y(() => e.color.get("hue"));
      function i(t) {
        if (!n.value || !a.value) return;
        const o = l.vnode.el.getBoundingClientRect(),
          { clientX: s, clientY: r } = Il(t);
        let i;
        if (e.vertical) {
          let e = r - o.top;
          ((e = Math.min(e, o.height - a.value.offsetHeight / 2)),
            (e = Math.max(a.value.offsetHeight / 2, e)),
            (i = Math.round(
              ((e - a.value.offsetHeight / 2) /
                (o.height - a.value.offsetHeight)) *
                360,
            )));
        } else {
          let e = s - o.left;
          ((e = Math.min(e, o.width - a.value.offsetWidth / 2)),
            (e = Math.max(a.value.offsetWidth / 2, e)),
            (i = Math.round(
              ((e - a.value.offsetWidth / 2) /
                (o.width - a.value.offsetWidth)) *
                360,
            )));
        }
        e.color.set("hue", i);
      }
      function u() {
        ((o.value = (function () {
          if (!a.value) return 0;
          const t = l.vnode.el;
          if (e.vertical) return 0;
          const n = e.color.get("hue");
          return t
            ? Math.round((n * (t.offsetWidth - a.value.offsetWidth / 2)) / 360)
            : 0;
        })()),
          (s.value = (function () {
            if (!a.value) return 0;
            const t = l.vnode.el;
            if (!e.vertical) return 0;
            const n = e.color.get("hue");
            return t
              ? Math.round(
                  (n * (t.offsetHeight - a.value.offsetHeight / 2)) / 360,
                )
              : 0;
          })()));
      }
      return (
        ie(
          () => r.value,
          () => {
            u();
          },
        ),
        w(() => {
          if (!n.value || !a.value) return;
          const e = {
            drag: (e) => {
              i(e);
            },
            end: (e) => {
              i(e);
            },
          };
          (Ca(n.value, e), Ca(a.value, e), u());
        }),
        {
          bar: n,
          thumb: a,
          thumbLeft: o,
          thumbTop: s,
          hueValue: r,
          handleClick: function (e) {
            e.target !== a.value && i(e);
          },
          update: u,
          ns: t,
        }
      );
    },
  }),
  [
    [
      "render",
      function (e, t, l, a, n, o) {
        return (
          x(),
          O(
            "div",
            { class: N([e.ns.b(), e.ns.is("vertical", e.vertical)]) },
            [
              V(
                "div",
                {
                  ref: "bar",
                  class: N(e.ns.e("bar")),
                  onClick:
                    t[0] ||
                    (t[0] = (...t) => e.handleClick && e.handleClick(...t)),
                },
                null,
                2,
              ),
              V(
                "div",
                {
                  ref: "thumb",
                  class: N(e.ns.e("thumb")),
                  style: E({
                    left: e.thumbLeft + "px",
                    top: e.thumbTop + "px",
                  }),
                },
                null,
                6,
              ),
            ],
            2,
          )
        );
      },
    ],
    [
      "__file",
      "/home/runner/work/element-plus/element-plus/packages/components/color-picker/src/components/hue-slider.vue",
    ],
  ],
);
const Ma = u({
    modelValue: String,
    id: String,
    showAlpha: Boolean,
    colorFormat: String,
    disabled: Boolean,
    size: de,
    popperClass: { type: String, default: "" },
    label: { type: String, default: void 0 },
    tabindex: { type: [String, Number], default: 0 },
    predefine: { type: c(Array) },
    validateEvent: { type: Boolean, default: !0 },
  }),
  Ia = {
    [ul]: (e) => p(e) || hl(e),
    [dl]: (e) => p(e) || hl(e),
    activeChange: (e) => p(e) || hl(e),
  },
  Oa = Symbol("colorPickerContextKey"),
  Aa = function (e, t, l) {
    return [e, (t * l) / ((e = (2 - t) * l) < 1 ? e : 2 - e) || 0, e / 2];
  },
  _a = function (e, t) {
    var l;
    "string" == typeof (l = e) &&
      l.includes(".") &&
      1 === Number.parseFloat(l) &&
      (e = "100%");
    const a = (function (e) {
      return "string" == typeof e && e.includes("%");
    })(e);
    return (
      (e = Math.min(t, Math.max(0, Number.parseFloat(`${e}`)))),
      a && (e = Number.parseInt("" + e * t, 10) / 100),
      Math.abs(e - t) < 1e-6 ? 1 : (e % t) / Number.parseFloat(t)
    );
  },
  Pa = { 10: "A", 11: "B", 12: "C", 13: "D", 14: "E", 15: "F" },
  La = (e) => {
    e = Math.min(Math.round(e), 255);
    const t = Math.floor(e / 16),
      l = e % 16;
    return `${Pa[t] || t}${Pa[l] || l}`;
  },
  $a = function ({ r: e, g: t, b: l }) {
    return Number.isNaN(+e) || Number.isNaN(+t) || Number.isNaN(+l)
      ? ""
      : `#${La(e)}${La(t)}${La(l)}`;
  },
  Ba = { A: 10, B: 11, C: 12, D: 13, E: 14, F: 15 },
  Da = function (e) {
    return 2 === e.length
      ? 16 * (Ba[e[0].toUpperCase()] || +e[0]) +
          (Ba[e[1].toUpperCase()] || +e[1])
      : Ba[e[1].toUpperCase()] || +e[1];
  },
  ja = (e, t, l) => {
    ((e = _a(e, 255)), (t = _a(t, 255)), (l = _a(l, 255)));
    const a = Math.max(e, t, l),
      n = Math.min(e, t, l);
    let o;
    const s = a,
      r = a - n,
      i = 0 === a ? 0 : r / a;
    if (a === n) o = 0;
    else {
      switch (a) {
        case e:
          o = (t - l) / r + (t < l ? 6 : 0);
          break;
        case t:
          o = (l - e) / r + 2;
          break;
        case l:
          o = (e - t) / r + 4;
      }
      o /= 6;
    }
    return { h: 360 * o, s: 100 * i, v: 100 * s };
  },
  Ra = function (e, t, l) {
    ((e = 6 * _a(e, 360)), (t = _a(t, 100)), (l = _a(l, 100)));
    const a = Math.floor(e),
      n = e - a,
      o = l * (1 - t),
      s = l * (1 - n * t),
      r = l * (1 - (1 - n) * t),
      i = a % 6,
      u = [l, s, o, o, r, l][i],
      c = [r, l, l, s, o, o][i],
      d = [o, o, r, l, l, s][i];
    return {
      r: Math.round(255 * u),
      g: Math.round(255 * c),
      b: Math.round(255 * d),
    };
  };
class za {
  constructor(e = {}) {
    ((this._hue = 0),
      (this._saturation = 100),
      (this._value = 100),
      (this._alpha = 100),
      (this.enableAlpha = !1),
      (this.format = "hex"),
      (this.value = ""));
    for (const t in e) Te(e, t) && (this[t] = e[t]);
    e.value ? this.fromString(e.value) : this.doOnChange();
  }
  set(e, t) {
    if (1 !== arguments.length || "object" != typeof e)
      ((this[`_${e}`] = t), this.doOnChange());
    else for (const l in e) Te(e, l) && this.set(l, e[l]);
  }
  get(e) {
    return "alpha" === e ? Math.floor(this[`_${e}`]) : this[`_${e}`];
  }
  toRgb() {
    return Ra(this._hue, this._saturation, this._value);
  }
  fromString(e) {
    if (!e)
      return (
        (this._hue = 0),
        (this._saturation = 100),
        (this._value = 100),
        void this.doOnChange()
      );
    const t = (e, t, l) => {
      ((this._hue = Math.max(0, Math.min(360, e))),
        (this._saturation = Math.max(0, Math.min(100, t))),
        (this._value = Math.max(0, Math.min(100, l))),
        this.doOnChange());
    };
    if (e.includes("hsl")) {
      const l = e
        .replace(/hsla|hsl|\(|\)/gm, "")
        .split(/\s|,/g)
        .filter((e) => "" !== e)
        .map((e, t) => (t > 2 ? Number.parseFloat(e) : Number.parseInt(e, 10)));
      if (
        (4 === l.length
          ? (this._alpha = 100 * Number.parseFloat(l[3]))
          : 3 === l.length && (this._alpha = 100),
        l.length >= 3)
      ) {
        const {
          h: e,
          s: a,
          v: n,
        } = (function (e, t, l) {
          l /= 100;
          let a = (t /= 100);
          const n = Math.max(l, 0.01);
          return (
            (t *= (l *= 2) <= 1 ? l : 2 - l),
            (a *= n <= 1 ? n : 2 - n),
            {
              h: e,
              s: 100 * (0 === l ? (2 * a) / (n + a) : (2 * t) / (l + t)),
              v: ((l + t) / 2) * 100,
            }
          );
        })(l[0], l[1], l[2]);
        t(e, a, n);
      }
    } else if (e.includes("hsv")) {
      const l = e
        .replace(/hsva|hsv|\(|\)/gm, "")
        .split(/\s|,/g)
        .filter((e) => "" !== e)
        .map((e, t) => (t > 2 ? Number.parseFloat(e) : Number.parseInt(e, 10)));
      (4 === l.length
        ? (this._alpha = 100 * Number.parseFloat(l[3]))
        : 3 === l.length && (this._alpha = 100),
        l.length >= 3 && t(l[0], l[1], l[2]));
    } else if (e.includes("rgb")) {
      const l = e
        .replace(/rgba|rgb|\(|\)/gm, "")
        .split(/\s|,/g)
        .filter((e) => "" !== e)
        .map((e, t) => (t > 2 ? Number.parseFloat(e) : Number.parseInt(e, 10)));
      if (
        (4 === l.length
          ? (this._alpha = 100 * Number.parseFloat(l[3]))
          : 3 === l.length && (this._alpha = 100),
        l.length >= 3)
      ) {
        const { h: e, s: a, v: n } = ja(l[0], l[1], l[2]);
        t(e, a, n);
      }
    } else if (e.includes("#")) {
      const l = e.replace("#", "").trim();
      if (!/^[0-9a-fA-F]{3}$|^[0-9a-fA-F]{6}$|^[0-9a-fA-F]{8}$/.test(l)) return;
      let a, n, o;
      (3 === l.length
        ? ((a = Da(l[0] + l[0])), (n = Da(l[1] + l[1])), (o = Da(l[2] + l[2])))
        : (6 !== l.length && 8 !== l.length) ||
          ((a = Da(l.slice(0, 2))),
          (n = Da(l.slice(2, 4))),
          (o = Da(l.slice(4, 6)))),
        8 === l.length
          ? (this._alpha = (Da(l.slice(6)) / 255) * 100)
          : (3 !== l.length && 6 !== l.length) || (this._alpha = 100));
      const { h: s, s: r, v: i } = ja(a, n, o);
      t(s, r, i);
    }
  }
  compare(e) {
    return (
      Math.abs(e._hue - this._hue) < 2 &&
      Math.abs(e._saturation - this._saturation) < 1 &&
      Math.abs(e._value - this._value) < 1 &&
      Math.abs(e._alpha - this._alpha) < 1
    );
  }
  doOnChange() {
    const { _hue: e, _saturation: t, _value: l, _alpha: a, format: n } = this;
    if (this.enableAlpha)
      switch (n) {
        case "hsl": {
          const a = Aa(e, t / 100, l / 100);
          this.value = `hsla(${e}, ${Math.round(100 * a[1])}%, ${Math.round(100 * a[2])}%, ${this.get("alpha") / 100})`;
          break;
        }
        case "hsv":
          this.value = `hsva(${e}, ${Math.round(t)}%, ${Math.round(l)}%, ${this.get("alpha") / 100})`;
          break;
        case "hex":
          this.value = `${$a(Ra(e, t, l))}${La((255 * a) / 100)}`;
          break;
        default: {
          const { r: a, g: n, b: o } = Ra(e, t, l);
          this.value = `rgba(${a}, ${n}, ${o}, ${this.get("alpha") / 100})`;
        }
      }
    else
      switch (n) {
        case "hsl": {
          const a = Aa(e, t / 100, l / 100);
          this.value = `hsl(${e}, ${Math.round(100 * a[1])}%, ${Math.round(100 * a[2])}%)`;
          break;
        }
        case "hsv":
          this.value = `hsv(${e}, ${Math.round(t)}%, ${Math.round(l)}%)`;
          break;
        case "rgb": {
          const { r: a, g: n, b: o } = Ra(e, t, l);
          this.value = `rgb(${a}, ${n}, ${o})`;
          break;
        }
        default:
          this.value = $a(Ra(e, t, l));
      }
  }
}
const Fa = v({
    props: {
      colors: { type: Array, required: !0 },
      color: { type: Object, required: !0 },
    },
    setup(e) {
      const t = g("color-predefine"),
        { currentColor: l } = G(Oa),
        a = b(n(e.colors, e.color));
      function n(e, t) {
        return e.map((e) => {
          const l = new za();
          return (
            (l.enableAlpha = !0),
            (l.format = "rgba"),
            l.fromString(e),
            (l.selected = l.value === t.value),
            l
          );
        });
      }
      return (
        ie(
          () => l.value,
          (e) => {
            const t = new za();
            (t.fromString(e),
              a.value.forEach((e) => {
                e.selected = t.compare(e);
              }));
          },
        ),
        Ee(() => {
          a.value = n(e.colors, e.color);
        }),
        {
          rgbaColors: a,
          handleSelect: function (t) {
            e.color.fromString(e.colors[t]);
          },
          ns: t,
        }
      );
    },
  }),
  Ka = ["onClick"];
var Ha = K(Fa, [
  [
    "render",
    function (e, t, l, a, n, o) {
      return (
        x(),
        O(
          "div",
          { class: N(e.ns.b()) },
          [
            V(
              "div",
              { class: N(e.ns.e("colors")) },
              [
                (x(!0),
                O(
                  P,
                  null,
                  L(
                    e.rgbaColors,
                    (t, l) => (
                      x(),
                      O(
                        "div",
                        {
                          key: e.colors[l],
                          class: N([
                            e.ns.e("color-selector"),
                            e.ns.is("alpha", t._alpha < 100),
                            { selected: t.selected },
                          ]),
                          onClick: (t) => e.handleSelect(l),
                        },
                        [
                          V(
                            "div",
                            { style: E({ backgroundColor: t.value }) },
                            null,
                            4,
                          ),
                        ],
                        10,
                        Ka,
                      )
                    ),
                  ),
                  128,
                )),
              ],
              2,
            ),
          ],
          2,
        )
      );
    },
  ],
  [
    "__file",
    "/home/runner/work/element-plus/element-plus/packages/components/color-picker/src/components/predefine.vue",
  ],
]);
const Wa = v({
    name: "ElSlPanel",
    props: { color: { type: Object, required: !0 } },
    setup(e) {
      const t = g("color-svpanel"),
        l = ae(),
        a = b(0),
        n = b(0),
        o = b("hsl(0, 100%, 50%)"),
        s = y(() => ({ hue: e.color.get("hue"), value: e.color.get("value") }));
      function r() {
        const t = e.color.get("saturation"),
          s = e.color.get("value"),
          r = l.vnode.el,
          { clientWidth: i, clientHeight: u } = r;
        ((n.value = (t * i) / 100),
          (a.value = ((100 - s) * u) / 100),
          (o.value = `hsl(${e.color.get("hue")}, 100%, 50%)`));
      }
      function i(t) {
        const o = l.vnode.el.getBoundingClientRect(),
          { clientX: s, clientY: r } = Il(t);
        let i = s - o.left,
          u = r - o.top;
        ((i = Math.max(0, i)),
          (i = Math.min(i, o.width)),
          (u = Math.max(0, u)),
          (u = Math.min(u, o.height)),
          (n.value = i),
          (a.value = u),
          e.color.set({
            saturation: (i / o.width) * 100,
            value: 100 - (u / o.height) * 100,
          }));
      }
      return (
        ie(
          () => s.value,
          () => {
            r();
          },
        ),
        w(() => {
          (Ca(l.vnode.el, {
            drag: (e) => {
              i(e);
            },
            end: (e) => {
              i(e);
            },
          }),
            r());
        }),
        {
          cursorTop: a,
          cursorLeft: n,
          background: o,
          colorValue: s,
          handleDrag: i,
          update: r,
          ns: t,
        }
      );
    },
  }),
  Ua = [V("div", null, null, -1)];
var qa = K(Wa, [
  [
    "render",
    function (e, t, l, a, n, o) {
      return (
        x(),
        O(
          "div",
          { class: N(e.ns.b()), style: E({ backgroundColor: e.background }) },
          [
            V("div", { class: N(e.ns.e("white")) }, null, 2),
            V("div", { class: N(e.ns.e("black")) }, null, 2),
            V(
              "div",
              {
                class: N(e.ns.e("cursor")),
                style: E({
                  top: e.cursorTop + "px",
                  left: e.cursorLeft + "px",
                }),
              },
              Ua,
              6,
            ),
          ],
          6,
        )
      );
    },
  ],
  [
    "__file",
    "/home/runner/work/element-plus/element-plus/packages/components/color-picker/src/components/sv-panel.vue",
  ],
]);
const Ya = [
    "id",
    "aria-label",
    "aria-labelledby",
    "aria-description",
    "tabindex",
    "onKeydown",
  ],
  Ga = v({ name: "ElColorPicker" });
const Xa = q(
    K(
      v({
        ...Ga,
        props: Ma,
        emits: Ia,
        setup(e, { expose: t, emit: l }) {
          const a = e,
            { t: n } = Y(),
            o = g("color"),
            { formItem: s } = he(),
            r = ve(),
            i = m(),
            { inputId: u, isLabeledByFormItem: c } = Me(a, {
              formItemContext: s,
            }),
            d = b(),
            p = b(),
            h = b(),
            v = b();
          let f = !0;
          const k = re(
              new za({
                enableAlpha: a.showAlpha,
                format: a.colorFormat || "",
                value: a.modelValue,
              }),
            ),
            I = b(!1),
            _ = b(!1),
            P = b(""),
            L = y(() =>
              a.modelValue || _.value
                ? (function (e, t) {
                    if (!(e instanceof za))
                      throw new TypeError(
                        "color should be instance of _color Class",
                      );
                    const { r: l, g: a, b: n } = e.toRgb();
                    return t
                      ? `rgba(${l}, ${a}, ${n}, ${e.get("alpha") / 100})`
                      : `rgb(${l}, ${a}, ${n})`;
                  })(k, a.showAlpha)
                : "transparent",
            ),
            $ = y(() => (a.modelValue || _.value ? k.value : "")),
            j = y(() =>
              c.value ? void 0 : a.label || n("el.colorpicker.defaultLabel"),
            ),
            z = y(() => (c.value ? (null == s ? void 0 : s.labelId) : void 0)),
            F = y(() => [
              o.b("picker"),
              o.is("disabled", i.value),
              o.bm("picker", r.value),
            ]);
          function K(e) {
            I.value = e;
          }
          const W = pl(K, 100);
          function U() {
            (W(!1), q());
          }
          function q() {
            H(() => {
              a.modelValue
                ? k.fromString(a.modelValue)
                : ((k.value = ""),
                  H(() => {
                    _.value = !1;
                  }));
            });
          }
          function G() {
            i.value || W(!I.value);
          }
          function Z() {
            k.fromString(P.value);
          }
          function J() {
            const e = k.value;
            (l(ul, e),
              l("change", e),
              a.validateEvent &&
                (null == s || s.validate("change").catch((e) => fe())),
              W(!1),
              H(() => {
                const e = new za({
                  enableAlpha: a.showAlpha,
                  format: a.colorFormat || "",
                  value: a.modelValue,
                });
                k.compare(e) || q();
              }));
          }
          function ee() {
            (W(!1),
              l(ul, null),
              l("change", null),
              null !== a.modelValue &&
                a.validateEvent &&
                (null == s || s.validate("change").catch((e) => fe())),
              q());
          }
          return (
            w(() => {
              a.modelValue && (P.value = $.value);
            }),
            ie(
              () => a.modelValue,
              (e) => {
                e
                  ? e && e !== k.value && ((f = !1), k.fromString(e))
                  : (_.value = !1);
              },
            ),
            ie(
              () => $.value,
              (e) => {
                ((P.value = e), f && l("activeChange", e), (f = !0));
              },
            ),
            ie(
              () => k.value,
              () => {
                a.modelValue || _.value || (_.value = !0);
              },
            ),
            ie(
              () => I.value,
              () => {
                H(() => {
                  var e, t, l;
                  (null == (e = d.value) || e.update(),
                    null == (t = p.value) || t.update(),
                    null == (l = h.value) || l.update());
                });
              },
            ),
            Q(Oa, { currentColor: $ }),
            t({
              color: k,
              show: function () {
                i.value || K(!0);
              },
              hide: U,
            }),
            (e, t) => (
              x(),
              S(
                T(Nt),
                {
                  ref_key: "popper",
                  ref: v,
                  visible: I.value,
                  "show-arrow": !1,
                  "fallback-placements": ["bottom", "top", "right", "left"],
                  offset: 0,
                  "gpu-acceleration": !1,
                  "popper-class": [
                    T(o).be("picker", "panel"),
                    T(o).b("dropdown"),
                    e.popperClass,
                  ],
                  "stop-popper-mouse-event": !1,
                  effect: "light",
                  trigger: "click",
                  transition: `${T(o).namespace.value}-zoom-in-top`,
                  persistent: "",
                },
                {
                  content: C(() => [
                    be(
                      (x(),
                      O("div", null, [
                        V(
                          "div",
                          { class: N(T(o).be("dropdown", "main-wrapper")) },
                          [
                            M(
                              Ea,
                              {
                                ref_key: "hue",
                                ref: d,
                                class: "hue-slider",
                                color: T(k),
                                vertical: "",
                              },
                              null,
                              8,
                              ["color"],
                            ),
                            M(
                              qa,
                              { ref_key: "sv", ref: p, color: T(k) },
                              null,
                              8,
                              ["color"],
                            ),
                          ],
                          2,
                        ),
                        e.showAlpha
                          ? (x(),
                            S(
                              Ta,
                              { key: 0, ref_key: "alpha", ref: h, color: T(k) },
                              null,
                              8,
                              ["color"],
                            ))
                          : X("v-if", !0),
                        e.predefine
                          ? (x(),
                            S(
                              Ha,
                              {
                                key: 1,
                                ref: "predefine",
                                color: T(k),
                                colors: e.predefine,
                              },
                              null,
                              8,
                              ["color", "colors"],
                            ))
                          : X("v-if", !0),
                        V(
                          "div",
                          { class: N(T(o).be("dropdown", "btns")) },
                          [
                            V(
                              "span",
                              { class: N(T(o).be("dropdown", "value")) },
                              [
                                M(
                                  T(Mt),
                                  {
                                    modelValue: P.value,
                                    "onUpdate:modelValue":
                                      t[0] || (t[0] = (e) => (P.value = e)),
                                    "validate-event": !1,
                                    size: "small",
                                    onKeyup: R(Z, ["enter"]),
                                    onBlur: Z,
                                  },
                                  null,
                                  8,
                                  ["modelValue", "onKeyup"],
                                ),
                              ],
                              2,
                            ),
                            M(
                              T(Ie),
                              {
                                class: N(T(o).be("dropdown", "link-btn")),
                                text: "",
                                size: "small",
                                onClick: ee,
                              },
                              {
                                default: C(() => [
                                  B(D(T(n)("el.colorpicker.clear")), 1),
                                ]),
                                _: 1,
                              },
                              8,
                              ["class"],
                            ),
                            M(
                              T(Ie),
                              {
                                plain: "",
                                size: "small",
                                class: N(T(o).be("dropdown", "btn")),
                                onClick: J,
                              },
                              {
                                default: C(() => [
                                  B(D(T(n)("el.colorpicker.confirm")), 1),
                                ]),
                                _: 1,
                              },
                              8,
                              ["class"],
                            ),
                          ],
                          2,
                        ),
                      ])),
                      [[T(wl), U]],
                    ),
                  ]),
                  default: C(() => [
                    V(
                      "div",
                      {
                        id: T(u),
                        class: N(T(F)),
                        role: "button",
                        "aria-label": T(j),
                        "aria-labelledby": T(z),
                        "aria-description": T(n)("el.colorpicker.description", {
                          color: e.modelValue || "",
                        }),
                        tabindex: e.tabindex,
                        onKeydown: R(G, ["enter"]),
                      },
                      [
                        T(i)
                          ? (x(),
                            O(
                              "div",
                              { key: 0, class: N(T(o).be("picker", "mask")) },
                              null,
                              2,
                            ))
                          : X("v-if", !0),
                        V(
                          "div",
                          {
                            class: N(T(o).be("picker", "trigger")),
                            onClick: G,
                          },
                          [
                            V(
                              "span",
                              {
                                class: N([
                                  T(o).be("picker", "color"),
                                  T(o).is("alpha", e.showAlpha),
                                ]),
                              },
                              [
                                V(
                                  "span",
                                  {
                                    class: N(T(o).be("picker", "color-inner")),
                                    style: E({ backgroundColor: T(L) }),
                                  },
                                  [
                                    be(
                                      M(
                                        T(A),
                                        {
                                          class: N([
                                            T(o).be("picker", "icon"),
                                            T(o).is("icon-arrow-down"),
                                          ]),
                                        },
                                        { default: C(() => [M(T(ke))]), _: 1 },
                                        8,
                                        ["class"],
                                      ),
                                      [[Se, e.modelValue || _.value]],
                                    ),
                                    e.modelValue || _.value
                                      ? X("v-if", !0)
                                      : (x(),
                                        S(
                                          T(A),
                                          {
                                            key: 0,
                                            class: N([
                                              T(o).be("picker", "empty"),
                                              T(o).is("icon-close"),
                                            ]),
                                          },
                                          {
                                            default: C(() => [M(T(Oe))]),
                                            _: 1,
                                          },
                                          8,
                                          ["class"],
                                        )),
                                  ],
                                  6,
                                ),
                              ],
                              2,
                            ),
                          ],
                          2,
                        ),
                      ],
                      42,
                      Ya,
                    ),
                  ]),
                  _: 1,
                },
                8,
                ["visible", "popper-class", "transition"],
              )
            )
          );
        },
      }),
      [
        [
          "__file",
          "/home/runner/work/element-plus/element-plus/packages/components/color-picker/src/color-picker.vue",
        ],
      ],
    ),
  ),
  Za = u({
    id: { type: String, default: void 0 },
    step: { type: Number, default: 1 },
    stepStrictly: Boolean,
    max: { type: Number, default: Number.POSITIVE_INFINITY },
    min: { type: Number, default: Number.NEGATIVE_INFINITY },
    modelValue: Number,
    readonly: Boolean,
    disabled: Boolean,
    size: de,
    controls: { type: Boolean, default: !0 },
    controlsPosition: { type: String, default: "", values: ["", "right"] },
    valueOnClear: {
      type: [String, Number, null],
      validator: (e) => null === e || Ae(e) || ["min", "max"].includes(e),
      default: null,
    },
    name: String,
    label: String,
    placeholder: String,
    precision: {
      type: Number,
      validator: (e) => e >= 0 && e === Number.parseInt(`${e}`, 10),
    },
    validateEvent: { type: Boolean, default: !0 },
  }),
  Qa = {
    [dl]: (e, t) => t !== e,
    blur: (e) => e instanceof FocusEvent,
    focus: (e) => e instanceof FocusEvent,
    [cl]: (e) => Ae(e) || hl(e),
    [ul]: (e) => Ae(e) || hl(e),
  },
  Ja = ["aria-label", "onKeydown"],
  en = ["aria-label", "onKeydown"],
  tn = v({ name: "ElInputNumber" });
const ln = q(
    K(
      v({
        ...tn,
        props: Za,
        emits: Qa,
        setup(e, { expose: t, emit: l }) {
          const a = e,
            { t: n } = Y(),
            o = g("input-number"),
            s = b(),
            r = re({ currentValue: a.modelValue, userInput: null }),
            { formItem: i } = he(),
            u = y(() => Ae(a.modelValue) && a.modelValue <= a.min),
            c = y(() => Ae(a.modelValue) && a.modelValue >= a.max),
            d = y(() => {
              const e = E(a.step);
              return se(a.precision)
                ? Math.max(E(a.modelValue), e)
                : (a.precision, a.precision);
            }),
            h = y(() => a.controls && "right" === a.controlsPosition),
            v = ve(),
            f = m(),
            k = y(() => {
              if (null !== r.userInput) return r.userInput;
              let e = r.currentValue;
              if (hl(e)) return "";
              if (Ae(e)) {
                if (Number.isNaN(e)) return "";
                se(a.precision) || (e = e.toFixed(a.precision));
              }
              return e;
            }),
            V = (e, t) => {
              if ((se(t) && (t = d.value), 0 === t)) return Math.round(e);
              let l = String(e);
              const a = l.indexOf(".");
              if (-1 === a) return e;
              if (!l.replace(".", "").split("")[a + t]) return e;
              const n = l.length;
              return (
                "5" === l.charAt(n - 1) &&
                  (l = `${l.slice(0, Math.max(0, n - 1))}6`),
                Number.parseFloat(Number(l).toFixed(t))
              );
            },
            E = (e) => {
              if (hl(e)) return 0;
              const t = e.toString(),
                l = t.indexOf(".");
              let a = 0;
              return (-1 !== l && (a = t.length - l - 1), a);
            },
            I = (e, t = 1) => (Ae(e) ? V(e + a.step * t) : r.currentValue),
            _ = () => {
              if (a.readonly || f.value || c.value) return;
              const e = Number(k.value) || 0,
                t = I(e);
              ($(t), l(cl, r.currentValue));
            },
            P = () => {
              if (a.readonly || f.value || u.value) return;
              const e = Number(k.value) || 0,
                t = I(e, -1);
              ($(t), l(cl, r.currentValue));
            },
            L = (e, t) => {
              const {
                max: n,
                min: o,
                step: s,
                precision: r,
                stepStrictly: i,
                valueOnClear: u,
              } = a;
              n < o && U("InputNumber", "min should not be greater than max.");
              let c = Number(e);
              if (hl(e) || Number.isNaN(c)) return null;
              if ("" === e) {
                if (null === u) return null;
                c = p(u) ? { min: o, max: n }[u] : u;
              }
              return (
                i && (c = V(Math.round(c / s) * s, r)),
                se(r) || (c = V(c, r)),
                (c > n || c < o) && ((c = c > n ? n : o), t && l(ul, c)),
                c
              );
            },
            $ = (e, t = !0) => {
              var n;
              const o = r.currentValue,
                s = L(e);
              t
                ? o !== s &&
                  ((r.userInput = null),
                  l(ul, s),
                  l(dl, s, o),
                  a.validateEvent &&
                    (null == (n = null == i ? void 0 : i.validate) ||
                      n.call(i, "change").catch((e) => fe())),
                  (r.currentValue = s))
                : l(ul, s);
            },
            B = (e) => {
              r.userInput = e;
              const t = "" === e ? null : Number(e);
              (l(cl, t), $(t, !1));
            },
            D = (e) => {
              const t = "" !== e ? Number(e) : "";
              (((Ae(t) && !Number.isNaN(t)) || "" === e) && $(t),
                (r.userInput = null));
            },
            j = (e) => {
              l("focus", e);
            },
            F = (e) => {
              var t;
              (l("blur", e),
                a.validateEvent &&
                  (null == (t = null == i ? void 0 : i.validate) ||
                    t.call(i, "blur").catch((e) => fe())));
            };
          return (
            ie(
              () => a.modelValue,
              (e) => {
                const t = L(r.userInput),
                  l = L(e, !0);
                Ae(t) ||
                  (t && t === l) ||
                  ((r.currentValue = l), (r.userInput = null));
              },
              { immediate: !0 },
            ),
            w(() => {
              var e;
              const { min: t, max: n, modelValue: o } = a,
                i = null == (e = s.value) ? void 0 : e.input;
              if (
                (i.setAttribute("role", "spinbutton"),
                Number.isFinite(n)
                  ? i.setAttribute("aria-valuemax", String(n))
                  : i.removeAttribute("aria-valuemax"),
                Number.isFinite(t)
                  ? i.setAttribute("aria-valuemin", String(t))
                  : i.removeAttribute("aria-valuemin"),
                i.setAttribute("aria-valuenow", String(r.currentValue)),
                i.setAttribute("aria-disabled", String(f.value)),
                !Ae(o) && null != o)
              ) {
                let e = Number(o);
                (Number.isNaN(e) && (e = null), l(ul, e));
              }
            }),
            _e(() => {
              var e;
              const t = null == (e = s.value) ? void 0 : e.input;
              null == t || t.setAttribute("aria-valuenow", `${r.currentValue}`);
            }),
            t({
              focus: () => {
                var e, t;
                null == (t = null == (e = s.value) ? void 0 : e.focus) ||
                  t.call(e);
              },
              blur: () => {
                var e, t;
                null == (t = null == (e = s.value) ? void 0 : e.blur) ||
                  t.call(e);
              },
            }),
            (e, t) => (
              x(),
              O(
                "div",
                {
                  class: N([
                    T(o).b(),
                    T(o).m(T(v)),
                    T(o).is("disabled", T(f)),
                    T(o).is("without-controls", !e.controls),
                    T(o).is("controls-right", T(h)),
                  ]),
                  onDragstart: t[1] || (t[1] = z(() => {}, ["prevent"])),
                },
                [
                  e.controls
                    ? be(
                        (x(),
                        O(
                          "span",
                          {
                            key: 0,
                            role: "button",
                            "aria-label": T(n)("el.inputNumber.decrease"),
                            class: N([
                              T(o).e("decrease"),
                              T(o).is("disabled", T(u)),
                            ]),
                            onKeydown: R(P, ["enter"]),
                          },
                          [
                            M(T(A), null, {
                              default: C(() => [
                                T(h)
                                  ? (x(), S(T(ke), { key: 0 }))
                                  : (x(), S(T(Pe), { key: 1 })),
                              ]),
                              _: 1,
                            }),
                          ],
                          42,
                          Ja,
                        )),
                        [[T(Gt), P]],
                      )
                    : X("v-if", !0),
                  e.controls
                    ? be(
                        (x(),
                        O(
                          "span",
                          {
                            key: 1,
                            role: "button",
                            "aria-label": T(n)("el.inputNumber.increase"),
                            class: N([
                              T(o).e("increase"),
                              T(o).is("disabled", T(c)),
                            ]),
                            onKeydown: R(_, ["enter"]),
                          },
                          [
                            M(T(A), null, {
                              default: C(() => [
                                T(h)
                                  ? (x(), S(T(Le), { key: 0 }))
                                  : (x(), S(T($e), { key: 1 })),
                              ]),
                              _: 1,
                            }),
                          ],
                          42,
                          en,
                        )),
                        [[T(Gt), _]],
                      )
                    : X("v-if", !0),
                  M(
                    T(Mt),
                    {
                      id: e.id,
                      ref_key: "input",
                      ref: s,
                      type: "number",
                      step: e.step,
                      "model-value": T(k),
                      placeholder: e.placeholder,
                      readonly: e.readonly,
                      disabled: T(f),
                      size: T(v),
                      max: e.max,
                      min: e.min,
                      name: e.name,
                      label: e.label,
                      "validate-event": !1,
                      onWheel: t[0] || (t[0] = z(() => {}, ["prevent"])),
                      onKeydown: [
                        R(z(_, ["prevent"]), ["up"]),
                        R(z(P, ["prevent"]), ["down"]),
                      ],
                      onBlur: F,
                      onFocus: j,
                      onInput: B,
                      onChange: D,
                    },
                    null,
                    8,
                    [
                      "id",
                      "step",
                      "model-value",
                      "placeholder",
                      "readonly",
                      "disabled",
                      "size",
                      "max",
                      "min",
                      "name",
                      "label",
                      "onKeydown",
                    ],
                  ),
                ],
                34,
              )
            )
          );
        },
      }),
      [
        [
          "__file",
          "/home/runner/work/element-plus/element-plus/packages/components/input-number/src/input-number.vue",
        ],
      ],
    ),
  ),
  an = u({
    modelValue: { type: Number, default: 0 },
    id: { type: String, default: void 0 },
    lowThreshold: { type: Number, default: 2 },
    highThreshold: { type: Number, default: 4 },
    max: { type: Number, default: 5 },
    colors: { type: c([Array, Object]), default: () => Be(["", "", ""]) },
    voidColor: { type: String, default: "" },
    disabledVoidColor: { type: String, default: "" },
    icons: { type: c([Array, Object]), default: () => [De, De, De] },
    voidIcon: { type: je, default: () => Re },
    disabledVoidIcon: { type: je, default: () => De },
    disabled: Boolean,
    allowHalf: Boolean,
    showText: Boolean,
    showScore: Boolean,
    textColor: { type: String, default: "" },
    texts: {
      type: c(Array),
      default: () =>
        Be(["Extremely bad", "Disappointed", "Fair", "Satisfied", "Surprise"]),
    },
    scoreTemplate: { type: String, default: "{value}" },
    size: de,
    label: { type: String, default: void 0 },
    clearable: { type: Boolean, default: !1 },
  }),
  nn = { [dl]: (e) => Ae(e), [ul]: (e) => Ae(e) },
  on = [
    "id",
    "aria-label",
    "aria-labelledby",
    "aria-valuenow",
    "aria-valuetext",
    "aria-valuemax",
  ],
  sn = ["onMousemove", "onClick"],
  rn = v({ name: "ElRate" }),
  un = v({
    ...rn,
    props: an,
    emits: nn,
    setup(e, { expose: t, emit: l }) {
      const a = e;
      function n(e, t) {
        const l = (e) => h(e),
          a = Object.keys(t)
            .map((e) => +e)
            .filter((a) => {
              const n = t[a];
              return !!l(n) && n.excluded ? e < a : e <= a;
            })
            .sort((e, t) => e - t),
          n = t[a[0]];
        return (l(n) && n.value) || n;
      }
      const o = G(ze, void 0),
        s = G(Fe, void 0),
        r = ve(),
        i = g("rate"),
        { inputId: u, isLabeledByFormItem: c } = Me(a, { formItemContext: s }),
        d = b(a.modelValue),
        v = b(-1),
        f = b(!0),
        m = y(() => [i.b(), i.m(r.value)]),
        k = y(() => a.disabled || (null == o ? void 0 : o.disabled)),
        w = y(() =>
          i.cssVarBlock({
            "void-color": a.voidColor,
            "disabled-void-color": a.disabledVoidColor,
            "fill-color": $.value,
          }),
        ),
        V = y(() => {
          let e = "";
          return (
            a.showScore
              ? (e = a.scoreTemplate.replace(
                  /\{\s*value\s*\}/,
                  k.value ? `${a.modelValue}` : `${d.value}`,
                ))
              : a.showText && (e = a.texts[Math.ceil(d.value) - 1]),
            e
          );
        }),
        I = y(() => 100 * a.modelValue - 100 * Math.floor(a.modelValue)),
        _ = y(() =>
          W(a.colors)
            ? {
                [a.lowThreshold]: a.colors[0],
                [a.highThreshold]: { value: a.colors[1], excluded: !0 },
                [a.max]: a.colors[2],
              }
            : a.colors,
        ),
        $ = y(() => {
          const e = n(d.value, _.value);
          return h(e) ? "" : e;
        }),
        B = y(() => {
          let e = "";
          return (
            k.value ? (e = `${I.value}%`) : a.allowHalf && (e = "50%"),
            { color: $.value, width: e }
          );
        }),
        j = y(() => {
          let e = W(a.icons) ? [...a.icons] : { ...a.icons };
          return (
            (e = Ke(e)),
            W(e)
              ? {
                  [a.lowThreshold]: e[0],
                  [a.highThreshold]: { value: e[1], excluded: !0 },
                  [a.max]: e[2],
                }
              : e
          );
        }),
        R = y(() => n(a.modelValue, j.value)),
        z = y(() =>
          k.value
            ? p(a.disabledVoidIcon)
              ? a.disabledVoidIcon
              : Ke(a.disabledVoidIcon)
            : p(a.voidIcon)
              ? a.voidIcon
              : Ke(a.voidIcon),
        ),
        F = y(() => n(d.value, j.value));
      function K(e) {
        const t =
            k.value && I.value > 0 && e - 1 < a.modelValue && e > a.modelValue,
          l = a.allowHalf && f.value && e - 0.5 <= d.value && e > d.value;
        return t || l;
      }
      function H(e) {
        (a.clearable && e === a.modelValue && (e = 0),
          l(ul, e),
          a.modelValue !== e && l("change", e));
      }
      function U(e) {
        if (k.value) return;
        let t = d.value;
        const n = e.code;
        return (
          n === Z.up || n === Z.right
            ? (a.allowHalf ? (t += 0.5) : (t += 1),
              e.stopPropagation(),
              e.preventDefault())
            : (n !== Z.left && n !== Z.down) ||
              (a.allowHalf ? (t -= 0.5) : (t -= 1),
              e.stopPropagation(),
              e.preventDefault()),
          (t = t < 0 ? 0 : t),
          (t = t > a.max ? a.max : t),
          l(ul, t),
          l("change", t),
          t
        );
      }
      function q(e, t) {
        if (!k.value) {
          if (a.allowHalf && t) {
            let l = t.target;
            (We(l, i.e("item")) && (l = l.querySelector(`.${i.e("icon")}`)),
              (0 === l.clientWidth || We(l, i.e("decimal"))) &&
                (l = l.parentNode),
              (f.value = 2 * t.offsetX <= l.clientWidth),
              (d.value = f.value ? e - 0.5 : e));
          } else d.value = e;
          v.value = e;
        }
      }
      function Y() {
        k.value ||
          (a.allowHalf && (f.value = a.modelValue !== Math.floor(a.modelValue)),
          (d.value = a.modelValue),
          (v.value = -1));
      }
      return (
        ie(
          () => a.modelValue,
          (e) => {
            ((d.value = e),
              (f.value = a.modelValue !== Math.floor(a.modelValue)));
          },
        ),
        a.modelValue || l(ul, 0),
        t({ setCurrentValue: q, resetCurrentValue: Y }),
        (e, t) => {
          var l;
          return (
            x(),
            O(
              "div",
              {
                id: T(u),
                class: N([T(m), T(i).is("disabled", T(k))]),
                role: "slider",
                "aria-label": T(c) ? void 0 : e.label || "rating",
                "aria-labelledby": T(c)
                  ? null == (l = T(s))
                    ? void 0
                    : l.labelId
                  : void 0,
                "aria-valuenow": d.value,
                "aria-valuetext": T(V) || void 0,
                "aria-valuemin": "0",
                "aria-valuemax": e.max,
                tabindex: "0",
                style: E(T(w)),
                onKeydown: U,
              },
              [
                (x(!0),
                O(
                  P,
                  null,
                  L(
                    e.max,
                    (e, t) => (
                      x(),
                      O(
                        "span",
                        {
                          key: t,
                          class: N(T(i).e("item")),
                          onMousemove: (t) => q(e, t),
                          onMouseleave: Y,
                          onClick: (t) => {
                            return (
                              (l = e),
                              void (
                                k.value ||
                                (a.allowHalf && f.value ? H(d.value) : H(l))
                              )
                            );
                            var l;
                          },
                        },
                        [
                          M(
                            T(A),
                            {
                              class: N([
                                T(i).e("icon"),
                                { hover: v.value === e },
                                T(i).is("active", e <= d.value),
                              ]),
                            },
                            {
                              default: C(() => [
                                K(e)
                                  ? X("v-if", !0)
                                  : (x(),
                                    O(
                                      P,
                                      { key: 0 },
                                      [
                                        be(
                                          (x(), S(He(T(F)), null, null, 512)),
                                          [[Se, e <= d.value]],
                                        ),
                                        be(
                                          (x(), S(He(T(z)), null, null, 512)),
                                          [[Se, !(e <= d.value)]],
                                        ),
                                      ],
                                      64,
                                    )),
                                K(e)
                                  ? (x(),
                                    S(
                                      T(A),
                                      {
                                        key: 1,
                                        style: E(T(B)),
                                        class: N([
                                          T(i).e("icon"),
                                          T(i).e("decimal"),
                                        ]),
                                      },
                                      {
                                        default: C(() => [(x(), S(He(T(R))))]),
                                        _: 1,
                                      },
                                      8,
                                      ["style", "class"],
                                    ))
                                  : X("v-if", !0),
                              ]),
                              _: 2,
                            },
                            1032,
                            ["class"],
                          ),
                        ],
                        42,
                        sn,
                      )
                    ),
                  ),
                  128,
                )),
                e.showText || e.showScore
                  ? (x(),
                    O("span", { key: 0, class: N(T(i).e("text")) }, D(T(V)), 3))
                  : X("v-if", !0),
              ],
              46,
              on,
            )
          );
        }
      );
    },
  });
const cn = q(
  K(un, [
    [
      "__file",
      "/home/runner/work/element-plus/element-plus/packages/components/rate/src/rate.vue",
    ],
  ]),
);
var dn =
  Number.isNaN ||
  function (e) {
    return "number" == typeof e && e != e;
  };
function pn(e, t) {
  if (e.length !== t.length) return !1;
  for (var l = 0; l < e.length; l++)
    if (((a = e[l]), (n = t[l]), !(a === n || (dn(a) && dn(n))))) return !1;
  var a, n;
  return !0;
}
const hn = () => {
    const e = ae().proxy.$props;
    return y(() => {
      const t = (e, t, l) => ({});
      return e.perfMode
        ? Ue(t)
        : (function (e, t) {
            void 0 === t && (t = pn);
            var l = null;
            function a() {
              for (var a = [], n = 0; n < arguments.length; n++)
                a[n] = arguments[n];
              if (l && l.lastThis === this && t(a, l.lastArgs))
                return l.lastResult;
              var o = e.apply(this, a);
              return ((l = { lastResult: o, lastArgs: a, lastThis: this }), o);
            }
            return (
              (a.clear = function () {
                l = null;
              }),
              a
            );
          })(t);
    });
  },
  vn = "itemRendered",
  fn = "scroll",
  mn = "forward",
  gn = "backward",
  bn = "auto",
  yn = "smart",
  kn = "start",
  wn = "center",
  xn = "horizontal",
  Sn = "vertical",
  Cn = "rtl",
  Vn = "negative",
  Nn = "positive-ascending",
  Tn = "positive-descending",
  En = { [xn]: "left", [Sn]: "top" },
  Mn = { [xn]: "deltaX", [Sn]: "deltaY" },
  In = qe({ type: c([Number, Function]), required: !0 }),
  On = qe({ type: Number }),
  An = qe({ type: Number, default: 2 }),
  _n = qe({ type: String, values: ["ltr", "rtl"], default: "ltr" }),
  Pn = qe({ type: Number, default: 0 }),
  Ln = qe({ type: Number, required: !0 }),
  $n = qe({ type: String, values: ["horizontal", "vertical"], default: Sn }),
  Bn = u({
    className: { type: String, default: "" },
    containerElement: { type: c([String, Object]), default: "div" },
    data: { type: c(Array), default: () => Be([]) },
    direction: _n,
    height: { type: [String, Number], required: !0 },
    innerElement: { type: [String, Object], default: "div" },
    style: { type: c([Object, String, Array]) },
    useIsScrolling: { type: Boolean, default: !1 },
    width: { type: [Number, String], required: !1 },
    perfMode: { type: Boolean, default: !0 },
    scrollbarAlwaysOn: { type: Boolean, default: !1 },
  }),
  Dn = u({
    cache: An,
    estimatedItemSize: On,
    layout: $n,
    initScrollOffset: Pn,
    total: Ln,
    itemSize: In,
    ...Bn,
  }),
  jn = { type: Number, default: 6 },
  Rn = { type: Number, default: 0 },
  zn = { type: Number, default: 2 };
u({
  columnCache: An,
  columnWidth: In,
  estimatedColumnWidth: On,
  estimatedRowHeight: On,
  initScrollLeft: Pn,
  initScrollTop: Pn,
  itemKey: {
    type: c(Function),
    default: ({ columnIndex: e, rowIndex: t }) => `${t}:${e}`,
  },
  rowCache: An,
  rowHeight: In,
  totalColumn: Ln,
  totalRow: Ln,
  hScrollbarSize: jn,
  vScrollbarSize: jn,
  scrollbarStartGap: Rn,
  scrollbarEndGap: zn,
  role: String,
  ...Bn,
});
const Fn = u({
    alwaysOn: Boolean,
    class: String,
    layout: $n,
    total: Ln,
    ratio: { type: Number, required: !0 },
    clientSize: { type: Number, required: !0 },
    scrollFrom: { type: Number, required: !0 },
    scrollbarSize: jn,
    startGap: Rn,
    endGap: zn,
    visible: Boolean,
  }),
  Kn = (e, t) => (e < t ? mn : gn),
  Hn = (e) => "ltr" === e || e === Cn || e === xn;
let Wn = null;
function Un(e = !1) {
  if (null === Wn || e) {
    const e = document.createElement("div"),
      t = e.style;
    ((t.width = "50px"),
      (t.height = "50px"),
      (t.overflow = "scroll"),
      (t.direction = "rtl"));
    const l = document.createElement("div"),
      a = l.style;
    return (
      (a.width = "100px"),
      (a.height = "100px"),
      e.appendChild(l),
      document.body.appendChild(e),
      e.scrollLeft > 0
        ? (Wn = Tn)
        : ((e.scrollLeft = 1), (Wn = 0 === e.scrollLeft ? Vn : Nn)),
      document.body.removeChild(e),
      Wn
    );
  }
  return Wn;
}
const qn = v({
    name: "ElVirtualScrollBar",
    props: Fn,
    emits: ["scroll", "start-move", "stop-move"],
    setup(e, { emit: t }) {
      const l = y(() => e.startGap + e.endGap),
        a = g("virtual-scrollbar"),
        n = g("scrollbar"),
        o = b(),
        s = b();
      let r = null,
        i = null;
      const u = re({ isDragging: !1, traveled: 0 }),
        c = y(() => Ye[e.layout]),
        d = y(() => e.clientSize - T(l)),
        p = y(() => ({
          position: "absolute",
          width: `${xn === e.layout ? d.value : e.scrollbarSize}px`,
          height: `${xn === e.layout ? e.scrollbarSize : d.value}px`,
          [En[e.layout]]: "2px",
          right: "2px",
          bottom: "2px",
          borderRadius: "4px",
        })),
        h = y(() => {
          const t = e.ratio,
            l = e.clientSize;
          if (t >= 100) return Number.POSITIVE_INFINITY;
          if (t >= 50) return (t * l) / 100;
          const a = l / 3;
          return Math.floor(Math.min(Math.max(t * l, 20), a));
        }),
        v = y(() => {
          if (!Number.isFinite(h.value)) return { display: "none" };
          const t = `${h.value}px`,
            l = (function ({ move: e, size: t, bar: l }, a) {
              const n = {},
                o = `translate${l.axis}(${e}px)`;
              return (
                (n[l.size] = t),
                (n.transform = o),
                (n.msTransform = o),
                (n.webkitTransform = o),
                "horizontal" === a ? (n.height = "100%") : (n.width = "100%"),
                n
              );
            })({ bar: c.value, size: t, move: u.traveled }, e.layout);
          return l;
        }),
        f = y(() => Math.floor(e.clientSize - h.value - T(l))),
        m = () => {
          (window.removeEventListener("mousemove", x),
            window.removeEventListener("mouseup", w),
            (document.onselectstart = i),
            (i = null));
          const e = T(s);
          e &&
            (e.removeEventListener("touchmove", x),
            e.removeEventListener("touchend", w));
        },
        k = (e) => {
          (e.stopImmediatePropagation(),
            e.ctrlKey ||
              [1, 2].includes(e.button) ||
              ((u.isDragging = !0),
              (u[c.value.axis] =
                e.currentTarget[c.value.offset] -
                (e[c.value.client] -
                  e.currentTarget.getBoundingClientRect()[c.value.direction])),
              t("start-move"),
              (() => {
                (window.addEventListener("mousemove", x),
                  window.addEventListener("mouseup", w));
                const e = T(s);
                e &&
                  ((i = document.onselectstart),
                  (document.onselectstart = () => !1),
                  e.addEventListener("touchmove", x),
                  e.addEventListener("touchend", w));
              })()));
        },
        w = () => {
          ((u.isDragging = !1), (u[c.value.axis] = 0), t("stop-move"), m());
        },
        x = (l) => {
          const { isDragging: a } = u;
          if (!a) return;
          if (!s.value || !o.value) return;
          const n = u[c.value.axis];
          if (!n) return;
          Pl(r);
          const i =
            -1 *
              (o.value.getBoundingClientRect()[c.value.direction] -
                l[c.value.client]) -
            (s.value[c.value.offset] - n);
          r = _l(() => {
            ((u.traveled = Math.max(e.startGap, Math.min(i, f.value))),
              t("scroll", i, f.value));
          });
        },
        S = (e) => {
          const l =
            Math.abs(
              e.target.getBoundingClientRect()[c.value.direction] -
                e[c.value.client],
            ) -
            s.value[c.value.offset] / 2;
          ((u.traveled = Math.max(0, Math.min(l, f.value))),
            t("scroll", l, f.value));
        };
      return (
        ie(
          () => e.scrollFrom,
          (e) => {
            u.isDragging || (u.traveled = Math.ceil(e * f.value));
          },
        ),
        Ge(() => {
          m();
        }),
        () =>
          J(
            "div",
            {
              role: "presentation",
              ref: o,
              class: [
                a.b(),
                e.class,
                (e.alwaysOn || u.isDragging) && "always-on",
              ],
              style: p.value,
              onMousedown: z(S, ["stop", "prevent"]),
              onTouchstartPrevent: k,
            },
            J(
              "div",
              { ref: s, class: n.e("thumb"), style: v.value, onMousedown: k },
              [],
            ),
          )
      );
    },
  }),
  Yn = ({
    name: t,
    getOffset: l,
    getItemSize: a,
    getItemOffset: n,
    getEstimatedTotalSize: o,
    getStartIndexForOffset: s,
    getStopIndexForStartIndex: r,
    initCache: i,
    clearCache: u,
    validateProps: c,
  }) =>
    v({
      name: null != t ? t : "ElVirtualList",
      props: Dn,
      emits: [vn, fn],
      setup(t, { emit: d, expose: p }) {
        c(t);
        const h = ae(),
          v = g("vl"),
          f = b(i(t, h)),
          m = hn(),
          k = b(),
          x = b(),
          S = b(),
          C = b({
            isScrolling: !1,
            scrollDir: "forward",
            scrollOffset: Ae(t.initScrollOffset) ? t.initScrollOffset : 0,
            updateRequested: !1,
            isScrollbarDragging: !1,
            scrollbarAlwaysOn: t.scrollbarAlwaysOn,
          }),
          V = y(() => {
            const { total: e, cache: l } = t,
              { isScrolling: a, scrollDir: n, scrollOffset: o } = T(C);
            if (0 === e) return [0, 0, 0, 0];
            const i = s(t, o, T(f)),
              u = r(t, i, o, T(f)),
              c = a && n !== gn ? 1 : Math.max(1, l),
              d = a && n !== mn ? 1 : Math.max(1, l);
            return [
              Math.max(0, i - c),
              Math.max(0, Math.min(e - 1, u + d)),
              i,
              u,
            ];
          }),
          N = y(() => o(t, T(f))),
          E = y(() => Hn(t.layout)),
          M = y(() => [
            {
              position: "relative",
              ["overflow-" + (E.value ? "x" : "y")]: "scroll",
              WebkitOverflowScrolling: "touch",
              willChange: "transform",
            },
            {
              direction: t.direction,
              height: Ae(t.height) ? `${t.height}px` : t.height,
              width: Ae(t.width) ? `${t.width}px` : t.width,
            },
            t.style,
          ]),
          I = y(() => {
            const e = T(N),
              t = T(E);
            return {
              height: t ? "100%" : `${e}px`,
              pointerEvents: T(C).isScrolling ? "none" : void 0,
              width: t ? `${e}px` : "100%",
            };
          }),
          O = y(() => (E.value ? t.width : t.height)),
          { onWheel: A } = ((
            { atEndEdge: e, atStartEdge: t, layout: l },
            a,
          ) => {
            let n,
              o = 0;
            const s = (l) => (l < 0 && t.value) || (l > 0 && e.value);
            return {
              hasReachedEdge: s,
              onWheel: (e) => {
                Pl(n);
                const t = e[Mn[l.value]];
                (s(o) && s(o + t)) ||
                  ((o += t),
                  Ot() || e.preventDefault(),
                  (n = _l(() => {
                    (a(o), (o = 0));
                  })));
              },
            };
          })(
            {
              atStartEdge: y(() => C.value.scrollOffset <= 0),
              atEndEdge: y(() => C.value.scrollOffset >= N.value),
              layout: y(() => t.layout),
            },
            (e) => {
              var t, l;
              (null == (l = (t = S.value).onMouseUp) || l.call(t),
                P(Math.min(C.value.scrollOffset + e, N.value - O.value)));
            },
          ),
          _ = () => {
            const { total: e } = t;
            if (e > 0) {
              const [e, t, l, a] = T(V);
              d(vn, e, t, l, a);
            }
            const { scrollDir: l, scrollOffset: a, updateRequested: n } = T(C);
            d(fn, l, a, n);
          },
          P = (e) => {
            (e = Math.max(e, 0)) !== T(C).scrollOffset &&
              ((C.value = {
                ...T(C),
                scrollOffset: e,
                scrollDir: Kn(T(C).scrollOffset, e),
                updateRequested: !0,
              }),
              H($));
          },
          L = (e, a = bn) => {
            const { scrollOffset: n } = T(C);
            ((e = Math.max(0, Math.min(e, t.total - 1))),
              P(l(t, e, a, n, T(f))));
          },
          $ = () => {
            ((C.value.isScrolling = !1),
              H(() => {
                m.value(-1, null, null);
              }));
          },
          B = () => {
            const e = k.value;
            e && (e.scrollTop = 0);
          };
        (w(() => {
          if (!e) return;
          const { initScrollOffset: l } = t,
            a = T(k);
          (Ae(l) && a && (T(E) ? (a.scrollLeft = l) : (a.scrollTop = l)), _());
        }),
          _e(() => {
            const { direction: e, layout: l } = t,
              { scrollOffset: a, updateRequested: n } = T(C),
              o = T(k);
            if (n && o)
              if (l === xn)
                if (e === Cn)
                  switch (Un()) {
                    case Vn:
                      o.scrollLeft = -a;
                      break;
                    case Nn:
                      o.scrollLeft = a;
                      break;
                    default: {
                      const { clientWidth: e, scrollWidth: t } = o;
                      o.scrollLeft = t - e - a;
                      break;
                    }
                  }
                else o.scrollLeft = a;
              else o.scrollTop = a;
          }));
        const D = {
          ns: v,
          clientSize: O,
          estimatedTotalSize: N,
          windowStyle: M,
          windowRef: k,
          innerRef: x,
          innerStyle: I,
          itemsToRender: V,
          scrollbarRef: S,
          states: C,
          getItemStyle: (e) => {
            const { direction: l, itemSize: o, layout: s } = t,
              r = m.value(u && o, u && s, u && l);
            let i;
            if (Te(r, String(e))) i = r[e];
            else {
              const o = n(t, e, T(f)),
                s = a(t, e, T(f)),
                u = T(E),
                c = l === Cn,
                d = u ? o : 0;
              r[e] = i = {
                position: "absolute",
                left: c ? void 0 : `${d}px`,
                right: c ? `${d}px` : void 0,
                top: u ? 0 : `${o}px`,
                height: u ? "100%" : `${s}px`,
                width: u ? `${s}px` : "100%",
              };
            }
            return i;
          },
          onScroll: (e) => {
            (T(E)
              ? ((e) => {
                  const {
                      clientWidth: l,
                      scrollLeft: a,
                      scrollWidth: n,
                    } = e.currentTarget,
                    o = T(C);
                  if (o.scrollOffset === a) return;
                  const { direction: s } = t;
                  let r = a;
                  if (s === Cn)
                    switch (Un()) {
                      case Vn:
                        r = -a;
                        break;
                      case Tn:
                        r = n - l - a;
                    }
                  ((r = Math.max(0, Math.min(r, n - l))),
                    (C.value = {
                      ...o,
                      isScrolling: !0,
                      scrollDir: Kn(o.scrollOffset, r),
                      scrollOffset: r,
                      updateRequested: !1,
                    }),
                    H($));
                })(e)
              : ((e) => {
                  const {
                      clientHeight: t,
                      scrollHeight: l,
                      scrollTop: a,
                    } = e.currentTarget,
                    n = T(C);
                  if (n.scrollOffset === a) return;
                  const o = Math.max(0, Math.min(a, l - t));
                  ((C.value = {
                    ...n,
                    isScrolling: !0,
                    scrollDir: Kn(n.scrollOffset, o),
                    scrollOffset: o,
                    updateRequested: !1,
                  }),
                    H($));
                })(e),
              _());
          },
          onScrollbarScroll: (e, t) => {
            const l = ((N.value - O.value) / t) * e;
            P(Math.min(N.value - O.value, l));
          },
          onWheel: A,
          scrollTo: P,
          scrollToItem: L,
          resetScrollTop: B,
        };
        return (
          p({
            windowRef: k,
            innerRef: x,
            getItemStyleCache: m,
            scrollTo: P,
            scrollToItem: L,
            resetScrollTop: B,
            states: C,
          }),
          D
        );
      },
      render(e) {
        var t;
        const {
            $slots: l,
            className: a,
            clientSize: n,
            containerElement: o,
            data: s,
            getItemStyle: r,
            innerElement: i,
            itemsToRender: u,
            innerStyle: c,
            layout: d,
            total: h,
            onScroll: v,
            onScrollbarScroll: f,
            onWheel: m,
            states: g,
            useIsScrolling: b,
            windowStyle: y,
            ns: k,
          } = e,
          [w, x] = u,
          S = He(o),
          C = He(i),
          V = [];
        if (h > 0)
          for (let p = w; p <= x; p++)
            V.push(
              null == (t = l.default)
                ? void 0
                : t.call(l, {
                    data: s,
                    key: p,
                    index: p,
                    isScrolling: b ? g.isScrolling : void 0,
                    style: r(p),
                  }),
            );
        const N = [
            J(
              C,
              { style: c, ref: "innerRef" },
              p(C) ? V : { default: () => V },
            ),
          ],
          T = J(qn, {
            ref: "scrollbarRef",
            clientSize: n,
            layout: d,
            onScroll: f,
            ratio: (100 * n) / this.estimatedTotalSize,
            scrollFrom: g.scrollOffset / (this.estimatedTotalSize - n),
            total: h,
          }),
          E = J(
            S,
            {
              class: [k.e("window"), a],
              style: y,
              onScroll: v,
              onWheel: m,
              ref: "windowRef",
              key: 0,
            },
            p(S) ? [N] : { default: () => [N] },
          );
        return J(
          "div",
          {
            key: 0,
            class: [k.e("wrapper"), g.scrollbarAlwaysOn ? "always-on" : ""],
          },
          [E, T],
        );
      },
    }),
  Gn = Yn({
    name: "ElFixedSizeList",
    getItemOffset: ({ itemSize: e }, t) => t * e,
    getItemSize: ({ itemSize: e }) => e,
    getEstimatedTotalSize: ({ total: e, itemSize: t }) => t * e,
    getOffset: (
      { height: e, total: t, itemSize: l, layout: a, width: n },
      o,
      s,
      r,
    ) => {
      const i = Hn(a) ? n : e,
        u = Math.max(0, t * l - i),
        c = Math.min(u, o * l),
        d = Math.max(0, (o + 1) * l - i);
      switch ((s === yn && (s = r >= d - i && r <= c + i ? bn : wn), s)) {
        case kn:
          return c;
        case "end":
          return d;
        case wn: {
          const e = Math.round(d + (c - d) / 2);
          return e < Math.ceil(i / 2) ? 0 : e > u + Math.floor(i / 2) ? u : e;
        }
        default:
          return r >= d && r <= c ? r : r < d ? d : c;
      }
    },
    getStartIndexForOffset: ({ total: e, itemSize: t }, l) =>
      Math.max(0, Math.min(e - 1, Math.floor(l / t))),
    getStopIndexForStartIndex: (
      { height: e, total: t, itemSize: l, layout: a, width: n },
      o,
      s,
    ) => {
      const r = o * l,
        i = Hn(a) ? n : e,
        u = Math.ceil((i + s - r) / l);
      return Math.max(0, Math.min(t - 1, o + u - 1));
    },
    initCache() {},
    clearCache: !0,
    validateProps() {},
  }),
  Xn = (e, t, l) => {
    const { itemSize: a } = e,
      { items: n, lastVisitedIndex: o } = l;
    if (t > o) {
      let e = 0;
      if (o >= 0) {
        const t = n[o];
        e = t.offset + t.size;
      }
      for (let l = o + 1; l <= t; l++) {
        const t = a(l);
        ((n[l] = { offset: e, size: t }), (e += t));
      }
      l.lastVisitedIndex = t;
    }
    return n[t];
  },
  Zn = (e, t, l, a, n) => {
    for (; l <= a; ) {
      const o = l + Math.floor((a - l) / 2),
        s = Xn(e, o, t).offset;
      if (s === n) return o;
      s < n ? (l = o + 1) : s > n && (a = o - 1);
    }
    return Math.max(0, l - 1);
  },
  Qn = (e, t, l, a) => {
    const { total: n } = e;
    let o = 1;
    for (; l < n && Xn(e, l, t).offset < a; ) ((l += o), (o *= 2));
    return Zn(e, t, Math.floor(l / 2), Math.min(l, n - 1), a);
  },
  Jn = (
    { total: e },
    { items: t, estimatedItemSize: l, lastVisitedIndex: a },
  ) => {
    let n = 0;
    if ((a >= e && (a = e - 1), a >= 0)) {
      const e = t[a];
      n = e.offset + e.size;
    }
    return n + (e - a - 1) * l;
  },
  eo = Yn({
    name: "ElDynamicSizeList",
    getItemOffset: (e, t, l) => Xn(e, t, l).offset,
    getItemSize: (e, t, { items: l }) => l[t].size,
    getEstimatedTotalSize: Jn,
    getOffset: (e, t, l, a, n) => {
      const { height: o, layout: s, width: r } = e,
        i = Hn(s) ? r : o,
        u = Xn(e, t, n),
        c = Jn(e, n),
        d = Math.max(0, Math.min(c - i, u.offset)),
        p = Math.max(0, u.offset - i + u.size);
      switch ((l === yn && (l = a >= p - i && a <= d + i ? bn : wn), l)) {
        case kn:
          return d;
        case "end":
          return p;
        case wn:
          return Math.round(p + (d - p) / 2);
        default:
          return a >= p && a <= d ? a : a < p ? p : d;
      }
    },
    getStartIndexForOffset: (e, t, l) =>
      ((e, t, l) => {
        const { items: a, lastVisitedIndex: n } = t;
        return (n > 0 ? a[n].offset : 0) >= l
          ? Zn(e, t, 0, n, l)
          : Qn(e, t, Math.max(0, n), l);
      })(e, l, t),
    getStopIndexForStartIndex: (e, t, l, a) => {
      const { height: n, total: o, layout: s, width: r } = e,
        i = Hn(s) ? r : n,
        u = Xn(e, t, a),
        c = l + i;
      let d = u.offset + u.size,
        p = t;
      for (; p < o - 1 && d < c; ) (p++, (d += Xn(e, p, a).size));
      return p;
    },
    initCache({ estimatedItemSize: e = 50 }, t) {
      const l = {
        items: {},
        estimatedItemSize: e,
        lastVisitedIndex: -1,
        clearCacheAfterIndex: (e, a = !0) => {
          var n, o;
          ((l.lastVisitedIndex = Math.min(l.lastVisitedIndex, e - 1)),
            null == (n = t.exposed) || n.getItemStyleCache(-1),
            a && (null == (o = t.proxy) || o.$forceUpdate()));
        },
      };
      return l;
    },
    clearCache: !1,
    validateProps: ({ itemSize: e }) => {},
  });
var to = K(
  v({
    props: {
      item: { type: Object, required: !0 },
      style: Object,
      height: Number,
    },
    setup: () => ({ ns: g("select") }),
  }),
  [
    [
      "render",
      function (e, t, l, a, n, o) {
        return e.item.isTitle
          ? (x(),
            O(
              "div",
              {
                key: 0,
                class: N(e.ns.be("group", "title")),
                style: E([e.style, { lineHeight: `${e.height}px` }]),
              },
              D(e.item.label),
              7,
            ))
          : (x(),
            O(
              "div",
              {
                key: 1,
                class: N(e.ns.be("group", "split")),
                style: E(e.style),
              },
              [
                V(
                  "span",
                  {
                    class: N(e.ns.be("group", "split-dash")),
                    style: E({ top: e.height / 2 + "px" }),
                  },
                  null,
                  6,
                ),
              ],
              6,
            ));
      },
    ],
    [
      "__file",
      "/home/runner/work/element-plus/element-plus/packages/components/select-v2/src/group-item.vue",
    ],
  ],
);
const lo = {
    allowCreate: Boolean,
    autocomplete: { type: String, default: "none" },
    automaticDropdown: Boolean,
    clearable: Boolean,
    clearIcon: { type: [String, Object], default: ye },
    effect: { type: String, default: "light" },
    collapseTags: Boolean,
    collapseTagsTooltip: { type: Boolean, default: !1 },
    maxCollapseTags: { type: Number, default: 1 },
    defaultFirstOption: Boolean,
    disabled: Boolean,
    estimatedOptionHeight: { type: Number, default: void 0 },
    filterable: Boolean,
    filterMethod: Function,
    height: { type: Number, default: 170 },
    itemHeight: { type: Number, default: 34 },
    id: String,
    loading: Boolean,
    loadingText: String,
    label: String,
    modelValue: [Array, String, Number, Boolean, Object],
    multiple: Boolean,
    multipleLimit: { type: Number, default: 0 },
    name: String,
    noDataText: String,
    noMatchText: String,
    remoteMethod: Function,
    reserveKeyword: { type: Boolean, default: !0 },
    options: { type: Array, required: !0 },
    placeholder: { type: String },
    teleported: Vt.teleported,
    persistent: { type: Boolean, default: !0 },
    popperClass: { type: String, default: "" },
    popperOptions: { type: Object, default: () => ({}) },
    remote: Boolean,
    size: { type: String, validator: xl },
    valueKey: { type: String, default: "value" },
    scrollbarAlwaysOn: { type: Boolean, default: !1 },
    validateEvent: { type: Boolean, default: !0 },
    placement: { type: c(String), values: Tt, default: "bottom-start" },
  },
  ao = {
    data: Array,
    disabled: Boolean,
    hovering: Boolean,
    item: Object,
    index: Number,
    style: Object,
    selected: Boolean,
    created: Boolean,
  },
  no = v({
    props: ao,
    emits: ["select", "hover"],
    setup(e, { emit: t }) {
      const l = g("select"),
        { hoverItem: a, selectOptionClick: n } = (function (e, { emit: t }) {
          return {
            hoverItem: () => {
              e.disabled || t("hover", e.index);
            },
            selectOptionClick: () => {
              e.disabled || t("select", e.item, e.index);
            },
          };
        })(e, { emit: t });
      return { ns: l, hoverItem: a, selectOptionClick: n };
    },
  }),
  oo = ["aria-selected"];
var so = K(no, [
  [
    "render",
    function (e, t, l, a, n, o) {
      return (
        x(),
        O(
          "li",
          {
            "aria-selected": e.selected,
            style: E(e.style),
            class: N([
              e.ns.be("dropdown", "option-item"),
              e.ns.is("selected", e.selected),
              e.ns.is("disabled", e.disabled),
              e.ns.is("created", e.created),
              { hover: e.hovering },
            ]),
            onMouseenter:
              t[0] || (t[0] = (...t) => e.hoverItem && e.hoverItem(...t)),
            onClick:
              t[1] ||
              (t[1] = z(
                (...t) => e.selectOptionClick && e.selectOptionClick(...t),
                ["stop"],
              )),
          },
          [
            $(
              e.$slots,
              "default",
              { item: e.item, index: e.index, disabled: e.disabled },
              () => [V("span", null, D(e.item.label), 1)],
            ),
          ],
          46,
          oo,
        )
      );
    },
  ],
  [
    "__file",
    "/home/runner/work/element-plus/element-plus/packages/components/select-v2/src/option-item.vue",
  ],
]);
const ro = Symbol("ElSelectV2Injection");
var io = v({
  name: "ElSelectDropdown",
  props: {
    data: { type: Array, required: !0 },
    hoveringIndex: Number,
    width: Number,
  },
  setup(e, { slots: t, expose: l }) {
    const a = G(ro),
      n = g("select"),
      o = b([]),
      s = b(),
      r = y(() => e.data.length);
    ie(
      () => r.value,
      () => {
        var e, t;
        null == (t = (e = a.popper.value).updatePopper) || t.call(e);
      },
    );
    const i = y(() => se(a.props.estimatedOptionHeight)),
      u = y(() =>
        i.value
          ? { itemSize: a.props.itemHeight }
          : {
              estimatedSize: a.props.estimatedOptionHeight,
              itemSize: (e) => o.value[e],
            },
      ),
      c = (e, t) => {
        const { valueKey: l } = a.props;
        return a.props.multiple
          ? ((e = [], t) => {
              const {
                props: { valueKey: l },
              } = a;
              return h(t)
                ? e && e.some((e) => Xe(e, l) === Xe(t, l))
                : e.includes(t);
            })(e, Xe(t, l))
          : ((e, t) => {
              if (h(t)) {
                const { valueKey: l } = a.props;
                return Xe(e, l) === Xe(t, l);
              }
              return e === t;
            })(e, Xe(t, l));
      },
      d = (e, t) => {
        const { disabled: l, multiple: n, multipleLimit: o } = a.props;
        return l || (!t && !!n && o > 0 && e.length >= o);
      },
      p = (t) => e.hoveringIndex === t;
    l({
      listRef: s,
      isSized: i,
      isItemDisabled: d,
      isItemHovering: p,
      isItemSelected: c,
      scrollToItem: (e) => {
        const t = s.value;
        t && t.scrollToItem(e);
      },
      resetScrollTop: () => {
        const e = s.value;
        e && e.resetScrollTop();
      },
    });
    const v = (e) => {
        const { index: l, data: n, style: o } = e,
          s = T(i),
          { itemSize: r, estimatedSize: h } = T(u),
          { modelValue: v } = a.props,
          { onSelect: f, onHover: m } = a,
          g = n[l];
        if ("Group" === g.type)
          return M(to, { item: g, style: o, height: s ? r : h }, null);
        const b = c(v, g),
          y = d(v, b),
          k = p(l);
        return M(
          so,
          j(e, {
            selected: b,
            disabled: g.disabled || y,
            created: !!g.created,
            hovering: k,
            item: g,
            onSelect: f,
            onHover: m,
          }),
          {
            default: (e) => {
              var l;
              return (
                (null == (l = t.default) ? void 0 : l.call(t, e)) ||
                M("span", null, [g.label])
              );
            },
          },
        );
      },
      { onKeyboardNavigate: f, onKeyboardSelect: m } = a,
      k = (e) => {
        const { code: t } = e,
          { tab: l, esc: n, down: o, up: s, enter: r } = Z;
        switch ((t !== l && (e.preventDefault(), e.stopPropagation()), t)) {
          case l:
          case n:
            a.expanded = !1;
            break;
          case o:
            f("forward");
            break;
          case s:
            f("backward");
            break;
          case r:
            m();
        }
      };
    return () => {
      var l;
      const { data: o, width: r } = e,
        { height: c, multiple: d, scrollbarAlwaysOn: p } = a.props;
      if (0 === o.length)
        return M(
          "div",
          { class: n.b("dropdown"), style: { width: `${r}px` } },
          [null == (l = t.empty) ? void 0 : l.call(t)],
        );
      const h = T(i) ? Gn : eo;
      return M("div", { class: [n.b("dropdown"), n.is("multiple", d)] }, [
        M(
          h,
          j({ ref: s }, T(u), {
            className: n.be("dropdown", "list"),
            scrollbarAlwaysOn: p,
            data: o,
            height: c,
            width: r,
            total: o.length,
            onKeydown: k,
          }),
          { default: (e) => M(v, e, null) },
        ),
      ]);
    };
  },
});
function uo(e, t) {
  const l = b(0),
    a = b(null),
    n = y(() => e.allowCreate && e.filterable);
  return {
    createNewOption: function (o) {
      if (n.value)
        if (
          o &&
          o.length > 0 &&
          !(function (l) {
            const a = (e) => e.value === l;
            return (e.options && e.options.some(a)) || t.createdOptions.some(a);
          })(o)
        ) {
          const e = { value: o, label: o, created: !0, disabled: !1 };
          t.createdOptions.length >= l.value
            ? (t.createdOptions[l.value] = e)
            : t.createdOptions.push(e);
        } else if (e.multiple) t.createdOptions.length = l.value;
        else {
          const e = a.value;
          ((t.createdOptions.length = 0),
            e && e.created && t.createdOptions.push(e));
        }
    },
    removeNewOption: function (a) {
      if (
        !n.value ||
        !a ||
        !a.created ||
        (a.created && e.reserveKeyword && t.inputValue === a.label)
      )
        return;
      const o = t.createdOptions.findIndex((e) => e.value === a.value);
      ~o && (t.createdOptions.splice(o, 1), l.value--);
    },
    selectNewOption: function (t) {
      n.value && (e.multiple && t.created ? l.value++ : (a.value = t));
    },
    clearAllNewOption: function () {
      n.value && ((t.createdOptions.length = 0), (l.value = 0));
    },
  };
}
const co = { larget: 51, default: 42, small: 33 },
  po = (e, t) => {
    const { t: l } = Y(),
      a = g("select-v2"),
      n = g("input"),
      { form: o, formItem: s } = he(),
      r = re({
        inputValue: "",
        displayInputValue: "",
        calculatedWidth: 0,
        cachedPlaceholder: "",
        cachedOptions: [],
        createdOptions: [],
        createdLabel: "",
        createdSelected: !1,
        currentPlaceholder: "",
        hoveringIndex: -1,
        comboBoxHovering: !1,
        isOnComposition: !1,
        isSilentBlur: !1,
        isComposing: !1,
        inputLength: 20,
        selectWidth: 200,
        initialInputHeight: 0,
        previousQuery: null,
        previousValue: void 0,
        query: "",
        selectedLabel: "",
        softFocus: !1,
        tagInMultiLine: !1,
      }),
      i = b(-1),
      u = b(-1),
      c = b(null),
      d = b(null),
      p = b(null),
      v = b(null),
      f = b(null),
      m = b(null),
      k = b(null),
      x = b(!1),
      S = y(() => e.disabled || (null == o ? void 0 : o.disabled)),
      C = y(() => {
        const t = 34 * _.value.length;
        return t > e.height ? e.height : t;
      }),
      V = y(() => !hl(e.modelValue)),
      N = y(() => {
        const t = e.multiple
          ? Array.isArray(e.modelValue) && e.modelValue.length > 0
          : V.value;
        return e.clearable && !S.value && r.comboBoxHovering && t;
      }),
      T = y(() => (e.remote && e.filterable ? "" : Le)),
      E = y(() => T.value && a.is("reverse", x.value)),
      M = y(() => (null == s ? void 0 : s.validateState) || ""),
      I = y(() => Ze[M.value]),
      O = y(() => (e.remote ? 300 : 0)),
      A = y(() => {
        const t = _.value;
        return e.loading
          ? e.loadingText || l("el.select.loading")
          : (!e.remote || "" !== r.inputValue || 0 !== t.length) &&
              (e.filterable && r.inputValue && t.length > 0
                ? e.noMatchText || l("el.select.noMatch")
                : 0 === t.length
                  ? e.noDataText || l("el.select.noData")
                  : null);
      }),
      _ = y(() => {
        const t = (e) => {
          const t = r.inputValue,
            l = new RegExp(fl(t), "i");
          return !t || l.test(e.label || "");
        };
        return e.loading
          ? []
          : ((e) => {
              const t = [];
              return (
                e.forEach((e) => {
                  W(e.options)
                    ? (t.push({ label: e.label, isTitle: !0, type: "Group" }),
                      e.options.forEach((e) => {
                        t.push(e);
                      }),
                      t.push({ type: "Group" }))
                    : t.push(e);
                }),
                t
              );
            })(
              e.options
                .concat(r.createdOptions)
                .map((l) => {
                  if (W(l.options)) {
                    const e = l.options.filter(t);
                    if (e.length > 0) return { ...l, options: e };
                  } else if (e.remote || t(l)) return l;
                  return null;
                })
                .filter((e) => null !== e),
            );
      }),
      P = y(() => {
        const e = new Map();
        return (
          _.value.forEach((t, l) => {
            e.set(me(t), { option: t, index: l });
          }),
          e
        );
      }),
      L = y(() => _.value.every((e) => e.disabled)),
      $ = ve(),
      B = y(() => ("small" === $.value ? "small" : "default")),
      D = y(() => {
        const e = m.value,
          t = B.value || "default",
          l = e ? Number.parseInt(getComputedStyle(e).paddingLeft) : 0,
          a = e ? Number.parseInt(getComputedStyle(e).paddingRight) : 0;
        return r.selectWidth - a - l - co[t];
      }),
      j = () => {
        var e;
        u.value = (null == (e = f.value) ? void 0 : e.offsetWidth) || 200;
      },
      R = y(() => ({
        width: `${0 === r.calculatedWidth ? 11 : Math.ceil(r.calculatedWidth) + 11}px`,
      })),
      z = y(() =>
        W(e.modelValue)
          ? 0 === e.modelValue.length && !r.displayInputValue
          : !e.filterable || 0 === r.displayInputValue.length,
      ),
      F = y(() => {
        const t = e.placeholder || l("el.select.placeholder");
        return e.multiple || hl(e.modelValue) ? t : r.selectedLabel;
      }),
      K = y(() => {
        var e, t;
        return null == (t = null == (e = v.value) ? void 0 : e.popperRef)
          ? void 0
          : t.contentRef;
      }),
      U = y(() => {
        if (e.multiple) {
          const t = e.modelValue.length;
          if (e.modelValue.length > 0 && P.value.has(e.modelValue[t - 1])) {
            const { index: l } = P.value.get(e.modelValue[t - 1]);
            return l;
          }
        } else if (e.modelValue && P.value.has(e.modelValue)) {
          const { index: t } = P.value.get(e.modelValue);
          return t;
        }
        return -1;
      }),
      q = y({
        get: () => x.value && !1 !== A.value,
        set(e) {
          x.value = e;
        },
      }),
      G = y(() => r.cachedOptions.slice(0, e.maxCollapseTags)),
      X = y(() => r.cachedOptions.slice(e.maxCollapseTags)),
      {
        createNewOption: Z,
        removeNewOption: Q,
        selectNewOption: J,
        clearAllNewOption: ee,
      } = uo(e, r),
      {
        handleCompositionStart: te,
        handleCompositionUpdate: le,
        handleCompositionEnd: ae,
      } = (function (e) {
        const t = b(!1);
        return {
          handleCompositionStart: () => {
            t.value = !0;
          },
          handleCompositionUpdate: (e) => {
            const l = e.target.value,
              a = l[l.length - 1] || "";
            t.value = !It(a);
          },
          handleCompositionEnd: (l) => {
            t.value && ((t.value = !1), oe(e) && e(l));
          },
        };
      })((e) => Ee(e)),
      ne = () => {
        var e, t, l;
        (null == (t = null == (e = d.value) ? void 0 : e.focus) || t.call(e),
          null == (l = v.value) || l.updatePopper());
      },
      se = () => {
        if (!e.automaticDropdown)
          return S.value
            ? void 0
            : (r.isComposing && (r.softFocus = !0),
              H(() => {
                var e, t;
                ((x.value = !x.value),
                  null == (t = null == (e = d.value) ? void 0 : e.focus) ||
                    t.call(e));
              }));
      },
      ue = () => (
        e.filterable &&
          r.inputValue !== r.selectedLabel &&
          (r.query = r.selectedLabel),
        de(r.inputValue),
        H(() => {
          Z(r.inputValue);
        })
      ),
      ce = pl(ue, O.value),
      de = (t) => {
        r.previousQuery !== t &&
          ((r.previousQuery = t),
          e.filterable && oe(e.filterMethod)
            ? e.filterMethod(t)
            : e.filterable &&
              e.remote &&
              oe(e.remoteMethod) &&
              e.remoteMethod(t));
      },
      pe = (l) => {
        (t(ul, l),
          ((l) => {
            gl(e.modelValue, l) || t(dl, l);
          })(l),
          (r.previousValue = null == l ? void 0 : l.toString()));
      },
      me = (t) => (h(t) ? Xe(t, e.valueKey) : t),
      be = () =>
        H(() => {
          var e, t;
          if (!d.value) return;
          const l = m.value;
          ((f.value.height = l.offsetHeight),
            x.value &&
              !1 !== A.value &&
              (null == (t = null == (e = v.value) ? void 0 : e.updatePopper) ||
                t.call(e)));
        }),
      ye = () => {
        var t, l;
        if (
          (ke(),
          j(),
          null == (l = null == (t = v.value) ? void 0 : t.updatePopper) ||
            l.call(t),
          e.multiple)
        )
          return be();
      },
      ke = () => {
        const e = m.value;
        e && (r.selectWidth = e.getBoundingClientRect().width);
      },
      we = (t, l, a = !0) => {
        var n, o;
        if (e.multiple) {
          let a = e.modelValue.slice();
          const s = ((t = [], l) => {
            if (!h(l)) return t.indexOf(l);
            const a = e.valueKey;
            let n = -1;
            return (
              t.some((e, t) => Xe(e, a) === Xe(l, a) && ((n = t), !0)),
              n
            );
          })(a, me(t));
          (s > -1
            ? ((a = [...a.slice(0, s), ...a.slice(s + 1)]),
              r.cachedOptions.splice(s, 1),
              Q(t))
            : (e.multipleLimit <= 0 || a.length < e.multipleLimit) &&
              ((a = [...a, me(t)]), r.cachedOptions.push(t), J(t), Ve(l)),
            pe(a),
            t.created && ((r.query = ""), de(""), (r.inputLength = 20)),
            e.filterable &&
              !e.reserveKeyword &&
              (null == (o = (n = d.value).focus) || o.call(n), Se("")),
            e.filterable &&
              (r.calculatedWidth = k.value.getBoundingClientRect().width),
            be(),
            Te());
        } else
          ((i.value = l),
            (r.selectedLabel = t.label),
            pe(me(t)),
            (x.value = !1),
            (r.isComposing = !1),
            (r.isSilentBlur = a),
            J(t),
            t.created || ee(),
            Ve(l));
      },
      xe = (e) => (
        (r.softFocus = !1),
        H(() => {
          var l, a;
          (null == (a = null == (l = d.value) ? void 0 : l.blur) || a.call(l),
            k.value &&
              (r.calculatedWidth = k.value.getBoundingClientRect().width),
            r.isSilentBlur
              ? (r.isSilentBlur = !1)
              : r.isComposing && t("blur", e),
            (r.isComposing = !1));
        })
      ),
      Se = (e) => {
        ((r.displayInputValue = e), (r.inputValue = e));
      },
      Ce = (e, t = void 0) => {
        const l = _.value;
        if (
          !["forward", "backward"].includes(e) ||
          S.value ||
          l.length <= 0 ||
          L.value
        )
          return;
        if (!x.value) return se();
        void 0 === t && (t = r.hoveringIndex);
        let a = -1;
        "forward" === e
          ? ((a = t + 1), a >= l.length && (a = 0))
          : "backward" === e &&
            ((a = t - 1), (a < 0 || a >= l.length) && (a = l.length - 1));
        const n = l[a];
        if (n.disabled || "Group" === n.type) return Ce(e, a);
        (Ve(a), Me(a));
      },
      Ve = (e) => {
        r.hoveringIndex = e;
      },
      Ne = () => {
        r.hoveringIndex = -1;
      },
      Te = () => {
        var e;
        const t = d.value;
        t && (null == (e = t.focus) || e.call(t));
      },
      Ee = (t) => {
        const l = t.target.value;
        if (
          (Se(l),
          r.displayInputValue.length > 0 && !x.value && (x.value = !0),
          (r.calculatedWidth = k.value.getBoundingClientRect().width),
          e.multiple && be(),
          !e.remote)
        )
          return ue();
        ce();
      },
      Me = (e) => {
        p.value.scrollToItem(e);
      },
      Ie = () => {
        if ((Ne(), e.multiple))
          if (e.modelValue.length > 0) {
            let t = !1;
            ((r.cachedOptions.length = 0),
              (r.previousValue = e.modelValue.toString()));
            for (const l of e.modelValue)
              if (P.value.has(l)) {
                const { index: e, option: a } = P.value.get(l);
                (r.cachedOptions.push(a), t || Ve(e), (t = !0));
              }
          } else ((r.cachedOptions = []), (r.previousValue = void 0));
        else if (V.value) {
          r.previousValue = e.modelValue;
          const t = _.value,
            l = t.findIndex((t) => me(t) === me(e.modelValue));
          ~l
            ? ((r.selectedLabel = t[l].label), Ve(l))
            : (r.selectedLabel = `${e.modelValue}`);
        } else ((r.selectedLabel = ""), (r.previousValue = void 0));
        (ee(), j());
      };
    return (
      ie(x, (e) => {
        var l, a;
        (t("visible-change", e),
          e
            ? null == (a = (l = v.value).update) || a.call(l)
            : ((r.displayInputValue = ""), (r.previousQuery = null), Z("")));
      }),
      ie(
        () => e.modelValue,
        (t, l) => {
          var a;
          ((t && t.toString() === r.previousValue) || Ie(),
            !gl(t, l) &&
              e.validateEvent &&
              (null == (a = null == s ? void 0 : s.validate) ||
                a.call(s, "change").catch((e) => fe())));
        },
        { deep: !0 },
      ),
      ie(
        () => e.options,
        () => {
          const e = d.value;
          (!e || (e && document.activeElement !== e)) && Ie();
        },
        { deep: !0 },
      ),
      ie(_, () => H(p.value.resetScrollTop)),
      ie(
        () => q.value,
        (e) => {
          e || Ne();
        },
      ),
      w(() => {
        Ie();
      }),
      ge(f, ye),
      {
        collapseTagSize: B,
        currentPlaceholder: F,
        expanded: x,
        emptyText: A,
        popupHeight: C,
        debounce: O,
        filteredOptions: _,
        iconComponent: T,
        iconReverse: E,
        inputWrapperStyle: R,
        popperSize: u,
        dropdownMenuVisible: q,
        hasModelValue: V,
        shouldShowPlaceholder: z,
        selectDisabled: S,
        selectSize: $,
        showClearBtn: N,
        states: r,
        tagMaxWidth: D,
        nsSelectV2: a,
        nsInput: n,
        calculatorRef: k,
        controlRef: c,
        inputRef: d,
        menuRef: p,
        popper: v,
        selectRef: f,
        selectionRef: m,
        popperRef: K,
        validateState: M,
        validateIcon: I,
        showTagList: G,
        collapseTagList: X,
        debouncedOnInputChange: ce,
        deleteTag: (l, a) => {
          const { valueKey: n } = e,
            o = e.modelValue.indexOf(Xe(a, n));
          if (o > -1 && !S.value) {
            const l = [
              ...e.modelValue.slice(0, o),
              ...e.modelValue.slice(o + 1),
            ];
            return (
              r.cachedOptions.splice(o, 1),
              pe(l),
              t("remove-tag", Xe(a, n)),
              (r.softFocus = !0),
              Q(a),
              H(ne)
            );
          }
          l.stopPropagation();
        },
        getLabel: (e) => (h(e) ? e.label : e),
        getValueKey: me,
        handleBlur: xe,
        handleClear: () => {
          let l;
          return (
            (l = W(e.modelValue) ? [] : void 0),
            (r.softFocus = !0),
            e.multiple ? (r.cachedOptions = []) : (r.selectedLabel = ""),
            (x.value = !1),
            pe(l),
            t("clear"),
            ee(),
            H(ne)
          );
        },
        handleClickOutside: () => ((x.value = !1), xe()),
        handleDel: (t) => {
          if (0 === r.displayInputValue.length) {
            t.preventDefault();
            const l = e.modelValue.slice();
            (l.pop(), Q(r.cachedOptions.pop()), pe(l));
          }
        },
        handleEsc: () => {
          r.displayInputValue.length > 0 ? Se("") : (x.value = !1);
        },
        handleFocus: (e) => {
          const l = r.isComposing;
          ((r.isComposing = !0),
            r.softFocus ? (r.softFocus = !1) : l || t("focus", e));
        },
        handleMenuEnter: () => (
          (r.inputValue = r.displayInputValue),
          H(() => {
            ~U.value && (Ve(U.value), Me(r.hoveringIndex));
          })
        ),
        handleResize: ye,
        toggleMenu: se,
        scrollTo: Me,
        onInput: Ee,
        onKeyboardNavigate: Ce,
        onKeyboardSelect: () => {
          if (!x.value) return se();
          ~r.hoveringIndex &&
            _.value[r.hoveringIndex] &&
            we(_.value[r.hoveringIndex], r.hoveringIndex, !1);
        },
        onSelect: we,
        onHover: Ve,
        onUpdateInputValue: Se,
        handleCompositionStart: te,
        handleCompositionEnd: ae,
        handleCompositionUpdate: le,
      }
    );
  },
  ho = v({
    name: "ElSelectV2",
    components: { ElSelectMenu: io, ElTag: kl, ElTooltip: Nt, ElIcon: A },
    directives: { ClickOutside: wl, ModelText: we },
    props: lo,
    emits: [ul, dl, "remove-tag", "clear", "visible-change", "focus", "blur"],
    setup(e, { emit: t }) {
      const l = y(() => {
          const { modelValue: t, multiple: l } = e,
            a = l ? [] : void 0;
          return W(t) ? (l ? t : a) : l ? a : t;
        }),
        a = po(re({ ...Qe(e), modelValue: l }), t);
      return (
        Q(ro, {
          props: re({ ...Qe(e), height: a.popupHeight, modelValue: l }),
          popper: a.popper,
          onSelect: a.onSelect,
          onHover: a.onHover,
          onKeyboardNavigate: a.onKeyboardNavigate,
          onKeyboardSelect: a.onKeyboardSelect,
        }),
        { ...a, modelValue: l }
      );
    },
  }),
  vo = { key: 0 },
  fo = [
    "id",
    "autocomplete",
    "aria-expanded",
    "aria-labelledby",
    "disabled",
    "readonly",
    "name",
    "unselectable",
  ],
  mo = ["textContent"],
  go = [
    "id",
    "aria-labelledby",
    "aria-expanded",
    "autocomplete",
    "disabled",
    "name",
    "readonly",
    "unselectable",
  ],
  bo = ["textContent"];
var yo = K(ho, [
  [
    "render",
    function (e, t, l, a, n, o) {
      const s = le("el-tag"),
        r = le("el-tooltip"),
        i = le("el-icon"),
        u = le("el-select-menu"),
        c = Je("model-text"),
        d = Je("click-outside");
      return be(
        (x(),
        O(
          "div",
          {
            ref: "selectRef",
            class: N([e.nsSelectV2.b(), e.nsSelectV2.m(e.selectSize)]),
            onClick:
              t[24] ||
              (t[24] = z(
                (...t) => e.toggleMenu && e.toggleMenu(...t),
                ["stop"],
              )),
            onMouseenter:
              t[25] || (t[25] = (t) => (e.states.comboBoxHovering = !0)),
            onMouseleave:
              t[26] || (t[26] = (t) => (e.states.comboBoxHovering = !1)),
          },
          [
            M(
              r,
              {
                ref: "popper",
                visible: e.dropdownMenuVisible,
                teleported: e.teleported,
                "popper-class": [e.nsSelectV2.e("popper"), e.popperClass],
                "gpu-acceleration": !1,
                "stop-popper-mouse-event": !1,
                "popper-options": e.popperOptions,
                "fallback-placements": [
                  "bottom-start",
                  "top-start",
                  "right",
                  "left",
                ],
                effect: e.effect,
                placement: e.placement,
                pure: "",
                transition: `${e.nsSelectV2.namespace.value}-zoom-in-top`,
                trigger: "click",
                persistent: e.persistent,
                onBeforeShow: e.handleMenuEnter,
                onHide:
                  t[23] ||
                  (t[23] = (t) =>
                    (e.states.inputValue = e.states.displayInputValue)),
              },
              {
                default: C(() => [
                  V(
                    "div",
                    {
                      ref: "selectionRef",
                      class: N([
                        e.nsSelectV2.e("wrapper"),
                        e.nsSelectV2.is(
                          "focused",
                          e.states.isComposing || e.expanded,
                        ),
                        e.nsSelectV2.is("hovering", e.states.comboBoxHovering),
                        e.nsSelectV2.is("filterable", e.filterable),
                        e.nsSelectV2.is("disabled", e.selectDisabled),
                      ]),
                    },
                    [
                      e.$slots.prefix
                        ? (x(), O("div", vo, [$(e.$slots, "prefix")]))
                        : X("v-if", !0),
                      e.multiple
                        ? (x(),
                          O(
                            "div",
                            { key: 1, class: N(e.nsSelectV2.e("selection")) },
                            [
                              e.collapseTags && e.modelValue.length > 0
                                ? (x(),
                                  O(
                                    P,
                                    { key: 0 },
                                    [
                                      (x(!0),
                                      O(
                                        P,
                                        null,
                                        L(
                                          e.showTagList,
                                          (t) => (
                                            x(),
                                            O(
                                              "div",
                                              {
                                                key: e.getValueKey(t),
                                                class: N(
                                                  e.nsSelectV2.e(
                                                    "selected-item",
                                                  ),
                                                ),
                                              },
                                              [
                                                M(
                                                  s,
                                                  {
                                                    closable:
                                                      !e.selectDisabled &&
                                                      !(null == t
                                                        ? void 0
                                                        : t.disable),
                                                    size: e.collapseTagSize,
                                                    type: "info",
                                                    "disable-transitions": "",
                                                    onClose: (l) =>
                                                      e.deleteTag(l, t),
                                                  },
                                                  {
                                                    default: C(() => [
                                                      V(
                                                        "span",
                                                        {
                                                          class: N(
                                                            e.nsSelectV2.e(
                                                              "tags-text",
                                                            ),
                                                          ),
                                                          style: E({
                                                            maxWidth: `${e.tagMaxWidth}px`,
                                                          }),
                                                        },
                                                        D(
                                                          null == t
                                                            ? void 0
                                                            : t.label,
                                                        ),
                                                        7,
                                                      ),
                                                    ]),
                                                    _: 2,
                                                  },
                                                  1032,
                                                  [
                                                    "closable",
                                                    "size",
                                                    "onClose",
                                                  ],
                                                ),
                                              ],
                                              2,
                                            )
                                          ),
                                        ),
                                        128,
                                      )),
                                      V(
                                        "div",
                                        {
                                          class: N(
                                            e.nsSelectV2.e("selected-item"),
                                          ),
                                        },
                                        [
                                          e.modelValue.length >
                                          e.maxCollapseTags
                                            ? (x(),
                                              S(
                                                s,
                                                {
                                                  key: 0,
                                                  closable: !1,
                                                  size: e.collapseTagSize,
                                                  type: "info",
                                                  "disable-transitions": "",
                                                },
                                                {
                                                  default: C(() => [
                                                    e.collapseTagsTooltip
                                                      ? (x(),
                                                        S(
                                                          r,
                                                          {
                                                            key: 0,
                                                            disabled:
                                                              e.dropdownMenuVisible,
                                                            "fallback-placements":
                                                              [
                                                                "bottom",
                                                                "top",
                                                                "right",
                                                                "left",
                                                              ],
                                                            effect: e.effect,
                                                            placement: "bottom",
                                                            teleported: !1,
                                                          },
                                                          {
                                                            default: C(() => [
                                                              V(
                                                                "span",
                                                                {
                                                                  class: N(
                                                                    e.nsSelectV2.e(
                                                                      "tags-text",
                                                                    ),
                                                                  ),
                                                                  style: E({
                                                                    maxWidth: `${e.tagMaxWidth}px`,
                                                                  }),
                                                                },
                                                                "+ " +
                                                                  D(
                                                                    e.modelValue
                                                                      .length -
                                                                      e.maxCollapseTags,
                                                                  ),
                                                                7,
                                                              ),
                                                            ]),
                                                            content: C(() => [
                                                              V(
                                                                "div",
                                                                {
                                                                  class: N(
                                                                    e.nsSelectV2.e(
                                                                      "selection",
                                                                    ),
                                                                  ),
                                                                },
                                                                [
                                                                  (x(!0),
                                                                  O(
                                                                    P,
                                                                    null,
                                                                    L(
                                                                      e.collapseTagList,
                                                                      (t) => (
                                                                        x(),
                                                                        O(
                                                                          "div",
                                                                          {
                                                                            key: e.getValueKey(
                                                                              t,
                                                                            ),
                                                                            class:
                                                                              N(
                                                                                e.nsSelectV2.e(
                                                                                  "selected-item",
                                                                                ),
                                                                              ),
                                                                          },
                                                                          [
                                                                            M(
                                                                              s,
                                                                              {
                                                                                closable:
                                                                                  !e.selectDisabled &&
                                                                                  !t.disabled,
                                                                                size: e.collapseTagSize,
                                                                                class:
                                                                                  "in-tooltip",
                                                                                type: "info",
                                                                                "disable-transitions":
                                                                                  "",
                                                                                onClose:
                                                                                  (
                                                                                    l,
                                                                                  ) =>
                                                                                    e.deleteTag(
                                                                                      l,
                                                                                      t,
                                                                                    ),
                                                                              },
                                                                              {
                                                                                default:
                                                                                  C(
                                                                                    () => [
                                                                                      V(
                                                                                        "span",
                                                                                        {
                                                                                          class:
                                                                                            N(
                                                                                              e.nsSelectV2.e(
                                                                                                "tags-text",
                                                                                              ),
                                                                                            ),
                                                                                          style:
                                                                                            E(
                                                                                              {
                                                                                                maxWidth: `${e.tagMaxWidth}px`,
                                                                                              },
                                                                                            ),
                                                                                        },
                                                                                        D(
                                                                                          e.getLabel(
                                                                                            t,
                                                                                          ),
                                                                                        ),
                                                                                        7,
                                                                                      ),
                                                                                    ],
                                                                                  ),
                                                                                _: 2,
                                                                              },
                                                                              1032,
                                                                              [
                                                                                "closable",
                                                                                "size",
                                                                                "onClose",
                                                                              ],
                                                                            ),
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
                                                            ]),
                                                            _: 1,
                                                          },
                                                          8,
                                                          [
                                                            "disabled",
                                                            "effect",
                                                          ],
                                                        ))
                                                      : (x(),
                                                        O(
                                                          "span",
                                                          {
                                                            key: 1,
                                                            class: N(
                                                              e.nsSelectV2.e(
                                                                "tags-text",
                                                              ),
                                                            ),
                                                            style: E({
                                                              maxWidth: `${e.tagMaxWidth}px`,
                                                            }),
                                                          },
                                                          "+ " +
                                                            D(
                                                              e.modelValue
                                                                .length -
                                                                e.maxCollapseTags,
                                                            ),
                                                          7,
                                                        )),
                                                  ]),
                                                  _: 1,
                                                },
                                                8,
                                                ["size"],
                                              ))
                                            : X("v-if", !0),
                                        ],
                                        2,
                                      ),
                                    ],
                                    64,
                                  ))
                                : (x(!0),
                                  O(
                                    P,
                                    { key: 1 },
                                    L(
                                      e.states.cachedOptions,
                                      (t) => (
                                        x(),
                                        O(
                                          "div",
                                          {
                                            key: e.getValueKey(t),
                                            class: N(
                                              e.nsSelectV2.e("selected-item"),
                                            ),
                                          },
                                          [
                                            M(
                                              s,
                                              {
                                                closable:
                                                  !e.selectDisabled &&
                                                  !t.disabled,
                                                size: e.collapseTagSize,
                                                type: "info",
                                                "disable-transitions": "",
                                                onClose: (l) =>
                                                  e.deleteTag(l, t),
                                              },
                                              {
                                                default: C(() => [
                                                  V(
                                                    "span",
                                                    {
                                                      class: N(
                                                        e.nsSelectV2.e(
                                                          "tags-text",
                                                        ),
                                                      ),
                                                      style: E({
                                                        maxWidth: `${e.tagMaxWidth}px`,
                                                      }),
                                                    },
                                                    D(e.getLabel(t)),
                                                    7,
                                                  ),
                                                ]),
                                                _: 2,
                                              },
                                              1032,
                                              ["closable", "size", "onClose"],
                                            ),
                                          ],
                                          2,
                                        )
                                      ),
                                    ),
                                    128,
                                  )),
                              V(
                                "div",
                                {
                                  class: N([
                                    e.nsSelectV2.e("selected-item"),
                                    e.nsSelectV2.e("input-wrapper"),
                                  ]),
                                  style: E(e.inputWrapperStyle),
                                },
                                [
                                  be(
                                    V(
                                      "input",
                                      {
                                        id: e.id,
                                        ref: "inputRef",
                                        autocomplete: e.autocomplete,
                                        "aria-autocomplete": "list",
                                        "aria-haspopup": "listbox",
                                        autocapitalize: "off",
                                        "aria-expanded": e.expanded,
                                        "aria-labelledby": e.label,
                                        class: N([
                                          e.nsSelectV2.is(e.selectSize),
                                          e.nsSelectV2.e("combobox-input"),
                                        ]),
                                        disabled: e.disabled,
                                        role: "combobox",
                                        readonly: !e.filterable,
                                        spellcheck: "false",
                                        type: "text",
                                        name: e.name,
                                        unselectable: e.expanded
                                          ? "on"
                                          : void 0,
                                        "onUpdate:modelValue":
                                          t[0] ||
                                          (t[0] = (...t) =>
                                            e.onUpdateInputValue &&
                                            e.onUpdateInputValue(...t)),
                                        onFocus:
                                          t[1] ||
                                          (t[1] = (...t) =>
                                            e.handleFocus &&
                                            e.handleFocus(...t)),
                                        onBlur:
                                          t[2] ||
                                          (t[2] = (...t) =>
                                            e.handleBlur && e.handleBlur(...t)),
                                        onInput:
                                          t[3] ||
                                          (t[3] = (...t) =>
                                            e.onInput && e.onInput(...t)),
                                        onCompositionstart:
                                          t[4] ||
                                          (t[4] = (...t) =>
                                            e.handleCompositionStart &&
                                            e.handleCompositionStart(...t)),
                                        onCompositionupdate:
                                          t[5] ||
                                          (t[5] = (...t) =>
                                            e.handleCompositionUpdate &&
                                            e.handleCompositionUpdate(...t)),
                                        onCompositionend:
                                          t[6] ||
                                          (t[6] = (...t) =>
                                            e.handleCompositionEnd &&
                                            e.handleCompositionEnd(...t)),
                                        onKeydown: [
                                          t[7] ||
                                            (t[7] = R(
                                              z(
                                                (t) =>
                                                  e.onKeyboardNavigate(
                                                    "backward",
                                                  ),
                                                ["stop", "prevent"],
                                              ),
                                              ["up"],
                                            )),
                                          t[8] ||
                                            (t[8] = R(
                                              z(
                                                (t) =>
                                                  e.onKeyboardNavigate(
                                                    "forward",
                                                  ),
                                                ["stop", "prevent"],
                                              ),
                                              ["down"],
                                            )),
                                          t[9] ||
                                            (t[9] = R(
                                              z(
                                                (...t) =>
                                                  e.onKeyboardSelect &&
                                                  e.onKeyboardSelect(...t),
                                                ["stop", "prevent"],
                                              ),
                                              ["enter"],
                                            )),
                                          t[10] ||
                                            (t[10] = R(
                                              z(
                                                (...t) =>
                                                  e.handleEsc &&
                                                  e.handleEsc(...t),
                                                ["stop", "prevent"],
                                              ),
                                              ["esc"],
                                            )),
                                          t[11] ||
                                            (t[11] = R(
                                              z(
                                                (...t) =>
                                                  e.handleDel &&
                                                  e.handleDel(...t),
                                                ["stop"],
                                              ),
                                              ["delete"],
                                            )),
                                        ],
                                      },
                                      null,
                                      42,
                                      fo,
                                    ),
                                    [[c, e.states.displayInputValue]],
                                  ),
                                  e.filterable
                                    ? (x(),
                                      O(
                                        "span",
                                        {
                                          key: 0,
                                          ref: "calculatorRef",
                                          "aria-hidden": "true",
                                          class: N(
                                            e.nsSelectV2.e("input-calculator"),
                                          ),
                                          textContent: D(
                                            e.states.displayInputValue,
                                          ),
                                        },
                                        null,
                                        10,
                                        mo,
                                      ))
                                    : X("v-if", !0),
                                ],
                                6,
                              ),
                            ],
                            2,
                          ))
                        : (x(),
                          O(
                            P,
                            { key: 2 },
                            [
                              V(
                                "div",
                                {
                                  class: N([
                                    e.nsSelectV2.e("selected-item"),
                                    e.nsSelectV2.e("input-wrapper"),
                                  ]),
                                },
                                [
                                  be(
                                    V(
                                      "input",
                                      {
                                        id: e.id,
                                        ref: "inputRef",
                                        "aria-autocomplete": "list",
                                        "aria-haspopup": "listbox",
                                        "aria-labelledby": e.label,
                                        "aria-expanded": e.expanded,
                                        autocapitalize: "off",
                                        autocomplete: e.autocomplete,
                                        class: N(
                                          e.nsSelectV2.e("combobox-input"),
                                        ),
                                        disabled: e.disabled,
                                        name: e.name,
                                        role: "combobox",
                                        readonly: !e.filterable,
                                        spellcheck: "false",
                                        type: "text",
                                        unselectable: e.expanded
                                          ? "on"
                                          : void 0,
                                        onCompositionstart:
                                          t[12] ||
                                          (t[12] = (...t) =>
                                            e.handleCompositionStart &&
                                            e.handleCompositionStart(...t)),
                                        onCompositionupdate:
                                          t[13] ||
                                          (t[13] = (...t) =>
                                            e.handleCompositionUpdate &&
                                            e.handleCompositionUpdate(...t)),
                                        onCompositionend:
                                          t[14] ||
                                          (t[14] = (...t) =>
                                            e.handleCompositionEnd &&
                                            e.handleCompositionEnd(...t)),
                                        onFocus:
                                          t[15] ||
                                          (t[15] = (...t) =>
                                            e.handleFocus &&
                                            e.handleFocus(...t)),
                                        onBlur:
                                          t[16] ||
                                          (t[16] = (...t) =>
                                            e.handleBlur && e.handleBlur(...t)),
                                        onInput:
                                          t[17] ||
                                          (t[17] = (...t) =>
                                            e.onInput && e.onInput(...t)),
                                        onKeydown: [
                                          t[18] ||
                                            (t[18] = R(
                                              z(
                                                (t) =>
                                                  e.onKeyboardNavigate(
                                                    "backward",
                                                  ),
                                                ["stop", "prevent"],
                                              ),
                                              ["up"],
                                            )),
                                          t[19] ||
                                            (t[19] = R(
                                              z(
                                                (t) =>
                                                  e.onKeyboardNavigate(
                                                    "forward",
                                                  ),
                                                ["stop", "prevent"],
                                              ),
                                              ["down"],
                                            )),
                                          t[20] ||
                                            (t[20] = R(
                                              z(
                                                (...t) =>
                                                  e.onKeyboardSelect &&
                                                  e.onKeyboardSelect(...t),
                                                ["stop", "prevent"],
                                              ),
                                              ["enter"],
                                            )),
                                          t[21] ||
                                            (t[21] = R(
                                              z(
                                                (...t) =>
                                                  e.handleEsc &&
                                                  e.handleEsc(...t),
                                                ["stop", "prevent"],
                                              ),
                                              ["esc"],
                                            )),
                                        ],
                                        "onUpdate:modelValue":
                                          t[22] ||
                                          (t[22] = (...t) =>
                                            e.onUpdateInputValue &&
                                            e.onUpdateInputValue(...t)),
                                      },
                                      null,
                                      42,
                                      go,
                                    ),
                                    [[c, e.states.displayInputValue]],
                                  ),
                                ],
                                2,
                              ),
                              e.filterable
                                ? (x(),
                                  O(
                                    "span",
                                    {
                                      key: 0,
                                      ref: "calculatorRef",
                                      "aria-hidden": "true",
                                      class: N([
                                        e.nsSelectV2.e("selected-item"),
                                        e.nsSelectV2.e("input-calculator"),
                                      ]),
                                      textContent: D(
                                        e.states.displayInputValue,
                                      ),
                                    },
                                    null,
                                    10,
                                    bo,
                                  ))
                                : X("v-if", !0),
                            ],
                            64,
                          )),
                      e.shouldShowPlaceholder
                        ? (x(),
                          O(
                            "span",
                            {
                              key: 3,
                              class: N([
                                e.nsSelectV2.e("placeholder"),
                                e.nsSelectV2.is(
                                  "transparent",
                                  e.multiple
                                    ? 0 === e.modelValue.length
                                    : !e.hasModelValue,
                                ),
                              ]),
                            },
                            D(e.currentPlaceholder),
                            3,
                          ))
                        : X("v-if", !0),
                      V(
                        "span",
                        { class: N(e.nsSelectV2.e("suffix")) },
                        [
                          e.iconComponent
                            ? be(
                                (x(),
                                S(
                                  i,
                                  {
                                    key: 0,
                                    class: N([
                                      e.nsSelectV2.e("caret"),
                                      e.nsInput.e("icon"),
                                      e.iconReverse,
                                    ]),
                                  },
                                  {
                                    default: C(() => [
                                      (x(), S(He(e.iconComponent))),
                                    ]),
                                    _: 1,
                                  },
                                  8,
                                  ["class"],
                                )),
                                [[Se, !e.showClearBtn]],
                              )
                            : X("v-if", !0),
                          e.showClearBtn && e.clearIcon
                            ? (x(),
                              S(
                                i,
                                {
                                  key: 1,
                                  class: N([
                                    e.nsSelectV2.e("caret"),
                                    e.nsInput.e("icon"),
                                  ]),
                                  onClick: z(e.handleClear, [
                                    "prevent",
                                    "stop",
                                  ]),
                                },
                                {
                                  default: C(() => [(x(), S(He(e.clearIcon)))]),
                                  _: 1,
                                },
                                8,
                                ["class", "onClick"],
                              ))
                            : X("v-if", !0),
                          e.validateState && e.validateIcon
                            ? (x(),
                              S(
                                i,
                                {
                                  key: 2,
                                  class: N([
                                    e.nsInput.e("icon"),
                                    e.nsInput.e("validateIcon"),
                                  ]),
                                },
                                {
                                  default: C(() => [
                                    (x(), S(He(e.validateIcon))),
                                  ]),
                                  _: 1,
                                },
                                8,
                                ["class"],
                              ))
                            : X("v-if", !0),
                        ],
                        2,
                      ),
                    ],
                    2,
                  ),
                ]),
                content: C(() => [
                  M(
                    u,
                    {
                      ref: "menuRef",
                      data: e.filteredOptions,
                      width: e.popperSize,
                      "hovering-index": e.states.hoveringIndex,
                      "scrollbar-always-on": e.scrollbarAlwaysOn,
                    },
                    {
                      default: C((t) => [$(e.$slots, "default", et(tt(t)))]),
                      empty: C(() => [
                        $(e.$slots, "empty", {}, () => [
                          V(
                            "p",
                            { class: N(e.nsSelectV2.e("empty")) },
                            D(e.emptyText ? e.emptyText : ""),
                            3,
                          ),
                        ]),
                      ]),
                      _: 3,
                    },
                    8,
                    ["data", "width", "hovering-index", "scrollbar-always-on"],
                  ),
                ]),
                _: 3,
              },
              8,
              [
                "visible",
                "teleported",
                "popper-class",
                "popper-options",
                "effect",
                "placement",
                "transition",
                "persistent",
                "onBeforeShow",
              ],
            ),
          ],
          34,
        )),
        [[d, e.handleClickOutside, e.popperRef]],
      );
    },
  ],
  [
    "__file",
    "/home/runner/work/element-plus/element-plus/packages/components/select-v2/src/select.vue",
  ],
]);
yo.install = (e) => {
  e.component(yo.name, yo);
};
const ko = yo,
  wo = Symbol("sliderContextKey"),
  xo = u({
    modelValue: { type: c([Number, Array]), default: 0 },
    id: { type: String, default: void 0 },
    min: { type: Number, default: 0 },
    max: { type: Number, default: 100 },
    step: { type: Number, default: 1 },
    showInput: Boolean,
    showInputControls: { type: Boolean, default: !0 },
    size: de,
    inputSize: de,
    showStops: Boolean,
    showTooltip: { type: Boolean, default: !0 },
    formatTooltip: { type: c(Function), default: void 0 },
    disabled: Boolean,
    range: Boolean,
    vertical: Boolean,
    height: String,
    debounce: { type: Number, default: 300 },
    label: { type: String, default: void 0 },
    rangeStartLabel: { type: String, default: void 0 },
    rangeEndLabel: { type: String, default: void 0 },
    formatValueText: { type: c(Function), default: void 0 },
    tooltipClass: { type: String, default: void 0 },
    placement: { type: String, values: Tt, default: "top" },
    marks: { type: c(Object) },
    validateEvent: { type: Boolean, default: !0 },
  }),
  So = (e) => Ae(e) || (W(e) && e.every(Ae)),
  Co = { [ul]: So, [cl]: So, [dl]: So },
  Vo = (e, t, l) => {
    const { form: a, formItem: n } = he(),
      o = Ve(),
      s = b(),
      r = b(),
      i = { firstButton: s, secondButton: r },
      u = y(() => e.disabled || (null == a ? void 0 : a.disabled) || !1),
      c = y(() => Math.min(t.firstValue, t.secondValue)),
      d = y(() => Math.max(t.firstValue, t.secondValue)),
      p = y(() =>
        e.range
          ? (100 * (d.value - c.value)) / (e.max - e.min) + "%"
          : (100 * (t.firstValue - e.min)) / (e.max - e.min) + "%",
      ),
      h = y(() =>
        e.range ? (100 * (c.value - e.min)) / (e.max - e.min) + "%" : "0%",
      ),
      v = y(() => (e.vertical ? { height: e.height } : {})),
      f = y(() =>
        e.vertical
          ? { height: p.value, bottom: h.value }
          : { width: p.value, left: h.value },
      ),
      m = () => {
        o.value &&
          (t.sliderSize =
            o.value["client" + (e.vertical ? "Height" : "Width")]);
      },
      g = (l) => {
        const a = ((l) => {
          const a = e.min + (l * (e.max - e.min)) / 100;
          if (!e.range) return s;
          let n;
          return (
            (n =
              Math.abs(c.value - a) < Math.abs(d.value - a)
                ? t.firstValue < t.secondValue
                  ? "firstButton"
                  : "secondButton"
                : t.firstValue > t.secondValue
                  ? "firstButton"
                  : "secondButton"),
            i[n]
          );
        })(l);
        return (a.value.setPosition(l), a);
      },
      k = (e) => {
        (l(ul, e), l(cl, e));
      },
      w = async () => {
        (await H(), l(dl, e.range ? [c.value, d.value] : e.modelValue));
      },
      x = (l) => {
        var a, n, s, r, i, c;
        if (u.value || t.dragging) return;
        m();
        let d = 0;
        if (e.vertical) {
          const e =
            null !=
            (s =
              null == (n = null == (a = l.touches) ? void 0 : a.item(0))
                ? void 0
                : n.clientY)
              ? s
              : l.clientY;
          d =
            ((o.value.getBoundingClientRect().bottom - e) / t.sliderSize) * 100;
        } else {
          d =
            (((null !=
            (c =
              null == (i = null == (r = l.touches) ? void 0 : r.item(0))
                ? void 0
                : i.clientX)
              ? c
              : l.clientX) -
              o.value.getBoundingClientRect().left) /
              t.sliderSize) *
            100;
        }
        return d < 0 || d > 100 ? void 0 : g(d);
      };
    return {
      elFormItem: n,
      slider: o,
      firstButton: s,
      secondButton: r,
      sliderDisabled: u,
      minValue: c,
      maxValue: d,
      runwayStyle: v,
      barStyle: f,
      resetSize: m,
      setPosition: g,
      emitChange: w,
      onSliderWrapperPrevent: (e) => {
        var t, l;
        ((null == (t = i.firstButton.value) ? void 0 : t.dragging) ||
          (null == (l = i.secondButton.value) ? void 0 : l.dragging)) &&
          e.preventDefault();
      },
      onSliderClick: (e) => {
        x(e) && w();
      },
      onSliderDown: async (e) => {
        const t = x(e);
        t && (await H(), t.value.onButtonDown(e));
      },
      setFirstValue: (l) => {
        ((t.firstValue = l), k(e.range ? [c.value, d.value] : l));
      },
      setSecondValue: (l) => {
        ((t.secondValue = l), e.range && k([c.value, d.value]));
      },
    };
  },
  {
    left: No,
    down: To,
    right: Eo,
    up: Mo,
    home: Io,
    end: Oo,
    pageUp: Ao,
    pageDown: _o,
  } = Z,
  Po = (e, t, l) => {
    const {
        disabled: a,
        min: n,
        max: o,
        step: s,
        showTooltip: r,
        precision: i,
        sliderSize: u,
        formatTooltip: c,
        emitChange: d,
        resetSize: p,
        updateDragging: h,
      } = G(wo),
      {
        tooltip: v,
        tooltipVisible: f,
        formatValue: m,
        displayTooltip: g,
        hideTooltip: k,
      } = ((e, t, l) => {
        const a = b(),
          n = b(!1),
          o = y(() => t.value instanceof Function),
          s = y(() => (o.value && t.value(e.modelValue)) || e.modelValue),
          r = pl(() => {
            l.value && (n.value = !0);
          }, 50),
          i = pl(() => {
            l.value && (n.value = !1);
          }, 50);
        return {
          tooltip: a,
          tooltipVisible: n,
          formatValue: s,
          displayTooltip: r,
          hideTooltip: i,
        };
      })(e, c, r),
      w = b(),
      x = y(() => ((e.modelValue - n.value) / (o.value - n.value)) * 100 + "%"),
      S = y(() => (e.vertical ? { bottom: x.value } : { left: x.value })),
      C = (e) => {
        a.value ||
          ((t.newPosition =
            Number.parseFloat(x.value) + (e / (o.value - n.value)) * 100),
          M(t.newPosition),
          d());
      },
      V = (e) => {
        let t, l;
        return (
          e.type.startsWith("touch")
            ? ((l = e.touches[0].clientY), (t = e.touches[0].clientX))
            : ((l = e.clientY), (t = e.clientX)),
          { clientX: t, clientY: l }
        );
      },
      N = (l) => {
        ((t.dragging = !0), (t.isClick = !0));
        const { clientX: a, clientY: n } = V(l);
        (e.vertical ? (t.startY = n) : (t.startX = a),
          (t.startPosition = Number.parseFloat(x.value)),
          (t.newPosition = t.startPosition));
      },
      T = (l) => {
        if (t.dragging) {
          let a;
          ((t.isClick = !1), g(), p());
          const { clientX: n, clientY: o } = V(l);
          (e.vertical
            ? ((t.currentY = o),
              (a = ((t.startY - t.currentY) / u.value) * 100))
            : ((t.currentX = n),
              (a = ((t.currentX - t.startX) / u.value) * 100)),
            (t.newPosition = t.startPosition + a),
            M(t.newPosition));
        }
      },
      E = () => {
        t.dragging &&
          (setTimeout(() => {
            ((t.dragging = !1),
              t.hovering || k(),
              t.isClick || M(t.newPosition),
              d());
          }, 0),
          window.removeEventListener("mousemove", T),
          window.removeEventListener("touchmove", T),
          window.removeEventListener("mouseup", E),
          window.removeEventListener("touchend", E),
          window.removeEventListener("contextmenu", E));
      },
      M = async (a) => {
        if (null === a || Number.isNaN(+a)) return;
        a < 0 ? (a = 0) : a > 100 && (a = 100);
        const r = 100 / ((o.value - n.value) / s.value);
        let u = Math.round(a / r) * r * (o.value - n.value) * 0.01 + n.value;
        ((u = Number.parseFloat(u.toFixed(i.value))),
          u !== e.modelValue && l(ul, u),
          t.dragging ||
            e.modelValue === t.oldValue ||
            (t.oldValue = e.modelValue),
          await H(),
          t.dragging && g(),
          v.value.updatePopper());
      };
    return (
      ie(
        () => t.dragging,
        (e) => {
          h(e);
        },
      ),
      {
        disabled: a,
        button: w,
        tooltip: v,
        tooltipVisible: f,
        showTooltip: r,
        wrapperStyle: S,
        formatValue: m,
        handleMouseEnter: () => {
          ((t.hovering = !0), g());
        },
        handleMouseLeave: () => {
          ((t.hovering = !1), t.dragging || k());
        },
        onButtonDown: (e) => {
          a.value ||
            (e.preventDefault(),
            N(e),
            window.addEventListener("mousemove", T),
            window.addEventListener("touchmove", T),
            window.addEventListener("mouseup", E),
            window.addEventListener("touchend", E),
            window.addEventListener("contextmenu", E),
            w.value.focus());
        },
        onKeyDown: (e) => {
          let t = !0;
          ([No, To].includes(e.key)
            ? C(-s.value)
            : [Eo, Mo].includes(e.key)
              ? C(s.value)
              : e.key === Io
                ? a.value || (M(0), d())
                : e.key === Oo
                  ? a.value || (M(100), d())
                  : e.key === _o
                    ? C(4 * -s.value)
                    : e.key === Ao
                      ? C(4 * s.value)
                      : (t = !1),
            t && e.preventDefault());
        },
        setPosition: M,
      }
    );
  },
  Lo = u({
    modelValue: { type: Number, default: 0 },
    vertical: Boolean,
    tooltipClass: String,
    placement: { type: String, values: Tt, default: "top" },
  }),
  $o = { [ul]: (e) => Ae(e) },
  Bo = ["tabindex"],
  Do = v({ name: "ElSliderButton" });
var jo = K(
  v({
    ...Do,
    props: Lo,
    emits: $o,
    setup(e, { expose: t, emit: l }) {
      const a = e,
        n = g("slider"),
        o = re({
          hovering: !1,
          dragging: !1,
          isClick: !1,
          startX: 0,
          currentX: 0,
          startY: 0,
          currentY: 0,
          startPosition: 0,
          newPosition: 0,
          oldValue: a.modelValue,
        }),
        {
          disabled: s,
          button: r,
          tooltip: i,
          showTooltip: u,
          tooltipVisible: c,
          wrapperStyle: d,
          formatValue: p,
          handleMouseEnter: h,
          handleMouseLeave: v,
          onButtonDown: f,
          onKeyDown: m,
          setPosition: b,
        } = Po(a, o, l),
        { hovering: y, dragging: k } = Qe(o);
      return (
        t({
          onButtonDown: f,
          onKeyDown: m,
          setPosition: b,
          hovering: y,
          dragging: k,
        }),
        (e, t) => (
          x(),
          O(
            "div",
            {
              ref_key: "button",
              ref: r,
              class: N([
                T(n).e("button-wrapper"),
                { hover: T(y), dragging: T(k) },
              ]),
              style: E(T(d)),
              tabindex: T(s) ? -1 : 0,
              onMouseenter: t[0] || (t[0] = (...e) => T(h) && T(h)(...e)),
              onMouseleave: t[1] || (t[1] = (...e) => T(v) && T(v)(...e)),
              onMousedown: t[2] || (t[2] = (...e) => T(f) && T(f)(...e)),
              onTouchstart: t[3] || (t[3] = (...e) => T(f) && T(f)(...e)),
              onFocus: t[4] || (t[4] = (...e) => T(h) && T(h)(...e)),
              onBlur: t[5] || (t[5] = (...e) => T(v) && T(v)(...e)),
              onKeydown: t[6] || (t[6] = (...e) => T(m) && T(m)(...e)),
            },
            [
              M(
                T(Nt),
                {
                  ref_key: "tooltip",
                  ref: i,
                  visible: T(c),
                  placement: e.placement,
                  "fallback-placements": ["top", "bottom", "right", "left"],
                  "stop-popper-mouse-event": !1,
                  "popper-class": e.tooltipClass,
                  disabled: !T(u),
                  persistent: "",
                },
                {
                  content: C(() => [V("span", null, D(T(p)), 1)]),
                  default: C(() => [
                    V(
                      "div",
                      {
                        class: N([
                          T(n).e("button"),
                          { hover: T(y), dragging: T(k) },
                        ]),
                      },
                      null,
                      2,
                    ),
                  ]),
                  _: 1,
                },
                8,
                ["visible", "placement", "popper-class", "disabled"],
              ),
            ],
            46,
            Bo,
          )
        )
      );
    },
  }),
  [
    [
      "__file",
      "/home/runner/work/element-plus/element-plus/packages/components/slider/src/button.vue",
    ],
  ],
);
const Ro = u({ mark: { type: c([String, Object]), default: void 0 } });
var zo = v({
  name: "ElSliderMarker",
  props: Ro,
  setup(e) {
    const t = g("slider"),
      l = y(() => (p(e.mark) ? e.mark : e.mark.label)),
      a = y(() => (p(e.mark) ? void 0 : e.mark.style));
    return () =>
      J("div", { class: t.e("marks-text"), style: a.value }, l.value);
  },
});
const Fo = ["id", "role", "aria-label", "aria-labelledby"],
  Ko = { key: 1 },
  Ho = v({ name: "ElSlider" });
const Wo = q(
    K(
      v({
        ...Ho,
        props: xo,
        emits: Co,
        setup(e, { expose: t, emit: l }) {
          const a = e,
            n = g("slider"),
            { t: o } = Y(),
            s = re({
              firstValue: 0,
              secondValue: 0,
              oldValue: 0,
              dragging: !1,
              sliderSize: 1,
            }),
            {
              elFormItem: r,
              slider: i,
              firstButton: u,
              secondButton: c,
              sliderDisabled: d,
              minValue: p,
              maxValue: h,
              runwayStyle: v,
              barStyle: f,
              resetSize: m,
              emitChange: k,
              onSliderWrapperPrevent: C,
              onSliderClick: I,
              onSliderDown: A,
              setFirstValue: _,
              setSecondValue: $,
            } = Vo(a, s, l),
            { stops: B, getStopStyle: D } = ((e, t, l, a) => ({
              stops: y(() => {
                if (!e.showStops || e.min > e.max) return [];
                if (0 === e.step) return [];
                const n = (e.max - e.min) / e.step,
                  o = (100 * e.step) / (e.max - e.min),
                  s = Array.from({ length: n - 1 }).map((e, t) => (t + 1) * o);
                return e.range
                  ? s.filter(
                      (t) =>
                        t < (100 * (l.value - e.min)) / (e.max - e.min) ||
                        t > (100 * (a.value - e.min)) / (e.max - e.min),
                    )
                  : s.filter(
                      (l) =>
                        l > (100 * (t.firstValue - e.min)) / (e.max - e.min),
                    );
              }),
              getStopStyle: (t) =>
                e.vertical ? { bottom: `${t}%` } : { left: `${t}%` },
            }))(a, s, p, h),
            { inputId: j, isLabeledByFormItem: R } = Me(a, {
              formItemContext: r,
            }),
            z = ve(),
            F = y(() => a.inputSize || z.value),
            K = y(
              () =>
                a.label ||
                o("el.slider.defaultLabel", { min: a.min, max: a.max }),
            ),
            W = y(() =>
              a.range
                ? a.rangeStartLabel || o("el.slider.defaultRangeStartLabel")
                : K.value,
            ),
            q = y(() =>
              a.formatValueText ? a.formatValueText(ae.value) : `${ae.value}`,
            ),
            G = y(() => a.rangeEndLabel || o("el.slider.defaultRangeEndLabel")),
            Z = y(() =>
              a.formatValueText ? a.formatValueText(ne.value) : `${ne.value}`,
            ),
            J = y(() => [
              n.b(),
              n.m(z.value),
              n.is("vertical", a.vertical),
              { [n.m("with-input")]: a.showInput },
            ]),
            ee = ((e) =>
              y(() =>
                e.marks
                  ? Object.keys(e.marks)
                      .map(Number.parseFloat)
                      .sort((e, t) => e - t)
                      .filter((t) => t <= e.max && t >= e.min)
                      .map((t) => ({
                        point: t,
                        position: (100 * (t - e.min)) / (e.max - e.min),
                        mark: e.marks[t],
                      }))
                  : [],
              ))(a);
          ((e, t, l, a, n, o) => {
            const s = (e) => {
                (n(ul, e), n(cl, e));
              },
              r = () =>
                e.range
                  ? ![l.value, a.value].every((e, l) => e === t.oldValue[l])
                  : e.modelValue !== t.oldValue,
              i = () => {
                var l, a;
                e.min > e.max &&
                  U("Slider", "min should not be greater than max.");
                const n = e.modelValue;
                e.range && Array.isArray(n)
                  ? n[1] < e.min
                    ? s([e.min, e.min])
                    : n[0] > e.max
                      ? s([e.max, e.max])
                      : n[0] < e.min
                        ? s([e.min, n[1]])
                        : n[1] > e.max
                          ? s([n[0], e.max])
                          : ((t.firstValue = n[0]),
                            (t.secondValue = n[1]),
                            r() &&
                              (e.validateEvent &&
                                (null ==
                                  (l = null == o ? void 0 : o.validate) ||
                                  l.call(o, "change").catch((e) => fe())),
                              (t.oldValue = n.slice())))
                  : e.range ||
                    "number" != typeof n ||
                    Number.isNaN(n) ||
                    (n < e.min
                      ? s(e.min)
                      : n > e.max
                        ? s(e.max)
                        : ((t.firstValue = n),
                          r() &&
                            (e.validateEvent &&
                              (null == (a = null == o ? void 0 : o.validate) ||
                                a.call(o, "change").catch((e) => fe())),
                            (t.oldValue = n))));
              };
            (i(),
              ie(
                () => t.dragging,
                (e) => {
                  e || i();
                },
              ),
              ie(
                () => e.modelValue,
                (e, l) => {
                  t.dragging ||
                    (Array.isArray(e) &&
                      Array.isArray(l) &&
                      e.every((e, t) => e === l[t]) &&
                      t.firstValue === e[0] &&
                      t.secondValue === e[1]) ||
                    i();
                },
                { deep: !0 },
              ),
              ie(
                () => [e.min, e.max],
                () => {
                  i();
                },
              ));
          })(a, s, p, h, l, r);
          const te = y(() => {
              const e = [a.min, a.max, a.step].map((e) => {
                const t = `${e}`.split(".")[1];
                return t ? t.length : 0;
              });
              return Math.max.apply(null, e);
            }),
            { sliderWrapper: le } = ((e, t, l) => {
              const a = b();
              return (
                w(async () => {
                  (e.range
                    ? (Array.isArray(e.modelValue)
                        ? ((t.firstValue = Math.max(e.min, e.modelValue[0])),
                          (t.secondValue = Math.min(e.max, e.modelValue[1])))
                        : ((t.firstValue = e.min), (t.secondValue = e.max)),
                      (t.oldValue = [t.firstValue, t.secondValue]))
                    : ("number" != typeof e.modelValue ||
                      Number.isNaN(e.modelValue)
                        ? (t.firstValue = e.min)
                        : (t.firstValue = Math.min(
                            e.max,
                            Math.max(e.min, e.modelValue),
                          )),
                      (t.oldValue = t.firstValue)),
                    lt(window, "resize", l),
                    await H(),
                    l());
                }),
                { sliderWrapper: a }
              );
            })(a, s, m),
            { firstValue: ae, secondValue: ne, sliderSize: oe } = Qe(s);
          return (
            Q(wo, {
              ...Qe(a),
              sliderSize: oe,
              disabled: d,
              precision: te,
              emitChange: k,
              resetSize: m,
              updateDragging: (e) => {
                s.dragging = e;
              },
            }),
            t({ onSliderClick: I }),
            (e, t) => {
              var l, a;
              return (
                x(),
                O(
                  "div",
                  {
                    id: e.range ? T(j) : void 0,
                    ref_key: "sliderWrapper",
                    ref: le,
                    class: N(T(J)),
                    role: e.range ? "group" : void 0,
                    "aria-label": e.range && !T(R) ? T(K) : void 0,
                    "aria-labelledby":
                      e.range && T(R)
                        ? null == (l = T(r))
                          ? void 0
                          : l.labelId
                        : void 0,
                    onTouchstart: t[2] || (t[2] = (...e) => T(C) && T(C)(...e)),
                    onTouchmove: t[3] || (t[3] = (...e) => T(C) && T(C)(...e)),
                  },
                  [
                    V(
                      "div",
                      {
                        ref_key: "slider",
                        ref: i,
                        class: N([
                          T(n).e("runway"),
                          { "show-input": e.showInput && !e.range },
                          T(n).is("disabled", T(d)),
                        ]),
                        style: E(T(v)),
                        onMousedown:
                          t[0] || (t[0] = (...e) => T(A) && T(A)(...e)),
                        onTouchstart:
                          t[1] || (t[1] = (...e) => T(A) && T(A)(...e)),
                      },
                      [
                        V(
                          "div",
                          { class: N(T(n).e("bar")), style: E(T(f)) },
                          null,
                          6,
                        ),
                        M(
                          jo,
                          {
                            id: e.range ? void 0 : T(j),
                            ref_key: "firstButton",
                            ref: u,
                            "model-value": T(ae),
                            vertical: e.vertical,
                            "tooltip-class": e.tooltipClass,
                            placement: e.placement,
                            role: "slider",
                            "aria-label": e.range || !T(R) ? T(W) : void 0,
                            "aria-labelledby":
                              !e.range && T(R)
                                ? null == (a = T(r))
                                  ? void 0
                                  : a.labelId
                                : void 0,
                            "aria-valuemin": e.min,
                            "aria-valuemax": e.range ? T(ne) : e.max,
                            "aria-valuenow": T(ae),
                            "aria-valuetext": T(q),
                            "aria-orientation": e.vertical
                              ? "vertical"
                              : "horizontal",
                            "aria-disabled": T(d),
                            "onUpdate:modelValue": T(_),
                          },
                          null,
                          8,
                          [
                            "id",
                            "model-value",
                            "vertical",
                            "tooltip-class",
                            "placement",
                            "aria-label",
                            "aria-labelledby",
                            "aria-valuemin",
                            "aria-valuemax",
                            "aria-valuenow",
                            "aria-valuetext",
                            "aria-orientation",
                            "aria-disabled",
                            "onUpdate:modelValue",
                          ],
                        ),
                        e.range
                          ? (x(),
                            S(
                              jo,
                              {
                                key: 0,
                                ref_key: "secondButton",
                                ref: c,
                                "model-value": T(ne),
                                vertical: e.vertical,
                                "tooltip-class": e.tooltipClass,
                                placement: e.placement,
                                role: "slider",
                                "aria-label": T(G),
                                "aria-valuemin": T(ae),
                                "aria-valuemax": e.max,
                                "aria-valuenow": T(ne),
                                "aria-valuetext": T(Z),
                                "aria-orientation": e.vertical
                                  ? "vertical"
                                  : "horizontal",
                                "aria-disabled": T(d),
                                "onUpdate:modelValue": T($),
                              },
                              null,
                              8,
                              [
                                "model-value",
                                "vertical",
                                "tooltip-class",
                                "placement",
                                "aria-label",
                                "aria-valuemin",
                                "aria-valuemax",
                                "aria-valuenow",
                                "aria-valuetext",
                                "aria-orientation",
                                "aria-disabled",
                                "onUpdate:modelValue",
                              ],
                            ))
                          : X("v-if", !0),
                        e.showStops
                          ? (x(),
                            O("div", Ko, [
                              (x(!0),
                              O(
                                P,
                                null,
                                L(
                                  T(B),
                                  (e, t) => (
                                    x(),
                                    O(
                                      "div",
                                      {
                                        key: t,
                                        class: N(T(n).e("stop")),
                                        style: E(T(D)(e)),
                                      },
                                      null,
                                      6,
                                    )
                                  ),
                                ),
                                128,
                              )),
                            ]))
                          : X("v-if", !0),
                        T(ee).length > 0
                          ? (x(),
                            O(
                              P,
                              { key: 2 },
                              [
                                V("div", null, [
                                  (x(!0),
                                  O(
                                    P,
                                    null,
                                    L(
                                      T(ee),
                                      (e, t) => (
                                        x(),
                                        O(
                                          "div",
                                          {
                                            key: t,
                                            style: E(T(D)(e.position)),
                                            class: N([
                                              T(n).e("stop"),
                                              T(n).e("marks-stop"),
                                            ]),
                                          },
                                          null,
                                          6,
                                        )
                                      ),
                                    ),
                                    128,
                                  )),
                                ]),
                                V(
                                  "div",
                                  { class: N(T(n).e("marks")) },
                                  [
                                    (x(!0),
                                    O(
                                      P,
                                      null,
                                      L(
                                        T(ee),
                                        (e, t) => (
                                          x(),
                                          S(
                                            T(zo),
                                            {
                                              key: t,
                                              mark: e.mark,
                                              style: E(T(D)(e.position)),
                                            },
                                            null,
                                            8,
                                            ["mark", "style"],
                                          )
                                        ),
                                      ),
                                      128,
                                    )),
                                  ],
                                  2,
                                ),
                              ],
                              64,
                            ))
                          : X("v-if", !0),
                      ],
                      38,
                    ),
                    e.showInput && !e.range
                      ? (x(),
                        S(
                          T(ln),
                          {
                            key: 0,
                            ref: "input",
                            "model-value": T(ae),
                            class: N(T(n).e("input")),
                            step: e.step,
                            disabled: T(d),
                            controls: e.showInputControls,
                            min: e.min,
                            max: e.max,
                            debounce: e.debounce,
                            size: T(F),
                            "onUpdate:modelValue": T(_),
                            onChange: T(k),
                          },
                          null,
                          8,
                          [
                            "model-value",
                            "class",
                            "step",
                            "disabled",
                            "controls",
                            "min",
                            "max",
                            "debounce",
                            "size",
                            "onUpdate:modelValue",
                            "onChange",
                          ],
                        ))
                      : X("v-if", !0),
                  ],
                  42,
                  Fo,
                )
              );
            }
          );
        },
      }),
      [
        [
          "__file",
          "/home/runner/work/element-plus/element-plus/packages/components/slider/src/slider.vue",
        ],
      ],
    ),
  ),
  Uo = u({
    format: { type: String, default: "HH:mm" },
    modelValue: String,
    disabled: Boolean,
    editable: { type: Boolean, default: !0 },
    effect: { type: String, default: "light" },
    clearable: { type: Boolean, default: !0 },
    size: de,
    placeholder: String,
    start: { type: String, default: "09:00" },
    end: { type: String, default: "18:00" },
    step: { type: String, default: "00:30" },
    minTime: String,
    maxTime: String,
    name: String,
    prefixIcon: { type: c([String, Object]), default: () => at },
    clearIcon: { type: c([String, Object]), default: () => ye },
  }),
  qo = (e) => {
    const t = (e || "").split(":");
    if (t.length >= 2) {
      let l = Number.parseInt(t[0], 10);
      const a = Number.parseInt(t[1], 10),
        n = e.toUpperCase();
      return (
        n.includes("AM") && 12 === l
          ? (l = 0)
          : n.includes("PM") && 12 !== l && (l += 12),
        { hours: l, minutes: a }
      );
    }
    return null;
  },
  Yo = (e, t) => {
    const l = qo(e);
    if (!l) return -1;
    const a = qo(t);
    if (!a) return -1;
    const n = l.minutes + 60 * l.hours,
      o = a.minutes + 60 * a.hours;
    return n === o ? 0 : n > o ? 1 : -1;
  },
  Go = (e) => `${e}`.padStart(2, "0"),
  Xo = (e) => `${Go(e.hours)}:${Go(e.minutes)}`,
  Zo = (e, t) => {
    const l = qo(e);
    if (!l) return "";
    const a = qo(t);
    if (!a) return "";
    const n = { hours: l.hours, minutes: l.minutes };
    return (
      (n.minutes += a.minutes),
      (n.hours += a.hours),
      (n.hours += Math.floor(n.minutes / 60)),
      (n.minutes = n.minutes % 60),
      Xo(n)
    );
  },
  Qo = v({ name: "ElTimeSelect" });
var Jo = K(
  v({
    ...Qo,
    props: Uo,
    emits: ["change", "blur", "focus", "update:modelValue"],
    setup(e, { expose: t }) {
      const l = e;
      Rt.extend(Ft);
      const { Option: a } = el,
        n = g("input"),
        o = b(),
        s = m(),
        r = y(() => l.modelValue),
        i = y(() => {
          const e = qo(l.start);
          return e ? Xo(e) : null;
        }),
        u = y(() => {
          const e = qo(l.end);
          return e ? Xo(e) : null;
        }),
        c = y(() => {
          const e = qo(l.step);
          return e ? Xo(e) : null;
        }),
        d = y(() => {
          const e = qo(l.minTime || "");
          return e ? Xo(e) : null;
        }),
        p = y(() => {
          const e = qo(l.maxTime || "");
          return e ? Xo(e) : null;
        }),
        h = y(() => {
          const e = [];
          if (l.start && l.end && l.step) {
            let t,
              a = i.value;
            for (; a && u.value && Yo(a, u.value) <= 0; )
              ((t = Rt(a, "HH:mm").format(l.format)),
                e.push({
                  value: t,
                  disabled:
                    Yo(a, d.value || "-1:-1") <= 0 ||
                    Yo(a, p.value || "100:100") >= 0,
                }),
                (a = Zo(a, c.value)));
          }
          return e;
        });
      return (
        t({
          blur: () => {
            var e, t;
            null == (t = null == (e = o.value) ? void 0 : e.blur) || t.call(e);
          },
          focus: () => {
            var e, t;
            null == (t = null == (e = o.value) ? void 0 : e.focus) || t.call(e);
          },
        }),
        (e, t) => (
          x(),
          S(
            T(el),
            {
              ref_key: "select",
              ref: o,
              "model-value": T(r),
              disabled: T(s),
              clearable: e.clearable,
              "clear-icon": e.clearIcon,
              size: e.size,
              effect: e.effect,
              placeholder: e.placeholder,
              "default-first-option": "",
              filterable: e.editable,
              "onUpdate:modelValue":
                t[0] || (t[0] = (t) => e.$emit("update:modelValue", t)),
              onChange: t[1] || (t[1] = (t) => e.$emit("change", t)),
              onBlur: t[2] || (t[2] = (t) => e.$emit("blur", t)),
              onFocus: t[3] || (t[3] = (t) => e.$emit("focus", t)),
            },
            {
              prefix: C(() => [
                e.prefixIcon
                  ? (x(),
                    S(
                      T(A),
                      { key: 0, class: N(T(n).e("prefix-icon")) },
                      { default: C(() => [(x(), S(He(e.prefixIcon)))]), _: 1 },
                      8,
                      ["class"],
                    ))
                  : X("v-if", !0),
              ]),
              default: C(() => [
                (x(!0),
                O(
                  P,
                  null,
                  L(
                    T(h),
                    (e) => (
                      x(),
                      S(
                        T(a),
                        {
                          key: e.value,
                          label: e.value,
                          value: e.value,
                          disabled: e.disabled,
                        },
                        null,
                        8,
                        ["label", "value", "disabled"],
                      )
                    ),
                  ),
                  128,
                )),
              ]),
              _: 1,
            },
            8,
            [
              "model-value",
              "disabled",
              "clearable",
              "clear-icon",
              "size",
              "effect",
              "placeholder",
              "filterable",
            ],
          )
        )
      );
    },
  }),
  [
    [
      "__file",
      "/home/runner/work/element-plus/element-plus/packages/components/time-select/src/time-select.vue",
    ],
  ],
);
Jo.install = (e) => {
  e.component(Jo.name, Jo);
};
const es = Jo,
  ts = "left-check-change",
  ls = "right-check-change",
  as = u({
    data: { type: c(Array), default: () => [] },
    titles: { type: c(Array), default: () => [] },
    buttonTexts: { type: c(Array), default: () => [] },
    filterPlaceholder: String,
    filterMethod: { type: c(Function) },
    leftDefaultChecked: { type: c(Array), default: () => [] },
    rightDefaultChecked: { type: c(Array), default: () => [] },
    renderContent: { type: c(Function) },
    modelValue: { type: c(Array), default: () => [] },
    format: { type: c(Object), default: () => ({}) },
    filterable: Boolean,
    props: {
      type: c(Object),
      default: () => Be({ label: "label", key: "key", disabled: "disabled" }),
    },
    targetOrder: {
      type: String,
      values: ["original", "push", "unshift"],
      default: "original",
    },
    validateEvent: { type: Boolean, default: !0 },
  }),
  ns = (e, t) => [e, t].every(W) || (W(e) && hl(t)),
  os = {
    [dl]: (e, t, l) => [e, l].every(W) && ["left", "right"].includes(t),
    [ul]: (e) => W(e),
    [ts]: ns,
    [ls]: ns,
  },
  ss = "checked-change",
  rs = u({
    data: as.data,
    optionRender: { type: c(Function) },
    placeholder: String,
    title: String,
    filterable: Boolean,
    format: as.format,
    filterMethod: as.filterMethod,
    defaultChecked: as.leftDefaultChecked,
    props: as.props,
  }),
  is = { [ss]: ns },
  us = (e) => {
    const t = { label: "label", key: "key", disabled: "disabled" };
    return y(() => ({ ...t, ...e.props }));
  },
  cs = v({ name: "ElTransferPanel" });
var ds = K(
  v({
    ...cs,
    props: rs,
    emits: is,
    setup(e, { expose: t, emit: l }) {
      const a = e,
        n = nt(),
        o = ({ option: e }) => e,
        { t: s } = Y(),
        r = g("transfer"),
        i = re({
          checked: [],
          allChecked: !1,
          query: "",
          checkChangeByUser: !0,
        }),
        u = us(a),
        {
          filteredData: c,
          checkedSummary: d,
          isIndeterminate: p,
          handleAllCheckedChange: h,
        } = ((e, t, l) => {
          const a = us(e),
            n = y(() =>
              e.data.filter((l) =>
                oe(e.filterMethod)
                  ? e.filterMethod(t.query, l)
                  : String(l[a.value.label] || l[a.value.key])
                      .toLowerCase()
                      .includes(t.query.toLowerCase()),
              ),
            ),
            o = y(() => n.value.filter((e) => !e[a.value.disabled])),
            s = y(() => {
              const l = t.checked.length,
                a = e.data.length,
                { noChecked: n, hasChecked: o } = e.format;
              return n && o
                ? l > 0
                  ? o
                      .replace(/\${checked}/g, l.toString())
                      .replace(/\${total}/g, a.toString())
                  : n.replace(/\${total}/g, a.toString())
                : `${l}/${a}`;
            }),
            r = y(() => {
              const e = t.checked.length;
              return e > 0 && e < o.value.length;
            }),
            i = () => {
              const e = o.value.map((e) => e[a.value.key]);
              t.allChecked =
                e.length > 0 && e.every((e) => t.checked.includes(e));
            };
          return (
            ie(
              () => t.checked,
              (e, a) => {
                if ((i(), t.checkChangeByUser)) {
                  const t = e
                    .concat(a)
                    .filter((t) => !e.includes(t) || !a.includes(t));
                  l(ss, e, t);
                } else (l(ss, e), (t.checkChangeByUser = !0));
              },
            ),
            ie(o, () => {
              i();
            }),
            ie(
              () => e.data,
              () => {
                const e = [],
                  l = n.value.map((e) => e[a.value.key]);
                (t.checked.forEach((t) => {
                  l.includes(t) && e.push(t);
                }),
                  (t.checkChangeByUser = !1),
                  (t.checked = e));
              },
            ),
            ie(
              () => e.defaultChecked,
              (e, l) => {
                if (l && e.length === l.length && e.every((e) => l.includes(e)))
                  return;
                const n = [],
                  s = o.value.map((e) => e[a.value.key]);
                (e.forEach((e) => {
                  s.includes(e) && n.push(e);
                }),
                  (t.checkChangeByUser = !1),
                  (t.checked = n));
              },
              { immediate: !0 },
            ),
            {
              filteredData: n,
              checkableData: o,
              checkedSummary: s,
              isIndeterminate: r,
              updateAllChecked: i,
              handleAllCheckedChange: (e) => {
                t.checked = e ? o.value.map((e) => e[a.value.key]) : [];
              },
            }
          );
        })(a, i, l),
        v = y(() => !ne(i.query) && ne(c.value)),
        f = y(() => !ne(n.default()[0].children)),
        { checked: m, allChecked: b, query: k } = Qe(i);
      return (
        t({ query: k }),
        (e, t) => (
          x(),
          O(
            "div",
            { class: N(T(r).b("panel")) },
            [
              V(
                "p",
                { class: N(T(r).be("panel", "header")) },
                [
                  M(
                    T(At),
                    {
                      modelValue: T(b),
                      "onUpdate:modelValue":
                        t[0] || (t[0] = (e) => (xe(b) ? (b.value = e) : null)),
                      indeterminate: T(p),
                      "validate-event": !1,
                      onChange: T(h),
                    },
                    {
                      default: C(() => [
                        B(D(e.title) + " ", 1),
                        V("span", null, D(T(d)), 1),
                      ]),
                      _: 1,
                    },
                    8,
                    ["modelValue", "indeterminate", "onChange"],
                  ),
                ],
                2,
              ),
              V(
                "div",
                {
                  class: N([
                    T(r).be("panel", "body"),
                    T(r).is("with-footer", T(f)),
                  ]),
                },
                [
                  e.filterable
                    ? (x(),
                      S(
                        T(Mt),
                        {
                          key: 0,
                          modelValue: T(k),
                          "onUpdate:modelValue":
                            t[1] ||
                            (t[1] = (e) => (xe(k) ? (k.value = e) : null)),
                          class: N(T(r).be("panel", "filter")),
                          size: "default",
                          placeholder: e.placeholder,
                          "prefix-icon": T(ot),
                          clearable: "",
                          "validate-event": !1,
                        },
                        null,
                        8,
                        ["modelValue", "class", "placeholder", "prefix-icon"],
                      ))
                    : X("v-if", !0),
                  be(
                    M(
                      T(_t),
                      {
                        modelValue: T(m),
                        "onUpdate:modelValue":
                          t[2] ||
                          (t[2] = (e) => (xe(m) ? (m.value = e) : null)),
                        "validate-event": !1,
                        class: N([
                          T(r).is("filterable", e.filterable),
                          T(r).be("panel", "list"),
                        ]),
                      },
                      {
                        default: C(() => [
                          (x(!0),
                          O(
                            P,
                            null,
                            L(
                              T(c),
                              (t) => (
                                x(),
                                S(
                                  T(At),
                                  {
                                    key: t[T(u).key],
                                    class: N(T(r).be("panel", "item")),
                                    label: t[T(u).key],
                                    disabled: t[T(u).disabled],
                                    "validate-event": !1,
                                  },
                                  {
                                    default: C(() => {
                                      var l;
                                      return [
                                        M(
                                          o,
                                          {
                                            option:
                                              null == (l = e.optionRender)
                                                ? void 0
                                                : l.call(e, t),
                                          },
                                          null,
                                          8,
                                          ["option"],
                                        ),
                                      ];
                                    }),
                                    _: 2,
                                  },
                                  1032,
                                  ["class", "label", "disabled"],
                                )
                              ),
                            ),
                            128,
                          )),
                        ]),
                        _: 1,
                      },
                      8,
                      ["modelValue", "class"],
                    ),
                    [[Se, !T(v) && !T(ne)(e.data)]],
                  ),
                  be(
                    V(
                      "p",
                      { class: N(T(r).be("panel", "empty")) },
                      D(
                        T(v)
                          ? T(s)("el.transfer.noMatch")
                          : T(s)("el.transfer.noData"),
                      ),
                      3,
                    ),
                    [[Se, T(v) || T(ne)(e.data)]],
                  ),
                ],
                2,
              ),
              T(f)
                ? (x(),
                  O(
                    "p",
                    { key: 0, class: N(T(r).be("panel", "footer")) },
                    [$(e.$slots, "default")],
                    2,
                  ))
                : X("v-if", !0),
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
      "/home/runner/work/element-plus/element-plus/packages/components/transfer/src/transfer-panel.vue",
    ],
  ],
);
const ps = { key: 0 },
  hs = { key: 0 },
  vs = v({ name: "ElTransfer" });
const fs = q(
    K(
      v({
        ...vs,
        props: as,
        emits: os,
        setup(e, { expose: t, emit: l }) {
          const a = e,
            n = nt(),
            { t: o } = Y(),
            s = g("transfer"),
            { formItem: r } = he(),
            i = re({ leftChecked: [], rightChecked: [] }),
            u = us(a),
            { sourceData: c, targetData: d } = ((e) => {
              const t = us(e),
                l = y(() =>
                  e.data.reduce((e, l) => (e[l[t.value.key]] = l) && e, {}),
                );
              return {
                sourceData: y(() =>
                  e.data.filter((l) => !e.modelValue.includes(l[t.value.key])),
                ),
                targetData: y(() =>
                  "original" === e.targetOrder
                    ? e.data.filter((l) =>
                        e.modelValue.includes(l[t.value.key]),
                      )
                    : e.modelValue.reduce((e, t) => {
                        const a = l.value[t];
                        return (a && e.push(a), e);
                      }, []),
                ),
              };
            })(a),
            { onSourceCheckedChange: p, onTargetCheckedChange: h } = ((
              e,
              t,
            ) => ({
              onSourceCheckedChange: (l, a) => {
                ((e.leftChecked = l), a && t(ts, l, a));
              },
              onTargetCheckedChange: (l, a) => {
                ((e.rightChecked = l), a && t(ls, l, a));
              },
            }))(i, l),
            { addToLeft: v, addToRight: f } = ((e, t, l) => {
              const a = us(e),
                n = (e, t, a) => {
                  (l(ul, e), l(dl, e, t, a));
                };
              return {
                addToLeft: () => {
                  const l = e.modelValue.slice();
                  (t.rightChecked.forEach((e) => {
                    const t = l.indexOf(e);
                    t > -1 && l.splice(t, 1);
                  }),
                    n(l, "left", t.rightChecked));
                },
                addToRight: () => {
                  let l = e.modelValue.slice();
                  const o = e.data
                    .filter((l) => {
                      const n = l[a.value.key];
                      return (
                        t.leftChecked.includes(n) && !e.modelValue.includes(n)
                      );
                    })
                    .map((e) => e[a.value.key]);
                  ((l =
                    "unshift" === e.targetOrder ? o.concat(l) : l.concat(o)),
                    "original" === e.targetOrder &&
                      (l = e.data
                        .filter((e) => l.includes(e[a.value.key]))
                        .map((e) => e[a.value.key])),
                    n(l, "right", t.leftChecked));
                },
              };
            })(a, i, l),
            m = b(),
            k = b(),
            w = y(() => 2 === a.buttonTexts.length),
            S = y(() => a.titles[0] || o("el.transfer.titles.0")),
            E = y(() => a.titles[1] || o("el.transfer.titles.1")),
            I = y(
              () => a.filterPlaceholder || o("el.transfer.filterPlaceholder"),
            );
          ie(
            () => a.modelValue,
            () => {
              var e;
              a.validateEvent &&
                (null == (e = null == r ? void 0 : r.validate) ||
                  e.call(r, "change").catch((e) => fe()));
            },
          );
          const _ = y(
            () => (e) =>
              a.renderContent
                ? a.renderContent(J, e)
                : n.default
                  ? n.default({ option: e })
                  : J("span", e[u.value.label] || e[u.value.key]),
          );
          return (
            t({
              clearQuery: (e) => {
                switch (e) {
                  case "left":
                    m.value.query = "";
                    break;
                  case "right":
                    k.value.query = "";
                }
              },
              leftPanel: m,
              rightPanel: k,
            }),
            (e, t) => (
              x(),
              O(
                "div",
                { class: N(T(s).b()) },
                [
                  M(
                    ds,
                    {
                      ref_key: "leftPanel",
                      ref: m,
                      data: T(c),
                      "option-render": T(_),
                      placeholder: T(I),
                      title: T(S),
                      filterable: e.filterable,
                      format: e.format,
                      "filter-method": e.filterMethod,
                      "default-checked": e.leftDefaultChecked,
                      props: a.props,
                      onCheckedChange: T(p),
                    },
                    { default: C(() => [$(e.$slots, "left-footer")]), _: 3 },
                    8,
                    [
                      "data",
                      "option-render",
                      "placeholder",
                      "title",
                      "filterable",
                      "format",
                      "filter-method",
                      "default-checked",
                      "props",
                      "onCheckedChange",
                    ],
                  ),
                  V(
                    "div",
                    { class: N(T(s).e("buttons")) },
                    [
                      M(
                        T(Ie),
                        {
                          type: "primary",
                          class: N([
                            T(s).e("button"),
                            T(s).is("with-texts", T(w)),
                          ]),
                          disabled: T(ne)(i.rightChecked),
                          onClick: T(v),
                        },
                        {
                          default: C(() => [
                            M(T(A), null, {
                              default: C(() => [M(T(st))]),
                              _: 1,
                            }),
                            T(se)(e.buttonTexts[0])
                              ? X("v-if", !0)
                              : (x(), O("span", ps, D(e.buttonTexts[0]), 1)),
                          ]),
                          _: 1,
                        },
                        8,
                        ["class", "disabled", "onClick"],
                      ),
                      M(
                        T(Ie),
                        {
                          type: "primary",
                          class: N([
                            T(s).e("button"),
                            T(s).is("with-texts", T(w)),
                          ]),
                          disabled: T(ne)(i.leftChecked),
                          onClick: T(f),
                        },
                        {
                          default: C(() => [
                            T(se)(e.buttonTexts[1])
                              ? X("v-if", !0)
                              : (x(), O("span", hs, D(e.buttonTexts[1]), 1)),
                            M(T(A), null, {
                              default: C(() => [M(T(te))]),
                              _: 1,
                            }),
                          ]),
                          _: 1,
                        },
                        8,
                        ["class", "disabled", "onClick"],
                      ),
                    ],
                    2,
                  ),
                  M(
                    ds,
                    {
                      ref_key: "rightPanel",
                      ref: k,
                      data: T(d),
                      "option-render": T(_),
                      placeholder: T(I),
                      filterable: e.filterable,
                      format: e.format,
                      "filter-method": e.filterMethod,
                      title: T(E),
                      "default-checked": e.rightDefaultChecked,
                      props: a.props,
                      onCheckedChange: T(h),
                    },
                    { default: C(() => [$(e.$slots, "right-footer")]), _: 3 },
                    8,
                    [
                      "data",
                      "option-render",
                      "placeholder",
                      "filterable",
                      "format",
                      "filter-method",
                      "title",
                      "default-checked",
                      "props",
                      "onCheckedChange",
                    ],
                  ),
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
          "/home/runner/work/element-plus/element-plus/packages/components/transfer/src/transfer.vue",
        ],
      ],
    ),
  ),
  ms = v({
    extends: tl,
    setup(e, t) {
      const l = tl.setup(e, t);
      delete l.selectOptionClick;
      const a = ae().proxy;
      return (
        H(() => {
          l.select.cachedOptions.get(a.value) || l.select.onOptionCreate(a);
        }),
        l
      );
    },
    methods: {
      selectOptionClick() {
        this.$el.parentElement.click();
      },
    },
  });
function gs(e) {
  return e || 0 === e;
}
function bs(e) {
  return Array.isArray(e) && e.length;
}
function ys(e) {
  return Array.isArray(e) ? e : gs(e) ? [e] : [];
}
function ks(e, t, l, a, n) {
  for (let o = 0; o < e.length; o++) {
    const s = e[o];
    if (t(s, o, e, n)) return a ? a(s, o, e, n) : s;
    {
      const e = l(s);
      if (bs(e)) {
        const n = ks(e, t, l, a, s);
        if (n) return n;
      }
    }
  }
}
function ws(e, t, l, a) {
  for (let n = 0; n < e.length; n++) {
    const o = e[n];
    t(o, n, e, a);
    const s = l(o);
    bs(s) && ws(s, t, l, o);
  }
}
const xs = (
  e,
  { attrs: t, slots: l, emit: a },
  { select: n, tree: o, key: s },
) => {
  ie(
    () => e.modelValue,
    () => {
      e.showCheckbox &&
        H(() => {
          const t = o.value;
          t &&
            !gl(t.getCheckedKeys(), ys(e.modelValue)) &&
            t.setCheckedKeys(ys(e.modelValue));
        });
    },
    { immediate: !0, deep: !0 },
  );
  const r = y(() => ({
      value: s.value,
      label: "label",
      children: "children",
      disabled: "disabled",
      isLeaf: "isLeaf",
      ...e.props,
    })),
    i = (e, t) => {
      var l;
      const a = r.value[e];
      return oe(a)
        ? a(t, null == (l = o.value) ? void 0 : l.getNode(i("value", t)))
        : t[a];
    },
    u = ys(e.modelValue)
      .map((t) =>
        ks(
          e.data || [],
          (e) => i("value", e) === t,
          (e) => i("children", e),
          (e, t, l, a) => a && i("value", a),
        ),
      )
      .filter((e) => gs(e)),
    c = y(() => {
      if (!e.renderAfterExpand && !e.lazy) return [];
      const t = [];
      return (
        ws(
          e.data.concat(e.cacheData),
          (e) => {
            const l = i("value", e);
            t.push({
              value: l,
              currentLabel: i("label", e),
              isDisabled: i("disabled", e),
            });
          },
          (e) => i("children", e),
        ),
        t
      );
    }),
    d = y(() => c.value.reduce((e, t) => ({ ...e, [t.value]: t }), {}));
  return {
    ...Pt(Qe(e), Object.keys(sl.props)),
    ...t,
    nodeKey: s,
    expandOnClickNode: y(() => !e.checkStrictly && e.expandOnClickNode),
    defaultExpandedKeys: y(() =>
      e.defaultExpandedKeys ? e.defaultExpandedKeys.concat(u) : u,
    ),
    renderContent: (t, { node: a, data: n, store: o }) =>
      t(
        ms,
        {
          value: i("value", n),
          label: i("label", n),
          disabled: i("disabled", n),
        },
        e.renderContent
          ? () => e.renderContent(t, { node: a, data: n, store: o })
          : l.default
            ? () => l.default({ node: a, data: n, store: o })
            : void 0,
      ),
    filterNodeMethod: (t, l, a) => {
      var n;
      return e.filterNodeMethod
        ? e.filterNodeMethod(t, l, a)
        : !t || (null == (n = i("label", l)) ? void 0 : n.includes(t));
    },
    onNodeClick: (l, a, o) => {
      var s, r, u;
      if (
        (null == (s = t.onNodeClick) || s.call(t, l, a, o),
        !e.showCheckbox || !e.checkOnClickNode)
      )
        if (e.showCheckbox || (!e.checkStrictly && !a.isLeaf))
          e.expandOnClickNode && o.proxy.handleExpandIconClick();
        else if (!i("disabled", l)) {
          const e =
            null == (r = n.value) ? void 0 : r.options.get(i("value", l));
          null == (u = n.value) || u.handleOptionSelect(e);
        }
    },
    onCheck: (l, n) => {
      if (!e.showCheckbox) return;
      const s = i("value", l),
        r = n.checkedKeys,
        u = e.multiple
          ? ys(e.modelValue).filter(
              (e) => e in d.value && !o.value.getNode(e) && !r.includes(e),
            )
          : [],
        c = r.concat(u);
      if (e.checkStrictly) a(ul, e.multiple ? c : c.includes(s) ? s : void 0);
      else if (e.multiple) a(ul, o.value.getCheckedKeys(!0));
      else {
        const t = ks(
            [l],
            (e) => !bs(i("children", e)) && !i("disabled", e),
            (e) => i("children", e),
          ),
          n = t ? i("value", t) : void 0,
          o =
            gs(e.modelValue) &&
            !!ks(
              [l],
              (t) => i("value", t) === e.modelValue,
              (e) => i("children", e),
            );
        a(ul, n === e.modelValue || o ? void 0 : n);
      }
      H(() => {
        var a;
        const n = ys(e.modelValue);
        (o.value.setCheckedKeys(n),
          null == (a = t.onCheck) ||
            a.call(t, l, {
              checkedKeys: o.value.getCheckedKeys(),
              checkedNodes: o.value.getCheckedNodes(),
              halfCheckedKeys: o.value.getHalfCheckedKeys(),
              halfCheckedNodes: o.value.getHalfCheckedNodes(),
            }));
      });
    },
    cacheOptions: c,
  };
};
var Ss = v({
  props: { data: { type: Array, default: () => [] } },
  setup(e) {
    const t = G(ll);
    return (
      ie(
        () => e.data,
        () => {
          var l;
          e.data.forEach((e) => {
            t.cachedOptions.has(e.value) || t.cachedOptions.set(e.value, e);
          });
          const a =
            (null == (l = t.selectWrapper)
              ? void 0
              : l.querySelectorAll("input")) || [];
          Array.from(a).includes(document.activeElement) || t.setSelected();
        },
        { flush: "post", immediate: !0 },
      ),
      () => {}
    );
  },
});
var Cs = K(
  v({
    name: "ElTreeSelect",
    inheritAttrs: !1,
    props: {
      ...el.props,
      ...sl.props,
      cacheData: { type: Array, default: () => [] },
    },
    setup(e, t) {
      const { slots: l, expose: a } = t,
        n = b(),
        o = b(),
        s = y(() => e.nodeKey || e.valueKey || "value"),
        r = ((e, { attrs: t }, { tree: l, key: a }) => {
          const n = g("tree-select"),
            o = {
              ...Pt(Qe(e), Object.keys(el.props)),
              ...t,
              valueKey: a,
              popperClass: y(() => {
                const t = [n.e("popper")];
                return (e.popperClass && t.push(e.popperClass), t.join(" "));
              }),
              filterMethod: (t = "") => {
                (e.filterMethod && e.filterMethod(t),
                  H(() => {
                    var e;
                    null == (e = l.value) || e.filter(t);
                  }));
              },
              onVisibleChange: (l) => {
                var a;
                (null == (a = t.onVisibleChange) || a.call(t, l),
                  e.filterable && l && o.filterMethod());
              },
            };
          return o;
        })(e, t, { select: n, tree: o, key: s }),
        { cacheOptions: i, ...u } = xs(e, t, { select: n, tree: o, key: s }),
        c = re({});
      return (
        a(c),
        w(() => {
          Object.assign(c, {
            ...Pt(o.value, [
              "filter",
              "updateKeyChildren",
              "getCheckedNodes",
              "setCheckedNodes",
              "getCheckedKeys",
              "setCheckedKeys",
              "setChecked",
              "getHalfCheckedNodes",
              "getHalfCheckedKeys",
              "getCurrentKey",
              "getCurrentNode",
              "setCurrentKey",
              "setCurrentNode",
              "getNode",
              "remove",
              "append",
              "insertBefore",
              "insertAfter",
            ]),
            ...Pt(n.value, ["focus", "blur"]),
          });
        }),
        () =>
          J(el, re({ ...r, ref: (e) => (n.value = e) }), {
            ...l,
            default: () => [
              J(Ss, { data: i.value }),
              J(sl, re({ ...u, ref: (e) => (o.value = e) })),
            ],
          })
      );
    },
  }),
  [
    [
      "__file",
      "/home/runner/work/element-plus/element-plus/packages/components/tree-select/src/tree-select.vue",
    ],
  ],
);
Cs.install = (e) => {
  e.component(Cs.name, Cs);
};
const Vs = Cs,
  Ns = (e, t) => e.push.apply(e, t),
  Ts = (e) => e.sort((e, t) => e.i - t.i || e.j - t.j),
  Es = (e) => {
    const t = {};
    let l = 1;
    return (
      e.forEach((e) => {
        ((t[e] = l), (l += 1));
      }),
      t
    );
  };
const Ms = {
    4: [
      [1, 2],
      [2, 3],
    ],
    5: [
      [1, 3],
      [2, 3],
      [2, 4],
    ],
    6: [
      [1, 2],
      [2, 4],
      [4, 5],
    ],
    7: [
      [1, 3],
      [2, 3],
      [4, 5],
      [4, 6],
    ],
    8: [
      [2, 4],
      [4, 6],
    ],
  },
  Is = /^[A-Z\xbf-\xdf][^A-Z\xbf-\xdf]+$/,
  Os = /^[^A-Z\xbf-\xdf]+[A-Z\xbf-\xdf]$/,
  As = /^[A-Z\xbf-\xdf]+$/,
  _s = /^[^a-z\xdf-\xff]+$/,
  Ps = /^[a-z\xdf-\xff]+$/,
  Ls = /^[^A-Z\xbf-\xdf]+$/,
  $s = /[a-z\xdf-\xff]/,
  Bs = /[A-Z\xbf-\xdf]/,
  Ds = /[^A-Za-z\xbf-\xdf]/gi,
  js = /^\d+$/,
  Rs = new Date().getFullYear(),
  zs = { recentYear: /19\d\d|200\d|201\d|202\d/g },
  Fs = [" ", ",", ";", ":", "|", "/", "\\", "_", ".", "-"],
  Ks = Fs.length;
class Hs {
  match({ password: e }) {
    const t = [
        ...this.getMatchesWithoutSeparator(e),
        ...this.getMatchesWithSeparator(e),
      ],
      l = this.filterNoise(t);
    return Ts(l);
  }
  getMatchesWithSeparator(e) {
    const t = [],
      l = /^(\d{1,4})([\s/\\_.-])(\d{1,2})\2(\d{1,4})$/;
    for (let a = 0; a <= Math.abs(e.length - 6); a += 1)
      for (let n = a + 5; n <= a + 9 && !(n >= e.length); n += 1) {
        const o = e.slice(a, +n + 1 || 9e9),
          s = l.exec(o);
        if (null != s) {
          const e = this.mapIntegersToDayMonthYear([
            parseInt(s[1], 10),
            parseInt(s[3], 10),
            parseInt(s[4], 10),
          ]);
          null != e &&
            t.push({
              pattern: "date",
              token: o,
              i: a,
              j: n,
              separator: s[2],
              year: e.year,
              month: e.month,
              day: e.day,
            });
        }
      }
    return t;
  }
  getMatchesWithoutSeparator(e) {
    const t = [],
      l = /^\d{4,8}$/,
      a = (e) => Math.abs(e.year - Rs);
    for (let n = 0; n <= Math.abs(e.length - 4); n += 1)
      for (let o = n + 3; o <= n + 7 && !(o >= e.length); o += 1) {
        const s = e.slice(n, +o + 1 || 9e9);
        if (l.exec(s)) {
          const e = [],
            l = s.length;
          if (
            (Ms[l].forEach(([t, l]) => {
              const a = this.mapIntegersToDayMonthYear([
                parseInt(s.slice(0, t), 10),
                parseInt(s.slice(t, l), 10),
                parseInt(s.slice(l), 10),
              ]);
              null != a && e.push(a);
            }),
            e.length > 0)
          ) {
            let l = e[0],
              r = a(e[0]);
            (e.slice(1).forEach((e) => {
              const t = a(e);
              t < r && ((l = e), (r = t));
            }),
              t.push({
                pattern: "date",
                token: s,
                i: n,
                j: o,
                separator: "",
                year: l.year,
                month: l.month,
                day: l.day,
              }));
          }
        }
      }
    return t;
  }
  filterNoise(e) {
    return e.filter((t) => {
      let l = !1;
      const a = e.length;
      for (let n = 0; n < a; n += 1) {
        const a = e[n];
        if (t !== a && a.i <= t.i && a.j >= t.j) {
          l = !0;
          break;
        }
      }
      return !l;
    });
  }
  mapIntegersToDayMonthYear(e) {
    if (e[1] > 31 || e[1] <= 0) return null;
    let t = 0,
      l = 0,
      a = 0;
    for (let n = 0, o = e.length; n < o; n += 1) {
      const o = e[n];
      if ((o > 99 && o < 1e3) || o > 2050) return null;
      (o > 31 && (l += 1), o > 12 && (t += 1), o <= 0 && (a += 1));
    }
    return l >= 2 || 3 === t || a >= 2 ? null : this.getDayMonth(e);
  }
  getDayMonth(e) {
    const t = [
        [e[2], e.slice(0, 2)],
        [e[0], e.slice(1, 3)],
      ],
      l = t.length;
    for (let a = 0; a < l; a += 1) {
      const [e, l] = t[a];
      if (1e3 <= e && e <= 2050) {
        const t = this.mapIntegersToDayMonth(l);
        return null != t ? { year: e, month: t.month, day: t.day } : null;
      }
    }
    for (let a = 0; a < l; a += 1) {
      const [e, l] = t[a],
        n = this.mapIntegersToDayMonth(l);
      if (null != n)
        return { year: this.twoToFourDigitYear(e), month: n.month, day: n.day };
    }
    return null;
  }
  mapIntegersToDayMonth(e) {
    const t = [e, e.slice().reverse()];
    for (let l = 0; l < t.length; l += 1) {
      const e = t[l],
        a = e[0],
        n = e[1];
      if (a >= 1 && a <= 31 && n >= 1 && n <= 12) return { day: a, month: n };
    }
    return null;
  }
  twoToFourDigitYear(e) {
    return e > 99 ? e : e > 50 ? e + 1900 : e + 2e3;
  }
}
const Ws = new Uint32Array(65536),
  Us = (e, t) => {
    if (e.length < t.length) {
      const l = t;
      ((t = e), (e = l));
    }
    return 0 === t.length
      ? e.length
      : e.length <= 32
        ? ((e, t) => {
            const l = e.length,
              a = t.length,
              n = 1 << (l - 1);
            let o = -1,
              s = 0,
              r = l,
              i = l;
            for (; i--; ) Ws[e.charCodeAt(i)] |= 1 << i;
            for (i = 0; i < a; i++) {
              let e = Ws[t.charCodeAt(i)];
              const l = e | s;
              ((e |= ((e & o) + o) ^ o),
                (s |= ~(e | o)),
                (o &= e),
                s & n && r++,
                o & n && r--,
                (s = (s << 1) | 1),
                (o = (o << 1) | ~(l | s)),
                (s &= l));
            }
            for (i = l; i--; ) Ws[e.charCodeAt(i)] = 0;
            return r;
          })(e, t)
        : ((e, t) => {
            const l = t.length,
              a = e.length,
              n = [],
              o = [],
              s = Math.ceil(l / 32),
              r = Math.ceil(a / 32);
            for (let v = 0; v < s; v++) ((o[v] = -1), (n[v] = 0));
            let i = 0;
            for (; i < r - 1; i++) {
              let s = 0,
                r = -1;
              const u = 32 * i,
                c = Math.min(32, a) + u;
              for (let t = u; t < c; t++) Ws[e.charCodeAt(t)] |= 1 << t;
              for (let e = 0; e < l; e++) {
                const l = Ws[t.charCodeAt(e)],
                  a = (o[(e / 32) | 0] >>> e) & 1,
                  i = (n[(e / 32) | 0] >>> e) & 1,
                  u = l | s,
                  c = ((((l | i) & r) + r) ^ r) | l | i;
                let d = s | ~(c | r),
                  p = r & c;
                ((d >>> 31) ^ a && (o[(e / 32) | 0] ^= 1 << e),
                  (p >>> 31) ^ i && (n[(e / 32) | 0] ^= 1 << e),
                  (d = (d << 1) | a),
                  (p = (p << 1) | i),
                  (r = p | ~(u | d)),
                  (s = d & u));
              }
              for (let t = u; t < c; t++) Ws[e.charCodeAt(t)] = 0;
            }
            let u = 0,
              c = -1;
            const d = 32 * i,
              p = Math.min(32, a - d) + d;
            for (let v = d; v < p; v++) Ws[e.charCodeAt(v)] |= 1 << v;
            let h = a;
            for (let v = 0; v < l; v++) {
              const e = Ws[t.charCodeAt(v)],
                l = (o[(v / 32) | 0] >>> v) & 1,
                s = (n[(v / 32) | 0] >>> v) & 1,
                r = e | u,
                i = ((((e | s) & c) + c) ^ c) | e | s;
              let d = u | ~(i | c),
                p = c & i;
              ((h += (d >>> (a - 1)) & 1),
                (h -= (p >>> (a - 1)) & 1),
                (d >>> 31) ^ l && (o[(v / 32) | 0] ^= 1 << v),
                (p >>> 31) ^ s && (n[(v / 32) | 0] ^= 1 << v),
                (d = (d << 1) | l),
                (p = (p << 1) | s),
                (c = p | ~(r | d)),
                (u = d & r));
            }
            for (let v = d; v < p; v++) Ws[e.charCodeAt(v)] = 0;
            return h;
          })(e, t);
  },
  qs = (e, t, l) => {
    let a = 0;
    const n = Object.keys(t).find((t) => {
      const n = ((e, t, l) => {
        const a = e.length <= t.length,
          n = e.length <= l;
        return a || n ? Math.ceil(e.length / 4) : l;
      })(e, t, l);
      if (Math.abs(e.length - t.length) > n) return !1;
      const o = Us(e, t),
        s = o <= n;
      return (s && (a = o), s);
    });
    return n ? { levenshteinDistance: a, levenshteinDistanceEntry: n } : {};
  };
var Ys = {
    a: ["4", "@"],
    b: ["8"],
    c: ["(", "{", "[", "<"],
    d: ["6", "|)"],
    e: ["3"],
    f: ["#"],
    g: ["6", "9", "&"],
    h: ["#", "|-|"],
    i: ["1", "!", "|"],
    k: ["<", "|<"],
    l: ["!", "1", "|", "7"],
    m: ["^^", "nn", "2n", "/\\\\/\\\\"],
    n: ["//"],
    o: ["0", "()"],
    q: ["9"],
    u: ["|_|"],
    s: ["$", "5"],
    t: ["+", "7"],
    v: ["<", ">", "/"],
    w: ["^/", "uu", "vv", "2u", "2v", "\\\\/\\\\/"],
    x: ["%", "><"],
    z: ["2"],
  },
  Gs = {
    warnings: {
      straightRow: "straightRow",
      keyPattern: "keyPattern",
      simpleRepeat: "simpleRepeat",
      extendedRepeat: "extendedRepeat",
      sequences: "sequences",
      recentYears: "recentYears",
      dates: "dates",
      topTen: "topTen",
      topHundred: "topHundred",
      common: "common",
      similarToCommon: "similarToCommon",
      wordByItself: "wordByItself",
      namesByThemselves: "namesByThemselves",
      commonNames: "commonNames",
      userInputs: "userInputs",
      pwned: "pwned",
    },
    suggestions: {
      l33t: "l33t",
      reverseWords: "reverseWords",
      allUppercase: "allUppercase",
      capitalization: "capitalization",
      dates: "dates",
      recentYears: "recentYears",
      associatedYears: "associatedYears",
      sequences: "sequences",
      repeated: "repeated",
      longerKeyboardPattern: "longerKeyboardPattern",
      anotherWord: "anotherWord",
      useWords: "useWords",
      noNeed: "noNeed",
      pwned: "pwned",
    },
    timeEstimation: {
      ltSecond: "ltSecond",
      second: "second",
      seconds: "seconds",
      minute: "minute",
      minutes: "minutes",
      hour: "hour",
      hours: "hours",
      day: "day",
      days: "days",
      month: "month",
      months: "months",
      year: "year",
      years: "years",
      centuries: "centuries",
    },
  };
class Xs {
  constructor(e = []) {
    ((this.parents = e), (this.children = new Map()));
  }
  addSub(e, ...t) {
    const l = e.charAt(0);
    this.children.has(l) || this.children.set(l, new Xs([...this.parents, l]));
    let a = this.children.get(l);
    for (let n = 1; n < e.length; n += 1) {
      const t = e.charAt(n);
      (a.hasChild(t) || a.addChild(t), (a = a.getChild(t)));
    }
    return ((a.subs = (a.subs || []).concat(t)), this);
  }
  getChild(e) {
    return this.children.get(e);
  }
  isTerminal() {
    return !!this.subs;
  }
  addChild(e) {
    this.hasChild(e) || this.children.set(e, new Xs([...this.parents, e]));
  }
  hasChild(e) {
    return this.children.has(e);
  }
}
var Zs = (e, t) => (
  Object.entries(e).forEach(([e, l]) => {
    l.forEach((l) => {
      t.addSub(l, e);
    });
  }),
  t
);
const Qs = new (class {
  constructor() {
    ((this.matchers = {}),
      (this.l33tTable = Ys),
      (this.trieNodeRoot = Zs(Ys, new Xs())),
      (this.dictionary = { userInputs: [] }),
      (this.rankedDictionaries = {}),
      (this.rankedDictionariesMaxWordSize = {}),
      (this.translations = Gs),
      (this.graphs = {}),
      (this.useLevenshteinDistance = !1),
      (this.levenshteinThreshold = 2),
      (this.l33tMaxSubstitutions = 512),
      (this.maxLength = 256),
      this.setRankedDictionaries());
  }
  setOptions(e = {}) {
    (e.l33tTable &&
      ((this.l33tTable = e.l33tTable),
      (this.trieNodeRoot = Zs(e.l33tTable, new Xs()))),
      e.dictionary &&
        ((this.dictionary = e.dictionary), this.setRankedDictionaries()),
      e.translations && this.setTranslations(e.translations),
      e.graphs && (this.graphs = e.graphs),
      void 0 !== e.useLevenshteinDistance &&
        (this.useLevenshteinDistance = e.useLevenshteinDistance),
      void 0 !== e.levenshteinThreshold &&
        (this.levenshteinThreshold = e.levenshteinThreshold),
      void 0 !== e.l33tMaxSubstitutions &&
        (this.l33tMaxSubstitutions = e.l33tMaxSubstitutions),
      void 0 !== e.maxLength && (this.maxLength = e.maxLength));
  }
  setTranslations(e) {
    if (!this.checkCustomTranslations(e))
      throw new Error("Invalid translations object fallback to keys");
    this.translations = e;
  }
  checkCustomTranslations(e) {
    let t = !0;
    return (
      Object.keys(Gs).forEach((l) => {
        if (l in e) {
          const a = l;
          Object.keys(Gs[a]).forEach((l) => {
            l in e[a] || (t = !1);
          });
        } else t = !1;
      }),
      t
    );
  }
  setRankedDictionaries() {
    const e = {},
      t = {};
    (Object.keys(this.dictionary).forEach((l) => {
      ((e[l] = Es(this.dictionary[l])),
        (t[l] = this.getRankedDictionariesMaxWordSize(this.dictionary[l])));
    }),
      (this.rankedDictionaries = e),
      (this.rankedDictionariesMaxWordSize = t));
  }
  getRankedDictionariesMaxWordSize(e) {
    const t = e.map((e) =>
      "string" != typeof e ? e.toString().length : e.length,
    );
    return 0 === t.length ? 0 : t.reduce((e, t) => Math.max(e, t), -1 / 0);
  }
  buildSanitizedRankedDictionary(e) {
    const t = [];
    return (
      e.forEach((e) => {
        const l = typeof e;
        ("string" !== l && "number" !== l && "boolean" !== l) ||
          t.push(e.toString().toLowerCase());
      }),
      Es(t)
    );
  }
  extendUserInputsDictionary(e) {
    this.dictionary.userInputs || (this.dictionary.userInputs = []);
    const t = [...this.dictionary.userInputs, ...e];
    ((this.rankedDictionaries.userInputs =
      this.buildSanitizedRankedDictionary(t)),
      (this.rankedDictionariesMaxWordSize.userInputs =
        this.getRankedDictionariesMaxWordSize(t)));
  }
  addMatcher(e, t) {
    this.matchers[e] || (this.matchers[e] = t);
  }
})();
class Js {
  constructor(e) {
    this.defaultMatch = e;
  }
  match({ password: e }) {
    const t = e.split("").reverse().join("");
    return this.defaultMatch({ password: t }).map((t) => ({
      ...t,
      token: t.token.split("").reverse().join(""),
      reversed: !0,
      i: e.length - 1 - t.j,
      j: e.length - 1 - t.i,
    }));
  }
}
class er {
  constructor({ substr: e, buffer: t, limit: l, trieRoot: a }) {
    ((this.finalPasswords = []),
      (this.substr = e),
      (this.buffer = t),
      (this.limit = l),
      (this.trieRoot = a));
  }
  getAllPossibleSubsAtIndex(e) {
    const t = [];
    let l = this.trieRoot;
    for (let a = e; a < this.substr.length; a += 1) {
      const e = this.substr.charAt(a);
      if (((l = l.getChild(e)), !l)) break;
      t.push(l);
    }
    return t;
  }
  helper({ onlyFullSub: e, isFullSub: t, index: l, subIndex: a, changes: n }) {
    if (this.finalPasswords.length >= this.limit) return;
    if (l === this.substr.length)
      return void (
        e === t &&
        this.finalPasswords.push({ password: this.buffer.join(""), changes: n })
      );
    const o = [...this.getAllPossibleSubsAtIndex(l)];
    let s = !1;
    for (let r = l + o.length - 1; r >= l; r -= 1) {
      const i = o[r - l];
      if (i.isTerminal()) {
        s = !0;
        const l = i.subs;
        for (const o of l) {
          this.buffer.push(o);
          const l = n.concat({
            i: a,
            letter: o,
            substitution: i.parents.join(""),
          });
          if (
            (this.helper({
              onlyFullSub: e,
              isFullSub: t,
              index: r + 1,
              subIndex: a + o.length,
              changes: l,
            }),
            this.buffer.pop(),
            this.finalPasswords.length >= this.limit)
          )
            return;
        }
      }
    }
    if (!e || !s) {
      const o = this.substr.charAt(l);
      (this.buffer.push(o),
        this.helper({
          onlyFullSub: e,
          isFullSub: t && !s,
          index: l + 1,
          subIndex: a + 1,
          changes: n,
        }),
        this.buffer.pop());
    }
  }
  getAll() {
    return (
      this.helper({
        onlyFullSub: !0,
        isFullSub: !0,
        index: 0,
        subIndex: 0,
        changes: [],
      }),
      this.helper({
        onlyFullSub: !1,
        isFullSub: !0,
        index: 0,
        subIndex: 0,
        changes: [],
      }),
      this.finalPasswords
    );
  }
}
class tr {
  constructor(e) {
    this.defaultMatch = e;
  }
  isAlreadyIncluded(e, t) {
    return e.some((e) =>
      Object.entries(e).every(([e, l]) => "subs" === e || l === t[e]),
    );
  }
  match({ password: e }) {
    const t = [],
      l =
        ((a = e),
        (n = Qs.l33tMaxSubstitutions),
        (o = Qs.trieNodeRoot),
        new er({ substr: a, buffer: [], limit: n, trieRoot: o }).getAll());
    var a, n, o;
    let s = !1,
      r = !0;
    return (
      l.forEach((l) => {
        if (s) return;
        const a = this.defaultMatch({
          password: l.password,
          useLevenshtein: r,
        });
        ((r = !1),
          a.forEach((a) => {
            s || (s = 0 === a.i && a.j === e.length - 1);
            const n = ((e, t, l) => {
                const a = e.changes
                    .filter((e) => e.i < t)
                    .reduce(
                      (e, t) => e - t.letter.length + t.substitution.length,
                      t,
                    ),
                  n = e.changes.filter((e) => e.i >= t && e.i <= l),
                  o = n.reduce(
                    (e, t) => e - t.letter.length + t.substitution.length,
                    l - t + a,
                  ),
                  s = [],
                  r = [];
                return (
                  n.forEach((e) => {
                    s.findIndex(
                      (t) =>
                        t.letter === e.letter &&
                        t.substitution === e.substitution,
                    ) < 0 &&
                      (s.push({
                        letter: e.letter,
                        substitution: e.substitution,
                      }),
                      r.push(`${e.substitution} -> ${e.letter}`));
                  }),
                  { i: a, j: o, subs: s, subDisplay: r.join(", ") }
                );
              })(l, a.i, a.j),
              o = e.slice(n.i, +n.j + 1 || 9e9),
              r = { ...a, l33t: !0, token: o, ...n },
              i = this.isAlreadyIncluded(t, r);
            o.toLowerCase() === a.matchedWord || i || t.push(r);
          }));
      }),
      t.filter((e) => e.token.length > 1)
    );
  }
}
class lr {
  constructor() {
    ((this.l33t = new tr(this.defaultMatch)),
      (this.reverse = new Js(this.defaultMatch)));
  }
  match({ password: e }) {
    const t = [
      ...this.defaultMatch({ password: e }),
      ...this.reverse.match({ password: e }),
      ...this.l33t.match({ password: e }),
    ];
    return Ts(t);
  }
  defaultMatch({ password: e, useLevenshtein: t = !0 }) {
    const l = [],
      a = e.length,
      n = e.toLowerCase();
    return (
      Object.keys(Qs.rankedDictionaries).forEach((o) => {
        const s = Qs.rankedDictionaries[o],
          r = Qs.rankedDictionariesMaxWordSize[o],
          i = Math.min(r, a);
        for (let u = 0; u < a; u += 1) {
          const r = Math.min(u + i, a);
          for (let i = u; i < r; i += 1) {
            const r = n.slice(u, +i + 1 || 9e9),
              c = r in s;
            let d = {};
            const p = 0 === u && i === a - 1;
            Qs.useLevenshteinDistance &&
              p &&
              !c &&
              t &&
              (d = qs(r, s, Qs.levenshteinThreshold));
            const h = 0 !== Object.keys(d).length;
            if (c || h) {
              const t = s[h ? d.levenshteinDistanceEntry : r];
              l.push({
                pattern: "dictionary",
                i: u,
                j: i,
                token: e.slice(u, +i + 1 || 9e9),
                matchedWord: r,
                rank: t,
                dictionaryName: o,
                reversed: !1,
                l33t: !1,
                ...d,
              });
            }
          }
        }
      }),
      l
    );
  }
}
class ar {
  match({ password: e, regexes: t = zs }) {
    const l = [];
    return (
      Object.keys(t).forEach((a) => {
        const n = t[a];
        let o;
        for (n.lastIndex = 0; (o = n.exec(e)); )
          if (o) {
            const e = o[0];
            l.push({
              pattern: "regex",
              token: e,
              i: o.index,
              j: o.index + o[0].length - 1,
              regexName: a,
              regexMatch: o,
            });
          }
      }),
      Ts(l)
    );
  }
}
var nr = {
  nCk(e, t) {
    let l = e;
    if (t > l) return 0;
    if (0 === t) return 1;
    let a = 1;
    for (let n = 1; n <= t; n += 1) ((a *= l), (a /= n), (l -= 1));
    return a;
  },
  log10: (e) => (0 === e ? 0 : Math.log(e) / Math.log(10)),
  log2: (e) => Math.log(e) / Math.log(2),
  factorial(e) {
    let t = 1;
    for (let l = 2; l <= e; l += 1) t *= l;
    return t;
  },
};
var or = (e) => {
  const t = e.replace(Ds, "");
  if (t.match(Ls) || t.toLowerCase() === t) return 1;
  const l = [Is, Os, _s],
    a = l.length;
  for (let n = 0; n < a; n += 1) {
    const e = l[n];
    if (t.match(e)) return 2;
  }
  return ((e) => {
    const t = e.split(""),
      l = t.filter((e) => e.match(Bs)).length,
      a = t.filter((e) => e.match($s)).length;
    let n = 0;
    const o = Math.min(l, a);
    for (let s = 1; s <= o; s += 1) n += nr.nCk(l + a, s);
    return n;
  })(t);
};
const sr = (e, t) => {
  let l = 0,
    a = e.indexOf(t);
  for (; a >= 0; ) ((l += 1), (a = e.indexOf(t, a + t.length)));
  return l;
};
var rr = ({ l33t: e, subs: t, token: l }) => {
  if (!e) return 1;
  let a = 1;
  return (
    t.forEach((e) => {
      const { subbedCount: t, unsubbedCount: n } = (({ sub: e, token: t }) => {
        const l = t.toLowerCase();
        return {
          subbedCount: sr(l, e.substitution),
          unsubbedCount: sr(l, e.letter),
        };
      })({ sub: e, token: l });
      if (0 === t || 0 === n) a *= 2;
      else {
        const e = Math.min(n, t);
        let l = 0;
        for (let a = 1; a <= e; a += 1) l += nr.nCk(n + t, a);
        a *= l;
      }
    }),
    a
  );
};
const ir = ({ token: e, graph: t, turns: l }) => {
  const a = Object.keys(Qs.graphs[t]).length,
    n = ((e) => {
      let t = 0;
      return (
        Object.keys(e).forEach((l) => {
          const a = e[l];
          t += a.filter((e) => !!e).length;
        }),
        (t /= Object.entries(e).length),
        t
      );
    })(Qs.graphs[t]);
  let o = 0;
  const s = e.length;
  for (let r = 2; r <= s; r += 1) {
    const e = Math.min(l, r - 1);
    for (let t = 1; t <= e; t += 1) o += nr.nCk(r - 1, t - 1) * a * n ** t;
  }
  return o;
};
const ur = {
  bruteforce: ({ token: e }) => {
    let t,
      l = 10 ** e.length;
    return (
      l === Number.POSITIVE_INFINITY && (l = Number.MAX_VALUE),
      (t = 1 === e.length ? 11 : 51),
      Math.max(l, t)
    );
  },
  date: ({ year: e, separator: t }) => {
    let l = 365 * Math.max(Math.abs(e - Rs), 20);
    return (t && (l *= 4), l);
  },
  dictionary: ({
    rank: e,
    reversed: t,
    l33t: l,
    subs: a,
    token: n,
    dictionaryName: o,
  }) => {
    const s = e,
      r = or(n),
      i = rr({ l33t: l, subs: a, token: n });
    let u;
    return (
      (u = "diceware" === o ? 3888 : s * r * i * (t ? 2 : 1)),
      {
        baseGuesses: s,
        uppercaseVariations: r,
        l33tVariations: i,
        calculation: u,
      }
    );
  },
  regex: ({ regexName: e, regexMatch: t, token: l }) => {
    const a = {
      alphaLower: 26,
      alphaUpper: 26,
      alpha: 52,
      alphanumeric: 62,
      digits: 10,
      symbols: 33,
    };
    return e in a
      ? a[e] ** l.length
      : "recentYear" === e
        ? Math.max(Math.abs(parseInt(t[0], 10) - Rs), 20)
        : 0;
  },
  repeat: ({ baseGuesses: e, repeatCount: t }) => e * t,
  sequence: ({ token: e, ascending: t }) => {
    const l = e.charAt(0);
    let a = 0;
    return (
      (a = ["a", "A", "z", "Z", "0", "1", "9"].includes(l)
        ? 4
        : l.match(/\d/)
          ? 10
          : 26),
      t || (a *= 2),
      a * e.length
    );
  },
  spatial: ({ graph: e, token: t, shiftedCount: l, turns: a }) => {
    let n = ir({ token: t, graph: e, turns: a });
    if (l) {
      const e = t.length - l;
      if (0 === l || 0 === e) n *= 2;
      else {
        let t = 0;
        for (let a = 1; a <= Math.min(l, e); a += 1) t += nr.nCk(l + e, a);
        n *= t;
      }
    }
    return Math.round(n);
  },
  separator: () => Ks,
};
var cr = (e, t) => {
  const l = {};
  if ("guesses" in e && null != e.guesses) return e;
  const a = ((e, t) => {
      let l = 1;
      return (
        e.token.length < t.length && (l = 1 === e.token.length ? 10 : 50),
        l
      );
    })(e, t),
    n = ((e, t) =>
      ur[e]
        ? ur[e](t)
        : Qs.matchers[e] && "scoring" in Qs.matchers[e]
          ? Qs.matchers[e].scoring(t)
          : 0)(e.pattern, e);
  let o = 0;
  "number" == typeof n
    ? (o = n)
    : "dictionary" === e.pattern &&
      ((o = n.calculation),
      (l.baseGuesses = n.baseGuesses),
      (l.uppercaseVariations = n.uppercaseVariations),
      (l.l33tVariations = n.l33tVariations));
  const s = Math.max(o, a);
  return { ...e, ...l, guesses: s, guessesLog10: nr.log10(s) };
};
const dr = {
  password: "",
  optimal: {},
  excludeAdditive: !1,
  separatorRegex: void 0,
  fillArray(e, t) {
    const l = [];
    for (let a = 0; a < e; a += 1) {
      let e = [];
      ("object" === t && (e = {}), l.push(e));
    }
    return l;
  },
  makeBruteforceMatch(e, t) {
    return {
      pattern: "bruteforce",
      token: this.password.slice(e, +t + 1 || 9e9),
      i: e,
      j: t,
    };
  },
  update(e, t) {
    const l = e.j,
      a = cr(e, this.password);
    let n = a.guesses;
    t > 1 && (n *= this.optimal.pi[a.i - 1][t - 1]);
    let o = nr.factorial(t) * n;
    this.excludeAdditive || (o += 1e4 ** (t - 1));
    let s = !1;
    (Object.keys(this.optimal.g[l]).forEach((e) => {
      const a = this.optimal.g[l][e];
      parseInt(e, 10) <= t && a <= o && (s = !0);
    }),
      s ||
        ((this.optimal.g[l][t] = o),
        (this.optimal.m[l][t] = a),
        (this.optimal.pi[l][t] = n)));
  },
  bruteforceUpdate(e) {
    let t = this.makeBruteforceMatch(0, e);
    this.update(t, 1);
    for (let l = 1; l <= e; l += 1) {
      t = this.makeBruteforceMatch(l, e);
      const a = this.optimal.m[l - 1];
      Object.keys(a).forEach((e) => {
        "bruteforce" !== a[e].pattern && this.update(t, parseInt(e, 10) + 1);
      });
    }
  },
  unwind(e) {
    const t = [];
    let l = e - 1,
      a = 0,
      n = 1 / 0;
    const o = this.optimal.g[l];
    for (
      o &&
      Object.keys(o).forEach((e) => {
        const t = o[e];
        t < n && ((a = parseInt(e, 10)), (n = t));
      });
      l >= 0;
    ) {
      const e = this.optimal.m[l][a];
      (t.unshift(e), (l = e.i - 1), (a -= 1));
    }
    return t;
  },
};
var pr = {
  mostGuessableMatchSequence(e, t, l = !1) {
    ((dr.password = e), (dr.excludeAdditive = l));
    const a = e.length;
    let n = dr.fillArray(a, "array");
    (t.forEach((e) => {
      n[e.j].push(e);
    }),
      (n = n.map((e) => e.sort((e, t) => e.i - t.i))),
      (dr.optimal = {
        m: dr.fillArray(a, "object"),
        pi: dr.fillArray(a, "object"),
        g: dr.fillArray(a, "object"),
      }));
    for (let i = 0; i < a; i += 1)
      (n[i].forEach((e) => {
        e.i > 0
          ? Object.keys(dr.optimal.m[e.i - 1]).forEach((t) => {
              dr.update(e, parseInt(t, 10) + 1);
            })
          : dr.update(e, 1);
      }),
        dr.bruteforceUpdate(i));
    const o = dr.unwind(a),
      s = o.length,
      r = this.getGuesses(e, s);
    return { password: e, guesses: r, guessesLog10: nr.log10(r), sequence: o };
  },
  getGuesses(e, t) {
    const l = e.length;
    let a = 0;
    return ((a = 0 === e.length ? 1 : dr.optimal.g[l - 1][t]), a);
  },
};
function hr({ isLazy: e = !1, isAnchored: t = !1, flags: l = "" }) {
  return new RegExp(`${t ? "^" : ""}(.+${e ? "?" : ""})\\1+${t ? "$" : ""}`, l);
}
class vr {
  match({ password: e, omniMatch: t }) {
    const l = [];
    let a = 0;
    for (; a < e.length; ) {
      const n = this.getGreedyMatch(e, a),
        o = this.getLazyMatch(e, a);
      if (null == n) break;
      const { match: s, baseToken: r } = this.setMatchToken(n, o);
      if (s) {
        const e = s.index + s[0].length - 1,
          n = this.getBaseGuesses(r, t);
        (l.push(this.normalizeMatch(r, e, s, n)), (a = e + 1));
      }
    }
    return l.some((e) => e instanceof Promise) ? Promise.all(l) : l;
  }
  normalizeMatch(e, t, l, a) {
    const n = {
      pattern: "repeat",
      i: l.index,
      j: t,
      token: l[0],
      baseToken: e,
      baseGuesses: 0,
      repeatCount: l[0].length / e.length,
    };
    return a instanceof Promise
      ? a.then((e) => ({ ...n, baseGuesses: e }))
      : { ...n, baseGuesses: a };
  }
  getGreedyMatch(e, t) {
    const l = hr({ isLazy: !1, flags: "g" });
    return ((l.lastIndex = t), l.exec(e));
  }
  getLazyMatch(e, t) {
    const l = hr({ isLazy: !0, flags: "g" });
    return ((l.lastIndex = t), l.exec(e));
  }
  setMatchToken(e, t) {
    const l = hr({ isLazy: !0, isAnchored: !0 });
    let a,
      n = "";
    if (t && e[0].length > t[0].length) {
      a = e;
      const t = l.exec(a[0]);
      t && (n = t[1]);
    } else ((a = t), a && (n = a[1]));
    return { match: a, baseToken: n };
  }
  getBaseGuesses(e, t) {
    const l = t.match(e);
    if (l instanceof Promise)
      return l.then((t) => pr.mostGuessableMatchSequence(e, t).guesses);
    return pr.mostGuessableMatchSequence(e, l).guesses;
  }
}
class fr {
  constructor() {
    this.MAX_DELTA = 5;
  }
  match({ password: e }) {
    const t = [];
    if (1 === e.length) return [];
    let l = 0,
      a = null;
    const n = e.length;
    for (let o = 1; o < n; o += 1) {
      const n = e.charCodeAt(o) - e.charCodeAt(o - 1);
      if ((null == a && (a = n), n !== a)) {
        const s = o - 1;
        (this.update({ i: l, j: s, delta: a, password: e, result: t }),
          (l = s),
          (a = n));
      }
    }
    return (
      this.update({ i: l, j: n - 1, delta: a, password: e, result: t }),
      t
    );
  }
  update({ i: e, j: t, delta: l, password: a, result: n }) {
    if (t - e > 1 || 1 === Math.abs(l)) {
      const o = Math.abs(l);
      if (o > 0 && o <= this.MAX_DELTA) {
        const o = a.slice(e, +t + 1 || 9e9),
          { sequenceName: s, sequenceSpace: r } = this.getSequence(o);
        return n.push({
          pattern: "sequence",
          i: e,
          j: t,
          token: a.slice(e, +t + 1 || 9e9),
          sequenceName: s,
          sequenceSpace: r,
          ascending: l > 0,
        });
      }
    }
    return null;
  }
  getSequence(e) {
    let t = "unicode",
      l = 26;
    return (
      Ps.test(e)
        ? ((t = "lower"), (l = 26))
        : As.test(e)
          ? ((t = "upper"), (l = 26))
          : js.test(e) && ((t = "digits"), (l = 10)),
      { sequenceName: t, sequenceSpace: l }
    );
  }
}
class mr {
  constructor() {
    this.SHIFTED_RX = /[~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?]/;
  }
  match({ password: e }) {
    const t = [];
    return (
      Object.keys(Qs.graphs).forEach((l) => {
        const a = Qs.graphs[l];
        Ns(t, this.helper(e, a, l));
      }),
      Ts(t)
    );
  }
  checkIfShifted(e, t, l) {
    return !e.includes("keypad") && this.SHIFTED_RX.test(t.charAt(l)) ? 1 : 0;
  }
  helper(e, t, l) {
    let a;
    const n = [];
    let o = 0;
    const s = e.length;
    for (; o < s - 1; ) {
      let r = o + 1,
        i = null,
        u = 0;
      for (a = this.checkIfShifted(l, e, o); ; ) {
        const c = t[e.charAt(r - 1)] || [];
        let d = !1,
          p = -1,
          h = -1;
        if (r < s) {
          const t = e.charAt(r),
            l = c.length;
          for (let e = 0; e < l; e += 1) {
            const l = c[e];
            if (((h += 1), l)) {
              const e = l.indexOf(t);
              if (-1 !== e) {
                ((d = !0),
                  (p = h),
                  1 === e && (a += 1),
                  i !== p && ((u += 1), (i = p)));
                break;
              }
            }
          }
        }
        if (!d) {
          (r - o > 2 &&
            n.push({
              pattern: "spatial",
              i: o,
              j: r - 1,
              token: e.slice(o, r),
              graph: l,
              turns: u,
              shiftedCount: a,
            }),
            (o = r));
          break;
        }
        r += 1;
      }
    }
    return n;
  }
}
const gr = new RegExp(`[${Fs.join("")}]`);
class br {
  static getMostUsedSeparatorChar(e) {
    const t = [
      ...e
        .split("")
        .filter((e) => gr.test(e))
        .reduce((e, t) => {
          const l = e.get(t);
          return (l ? e.set(t, l + 1) : e.set(t, 1), e);
        }, new Map())
        .entries(),
    ].sort(([e, t], [l, a]) => a - t);
    if (!t.length) return;
    const l = t[0];
    return l[1] < 2 ? void 0 : l[0];
  }
  static getSeparatorRegex(e) {
    return new RegExp(`([^${e}\n])(${e})(?!${e})`, "g");
  }
  match({ password: e }) {
    const t = [];
    if (0 === e.length) return t;
    const l = br.getMostUsedSeparatorChar(e);
    if (void 0 === l) return t;
    const a = br.getSeparatorRegex(l);
    for (const n of e.matchAll(a)) {
      if (void 0 === n.index) continue;
      const e = n.index + 1;
      t.push({ pattern: "separator", token: l, i: e, j: e });
    }
    return t;
  }
}
class yr {
  constructor() {
    this.matchers = {
      date: Hs,
      dictionary: lr,
      regex: ar,
      repeat: vr,
      sequence: fr,
      spatial: mr,
      separator: br,
    };
  }
  match(e) {
    const t = [],
      l = [];
    return (
      [...Object.keys(this.matchers), ...Object.keys(Qs.matchers)].forEach(
        (a) => {
          if (!this.matchers[a] && !Qs.matchers[a]) return;
          const n = new (this.matchers[a]
            ? this.matchers[a]
            : Qs.matchers[a].Matching)().match({
            password: e,
            omniMatch: this,
          });
          n instanceof Promise
            ? (n.then((e) => {
                Ns(t, e);
              }),
              l.push(n))
            : Ns(t, n);
        },
      ),
      l.length > 0
        ? new Promise((e, a) => {
            Promise.all(l)
              .then(() => {
                e(Ts(t));
              })
              .catch((e) => {
                a(e);
              });
          })
        : Ts(t)
    );
  }
}
const kr = 2678400,
  wr = 32140800,
  xr = {
    second: 1,
    minute: 60,
    hour: 3600,
    day: 86400,
    month: kr,
    year: wr,
    century: 321408e4,
  };
class Sr {
  translate(e, t) {
    let l = e;
    void 0 !== t && 1 !== t && (l += "s");
    const { timeEstimation: a } = Qs.translations;
    return a[l].replace("{base}", `${t}`);
  }
  estimateAttackTimes(e) {
    const t = {
        onlineThrottling100PerHour: e / (100 / 3600),
        onlineNoThrottling10PerSecond: e / 10,
        offlineSlowHashing1e4PerSecond: e / 1e4,
        offlineFastHashing1e10PerSecond: e / 1e10,
      },
      l = {
        onlineThrottling100PerHour: "",
        onlineNoThrottling10PerSecond: "",
        offlineSlowHashing1e4PerSecond: "",
        offlineFastHashing1e10PerSecond: "",
      };
    return (
      Object.keys(t).forEach((e) => {
        const a = t[e];
        l[e] = this.displayTime(a);
      }),
      {
        crackTimesSeconds: t,
        crackTimesDisplay: l,
        score: this.guessesToScore(e),
      }
    );
  }
  guessesToScore(e) {
    return e < 1005
      ? 0
      : e < 1000005
        ? 1
        : e < 100000005
          ? 2
          : e < 10000000005
            ? 3
            : 4;
  }
  displayTime(e) {
    let t,
      l = "centuries";
    const a = Object.keys(xr),
      n = a.findIndex((t) => e < xr[t]);
    return (
      n > -1 &&
        ((l = a[n - 1]),
        0 !== n ? (t = Math.round(e / xr[l])) : (l = "ltSecond")),
      this.translate(l, t)
    );
  }
}
var Cr = () => null,
  Vr = () => ({
    warning: Qs.translations.warnings.dates,
    suggestions: [Qs.translations.suggestions.dates],
  });
const Nr = (e, t) => {
  let l = null;
  const a = e.dictionaryName,
    n = "lastnames" === a || a.toLowerCase().includes("firstnames");
  return (
    "passwords" === a
      ? (l = ((e, t) => {
          let l = null;
          return (
            !t || e.l33t || e.reversed
              ? e.guessesLog10 <= 4 &&
                (l = Qs.translations.warnings.similarToCommon)
              : (l =
                  e.rank <= 10
                    ? Qs.translations.warnings.topTen
                    : e.rank <= 100
                      ? Qs.translations.warnings.topHundred
                      : Qs.translations.warnings.common),
            l
          );
        })(e, t))
      : a.includes("wikipedia")
        ? (l = ((e, t) => {
            let l = null;
            return (t && (l = Qs.translations.warnings.wordByItself), l);
          })(0, t))
        : n
          ? (l = ((e, t) =>
              t
                ? Qs.translations.warnings.namesByThemselves
                : Qs.translations.warnings.commonNames)(0, t))
          : "userInputs" === a && (l = Qs.translations.warnings.userInputs),
    l
  );
};
var Tr = (e, t) => {
    const l = Nr(e, t),
      a = [],
      n = e.token;
    return (
      n.match(Is)
        ? a.push(Qs.translations.suggestions.capitalization)
        : n.match(_s) &&
          n.toLowerCase() !== n &&
          a.push(Qs.translations.suggestions.allUppercase),
      e.reversed &&
        e.token.length >= 4 &&
        a.push(Qs.translations.suggestions.reverseWords),
      e.l33t && a.push(Qs.translations.suggestions.l33t),
      { warning: l, suggestions: a }
    );
  },
  Er = (e) =>
    "recentYear" === e.regexName
      ? {
          warning: Qs.translations.warnings.recentYears,
          suggestions: [
            Qs.translations.suggestions.recentYears,
            Qs.translations.suggestions.associatedYears,
          ],
        }
      : { warning: null, suggestions: [] },
  Mr = (e) => {
    let t = Qs.translations.warnings.extendedRepeat;
    return (
      1 === e.baseToken.length && (t = Qs.translations.warnings.simpleRepeat),
      { warning: t, suggestions: [Qs.translations.suggestions.repeated] }
    );
  },
  Ir = () => ({
    warning: Qs.translations.warnings.sequences,
    suggestions: [Qs.translations.suggestions.sequences],
  }),
  Or = (e) => {
    let t = Qs.translations.warnings.keyPattern;
    return (
      1 === e.turns && (t = Qs.translations.warnings.straightRow),
      {
        warning: t,
        suggestions: [Qs.translations.suggestions.longerKeyboardPattern],
      }
    );
  },
  Ar = () => null;
const _r = { warning: null, suggestions: [] };
class Pr {
  constructor() {
    ((this.matchers = {
      bruteforce: Cr,
      date: Vr,
      dictionary: Tr,
      regex: Er,
      repeat: Mr,
      sequence: Ir,
      spatial: Or,
      separator: Ar,
    }),
      (this.defaultFeedback = { warning: null, suggestions: [] }),
      this.setDefaultSuggestions());
  }
  setDefaultSuggestions() {
    this.defaultFeedback.suggestions.push(
      Qs.translations.suggestions.useWords,
      Qs.translations.suggestions.noNeed,
    );
  }
  getFeedback(e, t) {
    if (0 === t.length) return this.defaultFeedback;
    if (e > 2) return _r;
    const l = Qs.translations.suggestions.anotherWord,
      a = this.getLongestMatch(t);
    let n = this.getMatchFeedback(a, 1 === t.length);
    return (
      null != n
        ? n.suggestions.unshift(l)
        : (n = { warning: null, suggestions: [l] }),
      n
    );
  }
  getLongestMatch(e) {
    let t = e[0];
    return (
      e.slice(1).forEach((e) => {
        e.token.length > t.token.length && (t = e);
      }),
      t
    );
  }
  getMatchFeedback(e, t) {
    return this.matchers[e.pattern]
      ? this.matchers[e.pattern](e, t)
      : Qs.matchers[e.pattern] && "feedback" in Qs.matchers[e.pattern]
        ? Qs.matchers[e.pattern].feedback(e, t)
        : _r;
  }
}
const Lr = () => new Date().getTime(),
  $r = (e, t) => {
    const l = Lr(),
      a = ((e, t) => (
        t && Qs.extendUserInputsDictionary(t),
        new yr().match(e)
      ))(e, t);
    if (a instanceof Promise)
      throw new Error(
        "You are using a Promised matcher, please use `zxcvbnAsync` for it.",
      );
    return ((e, t, l) => {
      const a = new Pr(),
        n = new Sr(),
        o = pr.mostGuessableMatchSequence(t, e),
        s = Lr() - l,
        r = n.estimateAttackTimes(o.guesses);
      return {
        calcTime: s,
        ...o,
        ...r,
        feedback: a.getFeedback(r.score, o.sequence),
      };
    })(a, e, l);
  },
  Br = ["data-score"],
  Dr = ut(
    v({
      __name: "InputPassword",
      props: { strength: rt.bool.def(!1), modelValue: rt.string.def("") },
      emits: ["update:modelValue"],
      setup(e, { emit: t }) {
        const l = e,
          { getPrefixCls: a } = it(),
          n = a("input-password");
        ie(
          () => l.modelValue,
          (e) => {
            e !== T(r) && (r.value = e);
          },
        );
        const { configGlobal: o } = { configGlobal: G("configGlobal", {}) },
          s = b("password"),
          r = b(l.modelValue);
        ie(
          () => r.value,
          (e) => {
            t("update:modelValue", e);
          },
        );
        const i = y(() => {
          const e = T(r),
            t = $r(T(r));
          return e ? t.score : -1;
        });
        return (t, l) => {
          var a;
          return (
            x(),
            O(
              "div",
              {
                class: N([
                  T(n),
                  `${T(n)}--${null == (a = T(o)) ? void 0 : a.size}`,
                ]),
              },
              [
                M(
                  T(Mt),
                  j(t.$attrs, {
                    modelValue: r.value,
                    "onUpdate:modelValue":
                      l[0] || (l[0] = (e) => (r.value = e)),
                    showPassword: "",
                    type: s.value,
                  }),
                  null,
                  16,
                  ["modelValue", "type"],
                ),
                e.strength
                  ? (x(),
                    O(
                      "div",
                      {
                        key: 0,
                        class: N([
                          `${T(n)}__bar`,
                          "relative h-6px mt-10px mb-6px mr-auto ml-auto",
                        ]),
                      },
                      [
                        V(
                          "div",
                          {
                            class: N(`${T(n)}__bar--fill`),
                            "data-score": i.value,
                          },
                          null,
                          10,
                          Br,
                        ),
                      ],
                      2,
                    ))
                  : X("", !0),
              ],
              2,
            )
          );
        };
      },
    }),
    [["__scopeId", "data-v-24d2c228"]],
  ),
  jr = ["innerHTML"],
  Rr = v({
    __name: "Text",
    props: { modelValue: rt.string.def("") },
    setup(e) {
      const t = b(e.modelValue);
      return (e, l) => (x(), O("span", { innerHTML: t.value }, null, 8, jr));
    },
  });
var zr,
  Fr = { exports: {} };
const Kr = pt(
    (Fr.exports =
      ((zr = ct),
      (function () {
        var e = {
            789: function (e) {
              e.exports = zr;
            },
          },
          t = {};
        function l(a) {
          var n = t[a];
          if (void 0 !== n) return n.exports;
          var o = (t[a] = { exports: {} });
          return (e[a](o, o.exports, l), o.exports);
        }
        ((l.d = function (e, t) {
          for (var a in t)
            l.o(t, a) &&
              !l.o(e, a) &&
              Object.defineProperty(e, a, { enumerable: !0, get: t[a] });
        }),
          (l.o = function (e, t) {
            return Object.prototype.hasOwnProperty.call(e, t);
          }),
          (l.r = function (e) {
            ("undefined" != typeof Symbol &&
              Symbol.toStringTag &&
              Object.defineProperty(e, Symbol.toStringTag, { value: "Module" }),
              Object.defineProperty(e, "__esModule", { value: !0 }));
          }));
        var a = {};
        return (
          (function () {
            function e(e, t) {
              (null == t || t > e.length) && (t = e.length);
              for (var l = 0, a = new Array(t); l < t; l++) a[l] = e[l];
              return a;
            }
            function t(t, l) {
              if (t) {
                if ("string" == typeof t) return e(t, l);
                var a = Object.prototype.toString.call(t).slice(8, -1);
                return (
                  "Object" === a && t.constructor && (a = t.constructor.name),
                  "Map" === a || "Set" === a
                    ? Array.from(t)
                    : "Arguments" === a ||
                        /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(a)
                      ? e(t, l)
                      : void 0
                );
              }
            }
            function n(l) {
              return (
                (function (t) {
                  if (Array.isArray(t)) return e(t);
                })(l) ||
                (function (e) {
                  if (
                    ("undefined" != typeof Symbol &&
                      null != e[Symbol.iterator]) ||
                    null != e["@@iterator"]
                  )
                    return Array.from(e);
                })(l) ||
                t(l) ||
                (function () {
                  throw new TypeError(
                    "Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.",
                  );
                })()
              );
            }
            function o(e, t, l) {
              return (
                t in e
                  ? Object.defineProperty(e, t, {
                      value: l,
                      enumerable: !0,
                      configurable: !0,
                      writable: !0,
                    })
                  : (e[t] = l),
                e
              );
            }
            (l.r(a),
              l.d(a, {
                default: function () {
                  return w;
                },
              }));
            var s = l(789),
              r = (0, s.defineComponent)({
                props: {
                  data: { required: !0, type: String },
                  onClick: Function,
                },
                render: function () {
                  var e = this.data,
                    t = this.onClick;
                  return (0, s.createVNode)(
                    "span",
                    { class: "vjs-tree-brackets", onClick: t },
                    [e],
                  );
                },
              }),
              i = (0, s.defineComponent)({
                emits: ["change", "update:modelValue"],
                props: {
                  checked: { type: Boolean, default: !1 },
                  isMultiple: Boolean,
                  onChange: Function,
                },
                setup: function (e, t) {
                  var l = t.emit;
                  return {
                    uiType: (0, s.computed)(function () {
                      return e.isMultiple ? "checkbox" : "radio";
                    }),
                    model: (0, s.computed)({
                      get: function () {
                        return e.checked;
                      },
                      set: function (e) {
                        return l("update:modelValue", e);
                      },
                    }),
                  };
                },
                render: function () {
                  var e = this.uiType,
                    t = this.model,
                    l = this.$emit;
                  return (0, s.createVNode)(
                    "label",
                    {
                      class: ["vjs-check-controller", t ? "is-checked" : ""],
                      onClick: function (e) {
                        return e.stopPropagation();
                      },
                    },
                    [
                      (0, s.createVNode)(
                        "span",
                        { class: "vjs-check-controller-inner is-".concat(e) },
                        null,
                      ),
                      (0, s.createVNode)(
                        "input",
                        {
                          checked: t,
                          class: "vjs-check-controller-original is-".concat(e),
                          type: e,
                          onChange: function () {
                            return l("change", t);
                          },
                        },
                        null,
                      ),
                    ],
                  );
                },
              }),
              u = (0, s.defineComponent)({
                props: {
                  nodeType: { required: !0, type: String },
                  onClick: Function,
                },
                render: function () {
                  var e = this.nodeType,
                    t = this.onClick,
                    l = "objectStart" === e || "arrayStart" === e;
                  return l || "objectCollapsed" === e || "arrayCollapsed" === e
                    ? (0, s.createVNode)(
                        "span",
                        {
                          class: "vjs-carets vjs-carets-".concat(
                            l ? "open" : "close",
                          ),
                          onClick: t,
                        },
                        [
                          (0, s.createVNode)(
                            "svg",
                            {
                              viewBox: "0 0 1024 1024",
                              focusable: "false",
                              "data-icon": "caret-down",
                              width: "1em",
                              height: "1em",
                              fill: "currentColor",
                              "aria-hidden": "true",
                            },
                            [
                              (0, s.createVNode)(
                                "path",
                                {
                                  d: "M840.4 300H183.6c-19.7 0-30.7 20.8-18.5 35l328.4 380.8c9.4 10.9 27.5 10.9 37 0L858.9 335c12.2-14.2 1.2-35-18.5-35z",
                                },
                                null,
                              ),
                            ],
                          ),
                        ],
                      )
                    : null;
                },
              });
            function c(e) {
              return (c =
                "function" == typeof Symbol &&
                "symbol" == typeof Symbol.iterator
                  ? function (e) {
                      return typeof e;
                    }
                  : function (e) {
                      return e &&
                        "function" == typeof Symbol &&
                        e.constructor === Symbol &&
                        e !== Symbol.prototype
                        ? "symbol"
                        : typeof e;
                    })(e);
            }
            function d(e) {
              return Object.prototype.toString
                .call(e)
                .slice(8, -1)
                .toLowerCase();
            }
            function p(e) {
              var t =
                  arguments.length > 1 && void 0 !== arguments[1]
                    ? arguments[1]
                    : "root",
                l =
                  arguments.length > 2 && void 0 !== arguments[2]
                    ? arguments[2]
                    : 0,
                a = (arguments.length > 3 ? arguments[3] : void 0) || {},
                n = a.key,
                o = a.index,
                s = a.type,
                r = void 0 === s ? "content" : s,
                i = a.showComma,
                u = void 0 !== i && i,
                c = a.length,
                v = void 0 === c ? 1 : c,
                f = d(e);
              if ("array" === f) {
                var m = h(
                  e.map(function (e, a, n) {
                    return p(e, "".concat(t, "[").concat(a, "]"), l + 1, {
                      index: a,
                      showComma: a !== n.length - 1,
                      length: v,
                      type: r,
                    });
                  }),
                );
                return [
                  p("[", t, l, {
                    showComma: !1,
                    key: n,
                    length: e.length,
                    type: "arrayStart",
                  })[0],
                ].concat(
                  m,
                  p("]", t, l, {
                    showComma: u,
                    length: e.length,
                    type: "arrayEnd",
                  })[0],
                );
              }
              if ("object" === f) {
                var g = Object.keys(e),
                  b = h(
                    g.map(function (a, n, o) {
                      return p(
                        e[a],
                        /^[a-zA-Z_]\w*$/.test(a)
                          ? "".concat(t, ".").concat(a)
                          : "".concat(t, '["').concat(a, '"]'),
                        l + 1,
                        {
                          key: a,
                          showComma: n !== o.length - 1,
                          length: v,
                          type: r,
                        },
                      );
                    }),
                  );
                return [
                  p("{", t, l, {
                    showComma: !1,
                    key: n,
                    index: o,
                    length: g.length,
                    type: "objectStart",
                  })[0],
                ].concat(
                  b,
                  p("}", t, l, {
                    showComma: u,
                    length: g.length,
                    type: "objectEnd",
                  })[0],
                );
              }
              return [
                {
                  content: e,
                  level: l,
                  key: n,
                  index: o,
                  path: t,
                  showComma: u,
                  length: v,
                  type: r,
                },
              ];
            }
            function h(e) {
              if ("function" == typeof Array.prototype.flat) return e.flat();
              for (var t = n(e), l = []; t.length; ) {
                var a = t.shift();
                Array.isArray(a) ? t.unshift.apply(t, n(a)) : l.push(a);
              }
              return l;
            }
            function v(e) {
              var t =
                arguments.length > 1 && void 0 !== arguments[1]
                  ? arguments[1]
                  : new WeakMap();
              if (null == e) return e;
              if (e instanceof Date) return new Date(e);
              if (e instanceof RegExp) return new RegExp(e);
              if ("object" !== c(e)) return e;
              if (t.get(e)) return t.get(e);
              if (Array.isArray(e)) {
                var l = e.map(function (e) {
                  return v(e, t);
                });
                return (t.set(e, l), l);
              }
              var a = {};
              for (var n in e) a[n] = v(e[n], t);
              return (t.set(e, a), a);
            }
            function f(e, t) {
              var l = Object.keys(e);
              if (Object.getOwnPropertySymbols) {
                var a = Object.getOwnPropertySymbols(e);
                (t &&
                  (a = a.filter(function (t) {
                    return Object.getOwnPropertyDescriptor(e, t).enumerable;
                  })),
                  l.push.apply(l, a));
              }
              return l;
            }
            function m(e) {
              for (var t = 1; t < arguments.length; t++) {
                var l = null != arguments[t] ? arguments[t] : {};
                t % 2
                  ? f(Object(l), !0).forEach(function (t) {
                      o(e, t, l[t]);
                    })
                  : Object.getOwnPropertyDescriptors
                    ? Object.defineProperties(
                        e,
                        Object.getOwnPropertyDescriptors(l),
                      )
                    : f(Object(l)).forEach(function (t) {
                        Object.defineProperty(
                          e,
                          t,
                          Object.getOwnPropertyDescriptor(l, t),
                        );
                      });
              }
              return e;
            }
            var g = {
                showLength: { type: Boolean, default: !1 },
                showDoubleQuotes: { type: Boolean, default: !0 },
                renderNodeKey: Function,
                renderNodeValue: Function,
                selectableType: String,
                showSelectController: { type: Boolean, default: !1 },
                showLine: { type: Boolean, default: !0 },
                showLineNumber: { type: Boolean, default: !1 },
                selectOnClickNode: { type: Boolean, default: !0 },
                nodeSelectable: {
                  type: Function,
                  default: function () {
                    return !0;
                  },
                },
                highlightSelectedNode: { type: Boolean, default: !0 },
                showIcon: { type: Boolean, default: !1 },
                showKeyValueSpace: { type: Boolean, default: !0 },
                editable: { type: Boolean, default: !1 },
                editableTrigger: { type: String, default: "click" },
                onNodeClick: { type: Function },
                onBracketsClick: { type: Function },
                onIconClick: { type: Function },
                onValueChange: { type: Function },
              },
              b = (0, s.defineComponent)({
                name: "TreeNode",
                props: m(
                  m({}, g),
                  {},
                  {
                    node: { type: Object, required: !0 },
                    collapsed: Boolean,
                    checked: Boolean,
                    style: Object,
                    onSelectedChange: { type: Function },
                  },
                ),
                emits: [
                  "nodeClick",
                  "bracketsClick",
                  "iconClick",
                  "selectedChange",
                  "valueChange",
                ],
                setup: function (e, t) {
                  var l = t.emit,
                    a = (0, s.computed)(function () {
                      return d(e.node.content);
                    }),
                    n = (0, s.computed)(function () {
                      return "vjs-value vjs-value-".concat(a.value);
                    }),
                    o = (0, s.computed)(function () {
                      return e.showDoubleQuotes
                        ? '"'.concat(e.node.key, '"')
                        : e.node.key;
                    }),
                    c = (0, s.computed)(function () {
                      return "multiple" === e.selectableType;
                    }),
                    p = (0, s.computed)(function () {
                      return "single" === e.selectableType;
                    }),
                    h = (0, s.computed)(function () {
                      return e.nodeSelectable(e.node) && (c.value || p.value);
                    }),
                    v = (0, s.reactive)({ editing: !1 }),
                    f = function (t) {
                      var a,
                        n,
                        o =
                          "null" ===
                          (n =
                            null === (a = t.target) || void 0 === a
                              ? void 0
                              : a.value)
                            ? null
                            : "undefined" === n
                              ? void 0
                              : "true" === n ||
                                ("false" !== n &&
                                  (n[0] + n[n.length - 1] === '""' ||
                                  n[0] + n[n.length - 1] === "''"
                                    ? n.slice(1, -1)
                                    : ("number" == typeof Number(n) &&
                                          !isNaN(Number(n))) ||
                                        "NaN" === n
                                      ? Number(n)
                                      : n));
                      l("valueChange", o, e.node.path);
                    },
                    m = (0, s.computed)(function () {
                      var t,
                        l =
                          null === (t = e.node) || void 0 === t
                            ? void 0
                            : t.content;
                      return (
                        null === l
                          ? (l = "null")
                          : void 0 === l && (l = "undefined"),
                        "string" === a.value ? '"'.concat(l, '"') : l + ""
                      );
                    }),
                    g = function () {
                      var t = e.renderNodeValue;
                      return t
                        ? t({ node: e.node, defaultValue: m.value })
                        : m.value;
                    },
                    b = function () {
                      l("bracketsClick", !e.collapsed, e.node.path);
                    },
                    y = function () {
                      l("iconClick", !e.collapsed, e.node.path);
                    },
                    k = function () {
                      l("selectedChange", e.node);
                    },
                    w = function () {
                      (l("nodeClick", e.node),
                        h.value &&
                          e.selectOnClickNode &&
                          l("selectedChange", e.node));
                    },
                    x = function (t) {
                      if (e.editable && !v.editing) {
                        v.editing = !0;
                        var l = function e(l) {
                          var a;
                          l.target !== t.target &&
                            (null === (a = l.target) || void 0 === a
                              ? void 0
                              : a.parentElement) !== t.target &&
                            ((v.editing = !1),
                            document.removeEventListener("click", e));
                        };
                        (document.removeEventListener("click", l),
                          document.addEventListener("click", l));
                      }
                    };
                  return function () {
                    var t,
                      l = e.node;
                    return (0, s.createVNode)(
                      "div",
                      {
                        class: {
                          "vjs-tree-node": !0,
                          "has-selector": e.showSelectController,
                          "has-carets": e.showIcon,
                          "is-highlight": e.highlightSelectedNode && e.checked,
                        },
                        onClick: w,
                        style: e.style,
                      },
                      [
                        e.showLineNumber &&
                          (0, s.createVNode)(
                            "span",
                            { class: "vjs-node-index" },
                            [l.id + 1],
                          ),
                        e.showSelectController &&
                          h.value &&
                          "objectEnd" !== l.type &&
                          "arrayEnd" !== l.type &&
                          (0, s.createVNode)(
                            i,
                            {
                              isMultiple: c.value,
                              checked: e.checked,
                              onChange: k,
                            },
                            null,
                          ),
                        (0, s.createVNode)("div", { class: "vjs-indent" }, [
                          Array.from(Array(l.level)).map(function (t, l) {
                            return (0, s.createVNode)(
                              "div",
                              {
                                key: l,
                                class: {
                                  "vjs-indent-unit": !0,
                                  "has-line": e.showLine,
                                },
                              },
                              null,
                            );
                          }),
                          e.showIcon &&
                            (0, s.createVNode)(
                              u,
                              { nodeType: l.type, onClick: y },
                              null,
                            ),
                        ]),
                        l.key &&
                          (0, s.createVNode)("span", { class: "vjs-key" }, [
                            ((t = e.renderNodeKey),
                            t
                              ? t({ node: e.node, defaultKey: o.value || "" })
                              : o.value),
                            (0, s.createVNode)("span", { class: "vjs-colon" }, [
                              ":".concat(e.showKeyValueSpace ? " " : ""),
                            ]),
                          ]),
                        (0, s.createVNode)("span", null, [
                          "content" !== l.type && l.content
                            ? (0, s.createVNode)(
                                r,
                                { data: l.content.toString(), onClick: b },
                                null,
                              )
                            : (0, s.createVNode)(
                                "span",
                                {
                                  class: n.value,
                                  onClick:
                                    !e.editable ||
                                    (e.editableTrigger &&
                                      "click" !== e.editableTrigger)
                                      ? void 0
                                      : x,
                                  onDblclick:
                                    e.editable &&
                                    "dblclick" === e.editableTrigger
                                      ? x
                                      : void 0,
                                },
                                [
                                  e.editable && v.editing
                                    ? (0, s.createVNode)(
                                        "input",
                                        {
                                          value: m.value,
                                          onChange: f,
                                          style: {
                                            padding: "3px 8px",
                                            border: "1px solid #eee",
                                            boxShadow: "none",
                                            boxSizing: "border-box",
                                            borderRadius: 5,
                                            fontFamily: "inherit",
                                          },
                                        },
                                        null,
                                      )
                                    : g(),
                                ],
                              ),
                          l.showComma &&
                            (0, s.createVNode)("span", null, [","]),
                          e.showLength &&
                            e.collapsed &&
                            (0, s.createVNode)(
                              "span",
                              { class: "vjs-comment" },
                              [
                                (0, s.createTextVNode)(" // "),
                                l.length,
                                (0, s.createTextVNode)(" items "),
                              ],
                            ),
                        ]),
                      ],
                    );
                  };
                },
              });
            function y(e, t) {
              var l = Object.keys(e);
              if (Object.getOwnPropertySymbols) {
                var a = Object.getOwnPropertySymbols(e);
                (t &&
                  (a = a.filter(function (t) {
                    return Object.getOwnPropertyDescriptor(e, t).enumerable;
                  })),
                  l.push.apply(l, a));
              }
              return l;
            }
            function k(e) {
              for (var t = 1; t < arguments.length; t++) {
                var l = null != arguments[t] ? arguments[t] : {};
                t % 2
                  ? y(Object(l), !0).forEach(function (t) {
                      o(e, t, l[t]);
                    })
                  : Object.getOwnPropertyDescriptors
                    ? Object.defineProperties(
                        e,
                        Object.getOwnPropertyDescriptors(l),
                      )
                    : y(Object(l)).forEach(function (t) {
                        Object.defineProperty(
                          e,
                          t,
                          Object.getOwnPropertyDescriptor(l, t),
                        );
                      });
              }
              return e;
            }
            var w = (0, s.defineComponent)({
              name: "Tree",
              props: k(
                k({}, g),
                {},
                {
                  data: {
                    type: [String, Number, Boolean, Array, Object],
                    default: null,
                  },
                  deep: { type: Number, default: 1 / 0 },
                  pathCollapsible: {
                    type: Function,
                    default: function () {
                      return !1;
                    },
                  },
                  rootPath: { type: String, default: "root" },
                  virtual: { type: Boolean, default: !1 },
                  height: { type: Number, default: 400 },
                  itemHeight: { type: Number, default: 20 },
                  selectedValue: {
                    type: [String, Array],
                    default: function () {
                      return "";
                    },
                  },
                  collapsedOnClickBrackets: { type: Boolean, default: !0 },
                  style: Object,
                  onSelectedChange: { type: Function },
                },
              ),
              slots: ["renderNodeKey", "renderNodeValue"],
              emits: [
                "nodeClick",
                "bracketsClick",
                "iconClick",
                "selectedChange",
                "update:selectedValue",
                "update:data",
              ],
              setup: function (e, l) {
                var a = l.emit,
                  r = l.slots,
                  i = (0, s.ref)(),
                  u = (0, s.computed)(function () {
                    return p(e.data, e.rootPath);
                  }),
                  c = function (t) {
                    return u.value.reduce(function (l, a) {
                      var n,
                        s = a.level >= t,
                        r =
                          null === (n = e.pathCollapsible) || void 0 === n
                            ? void 0
                            : n.call(e, a);
                      return ("objectStart" !== a.type &&
                        "arrayStart" !== a.type) ||
                        (!s && !r)
                        ? l
                        : k(k({}, l), {}, o({}, a.path, 1));
                    }, {});
                  },
                  d = (0, s.reactive)({
                    translateY: 0,
                    visibleData: null,
                    hiddenPaths: c(e.deep),
                  }),
                  h = (0, s.computed)(function () {
                    for (
                      var e = null, t = [], l = u.value.length, a = 0;
                      a < l;
                      a++
                    ) {
                      var n = k(k({}, u.value[a]), {}, { id: a }),
                        o = d.hiddenPaths[n.path];
                      if (e && e.path === n.path) {
                        var s = "objectStart" === e.type,
                          r = k(
                            k(k({}, n), e),
                            {},
                            {
                              showComma: n.showComma,
                              content: s ? "{...}" : "[...]",
                              type: s ? "objectCollapsed" : "arrayCollapsed",
                            },
                          );
                        ((e = null), t.push(r));
                      } else {
                        if (o && !e) {
                          e = n;
                          continue;
                        }
                        if (e) continue;
                        t.push(n);
                      }
                    }
                    return t;
                  }),
                  f = (0, s.computed)(function () {
                    var t = e.selectedValue;
                    return t &&
                      "multiple" === e.selectableType &&
                      Array.isArray(t)
                      ? t
                      : [t];
                  }),
                  m = (0, s.computed)(function () {
                    return !e.selectableType ||
                      e.selectOnClickNode ||
                      e.showSelectController
                      ? ""
                      : "When selectableType is not null, selectOnClickNode and showSelectController cannot be false at the same time, because this will cause the selection to fail.";
                  }),
                  g = function () {
                    var t = h.value;
                    if (e.virtual) {
                      var l,
                        a = e.height / e.itemHeight,
                        n =
                          (null === (l = i.value) || void 0 === l
                            ? void 0
                            : l.scrollTop) || 0,
                        o = Math.floor(n / e.itemHeight),
                        s = o < 0 ? 0 : o + a > t.length ? t.length - a : o;
                      s < 0 && (s = 0);
                      var r = s + a;
                      ((d.translateY = s * e.itemHeight),
                        (d.visibleData = t.filter(function (e, t) {
                          return t >= s && t < r;
                        })));
                    } else d.visibleData = t;
                  },
                  y = function () {
                    g();
                  },
                  w = function (l) {
                    var o,
                      s,
                      r = l.path,
                      i = e.selectableType;
                    if ("multiple" === i) {
                      var u = f.value.findIndex(function (e) {
                          return e === r;
                        }),
                        c = n(f.value);
                      (-1 !== u ? c.splice(u, 1) : c.push(r),
                        a("update:selectedValue", c),
                        a("selectedChange", c, n(f.value)));
                    } else if ("single" === i && f.value[0] !== r) {
                      var d = ((o = f.value),
                        (s = 1),
                        (function (e) {
                          if (Array.isArray(e)) return e;
                        })(o) ||
                          (function (e, t) {
                            var l =
                              null == e
                                ? null
                                : ("undefined" != typeof Symbol &&
                                    e[Symbol.iterator]) ||
                                  e["@@iterator"];
                            if (null != l) {
                              var a,
                                n,
                                o = [],
                                s = !0,
                                r = !1;
                              try {
                                for (
                                  l = l.call(e);
                                  !(s = (a = l.next()).done) &&
                                  (o.push(a.value), !t || o.length !== t);
                                  s = !0
                                );
                              } catch (i) {
                                ((r = !0), (n = i));
                              } finally {
                                try {
                                  s || null == l.return || l.return();
                                } finally {
                                  if (r) throw n;
                                }
                              }
                              return o;
                            }
                          })(o, s) ||
                          t(o, s) ||
                          (function () {
                            throw new TypeError(
                              "Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.",
                            );
                          })())[0],
                        p = r;
                      (a("update:selectedValue", p), a("selectedChange", p, d));
                    }
                  },
                  x = function (e) {
                    a("nodeClick", e);
                  },
                  S = function (e, t) {
                    if (e)
                      d.hiddenPaths = k(k({}, d.hiddenPaths), {}, o({}, t, 1));
                    else {
                      var l = k({}, d.hiddenPaths);
                      (delete l[t], (d.hiddenPaths = l));
                    }
                  },
                  C = function (t, l) {
                    (e.collapsedOnClickBrackets && S(t, l),
                      a("bracketsClick", t));
                  },
                  V = function (e, t) {
                    (S(e, t), a("iconClick", e));
                  },
                  N = function (t, l) {
                    var n = v(e.data),
                      o = e.rootPath;
                    (new Function(
                      "data",
                      "val",
                      "data".concat(l.slice(o.length), "=val"),
                    )(n, t),
                      a("update:data", n));
                  };
                return (
                  (0, s.watchEffect)(function () {
                    m.value &&
                      (function (e) {
                        throw new Error("[VueJSONPretty] ".concat(e));
                      })(m.value);
                  }),
                  (0, s.watchEffect)(function () {
                    h.value && g();
                  }),
                  (0, s.watch)(
                    function () {
                      return e.deep;
                    },
                    function (e) {
                      e && (d.hiddenPaths = c(e));
                    },
                  ),
                  function () {
                    var t,
                      l,
                      a =
                        null !== (t = e.renderNodeKey) && void 0 !== t
                          ? t
                          : r.renderNodeKey,
                      n =
                        null !== (l = e.renderNodeValue) && void 0 !== l
                          ? l
                          : r.renderNodeValue,
                      o =
                        d.visibleData &&
                        d.visibleData.map(function (t) {
                          return (0, s.createVNode)(
                            b,
                            {
                              key: t.id,
                              node: t,
                              collapsed: !!d.hiddenPaths[t.path],
                              showDoubleQuotes: e.showDoubleQuotes,
                              showLength: e.showLength,
                              checked: f.value.includes(t.path),
                              selectableType: e.selectableType,
                              showLine: e.showLine,
                              showLineNumber: e.showLineNumber,
                              showSelectController: e.showSelectController,
                              selectOnClickNode: e.selectOnClickNode,
                              nodeSelectable: e.nodeSelectable,
                              highlightSelectedNode: e.highlightSelectedNode,
                              editable: e.editable,
                              editableTrigger: e.editableTrigger,
                              showIcon: e.showIcon,
                              showKeyValueSpace: e.showKeyValueSpace,
                              renderNodeKey: a,
                              renderNodeValue: n,
                              onNodeClick: x,
                              onBracketsClick: C,
                              onIconClick: V,
                              onSelectedChange: w,
                              onValueChange: N,
                              style:
                                e.itemHeight && 20 !== e.itemHeight
                                  ? {
                                      lineHeight: "".concat(e.itemHeight, "px"),
                                    }
                                  : {},
                            },
                            null,
                          );
                        });
                    return (0, s.createVNode)(
                      "div",
                      {
                        ref: i,
                        class: { "vjs-tree": !0, "is-virtual": e.virtual },
                        onScroll: e.virtual ? y : void 0,
                        style: e.showLineNumber
                          ? k(
                              {
                                paddingLeft: "".concat(
                                  12 * Number(u.value.length.toString().length),
                                  "px",
                                ),
                              },
                              e.style,
                            )
                          : e.style,
                      },
                      [
                        e.virtual
                          ? (0, s.createVNode)(
                              "div",
                              {
                                class: "vjs-tree-list",
                                style: { height: "".concat(e.height, "px") },
                              },
                              [
                                (0, s.createVNode)(
                                  "div",
                                  {
                                    class: "vjs-tree-list-holder",
                                    style: {
                                      height: "".concat(
                                        h.value.length * e.itemHeight,
                                        "px",
                                      ),
                                    },
                                  },
                                  [
                                    (0, s.createVNode)(
                                      "div",
                                      {
                                        class: "vjs-tree-list-holder-inner",
                                        style: {
                                          transform: "translateY(".concat(
                                            d.translateY,
                                            "px)",
                                          ),
                                        },
                                      },
                                      [o],
                                    ),
                                  ],
                                ),
                              ],
                            )
                          : o,
                      ],
                    );
                  }
                );
              },
            });
          })(),
          a
        );
      })())),
  ),
  Hr = v({
    __name: "JsonEditor",
    props: {
      modelValue: { type: Object, default: () => ({}) },
      deep: rt.number.def(5),
      showLength: rt.bool.def(!0),
      showLineNumbers: rt.bool.def(!0),
      showLineNumber: rt.bool.def(!0),
      showIcon: rt.bool.def(!0),
      showDoubleQuotes: rt.bool.def(!0),
      virtual: rt.bool.def(!1),
      height: rt.number.def(400),
      itemHeight: rt.number.def(20),
      rootPath: rt.string.def("root"),
      nodeSelectable: rt.func.def(),
      selectableType: rt.oneOf(["multiple", "single"]).def(),
      showSelectController: rt.bool.def(!1),
      selectOnClickNode: rt.bool.def(!0),
      highlightSelectedNode: rt.bool.def(!0),
      collapsedOnClickBrackets: rt.bool.def(!0),
      renderNodeKey: rt.func.def(),
      renderNodeValue: rt.func.def(),
      editable: rt.bool.def(!0),
      editableTrigger: rt.oneOf(["click", "dblclick"]).def("click"),
    },
    emits: [
      "update:modelValue",
      "node-click",
      "brackets-click",
      "icon-click",
      "selected-value",
    ],
    setup(e, { emit: t }) {
      const l = e,
        a = y(() => l.modelValue),
        n = y({
          get: () => a.value,
          set: (e) => {
            t("update:modelValue", e);
          },
        }),
        o = (e) => {
          t("node-click", e);
        },
        s = (e) => {
          t("brackets-click", e);
        },
        r = (e) => {
          t("icon-click", e);
        },
        i = (e, l) => {
          t("selected-value", e, l);
        };
      return (t, l) => (
        x(),
        S(
          T(Kr),
          {
            data: n.value,
            "onUpdate:data": l[0] || (l[0] = (e) => (n.value = e)),
            deep: e.deep,
            "show-length": e.showLength,
            "show-line-numbers": e.showLineNumbers,
            "show-line-number": e.showLineNumber,
            "show-icon": e.showIcon,
            "show-double-quotes": e.showDoubleQuotes,
            virtual: e.virtual,
            height: e.height,
            "item-height": e.itemHeight,
            "root-path": e.rootPath,
            "node-selectable": e.nodeSelectable,
            "selectable-type": e.selectableType,
            "show-select-controller": e.showSelectController,
            "select-on-click-node": e.selectOnClickNode,
            "highlight-selected-node": e.highlightSelectedNode,
            "collapsed-on-click-brackets": e.collapsedOnClickBrackets,
            "render-node-key": e.renderNodeKey,
            "render-node-value": e.renderNodeValue,
            editable: e.editable,
            "editable-trigger": e.editableTrigger,
            onNodeClick: o,
            onBracketsClick: s,
            onIconClick: r,
            onSelectedChange: i,
          },
          null,
          8,
          [
            "data",
            "deep",
            "show-length",
            "show-line-numbers",
            "show-line-number",
            "show-icon",
            "show-double-quotes",
            "virtual",
            "height",
            "item-height",
            "root-path",
            "node-selectable",
            "selectable-type",
            "show-select-controller",
            "select-on-click-node",
            "highlight-selected-node",
            "collapsed-on-click-brackets",
            "render-node-key",
            "render-node-value",
            "editable",
            "editable-trigger",
          ],
        )
      );
    },
  }),
  Wr = {
    RadioGroup: Qt,
    RadioButton: Qt,
    CheckboxGroup: _t,
    CheckboxButton: _t,
    Input: Mt,
    Autocomplete: Kl,
    InputNumber: ln,
    Select: el,
    Cascader: wa,
    Switch: nl,
    Slider: Wo,
    TimePicker: Gl,
    DatePicker: Xt,
    Rate: cn,
    ColorPicker: Xa,
    Transfer: fs,
    Divider: ol,
    TimeSelect: es,
    SelectV2: ko,
    InputPassword: Dr,
    Editor: il,
    TreeSelect: Vs,
    Upload: rl,
    JsonEditor: Hr,
    Text: Rr,
  },
  Ur = (e, t = "default", l) => {
    if (!e || !Reflect.has(e, t)) return null;
    if (!ht(e[t])) return null;
    const a = e[t];
    return a ? a(l) : null;
  };
var qr = ((e) => (
  (e.RADIO_GROUP = "RadioGroup"),
  (e.RADIO_BUTTON = "RadioButton"),
  (e.CHECKBOX_GROUP = "CheckboxGroup"),
  (e.CHECKBOX_BUTTON = "CheckboxButton"),
  (e.INPUT = "Input"),
  (e.AUTOCOMPLETE = "Autocomplete"),
  (e.INPUT_NUMBER = "InputNumber"),
  (e.SELECT = "Select"),
  (e.CASCADER = "Cascader"),
  (e.SWITCH = "Switch"),
  (e.SLIDER = "Slider"),
  (e.TIME_PICKER = "TimePicker"),
  (e.DATE_PICKER = "DatePicker"),
  (e.RATE = "Rate"),
  (e.COLOR_PICKER = "ColorPicker"),
  (e.TRANSFER = "Transfer"),
  (e.DIVIDER = "Divider"),
  (e.TIME_SELECT = "TimeSelect"),
  (e.SELECT_V2 = "SelectV2"),
  (e.INPUT_PASSWORD = "InputPassword"),
  (e.EDITOR = "Editor"),
  (e.TREE_SELECT = "TreeSelect"),
  (e.UPLOAD = "Upload"),
  (e.JSON_EDITOR = "JsonEditor"),
  (e.Text = "Text"),
  e
))(qr || {});
const { t: Yr } = vt(),
  Gr = (e = {}) => {
    const t = {};
    for (const l in e)
      e[l] &&
        (ht(e[l])
          ? (t[mt(l)] = (...t) => {
              var a;
              return null == (a = e[l]) ? void 0 : a.call(e, ...t);
            })
          : (t[mt(l)] = () => e[l]));
    return t;
  },
  Xr = (e, t) => {
    const l = { ...t };
    return (
      e.map((e) => {
        if (e.remove) delete l[e.field];
        else if ("Divider" !== e.component) {
          const t = Xe(l, e.field);
          ft(
            l,
            e.field,
            void 0 !== t
              ? Xe(l, e.field)
              : void 0 !== e.value
                ? e.value
                : void 0,
          );
        }
      }),
      l
    );
  };
function Zr(e) {
  return (
    "function" == typeof e ||
    ("[object Object]" === Object.prototype.toString.call(e) && !yt(e))
  );
}
const { renderSelectOptions: Qr } = (() => {
    const e = (e, t) => {
      var l, a, n, o;
      const s = e.componentProps,
        r = null == (l = null == s ? void 0 : s.props) ? void 0 : l.label,
        i = null == (a = null == s ? void 0 : s.props) ? void 0 : a.value,
        u = null == (n = null == s ? void 0 : s.props) ? void 0 : n.key,
        c = null == (o = s.slots) ? void 0 : o.optionDefault;
      return M(
        tl,
        j(t, {
          key: t[u || "key"],
          label: t[r || "label"],
          value: t[i || "value"],
        }),
        { default: () => (c ? c(t) : void 0) },
      );
    };
    return {
      renderSelectOptions: (t) => {
        var l, a, n, o;
        const s = null == t ? void 0 : t.componentProps,
          r =
            null == (l = null == s ? void 0 : s.slots)
              ? void 0
              : l.optionGroupDefault,
          i = null == (a = null == s ? void 0 : s.props) ? void 0 : a.label,
          u = null == (n = null == s ? void 0 : s.props) ? void 0 : n.key;
        return null == (o = null == s ? void 0 : s.options)
          ? void 0
          : o.map((l) => {
              var a;
              return (
                null == (a = null == l ? void 0 : l.options) ? void 0 : a.length
              )
                ? r
                  ? r(l)
                  : M(
                      al,
                      { label: l[i || "label"], key: l[u || "key"] },
                      {
                        default: () => {
                          var a;
                          return null == (a = null == l ? void 0 : l.options)
                            ? void 0
                            : a.map((l) => e(t, l));
                        },
                      },
                    )
                : e(t, l);
            });
      },
    };
  })(),
  { renderRadioOptions: Jr } = {
    renderRadioOptions: (e) => {
      var t, l, a, n;
      const o = null == e ? void 0 : e.componentProps,
        s =
          (null == (t = null == o ? void 0 : o.props) ? void 0 : t.value) ||
          "value",
        r =
          (null == (l = null == o ? void 0 : o.props) ? void 0 : l.label) ||
          "label",
        i =
          (null == (a = null == o ? void 0 : o.props) ? void 0 : a.disabled) ||
          "disabled",
        u = e.component === qr.RADIO_GROUP ? Zt : Jt;
      return null == (n = null == o ? void 0 : o.options)
        ? void 0
        : n.map((e) => {
            const { value: t, ...l } = e;
            return M(
              u,
              j(l, { disabled: e[i || "disabled"], label: e[s || "value"] }),
              { default: () => [e[r || "label"]] },
            );
          });
    },
  },
  { renderCheckboxOptions: ei } = {
    renderCheckboxOptions: (e) => {
      var t, l, a, n;
      const o = null == e ? void 0 : e.componentProps,
        s =
          (null == (t = null == o ? void 0 : o.props) ? void 0 : t.value) ||
          "value",
        r =
          (null == (l = null == o ? void 0 : o.props) ? void 0 : l.label) ||
          "label",
        i =
          (null == (a = null == o ? void 0 : o.props) ? void 0 : a.disabled) ||
          "disabled",
        u = e.component === qr.CHECKBOX_GROUP ? At : Lt;
      return null == (n = null == o ? void 0 : o.options)
        ? void 0
        : n.map((e) => {
            const { value: t, ...l } = e;
            return M(
              u,
              j(l, { disabled: e[i || "disabled"], label: e[s || "value"] }),
              { default: () => [e[r || "label"]] },
            );
          });
    },
  },
  { getPrefixCls: ti } = it(),
  li = ti("form"),
  ai = ut(
    v({
      name: "Form",
      props: {
        schema: { type: Array, default: () => [] },
        isCol: rt.bool.def(!0),
        model: { type: Object, default: () => ({}) },
        autoSetPlaceholder: rt.bool.def(!0),
        isCustom: rt.bool.def(!1),
        labelWidth: rt.oneOfType([String, Number]).def("auto"),
        rules: { type: Object, default: () => ({}) },
        labelPosition: rt.oneOf(["left", "right", "top"]).def("right"),
        labelSuffix: rt.string.def(""),
        hideRequiredAsterisk: rt.bool.def(!1),
        requireAsteriskPosition: rt.oneOf(["left", "right"]).def("left"),
        showMessage: rt.bool.def(!0),
        inlineMessage: rt.bool.def(!1),
        statusIcon: rt.bool.def(!1),
        validateOnRuleChange: rt.bool.def(!0),
        size: { type: String, default: void 0 },
        disabled: rt.bool.def(!1),
        scrollToError: rt.bool.def(!1),
        scrollToErrorOffset: rt.oneOfType([Boolean, Object]).def(void 0),
      },
      emits: ["register"],
      setup(e, { slots: t, expose: l, emit: a }) {
        const n = b(),
          o = b({}),
          s = b({}),
          r = y(() => {
            const t = { ...e };
            return (Object.assign(t, T(s)), t);
          }),
          i = b({}),
          u = b({}),
          c = b(e.model);
        w(() => {
          var e;
          ((() => {
            const { schema: e = [] } = T(r);
            e.filter(
              (e) => !0 !== e.remove && !0 !== e.hidden && !!e.optionApi,
            ).forEach((e) => {
              e.optionApi && p(e.optionApi, e);
            });
          })(),
            a("register", null == (e = T(n)) ? void 0 : e.$parent, T(n)));
        });
        const d = (e) => {
            const { schema: t } = T(r);
            for (const l of t)
              for (const t of e) l.field === t.field && ft(l, t.path, t.value);
          },
          p = async (e, t) => {
            const l = await e();
            d([
              {
                field: t.field,
                path:
                  t.component === qr.TREE_SELECT
                    ? "componentProps.data"
                    : "componentProps.options",
                value: l,
              },
            ]);
          };
        (l({
          setValues: (e = {}) => {
            c.value = Object.assign(T(c), e);
          },
          setValue: (e, t) => {
            c.value[e] = t;
          },
          formModel: c,
          setProps: (e = {}) => {
            ((s.value = Object.assign(T(s), e)), (o.value = e));
          },
          delSchema: (e) => {
            const { schema: t } = T(r),
              l = bt(t, (t) => t.field === e);
            l > -1 && t.splice(l, 1);
          },
          addSchema: (e, t) => {
            const { schema: l } = T(r);
            void 0 === t ? l.push(e) : l.splice(t, 0, e);
          },
          setSchema: d,
          getComponentExpose: (e) => T(i)[e],
          getFormItemExpose: (e) => T(u)[e],
        }),
          ie(
            () => T(r).schema,
            (e = []) => {
              c.value = Xr(e, T(c));
            },
            { immediate: !0, deep: !0 },
          ));
        const h = () => {
            const { schema: e = [], isCol: t } = T(r);
            return e
              .filter(
                (e) =>
                  !0 !== e.remove &&
                  !0 !== e.hidden &&
                  (!e.ifshow || e.ifshow(c.value)),
              )
              .map((e) => {
                let l;
                return "Divider" === e.component
                  ? M(
                      Wr.Divider,
                      { contentPosition: "left", ...e.componentProps },
                      { default: () => [null == e ? void 0 : e.label] },
                    )
                  : t
                    ? M(
                        Ct,
                        ((e = {}) => ({
                          ...(e.span
                            ? {}
                            : { xs: 24, sm: 12, md: 12, lg: 12, xl: 12 }),
                          ...e,
                        }))(e.colProps),
                        Zr((l = v(e))) ? l : { default: () => [l] },
                      )
                    : v(e);
              });
          },
          v = (e) => {
            var t, l, a, n;
            const o = {
              default: () => {
                var t, l, a, n, o;
                if (
                  null ==
                  (l =
                    null == (t = null == e ? void 0 : e.formItemProps)
                      ? void 0
                      : t.slots)
                    ? void 0
                    : l.default
                )
                  return null ==
                    (n =
                      null == (a = null == e ? void 0 : e.formItemProps)
                        ? void 0
                        : a.slots)
                    ? void 0
                    : n.default(c.value);
                {
                  const t = Wr[e.component],
                    { autoSetPlaceholder: l } = T(r),
                    a =
                      (null == (o = null == e ? void 0 : e.componentProps)
                        ? void 0
                        : o.slots) || {},
                    n = { ...Gr(a) };
                  (e.component === qr.SELECT &&
                    (n.default = a.default
                      ? () => {
                          var t;
                          return a.default(
                            T(
                              null ==
                                (t = null == e ? void 0 : e.componentProps)
                                ? void 0
                                : t.options,
                            ),
                          );
                        }
                      : () => Qr(e)),
                    e.component === qr.SELECT_V2 &&
                      a.default &&
                      (n.default = ({ item: e }) => a.default(e)),
                    (e.component !== qr.RADIO_GROUP &&
                      e.component !== qr.RADIO_BUTTON) ||
                      (n.default = a.default
                        ? () => {
                            var t;
                            return a.default(
                              T(
                                null ==
                                  (t = null == e ? void 0 : e.componentProps)
                                  ? void 0
                                  : t.options,
                              ),
                            );
                          }
                        : () => Jr(e)),
                    (e.component !== qr.CHECKBOX_GROUP &&
                      e.component !== qr.CHECKBOX_BUTTON) ||
                      (n.default = a.default
                        ? () => {
                            var t;
                            return a.default(
                              T(
                                null ==
                                  (t = null == e ? void 0 : e.componentProps)
                                  ? void 0
                                  : t.options,
                              ),
                            );
                          }
                        : () => ei(e)));
                  const s = () => {
                    var a;
                    const o = y({
                      get: () => Xe(c.value, e.field),
                      set: (t) => {
                        ft(c.value, e.field, t);
                      },
                    });
                    return M(
                      t,
                      j(
                        {
                          modelValue: o.value,
                          "onUpdate:modelValue": (e) => (o.value = e),
                          ref: (t) => {
                            return (
                              (l = t),
                              (a = e.field),
                              void (i.value[a] = l)
                            );
                            var l, a;
                          },
                        },
                        l &&
                          ((e) => {
                            var t, l;
                            const a = [
                                qr.INPUT,
                                qr.AUTOCOMPLETE,
                                qr.INPUT_NUMBER,
                                qr.INPUT_PASSWORD,
                              ],
                              n = [
                                qr.SELECT,
                                qr.TIME_PICKER,
                                qr.DATE_PICKER,
                                qr.TIME_SELECT,
                                qr.SELECT_V2,
                              ];
                            if (a.includes(null == e ? void 0 : e.component))
                              return { placeholder: `请输入${e.label}` };
                            if (n.includes(null == e ? void 0 : e.component))
                              return [
                                "datetimerange",
                                "daterange",
                                "monthrange",
                                "datetimerange",
                                "daterange",
                              ].includes(
                                (null ==
                                (t = null == e ? void 0 : e.componentProps)
                                  ? void 0
                                  : t.type) ||
                                  (null ==
                                  (l = null == e ? void 0 : e.componentProps)
                                    ? void 0
                                    : l.isRange),
                              )
                                ? {
                                    startPlaceholder: Yr(
                                      "common.startTimeText",
                                    ),
                                    endPlaceholder: Yr("common.endTimeText"),
                                    rangeSeparator: "-",
                                  }
                                : { placeholder: `请选择${e.label}` };
                            return {};
                          })(e),
                        ((e) => {
                          var t;
                          const l =
                              (null ==
                              (t = null == e ? void 0 : e.componentProps)
                                ? void 0
                                : t.on) || {},
                            a = {};
                          for (const o in l)
                            l[o] &&
                              (a[`on${gt(o)}`] = (...e) => {
                                l[o](...e);
                              });
                          const n = {
                            clearable: !0,
                            ...e.componentProps,
                            ...a,
                          };
                          return (
                            n.slots && delete n.slots,
                            n.on && delete n.on,
                            n
                          );
                        })(e),
                        {
                          style:
                            (null == (a = e.componentProps)
                              ? void 0
                              : a.style) || {},
                        },
                      ),
                      { ...n },
                    );
                  };
                  return M(P, null, [s()]);
                }
              },
            };
            return (
              (null == e ? void 0 : e.labelMessage) &&
                (o.label = () =>
                  M(P, null, [
                    M("span", null, [e.label]),
                    M(
                      Nt,
                      { placement: "top", "raw-content": !0 },
                      {
                        content: () =>
                          M("span", { innerHTML: e.labelMessage }, null),
                        default: () =>
                          M(
                            kt,
                            {
                              icon: "ep:warning",
                              size: 16,
                              color: "var(--el-color-primary)",
                              class: "ml-2px relative top-1px",
                            },
                            null,
                          ),
                      },
                    ),
                  ])),
              (null ==
              (l =
                null == (t = null == e ? void 0 : e.formItemProps)
                  ? void 0
                  : t.slots)
                ? void 0
                : l.label) &&
                (o.label = (...t) => {
                  var l, a;
                  return null ==
                    (a =
                      null == (l = null == e ? void 0 : e.formItemProps)
                        ? void 0
                        : l.slots)
                    ? void 0
                    : a.label(...t);
                }),
              (null ==
              (n =
                null == (a = null == e ? void 0 : e.formItemProps)
                  ? void 0
                  : a.slots)
                ? void 0
                : n.error) &&
                (o.error = (...t) => {
                  var l, a;
                  return null ==
                    (a =
                      null == (l = null == e ? void 0 : e.formItemProps)
                        ? void 0
                        : l.slots)
                    ? void 0
                    : a.error(...t);
                }),
              M(
                xt,
                j(
                  {
                    ref: (t) => {
                      return ((l = t), (a = e.field), void (u.value[a] = l));
                      var l, a;
                    },
                  },
                  e.formItemProps || {},
                  { prop: e.field, label: e.label || "" },
                ),
                Zr(o) ? o : { default: () => [o] },
              )
            );
          };
        return () =>
          M(
            wt,
            j(
              { ref: n },
              (() => {
                const e = [
                    "schema",
                    "isCol",
                    "autoSetPlaceholder",
                    "isCustom",
                    "model",
                  ],
                  t = { ...T(r) };
                for (const l in t) -1 !== e.indexOf(l) && delete t[l];
                return t;
              })(),
              { model: T(r).isCustom ? T(r).model : c, class: li },
            ),
            {
              default: () => {
                const { isCustom: e } = T(r);
                return e
                  ? Ur(t, "default")
                  : (() => {
                      let e;
                      const { isCol: t } = T(r);
                      return t
                        ? M(
                            St,
                            { gutter: 20 },
                            Zr((e = h())) ? e : { default: () => [e] },
                          )
                        : h();
                    })();
              },
            },
          );
      },
    }),
    [["__scopeId", "data-v-eaeb8dcf"]],
  ),
  ni = () => {
    const e = b(),
      t = b(),
      l = async () => {
        await H();
        const t = T(e);
        return t;
      };
    return {
      formRegister: (l, a) => {
        ((e.value = l), (t.value = a));
      },
      formMethods: {
        setProps: async (e = {}) => {
          const t = await l();
          (null == t || t.setProps(e),
            e.model && (null == t || t.setValues(e.model)));
        },
        setValues: async (e) => {
          const t = await l();
          null == t || t.setValues(e);
        },
        setValue: async (e, t) => {
          const a = await l();
          null == a || a.setValue(e, t);
        },
        setSchema: async (e) => {
          const t = await l();
          null == t || t.setSchema(e);
        },
        addSchema: async (e, t) => {
          const a = await l();
          null == a || a.addSchema(e, t);
        },
        delSchema: async (e) => {
          const t = await l();
          null == t || t.delSchema(e);
        },
        getFormData: async () => {
          const e = await l();
          return null == e ? void 0 : e.formModel;
        },
        getComponentExpose: async (e) => {
          const t = await l();
          return null == t ? void 0 : t.getComponentExpose(e);
        },
        getFormItemExpose: async (e) => {
          const t = await l();
          return null == t ? void 0 : t.getFormItemExpose(e);
        },
        getElFormExpose: async () => (await l(), T(t)),
        getFormExpose: async () => (await l(), T(e)),
      },
    };
  };
export { ai as F, Xr as a, Ur as g, Ml as i, Sl as o, Vl as t, ni as u };
