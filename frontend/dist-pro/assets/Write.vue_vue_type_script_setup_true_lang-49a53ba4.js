import { u as e, F as o } from './useForm-c59a8d29.js'
import { u as l } from './useValidator-db15330d.js'
import { c as t } from './role-0252bcb8.js'
import { c as a } from './dept-b8a01226.js'
import { g as s } from './client_group-aeb78440.js'
import { e as p, L as i, w as n, o as r, l as c, k as d } from './index-820a519e.js'
const m = p({
  __name: 'Write',
  props: { currentRow: { type: Object, default: () => null } },
  setup(p, { expose: m }) {
    const u = p,
      { required: f, isTelephone: w, isEmail: b } = l(),
      h = i([
        {
          field: 'name',
          label: '用户名称',
          colProps: { span: 12 },
          component: 'Input',
          componentProps: { style: { width: '100%' } }
        },
        {
          field: 'nickname',
          label: '用户昵称',
          colProps: { span: 12 },
          component: 'Input',
          componentProps: { style: { width: '100%' } }
        },
        {
          field: 'phone',
          label: '手机号码',
          colProps: { span: 12 },
          component: 'Input',
          componentProps: { style: { width: '100%' } }
        },
        {
          field: 'email',
          label: '邮箱',
          colProps: { span: 12 },
          component: 'Input',
          componentProps: { style: { width: '100%' } }
        },
        {
          field: 'gender',
          label: '性别',
          colProps: { span: 12 },
          component: 'RadioGroup',
          componentProps: {
            style: { width: '100%' },
            options: [
              { label: '男', value: '0' },
              { label: '女', value: '1' }
            ]
          },
          value: '0'
        },
        {
          field: '',
          label: '默认密码',
          colProps: { span: 12 },
          component: 'Text',
          componentProps: { style: { width: '100%' } },
          value: '手机号后六位',
          ifshow: (e) => void 0 === e.id
        },
        {
          field: 'is_staff',
          label: '工作人员',
          colProps: { span: 12 },
          component: 'RadioGroup',
          componentProps: {
            style: { width: '100%' },
            options: [
              { label: '是', value: !0 },
              { label: '否', value: !1 }
            ]
          },
          value: !0
        },
        {
          field: 'is_admin',
          label: '管理人员',
          colProps: { span: 12 },
          component: 'RadioGroup',
          componentProps: {
            style: { width: '100%' },
            options: [
              { label: '是', value: !0 },
              { label: '否', value: !1 }
            ]
          },
          value: !1
        },
        {
          field: 'is_active',
          label: '状态',
          colProps: { span: 12 },
          component: 'RadioGroup',
          componentProps: {
            style: { width: '100%' },
            options: [
              { label: '正常', value: !0 },
              { label: '停用', value: !1 }
            ]
          },
          value: !0
        },
        {
          field: 'iot_group_ids',
          label: '分组',
          colProps: { span: 12 },
          component: 'TreeSelect',
          componentProps: {
            style: { width: '100%' },
            checkStrictly: !0,
            defaultExpandAll: !0,
            multiple: !0
          },
          optionApi: async () => (await s()).data,
          value: [],
          ifshow: (e) => e.is_staff
        },
        {
          field: 'role_ids',
          label: '角色',
          colProps: { span: 12 },
          component: 'Select',
          componentProps: { style: { width: '100%' }, multiple: !0 },
          optionApi: async () => (await t()).data,
          value: [],
          ifshow: (e) => e.is_staff
        },
        {
          field: 'dept_id',
          label: '部门',
          colProps: { span: 24 },
          component: 'TreeSelect',
          componentProps: { style: { width: '100%' }, checkStrictly: !0, defaultExpandAll: !0 },
          optionApi: async () => (await a()).data,
          value: [],
          ifshow: (e) => e.is_staff
        }
      ]),
      v = i({
        name: [f()],
        is_active: [f()],
        is_staff: [f()],
        role_ids: [f()],
        dept_id: [f()],
        phone: [f(), { validator: w, trigger: 'blur' }],
        email: [{ validator: b, trigger: 'blur' }]
      }),
      { formRegister: P, formMethods: y } = e(),
      { setValues: _, getFormData: g, getElFormExpose: R } = y
    return (
      n(
        () => u.currentRow,
        (e) => {
          e && _(e)
        },
        { deep: !0, immediate: !0 }
      ),
      m({
        submit: async () => {
          const e = await R()
          if (await (null == e ? void 0 : e.validate())) {
            return await g()
          }
        }
      }),
      (e, l) => (
        r(),
        c(d(o), { rules: v, onRegister: d(P), schema: h }, null, 8, [
          'rules',
          'onRegister',
          'schema'
        ])
      )
    )
  }
})
export { m as _ }
