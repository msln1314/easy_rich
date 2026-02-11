import { u as e, F as o } from './useForm-c59a8d29.js'
import {
  e as a,
  K as s,
  v as t,
  A as l,
  r,
  L as n,
  x as i,
  N as d,
  a1 as p,
  w as c,
  af as u,
  P as m,
  o as h,
  l as g,
  k as f,
  ag as v,
  S as w,
  I as b
} from './index-820a519e.js'
import { u as P } from './useValidator-db15330d.js'
const y = a({
  __name: 'LoginForm',
  emits: ['to-telephone'],
  setup(a, { emit: y }) {
    const { required: R } = P(),
      x = s(),
      I = t(),
      { currentRoute: j, addRoute: k, push: F } = l(),
      { setStorage: _ } = w(),
      { t: E } = b()
    r(!1)
    const q = { telephone: [R()], method: [R()], password: [R()] },
      A = n([
        {
          field: 'title',
          colProps: { span: 24 },
          formItemProps: {
            slots: {
              default: () =>
                i('h2', { class: 'text-2xl font-bold text-center w-[100%]' }, [E('login.login')])
            }
          }
        },
        {
          field: 'phone',
          label: E('login.telephone'),
          value: '',
          component: 'Input',
          colProps: { span: 24 },
          componentProps: {
            style: { width: '100%' },
            placeholder: E('login.telephonePlaceholder'),
            maxlength: 11
          }
        },
        {
          field: 'password',
          label: E('login.password'),
          value: '',
          component: 'InputPassword',
          colProps: { span: 24 },
          componentProps: { style: { width: '100%' }, placeholder: E('login.passwordPlaceholder') }
        },
        { field: 'method', label: '登录类型', value: '0', component: 'Input', hidden: !0 },
        {
          field: 'login',
          colProps: { span: 24 },
          formItemProps: {
            slots: {
              default: () => {
                let e
                return i(p, null, [
                  i('div', { class: 'w-[100%]' }, [
                    i(
                      d,
                      { loading: C.value, type: 'primary', class: 'w-[100%]', onClick: K },
                      ((o = e = E('login.login')),
                      'function' == typeof o ||
                      ('[object Object]' === Object.prototype.toString.call(o) && !v(o))
                        ? e
                        : { default: () => [e] })
                    )
                  ])
                ])
                var o
              }
            }
          }
        }
      ]),
      { formRegister: S, formMethods: L } = e(),
      { getFormData: O, getElFormExpose: z } = L,
      C = r(!1),
      D = r('')
    c(
      () => j.value,
      (e) => {
        var o
        D.value = null == (o = null == e ? void 0 : e.query) ? void 0 : o.redirect
      },
      { immediate: !0 }
    )
    const K = async () => {
        const e = await z()
        if (await (null == e ? void 0 : e.validate())) {
          C.value = !0
          const e = await O()
          try {
            const o = await I.login(e)
            ;(u.success({ message: '正在加载系统中...' }),
              o
                ? o.data.is_reset_password
                  ? M()
                  : F({ path: '/reset/password' })
                : (C.value = !1))
          } catch (o) {
            C.value = !1
          }
        }
      },
      M = async () => {
        const e = await m()
        if (e) {
          const o = e.data || []
          ;(_('roleRouters', o),
            await x.generateRoutes(o).catch(() => {}),
            x.getAddRouters.forEach((e) => {
              k(e)
            }),
            x.setIsAddRouters(!0),
            F({ path: D.value || x.addRouters[0].path }))
        }
      }
    return (e, a) => (
      h(),
      g(
        f(o),
        {
          schema: A,
          rules: q,
          'label-position': 'top',
          'hide-required-asterisk': '',
          size: 'large',
          class: 'dark:border-1 dark:border-[var(--el-border-color)] dark:border-solid',
          onRegister: f(S)
        },
        null,
        8,
        ['schema', 'onRegister']
      )
    )
  }
})
export { y as _ }
