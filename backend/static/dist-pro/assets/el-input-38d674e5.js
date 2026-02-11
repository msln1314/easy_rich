import {
  aJ as e,
  f as a,
  aq as t,
  bO as l,
  r as n,
  ab as o,
  w as s,
  by as r,
  i,
  b as u,
  b6 as p,
  d,
  a as c,
  an as v,
  g as f,
  e as m,
  aT as y,
  aE as x,
  b8 as b,
  bi as g,
  b9 as h,
  aU as w,
  u as S,
  bv as k,
  c2 as z,
  c3 as C,
  at as E,
  as as F,
  ba as I,
  a2 as $,
  a4 as B,
  a0 as P,
  aH as _,
  o as j,
  j as M,
  F as R,
  a1 as V,
  s as N,
  k as A,
  q as T,
  y as H,
  l as O,
  m as K,
  p as W,
  E as L,
  a6 as q,
  x as U,
  bc as Y,
  aY as D,
  aS as J,
  z as Z,
  n as G,
  _ as Q,
  ap as X,
  t as ee,
} from "./index-6b60d190.js";
import { U as ae } from "./event-5568c9d8.js";
import { i as te } from "./isNil-1f22f7b0.js";
const le = () => e && /firefox/i.test(window.navigator.userAgent),
  ne = (e) => /([\uAC00-\uD7AF\u3130-\u318F])+/gi.test(e),
  oe = ["class", "style"],
  se = /^on[A-Z]/,
  re = (e = {}) => {
    const { excludeListeners: n = !1, excludeKeys: o } = e,
      s = a(() => ((null == o ? void 0 : o.value) || []).concat(oe)),
      r = t();
    return a(
      r
        ? () => {
            var e;
            return l(
              Object.entries(null == (e = r.proxy) ? void 0 : e.$attrs).filter(
                ([e]) => !(s.value.includes(e) || (n && se.test(e))),
              ),
            );
          }
        : () => ({}),
    );
  };
let ie;
const ue = `\n  height:0 !important;\n  visibility:hidden !important;\n  ${le() ? "" : "overflow:hidden !important;"}\n  position:absolute !important;\n  z-index:-1000 !important;\n  top:0 !important;\n  right:0 !important;\n`,
  pe = [
    "letter-spacing",
    "line-height",
    "padding-top",
    "padding-bottom",
    "font-family",
    "font-weight",
    "font-size",
    "text-rendering",
    "text-transform",
    "width",
    "text-indent",
    "padding-left",
    "padding-right",
    "border-width",
    "box-sizing",
  ];
