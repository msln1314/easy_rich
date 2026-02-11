import {
  e,
  r as a,
  a2 as s,
  o as l,
  j as o,
  y as t,
  x as r,
  m as i,
  k as n,
  al as d,
  a1 as c
} from './index-820a519e.js'
import { E as p } from './el-tree-8dac9473.js'
import './el-checkbox-77b6829c.js'
import { E as m } from './el-input-5ae17c8f.js'
import { g as u } from './client_group-aeb78440.js'
import './index-55f4d4a6.js'
import './event-5568c9d8.js'
import './isEqual-cb9e370d.js'
import './isNil-1f22f7b0.js'
const f = { class: 'head-container' },
  j = { class: 'head-container' },
  h = e({
    name: 'IotClientGroupTree',
    __name: 'GroupTree',
    emits: ['node-click'],
    setup(e, { emit: h }) {
      const x = a(''),
        k = a([]),
        v = a(),
        y = (e, a) => !e || a.label.includes(e),
        _ = async (e) => {
          h('node-click', e)
        }
      return (
        s(async () => {
          await (async () => {
            const e = await u()
            k.value = e.data
          })()
        }),
        (e, a) => (
          l(),
          o(
            c,
            null,
            [
              t('div', f, [
                r(
                  n(m),
                  {
                    modelValue: x.value,
                    'onUpdate:modelValue': a[0] || (a[0] = (e) => (x.value = e)),
                    class: 'mb-20px',
                    clearable: '',
                    placeholder: '请输入分组名称'
                  },
                  { prefix: i(() => [r(n(d), { icon: 'ep:search' })]), _: 1 },
                  8,
                  ['modelValue']
                )
              ]),
              t('div', j, [
                r(
                  n(p),
                  {
                    ref_key: 'treeRef',
                    ref: v,
                    data: k.value,
                    'expand-on-click-node': !1,
                    'filter-node-method': y,
                    props: e.defaultProps,
                    'default-expand-all': '',
                    'highlight-current': '',
                    'node-key': 'id',
                    onNodeClick: _
                  },
                  null,
                  8,
                  ['data', 'props']
                )
              ])
            ],
            64
          )
        )
      )
    }
  })
export { h as default }
