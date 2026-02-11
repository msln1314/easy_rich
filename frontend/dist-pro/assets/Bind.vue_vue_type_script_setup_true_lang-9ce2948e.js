import { u as e, F as o } from './useForm-c59a8d29.js'
import { u as t } from './useValidator-db15330d.js'
import { g as l } from './device-8e0c9577.js'
import { u as n } from './dict-451afacd.js'
import {
  e as a,
  r as s,
  a2 as c,
  k as p,
  L as i,
  w as r,
  o as m,
  l as d
} from './index-820a519e.js'
const u = a({
  __name: 'Bind',
  props: { currentRow: { type: Object, default: () => null } },
  setup(a, { expose: u }) {
    const _ = a,
      { required: y, isTelephone: v, isEmail: f } = t(),
      w = s([]),
      b = s([]),
      h = s([]),
      P = s([]),
      g = s([])
    c(async () => {
      await (async () => {
        const e = n(),
          o = await e.getDictObj([
            'connect_type',
            'connect_port',
            'connect_protocol',
            'connect_model'
          ])
        ;((w.value = o.connect_type),
          (b.value = o.connect_port),
          (h.value = o.connect_protocol),
          (g.value = o.connect_model))
      })()
    })
    const j = i([
        {
          field: 'name',
          label: '名称',
          colProps: { span: 24 },
          component: 'Input',
          componentProps: {
            style: { width: '100%' },
            placeholder: '请输入名称',
            readonly: !0,
            disabled: !0
          }
        },
        {
          field: 'sn',
          label: '桩号',
          colProps: { span: 24 },
          component: 'Input',
          componentProps: { style: { width: '100%' }, readonly: !0, disabled: !0 }
        },
        {
          field: 'device_id',
          label: '设备',
          colProps: { span: 16 },
          component: 'SelectV2',
          componentProps: {
            style: { width: '100%' },
            placeholder: '请输入设备MAC搜索',
            multiple: !1,
            clearable: !0,
            remote: !0,
            filterable: !0,
            options: P,
            remoteMethod: async (e) => {
              const o = { keywords: e, page: 1, limit: 20, device_type: '4g_io' },
                t = (await l(o)).data.map((e) => ({ label: `${e.ip} ${e.mac}`, value: e.id }))
              return ((P.value = t), t)
            },
            props: { label: 'ip', value: 'id' }
          },
          value: []
        },
        {
          field: 'port',
          label: '连接端口',
          colProps: { span: 8 },
          component: 'Select',
          componentProps: { style: { width: '100%' }, multiple: !1, options: b },
          value: []
        },
        {
          field: 'connect_model',
          label: '连接模式',
          colProps: { span: 12 },
          component: 'Select',
          componentProps: { style: { width: '100%' }, multiple: !1, options: g },
          value: []
        },
        {
          field: 'connect_type',
          label: '连接类型',
          colProps: { span: 12 },
          component: 'Select',
          componentProps: { style: { width: '100%' }, multiple: !1, options: w },
          value: []
        },
        {
          field: 'connect_protocol',
          label: '连接协议',
          colProps: { span: 12 },
          component: 'Select',
          componentProps: { style: { width: '100%' }, multiple: !1, options: h },
          value: []
        }
      ]),
      R = i({
        name: [y()],
        sn: [y()],
        port: [y()],
        device_id: [y()],
        connect_type: [y()],
        connect_protocol: [y()],
        connect_model: [y()]
      }),
      { formRegister: S, formMethods: x } = e(),
      { setValues: E, getFormData: F, getElFormExpose: M } = x
    return (
      r(
        () => _.currentRow,
        (e) => {
          e && E(e)
        },
        { deep: !0, immediate: !0 }
      ),
      u({
        submit: async () => {
          const e = await M()
          if (await (null == e ? void 0 : e.validate())) {
            return await F()
          }
        }
      }),
      (e, t) => (
        m(),
        d(p(o), { rules: R, onRegister: p(S), schema: j }, null, 8, [
          'rules',
          'onRegister',
          'schema'
        ])
      )
    )
  }
})
export { u as _ }