function de(e, a = 1, t) {
  var l;
  ie ||
    ((ie = document.createElement("textarea")), document.body.appendChild(ie));
  const {
    paddingSize: n,
    borderSize: o,
    boxSizing: s,
    contextStyle: r,
  } = (function (e) {
    const a = window.getComputedStyle(e),
      t = a.getPropertyValue("box-sizing"),
      l =
        Number.parseFloat(a.getPropertyValue("padding-bottom")) +
        Number.parseFloat(a.getPropertyValue("padding-top")),
      n =
        Number.parseFloat(a.getPropertyValue("border-bottom-width")) +
        Number.parseFloat(a.getPropertyValue("border-top-width"));
    return {
      contextStyle: pe.map((e) => `${e}:${a.getPropertyValue(e)}`).join(";"),
      paddingSize: l,
      borderSize: n,
      boxSizing: t,
    };
  })(e);
  (ie.setAttribute("style", `${r};${ue}`),
    (ie.value = e.value || e.placeholder || ""));
  let u = ie.scrollHeight;
  const p = {};
  ("border-box" === s ? (u += o) : "content-box" === s && (u -= n),
    (ie.value = ""));
  const d = ie.scrollHeight - n;
  if (i(a)) {
    let e = d * a;
    ("border-box" === s && (e = e + n + o),
      (u = Math.max(e, u)),
      (p.minHeight = `${e}px`));
  }
  if (i(t)) {
    let e = d * t;
    ("border-box" === s && (e = e + n + o), (u = Math.min(e, u)));
  }
  return (
    (p.height = `${u}px`),
    null == (l = ie.parentNode) || l.removeChild(ie),
    (ie = void 0),
    p
  );
}
const ce = u({
    id: { type: String, default: void 0 },
    size: p,
    disabled: Boolean,
    modelValue: { type: d([String, Number, Object]), default: "" },
    type: { type: String, default: "text" },
    resize: {
      type: String,
      values: ["none", "both", "horizontal", "vertical"],
    },
    autosize: { type: d([Boolean, Object]), default: !1 },
    autocomplete: { type: String, default: "off" },
    formatter: { type: Function },
    parser: { type: Function },
    placeholder: { type: String },
    form: { type: String },
    readonly: { type: Boolean, default: !1 },
    clearable: { type: Boolean, default: !1 },
    showPassword: { type: Boolean, default: !1 },
    showWordLimit: { type: Boolean, default: !1 },
    suffixIcon: { type: c },
    prefixIcon: { type: c },
    containerRole: { type: String, default: void 0 },
    label: { type: String, default: void 0 },
    tabindex: { type: [String, Number], default: 0 },
    validateEvent: { type: Boolean, default: !0 },
    inputStyle: { type: d([Object, Array, String]), default: () => v({}) },
  }),
  ve = {
    [ae]: (e) => f(e),
    input: (e) => f(e),
    change: (e) => f(e),
    focus: (e) => e instanceof FocusEvent,
    blur: (e) => e instanceof FocusEvent,
    clear: () => !0,
    mouseleave: (e) => e instanceof MouseEvent,
    mouseenter: (e) => e instanceof MouseEvent,
    keydown: (e) => e instanceof Event,
    compositionstart: (e) => e instanceof CompositionEvent,
    compositionupdate: (e) => e instanceof CompositionEvent,
    compositionend: (e) => e instanceof CompositionEvent,
  },
  fe = ["role"],
  me = [
    "id",
    "type",
    "disabled",
    "formatter",
    "parser",
    "readonly",
    "autocomplete",
    "tabindex",
    "aria-label",
    "placeholder",
    "form",
  ],
  ye = [
    "id",
    "tabindex",
    "disabled",
    "readonly",
    "autocomplete",
    "aria-label",
    "placeholder",
    "form",
  ],
  xe = m({ name: "ElInput", inheritAttrs: !1 });
