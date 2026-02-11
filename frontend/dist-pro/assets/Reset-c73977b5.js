import { u as s, F as e } from './useForm-c59a8d29.js'
import { u as t } from './useValidator-db15330d.js'
import {
  e as o,
  A as r,
  v as a,
  B as i,
  K as l,
  f as p,
  L as d,
  r as m,
  w as n,
  o as c,
  j as u,
  y as j,
  x as v,
  k as g,
  m as _,
  M as f,
  N as w,
  l as h,
  F as x,
  O as y,
  P as R,
  Q as b,
  R as k,
  S as F,
  J as P
} from './index-820a519e.js'
import { _ as E } from './Footer.vue_vue_type_script_setup_true_lang-120f04e3.js'
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
const I = { class: 'main-container' },
  q = { class: 'form-container' },
  A = ((s) => (b('data-v-ad559cf1'), (s = s()), k(), s))(() =>
    j(
      'div',
      null,
      [
        j(
          'h2',
          { class: 'text-2xl font-bold text-center w-[100%]' },
          '第一次登录系统，需先重置密码'
        )
      ],
      -1
    )
  ),
  M = { class: 'w-[100%]' },
  N = { class: 'footer-container' },
  S = P(
    o({
      __name: 'Reset',
      setup(o) {
        const { required: b } = t(),
          { setStorage: k } = F(),
          { addRoute: P, push: S, currentRoute: V } = r(),
          B = a(),
          C = i(),
          J = l(),
          K = p(() => C.getFooter),
          L = d([
            {
              field: 'password',
              label: '新密码',
              component: 'InputPassword',
              colProps: { span: 24 },
              componentProps: { style: { width: '100%' }, placeholder: '请输入新密码' }
            },
            {
              field: 'password_two',
              label: '再次输入新密码',
              component: 'InputPassword',
              colProps: { span: 24 },
              componentProps: { style: { width: '100%' }, placeholder: '请再次输入新密码' }
            }
          ]),
          O = {
            password: [
              b(),
              { min: 8, max: 16, message: '长度需为8-16个字符,请重新输入。', trigger: 'blur' }
            ],
            password_two: [
              b(),
              { min: 8, max: 16, message: '长度需为8-16个字符,请重新输入。', trigger: 'blur' }
            ]
          },
          { formRegister: Q, formMethods: U } = s(),
          { setValues: D, getFormData: G, getElFormExpose: H } = U
        D(B.getUser)
        const T = m(!1),
          W = m('')
        n(
          () => V.value,
          (s) => {
            var e
            W.value = null == (e = null == s ? void 0 : s.query) ? void 0 : e.redirect
          },
          { immediate: !0 }
        )
        const X = async () => {
            const s = await H()
            if (await (null == s ? void 0 : s.validate())) {
              T.value = !0
              const s = await G()
              try {
                ;(await y(s)) ? Y() : (T.value = !1)
              } catch (e) {
                T.value = !1
              }
            }
          },
          Y = async () => {
            const s = await R()
            if (s) {
              const e = s.data || []
              ;(k('roleRouters', e),
                await J.generateRoutes(e).catch(() => {}),
                J.getAddRouters.forEach((s) => {
                  P(s)
                }),
                J.setIsAddRouters(!0),
                S({ path: W.value || J.addRouters[0].path }))
            }
          }
        return (s, t) => (
          c(),
          u('div', I, [
            j('div', q, [
              A,
              v(
                g(e),
                {
                  onRegister: g(Q),
                  schema: L,
                  rules: O,
                  'hide-required-asterisk': '',
                  class: 'dark:border-1 dark:border-[var(--el-border-color)] dark:border-solid'
                },
                null,
                8,
                ['onRegister', 'schema']
              ),
              j('div', M, [
                v(
                  g(w),
                  { loading: T.value, type: 'primary', class: 'w-[100%]', onClick: X },
                  { default: _(() => [f(' 重置密码 ')]), _: 1 },
                  8,
                  ['loading']
                )
              ])
            ]),
            j('div', N, [K.value ? (c(), h(g(E), { key: 0 })) : x('', !0)])
          ])
        )
      }
    }),
    [['__scopeId', 'data-v-ad559cf1']]
  )
export { S as default }
