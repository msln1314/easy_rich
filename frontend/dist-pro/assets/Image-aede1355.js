import {
  U as e,
  e as a,
  I as t,
  L as l,
  x as i,
  a1 as s,
  N as o,
  M as r,
  r as n,
  dx as p,
  af as u,
  o as d,
  j as m,
  m as c,
  k as _,
  ai as g,
  z as f
} from './index-820a519e.js'
import { u as v, E as j, _ as h } from './Table.vue_vue_type_script_lang-a0f5d3d3.js'
import { a as w, E as y } from './el-col-beabe3f6.js'
import './el-image-viewer-73f400a0.js'
import { _ as x } from './Search.vue_vue_type_script_setup_true_lang-9de3bdd5.js'
import { _ as b } from './ContentWrap.vue_vue_type_script_setup_true_lang-37d6ee07.js'
import { _ as k } from './Write.vue_vue_type_style_index_0_lang-fe704935.js'
import { _ as z } from './Dialog.vue_vue_type_style_index_0_lang-ce349c68.js'
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
import './el-dropdown-item-a41cbdee.js'
import './refs-374e9e51.js'
/* empty css                   */ import './_Uint8Array-48df3306.js'
import './useIcon-24caadfc.js'
import './el-card-06c161d4.js'
import './useValidator-db15330d.js'
import './use-dialog-2de816dc.js'
const C = (a) => e.post({ url: '/resource/images', headersType: 'multipart/form-data', data: a }),
  R = a({
    name: 'ResourceImage',
    __name: 'Image',
    setup(a) {
      const { t: R } = t(),
        {
          tableRegister: D,
          tableState: S,
          tableMethods: I
        } = v({
          fetchDataApi: async () => {
            const { pageSize: a, currentPage: t } = S,
              l = await ((i = { page: _(t), limit: _(a), ..._(N) }),
              e.get({ url: '/resource/images', params: i }))
            var i
            return { list: l.data || [], total: l.count || 0 }
          },
          fetchDelApi: async (a) => {
            var t
            return 200 === (await ((t = a), e.delete({ url: '/resource/images', data: t }))).code
          }
        }),
        { dataList: P, loading: U, total: A, pageSize: E, currentPage: L } = S,
        { getList: V, delList: F } = I,
        W = l([
          { field: 'selection', type: 'selection', show: !0, disabled: !0 },
          {
            field: 'id',
            label: '编号',
            show: !0,
            disabled: !1,
            align: 'center',
            headerAlign: 'center',
            width: '80px'
          },
          {
            field: 'image_url',
            label: '图片',
            show: !0,
            disabled: !0,
            minWidth: '90px',
            slots: {
              default: (e) => {
                const a = e.row
                return i(s, null, [
                  i('div', { class: 'resource-image-name flex items-center' }, [
                    i('div', null, [
                      i(
                        j,
                        {
                          src: `${a.image_url}?x-oss-process=image/resize,m_fixed,h_100`,
                          'zoom-rate': 1.2,
                          'preview-src-list': P.value.map((e) => e.image_url),
                          'preview-teleported': !0,
                          'initial-index': e.$index,
                          style: 'height: 60px; display: block',
                          fit: 'cover'
                        },
                        null
                      )
                    ]),
                    i('div', { class: 'leading-[35px] ml-2 truncate' }, [
                      i('span', null, [a.filename])
                    ])
                  ])
                ])
              }
            }
          },
          { field: 'remark', label: '备注', show: !1, disabled: !1 },
          { field: 'update_datetime', label: '更新时间', show: !1, width: '180px' },
          { field: 'created_at', label: '创建时间', width: '180px', show: !0 },
          { field: 'create_user.name', label: '创建人', show: !1 },
          {
            field: 'action',
            width: '200px',
            label: '操作',
            fixed: 'right',
            disabled: !1,
            show: !0,
            slots: {
              default: (e) => {
                const a = e.row
                return i(s, null, [
                  i(
                    o,
                    { type: 'primary', link: !0, size: 'small', onClick: () => Q(a.id) },
                    { default: () => [r('复制编号')] }
                  ),
                  i(
                    o,
                    { type: 'primary', link: !0, size: 'small', onClick: () => Q(a.image_url) },
                    { default: () => [r('复制链接')] }
                  ),
                  i(
                    o,
                    {
                      type: 'danger',
                      loading: $.value,
                      link: !0,
                      size: 'small',
                      onClick: () => q(a)
                    },
                    { default: () => [r('删除')] }
                  )
                ])
              }
            }
          }
        ]),
        M = l([
          {
            field: 'filename',
            label: '文件名称',
            component: 'Input',
            componentProps: { clearable: !1, style: { width: '214px' } }
          }
        ]),
        N = n({}),
        T = (e) => {
          ;((L.value = 1), (N.value = e), V())
        },
        $ = n(!1),
        q = async (e) => {
          ;(($.value = !0),
            e
              ? await F(!0, [e.id]).finally(() => {
                  $.value = !1
                })
              : await F(!0).finally(() => {
                  $.value = !1
                }))
        },
        O = n(!1),
        B = n(''),
        G = n(),
        H = n(''),
        J = n(),
        K = n(!1),
        Q = async (e) => {
          const { copy: a } = p()
          return (await a(e), u.success('复制成功'))
        },
        X = () => {
          ;((B.value = '新增图片素材'), (H.value = 'add'), (G.value = void 0), (O.value = !0))
        },
        Y = async () => {
          const e = _(J),
            a = await (null == e ? void 0 : e.submit())
          if (a) {
            if (
              ((K.value = !0),
              null == a || a.images.forEach((e) => (e.status = 'uploading')),
              '2' === (null == a ? void 0 : a.upload_method))
            )
              for (const e of null == a ? void 0 : a.images) {
                const a = new FormData()
                ;(a.append('file', e.raw), await C(a), (e.status = 'success'))
              }
            else if ('1' === (null == a ? void 0 : a.upload_method)) {
              const e =
                null == a
                  ? void 0
                  : a.images.map(async (e) => {
                      const a = new FormData()
                      ;(a.append('file', e.raw), await C(a), (e.status = 'success'))
                    })
              await Promise.all(e)
            }
            ;(V(), (O.value = !1), (K.value = !1))
          }
        }
      return (e, a) => (
        d(),
        m(
          s,
          null,
          [
            i(_(b), null, {
              default: c(() => [
                i(_(x), { schema: M, onReset: T, onSearch: T }, null, 8, ['schema']),
                i(
                  _(h),
                  {
                    'current-page': _(L),
                    'onUpdate:currentPage': a[1] || (a[1] = (e) => (g(L) ? (L.value = e) : null)),
                    'page-size': _(E),
                    'onUpdate:pageSize': a[2] || (a[2] = (e) => (g(E) ? (E.value = e) : null)),
                    showAction: '',
                    columns: W,
                    'default-expand-all': '',
                    'node-key': 'id',
                    data: _(P),
                    loading: _(U),
                    pagination: { total: _(A) },
                    onRegister: _(D),
                    onRefresh: _(V)
                  },
                  {
                    toolbar: c(() => [
                      i(
                        _(w),
                        { gutter: 10 },
                        {
                          default: c(() => [
                            i(
                              _(y),
                              { span: 1.5 },
                              {
                                default: c(() => [
                                  i(
                                    _(o),
                                    { type: 'primary', onClick: X },
                                    { default: c(() => [r('新增图片素材')]), _: 1 }
                                  ),
                                  i(
                                    _(o),
                                    { type: 'danger', onClick: a[0] || (a[0] = (e) => q(null)) },
                                    { default: c(() => [r('批量删除')]), _: 1 }
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
            i(
              _(z),
              {
                modelValue: O.value,
                'onUpdate:modelValue': a[4] || (a[4] = (e) => (O.value = e)),
                title: B.value,
                width: '996px',
                height: '600px',
                top: '3vh'
              },
              {
                footer: c(() => [
                  i(
                    _(o),
                    { type: 'primary', loading: K.value, onClick: Y },
                    { default: c(() => [r(f(_(R)('exampleDemo.save')), 1)]), _: 1 },
                    8,
                    ['loading']
                  ),
                  i(
                    _(o),
                    { onClick: a[3] || (a[3] = (e) => (O.value = !1)) },
                    { default: c(() => [r(f(_(R)('dialogDemo.close')), 1)]), _: 1 }
                  )
                ]),
                default: c(() => [
                  i(k, { ref_key: 'writeRef', ref: J, 'current-row': G.value }, null, 8, [
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
export { R as default }