const be = ee(
  Q(
    m({
      ...xe,
      props: ce,
      emits: ve,
      setup(l, { expose: i, emit: u }) {
        const p = l,
          d = y(),
          c = x(),
          v = a(() => {
            const e = {};
            return (
              "combobox" === p.containerRole &&
                ((e["aria-haspopup"] = d["aria-haspopup"]),
                (e["aria-owns"] = d["aria-owns"]),
                (e["aria-expanded"] = d["aria-expanded"])),
              e
            );
          }),
          f = a(() => [
            "textarea" === p.type ? pe.b() : ue.b(),
            ue.m(se.value),
            ue.is("disabled", ie.value),
            ue.is("exceed", Ae.value),
            {
              [ue.b("group")]: c.prepend || c.append,
              [ue.bm("group", "append")]: c.append,
              [ue.bm("group", "prepend")]: c.prepend,
              [ue.m("prefix")]: c.prefix || p.prefixIcon,
              [ue.m("suffix")]:
                c.suffix || p.suffixIcon || p.clearable || p.showPassword,
              [ue.bm("suffix", "password-clear")]: Me.value && Re.value,
            },
            d.class,
          ]),
          m = a(() => [ue.e("wrapper"), ue.is("focus", ze.value)]),
          Q = re({ excludeKeys: a(() => Object.keys(v.value)) }),
          { form: ee, formItem: le } = b(),
          { inputId: oe } = g(p, { formItemContext: le }),
          se = h(),
          ie = w(),
          ue = S("input"),
          pe = S("textarea"),
          ce = o(),
          ve = o(),
          xe = n(!1),
          be = n(!1),
          ge = n(!1),
          he = n(),
          we = o(p.inputStyle),
          Se = a(() => ce.value || ve.value),
          {
            wrapperRef: ke,
            isFocused: ze,
            handleFocus: Ce,
            handleBlur: Ee,
          } = (function (e, { afterFocus: a, afterBlur: l } = {}) {
            const i = t(),
              { emit: u } = i,
              p = o(),
              d = n(!1);
            return (
              s(p, (e) => {
                e && e.setAttribute("tabindex", "-1");
              }),
              r(p, "click", () => {
                var a;
                null == (a = e.value) || a.focus();
              }),
              {
                wrapperRef: p,
                isFocused: d,
                handleFocus: (e) => {
                  d.value || ((d.value = !0), u("focus", e), null == a || a());
                },
                handleBlur: (e) => {
                  var a;
                  (e.relatedTarget &&
                    (null == (a = p.value)
                      ? void 0
                      : a.contains(e.relatedTarget))) ||
                    ((d.value = !1), u("blur", e), null == l || l());
                },
              }
            );
          })(Se, {
            afterBlur() {
              var e;
              p.validateEvent &&
                (null == (e = null == le ? void 0 : le.validate) ||
                  e.call(le, "blur").catch((e) => I()));
            },
          }),
          Fe = a(() => {
            var e;
            return null != (e = null == ee ? void 0 : ee.statusIcon) && e;
          }),
          Ie = a(() => (null == le ? void 0 : le.validateState) || ""),
          $e = a(() => Ie.value && k[Ie.value]),
          Be = a(() => (ge.value ? z : C)),
          Pe = a(() => [d.style, p.inputStyle]),
          _e = a(() => [p.inputStyle, we.value, { resize: p.resize }]),
          je = a(() => (te(p.modelValue) ? "" : String(p.modelValue))),
          Me = a(
            () =>
              p.clearable &&
              !ie.value &&
              !p.readonly &&
              !!je.value &&
              (ze.value || xe.value),
          ),
          Re = a(
            () =>
              p.showPassword &&
              !ie.value &&
              !p.readonly &&
              !!je.value &&
              (!!je.value || ze.value),
          ),
          Ve = a(
            () =>
              p.showWordLimit &&
              !!Q.value.maxlength &&
              ("text" === p.type || "textarea" === p.type) &&
              !ie.value &&
              !p.readonly &&
              !p.showPassword,
          ),
          Ne = a(() => je.value.length),
          Ae = a(() => !!Ve.value && Ne.value > Number(Q.value.maxlength)),
          Te = a(
            () =>
              !!c.suffix ||
              !!p.suffixIcon ||
              Me.value ||
              p.showPassword ||
              Ve.value ||
              (!!Ie.value && Fe.value),
          ),
          [He, Oe] = (function (e) {
            const a = n();
            return [
              function () {
                if (null == e.value) return;
                const {
                  selectionStart: t,
                  selectionEnd: l,
                  value: n,
                } = e.value;
                if (null == t || null == l) return;
                const o = n.slice(0, Math.max(0, t)),
                  s = n.slice(Math.max(0, l));
                a.value = {
                  selectionStart: t,
                  selectionEnd: l,
                  value: n,
                  beforeTxt: o,
                  afterTxt: s,
                };
              },
              function () {
                if (null == e.value || null == a.value) return;
                const { value: t } = e.value,
                  { beforeTxt: l, afterTxt: n, selectionStart: o } = a.value;
                if (null == l || null == n || null == o) return;
                let s = t.length;
                if (t.endsWith(n)) s = t.length - n.length;
                else if (t.startsWith(l)) s = l.length;
                else {
                  const e = l[o - 1],
                    a = t.indexOf(e, o - 1);
                  -1 !== a && (s = a + 1);
                }
                e.value.setSelectionRange(s, s);
              },
            ];
          })(ce);
        E(ve, (e) => {
          if ((We(), !Ve.value || "both" !== p.resize)) return;
          const a = e[0],
            { width: t } = a.contentRect;
          he.value = { right: `calc(100% - ${t + 15 + 6}px)` };
        });
        const Ke = () => {
            const { type: a, autosize: t } = p;
            if (e && "textarea" === a && ve.value)
              if (t) {
                const e = X(t) ? t.minRows : void 0,
                  a = X(t) ? t.maxRows : void 0,
                  l = de(ve.value, e, a);
                ((we.value = { overflowY: "hidden", ...l }),
                  F(() => {
                    (ve.value.offsetHeight, (we.value = l));
                  }));
              } else we.value = { minHeight: de(ve.value).minHeight };
          },
          We = ((e) => {
            let a = !1;
            return () => {
              var t;
              if (a || !p.autosize) return;
              null === (null == (t = ve.value) ? void 0 : t.offsetParent) ||
                (e(), (a = !0));
            };
          })(Ke),
          Le = () => {
            const e = Se.value,
              a = p.formatter ? p.formatter(je.value) : je.value;
            e && e.value !== a && (e.value = a);
          },
          qe = async (e) => {
            He();
            let { value: a } = e.target;
            (p.formatter && (a = p.parser ? p.parser(a) : a),
              be.value ||
                (a !== je.value
                  ? (u(ae, a), u("input", a), await F(), Le(), Oe())
                  : Le()));
          },
          Ue = (e) => {
            u("change", e.target.value);
          },
          Ye = (e) => {
            (u("compositionstart", e), (be.value = !0));
          },
          De = (e) => {
            var a;
            u("compositionupdate", e);
            const t = null == (a = e.target) ? void 0 : a.value,
              l = t[t.length - 1] || "";
            be.value = !ne(l);
          },
          Je = (e) => {
            (u("compositionend", e), be.value && ((be.value = !1), qe(e)));
          },
          Ze = () => {
            ((ge.value = !ge.value), Ge());
          },
          Ge = async () => {
            var e;
            (await F(), null == (e = Se.value) || e.focus());
          },
          Qe = (e) => {
            ((xe.value = !1), u("mouseleave", e));
          },
          Xe = (e) => {
            ((xe.value = !0), u("mouseenter", e));
          },
          ea = (e) => {
            u("keydown", e);
          },
          aa = () => {
            (u(ae, ""), u("change", ""), u("clear"), u("input", ""));
          };
        return (
          s(
            () => p.modelValue,
            () => {
              var e;
              (F(() => Ke()),
                p.validateEvent &&
                  (null == (e = null == le ? void 0 : le.validate) ||
                    e.call(le, "change").catch((e) => I())));
            },
          ),
          s(je, () => Le()),
          s(
            () => p.type,
            async () => {
              (await F(), Le(), Ke());
            },
          ),
          $(() => {
            (!p.formatter && p.parser, Le(), F(Ke));
          }),
          i({
            input: ce,
            textarea: ve,
            ref: Se,
            textareaStyle: _e,
            autosize: B(p, "autosize"),
            focus: Ge,
            blur: () => {
              var e;
              return null == (e = Se.value) ? void 0 : e.blur();
            },
            select: () => {
              var e;
              null == (e = Se.value) || e.select();
            },
            clear: aa,
            resizeTextarea: Ke,
          }),
          (e, a) =>
            P(
              (j(),
              M(
                "div",
                q(A(v), {
                  class: A(f),
                  style: A(Pe),
                  role: e.containerRole,
                  onMouseenter: Xe,
                  onMouseleave: Qe,
                }),
                [
                  R(" input "),
                  "textarea" !== e.type
                    ? (j(),
                      M(
                        V,
                        { key: 0 },
                        [
                          R(" prepend slot "),
                          e.$slots.prepend
                            ? (j(),
                              M(
                                "div",
                                {
                                  key: 0,
                                  class: N(A(ue).be("group", "prepend")),
                                },
                                [T(e.$slots, "prepend")],
                                2,
                              ))
                            : R("v-if", !0),
                          H(
                            "div",
                            { ref_key: "wrapperRef", ref: ke, class: N(A(m)) },
                            [
                              R(" prefix slot "),
                              e.$slots.prefix || e.prefixIcon
                                ? (j(),
                                  M(
                                    "span",
                                    { key: 0, class: N(A(ue).e("prefix")) },
                                    [
                                      H(
                                        "span",
                                        { class: N(A(ue).e("prefix-inner")) },
                                        [
                                          T(e.$slots, "prefix"),
                                          e.prefixIcon
                                            ? (j(),
                                              O(
                                                A(L),
                                                {
                                                  key: 0,
                                                  class: N(A(ue).e("icon")),
                                                },
                                                {
                                                  default: K(() => [
                                                    (j(), O(W(e.prefixIcon))),
                                                  ]),
                                                  _: 1,
                                                },
                                                8,
                                                ["class"],
                                              ))
                                            : R("v-if", !0),
                                        ],
                                        2,
                                      ),
                                    ],
                                    2,
                                  ))
                                : R("v-if", !0),
                              H(
                                "input",
                                q(
                                  {
                                    id: A(oe),
                                    ref_key: "input",
                                    ref: ce,
                                    class: A(ue).e("inner"),
                                  },
                                  A(Q),
                                  {
                                    type: e.showPassword
                                      ? ge.value
                                        ? "text"
                                        : "password"
                                      : e.type,
                                    disabled: A(ie),
                                    formatter: e.formatter,
                                    parser: e.parser,
                                    readonly: e.readonly,
                                    autocomplete: e.autocomplete,
                                    tabindex: e.tabindex,
                                    "aria-label": e.label,
                                    placeholder: e.placeholder,
                                    style: e.inputStyle,
                                    form: p.form,
                                    onCompositionstart: Ye,
                                    onCompositionupdate: De,
                                    onCompositionend: Je,
                                    onInput: qe,
                                    onFocus:
                                      a[0] ||
                                      (a[0] = (...e) => A(Ce) && A(Ce)(...e)),
                                    onBlur:
                                      a[1] ||
                                      (a[1] = (...e) => A(Ee) && A(Ee)(...e)),
                                    onChange: Ue,
                                    onKeydown: ea,
                                  },
                                ),
                                null,
                                16,
                                me,
                              ),
                              R(" suffix slot "),
                              A(Te)
                                ? (j(),
                                  M(
                                    "span",
                                    { key: 1, class: N(A(ue).e("suffix")) },
                                    [
                                      H(
                                        "span",
                                        { class: N(A(ue).e("suffix-inner")) },
                                        [
                                          A(Me) && A(Re) && A(Ve)
                                            ? R("v-if", !0)
                                            : (j(),
                                              M(
                                                V,
                                                { key: 0 },
                                                [
                                                  T(e.$slots, "suffix"),
                                                  e.suffixIcon
                                                    ? (j(),
                                                      O(
                                                        A(L),
                                                        {
                                                          key: 0,
                                                          class: N(
                                                            A(ue).e("icon"),
                                                          ),
                                                        },
                                                        {
                                                          default: K(() => [
                                                            (j(),
                                                            O(W(e.suffixIcon))),
                                                          ]),
                                                          _: 1,
                                                        },
                                                        8,
                                                        ["class"],
                                                      ))
                                                    : R("v-if", !0),
                                                ],
                                                64,
                                              )),
                                          A(Me)
                                            ? (j(),
                                              O(
                                                A(L),
                                                {
                                                  key: 1,
                                                  class: N([
                                                    A(ue).e("icon"),
                                                    A(ue).e("clear"),
                                                  ]),
                                                  onMousedown: D(A(J), [
                                                    "prevent",
                                                  ]),
                                                  onClick: aa,
                                                },
                                                {
                                                  default: K(() => [U(A(Y))]),
                                                  _: 1,
                                                },
                                                8,
                                                ["class", "onMousedown"],
                                              ))
                                            : R("v-if", !0),
                                          A(Re)
                                            ? (j(),
                                              O(
                                                A(L),
                                                {
                                                  key: 2,
                                                  class: N([
                                                    A(ue).e("icon"),
                                                    A(ue).e("password"),
                                                  ]),
                                                  onClick: Ze,
                                                },
                                                {
                                                  default: K(() => [
                                                    (j(), O(W(A(Be)))),
                                                  ]),
                                                  _: 1,
                                                },
                                                8,
                                                ["class"],
                                              ))
                                            : R("v-if", !0),
                                          A(Ve)
                                            ? (j(),
                                              M(
                                                "span",
                                                {
                                                  key: 3,
                                                  class: N(A(ue).e("count")),
                                                },
                                                [
                                                  H(
                                                    "span",
                                                    {
                                                      class: N(
                                                        A(ue).e("count-inner"),
                                                      ),
                                                    },
                                                    Z(A(Ne)) +
                                                      " / " +
                                                      Z(A(Q).maxlength),
                                                    3,
                                                  ),
                                                ],
                                                2,
                                              ))
                                            : R("v-if", !0),
                                          A(Ie) && A($e) && A(Fe)
                                            ? (j(),
                                              O(
                                                A(L),
                                                {
                                                  key: 4,
                                                  class: N([
                                                    A(ue).e("icon"),
                                                    A(ue).e("validateIcon"),
                                                    A(ue).is(
                                                      "loading",
                                                      "validating" === A(Ie),
                                                    ),
                                                  ]),
                                                },
                                                {
                                                  default: K(() => [
                                                    (j(), O(W(A($e)))),
                                                  ]),
                                                  _: 1,
                                                },
                                                8,
                                                ["class"],
                                              ))
                                            : R("v-if", !0),
                                        ],
                                        2,
                                      ),
                                    ],
                                    2,
                                  ))
                                : R("v-if", !0),
                            ],
                            2,
                          ),
                          R(" append slot "),
                          e.$slots.append
                            ? (j(),
                              M(
                                "div",
                                {
                                  key: 1,
                                  class: N(A(ue).be("group", "append")),
                                },
                                [T(e.$slots, "append")],
                                2,
                              ))
                            : R("v-if", !0),
                        ],
                        64,
                      ))
                    : (j(),
                      M(
                        V,
                        { key: 1 },
                        [
                          R(" textarea "),
                          H(
                            "textarea",
                            q(
                              {
                                id: A(oe),
                                ref_key: "textarea",
                                ref: ve,
                                class: A(pe).e("inner"),
                              },
                              A(Q),
                              {
                                tabindex: e.tabindex,
                                disabled: A(ie),
                                readonly: e.readonly,
                                autocomplete: e.autocomplete,
                                style: A(_e),
                                "aria-label": e.label,
                                placeholder: e.placeholder,
                                form: p.form,
                                onCompositionstart: Ye,
                                onCompositionupdate: De,
                                onCompositionend: Je,
                                onInput: qe,
                                onFocus:
                                  a[2] ||
                                  (a[2] = (...e) => A(Ce) && A(Ce)(...e)),
                                onBlur:
                                  a[3] ||
                                  (a[3] = (...e) => A(Ee) && A(Ee)(...e)),
                                onChange: Ue,
                                onKeydown: ea,
                              },
                            ),
                            null,
                            16,
                            ye,
                          ),
                          A(Ve)
                            ? (j(),
                              M(
                                "span",
                                {
                                  key: 0,
                                  style: G(he.value),
                                  class: N(A(ue).e("count")),
                                },
                                Z(A(Ne)) + " / " + Z(A(Q).maxlength),
                                7,
                              ))
                            : R("v-if", !0),
                        ],
                        64,
                      )),
                ],
                16,
                fe,
              )),
              [[_, "hidden" !== e.type]],
            )
        );
      },
    }),
    [
      [
        "__file",
        "/home/runner/work/element-plus/element-plus/packages/components/input/src/input.vue",
      ],
    ],
  ),
);
export { be as E, le as a, ne as i, re as u };
