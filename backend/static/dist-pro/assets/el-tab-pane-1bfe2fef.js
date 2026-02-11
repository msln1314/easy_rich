import {
  ab as e,
  ag as a,
  b as t,
  d as l,
  an as s,
  e as o,
  aq as n,
  ao as r,
  ar as i,
  u,
  r as d,
  w as c,
  as as v,
  at as p,
  o as b,
  j as m,
  s as f,
  k as h,
  n as y,
  _ as g,
  au as x,
  av as C,
  f as w,
  a2 as $,
  aw as k,
  x as P,
  E as N,
  ax as T,
  ay as B,
  az as S,
  aA as E,
  aB as R,
  am as A,
  aC as F,
  q as _,
  aD as j,
  g as q,
  i as L,
  aE as K,
  aF as z,
  L as V,
  aG as H,
  a0 as M,
  aH as U,
  F as D,
  t as G,
  a8 as O,
} from "./index-6b60d190.js";
import { c as W } from "./strings-00317668.js";
import { U as X } from "./event-5568c9d8.js";
import { f as Y } from "./vnode-34f6d346.js";
const I = (t, l) => {
    const s = {},
      o = e([]);
    return {
      children: o,
      addChild: (e) => {
        ((s[e.uid] = e),
          (o.value = ((e, t, l) =>
            Y(e.subTree)
              .filter((e) => {
                var l;
                return (
                  a(e) &&
                  (null == (l = e.type) ? void 0 : l.name) === t &&
                  !!e.component
                );
              })
              .map((e) => e.component.uid)
              .map((e) => l[e])
              .filter((e) => !!e))(t, l, s)));
      },
      removeChild: (e) => {
        (delete s[e], (o.value = o.value.filter((a) => a.uid !== e)));
      },
    };
  },
  J = Symbol("tabsRootContextKey"),
  Q = t({ tabs: { type: l(Array), default: () => s([]) } }),
  Z = "ElTabBar",
  ee = o({ name: Z });
