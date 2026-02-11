import {
  U as e,
  e as t,
  I as o,
  L as l,
  x as s,
  N as a,
  M as i,
  a1 as r,
  r as p,
  o as n,
  j as d,
  m,
  k as u,
  ai as c,
  z as _,
  l as j,
  F as h,
} from "./index-6b60d190.js";
import { u as b, _ as g } from "./Table.vue_vue_type_script_lang-230d9abb.js";
import { _ as f } from "./Search.vue_vue_type_script_setup_true_lang-9c85421f.js";
import { _ as w } from "./ContentWrap.vue_vue_type_script_setup_true_lang-067de0d9.js";
import { _ as v } from "./Detail.vue_vue_type_script_setup_true_lang-d485643d.js";
import { _ as x } from "./Dialog.vue_vue_type_style_index_0_lang-d732453c.js";
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
import "./el-switch-5507f2ea.js";
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
import "./use-dialog-0e1ee265.js";
const y = t({
  name: "SystemRecordOperation",
  __name: "Operation",
  setup(t) {
    const { t: y } = o(),
      {
        tableRegister: k,
        tableState: R,
        tableMethods: S,
      } = b({
        fetchDataApi: async () => {
          const { pageSize: t, currentPage: o } = R,
            l = await ((s = { page: u(o), limit: u(t), ...u(L) }),
            e.get({ url: "/logs/operations", params: s }));
          var s;
          return { list: l.data || [], total: l.count || 0 };
        },
      }),
      { dataList: z, loading: D, total: P, pageSize: I, currentPage: C } = R,
      { getList: U } = S,
      q = l([
        {
          field: "user_id",
          label: "操作人编号",
          show: !0,
          disabled: !0,
          width: "100px",
        },
        {
          field: "user_name",
          label: "操作人",
          show: !0,
          disabled: !0,
          width: "100px",
          sortable: "custom",
        },
        {
          field: "phone",
          label: "手机号",
          show: !0,
          disabled: !0,
          width: "130px",
          sortable: "custom",
        },
        {
          field: "request_method",
          label: "请求方法",
          show: !0,
          disabled: !0,
          width: "100px",
        },
        {
          field: "client_ip",
          label: "客户端地址",
          width: "130px",
          show: !0,
          disabled: !0,
        },
        { field: "tags", label: "标签", width: "130px", show: !0 },
        { field: "summary", label: "操作内容", show: !0 },
        { field: "description", label: "描述", show: !1 },
        {
          field: "status_code",
          label: "操作状态",
          show: !0,
          width: "100px",
          sortable: "custom",
        },
        { field: "route_name", label: "接口函数", show: !1, width: "150px" },
        { field: "api_path", label: "接口地址", show: !1 },
        { field: "params", label: "请求参数", show: !1 },
        { field: "browser", label: "浏览器", show: !0, width: "150px" },
        { field: "system", label: "系统", show: !1, width: "150px" },
        {
          field: "process_time",
          label: "总耗时",
          show: !0,
          sortable: "custom",
        },
        {
          field: "created_at",
          label: "操作时间",
          show: !0,
          sortable: "custom",
        },
        {
          field: "action",
          width: "100px",
          show: !0,
          label: "操作",
          slots: {
            default: (e) => {
              const t = e.row;
              return s(r, null, [
                s(
                  a,
                  { type: "primary", link: !0, onClick: () => W(t, "detail") },
                  { default: () => [i("详情")] },
                ),
              ]);
            },
          },
        },
      ]),
      A = l([
        {
          field: "telephone",
          label: "手机号",
          component: "Input",
          componentProps: { clearable: !1 },
        },
        {
          field: "request_method",
          label: "请求方法",
          component: "Input",
          componentProps: { clearable: !1 },
        },
        {
          field: "summary",
          label: "操作内容",
          component: "Input",
          componentProps: { clearable: !1 },
        },
      ]),
      L = p({ order: "desc", prop: "id" }),
      F = (e) => {
        ((C.value = 1), (L.value = e), U());
      },
      M = (e) => {
        ("descending" === e.order
          ? ((L.value.order = "desc"), (L.value.prop = e.prop))
          : ((L.value.order = "asc"), (L.value.prop = e.prop)),
          U());
      },
      N = p(!1),
      O = p(""),
      V = p(),
      E = p(""),
      W = (e, t) => {
        ((O.value = y("exampleDemo.detail")),
          (E.value = t),
          (V.value = e),
          (N.value = !0));
      };
    return (e, t) => (
      n(),
      d(
        r,
        null,
        [
          s(u(w), null, {
            default: m(() => [
              s(u(f), { schema: A, onReset: F, onSearch: F }, null, 8, [
                "schema",
              ]),
              s(
                u(g),
                {
                  "current-page": u(C),
                  "onUpdate:currentPage":
                    t[0] || (t[0] = (e) => (c(C) ? (C.value = e) : null)),
                  "page-size": u(I),
                  "onUpdate:pageSize":
                    t[1] || (t[1] = (e) => (c(I) ? (I.value = e) : null)),
                  onSortChange: M,
                  showAction: "",
                  columns: q,
                  "node-key": "id",
                  data: u(z),
                  loading: u(D),
                  pagination: { total: u(P) },
                  onRegister: u(k),
                  onRefresh: u(U),
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
          s(
            u(x),
            {
              modelValue: N.value,
              "onUpdate:modelValue": t[3] || (t[3] = (e) => (N.value = e)),
              title: O.value,
              width: "800px",
            },
            {
              footer: m(() => [
                s(
                  u(a),
                  { onClick: t[2] || (t[2] = (e) => (N.value = !1)) },
                  {
                    default: m(() => [i(_(u(y)("dialogDemo.close")), 1)]),
                    _: 1,
                  },
                ),
              ]),
              default: m(() => [
                "detail" === E.value
                  ? (n(),
                    j(v, { key: 0, "current-row": V.value }, null, 8, [
                      "current-row",
                    ]))
                  : h("", !0),
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
export { y as default };
