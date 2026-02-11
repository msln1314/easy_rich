import {
  b as e,
  a,
  d as t,
  b7 as i,
  g as l,
  i as n,
  e as o,
  aq as c,
  b8 as s,
  b9 as r,
  u as v,
  bi as u,
  aU as d,
  f as p,
  r as f,
  h as m,
  w as b,
  ba as y,
  a2 as h,
  o as k,
  j as g,
  y as I,
  k as x,
  s as C,
  aX as S,
  l as V,
  m as w,
  p as T,
  E as _,
  F as B,
  z as A,
  x as E,
  aW as N,
  n as P,
  aY as j,
  _ as U,
  aB as z,
  as as F,
  bb as K,
  ar as q,
  t as L,
} from "./index-6b60d190.js";
import { i as W } from "./validator-f032316f.js";
import { U as X, C as Y, I as D } from "./event-5568c9d8.js";
const G = e({
    modelValue: { type: [Boolean, String, Number], default: !1 },
    disabled: { type: Boolean, default: !1 },
    loading: { type: Boolean, default: !1 },
    size: { type: String, validator: W },
    width: { type: [String, Number], default: "" },
    inlinePrompt: { type: Boolean, default: !1 },
    inactiveActionIcon: { type: a },
    activeActionIcon: { type: a },
    activeIcon: { type: a },
    inactiveIcon: { type: a },
    activeText: { type: String, default: "" },
    inactiveText: { type: String, default: "" },
    activeValue: { type: [Boolean, String, Number], default: !0 },
    inactiveValue: { type: [Boolean, String, Number], default: !1 },
    activeColor: { type: String, default: "" },
    inactiveColor: { type: String, default: "" },
    borderColor: { type: String, default: "" },
    name: { type: String, default: "" },
    validateEvent: { type: Boolean, default: !0 },
    beforeChange: { type: t(Function) },
    id: String,
    tabindex: { type: [String, Number] },
    value: { type: [Boolean, String, Number], default: !1 },
  }),
  H = {
    [X]: (e) => i(e) || l(e) || n(e),
    [Y]: (e) => i(e) || l(e) || n(e),
    [D]: (e) => i(e) || l(e) || n(e),
  },
  J = ["onClick"],
  M = [
    "id",
    "aria-checked",
    "aria-disabled",
    "name",
    "true-value",
    "false-value",
    "disabled",
    "tabindex",
    "onKeydown",
  ],
  O = ["aria-hidden"],
  Q = ["aria-hidden"],
  R = ["aria-hidden"],
  Z = "ElSwitch",
  $ = o({ name: Z });
