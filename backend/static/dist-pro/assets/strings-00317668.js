import { c0 as e } from "./index-6b60d190.js";
const a = (e = "") =>
    e.replace(/[|\\{}()[\]^$+*?.]/g, "\\$&").replace(/-/g, "\\x2d"),
  c = (a) => e(a);
export { c, a as e };
