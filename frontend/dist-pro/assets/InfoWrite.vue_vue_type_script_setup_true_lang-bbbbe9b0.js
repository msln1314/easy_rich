import { u as e, F as s } from './useForm-c59a8d29.js'
import { u as o } from './useValidator-db15330d.js'
import {
  e as a,
  v as r,
  L as l,
  x as t,
  N as n,
  M as p,
  a1 as i,
  r as m,
  ae as d,
  af as c,
  o as u,
  l as f,
  k as P
} from './index-820a519e.js'
const v = a({
  __name: 'InfoWrite',
  setup(a) {
    const { required: v, isTelephone: b } = o(),
      g = r(),
      h = l([
        {
          field: 'name',
          label: '用户名称',
          component: 'Input',
          colProps: { span: 24 },
          formItemProps: { rules: [v()] },
          componentProps: { style: { width: '50%' } }
        },
        {
          field: 'nickname',
          label: '用户昵称',
          component: 'Input',
          colProps: { span: 24 },
          componentProps: { style: { width: '50%' } }
        },
        {
          field: 'telephone',
          label: '手机号',
          component: 'Input',
          colProps: { span: 24 },
          formItemProps: { rules: [v(), { validator: b, trigger: 'blur' }] },
          componentProps: { style: { width: '50%' }, maxlength: 11 }
        },
        {
          field: 'gender',
          label: '性别',
          colProps: { span: 24 },
          formItemProps: { rules: [v()] },
          component: 'RadioGroup',
          componentProps: {
            options: [
              { label: '男', value: '0' },
              { label: '女', value: '1' }
            ]
          }
        },
        {
          field: 'save',
          colProps: { span: 24 },
          formItemProps: {
            slots: {
              default: () =>
                t(i, null, [
                  t('div', { class: 'w-[50%]' }, [
                    t(
                      n,
                      { loading: F.value, type: 'primary', class: 'w-[100%]', onClick: R },
                      { default: () => [p('保存')] }
                    )
                  ])
                ])
            }
          }
        }
      ]),
      { formRegister: w, formMethods: y } = e(),
      { setValues: I, getFormData: k, getElFormExpose: x } = y
    I(g.getUser)
    const F = m(!1),
      R = async () => {
        const e = await x()
        if (await (null == e ? void 0 : e.validate())) {
          F.value = !0
          const e = await k()
          try {
            const s = await d(e)
            s && (g.updateUser(s.data), c.success('保存成功'))
          } finally {
            F.value = !1
          }
        }
      }
    return (e, o) => (
      u(),
      f(
        P(s),
        {
          onRegister: P(w),
          schema: h,
          'hide-required-asterisk': '',
          class: 'dark:border-1 dark:border-[var(--el-border-color)] dark:border-solid'
        },
        null,
        8,
        ['onRegister', 'schema']
      )
    )
  }
})
export { v as _ }
