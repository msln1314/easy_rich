import { e, f as t, h as a, i as l, j as s } from './issue-784d4340.js'
import { u as o, _ as i } from './Table.vue_vue_type_script_lang-a0f5d3d3.js'
import {
  e as r,
  I as p,
  r as n,
  L as u,
  x as m,
  a1 as d,
  N as c,
  M as v,
  o as _,
  j,
  m as f,
  k as g,
  ai as y,
  z as w
} from './index-820a519e.js'
import { E as b } from './el-switch-6f4f5b6a.js'
import { a as h, E as x } from './el-col-beabe3f6.js'
import { _ as k } from './Search.vue_vue_type_script_setup_true_lang-9de3bdd5.js'
import { _ as z } from './ContentWrap.vue_vue_type_script_setup_true_lang-37d6ee07.js'
import { _ as C } from './Write.vue_vue_type_script_setup_true_lang-7a103998.js'
import { _ as S } from './Dialog.vue_vue_type_style_index_0_lang-ce349c68.js'
import { u as R } from './dict-451afacd.js'
import { s as D } from './dict-4a6e55e6.js'
import './el-message-box-faa52860.js'
import './el-input-5ae17c8f.js'
import './event-5568c9d8.js'
import './isNil-1f22f7b0.js'
import './el-overlay-34b9d092.js'
import './scroll-ac7d0423.js'
import './vnode-06a99f10.js'
import './useForm-c59a8d29.js'
import './el-form-item-2e860f96.js'
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
import './useValidator-db15330d.js'
import './use-dialog-2de816dc.js'
import './dict-c8c7fcf4.js'
const P = r({
  name: 'HelpIssueCategory',
  __name: 'IssueCategory',
  setup(r) {
    const { t: P } = p(),
      {
        tableRegister: I,
        tableState: A,
        tableMethods: L
      } = o({
        fetchDataApi: async () => {
          const { pageSize: e, currentPage: a } = A,
            l = await t({ page: g(a), limit: g(e), ...g(T) })
          return { list: l.data || [], total: l.count || 0 }
        },
        fetchDelApi: async (e) => 200 === (await a(e)).code
      }),
      { dataList: U, loading: V, total: E, pageSize: M, currentPage: N } = A,
      { getList: W, delList: q } = L,
      F = n([])
    ;(async () => {
      const e = R(),
        t = await e.getDictObj(['sys_vadmin_platform'])
      F.value = t.sys_vadmin_platform
    })()
    const H = u([
        { field: 'id', label: '编号', show: !0, disabled: !0 },
        { field: 'name', label: '类别名称', show: !0, disabled: !0 },
        {
          field: 'platform',
          label: '展示平台',
          show: !0,
          slots: {
            default: (e) => {
              const t = e.row
              return m(d, null, [m('div', null, [D(F.value, t.platform)])])
            }
          }
        },
        {
          field: 'is_active',
          label: '是否可见',
          show: !0,
          slots: {
            default: (e) => {
              const t = e.row
              return m(d, null, [m(b, { value: t.is_active, disabled: !0 }, null)])
            }
          }
        },
        { field: 'created_at', label: '创建时间', show: !0, sortable: !0 },
        { field: 'create_user.name', label: '创建人', show: !0 },
        {
          field: 'action',
          width: '120px',
          label: '操作',
          show: !0,
          slots: {
            default: (e) => {
              const t = e.row
              return m(d, null, [
                m(
                  c,
                  { type: 'primary', link: !0, size: 'small', onClick: () => ee(t) },
                  { default: () => [v('编辑')] }
                ),
                m(
                  c,
                  {
                    type: 'danger',
                    loading: G.value,
                    link: !0,
                    size: 'small',
                    onClick: () => J(t)
                  },
                  { default: () => [v('删除')] }
                )
              ])
            }
          }
        }
      ]),
      O = u([
        {
          field: 'name',
          label: '类别名称',
          component: 'Input',
          componentProps: { clearable: !0, style: { width: '214px' } }
        },
        {
          field: 'platform',
          label: '登录平台',
          component: 'Select',
          componentProps: { style: { width: '214px' }, options: [] }
        },
        {
          field: 'is_active',
          label: '是否可见',
          component: 'Select',
          componentProps: {
            style: { width: '214px' },
            options: [
              { label: '可见', value: !0 },
              { label: '不可见', value: !1 }
            ]
          }
        }
      ]),
      T = n({}),
      B = (e) => {
        ;((N.value = 1), (T.value = e), W())
      },
      G = n(!1),
      J = async (e) => {
        ;((G.value = !0),
          await q(!0, [e.id]).finally(() => {
            G.value = !1
          }))
      },
      K = n(!1),
      Q = n(''),
      X = n(),
      Y = n(''),
      Z = n(),
      $ = n(!1),
      ee = async (t) => {
        const a = await e(t.id)
        a &&
          ((Q.value = '编辑常见问题类别'), (Y.value = 'edit'), (X.value = a.data), (K.value = !0))
      },
      te = () => {
        ;((Q.value = '新增常见问题类别'), (Y.value = 'add'), (X.value = void 0), (K.value = !0))
      },
      ae = async () => {
        const e = g(Z),
          t = await (null == e ? void 0 : e.submit())
        if (t) {
          $.value = !0
          try {
            const e = n({})
            'add' === Y.value
              ? ((e.value = await l(t)), e.value && ((K.value = !1), W()))
              : 'edit' === Y.value && ((e.value = await s(t)), e.value && ((K.value = !1), W()))
          } finally {
            $.value = !1
          }
        }
      }
    return (e, t) => (
      _(),
      j(
        d,
        null,
        [
          m(g(z), null, {
            default: f(() => [
              m(g(k), { schema: O, onReset: B, onSearch: B }, null, 8, ['schema']),
              m(
                g(i),
                {
                  'current-page': g(N),
                  'onUpdate:currentPage': t[0] || (t[0] = (e) => (y(N) ? (N.value = e) : null)),
                  'page-size': g(M),
                  'onUpdate:pageSize': t[1] || (t[1] = (e) => (y(M) ? (M.value = e) : null)),
                  showAction: '',
                  columns: H,
                  'default-expand-all': '',
                  'node-key': 'id',
                  data: g(U),
                  loading: g(V),
                  pagination: { total: g(E) },
                  onRegister: g(I),
                  onRefresh: g(W)
                },
                {
                  toolbar: f(() => [
                    m(
                      g(h),
                      { gutter: 10 },
                      {
                        default: f(() => [
                          m(
                            g(x),
                            { span: 1.5 },
                            {
                              default: f(() => [
                                m(
                                  g(c),
                                  { type: 'primary', onClick: te },
                                  { default: f(() => [v('新增常见问题类别')]), _: 1 }
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
            g(S),
            {
              modelValue: K.value,
              'onUpdate:modelValue': t[3] || (t[3] = (e) => (K.value = e)),
              title: Q.value,
              height: 650
            },
            {
              footer: f(() => [
                m(
                  g(c),
                  { type: 'primary', loading: $.value, onClick: ae },
                  { default: f(() => [v(w(g(P)('exampleDemo.save')), 1)]), _: 1 },
                  8,
                  ['loading']
                ),
                m(
                  g(c),
                  { onClick: t[2] || (t[2] = (e) => (K.value = !1)) },
                  { default: f(() => [v(w(g(P)('dialogDemo.close')), 1)]), _: 1 }
                )
              ]),
              default: f(() => [
                m(C, { ref_key: 'writeRef', ref: Z, 'current-row': X.value }, null, 8, [
                  'current-row'
                ])
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
