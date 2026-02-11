import { U as t } from './index-820a519e.js'
const s = (s) => t.get({ url: '/system/dict/types', params: s }),
  e = (s) => t.post({ url: '/system/dict/types', data: s }),
  a = (s) => t.delete({ url: '/system/dict/types', data: s }),
  d = (s) => t.put({ url: `/system/dict/types/${s.id}`, data: s }),
  i = (s) => t.get({ url: `/system/dict/types/${s}` }),
  y = () => t.get({ url: '/system/dict/types/options' }),
  p = (s) => t.post({ url: '/system/dict/type/dicts', data: s }),
  r = (s) => t.get({ url: '/system/dict', params: s }),
  m = (s) => t.post({ url: '/system/dict', data: s }),
  c = (s) => t.delete({ url: '/system/dict', data: s }),
  l = (s) => t.put({ url: `/system/dict/${s.id}`, data: s }),
  u = (s) => t.get({ url: `/system/dict/${s}` })
export {
  u as a,
  r as b,
  m as c,
  c as d,
  y as e,
  i as f,
  p as g,
  s as h,
  a as i,
  e as j,
  d as k,
  l as p
}
