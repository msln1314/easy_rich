import { u as e, F as a } from './useForm-c59a8d29.js'
import {
  e as o,
  ad as s,
  B as t,
  L as l,
  x as i,
  E as r,
  al as n,
  N as c,
  M as p,
  a1 as m,
  r as d,
  af as u,
  dI as g,
  o as b,
  l as f,
  k as w,
  S as _,
  ac as h
} from './index-820a519e.js'
import { E as y } from './el-progress-97dbc0fb.js'
import { u as I } from './useValidator-db15330d.js'
const P = o({
  __name: 'Basic',
  props: { tabId: s.number },
  setup(o) {
    const s = o,
      { required: P } = I(),
      { getStorage: x } = _(),
      O = t(),
      v = x(O.getToken),
      j = l([
        {
          field: 'web_title',
          label: '系统标题',
          colProps: { span: 24 },
          component: 'Input',
          componentProps: { style: { width: '500px' } }
        },
        {
          field: 'web_logo',
          label: '系统 LOGO',
          colProps: { span: 24 },
          formItemProps: {
            slots: {
              default: (e) =>
                i(
                  y,
                  {
                    class: 'system-settings-basic-image-uploader',
                    action: '/api/system/upload/image/to/local',
                    data: { path: 'system' },
                    'show-file-list': !1,
                    'before-upload': (e) => {
                      const a = ['image/jpeg', 'image/gif', 'image/png'].includes(e.type),
                        o = e.size / 1024 / 1024 < 5
                      return (
                        a || u.error('上传LOGO图片必须是 JPG/GIF/PNG/ 格式!'),
                        o || u.error('上传LOGO图片大小不能超过 5MB!'),
                        a && o
                      )
                    },
                    'on-success': (a) => {
                      200 === a.code ? (e.web_logo = a.data.remote_path) : u.error(a.message)
                    },
                    accept: 'image/jpeg,image/gif,image/png',
                    name: 'file',
                    headers: { Authorization: v }
                  },
                  {
                    default: () => [
                      e.web_logo
                        ? i('img', { src: e.web_logo, class: 'logo-image' }, null)
                        : i(
                            r,
                            { class: 'logo-image-uploader-icon' },
                            { default: () => [i(n, { icon: 'akar-icons:plus', size: 23 }, null)] }
                          )
                    ]
                  }
                )
            }
          }
        },
        {
          field: 'web_desc',
          label: '系统描述',
          colProps: { span: 24 },
          component: 'Input',
          componentProps: { rows: 4, type: 'textarea', style: { width: '500px' } }
        },
        {
          field: 'web_ico',
          label: 'ICO 图标',
          colProps: { span: 24 },
          formItemProps: {
            slots: {
              default: (e) =>
                i(
                  y,
                  {
                    class: 'system-settings-basic-image-uploader',
                    action: '/api/system/upload/image/to/local',
                    data: { path: 'system' },
                    'show-file-list': !1,
                    'before-upload': (e) => {
                      const a = ['image/x-icon'].includes(e.type),
                        o = e.size / 1024 / 1024 < 2
                      return (
                        a || u.error('上传ICO图标必须是 ico 格式!'),
                        o || u.error('上传ICO图标大小不能超过 2MB!'),
                        a && o
                      )
                    },
                    'on-success': (a) => {
                      200 === a.code
                        ? ((e.web_ico = a.data.remote_path),
                          (e.web_ico_local_path = a.data.local_path))
                        : u.error(a.message)
                    },
                    accept: 'image/jpeg,image/gif,image/png',
                    name: 'file',
                    headers: { Authorization: v }
                  },
                  {
                    default: () => [
                      e.web_ico
                        ? i('img', { src: e.web_ico, class: 'ico-image' }, null)
                        : i(
                            r,
                            { class: 'ico-image-uploader-icon' },
                            { default: () => [i(n, { icon: 'akar-icons:plus', size: 23 }, null)] }
                          )
                    ]
                  }
                )
            }
          }
        },
        {
          field: 'web_ico_local_path',
          label: 'ICO 图标服务器文件地址',
          component: 'Input',
          colProps: { span: 24 },
          hidden: !0
        },
        {
          field: 'web_icp_number',
          label: '备案号',
          colProps: { span: 24 },
          component: 'Input',
          componentProps: { style: { width: '500px' } }
        },
        {
          field: 'web_copyright',
          label: '版权信息',
          colProps: { span: 24 },
          component: 'Input',
          componentProps: { style: { width: '500px' } }
        },
        {
          field: 'active',
          label: '',
          colProps: { span: 24 },
          formItemProps: {
            slots: {
              default: () =>
                i(m, null, [
                  i(
                    c,
                    { loading: B.value, type: 'primary', onClick: M },
                    { default: () => [p('立即提交')] }
                  )
                ])
            }
          }
        }
      ]),
      C = l({ web_title: [P()], web_logo: [P()], web_ico: [P()] }),
      { formRegister: z, formMethods: F } = e(),
      { setValues: G, getFormData: k, getElFormExpose: E } = F
    let L = d({})
    const B = d(!1),
      M = async () => {
        const e = await E()
        if (await (null == e ? void 0 : e.validate())) {
          const e = await k()
          if (((B.value = !0), !e)) return ((B.value = !1), u.error('未获取到数据'))
          try {
            const a = await g(e)
            if (a)
              return (
                O.setTitle(a.data.web_title || '后台系统'),
                O.setLogoImage(a.data.web_logo || '/static/system/logo.png'),
                O.setFooterContent(a.data.web_copyright || 'Copyright ©2022-present K'),
                O.setIcpNumber(a.data.web_icp_number || ''),
                u.success('更新成功')
              )
          } finally {
            B.value = !1
          }
        }
      }
    return (
      (async () => {
        const e = await h({ tab_id: s.tabId })
        if (e) {
          ;(await G(e.data), (L.value = e.data))
          const a = await E()
          null == a || a.clearValidate()
        }
      })(),
      (e, o) => (
        b(),
        f(w(a), { rules: C, onRegister: w(z), schema: j }, null, 8, [
          'rules',
          'onRegister',
          'schema'
        ])
      )
    )
  }
})
export { P as _ }
