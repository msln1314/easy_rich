import {
  b as e,
  b6 as a,
  g as l,
  i as o,
  b7 as s,
  r as n,
  ao as r,
  f as d,
  b9 as i,
  aU as t,
  e as u,
  u as b,
  o as p,
  j as m,
  y as c,
  a0 as v,
  ck as f,
  k as g,
  ai as y,
  s as k,
  q as h,
  M as S,
  z as B,
  aY as R,
  _ as V,
  as as _,
  n as x,
  bL as w,
  b8 as E,
  bi as G,
  a2 as z,
  am as C,
  L as I,
  bw as U,
  w as $,
  ba as j,
  t as F,
  a8 as K,
} from "./index-6b60d190.js";
import { U as L, C as N } from "./event-5568c9d8.js";
const q = e({
    size: a,
    disabled: Boolean,
    label: { type: [String, Number, Boolean], default: "" },
  }),
  A = e({
    ...q,
    modelValue: { type: [String, Number, Boolean], default: "" },
    name: { type: String, default: "" },
    border: Boolean,
  }),
  M = { [L]: (e) => l(e) || o(e) || s(e), [N]: (e) => l(e) || o(e) || s(e) },
  Y = Symbol("radioGroupKey"),
  D = (e, a) => {
    const l = n(),
      o = r(Y, void 0),
      s = d(() => !!o),
      u = d({
        get: () => (s.value ? o.modelValue : e.modelValue),
        set(n) {
          (s.value ? o.changeEvent(n) : a && a(L, n),
            (l.value.checked = e.modelValue === e.label));
        },
      }),
      b = i(d(() => (null == o ? void 0 : o.size))),
      p = t(d(() => (null == o ? void 0 : o.disabled))),
      m = n(!1),
      c = d(() => (p.value || (s.value && u.value !== e.label) ? -1 : 0));
    return {
      radioRef: l,
      isGroup: s,
      radioGroup: o,
      focus: m,
      size: b,
      disabled: p,
      tabIndex: c,
      modelValue: u,
    };
  },
  H = ["value", "name", "disabled"],
  J = u({ name: "ElRadio" });
var O = V(
  u({
    ...J,
    props: A,
    emits: M,
    setup(e, { emit: a }) {
      const l = e,
        o = b("radio"),
        {
          radioRef: s,
          radioGroup: n,
          focus: r,
          size: d,
          disabled: i,
          modelValue: t,
        } = D(l, a);
      function u() {
        _(() => a("change", t.value));
      }
      return (e, a) => {
        var l;
        return (
          p(),
          m(
            "label",
            {
              class: k([
                g(o).b(),
                g(o).is("disabled", g(i)),
                g(o).is("focus", g(r)),
                g(o).is("bordered", e.border),
                g(o).is("checked", g(t) === e.label),
                g(o).m(g(d)),
              ]),
            },
            [
              c(
                "span",
                {
                  class: k([
                    g(o).e("input"),
                    g(o).is("disabled", g(i)),
                    g(o).is("checked", g(t) === e.label),
                  ]),
                },
                [
                  v(
                    c(
                      "input",
                      {
                        ref_key: "radioRef",
                        ref: s,
                        "onUpdate:modelValue":
                          a[0] || (a[0] = (e) => (y(t) ? (t.value = e) : null)),
                        class: k(g(o).e("original")),
                        value: e.label,
                        name: e.name || (null == (l = g(n)) ? void 0 : l.name),
                        disabled: g(i),
                        type: "radio",
                        onFocus: a[1] || (a[1] = (e) => (r.value = !0)),
                        onBlur: a[2] || (a[2] = (e) => (r.value = !1)),
                        onChange: u,
                      },
                      null,
                      42,
                      H,
                    ),
                    [[f, g(t)]],
                  ),
                  c("span", { class: k(g(o).e("inner")) }, null, 2),
                ],
                2,
              ),
              c(
                "span",
                {
                  class: k(g(o).e("label")),
                  onKeydown: a[3] || (a[3] = R(() => {}, ["stop"])),
                },
                [h(e.$slots, "default", {}, () => [S(B(e.label), 1)])],
                34,
              ),
            ],
            2,
          )
        );
      };
    },
  }),
  [
    [
      "__file",
      "/home/runner/work/element-plus/element-plus/packages/components/radio/src/radio.vue",
    ],
  ],
);
const P = e({ ...q, name: { type: String, default: "" } }),
  Q = ["value", "name", "disabled"],
  T = u({ name: "ElRadioButton" });
