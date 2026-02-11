import { u as e, a, F as s } from "./useForm-b6ceb895.js";
import {
  e as o,
  ad as t,
  I as n,
  o as i,
  j as l,
  l as d,
  m as r,
  M as c,
  z as h,
  k as u,
  N as m,
  F as p,
  a1 as f,
  r as g,
  f as b,
  b5 as w,
  bG as v,
  x,
  w as y,
  a2 as E,
  n as S,
  da as k,
  db as L,
  bD as F,
} from "./index-6b60d190.js";
import { u as R } from "./useIcon-7641a992.js";
const j = o({
    __name: "ActionButton",
    props: {
      showSearch: t.bool.def(!0),
      showReset: t.bool.def(!0),
      showExpand: t.bool.def(!1),
      visible: t.bool.def(!0),
      searchLoading: t.bool.def(!1),
      resetLoading: t.bool.def(!1),
    },
    emits: ["search", "reset", "expand"],
    setup(e, { emit: a }) {
      const { t: s } = n(),
        o = () => {
          a("search");
        },
        t = () => {
          a("reset");
        },
        g = () => {
          a("expand");
        };
      return (a, n) => (
        i(),
        l(
          f,
          null,
          [
            e.showSearch
              ? (i(),
                d(
                  u(m),
                  {
                    key: 0,
                    type: "primary",
                    loading: e.searchLoading,
                    icon: u(R)({ icon: "ep:search" }),
                    onClick: o,
                  },
                  { default: r(() => [c(h(u(s)("common.query")), 1)]), _: 1 },
                  8,
                  ["loading", "icon"],
                ))
              : p("", !0),
            e.showReset
              ? (i(),
                d(
                  u(m),
                  {
                    key: 1,
                    loading: e.resetLoading,
                    icon: u(R)({ icon: "ep:refresh-right" }),
                    onClick: t,
                  },
                  { default: r(() => [c(h(u(s)("common.reset")), 1)]), _: 1 },
                  8,
                  ["loading", "icon"],
                ))
              : p("", !0),
            e.showExpand
              ? (i(),
                d(
                  u(m),
                  {
                    key: 2,
                    icon: u(R)({
                      icon: e.visible ? "ep:arrow-down" : "ep:arrow-up",
                    }),
                    text: "",
                    onClick: g,
                  },
                  {
                    default: r(() => [
                      c(
                        h(u(s)(e.visible ? "common.shrink" : "common.expand")),
                        1,
                      ),
                    ]),
                    _: 1,
                  },
                  8,
                  ["icon"],
                ))
              : p("", !0),
          ],
          64,
        )
      );
    },
  }),
  _ = o({
    __name: "Search",
    props: {
      schema: { type: Array, default: () => [] },
      isCol: t.bool.def(!1),
      labelWidth: t.oneOfType([String, Number]).def("auto"),
      layout: t.string
        .validate((e) => ["inline", "bottom"].includes(e))
        .def("inline"),
      buttonPosition: t.string
        .validate((e) => ["left", "center", "right"].includes(e))
        .def("center"),
      showSearch: t.bool.def(!0),
      showReset: t.bool.def(!0),
      showExpand: t.bool.def(!1),
      expandField: t.string.def(""),
      inline: t.bool.def(!0),
      removeNoValueItem: t.bool.def(!0),
      model: { type: Object, default: () => ({}) },
      searchLoading: t.bool.def(!1),
      resetLoading: t.bool.def(!1),
    },
    emits: ["search", "reset", "register", "validate"],
    setup(o, { expose: t, emit: n }) {
      const d = o,
        r = g(!0),
        c = g(d.model),
        h = b(() => {
          const e = u(N);
          let a = w(e.schema);
          if (e.showExpand && e.expandField && !u(r)) {
            const s = v(a, (a) => a.field === e.expandField);
            a.map((e, a) => ((e.hidden = a >= s), e));
          }
          return (
            "inline" === e.layout &&
              (a = a.concat([
                {
                  field: "action",
                  formItemProps: {
                    labelWidth: "0px",
                    slots: {
                      default: () =>
                        x("div", null, [
                          x(
                            j,
                            {
                              showSearch: e.showSearch,
                              showReset: e.showReset,
                              showExpand: e.showExpand,
                              searchLoading: e.searchLoading,
                              resetLoading: e.resetLoading,
                              visible: r.value,
                              onExpand: D,
                              onReset: A,
                              onSearch: W,
                            },
                            null,
                          ),
                        ]),
                    },
                  },
                },
              ])),
            a
          );
        }),
        { formRegister: m, formMethods: R } = e(),
        { getElFormExpose: _, getFormData: O, getFormExpose: C } = R,
        I = g({}),
        V = g({}),
        N = b(() => {
          const e = { ...d };
          return (Object.assign(e, u(V)), e);
        });
      y(
        () => u(h),
        async (e = []) => {
          c.value = a(e, u(c));
        },
        { immediate: !0, deep: !0 },
      );
      const P = async () => {
          const e = await O();
          return u(N).removeNoValueItem
            ? Object.keys(e).reduce((a, s) => {
                const o = e[s];
                return (
                  k(o) ||
                    (L(o)
                      ? Object.keys(o).length > 0 && (a[s] = o)
                      : (a[s] = o)),
                  a
                );
              }, {})
            : e;
        },
        W = async () => {
          const e = await _();
          await (null == e
            ? void 0
            : e.validate(async (e) => {
                if (e) {
                  const e = await P();
                  n("search", e);
                }
              }));
        },
        A = async () => {
          const e = await _();
          null == e || e.resetFields();
          const a = await P();
          n("reset", a);
        },
        q = b(() => ({ textAlign: u(N).buttonPosition })),
        D = async () => {
          r.value = !u(r);
        },
        M = {
          getElFormExpose: _,
          setProps: (e = {}) => {
            ((V.value = Object.assign(u(V), e)), (I.value = e));
          },
          setSchema: (e) => {
            const { schema: a } = u(N);
            for (const s of a)
              for (const a of e) s.field === a.field && F(s, a.path, a.value);
          },
          setValues: async (e = {}) => {
            c.value = Object.assign(d.model, u(c), e);
            const a = await C();
            null == a || a.setValues(e);
          },
          delSchema: (e) => {
            const { schema: a } = u(N),
              s = v(a, (a) => a.field === e);
            s > -1 && a.splice(s, 1);
          },
          addSchema: (e, a) => {
            const { schema: s } = u(N);
            void 0 === a ? s.push(e) : s.splice(a, 0, e);
          },
        };
      (E(() => {
        n("register", M);
      }),
        t(M));
      const z = (e, a, s) => {
        n("validate", e, a, s);
      };
      return (e, a) => (
        i(),
        l(
          f,
          null,
          [
            x(
              u(s),
              {
                model: c.value,
                "is-custom": !1,
                "label-width": N.value.labelWidth,
                "hide-required-asterisk": "",
                inline: N.value.inline,
                "is-col": N.value.isCol,
                schema: h.value,
                onRegister: u(m),
                onValidate: z,
              },
              null,
              8,
              [
                "model",
                "label-width",
                "inline",
                "is-col",
                "schema",
                "onRegister",
              ],
            ),
            "bottom" === o.layout
              ? (i(),
                l(
                  "div",
                  { key: 0, style: S(q.value) },
                  [
                    x(
                      j,
                      {
                        "show-reset": N.value.showReset,
                        "show-search": N.value.showSearch,
                        "show-expand": N.value.showExpand,
                        "search-loading": N.value.searchLoading,
                        "reset-loading": N.value.resetLoading,
                        onExpand: D,
                        onReset: A,
                        onSearch: W,
                      },
                      null,
                      8,
                      [
                        "show-reset",
                        "show-search",
                        "show-expand",
                        "search-loading",
                        "reset-loading",
                      ],
                    ),
                  ],
                  4,
                ))
              : p("", !0),
          ],
          64,
        )
      );
    },
  });
export { _ };
