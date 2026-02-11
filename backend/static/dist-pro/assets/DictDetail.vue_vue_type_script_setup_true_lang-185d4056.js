import { a as e, b as a, d as l, c as t, p as i } from "./dict-593a5a5e.js";
import { u as s, _ as o } from "./Table.vue_vue_type_script_lang-230d9abb.js";
import {
  e as u,
  ad as d,
  I as n,
  L as r,
  x as p,
  a1 as c,
  N as v,
  M as _,
  r as f,
  w as m,
  o as g,
  j as y,
  m as w,
  k as b,
  ai as h,
  z as j,
} from "./index-6b60d190.js";
import { E as k } from "./el-switch-5507f2ea.js";
import { a as z, E as D } from "./el-col-b8aa0d1a.js";
import { _ as x } from "./Search.vue_vue_type_script_setup_true_lang-9c85421f.js";
import { _ as I } from "./ContentWrap.vue_vue_type_script_setup_true_lang-067de0d9.js";
import { _ as R } from "./Write.vue_vue_type_script_setup_true_lang-07f2bbbb.js";
import { _ as C } from "./Dialog.vue_vue_type_style_index_0_lang-d732453c.js";
const S = u({
  __name: "DictDetail",
  props: { dictTypeId: d.number.def(void 0) },
  setup(u) {
    const d = u,
      { t: S } = n(),
      {
        tableRegister: T,
        tableState: L,
        tableMethods: P,
      } = s({
        fetchDataApi: async () => {
          const { pageSize: e, currentPage: l } = L,
            t = await a({
              page: b(l),
              limit: b(e),
              dict_type_id: d.dictTypeId,
              ...b(B),
            });
          return { list: t.data || [], total: t.count || 0 };
        },
        fetchDelApi: async (e) => 200 === (await l(e)).code,
      }),
      { dataList: U, loading: A, total: M, pageSize: V, currentPage: E } = L,
      { getList: W, delList: J } = P,
      N = r([
        { field: "id", label: "字典编号", show: !1, disabled: !1 },
        { field: "label", label: "字典标签", show: !0, disabled: !0 },
        { field: "value", label: "字典键值", show: !0 },
        { field: "order", label: "字典排序", show: !0 },
        {
          field: "status",
          label: "状态",
          show: !0,
          slots: {
            default: (e) => {
              const a = e.row;
              return p(c, null, [
                p(k, { value: a.status, disabled: !0 }, null),
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
              return p(c, null, [
                p(
                  v,
                  {
                    type: "primary",
                    link: !0,
                    size: "small",
                    onClick: () => $(a),
                  },
                  { default: () => [_("编辑")] },
                ),
                p(
                  v,
                  {
                    type: "danger",
                    loading: G.value,
                    link: !0,
                    size: "small",
                    onClick: () => H(a),
                  },
                  { default: () => [_("删除")] },
                ),
              ]);
            },
          },
        },
      ]),
      q = r([
        {
          field: "label",
          label: "字典标签",
          component: "Input",
          componentProps: { clearable: !1 },
        },
      ]),
      B = f({}),
      F = (e) => {
        ((E.value = 1), (B.value = e), W());
      },
      G = f(!1),
      H = async (e) => {
        ((G.value = !0),
          await J(!0, [e.id]).finally(() => {
            G.value = !1;
          }));
      },
      K = f(!1),
      O = f(""),
      Q = f(),
      X = f(""),
      Y = f(),
      Z = f(!1),
      $ = async (a) => {
        const l = await e(a.id);
        l &&
          ((O.value = "编辑字段元素"),
          (X.value = "edit"),
          (Q.value = l.data),
          (K.value = !0));
      },
      ee = () => {
        ((O.value = "新增字段元素"),
          (X.value = "add"),
          (Q.value = void 0),
          (K.value = !0));
      },
      ae = async () => {
        const e = b(Y),
          a = await (null == e ? void 0 : e.submit());
        if (a) {
          Z.value = !0;
          try {
            const e = f({});
            "add" === X.value
              ? ((e.value = await t(a)), e.value && ((K.value = !1), await W()))
              : "edit" === X.value &&
                ((e.value = await i(a)),
                e.value && ((K.value = !1), await W()));
          } finally {
            Z.value = !1;
          }
        }
      };
    return (
      m(
        () => d.dictTypeId,
        () => {
          W();
        },
        { deep: !0 },
      ),
      (e, a) => (
        g(),
        y(
          c,
          null,
          [
            p(b(I), null, {
              default: w(() => [
                p(b(x), { schema: q, onReset: F, onSearch: F }, null, 8, [
                  "schema",
                ]),
                p(
                  b(o),
                  {
                    "current-page": b(E),
                    "onUpdate:currentPage":
                      a[0] || (a[0] = (e) => (h(E) ? (E.value = e) : null)),
                    "page-size": b(V),
                    "onUpdate:pageSize":
                      a[1] || (a[1] = (e) => (h(V) ? (V.value = e) : null)),
                    showAction: "",
                    activeUID: "detail",
                    columns: N,
                    "default-expand-all": "",
                    "node-key": "id",
                    data: b(U),
                    loading: b(A),
                    pagination: { total: b(M) },
                    onRegister: b(T),
                    onRefresh: b(W),
                  },
                  {
                    toolbar: w(() => [
                      p(
                        b(z),
                        { gutter: 10 },
                        {
                          default: w(() => [
                            p(
                              b(D),
                              { span: 1.5 },
                              {
                                default: w(() => [
                                  p(
                                    b(v),
                                    { type: "primary", onClick: ee },
                                    {
                                      default: w(() => [_("新增字典元素")]),
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
            p(
              b(C),
              {
                modelValue: K.value,
                "onUpdate:modelValue": a[3] || (a[3] = (e) => (K.value = e)),
                title: O.value,
                height: 650,
              },
              {
                footer: w(() => [
                  p(
                    b(v),
                    { type: "primary", loading: Z.value, onClick: ae },
                    {
                      default: w(() => [_(j(b(S)("exampleDemo.save")), 1)]),
                      _: 1,
                    },
                    8,
                    ["loading"],
                  ),
                  p(
                    b(v),
                    { onClick: a[2] || (a[2] = (e) => (K.value = !1)) },
                    {
                      default: w(() => [_(j(b(S)("dialogDemo.close")), 1)]),
                      _: 1,
                    },
                  ),
                ]),
                default: w(() => [
                  p(
                    R,
                    {
                      ref_key: "writeRef",
                      ref: Y,
                      "current-row": Q.value,
                      "dict-type-id": u.dictTypeId,
                    },
                    null,
                    8,
                    ["current-row", "dict-type-id"],
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
      )
    );
  },
});
export { S as _ };
