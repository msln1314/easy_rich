import { f as e, h as a, i as t, j as l, k as s } from "./dict-593a5a5e.js";
import { u as i, _ as n } from "./Table.vue_vue_type_script_lang-230d9abb.js";
import {
  e as o,
  I as u,
  L as r,
  x as d,
  al as p,
  a1 as c,
  N as _,
  M as m,
  r as f,
  o as v,
  j as y,
  m as g,
  k as w,
  ai as h,
  z as b,
  dx as k,
  af as j,
} from "./index-6b60d190.js";
import { E as C } from "./el-switch-5507f2ea.js";
import { a as x, E as D } from "./el-col-b8aa0d1a.js";
import { _ as R } from "./Search.vue_vue_type_script_setup_true_lang-9c85421f.js";
import { _ as z } from "./ContentWrap.vue_vue_type_script_setup_true_lang-067de0d9.js";
import { _ as I } from "./Write.vue_vue_type_script_setup_true_lang-f3243979.js";
import { _ as P } from "./Dialog.vue_vue_type_style_index_0_lang-d732453c.js";
const T = o({
  __name: "DictType",
  emits: ["updateDictTypeId"],
  setup(o, { emit: T }) {
    const { t: S } = u(),
      {
        tableRegister: L,
        tableState: E,
        tableMethods: U,
      } = i({
        fetchDataApi: async () => {
          const { pageSize: e, currentPage: t } = E,
            l = await a({ page: w(t), limit: w(e), ...w(J) });
          return { list: l.data || [], total: l.count || 0 };
        },
        fetchDelApi: async (e) => {
          const a = await t(e);
          return (200 === a.code && (await ne()), 200 === a.code);
        },
      }),
      { dataList: A, loading: M, total: V, pageSize: W, currentPage: N } = E,
      { getList: q, delList: B, getElTableExpose: F } = U,
      G = r([
        {
          field: "id",
          label: "字典编号",
          width: "80px",
          show: !1,
          disabled: !1,
        },
        { field: "dict_name", label: "字典名称", show: !0, disabled: !0 },
        {
          field: "dict_type",
          label: "字典类型",
          show: !0,
          disabled: !0,
          slots: {
            default: (e) => {
              const a = e.row;
              return d(c, null, [
                d(
                  "span",
                  {
                    onClick: () =>
                      (async (e) => {
                        const { copy: a } = k();
                        return (await a(e), j.success("复制成功"));
                      })(a.dict_type),
                  },
                  [
                    d(
                      p,
                      {
                        icon: "material-symbols:content-copy-rounded",
                        class: "cursor-pointer",
                      },
                      null,
                    ),
                  ],
                ),
                d("span", null, [a.dict_type]),
              ]);
            },
          },
        },
        {
          field: "status",
          label: "状态",
          width: "120px",
          show: !0,
          slots: {
            default: (e) => {
              const a = e.row;
              return d(c, null, [
                d(C, { value: a.status, disabled: !0 }, null),
              ]);
            },
          },
        },
        { field: "remark", label: "备注", show: !1 },
        { field: "created_at", label: "创建时间", show: !1 },
        {
          field: "action",
          width: "120px",
          label: "操作",
          show: !0,
          slots: {
            default: (e) => {
              const a = e.row;
              return d(c, null, [
                d(
                  _,
                  {
                    type: "primary",
                    link: !0,
                    size: "small",
                    onClick: () => te(a),
                  },
                  { default: () => [m("编辑")] },
                ),
                d(
                  _,
                  {
                    type: "danger",
                    loading: O.value,
                    link: !0,
                    size: "small",
                    onClick: () => Q(a),
                  },
                  { default: () => [m("删除")] },
                ),
              ]);
            },
          },
        },
      ]),
      H = r([
        {
          field: "dict_name",
          label: "字典名称",
          colProps: { span: 24 },
          component: "Input",
          componentProps: { clearable: !1 },
        },
        {
          field: "dict_type",
          label: "字典类型",
          colProps: { span: 24 },
          component: "Input",
          componentProps: { clearable: !1 },
        },
      ]),
      J = f({}),
      K = (e) => {
        ((N.value = 1), (J.value = e), q());
      },
      O = f(!1),
      Q = async (e) => {
        ((O.value = !0),
          await B(!0, [e.id]).finally(() => {
            O.value = !1;
          }));
      },
      X = f(!1),
      Y = f(""),
      Z = f(),
      $ = f(""),
      ee = f(),
      ae = f(!1),
      te = async (a) => {
        const t = await e(a.id);
        t &&
          ((Y.value = "编辑字典类型"),
          ($.value = "edit"),
          (Z.value = t.data),
          (X.value = !0));
      },
      le = () => {
        ((Y.value = "新增字典类型"),
          ($.value = "add"),
          (Z.value = void 0),
          (X.value = !0));
      },
      se = async () => {
        const e = w(ee),
          a = await (null == e ? void 0 : e.submit());
        if (a) {
          ae.value = !0;
          try {
            const e = f({});
            "add" === $.value
              ? ((e.value = await l(a)), e.value && ((X.value = !1), await q()))
              : "edit" === $.value &&
                ((e.value = await s(a)),
                e.value && ((X.value = !1), await q()));
          } finally {
            ae.value = !1;
          }
        }
      },
      ie = async (e) => {
        T("updateDictTypeId", e ? e.id : e);
      },
      ne = async () => {
        const e = await F();
        (null == e || e.setCurrentRow(null), T("updateDictTypeId", null));
      };
    return (e, a) => (
      v(),
      y(
        c,
        null,
        [
          d(w(z), null, {
            default: g(() => [
              d(w(R), { schema: H, onReset: K, onSearch: K }, null, 8, [
                "schema",
              ]),
              d(
                w(n),
                {
                  "current-page": w(N),
                  "onUpdate:currentPage":
                    a[0] || (a[0] = (e) => (h(N) ? (N.value = e) : null)),
                  "page-size": w(W),
                  "onUpdate:pageSize":
                    a[1] || (a[1] = (e) => (h(W) ? (W.value = e) : null)),
                  showAction: "",
                  activeUID: "type",
                  columns: G,
                  "default-expand-all": "",
                  highlightCurrentRow: !0,
                  "node-key": "id",
                  data: w(A),
                  loading: w(M),
                  pagination: { total: w(V) },
                  onRegister: w(L),
                  onCurrentChange: ie,
                  onRefresh: w(q),
                },
                {
                  toolbar: g(() => [
                    d(
                      w(x),
                      { gutter: 10 },
                      {
                        default: g(() => [
                          d(
                            w(D),
                            { span: 1.5 },
                            {
                              default: g(() => [
                                d(
                                  w(_),
                                  { type: "primary", onClick: le },
                                  {
                                    default: g(() => [m("新增字典类型")]),
                                    _: 1,
                                  },
                                ),
                              ]),
                              _: 1,
                            },
                          ),
                          d(
                            w(D),
                            { span: 1.5 },
                            {
                              default: g(() => [
                                d(
                                  w(_),
                                  { type: "danger", onClick: ne },
                                  { default: g(() => [m("清除选择")]), _: 1 },
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
          d(
            w(P),
            {
              modelValue: X.value,
              "onUpdate:modelValue": a[3] || (a[3] = (e) => (X.value = e)),
              title: Y.value,
              height: 650,
            },
            {
              footer: g(() => [
                d(
                  w(_),
                  { type: "primary", loading: ae.value, onClick: se },
                  {
                    default: g(() => [m(b(w(S)("exampleDemo.save")), 1)]),
                    _: 1,
                  },
                  8,
                  ["loading"],
                ),
                d(
                  w(_),
                  { onClick: a[2] || (a[2] = (e) => (X.value = !1)) },
                  {
                    default: g(() => [m(b(w(S)("dialogDemo.close")), 1)]),
                    _: 1,
                  },
                ),
              ]),
              default: g(() => [
                d(
                  I,
                  { ref_key: "writeRef", ref: ee, "current-row": Z.value },
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
export { T as _ };
