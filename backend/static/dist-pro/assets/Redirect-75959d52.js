import { e, A as t, k as r, o as a, j as s } from "./index-6b60d190.js";
const p = e({
  __name: "Redirect",
  setup(e) {
    const { currentRoute: p, replace: o } = t(),
      { params: c, query: n } = r(p),
      { path: i, _redirect_type: y = "path" } = c;
    (Reflect.deleteProperty(c, "_redirect_type"),
      Reflect.deleteProperty(c, "path"));
    const d = Array.isArray(i) ? i.join("/") : i;
    return (
      o(
        "name" === y
          ? { name: d, query: n, params: c }
          : { path: d.startsWith("/") ? d : "/" + d, query: n },
      ),
      (e, t) => (a(), s("div"))
    );
  },
});
export { p as default };
