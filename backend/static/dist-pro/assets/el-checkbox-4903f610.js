import {
  c4 as e,
  c5 as a,
  c6 as l,
  c7 as n,
  bJ as o,
  c8 as t,
  c9 as i,
  ca as s,
  cb as u,
  b6 as d,
  g as r,
  i as c,
  b7 as b,
  ao as v,
  f as m,
  aD as h,
  aU as p,
  b8 as f,
  aq as k,
  w as x,
  ba as g,
  as as y,
  r as C,
  aZ as L,
  ap as B,
  cc as S,
  b9 as E,
  bi as I,
  e as F,
  aE as w,
  u as z,
  o as V,
  l as D,
  m as _,
  y as N,
  s as O,
  k as j,
  a0 as G,
  j as U,
  ai as $,
  cd as R,
  q,
  a1 as A,
  M,
  z as J,
  F as K,
  p as P,
  _ as Z,
  n as H,
  b as Q,
  d as T,
  am as W,
  bw as X,
  t as Y,
  a8 as ee,
} from "./index-6b60d190.js";
import { U as ae } from "./event-5568c9d8.js";
import { i as le } from "./isEqual-b8d86c27.js";
function ne(e, a) {
  return null != e && a in Object(e);
}
function oe(i, s) {
  return (
    null != i &&
    (function (i, s, u) {
      for (var d = -1, r = (s = e(s, i)).length, c = !1; ++d < r; ) {
        var b = a(s[d]);
        if (!(c = null != i && u(i, b))) break;
        i = i[b];
      }
      return c || ++d != r
        ? c
        : !!(r = null == i ? 0 : i.length) && l(r) && n(b, r) && (o(i) || t(i));
    })(i, s, ne)
  );
}
function te(a, l) {
  return (function (a, l, n) {
    for (var o = -1, t = l.length, u = {}; ++o < t; ) {
      var d = l[o],
        r = i(a, d);
      n(r, d) && s(u, e(d, a), r);
    }
    return u;
  })(a, l, function (e, l) {
    return oe(a, l);
  });
}
const ie = u(function (e, a) {
    return null == e ? {} : te(e, a);
  }),
  se = {
    modelValue: { type: [Number, String, Boolean], default: void 0 },
    label: { type: [String, Boolean, Number, Object] },
    indeterminate: Boolean,
    disabled: Boolean,
    checked: Boolean,
    name: { type: String, default: void 0 },
    trueLabel: { type: [String, Number], default: void 0 },
    falseLabel: { type: [String, Number], default: void 0 },
    id: { type: String, default: void 0 },
    controls: { type: String, default: void 0 },
    border: Boolean,
    size: d,
    tabindex: [String, Number],
    validateEvent: { type: Boolean, default: !0 },
  },
  ue = {
    [ae]: (e) => r(e) || c(e) || b(e),
    change: (e) => r(e) || c(e) || b(e),
  },
  de = Symbol("checkboxGroupContextKey"),
  re = (
    e,
    {
      model: a,
      isLimitExceeded: l,
      hasOwnLabel: n,
      isDisabled: o,
      isLabeledByFormItem: t,
    },
  ) => {
    const i = v(de, void 0),
      { formItem: s } = f(),
      { emit: u } = k();
    function d(a) {
      var l, n;
      return a === e.trueLabel || !0 === a
        ? null == (l = e.trueLabel) || l
        : null != (n = e.falseLabel) && n;
    }
    const r = m(
      () => (null == i ? void 0 : i.validateEvent) || e.validateEvent,
    );
    return (
      x(
        () => e.modelValue,
        () => {
          r.value && (null == s || s.validate("change").catch((e) => g()));
        },
      ),
      {
        handleChange: function (e) {
          if (l.value) return;
          const a = e.target;
          u("change", d(a.checked), e);
        },
        onClickRoot: async function (i) {
          if (!l.value && !n.value && !o.value && t.value) {
            i.composedPath().some((e) => "LABEL" === e.tagName) ||
              ((a.value = d([!1, e.falseLabel].includes(a.value))),
              await y(),
              (function (e, a) {
                u("change", d(e), a);
              })(a.value, i));
          }
        },
      }
    );
  },
  ce = (e, a) => {
    const { formItem: l } = f(),
      {
        model: n,
        isGroup: o,
        isLimitExceeded: t,
      } = ((e) => {
        const a = C(!1),
          { emit: l } = k(),
          n = v(de, void 0),
          o = m(() => !1 === h(n)),
          t = C(!1);
        return {
          model: m({
            get() {
              var l, t;
              return o.value
                ? null == (l = null == n ? void 0 : n.modelValue)
                  ? void 0
                  : l.value
                : null != (t = e.modelValue)
                  ? t
                  : a.value;
            },
            set(e) {
              var i, s;
              o.value && L(e)
                ? ((t.value =
                    void 0 !==
                      (null == (i = null == n ? void 0 : n.max)
                        ? void 0
                        : i.value) &&
                    e.length > (null == n ? void 0 : n.max.value)),
                  !1 === t.value &&
                    (null == (s = null == n ? void 0 : n.changeEvent) ||
                      s.call(n, e)))
                : (l(ae, e), (a.value = e));
            },
          }),
          isGroup: o,
          isLimitExceeded: t,
        };
      })(e),
      {
        isFocused: i,
        isChecked: s,
        checkboxButtonSize: u,
        checkboxSize: d,
        hasOwnLabel: r,
      } = ((e, a, { model: l }) => {
        const n = v(de, void 0),
          o = C(!1),
          t = m(() => {
            const a = l.value;
            return b(a)
              ? a
              : L(a)
                ? B(e.label)
                  ? a.map(S).some((a) => le(a, e.label))
                  : a.map(S).includes(e.label)
                : null != a
                  ? a === e.trueLabel
                  : !!a;
          });
        return {
          checkboxButtonSize: E(
            m(() => {
              var e;
              return null == (e = null == n ? void 0 : n.size)
                ? void 0
                : e.value;
            }),
            { prop: !0 },
          ),
          isChecked: t,
          isFocused: o,
          checkboxSize: E(
            m(() => {
              var e;
              return null == (e = null == n ? void 0 : n.size)
                ? void 0
                : e.value;
            }),
          ),
          hasOwnLabel: m(() => !(!a.default && !e.label)),
        };
      })(e, a, { model: n }),
      { isDisabled: c } = (({ model: e, isChecked: a }) => {
        const l = v(de, void 0),
          n = m(() => {
            var n, o;
            const t =
                null == (n = null == l ? void 0 : l.max) ? void 0 : n.value,
              i = null == (o = null == l ? void 0 : l.min) ? void 0 : o.value;
            return (
              (!h(t) && e.value.length >= t && !a.value) ||
              (!h(i) && e.value.length <= i && a.value)
            );
          });
        return {
          isDisabled: p(
            m(() => (null == l ? void 0 : l.disabled.value) || n.value),
          ),
          isLimitDisabled: n,
        };
      })({ model: n, isChecked: s }),
      { inputId: x, isLabeledByFormItem: g } = I(e, {
        formItemContext: l,
        disableIdGeneration: r,
        disableIdManagement: o,
      }),
      { handleChange: y, onClickRoot: F } = re(e, {
        model: n,
        isLimitExceeded: t,
        hasOwnLabel: r,
        isDisabled: c,
        isLabeledByFormItem: g,
      });
    return (
      ((e, { model: a }) => {
        e.checked &&
          (L(a.value) && !a.value.includes(e.label)
            ? a.value.push(e.label)
            : (a.value = e.trueLabel || !0));
      })(e, { model: n }),
      {
        inputId: x,
        isLabeledByFormItem: g,
        isChecked: s,
        isDisabled: c,
        isFocused: i,
        checkboxButtonSize: u,
        checkboxSize: d,
        hasOwnLabel: r,
        model: n,
        handleChange: y,
        onClickRoot: F,
      }
    );
  },
  be = ["tabindex", "role", "aria-checked"],
  ve = [
    "id",
    "aria-hidden",
    "name",
    "tabindex",
    "disabled",
    "true-value",
    "false-value",
  ],
  me = ["id", "aria-hidden", "disabled", "value", "name", "tabindex"],
  he = F({ name: "ElCheckbox" });
