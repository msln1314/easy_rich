import { U as t } from './index-820a519e.js'
const o = (o) => t.get({ url: '/iot/client_groups', params: o }),
  s = (o) => t.delete({ url: '/iot/client_groups', data: o }),
  a = (o) => t.post({ url: '/iot/client_groups', data: o }),
  r = (o) => t.put({ url: `/iot/client_groups/${o.id}`, data: o }),
  e = () => t.get({ url: '/iot/client_groups/tree/options' })
export { o as a, a as b, s as d, e as g, r as p }