var ae = g(
  o({
    ...ee,
    props: Q,
    setup(e, { expose: a }) {
      const t = e,
        l = n(),
        s = r(J);
      s || i(Z, "<el-tabs><el-tab-bar /></el-tabs>");
      const o = u("tabs"),
        g = d(),
        x = d(),
        C = () =>
          (x.value = (() => {
            let e = 0,
              a = 0;
            const o = ["top", "bottom"].includes(s.props.tabPosition)
                ? "width"
                : "height",
              n = "width" === o ? "x" : "y",
              r = "x" === n ? "left" : "top";
            return (
              t.tabs.every((s) => {
                var n, i;
                const u =
                  null == (i = null == (n = l.parent) ? void 0 : n.refs)
                    ? void 0
                    : i[`tab-${s.uid}`];
                if (!u) return !1;
                if (!s.active) return !0;
                ((e = u[`offset${W(r)}`]), (a = u[`client${W(o)}`]));
                const d = window.getComputedStyle(u);
                return (
                  "width" === o &&
                    (t.tabs.length > 1 &&
                      (a -=
                        Number.parseFloat(d.paddingLeft) +
                        Number.parseFloat(d.paddingRight)),
                    (e += Number.parseFloat(d.paddingLeft))),
                  !1
                );
              }),
              { [o]: `${a}px`, transform: `translate${W(n)}(${e}px)` }
            );
          })());
      return (
        c(
          () => t.tabs,
          async () => {
            (await v(), C());
          },
          { immediate: !0 },
        ),
        p(g, () => C()),
        a({ ref: g, update: C }),
        (e, a) => (
          b(),
          m(
            "div",
            {
              ref_key: "barRef",
              ref: g,
              class: f([h(o).e("active-bar"), h(o).is(h(s).props.tabPosition)]),
              style: y(x.value),
            },
            null,
            6,
          )
        )
      );
    },
  }),
  [
    [
      "__file",
      "/home/runner/work/element-plus/element-plus/packages/components/tabs/src/tab-bar.vue",
    ],
  ],
);
const te = t({
    panes: { type: l(Array), default: () => s([]) },
    currentName: { type: [String, Number], default: "" },
    editable: Boolean,
    type: { type: String, values: ["card", "border-card", ""], default: "" },
    stretch: Boolean,
  }),
  le = "ElTabNav",
  se = o({
    name: le,
    props: te,
    emits: {
      tabClick: (e, a, t) => t instanceof Event,
      tabRemove: (e, a) => a instanceof Event,
    },
    setup(e, { expose: a, emit: t }) {
      const l = n(),
        s = r(J);
      s || i(le, "<el-tabs><tab-nav /></el-tabs>");
      const o = u("tabs"),
        b = x(),
        m = C(),
        f = d(),
        h = d(),
        y = d(),
        g = d(),
        R = d(!1),
        A = d(0),
        F = d(!1),
        _ = d(!0),
        j = w(() =>
          ["top", "bottom"].includes(s.props.tabPosition) ? "width" : "height",
        ),
        q = w(() => ({
          transform: `translate${"width" === j.value ? "X" : "Y"}(-${A.value}px)`,
        })),
        L = () => {
          if (!f.value) return;
          const e = f.value[`offset${W(j.value)}`],
            a = A.value;
          if (!a) return;
          const t = a > e ? a - e : 0;
          A.value = t;
        },
        K = () => {
          if (!f.value || !h.value) return;
          const e = h.value[`offset${W(j.value)}`],
            a = f.value[`offset${W(j.value)}`],
            t = A.value;
          if (e - t <= a) return;
          const l = e - t > 2 * a ? t + a : e - a;
          A.value = l;
        },
        z = async () => {
          const e = h.value;
          if (!(R.value && y.value && f.value && e)) return;
          await v();
          const a = y.value.querySelector(".is-active");
          if (!a) return;
          const t = f.value,
            l = ["top", "bottom"].includes(s.props.tabPosition),
            o = a.getBoundingClientRect(),
            n = t.getBoundingClientRect(),
            r = l ? e.offsetWidth - n.width : e.offsetHeight - n.height,
            i = A.value;
          let u = i;
          (l
            ? (o.left < n.left && (u = i - (n.left - o.left)),
              o.right > n.right && (u = i + o.right - n.right))
            : (o.top < n.top && (u = i - (n.top - o.top)),
              o.bottom > n.bottom && (u = i + (o.bottom - n.bottom))),
            (u = Math.max(u, 0)),
            (A.value = Math.min(u, r)));
        },
        V = () => {
          var a;
          if (!h.value || !f.value) return;
          e.stretch && (null == (a = g.value) || a.update());
          const t = h.value[`offset${W(j.value)}`],
            l = f.value[`offset${W(j.value)}`],
            s = A.value;
          l < t
            ? ((R.value = R.value || {}),
              (R.value.prev = s),
              (R.value.next = s + l < t),
              t - s < l && (A.value = t - l))
            : ((R.value = !1), s > 0 && (A.value = 0));
        },
        H = (e) => {
          const a = e.code,
            { up: t, down: l, left: s, right: o } = E;
          if (![t, l, s, o].includes(a)) return;
          const n = Array.from(
              e.currentTarget.querySelectorAll("[role=tab]:not(.is-disabled)"),
            ),
            r = n.indexOf(e.target);
          let i;
          ((i =
            a === s || a === t
              ? 0 === r
                ? n.length - 1
                : r - 1
              : r < n.length - 1
                ? r + 1
                : 0),
            n[i].focus({ preventScroll: !0 }),
            n[i].click(),
            M());
        },
        M = () => {
          _.value && (F.value = !0);
        },
        U = () => (F.value = !1);
      return (
        c(b, (e) => {
          "hidden" === e
            ? (_.value = !1)
            : "visible" === e && setTimeout(() => (_.value = !0), 50);
        }),
        c(m, (e) => {
          e ? setTimeout(() => (_.value = !0), 50) : (_.value = !1);
        }),
        p(y, V),
        $(() => setTimeout(() => z(), 0)),
        k(() => V()),
        a({ scrollToActiveTab: z, removeFocus: U }),
        c(
          () => e.panes,
          () => l.update(),
          { flush: "post", deep: !0 },
        ),
        () => {
          const a = R.value
              ? [
                  P(
                    "span",
                    {
                      class: [o.e("nav-prev"), o.is("disabled", !R.value.prev)],
                      onClick: L,
                    },
                    [P(N, null, { default: () => [P(T, null, null)] })],
                  ),
                  P(
                    "span",
                    {
                      class: [o.e("nav-next"), o.is("disabled", !R.value.next)],
                      onClick: K,
                    },
                    [P(N, null, { default: () => [P(B, null, null)] })],
                  ),
                ]
              : null,
            l = e.panes.map((a, l) => {
              var n, r, i, u;
              const d = a.uid,
                c = a.props.disabled,
                v =
                  null != (r = null != (n = a.props.name) ? n : a.index)
                    ? r
                    : `${l}`,
                p = !c && (a.isClosable || e.editable);
              a.index = `${l}`;
              const b = p
                  ? P(
                      N,
                      {
                        class: "is-icon-close",
                        onClick: (e) => t("tabRemove", a, e),
                      },
                      { default: () => [P(S, null, null)] },
                    )
                  : null,
                m =
                  (null == (u = (i = a.slots).label) ? void 0 : u.call(i)) ||
                  a.props.label,
                f = !c && a.active ? 0 : -1;
              return P(
                "div",
                {
                  ref: `tab-${d}`,
                  class: [
                    o.e("item"),
                    o.is(s.props.tabPosition),
                    o.is("active", a.active),
                    o.is("disabled", c),
                    o.is("closable", p),
                    o.is("focus", F.value),
                  ],
                  id: `tab-${v}`,
                  key: `tab-${d}`,
                  "aria-controls": `pane-${v}`,
                  role: "tab",
                  "aria-selected": a.active,
                  tabindex: f,
                  onFocus: () => M(),
                  onBlur: () => U(),
                  onClick: (e) => {
                    (U(), t("tabClick", a, v, e));
                  },
                  onKeydown: (e) => {
                    !p ||
                      (e.code !== E.delete && e.code !== E.backspace) ||
                      t("tabRemove", a, e);
                  },
                },
                [m, b],
              );
            });
          return P(
            "div",
            {
              ref: y,
              class: [
                o.e("nav-wrap"),
                o.is("scrollable", !!R.value),
                o.is(s.props.tabPosition),
              ],
            },
            [
              a,
              P("div", { class: o.e("nav-scroll"), ref: f }, [
                P(
                  "div",
                  {
                    class: [
                      o.e("nav"),
                      o.is(s.props.tabPosition),
                      o.is(
                        "stretch",
                        e.stretch &&
                          ["top", "bottom"].includes(s.props.tabPosition),
                      ),
                    ],
                    ref: h,
                    style: q.value,
                    role: "tablist",
                    onKeydown: H,
                  },
                  [
                    e.type ? null : P(ae, { ref: g, tabs: [...e.panes] }, null),
                    l,
                  ],
                ),
              ]),
            ],
          );
        }
      );
    },
  }),
  oe = t({
    type: { type: String, values: ["card", "border-card", ""], default: "" },
    activeName: { type: [String, Number] },
    closable: Boolean,
    addable: Boolean,
    modelValue: { type: [String, Number] },
    editable: Boolean,
    tabPosition: {
      type: String,
      values: ["top", "right", "bottom", "left"],
      default: "top",
    },
    beforeLeave: { type: l(Function), default: () => !0 },
    stretch: Boolean,
  }),
  ne = (e) => q(e) || L(e);