var pe = Z(
  F({
    ...he,
    props: se,
    emits: ue,
    setup(e) {
      const a = e,
        l = w(),
        {
          inputId: n,
          isLabeledByFormItem: o,
          isChecked: t,
          isDisabled: i,
          isFocused: s,
          checkboxSize: u,
          hasOwnLabel: d,
          model: r,
          handleChange: c,
          onClickRoot: b,
        } = ce(a, l),
        v = z("checkbox"),
        h = m(() => [
          v.b(),
          v.m(u.value),
          v.is("disabled", i.value),
          v.is("bordered", a.border),
          v.is("checked", t.value),
        ]),
        p = m(() => [
          v.e("input"),
          v.is("disabled", i.value),
          v.is("checked", t.value),
          v.is("indeterminate", a.indeterminate),
          v.is("focus", s.value),
        ]);
      return (e, a) => (
        V(),
        D(
          P(!j(d) && j(o) ? "span" : "label"),
          {
            class: O(j(h)),
            "aria-controls": e.indeterminate ? e.controls : null,
            onClick: j(b),
          },
          {
            default: _(() => [
              N(
                "span",
                {
                  class: O(j(p)),
                  tabindex: e.indeterminate ? 0 : void 0,
                  role: e.indeterminate ? "checkbox" : void 0,
                  "aria-checked": e.indeterminate ? "mixed" : void 0,
                },
                [
                  e.trueLabel || e.falseLabel
                    ? G(
                        (V(),
                        U(
                          "input",
                          {
                            key: 0,
                            id: j(n),
                            "onUpdate:modelValue":
                              a[0] ||
                              (a[0] = (e) => ($(r) ? (r.value = e) : null)),
                            class: O(j(v).e("original")),
                            type: "checkbox",
                            "aria-hidden": e.indeterminate ? "true" : "false",
                            name: e.name,
                            tabindex: e.tabindex,
                            disabled: j(i),
                            "true-value": e.trueLabel,
                            "false-value": e.falseLabel,
                            onChange:
                              a[1] || (a[1] = (...e) => j(c) && j(c)(...e)),
                            onFocus: a[2] || (a[2] = (e) => (s.value = !0)),
                            onBlur: a[3] || (a[3] = (e) => (s.value = !1)),
                          },
                          null,
                          42,
                          ve,
                        )),
                        [[R, j(r)]],
                      )
                    : G(
                        (V(),
                        U(
                          "input",
                          {
                            key: 1,
                            id: j(n),
                            "onUpdate:modelValue":
                              a[4] ||
                              (a[4] = (e) => ($(r) ? (r.value = e) : null)),
                            class: O(j(v).e("original")),
                            type: "checkbox",
                            "aria-hidden": e.indeterminate ? "true" : "false",
                            disabled: j(i),
                            value: e.label,
                            name: e.name,
                            tabindex: e.tabindex,
                            onChange:
                              a[5] || (a[5] = (...e) => j(c) && j(c)(...e)),
                            onFocus: a[6] || (a[6] = (e) => (s.value = !0)),
                            onBlur: a[7] || (a[7] = (e) => (s.value = !1)),
                          },
                          null,
                          42,
                          me,
                        )),
                        [[R, j(r)]],
                      ),
                  N("span", { class: O(j(v).e("inner")) }, null, 2),
                ],
                10,
                be,
              ),
              j(d)
                ? (V(),
                  U(
                    "span",
                    { key: 0, class: O(j(v).e("label")) },
                    [
                      q(e.$slots, "default"),
                      e.$slots.default
                        ? K("v-if", !0)
                        : (V(), U(A, { key: 0 }, [M(J(e.label), 1)], 64)),
                    ],
                    2,
                  ))
                : K("v-if", !0),
            ]),
            _: 3,
          },
          8,
          ["class", "aria-controls", "onClick"],
        )
      );
    },
  }),
  [
    [
      "__file",
      "/home/runner/work/element-plus/element-plus/packages/components/checkbox/src/checkbox.vue",
    ],
  ],
);
const fe = ["name", "tabindex", "disabled", "true-value", "false-value"],
  ke = ["name", "tabindex", "disabled", "value"],
  xe = F({ name: "ElCheckboxButton" });
