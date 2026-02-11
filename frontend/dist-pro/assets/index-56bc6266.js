import {
  b as s,
  c as e,
  e as a,
  b9 as l,
  u as o,
  f as n,
  o as t,
  j as c,
  y as i,
  q as r,
  s as u,
  k as p,
  l as f,
  m as d,
  x as k,
  az as m,
  aY as g,
  E as y,
  F as b,
  n as v,
  D as C,
  _ as h,
  t as _
} from './index-820a519e.js'
const E = s({
    type: { type: String, values: ['success', 'info', 'warning', 'danger', ''], default: '' },
    closable: Boolean,
    disableTransitions: Boolean,
    hit: Boolean,
    color: { type: String, default: '' },
    size: { type: String, values: e, default: '' },
    effect: { type: String, values: ['dark', 'light', 'plain'], default: 'light' },
    round: Boolean
  }),
  B = { close: (s) => s instanceof MouseEvent, click: (s) => s instanceof MouseEvent },
  S = a({ name: 'ElTag' })
const x = _(
  h(
    a({
      ...S,
      props: E,
      emits: B,
      setup(s, { emit: e }) {
        const a = s,
          h = l(),
          _ = o('tag'),
          E = n(() => {
            const { type: s, hit: e, effect: l, closable: o, round: n } = a
            return [
              _.b(),
              _.is('closable', o),
              _.m(s),
              _.m(h.value),
              _.m(l),
              _.is('hit', e),
              _.is('round', n)
            ]
          }),
          B = (s) => {
            e('close', s)
          },
          S = (s) => {
            e('click', s)
          }
        return (s, e) =>
          s.disableTransitions
            ? (t(),
              c(
                'span',
                { key: 0, class: u(p(E)), style: v({ backgroundColor: s.color }), onClick: S },
                [
                  i('span', { class: u(p(_).e('content')) }, [r(s.$slots, 'default')], 2),
                  s.closable
                    ? (t(),
                      f(
                        p(y),
                        { key: 0, class: u(p(_).e('close')), onClick: g(B, ['stop']) },
                        { default: d(() => [k(p(m))]), _: 1 },
                        8,
                        ['class', 'onClick']
                      ))
                    : b('v-if', !0)
                ],
                6
              ))
            : (t(),
              f(
                C,
                { key: 1, name: `${p(_).namespace.value}-zoom-in-center`, appear: '' },
                {
                  default: d(() => [
                    i(
                      'span',
                      { class: u(p(E)), style: v({ backgroundColor: s.color }), onClick: S },
                      [
                        i('span', { class: u(p(_).e('content')) }, [r(s.$slots, 'default')], 2),
                        s.closable
                          ? (t(),
                            f(
                              p(y),
                              { key: 0, class: u(p(_).e('close')), onClick: g(B, ['stop']) },
                              { default: d(() => [k(p(m))]), _: 1 },
                              8,
                              ['class', 'onClick']
                            ))
                          : b('v-if', !0)
                      ],
                      6
                    )
                  ]),
                  _: 3
                },
                8,
                ['name']
              ))
      }
    }),
    [['__file', '/home/runner/work/element-plus/element-plus/packages/components/tag/src/tag.vue']]
  )
)
export { x as E, E as t }
