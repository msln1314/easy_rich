import { c0 as e } from './index-820a519e.js'
const a = (e = '') => e.replace(/[|\\{}()[\]^$+*?.]/g, '\\$&').replace(/-/g, '\\x2d'),
  c = (a) => e(a)
export { c, a as e }
