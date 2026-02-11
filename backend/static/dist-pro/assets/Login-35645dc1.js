import {
  e as t,
  B as e,
  r as s,
  f as a,
  o as l,
  j as i,
  x as r,
  m as o,
  y as p,
  s as m,
  k as x,
  z as n,
  C as c,
  T as d,
  D as u,
  l as j,
  F as _,
  G as g,
  H as v,
  I as f,
  J as h,
} from "./index-6b60d190.js";
import { _ as w } from "./LoginForm.vue_vue_type_script_setup_true_lang-58e61ebd.js";
import "./useForm-b6ceb895.js";
import "./el-input-38d674e5.js";
import "./el-divider-2dd0a1ee.js";
import "./useValidator-63200dcb.js";
import {
  T as y,
  _ as b,
} from "./LocaleDropdown.vue_vue_type_script_setup_true_lang-1e29b4aa.js";
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
import "./useIcon-7641a992.js";
import "./el-dropdown-item-943c2eb7.js";
import "./dropdown-84a04b2c.js";
import "./refs-64421a9c.js";
const k = { class: "relative flex mx-auto min-h-100vh" },
  I = { class: "flex items-center relative text-white" },
  L = ["src"],
  T = { class: "text-20px font-bold" },
  F = { class: "flex justify-center items-center h-[calc(100%-60px)]" },
  C = { class: "text-3xl text-white", key: "2" },
  D = { class: "mt-5 font-normal text-white text-14px", key: "3" },
  q = {
    class:
      "p-30px bg-opacity-20 lt-sm:p-10px dark:bg-[var(--login-bg-color)] relative",
  },
  z = {
    class:
      "flex justify-between items-center text-white at-2xl:justify-end at-xl:justify-end",
  },
  B = { class: "flex items-center at-2xl:hidden at-xl:hidden" },
  E = ["src"],
  G = { class: "text-20px font-bold" },
  H = { class: "flex justify-end items-center space-x-10px" },
  J = {
    class:
      "h-full flex items-center m-auto w-[100%] at-2xl:max-w-500px at-xl:max-w-500px at-md:max-w-500px at-lg:max-w-500px",
  },
  N = h(
    t({
      __name: "Login",
      setup(t) {
        const { getPrefixCls: h } = v(),
          N = h("login"),
          P = e(),
          { t: R } = f(),
          V = s(!0),
          A = a(() => P.getLogoImage),
          K = () => {
            V.value = !1;
          };
        return (t, e) => (
          l(),
          i(
            "div",
            {
              class: m([
                x(N),
                "h-[100%] relative lt-xl:bg-[var(--login-bg-color)] lt-sm:px-10px lt-xl:px-10px lt-md:px-10px",
              ]),
            },
            [
              r(
                x(g),
                { class: "h-full" },
                {
                  default: o(() => [
                    p("div", k, [
                      p(
                        "div",
                        {
                          class: m(
                            `${x(N)}__left flex-1 bg-gray-500 bg-opacity-20 relative p-30px lt-xl:hidden`,
                          ),
                        },
                        [
                          p("div", I, [
                            p(
                              "img",
                              {
                                src: A.value,
                                alt: "",
                                class: "w-48px h-48px mr-10px",
                              },
                              null,
                              8,
                              L,
                            ),
                            p("span", T, n(x(c)(x(P).getTitle)), 1),
                          ]),
                          p("div", F, [
                            r(
                              d,
                              {
                                appear: "",
                                tag: "div",
                                "enter-active-class":
                                  "animate__animated animate__bounceInLeft",
                              },
                              {
                                default: o(() => [
                                  p("div", C, n(x(R)("login.welcome")), 1),
                                  p("div", D, n(x(R)("login.message")), 1),
                                ]),
                                _: 1,
                              },
                            ),
                          ]),
                        ],
                        2,
                      ),
                      p("div", q, [
                        p("div", z, [
                          p("div", B, [
                            p(
                              "img",
                              {
                                src: A.value,
                                alt: "",
                                class: "w-48px h-48px mr-10px",
                              },
                              null,
                              8,
                              E,
                            ),
                            p("span", G, n(x(c)(x(P).getTitle)), 1),
                          ]),
                          p("div", H, [
                            r(x(y)),
                            r(x(b), {
                              class: "lt-xl:text-white dark:text-white",
                            }),
                          ]),
                        ]),
                        r(
                          u,
                          {
                            appear: "",
                            "enter-active-class":
                              "animate__animated animate__bounceInRight",
                          },
                          {
                            default: o(() => [
                              p("div", J, [
                                V.value
                                  ? (l(),
                                    j(x(w), {
                                      key: 0,
                                      class:
                                        "p-20px h-auto m-auto lt-xl:rounded-3xl lt-xl:light:bg-white",
                                      onToTelephone: K,
                                    }))
                                  : _("", !0),
                              ]),
                            ]),
                            _: 1,
                          },
                        ),
                      ]),
                    ]),
                  ]),
                  _: 1,
                },
              ),
            ],
            2,
          )
        );
      },
    }),
    [["__scopeId", "data-v-47e86f55"]],
  );
export { N as default };
