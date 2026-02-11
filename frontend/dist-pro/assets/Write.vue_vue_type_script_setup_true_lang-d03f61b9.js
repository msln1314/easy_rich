import { u as e, F as t } from './useForm-c59a8d29.js'
import { u as o } from './useValidator-db15330d.js'
import {
  U as a,
  e as s,
  r as l,
  a2 as p,
  L as n,
  w as i,
  o as c,
  l as r,
  k as m
} from './index-820a519e.js'
import { u as d } from './dict-451afacd.js'
const u = () => a.get({ url: '/iot/products/options' }),
  v = s({
    __name: 'Write',
    props: { currentRow: { type: Object, default: () => null } },
    setup(a, { expose: s }) {
      const v = a,
        { required: P, isTelephone: f, isEmail: y } = o(),
        w = l([]),
        _ = l([]),
        b = l([]),
        h = l([])
      p(async () => {
        await (async () => {
          const e = d(),
            t = await e.getDictObj(['active_status', 'device_tag', 'device_type', 'area_list'])
          ;((_.value = t.active_status),
            (w.value = t.device_tag),
            (b.value = t.device_type),
            (h.value = t.area_list))
        })()
      })
      const g = n([
          {
            field: 'ip',
            label: 'IP地址',
            colProps: { span: 24 },
            component: 'Input',
            componentProps: { style: { width: '100%' } }
          },
          {
            field: 'mac',
            label: 'Mac地址',
            colProps: { span: 24 },
            component: 'Input',
            componentProps: { style: { width: '100%' } }
          },
          {
            field: 'area',
            label: '区域',
            colProps: { span: 12 },
            component: 'Select',
            componentProps: { style: { width: '100%' }, multiple: !1, options: h },
            value: []
          },
          {
            field: 'address',
            label: '地址',
            colProps: { span: 12 },
            component: 'Input',
            componentProps: { style: { width: '100%' } }
          },
          {
            field: 'product_id',
            label: '产品',
            colProps: { span: 12 },
            component: 'Select',
            componentProps: { style: { width: '100%' }, checkStrictly: !0, defaultExpandAll: !0 },
            optionApi: async () => (await u()).data
          },
          {
            field: 'device_type',
            label: '设备类型',
            colProps: { span: 12 },
            component: 'Select',
            componentProps: { style: { width: '100%' }, multiple: !1, options: b },
            value: []
          },
          {
            field: 'device_tag',
            label: '标签',
            colProps: { span: 12 },
            component: 'Select',
            componentProps: { style: { width: '100%' }, multiple: !1, options: w },
            value: []
          },
          {
            field: 'is_active',
            label: '是否可用',
            colProps: { span: 12 },
            component: 'RadioGroup',
            componentProps: {
              options: [
                { label: '可用', value: 1 },
                { label: '不可用', value: 0 }
              ]
            },
            value: []
          },
          {
            field: 'remark',
            label: '备注',
            colProps: { span: 24 },
            component: 'Input',
            componentProps: { style: { width: '100%' } }
          }
        ]),
        j = n({ ip: [P()], mac: [P()], is_active: [P()], device_type: [P()], area: [P()] }),
        { formRegister: R, formMethods: x } = e(),
        { setValues: E, getFormData: I, getElFormExpose: S } = x
      return (
        i(
          () => v.currentRow,
          (e) => {
            e && E(e)
          },
          { deep: !0, immediate: !0 }
        ),
        s({
          submit: async () => {
            const e = await S()
            if (await (null == e ? void 0 : e.validate())) {
              return await I()
            }
          }
        }),
        (e, o) => (
          c(),
          r(m(t), { rules: j, onRegister: m(R), schema: g }, null, 8, [
            'rules',
            'onRegister',
            'schema'
          ])
        )
      )
    }
  })
export { v as _, u as g }
