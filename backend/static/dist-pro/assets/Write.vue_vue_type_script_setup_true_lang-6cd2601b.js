import { u as e, F as o } from "./useForm-b6ceb895.js";
import { u as l } from "./useValidator-63200dcb.js";
import { c as t } from "./role-af5fad9c.js";
import { c as a } from "./dept-7c279e0e.js";
import {
  e as s,
  L as n,
  w as p,
  o as i,
  l as r,
  k as c,
} from "./index-6b60d190.js";
const d = s({
  __name: "Write",
  props: { currentRow: { type: Object, default: () => null } },
  setup(s, { expose: d }) {
    const m = s,
      { required: u, isTelephone: f, isEmail: b } = l(),
      v = n([
        {
          field: "name",
          label: "用户名称",
          colProps: { span: 12 },
          component: "Input",
          componentProps: { style: { width: "100%" } },
        },
        {
          field: "nickname",
          label: "用户昵称",
          colProps: { span: 12 },
          component: "Input",
          componentProps: { style: { width: "100%" } },
        },
        {
          field: "phone",
          label: "手机号码",
          colProps: { span: 12 },
          component: "Input",
          componentProps: { style: { width: "100%" } },
        },
        {
          field: "email",
          label: "邮箱",
          colProps: { span: 12 },
          component: "Input",
          componentProps: { style: { width: "100%" } },
        },
        {
          field: "gender",
          label: "性别",
          colProps: { span: 12 },
          component: "RadioGroup",
          componentProps: {
            style: { width: "100%" },
            options: [
              { label: "男", value: "0" },
              { label: "女", value: "1" },
            ],
          },
          value: "0",
        },
        {
          field: "",
          label: "默认密码",
          colProps: { span: 12 },
          component: "Text",
          componentProps: { style: { width: "100%" } },
          value: "手机号后六位",
          ifshow: (e) => void 0 === e.id,
        },
        {
          field: "is_staff",
          label: "工作人员",
          colProps: { span: 12 },
          component: "RadioGroup",
          componentProps: {
            style: { width: "100%" },
            options: [
              { label: "是", value: !0 },
              { label: "否", value: !1 },
            ],
          },
          value: !0,
        },
        {
          field: "is_admin",
          label: "管理人员",
          colProps: { span: 12 },
          component: "RadioGroup",
          componentProps: {
            style: { width: "100%" },
            options: [
              { label: "是", value: !0 },
              { label: "否", value: !1 },
            ],
          },
          value: !1,
        },
        {
          field: "is_active",
          label: "状态",
          colProps: { span: 12 },
          component: "RadioGroup",
          componentProps: {
            style: { width: "100%" },
            options: [
              { label: "正常", value: !0 },
              { label: "停用", value: !1 },
            ],
          },
          value: !0,
        },
        {
          field: "role_ids",
          label: "角色",
          colProps: { span: 24 },
          component: "Select",
          componentProps: { style: { width: "100%" }, multiple: !0 },
          optionApi: async () => (await t()).data,
          value: [],
          ifshow: (e) => e.is_staff,
        },
        {
          field: "dept_id",
          label: "部门",
          colProps: { span: 24 },
          component: "TreeSelect",
          componentProps: {
            style: { width: "100%" },
            checkStrictly: !0,
            defaultExpandAll: !0,
          },
          optionApi: async () => (await a()).data,
          value: [],
          ifshow: (e) => e.is_staff,
        },
      ]),
      w = n({
        name: [u()],
        is_active: [u()],
        is_staff: [u()],
        role_ids: [u()],
        dept_ids: [u()],
        telephone: [u(), { validator: f, trigger: "blur" }],
        email: [{ validator: b, trigger: "blur" }],
      }),
      { formRegister: P, formMethods: h } = e(),
      { setValues: y, getFormData: _, getElFormExpose: g } = h;
    return (
      p(
        () => m.currentRow,
        (e) => {
          e && y(e);
        },
        { deep: !0, immediate: !0 },
      ),
      d({
        submit: async () => {
          const e = await g();
          if (await (null == e ? void 0 : e.validate())) {
            return await _();
          }
        },
      }),
      (e, l) => (
        i(),
        r(c(o), { rules: w, onRegister: c(P), schema: v }, null, 8, [
          "rules",
          "onRegister",
          "schema",
        ])
      )
    );
  },
});
export { d as _ };
