import {
  e,
  r as a,
  a2 as s,
  o as l,
  j as o,
  y as t,
  x as r,
  m as n,
  k as d,
  al as c,
  a1 as i
} from './index-820a519e.js'
import { E as p } from './el-tree-8dac9473.js'
import './el-checkbox-77b6829c.js'
import { E as m } from './el-input-5ae17c8f.js'
import { b as u } from './dept-b8a01226.js'
const f = { class: 'head-container' },
  h = { class: 'head-container' },
  k = e({
    name: 'SystemUserDeptTree',
    __name: 'DeptTree',
    emits: ['node-click'],
    setup(e, { emit: k }) {
      const x = a(''),
        y = a([]),
        j = a(),
        v = (e, a) => !e || a.label.includes(e),
        _ = async (e) => {
          k('node-click', e)
        }
      return (
        s(async () => {
          await (async () => {
            const e = await u()
            y.value = e.data
          })()
        }),
        (e, a) => (
          l(),
          o(
            i,
            null,
            [
              t('div', f, [
                r(
                  d(m),
                  {
                    modelValue: x.value,
                    'onUpdate:modelValue': a[0] || (a[0] = (e) => (x.value = e)),
                    class: 'mb-20px',
                    clearable: '',
                    placeholder: '请输入部门名称'
                  },
                  { prefix: n(() => [r(d(c), { icon: 'ep:search' })]), _: 1 },
                  8,
                  ['modelValue']
                )
              ]),
              t('div', h, [
                r(
                  d(p),
                  {
                    ref_key: 'treeRef',
                    ref: j,
                    data: y.value,
                    'expand-on-click-node': !1,
                    'filter-node-method': v,
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
export { k as _ }
