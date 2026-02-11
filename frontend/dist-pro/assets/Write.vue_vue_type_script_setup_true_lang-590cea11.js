import { u as e, F as t } from './useForm-c59a8d29.js'
import { u as o } from './useValidator-db15330d.js'
import { g as a } from './client_group-aeb78440.js'
import { u as l } from './dict-451afacd.js'
import {
  e as s,
  r as n,
  a2 as p,
  k as i,
  L as r,
  w as c,
  o as d,
  l as m
} from './index-820a519e.js'
const u = s({
  __name: 'Write',
  props: {
    currentRow: { type: Object, default: () => null },
    actionType: { type: String, default: () => 'add' }
  },
  setup(s, { expose: u }) {
    const y = s,
      { required: f, isTelephone: P, isEmail: w } = o(),
      b = (n([]), n([])),
      v = n([]),
      _ = n([]),
      g = n([])
    p(async () => {
      await (async () => {
        const e = l(),
          t = await e.getDictObj(['active_status', 'client_tag', 'client_type', 'area_list'])
        ;((v.value = t.active_status),
          (b.value = t.client_tag),
          (_.value = t.client_type),
          (g.value = t.area_list))
      })()
    })
    const h = r([
        {
          field: 'name',
          label: '名称',
          colProps: { span: 24 },
          component: 'Input',
          componentProps: {
            style: { width: '100%' },
            readonly: 'add' != y.actionType,
            disabled: 'add' != y.actionType
          }
        },
        {
          field: 'sn',
          label: '桩号',
          colProps: { span: 24 },
          component: 'Input',
          componentProps: {
            style: { width: '100%' },
            readonly: 'add' != y.actionType,
            disabled: 'add' != y.actionType
          }
        },
        {
          field: 'area',
          label: '区域',
          colProps: { span: 12 },
          component: 'Select',
          componentProps: { style: { width: '100%' }, multiple: !1, options: g },
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
          field: 'group_id',
          label: '分组',
          colProps: { span: 12 },
          component: 'TreeSelect',
          componentProps: { style: { width: '100%' }, checkStrictly: !0, defaultExpandAll: !0 },
          optionApi: async () => (await a()).data
        },
        {
          field: 'client_type',
          label: '充电桩类型',
          colProps: { span: 12 },
          component: 'Select',
          componentProps: { style: { width: '100%' }, multiple: !1, options: _ },
          value: []
        },
        {
          field: 'client_tag',
          label: '标签',
          colProps: { span: 12 },
          component: 'Select',
          componentProps: { style: { width: '100%' }, multiple: !1, options: b },
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
      j = r({ name: [f()], sn: [f()], area: [f()] }),
      { formRegister: T, formMethods: R } = e(),
      { setValues: S, getFormData: x, getElFormExpose: E } = R
    return (
      c(
        () => y.currentRow,
        (e) => {
          e && S(e)
        },
        { deep: !0, immediate: !0 }
      ),
      u({
        submit: async () => {
          const e = await E()
          if (await (null == e ? void 0 : e.validate())) {
            return await x()
          }
        }
      }),
      (e, o) => (
        d(),
        m(i(t), { rules: j, onRegister: i(T), schema: h }, null, 8, [
          'rules',
          'onRegister',
          'schema'
        ])
      )
    )
  }
})
export { u as _ }