var re = o({
  name: "ElTabs",
  props: oe,
  emits: {
    [X]: (e) => ne(e),
    tabClick: (e, a) => a instanceof Event,
    tabChange: (e) => ne(e),
    edit: (e, a) => ["remove", "add"].includes(a),
    tabRemove: (e) => ne(e),
    tabAdd: () => !0,
  },
  setup(e, { emit: a, slots: t, expose: l }) {
    var s, o;
    const r = u("tabs"),
      { children: i, addChild: p, removeChild: b } = I(n(), "ElTabPane"),
      m = d(),
      f = d(
        null != (o = null != (s = e.modelValue) ? s : e.activeName) ? o : "0",
      ),
      h = async (t) => {
        var l, s, o;
        if (f.value !== t && !j(t))
          try {
            !1 !==
              (await (null == (l = e.beforeLeave)
                ? void 0
                : l.call(e, t, f.value))) &&
              (((e) => {
                ((f.value = e), a(X, e), a("tabChange", e));
              })(t),
              null == (o = null == (s = m.value) ? void 0 : s.removeFocus) ||
                o.call(s));
          } catch (n) {}
      },
      y = (e, t, l) => {
        e.props.disabled || (h(t), a("tabClick", e, l));
      },
      g = (e, t) => {
        e.props.disabled ||
          j(e.props.name) ||
          (t.stopPropagation(),
          a("edit", e.props.name, "remove"),
          a("tabRemove", e.props.name));
      },
      x = () => {
        (a("edit", void 0, "add"), a("tabAdd"));
      };
    return (
      R(
        {
          from: '"activeName"',
          replacement: '"model-value" or "v-model"',
          scope: "ElTabs",
          version: "2.3.0",
          ref: "https://element-plus.org/en-US/component/tabs.html#attributes",
          type: "Attribute",
        },
        w(() => !!e.activeName),
      ),
      c(
        () => e.activeName,
        (e) => h(e),
      ),
      c(
        () => e.modelValue,
        (e) => h(e),
      ),
      c(f, async () => {
        var e;
        (await v(), null == (e = m.value) || e.scrollToActiveTab());
      }),
      A(J, { props: e, currentName: f, registerPane: p, unregisterPane: b }),
      l({ currentName: f }),
      () => {
        const a =
            e.editable || e.addable
              ? P(
                  "span",
                  {
                    class: r.e("new-tab"),
                    tabindex: "0",
                    onClick: x,
                    onKeydown: (e) => {
                      e.code === E.enter && x();
                    },
                  },
                  [
                    P(
                      N,
                      { class: r.is("icon-plus") },
                      { default: () => [P(F, null, null)] },
                    ),
                  ],
                )
              : null,
          l = P("div", { class: [r.e("header"), r.is(e.tabPosition)] }, [
            a,
            P(
              se,
              {
                ref: m,
                currentName: f.value,
                editable: e.editable,
                type: e.type,
                panes: i.value,
                stretch: e.stretch,
                onTabClick: y,
                onTabRemove: g,
              },
              null,
            ),
          ]),
          s = P("div", { class: r.e("content") }, [_(t, "default")]);
        return P(
          "div",
          {
            class: [
              r.b(),
              r.m(e.tabPosition),
              {
                [r.m("card")]: "card" === e.type,
                [r.m("border-card")]: "border-card" === e.type,
              },
            ],
          },
          [...("bottom" !== e.tabPosition ? [l, s] : [s, l])],
        );
      }
    );
  },
});
const ie = t({
    label: { type: String, default: "" },
    name: { type: [String, Number] },
    closable: Boolean,
    disabled: Boolean,
    lazy: Boolean,
  }),
  ue = ["id", "aria-hidden", "aria-labelledby"],
  de = "ElTabPane",
  ce = o({ name: de });
