import {
  e,
  r as a,
  a2 as s,
  o as l,
  j as o,
  y as t,
  x as r,
  m as n,
  k as d,
  al as c,
  a1 as i,
} from "./index-6b60d190.js";
import { E as p } from "./el-tree-84af12f2.js";
import "./el-checkbox-4903f610.js";
import { E as m } from "./el-input-38d674e5.js";
import { b as u } from "./dept-7c279e0e.js";
const f = { class: "head-container" },
  h = { class: "head-container" },
  k = e({
    name: "SystemUserDeptTree",
    __name: "DeptTree",
    emits: ["node-click"],
    setup(e, { emit: k }) {
      const x = a(""),
        y = a([]),
        j = a(),
        v = (e, a) => !e || a.label.includes(e),
        b = async (e) => {
          k("node-click", e);
        };
      return (
        s(async () => {
          await (async () => {
            const e = await u();
            y.value = e.data;
          })();
        }),
        (e, a) => (
          l(),
          o(
            i,
            null,
            [
              t("div", f, [
                r(
                  d(m),
                  {
                    modelValue: x.value,
                    "onUpdate:modelValue":
                      a[0] || (a[0] = (e) => (x.value = e)),
                    class: "mb-20px",
                    clearable: "",
                    placeholder: "请输入部门名称",
                  },
                  { prefix: n(() => [r(d(c), { icon: "ep:search" })]), _: 1 },
                  8,
                  ["modelValue"],
                ),
              ]),
              t("div", h, [
                r(
                  d(p),
                  {
                    ref_key: "treeRef",
                    ref: j,
                    data: y.value,
                    "expand-on-click-node": !1,
                    "filter-node-method": v,
                    props: e.defaultProps,
                    "default-expand-all": "",
                    "highlight-current": "",
                    "node-key": "id",
                    onNodeClick: b,
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
export { k as _ };
