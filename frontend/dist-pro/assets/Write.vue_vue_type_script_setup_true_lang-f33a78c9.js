import { u as e, F as o } from './useForm-c59a8d29.js'
import { u as l } from './useValidator-db15330d.js'
import { e as a } from './dict-c8c7fcf4.js'
import { e as t, ad as s, L as r, w as p, o as n, l as i, k as u } from './index-820a519e.js'
const m = t({
  __name: 'Write',
  props: { currentRow: { type: Object, default: () => null }, dictTypeId: s.number.def(void 0) },
  setup(t, { expose: s }) {
    const m = t,
      { required: c } = l(),
      d = r([
        {
          field: 'dict_type_id',
          label: '字典类型',
          colProps: { span: 24 },
          component: 'Select',
          componentProps: { clearable: !1, style: { width: '100%' } },
          optionApi: async () => (await a()).data,
          formItemProps: { rules: [c()] },
          value: m.dictTypeId
        },
        {
          field: 'label',
          label: '字典标签',
          colProps: { span: 24 },
          component: 'Input',
          formItemProps: { rules: [c()] }
        },
        {
          field: 'value',
          label: '字典键值',
          colProps: { span: 24 },
          component: 'Input',
          formItemProps: { rules: [c()] }
        },
        {
          field: 'color_type',
          label: '颜色类型',
          colProps: { span: 12 },
          component: 'Select',
          componentProps: {
            style: { width: '100%' },
            multiple: !1,
            options: [
              { value: 'default', label: '默认' },
              { value: 'primary', label: '主要' },
              { value: 'success', label: '成功' },
              { value: 'info', label: '信息' },
              { value: 'warning', label: '警告' },
              { value: 'danger', label: '危险' }
            ]
          },
          value: []
        },
        {
          field: 'order',
          label: '排序',
          colProps: { span: 24 },
          component: 'InputNumber',
          componentProps: { style: { width: '50%' } },
          formItemProps: { rules: [c()] }
        },
        {
          field: 'is_default',
          label: '是否默认',
          colProps: { span: 24 },
          component: 'RadioGroup',
          componentProps: {
            style: { width: '100%' },
            options: [
              { label: '是', value: !0 },
              { label: '否', value: !1 }
            ]
          },
          value: !1,
          formItemProps: { rules: [c()] }
        },
        {
          field: 'status',
          label: '是否启用用',
          colProps: { span: 24 },
          component: 'RadioGroup',
          componentProps: {
            style: { width: '100%' },
            options: [
              { label: '启用', value: !0 },
              { label: '禁用', value: !1 }
            ]
          },
          value: !0,
          formItemProps: { rules: [c()] }
        },
        { field: 'remark', label: '备注', colProps: { span: 24 }, component: 'Input' }
      ]),
      { formRegister: f, formMethods: b } = e(),
      { setValues: P, getFormData: v, getElFormExpose: w } = b
    return (
      p(
        () => m.currentRow,
        (e) => {
          e && P(e)
        },
        { deep: !0, immediate: !0 }
      ),
      s({
        submit: async () => {
          const e = await w()
          if (await (null == e ? void 0 : e.validate())) {
            return await v()
          }
        }
      }),
      (e, l) => (n(), i(u(o), { onRegister: u(f), schema: d }, null, 8, ['onRegister', 'schema']))
    )
  }
})
export { m as _ }
