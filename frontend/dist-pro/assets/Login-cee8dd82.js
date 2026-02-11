import {
  U as e,
  e as l,
  I as t,
  r as o,
  L as s,
  x as a,
  a1 as i,
  N as r,
  M as p,
  o as n,
  j as d,
  m,
  k as u,
  ai as c,
  z as j,
  l as _,
  F as f
} from './index-820a519e.js'
import { u as g, _ as h } from './Table.vue_vue_type_script_lang-a0f5d3d3.js'
import { E as v } from './el-switch-6f4f5b6a.js'
import { _ as b } from './Search.vue_vue_type_script_setup_true_lang-9de3bdd5.js'
import { _ as w } from './ContentWrap.vue_vue_type_script_setup_true_lang-37d6ee07.js'
import { _ as y } from './Detail.vue_vue_type_script_setup_true_lang-5656905b.js'
import { _ as x } from './Dialog.vue_vue_type_style_index_0_lang-ce349c68.js'
import { s as S } from './dict-4a6e55e6.js'
import { u as k } from './dict-451afacd.js'
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
const P = l({
  name: 'SystemRecordLogin',
  __name: 'Login',
  setup(l) {
    const { t: P } = t(),
      z = o([]),
      D = o([])
    ;(async () => {
      const e = k(),
        l = await e.getDictObj(['sys_platform', 'sys_login_method'])
      ;((z.value = l.sys_platform), (D.value = l.sys_login_method))
    })()
    const {
        tableRegister: R,
        tableState: I,
        tableMethods: L
      } = g({
        fetchDataApi: async () => {
          const { pageSize: l, currentPage: t } = I,
            o = await ((s = { page: u(t), limit: u(l), ...u(N) }),
            e.get({ url: '/logs/logins', params: s }))
          var s
          return { list: o.data || [], total: o.count || 0 }
        }
      }),
      { dataList: U, loading: C, total: A, pageSize: V, currentPage: q } = I,
      { getList: E } = L,
      F = s([
        { field: 'id', label: '编号', show: !0, disabled: !0, width: '120px' },
        {
          field: 'phone',
          label: '手机号',
          width: '150px',
          show: !0,
          disabled: !0,
          sortable: 'custom'
        },
        {
          field: 'status',
          label: '登录状态',
          show: !0,
          slots: {
            default: (e) =>
              a(i, null, [a(v, { value: e.row.status, size: 'small', disabled: !0 }, null)])
          }
        },
        {
          field: 'platform',
          label: '登录平台',
          width: '150px',
          show: !0,
          slots: { default: (e) => a(i, null, [a('div', null, [S(z.value, e.row.platform)])]) }
        },
        {
          field: 'login_method',
          label: '认证方式',
          width: '150px',
          show: !0,
          slots: { default: (e) => a(i, null, [a('div', null, [S(D.value, e.row.login_method)])]) }
        },
        {
          field: 'ip',
          label: '登录地址',
          show: !0,
          disabled: !0,
          width: '150px',
          sortable: 'custom'
        },
        { field: 'address', label: '登录地点', show: !0 },
        { field: 'postal_code', label: '邮政编码', show: !1 },
        { field: 'area_code', label: '地区区号', show: !1 },
        { field: 'browser', label: '浏览器', show: !0 },
        { field: 'system', label: '操作系统', show: !0 },
        { field: 'response', label: '响应信息', show: !1, disabled: !0 },
        { field: 'request', label: '请求信息', show: !1, disabled: !0 },
        { field: 'created_at', label: '创建时间', show: !0, sortable: 'custom' },
        {
          field: 'action',
          label: '操作',
          show: !0,
          width: 100,
          slots: {
            default: (e) => {
              const l = e.row
              return a(i, null, [
                a(
                  r,
                  { type: 'primary', link: !0, onClick: () => B(l, 'detail') },
                  { default: () => [p('详情')] }
                )
              ])
            }
          }
        }
      ]),
      M = s([
        {
          field: 'telephone',
          label: '手机号',
          component: 'Input',
          componentProps: { clearable: !1, style: { width: '214px' } }
        },
        {
          field: 'platform',
          label: '登录平台',
          component: 'Select',
          componentProps: { style: { width: '214px' }, options: z.value }
        },
        {
          field: 'ip',
          label: '登录地址',
          component: 'Input',
          componentProps: { clearable: !1, style: { width: '214px' } }
        },
        {
          field: 'address',
          label: '登录地点',
          component: 'Input',
          componentProps: { clearable: !1, style: { width: '214px' } }
        },
        {
          field: 'status',
          label: '登录状态',
          component: 'Select',
          componentProps: {
            style: { width: '214px' },
            options: [
              { label: '登录成功', value: !0 },
              { label: '登录失败', value: !1 }
            ]
          }
        }
      ]),
      N = o({ order: 'desc', prop: 'id' }),
      H = (e) => {
        ;((q.value = 1), (N.value = e), E())
      },
      J = o(!1),
      K = o(''),
      O = o(),
      T = o(''),
      W = (e) => {
        ;('descending' === e.order
          ? ((N.value.order = 'desc'), (N.value.prop = e.prop))
          : ((N.value.order = 'asc'), (N.value.prop = e.prop)),
          E())
      },
      B = (e, l) => {
        ;((K.value = P('exampleDemo.detail')), (T.value = l), (O.value = e), (J.value = !0))
      }
    return (e, l) => (
      n(),
      d(
        i,
        null,
        [
          a(u(w), null, {
            default: m(() => [
              a(u(b), { schema: M, onReset: H, onSearch: H }, null, 8, ['schema']),
              a(
                u(h),
                {
                  'current-page': u(q),
                  'onUpdate:currentPage': l[0] || (l[0] = (e) => (c(q) ? (q.value = e) : null)),
                  'page-size': u(V),
                  'onUpdate:pageSize': l[1] || (l[1] = (e) => (c(V) ? (V.value = e) : null)),
                  onSortChange: W,
                  showAction: '',
                  columns: F,
                  'node-key': 'id',
                  data: u(U),
                  loading: u(C),
                  pagination: { total: u(A) },
                  onRegister: u(R),
                  onRefresh: u(E)
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
          a(
            u(x),
            {
              modelValue: J.value,
              'onUpdate:modelValue': l[3] || (l[3] = (e) => (J.value = e)),
              title: K.value,
              width: '800px'
            },
            {
              footer: m(() => [
                a(
                  u(r),
                  { onClick: l[2] || (l[2] = (e) => (J.value = !1)) },
                  { default: m(() => [p(j(u(P)('dialogDemo.close')), 1)]), _: 1 }
                )
              ]),
              default: m(() => [
                'detail' === T.value
                  ? (n(), _(y, { key: 0, 'current-row': O.value }, null, 8, ['current-row']))
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
  }
})
export { P as default }
