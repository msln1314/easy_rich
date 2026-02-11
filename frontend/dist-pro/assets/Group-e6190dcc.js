import { a as e, d as a, b as t, p as l } from './client_group-aeb78440.js'
import { u as s, _ as o } from './Table.vue_vue_type_script_lang-a0f5d3d3.js'
import {
  e as i,
  I as r,
  L as u,
  x as p,
  a1 as d,
  N as n,
  M as m,
  r as v,
  o as j,
  j as c,
  m as _,
  k as f,
  l as g,
  z as y,
  F as w,
  af as b
} from './index-820a519e.js'
import { E as h } from './el-switch-6f4f5b6a.js'
import { a as k, E as x } from './el-col-beabe3f6.js'
import { _ as C } from './ContentWrap.vue_vue_type_script_setup_true_lang-37d6ee07.js'
import { _ as R } from './Write.vue_vue_type_script_setup_true_lang-8611dff4.js'
import { _ as D } from './Dialog.vue_vue_type_style_index_0_lang-ce349c68.js'
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
const z = i({
  name: 'IotClientGroup',
  __name: 'Group',
  setup(i) {
    const { t: z } = r(),
      {
        tableRegister: L,
        tableState: S,
        tableMethods: V
      } = s({
        fetchDataApi: async () => {
          const { pageSize: a, currentPage: t } = S,
            l = await e({ page: f(t), limit: f(a) })
          return { list: l.data || [], total: l.count || 0 }
        },
        fetchDelApi: async (e) => 200 === (await a(e)).code
      }),
      { dataList: A, loading: E } = S,
      { getList: F, delList: G } = V,
      I = u([
        { field: 'name', label: '分组名称', disabled: !0, show: !0 },
        { field: 'remark', label: '描述', show: !0 },
        { field: 'order', label: '排序', width: '120px', show: !0 },
        {
          field: 'status',
          label: '状态',
          width: '120px',
          show: !0,
          slots: {
            default: (e) => {
              const a = e.row
              return p(d, null, [p(h, { value: a.status, disabled: !0 }, null)])
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
              return p(d, null, [
                p(
                  n,
                  { type: 'primary', link: !0, size: 'small', onClick: () => J(a) },
                  { default: () => [m('编辑')] }
                ),
                p(
                  n,
                  { type: 'primary', link: !0, size: 'small', onClick: () => O(a) },
                  { default: () => [m('添加子组')] }
                ),
                p(
                  n,
                  {
                    type: 'danger',
                    loading: M.value,
                    link: !0,
                    size: 'small',
                    onClick: () => N(a)
                  },
                  { default: () => [m('删除')] }
                )
              ])
            }
          }
        }
      ]),
      M = v(!1),
      N = async (e) => {
        ;((M.value = !0),
          await G(!0, [e.id]).finally(() => {
            M.value = !1
          }))
      },
      U = v(!1),
      W = v(''),
      q = v(),
      P = v(void 0),
      T = v(''),
      B = v(),
      H = v(!1),
      J = (e) => {
        ;((W.value = '编辑'), (T.value = 'edit'), (q.value = e), (U.value = !0))
      },
      K = () => {
        ;((W.value = '新增'), (T.value = 'add'), (q.value = void 0), (U.value = !0))
      },
      O = (e) => {
        ;((W.value = '添加子部门'),
          (T.value = 'addSon'),
          (P.value = e.id),
          (q.value = void 0),
          (U.value = !0))
      },
      Q = async () => {
        const e = f(B),
          a = await (null == e ? void 0 : e.submit())
        if (a) {
          H.value = !0
          try {
            const e = v({})
            'add' === T.value || 'addSon' === T.value
              ? ((e.value = await t(a)),
                e.value && ((P.value = void 0), (U.value = !1), F(), b.success('添加成功!')))
              : 'edit' === T.value &&
                ((e.value = await l(a)), e.value && ((U.value = !1), F(), b.success('编辑成功!')))
          } finally {
            H.value = !1
          }
        }
      }
    return (e, a) => (
      j(),
      c(
        d,
        null,
        [
          p(f(C), null, {
            default: _(() => [
              p(
                f(o),
                {
                  columns: I,
                  showAction: '',
                  'default-expand-all': '',
                  'node-key': 'id',
                  data: f(A),
                  loading: f(E),
                  onRegister: f(L),
                  onRefresh: f(F)
                },
                {
                  toolbar: _(() => [
                    p(
                      f(k),
                      { gutter: 10 },
                      {
                        default: _(() => [
                          p(
                            f(x),
                            { span: 1.5 },
                            {
                              default: _(() => [
                                p(
                                  f(n),
                                  { type: 'primary', onClick: K },
                                  { default: _(() => [m('新增分组')]), _: 1 }
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
          p(
            f(D),
            {
              modelValue: U.value,
              'onUpdate:modelValue': a[1] || (a[1] = (e) => (U.value = e)),
              title: W.value
            },
            {
              footer: _(() => [
                'detail' !== T.value
                  ? (j(),
                    g(
                      f(n),
                      { key: 0, type: 'primary', loading: H.value, onClick: Q },
                      { default: _(() => [m(y(f(z)('exampleDemo.save')), 1)]), _: 1 },
                      8,
                      ['loading']
                    ))
                  : w('', !0),
                p(
                  f(n),
                  { onClick: a[0] || (a[0] = (e) => (U.value = !1)) },
                  { default: _(() => [m(y(f(z)('dialogDemo.close')), 1)]), _: 1 }
                )
              ]),
              default: _(() => [
                p(
                  R,
                  { ref_key: 'writeRef', ref: B, 'current-row': q.value, 'parent-id': P.value },
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
export { z as default }
