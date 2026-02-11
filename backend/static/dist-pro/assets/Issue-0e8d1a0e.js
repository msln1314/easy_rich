import { g as e, d as t } from "./issue-18263b13.js";
import { u as s, _ as a } from "./Table.vue_vue_type_script_lang-230d9abb.js";
import {
  e as i,
  A as l,
  r as o,
  L as r,
  x as p,
  a1 as n,
  N as m,
  M as d,
  o as u,
  l as c,
  m as j,
  k as _,
  ai as f,
} from "./index-6b60d190.js";
import { E as g } from "./el-switch-5507f2ea.js";
import { a as h, E as v } from "./el-col-b8aa0d1a.js";
import { _ as b } from "./Search.vue_vue_type_script_setup_true_lang-9c85421f.js";
import { _ as w } from "./ContentWrap.vue_vue_type_script_setup_true_lang-067de0d9.js";
import { u as y } from "./dict-2254259d.js";
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
import "./dict-593a5a5e.js";
const x = i({
  name: "HelpIssue",
  __name: "Issue",
  setup(i) {
    const { push: x } = l(),
      {
        tableRegister: k,
        tableState: z,
        tableMethods: S,
      } = s({
        fetchDataApi: async () => {
          const { pageSize: t, currentPage: s } = z,
            a = await e({ page: _(s), limit: _(t), ..._(U) });
          return { list: a.data || [], total: a.count || 0 };
        },
        fetchDelApi: async (e) => 200 === (await t(e)).code,
      }),
      { dataList: P, loading: R, total: A, pageSize: C, currentPage: I } = z,
      { getList: L, delList: D } = S,
      E = o([]);
    (async () => {
      const e = y(),
        t = await e.getDictObj(["sys_vadmin_platform"]);
      E.value = t.sys_vadmin_platform;
    })();
    const M = r([
        { field: "id", label: "编号", show: !0, disabled: !0, width: "120px" },
        {
          field: "category.name",
          label: "类别名称",
          width: "200px",
          show: !0,
          disabled: !0,
        },
        { field: "title", label: "标题", show: !0 },
        { field: "view_number", label: "查看次数", show: !0, width: "100px" },
        {
          field: "is_active",
          label: "是否可见",
          show: !0,
          width: "100px",
          slots: {
            default: (e) => {
              const t = e.row;
              return p(n, null, [
                p(g, { value: t.is_active, disabled: !0 }, null),
              ]);
            },
          },
        },
        {
          field: "created_at",
          label: "创建时间",
          show: !0,
          width: "200px",
          sortable: !0,
        },
        {
          field: "create_user.name",
          label: "创建人",
          show: !0,
          width: "100px",
        },
        {
          field: "action",
          width: "120px",
          label: "操作",
          show: !0,
          slots: {
            default: (e) => {
              const t = e.row;
              return p(n, null, [
                p(
                  m,
                  {
                    type: "primary",
                    link: !0,
                    size: "small",
                    onClick: () => O(t),
                  },
                  { default: () => [d("编辑")] },
                ),
                p(
                  m,
                  {
                    type: "danger",
                    loading: F.value,
                    link: !0,
                    size: "small",
                    onClick: () => H(t),
                  },
                  { default: () => [d("删除")] },
                ),
              ]);
            },
          },
        },
      ]),
      N = r([
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
          componentProps: { style: { width: "214px" }, options: E.value },
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
      U = o({}),
      q = (e) => {
        ((I.value = 1), (U.value = e), L());
      },
      F = o(!1),
      H = async (e) => {
        ((F.value = !0),
          await D(!0, [e.id]).finally(() => {
            F.value = !1;
          }));
      },
      O = async (e) => {
        x(`/help/issue/form?id=${e.id}`);
      },
      T = () => {
        x("/help/issue/form");
      };
    return (e, t) => (
      u(),
      c(_(w), null, {
        default: j(() => [
          p(_(b), { schema: N, onReset: q, onSearch: q }, null, 8, ["schema"]),
          p(
            _(a),
            {
              "current-page": _(I),
              "onUpdate:currentPage":
                t[0] || (t[0] = (e) => (f(I) ? (I.value = e) : null)),
              "page-size": _(C),
              "onUpdate:pageSize":
                t[1] || (t[1] = (e) => (f(C) ? (C.value = e) : null)),
              showAction: "",
              columns: M,
              "default-expand-all": "",
              "node-key": "id",
              data: _(P),
              loading: _(R),
              pagination: { total: _(A) },
              onRegister: _(k),
              onRefresh: _(L),
            },
            {
              toolbar: j(() => [
                p(
                  _(h),
                  { gutter: 10 },
                  {
                    default: j(() => [
                      p(
                        _(v),
                        { span: 1.5 },
                        {
                          default: j(() => [
                            p(
                              _(m),
                              { type: "primary", onClick: T },
                              { default: j(() => [d("新增常见问题")]), _: 1 },
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
      })
    );
  },
});
export { x as default };
