import { U as s } from './index-820a519e.js'
const t = (t) => s.get({ url: '/system/tasks', params: t }),
  a = (t) => s.post({ url: '/system/tasks', data: t }),
  e = (t) => s.delete({ url: `/system/tasks?_id=${t}` }),
  r = (t, a) => s.put({ url: `/system/tasks?_id=${t}`, data: a }),
  m = (t) => s.get({ url: `/system/task?_id=${t}` }),
  d = () => s.get({ url: '/system/task/group/options' }),
  o = (t) => s.get({ url: '/system/task/records', params: t }),
  p = (t) => s.post({ url: `/system/task?_id=${t}` })
export { m as a, t as b, a as c, e as d, d as e, o as g, r as p, p as r }
