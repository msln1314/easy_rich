import {
  e,
  I as a,
  L as l,
  x as t,
  a1 as s,
  a0 as o,
  aH as i,
  Z as r,
  N as n,
  M as p,
  r as u,
  b1 as d,
  o as m,
  j as c,
  m as _,
  k as j,
  ai as v,
  l as f,
  z as g,
  af as y
} from './index-820a519e.js'
import { g as b, a as h, d as w, b as k, p as x } from './role-0252bcb8.js'
import { u as R, _ as S } from './Table.vue_vue_type_script_lang-a0f5d3d3.js'
import { E as P } from './el-switch-6f4f5b6a.js'
import { _ as z } from './Search.vue_vue_type_script_setup_true_lang-9de3bdd5.js'
import { _ as C } from './ContentWrap.vue_vue_type_script_setup_true_lang-37d6ee07.js'
import { _ as D } from './Write.vue_vue_type_script_setup_true_lang-6737bcda.js'
import A from './RoleAssignMenuForm-ea746ff8.js'
import { _ as E } from './Dialog.vue_vue_type_style_index_0_lang-ce349c68.js'
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
import './useValidator-db15330d.js'
import './tree-ae7cba8b.js'
import './use-dialog-2de816dc.js'
const I = e({
  name: 'SysRole',
  __name: 'Role',
  setup(e) {
    const { t: I } = a(),
      {
        tableRegister: L,
        tableState: M,
        tableMethods: U
      } = R({
        fetchDataApi: async () => {
          const { pageSize: e, currentPage: a } = M,
            l = await h({ page: j(a), limit: j(e), ...j(B) })
          return { list: l.data || [], total: l.count || 0 }
        },
        fetchDelApi: async (e) => 200 === (await w(e)).code
      }),
      { dataList: V, loading: F, total: N, pageSize: W, currentPage: q } = M,
      { getList: H, delList: T } = U,
      Z = l([
        { field: 'id', label: '角色编号', show: !1, disabled: !1 },
        { field: 'name', label: '角色名称', show: !0, disabled: !0 },
        { field: 'code', label: '权限字符', show: !0 },
        { field: 'order', label: '显示顺序', show: !0 },
        {
          field: 'status',
          label: '角色状态',
          show: !0,
          slots: {
            default: (e) => {
              const a = e.row
              return t(s, null, [t(P, { value: a.status, disabled: !0 }, null)])
            }
          }
        },
        {
          field: 'is_admin',
          label: '最高权限',
          show: !0,
          slots: {
            default: (e) => {
              const a = e.row
              return t(s, null, [t(P, { value: a.is_admin, disabled: !0 }, null)])
            }
          }
        },
        { field: 'created_at', label: '创建时间', show: !0 },
        {
          field: 'action',
          width: '170px',
          label: '操作',
          show: !0,
          slots: {
            default: (e) => {
              const a = e.row
              return t(s, null, [
                o(
                  t(
                    n,
                    { type: 'primary', link: !0, size: 'small', onClick: () => se(a) },
                    { default: () => [p('编辑')] }
                  ),
                  [
                    [i, 1 !== a.id],
                    [r('hasPermi'), ['sys.role.update']]
                  ]
                ),
                o(
                  t(
                    n,
                    { type: 'primary', link: !0, size: 'small', onClick: () => Q(a) },
                    { default: () => [p('菜单管理')] }
                  ),
                  [[i, 1 !== a.id]]
                ),
                o(
                  t(
                    n,
                    {
                      type: 'danger',
                      loading: J.value,
                      link: !0,
                      size: 'small',
                      onClick: () => K(a)
                    },
                    { default: () => [p('删除')] }
                  ),
                  [
                    [i, 1 !== a.id],
                    [r('hasPermi'), ['sys.role.delete']]
                  ]
                )
              ])
            }
          }
        }
      ]),
      $ = l([
        {
          field: 'name',
          label: '角色名称',
          component: 'Input',
          componentProps: { clearable: !1, style: { width: '214px' } }
        },
        {
          field: 'role_key',
          label: '权限字符',
          component: 'Input',
          componentProps: { clearable: !1, style: { width: '214px' } }
        },
        {
          field: 'disabled',
          label: '状态',
          component: 'Select',
          componentProps: {
            style: { width: '214px' },
            options: [
              { label: '正常', value: !1 },
              { label: '停用', value: !0 }
            ]
          }
        }
      ]),
      B = u({}),
      G = (e) => {
        ;((q.value = 1), (B.value = e), H())
      },
      J = u(!1),
      K = async (e) => {
        ;((J.value = !0),
          await T(!0, [e.id]).finally(() => {
            J.value = !1
          }))
      },
      O = u(),
      Q = async (e) => {
        O.value.open(e)
      },
      X = u(!1),
      Y = u(''),
      ee = u(),
      ae = u(''),
      le = u(),
      te = u(!1),
      se = async (e) => {
        const a = await b(e.id)
        a && ((Y.value = '编辑角色'), (ae.value = 'edit'), (ee.value = a.data), (X.value = !0))
      },
      oe = () => {
        ;((Y.value = '新增角色'), (ae.value = 'add'), (ee.value = void 0), (X.value = !0))
      },
      ie = async () => {
        const e = j(le),
          a = await (null == e ? void 0 : e.submit())
        if (a) {
          te.value = !0
          try {
            const e = u({})
            'add' === ae.value
              ? ((e.value = await k(a)), e.value && ((X.value = !1), H(), y.success('添加成功!')))
              : 'edit' === ae.value &&
                ((e.value = await x(a)), e.value && ((X.value = !1), H(), y.success('编辑成功!')))
          } finally {
            te.value = !1
          }
        }
      }
    return (e, a) => {
      const l = d('ElCol'),
        i = d('ElRow'),
        u = r('hasPermi')
      return (
        m(),
        c(
          s,
          null,
          [
            t(j(C), null, {
              default: _(() => [
                t(j(z), { schema: $, onReset: G, onSearch: G }, null, 8, ['schema']),
                t(
                  j(S),
                  {
                    'current-page': j(q),
                    'onUpdate:currentPage': a[0] || (a[0] = (e) => (v(q) ? (q.value = e) : null)),
                    'page-size': j(W),
                    'onUpdate:pageSize': a[1] || (a[1] = (e) => (v(W) ? (W.value = e) : null)),
                    showAction: '',
                    columns: Z,
                    'default-expand-all': '',
                    'node-key': 'id',
                    data: j(V),
                    loading: j(F),
                    pagination: { total: j(N) },
                    onRegister: j(L),
                    onRefresh: j(H)
                  },
                  {
                    toolbar: _(() => [
                      t(
                        i,
                        { gutter: 10 },
                        {
                          default: _(() => [
                            t(
                              l,
                              { span: 1.5 },
                              {
                                default: _(() => [
                                  o(
                                    (m(),
                                    f(
                                      j(n),
                                      { type: 'primary', onClick: oe },
                                      { default: _(() => [p('新增角色')]), _: 1 }
                                    )),
                                    [[u, ['sys.role.create']]]
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
            t(
              j(E),
              {
                modelValue: X.value,
                'onUpdate:modelValue': a[3] || (a[3] = (e) => (X.value = e)),
                title: Y.value,
                height: 650
              },
              {
                footer: _(() => [
                  t(
                    j(n),
                    { type: 'primary', loading: te.value, onClick: ie },
                    { default: _(() => [p(g(j(I)('exampleDemo.save')), 1)]), _: 1 },
                    8,
                    ['loading']
                  ),
                  t(
                    j(n),
                    { onClick: a[2] || (a[2] = (e) => (X.value = !1)) },
                    { default: _(() => [p(g(j(I)('dialogDemo.close')), 1)]), _: 1 }
                  )
                ]),
                default: _(() => [
                  t(D, { ref_key: 'writeRef', ref: le, 'current-row': ee.value }, null, 8, [
                    'current-row'
                  ])
                ]),
                _: 1
              },
              8,
              ['modelValue', 'title']
            ),
            t(A, { ref_key: 'assignMenuFormRef', ref: O, onSuccess: j(H) }, null, 8, ['onSuccess'])
          ],
          64
        )
      )
    }
  }
})
export { I as default }
