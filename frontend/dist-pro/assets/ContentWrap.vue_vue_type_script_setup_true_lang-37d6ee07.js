import {
  e as s,
  ad as e,
  b1 as a,
  o as t,
  l,
  ak as o,
  m as r,
  y as n,
  z as i,
  k as p,
  x as c,
  F as d,
  q as f,
  s as m,
  H as x
} from './index-820a519e.js'
import { E as g } from './el-card-06c161d4.js'
import './el-tooltip-4ed993c7.js'
import { E as u } from './el-popper-797844d6.js'
const v = { class: 'flex items-center' },
  h = { class: 'text-16px font-700' },
  k = { class: 'max-w-200px' },
  _ = { class: 'flex pl-20px flex-grow' },
  j = s({
    __name: 'ContentWrap',
    props: { title: e.string.def(''), message: e.string.def('') },
    setup(s) {
      const { getPrefixCls: e } = x(),
        j = e('content-wrap')
      return (e, x) => {
        const w = a('Icon')
        return (
          t(),
          l(
            p(g),
            { class: m([[p(j)], '!b-0 h-[100%]']), shadow: 'never' },
            o({ default: r(() => [n('div', null, [f(e.$slots, 'default')])]), _: 2 }, [
              s.title
                ? {
                    name: 'header',
                    fn: r(() => [
                      n('div', v, [
                        n('span', h, i(s.title), 1),
                        s.message
                          ? (t(),
                            l(
                              p(u),
                              { key: 0, effect: 'dark', placement: 'right' },
                              {
                                content: r(() => [n('div', k, i(s.message), 1)]),
                                default: r(() => [
                                  c(w, {
                                    class: 'ml-5px',
                                    icon: 'bi:question-circle-fill',
                                    size: 14
                                  })
                                ]),
                                _: 1
                              }
                            ))
                          : d('', !0),
                        n('div', _, [f(e.$slots, 'header')])
                      ])
                    ]),
                    key: '0'
                  }
                : void 0
            ]),
            1032,
            ['class']
          )
        )
      }
    }
  })
export { j as _ }
