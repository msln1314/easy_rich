import { u as e, F as t } from "./useForm-b6ceb895.js";
import {
  e as o,
  I as s,
  A as a,
  K as l,
  v as r,
  L as i,
  x as p,
  a1 as n,
  N as d,
  r as c,
  w as u,
  ah as m,
  af as v,
  P as f,
  o as g,
  l as h,
  k as j,
  ag as w,
  S as y,
} from "./index-6b60d190.js";
import { E as x } from "./el-input-38d674e5.js";
import { E as b } from "./el-divider-2dd0a1ee.js";
import { u as k } from "./useValidator-63200dcb.js";
import "./el-form-item-ce18addb.js";
import "./el-col-b8aa0d1a.js";
import "./el-tooltip-4ed993c7.js";
import "./el-popper-09548d54.js";
import "./isNil-1f22f7b0.js";
import "./focus-trap-275966d8.js";
/* empty css               */ import "./el-checkbox-4903f610.js";
import "./event-5568c9d8.js";
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
import "./el-tree-84af12f2.js";
import "./index-55fef7b1.js";
import "./el-progress-31e0b945.js";
import "./style.css_vue_type_style_index_0_src_true_lang-d8fdefc2.js";
function P(e) {
  return (
    "function" == typeof e ||
    ("[object Object]" === Object.prototype.toString.call(e) && !w(e))
  );
}
const R = o({
  __name: "TelephoneCodeForm",
  emits: ["to-password"],
  setup(o, { emit: w }) {
    const { formRegister: R, formMethods: _ } = e(),
      { getFormData: I, getElFormExpose: S } = _,
      { t: C } = s(),
      { required: E } = k(),
      { currentRoute: F, addRoute: q, push: M } = a(),
      A = l(),
      L = r(),
      { setStorage: N } = y(),
      O = i([
        {
          field: "title",
          colProps: { span: 24 },
          formItemProps: {
            slots: {
              default: () =>
                p("h2", { class: "text-2xl font-bold text-center w-[100%]" }, [
                  C("login.login"),
                ]),
            },
          },
        },
        {
          field: "telephone",
          label: C("login.telephone"),
          value: "",
          component: "Input",
          colProps: { span: 24 },
          componentProps: {
            style: { width: "100%" },
            placeholder: C("login.telephonePlaceholder"),
            maxlength: 11,
          },
        },
        {
          field: "password",
          label: C("login.SMSCode"),
          colProps: { span: 24 },
          formItemProps: {
            slots: {
              default: (e) =>
                p("div", { class: "w-[100%] flex" }, [
                  p(
                    x,
                    {
                      modelValue: e.password,
                      "onUpdate:modelValue": (t) => (e.password = t),
                      placeholder: C("login.codePlaceholder"),
                    },
                    {
                      suffix: () => {
                        let e;
                        return p(n, null, [
                          p(b, { direction: "vertical" }, null),
                          G.value
                            ? p(
                                d,
                                { type: "primary", link: !0, onClick: J },
                                P((e = C("login.getSMSCode")))
                                  ? e
                                  : { default: () => [e] },
                              )
                            : p(
                                d,
                                {
                                  type: "primary",
                                  disabled: !G.value,
                                  link: !0,
                                },
                                {
                                  default: () => [
                                    H.value + C("login.SMSCodeRetry"),
                                  ],
                                },
                              ),
                        ]);
                      },
                    },
                  ),
                ]),
            },
          },
        },
        {
          field: "method",
          label: "登录类型",
          value: "1",
          component: "Input",
          hidden: !0,
        },
        {
          field: "login",
          colProps: { span: 24 },
          formItemProps: {
            slots: {
              default: () => {
                let e, t;
                return p("div", { class: "w-[100%]" }, [
                  p("div", { class: "w-[100%]" }, [
                    p(
                      d,
                      {
                        type: "primary",
                        class: "w-[100%]",
                        loading: D.value,
                        onClick: B,
                      },
                      P((e = C("login.login"))) ? e : { default: () => [e] },
                    ),
                  ]),
                  p("div", { class: "w-[100%] mt-15px" }, [
                    p(
                      d,
                      { class: "w-[100%]", onClick: z },
                      P((t = C("login.passwordLogin")))
                        ? t
                        : { default: () => [t] },
                    ),
                  ]),
                ]);
              },
            },
          },
        },
      ]),
      V = { telephone: [E()], method: [E()], password: [E()] },
      z = () => {
        w("to-password");
      },
      D = c(!1),
      K = c("");
    u(
      () => F.value,
      (e) => {
        var t;
        K.value =
          null == (t = null == e ? void 0 : e.query) ? void 0 : t.redirect;
      },
      { immediate: !0 },
    );
    const B = async () => {
      const e = await S();
      if (await (null == e ? void 0 : e.validate())) {
        D.value = !0;
        const e = await I();
        try {
          const t = await L.login(e);
          t
            ? t.data.is_reset_password
              ? Q()
              : M({ path: "/reset/password" })
            : (D.value = !1);
        } catch (t) {
          D.value = !1;
        }
      }
    };
    let G = c(!0),
      H = c(60);
    const J = async () => {
        const e = await S();
        if (await (null == e ? void 0 : e.validateField("telephone"))) {
          ((G.value = !1), (H.value = 60));
          const e = await I();
          try {
            const t = await m({ telephone: e.telephone });
            if (null == t ? void 0 : t.data) {
              let e = setInterval(() => {
                (H.value--, H.value < 1 && ((G.value = !0), clearInterval(e)));
              }, 1e3);
            } else (v.error("发送失败，请联系管理员"), (G.value = !0));
          } catch (t) {
            G.value = !0;
          }
        }
      },
      Q = async () => {
        const e = await f();
        if (e) {
          const t = e.data || [];
          (N("roleRouters", t),
            await A.generateRoutes(t).catch(() => {}),
            A.getAddRouters.forEach((e) => {
              q(e);
            }),
            A.setIsAddRouters(!0),
            M({ path: K.value || A.addRouters[0].path }));
        }
      };
    return (e, o) => (
      g(),
      h(
        j(t),
        {
          schema: O,
          rules: V,
          "label-position": "top",
          "hide-required-asterisk": "",
          size: "large",
          class:
            "dark:border-1 dark:border-[var(--el-border-color)] dark:border-solid",
          onRegister: j(R),
        },
        null,
        8,
        ["schema", "onRegister"],
      )
    );
  },
});
export { R as default };
