import { U as s } from './index-820a519e.js'
const e = (e) => s.get({ url: '/system/roles', params: e }),
  t = (e) => s.post({ url: '/system/roles', data: e }),
  a = (e) => s.delete({ url: '/system/roles', data: e }),
  r = (e) => s.put({ url: `/system/roles/${e.id}`, data: e }),
  l = (e) => s.get({ url: `/system/roles/${e}` }),
  o = () => s.get({ url: '/system/roles/options' })
export { e as a, t as b, o as c, a as d, l as g, r as p }
