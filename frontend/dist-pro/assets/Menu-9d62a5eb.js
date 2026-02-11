import {
  e,
  I as l,
  r as t,
  L as a,
  x as s,
  al as i,
  a1 as o,
  a0 as r,
  Z as u,
  N as n,
  M as d,
  o as p,
  j as m,
  m as c,
  k as v,
  l as j,
  z as _,
  F as f,
  dz as w,
  dA as y,
  dB as h,
  dC as g
} from './index-820a519e.js'
import { u as b, _ as x } from './Table.vue_vue_type_script_lang-a0f5d3d3.js'
import { E as k } from './el-switch-6f4f5b6a.js'
import { a as C, E as z } from './el-col-beabe3f6.js'
import { _ as A } from './ContentWrap.vue_vue_type_script_setup_true_lang-37d6ee07.js'
import { _ as D } from './Write.vue_vue_type_script_setup_true_lang-d14cb56c.js'
import { _ as R } from './Dialog.vue_vue_type_style_index_0_lang-ce349c68.js'
import { u as P } from './dict-451afacd.js'
import { s as L } from './dict-4a6e55e6.js'
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
import './el-card-06c161d4.js'
import './useValidator-db15330d.js'
import './el-tab-pane-bc33a695.js'
import './use-dialog-2de816dc.js'
import './dict-c8c7fcf4.js'
const M = e({
  name: 'AuthMenu',
  __name: 'Menu',
  setup(e) {
    const { t: M } = l(),
      {
        tableRegister: S,
        tableState: V,
        tableMethods: E
      } = b({
        fetchDataApi: async () => {
          const { pageSize: e, currentPage: l } = V,
            t = await w({ page: v(l), limit: v(e) })
          return { list: t.data || [], total: t.count || 0 }
        },
        fetchDelApi: async (e) => 200 === (await y(e)).code
      }),
      { dataList: F, loading: N } = V,
      { getList: U, delList: W } = E
    let q = t([])
    ;(async () => {
      const e = P(),
        l = await e.getDictObj(['sys_menu_type'])
      q.value = l.sys_menu_type
    })()
    const B = a([
        { field: 'menu_name', label: '菜单名称', width: '200px', disabled: !0, show: !0 },
        {
          field: 'icon',
          label: '图标',
          width: '120px',
          show: !1,
          slots: {
            default: (e) => {
              const l = e.row
              return s(o, null, [l.icon ? s(i, { icon: l.icon }, null) : ''])
            }
          }
        },
        { field: 'order', label: '排序', width: '120px', show: !0 },
        {
          field: 'menu_type',
          label: '菜单类型',
          width: '120px',
          show: !0,
          slots: {
            default: (e) => {
              const l = e.row
              return s(o, null, [s('span', null, [L(q.value, l.menu_type)])])
            }
          }
        },
        { field: 'perms', label: '权限标识', width: '150px', show: !0 },
        { field: 'path', label: '路由地址', show: !0 },
        { field: 'component', label: '组件路径', show: !0 },
        {
          field: 'noCache',
          label: '页面缓存',
          width: '120px',
          show: !0,
          slots: {
            default: (e) => {
              const l = e.row
              return s(o, null, [s(k, { value: !l.noCache, disabled: !0 }, null)])
            }
          }
        },
        {
          field: 'hidden',
          label: '显示状态',
          width: '120px',
          show: !0,
          slots: {
            default: (e) => {
              const l = e.row
              return s(o, null, [s(k, { value: !l.hidden, disabled: !0 }, null)])
            }
          }
        },
        {
          field: 'status',
          label: '菜单状态',
          width: '120px',
          show: !0,
          slots: {
            default: (e) => {
              const l = e.row
              return s(o, null, [s(k, { value: l.status, disabled: !0 }, null)])
            }
          }
        },
        {
          field: 'action',
          width: '200px',
          label: '操作',
          show: !0,
          slots: {
            default: (e) => {
              const l = e.row
              return s(o, null, [
                r(
                  s(
                    n,
                    { type: 'primary', link: !0, size: 'small', onClick: () => X(l) },
                    { default: () => [d('编辑')] }
                  ),
                  [[u('hasPermi'), ['sys.menu.update']]]
                ),
                r(
                  s(
                    n,
                    { type: 'primary', link: !0, size: 'small', onClick: () => $(l) },
                    { default: () => [d('添加子菜单')] }
                  ),
                  [[u('hasPermi'), ['sys.menu.create']]]
                ),
                r(
                  s(
                    n,
                    {
                      type: 'danger',
                      loading: I.value,
                      link: !0,
                      size: 'small',
                      onClick: () => O(l)
                    },
                    { default: () => [d('删除')] }
                  ),
                  [[u('hasPermi'), ['sys.menu.delete']]]
                )
              ])
            }
          }
        }
      ]),
      I = t(!1),
      O = async (e) => {
        ;((I.value = !0),
          await W(!0, [e.id]).finally(() => {
            I.value = !1
          }))
      },
      T = t(!1),
      Z = t(''),
      G = t(),
      H = t(void 0),
      J = t(''),
      K = t(),
      Q = t(!1),
      X = (e) => {
        ;((Z.value = '编辑'), (J.value = 'edit'), (G.value = e), (T.value = !0))
      },
      Y = () => {
        ;((Z.value = '新增'), (J.value = 'add'), (G.value = void 0), (T.value = !0))
      },
      $ = (e) => {
        ;((Z.value = '添加子菜单'),
          (J.value = 'addSon'),
          (H.value = e.id),
          (G.value = void 0),
          (T.value = !0))
      },
      ee = async () => {
        const e = v(K),
          l = await (null == e ? void 0 : e.submit())
        if (l) {
          Q.value = !0
          try {
            const e = t({})
            'add' === J.value || 'addSon' === J.value
              ? ((e.value = await h(l)), e.value && ((H.value = void 0), await U(), (T.value = !1)))
              : 'edit' === J.value &&
                ((e.value = await g(l)), e.value && (await U(), (T.value = !1)))
          } finally {
            Q.value = !1
          }
        }
      }
    return (e, l) => {
      const t = u('hasPermi')
      return (
        p(),
        m(
          o,
          null,
          [
            s(v(A), null, {
              default: c(() => [
                s(
                  v(x),
                  {
                    columns: B,
                    showAction: '',
                    'default-expand-all': '',
                    'node-key': 'id',
                    data: v(F),
                    loading: v(N),
                    onRegister: v(S),
                    onRefresh: v(U)
                  },
                  {
                    toolbar: c(() => [
                      s(
                        v(C),
                        { gutter: 10 },
                        {
                          default: c(() => [
                            s(
                              v(z),
                              { span: 1.5 },
                              {
                                default: c(() => [
                                  r(
                                    (p(),
                                    j(
                                      v(n),
                                      { type: 'primary', onClick: Y },
                                      { default: c(() => [d('新增菜单')]), _: 1 }
                                    )),
                                    [[t, ['sys.menu.create']]]
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
                  ['columns', 'data', 'loading', 'onRegister', 'onRefresh']
                )
              ]),
              _: 1
            }),
            s(
              v(R),
              {
                modelValue: T.value,
                'onUpdate:modelValue': l[1] || (l[1] = (e) => (T.value = e)),
                title: Z.value
              },
              {
                footer: c(() => [
                  'detail' !== J.value
                    ? (p(),
                      j(
                        v(n),
                        { key: 0, type: 'primary', loading: Q.value, onClick: ee },
                        { default: c(() => [d(_(v(M)('exampleDemo.save')), 1)]), _: 1 },
                        8,
                        ['loading']
                      ))
                    : f('', !0),
                  s(
                    v(n),
                    { onClick: l[0] || (l[0] = (e) => (T.value = !1)) },
                    { default: c(() => [d(_(v(M)('dialogDemo.close')), 1)]), _: 1 }
                  )
                ]),
                default: c(() => [
                  s(
                    D,
                    { ref_key: 'writeRef', ref: K, 'current-row': G.value, 'parent-id': H.value },
                    null,
                    8,
                    ['current-row', 'parent-id']
                  )
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
  }
})
export { M as default }
