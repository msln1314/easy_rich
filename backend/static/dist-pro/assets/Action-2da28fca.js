import {
  U as e,
  e as t,
  I as o,
  L as s,
  x as l,
  a1 as a,
  N as i,
  M as r,
  r as p,
  o as n,
  j as d,
  m,
  k as u,
  ai as c,
  z as j,
  l as _,
  F as g,
} from "./index-6b60d190.js";
import { u as v, _ as h } from "./Table.vue_vue_type_script_lang-230d9abb.js";
import { _ as f } from "./Search.vue_vue_type_script_setup_true_lang-9c85421f.js";
import { _ as w } from "./ContentWrap.vue_vue_type_script_setup_true_lang-067de0d9.js";
import { _ as b } from "./Detail.vue_vue_type_script_setup_true_lang-a8aea609.js";
import { _ as x } from "./Dialog.vue_vue_type_style_index_0_lang-d732453c.js";
import { _ as y } from "./DictTag.vue_vue_type_script_lang-5f3c338f.js";
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
import "./dict-2254259d.js";
import "./dict-593a5a5e.js";
const k = t({
  name: "SystemLogAction",
  __name: "Action",
  setup(t) {
    const { t: k } = o(),
      {
        tableRegister: S,
        tableState: D,
        tableMethods: z,
      } = v({
        fetchDataApi: async () => {
          const { pageSize: t, currentPage: o } = D,
            s = await ((l = { page: u(o), limit: u(t), ...u(T) }),
            e.get({ url: "/logs/actions", params: l }));
          var l;
          return { list: s.data || [], total: s.count || 0 };
        },
      }),
      { dataList: R, loading: A, total: P, pageSize: C, currentPage: I } = D,
      { getList: L } = z,
      U = s([
        {
          field: "user_id",
          label: "操作人编号",
          show: !0,
          disabled: !0,
          width: "100px",
        },
        {
          field: "user.name",
          label: "操作人",
          show: !0,
          disabled: !0,
          width: "100px",
        },
        {
          field: "phone",
          label: "手机号",
          show: !0,
          disabled: !0,
          sortable: !0,
          width: "130px",
        },
        {
          field: "device.mac",
          label: "设备SN",
          show: !0,
          disabled: !0,
          width: "100px",
        },
        {
          field: "client_ip",
          label: "客户端地址",
          width: "130px",
          show: !0,
          sortable: !0,
          disabled: !0,
        },
        {
          field: "message",
          label: "操作内容",
          show: !0,
          width: "300px",
          showOverflowTooltip: !1,
        },
        {
          field: "status",
          label: "操作状态",
          show: !0,
          width: "100px",
          slots: {
            default: (e) => {
              const t = e.row;
              return l(a, null, [
                l(y, { type: "status", value: t.status }, null),
              ]);
            },
          },
        },
        { field: "browser", label: "浏览器", show: !0, width: "150px" },
        { field: "system", label: "系统", show: !1, width: "150px" },
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
              return l(a, null, [
                l(
                  i,
                  { type: "primary", link: !0, onClick: () => O(t, "detail") },
                  { default: () => [r("详情")] },
                ),
              ]);
            },
          },
        },
      ]),
      N = s([
        {
          field: "phone",
          label: "手机号",
          component: "Input",
          componentProps: { clearable: !1 },
        },
        {
          field: "message",
          label: "操作内容",
          component: "Input",
          componentProps: { clearable: !1 },
        },
      ]),
      T = p({ order: "desc", prop: "id" }),
      F = (e) => {
        ((I.value = 1), (T.value = e), L());
      },
      M = p(!1),
      V = p(""),
      q = p(),
      E = p(""),
      O = (e, t) => {
        ((V.value = k("exampleDemo.detail")),
          (E.value = t),
          (q.value = e),
          (M.value = !0));
      },
      W = (e) => {
        ("descending" === e.order
          ? ((T.value.order = "desc"), (T.value.prop = e.prop))
          : ((T.value.order = "asc"), (T.value.prop = e.prop)),
          L());
      };
    return (e, t) => (
      n(),
      d(
        a,
        null,
        [
          l(u(w), null, {
            default: m(() => [
              l(u(f), { schema: N, onReset: F, onSearch: F }, null, 8, [
                "schema",
              ]),
              l(
                u(h),
                {
                  "current-page": u(I),
                  "onUpdate:currentPage":
                    t[0] || (t[0] = (e) => (c(I) ? (I.value = e) : null)),
                  "page-size": u(C),
                  "onUpdate:pageSize":
                    t[1] || (t[1] = (e) => (c(C) ? (C.value = e) : null)),
                  onSortChange: W,
                  showAction: "",
                  columns: U,
                  "node-key": "id",
                  data: u(R),
                  loading: u(A),
                  pagination: { total: u(P) },
                  onRegister: u(S),
                  onRefresh: u(L),
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
          l(
            u(x),
            {
              modelValue: M.value,
              "onUpdate:modelValue": t[3] || (t[3] = (e) => (M.value = e)),
              title: V.value,
              width: "800px",
            },
            {
              footer: m(() => [
                l(
                  u(i),
                  { onClick: t[2] || (t[2] = (e) => (M.value = !1)) },
                  {
                    default: m(() => [r(j(u(k)("dialogDemo.close")), 1)]),
                    _: 1,
                  },
                ),
              ]),
              default: m(() => [
                "detail" === E.value
                  ? (n(),
                    _(b, { key: 0, "current-row": q.value }, null, 8, [
                      "current-row",
                    ]))
                  : g("", !0),
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
export { k as default };
