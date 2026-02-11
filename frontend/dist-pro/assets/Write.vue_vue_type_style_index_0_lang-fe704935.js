import { u as e, F as a } from './useForm-c59a8d29.js'
import { u as l } from './useValidator-db15330d.js'
import {
  e as s,
  L as i,
  x as t,
  M as o,
  al as r,
  a1 as u,
  r as n,
  af as p,
  w as m,
  o as c,
  j as d,
  k as v,
  l as g,
  F as f
} from './index-820a519e.js'
import { E as x } from './el-progress-97dbc0fb.js'
import { E as w } from './el-image-viewer-73f400a0.js'
const h = s({
  __name: 'Write',
  props: { currentRow: { type: Object, default: () => null } },
  setup(s, { expose: h }) {
    const j = s,
      { required: b } = l(),
      P = i([
        {
          field: 'upload_method',
          label: '上传方式',
          colProps: { span: 24 },
          component: 'RadioGroup',
          componentProps: {
            options: [
              { label: '同时上传', value: '1' },
              { label: '按顺序上传', value: '2' }
            ]
          },
          value: '1',
          formItemProps: { rules: [b()] }
        },
        {
          field: 'images',
          label: '',
          colProps: { span: 24 },
          formItemProps: {
            rules: [b()],
            slots: {
              default: () =>
                t(u, null, [
                  t('div', { class: 'flex justify-between w-[100%]' }, [
                    t('span', null, [o('图片资源')]),
                    t('span', null, [o('最大数量限制：'), M.value.length, o('/'), I.value])
                  ]),
                  t(
                    x,
                    {
                      class: 'resource-image-uploader',
                      action: '#',
                      'http-request': B,
                      'file-list': M.value,
                      'onUpdate:file-list': (e) => (M.value = e),
                      'show-file-list': !0,
                      multiple: !0,
                      'before-upload': V,
                      'on-success': q,
                      'on-preview': C,
                      'on-exceed': J,
                      accept: 'image/jpeg,image/png',
                      name: 'file',
                      'list-type': 'picture-card',
                      limit: I.value,
                      drag: !0,
                      disabled: I.value <= M.value.length
                    },
                    {
                      default: () => [
                        M.value.length < I.value
                          ? t('div', { class: 'resource-image-uploader-icon' }, [
                              t(r, { icon: 'akar-icons:plus', size: 23 }, null),
                              t('span', { class: 'text-[12px]' }, [o('点击或拖拽到这里')]),
                              t('span', { class: 'text-[12px]' }, [M.value.length, o('/'), I.value])
                            ])
                          : t('div', { class: 'resource-image-uploader-icon' }, [
                              t('span', { class: 'text-[12px]' }, [o('已到最大限制')]),
                              t('span', { class: 'text-[12px]' }, [M.value.length, o('/'), I.value])
                            ])
                      ]
                    }
                  )
                ])
            }
          }
        }
      ]),
      { formRegister: y, formMethods: R } = e(),
      { setValues: E, getFormData: F, getElFormExpose: _, setValue: k } = R,
      z = n(!1),
      G = n(0),
      I = n(50),
      M = n([]),
      V = (e) => {
        const a = ['image/jpeg', 'image/gif', 'image/png'].includes(e.type),
          l = e.size / 1024 / 1024 < 3
        return (
          a || p.error('上传图片素材必须是 JPG/PNG/ 格式!'),
          l || p.error('上传图片素材大小不能超过 3MB!'),
          a && l
        )
      },
      q = (e, a, l) => {
        ;((M.value = l), k('images', l))
      },
      B = (e) =>
        new Promise((a) => {
          a(e)
        }),
      C = (e) => {
        ;((G.value = M.value.findIndex((a) => a.uid === e.uid)), (z.value = !0))
      },
      D = () => {
        z.value = !1
      },
      J = () => {
        p.error('上传失败，超出图片最大数量限制!')
      }
    return (
      m(
        () => j.currentRow,
        (e) => {
          e && E(e)
        },
        { deep: !0, immediate: !0 }
      ),
      h({
        submit: async () => {
          const e = await _()
          if (await (null == e ? void 0 : e.validate())) {
            return await F()
          }
        }
      }),
      (e, l) => (
        c(),
        d(
          u,
          null,
          [
            t(v(a), { onRegister: v(y), schema: P }, null, 8, ['onRegister', 'schema']),
            z.value
              ? (c(),
                g(
                  v(w),
                  {
                    key: 0,
                    'z-index': 9999,
                    onClose: D,
                    'url-list': M.value.map((e) => e.url),
                    'initial-index': G.value
                  },
                  null,
                  8,
                  ['url-list', 'initial-index']
                ))
              : f('', !0)
          ],
          64
        )
      )
    )
  }
})
export { h as _ }
