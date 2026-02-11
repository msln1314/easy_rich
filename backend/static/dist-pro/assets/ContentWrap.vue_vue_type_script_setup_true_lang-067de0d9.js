import {
  e as s,
  ad as e,
  b1 as a,
  o as t,
  l,
  ak as o,
  m as r,
  y as i,
  z as n,
  k as p,
  x as c,
  F as d,
  q as f,
  s as m,
  H as x,
} from "./index-6b60d190.js";
import { E as g } from "./el-card-37d6f3c4.js";
import "./el-tooltip-4ed993c7.js";
import { E as u } from "./el-popper-09548d54.js";
const v = { class: "flex items-center" },
  h = { class: "text-16px font-700" },
  k = { class: "max-w-200px" },
  w = { class: "flex pl-20px flex-grow" },
  _ = s({
    __name: "ContentWrap",
    props: { title: e.string.def(""), message: e.string.def("") },
    setup(s) {
      const { getPrefixCls: e } = x(),
        _ = e("content-wrap");
      return (e, x) => {
        const j = a("Icon");
        return (
          t(),
          l(
            p(g),
            { class: m([[p(_)], "!b-0 h-[100%]"]), shadow: "never" },
            o(
              {
                default: r(() => [i("div", null, [f(e.$slots, "default")])]),
                _: 2,
              },
              [
                s.title
                  ? {
                      name: "header",
                      fn: r(() => [
                        i("div", v, [
                          i("span", h, n(s.title), 1),
                          s.message
                            ? (t(),
                              l(
                                p(u),
                                { key: 0, effect: "dark", placement: "right" },
                                {
                                  content: r(() => [
                                    i("div", k, n(s.message), 1),
                                  ]),
                                  default: r(() => [
                                    c(j, {
                                      class: "ml-5px",
                                      icon: "bi:question-circle-fill",
                                      size: 14,
                                    }),
                                  ]),
                                  _: 1,
                                },
                              ))
                            : d("", !0),
                          i("div", w, [f(e.$slots, "header")]),
                        ]),
                      ]),
                      key: "0",
                    }
                  : void 0,
              ],
            ),
            1032,
            ["class"],
          )
        );
      };
    },
  });
export { _ };
