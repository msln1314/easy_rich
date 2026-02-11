import { a as e, b as t, d as l, p as a, c as i, e as o } from './device-8e0c9577.js'
import { _ as s, g as r } from './Write.vue_vue_type_script_setup_true_lang-d03f61b9.js'
import { u as p, _ as n } from './Table.vue_vue_type_script_lang-a0f5d3d3.js'
import {
  e as u,
  I as d,
  r as c,
  a2 as m,
  aj as v,
  L as _,
  x as f,
  k as j,
  a1 as w,
  a0 as h,
  Z as g,
  N as y,
  M as b,
  o as x,
  j as k,
  m as P,
  ai as I,
  l as C,
  ak as D,
  z as S,
  F as z,
  af as A
} from './index-820a519e.js'
import { a as L, E as R } from './el-col-beabe3f6.js'
import { E as T } from './el-divider-9c19755b.js'
import { _ as W } from './Search.vue_vue_type_script_setup_true_lang-9de3bdd5.js'
import { _ as E } from './ContentWrap.vue_vue_type_script_setup_true_lang-37d6ee07.js'
import { _ as O } from './Dialog.vue_vue_type_style_index_0_lang-ce349c68.js'
import { s as M } from './dict-4a6e55e6.js'
import { u as U } from './dict-451afacd.js'
import { _ as V } from './Import.vue_vue_type_script_setup_true_lang-7af5b51d.js'
import { _ as F } from './DictTag.vue_vue_type_script_lang-ded36db6.js'
import './useForm-c59a8d29.js'
import './el-form-item-2e860f96.js'
import './el-tooltip-4ed993c7.js'
import './el-popper-797844d6.js'
import './isNil-1f22f7b0.js'
import './focus-trap-949626e0.js'
import './el-input-5ae17c8f.js'
import './event-5568c9d8.js'
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
import './scroll-ac7d0423.js'
import './validator-a9d8fe4c.js'
import './el-switch-6f4f5b6a.js'
import './el-tree-8dac9473.js'
import './index-55f4d4a6.js'
import './el-progress-97dbc0fb.js'
import './style.css_vue_type_style_index_0_src_true_lang-4a035adc.js'
import './useValidator-db15330d.js'
import './el-message-box-faa52860.js'
import './el-overlay-34b9d092.js'
import './vnode-06a99f10.js'
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
import './use-dialog-2de816dc.js'
import './dict-c8c7fcf4.js'
import './el-link-dbc80422.js'
import './el-popconfirm-e835aac7.js'
import './client-5512447a.js'
const G = u({
  name: 'IotDevice',
  __name: 'Device',
  setup(u) {
    const { t: G } = d(),
      {
        tableRegister: N,
        tableState: q,
        tableMethods: B
      } = p({
        fetchDataApi: async () => {
          const { pageSize: e, currentPage: l } = q,
            a = await t({ page: j(l), limit: j(e), ...j(re) })
          return { list: a.data || [], total: a.count || 0 }
        },
        fetchDelApi: async (e) => 200 === (await l(e)).code,
        fetchExportApi: async (e) => {
          const { pageSize: t, currentPage: l } = q
          return await a({ page: j(l), limit: j(t), ...j(re) }, e)
        }
      }),
      { dataList: K, loading: Q, total: Z, pageSize: H, currentPage: J } = q,
      { getList: X, delList: Y, getSelections: $, exportQueryList: ee } = B,
      te = c([]),
      le = c([]),
      ae = c([]),
      ie = c(null)
    ;(m(() => {
      ie.value = setInterval(X, 5e4)
    }),
      v(() => {
        clearInterval(ie.value)
      }),
      m(async () => {
        await (async () => {
          const e = U(),
            t = await e.getDictObj(['Device_type', 'device_tag', 'port_status'])
          ;((te.value = t.Device_type), (le.value = t.connect_type))
          const l = await r()
          ae.value = l.data
        })()
      }))
    const oe = _([
        { field: 'selection', type: 'selection', show: !0, disabled: !0 },
        { field: 'ip', label: 'IP地址', width: '100px', show: !0, disabled: !1 },
        {
          field: 'mac',
          label: 'MAC地址',
          show: !0,
          align: 'center',
          showOverflowTooltip: !1,
          minWidth: '220px'
        },
        {
          field: 'device_type',
          label: '客户端类型',
          show: !1,
          slots: {
            default: (e) => {
              const t = e.row
              return f(w, null, [f('div', null, [M(j(te), t.device_type)])])
            }
          }
        },
        {
          field: 'device_tag',
          label: '设备标记',
          show: !1,
          slots: {
            default: (e) => {
              const t = e.row
              return f(w, null, [f(F, { type: 'device_tag', value: t.device_tag }, null)])
            }
          }
        },
        {
          field: 'online_status',
          label: '在线状态',
          show: !0,
          showOverflowTooltip: !1,
          minWidth: '120px',
          slots: {
            default: (e) => {
              const t = e.row
              return f(w, null, [
                f(F, { type: 'online_status', value: t.online_status }, null),
                f(T, { direction: 'vertical' }, null),
                t.last_time
              ])
            }
          }
        },
        { field: 'address', label: '位置', show: !0, showOverflowTooltip: !1, disabled: !0 },
        { field: 'area', label: '单位', show: !0, disabled: !0 },
        {
          field: 'is_active',
          label: '是否可用',
          show: !1,
          slots: {
            default: (e) => {
              const t = e.row
              return f(w, null, [f(F, { type: 'active_status', value: t.is_active }, null)])
            }
          }
        },
        { field: 'ccid', label: 'ccid', width: '220px', show: !1 },
        { field: 'phone', label: 'phone', width: '100px', show: !0 },
        { field: 'created_at', label: '创建时间', width: '190px', show: !1 },
        {
          field: 'remark',
          label: '备注',
          width: '100px',
          show: !0,
          showOverflowTooltip: !1,
          resizable: !0
        },
        {
          field: 'action',
          width: '180px',
          label: '操作',
          showOverflowTooltip: !1,
          show: !0,
          slots: {
            default: (e) => {
              const t = e.row
              return f(w, null, [
                h(
                  f(
                    y,
                    { type: 'primary', link: !0, size: 'small', onClick: () => we(t) },
                    { default: () => [b('编辑')] }
                  ),
                  [[g('hasPermi'), ['iot.device.update']]]
                ),
                h(
                  f(
                    y,
                    {
                      type: 'danger',
                      loading: ue.value,
                      link: !0,
                      size: 'small',
                      onClick: () => de(t)
                    },
                    { default: () => [b('删除')] }
                  ),
                  [[g('hasPermi'), ['iot.Device.delete']]]
                )
              ])
            }
          }
        }
      ]),
      se = _([
        {
          field: 'ip',
          label: 'IP',
          component: 'Input',
          componentProps: { clearable: !1, style: { width: '214px' } },
          formItemProps: { labelWidth: '80px' }
        },
        {
          field: 'mac',
          label: 'MAC',
          component: 'Input',
          componentProps: { clearable: !1, style: { width: '214px' } },
          formItemProps: { labelWidth: '80px' }
        },
        {
          field: 'ccid',
          label: 'CCID',
          component: 'Input',
          componentProps: { clearable: !1, style: { width: '214px' } },
          formItemProps: { labelWidth: '80px' }
        },
        {
          field: 'is_active',
          label: '状态',
          component: 'Select',
          componentProps: {
            style: { width: '180px' },
            options: [
              { label: '正常', value: !0 },
              { label: '停用', value: !1 }
            ]
          }
        },
        {
          field: 'product_id',
          label: '产品',
          colProps: { span: 12 },
          component: 'Select',
          componentProps: {
            style: { width: '100%' },
            nodeKey: 'value',
            checkStrictly: !0,
            defaultExpandAll: !0,
            options: ae
          }
        },
        {
          field: 'online_status',
          label: '在线状态',
          component: 'Select',
          componentProps: {
            style: { width: '180px' },
            options: [
              { label: '在线', value: '1' },
              { label: '离线', value: '0' },
              { label: '空', value: '-1' }
            ]
          }
        }
      ]),
      re = c({}),
      pe = (e) => {
        ;((J.value = 1), (re.value = e), X())
      },
      ne = () => {
        ;((J.value = 1), (re.value = {}), X())
      },
      ue = c(!1),
      de = async (e) => {
        ;((ue.value = !0),
          e
            ? await Y(!0, [e.id]).finally(() => {
                ue.value = !1
              })
            : await Y(!0).finally(() => {
                ue.value = !1
              }))
      },
      ce = c(!1),
      me = c(''),
      ve = c(),
      _e = c(''),
      fe = c()
    c()
    const je = c(!1),
      we = async (t) => {
        const l = await e(t.id)
        l && ((me.value = '编辑设备'), (_e.value = 'edit'), (ve.value = l.data), (ce.value = !0))
      },
      he = () => {
        ;((me.value = '新增设备'), (_e.value = 'add'), (ve.value = void 0), (ce.value = !0))
      },
      ge = () => {
        ;((me.value = '批量导入设备'), (_e.value = 'import'), (ve.value = void 0), (ce.value = !0))
      }
    c([])
    const ye = async () => {
      const e = j(fe),
        t = await (null == e ? void 0 : e.submit())
      if (t) {
        je.value = !0
        try {
          const e = c({})
          'add' === _e.value
            ? ((e.value = await i(t)),
              e.value && ((ce.value = !1), await X(), A.success('添加成功!')))
            : 'edit' === _e.value &&
              ((e.value = await o(t)),
              e.value && ((ce.value = !1), await X(), A.success('编辑成功!')))
        } finally {
          je.value = !1
        }
      }
    }
    return (e, t) => {
      const l = g('hasPermi')
      return (
        x(),
        k(
          w,
          null,
          [
            f(j(E), null, {
              default: P(() => [
                f(j(W), { schema: se, onReset: ne, onSearch: pe }, null, 8, ['schema']),
                f(
                  j(n),
                  {
                    'current-page': j(J),
                    'onUpdate:currentPage': t[2] || (t[2] = (e) => (I(J) ? (J.value = e) : null)),
                    'page-size': j(H),
                    'onUpdate:pageSize': t[3] || (t[3] = (e) => (I(H) ? (H.value = e) : null)),
                    showAction: '',
                    columns: oe,
                    'default-expand-all': '',
                    'node-key': 'id',
                    data: j(K),
                    loading: j(Q),
                    pagination: { total: j(Z) },
                    onRegister: j(N),
                    onRefresh: j(X)
                  },
                  {
                    toolbar: P(() => [
                      f(
                        j(L),
                        { gutter: 10 },
                        {
                          default: P(() => [
                            h(
                              (x(),
                              C(
                                j(R),
                                { span: 1.5 },
                                {
                                  default: P(() => [
                                    f(
                                      j(y),
                                      { type: 'primary', onClick: he },
                                      { default: P(() => [b('新增设备')]), _: 1 }
                                    )
                                  ]),
                                  _: 1
                                }
                              )),
                              [[l, ['iot.device.create']]]
                            ),
                            h(
                              (x(),
                              C(
                                j(R),
                                { span: 1.5 },
                                {
                                  default: P(() => [
                                    f(
                                      j(y),
                                      { onClick: ge },
                                      { default: P(() => [b('批量导入设备')]), _: 1 }
                                    )
                                  ]),
                                  _: 1
                                }
                              )),
                              [[l, ['iot.device.import']]]
                            ),
                            h(
                              (x(),
                              C(
                                j(R),
                                { span: 1.5 },
                                {
                                  default: P(() => [
                                    f(
                                      j(y),
                                      { onClick: t[0] || (t[0] = (e) => j(ee)()) },
                                      { default: P(() => [b('导出筛选设备')]), _: 1 }
                                    )
                                  ]),
                                  _: 1
                                }
                              )),
                              [[l, ['iot.device.export']]]
                            ),
                            h(
                              (x(),
                              C(
                                j(R),
                                { span: 1.5 },
                                {
                                  default: P(() => [
                                    f(
                                      j(y),
                                      { type: 'danger', onClick: t[1] || (t[1] = (e) => de(null)) },
                                      { default: P(() => [b('批量删除')]), _: 1 }
                                    )
                                  ]),
                                  _: 1
                                }
                              )),
                              [[l, ['iot.device.delete']]]
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
            f(
              j(O),
              {
                modelValue: ce.value,
                'onUpdate:modelValue': t[5] || (t[5] = (e) => (ce.value = e)),
                title: me.value,
                height: 600,
                width: 700
              },
              D(
                {
                  default: P(() => [
                    'add' === _e.value || 'edit' === _e.value
                      ? (x(),
                        C(
                          s,
                          { key: 0, ref_key: 'writeRef', ref: fe, 'current-row': ve.value },
                          null,
                          8,
                          ['current-row']
                        ))
                      : 'import' === _e.value
                        ? (x(), C(V, { key: 1, onGetList: j(X) }, null, 8, ['onGetList']))
                        : z('', !0)
                  ]),
                  _: 2
                },
                [
                  'add' === _e.value || 'edit' === _e.value || 'bind' === _e.value
                    ? {
                        name: 'footer',
                        fn: P(() => [
                          f(
                            j(y),
                            { type: 'primary', loading: je.value, onClick: ye },
                            { default: P(() => [b(S(j(G)('exampleDemo.save')), 1)]), _: 1 },
                            8,
                            ['loading']
                          ),
                          f(
                            j(y),
                            { onClick: t[4] || (t[4] = (e) => (ce.value = !1)) },
                            { default: P(() => [b(S(j(G)('dialogDemo.close')), 1)]), _: 1 }
                          )
                        ]),
                        key: '0'
                      }
                    : void 0
                ]
              ),
              1032,
              ['modelValue', 'title']
            )
          ],
          64
        )
      )
    }
  }
})
export { G as default }
