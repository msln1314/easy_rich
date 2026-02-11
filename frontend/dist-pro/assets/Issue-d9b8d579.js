import { g as e, d as t } from './issue-784d4340.js'
import { u as s, _ as a } from './Table.vue_vue_type_script_lang-a0f5d3d3.js'
import {
  e as i,
  A as l,
  r as o,
  L as r,
  x as p,
  a1 as n,
  N as m,
  M as d,
  o as u,
  l as c,
  m as j,
  k as _,
  ai as f
} from './index-820a519e.js'
import { E as g } from './el-switch-6f4f5b6a.js'
import { a as h, E as v } from './el-col-beabe3f6.js'
import { _ as b } from './Search.vue_vue_type_script_setup_true_lang-9de3bdd5.js'
import { _ as w } from './ContentWrap.vue_vue_type_script_setup_true_lang-37d6ee07.js'
import { u as y } from './dict-451afacd.js'
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
import './dict-c8c7fcf4.js'
const x = i({
  name: 'HelpIssue',
  __name: 'Issue',
  setup(i) {
    const { push: x } = l(),
      {
        tableRegister: k,
        tableState: S,
        tableMethods: z
      } = s({
        fetchDataApi: async () => {
          const { pageSize: t, currentPage: s } = S,
            a = await e({ page: _(s), limit: _(t), ..._(N) })
          return { list: a.data || [], total: a.count || 0 }
        },
        fetchDelApi: async (e) => 200 === (await t(e)).code
      }),
      { dataList: P, loading: R, total: A, pageSize: C, currentPage: I } = S,
      { getList: L, delList: D } = z,
      E = o([])
    ;(async () => {
      const e = y(),
        t = await e.getDictObj(['sys_vadmin_platform'])
      E.value = t.sys_vadmin_platform
    })()
    const U = r([
        { field: 'id', label: '编号', show: !0, disabled: !0, width: '120px' },
        { field: 'category.name', label: '类别名称', width: '200px', show: !0, disabled: !0 },
        { field: 'title', label: '标题', show: !0 },
        { field: 'view_number', label: '查看次数', show: !0, width: '100px' },
        {
          field: 'is_active',
          label: '是否可见',
          show: !0,
          width: '100px',
          slots: {
            default: (e) => {
              const t = e.row
              return p(n, null, [p(g, { value: t.is_active, disabled: !0 }, null)])
            }
          }
        },
        { field: 'created_at', label: '创建时间', show: !0, width: '200px', sortable: !0 },
        { field: 'create_user.name', label: '创建人', show: !0, width: '100px' },
        {
          field: 'action',
          width: '120px',
          label: '操作',
          show: !0,
          slots: {
            default: (e) => {
              const t = e.row
              return p(n, null, [
                p(
                  m,
                  { type: 'primary', link: !0, size: 'small', onClick: () => O(t) },
                  { default: () => [d('编辑')] }
                ),
                p(
                  m,
                  {
                    type: 'danger',
                    loading: F.value,
                    link: !0,
                    size: 'small',
                    onClick: () => H(t)
                  },
                  { default: () => [d('删除')] }
                )
              ])
            }
          }
        }
      ]),
      M = r([
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
          componentProps: { style: { width: '214px' }, options: E.value }
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
      N = o({}),
      q = (e) => {
        ;((I.value = 1), (N.value = e), L())
      },
      F = o(!1),
      H = async (e) => {
        ;((F.value = !0),
          await D(!0, [e.id]).finally(() => {
            F.value = !1
          }))
      },
      O = async (e) => {
        x(`/help/issue/form?id=${e.id}`)
      },
      T = () => {
        x('/help/issue/form')
      }
    return (e, t) => (
      u(),
      c(_(w), null, {
        default: j(() => [
          p(_(b), { schema: M, onReset: q, onSearch: q }, null, 8, ['schema']),
          p(
            _(a),
            {
              'current-page': _(I),
              'onUpdate:currentPage': t[0] || (t[0] = (e) => (f(I) ? (I.value = e) : null)),
              'page-size': _(C),
              'onUpdate:pageSize': t[1] || (t[1] = (e) => (f(C) ? (C.value = e) : null)),
              showAction: '',
              columns: U,
              'default-expand-all': '',
              'node-key': 'id',
              data: _(P),
              loading: _(R),
              pagination: { total: _(A) },
              onRegister: _(k),
              onRefresh: _(L)
            },
            {
              toolbar: j(() => [
                p(
                  _(h),
                  { gutter: 10 },
                  {
                    default: j(() => [
                      p(
                        _(v),
                        { span: 1.5 },
                        {
                          default: j(() => [
                            p(
                              _(m),
                              { type: 'primary', onClick: T },
                              { default: j(() => [d('新增常见问题')]), _: 1 }
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
      })
    )
  }
})
export { x as default }
