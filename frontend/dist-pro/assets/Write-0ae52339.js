import { u as e, F as s } from './useForm-c59a8d29.js'
import { u as t } from './useValidator-db15330d.js'
import {
  e as o,
  A as r,
  L as a,
  x as i,
  N as l,
  M as p,
  a1 as m,
  r as n,
  af as u,
  o as c,
  l as d,
  m as j,
  k as f
} from './index-820a519e.js'
import { _ as v } from './ContentWrap.vue_vue_type_script_setup_true_lang-37d6ee07.js'
import { a as _, b as g, p as y, c as w } from './issue-784d4340.js'
import './el-form-item-2e860f96.js'
import './el-col-beabe3f6.js'
import './el-tooltip-4ed993c7.js'
import './el-popper-797844d6.js'
import './isNil-1f22f7b0.js'
import './focus-trap-949626e0.js'
import './el-input-5ae17c8f.js'
import './event-5568c9d8.js'
/* empty css               */ import './el-checkbox-77b6829c.js'
import './isEqual-cb9e370d.js'
/* empty css                          */ import './el-date-picker-6b1a21d2.js'
import './dayjs.min-e5ba30ae.js'
import './debounce-5bc596c6.js'
import './index-eb31d854.js'
import './el-radio-group-4cb40939.js'
import './el-select-38080147.js'
import './index-56bc6266.js'
import './strings-ed83d626.js'
import './scroll-ac7d0423.js'
import './validator-a9d8fe4c.js'
import './el-switch-6f4f5b6a.js'
import './el-divider-9c19755b.js'
import './el-tree-8dac9473.js'
import './index-55f4d4a6.js'
import './el-progress-97dbc0fb.js'
import './style.css_vue_type_style_index_0_src_true_lang-4a035adc.js'
import './el-card-06c161d4.js'
const b = o({
  name: 'HelpIssueForm',
  __name: 'Write',
  setup(o, { expose: b }) {
    const { required: h } = t(),
      { push: P, currentRoute: x } = r(),
      I = {
        customAlert: (e, s) => {
          switch (s) {
            case 'success':
              u.success(e)
              break
            case 'info':
            default:
              u.info(e)
              break
            case 'warning':
              u.warning(e)
              break
            case 'error':
              u.error(e)
          }
        },
        autoFocus: !1,
        scroll: !0,
        readOnly: !1,
        uploadImgShowBase64: !0,
        placeholder: '请输入内容...'
      },
      k = a([
        {
          field: 'title',
          label: '标题名称',
          component: 'Input',
          colProps: { span: 24 },
          componentProps: { style: { width: '100%' } },
          formItemProps: { rules: [h()] }
        },
        {
          field: 'content',
          label: '内容',
          colProps: { span: 24 },
          component: 'Editor',
          componentProps: { style: { width: '100%' }, editorConfig: I, editorId: 'issueContent' },
          formItemProps: { rules: [h()] }
        },
        {
          field: 'category_id',
          label: '问题类别',
          colProps: { span: 24 },
          component: 'Select',
          componentProps: { style: { width: '100%' } },
          formItemProps: { rules: [h()] },
          optionApi: async () => (await _()).data
        },
        {
          field: '',
          label: '',
          colProps: { span: 24 },
          formItemProps: {
            slots: {
              default: () =>
                i(m, null, [
                  i(
                    l,
                    { loading: A.value, type: 'primary', onClick: M },
                    { default: () => [p('立即保存')] }
                  )
                ])
            }
          }
        }
      ]),
      { formRegister: F, formMethods: C } = e(),
      { getFormData: E, getElFormExpose: R, setValues: N } = C,
      q = n(''),
      A = n(!1)
    ;(async () => {
      const e = x.value.query.id
      if (e) {
        q.value = 'edit'
        const s = await w(Number(e))
        s ? N(s.data) : P('/404')
      } else q.value = 'add'
    })()
    const M = async () => {
      const e = await R()
      if (await (null == e ? void 0 : e.validate())) {
        A.value = !0
        const s = await E()
        if (!s) return ((A.value = !1), u.error('未获取到数据'))
        const t = n()
        try {
          'add' === q.value
            ? ((t.value = await g(s)),
              t.value && (null == e || e.resetFields(), u.success('新增成功')))
            : 'edit' === q.value &&
              ((t.value = await y(s)), t.value && (N(t.value.data), u.success('更新成功')))
        } finally {
          A.value = !1
        }
      }
    }
    return (
      b({ submit: M }),
      (e, t) => (
        c(),
        d(f(v), null, {
          default: j(() => [
            i(f(s), { onRegister: f(F), schema: k, labelPosition: 'top' }, null, 8, [
              'onRegister',
              'schema'
            ])
          ]),
          _: 1
        })
      )
    )
  }
})
export { b as default }
