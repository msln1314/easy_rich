import { b3 as o } from './index-820a519e.js'
const a =
  (...a) =>
  (r) => {
    a.forEach((a) => {
      o(a) ? a(r) : (a.value = r)
    })
  }
export { a as c }
