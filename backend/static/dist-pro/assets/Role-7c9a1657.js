import {
  e,
  I as a,
  L as l,
  x as t,
  a1 as s,
  a0 as o,
  aH as i,
  Z as r,
  N as n,
  M as p,
  r as u,
  b1 as d,
  o as m,
  j as c,
  m as v,
  k as _,
  ai as j,
  l as f,
  z as g,
  af as y,
} from "./index-6b60d190.js";
import { g as b, a as w, d as h, b as x, p as k } from "./role-af5fad9c.js";
import { u as R, _ as P } from "./Table.vue_vue_type_script_lang-230d9abb.js";
import { E as S } from "./el-switch-5507f2ea.js";
import { _ as z } from "./Search.vue_vue_type_script_setup_true_lang-9c85421f.js";
import { _ as C } from "./ContentWrap.vue_vue_type_script_setup_true_lang-067de0d9.js";
import { _ as A } from "./Write.vue_vue_type_script_setup_true_lang-f974c2ee.js";
import D from "./RoleAssignMenuForm-fc0804ba.js";
import { _ as E } from "./Dialog.vue_vue_type_style_index_0_lang-d732453c.js";
import "./el-message-box-2d28828b.js";
import "./el-input-38d674e5.js";
import "./event-5568c9d8.js";
import "./isNil-1f22f7b0.js";
import "./el-overlay-2c5c0104.js";
import "./scroll-6dba6951.js";
import "./vnode-34f6d346.js";
import "./useForm-b6ceb895.js";
import "./el-form-item-ce18addb.js";
import "./el-col-b8aa0d1a.js";
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
import "./useIcon-7641a992.js";
import "./el-card-37d6f3c4.js";
import "./useValidator-63200dcb.js";
import "./tree-ae7cba8b.js";
import "./use-dialog-0e1ee265.js";
const I = e({
  name: "SysRole",
  __name: "Role",
  setup(e) {
    const { t: I } = a(),
      {
        tableRegister: L,
        tableState: M,
        tableMethods: F,
      } = R({
        fetchDataApi: async () => {
          const { pageSize: e, currentPage: a } = M,
            l = await w({ page: _(a), limit: _(e), ..._(B) });
          return { list: l.data || [], total: l.count || 0 };
        },
        fetchDelApi: async (e) => 200 === (await h(e)).code,
      }),
      { dataList: N, loading: U, total: V, pageSize: W, currentPage: q } = M,
      { getList: H, delList: O } = F,
      Y = l([
        { field: "id", label: "角色编号", show: !1, disabled: !1 },
        { field: "name", label: "角色名称", show: !0, disabled: !0 },
        { field: "code", label: "权限字符", show: !0 },
        { field: "order", label: "显示顺序", show: !0 },
        {
          field: "status",
          label: "角色状态",
          show: !0,
          slots: {
            default: (e) => {
              const a = e.row;
              return t(s, null, [
                t(S, { value: a.status, disabled: !0 }, null),
              ]);
            },
          },
        },
        {
          field: "is_admin",
          label: "最高权限",
          show: !0,
          slots: {
            default: (e) => {
              const a = e.row;
              return t(s, null, [
                t(S, { value: a.is_admin, disabled: !0 }, null),
              ]);
            },
          },
        },
        { field: "created_at", label: "创建时间", show: !0 },
        {
          field: "action",
          width: "170px",
          label: "操作",
          show: !0,
          slots: {
            default: (e) => {
              const a = e.row;
              return t(s, null, [
                o(
                  t(
                    n,
                    {
                      type: "primary",
                      link: !0,
                      size: "small",
                      onClick: () => se(a),
                    },
                    { default: () => [p("编辑")] },
                  ),
                  [
                    [i, 1 !== a.id],
                    [r("hasPermi"), ["sys.role.update"]],
                  ],
                ),
                o(
                  t(
                    n,
                    {
                      type: "primary",
                      link: !0,
                      size: "small",
                      onClick: () => T(a),
                    },
                    { default: () => [p("菜单管理")] },
                  ),
                  [[i, 1 !== a.id]],
                ),
                o(
                  t(
                    n,
                    {
                      type: "danger",
                      loading: J.value,
                      link: !0,
                      size: "small",
                      onClick: () => K(a),
                    },
                    { default: () => [p("删除")] },
                  ),
                  [
                    [i, 1 !== a.id],
                    [r("hasPermi"), ["sys.role.delete"]],
                  ],
                ),
              ]);
            },
          },
        },
      ]),
      Z = l([
        {
          field: "name",
          label: "角色名称",
          component: "Input",
          componentProps: { clearable: !1, style: { width: "214px" } },
        },
        {
          field: "role_key",
          label: "权限字符",
          component: "Input",
          componentProps: { clearable: !1, style: { width: "214px" } },
        },
        {
          field: "disabled",
          label: "状态",
          component: "Select",
          componentProps: {
            style: { width: "214px" },
            options: [
              { label: "正常", value: !1 },
              { label: "停用", value: !0 },
            ],
          },
        },
      ]),
      B = u({}),
      G = (e) => {
        ((q.value = 1), (B.value = e), H());
      },
      J = u(!1),
      K = async (e) => {
        ((J.value = !0),
          await O(!0, [e.id]).finally(() => {
            J.value = !1;
          }));
      },
      Q = u(),
      T = async (e) => {
        Q.value.open(e);
      },
      X = u(!1),
      $ = u(""),
      ee = u(),
      ae = u(""),
      le = u(),
      te = u(!1),
      se = async (e) => {
        const a = await b(e.id);
        a &&
          (($.value = "编辑角色"),
          (ae.value = "edit"),
          (ee.value = a.data),
          (X.value = !0));
      },
      oe = () => {
        (($.value = "新增角色"),
          (ae.value = "add"),
          (ee.value = void 0),
          (X.value = !0));
      },
      ie = async () => {
        const e = _(le),
          a = await (null == e ? void 0 : e.submit());
        if (a) {
          te.value = !0;
          try {
            const e = u({});
            "add" === ae.value
              ? ((e.value = await x(a)),
                e.value && ((X.value = !1), H(), y.success("添加成功!")))
              : "edit" === ae.value &&
                ((e.value = await k(a)),
                e.value && ((X.value = !1), H(), y.success("编辑成功!")));
          } finally {
            te.value = !1;
          }
        }
      };
    return (e, a) => {
      const l = d("ElCol"),
        i = d("ElRow"),
        u = r("hasPermi");
      return (
        m(),
        c(
          s,
          null,
          [
            t(_(C), null, {
              default: v(() => [
                t(_(z), { schema: Z, onReset: G, onSearch: G }, null, 8, [
                  "schema",
                ]),
                t(
                  _(P),
                  {
                    "current-page": _(q),
                    "onUpdate:currentPage":
                      a[0] || (a[0] = (e) => (j(q) ? (q.value = e) : null)),
                    "page-size": _(W),
                    "onUpdate:pageSize":
                      a[1] || (a[1] = (e) => (j(W) ? (W.value = e) : null)),
                    showAction: "",
                    columns: Y,
                    "default-expand-all": "",
                    "node-key": "id",
                    data: _(N),
                    loading: _(U),
                    pagination: { total: _(V) },
                    onRegister: _(L),
                    onRefresh: _(H),
                  },
                  {
                    toolbar: v(() => [
                      t(
                        i,
                        { gutter: 10 },
                        {
                          default: v(() => [
                            t(
                              l,
                              { span: 1.5 },
                              {
                                default: v(() => [
                                  o(
                                    (m(),
                                    f(
                                      _(n),
                                      { type: "primary", onClick: oe },
                                      {
                                        default: v(() => [p("新增角色")]),
                                        _: 1,
                                      },
                                    )),
                                    [[u, ["sys.role.create"]]],
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
                  [
                    "current-page",
                    "page-size",
                    "columns",
                    "data",
                    "loading",
                    "pagination",
                    "onRegister",
                    "onRefresh",
                  ],
                ),
              ]),
              _: 1,
            }),
            t(
              _(E),
              {
                modelValue: X.value,
                "onUpdate:modelValue": a[3] || (a[3] = (e) => (X.value = e)),
                title: $.value,
                height: 650,
              },
              {
                footer: v(() => [
                  t(
                    _(n),
                    { type: "primary", loading: te.value, onClick: ie },
                    {
                      default: v(() => [p(g(_(I)("exampleDemo.save")), 1)]),
                      _: 1,
                    },
                    8,
                    ["loading"],
                  ),
                  t(
                    _(n),
                    { onClick: a[2] || (a[2] = (e) => (X.value = !1)) },
                    {
                      default: v(() => [p(g(_(I)("dialogDemo.close")), 1)]),
                      _: 1,
                    },
                  ),
                ]),
                default: v(() => [
                  t(
                    A,
                    { ref_key: "writeRef", ref: le, "current-row": ee.value },
                    null,
                    8,
                    ["current-row"],
                  ),
                ]),
                _: 1,
              },
              8,
              ["modelValue", "title"],
            ),
            t(
              D,
              { ref_key: "assignMenuFormRef", ref: Q, onSuccess: _(H) },
              null,
              8,
              ["onSuccess"],
            ),
          ],
          64,
        )
      );
    };
  },
});
export { I as default };
