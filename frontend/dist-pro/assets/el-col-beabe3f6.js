import {
  b as e,
  e as t,
  u as s,
  f as a,
  am as u,
  o as l,
  l as r,
  m as n,
  q as p,
  s as o,
  k as c,
  n as f,
  p as m,
  _ as d,
  t as g,
  d as i,
  an as b,
  ao as y,
  i as $,
  ap as h
} from './index-820a519e.js'
const j = Symbol('rowContextKey'),
  v = e({
    tag: { type: String, default: 'div' },
    gutter: { type: Number, default: 0 },
    justify: {
      type: String,
      values: ['start', 'center', 'end', 'space-around', 'space-between', 'space-evenly'],
      default: 'start'
    },
    align: { type: String, values: ['top', 'middle', 'bottom'] }
  }),
  N = t({ name: 'ElRow' })
const x = g(
    d(
      t({
        ...N,
        props: v,
        setup(e) {
          const t = e,
            d = s('row'),
            g = a(() => t.gutter)
          u(j, { gutter: g })
          const i = a(() => {
              const e = {}
              return t.gutter ? ((e.marginRight = e.marginLeft = `-${t.gutter / 2}px`), e) : e
            }),
            b = a(() => [
              d.b(),
              d.is(`justify-${t.justify}`, 'start' !== t.justify),
              d.is(`align-${t.align}`, !!t.align)
            ])
          return (e, t) => (
            l(),
            r(
              m(e.tag),
              { class: o(c(b)), style: f(c(i)) },
              { default: n(() => [p(e.$slots, 'default')]), _: 3 },
              8,
              ['class', 'style']
            )
          )
        }
      }),
      [
        [
          '__file',
          '/home/runner/work/element-plus/element-plus/packages/components/row/src/row.vue'
        ]
      ]
    )
  ),
  w = e({
    tag: { type: String, default: 'div' },
    span: { type: Number, default: 24 },
    offset: { type: Number, default: 0 },
    pull: { type: Number, default: 0 },
    push: { type: Number, default: 0 },
    xs: { type: i([Number, Object]), default: () => b({}) },
    sm: { type: i([Number, Object]), default: () => b({}) },
    md: { type: i([Number, Object]), default: () => b({}) },
    lg: { type: i([Number, Object]), default: () => b({}) },
    xl: { type: i([Number, Object]), default: () => b({}) }
  }),
  _ = t({ name: 'ElCol' })
const E = g(
  d(
    t({
      ..._,
      props: w,
      setup(e) {
        const t = e,
          { gutter: u } = y(j, { gutter: a(() => 0) }),
          d = s('col'),
          g = a(() => {
            const e = {}
            return (u.value && (e.paddingLeft = e.paddingRight = u.value / 2 + 'px'), e)
          }),
          i = a(() => {
            const e = []
            ;['span', 'offset', 'pull', 'push'].forEach((s) => {
              const a = t[s]
              $(a) && ('span' === s ? e.push(d.b(`${t[s]}`)) : a > 0 && e.push(d.b(`${s}-${t[s]}`)))
            })
            return (
              ['xs', 'sm', 'md', 'lg', 'xl'].forEach((s) => {
                $(t[s])
                  ? e.push(d.b(`${s}-${t[s]}`))
                  : h(t[s]) &&
                    Object.entries(t[s]).forEach(([t, a]) => {
                      e.push('span' !== t ? d.b(`${s}-${t}-${a}`) : d.b(`${s}-${a}`))
                    })
              }),
              u.value && e.push(d.is('guttered')),
              [d.b(), e]
            )
          })
        return (e, t) => (
          l(),
          r(
            m(e.tag),
            { class: o(c(i)), style: f(c(g)) },
            { default: n(() => [p(e.$slots, 'default')]), _: 3 },
            8,
            ['class', 'style']
          )
        )
      }
    }),
    [['__file', '/home/runner/work/element-plus/element-plus/packages/components/col/src/col.vue']]
  )
)
export { E, x as a }
