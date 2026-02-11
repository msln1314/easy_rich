import {
  cl as e,
  ao as l,
  f as t,
  aq as o,
  cc as a,
  bu as n,
  w as s,
  k as i,
  _ as r,
  e as u,
  u as p,
  L as d,
  bw as c,
  aj as v,
  as as h,
  a0 as m,
  aH as f,
  o as b,
  j as g,
  q as y,
  y as C,
  z as S,
  s as O,
  aY as x,
  r as T,
  a2 as w,
  at as L,
  n as I,
  a_ as E,
  aB as M,
  ab as P,
  b8 as V,
  bv as k,
  b9 as D,
  ba as K,
  b3 as q,
  cm as z,
  aJ as A,
  i as W,
  cn as B,
  ap as F,
  aA as H,
  g as R,
  G as j,
  E as _,
  a as $,
  bc as Q,
  bd as N,
  am as G,
  co as U,
  b1 as J,
  Z as X,
  x as Y,
  m as Z,
  l as ee,
  D as le,
  a1 as te,
  a5 as oe,
  F as ae,
  aX as ne,
  be as se,
  ak as ie,
  p as re,
  t as ue,
  a8 as pe,
} from "./index-6b60d190.js";
import { E as de, u as ce, a as ve } from "./el-popper-09548d54.js";
import { i as he, E as me } from "./el-input-38d674e5.js";
import { E as fe, t as be } from "./index-b7c1540b.js";
import { e as ge } from "./strings-00317668.js";
import { U as ye, C as Ce } from "./event-5568c9d8.js";
import { s as Se } from "./scroll-6dba6951.js";
import { i as Oe } from "./isEqual-b8d86c27.js";
import { d as xe } from "./debounce-5c500a3d.js";
import { C as Te } from "./index-fdfa028a.js";
import { i as we } from "./validator-f032316f.js";
const Le = Symbol("ElSelectGroup"),
  Ie = Symbol("ElSelect");
