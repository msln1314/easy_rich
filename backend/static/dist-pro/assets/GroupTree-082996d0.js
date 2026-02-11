import {
  e,
  r as a,
  a2 as s,
  o as l,
  j as o,
  y as r,
  x as t,
  m as i,
  k as n,
  al as d,
  a1 as c,
} from "./index-6b60d190.js";
import { E as p } from "./el-tree-84af12f2.js";
import "./el-checkbox-4903f610.js";
import { E as m } from "./el-input-38d674e5.js";
import { g as u } from "./client_group-caf4c37c.js";
import "./index-55fef7b1.js";
import "./event-5568c9d8.js";
import "./isEqual-b8d86c27.js";
import "./isNil-1f22f7b0.js";
const f = { class: "head-container" },
  j = { class: "head-container" },
  x = e({
    name: "IotClientGroupTree",
    __name: "GroupTree",
    emits: ["node-click"],
    setup(e, { emit: x }) {
      const h = a(""),
        k = a([]),
        v = a(),
        y = (e, a) => !e || a.label.includes(e),
        _ = async (e) => {
          x("node-click", e);
        };
      return (
        s(async () => {
          await (async () => {
            const e = await u();
            k.value = e.data;
          })();
        }),
        (e, a) => (
          l(),
          o(
            c,
            null,
            [
              r("div", f, [
                t(
                  n(m),
                  {
                    modelValue: h.value,
                    "onUpdate:modelValue":
                      a[0] || (a[0] = (e) => (h.value = e)),
                    class: "mb-20px",
                    clearable: "",
                    placeholder: "请输入分组名称",
                  },
                  { prefix: i(() => [t(n(d), { icon: "ep:search" })]), _: 1 },
                  8,
                  ["modelValue"],
                ),
              ]),
              r("div", j, [
                t(
                  n(p),
                  {
                    ref_key: "treeRef",
                    ref: v,
                    data: k.value,
                    "expand-on-click-node": !1,
                    "filter-node-method": y,
                    props: e.defaultProps,
                    "default-expand-all": "",
                    "highlight-current": "",
                    "node-key": "id",
                    onNodeClick: _,
                  },
                  null,
                  8,
                  ["data", "props"],
                ),
              ]),
            ],
            64,
          )
        )
      );
    },
  });
export { x as default };
