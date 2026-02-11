import { e, r as t, x as r } from './index-820a519e.js'
/* empty css               */ import { u as a } from './dict-451afacd.js'
import { E as l } from './index-56bc6266.js'
const o = e({
  name: 'DictTag',
  props: {
    type: { type: String, required: !0 },
    value: { type: [String, Number, Boolean], required: !0 }
  },
  setup(e) {
    const o = t(),
      u = async (e, t) => {
        ;(
          await (async (e) => {
            const t = a(),
              r = await t.getDictObj([e])
            return r[e] ? r[e] : []
          })(e)
        ).forEach((e) => {
          e.value == t &&
            ((e.color_type + '' != 'primary' && e.color_type + '' != 'default') ||
              (e.color_type = ''),
            (o.value = e))
        })
      }
    return () => {
      return e.type
        ? void 0 === e.value || null === e.value
          ? null
          : (u(e.type, e.value.toString()),
            r(
              l,
              { type: null == (t = o.value) ? void 0 : t.color_type, disableTransitions: !0 },
              {
                default: () => {
                  var t
                  return [(null == (t = o.value) ? void 0 : t.label) || e.value]
                }
              }
            ))
        : null
      var t
    }
  }
})
export { o as _ }
