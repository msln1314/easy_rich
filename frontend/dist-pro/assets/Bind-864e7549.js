import { u as e, F as o } from './useForm-c59a8d29.js'
import { u as t } from './useValidator-db15330d.js'
import { g as s } from './device-8e0c9577.js'
import { u as l } from './dict-451afacd.js'
import {
  e as i,
  r as p,
  a2 as r,
  k as a,
  L as n,
  w as c,
  o as m,
  l as d
} from './index-820a519e.js'
import './el-form-item-2e860f96.js'
import './el-col-beabe3f6.js'
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
import './el-divider-9c19755b.js'
import './el-tree-8dac9473.js'
import './index-55f4d4a6.js'
import './el-progress-97dbc0fb.js'
import './style.css_vue_type_style_index_0_src_true_lang-4a035adc.js'
import './dict-c8c7fcf4.js'
const u = i({
  __name: 'Bind',
  props: { currentRow: { type: Object, default: () => null } },
  setup(i, { expose: u }) {
    const j = i,
      { required: y, isTelephone: _, isEmail: f } = t(),
      v = p([]),
      b = p([]),
      w = p([]),
      g = p([])
    r(async () => {
      await (async () => {
        const e = l(),
          o = await e.getDictObj(['connect_type', 'connect_port', 'connect_protocol'])
        ;((v.value = o.connect_type), (b.value = o.connect_port), (w.value = o.connect_protocol))
      })()
    })
    const h = n([
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
            multiple: !1,
            clearable: !0,
            remote: !0,
            filterable: !0,
            options: g,
            remoteMethod: async (e) => {
              const o = { keywords: e, page: 1, limit: 20, device_type: '4g_io' },
                t = (await s(o)).data.map((e) => ({ label: `${e.ip} ${e.mac}`, value: e.id }))
              return ((g.value = t), t)
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
          field: 'connect_type',
          label: '连接类型',
          colProps: { span: 12 },
          component: 'Select',
          componentProps: { style: { width: '100%' }, multiple: !1, options: v },
          value: []
        },
        {
          field: 'connect_protocol',
          label: '连接协议',
          colProps: { span: 12 },
          component: 'Select',
          componentProps: { style: { width: '100%' }, multiple: !1, options: w },
          value: []
        }
      ]),
      P = n({ name: [y()], sn: [y()] }),
      { formRegister: x, formMethods: R } = e(),
      { setValues: k, getFormData: E, getElFormExpose: F } = R
    return (
      c(
        () => j.currentRow,
        (e) => {
          e && k(e)
        },
        { deep: !0, immediate: !0 }
      ),
      u({
        submit: async () => {
          const e = await F()
          if (await (null == e ? void 0 : e.validate())) {
            return await E()
          }
        }
      }),
      (e, t) => (
        m(),
        d(a(o), { rules: P, onRegister: a(x), schema: h }, null, 8, [
          'rules',
          'onRegister',
          'schema'
        ])
      )
    )
  }
})
export { u as default }
