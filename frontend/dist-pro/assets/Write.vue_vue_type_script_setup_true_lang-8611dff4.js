import { u as e, F as o } from './useForm-c59a8d29.js'
import { u as a } from './useValidator-db15330d.js'
import { e as t, ad as s, L as l, w as r, o as n, l as p, k as i } from './index-820a519e.js'
import { g as u } from './client_group-aeb78440.js'
const d = t({
  __name: 'Write',
  props: { currentRow: { type: Object, default: () => null }, parentId: s.number.def(void 0) },
  setup(t, { expose: s }) {
    const d = t,
      { required: m } = a(),
      c = l([
        {
          field: 'parent_id',
          label: '上级组',
          colProps: { span: 24 },
          component: 'TreeSelect',
          componentProps: {
            style: { width: '100%' },
            checkStrictly: !0,
            placeholder: '请选择上级组',
            nodeKey: 'value',
            defaultExpandAll: !0
          },
          optionApi: async () => (await u()).data,
          value: d.parentId
        },
        { field: 'name', label: '分组名称', component: 'Input', colProps: { span: 12 } },
        { field: 'remak', label: '描述', component: 'Input', colProps: { span: 12 } },
        {
          field: 'order',
          label: '显示排序',
          component: 'InputNumber',
          colProps: { span: 12 },
          componentProps: { style: { width: '100%' } }
        },
        {
          field: 'status',
          label: '是否启用',
          colProps: { span: 12 },
          component: 'RadioGroup',
          componentProps: {
            style: { width: '100%' },
            options: [
              { label: '正常', value: !0 },
              { label: '停用', value: !1 }
            ]
          },
          value: !1
        }
      ]),
      f = l({ name: [m()], status: [m()], order: [m()] }),
      { formRegister: b, formMethods: w } = e(),
      { setValues: h, getFormData: v, getElFormExpose: y } = w
    return (
      r(
        () => d.currentRow,
        (e) => {
          e && h(e)
        },
        { deep: !0, immediate: !0 }
      ),
      s({
        submit: async () => {
          const e = await y()
          if (await (null == e ? void 0 : e.validate())) {
            return await v()
          }
        }
      }),
      (e, a) => (
        n(),
        p(i(o), { rules: f, onRegister: i(b), schema: c, labelWidth: 100 }, null, 8, [
          'rules',
          'onRegister',
          'schema'
        ])
      )
    )
  }
})
export { d as _ }
