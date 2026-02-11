import {
  e,
  I as l,
  r as a,
  L as t,
  x as s,
  al as i,
  a1 as o,
  a0 as r,
  Z as u,
  N as n,
  M as d,
  o as p,
  j as m,
  m as c,
  k as v,
  l as j,
  z as f,
  F as _,
  dz as w,
  dA as y,
  dB as h,
  dC as g,
} from "./index-6b60d190.js";
import { u as b, _ as x } from "./Table.vue_vue_type_script_lang-230d9abb.js";
import { E as k } from "./el-switch-5507f2ea.js";
import { a as C, E as z } from "./el-col-b8aa0d1a.js";
import { _ as A } from "./ContentWrap.vue_vue_type_script_setup_true_lang-067de0d9.js";
import { _ as D } from "./Write.vue_vue_type_script_setup_true_lang-f05dbf10.js";
import { _ as R } from "./Dialog.vue_vue_type_style_index_0_lang-d732453c.js";
import { u as M } from "./dict-2254259d.js";
import { s as P } from "./dict-4a6e55e6.js";
import "./el-message-box-2d28828b.js";
import "./el-input-38d674e5.js";
import "./event-5568c9d8.js";
import "./isNil-1f22f7b0.js";
import "./el-overlay-2c5c0104.js";
import "./scroll-6dba6951.js";
import "./vnode-34f6d346.js";
import "./useForm-b6ceb895.js";
import "./el-form-item-ce18addb.js";
import "./el-tooltip-4ed993c7.js";
import "./el-popper-09548d54.js";
import "./focus-trap-275966d8.js";
/* empty css               */ import "./el-checkbox-4903f610.js";
import "./isEqual-b8d86c27.js";
/* empty css                          */ import "./el-date-picker-91f17f23.js";
import "./debounce-5c500a3d.js";
import "./index-fdfa028a.js";
import "./el-radio-group-0c46635e.js";
import "./el-select-8805ff65.js";
import "./index-b7c1540b.js";
import "./strings-00317668.js";
import "./validator-f032316f.js";
import "./el-divider-2dd0a1ee.js";
import "./el-tree-84af12f2.js";
import "./index-55fef7b1.js";
import "./el-progress-31e0b945.js";
import "./style.css_vue_type_style_index_0_src_true_lang-d8fdefc2.js";
import "./index-62254dd8.js";
import "./el-table-column-0bcf5917.js";
import "./el-pagination-491dd0e9.js";
import "./dropdown-84a04b2c.js";
import "./el-image-viewer-5060851c.js";
import "./el-dropdown-item-943c2eb7.js";
import "./refs-64421a9c.js";
/* empty css                   */ import "./_Uint8Array-f98e6540.js";
import "./el-card-37d6f3c4.js";
import "./useValidator-63200dcb.js";
import "./el-tab-pane-1bfe2fef.js";
import "./use-dialog-0e1ee265.js";
import "./dict-593a5a5e.js";
const L = e({
  name: "AuthMenu",
  __name: "Menu",
  setup(e) {
    const { t: L } = l(),
      {
        tableRegister: S,
        tableState: E,
        tableMethods: V,
      } = b({
        fetchDataApi: async () => {
          const { pageSize: e, currentPage: l } = E,
            a = await w({ page: v(l), limit: v(e) });
          return { list: a.data || [], total: a.count || 0 };
        },
        fetchDelApi: async (e) => 200 === (await y(e)).code,
      }),
      { dataList: F, loading: N } = E,
      { getList: q, delList: B } = V;
    let I = a([]);
    (async () => {
      const e = M(),
        l = await e.getDictObj(["sys_menu_type"]);
      I.value = l.sys_menu_type;
    })();
    const O = t([
        {
          field: "menu_name",
          label: "菜单名称",
          width: "200px",
          disabled: !0,
          show: !0,
        },
        {
          field: "icon",
          label: "图标",
          width: "120px",
          show: !1,
          slots: {
            default: (e) => {
              const l = e.row;
              return s(o, null, [l.icon ? s(i, { icon: l.icon }, null) : ""]);
            },
          },
        },
        { field: "order", label: "排序", width: "120px", show: !0 },
        {
          field: "menu_type",
          label: "菜单类型",
          width: "120px",
          show: !0,
          slots: {
            default: (e) => {
              const l = e.row;
              return s(o, null, [s("span", null, [P(I.value, l.menu_type)])]);
            },
          },
        },
        { field: "perms", label: "权限标识", width: "150px", show: !0 },
        { field: "path", label: "路由地址", show: !0 },
        { field: "component", label: "组件路径", show: !0 },
        {
          field: "noCache",
          label: "页面缓存",
          width: "120px",
          show: !0,
          slots: {
            default: (e) => {
              const l = e.row;
              return s(o, null, [
                s(k, { value: !l.noCache, disabled: !0 }, null),
              ]);
            },
          },
        },
        {
          field: "hidden",
          label: "显示状态",
          width: "120px",
          show: !0,
          slots: {
            default: (e) => {
              const l = e.row;
              return s(o, null, [
                s(k, { value: !l.hidden, disabled: !0 }, null),
              ]);
            },
          },
        },
        {
          field: "status",
          label: "菜单状态",
          width: "120px",
          show: !0,
          slots: {
            default: (e) => {
              const l = e.row;
              return s(o, null, [
                s(k, { value: l.status, disabled: !0 }, null),
              ]);
            },
          },
        },
        {
          field: "action",
          width: "200px",
          label: "操作",
          show: !0,
          slots: {
            default: (e) => {
              const l = e.row;
              return s(o, null, [
                r(
                  s(
                    n,
                    {
                      type: "primary",
                      link: !0,
                      size: "small",
                      onClick: () => X(l),
                    },
                    { default: () => [d("编辑")] },
                  ),
                  [[u("hasPermi"), ["sys.menu.update"]]],
                ),
                r(
                  s(
                    n,
                    {
                      type: "primary",
                      link: !0,
                      size: "small",
                      onClick: () => $(l),
                    },
                    { default: () => [d("添加子菜单")] },
                  ),
                  [[u("hasPermi"), ["sys.menu.create"]]],
                ),
                r(
                  s(
                    n,
                    {
                      type: "danger",
                      loading: T.value,
                      link: !0,
                      size: "small",
                      onClick: () => U(l),
                    },
                    { default: () => [d("删除")] },
                  ),
                  [[u("hasPermi"), ["sys.menu.delete"]]],
                ),
              ]);
            },
          },
        },
      ]),
      T = a(!1),
      U = async (e) => {
        ((T.value = !0),
          await B(!0, [e.id]).finally(() => {
            T.value = !1;
          }));
      },
      W = a(!1),
      Z = a(""),
      G = a(),
      H = a(void 0),
      J = a(""),
      K = a(),
      Q = a(!1),
      X = (e) => {
        ((Z.value = "编辑"), (J.value = "edit"), (G.value = e), (W.value = !0));
      },
      Y = () => {
        ((Z.value = "新增"),
          (J.value = "add"),
          (G.value = void 0),
          (W.value = !0));
      },
      $ = (e) => {
        ((Z.value = "添加子菜单"),
          (J.value = "addSon"),
          (H.value = e.id),
          (G.value = void 0),
          (W.value = !0));
      },
      ee = async () => {
        const e = v(K),
          l = await (null == e ? void 0 : e.submit());
        if (l) {
          Q.value = !0;
          try {
            const e = a({});
            "add" === J.value || "addSon" === J.value
              ? ((e.value = await h(l)),
                e.value && ((H.value = void 0), await q(), (W.value = !1)))
              : "edit" === J.value &&
                ((e.value = await g(l)),
                e.value && (await q(), (W.value = !1)));
          } finally {
            Q.value = !1;
          }
        }
      };
    return (e, l) => {
      const a = u("hasPermi");
      return (
        p(),
        m(
          o,
          null,
          [
            s(v(A), null, {
              default: c(() => [
                s(
                  v(x),
                  {
                    columns: O,
                    showAction: "",
                    "default-expand-all": "",
                    "node-key": "id",
                    data: v(F),
                    loading: v(N),
                    onRegister: v(S),
                    onRefresh: v(q),
                  },
                  {
                    toolbar: c(() => [
                      s(
                        v(C),
                        { gutter: 10 },
                        {
                          default: c(() => [
                            s(
                              v(z),
                              { span: 1.5 },
                              {
                                default: c(() => [
                                  r(
                                    (p(),
                                    j(
                                      v(n),
                                      { type: "primary", onClick: Y },
                                      {
                                        default: c(() => [d("新增菜单")]),
                                        _: 1,
                                      },
                                    )),
                                    [[a, ["sys.menu.create"]]],
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
                  ["columns", "data", "loading", "onRegister", "onRefresh"],
                ),
              ]),
              _: 1,
            }),
            s(
              v(R),
              {
                modelValue: W.value,
                "onUpdate:modelValue": l[1] || (l[1] = (e) => (W.value = e)),
                title: Z.value,
              },
              {
                footer: c(() => [
                  "detail" !== J.value
                    ? (p(),
                      j(
                        v(n),
                        {
                          key: 0,
                          type: "primary",
                          loading: Q.value,
                          onClick: ee,
                        },
                        {
                          default: c(() => [d(f(v(L)("exampleDemo.save")), 1)]),
                          _: 1,
                        },
                        8,
                        ["loading"],
                      ))
                    : _("", !0),
                  s(
                    v(n),
                    { onClick: l[0] || (l[0] = (e) => (W.value = !1)) },
                    {
                      default: c(() => [d(f(v(L)("dialogDemo.close")), 1)]),
                      _: 1,
                    },
                  ),
                ]),
                default: c(() => [
                  s(
                    D,
                    {
                      ref_key: "writeRef",
                      ref: K,
                      "current-row": G.value,
                      "parent-id": H.value,
                    },
                    null,
                    8,
                    ["current-row", "parent-id"],
                  ),
                ]),
                _: 1,
              },
              8,
              ["modelValue", "title"],
            ),
          ],
          64,
        )
      );
    };
  },
});
export { L as default };
