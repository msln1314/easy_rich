import { u as s, F as e } from './useForm-c59a8d29.js'
import {
  e as a,
  ad as t,
  L as o,
  x as n,
  N as l,
  M as p,
  a1 as r,
  r as c,
  af as i,
  dI as m,
  o as d,
  l as _,
  k as u,
  ac as f
} from './index-820a519e.js'
import { u as y } from './useValidator-db15330d.js'
const P = a({
  __name: 'SMS',
  props: { tabId: t.number },
  setup(a) {
    const t = a,
      { required: P } = y(),
      w = o([
        {
          field: 'sms_access_key',
          label: 'AccessKey',
          colProps: { span: 24 },
          component: 'Input',
          componentProps: { style: { width: '500px' } }
        },
        {
          field: 'sms_access_key_secret',
          label: 'AccessKeySecret',
          colProps: { span: 24 },
          component: 'Input',
          componentProps: { style: { width: '500px' } }
        },
        {
          field: 'sms_sign_name_1',
          label: '短信验证码签名',
          colProps: { span: 24 },
          component: 'Input',
          componentProps: { style: { width: '500px' } }
        },
        {
          field: 'sms_template_code_1',
          label: '短信验证码模板',
          colProps: { span: 24 },
          component: 'Input',
          componentProps: { style: { width: '500px' } }
        },
        {
          field: 'sms_sign_name_2',
          label: '重置密码签名',
          colProps: { span: 24 },
          component: 'Input',
          componentProps: { style: { width: '500px' } }
        },
        {
          field: 'sms_template_code_2',
          label: '重置密码模板',
          colProps: { span: 24 },
          component: 'Input',
          componentProps: { style: { width: '500px' } }
        },
        {
          field: 'sms_send_interval',
          label: '发送频率',
          colProps: { span: 24 },
          component: 'Input',
          componentProps: { style: { width: '500px' } }
        },
        {
          field: 'sms_valid_time',
          label: '有效时间',
          colProps: { span: 24 },
          component: 'Input',
          componentProps: { style: { width: '500px' } }
        },
        {
          field: 'active',
          label: '',
          colProps: { span: 24 },
          formItemProps: {
            slots: {
              default: () =>
                n(r, null, [
                  n(
                    l,
                    { loading: j.value, type: 'primary', onClick: E },
                    { default: () => [p('立即提交')] }
                  )
                ])
            }
          }
        }
      ]),
      b = o({
        sms_access_key: [P()],
        sms_access_key_secret: [P()],
        sms_send_interval: [P()],
        sms_valid_time: [P()]
      }),
      { formRegister: v, formMethods: x } = s(),
      { setValues: I, getFormData: h, getElFormExpose: g } = x
    let k = c({})
    const F = async () => {
        const s = await f({ tab_id: t.tabId })
        if (s) {
          ;(await I(s.data), (k.value = s.data))
          const e = await g()
          null == e || e.clearValidate()
        }
      },
      j = c(!1),
      E = async () => {
        const s = await g()
        if (await (null == s ? void 0 : s.validate())) {
          const s = await h()
          if (((j.value = !0), !s)) return ((j.value = !1), i.error('未获取到数据'))
          try {
            if (await m(s)) return (F(), i.success('更新成功'))
          } finally {
            j.value = !1
          }
        }
      }
    return (
      F(),
      (s, a) => (
        d(),
        _(u(e), { rules: b, onRegister: u(v), schema: w }, null, 8, [
          'rules',
          'onRegister',
          'schema'
        ])
      )
    )
  }
})
export { P as _ }
