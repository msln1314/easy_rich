import {
  ab as e,
  r as t,
  by as l,
  a2 as a,
  ar as o,
  d7 as n,
  e as r,
  u as s,
  f as u,
  o as i,
  l as c,
  m as d,
  k as p,
  j as v,
  n as m,
  s as h,
  aY as f,
  q as g,
  x,
  E as b,
  dV as y,
  F as w,
  D as _,
  _ as C,
  t as k,
  b as M,
  a as I,
  am as T,
  d as $,
  aq as V,
  ao as S,
  y as j,
  p as P,
  z as L,
  a8 as B,
  aA as z,
  a6 as A,
  cq as E,
  cp as O,
  bq as R,
  dW as H,
  aB as N,
  bd as U,
  ay as F,
  L as q,
  w as D,
  aj as W,
  a$ as G,
  g as Z,
  a0 as K,
  aH as Q,
  a1 as Y,
  du as J,
  an as X,
  bh as ee,
  at as te,
  dX as le,
  ap as ae,
  as as oe,
  a4 as ne,
  b1 as re,
  M as se,
  H as ue,
  I as ie,
  al as ce,
  dY as de,
  dZ as pe,
  B as ve,
  A as me,
  K as he,
  G as fe,
  ag as ge,
  J as xe,
  b5 as be,
  Z as ye,
  a5 as we,
  d_ as _e,
  d$ as Ce,
  e0 as ke,
  e1 as Me,
  ad as Ie,
  aI as Te,
  N as $e,
  Q as Ve,
  R as Se,
  e2 as je,
  e3 as Pe,
  bw as Le,
  v as Be,
  bZ as ze,
  e4 as Ae,
  T as Ee,
  e5 as Oe,
  e6 as Re,
  e7 as He,
  dx as Ne,
  af as Ue,
  S as Fe,
} from "./index-6b60d190.js";
import "./el-tooltip-4ed993c7.js";
import { E as qe } from "./el-popper-09548d54.js";
import { f as De, a as We, t as Ge } from "./tree-ae7cba8b.js";
import { t as Ze, u as Ke, F as Qe } from "./useForm-b6ceb895.js";
import { _ as Ye } from "./index-55fef7b1.js";
import { f as Je } from "./vnode-34f6d346.js";
import { i as Xe } from "./isNil-1f22f7b0.js";
import { C as et } from "./index-fdfa028a.js";
import { E as tt, b as lt, a as at } from "./el-dropdown-item-943c2eb7.js";
import { _ as ot } from "./Footer.vue_vue_type_script_setup_true_lang-c9dc208e.js";
import {
  T as nt,
  _ as rt,
} from "./LocaleDropdown.vue_vue_type_script_setup_true_lang-1e29b4aa.js";
import { E as st } from "./el-message-box-2d28828b.js";
import { E as ut } from "./el-input-38d674e5.js";
import "./el-overlay-2c5c0104.js";
import { a as it } from "./avatar-d437f563.js";
import { _ as ct } from "./Dialog.vue_vue_type_style_index_0_lang-d732453c.js";
import { u as dt } from "./useValidator-63200dcb.js";
import { d as pt } from "./el-date-picker-91f17f23.js";
import { E as vt } from "./el-drawer-64f23d0f.js";
import { E as mt } from "./el-divider-2dd0a1ee.js";
import { E as ht } from "./el-switch-5507f2ea.js";
import "./focus-trap-275966d8.js";
import "./el-form-item-ce18addb.js";
import "./el-col-b8aa0d1a.js";
/* empty css               */ import "./el-checkbox-4903f610.js";
import "./event-5568c9d8.js";
import "./isEqual-b8d86c27.js";
/* empty css                          */ import "./el-radio-group-0c46635e.js";
import "./el-select-8805ff65.js";
import "./index-b7c1540b.js";
import "./strings-00317668.js";
import "./scroll-6dba6951.js";
import "./debounce-5c500a3d.js";
import "./validator-f032316f.js";
import "./el-tree-84af12f2.js";
import "./el-progress-31e0b945.js";
import "./style.css_vue_type_style_index_0_src_true_lang-d8fdefc2.js";
import "./dropdown-84a04b2c.js";
import "./refs-64421a9c.js";
import "./useIcon-7641a992.js";
import "./index-62254dd8.js";
import "./use-dialog-0e1ee265.js";
const ft = {
    visibilityHeight: { type: Number, default: 200 },
    target: { type: String, default: "" },
    right: { type: Number, default: 40 },
    bottom: { type: Number, default: 40 },
  },
  gt = { click: (e) => e instanceof MouseEvent },
  xt = "ElBacktop",
  bt = r({ name: xt });
const yt = k(
    C(
      r({
        ...bt,
        props: ft,
        emits: gt,
        setup(r, { emit: C }) {
          const k = r,
            M = s("backtop"),
            { handleClick: I, visible: T } = ((r, s, u) => {
              const i = e(),
                c = e(),
                d = t(!1),
                p = () => {
                  i.value &&
                    (d.value = i.value.scrollTop >= r.visibilityHeight);
                },
                v = n(p, 300, !0);
              return (
                l(c, "scroll", v),
                a(() => {
                  var e;
                  ((c.value = document),
                    (i.value = document.documentElement),
                    r.target &&
                      ((i.value =
                        null != (e = document.querySelector(r.target))
                          ? e
                          : void 0),
                      i.value || o(u, `target does not exist: ${r.target}`),
                      (c.value = i.value)),
                    p());
                }),
                {
                  visible: d,
                  handleClick: (e) => {
                    var t;
                    (null == (t = i.value) ||
                      t.scrollTo({ top: 0, behavior: "smooth" }),
                      s("click", e));
                  },
                }
              );
            })(k, C, xt),
            $ = u(() => ({ right: `${k.right}px`, bottom: `${k.bottom}px` }));
          return (e, t) => (
            i(),
            c(
              _,
              { name: `${p(M).namespace.value}-fade-in` },
              {
                default: d(() => [
                  p(T)
                    ? (i(),
                      v(
                        "div",
                        {
                          key: 0,
                          style: m(p($)),
                          class: h(p(M).b()),
                          onClick:
                            t[0] ||
                            (t[0] = f((...e) => p(I) && p(I)(...e), ["stop"])),
                        },
                        [
                          g(e.$slots, "default", {}, () => [
                            x(
                              p(b),
                              { class: h(p(M).e("icon")) },
                              { default: d(() => [x(p(y))]), _: 1 },
                              8,
                              ["class"],
                            ),
                          ]),
                        ],
                        6,
                      ))
                    : w("v-if", !0),
                ]),
                _: 3,
              },
              8,
              ["name"],
            )
          );
        },
      }),
      [
        [
          "__file",
          "/home/runner/work/element-plus/element-plus/packages/components/backtop/src/backtop.vue",
        ],
      ],
    ),
  ),
  wt = Symbol("breadcrumbKey"),
  _t = M({
    separator: { type: String, default: "/" },
    separatorIcon: { type: I },
  }),
  Ct = r({ name: "ElBreadcrumb" });
var kt = C(
  r({
    ...Ct,
    props: _t,
    setup(e) {
      const l = e,
        o = s("breadcrumb"),
        n = t();
      return (
        T(wt, l),
        a(() => {
          const e = n.value.querySelectorAll(`.${o.e("item")}`);
          e.length && e[e.length - 1].setAttribute("aria-current", "page");
        }),
        (e, t) => (
          i(),
          v(
            "div",
            {
              ref_key: "breadcrumb",
              ref: n,
              class: h(p(o).b()),
              "aria-label": "Breadcrumb",
              role: "navigation",
            },
            [g(e.$slots, "default")],
            2,
          )
        )
      );
    },
  }),
  [
    [
      "__file",
      "/home/runner/work/element-plus/element-plus/packages/components/breadcrumb/src/breadcrumb.vue",
    ],
  ],
);
const Mt = M({
    to: { type: $([String, Object]), default: "" },
    replace: { type: Boolean, default: !1 },
  }),
  It = r({ name: "ElBreadcrumbItem" });