var ge = Z(
  F({
    ...xe,
    props: se,
    emits: ue,
    setup(e) {
      const a = e,
        l = w(),
        {
          isFocused: n,
          isChecked: o,
          isDisabled: t,
          checkboxButtonSize: i,
          model: s,
          handleChange: u,
        } = ce(a, l),
        d = v(de, void 0),
        r = z("checkbox"),
        c = m(() => {
          var e, a, l, n;
          const o =
            null !=
            (a = null == (e = null == d ? void 0 : d.fill) ? void 0 : e.value)
              ? a
              : "";
          return {
            backgroundColor: o,
            borderColor: o,
            color:
              null !=
              (n =
                null == (l = null == d ? void 0 : d.textColor)
                  ? void 0
                  : l.value)
                ? n
                : "",
            boxShadow: o ? `-1px 0 0 0 ${o}` : void 0,
          };
        }),
        b = m(() => [
          r.b("button"),
          r.bm("button", i.value),
          r.is("disabled", t.value),
          r.is("checked", o.value),
          r.is("focus", n.value),
        ]);
      return (e, a) => (
        V(),
        U(
          "label",
          { class: O(j(b)) },
          [
            e.trueLabel || e.falseLabel
              ? G(
                  (V(),
                  U(
                    "input",
                    {
                      key: 0,
                      "onUpdate:modelValue":
                        a[0] || (a[0] = (e) => ($(s) ? (s.value = e) : null)),
                      class: O(j(r).be("button", "original")),
                      type: "checkbox",
                      name: e.name,
                      tabindex: e.tabindex,
                      disabled: j(t),
                      "true-value": e.trueLabel,
                      "false-value": e.falseLabel,
                      onChange: a[1] || (a[1] = (...e) => j(u) && j(u)(...e)),
                      onFocus: a[2] || (a[2] = (e) => (n.value = !0)),
                      onBlur: a[3] || (a[3] = (e) => (n.value = !1)),
                    },
                    null,
                    42,
                    fe,
                  )),
                  [[R, j(s)]],
                )
              : G(
                  (V(),
                  U(
                    "input",
                    {
                      key: 1,
                      "onUpdate:modelValue":
                        a[4] || (a[4] = (e) => ($(s) ? (s.value = e) : null)),
                      class: O(j(r).be("button", "original")),
                      type: "checkbox",
                      name: e.name,
                      tabindex: e.tabindex,
                      disabled: j(t),
                      value: e.label,
                      onChange: a[5] || (a[5] = (...e) => j(u) && j(u)(...e)),
                      onFocus: a[6] || (a[6] = (e) => (n.value = !0)),
                      onBlur: a[7] || (a[7] = (e) => (n.value = !1)),
                    },
                    null,
                    42,
                    ke,
                  )),
                  [[R, j(s)]],
                ),
            e.$slots.default || e.label
              ? (V(),
                U(
                  "span",
                  {
                    key: 2,
                    class: O(j(r).be("button", "inner")),
                    style: H(j(o) ? j(c) : void 0),
                  },
                  [q(e.$slots, "default", {}, () => [M(J(e.label), 1)])],
                  6,
                ))
              : K("v-if", !0),
          ],
          2,
        )
      );
    },
  }),
  [
    [
      "__file",
      "/home/runner/work/element-plus/element-plus/packages/components/checkbox/src/checkbox-button.vue",
    ],
  ],
);
const ye = Q({
    modelValue: { type: T(Array), default: () => [] },
    disabled: Boolean,
    min: Number,
    max: Number,
    size: d,
    label: String,
    fill: String,
    textColor: String,
    tag: { type: String, default: "div" },
    validateEvent: { type: Boolean, default: !0 },
  }),
  Ce = { [ae]: (e) => L(e), change: (e) => L(e) },
  Le = F({ name: "ElCheckboxGroup" });