const ee = L(
  U(
    o({
      ...$,
      props: G,
      emits: H,
      setup(e, { expose: a, emit: t }) {
        const l = e,
          n = c(),
          { formItem: o } = s(),
          U = r(),
          L = v("switch");
        [
          ['"value"', '"model-value" or "v-model"', "value"],
          ['"active-color"', "CSS var `--el-switch-on-color`", "activeColor"],
          [
            '"inactive-color"',
            "CSS var `--el-switch-off-color`",
            "inactiveColor",
          ],
          [
            '"border-color"',
            "CSS var `--el-switch-border-color`",
            "borderColor",
          ],
        ].forEach((e) => {
          z(
            {
              from: e[0],
              replacement: e[1],
              scope: Z,
              version: "2.3.0",
              ref: "https://element-plus.org/en-US/component/switch.html#attributes",
              type: "Attribute",
            },
            p(() => {
              var a;
              return !!(null == (a = n.vnode.props) ? void 0 : a[e[2]]);
            }),
          );
        });
        const { inputId: W } = u(l, { formItemContext: o }),
          G = d(p(() => l.loading)),
          H = f(!1 !== l.modelValue),
          $ = f(),
          ee = f(),
          ae = p(() => [
            L.b(),
            L.m(U.value),
            L.is("disabled", G.value),
            L.is("checked", oe.value),
          ]),
          te = p(() => [
            L.e("label"),
            L.em("label", "left"),
            L.is("active", !oe.value),
          ]),
          ie = p(() => [
            L.e("label"),
            L.em("label", "right"),
            L.is("active", oe.value),
          ]),
          le = p(() => ({ width: m(l.width) }));
        (b(
          () => l.modelValue,
          () => {
            H.value = !0;
          },
        ),
          b(
            () => l.value,
            () => {
              H.value = !1;
            },
          ));
        const ne = p(() => (H.value ? l.modelValue : l.value)),
          oe = p(() => ne.value === l.activeValue);
        ([l.activeValue, l.inactiveValue].includes(ne.value) ||
          (t(X, l.inactiveValue), t(Y, l.inactiveValue), t(D, l.inactiveValue)),
          b(oe, (e) => {
            var a;
            (($.value.checked = e),
              l.validateEvent &&
                (null == (a = null == o ? void 0 : o.validate) ||
                  a.call(o, "change").catch((e) => y())));
          }));
        const ce = () => {
            const e = oe.value ? l.inactiveValue : l.activeValue;
            (t(X, e),
              t(Y, e),
              t(D, e),
              F(() => {
                $.value.checked = oe.value;
              }));
          },
          se = () => {
            if (G.value) return;
            const { beforeChange: e } = l;
            if (!e) return void ce();
            const a = e();
            ([K(a), i(a)].includes(!0) ||
              q(
                Z,
                "beforeChange must return type `Promise<boolean>` or `boolean`",
              ),
              K(a)
                ? a
                    .then((e) => {
                      e && ce();
                    })
                    .catch((e) => {})
                : a && ce());
          },
          re = p(() =>
            L.cssVarBlock({
              ...(l.activeColor ? { "on-color": l.activeColor } : null),
              ...(l.inactiveColor ? { "off-color": l.inactiveColor } : null),
              ...(l.borderColor ? { "border-color": l.borderColor } : null),
            }),
          );
        return (
          h(() => {
            $.value.checked = oe.value;
          }),
          a({
            focus: () => {
              var e, a;
              null == (a = null == (e = $.value) ? void 0 : e.focus) ||
                a.call(e);
            },
            checked: oe,
          }),
          (e, a) => (
            k(),
            g(
              "div",
              { class: C(x(ae)), style: P(x(re)), onClick: j(se, ["prevent"]) },
              [
                I(
                  "input",
                  {
                    id: x(W),
                    ref_key: "input",
                    ref: $,
                    class: C(x(L).e("input")),
                    type: "checkbox",
                    role: "switch",
                    "aria-checked": x(oe),
                    "aria-disabled": x(G),
                    name: e.name,
                    "true-value": e.activeValue,
                    "false-value": e.inactiveValue,
                    disabled: x(G),
                    tabindex: e.tabindex,
                    onChange: ce,
                    onKeydown: S(se, ["enter"]),
                  },
                  null,
                  42,
                  M,
                ),
                e.inlinePrompt || (!e.inactiveIcon && !e.inactiveText)
                  ? B("v-if", !0)
                  : (k(),
                    g(
                      "span",
                      { key: 0, class: C(x(te)) },
                      [
                        e.inactiveIcon
                          ? (k(),
                            V(
                              x(_),
                              { key: 0 },
                              {
                                default: w(() => [(k(), V(T(e.inactiveIcon)))]),
                                _: 1,
                              },
                            ))
                          : B("v-if", !0),
                        !e.inactiveIcon && e.inactiveText
                          ? (k(),
                            g(
                              "span",
                              { key: 1, "aria-hidden": x(oe) },
                              A(e.inactiveText),
                              9,
                              O,
                            ))
                          : B("v-if", !0),
                      ],
                      2,
                    )),
                I(
                  "span",
                  {
                    ref_key: "core",
                    ref: ee,
                    class: C(x(L).e("core")),
                    style: P(x(le)),
                  },
                  [
                    e.inlinePrompt
                      ? (k(),
                        g(
                          "div",
                          { key: 0, class: C(x(L).e("inner")) },
                          [
                            e.activeIcon || e.inactiveIcon
                              ? (k(),
                                V(
                                  x(_),
                                  { key: 0, class: C(x(L).is("icon")) },
                                  {
                                    default: w(() => [
                                      (k(),
                                      V(
                                        T(
                                          x(oe) ? e.activeIcon : e.inactiveIcon,
                                        ),
                                      )),
                                    ]),
                                    _: 1,
                                  },
                                  8,
                                  ["class"],
                                ))
                              : e.activeText || e.inactiveText
                                ? (k(),
                                  g(
                                    "span",
                                    {
                                      key: 1,
                                      class: C(x(L).is("text")),
                                      "aria-hidden": !x(oe),
                                    },
                                    A(x(oe) ? e.activeText : e.inactiveText),
                                    11,
                                    Q,
                                  ))
                                : B("v-if", !0),
                          ],
                          2,
                        ))
                      : B("v-if", !0),
                    I(
                      "div",
                      { class: C(x(L).e("action")) },
                      [
                        e.loading
                          ? (k(),
                            V(
                              x(_),
                              { key: 0, class: C(x(L).is("loading")) },
                              { default: w(() => [E(x(N))]), _: 1 },
                              8,
                              ["class"],
                            ))
                          : e.activeActionIcon && x(oe)
                            ? (k(),
                              V(
                                x(_),
                                { key: 1 },
                                {
                                  default: w(() => [
                                    (k(), V(T(e.activeActionIcon))),
                                  ]),
                                  _: 1,
                                },
                              ))
                            : e.inactiveActionIcon && !x(oe)
                              ? (k(),
                                V(
                                  x(_),
                                  { key: 2 },
                                  {
                                    default: w(() => [
                                      (k(), V(T(e.inactiveActionIcon))),
                                    ]),
                                    _: 1,
                                  },
                                ))
                              : B("v-if", !0),
                      ],
                      2,
                    ),
                  ],
                  6,
                ),
                e.inlinePrompt || (!e.activeIcon && !e.activeText)
                  ? B("v-if", !0)
                  : (k(),
                    g(
                      "span",
                      { key: 1, class: C(x(ie)) },
                      [
                        e.activeIcon
                          ? (k(),
                            V(
                              x(_),
                              { key: 0 },
                              {
                                default: w(() => [(k(), V(T(e.activeIcon)))]),
                                _: 1,
                              },
                            ))
                          : B("v-if", !0),
                        !e.activeIcon && e.activeText
                          ? (k(),
                            g(
                              "span",
                              { key: 1, "aria-hidden": !x(oe) },
                              A(e.activeText),
                              9,
                              R,
                            ))
                          : B("v-if", !0),
                      ],
                      2,
                    )),
              ],
              14,
              J,
            )
          )
        );
      },
    }),
    [
      [
        "__file",
        "/home/runner/work/element-plus/element-plus/packages/components/switch/src/switch.vue",
      ],
    ],
  ),
);
export { ee as E };
