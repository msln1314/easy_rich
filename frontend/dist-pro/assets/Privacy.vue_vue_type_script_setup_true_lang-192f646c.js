import {
  e as a,
  ad as e,
  r as s,
  o as r,
  j as l,
  x as t,
  k as o,
  y as c,
  m as i,
  M as n,
  N as u,
  a1 as d,
  ac as _,
  dI as y,
  af as p
} from './index-820a519e.js'
import { _ as f } from './style.css_vue_type_style_index_0_src_true_lang-4a035adc.js'
const m = { class: 'mt-10px', style: { float: 'right' } },
  v = a({
    __name: 'Privacy',
    props: { tabId: e.number },
    setup(a) {
      const e = a,
        v = s(),
        b = s(''),
        w = async () => {
          const a = await _({ tab_id: e.tabId })
          a && (b.value = a.data.web_privacy || '')
        },
        g = s(!1),
        k = async () => {
          g.value = !0
          try {
            if (await y({ web_privacy: b.value })) return (w(), p.success('更新成功'))
          } finally {
            g.value = !1
          }
        },
        x = {
          customAlert: (a, e) => {
            switch (e) {
              case 'success':
                p.success(a)
                break
              case 'info':
              default:
                p.info(a)
                break
              case 'warning':
                p.warning(a)
                break
              case 'error':
                p.error(a)
            }
          },
          autoFocus: !0,
          scroll: !0,
          readOnly: !1,
          uploadImgShowBase64: !0
        }
      return (
        w(),
        (a, e) => (
          r(),
          l(
            d,
            null,
            [
              t(
                o(f),
                {
                  modelValue: b.value,
                  'onUpdate:modelValue': e[0] || (e[0] = (a) => (b.value = a)),
                  ref_key: 'editorRef',
                  ref: v,
                  editorId: 'web_privacy',
                  editorConfig: x
                },
                null,
                8,
                ['modelValue']
              ),
              c('div', m, [
                t(
                  o(u),
                  { loading: g.value, type: 'primary', onClick: k },
                  { default: i(() => [n('立即保存')]), _: 1 },
                  8,
                  ['loading']
                )
              ])
            ],
            64
          )
        )
      )
    }
  })
export { v as _ }
