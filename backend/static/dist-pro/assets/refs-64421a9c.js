import { b3 as o } from "./index-6b60d190.js";
const a =
  (...a) =>
  (r) => {
    a.forEach((a) => {
      o(a) ? a(r) : (a.value = r);
    });
  };
export { a as c };
