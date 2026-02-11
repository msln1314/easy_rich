import {
  U as e,
  e as l,
  I as t,
  r as o,
  L as s,
  x as a,
  a1 as i,
  N as r,
  M as p,
  o as n,
  j as d,
  m,
  k as u,
  ai as c,
  z as j,
  l as _,
  F as f,
} from "./index-6b60d190.js";
import { u as g, _ as v } from "./Table.vue_vue_type_script_lang-230d9abb.js";
import { E as b } from "./el-switch-5507f2ea.js";
import { _ as h } from "./Search.vue_vue_type_script_setup_true_lang-9c85421f.js";
import { _ as w } from "./ContentWrap.vue_vue_type_script_setup_true_lang-067de0d9.js";
import { _ as y } from "./Detail.vue_vue_type_script_setup_true_lang-a80f137f.js";
import { _ as x } from "./Dialog.vue_vue_type_style_index_0_lang-d732453c.js";
import { s as S } from "./dict-4a6e55e6.js";
import { u as k } from "./dict-2254259d.js";
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
import "./Descriptions-889cd6fb.js";
import "./el-descriptions-item-68636e02.js";
/* empty css              */ import "./use-dialog-0e1ee265.js";
import "./dict-593a5a5e.js";
const P = l({
  name: "SystemRecordLogin",
  __name: "Login",
  setup(l) {
    const { t: P } = t(),
      z = o([]),
      D = o([]);
    (async () => {
      const e = k(),
        l = await e.getDictObj(["sys_platform", "sys_login_method"]);
      ((z.value = l.sys_platform), (D.value = l.sys_login_method));
    })();
    const {
        tableRegister: R,
        tableState: I,
        tableMethods: L,
      } = g({
        fetchDataApi: async () => {
          const { pageSize: l, currentPage: t } = I,
            o = await ((s = { page: u(t), limit: u(l), ...u(V) }),
            e.get({ url: "/logs/logins", params: s }));
          var s;
          return { list: o.data || [], total: o.count || 0 };
        },
      }),
      { dataList: C, loading: U, total: A, pageSize: q, currentPage: E } = I,
      { getList: F } = L,
      M = s([
        { field: "id", label: "编号", show: !0, disabled: !0, width: "120px" },
        {
          field: "phone",
          label: "手机号",
          width: "150px",
          show: !0,
          disabled: !0,
          sortable: "custom",
        },
        {
          field: "status",
          label: "登录状态",
          show: !0,
          slots: {
            default: (e) =>
              a(i, null, [
                a(
                  b,
                  { value: e.row.status, size: "small", disabled: !0 },
                  null,
                ),
              ]),
          },
        },
        {
          field: "platform",
          label: "登录平台",
          width: "150px",
          show: !0,
          slots: {
            default: (e) =>
              a(i, null, [a("div", null, [S(z.value, e.row.platform)])]),
          },
        },
        {
          field: "login_method",
          label: "认证方式",
          width: "150px",
          show: !0,
          slots: {
            default: (e) =>
              a(i, null, [a("div", null, [S(D.value, e.row.login_method)])]),
          },
        },
        {
          field: "ip",
          label: "登录地址",
          show: !0,
          disabled: !0,
          width: "150px",
          sortable: "custom",
        },
        { field: "address", label: "登录地点", show: !0 },
        { field: "postal_code", label: "邮政编码", show: !1 },
        { field: "area_code", label: "地区区号", show: !1 },
        { field: "browser", label: "浏览器", show: !0 },
        { field: "system", label: "操作系统", show: !0 },
        { field: "response", label: "响应信息", show: !1, disabled: !0 },
        { field: "request", label: "请求信息", show: !1, disabled: !0 },
        {
          field: "created_at",
          label: "创建时间",
          show: !0,
          sortable: "custom",
        },
        {
          field: "action",
          label: "操作",
          show: !0,
          width: 100,
          slots: {
            default: (e) => {
              const l = e.row;
              return a(i, null, [
                a(
                  r,
                  { type: "primary", link: !0, onClick: () => J(l, "detail") },
                  { default: () => [p("详情")] },
                ),
              ]);
            },
          },
        },
      ]),
      N = s([
        {
          field: "telephone",
          label: "手机号",
          component: "Input",
          componentProps: { clearable: !1, style: { width: "214px" } },
        },
        {
          field: "platform",
          label: "登录平台",
          component: "Select",
          componentProps: { style: { width: "214px" }, options: z.value },
        },
        {
          field: "ip",
          label: "登录地址",
          component: "Input",
          componentProps: { clearable: !1, style: { width: "214px" } },
        },
        {
          field: "address",
          label: "登录地点",
          component: "Input",
          componentProps: { clearable: !1, style: { width: "214px" } },
        },
        {
          field: "status",
          label: "登录状态",
          component: "Select",
          componentProps: {
            style: { width: "214px" },
            options: [
              { label: "登录成功", value: !0 },
              { label: "登录失败", value: !1 },
            ],
          },
        },
      ]),
      V = o({ order: "desc", prop: "id" }),
      O = (e) => {
        ((E.value = 1), (V.value = e), F());
      },
      T = o(!1),
      W = o(""),
      B = o(),
      G = o(""),
      H = (e) => {
        ("descending" === e.order
          ? ((V.value.order = "desc"), (V.value.prop = e.prop))
          : ((V.value.order = "asc"), (V.value.prop = e.prop)),
          F());
      },
      J = (e, l) => {
        ((W.value = P("exampleDemo.detail")),
          (G.value = l),
          (B.value = e),
          (T.value = !0));
      };
    return (e, l) => (
      n(),
      d(
        i,
        null,
        [
          a(u(w), null, {
            default: m(() => [
              a(u(h), { schema: N, onReset: O, onSearch: O }, null, 8, [
                "schema",
              ]),
              a(
                u(v),
                {
                  "current-page": u(E),
                  "onUpdate:currentPage":
                    l[0] || (l[0] = (e) => (c(E) ? (E.value = e) : null)),
                  "page-size": u(q),
                  "onUpdate:pageSize":
                    l[1] || (l[1] = (e) => (c(q) ? (q.value = e) : null)),
                  onSortChange: H,
                  showAction: "",
                  columns: M,
                  "node-key": "id",
                  data: u(C),
                  loading: u(U),
                  pagination: { total: u(A) },
                  onRegister: u(R),
                  onRefresh: u(F),
                },
                null,
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
          a(
            u(x),
            {
              modelValue: T.value,
              "onUpdate:modelValue": l[3] || (l[3] = (e) => (T.value = e)),
              title: W.value,
              width: "800px",
            },
            {
              footer: m(() => [
                a(
                  u(r),
                  { onClick: l[2] || (l[2] = (e) => (T.value = !1)) },
                  {
                    default: m(() => [p(j(u(P)("dialogDemo.close")), 1)]),
                    _: 1,
                  },
                ),
              ]),
              default: m(() => [
                "detail" === G.value
                  ? (n(),
                    _(y, { key: 0, "current-row": B.value }, null, 8, [
                      "current-row",
                    ]))
                  : f("", !0),
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
  },
});
export { P as default };
