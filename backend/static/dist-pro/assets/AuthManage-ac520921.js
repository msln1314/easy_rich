import {
  e,
  aE as a,
  u as s,
  f as t,
  o as l,
  j as r,
  q as o,
  s as n,
  k as i,
  _ as u,
  n as d,
  t as c,
  a8 as p,
  r as m,
  w as v,
  x as f,
  m as h,
  y,
  al as g,
  z as _,
  N as b,
  M as k,
  a1 as w,
  a5 as j,
  l as x,
  F as E,
  da as C,
  af as R,
  Q as V,
  R as K,
  as as N,
  dG as S,
  J as z,
} from "./index-6b60d190.js";
import { E as F } from "./el-drawer-64f23d0f.js";
import "./el-overlay-2c5c0104.js";
import { E as O } from "./el-divider-2dd0a1ee.js";
import "./el-input-38d674e5.js";
/* empty css               */ import {
  E as $,
  a as A,
} from "./el-select-8805ff65.js";
import "./el-popper-09548d54.js";
import { E as B } from "./el-tree-84af12f2.js";
import "./el-checkbox-4903f610.js";
import { u as H } from "./dict-2254259d.js";
import { c as J } from "./dept-7c279e0e.js";
import { e as M } from "./tree-ae7cba8b.js";
import { p as q } from "./role-af5fad9c.js";
import "./use-dialog-0e1ee265.js";
import "./event-5568c9d8.js";
import "./focus-trap-275966d8.js";
import "./isNil-1f22f7b0.js";
import "./scroll-6dba6951.js";
import "./vnode-34f6d346.js";
import "./index-b7c1540b.js";
import "./strings-00317668.js";
import "./isEqual-b8d86c27.js";
import "./debounce-5c500a3d.js";
import "./index-fdfa028a.js";
import "./validator-f032316f.js";
import "./index-55fef7b1.js";
import "./dict-593a5a5e.js";
const G = e({ name: "ElContainer" });
var L = u(
  e({
    ...G,
    props: { direction: { type: String } },
    setup(e) {
      const u = e,
        d = a(),
        c = s("container"),
        p = t(() => {
          if ("vertical" === u.direction) return !0;
          if ("horizontal" === u.direction) return !1;
          if (d && d.default) {
            return d.default().some((e) => {
              const a = e.type.name;
              return "ElHeader" === a || "ElFooter" === a;
            });
          }
          return !1;
        });
      return (e, a) => (
        l(),
        r(
          "section",
          { class: n([i(c).b(), i(c).is("vertical", i(p))]) },
          [o(e.$slots, "default")],
          2,
        )
      );
    },
  }),
  [
    [
      "__file",
      "/home/runner/work/element-plus/element-plus/packages/components/container/src/container.vue",
    ],
  ],
);
const T = e({ name: "ElAside" });
var D = u(
  e({
    ...T,
    props: { width: { type: String, default: null } },
    setup(e) {
      const a = e,
        u = s("aside"),
        c = t(() => (a.width ? u.cssVarBlock({ width: a.width }) : {}));
      return (e, a) => (
        l(),
        r(
          "aside",
          { class: n(i(u).b()), style: d(i(c)) },
          [o(e.$slots, "default")],
          6,
        )
      );
    },
  }),
  [
    [
      "__file",
      "/home/runner/work/element-plus/element-plus/packages/components/container/src/aside.vue",
    ],
  ],
);
const I = e({ name: "ElFooter" });
var P = u(
  e({
    ...I,
    props: { height: { type: String, default: null } },
    setup(e) {
      const a = e,
        u = s("footer"),
        c = t(() => (a.height ? u.cssVarBlock({ height: a.height }) : {}));
      return (e, a) => (
        l(),
        r(
          "footer",
          { class: n(i(u).b()), style: d(i(c)) },
          [o(e.$slots, "default")],
          6,
        )
      );
    },
  }),
  [
    [
      "__file",
      "/home/runner/work/element-plus/element-plus/packages/components/container/src/footer.vue",
    ],
  ],
);
const Q = e({ name: "ElHeader" });
var U = u(
  e({
    ...Q,
    props: { height: { type: String, default: null } },
    setup(e) {
      const a = e,
        u = s("header"),
        c = t(() => (a.height ? u.cssVarBlock({ height: a.height }) : {}));
      return (e, a) => (
        l(),
        r(
          "header",
          { class: n(i(u).b()), style: d(i(c)) },
          [o(e.$slots, "default")],
          6,
        )
      );
    },
  }),
  [
    [
      "__file",
      "/home/runner/work/element-plus/element-plus/packages/components/container/src/header.vue",
    ],
  ],
);
const W = e({ name: "ElMain" });
var X = u(
  e({
    ...W,
    setup(e) {
      const a = s("main");
      return (e, s) => (
        l(),
        r("main", { class: n(i(a).b()) }, [o(e.$slots, "default")], 2)
      );
    },
  }),
  [
    [
      "__file",
      "/home/runner/work/element-plus/element-plus/packages/components/container/src/main.vue",
    ],
  ],
);
const Y = c(L, { Aside: D, Footer: P, Header: U, Main: X }),
  Z = p(D);
