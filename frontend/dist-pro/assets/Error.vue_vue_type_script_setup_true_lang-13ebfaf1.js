import {
  e,
  ad as r,
  o as s,
  j as t,
  y as a,
  z as o,
  x as n,
  m as i,
  k as l,
  I as c,
  M as m,
  N as u
} from './index-820a519e.js'
const p = { class: 'flex justify-center' },
  x = { class: 'text-center' },
  d = ['src'],
  f = { class: 'text-14px text-[var(--el-color-info)]' },
  g = { class: 'mt-20px' },
  v = e({
    __name: 'Error',
    props: { type: r.string.validate((e) => ['404', '500', '403'].includes(e)).def('404') },
    emits: ['errorClick'],
    setup(e, { emit: r }) {
      const v = e,
        { t: y } = c(),
        T = {
          404: {
            url: '/assets/404-1759fece.svg',
            message: y('error.pageError'),
            buttonText: y('error.returnToHome')
          },
          500: {
            url: '/assets/500-8fda557c.svg',
            message: y('error.networkError'),
            buttonText: y('error.returnToHome')
          },
          403: {
            url: '/assets/403-af24f6bf.svg',
            message: y('error.noPermission'),
            buttonText: y('error.returnToHome')
          }
        },
        b = () => {
          r('errorClick', v.type)
        }
      return (r, c) => (
        s(),
        t('div', p, [
          a('div', x, [
            a('img', { width: '350', src: T[e.type].url, alt: '' }, null, 8, d),
            a('div', f, o(T[e.type].message), 1),
            a('div', g, [
              n(
                l(u),
                { type: 'primary', onClick: b },
                { default: i(() => [m(o(T[e.type].buttonText), 1)]), _: 1 }
              )
            ])
          ])
        ])
      )
    }
  })
export { v as _ }
