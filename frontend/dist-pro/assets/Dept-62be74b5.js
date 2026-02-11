import { g as e, d as a, a as l, p as t } from './dept-b8a01226.js'
import { u as s, _ as i } from './Table.vue_vue_type_script_lang-a0f5d3d3.js'
import {
  e as o,
  I as r,
  L as p,
  x as u,
  a1 as d,
  N as n,
  M as m,
  r as v,
  o as c,
  j,
  m as _,
  k as f,
  l as g,
  z as y,
  F as w,
  af as h
} from './index-820a519e.js'
import { E as b } from './el-switch-6f4f5b6a.js'
import { a as k, E as x } from './el-col-beabe3f6.js'
import { _ as C } from './ContentWrap.vue_vue_type_script_setup_true_lang-37d6ee07.js'
import { _ as D } from './Write.vue_vue_type_script_setup_true_lang-b9a444c0.js'
import { _ as R } from './Dialog.vue_vue_type_style_index_0_lang-ce349c68.js'
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
import './use-dialog-2de816dc.js'
const V = o({
  name: 'AuthDept',
  __name: 'Dept',
  setup(o) {
    const { t: V } = r(),
      {
        tableRegister: z,
        tableState: A,
        tableMethods: L
      } = s({
        fetchDataApi: async () => {
          const { pageSize: a, currentPage: l } = A,
            t = await e({ page: f(l), limit: f(a) })
          return { list: t.data || [], total: t.count || 0 }
        },
        fetchDelApi: async (e) => 200 === (await a(e)).code
      }),
      { dataList: S, loading: E } = A,
      { getList: U, delList: F } = L,
      M = p([
        { field: 'name', label: '部门名称', disabled: !0, show: !0 },
        { field: 'code', label: '部门标识', show: !0 },
        { field: 'manager', label: '负责人', show: !0 },
        { field: 'phone', label: '联系电话', show: !0 },
        { field: 'email', label: '邮箱', show: !0 },
        { field: 'desc', label: '描述', show: !0 },
        { field: 'order', label: '排序', width: '120px', show: !0 },
        {
          field: 'status',
          label: '状态',
          width: '120px',
          show: !0,
          slots: {
            default: (e) => {
              const a = e.row
              return u(d, null, [u(b, { value: !a.disabled, disabled: !0 }, null)])
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
              const a = e.row
              return u(d, null, [
                u(
                  n,
                  { type: 'primary', link: !0, size: 'small', onClick: () => J(a) },
                  { default: () => [m('编辑')] }
                ),
                u(
                  n,
                  { type: 'primary', link: !0, size: 'small', onClick: () => O(a) },
                  { default: () => [m('添加子部门')] }
                ),
                u(
                  n,
                  {
                    type: 'danger',
                    loading: N.value,
                    link: !0,
                    size: 'small',
                    onClick: () => W(a)
                  },
                  { default: () => [m('删除')] }
                )
              ])
            }
          }
        }
      ]),
      N = v(!1),
      W = async (e) => {
        ;((N.value = !0),
          await F(!0, [e.id]).finally(() => {
            N.value = !1
          }))
      },
      q = v(!1),
      I = v(''),
      P = v(),
      T = v(void 0),
      B = v(''),
      G = v(),
      H = v(!1),
      J = (e) => {
        ;((I.value = '编辑'), (B.value = 'edit'), (P.value = e), (q.value = !0))
      },
      K = () => {
        ;((I.value = '新增'), (B.value = 'add'), (P.value = void 0), (q.value = !0))
      },
      O = (e) => {
        ;((I.value = '添加子部门'),
          (B.value = 'addSon'),
          (T.value = e.id),
          (P.value = void 0),
          (q.value = !0))
      },
      Q = async () => {
        const e = f(G),
          a = await (null == e ? void 0 : e.submit())
        if (a) {
          H.value = !0
          try {
            const e = v({})
            'add' === B.value || 'addSon' === B.value
              ? ((e.value = await l(a)),
                e.value && ((T.value = void 0), (q.value = !1), U(), h.success('添加成功!')))
              : 'edit' === B.value &&
                ((e.value = await t(a)), e.value && ((q.value = !1), U(), h.success('编辑成功!')))
          } finally {
            H.value = !1
          }
        }
      }
    return (e, a) => (
      c(),
      j(
        d,
        null,
        [
          u(f(C), null, {
            default: _(() => [
              u(
                f(i),
                {
                  columns: M,
                  showAction: '',
                  'default-expand-all': '',
                  'node-key': 'id',
                  data: f(S),
                  loading: f(E),
                  onRegister: f(z),
                  onRefresh: f(U)
                },
                {
                  toolbar: _(() => [
                    u(
                      f(k),
                      { gutter: 10 },
                      {
                        default: _(() => [
                          u(
                            f(x),
                            { span: 1.5 },
                            {
                              default: _(() => [
                                u(
                                  f(n),
                                  { type: 'primary', onClick: K },
                                  { default: _(() => [m('新增部门')]), _: 1 }
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
          u(
            f(R),
            {
              modelValue: q.value,
              'onUpdate:modelValue': a[1] || (a[1] = (e) => (q.value = e)),
              title: I.value
            },
            {
              footer: _(() => [
                'detail' !== B.value
                  ? (c(),
                    g(
                      f(n),
                      { key: 0, type: 'primary', loading: H.value, onClick: Q },
                      { default: _(() => [m(y(f(V)('exampleDemo.save')), 1)]), _: 1 },
                      8,
                      ['loading']
                    ))
                  : w('', !0),
                u(
                  f(n),
                  { onClick: a[0] || (a[0] = (e) => (q.value = !1)) },
                  { default: _(() => [m(y(f(V)('dialogDemo.close')), 1)]), _: 1 }
                )
              ]),
              default: _(() => [
                u(
                  D,
                  { ref_key: 'writeRef', ref: G, 'current-row': P.value, 'parent-id': T.value },
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
})
export { V as default }
