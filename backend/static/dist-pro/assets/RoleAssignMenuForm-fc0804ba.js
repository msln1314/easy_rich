import { d as e } from "./tree-ae7cba8b.js";
import { g as a, p as l } from "./role-af5fad9c.js";
import {
  e as s,
  r as t,
  Z as o,
  o as u,
  l as i,
  m as r,
  x as d,
  k as m,
  N as n,
  M as v,
  a0 as p,
  z as f,
  dG as c,
  as as _,
  af as j,
  J as x,
} from "./index-6b60d190.js";
import { E as y } from "./el-switch-5507f2ea.js";
/* empty css               */ import {
  E as g,
  a as h,
} from "./el-form-item-ce18addb.js";
import { E as k } from "./el-tree-84af12f2.js";
import "./el-checkbox-4903f610.js";
import { E as b } from "./el-card-37d6f3c4.js";
import { _ as C } from "./Dialog.vue_vue_type_style_index_0_lang-d732453c.js";
import { E as V } from "./index-b7c1540b.js";
import "./validator-f032316f.js";
import "./event-5568c9d8.js";
import "./index-55fef7b1.js";
import "./isEqual-b8d86c27.js";
import "./el-overlay-2c5c0104.js";
import "./scroll-6dba6951.js";
import "./vnode-34f6d346.js";
import "./use-dialog-0e1ee265.js";
import "./focus-trap-275966d8.js";
import "./isNil-1f22f7b0.js";
import "./refs-64421a9c.js";
import "./index-62254dd8.js";
const w = x(
  s({
    name: "SystemRoleAssignMenuForm",
    __name: "RoleAssignMenuForm",
    emits: ["success"],
    setup(s, { expose: x, emit: w }) {
      const E = t(!1),
        M = t(!1),
        N = t({}),
        R = t(),
        A = t([]),
        K = t(!1),
        U = t(),
        F = t(!1);
      x({
        open: async (e) => {
          const { data: l } = await a(e.id);
          E.value = !0;
          const s = await c();
          if (s) {
            ((A.value = s.data), (N.value = l), (M.value = !0), await _());
            try {
              const e = l.menus.map((e) => e.id);
              ((N.value.menu_ids = e),
                N.value.menu_ids.forEach((e) => {
                  U.value.setChecked(e, !0, !1);
                }));
            } finally {
              M.value = !1;
            }
          }
        },
      });
      const H = async () => {
          if (!R.value) return;
          if (await R.value.validate()) {
            M.value = !0;
            try {
              const e = [
                ...U.value.getCheckedKeys(!1),
                ...U.value.getHalfCheckedKeys(),
              ];
              ((N.value.menu_ids = e),
                await l(N.value),
                j.success("保存成功!"),
                (E.value = !1),
                w("success"));
            } finally {
              M.value = !1;
            }
          }
        },
        J = () => {
          U.value.setCheckedNodes(F.value ? A.value : []);
        },
        P = () => {
          var e;
          const a = null == (e = U.value) ? void 0 : e.store.nodesMap;
          for (let l in a)
            a[l].expanded !== K.value && (a[l].expanded = K.value);
        };
      return (a, l) => {
        const s = o("loading");
        return (
          u(),
          i(
            m(C),
            {
              modelValue: E.value,
              "onUpdate:modelValue": l[3] || (l[3] = (e) => (E.value = e)),
              title: "菜单权限",
            },
            {
              footer: r(() => [
                d(
                  m(n),
                  { disabled: M.value, type: "primary", onClick: H },
                  { default: r(() => [v("确 定")]), _: 1 },
                  8,
                  ["disabled"],
                ),
                d(
                  m(n),
                  { onClick: l[2] || (l[2] = (e) => (E.value = !1)) },
                  { default: r(() => [v("取 消")]), _: 1 },
                ),
              ]),
              default: r(() => [
                p(
                  (u(),
                  i(
                    m(g),
                    {
                      ref_key: "formRef",
                      ref: R,
                      model: N.value,
                      "label-width": "80px",
                    },
                    {
                      default: r(() => [
                        d(
                          m(h),
                          { label: "角色名称" },
                          {
                            default: r(() => [
                              d(m(V), null, {
                                default: r(() => [v(f(N.value.name), 1)]),
                                _: 1,
                              }),
                            ]),
                            _: 1,
                          },
                        ),
                        d(
                          m(h),
                          { label: "角色标识" },
                          {
                            default: r(() => [
                              d(m(V), null, {
                                default: r(() => [v(f(N.value.code), 1)]),
                                _: 1,
                              }),
                            ]),
                            _: 1,
                          },
                        ),
                        d(
                          m(h),
                          { label: "菜单权限" },
                          {
                            default: r(() => [
                              d(
                                m(b),
                                { class: "cardHeight" },
                                {
                                  header: r(() => [
                                    v(" 全选/全不选: "),
                                    d(
                                      m(y),
                                      {
                                        modelValue: F.value,
                                        "onUpdate:modelValue":
                                          l[0] || (l[0] = (e) => (F.value = e)),
                                        "active-text": "是",
                                        "inactive-text": "否",
                                        "inline-prompt": "",
                                        onChange: J,
                                      },
                                      null,
                                      8,
                                      ["modelValue"],
                                    ),
                                    v(" 全部展开/折叠: "),
                                    d(
                                      m(y),
                                      {
                                        modelValue: K.value,
                                        "onUpdate:modelValue":
                                          l[1] || (l[1] = (e) => (K.value = e)),
                                        "active-text": "展开",
                                        "inactive-text": "折叠",
                                        "inline-prompt": "",
                                        onChange: P,
                                      },
                                      null,
                                      8,
                                      ["modelValue"],
                                    ),
                                  ]),
                                  default: r(() => [
                                    d(
                                      m(k),
                                      {
                                        ref_key: "treeRef",
                                        ref: U,
                                        data: A.value,
                                        props: m(e),
                                        "empty-text": "加载中，请稍候",
                                        "node-key": "value",
                                        "show-checkbox": "",
                                      },
                                      null,
                                      8,
                                      ["data", "props"],
                                    ),
                                  ]),
                                  _: 1,
                                },
                              ),
                            ]),
                            _: 1,
                          },
                        ),
                      ]),
                      _: 1,
                    },
                    8,
                    ["model"],
                  )),
                  [[s, M.value]],
                ),
              ]),
              _: 1,
            },
            8,
            ["modelValue"],
          )
        );
      };
    },
  }),
  [["__scopeId", "data-v-ee17db22"]],
);
export { w as default };
