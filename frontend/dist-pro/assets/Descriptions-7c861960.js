import {
  e,
  ad as l,
  f as a,
  k as t,
  r as s,
  x as r,
  al as o,
  a0 as i,
  aH as d,
  a6 as n,
  bu as c,
  B as f,
  H as p,
  J as u
} from './index-820a519e.js'
import { E as m, a as b } from './el-descriptions-item-6ddb822e.js'
import './el-tooltip-4ed993c7.js'
import { E as x } from './el-popper-797844d6.js'
import { E as v } from './index-55f4d4a6.js'
const g = f(),
  h = a(() => g.getMobile),
  { getPrefixCls: j } = p(),
  k = j('descriptions'),
  y = u(
    e({
      name: 'Descriptions',
      props: {
        title: l.string.def(''),
        message: l.string.def(''),
        collapse: l.bool.def(!0),
        border: l.bool.def(!0),
        column: l.number.def(2),
        size: l.oneOf(['large', 'default', 'small']).def('default'),
        direction: l.oneOf(['horizontal', 'vertical']).def('horizontal'),
        extra: l.string.def(''),
        schema: { type: Array, default: () => [] },
        data: { type: Object, default: () => ({}) }
      },
      setup(e, { slots: l, attrs: f }) {
        const p = a(() => {
            const l = ['title', 'message', 'collapse', 'schema', 'data', 'class'],
              a = { ...f, ...e }
            for (const e in a) -1 !== l.indexOf(e) && delete a[e]
            return (t(h) && (a.direction = 'vertical'), a)
          }),
          u = s(!0),
          g = () => {
            e.collapse && (u.value = !t(u))
          }
        return () =>
          r(
            'div',
            {
              class: [
                k,
                'bg-[var(--el-color-white)] dark:bg-[var(--el-bg-color)] dark:border-[var(--el-border-color)] dark:border-1px'
              ]
            },
            [
              e.title
                ? r(
                    'div',
                    {
                      class: [
                        `${k}-header`,
                        'relative h-50px flex justify-between items-center layout-border__bottom px-10px cursor-pointer'
                      ],
                      onClick: g
                    },
                    [
                      r(
                        'div',
                        { class: [`${k}-header__title`, 'relative font-18px font-bold ml-10px'] },
                        [
                          r('div', { class: 'flex items-center' }, [
                            e.title,
                            e.message
                              ? r(
                                  x,
                                  { content: e.message, placement: 'right' },
                                  {
                                    default: () => [
                                      r(
                                        o,
                                        {
                                          icon: 'bi:question-circle-fill',
                                          class: 'ml-5px',
                                          size: 14
                                        },
                                        null
                                      )
                                    ]
                                  }
                                )
                              : null
                          ])
                        ]
                      ),
                      e.collapse
                        ? r(o, { icon: u.value ? 'ep:arrow-down' : 'ep:arrow-up' }, null)
                        : null
                    ]
                  )
                : null,
              r(v, null, {
                default: () => [
                  i(
                    r('div', { class: [`${k}-content`, 'p-20px'] }, [
                      r(m, t(p), {
                        extra: () => (l.extra ? l.extra() : e.extra),
                        default: () =>
                          e.schema.map((l) =>
                            r(
                              b,
                              n(
                                { key: l.field },
                                ((e) => {
                                  const l = ['field'],
                                    a = { ...e }
                                  for (const t in a) -1 !== l.indexOf(t) && delete a[t]
                                  return a
                                })(l)
                              ),
                              {
                                label: () => {
                                  var e, a
                                  return (null == (e = l.slots) ? void 0 : e.label)
                                    ? null == (a = l.slots)
                                      ? void 0
                                      : a.label(l)
                                    : l.label
                                },
                                default: () => {
                                  var a, t
                                  return (null == (a = l.slots) ? void 0 : a.default)
                                    ? null == (t = l.slots)
                                      ? void 0
                                      : t.default(e.data)
                                    : c(e.data, l.field)
                                }
                              }
                            )
                          )
                      })
                    ]),
                    [[d, t(u)]]
                  )
                ]
              })
            ]
          )
      }
    }),
    [['__scopeId', 'data-v-cca2de29']]
  )
export { y as D }
