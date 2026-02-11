import { u as e, _ as t } from './Table.vue_vue_type_script_lang-a0f5d3d3.js'
import {
  e as s,
  I as a,
  A as l,
  r as o,
  L as i,
  x as r,
  a1 as p,
  N as n,
  M as m,
  o as d,
  j as u,
  m as c,
  k as j,
  ai as _,
  z as g,
  l as v,
  F as f
} from './index-820a519e.js'
import { _ as b } from './Search.vue_vue_type_script_setup_true_lang-9de3bdd5.js'
import { _ as h } from './ContentWrap.vue_vue_type_script_setup_true_lang-37d6ee07.js'
import { _ as w } from './Detail.vue_vue_type_script_setup_true_lang-1876cf86.js'
import { _ as x } from './Dialog.vue_vue_type_style_index_0_lang-ce349c68.js'
import { s as y } from './dict-4a6e55e6.js'
import { u as k } from './dict-451afacd.js'
import { g as R } from './task-7432fb5b.js'
import './el-message-box-faa52860.js'
import './el-input-5ae17c8f.js'
import './event-5568c9d8.js'
import './isNil-1f22f7b0.js'
import './el-overlay-34b9d092.js'
import './scroll-ac7d0423.js'
import './vnode-06a99f10.js'
import './useForm-c59a8d29.js'
import './el-form-item-2e860f96.js'
import './el-col-beabe3f6.js'
import './el-tooltip-4ed993c7.js'
import './el-popper-797844d6.js'
import './focus-trap-949626e0.js'
/* empty css               */ import './el-checkbox-77b6829c.js'
import './isEqual-cb9e370d.js'
/* empty css                          */ import './el-date-picker-6b1a21d2.js'
import './dayjs.min-e5ba30ae.js'
import './debounce-5bc596c6.js'
import './index-eb31d854.js'
import './el-radio-group-4cb40939.js'
import './el-select-38080147.js'
import './index-56bc6266.js'
import './strings-ed83d626.js'
import './validator-a9d8fe4c.js'
import './el-switch-6f4f5b6a.js'
import './el-divider-9c19755b.js'
import './el-tree-8dac9473.js'
import './index-55f4d4a6.js'
import './el-progress-97dbc0fb.js'
import './style.css_vue_type_style_index_0_src_true_lang-4a035adc.js'
import './index-2b3f7e71.js'
import './el-table-column-36e57984.js'
import './el-pagination-60eda460.js'
import './dropdown-394a0a1a.js'
import './el-image-viewer-73f400a0.js'
import './el-dropdown-item-a41cbdee.js'
import './refs-374e9e51.js'
/* empty css                   */ import './_Uint8Array-48df3306.js'
import './useIcon-24caadfc.js'
import './el-card-06c161d4.js'
import './Descriptions-7c861960.js'
import './el-descriptions-item-6ddb822e.js'
/* empty css              */ import './use-dialog-2de816dc.js'
import './dict-c8c7fcf4.js'
const z = s({
  name: 'SystemRecordTask',
  __name: 'Task',
  setup(s) {
    const { t: z } = a(),
      { currentRoute: D } = l(),
      S = D.value.query.job_id,
      I = o([])
    ;(async () => {
      const e = k(),
        t = await e.getDictObj(['vadmin_system_task_exec_strategy'])
      I.value = t.vadmin_system_task_exec_strategy
    })()
    const {
        tableRegister: P,
        tableState: A,
        tableMethods: U
      } = e({
        immediate: !1,
        fetchDataApi: async () => {
          const { pageSize: e, currentPage: t } = A,
            s = await R({ page: j(t), limit: j(e), ...j(E) })
          return { list: s.data || [], total: s.count || 0 }
        }
      }),
      { dataList: C, loading: L, total: M, pageSize: N, currentPage: T } = A,
      { getList: V } = U,
      q = i([
        { field: 'job_id', label: '任务编号', show: !0, disabled: !0, width: '240px' },
        { field: 'name', label: '任务名称', show: !0, disabled: !0 },
        { field: 'group', label: '任务分组', show: !0, span: 2 },
        { field: 'job_class', label: '调用目标', show: !0 },
        {
          field: 'exec_strategy',
          label: '执行策略',
          show: !0,
          slots: {
            default: (e) => {
              const t = e.row
              return r(p, null, [r('div', null, [y(I.value, t.exec_strategy)])])
            }
          }
        },
        { field: 'expression', label: '表达式', show: !0, span: 24 },
        { field: 'start_time', label: '开始执行时间', show: !1, width: '200px' },
        { field: 'end_time', label: '执行完成时间', width: '200px', show: !0 },
        { field: 'process_time', label: '耗时(秒)', width: '110px', show: !0 },
        { field: 'retval', label: '任务返回值', show: !0 },
        { field: 'exception', label: '异常信息', show: !1, span: 24 },
        { field: 'traceback', label: '堆栈跟踪', show: !1, width: '100px' },
        {
          field: 'action',
          width: '100px',
          label: '操作',
          show: !0,
          disabled: !0,
          slots: {
            default: (e) => {
              const t = e.row
              return r(p, null, [
                r(
                  n,
                  { type: 'primary', link: !0, size: 'small', onClick: () => G(t) },
                  { default: () => [m('详情')] }
                )
              ])
            }
          }
        }
      ]),
      F = i([
        {
          field: 'job_id',
          label: '任务编号',
          component: 'Input',
          componentProps: { clearable: !0, style: { width: '240px' } },
          value: S
        },
        { field: 'name', label: '任务名称', component: 'Input', componentProps: { clearable: !0 } }
      ]),
      E = o({}),
      H = (e) => {
        ;((T.value = 1), (E.value = e), V())
      },
      K = o(!1),
      O = o(''),
      W = o(),
      B = o(''),
      G = (e) => {
        ;((O.value = z('exampleDemo.detail')), (B.value = 'detail'), (W.value = e), (K.value = !0))
      }
    return (
      S ? ((E.value = { job_id: S }), V()) : V(),
      (e, s) => (
        d(),
        u(
          p,
          null,
          [
            r(j(h), null, {
              default: c(() => [
                r(j(b), { schema: F, onReset: H, onSearch: H }, null, 8, ['schema']),
                r(
                  j(t),
                  {
                    'current-page': j(T),
                    'onUpdate:currentPage': s[0] || (s[0] = (e) => (_(T) ? (T.value = e) : null)),
                    'page-size': j(N),
                    'onUpdate:pageSize': s[1] || (s[1] = (e) => (_(N) ? (N.value = e) : null)),
                    showAction: '',
                    columns: q,
                    'node-key': 'id',
                    data: j(C),
                    loading: j(L),
                    pagination: { total: j(M) },
                    onRegister: j(P),
                    onRefresh: j(V)
                  },
                  null,
                  8,
                  [
                    'current-page',
                    'page-size',
                    'columns',
                    'data',
                    'loading',
                    'pagination',
                    'onRegister',
                    'onRefresh'
                  ]
                )
              ]),
              _: 1
            }),
            r(
              j(x),
              {
                modelValue: K.value,
                'onUpdate:modelValue': s[3] || (s[3] = (e) => (K.value = e)),
                title: O.value,
                width: '800px'
              },
              {
                footer: c(() => [
                  r(
                    j(n),
                    { onClick: s[2] || (s[2] = (e) => (K.value = !1)) },
                    { default: c(() => [m(g(j(z)('dialogDemo.close')), 1)]), _: 1 }
                  )
                ]),
                default: c(() => [
                  'detail' === B.value
                    ? (d(), v(w, { key: 0, 'current-row': W.value }, null, 8, ['current-row']))
                    : f('', !0)
                ]),
                _: 1
              },
              8,
              ['modelValue', 'title']
            )
          ],
          64
        )
      )
    )
  }
})
export { z as default }
