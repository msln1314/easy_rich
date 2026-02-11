import {
  U as e,
  e as t,
  I as o,
  L as s,
  x as l,
  a1 as a,
  N as i,
  M as r,
  r as p,
  o as n,
  j as m,
  m as d,
  k as u,
  ai as c,
  z as j,
  l as _,
  F as g
} from './index-820a519e.js'
import { u as v, _ as h } from './Table.vue_vue_type_script_lang-a0f5d3d3.js'
import { _ as f } from './Search.vue_vue_type_script_setup_true_lang-9de3bdd5.js'
import { _ as w } from './ContentWrap.vue_vue_type_script_setup_true_lang-37d6ee07.js'
import { _ as b } from './Detail.vue_vue_type_script_setup_true_lang-79bb103a.js'
import { _ as x } from './Dialog.vue_vue_type_style_index_0_lang-ce349c68.js'
import { _ as y } from './DictTag.vue_vue_type_script_lang-ded36db6.js'
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
import './use-dialog-2de816dc.js'
import './dict-451afacd.js'
import './dict-c8c7fcf4.js'
const k = t({
  name: 'SystemLogAction',
  __name: 'Action',
  setup(t) {
    const { t: k } = o(),
      {
        tableRegister: S,
        tableState: D,
        tableMethods: z
      } = v({
        fetchDataApi: async () => {
          const { pageSize: t, currentPage: o } = D,
            s = await ((l = { page: u(o), limit: u(t), ...u(T) }),
            e.get({ url: '/logs/actions', params: l }))
          var l
          return { list: s.data || [], total: s.count || 0 }
        }
      }),
      { dataList: R, loading: A, total: I, pageSize: P, currentPage: U } = D,
      { getList: C } = z,
      L = s([
        { field: 'user_id', label: '操作人编号', show: !0, disabled: !0, width: '100px' },
        { field: 'user.name', label: '操作人', show: !0, disabled: !0, width: '100px' },
        { field: 'phone', label: '手机号', show: !0, disabled: !0, sortable: !0, width: '130px' },
        { field: 'device.mac', label: '设备SN', show: !0, disabled: !0, width: '100px' },
        {
          field: 'client_ip',
          label: '客户端地址',
          width: '130px',
          show: !0,
          sortable: !0,
          disabled: !0
        },
        { field: 'message', label: '操作内容', show: !0, width: '300px', showOverflowTooltip: !1 },
        {
          field: 'status',
          label: '操作状态',
          show: !0,
          width: '100px',
          slots: {
            default: (e) => {
              const t = e.row
              return l(a, null, [l(y, { type: 'status', value: t.status }, null)])
            }
          }
        },
        { field: 'browser', label: '浏览器', show: !0, width: '150px' },
        { field: 'system', label: '系统', show: !1, width: '150px' },
        { field: 'created_at', label: '操作时间', show: !0, sortable: 'custom' },
        {
          field: 'action',
          width: '100px',
          show: !0,
          label: '操作',
          slots: {
            default: (e) => {
              const t = e.row
              return l(a, null, [
                l(
                  i,
                  { type: 'primary', link: !0, onClick: () => G(t, 'detail') },
                  { default: () => [r('详情')] }
                )
              ])
            }
          }
        }
      ]),
      N = s([
        { field: 'phone', label: '手机号', component: 'Input', componentProps: { clearable: !1 } },
        {
          field: 'message',
          label: '操作内容',
          component: 'Input',
          componentProps: { clearable: !1 }
        }
      ]),
      T = p({ order: 'desc', prop: 'id' }),
      V = (e) => {
        ;((U.value = 1), (T.value = e), C())
      },
      F = p(!1),
      M = p(''),
      q = p(),
      E = p(''),
      G = (e, t) => {
        ;((M.value = k('exampleDemo.detail')), (E.value = t), (q.value = e), (F.value = !0))
      },
      H = (e) => {
        ;('descending' === e.order
          ? ((T.value.order = 'desc'), (T.value.prop = e.prop))
          : ((T.value.order = 'asc'), (T.value.prop = e.prop)),
          C())
      }
    return (e, t) => (
      n(),
      m(
        a,
        null,
        [
          l(u(w), null, {
            default: d(() => [
              l(u(f), { schema: N, onReset: V, onSearch: V }, null, 8, ['schema']),
              l(
                u(h),
                {
                  'current-page': u(U),
                  'onUpdate:currentPage': t[0] || (t[0] = (e) => (c(U) ? (U.value = e) : null)),
                  'page-size': u(P),
                  'onUpdate:pageSize': t[1] || (t[1] = (e) => (c(P) ? (P.value = e) : null)),
                  onSortChange: H,
                  showAction: '',
                  columns: L,
                  'node-key': 'id',
                  data: u(R),
                  loading: u(A),
                  pagination: { total: u(I) },
                  onRegister: u(S),
                  onRefresh: u(C)
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
          l(
            u(x),
            {
              modelValue: F.value,
              'onUpdate:modelValue': t[3] || (t[3] = (e) => (F.value = e)),
              title: M.value,
              width: '800px'
            },
            {
              footer: d(() => [
                l(
                  u(i),
                  { onClick: t[2] || (t[2] = (e) => (F.value = !1)) },
                  { default: d(() => [r(j(u(k)('dialogDemo.close')), 1)]), _: 1 }
                )
              ]),
              default: d(() => [
                'detail' === E.value
                  ? (n(), _(b, { key: 0, 'current-row': q.value }, null, 8, ['current-row']))
                  : g('', !0)
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
export { k as default }