var ve = g(
  o({
    ...ce,
    props: ie,
    setup(e) {
      const a = e,
        t = n(),
        l = K(),
        s = r(J);
      s || i(de, "usage: <el-tabs><el-tab-pane /></el-tabs/>");
      const o = u("tab-pane"),
        v = d(),
        p = w(() => a.closable || s.props.closable),
        y = z(() => {
          var e;
          return s.currentName.value === (null != (e = a.name) ? e : v.value);
        }),
        g = d(y.value),
        x = w(() => {
          var e;
          return null != (e = a.name) ? e : v.value;
        }),
        C = z(() => !a.lazy || g.value || y.value);
      c(y, (e) => {
        e && (g.value = !0);
      });
      const k = V({
        uid: t.uid,
        slots: l,
        props: a,
        paneName: x,
        active: y,
        index: v,
        isClosable: p,
      });
      return (
        $(() => {
          s.registerPane(k);
        }),
        H(() => {
          s.unregisterPane(k.uid);
        }),
        (e, a) =>
          h(C)
            ? M(
                (b(),
                m(
                  "div",
                  {
                    key: 0,
                    id: `pane-${h(x)}`,
                    class: f(h(o).b()),
                    role: "tabpanel",
                    "aria-hidden": !h(y),
                    "aria-labelledby": `tab-${h(x)}`,
                  },
                  [_(e.$slots, "default")],
                  10,
                  ue,
                )),
                [[U, h(y)]],
              )
            : D("v-if", !0)
      );
    },
  }),
  [
    [
      "__file",
      "/home/runner/work/element-plus/element-plus/packages/components/tabs/src/tab-pane.vue",
    ],
  ],
);
const pe = G(re, { TabPane: ve }),
  be = O(ve);
export { pe as E, be as a };
