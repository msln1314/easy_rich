import { U as s } from './index-820a519e.js'
const t = (t) => s.get({ url: '/system/depts', params: t }),
  e = (t) => s.delete({ url: '/system/depts', data: t }),
  a = (t) => s.post({ url: '/system/depts', data: t }),
  p = (t) => s.put({ url: `/system/depts/${t.id}`, data: t }),
  d = () => s.get({ url: '/system/depts/tree/options' }),
  r = () => s.get({ url: '/system/depts/user/tree/options' })
export { a, d as b, r as c, e as d, t as g, p }
