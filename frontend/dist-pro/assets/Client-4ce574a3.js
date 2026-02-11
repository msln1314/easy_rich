import {
  g as e,
  p as t,
  a as l,
  b as a,
  d as o,
  c as s,
  e as i,
  f as n,
  h as r
} from './client-5512447a.js'
import { g as u } from './client_group-aeb78440.js'
import { u as p, _ as d } from './Table.vue_vue_type_script_lang-a0f5d3d3.js'
import {
  e as c,
  I as m,
  r as v,
  a2 as _,
  aj as f,
  L as w,
  x as y,
  k as b,
  a1 as h,
  M as j,
  a0 as g,
  Z as x,
  N as k,
  af as C,
  o as P,
  j as z,
  m as S,
  ai as T,
  l as I,
  ak as O,
  z as W,
  F as A
} from './index-820a519e.js'
import { E as R } from './el-switch-6f4f5b6a.js'
import { a as D, E } from './el-col-beabe3f6.js'
import { E as L } from './el-message-box-faa52860.js'
import './el-input-5ae17c8f.js'
import './el-overlay-34b9d092.js'
import { E as V } from './el-divider-9c19755b.js'
import { _ as U } from './Search.vue_vue_type_script_setup_true_lang-9de3bdd5.js'
import { _ as M } from './ContentWrap.vue_vue_type_script_setup_true_lang-37d6ee07.js'
import { _ as B } from './Write.vue_vue_type_script_setup_true_lang-590cea11.js'
import { _ as F } from './Dialog.vue_vue_type_style_index_0_lang-ce349c68.js'
import { s as G } from './dict-4a6e55e6.js'
import { u as N } from './dict-451afacd.js'
import { _ as q } from './Import.vue_vue_type_script_setup_true_lang-0031ffd0.js'
import { _ as K } from './Bind.vue_vue_type_script_setup_true_lang-9ce2948e.js'
import { _ as Q } from './DictTag.vue_vue_type_script_lang-ded36db6.js'
import './el-table-column-36e57984.js'
import './el-popper-797844d6.js'
import './isNil-1f22f7b0.js'
import './focus-trap-949626e0.js'
import './isEqual-cb9e370d.js'
import './el-checkbox-77b6829c.js'
import './event-5568c9d8.js'
import './debounce-5bc596c6.js'
import './index-eb31d854.js'
import './el-tooltip-4ed993c7.js'
/* empty css               */ import './el-pagination-60eda460.js'
import './el-select-38080147.js'
import './index-56bc6266.js'
import './strings-ed83d626.js'
import './scroll-ac7d0423.js'
import './validator-a9d8fe4c.js'
import './dropdown-394a0a1a.js'
import './el-image-viewer-73f400a0.js'
import './useForm-c59a8d29.js'
import './el-form-item-2e860f96.js'
/* empty css                          */ import './el-date-picker-6b1a21d2.js'
import './dayjs.min-e5ba30ae.js'
import './el-radio-group-4cb40939.js'
import './el-tree-8dac9473.js'
import './index-55f4d4a6.js'
import './el-progress-97dbc0fb.js'
import './style.css_vue_type_style_index_0_src_true_lang-4a035adc.js'
import './el-dropdown-item-a41cbdee.js'
import './refs-374e9e51.js'
/* empty css                   */ import './_Uint8Array-48df3306.js'
import './index-2b3f7e71.js'
import './vnode-06a99f10.js'
import './useIcon-24caadfc.js'
import './el-card-06c161d4.js'
import './useValidator-db15330d.js'
import './use-dialog-2de816dc.js'
import './dict-c8c7fcf4.js'
import './el-link-dbc80422.js'
import './el-popconfirm-e835aac7.js'
import './device-8e0c9577.js'
const Z = c({
  name: 'IotClient',
  __name: 'Client',
  setup(c) {
    const { t: Z } = m(),
      {
        tableRegister: H,
        tableState: J,
        tableMethods: X
      } = p({
        fetchDataApi: async () => {
          const { pageSize: e, currentPage: t } = J,
            l = await a({ page: b(t), limit: b(e), ...b(ve) })
          return { list: l.data || [], total: l.count || 0 }
        },
        fetchDelApi: async (e) => 200 === (await o(e)).code,
        fetchExportApi: async (e) => {
          const { pageSize: t, currentPage: l } = J
          return await s({ page: b(l), limit: b(t), ...b(ve) }, e)
        }
      }),
      { dataList: Y, loading: $, total: ee, pageSize: te, currentPage: le } = J,
      { getList: ae, delList: oe, getSelections: se, exportQueryList: ie } = X,
      ne = v([]),
      re = v([]),
      ue = v([]),
      pe = v([]),
      de = v(null)
    ;(_(() => {
      de.value = setInterval(ae, 5e4)
    }),
      f(() => {
        clearInterval(de.value)
      }),
      _(async () => {
        await (async () => {
          const e = N(),
            t = await e.getDictObj(['client_type', 'connect_type', 'port_status'])
          ;((ne.value = t.client_type), (re.value = t.connect_type), (ue.value = t.port_status))
          const l = await u()
          pe.value = l.data
        })()
      }))
    const ce = w([
        { field: 'selection', type: 'selection', show: !0, disabled: !0 },
        { field: 'id', label: '编号', width: '100px', show: !1, disabled: !1 },
        {
          field: 'sn',
          label: '桩编号',
          show: !0,
          align: 'center',
          showOverflowTooltip: !1,
          minWidth: '220px',
          cellStyle: { 'background-color': '#f5f7fa', color: '#f5f7fa', 'font-size': '15px' }
        },
        {
          field: 'name',
          label: '站名称',
          show: !0,
          resizable: !0,
          minWidth: '220px',
          showOverflowTooltip: !1
        },
        {
          field: 'client_type',
          label: '充电桩类型',
          show: !1,
          slots: {
            default: (e) => {
              const t = e.row
              return y(h, null, [y('div', null, [G(b(ne), t.client_type)])])
            }
          }
        },
        {
          field: 'connect_type',
          label: '连接类型',
          show: !1,
          slots: {
            default: (e) => {
              const t = e.row
              return y(h, null, [y(Q, { type: 'connect_type', value: t.connect_type }, null)])
            }
          }
        },
        {
          field: 'port_status',
          label: '端口状态',
          show: !0,
          showOverflowTooltip: !1,
          minWidth: '120px',
          slots: {
            default: (e) => {
              const t = e.row
              return y(h, null, [
                y(Q, { type: 'online_status', value: t.online_status }, null),
                y(V, { direction: 'vertical' }, null),
                y(Q, { type: 'port_status', value: t.port_status }, null)
              ])
            }
          }
        },
        { field: 'address', label: '位置', show: !0, showOverflowTooltip: !1, disabled: !0 },
        { field: 'area', label: '单位', show: !0, disabled: !0 },
        { field: 'client_tag', label: '标签', show: !0 },
        {
          field: 'port',
          label: '连接信息',
          resizable: !0,
          minWidth: '180px',
          showOverflowTooltip: !1,
          slots: {
            default: (e) => {
              var t, l
              const a = e.row
              return y(h, null, [
                y('div', { class: 'text-truncate' }, [
                  a.connect_type,
                  a.connect_protocol,
                  (null == (t = a.device) ? void 0 : t.connect_time) ? a.device.connect_time : '',
                  y('br', null, null),
                  j(' 最近:'),
                  null == (l = a.device) ? void 0 : l.last_time
                ])
              ])
            }
          },
          show: !0
        },
        {
          field: 'device',
          label: '设备',
          show: !0,
          resizable: !0,
          minWidth: '140px',
          showOverflowTooltip: !1,
          slots: {
            default: (e) => {
              var t, l
              const a = e.row
              return y(h, null, [
                y('div', null, [
                  a.port,
                  j(' '),
                  a.connect_model,
                  y('br', null, null),
                  j(' '),
                  null == (t = a.device) ? void 0 : t.ip,
                  y('br', null, null),
                  j(' '),
                  null == (l = a.device) ? void 0 : l.mac
                ])
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
              const t = e.row
              return y(h, null, [y(Q, { type: 'active_status', value: t.is_active }, null)])
            }
          }
        },
        {
          field: 'bind_status',
          label: '绑定状态',
          show: !0,
          showOverflowTooltip: !1,
          resizable: !0,
          minWidth: '120px',
          slots: {
            default: (e) => {
              const t = e.row
              return y(h, null, [y(Q, { type: 'bind_status', value: t.bind_status }, null)])
            }
          }
        },
        { field: 'bind_time', label: '绑定时间', show: !1, width: '190px' },
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
              const t = e.row,
                l = ['iot.Client.bind']
              return y(h, null, [
                (1 == t.port_status || 0 == t.port_status) &&
                  1 == t.online_status &&
                  g(
                    y(
                      R,
                      {
                        size: 'default',
                        'active-value': 1,
                        'inactive-value': 0,
                        'active-text': '合闸',
                        'inactive-text': '断开',
                        'inline-prompt': !0,
                        onClick: async () => await Te(t),
                        modelValue: t.port_status,
                        'onUpdate:modelValue': (e) => (t.port_status = e)
                      },
                      null
                    ),
                    [[x('hasPermi'), ['iot.Client.on_of']]]
                  ),
                g(
                  y(
                    k,
                    { type: 'primary', link: !0, size: 'small', onClick: () => Pe(t) },
                    { default: () => [j('编辑')] }
                  ),
                  [[x('hasPermi'), ['iot.Client.update']]]
                ),
                0 == t.bind_status &&
                  g(
                    y(
                      k,
                      { type: 'success', link: !0, size: 'small', onClick: () => ze(t) },
                      { default: () => [j('绑定')] }
                    ),
                    [[x('hasPermi'), l]]
                  ),
                1 == t.bind_status &&
                  g(
                    y(
                      k,
                      { type: 'danger', link: !0, size: 'small', onClick: () => Se(t) },
                      { default: () => [j('解绑'), 1 == t.bind_status] }
                    ),
                    [[x('hasPermi'), l]]
                  ),
                g(
                  y(
                    k,
                    {
                      type: 'danger',
                      loading: we.value,
                      link: !0,
                      size: 'small',
                      onClick: () => ye(t)
                    },
                    { default: () => [j('删除')] }
                  ),
                  [[x('hasPermi'), ['iot.Client.delete']]]
                )
              ])
            }
          }
        }
      ]),
      me = w([
        {
          field: 'name',
          label: '桩编号|站名称',
          component: 'Input',
          componentProps: { clearable: !1, style: { width: '214px' } }
        },
        {
          field: 'keywords',
          label: 'IP|MAC',
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
          field: 'port_status',
          label: '端口状态',
          component: 'Select',
          componentProps: {
            style: { width: '180px' },
            options: [
              { label: '合闸', value: 1 },
              { label: '断开', value: 0 },
              { label: '未使用', value: -1 }
            ]
          }
        },
        {
          field: 'group_id',
          label: '组',
          colProps: { span: 24 },
          component: 'TreeSelect',
          componentProps: {
            style: { width: '100%' },
            checkStrictly: !0,
            placeholder: '请选择组',
            nodeKey: 'value',
            defaultExpandAll: !0,
            data: pe
          }
        },
        {
          field: 'bind_status',
          label: '绑定状态',
          component: 'Select',
          componentProps: {
            style: { width: '180px' },
            options: [
              { label: '是', value: 1 },
              { label: '否', value: 0 }
            ]
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
      ve = v({}),
      _e = (e) => {
        ;((le.value = 1), (ve.value = e), ae())
      },
      fe = () => {
        ;((le.value = 1), (ve.value = {}), ae())
      },
      we = v(!1),
      ye = async (e) => {
        ;((we.value = !0),
          e
            ? await oe(!0, [e.id]).finally(() => {
                we.value = !1
              })
            : await oe(!0).finally(() => {
                we.value = !1
              }))
      },
      be = v(!1),
      he = v(''),
      je = v(),
      ge = v(''),
      xe = v(),
      ke = v(),
      Ce = v(!1),
      Pe = async (t) => {
        const l = await e(t.id)
        l && ((he.value = '编辑充电桩'), (ge.value = 'edit'), (je.value = l.data), (be.value = !0))
      },
      ze = async (t) => {
        const l = await e(t.id)
        l && ((he.value = '绑定充电桩'), (ge.value = 'bind'), (je.value = l.data), (be.value = !0))
      },
      Se = async (e) => {
        try {
          ;(await L.confirm('确认要解绑' + e.sn + '"设备吗?'),
            C.success('执行中，请等待....'),
            await t({ id: e.id }),
            await ae(),
            C.success('解绑成功'))
        } catch {
          C.error('执行失败')
        }
      },
      Te = async (e) => {
        try {
          const t = 1 == e.port_status ? '合闸' : '断开'
          ;(await L.confirm('确认要"' + t + '""' + e.sn + '"设备吗?'),
            C.success('执行中，请等待....'),
            await l({ id: e.id, port_status: e.port_status }),
            await ae(),
            C.success(t + '执行成功'))
        } catch {
          ;(C.error('执行失败'), (e.port_status = 1 == e.port_status ? 0 : 1))
        }
      },
      Ie = () => {
        ;((he.value = '新增充电桩'), (ge.value = 'add'), (je.value = void 0), (be.value = !0))
      },
      Oe = () => {
        ;((he.value = '批量导入充电桩'),
          (ge.value = 'import'),
          (je.value = void 0),
          (be.value = !0))
      }
    v([])
    const We = async () => {
      const e = 'bind' === ge.value ? b(ke) : b(xe),
        t = await (null == e ? void 0 : e.submit())
      if (t) {
        Ce.value = !0
        try {
          const e = v({})
          'add' === ge.value
            ? ((e.value = await i(t)),
              e.value && ((be.value = !1), await ae(), C.success('添加成功!')))
            : 'edit' === ge.value
              ? ((e.value = await n(t)),
                e.value && ((be.value = !1), await ae(), C.success('编辑成功!')))
              : 'bind' === ge.value &&
                ((e.value = await r(t)),
                e.value && ((be.value = !1), await ae(), C.success('绑定成功!')))
        } finally {
          Ce.value = !1
        }
      }
    }
    return (e, t) => {
      const l = x('hasPermi')
      return (
        P(),
        z(
          h,
          null,
          [
            y(b(M), null, {
              default: S(() => [
                y(b(U), { schema: me, onReset: fe, onSearch: _e }, null, 8, ['schema']),
                y(
                  b(d),
                  {
                    'current-page': b(le),
                    'onUpdate:currentPage': t[2] || (t[2] = (e) => (T(le) ? (le.value = e) : null)),
                    'page-size': b(te),
                    'onUpdate:pageSize': t[3] || (t[3] = (e) => (T(te) ? (te.value = e) : null)),
                    showAction: '',
                    columns: ce,
                    'default-expand-all': '',
                    'node-key': 'id',
                    data: b(Y),
                    loading: b($),
                    pagination: { total: b(ee) },
                    onRegister: b(H),
                    onRefresh: b(ae)
                  },
                  {
                    toolbar: S(() => [
                      y(
                        b(D),
                        { gutter: 10 },
                        {
                          default: S(() => [
                            g(
                              (P(),
                              I(
                                b(E),
                                { span: 1.5 },
                                {
                                  default: S(() => [
                                    y(
                                      b(k),
                                      { type: 'primary', onClick: Ie },
                                      { default: S(() => [j('新增充电桩')]), _: 1 }
                                    )
                                  ]),
                                  _: 1
                                }
                              )),
                              [[l, ['iot.Client.create']]]
                            ),
                            g(
                              (P(),
                              I(
                                b(E),
                                { span: 1.5 },
                                {
                                  default: S(() => [
                                    y(
                                      b(k),
                                      { onClick: Oe },
                                      { default: S(() => [j('批量导入充电桩')]), _: 1 }
                                    )
                                  ]),
                                  _: 1
                                }
                              )),
                              [[l, ['iot.Client.import']]]
                            ),
                            g(
                              (P(),
                              I(
                                b(E),
                                { span: 1.5 },
                                {
                                  default: S(() => [
                                    y(
                                      b(k),
                                      { onClick: t[0] || (t[0] = (e) => b(ie)()) },
                                      { default: S(() => [j('导出筛选充电桩')]), _: 1 }
                                    )
                                  ]),
                                  _: 1
                                }
                              )),
                              [[l, ['iot.Client.export']]]
                            ),
                            g(
                              (P(),
                              I(
                                b(E),
                                { span: 1.5 },
                                {
                                  default: S(() => [
                                    y(
                                      b(k),
                                      { type: 'danger', onClick: t[1] || (t[1] = (e) => ye(null)) },
                                      { default: S(() => [j('批量删除')]), _: 1 }
                                    )
                                  ]),
                                  _: 1
                                }
                              )),
                              [[l, ['iot.Client.delete']]]
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
            y(
              b(F),
              {
                modelValue: be.value,
                'onUpdate:modelValue': t[5] || (t[5] = (e) => (be.value = e)),
                title: he.value,
                height: 600,
                width: 700
              },
              O(
                {
                  default: S(() => [
                    'add' === ge.value || 'edit' === ge.value
                      ? (P(),
                        I(
                          B,
                          {
                            key: 0,
                            ref_key: 'writeRef',
                            ref: xe,
                            actionType: ge.value,
                            'current-row': je.value
                          },
                          null,
                          8,
                          ['actionType', 'current-row']
                        ))
                      : 'bind' === ge.value
                        ? (P(),
                          I(
                            K,
                            { key: 1, ref_key: 'bindRef', ref: ke, 'current-row': je.value },
                            null,
                            8,
                            ['current-row']
                          ))
                        : 'import' === ge.value
                          ? (P(), I(q, { key: 2, onGetList: b(ae) }, null, 8, ['onGetList']))
                          : A('', !0)
                  ]),
                  _: 2
                },
                [
                  'add' === ge.value || 'edit' === ge.value || 'bind' === ge.value
                    ? {
                        name: 'footer',
                        fn: S(() => [
                          y(
                            b(k),
                            { type: 'primary', loading: Ce.value, onClick: We },
                            { default: S(() => [j(W(b(Z)('exampleDemo.save')), 1)]), _: 1 },
                            8,
                            ['loading']
                          ),
                          y(
                            b(k),
                            { onClick: t[4] || (t[4] = (e) => (be.value = !1)) },
                            { default: S(() => [j(W(b(Z)('dialogDemo.close')), 1)]), _: 1 }
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
export { Z as default }
