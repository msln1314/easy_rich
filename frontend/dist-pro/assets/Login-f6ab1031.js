import {
  e as t,
  B as e,
  r as s,
  f as a,
  o as l,
  j as i,
  x as o,
  m as r,
  y as p,
  s as m,
  k as x,
  z as n,
  C as c,
  T as d,
  D as u,
  l as j,
  F as _,
  G as g,
  H as v,
  I as f,
  J as h
} from './index-820a519e.js'
import { _ as w } from './LoginForm.vue_vue_type_script_setup_true_lang-3e89154f.js'
import './useForm-c59a8d29.js'
import './el-input-5ae17c8f.js'
import './el-divider-9c19755b.js'
import './useValidator-db15330d.js'
import { T as y, _ as b } from './LocaleDropdown.vue_vue_type_script_setup_true_lang-290dde7d.js'
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
import './useIcon-24caadfc.js'
import './el-dropdown-item-a41cbdee.js'
import './dropdown-394a0a1a.js'
import './refs-374e9e51.js'
const k = { class: 'relative flex mx-auto min-h-100vh' },
  I = { class: 'flex items-center relative text-white' },
  T = ['src'],
  L = { class: 'text-20px font-bold' },
  F = { class: 'flex justify-center items-center h-[calc(100%-60px)]' },
  C = { class: 'text-3xl text-white', key: '2' },
  B = { class: 'mt-5 font-normal text-white text-14px', key: '3' },
  D = { class: 'p-30px bg-opacity-20 lt-sm:p-10px dark:bg-[var(--login-bg-color)] relative' },
  E = {
    class: 'flex justify-between items-center text-white at-2xl:justify-end at-xl:justify-end'
  },
  G = { class: 'flex items-center at-2xl:hidden at-xl:hidden' },
  H = ['src'],
  J = { class: 'text-20px font-bold' },
  N = { class: 'flex justify-end items-center space-x-10px' },
  P = {
    class:
      'h-full flex items-center m-auto w-[100%] at-2xl:max-w-500px at-xl:max-w-500px at-md:max-w-500px at-lg:max-w-500px'
  },
  R = h(
    t({
      __name: 'Login',
      setup(t) {
        const { getPrefixCls: h } = v(),
          R = h('login'),
          V = e(),
          { t: $ } = f(),
          q = s(!0),
          z = a(() => V.getLogoImage),
          K = () => {
            q.value = !1
          }
        return (t, e) => (
          l(),
          i(
            'div',
            {
              class: m([
                x(R),
                'h-[100%] relative lt-xl:bg-[var(--login-bg-color)] lt-sm:px-10px lt-xl:px-10px lt-md:px-10px'
              ])
            },
            [
              o(
                x(g),
                { class: 'h-full' },
                {
                  default: r(() => [
                    p('div', k, [
                      p(
                        'div',
                        {
                          class: m(
                            `${x(R)}__left flex-1 bg-gray-500 bg-opacity-20 relative p-30px lt-xl:hidden`
                          )
                        },
                        [
                          p('div', I, [
                            p(
                              'img',
                              { src: z.value, alt: '', class: 'w-48px h-48px mr-10px' },
                              null,
                              8,
                              T
                            ),
                            p('span', L, n(x(c)(x(V).getTitle)), 1)
                          ]),
                          p('div', F, [
                            o(
                              d,
                              {
                                appear: '',
                                tag: 'div',
                                'enter-active-class': 'animate__animated animate__bounceInLeft'
                              },
                              {
                                default: r(() => [
                                  p('div', C, n(x($)('login.welcome')), 1),
                                  p('div', B, n(x($)('login.message')), 1)
                                ]),
                                _: 1
                              }
                            )
                          ])
                        ],
                        2
                      ),
                      p('div', D, [
                        p('div', E, [
                          p('div', G, [
                            p(
                              'img',
                              { src: z.value, alt: '', class: 'w-48px h-48px mr-10px' },
                              null,
                              8,
                              H
                            ),
                            p('span', J, n(x(c)(x(V).getTitle)), 1)
                          ]),
                          p('div', N, [
                            o(x(y)),
                            o(x(b), { class: 'lt-xl:text-white dark:text-white' })
                          ])
                        ]),
                        o(
                          u,
                          {
                            appear: '',
                            'enter-active-class': 'animate__animated animate__bounceInRight'
                          },
                          {
                            default: r(() => [
                              p('div', P, [
                                q.value
                                  ? (l(),
                                    j(x(w), {
                                      key: 0,
                                      class:
                                        'p-20px h-auto m-auto lt-xl:rounded-3xl lt-xl:light:bg-white',
                                      onToTelephone: K
                                    }))
                                  : _('', !0)
                              ])
                            ]),
                            _: 1
                          }
                        )
                      ])
                    ])
                  ]),
                  _: 1
                }
              )
            ],
            2
          )
        )
      }
    }),
    [['__scopeId', 'data-v-47e86f55']]
  )
export { R as default }
