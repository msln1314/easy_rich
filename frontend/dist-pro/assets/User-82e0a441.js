import {
  e,
  I as a,
  r as t,
  L as l,
  x as s,
  k as i,
  a1 as o,
  a0 as r,
  Z as u,
  N as n,
  M as p,
  dK as d,
  o as m,
  j as c,
  m as _,
  ai as v,
  l as f,
  ak as g,
  z as j,
  F as y,
  dL as w,
  dM as h,
  dN as b,
  af as x,
  dO as k,
  dP as P
} from './index-820a519e.js'
import { u as L, _ as S } from './Table.vue_vue_type_script_lang-a0f5d3d3.js'
import { E as C } from './el-switch-6f4f5b6a.js'
import { E as z, a as G } from './el-col-beabe3f6.js'
import { _ as R } from './Search.vue_vue_type_script_setup_true_lang-9de3bdd5.js'
import { _ as A } from './ContentWrap.vue_vue_type_script_setup_true_lang-37d6ee07.js'
import { _ as D } from './Write.vue_vue_type_script_setup_true_lang-49a53ba4.js'
import { _ as U } from './Dialog.vue_vue_type_style_index_0_lang-ce349c68.js'
import { s as I } from './dict-4a6e55e6.js'
import { u as E } from './dict-451afacd.js'
import { _ as M } from './Import.vue_vue_type_script_setup_true_lang-0a3ca508.js'
import { _ as N } from './PasswordSendSMS.vue_vue_type_script_setup_true_lang-f2c0c522.js'
import { _ as V } from './PasswordSendEmail.vue_vue_type_script_setup_true_lang-e1bf6ec7.js'
import { _ as W } from './PasswordReset.vue_vue_type_script_setup_true_lang-27dff608.js'
import { _ as F } from './DeptTree.vue_vue_type_script_setup_true_lang-c9acf851.js'
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
import './role-0252bcb8.js'
import './dept-b8a01226.js'
import './client_group-aeb78440.js'
import './use-dialog-2de816dc.js'
import './dict-c8c7fcf4.js'
import './el-link-dbc80422.js'
import './el-popconfirm-e835aac7.js'
const O = e({
  name: 'AuthUser',
  __name: 'User',
  setup(e) {
    const { t: O } = a(),
      {
        tableRegister: T,
        tableState: q,
        tableMethods: B
      } = L({
        fetchDataApi: async () => {
          const { pageSize: e, currentPage: a } = q,
            t = await w({ page: i(a), limit: i(e), ...i(se) })
          return { list: t.data || [], total: t.count || 0 }
        },
        fetchDelApi: async (e) => 200 === (await h(e)).code,
        fetchExportApi: async (e) => {
          const { pageSize: a, currentPage: t } = q
          return await b({ page: i(t), limit: i(a), ...i(se) }, e)
        }
      }),
      { dataList: K, loading: Q, total: Z, pageSize: $, currentPage: H } = q,
      { getList: J, delList: X, getSelections: Y, exportQueryList: ee } = B,
      ae = t([])
    ;(async () => {
      const e = E(),
        a = await e.getDictObj(['sys_gender'])
      ae.value = a.sys_vadmin_gender
    })()
    const te = l([
        { field: 'selection', type: 'selection', show: !0, disabled: !0 },
        { field: 'id', label: '用户编号', width: '100px', show: !1, disabled: !1 },
        { field: 'name', label: '姓名', show: !0, disabled: !0 },
        { field: 'nickname', label: '昵称', show: !0 },
        { field: 'phone', label: '手机号', show: !0, disabled: !0 },
        { field: 'email', label: '邮箱', show: !0, disabled: !0 },
        {
          field: 'gender',
          label: '性别',
          show: !1,
          slots: {
            default: (e) => {
              const a = e.row
              return s(o, null, [s('div', null, [I(i(ae), a.gender)])])
            }
          }
        },
        {
          field: 'roles',
          label: '角色',
          show: !0,
          slots: {
            default: (e) => {
              const a = e.row
              return s(o, null, [
                s('div', { class: 'text-truncate' }, [a.roles.map((e) => e.name).join()])
              ])
            }
          }
        },
        {
          field: 'dept',
          label: '部门',
          show: !0,
          slots: {
            default: (e) => {
              var a
              const t = e.row
              return s(o, null, [
                s('div', { class: 'text-truncate' }, [null == (a = t.dept) ? void 0 : a.name])
              ])
            }
          }
        },
        {
          field: 'is_active',
          label: '是否可用',
          show: !1,
          slots: {
            default: (e) => {
              const a = e.row
              return s(o, null, [s(C, { value: a.is_active, disabled: !0 }, null)])
            }
          }
        },
        {
          field: 'is_staff',
          label: '工作人员',
          show: !0,
          slots: {
            default: (e) => {
              const a = e.row
              return s(o, null, [s(C, { value: a.is_staff, disabled: !0 }, null)])
            }
          }
        },
        {
          field: 'is_admin',
          label: '管理人员',
          show: !0,
          slots: {
            default: (e) => {
              const a = e.row
              return s(o, null, [s(C, { value: a.is_admin, disabled: !0 }, null)])
            }
          }
        },
        { field: 'last_login', label: '最近登录时间', show: !0, width: '190px' },
        { field: 'created_at', label: '创建时间', width: '190px', show: !1 },
        {
          field: 'action',
          width: '150px',
          label: '操作',
          show: !0,
          slots: {
            default: (e) => {
              const a = e.row
              return s(o, null, [
                r(
                  s(
                    n,
                    { type: 'primary', link: !0, size: 'small', onClick: () => ve(a) },
                    { default: () => [p('编辑')] }
                  ),
                  [[u('hasPermi'), ['sys.user.update']]]
                ),
                r(
                  s(
                    n,
                    {
                      type: 'danger',
                      loading: re.value,
                      link: !0,
                      size: 'small',
                      onClick: () => ue(a)
                    },
                    { default: () => [p('删除')] }
                  ),
                  [[u('hasPermi'), ['sys.user.delete']]]
                )
              ])
            }
          }
        }
      ]),
      le = l([
        {
          field: 'name',
          label: '姓名',
          component: 'Input',
          componentProps: { clearable: !1, style: { width: '214px' } },
          formItemProps: { labelWidth: '47px' }
        },
        {
          field: 'phone',
          label: '手机号',
          component: 'Input',
          componentProps: { clearable: !1, style: { width: '214px' } }
        },
        {
          field: 'is_active',
          label: '状态',
          component: 'Select',
          componentProps: {
            style: { width: '214px' },
            options: [
              { label: '正常', value: !0 },
              { label: '停用', value: !1 }
            ]
          }
        },
        {
          field: 'is_staff',
          label: '工作人员',
          component: 'Select',
          componentProps: {
            style: { width: '214px' },
            options: [
              { label: '是', value: !0 },
              { label: '否', value: !1 }
            ]
          }
        }
      ]),
      se = t({}),
      ie = (e) => {
        ;((H.value = 1), (se.value = e), J())
      },
      oe = () => {
        ;((H.value = 1), (se.value = {}), J())
      },
      re = t(!1),
      ue = async (e) => {
        ;((re.value = !0),
          e
            ? await X(!0, [e.id]).finally(() => {
                re.value = !1
              })
            : await X(!0).finally(() => {
                re.value = !1
              }))
      },
      ne = t(!1),
      pe = t(''),
      de = t(),
      me = t(''),
      ce = t(),
      _e = t(!1),
      ve = async (e) => {
        const a = await d(e.id)
        a &&
          ((pe.value = '编辑用户'),
          (a.data.role_ids = a.data.roles.map((e) => e.id)),
          (a.data.iot_group_ids = a.data.iot_groups.map((e) => e.id)),
          (me.value = 'edit'),
          (de.value = a.data),
          (ne.value = !0))
      },
      fe = () => {
        ;((pe.value = '新增用户'), (me.value = 'add'), (de.value = void 0), (ne.value = !0))
      },
      ge = () => {
        ;((pe.value = '批量导入用户'), (me.value = 'import'), (de.value = void 0), (ne.value = !0))
      },
      je = t([]),
      ye = async () => {
        if (((je.value = await Y()), !(je.value.length > 0))) return x.warning('请先选择数据')
        ;((pe.value = '重置密码并发送短信'),
          (me.value = 'sms'),
          (de.value = void 0),
          (ne.value = !0))
      },
      we = async () => {
        if (((je.value = await Y()), !(je.value.length > 0))) return x.warning('请先选择数据')
        ;((pe.value = '重置密码并发送邮件'),
          (me.value = 'email'),
          (de.value = void 0),
          (ne.value = !0))
      },
      he = async () => {
        if (((je.value = await Y()), !(je.value.length > 0))) return x.warning('请先选择数据')
        ;((pe.value = '重置密码'),
          (me.value = 'reset_password'),
          (de.value = void 0),
          (ne.value = !0))
      },
      be = async (e) => {
        ;((se.value.dept_id = e.value), await J())
      },
      xe = async () => {
        const e = i(ce),
          a = await (null == e ? void 0 : e.submit())
        if (a) {
          _e.value = !0
          try {
            const e = t({})
            'add' === me.value
              ? ((e.value = await k(a)),
                e.value && ((ne.value = !1), await J(), x.success('添加成功!')))
              : 'edit' === me.value &&
                ((e.value = await P(a)),
                e.value && ((ne.value = !1), await J(), x.success('编辑成功!')))
          } finally {
            _e.value = !1
          }
        }
      }
    return (e, a) => {
      const t = u('hasPermi')
      return (
        m(),
        c(
          o,
          null,
          [
            s(
              i(G),
              { gutter: 20 },
              {
                default: _(() => [
                  s(
                    i(z),
                    { span: 4, xs: 24 },
                    {
                      default: _(() => [
                        s(
                          i(A),
                          { class: 'h-1/1 -mr-15px' },
                          { default: _(() => [s(F, { onNodeClick: be })]), _: 1 }
                        )
                      ]),
                      _: 1
                    }
                  ),
                  s(
                    i(z),
                    { span: 20, xs: 24 },
                    {
                      default: _(() => [
                        s(i(A), null, {
                          default: _(() => [
                            s(i(R), { schema: le, onReset: oe, onSearch: ie }, null, 8, ['schema']),
                            s(
                              i(S),
                              {
                                'current-page': i(H),
                                'onUpdate:currentPage':
                                  a[2] || (a[2] = (e) => (v(H) ? (H.value = e) : null)),
                                'page-size': i($),
                                'onUpdate:pageSize':
                                  a[3] || (a[3] = (e) => (v($) ? ($.value = e) : null)),
                                showAction: '',
                                columns: te,
                                'default-expand-all': '',
                                'node-key': 'id',
                                data: i(K),
                                loading: i(Q),
                                pagination: { total: i(Z) },
                                onRegister: i(T),
                                onRefresh: i(J)
                              },
                              {
                                toolbar: _(() => [
                                  s(
                                    i(G),
                                    { gutter: 10 },
                                    {
                                      default: _(() => [
                                        r(
                                          (m(),
                                          f(
                                            i(z),
                                            { span: 1.5 },
                                            {
                                              default: _(() => [
                                                s(
                                                  i(n),
                                                  { type: 'primary', onClick: fe },
                                                  { default: _(() => [p('新增用户')]), _: 1 }
                                                )
                                              ]),
                                              _: 1
                                            }
                                          )),
                                          [[t, ['sys.user.create']]]
                                        ),
                                        r(
                                          (m(),
                                          f(
                                            i(z),
                                            { span: 1.5 },
                                            {
                                              default: _(() => [
                                                s(
                                                  i(n),
                                                  { onClick: ge },
                                                  { default: _(() => [p('批量导入用户')]), _: 1 }
                                                )
                                              ]),
                                              _: 1
                                            }
                                          )),
                                          [[t, ['sys.user.import']]]
                                        ),
                                        r(
                                          (m(),
                                          f(
                                            i(z),
                                            { span: 1.5 },
                                            {
                                              default: _(() => [
                                                s(
                                                  i(n),
                                                  { onClick: a[0] || (a[0] = (e) => i(ee)()) },
                                                  { default: _(() => [p('导出筛选用户')]), _: 1 }
                                                )
                                              ]),
                                              _: 1
                                            }
                                          )),
                                          [[t, ['sys.user.export']]]
                                        ),
                                        r(
                                          (m(),
                                          f(
                                            i(z),
                                            { span: 1.5 },
                                            {
                                              default: _(() => [
                                                s(
                                                  i(n),
                                                  { onClick: ye },
                                                  {
                                                    default: _(() => [p('重置密码通知短信')]),
                                                    _: 1
                                                  }
                                                )
                                              ]),
                                              _: 1
                                            }
                                          )),
                                          [[t, ['sys.user.reset']]]
                                        ),
                                        r(
                                          (m(),
                                          f(
                                            i(z),
                                            { span: 1.5 },
                                            {
                                              default: _(() => [
                                                s(
                                                  i(n),
                                                  { onClick: we },
                                                  {
                                                    default: _(() => [p('重置密码通知邮件')]),
                                                    _: 1
                                                  }
                                                )
                                              ]),
                                              _: 1
                                            }
                                          )),
                                          [[t, ['sys.user.reset']]]
                                        ),
                                        r(
                                          (m(),
                                          f(
                                            i(z),
                                            { span: 1.5 },
                                            {
                                              default: _(() => [
                                                s(
                                                  i(n),
                                                  { onClick: he },
                                                  { default: _(() => [p('重置密码')]), _: 1 }
                                                )
                                              ]),
                                              _: 1
                                            }
                                          )),
                                          [[t, ['sys.user.reset']]]
                                        ),
                                        r(
                                          (m(),
                                          f(
                                            i(z),
                                            { span: 1.5 },
                                            {
                                              default: _(() => [
                                                s(
                                                  i(n),
                                                  {
                                                    type: 'danger',
                                                    onClick: a[1] || (a[1] = (e) => ue(null))
                                                  },
                                                  { default: _(() => [p('批量删除')]), _: 1 }
                                                )
                                              ]),
                                              _: 1
                                            }
                                          )),
                                          [[t, ['sys.user.delete']]]
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
                        })
                      ]),
                      _: 1
                    }
                  )
                ]),
                _: 1
              }
            ),
            s(
              i(U),
              {
                modelValue: ne.value,
                'onUpdate:modelValue': a[5] || (a[5] = (e) => (ne.value = e)),
                title: pe.value,
                height: 600,
                width: 'sms' === me.value || 'email' === me.value ? '1000px' : '700px'
              },
              g(
                {
                  default: _(() => [
                    'add' === me.value || 'edit' === me.value
                      ? (m(),
                        f(
                          D,
                          { key: 0, ref_key: 'writeRef', ref: ce, 'current-row': de.value },
                          null,
                          8,
                          ['current-row']
                        ))
                      : 'import' === me.value
                        ? (m(), f(M, { key: 1, onGetList: i(J) }, null, 8, ['onGetList']))
                        : 'sms' === me.value
                          ? (m(),
                            f(N, { key: 2, selections: je.value, onGetList: i(J) }, null, 8, [
                              'selections',
                              'onGetList'
                            ]))
                          : 'email' === me.value
                            ? (m(),
                              f(V, { key: 3, selections: je.value, onGetList: i(J) }, null, 8, [
                                'selections',
                                'onGetList'
                              ]))
                            : 'reset_password' === me.value
                              ? (m(),
                                f(W, { key: 4, selections: je.value, onGetList: i(J) }, null, 8, [
                                  'selections',
                                  'onGetList'
                                ]))
                              : y('', !0)
                  ]),
                  _: 2
                },
                [
                  'add' === me.value || 'edit' === me.value
                    ? {
                        name: 'footer',
                        fn: _(() => [
                          s(
                            i(n),
                            { type: 'primary', loading: _e.value, onClick: xe },
                            { default: _(() => [p(j(i(O)('exampleDemo.save')), 1)]), _: 1 },
                            8,
                            ['loading']
                          ),
                          s(
                            i(n),
                            { onClick: a[4] || (a[4] = (e) => (ne.value = !1)) },
                            { default: _(() => [p(j(i(O)('dialogDemo.close')), 1)]), _: 1 }
                          )
                        ]),
                        key: '0'
                      }
                    : void 0
                ]
              ),
              1032,
              ['modelValue', 'title', 'width']
            )
          ],
          64
        )
      )
    }
  }
})
export { O as default }
