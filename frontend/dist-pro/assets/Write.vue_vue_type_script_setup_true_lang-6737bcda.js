import { u as e, F as o } from './useForm-c59a8d29.js'
import { u as a } from './useValidator-db15330d.js'
import { e as s, L as t, w as l, o as r, l as n, k as p } from './index-820a519e.js'
const i = s({
  __name: 'Write',
  props: { currentRow: { type: Object, default: () => null } },
  setup(s, { expose: i }) {
    const m = s,
      { required: u } = a(),
      c = t([
        { field: 'name', label: '角色名称', colProps: { span: 12 }, component: 'Input' },
        { field: 'code', label: '权限字符', colProps: { span: 12 }, component: 'Input' },
        {
          field: 'status',
          label: '角色状态',
          colProps: { span: 12 },
          component: 'RadioGroup',
          componentProps: {
            style: { width: '100%' },
            options: [
              { label: '正常', value: !0 },
              { label: '禁用', value: !1 }
            ]
          },
          value: !1
        },
        {
          field: 'is_admin',
          label: '最高权限',
          colProps: { span: 12 },
          component: 'RadioGroup',
          componentProps: {
            style: { width: '100%' },
            options: [
              { label: '是', value: !0 },
              { label: '否', value: !1 }
            ]
          },
          value: !1
        },
        {
          field: 'order',
          label: '显示排序',
          colProps: { span: 12 },
          component: 'InputNumber',
          componentProps: { style: { width: '100%' } }
        },
        {
          field: 'remark',
          label: '角色描述',
          colProps: { span: 24 },
          component: 'Input',
          componentProps: { rows: 4, type: 'textarea', style: { width: '600px' } }
        }
      ]),
      d = t({ name: [u()], code: [u()], order: [u()] }),
      { formRegister: b, formMethods: f } = e(),
      { setValues: w, getFormData: P, getElFormExpose: v } = f
    return (
      l(
        () => m.currentRow,
        (e) => {
          e && w(e)
        },
        { deep: !0, immediate: !0 }
      ),
      i({
        submit: async () => {
          const e = await v()
          if (await (null == e ? void 0 : e.validate())) {
            return await P()
          }
        }
      }),
      (e, a) => (
        r(),
        n(p(o), { rules: d, onRegister: p(b), schema: c }, null, 8, [
          'rules',
          'onRegister',
          'schema'
        ])
      )
    )
  }
})
export { i as _ }