var Ee = r(
  u({
    name: "ElOption",
    componentName: "ElOption",
    props: {
      value: { required: !0, type: [String, Number, Boolean, Object] },
      label: [String, Number],
      created: Boolean,
      disabled: { type: Boolean, default: !1 },
    },
    setup(e) {
      const r = p("select"),
        u = t(() => [
          r.be("dropdown", "item"),
          r.is("disabled", i(g)),
          { selected: i(b), hover: i(O) },
        ]),
        m = d({
          index: -1,
          groupDisabled: !1,
          visible: !0,
          hitState: !1,
          hover: !1,
        }),
        {
          currentLabel: f,
          itemSelected: b,
          isDisabled: g,
          select: y,
          hoverItem: C,
        } = (function (e, r) {
          const u = l(Ie),
            p = l(Le, { disabled: !1 }),
            d = t(
              () =>
                "[object object]" ===
                Object.prototype.toString.call(e.value).toLowerCase(),
            ),
            c = t(() =>
              u.props.multiple
                ? g(u.props.modelValue, e.value)
                : y(e.value, u.props.modelValue),
            ),
            v = t(() => {
              if (u.props.multiple) {
                const e = u.props.modelValue || [];
                return (
                  !c.value &&
                  e.length >= u.props.multipleLimit &&
                  u.props.multipleLimit > 0
                );
              }
              return !1;
            }),
            h = t(() => e.label || (d.value ? "" : e.value)),
            m = t(() => e.value || e.label || ""),
            f = t(() => e.disabled || r.groupDisabled || v.value),
            b = o(),
            g = (e = [], l) => {
              if (d.value) {
                const t = u.props.valueKey;
                return e && e.some((e) => a(n(e, t)) === n(l, t));
              }
              return e && e.includes(l);
            },
            y = (e, l) => {
              if (d.value) {
                const { valueKey: t } = u.props;
                return n(e, t) === n(l, t);
              }
              return e === l;
            };
          (s(
            () => h.value,
            () => {
              e.created || u.props.remote || u.setSelected();
            },
          ),
            s(
              () => e.value,
              (l, t) => {
                const { remote: o, valueKey: a } = u.props;
                if (
                  (Object.is(l, t) ||
                    (u.onOptionDestroy(t, b.proxy), u.onOptionCreate(b.proxy)),
                  !e.created && !o)
                ) {
                  if (
                    a &&
                    "object" == typeof l &&
                    "object" == typeof t &&
                    l[a] === t[a]
                  )
                    return;
                  u.setSelected();
                }
              },
            ),
            s(
              () => p.disabled,
              () => {
                r.groupDisabled = p.disabled;
              },
              { immediate: !0 },
            ));
          const { queryChange: C } = a(u);
          return (
            s(
              C,
              (l) => {
                const { query: t } = i(l),
                  o = new RegExp(ge(t), "i");
                ((r.visible = o.test(h.value) || e.created),
                  r.visible || u.filteredOptionsCount--);
              },
              { immediate: !0 },
            ),
            {
              select: u,
              currentLabel: h,
              currentValue: m,
              itemSelected: c,
              isDisabled: f,
              hoverItem: () => {
                e.disabled ||
                  p.disabled ||
                  (u.hoverIndex = u.optionsArray.indexOf(b.proxy));
              },
            }
          );
        })(e, m),
        { visible: S, hover: O } = c(m),
        x = o().proxy;
      return (
        y.onOptionCreate(x),
        v(() => {
          const e = x.value,
            { selected: l } = y,
            t = (y.props.multiple ? l : [l]).some((e) => e.value === x.value);
          (h(() => {
            y.cachedOptions.get(e) !== x || t || y.cachedOptions.delete(e);
          }),
            y.onOptionDestroy(e, x));
        }),
        {
          ns: r,
          containerKls: u,
          currentLabel: f,
          itemSelected: b,
          isDisabled: g,
          select: y,
          hoverItem: C,
          visible: S,
          hover: O,
          selectOptionClick: function () {
            !0 !== e.disabled &&
              !0 !== m.groupDisabled &&
              y.handleOptionSelect(x);
          },
          states: m,
        }
      );
    },
  }),
  [
    [
      "render",
      function (e, l, t, o, a, n) {
        return m(
          (b(),
          g(
            "li",
            {
              class: O(e.containerKls),
              onMouseenter:
                l[0] || (l[0] = (...l) => e.hoverItem && e.hoverItem(...l)),
              onClick:
                l[1] ||
                (l[1] = x(
                  (...l) => e.selectOptionClick && e.selectOptionClick(...l),
                  ["stop"],
                )),
            },
            [
              y(e.$slots, "default", {}, () => [
                C("span", null, S(e.currentLabel), 1),
              ]),
            ],
            34,
          )),
          [[f, e.visible]],
        );
      },
    ],
    [
      "__file",
      "/home/runner/work/element-plus/element-plus/packages/components/select/src/option.vue",
    ],
  ],
);
var Me = r(
  u({
    name: "ElSelectDropdown",
    componentName: "ElSelectDropdown",
    setup() {
      const e = l(Ie),
        o = p("select"),
        a = t(() => e.props.popperClass),
        n = t(() => e.props.multiple),
        s = t(() => e.props.fitInputWidth),
        i = T("");
      function r() {
        var l;
        i.value = `${null == (l = e.selectWrapper) ? void 0 : l.offsetWidth}px`;
      }
      return (
        w(() => {
          (r(), L(e.selectWrapper, r));
        }),
        {
          ns: o,
          minWidth: i,
          popperClass: a,
          isMultiple: n,
          isFitInputWidth: s,
        }
      );
    },
  }),
  [
    [
      "render",
      function (e, l, t, o, a, n) {
        return (
          b(),
          g(
            "div",
            {
              class: O([
                e.ns.b("dropdown"),
                e.ns.is("multiple", e.isMultiple),
                e.popperClass,
              ]),
              style: I({
                [e.isFitInputWidth ? "width" : "minWidth"]: e.minWidth,
              }),
            },
            [y(e.$slots, "default")],
            6,
          )
        );
      },
    ],
    [
      "__file",
      "/home/runner/work/element-plus/element-plus/packages/components/select/src/select-dropdown.vue",
    ],
  ],
);
const Pe = (l, o, r) => {
  const { t: u } = E(),
    d = p("select");
  M(
    {
      from: "suffixTransition",
      replacement: "override style scheme",
      version: "2.3.0",
      scope: "props",
      ref: "https://element-plus.org/en-US/component/select.html#select-attributes",
    },
    t(() => !1 === l.suffixTransition),
  );
  const c = T(null),
    v = T(null),
    m = T(null),
    f = T(null),
    b = T(null),
    g = T(null),
    y = T(null),
    C = T(null),
    S = T(-1),
    O = P({ query: "" }),
    x = P(""),
    w = T([]);
  let L = 0;
  const { form: I, formItem: j } = V(),
    _ = t(() => !l.filterable || l.multiple || !o.visible),
    $ = t(() => l.disabled || (null == I ? void 0 : I.disabled)),
    Q = t(() => {
      const e = l.multiple
        ? Array.isArray(l.modelValue) && l.modelValue.length > 0
        : void 0 !== l.modelValue &&
          null !== l.modelValue &&
          "" !== l.modelValue;
      return l.clearable && !$.value && o.inputHovering && e;
    }),
    N = t(() =>
      l.remote && l.filterable && !l.remoteShowSuffix ? "" : l.suffixIcon,
    ),
    G = t(() => d.is("reverse", N.value && o.visible && l.suffixTransition)),
    U = t(
      () =>
        (null == I ? void 0 : I.statusIcon) &&
        (null == j ? void 0 : j.validateState) &&
        k[null == j ? void 0 : j.validateState],
    ),
    J = t(() => (l.remote ? 300 : 0)),
    X = t(() =>
      l.loading
        ? l.loadingText || u("el.select.loading")
        : (!l.remote || "" !== o.query || 0 !== o.options.size) &&
          (l.filterable &&
          o.query &&
          o.options.size > 0 &&
          0 === o.filteredOptionsCount
            ? l.noMatchText || u("el.select.noMatch")
            : 0 === o.options.size
              ? l.noDataText || u("el.select.noData")
              : null),
    ),
    Y = t(() => {
      const e = Array.from(o.options.values()),
        l = [];
      return (
        w.value.forEach((t) => {
          const o = e.findIndex((e) => e.currentLabel === t);
          o > -1 && l.push(e[o]);
        }),
        l.length ? l : e
      );
    }),
    Z = t(() => Array.from(o.cachedOptions.values())),
    ee = t(() => {
      const e = Y.value
        .filter((e) => !e.created)
        .some((e) => e.currentLabel === o.query);
      return l.filterable && l.allowCreate && "" !== o.query && !e;
    }),
    le = D(),
    te = t(() => (["small"].includes(le.value) ? "small" : "default")),
    oe = t({
      get: () => o.visible && !1 !== X.value,
      set(e) {
        o.visible = e;
      },
    });
  (s(
    [() => $.value, () => le.value, () => (null == I ? void 0 : I.size)],
    () => {
      h(() => {
        ae();
      });
    },
  ),
    s(
      () => l.placeholder,
      (e) => {
        o.cachedPlaceHolder = o.currentPlaceholder = e;
        l.multiple &&
          Array.isArray(l.modelValue) &&
          l.modelValue.length > 0 &&
          (o.currentPlaceholder = "");
      },
    ),
    s(
      () => l.modelValue,
      (e, t) => {
        (l.multiple &&
          (ae(),
          (e && e.length > 0) || (v.value && "" !== o.query)
            ? (o.currentPlaceholder = "")
            : (o.currentPlaceholder = o.cachedPlaceHolder),
          l.filterable && !l.reserveKeyword && ((o.query = ""), ne(o.query))),
          re(),
          l.filterable && !l.multiple && (o.inputLength = 20),
          !Oe(e, t) &&
            l.validateEvent &&
            (null == j || j.validate("change").catch((e) => K())));
      },
      { flush: "post", deep: !0 },
    ),
    s(
      () => o.visible,
      (e) => {
        var t, a, n, s, i;
        (e
          ? (null == (a = null == (t = f.value) ? void 0 : t.updatePopper) ||
              a.call(t),
            l.filterable &&
              ((o.filteredOptionsCount = o.optionsCount),
              (o.query = l.remote ? "" : o.selectedLabel),
              null == (s = null == (n = m.value) ? void 0 : n.focus) ||
                s.call(n),
              l.multiple
                ? null == (i = v.value) || i.focus()
                : o.selectedLabel &&
                  ((o.currentPlaceholder = `${o.selectedLabel}`),
                  (o.selectedLabel = "")),
              ne(o.query),
              l.multiple || l.remote || ((O.value.query = ""), z(O), z(x))))
          : (l.filterable &&
              (q(l.filterMethod) && l.filterMethod(""),
              q(l.remoteMethod) && l.remoteMethod("")),
            (o.query = ""),
            (o.previousQuery = null),
            (o.selectedLabel = ""),
            (o.inputLength = 20),
            (o.menuVisibleOnFocus = !1),
            pe(),
            h(() => {
              v.value &&
                "" === v.value.value &&
                0 === o.selected.length &&
                (o.currentPlaceholder = o.cachedPlaceHolder);
            }),
            l.multiple ||
              (o.selected &&
                (l.filterable &&
                l.allowCreate &&
                o.createdSelected &&
                o.createdLabel
                  ? (o.selectedLabel = o.createdLabel)
                  : (o.selectedLabel = o.selected.currentLabel),
                l.filterable && (o.query = o.selectedLabel)),
              l.filterable && (o.currentPlaceholder = o.cachedPlaceHolder))),
          r.emit("visible-change", e));
      },
    ),
    s(
      () => o.options.entries(),
      () => {
        var e, t, a;
        if (!A) return;
        (null == (t = null == (e = f.value) ? void 0 : e.updatePopper) ||
          t.call(e),
          l.multiple && ae());
        const n =
          (null == (a = y.value) ? void 0 : a.querySelectorAll("input")) || [];
        (Array.from(n).includes(document.activeElement) || re(),
          l.defaultFirstOption &&
            (l.filterable || l.remote) &&
            o.filteredOptionsCount &&
            ie());
      },
      { flush: "post" },
    ),
    s(
      () => o.hoverIndex,
      (e) => {
        (W(e) && e > -1 ? (S.value = Y.value[e] || {}) : (S.value = {}),
          Y.value.forEach((e) => {
            e.hover = S.value === e;
          }));
      },
    ));
  const ae = () => {
      h(() => {
        var l, t;
        if (!c.value) return;
        const a = c.value.$el.querySelector("input");
        L = L || (a.clientHeight > 0 ? a.clientHeight + 2 : 0);
        const n = g.value,
          s =
            ((i = le.value || (null == I ? void 0 : I.size)),
            e[i || "default"]);
        var i;
        const r = le.value || s === L || L <= 0 ? s : L;
        (!(null === a.offsetParent) &&
          (a.style.height =
            (0 === o.selected.length
              ? r
              : Math.max(
                  n ? n.clientHeight + (n.clientHeight > r ? 6 : 0) : 0,
                  r,
                )) -
            2 +
            "px"),
          o.visible &&
            !1 !== X.value &&
            (null == (t = null == (l = f.value) ? void 0 : l.updatePopper) ||
              t.call(l)));
      });
    },
    ne = async (e) => {
      o.previousQuery === e ||
        o.isOnComposition ||
        (null !== o.previousQuery || (!q(l.filterMethod) && !q(l.remoteMethod))
          ? ((o.previousQuery = e),
            h(() => {
              var e, l;
              o.visible &&
                (null ==
                  (l = null == (e = f.value) ? void 0 : e.updatePopper) ||
                  l.call(e));
            }),
            (o.hoverIndex = -1),
            l.multiple &&
              l.filterable &&
              h(() => {
                const e = 15 * v.value.value.length + 20;
                ((o.inputLength = l.collapseTags ? Math.min(50, e) : e),
                  se(),
                  ae());
              }),
            l.remote && q(l.remoteMethod)
              ? ((o.hoverIndex = -1), l.remoteMethod(e))
              : q(l.filterMethod)
                ? (l.filterMethod(e), z(x))
                : ((o.filteredOptionsCount = o.optionsCount),
                  (O.value.query = e),
                  z(O),
                  z(x)),
            l.defaultFirstOption &&
              (l.filterable || l.remote) &&
              o.filteredOptionsCount &&
              (await h(), ie()))
          : (o.previousQuery = e));
    },
    se = () => {
      "" !== o.currentPlaceholder &&
        (o.currentPlaceholder = v.value.value ? "" : o.cachedPlaceHolder);
    },
    ie = () => {
      const e = Y.value.filter(
          (e) => e.visible && !e.disabled && !e.states.groupDisabled,
        ),
        l = e.find((e) => e.created),
        t = e[0];
      o.hoverIndex = Te(Y.value, l || t);
    },
    re = () => {
      var e;
      if (!l.multiple) {
        const t = ue(l.modelValue);
        return (
          (null == (e = t.props) ? void 0 : e.created)
            ? ((o.createdLabel = t.props.value), (o.createdSelected = !0))
            : (o.createdSelected = !1),
          (o.selectedLabel = t.currentLabel),
          (o.selected = t),
          void (l.filterable && (o.query = o.selectedLabel))
        );
      }
      o.selectedLabel = "";
      const t = [];
      (Array.isArray(l.modelValue) &&
        l.modelValue.forEach((e) => {
          t.push(ue(e));
        }),
        (o.selected = t),
        h(() => {
          ae();
        }));
    },
    ue = (e) => {
      let t;
      const a = "object" === B(e).toLowerCase(),
        s = "null" === B(e).toLowerCase(),
        i = "undefined" === B(e).toLowerCase();
      for (let u = o.cachedOptions.size - 1; u >= 0; u--) {
        const o = Z.value[u];
        if (a ? n(o.value, l.valueKey) === n(e, l.valueKey) : o.value === e) {
          t = {
            value: e,
            currentLabel: o.currentLabel,
            isDisabled: o.isDisabled,
          };
          break;
        }
      }
      if (t) return t;
      const r = { value: e, currentLabel: a ? e.label : s || i ? "" : e };
      return (l.multiple && (r.hitState = !1), r);
    },
    pe = () => {
      setTimeout(() => {
        const e = l.valueKey;
        l.multiple
          ? o.selected.length > 0
            ? (o.hoverIndex = Math.min.apply(
                null,
                o.selected.map((l) =>
                  Y.value.findIndex((t) => n(t, e) === n(l, e)),
                ),
              ))
            : (o.hoverIndex = -1)
          : (o.hoverIndex = Y.value.findIndex((e) => Ve(e) === Ve(o.selected)));
      }, 300);
    },
    de = () => {
      var e;
      o.inputWidth = null == (e = c.value) ? void 0 : e.$el.offsetWidth;
    },
    ce = xe(() => {
      l.filterable &&
        o.query !== o.selectedLabel &&
        ((o.query = o.selectedLabel), ne(o.query));
    }, J.value),
    ve = xe((e) => {
      ne(e.target.value);
    }, J.value),
    me = (e) => {
      Oe(l.modelValue, e) || r.emit(Ce, e);
    },
    fe = (e, t) => {
      const a = o.selected.indexOf(t);
      if (a > -1 && !$.value) {
        const e = l.modelValue.slice();
        (e.splice(a, 1), r.emit(ye, e), me(e), r.emit("remove-tag", t.value));
      }
      (e.stopPropagation(), Ee());
    },
    be = (e) => {
      e.stopPropagation();
      const t = l.multiple ? [] : "";
      if (!R(t)) for (const l of o.selected) l.isDisabled && t.push(l.value);
      (r.emit(ye, t),
        me(t),
        (o.hoverIndex = -1),
        (o.visible = !1),
        r.emit("clear"),
        Ee());
    },
    ge = (e) => {
      var t;
      if (l.multiple) {
        const a = (l.modelValue || []).slice(),
          n = Te(a, e.value);
        (n > -1
          ? a.splice(n, 1)
          : (l.multipleLimit <= 0 || a.length < l.multipleLimit) &&
            a.push(e.value),
          r.emit(ye, a),
          me(a),
          e.created && ((o.query = ""), ne(""), (o.inputLength = 20)),
          l.filterable && (null == (t = v.value) || t.focus()));
      } else (r.emit(ye, e.value), me(e.value), (o.visible = !1));
      (we(),
        o.visible ||
          h(() => {
            Le(e);
          }));
    },
    Te = (e = [], t) => {
      if (!F(t)) return e.indexOf(t);
      const o = l.valueKey;
      let s = -1;
      return (e.some((e, l) => a(n(e, o)) === n(t, o) && ((s = l), !0)), s);
    },
    we = () => {
      const e = v.value || c.value;
      e && (null == e || e.focus());
    },
    Le = (e) => {
      var l, t, o, a, n;
      const s = Array.isArray(e) ? e[0] : e;
      let i = null;
      if (null == s ? void 0 : s.value) {
        const e = Y.value.filter((e) => e.value === s.value);
        e.length > 0 && (i = e[0].$el);
      }
      if (f.value && i) {
        const e =
          null ==
          (a =
            null ==
            (o =
              null == (t = null == (l = f.value) ? void 0 : l.popperRef)
                ? void 0
                : t.contentRef)
              ? void 0
              : o.querySelector)
            ? void 0
            : a.call(o, `.${d.be("dropdown", "wrap")}`);
        e && Se(e, i);
      }
      null == (n = C.value) || n.handleScroll();
    },
    Ie = (e) => {
      if (!Array.isArray(o.selected)) return;
      const l = o.selected[o.selected.length - 1];
      return l
        ? !0 === e || !1 === e
          ? ((l.hitState = e), e)
          : ((l.hitState = !l.hitState), l.hitState)
        : void 0;
    },
    Ee = () => {
      var e, l;
      o.visible
        ? null == (e = v.value || c.value) || e.focus()
        : null == (l = c.value) || l.focus();
    },
    Me = () => {
      o.visible = !1;
    },
    Pe = (e) => {
      (e && !o.mouseEnter) ||
        $.value ||
        (o.menuVisibleOnFocus
          ? (o.menuVisibleOnFocus = !1)
          : (f.value && f.value.isFocusInsideContent()) ||
            (o.visible = !o.visible),
        Ee());
    },
    Ve = (e) => (F(e.value) ? n(e.value, l.valueKey) : e.value),
    ke = t(() => Y.value.filter((e) => e.visible).every((e) => e.disabled)),
    De = t(() => o.selected.slice(0, l.maxCollapseTags)),
    Ke = t(() => o.selected.slice(l.maxCollapseTags)),
    qe = (e) => {
      if (o.visible) {
        if (
          0 !== o.options.size &&
          0 !== o.filteredOptionsCount &&
          !o.isOnComposition &&
          !ke.value
        ) {
          "next" === e
            ? (o.hoverIndex++,
              o.hoverIndex === o.options.size && (o.hoverIndex = 0))
            : "prev" === e &&
              (o.hoverIndex--,
              o.hoverIndex < 0 && (o.hoverIndex = o.options.size - 1));
          const l = Y.value[o.hoverIndex];
          ((!0 !== l.disabled && !0 !== l.states.groupDisabled && l.visible) ||
            qe(e),
            h(() => Le(S.value)));
        }
      } else o.visible = !0;
    },
    ze = t(() => ({
      maxWidth: i(o.inputWidth) - 32 - (U.value ? 22 : 0) + "px",
      width: "100%",
    }));
  return {
    optionList: w,
    optionsArray: Y,
    selectSize: le,
    handleResize: () => {
      var e, t;
      (de(),
        null == (t = null == (e = f.value) ? void 0 : e.updatePopper) ||
          t.call(e),
        l.multiple && ae());
    },
    debouncedOnInputChange: ce,
    debouncedQueryChange: ve,
    deletePrevTag: (e) => {
      if (e.code !== H.delete) {
        if (e.target.value.length <= 0 && !Ie()) {
          const e = l.modelValue.slice();
          (e.pop(), r.emit(ye, e), me(e));
        }
        1 === e.target.value.length &&
          0 === l.modelValue.length &&
          (o.currentPlaceholder = o.cachedPlaceHolder);
      }
    },
    deleteTag: fe,
    deleteSelected: be,
    handleOptionSelect: ge,
    scrollToOption: Le,
    readonly: _,
    resetInputHeight: ae,
    showClose: Q,
    iconComponent: N,
    iconReverse: G,
    showNewOption: ee,
    collapseTagSize: te,
    setSelected: re,
    managePlaceholder: se,
    selectDisabled: $,
    emptyText: X,
    toggleLastOptionHitState: Ie,
    resetInputState: (e) => {
      (e.code !== H.backspace && Ie(!1),
        (o.inputLength = 15 * v.value.value.length + 20),
        ae());
    },
    handleComposition: (e) => {
      const l = e.target.value;
      if ("compositionend" === e.type)
        ((o.isOnComposition = !1), h(() => ne(l)));
      else {
        const e = l[l.length - 1] || "";
        o.isOnComposition = !he(e);
      }
    },
    onOptionCreate: (e) => {
      (o.optionsCount++,
        o.filteredOptionsCount++,
        o.options.set(e.value, e),
        o.cachedOptions.set(e.value, e));
    },
    onOptionDestroy: (e, l) => {
      o.options.get(e) === l &&
        (o.optionsCount--, o.filteredOptionsCount--, o.options.delete(e));
    },
    handleMenuEnter: () => {
      h(() => Le(o.selected));
    },
    handleFocus: (e) => {
      o.focused ||
        ((l.automaticDropdown || l.filterable) &&
          (l.filterable && !o.visible && (o.menuVisibleOnFocus = !0),
          (o.visible = !0)),
        (o.focused = !0),
        r.emit("focus", e));
    },
    focus: Ee,
    blur: () => {
      var e, l, t;
      ((o.visible = !1),
        null == (e = c.value) || e.blur(),
        null == (t = null == (l = m.value) ? void 0 : l.blur) || t.call(l));
    },
    handleBlur: (e) => {
      var l, t, a;
      (null == (l = f.value) ? void 0 : l.isFocusInsideContent(e)) ||
        (null == (t = b.value) ? void 0 : t.isFocusInsideContent(e)) ||
        (null == (a = y.value) ? void 0 : a.contains(e.relatedTarget)) ||
        (o.visible && Me(), (o.focused = !1), r.emit("blur", e));
    },
    handleClearClick: (e) => {
      be(e);
    },
    handleClose: Me,
    handleKeydownEscape: (e) => {
      o.visible && (e.preventDefault(), e.stopPropagation(), (o.visible = !1));
    },
    toggleMenu: Pe,
    selectOption: () => {
      o.visible ? Y.value[o.hoverIndex] && ge(Y.value[o.hoverIndex]) : Pe();
    },
    getValueKey: Ve,
    navigateOptions: qe,
    handleDeleteTooltipTag: (e, l) => {
      var t, o;
      (fe(e, l),
        null == (o = null == (t = b.value) ? void 0 : t.updatePopper) ||
          o.call(t));
    },
    dropMenuVisible: oe,
    queryChange: O,
    groupQueryChange: x,
    showTagList: De,
    collapseTagList: Ke,
    selectTagsStyle: ze,
    reference: c,
    input: v,
    iOSInput: m,
    tooltipRef: f,
    tagTooltipRef: b,
    tags: g,
    selectWrapper: y,
    scrollbar: C,
    handleMouseEnter: () => {
      o.mouseEnter = !0;
    },
    handleMouseLeave: () => {
      o.mouseEnter = !1;
    },
  };
};
var Ve = u({
  name: "ElOptions",
  emits: ["update-options"],
  setup(e, { slots: l, emit: t }) {
    let o = [];
    return () => {
      var e, a;
      const n = null == (e = l.default) ? void 0 : e.call(l),
        s = [];
      return (
        n.length &&
          (function e(l) {
            Array.isArray(l) &&
              l.forEach((l) => {
                var t, o, a, n;
                const i =
                  null == (t = (null == l ? void 0 : l.type) || {})
                    ? void 0
                    : t.name;
                "ElOptionGroup" === i
                  ? e(
                      R(l.children) ||
                        Array.isArray(l.children) ||
                        !q(null == (o = l.children) ? void 0 : o.default)
                        ? l.children
                        : null == (a = l.children)
                          ? void 0
                          : a.default(),
                    )
                  : "ElOption" === i
                    ? s.push(null == (n = l.props) ? void 0 : n.label)
                    : Array.isArray(l.children) && e(l.children);
              });
          })(null == (a = n[0]) ? void 0 : a.children),
        (function (e, l) {
          if (e.length !== l.length) return !1;
          for (const [t] of e.entries()) if (e[t] != l[t]) return !1;
          return !0;
        })(s, o) || ((o = s), t("update-options", s)),
        n
      );
    };
  },
});
const ke = "ElSelect",
  De = u({
    name: ke,
    componentName: ke,
    components: {
      ElInput: me,
      ElSelectMenu: Me,
      ElOption: Ee,
      ElOptions: Ve,
      ElTag: fe,
      ElScrollbar: j,
      ElTooltip: de,
      ElIcon: _,
    },
    directives: { ClickOutside: Te },
    props: {
      name: String,
      id: String,
      modelValue: {
        type: [Array, String, Number, Boolean, Object],
        default: void 0,
      },
      autocomplete: { type: String, default: "off" },
      automaticDropdown: Boolean,
      size: { type: String, validator: we },
      effect: { type: String, default: "light" },
      disabled: Boolean,
      clearable: Boolean,
      filterable: Boolean,
      allowCreate: Boolean,
      loading: Boolean,
      popperClass: { type: String, default: "" },
      popperOptions: { type: Object, default: () => ({}) },
      remote: Boolean,
      loadingText: String,
      noMatchText: String,
      noDataText: String,
      remoteMethod: Function,
      filterMethod: Function,
      multiple: Boolean,
      multipleLimit: { type: Number, default: 0 },
      placeholder: { type: String },
      defaultFirstOption: Boolean,
      reserveKeyword: { type: Boolean, default: !0 },
      valueKey: { type: String, default: "value" },
      collapseTags: Boolean,
      collapseTagsTooltip: { type: Boolean, default: !1 },
      maxCollapseTags: { type: Number, default: 1 },
      teleported: ce.teleported,
      persistent: { type: Boolean, default: !0 },
      clearIcon: { type: $, default: Q },
      fitInputWidth: { type: Boolean, default: !1 },
      suffixIcon: { type: $, default: N },
      tagType: { ...be.type, default: "info" },
      validateEvent: { type: Boolean, default: !0 },
      remoteShowSuffix: { type: Boolean, default: !1 },
      suffixTransition: { type: Boolean, default: !0 },
      placement: { type: String, values: ve, default: "bottom-start" },
    },
    emits: [ye, Ce, "remove-tag", "clear", "visible-change", "focus", "blur"],
    setup(e, l) {
      const o = p("select"),
        a = p("input"),
        { t: n } = E(),
        s = (function (e) {
          const { t: l } = E();
          return d({
            options: new Map(),
            cachedOptions: new Map(),
            createdLabel: null,
            createdSelected: !1,
            selected: e.multiple ? [] : {},
            inputLength: 20,
            inputWidth: 0,
            optionsCount: 0,
            filteredOptionsCount: 0,
            visible: !1,
            selectedLabel: "",
            hoverIndex: -1,
            query: "",
            previousQuery: null,
            inputHovering: !1,
            cachedPlaceHolder: "",
            currentPlaceholder: l("el.select.placeholder"),
            menuVisibleOnFocus: !1,
            isOnComposition: !1,
            prefixWidth: 11,
            mouseEnter: !1,
            focused: !1,
          });
        })(e),
        {
          optionList: r,
          optionsArray: u,
          selectSize: v,
          readonly: m,
          handleResize: f,
          collapseTagSize: b,
          debouncedOnInputChange: g,
          debouncedQueryChange: y,
          deletePrevTag: C,
          deleteTag: S,
          deleteSelected: O,
          handleOptionSelect: x,
          scrollToOption: T,
          setSelected: I,
          resetInputHeight: M,
          managePlaceholder: P,
          showClose: V,
          selectDisabled: k,
          iconComponent: D,
          iconReverse: K,
          showNewOption: q,
          emptyText: z,
          toggleLastOptionHitState: A,
          resetInputState: W,
          handleComposition: B,
          onOptionCreate: F,
          onOptionDestroy: H,
          handleMenuEnter: R,
          handleFocus: j,
          focus: _,
          blur: $,
          handleBlur: Q,
          handleClearClick: N,
          handleClose: J,
          handleKeydownEscape: X,
          toggleMenu: Y,
          selectOption: Z,
          getValueKey: ee,
          navigateOptions: le,
          handleDeleteTooltipTag: te,
          dropMenuVisible: oe,
          reference: ae,
          input: ne,
          iOSInput: se,
          tooltipRef: ie,
          tagTooltipRef: re,
          tags: ue,
          selectWrapper: pe,
          scrollbar: de,
          queryChange: ce,
          groupQueryChange: ve,
          handleMouseEnter: he,
          handleMouseLeave: me,
          showTagList: fe,
          collapseTagList: be,
          selectTagsStyle: ge,
        } = Pe(e, s, l),
        {
          inputWidth: Ce,
          selected: Se,
          inputLength: Oe,
          filteredOptionsCount: xe,
          visible: Te,
          selectedLabel: we,
          hoverIndex: Le,
          query: Ee,
          inputHovering: Me,
          currentPlaceholder: Ve,
          menuVisibleOnFocus: ke,
          isOnComposition: De,
          options: Ke,
          cachedOptions: qe,
          optionsCount: ze,
          prefixWidth: Ae,
        } = c(s),
        We = t(() => {
          const l = [o.b()],
            t = i(v);
          return (
            t && l.push(o.m(t)),
            e.disabled && l.push(o.m("disabled")),
            l
          );
        }),
        Be = t(() => [o.e("tags"), o.is("disabled", i(k))]),
        Fe = t(() => [
          o.b("tags-wrapper"),
          { "has-prefix": i(Ae) && i(Se).length },
        ]),
        He = t(() => [o.e("input"), o.is(i(v)), o.is("disabled", i(k))]),
        Re = t(() => [o.e("input"), o.is(i(v)), o.em("input", "iOS")]),
        je = t(() => [
          o.is("empty", !e.allowCreate && Boolean(i(Ee)) && 0 === i(xe)),
        ]),
        _e = t(() => ({
          maxWidth: `${i(Ce) > 123 ? i(Ce) - 123 : i(Ce) - 75}px`,
        })),
        $e = t(() => ({
          marginLeft: `${i(Ae)}px`,
          flexGrow: 1,
          width: i(Oe) / (i(Ce) - 32) + "%",
          maxWidth: i(Ce) - 42 + "px",
        }));
      (G(
        Ie,
        d({
          props: e,
          options: Ke,
          optionsArray: u,
          cachedOptions: qe,
          optionsCount: ze,
          filteredOptionsCount: xe,
          hoverIndex: Le,
          handleOptionSelect: x,
          onOptionCreate: F,
          onOptionDestroy: H,
          selectWrapper: pe,
          selected: Se,
          setSelected: I,
          queryChange: ce,
          groupQueryChange: ve,
        }),
      ),
        w(() => {
          ((s.cachedPlaceHolder = Ve.value =
            e.placeholder || (() => n("el.select.placeholder"))),
            e.multiple &&
              Array.isArray(e.modelValue) &&
              e.modelValue.length > 0 &&
              (Ve.value = ""),
            L(pe, f),
            e.remote && e.multiple && M(),
            h(() => {
              const e = ae.value && ae.value.$el;
              if (
                e &&
                ((Ce.value = e.getBoundingClientRect().width), l.slots.prefix)
              ) {
                const l = e.querySelector(`.${a.e("prefix")}`);
                Ae.value = Math.max(l.getBoundingClientRect().width + 11, 30);
              }
            }),
            I());
        }),
        e.multiple && !Array.isArray(e.modelValue) && l.emit(ye, []),
        !e.multiple && Array.isArray(e.modelValue) && l.emit(ye, ""));
      const Qe = t(() => {
        var e, l;
        return null == (l = null == (e = ie.value) ? void 0 : e.popperRef)
          ? void 0
          : l.contentRef;
      });
      return {
        isIOS: U,
        onOptionsRendered: (e) => {
          r.value = e;
        },
        prefixWidth: Ae,
        selectSize: v,
        readonly: m,
        handleResize: f,
        collapseTagSize: b,
        debouncedOnInputChange: g,
        debouncedQueryChange: y,
        deletePrevTag: C,
        deleteTag: S,
        handleDeleteTooltipTag: te,
        deleteSelected: O,
        handleOptionSelect: x,
        scrollToOption: T,
        inputWidth: Ce,
        selected: Se,
        inputLength: Oe,
        filteredOptionsCount: xe,
        visible: Te,
        selectedLabel: we,
        hoverIndex: Le,
        query: Ee,
        inputHovering: Me,
        currentPlaceholder: Ve,
        menuVisibleOnFocus: ke,
        isOnComposition: De,
        options: Ke,
        resetInputHeight: M,
        managePlaceholder: P,
        showClose: V,
        selectDisabled: k,
        iconComponent: D,
        iconReverse: K,
        showNewOption: q,
        emptyText: z,
        toggleLastOptionHitState: A,
        resetInputState: W,
        handleComposition: B,
        handleMenuEnter: R,
        handleFocus: j,
        focus: _,
        blur: $,
        handleBlur: Q,
        handleClearClick: N,
        handleClose: J,
        handleKeydownEscape: X,
        toggleMenu: Y,
        selectOption: Z,
        getValueKey: ee,
        navigateOptions: le,
        dropMenuVisible: oe,
        reference: ae,
        input: ne,
        iOSInput: se,
        tooltipRef: ie,
        popperPaneRef: Qe,
        tags: ue,
        selectWrapper: pe,
        scrollbar: de,
        wrapperKls: We,
        tagsKls: Be,
        tagWrapperKls: Fe,
        inputKls: He,
        iOSInputKls: Re,
        scrollbarKls: je,
        selectTagsStyle: ge,
        nsSelect: o,
        tagTextStyle: _e,
        inputStyle: $e,
        handleMouseEnter: he,
        handleMouseLeave: me,
        showTagList: fe,
        collapseTagList: be,
        tagTooltipRef: re,
      };
    },
  }),
  Ke = ["disabled", "autocomplete"],
  qe = ["disabled"],
  ze = {
    style: {
      height: "100%",
      display: "flex",
      "justify-content": "center",
      "align-items": "center",
    },
  };