var Tt = C(
  r({
    ...It,
    props: Mt,
    setup(e) {
      const l = e,
        a = V(),
        o = S(wt, void 0),
        n = s("breadcrumb"),
        r = a.appContext.config.globalProperties.$router,
        u = t(),
        m = () => {
          l.to && r && (l.replace ? r.replace(l.to) : r.push(l.to));
        };
      return (e, t) => {
        var l, a;
        return (
          i(),
          v(
            "span",
            { class: h(p(n).e("item")) },
            [
              j(
                "span",
                {
                  ref_key: "link",
                  ref: u,
                  class: h([p(n).e("inner"), p(n).is("link", !!e.to)]),
                  role: "link",
                  onClick: m,
                },
                [g(e.$slots, "default")],
                2,
              ),
              (null == (l = p(o)) ? void 0 : l.separatorIcon)
                ? (i(),
                  c(
                    p(b),
                    { key: 0, class: h(p(n).e("separator")) },
                    {
                      default: d(() => [(i(), c(P(p(o).separatorIcon)))]),
                      _: 1,
                    },
                    8,
                    ["class"],
                  ))
                : (i(),
                  v(
                    "span",
                    {
                      key: 1,
                      class: h(p(n).e("separator")),
                      role: "presentation",
                    },
                    L(null == (a = p(o)) ? void 0 : a.separator),
                    3,
                  )),
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
      "/home/runner/work/element-plus/element-plus/packages/components/breadcrumb/src/breadcrumb-item.vue",
    ],
  ],
);
const $t = k(kt, { BreadcrumbItem: Tt }),
  Vt = B(Tt);
var St = C(
  r({
    name: "ElMenuCollapseTransition",
    setup() {
      const e = s("menu");
      return {
        listeners: {
          onBeforeEnter: (e) => (e.style.opacity = "0.2"),
          onEnter(t, l) {
            (E(t, `${e.namespace.value}-opacity-transition`),
              (t.style.opacity = "1"),
              l());
          },
          onAfterEnter(t) {
            (O(t, `${e.namespace.value}-opacity-transition`),
              (t.style.opacity = ""));
          },
          onBeforeLeave(t) {
            (t.dataset || (t.dataset = {}),
              R(t, e.m("collapse"))
                ? (O(t, e.m("collapse")),
                  (t.dataset.oldOverflow = t.style.overflow),
                  (t.dataset.scrollWidth = t.clientWidth.toString()),
                  E(t, e.m("collapse")))
                : (E(t, e.m("collapse")),
                  (t.dataset.oldOverflow = t.style.overflow),
                  (t.dataset.scrollWidth = t.clientWidth.toString()),
                  O(t, e.m("collapse"))),
              (t.style.width = `${t.scrollWidth}px`),
              (t.style.overflow = "hidden"));
          },
          onLeave(e) {
            (E(e, "horizontal-collapse-transition"),
              (e.style.width = `${e.dataset.scrollWidth}px`));
          },
        },
      };
    },
  }),
  [
    [
      "render",
      function (e, t, l, a, o, n) {
        return (
          i(),
          c(
            _,
            A({ mode: "out-in" }, e.listeners),
            { default: d(() => [g(e.$slots, "default")]), _: 3 },
            16,
          )
        );
      },
    ],
    [
      "__file",
      "/home/runner/work/element-plus/element-plus/packages/components/menu/src/menu-collapse-transition.vue",
    ],
  ],
);
function jt(e, t) {
  const l = u(() => {
    let l = e.parent;
    const a = [t.value];
    for (; "ElMenu" !== l.type.name; )
      (l.props.index && a.unshift(l.props.index), (l = l.parent));
    return a;
  });
  return {
    parentMenu: u(() => {
      let t = e.parent;
      for (; t && !["ElMenu", "ElSubMenu"].includes(t.type.name); )
        t = t.parent;
      return t;
    }),
    indexPath: l,
  };
}
function Pt(e) {
  return u(() => {
    const t = e.backgroundColor;
    return t ? new H(t).shade(20).toString() : "";
  });
}
const Lt = (e, t) => {
    const l = s("menu");
    return u(() =>
      l.cssVarBlock({
        "text-color": e.textColor || "",
        "hover-text-color": e.textColor || "",
        "bg-color": e.backgroundColor || "",
        "hover-bg-color": Pt(e).value || "",
        "active-color": e.activeTextColor || "",
        level: `${t}`,
      }),
    );
  },
  Bt = M({
    index: { type: String, required: !0 },
    showTimeout: { type: Number, default: 300 },
    hideTimeout: { type: Number, default: 300 },
    popperClass: String,
    disabled: Boolean,
    popperAppendToBody: { type: Boolean, default: void 0 },
    teleported: { type: Boolean, default: void 0 },
    popperOffset: { type: Number, default: 6 },
    expandCloseIcon: { type: I },
    expandOpenIcon: { type: I },
    collapseCloseIcon: { type: I },
    collapseOpenIcon: { type: I },
  }),
  zt = "ElSubMenu";
var At = r({
  name: zt,
  props: Bt,
  setup(e, { slots: l, expose: n }) {
    N(
      {
        from: "popper-append-to-body",
        replacement: "teleported",
        scope: zt,
        version: "2.3.0",
        ref: "https://element-plus.org/en-US/component/menu.html#submenu-attributes",
      },
      u(() => void 0 !== e.popperAppendToBody),
    );
    const r = V(),
      { indexPath: i, parentMenu: c } = jt(
        r,
        u(() => e.index),
      ),
      d = s("menu"),
      p = s("sub-menu"),
      v = S("rootMenu");
    v || o(zt, "can not inject root menu");
    const m = S(`subMenu:${c.value.uid}`);
    m || o(zt, "can not inject sub menu");
    const h = t({}),
      f = t({});
    let g;
    const x = t(!1),
      y = t(),
      w = t(null),
      _ = u(() =>
        "horizontal" === A.value && k.value ? "bottom-start" : "right-start",
      ),
      C = u(() =>
        ("horizontal" === A.value && k.value) ||
        ("vertical" === A.value && !v.props.collapse)
          ? e.expandCloseIcon && e.expandOpenIcon
            ? j.value
              ? e.expandOpenIcon
              : e.expandCloseIcon
            : U
          : e.collapseCloseIcon && e.collapseOpenIcon
            ? j.value
              ? e.collapseOpenIcon
              : e.collapseCloseIcon
            : F,
      ),
      k = u(() => 0 === m.level),
      M = u(() => {
        var t;
        const l = null != (t = e.teleported) ? t : e.popperAppendToBody;
        return void 0 === l ? k.value : l;
      }),
      I = u(() =>
        v.props.collapse
          ? `${d.namespace.value}-zoom-in-left`
          : `${d.namespace.value}-zoom-in-top`,
      ),
      $ = u(() =>
        "horizontal" === A.value && k.value
          ? [
              "bottom-start",
              "bottom-end",
              "top-start",
              "top-end",
              "right-start",
              "left-start",
            ]
          : [
              "right-start",
              "right",
              "right-end",
              "left-start",
              "bottom-start",
              "bottom-end",
              "top-start",
              "top-end",
            ],
      ),
      j = u(() => v.openedMenus.includes(e.index)),
      P = u(() => {
        let e = !1;
        return (
          Object.values(h.value).forEach((t) => {
            t.active && (e = !0);
          }),
          Object.values(f.value).forEach((t) => {
            t.active && (e = !0);
          }),
          e
        );
      }),
      L = u(() => v.props.backgroundColor || ""),
      B = u(() => v.props.activeTextColor || ""),
      z = u(() => v.props.textColor || ""),
      A = u(() => v.props.mode),
      E = q({ index: e.index, indexPath: i, active: P }),
      O = Lt(v.props, m.level + 1),
      R = u(() =>
        "horizontal" !== A.value
          ? { color: z.value }
          : {
              borderBottomColor: P.value
                ? v.props.activeTextColor
                  ? B.value
                  : ""
                : "transparent",
              color: P.value ? B.value : z.value,
            },
      ),
      H = (e) => {
        var t, l, a;
        e ||
          null ==
            (a =
              null == (l = null == (t = w.value) ? void 0 : t.popperRef)
                ? void 0
                : l.popperInstanceRef) ||
          a.destroy();
      },
      X = () => {
        ("hover" === v.props.menuTrigger && "horizontal" === v.props.mode) ||
          (v.props.collapse && "vertical" === v.props.mode) ||
          e.disabled ||
          v.handleSubMenuClick({
            index: e.index,
            indexPath: i.value,
            active: P.value,
          });
      },
      ee = (t, l = e.showTimeout) => {
        var a;
        "focus" !== t.type &&
          (("click" === v.props.menuTrigger && "horizontal" === v.props.mode) ||
            (!v.props.collapse && "vertical" === v.props.mode) ||
            e.disabled ||
            ((m.mouseInChild.value = !0),
            null == g || g(),
            ({ stop: g } = J(() => {
              v.openMenu(e.index, i.value);
            }, l)),
            M.value &&
              (null == (a = c.value.vnode.el) ||
                a.dispatchEvent(new MouseEvent("mouseenter")))));
      },
      te = (t = !1) => {
        var l, a;
        ("click" === v.props.menuTrigger && "horizontal" === v.props.mode) ||
          (!v.props.collapse && "vertical" === v.props.mode) ||
          (null == g || g(),
          (m.mouseInChild.value = !1),
          ({ stop: g } = J(
            () => !x.value && v.closeMenu(e.index, i.value),
            e.hideTimeout,
          )),
          M.value &&
            t &&
            "ElSubMenu" === (null == (l = r.parent) ? void 0 : l.type.name) &&
            (null == (a = m.handleMouseleave) || a.call(m, !0)));
      };
    D(
      () => v.props.collapse,
      (e) => H(Boolean(e)),
    );
    {
      const e = (e) => {
          f.value[e.index] = e;
        },
        t = (e) => {
          delete f.value[e.index];
        };
      T(`subMenu:${r.uid}`, {
        addSubMenu: e,
        removeSubMenu: t,
        handleMouseleave: te,
        mouseInChild: x,
        level: m.level + 1,
      });
    }
    return (
      n({ opened: j }),
      a(() => {
        (v.addSubMenu(E), m.addSubMenu(E));
      }),
      W(() => {
        (m.removeSubMenu(E), v.removeSubMenu(E));
      }),
      () => {
        var t;
        const a = [
            null == (t = l.title) ? void 0 : t.call(l),
            G(
              b,
              {
                class: p.e("icon-arrow"),
                style: {
                  transform: j.value
                    ? (e.expandCloseIcon && e.expandOpenIcon) ||
                      (e.collapseCloseIcon &&
                        e.collapseOpenIcon &&
                        v.props.collapse)
                      ? "none"
                      : "rotateZ(180deg)"
                    : "none",
                },
              },
              {
                default: () =>
                  Z(C.value) ? G(r.appContext.components[C.value]) : G(C.value),
              },
            ),
          ],
          o = v.isMenuPopup
            ? G(
                qe,
                {
                  ref: w,
                  visible: j.value,
                  effect: "light",
                  pure: !0,
                  offset: e.popperOffset,
                  showArrow: !1,
                  persistent: !0,
                  popperClass: e.popperClass,
                  placement: _.value,
                  teleported: M.value,
                  fallbackPlacements: $.value,
                  transition: I.value,
                  gpuAcceleration: !1,
                },
                {
                  content: () => {
                    var t;
                    return G(
                      "div",
                      {
                        class: [
                          d.m(A.value),
                          d.m("popup-container"),
                          e.popperClass,
                        ],
                        onMouseenter: (e) => ee(e, 100),
                        onMouseleave: () => te(!0),
                        onFocus: (e) => ee(e, 100),
                      },
                      [
                        G(
                          "ul",
                          {
                            class: [
                              d.b(),
                              d.m("popup"),
                              d.m(`popup-${_.value}`),
                            ],
                            style: O.value,
                          },
                          [null == (t = l.default) ? void 0 : t.call(l)],
                        ),
                      ],
                    );
                  },
                  default: () =>
                    G(
                      "div",
                      {
                        class: p.e("title"),
                        style: [R.value, { backgroundColor: L.value }],
                        onClick: X,
                      },
                      a,
                    ),
                },
              )
            : G(Y, {}, [
                G(
                  "div",
                  {
                    class: p.e("title"),
                    style: [R.value, { backgroundColor: L.value }],
                    ref: y,
                    onClick: X,
                  },
                  a,
                ),
                G(
                  Ye,
                  {},
                  {
                    default: () => {
                      var e;
                      return K(
                        G(
                          "ul",
                          {
                            role: "menu",
                            class: [d.b(), d.m("inline")],
                            style: O.value,
                          },
                          [null == (e = l.default) ? void 0 : e.call(l)],
                        ),
                        [[Q, j.value]],
                      );
                    },
                  },
                ),
              ]);
        return G(
          "li",
          {
            class: [
              p.b(),
              p.is("active", P.value),
              p.is("opened", j.value),
              p.is("disabled", e.disabled),
            ],
            role: "menuitem",
            ariaHaspopup: !0,
            ariaExpanded: j.value,
            onMouseenter: ee,
            onMouseleave: () => te(!0),
            onFocus: ee,
          },
          [o],
        );
      }
    );
  },
});
const Et = M({
    mode: {
      type: String,
      values: ["horizontal", "vertical"],
      default: "vertical",
    },
    defaultActive: { type: String, default: "" },
    defaultOpeneds: { type: $(Array), default: () => X([]) },
    uniqueOpened: Boolean,
    router: Boolean,
    menuTrigger: { type: String, values: ["hover", "click"], default: "hover" },
    collapse: Boolean,
    backgroundColor: String,
    textColor: String,
    activeTextColor: String,
    collapseTransition: { type: Boolean, default: !0 },
    ellipsis: { type: Boolean, default: !0 },
    popperEffect: { type: String, values: ["dark", "light"], default: "dark" },
  }),
  Ot = (e) => Array.isArray(e) && e.every((e) => Z(e));
var Rt = r({
  name: "ElMenu",
  props: Et,
  emits: {
    close: (e, t) => Z(e) && Ot(t),
    open: (e, t) => Z(e) && Ot(t),
    select: (e, t, l, a) =>
      Z(e) && Ot(t) && ae(l) && (void 0 === a || a instanceof Promise),
  },
  setup(e, { emit: l, slots: o, expose: n }) {
    const r = V(),
      i = r.appContext.config.globalProperties.$router,
      c = t(),
      d = s("menu"),
      p = s("sub-menu"),
      v = t(-1),
      m = t(e.defaultOpeneds && !e.collapse ? e.defaultOpeneds.slice(0) : []),
      h = t(e.defaultActive),
      f = t({}),
      g = t({}),
      x = u(
        () => "horizontal" === e.mode || ("vertical" === e.mode && e.collapse),
      ),
      y = (t, a) => {
        m.value.includes(t) ||
          (e.uniqueOpened && (m.value = m.value.filter((e) => a.includes(e))),
          m.value.push(t),
          l("open", t, a));
      },
      w = (e) => {
        const t = m.value.indexOf(e);
        -1 !== t && m.value.splice(t, 1);
      },
      _ = (e, t) => {
        (w(e), l("close", e, t));
      },
      C = ({ index: e, indexPath: t }) => {
        m.value.includes(e) ? _(e, t) : y(e, t);
      },
      k = (t) => {
        ("horizontal" === e.mode || e.collapse) && (m.value = []);
        const { index: a, indexPath: o } = t;
        if (!Xe(a) && !Xe(o))
          if (e.router && i) {
            const e = t.route || a,
              n = i.push(e).then((e) => (e || (h.value = a), e));
            l("select", a, o, { index: a, indexPath: o, route: e }, n);
          } else ((h.value = a), l("select", a, o, { index: a, indexPath: o }));
      };
    let M = !0;
    const I = () => {
      const e = () => {
        ((v.value = -1),
          oe(() => {
            v.value = (() => {
              var e, t;
              if (!c.value) return -1;
              const l = Array.from(
                  null != (t = null == (e = c.value) ? void 0 : e.childNodes)
                    ? t
                    : [],
                ).filter(
                  (e) =>
                    "#comment" !== e.nodeName &&
                    ("#text" !== e.nodeName || e.nodeValue),
                ),
                a = Number.parseInt(getComputedStyle(c.value).paddingLeft, 10),
                o = Number.parseInt(getComputedStyle(c.value).paddingRight, 10),
                n = c.value.clientWidth - a - o;
              let r = 0,
                s = 0;
              return (
                l.forEach((e, t) => {
                  ((r += e.offsetWidth || 0), r <= n - 64 && (s = t + 1));
                }),
                s === l.length ? -1 : s
              );
            })();
          }));
      };
      (M
        ? e()
        : ((e, t = 33.34) => {
            let l;
            return () => {
              (l && clearTimeout(l),
                (l = setTimeout(() => {
                  e();
                }, t)));
            };
          })(e)(),
        (M = !1));
    };
    let $;
    (D(
      () => e.defaultActive,
      (t) => {
        (f.value[t] || (h.value = ""),
          ((t) => {
            const l = f.value,
              a = l[t] || (h.value && l[h.value]) || l[e.defaultActive];
            h.value = a ? a.index : t;
          })(t));
      },
    ),
      D(
        () => e.collapse,
        (e) => {
          e && (m.value = []);
        },
      ),
      D(f.value, () => {
        const t = h.value && f.value[h.value];
        if (!t || "horizontal" === e.mode || e.collapse) return;
        t.indexPath.forEach((e) => {
          const t = g.value[e];
          t && y(e, t.indexPath);
        });
      }),
      ee(() => {
        "horizontal" === e.mode && e.ellipsis
          ? ($ = te(c, I).stop)
          : null == $ || $();
      }));
    {
      const l = (e) => {
          g.value[e.index] = e;
        },
        a = (e) => {
          delete g.value[e.index];
        },
        o = (e) => {
          f.value[e.index] = e;
        },
        n = (e) => {
          delete f.value[e.index];
        };
      (T(
        "rootMenu",
        q({
          props: e,
          openedMenus: m,
          items: f,
          subMenus: g,
          activeIndex: h,
          isMenuPopup: x,
          addMenuItem: o,
          removeMenuItem: n,
          addSubMenu: l,
          removeSubMenu: a,
          openMenu: y,
          closeMenu: _,
          handleMenuItemClick: k,
          handleSubMenuClick: C,
        }),
      ),
        T(`subMenu:${r.uid}`, {
          addSubMenu: l,
          removeSubMenu: a,
          mouseInChild: t(!1),
          level: 0,
        }));
    }
    a(() => {
      "horizontal" === e.mode &&
        new (class {
          constructor(e, t) {
            ((this.domNode = e), this.init(t));
          }
          init(e) {
            const t = this.domNode.childNodes;
            Array.from(t).forEach((t) => {
              1 === t.nodeType &&
                new (class {
                  constructor(e, t) {
                    ((this.domNode = e),
                      (this.submenu = null),
                      (this.submenu = null),
                      this.init(t));
                  }
                  init(e) {
                    this.domNode.setAttribute("tabindex", "0");
                    const t = this.domNode.querySelector(`.${e}-menu`);
                    (t &&
                      (this.submenu = new (class {
                        constructor(e, t) {
                          ((this.parent = e),
                            (this.domNode = t),
                            (this.subIndex = 0),
                            (this.subIndex = 0),
                            this.init());
                        }
                        init() {
                          ((this.subMenuItems =
                            this.domNode.querySelectorAll("li")),
                            this.addListeners());
                        }
                        gotoSubIndex(e) {
                          (e === this.subMenuItems.length
                            ? (e = 0)
                            : e < 0 && (e = this.subMenuItems.length - 1),
                            this.subMenuItems[e].focus(),
                            (this.subIndex = e));
                        }
                        addListeners() {
                          const e = this.parent.domNode;
                          Array.prototype.forEach.call(
                            this.subMenuItems,
                            (t) => {
                              t.addEventListener("keydown", (t) => {
                                let l = !1;
                                switch (t.code) {
                                  case z.down:
                                    (this.gotoSubIndex(this.subIndex + 1),
                                      (l = !0));
                                    break;
                                  case z.up:
                                    (this.gotoSubIndex(this.subIndex - 1),
                                      (l = !0));
                                    break;
                                  case z.tab:
                                    Ze(e, "mouseleave");
                                    break;
                                  case z.enter:
                                  case z.space:
                                    ((l = !0), t.currentTarget.click());
                                }
                                return (
                                  l &&
                                    (t.preventDefault(), t.stopPropagation()),
                                  !1
                                );
                              });
                            },
                          );
                        }
                      })(this, t)),
                      this.addListeners());
                  }
                  addListeners() {
                    this.domNode.addEventListener("keydown", (e) => {
                      let t = !1;
                      switch (e.code) {
                        case z.down:
                          (Ze(e.currentTarget, "mouseenter"),
                            this.submenu && this.submenu.gotoSubIndex(0),
                            (t = !0));
                          break;
                        case z.up:
                          (Ze(e.currentTarget, "mouseenter"),
                            this.submenu &&
                              this.submenu.gotoSubIndex(
                                this.submenu.subMenuItems.length - 1,
                              ),
                            (t = !0));
                          break;
                        case z.tab:
                          Ze(e.currentTarget, "mouseleave");
                          break;
                        case z.enter:
                        case z.space:
                          ((t = !0), e.currentTarget.click());
                      }
                      t && e.preventDefault();
                    });
                  }
                })(t, e);
            });
          }
        })(r.vnode.el, d.namespace.value);
    });
    n({
      open: (e) => {
        const { indexPath: t } = g.value[e];
        t.forEach((e) => y(e, t));
      },
      close: w,
      handleResize: I,
    });
    return () => {
      var t, l;
      let a =
        null != (l = null == (t = o.default) ? void 0 : t.call(o)) ? l : [];
      const n = [];
      if ("horizontal" === e.mode && c.value) {
        const t = Je(a),
          l = -1 === v.value ? t : t.slice(0, v.value),
          o = -1 === v.value ? [] : t.slice(v.value);
        (null == o ? void 0 : o.length) &&
          e.ellipsis &&
          ((a = l),
          n.push(
            G(
              At,
              { index: "sub-menu-more", class: p.e("hide-arrow") },
              {
                title: () =>
                  G(b, { class: p.e("icon-more") }, { default: () => G(le) }),
                default: () => o,
              },
            ),
          ));
      }
      const r = Lt(e, 0),
        s = G(
          "ul",
          {
            key: String(e.collapse),
            role: "menubar",
            ref: c,
            style: r.value,
            class: {
              [d.b()]: !0,
              [d.m(e.mode)]: !0,
              [d.m("collapse")]: e.collapse,
            },
          },
          [...a, ...n],
        );
      return e.collapseTransition && "vertical" === e.mode ? G(St, () => s) : s;
    };
  },
});
const Ht = M({
    index: { type: $([String, null]), default: null },
    route: { type: $([String, Object]) },
    disabled: Boolean,
  }),
  Nt = "ElMenuItem";
var Ut = C(
  r({
    name: Nt,
    components: { ElTooltip: qe },
    props: Ht,
    emits: { click: (e) => Z(e.index) && Array.isArray(e.indexPath) },
    setup(e, { emit: t }) {
      const l = V(),
        n = S("rootMenu"),
        r = s("menu"),
        i = s("menu-item");
      n || o(Nt, "can not inject root menu");
      const { parentMenu: c, indexPath: d } = jt(l, ne(e, "index")),
        p = S(`subMenu:${c.value.uid}`);
      p || o(Nt, "can not inject sub menu");
      const v = u(() => e.index === n.activeIndex),
        m = q({ index: e.index, indexPath: d, active: v });
      return (
        a(() => {
          (p.addSubMenu(m), n.addMenuItem(m));
        }),
        W(() => {
          (p.removeSubMenu(m), n.removeMenuItem(m));
        }),
        {
          parentMenu: c,
          rootMenu: n,
          active: v,
          nsMenu: r,
          nsMenuItem: i,
          handleClick: () => {
            e.disabled ||
              (n.handleMenuItemClick({
                index: e.index,
                indexPath: d.value,
                route: e.route,
              }),
              t("click", m));
          },
        }
      );
    },
  }),
  [
    [
      "render",
      function (e, t, l, a, o, n) {
        const r = re("el-tooltip");
        return (
          i(),
          v(
            "li",
            {
              class: h([
                e.nsMenuItem.b(),
                e.nsMenuItem.is("active", e.active),
                e.nsMenuItem.is("disabled", e.disabled),
              ]),
              role: "menuitem",
              tabindex: "-1",
              onClick:
                t[0] || (t[0] = (...t) => e.handleClick && e.handleClick(...t)),
            },
            [
              "ElMenu" === e.parentMenu.type.name &&
              e.rootMenu.props.collapse &&
              e.$slots.title
                ? (i(),
                  c(
                    r,
                    {
                      key: 0,
                      effect: e.rootMenu.props.popperEffect,
                      placement: "right",
                      "fallback-placements": ["left"],
                      persistent: "",
                    },
                    {
                      content: d(() => [g(e.$slots, "title")]),
                      default: d(() => [
                        j(
                          "div",
                          { class: h(e.nsMenu.be("tooltip", "trigger")) },
                          [g(e.$slots, "default")],
                          2,
                        ),
                      ]),
                      _: 3,
                    },
                    8,
                    ["effect"],
                  ))
                : (i(),
                  v(
                    Y,
                    { key: 1 },
                    [g(e.$slots, "default"), g(e.$slots, "title")],
                    64,
                  )),
            ],
            2,
          )
        );
      },
    ],
    [
      "__file",
      "/home/runner/work/element-plus/element-plus/packages/components/menu/src/menu-item.vue",
    ],
  ],
);
var Ft = C(
  r({
    name: "ElMenuItemGroup",
    props: { title: String },
    setup: () => ({ ns: s("menu-item-group") }),
  }),
  [
    [
      "render",
      function (e, t, l, a, o, n) {
        return (
          i(),
          v(
            "li",
            { class: h(e.ns.b()) },
            [
              j(
                "div",
                { class: h(e.ns.e("title")) },
                [
                  e.$slots.title
                    ? g(e.$slots, "title", { key: 1 })
                    : (i(), v(Y, { key: 0 }, [se(L(e.title), 1)], 64)),
                ],
                2,
              ),
              j("ul", null, [g(e.$slots, "default")]),
            ],
            2,
          )
        );
      },
    ],
    [
      "__file",
      "/home/runner/work/element-plus/element-plus/packages/components/menu/src/menu-item-group.vue",
    ],
  ],
);
const qt = k(Rt, { MenuItem: Ut, MenuItemGroup: Ft, SubMenu: At }),
  Dt = B(Ut);
B(Ft);
const Wt = B(At),
  Gt = r({
    __name: "Backtop",
    setup(e) {
      const { getPrefixCls: t, variables: l } = ue(),
        a = t("backtop");
      return (e, t) => (
        i(),
        c(
          p(yt),
          {
            class: h(`${p(a)}-backtop`),
            target: `.${p(l).namespace}-layout-content-scrollbar .${p(l).elNamespace}-scrollbar__wrap`,
          },
          null,
          8,
          ["class", "target"],
        )
      );
    },
  }),
  Zt = (e, t) => (De(e, (e) => e.path === t) || []).map((e) => e.path),
  { renderMenuTitle: Kt } = {
    renderMenuTitle: (e) => {
      const { t: t } = ie(),
        { title: l = "Please set title", icon: a } = e;
      return a
        ? x(Y, null, [
            x(ce, { icon: e.icon }, null),
            x("span", { class: "v-menu__title" }, [t(l)]),
          ])
        : x("span", { class: "v-menu__title" }, [t(l)]);
    },
  },
  Qt = (e) => {
    const l = (a, o = "/") =>
      a.map((a) => {
        const n = a.meta ?? {};
        if (!n.hidden) {
          const { oneShowingChild: r, onlyOneChild: s } = ((e = [], l) => {
              const a = t(),
                o = e.filter(
                  (e) => !(e.meta ?? {}).hidden && ((a.value = e), !0),
                );
              return 1 === o.length
                ? { oneShowingChild: !0, onlyOneChild: p(a) }
                : o.length
                  ? { oneShowingChild: !1, onlyOneChild: p(a) }
                  : ((a.value = { ...l, path: "", noShowingChildren: !0 }),
                    { oneShowingChild: !0, onlyOneChild: p(a) });
            })(a.children, a),
            u = de(a.path) ? a.path : pe(o, a.path);
          if (
            !r ||
            ((null == s ? void 0 : s.children) &&
              !(null == s ? void 0 : s.noShowingChildren)) ||
            (null == n ? void 0 : n.alwaysShow)
          ) {
            const { getPrefixCls: t } = ue(),
              o = t("menu-popper");
            return x(
              Wt,
              {
                index: u,
                popperClass:
                  "vertical" === e ? `${o}--vertical` : `${o}--horizontal`,
              },
              { title: () => Kt(n), default: () => l(a.children, u) },
            );
          }
          return x(
            Dt,
            { index: s ? pe(u, s.path) : u },
            { default: () => Kt(s ? (null == s ? void 0 : s.meta) : n) },
          );
        }
      });
    return { renderMenuItem: l };
  };
const { getPrefixCls: Yt } = ue(),
  Jt = Yt("menu"),
  Xt = xe(
    r({
      name: "Menu",
      props: { menuSelect: { type: Function, default: void 0 } },
      setup(e) {
        const t = ve(),
          l = u(() => t.getLayout),
          { push: a, currentRoute: o } = me(),
          n = he(),
          r = u(() =>
            ["classic", "topLeft", "cutMenu"].includes(p(l))
              ? "vertical"
              : "horizontal",
          ),
          s = u(() =>
            "cutMenu" === p(l) ? n.getMenuTabRouters : n.getRouters,
          ),
          i = u(() => t.getCollapse),
          c = u(() => t.getUniqueOpened),
          d = u(() => {
            const { meta: e, path: t } = p(o);
            return e.activeMenu ? e.activeMenu : t;
          }),
          v = (t) => {
            (e.menuSelect && e.menuSelect(t), de(t) ? window.open(t) : a(t));
          },
          m = () => {
            if ("top" === p(l)) return h();
            {
              let t;
              return x(
                fe,
                null,
                "function" == typeof (e = t = h()) ||
                  ("[object Object]" === Object.prototype.toString.call(e) &&
                    !ge(e))
                  ? t
                  : { default: () => [t] },
              );
            }
            var e;
          },
          h = () =>
            x(
              qt,
              {
                defaultActive: p(d),
                mode: p(r),
                collapse: "top" !== p(l) && "cutMenu" !== p(l) && p(i),
                uniqueOpened: "top" !== p(l) && p(c),
                backgroundColor: "var(--left-menu-bg-color)",
                textColor: "var(--left-menu-text-color)",
                activeTextColor: "var(--left-menu-text-active-color)",
                onSelect: v,
              },
              {
                default: () => {
                  const { renderMenuItem: e } = Qt(p(r));
                  return e(p(s));
                },
              },
            );
        return () =>
          x(
            "div",
            {
              id: Jt,
              class: [
                `${Jt} ${Jt}__${p(r)}`,
                "h-[100%] overflow-hidden flex-col bg-[var(--left-menu-bg-color)]",
                {
                  "w-[var(--left-menu-min-width)]": p(i) && "cutMenu" !== p(l),
                  "w-[var(--left-menu-max-width)]": !p(i) && "cutMenu" !== p(l),
                },
              ],
            },
            [m()],
          );
      },
    }),
    [["__scopeId", "data-v-f958223e"]],
  ),
  el = q({}),
  tl = (e, t) => {
    const l = [];
    for (const a of e) {
      let e = null;
      const o = a.meta ?? {};
      if (!o.hidden || o.canTo) {
        const o = Zt(t, a.path),
          n = de(a.path) ? a.path : o.join("/");
        ((e = be(a)),
          (e.path = n),
          a.children && e && (e.children = tl(a.children, t)),
          e && l.push(e),
          o.length && Reflect.has(el, o[0]) && el[o[0]].push(n));
      }
    }
    return l;
  },
  { getPrefixCls: ll, variables: al } = ue(),
  ol = ll("tab-menu"),
  nl = xe(
    r({
      name: "TabMenu",
      directives: { ClickOutside: et },
      setup() {
        const { push: e, currentRoute: l } = me(),
          { t: o } = ie(),
          n = ve(),
          r = u(() => n.getCollapse),
          s = u(() => n.getFixedMenu),
          i = he(),
          c = u(() => i.getRouters),
          d = u(() =>
            p(c).filter((e) => {
              var t;
              return !(null == (t = null == e ? void 0 : e.meta)
                ? void 0
                : t.hidden);
            }),
          ),
          v = () => {
            n.setCollapse(!p(r));
          };
        (a(() => {
          var e;
          if (p(s)) {
            const t = `/${p(l).path.split("/")[1]}`,
              a =
                null ==
                (e = p(d).find((e) => {
                  var l, a, o;
                  return (
                    ((null == (l = e.meta) ? void 0 : l.alwaysShow) ||
                      ((null == (a = null == e ? void 0 : e.children)
                        ? void 0
                        : a.length) &&
                        (null == (o = null == e ? void 0 : e.children)
                          ? void 0
                          : o.length) > 1)) &&
                    e.path === t
                  );
                }))
                  ? void 0
                  : e.children;
            ((f.value = t),
              a &&
                i.setMenuTabRouters(
                  be(a).map((e) => ((e.path = pe(p(f), e.path)), e)),
                ));
          }
        }),
          D(
            () => c.value,
            (e) => {
              (((e) => {
                for (const t of e) {
                  const e = t.meta ?? {};
                  (null == e ? void 0 : e.hidden) || (el[t.path] = []);
                }
              })(e),
                tl(e, e));
            },
            { immediate: !0, deep: !0 },
          ));
        const m = t(!0);
        D(
          () => r.value,
          (e) => {
            e
              ? (m.value = !e)
              : setTimeout(() => {
                  m.value = !e;
                }, 200);
          },
        );
        const h = t(!!p(s)),
          f = t(""),
          g = (e) => {
            const { path: t } = p(l);
            return !!el[e].includes(t);
          },
          b = () => {
            p(s) || (h.value = !1);
          };
        return () =>
          K(
            x(
              "div",
              {
                id: `${al.namespace}-menu`,
                class: [
                  ol,
                  "relative bg-[var(--left-menu-bg-color)] top-1px layout-border__right",
                  {
                    "w-[var(--tab-menu-max-width)]": !p(r),
                    "w-[var(--tab-menu-min-width)]": p(r),
                  },
                ],
              },
              [
                x(
                  fe,
                  {
                    class:
                      "!h-[calc(100%-var(--tab-menu-collapse-height)-1px)]",
                  },
                  {
                    default: () => [
                      x("div", null, {
                        default: () =>
                          p(d).map((t) => {
                            var l, a, n, r, s, u;
                            const c =
                              (null == (l = t.meta) ? void 0 : l.alwaysShow) ||
                              ((null == (a = null == t ? void 0 : t.children)
                                ? void 0
                                : a.length) &&
                                (null == (n = null == t ? void 0 : t.children)
                                  ? void 0
                                  : n.length) > 1)
                                ? t
                                : {
                                    ...((null == t ? void 0 : t.children) &&
                                      (null == t ? void 0 : t.children[0])),
                                    path: pe(
                                      t.path,
                                      null ==
                                        (r =
                                          (null == t ? void 0 : t.children) &&
                                          (null == t ? void 0 : t.children[0]))
                                        ? void 0
                                        : r.path,
                                    ),
                                  };
                            return x(
                              "div",
                              {
                                class: [
                                  `${ol}__item`,
                                  "text-center text-12px relative py-12px cursor-pointer",
                                  { "is-active": g(t.path) },
                                ],
                                onClick: () => {
                                  ((t) => {
                                    if (de(t.path))
                                      return void window.open(t.path);
                                    const l = t.children
                                        ? t.path
                                        : t.path.split("/")[0],
                                      a = p(f);
                                    ((f.value = t.children
                                      ? t.path
                                      : t.path.split("/")[0]),
                                      t.children
                                        ? ((l !== a && p(h)) ||
                                            (h.value = !p(h)),
                                          p(h) &&
                                            i.setMenuTabRouters(
                                              be(t.children).map(
                                                (e) => (
                                                  (e.path = pe(p(f), e.path)),
                                                  e
                                                ),
                                              ),
                                            ))
                                        : (e(t.path),
                                          i.setMenuTabRouters([]),
                                          (h.value = !1)));
                                  })(c);
                                },
                              },
                              [
                                x("div", null, [
                                  x(
                                    ce,
                                    {
                                      icon:
                                        null ==
                                        (s = null == c ? void 0 : c.meta)
                                          ? void 0
                                          : s.icon,
                                    },
                                    null,
                                  ),
                                ]),
                                p(m)
                                  ? x(
                                      "p",
                                      { class: "break-words mt-5px px-2px" },
                                      [
                                        o(
                                          (null == (u = c.meta)
                                            ? void 0
                                            : u.title) || "",
                                        ),
                                      ],
                                    )
                                  : void 0,
                              ],
                            );
                          }),
                      }),
                    ],
                  },
                ),
                x(
                  "div",
                  {
                    class: [
                      `${ol}--collapse`,
                      "text-center h-[var(--tab-menu-collapse-height)] leading-[var(--tab-menu-collapse-height)] cursor-pointer",
                    ],
                    onClick: v,
                  },
                  [
                    x(
                      ce,
                      { icon: p(r) ? "ep:d-arrow-right" : "ep:d-arrow-left" },
                      null,
                    ),
                  ],
                ),
                x(
                  Xt,
                  {
                    class: [
                      "!absolute top-0 z-1000",
                      {
                        "!left-[var(--tab-menu-min-width)]": p(r),
                        "!left-[var(--tab-menu-max-width)]": !p(r),
                        "!w-[var(--left-menu-max-width)]": p(h) || p(s),
                        "!w-0": !p(h) && !p(s),
                      },
                    ],
                    style:
                      "transition: width var(--transition-time-02), left var(--transition-time-02);",
                  },
                  null,
                ),
              ],
            ),
            [[ye("click-outside"), b]],
          );
      },
    }),
    [["__scopeId", "data-v-f15eb29d"]],
  ),
  rl = (e, t = "") => {
    let l = [];
    return (
      e.forEach((e) => {
        const a = e.meta ?? {},
          o = pe(t, e.path);
        if (
          ((null == a ? void 0 : a.affix) &&
            l.push({ ...e, path: o, fullPath: o }),
          e.children)
        ) {
          const t = rl(e.children, o);
          t.length >= 1 && (l = [...l, ...t]);
        }
      }),
      l
    );
  },
  sl = r({
    __name: "ContextMenu",
    props: {
      schema: { type: Array, default: () => [] },
      trigger: { type: String, default: "contextmenu" },
      tagItem: { type: Object, default: () => ({}) },
    },
    emits: ["visibleChange"],
    setup(e, { expose: l, emit: a }) {
      const o = e,
        { getPrefixCls: n } = ue(),
        r = n("context-menu"),
        { t: s } = ie(),
        u = (e) => {
          e.command && e.command(e);
        },
        m = (e) => {
          a("visibleChange", e, o.tagItem);
        },
        f = t();
      return (
        l({ elDropdownMenuRef: f, tagItem: o.tagItem }),
        (t, l) => {
          const a = re("Icon");
          return (
            i(),
            c(
              p(at),
              {
                ref_key: "elDropdownMenuRef",
                ref: f,
                class: h(p(r)),
                trigger: e.trigger,
                placement: "bottom-start",
                onCommand: u,
                onVisibleChange: m,
                "popper-class": "v-context-menu-popper",
              },
              {
                dropdown: d(() => [
                  x(p(tt), null, {
                    default: d(() => [
                      (i(!0),
                      v(
                        Y,
                        null,
                        we(
                          e.schema,
                          (e, t) => (
                            i(),
                            c(
                              p(lt),
                              {
                                key: `dropdown${t}`,
                                divided: e.divided,
                                disabled: e.disabled,
                                command: e,
                              },
                              {
                                default: d(() => [
                                  x(a, { icon: e.icon }, null, 8, ["icon"]),
                                  se(" " + L(p(s)(e.label)), 1),
                                ]),
                                _: 2,
                              },
                              1032,
                              ["divided", "disabled", "command"],
                            )
                          ),
                        ),
                        128,
                      )),
                    ]),
                    _: 1,
                  }),
                ]),
                default: d(() => [g(t.$slots, "default")]),
                _: 3,
              },
              8,
              ["class", "trigger"],
            )
          );
        }
      );
    },
  });
function ul({
  el: e,
  position: l = "scrollLeft",
  to: a,
  duration: o = 500,
  callback: n,
}) {
  const r = t(!1),
    s = e[l],
    u = a - s,
    i = 20;
  let c = 0;
  function d() {
    if (!p(r)) return;
    c += i;
    const t =
      ((a = c),
      (v = s),
      (m = u),
      (a /= o / 2) < 1
        ? (m / 2) * a * a + v
        : (-m / 2) * (--a * (a - 2) - 1) + v);
    var a, v, m;
    (((e, t, l) => {
      e[t] = l;
    })(e, l, t),
      c < o && p(r) ? requestAnimationFrame(d) : n && n());
  }
  return {
    start: function () {
      ((r.value = !0), d());
    },
    stop: function () {
      r.value = !1;
    },
  };
}
const il = ["id"],
  cl = { class: "overflow-hidden flex-1" },
  dl = { class: "flex h-full" },
  pl = ["onClick"],
  vl = xe(
    r({
      __name: "TagsView",
      setup(e) {
        const { getPrefixCls: l } = ue(),
          o = l("tags-view"),
          { t: n } = ie(),
          { currentRoute: r, push: s } = me(),
          {
            closeAll: m,
            closeLeft: g,
            closeRight: b,
            closeOther: y,
            closeCurrent: _,
            refreshPage: C,
          } = (() => {
            const e = _e(),
              { replace: t, currentRoute: l } = me(),
              a = u(() => e.getSelectedTag);
            return {
              closeAll: (t) => {
                (e.delAllViews(), null == t || t());
              },
              closeLeft: (t) => {
                (e.delLeftViews(p(a)), null == t || t());
              },
              closeRight: (t) => {
                (e.delRightViews(p(a)), null == t || t());
              },
              closeOther: (t) => {
                (e.delOthersViews(p(a)), null == t || t());
              },
              closeCurrent: (t, a) => {
                var o;
                (null == (o = null == t ? void 0 : t.meta)
                  ? void 0
                  : o.affix) || (e.delView(t || p(l)), null == a || a());
              },
              refreshPage: async (a, o) => {
                e.delCachedView();
                const { path: n, query: r } = a || p(l);
                (await oe(),
                  t({ path: "/redirect" + n, query: r }),
                  null == o || o());
              },
              setTitle: (t, l) => {
                e.setTitle(t, l);
              },
            };
          })(),
          k = he(),
          M = u(() => k.getRouters),
          I = Ce(),
          T = u(() => I.getVisitedViews),
          $ = t([]),
          V = u(() => I.getSelectedTag),
          S = I.setSelectedTag,
          P = ve(),
          B = u(() => P.getTagsViewIcon),
          z = u(() => P.getIsDark),
          A = () => {
            const { name: e } = p(r);
            e && (S(p(r)), I.addView(p(r)));
          },
          E = (e) => {
            _(e, () => {
              G(e) && O();
            });
          },
          O = () => {
            const e = I.getVisitedViews.slice(-1)[0];
            if (e) s(e);
            else {
              if (
                p(r).path === k.getAddRouters[0].path ||
                p(r).path === k.getAddRouters[0].redirect
              )
                return void A();
              s(k.getAddRouters[0].path);
            }
          },
          R = () => {
            m(() => {
              O();
            });
          },
          H = () => {
            y();
          },
          N = async (e) => {
            C(e);
          },
          U = () => {
            g();
          },
          F = () => {
            b();
          },
          q = ke(),
          W = (e) => {
            var t;
            const l = null == (t = p(Q)) ? void 0 : t.wrapRef;
            let a = null,
              n = null;
            const r = p(q);
            if (
              (r.length > 0 && ((a = r[0]), (n = r[r.length - 1])),
              (null == a ? void 0 : a.to).fullPath === e.fullPath)
            ) {
              const { start: e } = ul({
                el: l,
                position: "scrollLeft",
                to: 0,
                duration: 500,
              });
              e();
            } else if ((null == n ? void 0 : n.to).fullPath === e.fullPath) {
              const { start: e } = ul({
                el: l,
                position: "scrollLeft",
                to: l.scrollWidth - l.offsetWidth,
                duration: 500,
              });
              e();
            } else {
              const t = r.findIndex(
                  (t) => (null == t ? void 0 : t.to).fullPath === e.fullPath,
                ),
                a = document.getElementsByClassName(`${o}__item`),
                n = a[t - 1],
                s = a[t + 1],
                u = s.offsetLeft + s.offsetWidth + 4,
                i = n.offsetLeft - 4;
              if (u > p(J) + l.offsetWidth) {
                const { start: e } = ul({
                  el: l,
                  position: "scrollLeft",
                  to: u - l.offsetWidth,
                  duration: 500,
                });
                e();
              } else if (i < p(J)) {
                const { start: e } = ul({
                  el: l,
                  position: "scrollLeft",
                  to: i,
                  duration: 500,
                });
                e();
              }
            }
          },
          G = (e) => e.path === p(r).path,
          Z = ke(),
          K = (e, t) => {
            if (e)
              for (const l of p(Z)) {
                const e = l.elDropdownMenuRef;
                t.fullPath !== l.tagItem.fullPath &&
                  (null == e || e.handleClose());
              }
          },
          Q = t(),
          J = t(0),
          X = ({ scrollLeft: e }) => {
            J.value = e;
          },
          ee = (e) => {
            var t;
            const l = null == (t = p(Q)) ? void 0 : t.wrapRef,
              { start: a } = ul({
                el: l,
                position: "scrollLeft",
                to: p(J) + e,
                duration: 500,
              });
            a();
          };
        return (
          a(() => {
            ((() => {
              $.value = rl(p(M));
              for (const e of p($)) e.name && I.addVisitedView(be(e));
            })(),
              A());
          }),
          D(
            () => r.value,
            () => {
              (A(),
                (async () => {
                  await oe();
                  for (const e of p(T))
                    if (e.fullPath === p(r).path) {
                      (W(e),
                        e.fullPath !== p(r).fullPath &&
                          I.updateVisitedView(p(r)));
                      break;
                    }
                })());
            },
          ),
          (e, t) => {
            var l, a, r, s, u, m;
            const g = re("Icon"),
              b = re("router-link");
            return (
              i(),
              v(
                "div",
                {
                  id: p(o),
                  class: h([
                    p(o),
                    "flex w-full relative bg-[#fff] dark:bg-[var(--el-bg-color)]",
                  ]),
                },
                [
                  j(
                    "span",
                    {
                      class: h([
                        `${p(o)}__tool ${p(o)}__tool--first`,
                        "w-[var(--tags-view-height)] h-[var(--tags-view-height)] flex items-center justify-center cursor-pointer",
                      ]),
                      onClick: t[0] || (t[0] = (e) => ee(-200)),
                    },
                    [
                      x(
                        g,
                        {
                          icon: "ep:d-arrow-left",
                          color: "var(--el-text-color-placeholder)",
                          "hover-color": z.value
                            ? "#fff"
                            : "var(--el-color-black)",
                        },
                        null,
                        8,
                        ["hover-color"],
                      ),
                    ],
                    2,
                  ),
                  j("div", cl, [
                    x(
                      p(fe),
                      {
                        ref_key: "scrollbarRef",
                        ref: Q,
                        class: "h-full",
                        onScroll: X,
                      },
                      {
                        default: d(() => [
                          j("div", dl, [
                            (i(!0),
                            v(
                              Y,
                              null,
                              we(T.value, (e) => {
                                var t, l, a, r, s, u, v, m, y;
                                return (
                                  i(),
                                  c(
                                    p(sl),
                                    {
                                      ref_for: !0,
                                      ref: p(Z).set,
                                      schema: [
                                        {
                                          icon: "ant-design:sync-outlined",
                                          label: p(n)("common.reload"),
                                          disabled:
                                            (null == (t = V.value)
                                              ? void 0
                                              : t.fullPath) !== e.fullPath,
                                          command: () => {
                                            N(e);
                                          },
                                        },
                                        {
                                          icon: "ant-design:close-outlined",
                                          label: p(n)("common.closeTab"),
                                          disabled:
                                            !!(null == (l = T.value)
                                              ? void 0
                                              : l.length) &&
                                            (null == (a = V.value)
                                              ? void 0
                                              : a.meta.affix),
                                          command: () => {
                                            E(e);
                                          },
                                        },
                                        {
                                          divided: !0,
                                          icon: "ant-design:vertical-right-outlined",
                                          label: p(n)("common.closeTheLeftTab"),
                                          disabled:
                                            !!(null == (r = T.value)
                                              ? void 0
                                              : r.length) &&
                                            (e.fullPath ===
                                              T.value[0].fullPath ||
                                              (null == (s = V.value)
                                                ? void 0
                                                : s.fullPath) !== e.fullPath),
                                          command: () => {
                                            U();
                                          },
                                        },
                                        {
                                          icon: "ant-design:vertical-left-outlined",
                                          label: p(n)(
                                            "common.closeTheRightTab",
                                          ),
                                          disabled:
                                            !!(null == (u = T.value)
                                              ? void 0
                                              : u.length) &&
                                            (e.fullPath ===
                                              T.value[T.value.length - 1]
                                                .fullPath ||
                                              (null == (v = V.value)
                                                ? void 0
                                                : v.fullPath) !== e.fullPath),
                                          command: () => {
                                            F();
                                          },
                                        },
                                        {
                                          divided: !0,
                                          icon: "ant-design:tag-outlined",
                                          label: p(n)("common.closeOther"),
                                          disabled:
                                            (null == (m = V.value)
                                              ? void 0
                                              : m.fullPath) !== e.fullPath,
                                          command: () => {
                                            H();
                                          },
                                        },
                                        {
                                          icon: "ant-design:line-outlined",
                                          label: p(n)("common.closeAll"),
                                          command: () => {
                                            R();
                                          },
                                        },
                                      ],
                                      key: e.fullPath,
                                      "tag-item": e,
                                      class: h([
                                        `${p(o)}__item`,
                                        (
                                          null ==
                                          (y = null == e ? void 0 : e.meta)
                                            ? void 0
                                            : y.affix
                                        )
                                          ? `${p(o)}__item--affix`
                                          : "",
                                        { "is-active": G(e) },
                                      ]),
                                      onVisibleChange: K,
                                    },
                                    {
                                      default: d(() => [
                                        j("div", null, [
                                          x(
                                            b,
                                            {
                                              ref_for: !0,
                                              ref: p(q).set,
                                              to: { ...e },
                                              custom: "",
                                            },
                                            {
                                              default: d(({ navigate: t }) => {
                                                var l, a, r, s, u;
                                                return [
                                                  j(
                                                    "div",
                                                    {
                                                      onClick: t,
                                                      class:
                                                        "h-full flex justify-center items-center whitespace-nowrap pl-15px",
                                                    },
                                                    [
                                                      (null == e
                                                        ? void 0
                                                        : e.matched) &&
                                                      (null == e
                                                        ? void 0
                                                        : e.matched[1]) &&
                                                      (null ==
                                                      (a =
                                                        null ==
                                                        (l =
                                                          null == e
                                                            ? void 0
                                                            : e.matched[1])
                                                          ? void 0
                                                          : l.meta)
                                                        ? void 0
                                                        : a.icon) &&
                                                      B.value
                                                        ? (i(),
                                                          c(
                                                            g,
                                                            {
                                                              key: 0,
                                                              icon:
                                                                null ==
                                                                (s =
                                                                  null ==
                                                                  (r =
                                                                    null == e
                                                                      ? void 0
                                                                      : e
                                                                          .matched[1])
                                                                    ? void 0
                                                                    : r.meta)
                                                                  ? void 0
                                                                  : s.icon,
                                                              size: 12,
                                                              class: "mr-5px",
                                                            },
                                                            null,
                                                            8,
                                                            ["icon"],
                                                          ))
                                                        : w("", !0),
                                                      se(
                                                        " " +
                                                          L(
                                                            p(n)(
                                                              null ==
                                                                (u =
                                                                  null == e
                                                                    ? void 0
                                                                    : e.meta)
                                                                ? void 0
                                                                : u.title,
                                                            ),
                                                          ) +
                                                          " ",
                                                        1,
                                                      ),
                                                      x(
                                                        g,
                                                        {
                                                          class: h(
                                                            `${p(o)}__item--close`,
                                                          ),
                                                          color: "#333",
                                                          icon: "ant-design:close-outlined",
                                                          size: 12,
                                                          onClick: f(
                                                            (t) => E(e),
                                                            ["prevent", "stop"],
                                                          ),
                                                        },
                                                        null,
                                                        8,
                                                        ["class", "onClick"],
                                                      ),
                                                    ],
                                                    8,
                                                    pl,
                                                  ),
                                                ];
                                              }),
                                              _: 2,
                                            },
                                            1032,
                                            ["to"],
                                          ),
                                        ]),
                                      ]),
                                      _: 2,
                                    },
                                    1032,
                                    ["schema", "tag-item", "class"],
                                  )
                                );
                              }),
                              128,
                            )),
                          ]),
                        ]),
                        _: 1,
                      },
                      512,
                    ),
                  ]),
                  j(
                    "span",
                    {
                      class: h([
                        `${p(o)}__tool`,
                        "w-[var(--tags-view-height)] h-[var(--tags-view-height)] flex items-center justify-center cursor-pointer",
                      ]),
                      onClick: t[1] || (t[1] = (e) => ee(200)),
                    },
                    [
                      x(
                        g,
                        {
                          icon: "ep:d-arrow-right",
                          color: "var(--el-text-color-placeholder)",
                          "hover-color": z.value
                            ? "#fff"
                            : "var(--el-color-black)",
                        },
                        null,
                        8,
                        ["hover-color"],
                      ),
                    ],
                    2,
                  ),
                  j(
                    "span",
                    {
                      class: h([
                        `${p(o)}__tool`,
                        "w-[var(--tags-view-height)] h-[var(--tags-view-height)] flex items-center justify-center cursor-pointer",
                      ]),
                      onClick: t[2] || (t[2] = (e) => N(V.value)),
                    },
                    [
                      x(
                        g,
                        {
                          icon: "ant-design:reload-outlined",
                          color: "var(--el-text-color-placeholder)",
                          "hover-color": z.value
                            ? "#fff"
                            : "var(--el-color-black)",
                        },
                        null,
                        8,
                        ["hover-color"],
                      ),
                    ],
                    2,
                  ),
                  x(
                    p(sl),
                    {
                      trigger: "click",
                      schema: [
                        {
                          icon: "ant-design:sync-outlined",
                          label: p(n)("common.reload"),
                          command: () => {
                            N(V.value);
                          },
                        },
                        {
                          icon: "ant-design:close-outlined",
                          label: p(n)("common.closeTab"),
                          disabled:
                            !!(null == (l = T.value) ? void 0 : l.length) &&
                            (null == (a = V.value) ? void 0 : a.meta.affix),
                          command: () => {
                            E(V.value);
                          },
                        },
                        {
                          divided: !0,
                          icon: "ant-design:vertical-right-outlined",
                          label: p(n)("common.closeTheLeftTab"),
                          disabled:
                            !!(null == (r = T.value) ? void 0 : r.length) &&
                            (null == (s = V.value) ? void 0 : s.fullPath) ===
                              T.value[0].fullPath,
                          command: () => {
                            U();
                          },
                        },
                        {
                          icon: "ant-design:vertical-left-outlined",
                          label: p(n)("common.closeTheRightTab"),
                          disabled:
                            !!(null == (u = T.value) ? void 0 : u.length) &&
                            (null == (m = V.value) ? void 0 : m.fullPath) ===
                              T.value[T.value.length - 1].fullPath,
                          command: () => {
                            F();
                          },
                        },
                        {
                          divided: !0,
                          icon: "ant-design:tag-outlined",
                          label: p(n)("common.closeOther"),
                          command: () => {
                            H();
                          },
                        },
                        {
                          icon: "ant-design:line-outlined",
                          label: p(n)("common.closeAll"),
                          command: () => {
                            R();
                          },
                        },
                      ],
                    },
                    {
                      default: d(() => [
                        j(
                          "span",
                          {
                            class: h([
                              `${p(o)}__tool`,
                              "w-[var(--tags-view-height)] h-[var(--tags-view-height)] flex items-center justify-center cursor-pointer block",
                            ]),
                          },
                          [
                            x(
                              g,
                              {
                                icon: "ant-design:setting-outlined",
                                color: "var(--el-text-color-placeholder)",
                                "hover-color": z.value
                                  ? "#fff"
                                  : "var(--el-color-black)",
                              },
                              null,
                              8,
                              ["hover-color"],
                            ),
                          ],
                          2,
                        ),
                      ]),
                      _: 1,
                    },
                    8,
                    ["schema"],
                  ),
                ],
                10,
                il,
              )
            );
          }
        );
      },
    }),
    [["__scopeId", "data-v-7bf23422"]],
  ),
  ml = ["src"],
  hl = r({
    __name: "Logo",
    setup(e) {
      const { getPrefixCls: l } = ue(),
        o = l("logo"),
        n = ve(),
        r = t(!0),
        s = u(() => n.getTitle),
        c = u(() => n.getLayout),
        m = u(() => n.getCollapse),
        f = u(() => n.getLogoImage);
      return (
        a(() => {
          p(m) && (r.value = !1);
        }),
        D(
          () => m.value,
          (e) => {
            "topLeft" !== p(c) && "cutMenu" !== p(c)
              ? e
                ? (r.value = !e)
                : setTimeout(() => {
                    r.value = !e;
                  }, 400)
              : (r.value = !0);
          },
        ),
        D(
          () => c.value,
          (e) => {
            "top" === e || "cutMenu" === e
              ? (r.value = !0)
              : p(m)
                ? (r.value = !1)
                : (r.value = !0);
          },
        ),
        (e, t) => {
          const l = re("router-link");
          return (
            i(),
            v("div", null, [
              x(
                l,
                {
                  class: h([
                    p(o),
                    "classic" !== c.value ? `${p(o)}__Top` : "",
                    "flex !h-[var(--logo-height)] items-center cursor-pointer pl-8px relative decoration-none overflow-hidden",
                  ]),
                  to: "/",
                },
                {
                  default: d(() => [
                    j(
                      "img",
                      {
                        src: f.value,
                        class:
                          "w-[calc(var(--logo-height)-10px)] h-[calc(var(--logo-height)-10px)]",
                      },
                      null,
                      8,
                      ml,
                    ),
                    r.value
                      ? (i(),
                        v(
                          "div",
                          {
                            key: 0,
                            class: h([
                              "ml-10px text-16px font-700",
                              {
                                "text-[var(--logo-title-text-color)]":
                                  "classic" === c.value,
                                "text-[var(--top-header-text-color)]":
                                  "topLeft" === c.value ||
                                  "top" === c.value ||
                                  "cutMenu" === c.value,
                              },
                            ]),
                          },
                          L(s.value),
                          3,
                        ))
                      : w("", !0),
                  ]),
                  _: 1,
                },
                8,
                ["class"],
              ),
            ])
          );
        }
      );
    },
  }),
  fl = r({
    __name: "AppView",
    setup(e) {
      const t = ve(),
        l = u(() => t.getLayout),
        a = u(() => t.getFixedHeader),
        o = u(() => t.getFooter),
        n = Ce(),
        r = u(() => n.getCachedViews),
        s = u(() => t.getTagsView);
      return (e, t) => {
        const n = re("router-view");
        return (
          i(),
          v(
            Y,
            null,
            [
              j(
                "section",
                {
                  class: h([
                    "p-[var(--app-content-padding)] w-[calc(100%-var(--app-content-padding)-var(--app-content-padding))] bg-[var(--app-content-bg-color-new)] dark:bg-[var(--el-bg-color)]",
                    {
                      "!min-h-[calc(100%-var(--app-footer-height))]":
                        (a.value &&
                          ("classic" === l.value ||
                            "topLeft" === l.value ||
                            "top" === l.value) &&
                          o.value) ||
                        (!s.value && "top" === l.value && o.value),
                      "!min-h-[calc(100%-var(--app-content-padding)-var(--app-content-padding)-var(--app-footer-height)-var(--tags-view-height))]":
                        s.value && "top" === l.value && o.value,
                      "!min-h-[calc(100%-var(--tags-view-height)-var(--app-content-padding)-var(--app-content-padding)-var(--top-tool-height)-var(--app-footer-height))]":
                        !a.value && "classic" === l.value && o.value,
                      "!min-h-[calc(100%-var(--tags-view-height)-var(--app-content-padding)-var(--app-content-padding)-var(--app-footer-height))]":
                        !a.value && "topLeft" === l.value && o.value,
                      "!min-h-[calc(100%-var(--top-tool-height)-var(--app-content-padding)-var(--app-content-padding))]":
                        a.value && "cutMenu" === l.value && o.value,
                      "!min-h-[calc(100%-var(--top-tool-height)-var(--app-content-padding)-var(--app-content-padding)-var(--tags-view-height))]":
                        !a.value && "cutMenu" === l.value && o.value,
                    },
                  ]),
                },
                [
                  x(n, null, {
                    default: d(({ Component: e, route: t }) => [
                      (i(),
                      c(
                        Me,
                        { include: r.value },
                        [(i(), c(P(e), { key: t.fullPath }))],
                        1032,
                        ["include"],
                      )),
                    ]),
                    _: 1,
                  }),
                ],
                2,
              ),
              o.value ? (i(), c(p(ot), { key: 0 })) : w("", !0),
            ],
            64,
          )
        );
      };
    },
  }),
  gl = r({
    __name: "Collapse",
    props: { color: Ie.string.def("") },
    setup(e) {
      const { getPrefixCls: t } = ue(),
        l = t("collapse"),
        a = ve(),
        o = u(() => a.getCollapse),
        n = () => {
          const e = p(o);
          a.setCollapse(!e);
        };
      return (t, a) => {
        const r = re("Icon");
        return (
          i(),
          v(
            "div",
            { class: h(p(l)), onClick: n },
            [
              x(
                r,
                {
                  size: 18,
                  icon: o.value
                    ? "ant-design:menu-unfold-outlined"
                    : "ant-design:menu-fold-outlined",
                  color: e.color,
                  class: "cursor-pointer",
                },
                null,
                8,
                ["icon", "color"],
              ),
            ],
            2,
          )
        );
      };
    },
  }),
  xl = r({
    __name: "SizeDropdown",
    props: { color: Ie.string.def("") },
    setup(e) {
      const { getPrefixCls: t } = ue(),
        l = t("size-dropdown"),
        { t: a } = ie(),
        o = ve(),
        n = u(() => o.sizeMap),
        r = (e) => {
          o.setCurrentSize(e);
        };
      return (t, o) => {
        const s = re("Icon");
        return (
          i(),
          c(
            p(at),
            { class: h(p(l)), trigger: "click", onCommand: r },
            {
              dropdown: d(() => [
                x(p(tt), null, {
                  default: d(() => [
                    (i(!0),
                    v(
                      Y,
                      null,
                      we(
                        n.value,
                        (e) => (
                          i(),
                          c(
                            p(lt),
                            { key: e, command: e },
                            {
                              default: d(() => [se(L(p(a)(`size.${e}`)), 1)]),
                              _: 2,
                            },
                            1032,
                            ["command"],
                          )
                        ),
                      ),
                      128,
                    )),
                  ]),
                  _: 1,
                }),
              ]),
              default: d(() => [
                x(
                  s,
                  {
                    size: 18,
                    icon: "mdi:format-size",
                    color: e.color,
                    class: "cursor-pointer",
                  },
                  null,
                  8,
                  ["color"],
                ),
              ]),
              _: 1,
            },
            8,
            ["class"],
          )
        );
      };
    },
  }),
  bl = Te("lock", {
    state: () => ({ lockInfo: {} }),
    getters: {
      getLockInfo() {
        return this.lockInfo;
      },
    },
    actions: {
      setLockInfo(e) {
        this.lockInfo = e;
      },
      resetLockInfo() {
        this.lockInfo = {};
      },
      unLock(e) {
        var t;
        return (
          (null == (t = this.lockInfo) ? void 0 : t.password) === e &&
          (this.resetLockInfo(), !0)
        );
      },
    },
    persist: {
      enabled: !0,
      strategies: [{ key: "lock", storage: localStorage }],
    },
  }),
  yl = ((e) => (Ve("data-v-44fc72b4"), (e = e()), Se(), e))(() =>
    j(
      "div",
      { class: "flex flex-col items-center" },
      [
        j("img", { src: it, alt: "", class: "w-70px h-70px rounded-[50%]" }),
        j(
          "span",
          { class: "text-14px my-10px text-[var(--top-header-text-color)]" },
          "Archer",
        ),
      ],
      -1,
    ),
  ),
  wl = xe(
    r({
      __name: "LockDialog",
      props: { modelValue: { type: Boolean } },
      emits: ["update:modelValue"],
      setup(e, { emit: l }) {
        const a = e,
          { getPrefixCls: o } = ue(),
          n = o("lock-dialog"),
          { required: r } = dt(),
          { t: s } = ie(),
          v = bl(),
          m = u({
            get: () => a.modelValue,
            set: (e) => {
              l("update:modelValue", e);
            },
          }),
          f = t(s("lock.lockScreen")),
          g = q({ password: [r()] }),
          b = q([
            {
              label: s("lock.lockPassword"),
              field: "password",
              component: "Input",
              componentProps: { type: "password", showPassword: !0 },
            },
          ]),
          { formRegister: y, formMethods: w } = Ke(),
          { getFormData: _, getElFormExpose: C } = w,
          k = async () => {
            const e = await C();
            null == e ||
              e.validate(async (e) => {
                if (e) {
                  m.value = !1;
                  const e = await _();
                  v.setLockInfo({ isLock: !0, ...e });
                }
              });
          };
        return (e, t) => (
          i(),
          c(
            p(ct),
            {
              modelValue: m.value,
              "onUpdate:modelValue": t[0] || (t[0] = (e) => (m.value = e)),
              width: "500px",
              "max-height": "170px",
              class: h(p(n)),
              title: f.value,
            },
            {
              footer: d(() => [
                x(
                  p($e),
                  { type: "primary", onClick: k },
                  { default: d(() => [se(L(p(s)("lock.lock")), 1)]), _: 1 },
                ),
              ]),
              default: d(() => [
                yl,
                x(
                  p(Qe),
                  { "is-col": !1, schema: b, rules: g, onRegister: p(y) },
                  null,
                  8,
                  ["schema", "rules", "onRegister"],
                ),
              ]),
              _: 1,
            },
            8,
            ["modelValue", "class", "title"],
          )
        );
      },
    }),
    [["__scopeId", "data-v-44fc72b4"]],
  ),
  _l = pt,
  Cl = { class: "flex w-screen h-screen justify-center items-center" },
  kl = ((e) => (Ve("data-v-446e738e"), (e = e()), Se(), e))(() =>
    j(
      "div",
      { class: "flex flex-col items-center" },
      [
        j("img", { src: it, alt: "", class: "w-70px h-70px rounded-[50%]" }),
        j(
          "span",
          { class: "text-14px my-10px text-[var(--logo-title-text-color)]" },
          "Archer",
        ),
      ],
      -1,
    ),
  ),
  Ml = {
    class:
      "absolute bottom-5 w-full text-gray-300 xl:text-xl 2xl:text-3xl text-center enter-y",
  },
  Il = { class: "text-5xl mb-4 enter-x" },
  Tl = { class: "text-3xl" },
  $l = { class: "text-2xl" },
  Vl = xe(
    r({
      __name: "LockPage",
      setup(e) {
        const l = Be(),
          a = t(""),
          o = t(!1),
          n = t(!1),
          r = t(!0),
          { getPrefixCls: s } = ue(),
          u = s("lock-page"),
          c = bl(),
          {
            hour: m,
            month: f,
            minute: g,
            meridiem: b,
            year: y,
            day: C,
            week: k,
          } = ((e = !0) => {
            let t;
            const l = q({
                year: 0,
                month: 0,
                week: "",
                day: 0,
                hour: "",
                minute: "",
                second: 0,
                meridiem: "",
              }),
              a = () => {
                const e = _l(),
                  t = e.format("HH"),
                  a = e.format("mm"),
                  o = e.get("s");
                ((l.year = e.get("y")),
                  (l.month = e.get("M") + 1),
                  (l.week =
                    "星期" +
                    ["日", "一", "二", "三", "四", "五", "六"][e.day()]),
                  (l.day = e.get("date")),
                  (l.hour = t),
                  (l.minute = a),
                  (l.second = o),
                  (l.meridiem = e.format("A")));
              };
            function o() {
              (a(), clearInterval(t), (t = setInterval(() => a(), 1e3)));
            }
            function n() {
              clearInterval(t);
            }
            return (
              je(() => {
                e && o();
              }),
              Pe(() => {
                n();
              }),
              { ...Le(l), start: o, stop: n }
            );
          })(!0),
          { t: M } = ie();
        async function I() {
          l.logout();
        }
        function T(e = !1) {
          r.value = e;
        }
        return (e, t) => (
          i(),
          v(
            "div",
            {
              class: h([
                p(u),
                "fixed inset-0 flex h-screen w-screen bg-black items-center justify-center",
              ]),
            },
            [
              K(
                j(
                  "div",
                  {
                    class: h([
                      `${p(u)}__unlock`,
                      "absolute top-0 left-1/2 flex pt-5 h-16 items-center justify-center sm:text-md xl:text-xl text-white flex-col cursor-pointer transform translate-x-1/2",
                    ]),
                    onClick: t[0] || (t[0] = (e) => T(!1)),
                  },
                  [
                    x(p(ce), { icon: "ep:lock" }),
                    j("span", null, L(p(M)("lock.unlock")), 1),
                  ],
                  2,
                ),
                [[Q, r.value]],
              ),
              j("div", Cl, [
                j(
                  "div",
                  {
                    class: h([
                      `${p(u)}__hour`,
                      "relative mr-5 md:mr-20 w-2/5 h-2/5 md:h-4/5",
                    ]),
                  },
                  [
                    j("span", null, L(p(m)), 1),
                    K(
                      j(
                        "span",
                        {
                          class:
                            "meridiem absolute left-5 top-5 text-md xl:text-xl",
                        },
                        L(p(b)),
                        513,
                      ),
                      [[Q, r.value]],
                    ),
                  ],
                  2,
                ),
                j(
                  "div",
                  { class: h(`${p(u)}__minute w-2/5 h-2/5 md:h-4/5 `) },
                  [j("span", null, L(p(g)), 1)],
                  2,
                ),
              ]),
              x(
                _,
                { name: "fade-slide" },
                {
                  default: d(() => [
                    K(
                      j(
                        "div",
                        { class: h(`${p(u)}-entry`) },
                        [
                          j(
                            "div",
                            { class: h(`${p(u)}-entry-content`) },
                            [
                              kl,
                              x(
                                p(ut),
                                {
                                  type: "password",
                                  placeholder: p(M)("lock.placeholder"),
                                  class: "enter-x",
                                  modelValue: a.value,
                                  "onUpdate:modelValue":
                                    t[1] || (t[1] = (e) => (a.value = e)),
                                },
                                null,
                                8,
                                ["placeholder", "modelValue"],
                              ),
                              n.value
                                ? (i(),
                                  v(
                                    "span",
                                    {
                                      key: 0,
                                      class: h(
                                        `text-14px ${p(u)}-entry__err-msg enter-x`,
                                      ),
                                    },
                                    L(p(M)("lock.message")),
                                    3,
                                  ))
                                : w("", !0),
                              j(
                                "div",
                                { class: h(`${p(u)}-entry__footer enter-x`) },
                                [
                                  x(
                                    p($e),
                                    {
                                      type: "primary",
                                      size: "small",
                                      class: "mt-2 mr-2 enter-x",
                                      link: "",
                                      disabled: o.value,
                                      onClick: t[2] || (t[2] = (e) => T(!0)),
                                    },
                                    {
                                      default: d(() => [
                                        se(L(p(M)("common.back")), 1),
                                      ]),
                                      _: 1,
                                    },
                                    8,
                                    ["disabled"],
                                  ),
                                  x(
                                    p($e),
                                    {
                                      type: "primary",
                                      size: "small",
                                      class: "mt-2 mr-2 enter-x",
                                      link: "",
                                      disabled: o.value,
                                      onClick: I,
                                    },
                                    {
                                      default: d(() => [
                                        se(L(p(M)("lock.backToLogin")), 1),
                                      ]),
                                      _: 1,
                                    },
                                    8,
                                    ["disabled"],
                                  ),
                                  x(
                                    p($e),
                                    {
                                      type: "primary",
                                      class: "mt-2",
                                      size: "small",
                                      link: "",
                                      onClick:
                                        t[3] ||
                                        (t[3] = (e) =>
                                          (async function () {
                                            if (!a.value) return;
                                            let e = a.value;
                                            try {
                                              o.value = !0;
                                              const t = await c.unLock(e);
                                              n.value = !t;
                                            } finally {
                                              o.value = !1;
                                            }
                                          })()),
                                      disabled: o.value,
                                    },
                                    {
                                      default: d(() => [
                                        se(L(p(M)("lock.entrySystem")), 1),
                                      ]),
                                      _: 1,
                                    },
                                    8,
                                    ["disabled"],
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
                      [[Q, !r.value]],
                    ),
                  ]),
                  _: 1,
                },
              ),
              j("div", Ml, [
                K(
                  j(
                    "div",
                    Il,
                    [
                      se(L(p(m)) + ":" + L(p(g)) + " ", 1),
                      j("span", Tl, L(p(b)), 1),
                    ],
                    512,
                  ),
                  [[Q, !r.value]],
                ),
                j(
                  "div",
                  $l,
                  L(p(y)) + "/" + L(p(f)) + "/" + L(p(C)) + " " + L(p(k)),
                  1,
                ),
              ]),
            ],
            2,
          )
        );
      },
    }),
    [["__scopeId", "data-v-446e738e"]],
  ),
  Sl = { class: "flex items-center" },
  jl = ["src"],
  Pl = {
    class: "<lg:hidden text-14px pl-[5px] text-[var(--top-header-text-color)]",
  },
  Ll = r({
    __name: "UserInfo",
    setup(e) {
      const l = bl(),
        a = u(() => {
          var e;
          return (null == (e = l.getLockInfo) ? void 0 : e.isLock) ?? !1;
        }),
        o = Be(),
        { getPrefixCls: n } = ue(),
        r = n("user-info"),
        { push: s } = me(),
        { t: m } = ie(),
        f = () => {
          st.confirm(m("common.loginOutMessage"), m("common.reminder"), {
            confirmButtonText: m("common.ok"),
            cancelButtonText: m("common.cancel"),
            type: "warning",
          })
            .then(() => {
              o.logout();
            })
            .catch(() => {});
        },
        g = t(!1),
        b = () => {
          g.value = !0;
        },
        y = () => {
          s("/home");
        },
        C = u(() => o.getUser);
      return (e, t) => {
        const l = re("ElButton");
        return (
          i(),
          v(
            Y,
            null,
            [
              x(
                p(at),
                { class: h(["custom-hover", p(r)]), trigger: "click" },
                {
                  dropdown: d(() => [
                    x(p(tt), null, {
                      default: d(() => [
                        x(p(lt), null, {
                          default: d(() => [
                            x(
                              l,
                              { onClick: y, link: "" },
                              { default: d(() => [se("个人主页")]), _: 1 },
                            ),
                          ]),
                          _: 1,
                        }),
                        x(
                          p(lt),
                          { divided: "" },
                          {
                            default: d(() => [
                              j(
                                "div",
                                { onClick: b },
                                L(p(m)("lock.lockScreen")),
                                1,
                              ),
                            ]),
                            _: 1,
                          },
                        ),
                        x(p(lt), null, {
                          default: d(() => [
                            j(
                              "div",
                              { onClick: f },
                              L(p(m)("common.loginOut")),
                              1,
                            ),
                          ]),
                          _: 1,
                        }),
                      ]),
                      _: 1,
                    }),
                  ]),
                  default: d(() => [
                    j("div", Sl, [
                      j(
                        "img",
                        {
                          src: C.value.avatar ? C.value.avatar : p(it),
                          alt: "",
                          class:
                            "w-[calc(var(--logo-height)-25px)] rounded-[50%]",
                        },
                        null,
                        8,
                        jl,
                      ),
                      j("span", Pl, L(C.value.name), 1),
                    ]),
                  ]),
                  _: 1,
                },
                8,
                ["class"],
              ),
              g.value
                ? (i(),
                  c(
                    wl,
                    {
                      key: 0,
                      modelValue: g.value,
                      "onUpdate:modelValue":
                        t[0] || (t[0] = (e) => (g.value = e)),
                    },
                    null,
                    8,
                    ["modelValue"],
                  ))
                : w("", !0),
              (i(),
              c(ze, { to: "body" }, [
                x(
                  _,
                  { name: "fade-bottom", mode: "out-in" },
                  {
                    default: d(() => [
                      a.value ? (i(), c(Vl, { key: 0 })) : w("", !0),
                    ]),
                    _: 1,
                  },
                ),
              ])),
            ],
            64,
          )
        );
      };
    },
  }),
  Bl = r({
    __name: "Screenfull",
    props: { color: Ie.string.def("") },
    setup(e) {
      const { getPrefixCls: t } = ue(),
        l = t("screenfull"),
        { toggle: a, isFullscreen: o } = Ae(),
        n = () => {
          a();
        };
      return (t, a) => (
        i(),
        v(
          "div",
          { class: h(p(l)), onClick: n },
          [
            x(
              p(ce),
              {
                size: 18,
                icon: p(o) ? "zmdi:fullscreen-exit" : "zmdi:fullscreen",
                color: e.color,
              },
              null,
              8,
              ["icon", "color"],
            ),
          ],
          2,
        )
      );
    },
  }),
  zl = (e, t = "") => {
    var l;
    const a = [];
    for (const o of e) {
      const e = null == o ? void 0 : o.meta;
      if (e.hidden && !e.canTo) continue;
      const n =
        e.alwaysShow || 1 !== (null == (l = o.children) ? void 0 : l.length)
          ? { ...o }
          : { ...o.children[0], path: pe(o.path, o.children[0].path) };
      ((n.path = pe(t, n.path)),
        n.children && (n.children = zl(n.children, n.path)),
        n && a.push(n));
    }
    return a;
  };
const { getPrefixCls: Al } = ue(),
  El = Al("breadcrumb"),
  Ol = ve(),
  Rl = u(() => Ol.getBreadcrumbIcon),
  Hl = xe(
    r({
      name: "Breadcrumb",
      setup() {
        const { currentRoute: e } = me(),
          { t: l } = ie(),
          a = t([]),
          o = he(),
          n = u(() => {
            const e = o.getRouters;
            return zl(e);
          });
        return (
          D(
            () => e.value,
            (t) => {
              t.path.startsWith("/redirect/") ||
                (() => {
                  const t = e.value.matched.slice(-1)[0].path;
                  a.value = We(p(n), (e) => e.path === t);
                })();
            },
            { immediate: !0 },
          ),
          () => {
            let e;
            return x(
              $t,
              {
                separator: "/",
                class: `${El} flex items-center h-full ml-[10px]`,
              },
              {
                default: () => {
                  return [
                    x(
                      Ee,
                      {
                        appear: !0,
                        "enter-active-class":
                          "animate__animated animate__fadeInRight",
                      },
                      ((t = e =
                        Ge(p(a)).map((e) => {
                          const t = !e.redirect || "noredirect" === e.redirect,
                            a = e.meta;
                          return x(
                            Vt,
                            { to: { path: t ? "" : e.path }, key: e.name },
                            {
                              default: () => {
                                var t, o;
                                return [
                                  (null == a ? void 0 : a.icon) && Rl.value
                                    ? x(Y, null, [
                                        x(
                                          ce,
                                          { icon: a.icon, class: "mr-[5px]" },
                                          null,
                                        ),
                                        se(" "),
                                        l(
                                          (null ==
                                          (t = null == e ? void 0 : e.meta)
                                            ? void 0
                                            : t.title) || "",
                                        ),
                                      ])
                                    : l(
                                        (null ==
                                        (o = null == e ? void 0 : e.meta)
                                          ? void 0
                                          : o.title) || "",
                                      ),
                                ];
                              },
                            },
                          );
                        })),
                      "function" == typeof t ||
                      ("[object Object]" ===
                        Object.prototype.toString.call(t) &&
                        !ge(t))
                        ? e
                        : { default: () => [e] }),
                    ),
                  ];
                  var t;
                },
              },
            );
          }
        );
      },
    }),
    [["__scopeId", "data-v-48a8fb48"]],
  ),
  Nl = (e) => /^#([0-9a-fA-F]{3}|[0-9a-fA-f]{6})$/.test(e),
  Ul = (e, t) => {
    let l = e.toLowerCase();
    if (Nl(e)) {
      if (4 === l.length) {
        let e = "#";
        for (let t = 1; t < 4; t += 1)
          e += l.slice(t, t + 1).concat(l.slice(t, t + 1));
        l = e;
      }
      const e = [];
      for (let t = 1; t < 7; t += 2) e.push(parseInt("0x" + l.slice(t, t + 2)));
      return t
        ? "RGBA(" + e.join(",") + "," + t + ")"
        : "RGB(" + e.join(",") + ")";
    }
    return l;
  },
  Fl = (e) => {
    if (!Nl(e)) return;
    const [t, l, a] = Ul(e)
      .replace(/(?:\(|\)|rgb|RGB)*/g, "")
      .split(",")
      .map((e) => Number(e));
    return 0.299 * t + 0.578 * l + 0.114 * a < 192;
  },
  ql = (e, t) => (
    (e = e.indexOf("#") >= 0 ? e.substring(1, e.length) : e),
    (t = Math.trunc((255 * t) / 100)),
    `#${Dl(e.substring(0, 2), t)}${Dl(e.substring(2, 4), t)}${Dl(e.substring(4, 6), t)}`
  ),
  Dl = (e, t) => {
    const l = parseInt(e, 16) + t,
      a = l > 255 ? 255 : l;
    return a.toString(16).length > 1 ? a.toString(16) : `0${a.toString(16)}`;
  },
  Wl = ["onClick"],
  Gl = xe(
    r({
      __name: "ColorRadioPicker",
      props: {
        schema: { type: Array, default: () => [] },
        modelValue: Ie.string.def(""),
      },
      emits: ["update:modelValue", "change"],
      setup(e, { emit: l }) {
        const a = e,
          { getPrefixCls: o } = ue(),
          n = o("color-radio-picker"),
          r = t(a.modelValue);
        return (
          D(
            () => a.modelValue,
            (e) => {
              e !== p(r) && (r.value = e);
            },
          ),
          D(
            () => r.value,
            (e) => {
              (l("update:modelValue", e), l("change", e));
            },
          ),
          (t, l) => {
            const a = re("Icon");
            return (
              i(),
              v(
                "div",
                { class: h([p(n), "flex flex-wrap space-x-14px"]) },
                [
                  (i(!0),
                  v(
                    Y,
                    null,
                    we(
                      e.schema,
                      (e, t) => (
                        i(),
                        v(
                          "span",
                          {
                            key: `radio-${t}`,
                            class: h([
                              "w-20px h-20px cursor-pointer rounded-2px border-solid border-gray-300 border-2px text-center leading-20px mb-5px",
                              { "is-active": r.value === e },
                            ]),
                            style: m({ background: e }),
                            onClick: (t) => (r.value = e),
                          },
                          [
                            r.value === e
                              ? (i(),
                                c(a, {
                                  key: 0,
                                  color: "#fff",
                                  icon: "ep:check",
                                  size: 16,
                                }))
                              : w("", !0),
                          ],
                          14,
                          Wl,
                        )
                      ),
                    ),
                    128,
                  )),
                ],
                2,
              )
            );
          }
        );
      },
    }),
    [["__scopeId", "data-v-01144e6d"]],
  ),
  Zl = { class: "flex justify-between items-center" },
  Kl = { class: "text-14px" },
  Ql = { class: "flex justify-between items-center" },
  Yl = { class: "text-14px" },
  Jl = { class: "flex justify-between items-center" },
  Xl = { class: "text-14px" },
  ea = { class: "flex justify-between items-center" },
  ta = { class: "text-14px" },
  la = { class: "flex justify-between items-center" },
  aa = { class: "text-14px" },
  oa = { class: "flex justify-between items-center" },
  na = { class: "text-14px" },
  ra = { class: "flex justify-between items-center" },
  sa = { class: "text-14px" },
  ua = { class: "flex justify-between items-center" },
  ia = { class: "text-14px" },
  ca = { class: "flex justify-between items-center" },
  da = { class: "text-14px" },
  pa = { class: "flex justify-between items-center" },
  va = { class: "text-14px" },
  ma = { class: "flex justify-between items-center" },
  ha = { class: "text-14px" },
  fa = { class: "flex justify-between items-center" },
  ga = { class: "text-14px" },
  xa = { class: "flex justify-between items-center" },
  ba = { class: "text-14px" },
  ya = r({
    __name: "InterfaceDisplay",
    setup(e) {
      const { getPrefixCls: l } = ue(),
        a = l("interface-display"),
        o = ve(),
        { t: n } = ie(),
        r = t(o.getBreadcrumb),
        s = (e) => {
          o.setBreadcrumb(e);
        },
        c = t(o.getBreadcrumbIcon),
        d = (e) => {
          o.setBreadcrumbIcon(e);
        },
        m = t(o.getHamburger),
        f = (e) => {
          o.setHamburger(e);
        },
        g = t(o.getScreenfull),
        b = (e) => {
          o.setScreenfull(e);
        },
        y = t(o.getSize),
        w = (e) => {
          o.setSize(e);
        },
        _ = t(o.getLocale),
        C = (e) => {
          o.setLocale(e);
        },
        k = t(o.getTagsView),
        M = (e) => {
          (Oe("--tags-view-height", e ? "35px" : "0px"), o.setTagsView(e));
        },
        I = t(o.getTagsViewIcon),
        T = (e) => {
          o.setTagsViewIcon(e);
        },
        $ = t(o.getLogo),
        V = (e) => {
          o.setLogo(e);
        },
        S = t(o.getUniqueOpened),
        P = (e) => {
          o.setUniqueOpened(e);
        },
        B = t(o.getFixedHeader),
        z = (e) => {
          o.setFixedHeader(e);
        },
        A = t(o.getFooter),
        E = (e) => {
          o.setFooter(e);
        },
        O = t(o.getGreyMode),
        R = (e) => {
          o.setGreyMode(e);
        },
        H = u(() => o.getLayout);
      return (
        D(
          () => H.value,
          (e) => {
            "top" === e && o.setCollapse(!1);
          },
        ),
        (e, t) => (
          i(),
          v(
            "div",
            { class: h(p(a)) },
            [
              j("div", Zl, [
                j("span", Kl, L(p(n)("setting.breadcrumb")), 1),
                x(
                  p(ht),
                  {
                    modelValue: r.value,
                    "onUpdate:modelValue":
                      t[0] || (t[0] = (e) => (r.value = e)),
                    onChange: s,
                  },
                  null,
                  8,
                  ["modelValue"],
                ),
              ]),
              j("div", Ql, [
                j("span", Yl, L(p(n)("setting.breadcrumbIcon")), 1),
                x(
                  p(ht),
                  {
                    modelValue: c.value,
                    "onUpdate:modelValue":
                      t[1] || (t[1] = (e) => (c.value = e)),
                    onChange: d,
                  },
                  null,
                  8,
                  ["modelValue"],
                ),
              ]),
              j("div", Jl, [
                j("span", Xl, L(p(n)("setting.hamburgerIcon")), 1),
                x(
                  p(ht),
                  {
                    modelValue: m.value,
                    "onUpdate:modelValue":
                      t[2] || (t[2] = (e) => (m.value = e)),
                    onChange: f,
                  },
                  null,
                  8,
                  ["modelValue"],
                ),
              ]),
              j("div", ea, [
                j("span", ta, L(p(n)("setting.screenfullIcon")), 1),
                x(
                  p(ht),
                  {
                    modelValue: g.value,
                    "onUpdate:modelValue":
                      t[3] || (t[3] = (e) => (g.value = e)),
                    onChange: b,
                  },
                  null,
                  8,
                  ["modelValue"],
                ),
              ]),
              j("div", la, [
                j("span", aa, L(p(n)("setting.sizeIcon")), 1),
                x(
                  p(ht),
                  {
                    modelValue: y.value,
                    "onUpdate:modelValue":
                      t[4] || (t[4] = (e) => (y.value = e)),
                    onChange: w,
                  },
                  null,
                  8,
                  ["modelValue"],
                ),
              ]),
              j("div", oa, [
                j("span", na, L(p(n)("setting.localeIcon")), 1),
                x(
                  p(ht),
                  {
                    modelValue: _.value,
                    "onUpdate:modelValue":
                      t[5] || (t[5] = (e) => (_.value = e)),
                    onChange: C,
                  },
                  null,
                  8,
                  ["modelValue"],
                ),
              ]),
              j("div", ra, [
                j("span", sa, L(p(n)("setting.tagsView")), 1),
                x(
                  p(ht),
                  {
                    modelValue: k.value,
                    "onUpdate:modelValue":
                      t[6] || (t[6] = (e) => (k.value = e)),
                    onChange: M,
                  },
                  null,
                  8,
                  ["modelValue"],
                ),
              ]),
              j("div", ua, [
                j("span", ia, L(p(n)("setting.tagsViewIcon")), 1),
                x(
                  p(ht),
                  {
                    modelValue: I.value,
                    "onUpdate:modelValue":
                      t[7] || (t[7] = (e) => (I.value = e)),
                    onChange: T,
                  },
                  null,
                  8,
                  ["modelValue"],
                ),
              ]),
              j("div", ca, [
                j("span", da, L(p(n)("setting.logo")), 1),
                x(
                  p(ht),
                  {
                    modelValue: $.value,
                    "onUpdate:modelValue":
                      t[8] || (t[8] = (e) => ($.value = e)),
                    onChange: V,
                  },
                  null,
                  8,
                  ["modelValue"],
                ),
              ]),
              j("div", pa, [
                j("span", va, L(p(n)("setting.uniqueOpened")), 1),
                x(
                  p(ht),
                  {
                    modelValue: S.value,
                    "onUpdate:modelValue":
                      t[9] || (t[9] = (e) => (S.value = e)),
                    onChange: P,
                  },
                  null,
                  8,
                  ["modelValue"],
                ),
              ]),
              j("div", ma, [
                j("span", ha, L(p(n)("setting.fixedHeader")), 1),
                x(
                  p(ht),
                  {
                    modelValue: B.value,
                    "onUpdate:modelValue":
                      t[10] || (t[10] = (e) => (B.value = e)),
                    onChange: z,
                  },
                  null,
                  8,
                  ["modelValue"],
                ),
              ]),
              j("div", fa, [
                j("span", ga, L(p(n)("setting.footer")), 1),
                x(
                  p(ht),
                  {
                    modelValue: A.value,
                    "onUpdate:modelValue":
                      t[11] || (t[11] = (e) => (A.value = e)),
                    onChange: E,
                  },
                  null,
                  8,
                  ["modelValue"],
                ),
              ]),
              j("div", xa, [
                j("span", ba, L(p(n)("setting.greyMode")), 1),
                x(
                  p(ht),
                  {
                    modelValue: O.value,
                    "onUpdate:modelValue":
                      t[12] || (t[12] = (e) => (O.value = e)),
                    onChange: R,
                  },
                  null,
                  8,
                  ["modelValue"],
                ),
              ]),
            ],
            2,
          )
        )
      );
    },
  }),
  wa = [
    ((e) => (Ve("data-v-8c3c6718"), (e = e()), Se(), e))(() =>
      j(
        "div",
        { class: "absolute h-full w-[33%] top-0 left-[10%] bg-gray-200" },
        null,
        -1,
      ),
    ),
  ],
  _a = xe(
    r({
      __name: "LayoutRadioPicker",
      setup(e) {
        const { getPrefixCls: t } = ue(),
          l = t("layout-radio-picker"),
          a = ve(),
          o = u(() => a.getLayout);
        return (e, t) => (
          i(),
          v(
            "div",
            { class: h([p(l), "flex flex-wrap space-x-14px"]) },
            [
              j(
                "div",
                {
                  class: h([
                    `${p(l)}__classic`,
                    "relative w-56px h-48px cursor-pointer bg-gray-300",
                    { "is-acitve": "classic" === o.value },
                  ]),
                  onClick: t[0] || (t[0] = (e) => p(a).setLayout("classic")),
                },
                null,
                2,
              ),
              j(
                "div",
                {
                  class: h([
                    `${p(l)}__top-left`,
                    "relative w-56px h-48px cursor-pointer bg-gray-300",
                    { "is-acitve": "topLeft" === o.value },
                  ]),
                  onClick: t[1] || (t[1] = (e) => p(a).setLayout("topLeft")),
                },
                null,
                2,
              ),
              j(
                "div",
                {
                  class: h([
                    `${p(l)}__top`,
                    "relative w-56px h-48px cursor-pointer bg-gray-300",
                    { "is-acitve": "top" === o.value },
                  ]),
                  onClick: t[2] || (t[2] = (e) => p(a).setLayout("top")),
                },
                null,
                2,
              ),
              j(
                "div",
                {
                  class: h([
                    `${p(l)}__cut-menu`,
                    "relative w-56px h-48px cursor-pointer bg-gray-300",
                    { "is-acitve": "cutMenu" === o.value },
                  ]),
                  onClick: t[3] || (t[3] = (e) => p(a).setLayout("cutMenu")),
                },
                wa,
                2,
              ),
            ],
            2,
          )
        );
      },
    }),
    [["__scopeId", "data-v-8c3c6718"]],
  ),
  Ca = { class: "text-16px font-700" },
  ka = { class: "text-center" },
  Ma = { class: "mt-5px" },
  Ia = xe(
    r({
      __name: "SettingV2",
      props: { color: Ie.string.def("") },
      setup(e) {
        const { removeStorage: l } = Fe(),
          { getPrefixCls: a } = ue(),
          o = a("setting-v2"),
          n = ve(),
          { t: r } = ie(),
          s = u(() => n.getLayout),
          c = t(!1),
          m = t(n.getTheme.elColorPrimary),
          f = (e) => {
            (Oe("--el-color-primary", e), n.setTheme({ elColorPrimary: e }));
            const t = Re("--left-menu-bg-color", document.documentElement);
            _(He(p(t)));
          },
          g = t(n.getTheme.topHeaderBgColor || ""),
          b = (e) => {
            const t = Fl(e),
              l = t ? "#fff" : "inherit",
              a = t ? ql(e, 6) : "#f6f6f6",
              o = t ? e : "#eee";
            (Oe("--top-header-bg-color", e),
              Oe("--top-header-text-color", l),
              Oe("--top-header-hover-color", a),
              n.setTheme({
                topHeaderBgColor: e,
                topHeaderTextColor: l,
                topHeaderHoverColor: a,
                topToolBorderColor: o,
              }),
              "top" === p(s) && _(e));
          },
          y = t(n.getTheme.leftMenuBgColor || ""),
          _ = (e) => {
            const t = Re("--el-color-primary", document.documentElement),
              l = Fl(e),
              a = {
                leftMenuBorderColor: l ? "inherit" : "#eee",
                leftMenuBgColor: e,
                leftMenuBgLightColor: l ? ql(e, 6) : e,
                leftMenuBgActiveColor: l
                  ? "var(--el-color-primary)"
                  : Ul(p(t), 0.1),
                leftMenuCollapseBgActiveColor: l
                  ? "var(--el-color-primary)"
                  : Ul(p(t), 0.1),
                leftMenuTextColor: l ? "#bfcbd9" : "#333",
                leftMenuTextActiveColor: l ? "#fff" : "var(--el-color-primary)",
                logoTitleTextColor: l ? "#fff" : "inherit",
                logoBorderColor: l ? e : "#eee",
              };
            (n.setTheme(a), n.setCssVarTheme());
          };
        D(
          () => s.value,
          (e) => {
            "top" !== e || n.getIsDark
              ? _(p(y))
              : ((g.value = "#fff"), b("#fff"));
          },
        );
        const C = async () => {
            const {
              copy: e,
              copied: t,
              isSupported: l,
            } = Ne({
              source: `\n      // 面包屑\n      breadcrumb: ${n.getBreadcrumb},\n      // 面包屑图标\n      breadcrumbIcon: ${n.getBreadcrumbIcon},\n      // 折叠图标\n      hamburger: ${n.getHamburger},\n      // 全屏图标\n      screenfull: ${n.getScreenfull},\n      // 尺寸图标\n      size: ${n.getSize},\n      // 多语言图标\n      locale: ${n.getLocale},\n      // 标签页\n      tagsView: ${n.getTagsView},\n      // 标签页图标\n      getTagsViewIcon: ${n.getTagsViewIcon},\n      // logo\n      logo: ${n.getLogo},\n      // 菜单手风琴\n      uniqueOpened: ${n.getUniqueOpened},\n      // 固定header\n      fixedHeader: ${n.getFixedHeader},\n      // 页脚\n      footer: ${n.getFooter},\n      // 灰色模式\n      greyMode: ${n.getGreyMode},\n      // layout布局\n      layout: '${n.getLayout}',\n      // 暗黑模式\n      isDark: ${n.getIsDark},\n      // 组件尺寸\n      currentSize: '${n.getCurrentSize}',\n      // 主题相关\n      theme: {\n        // 主题色\n        elColorPrimary: '${n.getTheme.elColorPrimary}',\n        // 左侧菜单边框颜色\n        leftMenuBorderColor: '${n.getTheme.leftMenuBorderColor}',\n        // 左侧菜单背景颜色\n        leftMenuBgColor: '${n.getTheme.leftMenuBgColor}',\n        // 左侧菜单浅色背景颜色\n        leftMenuBgLightColor: '${n.getTheme.leftMenuBgLightColor}',\n        // 左侧菜单选中背景颜色\n        leftMenuBgActiveColor: '${n.getTheme.leftMenuBgActiveColor}',\n        // 左侧菜单收起选中背景颜色\n        leftMenuCollapseBgActiveColor: '${n.getTheme.leftMenuCollapseBgActiveColor}',\n        // 左侧菜单字体颜色\n        leftMenuTextColor: '${n.getTheme.leftMenuTextColor}',\n        // 左侧菜单选中字体颜色\n        leftMenuTextActiveColor: '${n.getTheme.leftMenuTextActiveColor}',\n        // logo字体颜色\n        logoTitleTextColor: '${n.getTheme.logoTitleTextColor}',\n        // logo边框颜色\n        logoBorderColor: '${n.getTheme.logoBorderColor}',\n        // 头部背景颜色\n        topHeaderBgColor: '${n.getTheme.topHeaderBgColor}',\n        // 头部字体颜色\n        topHeaderTextColor: '${n.getTheme.topHeaderTextColor}',\n        // 头部悬停颜色\n        topHeaderHoverColor: '${n.getTheme.topHeaderHoverColor}',\n        // 头部边框颜色\n        topToolBorderColor: '${n.getTheme.topToolBorderColor}'\n      }\n    `,
            });
            l
              ? (await e(), p(t) && Ue.success(r("setting.copySuccess")))
              : Ue.error(r("setting.copyFailed"));
          },
          k = () => {
            (l("layout"), l("theme"), l("isDark"), window.location.reload());
          };
        return (t, l) => {
          const a = re("Icon");
          return (
            i(),
            v(
              "div",
              { class: h(p(o)) },
              [
                x(
                  a,
                  {
                    icon: "icon-park-outline:theme",
                    onClick: l[0] || (l[0] = (e) => (c.value = !0)),
                    class: h(["cursor-pointer !p-0", t.$attrs.class]),
                    color: e.color,
                    size: 18,
                  },
                  null,
                  8,
                  ["class", "color"],
                ),
                x(
                  p(vt),
                  {
                    modelValue: c.value,
                    "onUpdate:modelValue":
                      l[4] || (l[4] = (e) => (c.value = e)),
                    direction: "rtl",
                    size: "350px",
                    "z-index": 4e3,
                  },
                  {
                    header: d(() => [
                      j("span", Ca, L(p(r)("setting.projectSetting")), 1),
                    ]),
                    default: d(() => [
                      j("div", ka, [
                        x(p(mt), null, {
                          default: d(() => [se(L(p(r)("setting.theme")), 1)]),
                          _: 1,
                        }),
                        x(p(nt)),
                        x(p(mt), null, {
                          default: d(() => [se(L(p(r)("setting.layout")), 1)]),
                          _: 1,
                        }),
                        x(_a),
                        x(p(mt), null, {
                          default: d(() => [
                            se(L(p(r)("setting.systemTheme")), 1),
                          ]),
                          _: 1,
                        }),
                        x(
                          Gl,
                          {
                            modelValue: m.value,
                            "onUpdate:modelValue":
                              l[1] || (l[1] = (e) => (m.value = e)),
                            schema: [
                              "#409eff",
                              "#009688",
                              "#536dfe",
                              "#ff5c93",
                              "#ee4f12",
                              "#0096c7",
                              "#9c27b0",
                              "#ff9800",
                            ],
                            onChange: f,
                          },
                          null,
                          8,
                          ["modelValue"],
                        ),
                        x(p(mt), null, {
                          default: d(() => [
                            se(L(p(r)("setting.headerTheme")), 1),
                          ]),
                          _: 1,
                        }),
                        x(
                          Gl,
                          {
                            modelValue: g.value,
                            "onUpdate:modelValue":
                              l[2] || (l[2] = (e) => (g.value = e)),
                            schema: [
                              "#fff",
                              "#151515",
                              "#5172dc",
                              "#e74c3c",
                              "#24292e",
                              "#394664",
                              "#009688",
                              "#383f45",
                            ],
                            onChange: b,
                          },
                          null,
                          8,
                          ["modelValue"],
                        ),
                        "top" !== s.value
                          ? (i(),
                            v(
                              Y,
                              { key: 0 },
                              [
                                x(p(mt), null, {
                                  default: d(() => [
                                    se(L(p(r)("setting.menuTheme")), 1),
                                  ]),
                                  _: 1,
                                }),
                                x(
                                  Gl,
                                  {
                                    modelValue: y.value,
                                    "onUpdate:modelValue":
                                      l[3] || (l[3] = (e) => (y.value = e)),
                                    schema: [
                                      "#fff",
                                      "#001529",
                                      "#212121",
                                      "#273352",
                                      "#191b24",
                                      "#383f45",
                                      "#001628",
                                      "#344058",
                                    ],
                                    onChange: _,
                                  },
                                  null,
                                  8,
                                  ["modelValue"],
                                ),
                              ],
                              64,
                            ))
                          : w("", !0),
                      ]),
                      x(p(mt), null, {
                        default: d(() => [
                          se(L(p(r)("setting.interfaceDisplay")), 1),
                        ]),
                        _: 1,
                      }),
                      x(ya),
                      x(p(mt)),
                      j("div", null, [
                        x(
                          p($e),
                          { type: "primary", class: "w-full", onClick: C },
                          {
                            default: d(() => [se(L(p(r)("setting.copy")), 1)]),
                            _: 1,
                          },
                        ),
                      ]),
                      j("div", Ma, [
                        x(
                          p($e),
                          { type: "danger", class: "w-full", onClick: k },
                          {
                            default: d(() => [
                              se(L(p(r)("setting.clearAndReset")), 1),
                            ]),
                            _: 1,
                          },
                        ),
                      ]),
                    ]),
                    _: 1,
                  },
                  8,
                  ["modelValue"],
                ),
              ],
              2,
            )
          );
        };
      },
    }),
    [["__scopeId", "data-v-23ae369e"]],
  ),
  { getPrefixCls: Ta, variables: $a } = ue(),
  Va = Ta("tool-header"),
  Sa = ve(),
  ja = u(() => Sa.getBreadcrumb),
  Pa = u(() => Sa.getHamburger),
  La = u(() => Sa.getScreenfull),
  Ba = u(() => Sa.getSize),
  za = u(() => Sa.getLayout),
  Aa = u(() => Sa.getLocale),
  Ea = xe(
    r({
      name: "ToolHeader",
      setup: () => () =>
        x(
          "div",
          {
            id: `${$a.namespace}-tool-header`,
            class: [
              Va,
              "h-[var(--top-tool-height)] relative px-[var(--top-tool-p-x)] flex items-center justify-between",
              "dark:bg-[var(--el-bg-color)]",
            ],
          },
          [
            "top" !== za.value
              ? x("div", { class: "h-full flex items-center" }, [
                  Pa.value && "cutMenu" !== za.value
                    ? x(
                        gl,
                        {
                          class: "custom-hover",
                          color: "var(--top-header-text-color)",
                        },
                        null,
                      )
                    : void 0,
                  ja.value ? x(Hl, { class: "<md:hidden" }, null) : void 0,
                ])
              : void 0,
            x("div", { class: "h-full flex items-center" }, [
              x(
                Ia,
                {
                  class: "custom-hover",
                  color: "var(--top-header-text-color)",
                },
                null,
              ),
              La.value
                ? x(
                    Bl,
                    {
                      class: "custom-hover",
                      color: "var(--top-header-text-color)",
                    },
                    null,
                  )
                : void 0,
              Ba.value
                ? x(
                    xl,
                    {
                      class: "custom-hover",
                      color: "var(--top-header-text-color)",
                    },
                    null,
                  )
                : void 0,
              Aa.value
                ? x(
                    rt,
                    {
                      class: "custom-hover",
                      color: "var(--top-header-text-color)",
                    },
                    null,
                  )
                : void 0,
              x(Ll, null, null),
            ]),
          ],
        ),
    }),
    [["__scopeId", "data-v-df17a94c"]],
  ),
  { getPrefixCls: Oa } = ue(),
  Ra = Oa("layout"),
  Ha = ve(),
  Na = u(() => Ha.getPageLoading),
  Ua = u(() => Ha.getTagsView),
  Fa = u(() => Ha.getCollapse),
  qa = u(() => Ha.logo),
  Da = u(() => Ha.getFixedHeader),
  Wa = u(() => Ha.getMobile),
  Ga = u(() => Ha.getFixedMenu),
  Za = () => ({
    renderClassic: () =>
      x(Y, null, [
        x(
          "div",
          {
            class: [
              "absolute top-0 left-0 h-full layout-border__right",
              { "!fixed z-3000": Wa.value },
            ],
          },
          [
            qa.value
              ? x(
                  hl,
                  {
                    class: [
                      "bg-[var(--left-menu-bg-color)] relative",
                      {
                        "!pl-0": Wa.value && Fa.value,
                        "w-[var(--left-menu-min-width)]": Ha.getCollapse,
                        "w-[var(--left-menu-max-width)]": !Ha.getCollapse,
                      },
                    ],
                    style: "transition: all var(--transition-time-02);",
                  },
                  null,
                )
              : void 0,
            x(
              Xt,
              { class: [{ "!h-[calc(100%-var(--logo-height))]": qa.value }] },
              null,
            ),
          ],
        ),
        x(
          "div",
          {
            class: [
              `${Ra}-content`,
              "absolute top-0 h-[100%]",
              {
                "w-[calc(100%-var(--left-menu-min-width))] left-[var(--left-menu-min-width)]":
                  Fa.value && !Wa.value && !Wa.value,
                "w-[calc(100%-var(--left-menu-max-width))] left-[var(--left-menu-max-width)]":
                  !Fa.value && !Wa.value && !Wa.value,
                "fixed !w-full !left-0": Wa.value,
              },
            ],
            style: "transition: all var(--transition-time-02);",
          },
          [
            K(
              x(
                fe,
                {
                  class: [
                    `${Ra}-content-scrollbar`,
                    {
                      "!h-[calc(100%-var(--top-tool-height)-var(--tags-view-height))] mt-[calc(var(--top-tool-height)+var(--tags-view-height))]":
                        Da.value,
                    },
                  ],
                },
                {
                  default: () => [
                    x(
                      "div",
                      {
                        class: [
                          {
                            "fixed top-0 left-0 z-10": Da.value,
                            "w-[calc(100%-var(--left-menu-min-width))] !left-[var(--left-menu-min-width)]":
                              Fa.value && Da.value && !Wa.value,
                            "w-[calc(100%-var(--left-menu-max-width))] !left-[var(--left-menu-max-width)]":
                              !Fa.value && Da.value && !Wa.value,
                            "!w-full !left-0": Wa.value,
                          },
                        ],
                        style: "transition: all var(--transition-time-02);",
                      },
                      [
                        x(
                          Ea,
                          {
                            class: [
                              "bg-[var(--top-header-bg-color)]",
                              { "layout-border__bottom": !Ua.value },
                            ],
                          },
                          null,
                        ),
                        Ua.value
                          ? x(
                              vl,
                              {
                                class:
                                  "layout-border__bottom layout-border__top",
                              },
                              null,
                            )
                          : void 0,
                      ],
                    ),
                    x(fl, null, null),
                  ],
                },
              ),
              [[ye("loading"), Na.value]],
            ),
          ],
        ),
      ]),
    renderTopLeft: () =>
      x(Y, null, [
        x(
          "div",
          {
            class:
              "flex items-center bg-[var(--top-header-bg-color)] relative layout-border__bottom dark:bg-[var(--el-bg-color)]",
          },
          [
            qa.value ? x(hl, { class: "custom-hover" }, null) : void 0,
            x(Ea, { class: "flex-1" }, null),
          ],
        ),
        x(
          "div",
          {
            class:
              "absolute top-[var(--logo-height)+1px] left-0 w-full h-[calc(100%-1px-var(--logo-height))] flex",
          },
          [
            x(Xt, { class: "!h-full relative layout-border__right" }, null),
            x(
              "div",
              {
                class: [
                  `${Ra}-content`,
                  "h-[100%]",
                  {
                    "w-[calc(100%-var(--left-menu-min-width))] left-[var(--left-menu-min-width)]":
                      Fa.value,
                    "w-[calc(100%-var(--left-menu-max-width))] left-[var(--left-menu-max-width)]":
                      !Fa.value,
                  },
                ],
                style: "transition: all var(--transition-time-02);",
              },
              [
                K(
                  x(
                    fe,
                    {
                      class: [
                        `${Ra}-content-scrollbar`,
                        {
                          "!h-[calc(100%-var(--tags-view-height))] mt-[calc(var(--tags-view-height))]":
                            Da.value && Ua.value,
                        },
                      ],
                    },
                    {
                      default: () => [
                        Ua.value
                          ? x(
                              vl,
                              {
                                class: [
                                  "layout-border__bottom absolute",
                                  {
                                    "!fixed top-0 left-0 z-10": Da.value,
                                    "w-[calc(100%-var(--left-menu-min-width))] !left-[var(--left-menu-min-width)] mt-[calc(var(--logo-height)+1px)]":
                                      Fa.value && Da.value,
                                    "w-[calc(100%-var(--left-menu-max-width))] !left-[var(--left-menu-max-width)] mt-[calc(var(--logo-height)+1px)]":
                                      !Fa.value && Da.value,
                                  },
                                ],
                                style:
                                  "transition: width var(--transition-time-02), left var(--transition-time-02);",
                              },
                              null,
                            )
                          : void 0,
                        x(fl, null, null),
                      ],
                    },
                  ),
                  [[ye("loading"), Na.value]],
                ),
              ],
            ),
          ],
        ),
      ]),
    renderTop: () =>
      x(Y, null, [
        x(
          "div",
          {
            class: [
              "flex items-center justify-between bg-[var(--top-header-bg-color)] relative",
              { "layout-border__bottom": !Ua.value },
            ],
          },
          [
            qa.value ? x(hl, { class: "custom-hover" }, null) : void 0,
            x(Xt, { class: "flex-1 px-10px h-[var(--top-tool-height)]" }, null),
            x(Ea, null, null),
          ],
        ),
        x(
          "div",
          {
            class: [
              `${Ra}-content`,
              "w-full",
              {
                "h-[calc(100%-var(--app-footer-height))]": !Da.value,
                "h-[calc(100%-var(--tags-view-height)-var(--app-footer-height))]":
                  Da.value,
              },
            ],
          },
          [
            K(
              x(
                fe,
                {
                  class: [
                    `${Ra}-content-scrollbar`,
                    {
                      "mt-[var(--tags-view-height)] !pb-[calc(var(--tags-view-height)+var(--app-footer-height))]":
                        Da.value,
                      "pb-[var(--app-footer-height)]": !Da.value,
                    },
                  ],
                },
                {
                  default: () => [
                    Ua.value
                      ? x(
                          vl,
                          {
                            class: [
                              "layout-border__bottom layout-border__top relative",
                              {
                                "!fixed w-full top-[calc(var(--top-tool-height)+1px)] left-0":
                                  Da.value,
                              },
                            ],
                            style:
                              "transition: width var(--transition-time-02), left var(--transition-time-02);",
                          },
                          null,
                        )
                      : void 0,
                    x(fl, null, null),
                  ],
                },
              ),
              [[ye("loading"), Na.value]],
            ),
          ],
        ),
      ]),
    renderCutMenu: () =>
      x(Y, null, [
        x(
          "div",
          {
            class:
              "flex items-center bg-[var(--top-header-bg-color)] relative layout-border__bottom",
          },
          [
            qa.value ? x(hl, { class: "custom-hover !pr-15px" }, null) : void 0,
            x(Ea, { class: "flex-1" }, null),
          ],
        ),
        x(
          "div",
          {
            class:
              "absolute top-[var(--logo-height)] left-0 w-[calc(100%-2px)] h-[calc(100%-var(--logo-height))] flex",
          },
          [
            x(nl, null, null),
            x(
              "div",
              {
                class: [
                  `${Ra}-content`,
                  "h-[100%]",
                  {
                    "w-[calc(100%-var(--tab-menu-min-width))] left-[var(--tab-menu-min-width)]":
                      Fa.value && !Ga.value,
                    "w-[calc(100%-var(--tab-menu-max-width))] left-[var(--tab-menu-max-width)]":
                      !Fa.value && !Ga.value,
                    "w-[calc(100%-var(--tab-menu-min-width)-var(--left-menu-max-width))] ml-[var(--left-menu-max-width)]":
                      Fa.value && Ga.value,
                    "w-[calc(100%-var(--tab-menu-max-width)-var(--left-menu-max-width))] ml-[var(--left-menu-max-width)]":
                      !Fa.value && Ga.value,
                  },
                ],
                style: "transition: all var(--transition-time-02);",
              },
              [
                K(
                  x(
                    fe,
                    {
                      class: [
                        `${Ra}-content-scrollbar`,
                        {
                          "!h-[calc(100%-var(--tags-view-height))] mt-[calc(var(--tags-view-height))]":
                            Da.value && Ua.value,
                        },
                      ],
                    },
                    {
                      default: () => [
                        Ua.value
                          ? x(
                              vl,
                              {
                                class: [
                                  "relative layout-border__bottom layout-border__top",
                                  {
                                    "!fixed top-0 left-0 z-10": Da.value,
                                    "w-[calc(100%-var(--tab-menu-min-width))] !left-[var(--tab-menu-min-width)] mt-[var(--logo-height)]":
                                      Fa.value && Da.value,
                                    "w-[calc(100%-var(--tab-menu-max-width))] !left-[var(--tab-menu-max-width)] mt-[var(--logo-height)]":
                                      !Fa.value && Da.value,
                                    "!fixed top-0 !left-[var(--tab-menu-min-width)+var(--left-menu-max-width)] z-10":
                                      Da.value && Ga.value,
                                    "w-[calc(100%-var(--tab-menu-min-width)-var(--left-menu-max-width))] !left-[var(--tab-menu-min-width)+var(--left-menu-max-width)] mt-[var(--logo-height)]":
                                      Fa.value && Da.value && Ga.value,
                                    "w-[calc(100%-var(--tab-menu-max-width)-var(--left-menu-max-width))] !left-[var(--tab-menu-max-width)+var(--left-menu-max-width)] mt-[var(--logo-height)]":
                                      !Fa.value && Da.value && Ga.value,
                                  },
                                ],
                                style:
                                  "transition: width var(--transition-time-02), left var(--transition-time-02);",
                              },
                              null,
                            )
                          : void 0,
                        x(fl, null, null),
                      ],
                    },
                  ),
                  [[ye("loading"), Na.value]],
                ),
              ],
            ),
          ],
        ),
      ]),
  }),
  { getPrefixCls: Ka } = ue(),
  Qa = Ka("layout"),
  Ya = ve(),
  Ja = u(() => Ya.getMobile),
  Xa = u(() => Ya.getCollapse),
  eo = u(() => Ya.getLayout),
  to = () => {
    Ya.setCollapse(!0);
  },
  lo = () => {
    switch (p(eo)) {
      case "classic":
        const { renderClassic: e } = Za();
        return e();
      case "topLeft":
        const { renderTopLeft: t } = Za();
        return t();
      case "top":
        const { renderTop: l } = Za();
        return l();
      case "cutMenu":
        const { renderCutMenu: a } = Za();
        return a();
    }
  },
  ao = xe(
    r({
      name: "Layout",
      setup: () => () =>
        x(
          "section",
          { class: [Qa, `${Qa}__${eo.value}`, "w-[100%] h-[100%] relative"] },
          [
            Ja.value && !Xa.value
              ? x(
                  "div",
                  {
                    class:
                      "absolute top-0 left-0 w-full h-full opacity-30 z-99 bg-[var(--el-color-black)]",
                    onClick: to,
                  },
                  null,
                )
              : void 0,
            lo(),
            x(Gt, null, null),
          ],
        ),
    }),
    [["__scopeId", "data-v-e270d92a"]],
  );
export { ao as default };