p(P);
const ee = p(U),
  ae = p(X),
  se = (e) => (V("data-v-159700c0"), (e = e()), K(), e),
  te = { class: "auth-manage-main-view" },
  le = { class: "flex justify-between pt-[20px] pb-[20px]" },
  re = se(() => y("span", null, "权限管理", -1)),
  oe = { class: "h-12 flex justify-between mt-3 mr-3 ml-5" },
  ne = { class: "mt-1 text-[#909399]" },
  ie = {
    class:
      "border-r-1 border-r-[#f0f0f0] b-r-solid h-[100%] p-[20px] box-border",
  },
  ue = se(() =>
    y(
      "div",
      { class: "flex items-center" },
      [y("div", { class: "yxt-divider" }), y("span", null, "数据权限")],
      -1,
    ),
  ),
  de = { class: "ml-4 mt-3" },
  ce = {
    key: 0,
    class: "mt-3 max-h-[65vh] b-1 b-solid b-[#e5e7eb] p-10px overflow-auto",
  },
  pe = se(() =>
    y(
      "div",
      { class: "flex items-center" },
      [y("div", { class: "yxt-divider" }), y("span", null, "菜单权限")],
      -1,
    ),
  ),
  me = {
    class:
      "mt-5 max-h-[70vh] b-1 b-solid b-[#e5e7eb] p-10px overflow-auto box-border",
  },
  ve = z(
    e({
      __name: "AuthManage",
      props: { currentRow: { type: Object, default: () => null } },
      emits: ["getList"],
      setup(e, { expose: a, emit: s }) {
        const t = e,
          o = m({});
        v(
          () => t.currentRow,
          (e) => {
            e && (o.value = JSON.parse(JSON.stringify(e)));
          },
          { deep: !0, immediate: !0 },
        );
        const n = m(!1),
          u = m(),
          d = { children: "children", label: "label" };
        let c = m([]);
        const p = m();
        let V = m([]);
        const K = m(),
          z = m(!1),
          G = async () => {
            var e, a, t;
            if (z.value) return;
            if (C(o.value.data_range))
              return void R.error("数据范围选择项不能为空！");
            z.value = !0;
            const l = [
              ...((null == (e = i(K)) ? void 0 : e.getCheckedKeys()) || []),
              ...((null == (a = i(K)) ? void 0 : a.getHalfCheckedKeys()) || []),
            ];
            ((o.value.menu_ids = l),
              (o.value.dept_ids =
                null == (t = i(p)) ? void 0 : t.getCheckedKeys()));
            try {
              (await q(o.value)) &&
                ((z.value = !1), R.success("保存成功"), L(), s("getList"));
            } finally {
              z.value = !1;
            }
          },
          L = () => {
            var e, a;
            ((n.value = !1),
              (o.value = {}),
              null == (e = i(K)) || e.setCheckedKeys([]),
              null == (a = i(p)) || a.setCheckedKeys([]));
          };
        return (
          (async () => {
            const e = H(),
              a = await e.getDictObj(["sys_vadmin_data_range"]);
            u.value = a.sys_vadmin_data_range;
          })(),
          a({
            openDrawer: () => {
              ((n.value = !0),
                (async () => {
                  var e;
                  const a = await S();
                  if (a && ((V.value = a.data), await N(), t.currentRow)) {
                    const s = t.currentRow.menus.map((e) => e.id),
                      l = [];
                    M(a.data, (e) => {
                      s.includes(e.value) && l.push(e.value);
                    });
                    for (const a of l)
                      null == (e = i(K)) || e.setChecked(a, !0, !1);
                  }
                })(),
                (async () => {
                  var e;
                  const a = await J();
                  if (a && ((c.value = a.data), await N(), t.currentRow)) {
                    const s = t.currentRow.depts.map((e) => e.id),
                      l = [];
                    M(a.data, (e) => {
                      s.includes(e.value) && l.push(e.value);
                    });
                    for (const a of l)
                      null == (e = i(p)) || e.setChecked(a, !0, !1);
                  }
                })());
            },
          }),
          (e, a) => (
            l(),
            r("div", te, [
              f(
                i(F),
                {
                  modelValue: n.value,
                  "onUpdate:modelValue": a[1] || (a[1] = (e) => (n.value = e)),
                  "with-header": !1,
                  size: 1e3,
                  "before-close": L,
                },
                {
                  default: h(() => [
                    f(i(Y), null, {
                      default: h(() => [
                        f(i(ee), null, {
                          default: h(() => [
                            y("div", le, [
                              re,
                              y(
                                "span",
                                { onClick: L, class: "flex cursor-pointer" },
                                [
                                  f(i(g), {
                                    icon: "iconamoon:close-thin",
                                    size: 23,
                                  }),
                                ],
                              ),
                            ]),
                          ]),
                          _: 1,
                        }),
                        f(i(O)),
                        y("div", oe, [
                          y("div", ne, [
                            y("span", null, "角色名称：" + _(o.value.name), 1),
                          ]),
                          f(
                            i(b),
                            { type: "primary", loading: z.value, onClick: G },
                            { default: h(() => [k("保存")]), _: 1 },
                            8,
                            ["loading"],
                          ),
                        ]),
                        f(i(O)),
                        f(i(Y), null, {
                          default: h(() => [
                            f(
                              i(Z),
                              { width: "450px" },
                              {
                                default: h(() => [
                                  y("div", ie, [
                                    y("div", null, [
                                      ue,
                                      y("div", de, [
                                        f(
                                          i($),
                                          {
                                            modelValue: o.value.data_range,
                                            "onUpdate:modelValue":
                                              a[0] ||
                                              (a[0] = (e) =>
                                                (o.value.data_range = e)),
                                            placeholder: "请选择数据范围",
                                          },
                                          {
                                            default: h(() => [
                                              (l(!0),
                                              r(
                                                w,
                                                null,
                                                j(
                                                  u.value,
                                                  (e) => (
                                                    l(),
                                                    x(
                                                      i(A),
                                                      {
                                                        key: e.value,
                                                        label: e.label,
                                                        value: e.value,
                                                      },
                                                      null,
                                                      8,
                                                      ["label", "value"],
                                                    )
                                                  ),
                                                ),
                                                128,
                                              )),
                                            ]),
                                            _: 1,
                                          },
                                          8,
                                          ["modelValue"],
                                        ),
                                        "4" === o.value.data_range
                                          ? (l(),
                                            r("div", ce, [
                                              f(
                                                i(B),
                                                {
                                                  ref_key: "deptTreeRef",
                                                  ref: p,
                                                  data: i(c),
                                                  "show-checkbox": "",
                                                  "node-key": "value",
                                                  props: d,
                                                  "default-expand-all": !0,
                                                  "check-strictly": !0,
                                                },
                                                null,
                                                8,
                                                ["data"],
                                              ),
                                            ]))
                                          : E("", !0),
                                      ]),
                                    ]),
                                  ]),
                                ]),
                                _: 1,
                              },
                            ),
                            f(i(ae), null, {
                              default: h(() => [
                                pe,
                                y("div", me, [
                                  f(
                                    i(B),
                                    {
                                      ref_key: "menuTreeRef",
                                      ref: K,
                                      data: i(V),
                                      "show-checkbox": "",
                                      "node-key": "value",
                                      props: d,
                                      "default-expand-all": !0,
                                      "check-strictly": !1,
                                    },
                                    null,
                                    8,
                                    ["data"],
                                  ),
                                ]),
                              ]),
                              _: 1,
                            }),
                          ]),
                          _: 1,
                        }),
                      ]),
                      _: 1,
                    }),
                    f(i(O)),
                  ]),
                  _: 1,
                },
                8,
                ["modelValue"],
              ),
            ])
          )
        );
      },
    }),
    [["__scopeId", "data-v-159700c0"]],
  );
export { ve as default };
