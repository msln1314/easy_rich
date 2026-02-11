import {
  a as e,
  r as a,
  b as t,
  d as l,
  c as s,
  p as i,
} from "./task-5807e24e.js";
import { u as o, _ as r } from "./Table.vue_vue_type_script_lang-230d9abb.js";
import {
  e as p,
  A as n,
  I as u,
  L as d,
  x as m,
  a1 as c,
  N as _,
  M as v,
  r as f,
  af as j,
  o as y,
  j as g,
  m as w,
  k as h,
  ai as b,
  z as x,
  l as k,
  F as C,
} from "./index-6b60d190.js";
import { E as z } from "./el-switch-5507f2ea.js";
import { a as P, E as R } from "./el-col-b8aa0d1a.js";
import { E as S } from "./el-message-box-2d28828b.js";
import "./el-input-38d674e5.js";
import "./el-overlay-2c5c0104.js";
import { _ as D } from "./Search.vue_vue_type_script_setup_true_lang-9c85421f.js";
import { _ as E } from "./ContentWrap.vue_vue_type_script_setup_true_lang-067de0d9.js";
import { _ as A } from "./Write.vue_vue_type_script_setup_true_lang-04aaecc8.js";
import { _ as L } from "./Dialog.vue_vue_type_style_index_0_lang-d732453c.js";
import { _ as T } from "./CronExpression.vue_vue_type_style_index_0_lang-e9dd87a4.js";
import "./el-table-column-0bcf5917.js";
import "./el-popper-09548d54.js";
import "./isNil-1f22f7b0.js";
import "./focus-trap-275966d8.js";
import "./isEqual-b8d86c27.js";
import "./el-checkbox-4903f610.js";
import "./event-5568c9d8.js";
import "./debounce-5c500a3d.js";
import "./index-fdfa028a.js";
import "./el-tooltip-4ed993c7.js";
/* empty css               */ import "./el-pagination-491dd0e9.js";
import "./el-select-8805ff65.js";
import "./index-b7c1540b.js";
import "./strings-00317668.js";
import "./scroll-6dba6951.js";
import "./validator-f032316f.js";
import "./dropdown-84a04b2c.js";
import "./el-image-viewer-5060851c.js";
import "./useForm-b6ceb895.js";
import "./el-form-item-ce18addb.js";
/* empty css                          */ import "./el-date-picker-91f17f23.js";
import "./el-radio-group-0c46635e.js";
import "./el-divider-2dd0a1ee.js";
import "./el-tree-84af12f2.js";
import "./index-55fef7b1.js";
import "./el-progress-31e0b945.js";
import "./style.css_vue_type_style_index_0_src_true_lang-d8fdefc2.js";
import "./el-dropdown-item-943c2eb7.js";
import "./refs-64421a9c.js";
/* empty css                   */ import "./_Uint8Array-f98e6540.js";
import "./index-62254dd8.js";
import "./vnode-34f6d346.js";
import "./useIcon-7641a992.js";
import "./el-card-37d6f3c4.js";
import "./useValidator-63200dcb.js";
import "./dict-2254259d.js";
import "./dict-593a5a5e.js";
import "./use-dialog-0e1ee265.js";
import "./el-tab-pane-1bfe2fef.js";
import "./RunDatetimeList-f639e348.js";
import "./CronExample-e315085c.js";
import "./el-descriptions-item-68636e02.js";
const I = p({
  name: "SystemTask",
  __name: "Task",
  setup(p) {
    const { push: I } = n(),
      { t: U } = u(),
      {
        tableRegister: V,
        tableState: B,
        tableMethods: F,
      } = o({
        fetchDataApi: async () => {
          const { pageSize: e, currentPage: a } = B,
            l = await t({ page: h(a), limit: h(e), ...h(J) });
          return { list: l.data || [], total: l.count || 0 };
        },
        fetchDelApi: async (e) => 200 === (await l(e)).code,
      }),
      { dataList: M, loading: N, total: W, pageSize: q, currentPage: O } = B,
      { getList: X, delList: Y } = F,
      G = d([
        {
          field: "_id",
          label: "任务编号",
          show: !0,
          disabled: !0,
          width: "230px",
          span: 24,
        },
        { field: "name", label: "任务名称", show: !0, disabled: !0, span: 24 },
        { field: "group", label: "任务分组", show: !0, span: 24 },
        { field: "job_class", label: "调用目标", show: !0, span: 24 },
        {
          field: "exec_strategy",
          label: "执行策略",
          show: !0,
          colProps: { span: 24 },
          componentProps: { style: { width: "100%" } },
        },
        { field: "expression", label: "表达式", show: !0, span: 24 },
        {
          field: "is_active",
          label: "任务状态",
          show: !0,
          width: "100px",
          slots: {
            default: (e) => {
              const a = e.row;
              return m(c, null, [
                m(z, { value: a.is_active, disabled: !0 }, null),
              ]);
            },
          },
        },
        {
          field: "last_run_datetime",
          label: "最近一次执行时间",
          show: !0,
          width: "180px",
          span: 24,
        },
        { field: "remark", label: "任务备注", show: !0, span: 24 },
        {
          field: "created_at",
          label: "创建时间",
          show: !0,
          width: "180px",
          span: 24,
        },
        {
          field: "action",
          label: "操作",
          show: !0,
          disabled: !1,
          width: "240px",
          slots: {
            default: (e) => {
              const a = e.row;
              return m(c, null, [
                m(
                  _,
                  {
                    type: "primary",
                    link: !0,
                    size: "small",
                    onClick: () => ie(a),
                  },
                  { default: () => [v("编辑")] },
                ),
                m(
                  _,
                  {
                    type: "primary",
                    link: !0,
                    size: "small",
                    onClick: () => ne(a),
                  },
                  { default: () => [v("调度日志")] },
                ),
                m(
                  _,
                  {
                    type: "primary",
                    link: !0,
                    size: "small",
                    onClick: () => ue(a),
                  },
                  { default: () => [v("执行一次")] },
                ),
                m(
                  _,
                  {
                    type: "danger",
                    link: !0,
                    size: "small",
                    onClick: () => Z(a),
                  },
                  { default: () => [v("删除")] },
                ),
              ]);
            },
          },
        },
      ]),
      H = d([
        {
          field: "name",
          label: "任务名称",
          component: "Input",
          componentProps: { clearable: !0, style: { width: "214px" } },
        },
        {
          field: "_id",
          label: "任务编号",
          component: "Input",
          componentProps: { clearable: !0, style: { width: "214px" } },
        },
        {
          field: "group",
          label: "任务分组",
          component: "Select",
          componentProps: { style: { width: "214px" }, options: [] },
        },
      ]),
      J = f({}),
      K = (e) => {
        ((O.value = 1), (J.value = e), X());
      },
      Q = f(!1),
      Z = async (e) => {
        ((Q.value = !0),
          await Y(!0, [e._id]).finally(() => {
            Q.value = !1;
          }));
      },
      $ = f(!1),
      ee = f(""),
      ae = f(),
      te = f(""),
      le = f(),
      se = f(!1),
      ie = async (a) => {
        const t = await e(a._id);
        t &&
          ((ee.value = "编辑定时任务"),
          (te.value = "edit"),
          (ae.value = t.data),
          ($.value = !0));
      },
      oe = () => {
        ((ee.value = "新增定时任务"),
          (te.value = "add"),
          (ae.value = void 0),
          ($.value = !0));
      },
      re = async () => {
        const e = h(le),
          a = await (null == e ? void 0 : e.submit());
        if (a) {
          se.value = !0;
          try {
            const e = f({});
            "add" === te.value
              ? ((e.value = await s(a)), e.value && (($.value = !1), X()))
              : "edit" === te.value &&
                ((e.value = await i(a._id, a)),
                e.value && (($.value = !1), X()));
          } finally {
            se.value = !1;
          }
        }
      },
      pe = () => {
        ((ee.value = "Cron 表达式"),
          (te.value = "expression"),
          (ae.value = void 0),
          ($.value = !0));
      },
      ne = (e) => {
        I(e ? `/record/task?job_id=${e._id}` : "/record/task");
      },
      ue = async (e) => {
        S.confirm("是否确认立即执行一次任务", "提示", {
          confirmButtonText: U("common.delOk"),
          cancelButtonText: U("common.delCancel"),
          type: "warning",
        }).then(async () => {
          const t = await a(e._id);
          t &&
            (t.data > 0
              ? j.success("任务成功被消费者接收！")
              : j.error(
                  "执行失败，未有消费者接收任务，请检查定时任务程序状态！",
                ));
        });
      };
    return (e, a) => (
      y(),
      g(
        c,
        null,
        [
          m(h(E), null, {
            default: w(() => [
              m(h(D), { schema: H, onReset: K, onSearch: K }, null, 8, [
                "schema",
              ]),
              m(
                h(r),
                {
                  "current-page": h(O),
                  "onUpdate:currentPage":
                    a[1] || (a[1] = (e) => (b(O) ? (O.value = e) : null)),
                  "page-size": h(q),
                  "onUpdate:pageSize":
                    a[2] || (a[2] = (e) => (b(q) ? (q.value = e) : null)),
                  showAction: "",
                  columns: G,
                  "default-expand-all": "",
                  "node-key": "id",
                  data: h(M),
                  loading: h(N),
                  pagination: { total: h(W) },
                  onRegister: h(V),
                  onRefresh: h(X),
                },
                {
                  toolbar: w(() => [
                    m(
                      h(P),
                      { gutter: 10 },
                      {
                        default: w(() => [
                          m(
                            h(R),
                            { span: 1.5 },
                            {
                              default: w(() => [
                                m(
                                  h(_),
                                  { type: "primary", onClick: oe },
                                  {
                                    default: w(() => [v("新增定时任务")]),
                                    _: 1,
                                  },
                                ),
                              ]),
                              _: 1,
                            },
                          ),
                          m(
                            h(R),
                            { span: 1.5 },
                            {
                              default: w(() => [
                                m(
                                  h(_),
                                  {
                                    type: "primary",
                                    onClick: a[0] || (a[0] = (e) => ne(null)),
                                  },
                                  { default: w(() => [v("调度日志")]), _: 1 },
                                ),
                              ]),
                              _: 1,
                            },
                          ),
                          m(
                            h(R),
                            { span: 1.5 },
                            {
                              default: w(() => [
                                m(
                                  h(_),
                                  { type: "primary", onClick: pe },
                                  {
                                    default: w(() => [
                                      v("快速生成 Cron 表达式"),
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
            h(L),
            {
              modelValue: $.value,
              "onUpdate:modelValue": a[4] || (a[4] = (e) => ($.value = e)),
              title: ee.value,
              height: 680,
              width: 850,
            },
            {
              footer: w(() => [
                m(
                  h(_),
                  { type: "primary", loading: se.value, onClick: re },
                  {
                    default: w(() => [v(x(h(U)("exampleDemo.save")), 1)]),
                    _: 1,
                  },
                  8,
                  ["loading"],
                ),
                m(
                  h(_),
                  { onClick: a[3] || (a[3] = (e) => ($.value = !1)) },
                  {
                    default: w(() => [v(x(h(U)("dialogDemo.close")), 1)]),
                    _: 1,
                  },
                ),
              ]),
              default: w(() => [
                "add" === te.value || "edit" === te.value
                  ? (y(),
                    k(
                      A,
                      {
                        key: 0,
                        ref_key: "writeRef",
                        ref: le,
                        "current-row": ae.value,
                      },
                      null,
                      8,
                      ["current-row"],
                    ))
                  : C("", !0),
                "expression" === te.value ? (y(), k(T, { key: 1 })) : C("", !0),
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
export { I as default };
