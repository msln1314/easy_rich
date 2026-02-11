import {
  e as a,
  B as o,
  r as e,
  o as s,
  l,
  s as c,
  k as n,
  H as t,
  J as r,
  cO as i,
  cP as m,
  cQ as d,
  cR as u,
  cS as p,
  ad as g,
  cz as _,
  f,
  b1 as v,
  m as h,
  x as j,
  j as w,
  a5 as L,
  a1 as C,
  M as b,
  z as I
} from './index-820a519e.js'
import { E as k } from './el-switch-6f4f5b6a.js'
import { u as E } from './useIcon-24caadfc.js'
import { E as x, a as z, b as D } from './el-dropdown-item-a41cbdee.js'
import './el-popper-797844d6.js'
const P = 'var(--el-color-black)',
  V = r(
    a({
      __name: 'ThemeSwitch',
      setup(a) {
        const { getPrefixCls: r } = t(),
          i = r('theme-switch'),
          m = E({ icon: 'emojione-monotone:sun', color: '#fde047' }),
          d = E({ icon: 'emojione-monotone:crescent-moon', color: '#fde047' }),
          u = o(),
          p = e(u.getIsDark),
          g = (a) => {
            u.setIsDark(a)
          }
        return (a, o) => (
          s(),
          l(
            n(k),
            {
              class: c(n(i)),
              modelValue: p.value,
              'onUpdate:modelValue': o[0] || (o[0] = (a) => (p.value = a)),
              'inline-prompt': '',
              'border-color': P,
              'inactive-color': P,
              'active-color': P,
              'active-icon': n(m),
              'inactive-icon': n(d),
              onChange: g
            },
            null,
            8,
            ['class', 'modelValue', 'active-icon', 'inactive-icon']
          )
        )
      }
    }),
    [['__scopeId', 'data-v-52ce9834']]
  ),
  O = () => ({
    changeLocale: async (a) => {
      const o = i.global,
        e = await m(
          Object.assign({
            '../../locales/en.ts': () => d(() => import('./en-2cd58d43.js'), []),
            '../../locales/zh-CN.ts': () => d(() => import('./zh-CN-47b74965.js'), [])
          }),
          `../../locales/${a}.ts`
        )
      ;(o.setLocaleMessage(a, e.default),
        ((a) => {
          const o = u()
          ;('legacy' === i.mode ? (i.global.locale = a) : (i.global.locale.value = a),
            o.setCurrentLocale({ lang: a }),
            p(a))
        })(a))
    }
  }),
  T = a({
    __name: 'LocaleDropdown',
    props: { color: g.string.def('') },
    setup(a) {
      const { getPrefixCls: o } = t(),
        e = o('locale-dropdown'),
        r = _(),
        i = f(() => r.getLocaleMap),
        m = f(() => r.getCurrentLocale),
        d = (a) => {
          if (a === n(m).lang) return
          ;(window.location.reload(), r.setCurrentLocale({ lang: a }))
          const { changeLocale: o } = O()
          o(a)
        }
      return (o, t) => {
        const r = v('Icon')
        return (
          s(),
          l(
            n(z),
            { class: c(n(e)), trigger: 'click', onCommand: d },
            {
              dropdown: h(() => [
                j(n(x), null, {
                  default: h(() => [
                    (s(!0),
                    w(
                      C,
                      null,
                      L(
                        i.value,
                        (a) => (
                          s(),
                          l(
                            n(D),
                            { key: a.lang, command: a.lang },
                            { default: h(() => [b(I(a.name), 1)]), _: 2 },
                            1032,
                            ['command']
                          )
                        )
                      ),
                      128
                    ))
                  ]),
                  _: 1
                })
              ]),
              default: h(() => [
                j(
                  r,
                  {
                    size: 18,
                    icon: 'ion:language-sharp',
                    class: c(['cursor-pointer !p-0', o.$attrs.class]),
                    color: a.color
                  },
                  null,
                  8,
                  ['class', 'color']
                )
              ]),
              _: 1
            },
            8,
            ['class']
          )
        )
      }
    }
  })
export { V as T, T as _ }