var Be = Z(
  F({
    ...Le,
    props: ye,
    emits: Ce,
    setup(e, { emit: a }) {
      const l = e,
        n = z("checkbox"),
        { formItem: o } = f(),
        { inputId: t, isLabeledByFormItem: i } = I(l, { formItemContext: o }),
        s = async (e) => {
          (a(ae, e), await y(), a("change", e));
        },
        u = m({
          get: () => l.modelValue,
          set(e) {
            s(e);
          },
        });
      return (
        W(de, {
          ...ie(X(l), [
            "size",
            "min",
            "max",
            "disabled",
            "validateEvent",
            "fill",
            "textColor",
          ]),
          modelValue: u,
          changeEvent: s,
        }),
        x(
          () => l.modelValue,
          () => {
            l.validateEvent &&
              (null == o || o.validate("change").catch((e) => g()));
          },
        ),
        (e, a) => {
          var l;
          return (
            V(),
            D(
              P(e.tag),
              {
                id: j(t),
                class: O(j(n).b("group")),
                role: "group",
                "aria-label": j(i) ? void 0 : e.label || "checkbox-group",
                "aria-labelledby": j(i)
                  ? null == (l = j(o))
                    ? void 0
                    : l.labelId
                  : void 0,
              },
              { default: _(() => [q(e.$slots, "default")]), _: 3 },
              8,
              ["id", "class", "aria-label", "aria-labelledby"],
            )
          );
        }
      );
    },
  }),
  [
    [
      "__file",
      "/home/runner/work/element-plus/element-plus/packages/components/checkbox/src/checkbox-group.vue",
    ],
  ],
);
const Se = Y(pe, { CheckboxButton: ge, CheckboxGroup: Be }),
  Ee = ee(ge),
  Ie = ee(Be);
export { Se as E, Ie as a, Ee as b, oe as h, ie as p };
