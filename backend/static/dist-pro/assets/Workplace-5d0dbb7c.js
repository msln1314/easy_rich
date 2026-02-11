import {
  U as a,
  e as t,
  V as s,
  r as e,
  L as l,
  f as c,
  o as r,
  j as n,
  y as o,
  x as i,
  m as p,
  k as d,
  z as m,
  W as x,
  X as u,
  Y as g,
  I as v,
} from "./index-6b60d190.js";
import { a as f, E as j } from "./el-col-b8aa0d1a.js";
import { E as w } from "./el-skeleton-item-298f4c82.js";
import { E as y } from "./el-card-37d6f3c4.js";
import { a as h } from "./avatar-d437f563.js";
const b = { class: "bg-[var(--app-content-bg-color)] flex-grow" },
  k = { class: "flex items-center" },
  _ = ["src"],
  O = { class: "text-20px" },
  E = { class: "mt-10px text-14px text-gray-500" },
  W = { class: "flex h-70px items-center justify-end <sm:mt-20px" },
  D = { class: "px-8px text-right" },
  U = o(
    "div",
    { class: "text-14px text-gray-400 mb-20px" },
    "最近登录时间",
    -1,
  ),
  z = { class: "text-20px" },
  I = t({
    name: "DashboardWorkplace",
    __name: "Workplace",
    setup(t) {
      const I = s(),
        L = e(!0);
      let P = l([]);
      const V = async () => {
        const t = await a.get({ url: "/workplace/project" }).catch(() => {});
        t && (P = Object.assign(P, t.data));
      };
      let X = l([]);
      (async () => {
        const t = await a.get({ url: "/workplace/shortcuts" }).catch(() => {});
        t && (X = Object.assign(X, t.data));
      })();
      let Y = l([]);
      const q = async () => {
        const t = await a.get({ url: "/workplace/dynamic" }).catch(() => {});
        t && (Y = Object.assign(Y, t.data));
      };
      let A = l([]);
      const B = async () => {
        const t = await a.get({ url: "/workplace/team" }).catch(() => {});
        t && (A = Object.assign(A, t.data));
      };
      (async () => {
        (await Promise.all([V(), q(), B()]), (L.value = !1));
      })();
      const { t: C } = v(),
        F = c(() => I.getUser);
      return (a, t) => (
        r(),
        n("div", b, [
          o("div", null, [
            i(
              d(y),
              { shadow: "never" },
              {
                default: p(() => [
                  i(
                    d(w),
                    { loading: L.value, animated: "" },
                    {
                      default: p(() => [
                        i(
                          d(f),
                          { gutter: 20, justify: "space-between" },
                          {
                            default: p(() => [
                              i(
                                d(j),
                                { xl: 12, lg: 12, md: 12, sm: 24, xs: 24 },
                                {
                                  default: p(() => [
                                    o("div", k, [
                                      o(
                                        "img",
                                        {
                                          src: F.value.avatar
                                            ? F.value.avatar
                                            : d(h),
                                          alt: "",
                                          class:
                                            "w-70px h-70px rounded-[50%] mr-20px",
                                        },
                                        null,
                                        8,
                                        _,
                                      ),
                                      o("div", null, [
                                        o(
                                          "div",
                                          O,
                                          m(d(x)()) +
                                            "，" +
                                            m(F.value.name) +
                                            "，" +
                                            m(d(C)("workplace.happyDay")),
                                          1,
                                        ),
                                        o(
                                          "div",
                                          E,
                                          m(d(u)()) + "，" + m(d(g)()),
                                          1,
                                        ),
                                      ]),
                                    ]),
                                  ]),
                                  _: 1,
                                },
                              ),
                              i(
                                d(j),
                                { xl: 12, lg: 12, md: 12, sm: 24, xs: 24 },
                                {
                                  default: p(() => {
                                    var a;
                                    return [
                                      o("div", W, [
                                        o("div", D, [
                                          U,
                                          o(
                                            "span",
                                            z,
                                            m(
                                              null == (a = F.value.last_login)
                                                ? void 0
                                                : a.split(" ")[0],
                                            ),
                                            1,
                                          ),
                                        ]),
                                      ]),
                                    ];
                                  }),
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
                    ["loading"],
                  ),
                ]),
                _: 1,
              },
            ),
          ]),
        ])
      );
    },
  });
export { I as default };