var W = V(
  u({
    ...T,
    props: P,
    setup(e) {
      const a = e,
        l = b("radio"),
        {
          radioRef: o,
          focus: s,
          size: n,
          disabled: r,
          modelValue: i,
          radioGroup: t,
        } = D(a),
        u = d(() => ({
          backgroundColor: (null == t ? void 0 : t.fill) || "",
          borderColor: (null == t ? void 0 : t.fill) || "",
          boxShadow: (null == t ? void 0 : t.fill)
            ? `-1px 0 0 0 ${t.fill}`
            : "",
          color: (null == t ? void 0 : t.textColor) || "",
        }));
      return (e, a) => {
        var d;
        return (
          p(),
          m(
            "label",
            {
              class: k([
                g(l).b("button"),
                g(l).is("active", g(i) === e.label),
                g(l).is("disabled", g(r)),
                g(l).is("focus", g(s)),
                g(l).bm("button", g(n)),
              ]),
            },
            [
              v(
                c(
                  "input",
                  {
                    ref_key: "radioRef",
                    ref: o,
                    "onUpdate:modelValue":
                      a[0] || (a[0] = (e) => (y(i) ? (i.value = e) : null)),
                    class: k(g(l).be("button", "original-radio")),
                    value: e.label,
                    type: "radio",
                    name: e.name || (null == (d = g(t)) ? void 0 : d.name),
                    disabled: g(r),
                    onFocus: a[1] || (a[1] = (e) => (s.value = !0)),
                    onBlur: a[2] || (a[2] = (e) => (s.value = !1)),
                  },
                  null,
                  42,
                  Q,
                ),
                [[f, g(i)]],
              ),
              c(
                "span",
                {
                  class: k(g(l).be("button", "inner")),
                  style: x(g(i) === e.label ? g(u) : {}),
                  onKeydown: a[3] || (a[3] = R(() => {}, ["stop"])),
                },
                [h(e.$slots, "default", {}, () => [S(B(e.label), 1)])],
                38,
              ),
            ],
            2,
          )
        );
      };
    },
  }),
  [
    [
      "__file",
      "/home/runner/work/element-plus/element-plus/packages/components/radio/src/radio-button.vue",
    ],
  ],
);
const X = e({
    id: { type: String, default: void 0 },
    size: a,
    disabled: Boolean,
    modelValue: { type: [String, Number, Boolean], default: "" },
    fill: { type: String, default: "" },
    label: { type: String, default: void 0 },
    textColor: { type: String, default: "" },
    name: { type: String, default: void 0 },
    validateEvent: { type: Boolean, default: !0 },
  }),
  Z = M,
  ee = ["id", "aria-label", "aria-labelledby"],
  ae = u({ name: "ElRadioGroup" });
var le = V(
  u({
    ...ae,
    props: X,
    emits: Z,
    setup(e, { emit: a }) {
      const l = e,
        o = b("radio"),
        s = w(),
        r = n(),
        { formItem: i } = E(),
        { inputId: t, isLabeledByFormItem: u } = G(l, { formItemContext: i });
      z(() => {
        const e = r.value.querySelectorAll("[type=radio]"),
          a = e[0];
        !Array.from(e).some((e) => e.checked) && a && (a.tabIndex = 0);
      });
      const c = d(() => l.name || s.value);
      return (
        C(
          Y,
          I({
            ...U(l),
            changeEvent: (e) => {
              (a(L, e), _(() => a("change", e)));
            },
            name: c,
          }),
        ),
        $(
          () => l.modelValue,
          () => {
            l.validateEvent &&
              (null == i || i.validate("change").catch((e) => j()));
          },
        ),
        (e, a) => (
          p(),
          m(
            "div",
            {
              id: g(t),
              ref_key: "radioGroupRef",
              ref: r,
              class: k(g(o).b("group")),
              role: "radiogroup",
              "aria-label": g(u) ? void 0 : e.label || "radio-group",
              "aria-labelledby": g(u) ? g(i).labelId : void 0,
            },
            [h(e.$slots, "default")],
            10,
            ee,
          )
        )
      );
    },
  }),
  [
    [
      "__file",
      "/home/runner/work/element-plus/element-plus/packages/components/radio/src/radio-group.vue",
    ],
  ],
);
const oe = F(O, { RadioButton: W, RadioGroup: le }),
  se = K(le),
  ne = K(W);
export { ne as E, se as a, oe as b };
