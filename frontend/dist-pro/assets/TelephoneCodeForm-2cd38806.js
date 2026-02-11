import { u as e, F as o } from './useForm-c59a8d29.js'
import {
  e as t,
  I as s,
  A as a,
  K as l,
  v as r,
  L as i,
  x as p,
  a1 as n,
  N as d,
  r as c,
  w as u,
  ah as m,
  af as v,
  P as f,
  o as j,
  l as g,
  k as h,
  ag as w,
  S as y
} from './index-820a519e.js'
import { E as x } from './el-input-5ae17c8f.js'
import { E as b } from './el-divider-9c19755b.js'
import { u as k } from './useValidator-db15330d.js'
import './el-form-item-2e860f96.js'
import './el-col-beabe3f6.js'
import './el-tooltip-4ed993c7.js'
import './el-popper-797844d6.js'
import './isNil-1f22f7b0.js'
import './focus-trap-949626e0.js'
/* empty css               */ import './el-checkbox-77b6829c.js'
import './event-5568c9d8.js'
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
import './el-tree-8dac9473.js'
import './index-55f4d4a6.js'
import './el-progress-97dbc0fb.js'
import './style.css_vue_type_style_index_0_src_true_lang-4a035adc.js'
function _(e) {
  return (
    'function' == typeof e || ('[object Object]' === Object.prototype.toString.call(e) && !w(e))
  )
}
const P = t({
  __name: 'TelephoneCodeForm',
  emits: ['to-password'],
  setup(t, { emit: w }) {
    const { formRegister: P, formMethods: R } = e(),
      { getFormData: I, getElFormExpose: S } = R,
      { t: C } = s(),
      { required: E } = k(),
      { currentRoute: F, addRoute: M, push: q } = a(),
      V = l(),
      A = r(),
      { setStorage: L } = y(),
      N = i([
        {
          field: 'title',
          colProps: { span: 24 },
          formItemProps: {
            slots: {
              default: () =>
                p('h2', { class: 'text-2xl font-bold text-center w-[100%]' }, [C('login.login')])
            }
          }
        },
        {
          field: 'telephone',
          label: C('login.telephone'),
          value: '',
          component: 'Input',
          colProps: { span: 24 },
          componentProps: {
            style: { width: '100%' },
            placeholder: C('login.telephonePlaceholder'),
            maxlength: 11
          }
        },
        {
          field: 'password',
          label: C('login.SMSCode'),
          colProps: { span: 24 },
          formItemProps: {
            slots: {
              default: (e) =>
                p('div', { class: 'w-[100%] flex' }, [
                  p(
                    x,
                    {
                      modelValue: e.password,
                      'onUpdate:modelValue': (o) => (e.password = o),
                      placeholder: C('login.codePlaceholder')
                    },
                    {
                      suffix: () => {
                        let e
                        return p(n, null, [
                          p(b, { direction: 'vertical' }, null),
                          B.value
                            ? p(
                                d,
                                { type: 'primary', link: !0, onClick: G },
                                _((e = C('login.getSMSCode'))) ? e : { default: () => [e] }
                              )
                            : p(
                                d,
                                { type: 'primary', disabled: !B.value, link: !0 },
                                { default: () => [D.value + C('login.SMSCodeRetry')] }
                              )
                        ])
                      }
                    }
                  )
                ])
            }
          }
        },
        { field: 'method', label: '登录类型', value: '1', component: 'Input', hidden: !0 },
        {
          field: 'login',
          colProps: { span: 24 },
          formItemProps: {
            slots: {
              default: () => {
                let e, o
                return p('div', { class: 'w-[100%]' }, [
                  p('div', { class: 'w-[100%]' }, [
                    p(
                      d,
                      { type: 'primary', class: 'w-[100%]', loading: T.value, onClick: z },
                      _((e = C('login.login'))) ? e : { default: () => [e] }
                    )
                  ]),
                  p('div', { class: 'w-[100%] mt-15px' }, [
                    p(
                      d,
                      { class: 'w-[100%]', onClick: K },
                      _((o = C('login.passwordLogin'))) ? o : { default: () => [o] }
                    )
                  ])
                ])
              }
            }
          }
        }
      ]),
      O = { telephone: [E()], method: [E()], password: [E()] },
      K = () => {
        w('to-password')
      },
      T = c(!1),
      U = c('')
    u(
      () => F.value,
      (e) => {
        var o
        U.value = null == (o = null == e ? void 0 : e.query) ? void 0 : o.redirect
      },
      { immediate: !0 }
    )
    const z = async () => {
      const e = await S()
      if (await (null == e ? void 0 : e.validate())) {
        T.value = !0
        const e = await I()
        try {
          const o = await A.login(e)
          o ? (o.data.is_reset_password ? H() : q({ path: '/reset/password' })) : (T.value = !1)
        } catch (o) {
          T.value = !1
        }
      }
    }
    let B = c(!0),
      D = c(60)
    const G = async () => {
        const e = await S()
        if (await (null == e ? void 0 : e.validateField('telephone'))) {
          ;((B.value = !1), (D.value = 60))
          const e = await I()
          try {
            const o = await m({ telephone: e.telephone })
            if (null == o ? void 0 : o.data) {
              let e = setInterval(() => {
                ;(D.value--, D.value < 1 && ((B.value = !0), clearInterval(e)))
              }, 1e3)
            } else (v.error('发送失败，请联系管理员'), (B.value = !0))
          } catch (o) {
            B.value = !0
          }
        }
      },
      H = async () => {
        const e = await f()
        if (e) {
          const o = e.data || []
          ;(L('roleRouters', o),
            await V.generateRoutes(o).catch(() => {}),
            V.getAddRouters.forEach((e) => {
              M(e)
            }),
            V.setIsAddRouters(!0),
            q({ path: U.value || V.addRouters[0].path }))
        }
      }
    return (e, t) => (
      j(),
      g(
        h(o),
        {
          schema: N,
          rules: O,
          'label-position': 'top',
          'hide-required-asterisk': '',
          size: 'large',
          class: 'dark:border-1 dark:border-[var(--el-border-color)] dark:border-solid',
          onRegister: h(P)
        },
        null,
        8,
        ['schema', 'onRegister']
      )
    )
  }
})
export { P as default }
