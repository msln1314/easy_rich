import { a as e, r as a, b as t, d as l, c as s, p as i } from './task-7432fb5b.js'
import { u as o, _ as r } from './Table.vue_vue_type_script_lang-a0f5d3d3.js'
import {
  e as p,
  A as n,
  I as u,
  L as d,
  x as m,
  a1 as c,
  N as _,
  M as v,
  r as j,
  af as f,
  o as y,
  j as g,
  m as w,
  k as h,
  ai as b,
  z as x,
  l as k,
  F as C
} from './index-820a519e.js'
import { E as z } from './el-switch-6f4f5b6a.js'
import { a as P, E as R } from './el-col-beabe3f6.js'
import { E as S } from './el-message-box-faa52860.js'
import './el-input-5ae17c8f.js'
import './el-overlay-34b9d092.js'
import { _ as D } from './Search.vue_vue_type_script_setup_true_lang-9de3bdd5.js'
import { _ as E } from './ContentWrap.vue_vue_type_script_setup_true_lang-37d6ee07.js'
import { _ as A } from './Write.vue_vue_type_script_setup_true_lang-1a4ba76a.js'
import { _ as I } from './Dialog.vue_vue_type_style_index_0_lang-ce349c68.js'
import { _ as L } from './CronExpression.vue_vue_type_style_index_0_lang-f163e044.js'
import './el-table-column-36e57984.js'
import './el-popper-797844d6.js'
import './isNil-1f22f7b0.js'
import './focus-trap-949626e0.js'
import './isEqual-cb9e370d.js'
import './el-checkbox-77b6829c.js'
import './event-5568c9d8.js'
import './debounce-5bc596c6.js'
import './index-eb31d854.js'
import './el-tooltip-4ed993c7.js'
/* empty css               */ import './el-pagination-60eda460.js'
import './el-select-38080147.js'
import './index-56bc6266.js'
import './strings-ed83d626.js'
import './scroll-ac7d0423.js'
import './validator-a9d8fe4c.js'
import './dropdown-394a0a1a.js'
import './el-image-viewer-73f400a0.js'
import './useForm-c59a8d29.js'
import './el-form-item-2e860f96.js'
/* empty css                          */ import './el-date-picker-6b1a21d2.js'
import './dayjs.min-e5ba30ae.js'
import './el-radio-group-4cb40939.js'
import './el-divider-9c19755b.js'
import './el-tree-8dac9473.js'
import './index-55f4d4a6.js'
import './el-progress-97dbc0fb.js'
import './style.css_vue_type_style_index_0_src_true_lang-4a035adc.js'
import './el-dropdown-item-a41cbdee.js'
import './refs-374e9e51.js'
/* empty css                   */ import './_Uint8Array-48df3306.js'
import './index-2b3f7e71.js'
import './vnode-06a99f10.js'
import './useIcon-24caadfc.js'
import './el-card-06c161d4.js'
import './useValidator-db15330d.js'
import './dict-451afacd.js'
import './dict-c8c7fcf4.js'
import './use-dialog-2de816dc.js'
import './el-tab-pane-bc33a695.js'
import './RunDatetimeList-73d2c95a.js'
import './CronExample-1392a638.js'
import './el-descriptions-item-6ddb822e.js'
const T = p({
  name: 'SystemTask',
  __name: 'Task',
  setup(p) {
    const { push: T } = n(),
      { t: U } = u(),
      {
        tableRegister: V,
        tableState: N,
        tableMethods: B
      } = o({
        fetchDataApi: async () => {
          const { pageSize: e, currentPage: a } = N,
            l = await t({ page: h(a), limit: h(e), ...h(K) })
          return { list: l.data || [], total: l.count || 0 }
        },
        fetchDelApi: async (e) => 200 === (await l(e)).code
      }),
      { dataList: F, loading: M, total: W, pageSize: q, currentPage: O } = N,
      { getList: $, delList: G } = B,
      H = d([
        { field: '_id', label: '任务编号', show: !0, disabled: !0, width: '230px', span: 24 },
        { field: 'name', label: '任务名称', show: !0, disabled: !0, span: 24 },
        { field: 'group', label: '任务分组', show: !0, span: 24 },
        { field: 'job_class', label: '调用目标', show: !0, span: 24 },
        {
          field: 'exec_strategy',
          label: '执行策略',
          show: !0,
          colProps: { span: 24 },
          componentProps: { style: { width: '100%' } }
        },
        { field: 'expression', label: '表达式', show: !0, span: 24 },
        {
          field: 'is_active',
          label: '任务状态',
          show: !0,
          width: '100px',
          slots: {
            default: (e) => {
              const a = e.row
              return m(c, null, [m(z, { value: a.is_active, disabled: !0 }, null)])
            }
          }
        },
        {
          field: 'last_run_datetime',
          label: '最近一次执行时间',
          show: !0,
          width: '180px',
          span: 24
        },
        { field: 'remark', label: '任务备注', show: !0, span: 24 },
        { field: 'created_at', label: '创建时间', show: !0, width: '180px', span: 24 },
        {
          field: 'action',
          label: '操作',
          show: !0,
          disabled: !1,
          width: '240px',
          slots: {
            default: (e) => {
              const a = e.row
              return m(c, null, [
                m(
                  _,
                  { type: 'primary', link: !0, size: 'small', onClick: () => ie(a) },
                  { default: () => [v('编辑')] }
                ),
                m(
                  _,
                  { type: 'primary', link: !0, size: 'small', onClick: () => ne(a) },
                  { default: () => [v('调度日志')] }
                ),
                m(
                  _,
                  { type: 'primary', link: !0, size: 'small', onClick: () => ue(a) },
                  { default: () => [v('执行一次')] }
                ),
                m(
                  _,
                  { type: 'danger', link: !0, size: 'small', onClick: () => Y(a) },
                  { default: () => [v('删除')] }
                )
              ])
            }
          }
        }
      ]),
      J = d([
        {
          field: 'name',
          label: '任务名称',
          component: 'Input',
          componentProps: { clearable: !0, style: { width: '214px' } }
        },
        {
          field: '_id',
          label: '任务编号',
          component: 'Input',
          componentProps: { clearable: !0, style: { width: '214px' } }
        },
        {
          field: 'group',
          label: '任务分组',
          component: 'Select',
          componentProps: { style: { width: '214px' }, options: [] }
        }
      ]),
      K = j({}),
      Q = (e) => {
        ;((O.value = 1), (K.value = e), $())
      },
      X = j(!1),
      Y = async (e) => {
        ;((X.value = !0),
          await G(!0, [e._id]).finally(() => {
            X.value = !1
          }))
      },
      Z = j(!1),
      ee = j(''),
      ae = j(),
      te = j(''),
      le = j(),
      se = j(!1),
      ie = async (a) => {
        const t = await e(a._id)
        t && ((ee.value = '编辑定时任务'), (te.value = 'edit'), (ae.value = t.data), (Z.value = !0))
      },
      oe = () => {
        ;((ee.value = '新增定时任务'), (te.value = 'add'), (ae.value = void 0), (Z.value = !0))
      },
      re = async () => {
        const e = h(le),
          a = await (null == e ? void 0 : e.submit())
        if (a) {
          se.value = !0
          try {
            const e = j({})
            'add' === te.value
              ? ((e.value = await s(a)), e.value && ((Z.value = !1), $()))
              : 'edit' === te.value &&
                ((e.value = await i(a._id, a)), e.value && ((Z.value = !1), $()))
          } finally {
            se.value = !1
          }
        }
      },
      pe = () => {
        ;((ee.value = 'Cron 表达式'),
          (te.value = 'expression'),
          (ae.value = void 0),
          (Z.value = !0))
      },
      ne = (e) => {
        T(e ? `/record/task?job_id=${e._id}` : '/record/task')
      },
      ue = async (e) => {
        S.confirm('是否确认立即执行一次任务', '提示', {
          confirmButtonText: U('common.delOk'),
          cancelButtonText: U('common.delCancel'),
          type: 'warning'
        }).then(async () => {
          const t = await a(e._id)
          t &&
            (t.data > 0
              ? f.success('任务成功被消费者接收！')
              : f.error('执行失败，未有消费者接收任务，请检查定时任务程序状态！'))
        })
      }
    return (e, a) => (
      y(),
      g(
        c,
        null,
        [
          m(h(E), null, {
            default: w(() => [
              m(h(D), { schema: J, onReset: Q, onSearch: Q }, null, 8, ['schema']),
              m(
                h(r),
                {
                  'current-page': h(O),
                  'onUpdate:currentPage': a[1] || (a[1] = (e) => (b(O) ? (O.value = e) : null)),
                  'page-size': h(q),
                  'onUpdate:pageSize': a[2] || (a[2] = (e) => (b(q) ? (q.value = e) : null)),
                  showAction: '',
                  columns: H,
                  'default-expand-all': '',
                  'node-key': 'id',
                  data: h(F),
                  loading: h(M),
                  pagination: { total: h(W) },
                  onRegister: h(V),
                  onRefresh: h($)
                },
                {
                  toolbar: w(() => [
                    m(
                      h(P),
                      { gutter: 10 },
                      {
                        default: w(() => [
                          m(
                            h(R),
                            { span: 1.5 },
                            {
                              default: w(() => [
                                m(
                                  h(_),
                                  { type: 'primary', onClick: oe },
                                  { default: w(() => [v('新增定时任务')]), _: 1 }
                                )
                              ]),
                              _: 1
                            }
                          ),
                          m(
                            h(R),
                            { span: 1.5 },
                            {
                              default: w(() => [
                                m(
                                  h(_),
                                  { type: 'primary', onClick: a[0] || (a[0] = (e) => ne(null)) },
                                  { default: w(() => [v('调度日志')]), _: 1 }
                                )
                              ]),
                              _: 1
                            }
                          ),
                          m(
                            h(R),
                            { span: 1.5 },
                            {
                              default: w(() => [
                                m(
                                  h(_),
                                  { type: 'primary', onClick: pe },
                                  { default: w(() => [v('快速生成 Cron 表达式')]), _: 1 }
                                )
                              ]),
                              _: 1
                            }
                          )
                        ]),
                        _: 1
                      }
                    )
                  ]),
                  _: 1
                },
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
          m(
            h(I),
            {
              modelValue: Z.value,
              'onUpdate:modelValue': a[4] || (a[4] = (e) => (Z.value = e)),
              title: ee.value,
              height: 680,
              width: 850
            },
            {
              footer: w(() => [
                m(
                  h(_),
                  { type: 'primary', loading: se.value, onClick: re },
                  { default: w(() => [v(x(h(U)('exampleDemo.save')), 1)]), _: 1 },
                  8,
                  ['loading']
                ),
                m(
                  h(_),
                  { onClick: a[3] || (a[3] = (e) => (Z.value = !1)) },
                  { default: w(() => [v(x(h(U)('dialogDemo.close')), 1)]), _: 1 }
                )
              ]),
              default: w(() => [
                'add' === te.value || 'edit' === te.value
                  ? (y(),
                    k(
                      A,
                      { key: 0, ref_key: 'writeRef', ref: le, 'current-row': ae.value },
                      null,
                      8,
                      ['current-row']
                    ))
                  : C('', !0),
                'expression' === te.value ? (y(), k(L, { key: 1 })) : C('', !0)
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
  }
})
export { T as default }
