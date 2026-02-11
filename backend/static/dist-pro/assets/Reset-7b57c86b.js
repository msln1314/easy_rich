import { u as s, F as e } from "./useForm-b6ceb895.js";
import { u as t } from "./useValidator-63200dcb.js";
import {
  e as o,
  A as r,
  v as a,
  B as i,
  K as l,
  f as p,
  L as d,
  r as m,
  w as n,
  o as c,
  j as u,
  y as j,
  x as v,
  k as g,
  m as _,
  M as w,
  N as f,
  l as h,
  F as x,
  O as y,
  P as R,
  Q as b,
  R as k,
  S as F,
  J as P,
} from "./index-6b60d190.js";
import { _ as q } from "./Footer.vue_vue_type_script_setup_true_lang-c9dc208e.js";
import "./el-form-item-ce18addb.js";
import "./el-col-b8aa0d1a.js";
import "./el-tooltip-4ed993c7.js";
import "./el-popper-09548d54.js";
import "./isNil-1f22f7b0.js";
import "./focus-trap-275966d8.js";
import "./el-input-38d674e5.js";
import "./event-5568c9d8.js";
/* empty css               */ import "./el-checkbox-4903f610.js";
import "./isEqual-b8d86c27.js";
/* empty css                          */ import "./el-date-picker-91f17f23.js";
import "./debounce-5c500a3d.js";
import "./index-fdfa028a.js";
import "./el-radio-group-0c46635e.js";
import "./el-select-8805ff65.js";
import "./index-b7c1540b.js";
import "./strings-00317668.js";
import "./scroll-6dba6951.js";
import "./validator-f032316f.js";
import "./el-switch-5507f2ea.js";
import "./el-divider-2dd0a1ee.js";
import "./el-tree-84af12f2.js";
import "./index-55fef7b1.js";
import "./el-progress-31e0b945.js";
import "./style.css_vue_type_style_index_0_src_true_lang-d8fdefc2.js";
const E = { class: "main-container" },
  I = { class: "form-container" },
  A = ((s) => (b("data-v-ad559cf1"), (s = s()), k(), s))(() =>
    j(
      "div",
      null,
      [
        j(
          "h2",
          { class: "text-2xl font-bold text-center w-[100%]" },
          "第一次登录系统，需先重置密码",
        ),
      ],
      -1,
    ),
  ),
  M = { class: "w-[100%]" },
  N = { class: "footer-container" },
  S = P(
    o({
      __name: "Reset",
      setup(o) {
        const { required: b } = t(),
          { setStorage: k } = F(),
          { addRoute: P, push: S, currentRoute: B } = r(),
          C = a(),
          D = i(),
          J = l(),
          K = p(() => D.getFooter),
          L = d([
            {
              field: "password",
              label: "新密码",
              component: "InputPassword",
              colProps: { span: 24 },
              componentProps: {
                style: { width: "100%" },
                placeholder: "请输入新密码",
              },
            },
            {
              field: "password_two",
              label: "再次输入新密码",
              component: "InputPassword",
              colProps: { span: 24 },
              componentProps: {
                style: { width: "100%" },
                placeholder: "请再次输入新密码",
              },
            },
          ]),
          O = {
            password: [
              b(),
              {
                min: 8,
                max: 16,
                message: "长度需为8-16个字符,请重新输入。",
                trigger: "blur",
              },
            ],
            password_two: [
              b(),
              {
                min: 8,
                max: 16,
                message: "长度需为8-16个字符,请重新输入。",
                trigger: "blur",
              },
            ],
          },
          { formRegister: Q, formMethods: V } = s(),
          { setValues: z, getFormData: G, getElFormExpose: H } = V;
        z(C.getUser);
        const U = m(!1),
          T = m("");
        n(
          () => B.value,
          (s) => {
            var e;
            T.value =
              null == (e = null == s ? void 0 : s.query) ? void 0 : e.redirect;
          },
          { immediate: !0 },
        );
        const W = async () => {
            const s = await H();
            if (await (null == s ? void 0 : s.validate())) {
              U.value = !0;
              const s = await G();
              try {
                (await y(s)) ? X() : (U.value = !1);
              } catch (e) {
                U.value = !1;
              }
            }
          },
          X = async () => {
            const s = await R();
            if (s) {
              const e = s.data || [];
              (k("roleRouters", e),
                await J.generateRoutes(e).catch(() => {}),
                J.getAddRouters.forEach((s) => {
                  P(s);
                }),
                J.setIsAddRouters(!0),
                S({ path: T.value || J.addRouters[0].path }));
            }
          };
        return (s, t) => (
          c(),
          u("div", E, [
            j("div", I, [
              A,
              v(
                g(e),
                {
                  onRegister: g(Q),
                  schema: L,
                  rules: O,
                  "hide-required-asterisk": "",
                  class:
                    "dark:border-1 dark:border-[var(--el-border-color)] dark:border-solid",
                },
                null,
                8,
                ["onRegister", "schema"],
              ),
              j("div", M, [
                v(
                  g(f),
                  {
                    loading: U.value,
                    type: "primary",
                    class: "w-[100%]",
                    onClick: W,
                  },
                  { default: _(() => [w(" 重置密码 ")]), _: 1 },
                  8,
                  ["loading"],
                ),
              ]),
            ]),
            j("div", N, [K.value ? (c(), h(g(q), { key: 0 })) : x("", !0)]),
          ])
        );
      },
    }),
    [["__scopeId", "data-v-ad559cf1"]],
  );
export { S as default };
