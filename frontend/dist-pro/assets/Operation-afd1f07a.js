import {
  U as e,
  e as t,
  I as o,
  L as l,
  x as s,
  N as a,
  M as i,
  a1 as r,
  r as p,
  o as n,
  j as d,
  m,
  k as u,
  ai as c,
  z as _,
  l as j,
  F as h
} from './index-820a519e.js'
import { u as b, _ as g } from './Table.vue_vue_type_script_lang-a0f5d3d3.js'
import { _ as f } from './Search.vue_vue_type_script_setup_true_lang-9de3bdd5.js'
import { _ as w } from './ContentWrap.vue_vue_type_script_setup_true_lang-37d6ee07.js'
import { _ as v } from './Detail.vue_vue_type_script_setup_true_lang-34076b4a.js'
import { _ as x } from './Dialog.vue_vue_type_style_index_0_lang-ce349c68.js'
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
const y = t({
  name: 'SystemRecordOperation',
  __name: 'Operation',
  setup(t) {
    const { t: y } = o(),
      {
        tableRegister: k,
        tableState: S,
        tableMethods: R
      } = b({
        fetchDataApi: async () => {
          const { pageSize: t, currentPage: o } = S,
            l = await ((s = { page: u(o), limit: u(t), ...u(V) }),
            e.get({ url: '/logs/operations', params: s }))
          var s
          return { list: l.data || [], total: l.count || 0 }
        }
      }),
      { dataList: D, loading: I, total: P, pageSize: z, currentPage: U } = S,
      { getList: C } = R,
      L = l([
        { field: 'user_id', label: '操作人编号', show: !0, disabled: !0, width: '100px' },
        {
          field: 'user_name',
          label: '操作人',
          show: !0,
          disabled: !0,
          width: '100px',
          sortable: 'custom'
        },
        {
          field: 'phone',
          label: '手机号',
          show: !0,
          disabled: !0,
          width: '130px',
          sortable: 'custom'
        },
        { field: 'request_method', label: '请求方法', show: !0, disabled: !0, width: '100px' },
        { field: 'client_ip', label: '客户端地址', width: '130px', show: !0, disabled: !0 },
        { field: 'tags', label: '标签', width: '130px', show: !0 },
        { field: 'summary', label: '操作内容', show: !0 },
        { field: 'description', label: '描述', show: !1 },
        { field: 'status_code', label: '操作状态', show: !0, width: '100px', sortable: 'custom' },
        { field: 'route_name', label: '接口函数', show: !1, width: '150px' },
        { field: 'api_path', label: '接口地址', show: !1 },
        { field: 'params', label: '请求参数', show: !1 },
        { field: 'browser', label: '浏览器', show: !0, width: '150px' },
        { field: 'system', label: '系统', show: !1, width: '150px' },
        { field: 'process_time', label: '总耗时', show: !0, sortable: 'custom' },
        { field: 'created_at', label: '操作时间', show: !0, sortable: 'custom' },
        {
          field: 'action',
          width: '100px',
          show: !0,
          label: '操作',
          slots: {
            default: (e) => {
              const t = e.row
              return s(r, null, [
                s(
                  a,
                  { type: 'primary', link: !0, onClick: () => H(t, 'detail') },
                  { default: () => [i('详情')] }
                )
              ])
            }
          }
        }
      ]),
      q = l([
        {
          field: 'telephone',
          label: '手机号',
          component: 'Input',
          componentProps: { clearable: !1 }
        },
        {
          field: 'request_method',
          label: '请求方法',
          component: 'Input',
          componentProps: { clearable: !1 }
        },
        {
          field: 'summary',
          label: '操作内容',
          component: 'Input',
          componentProps: { clearable: !1 }
        }
      ]),
      V = p({ order: 'desc', prop: 'id' }),
      A = (e) => {
        ;((U.value = 1), (V.value = e), C())
      },
      F = (e) => {
        ;('descending' === e.order
          ? ((V.value.order = 'desc'), (V.value.prop = e.prop))
          : ((V.value.order = 'asc'), (V.value.prop = e.prop)),
          C())
      },
      M = p(!1),
      N = p(''),
      O = p(),
      E = p(''),
      H = (e, t) => {
        ;((N.value = y('exampleDemo.detail')), (E.value = t), (O.value = e), (M.value = !0))
      }
    return (e, t) => (
      n(),
      d(
        r,
        null,
        [
          s(u(w), null, {
            default: m(() => [
              s(u(f), { schema: q, onReset: A, onSearch: A }, null, 8, ['schema']),
              s(
                u(g),
                {
                  'current-page': u(U),
                  'onUpdate:currentPage': t[0] || (t[0] = (e) => (c(U) ? (U.value = e) : null)),
                  'page-size': u(z),
                  'onUpdate:pageSize': t[1] || (t[1] = (e) => (c(z) ? (z.value = e) : null)),
                  onSortChange: F,
                  showAction: '',
                  columns: L,
                  'node-key': 'id',
                  data: u(D),
                  loading: u(I),
                  pagination: { total: u(P) },
                  onRegister: u(k),
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
          s(
            u(x),
            {
              modelValue: M.value,
              'onUpdate:modelValue': t[3] || (t[3] = (e) => (M.value = e)),
              title: N.value,
              width: '800px'
            },
            {
              footer: m(() => [
                s(
                  u(a),
                  { onClick: t[2] || (t[2] = (e) => (M.value = !1)) },
                  { default: m(() => [i(_(u(y)('dialogDemo.close')), 1)]), _: 1 }
                )
              ]),
              default: m(() => [
                'detail' === E.value
                  ? (n(), j(v, { key: 0, 'current-row': O.value }, null, 8, ['current-row']))
                  : h('', !0)
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
export { y as default }
