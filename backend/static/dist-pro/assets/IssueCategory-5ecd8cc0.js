import { e, f as a, h as t, i as l, j as o } from "./issue-18263b13.js";
import { u as s, _ as i } from "./Table.vue_vue_type_script_lang-230d9abb.js";
import {
  e as r,
  I as p,
  r as n,
  L as u,
  x as m,
  a1 as d,
  N as c,
  M as v,
  o as _,
  j,
  m as f,
  k as g,
  ai as y,
  z as w,
} from "./index-6b60d190.js";
import { E as b } from "./el-switch-5507f2ea.js";
import { a as h, E as x } from "./el-col-b8aa0d1a.js";
import { _ as k } from "./Search.vue_vue_type_script_setup_true_lang-9c85421f.js";
import { _ as z } from "./ContentWrap.vue_vue_type_script_setup_true_lang-067de0d9.js";
import { _ as C } from "./Write.vue_vue_type_script_setup_true_lang-633fde4e.js";
import { _ as S } from "./Dialog.vue_vue_type_style_index_0_lang-d732453c.js";
import { u as R } from "./dict-2254259d.js";
import { s as D } from "./dict-4a6e55e6.js";
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
import "./useIcon-7641a992.js";
import "./el-card-37d6f3c4.js";
import "./useValidator-63200dcb.js";
import "./use-dialog-0e1ee265.js";
import "./dict-593a5a5e.js";
const P = r({
  name: "HelpIssueCategory",
  __name: "IssueCategory",
  setup(r) {
    const { t: P } = p(),
      {
        tableRegister: I,
        tableState: A,
        tableMethods: L,
      } = s({
        fetchDataApi: async () => {
          const { pageSize: e, currentPage: t } = A,
            l = await a({ page: g(t), limit: g(e), ...g(T) });
          return { list: l.data || [], total: l.count || 0 };
        },
        fetchDelApi: async (e) => 200 === (await t(e)).code,
      }),
      { dataList: E, loading: U, total: V, pageSize: M, currentPage: N } = A,
      { getList: W, delList: q } = L,
      F = n([]);
    (async () => {
      const e = R(),
        a = await e.getDictObj(["sys_vadmin_platform"]);
      F.value = a.sys_vadmin_platform;
    })();
    const H = u([
        { field: "id", label: "编号", show: !0, disabled: !0 },
        { field: "name", label: "类别名称", show: !0, disabled: !0 },
        {
          field: "platform",
          label: "展示平台",
          show: !0,
          slots: {
            default: (e) => {
              const a = e.row;
              return m(d, null, [m("div", null, [D(F.value, a.platform)])]);
            },
          },
        },
        {
          field: "is_active",
          label: "是否可见",
          show: !0,
          slots: {
            default: (e) => {
              const a = e.row;
              return m(d, null, [
                m(b, { value: a.is_active, disabled: !0 }, null),
              ]);
            },
          },
        },
        { field: "created_at", label: "创建时间", show: !0, sortable: !0 },
        { field: "create_user.name", label: "创建人", show: !0 },
        {
          field: "action",
          width: "120px",
          label: "操作",
          show: !0,
          slots: {
            default: (e) => {
              const a = e.row;
              return m(d, null, [
                m(
                  c,
                  {
                    type: "primary",
                    link: !0,
                    size: "small",
                    onClick: () => ee(a),
                  },
                  { default: () => [v("编辑")] },
                ),
                m(
                  c,
                  {
                    type: "danger",
                    loading: G.value,
                    link: !0,
                    size: "small",
                    onClick: () => J(a),
                  },
                  { default: () => [v("删除")] },
                ),
              ]);
            },
          },
        },
      ]),
      O = u([
        {
          field: "name",
          label: "类别名称",
          component: "Input",
          componentProps: { clearable: !0, style: { width: "214px" } },
        },
        {
          field: "platform",
          label: "登录平台",
          component: "Select",
          componentProps: { style: { width: "214px" }, options: [] },
        },
        {
          field: "is_active",
          label: "是否可见",
          component: "Select",
          componentProps: {
            style: { width: "214px" },
            options: [
              { label: "可见", value: !0 },
              { label: "不可见", value: !1 },
            ],
          },
        },
      ]),
      T = n({}),
      B = (e) => {
        ((N.value = 1), (T.value = e), W());
      },
      G = n(!1),
      J = async (e) => {
        ((G.value = !0),
          await q(!0, [e.id]).finally(() => {
            G.value = !1;
          }));
      },
      K = n(!1),
      Q = n(""),
      X = n(),
      Y = n(""),
      Z = n(),
      $ = n(!1),
      ee = async (a) => {
        const t = await e(a.id);
        t &&
          ((Q.value = "编辑常见问题类别"),
          (Y.value = "edit"),
          (X.value = t.data),
          (K.value = !0));
      },
      ae = () => {
        ((Q.value = "新增常见问题类别"),
          (Y.value = "add"),
          (X.value = void 0),
          (K.value = !0));
      },
      te = async () => {
        const e = g(Z),
          a = await (null == e ? void 0 : e.submit());
        if (a) {
          $.value = !0;
          try {
            const e = n({});
            "add" === Y.value
              ? ((e.value = await l(a)), e.value && ((K.value = !1), W()))
              : "edit" === Y.value &&
                ((e.value = await o(a)), e.value && ((K.value = !1), W()));
          } finally {
            $.value = !1;
          }
        }
      };
    return (e, a) => (
      _(),
      j(
        d,
        null,
        [
          m(g(z), null, {
            default: f(() => [
              m(g(k), { schema: O, onReset: B, onSearch: B }, null, 8, [
                "schema",
              ]),
              m(
                g(i),
                {
                  "current-page": g(N),
                  "onUpdate:currentPage":
                    a[0] || (a[0] = (e) => (y(N) ? (N.value = e) : null)),
                  "page-size": g(M),
                  "onUpdate:pageSize":
                    a[1] || (a[1] = (e) => (y(M) ? (M.value = e) : null)),
                  showAction: "",
                  columns: H,
                  "default-expand-all": "",
                  "node-key": "id",
                  data: g(E),
                  loading: g(U),
                  pagination: { total: g(V) },
                  onRegister: g(I),
                  onRefresh: g(W),
                },
                {
                  toolbar: f(() => [
                    m(
                      g(h),
                      { gutter: 10 },
                      {
                        default: f(() => [
                          m(
                            g(x),
                            { span: 1.5 },
                            {
                              default: f(() => [
                                m(
                                  g(c),
                                  { type: "primary", onClick: ae },
                                  {
                                    default: f(() => [v("新增常见问题类别")]),
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
          m(
            g(S),
            {
              modelValue: K.value,
              "onUpdate:modelValue": a[3] || (a[3] = (e) => (K.value = e)),
              title: Q.value,
              height: 650,
            },
            {
              footer: f(() => [
                m(
                  g(c),
                  { type: "primary", loading: $.value, onClick: te },
                  {
                    default: f(() => [v(w(g(P)("exampleDemo.save")), 1)]),
                    _: 1,
                  },
                  8,
                  ["loading"],
                ),
                m(
                  g(c),
                  { onClick: a[2] || (a[2] = (e) => (K.value = !1)) },
                  {
                    default: f(() => [v(w(g(P)("dialogDemo.close")), 1)]),
                    _: 1,
                  },
                ),
              ]),
              default: f(() => [
                m(
                  C,
                  { ref_key: "writeRef", ref: Z, "current-row": X.value },
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
        ],
        64,
      )
    );
  },
});
export { P as default };
