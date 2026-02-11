import { U as e } from './index-820a519e.js'
const t = (t) => e.get({ url: '/iot/devices', params: t }),
  s = (t) => e.post({ url: '/iot/devices', data: t }),
  a = (t) => e.delete({ url: '/iot/devices', data: t }),
  i = (t) => e.put({ url: `/iot/devices/${t.id}`, data: t }),
  o = (t) => e.get({ url: `/iot/devices/${t}` }),
  d = (t, s) => e.post({ url: '/iot/devices/export/query/list/to/excel', params: t, data: s }),
  r = (t) => e.get({ url: '/iot/devices/options', params: t })
export { o as a, t as b, s as c, a as d, i as e, r as g, d as p }