var Ae = r(De, [
  [
    "render",
    function (e, l, t, o, a, n) {
      const s = J("el-tag"),
        i = J("el-tooltip"),
        r = J("el-icon"),
        u = J("el-input"),
        p = J("el-option"),
        d = J("el-options"),
        c = J("el-scrollbar"),
        v = J("el-select-menu"),
        h = X("click-outside");
      return m(
        (b(),
        g(
          "div",
          {
            ref: "selectWrapper",
            class: O(e.wrapperKls),
            onMouseenter:
              l[22] ||
              (l[22] = (...l) =>
                e.handleMouseEnter && e.handleMouseEnter(...l)),
            onMouseleave:
              l[23] ||
              (l[23] = (...l) =>
                e.handleMouseLeave && e.handleMouseLeave(...l)),
            onClick:
              l[24] ||
              (l[24] = x(
                (...l) => e.toggleMenu && e.toggleMenu(...l),
                ["stop"],
              )),
          },
          [
            Y(
              i,
              {
                ref: "tooltipRef",
                visible: e.dropMenuVisible,
                placement: e.placement,
                teleported: e.teleported,
                "popper-class": [e.nsSelect.e("popper"), e.popperClass],
                "popper-options": e.popperOptions,
                "fallback-placements": [
                  "bottom-start",
                  "top-start",
                  "right",
                  "left",
                ],
                effect: e.effect,
                pure: "",
                trigger: "click",
                transition: `${e.nsSelect.namespace.value}-zoom-in-top`,
                "stop-popper-mouse-event": !1,
                "gpu-acceleration": !1,
                persistent: e.persistent,
                onShow: e.handleMenuEnter,
              },
              {
                default: Z(() => [
                  C(
                    "div",
                    {
                      class: "select-trigger",
                      onMouseenter:
                        l[20] || (l[20] = (l) => (e.inputHovering = !0)),
                      onMouseleave:
                        l[21] || (l[21] = (l) => (e.inputHovering = !1)),
                    },
                    [
                      e.multiple
                        ? (b(),
                          g(
                            "div",
                            {
                              key: 0,
                              ref: "tags",
                              tabindex: "-1",
                              class: O(e.tagsKls),
                              style: I(e.selectTagsStyle),
                              onClick:
                                l[15] ||
                                (l[15] = (...l) => e.focus && e.focus(...l)),
                            },
                            [
                              e.collapseTags && e.selected.length
                                ? (b(),
                                  ee(
                                    le,
                                    {
                                      key: 0,
                                      onAfterLeave: e.resetInputHeight,
                                    },
                                    {
                                      default: Z(() => [
                                        C(
                                          "span",
                                          { class: O(e.tagWrapperKls) },
                                          [
                                            (b(!0),
                                            g(
                                              te,
                                              null,
                                              oe(
                                                e.showTagList,
                                                (l) => (
                                                  b(),
                                                  ee(
                                                    s,
                                                    {
                                                      key: e.getValueKey(l),
                                                      closable:
                                                        !e.selectDisabled &&
                                                        !l.isDisabled,
                                                      size: e.collapseTagSize,
                                                      hit: l.hitState,
                                                      type: e.tagType,
                                                      "disable-transitions": "",
                                                      onClose: (t) =>
                                                        e.deleteTag(t, l),
                                                    },
                                                    {
                                                      default: Z(() => [
                                                        C(
                                                          "span",
                                                          {
                                                            class: O(
                                                              e.nsSelect.e(
                                                                "tags-text",
                                                              ),
                                                            ),
                                                            style: I(
                                                              e.tagTextStyle,
                                                            ),
                                                          },
                                                          S(l.currentLabel),
                                                          7,
                                                        ),
                                                      ]),
                                                      _: 2,
                                                    },
                                                    1032,
                                                    [
                                                      "closable",
                                                      "size",
                                                      "hit",
                                                      "type",
                                                      "onClose",
                                                    ],
                                                  )
                                                ),
                                              ),
                                              128,
                                            )),
                                            e.selected.length >
                                            e.maxCollapseTags
                                              ? (b(),
                                                ee(
                                                  s,
                                                  {
                                                    key: 0,
                                                    closable: !1,
                                                    size: e.collapseTagSize,
                                                    type: e.tagType,
                                                    "disable-transitions": "",
                                                  },
                                                  {
                                                    default: Z(() => [
                                                      e.collapseTagsTooltip
                                                        ? (b(),
                                                          ee(
                                                            i,
                                                            {
                                                              key: 0,
                                                              ref: "tagTooltipRef",
                                                              disabled:
                                                                e.dropMenuVisible,
                                                              "fallback-placements":
                                                                [
                                                                  "bottom",
                                                                  "top",
                                                                  "right",
                                                                  "left",
                                                                ],
                                                              effect: e.effect,
                                                              placement:
                                                                "bottom",
                                                              teleported:
                                                                e.teleported,
                                                            },
                                                            {
                                                              default: Z(() => [
                                                                C(
                                                                  "span",
                                                                  {
                                                                    class: O(
                                                                      e.nsSelect.e(
                                                                        "tags-text",
                                                                      ),
                                                                    ),
                                                                  },
                                                                  "+ " +
                                                                    S(
                                                                      e.selected
                                                                        .length -
                                                                        e.maxCollapseTags,
                                                                    ),
                                                                  3,
                                                                ),
                                                              ]),
                                                              content: Z(() => [
                                                                C(
                                                                  "div",
                                                                  {
                                                                    class: O(
                                                                      e.nsSelect.e(
                                                                        "collapse-tags",
                                                                      ),
                                                                    ),
                                                                  },
                                                                  [
                                                                    (b(!0),
                                                                    g(
                                                                      te,
                                                                      null,
                                                                      oe(
                                                                        e.collapseTagList,
                                                                        (l) => (
                                                                          b(),
                                                                          g(
                                                                            "div",
                                                                            {
                                                                              key: e.getValueKey(
                                                                                l,
                                                                              ),
                                                                              class:
                                                                                O(
                                                                                  e.nsSelect.e(
                                                                                    "collapse-tag",
                                                                                  ),
                                                                                ),
                                                                            },
                                                                            [
                                                                              Y(
                                                                                s,
                                                                                {
                                                                                  class:
                                                                                    "in-tooltip",
                                                                                  closable:
                                                                                    !e.selectDisabled &&
                                                                                    !l.isDisabled,
                                                                                  size: e.collapseTagSize,
                                                                                  hit: l.hitState,
                                                                                  type: e.tagType,
                                                                                  "disable-transitions":
                                                                                    "",
                                                                                  style:
                                                                                    {
                                                                                      margin:
                                                                                        "2px",
                                                                                    },
                                                                                  onClose:
                                                                                    (
                                                                                      t,
                                                                                    ) =>
                                                                                      e.handleDeleteTooltipTag(
                                                                                        t,
                                                                                        l,
                                                                                      ),
                                                                                },
                                                                                {
                                                                                  default:
                                                                                    Z(
                                                                                      () => [
                                                                                        C(
                                                                                          "span",
                                                                                          {
                                                                                            class:
                                                                                              O(
                                                                                                e.nsSelect.e(
                                                                                                  "tags-text",
                                                                                                ),
                                                                                              ),
                                                                                            style:
                                                                                              I(
                                                                                                {
                                                                                                  maxWidth:
                                                                                                    e.inputWidth -
                                                                                                    75 +
                                                                                                    "px",
                                                                                                },
                                                                                              ),
                                                                                          },
                                                                                          S(
                                                                                            l.currentLabel,
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
                                                                                  "hit",
                                                                                  "type",
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
                                                              "teleported",
                                                            ],
                                                          ))
                                                        : (b(),
                                                          g(
                                                            "span",
                                                            {
                                                              key: 1,
                                                              class: O(
                                                                e.nsSelect.e(
                                                                  "tags-text",
                                                                ),
                                                              ),
                                                            },
                                                            "+ " +
                                                              S(
                                                                e.selected
                                                                  .length -
                                                                  e.maxCollapseTags,
                                                              ),
                                                            3,
                                                          )),
                                                    ]),
                                                    _: 1,
                                                  },
                                                  8,
                                                  ["size", "type"],
                                                ))
                                              : ae("v-if", !0),
                                          ],
                                          2,
                                        ),
                                      ]),
                                      _: 1,
                                    },
                                    8,
                                    ["onAfterLeave"],
                                  ))
                                : ae("v-if", !0),
                              e.collapseTags
                                ? ae("v-if", !0)
                                : (b(),
                                  ee(
                                    le,
                                    {
                                      key: 1,
                                      onAfterLeave: e.resetInputHeight,
                                    },
                                    {
                                      default: Z(() => [
                                        C(
                                          "span",
                                          {
                                            class: O(e.tagWrapperKls),
                                            style: I(
                                              e.prefixWidth && e.selected.length
                                                ? {
                                                    marginLeft: `${e.prefixWidth}px`,
                                                  }
                                                : "",
                                            ),
                                          },
                                          [
                                            (b(!0),
                                            g(
                                              te,
                                              null,
                                              oe(
                                                e.selected,
                                                (l) => (
                                                  b(),
                                                  ee(
                                                    s,
                                                    {
                                                      key: e.getValueKey(l),
                                                      closable:
                                                        !e.selectDisabled &&
                                                        !l.isDisabled,
                                                      size: e.collapseTagSize,
                                                      hit: l.hitState,
                                                      type: e.tagType,
                                                      "disable-transitions": "",
                                                      onClose: (t) =>
                                                        e.deleteTag(t, l),
                                                    },
                                                    {
                                                      default: Z(() => [
                                                        C(
                                                          "span",
                                                          {
                                                            class: O(
                                                              e.nsSelect.e(
                                                                "tags-text",
                                                              ),
                                                            ),
                                                            style: I({
                                                              maxWidth:
                                                                e.inputWidth -
                                                                75 +
                                                                "px",
                                                            }),
                                                          },
                                                          S(l.currentLabel),
                                                          7,
                                                        ),
                                                      ]),
                                                      _: 2,
                                                    },
                                                    1032,
                                                    [
                                                      "closable",
                                                      "size",
                                                      "hit",
                                                      "type",
                                                      "onClose",
                                                    ],
                                                  )
                                                ),
                                              ),
                                              128,
                                            )),
                                          ],
                                          6,
                                        ),
                                      ]),
                                      _: 1,
                                    },
                                    8,
                                    ["onAfterLeave"],
                                  )),
                              e.filterable && !e.selectDisabled
                                ? m(
                                    (b(),
                                    g(
                                      "input",
                                      {
                                        key: 2,
                                        ref: "input",
                                        "onUpdate:modelValue":
                                          l[0] || (l[0] = (l) => (e.query = l)),
                                        type: "text",
                                        class: O(e.inputKls),
                                        disabled: e.selectDisabled,
                                        autocomplete: e.autocomplete,
                                        style: I(e.inputStyle),
                                        onFocus:
                                          l[1] ||
                                          (l[1] = (...l) =>
                                            e.handleFocus &&
                                            e.handleFocus(...l)),
                                        onBlur:
                                          l[2] ||
                                          (l[2] = (...l) =>
                                            e.handleBlur && e.handleBlur(...l)),
                                        onKeyup:
                                          l[3] ||
                                          (l[3] = (...l) =>
                                            e.managePlaceholder &&
                                            e.managePlaceholder(...l)),
                                        onKeydown: [
                                          l[4] ||
                                            (l[4] = (...l) =>
                                              e.resetInputState &&
                                              e.resetInputState(...l)),
                                          l[5] ||
                                            (l[5] = ne(
                                              x(
                                                (l) =>
                                                  e.navigateOptions("next"),
                                                ["prevent"],
                                              ),
                                              ["down"],
                                            )),
                                          l[6] ||
                                            (l[6] = ne(
                                              x(
                                                (l) =>
                                                  e.navigateOptions("prev"),
                                                ["prevent"],
                                              ),
                                              ["up"],
                                            )),
                                          l[7] ||
                                            (l[7] = ne(
                                              (...l) =>
                                                e.handleKeydownEscape &&
                                                e.handleKeydownEscape(...l),
                                              ["esc"],
                                            )),
                                          l[8] ||
                                            (l[8] = ne(
                                              x(
                                                (...l) =>
                                                  e.selectOption &&
                                                  e.selectOption(...l),
                                                ["stop", "prevent"],
                                              ),
                                              ["enter"],
                                            )),
                                          l[9] ||
                                            (l[9] = ne(
                                              (...l) =>
                                                e.deletePrevTag &&
                                                e.deletePrevTag(...l),
                                              ["delete"],
                                            )),
                                          l[10] ||
                                            (l[10] = ne(
                                              (l) => (e.visible = !1),
                                              ["tab"],
                                            )),
                                        ],
                                        onCompositionstart:
                                          l[11] ||
                                          (l[11] = (...l) =>
                                            e.handleComposition &&
                                            e.handleComposition(...l)),
                                        onCompositionupdate:
                                          l[12] ||
                                          (l[12] = (...l) =>
                                            e.handleComposition &&
                                            e.handleComposition(...l)),
                                        onCompositionend:
                                          l[13] ||
                                          (l[13] = (...l) =>
                                            e.handleComposition &&
                                            e.handleComposition(...l)),
                                        onInput:
                                          l[14] ||
                                          (l[14] = (...l) =>
                                            e.debouncedQueryChange &&
                                            e.debouncedQueryChange(...l)),
                                      },
                                      null,
                                      46,
                                      Ke,
                                    )),
                                    [[se, e.query]],
                                  )
                                : ae("v-if", !0),
                            ],
                            6,
                          ))
                        : ae("v-if", !0),
                      ae(
                        " fix: https://github.com/element-plus/element-plus/issues/11415 ",
                      ),
                      e.isIOS && !e.multiple && e.filterable && e.readonly
                        ? (b(),
                          g(
                            "input",
                            {
                              key: 1,
                              ref: "iOSInput",
                              class: O(e.iOSInputKls),
                              disabled: e.selectDisabled,
                              type: "text",
                            },
                            null,
                            10,
                            qe,
                          ))
                        : ae("v-if", !0),
                      Y(
                        u,
                        {
                          id: e.id,
                          ref: "reference",
                          modelValue: e.selectedLabel,
                          "onUpdate:modelValue":
                            l[16] || (l[16] = (l) => (e.selectedLabel = l)),
                          type: "text",
                          placeholder:
                            "function" == typeof e.currentPlaceholder
                              ? e.currentPlaceholder()
                              : e.currentPlaceholder,
                          name: e.name,
                          autocomplete: e.autocomplete,
                          size: e.selectSize,
                          disabled: e.selectDisabled,
                          readonly: e.readonly,
                          "validate-event": !1,
                          class: O([e.nsSelect.is("focus", e.visible)]),
                          tabindex: e.multiple && e.filterable ? -1 : void 0,
                          onFocus: e.handleFocus,
                          onBlur: e.handleBlur,
                          onInput: e.debouncedOnInputChange,
                          onPaste: e.debouncedOnInputChange,
                          onCompositionstart: e.handleComposition,
                          onCompositionupdate: e.handleComposition,
                          onCompositionend: e.handleComposition,
                          onKeydown: [
                            l[17] ||
                              (l[17] = ne(
                                x(
                                  (l) => e.navigateOptions("next"),
                                  ["stop", "prevent"],
                                ),
                                ["down"],
                              )),
                            l[18] ||
                              (l[18] = ne(
                                x(
                                  (l) => e.navigateOptions("prev"),
                                  ["stop", "prevent"],
                                ),
                                ["up"],
                              )),
                            ne(x(e.selectOption, ["stop", "prevent"]), [
                              "enter",
                            ]),
                            ne(e.handleKeydownEscape, ["esc"]),
                            l[19] ||
                              (l[19] = ne((l) => (e.visible = !1), ["tab"])),
                          ],
                        },
                        ie(
                          {
                            suffix: Z(() => [
                              e.iconComponent && !e.showClose
                                ? (b(),
                                  ee(
                                    r,
                                    {
                                      key: 0,
                                      class: O([
                                        e.nsSelect.e("caret"),
                                        e.nsSelect.e("icon"),
                                        e.iconReverse,
                                      ]),
                                    },
                                    {
                                      default: Z(() => [
                                        (b(), ee(re(e.iconComponent))),
                                      ]),
                                      _: 1,
                                    },
                                    8,
                                    ["class"],
                                  ))
                                : ae("v-if", !0),
                              e.showClose && e.clearIcon
                                ? (b(),
                                  ee(
                                    r,
                                    {
                                      key: 1,
                                      class: O([
                                        e.nsSelect.e("caret"),
                                        e.nsSelect.e("icon"),
                                      ]),
                                      onClick: e.handleClearClick,
                                    },
                                    {
                                      default: Z(() => [
                                        (b(), ee(re(e.clearIcon))),
                                      ]),
                                      _: 1,
                                    },
                                    8,
                                    ["class", "onClick"],
                                  ))
                                : ae("v-if", !0),
                            ]),
                            _: 2,
                          },
                          [
                            e.$slots.prefix
                              ? {
                                  name: "prefix",
                                  fn: Z(() => [
                                    C("div", ze, [y(e.$slots, "prefix")]),
                                  ]),
                                }
                              : void 0,
                          ],
                        ),
                        1032,
                        [
                          "id",
                          "modelValue",
                          "placeholder",
                          "name",
                          "autocomplete",
                          "size",
                          "disabled",
                          "readonly",
                          "class",
                          "tabindex",
                          "onFocus",
                          "onBlur",
                          "onInput",
                          "onPaste",
                          "onCompositionstart",
                          "onCompositionupdate",
                          "onCompositionend",
                          "onKeydown",
                        ],
                      ),
                    ],
                    32,
                  ),
                ]),
                content: Z(() => [
                  Y(v, null, {
                    default: Z(() => [
                      m(
                        Y(
                          c,
                          {
                            ref: "scrollbar",
                            tag: "ul",
                            "wrap-class": e.nsSelect.be("dropdown", "wrap"),
                            "view-class": e.nsSelect.be("dropdown", "list"),
                            class: O(e.scrollbarKls),
                          },
                          {
                            default: Z(() => [
                              e.showNewOption
                                ? (b(),
                                  ee(
                                    p,
                                    { key: 0, value: e.query, created: !0 },
                                    null,
                                    8,
                                    ["value"],
                                  ))
                                : ae("v-if", !0),
                              Y(
                                d,
                                { onUpdateOptions: e.onOptionsRendered },
                                {
                                  default: Z(() => [y(e.$slots, "default")]),
                                  _: 3,
                                },
                                8,
                                ["onUpdateOptions"],
                              ),
                            ]),
                            _: 3,
                          },
                          8,
                          ["wrap-class", "view-class", "class"],
                        ),
                        [[f, e.options.size > 0 && !e.loading]],
                      ),
                      e.emptyText &&
                      (!e.allowCreate ||
                        e.loading ||
                        (e.allowCreate && 0 === e.options.size))
                        ? (b(),
                          g(
                            te,
                            { key: 0 },
                            [
                              e.$slots.empty
                                ? y(e.$slots, "empty", { key: 0 })
                                : (b(),
                                  g(
                                    "p",
                                    {
                                      key: 1,
                                      class: O(
                                        e.nsSelect.be("dropdown", "empty"),
                                      ),
                                    },
                                    S(e.emptyText),
                                    3,
                                  )),
                            ],
                            64,
                          ))
                        : ae("v-if", !0),
                    ]),
                    _: 3,
                  }),
                ]),
                _: 3,
              },
              8,
              [
                "visible",
                "placement",
                "teleported",
                "popper-class",
                "popper-options",
                "effect",
                "transition",
                "persistent",
                "onShow",
              ],
            ),
          ],
          34,
        )),
        [[h, e.handleClose, e.popperPaneRef]],
      );
    },
  ],
  [
    "__file",
    "/home/runner/work/element-plus/element-plus/packages/components/select/src/select.vue",
  ],
]);
var We = r(
  u({
    name: "ElOptionGroup",
    componentName: "ElOptionGroup",
    props: { label: String, disabled: { type: Boolean, default: !1 } },
    setup(e) {
      const t = p("select"),
        n = T(!0),
        i = o(),
        r = T([]);
      G(Le, d({ ...c(e) }));
      const u = l(Ie);
      w(() => {
        r.value = v(i.subTree);
      });
      const v = (e) => {
          const l = [];
          return (
            Array.isArray(e.children) &&
              e.children.forEach((e) => {
                var t;
                e.type &&
                "ElOption" === e.type.name &&
                e.component &&
                e.component.proxy
                  ? l.push(e.component.proxy)
                  : (null == (t = e.children) ? void 0 : t.length) &&
                    l.push(...v(e));
              }),
            l
          );
        },
        { groupQueryChange: h } = a(u);
      return (
        s(
          h,
          () => {
            n.value = r.value.some((e) => !0 === e.visible);
          },
          { flush: "post" },
        ),
        { visible: n, ns: t }
      );
    },
  }),
  [
    [
      "render",
      function (e, l, t, o, a, n) {
        return m(
          (b(),
          g(
            "ul",
            { class: O(e.ns.be("group", "wrap")) },
            [
              C("li", { class: O(e.ns.be("group", "title")) }, S(e.label), 3),
              C("li", null, [
                C(
                  "ul",
                  { class: O(e.ns.b("group")) },
                  [y(e.$slots, "default")],
                  2,
                ),
              ]),
            ],
            2,
          )),
          [[f, e.visible]],
        );
      },
    ],
    [
      "__file",
      "/home/runner/work/element-plus/element-plus/packages/components/select/src/option-group.vue",
    ],
  ],
);
const Be = ue(Ae, { Option: Ee, OptionGroup: We }),
  Fe = pe(Ee),
  He = pe(We);
export { Be as E, Fe as a, He as b, Ie as s };
