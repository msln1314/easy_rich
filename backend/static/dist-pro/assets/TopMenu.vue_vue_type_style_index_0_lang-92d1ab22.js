import {
  e as a,
  ad as e,
  o as s,
  j as n,
  x as t,
  m,
  a1 as i,
  a5 as u,
  l as r,
  k as d,
  M as o,
  z as l,
} from "./index-6b60d190.js";
import { W as p, b as _ } from "./datav-vue3.es-6b3b0f04.js";
const v = { class: "top-menu-view" },
  c = { key: 1 },
  f = a({
    __name: "TopMenu",
    props: { menus: { type: Array, required: !0 }, activeIndex: e.number },
    setup(a) {
      const e = a;
      return (a, f) => (
        s(),
        n("div", v, [
          t(d(_), null, {
            default: m(() => [
              (s(!0),
              n(
                i,
                null,
                u(
                  e.menus,
                  (a, t) => (
                    s(),
                    n("div", { class: "menu-item-view", key: t }, [
                      t === e.activeIndex
                        ? (s(),
                          r(
                            d(p),
                            {
                              key: 0,
                              class: "animate__animated animate__fadeInDown",
                            },
                            { default: m(() => [o(l(a), 1)]), _: 2 },
                            1024,
                          ))
                        : (s(), n("span", c, l(a), 1)),
                    ])
                  ),
                ),
                128,
              )),
            ]),
            _: 1,
          }),
        ])
      );
    },
  });
export { f as _ };
