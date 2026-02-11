import { g as e, d as a, a as l, p as t } from "./dept-7c279e0e.js";
import { u as s, _ as i } from "./Table.vue_vue_type_script_lang-230d9abb.js";
import {
  e as o,
  I as r,
  L as p,
  x as u,
  a1 as d,
  N as n,
  M as m,
  r as v,
  o as c,
  j,
  m as f,
  k as _,
  l as g,
  z as y,
  F as w,
  af as b,
} from "./index-6b60d190.js";
import { E as h } from "./el-switch-5507f2ea.js";
import { a as x, E as k } from "./el-col-b8aa0d1a.js";
import { _ as C } from "./ContentWrap.vue_vue_type_script_setup_true_lang-067de0d9.js";
import { _ as D } from "./Write.vue_vue_type_script_setup_true_lang-24edb564.js";
import { _ as R } from "./Dialog.vue_vue_type_style_index_0_lang-d732453c.js";
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
import "./use-dialog-0e1ee265.js";
const z = o({
  name: "AuthDept",
  __name: "Dept",
  setup(o) {
    const { t: z } = r(),
      {
        tableRegister: A,
        tableState: L,
        tableMethods: S,
      } = s({
        fetchDataApi: async () => {
          const { pageSize: a, currentPage: l } = L,
            t = await e({ page: _(l), limit: _(a) });
          return { list: t.data || [], total: t.count || 0 };
        },
        fetchDelApi: async (e) => 200 === (await a(e)).code,
      }),
      { dataList: E, loading: V } = L,
      { getList: F, delList: M } = S,
      N = p([
        { field: "name", label: "部门名称", disabled: !0, show: !0 },
        { field: "code", label: "部门标识", show: !0 },
        { field: "manager", label: "负责人", show: !0 },
        { field: "phone", label: "联系电话", show: !0 },
        { field: "email", label: "邮箱", show: !0 },
        { field: "desc", label: "描述", show: !0 },
        { field: "order", label: "排序", width: "120px", show: !0 },
        {
          field: "status",
          label: "状态",
          width: "120px",
          show: !0,
          slots: {
            default: (e) => {
              const a = e.row;
              return u(d, null, [
                u(h, { value: !a.disabled, disabled: !0 }, null),
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
              const a = e.row;
              return u(d, null, [
                u(
                  n,
                  {
                    type: "primary",
                    link: !0,
                    size: "small",
                    onClick: () => K(a),
                  },
                  { default: () => [m("编辑")] },
                ),
                u(
                  n,
                  {
                    type: "primary",
                    link: !0,
                    size: "small",
                    onClick: () => Q(a),
                  },
                  { default: () => [m("添加子部门")] },
                ),
                u(
                  n,
                  {
                    type: "danger",
                    loading: q.value,
                    link: !0,
                    size: "small",
                    onClick: () => G(a),
                  },
                  { default: () => [m("删除")] },
                ),
              ]);
            },
          },
        },
      ]),
      q = v(!1),
      G = async (e) => {
        ((q.value = !0),
          await M(!0, [e.id]).finally(() => {
            q.value = !1;
          }));
      },
      H = v(!1),
      I = v(""),
      P = v(),
      U = v(void 0),
      W = v(""),
      B = v(),
      J = v(!1),
      K = (e) => {
        ((I.value = "编辑"), (W.value = "edit"), (P.value = e), (H.value = !0));
      },
      O = () => {
        ((I.value = "新增"),
          (W.value = "add"),
          (P.value = void 0),
          (H.value = !0));
      },
      Q = (e) => {
        ((I.value = "添加子部门"),
          (W.value = "addSon"),
          (U.value = e.id),
          (P.value = void 0),
          (H.value = !0));
      },
      T = async () => {
        const e = _(B),
          a = await (null == e ? void 0 : e.submit());
        if (a) {
          J.value = !0;
          try {
            const e = v({});
            "add" === W.value || "addSon" === W.value
              ? ((e.value = await l(a)),
                e.value &&
                  ((U.value = void 0),
                  (H.value = !1),
                  F(),
                  b.success("添加成功!")))
              : "edit" === W.value &&
                ((e.value = await t(a)),
                e.value && ((H.value = !1), F(), b.success("编辑成功!")));
          } finally {
            J.value = !1;
          }
        }
      };
    return (e, a) => (
      c(),
      j(
        d,
        null,
        [
          u(_(C), null, {
            default: f(() => [
              u(
                _(i),
                {
                  columns: N,
                  showAction: "",
                  "default-expand-all": "",
                  "node-key": "id",
                  data: _(E),
                  loading: _(V),
                  onRegister: _(A),
                  onRefresh: _(F),
                },
                {
                  toolbar: f(() => [
                    u(
                      _(x),
                      { gutter: 10 },
                      {
                        default: f(() => [
                          u(
                            _(k),
                            { span: 1.5 },
                            {
                              default: f(() => [
                                u(
                                  _(n),
                                  { type: "primary", onClick: O },
                                  { default: f(() => [m("新增部门")]), _: 1 },
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
          u(
            _(R),
            {
              modelValue: H.value,
              "onUpdate:modelValue": a[1] || (a[1] = (e) => (H.value = e)),
              title: I.value,
            },
            {
              footer: f(() => [
                "detail" !== W.value
                  ? (c(),
                    g(
                      _(n),
                      { key: 0, type: "primary", loading: J.value, onClick: T },
                      {
                        default: f(() => [m(y(_(z)("exampleDemo.save")), 1)]),
                        _: 1,
                      },
                      8,
                      ["loading"],
                    ))
                  : w("", !0),
                u(
                  _(n),
                  { onClick: a[0] || (a[0] = (e) => (H.value = !1)) },
                  {
                    default: f(() => [m(y(_(z)("dialogDemo.close")), 1)]),
                    _: 1,
                  },
                ),
              ]),
              default: f(() => [
                u(
                  D,
                  {
                    ref_key: "writeRef",
                    ref: B,
                    "current-row": P.value,
                    "parent-id": U.value,
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
  },
});
export { z as default };
