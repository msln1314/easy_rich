import {
  e,
  u as t,
  o as a,
  l as o,
  m as l,
  q as s,
  a6 as d,
  cN as n,
  k as i,
  D as p,
  _ as r
} from './index-820a519e.js'
const g = e({ name: 'ElCollapseTransition' })
var m = r(
  e({
    ...g,
    setup(e) {
      const r = t('collapse-transition'),
        g = (e) => {
          ;((e.style.maxHeight = ''),
            (e.style.overflow = e.dataset.oldOverflow),
            (e.style.paddingTop = e.dataset.oldPaddingTop),
            (e.style.paddingBottom = e.dataset.oldPaddingBottom))
        },
        m = {
          beforeEnter(e) {
            ;(e.dataset || (e.dataset = {}),
              (e.dataset.oldPaddingTop = e.style.paddingTop),
              (e.dataset.oldPaddingBottom = e.style.paddingBottom),
              (e.style.maxHeight = 0),
              (e.style.paddingTop = 0),
              (e.style.paddingBottom = 0))
          },
          enter(e) {
            ;((e.dataset.oldOverflow = e.style.overflow),
              0 !== e.scrollHeight
                ? (e.style.maxHeight = `${e.scrollHeight}px`)
                : (e.style.maxHeight = 0),
              (e.style.paddingTop = e.dataset.oldPaddingTop),
              (e.style.paddingBottom = e.dataset.oldPaddingBottom),
              (e.style.overflow = 'hidden'))
          },
          afterEnter(e) {
            ;((e.style.maxHeight = ''), (e.style.overflow = e.dataset.oldOverflow))
          },
          enterCancelled(e) {
            g(e)
          },
          beforeLeave(e) {
            ;(e.dataset || (e.dataset = {}),
              (e.dataset.oldPaddingTop = e.style.paddingTop),
              (e.dataset.oldPaddingBottom = e.style.paddingBottom),
              (e.dataset.oldOverflow = e.style.overflow),
              (e.style.maxHeight = `${e.scrollHeight}px`),
              (e.style.overflow = 'hidden'))
          },
          leave(e) {
            0 !== e.scrollHeight &&
              ((e.style.maxHeight = 0), (e.style.paddingTop = 0), (e.style.paddingBottom = 0))
          },
          afterLeave(e) {
            g(e)
          },
          leaveCancelled(e) {
            g(e)
          }
        }
      return (e, t) => (
        a(),
        o(
          p,
          d({ name: i(r).b() }, n(m)),
          { default: l(() => [s(e.$slots, 'default')]), _: 3 },
          16,
          ['name']
        )
      )
    }
  }),
  [
    [
      '__file',
      '/home/runner/work/element-plus/element-plus/packages/components/collapse-transition/src/collapse-transition.vue'
    ]
  ]
)
m.install = (e) => {
  e.component(m.name, m)
}
const y = m,
  f = y
export { f as E, y as _ }
