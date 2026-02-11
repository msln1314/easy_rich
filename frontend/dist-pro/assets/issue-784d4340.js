import { U as s } from './index-820a519e.js'
const e = (e) => s.get({ url: '/help/issue/categorys', params: e }),
  a = (e) => s.post({ url: '/help/issue/categorys', data: e }),
  t = (e) => s.delete({ url: '/help/issue/categorys', data: e }),
  l = (e) => s.put({ url: `/help/issue/categorys/${e.id}`, data: e }),
  u = (e) => s.get({ url: `/help/issue/categorys/${e}` }),
  r = () => s.get({ url: '/help/issue/categorys/options' }),
  p = (e) => s.get({ url: '/help/issues', params: e }),
  i = (e) => s.post({ url: '/help/issues', data: e }),
  o = (e) => s.delete({ url: '/help/issues', data: e }),
  d = (e) => s.put({ url: `/help/issues/${e.id}`, data: e }),
  g = (e) => s.get({ url: `/help/issues/${e}` })
export { r as a, i as b, g as c, o as d, u as e, e as f, p as g, t as h, a as i, l as j, d as p }
