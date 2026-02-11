import { u as e, F as o } from "./useForm-b6ceb895.js";
import { u as a } from "./useValidator-63200dcb.js";
import {
  e as t,
  ad as l,
  L as n,
  w as s,
  o as p,
  l as r,
  k as i,
} from "./index-6b60d190.js";
import { b as d } from "./dept-7c279e0e.js";
const c = t({
  __name: "Write",
  props: {
    currentRow: { type: Object, default: () => null },
    parentId: l.number.def(void 0),
  },
  setup(t, { expose: l }) {
    const c = t,
      { required: m } = a(),
      u = n([
        {
          field: "parent_id",
          label: "上级部门",
          colProps: { span: 24 },
          component: "TreeSelect",
          componentProps: {
            style: { width: "100%" },
            checkStrictly: !0,
            placeholder: "请选择上级部门",
            nodeKey: "value",
            defaultExpandAll: !0,
          },
          optionApi: async () => (await d()).data,
          value: c.parentId,
        },
        {
          field: "name",
          label: "部门名称",
          component: "Input",
          colProps: { span: 12 },
        },
        {
          field: "code",
          label: "部门标识",
          component: "Input",
          colProps: { span: 12 },
        },
        {
          field: "manager",
          label: "负责人",
          component: "Input",
          colProps: { span: 12 },
        },
        {
          field: "phone",
          label: "联系电话",
          component: "Input",
          colProps: { span: 12 },
        },
        {
          field: "email",
          label: "邮箱",
          component: "Input",
          colProps: { span: 12 },
        },
        {
          field: "remak",
          label: "描述",
          component: "Input",
          colProps: { span: 12 },
        },
        {
          field: "order",
          label: "显示排序",
          component: "InputNumber",
          colProps: { span: 12 },
          componentProps: { style: { width: "100%" } },
        },
        {
          field: "status",
          label: "是否禁用",
          colProps: { span: 12 },
          component: "RadioGroup",
          componentProps: {
            style: { width: "100%" },
            options: [
              { label: "正常", value: !1 },
              { label: "停用", value: !0 },
            ],
          },
          value: !1,
        },
      ]),
      f = n({ name: [m()], code: [m()], status: [m()], order: [m()] }),
      { formRegister: b, formMethods: P } = e(),
      { setValues: h, getFormData: w, getElFormExpose: I } = P;
    return (
      s(
        () => c.currentRow,
        (e) => {
          e && h(e);
        },
        { deep: !0, immediate: !0 },
      ),
      l({
        submit: async () => {
          const e = await I();
          if (await (null == e ? void 0 : e.validate())) {
            return await w();
          }
        },
      }),
      (e, a) => (
        p(),
        r(
          i(o),
          { rules: f, onRegister: i(b), schema: u, labelWidth: 100 },
          null,
          8,
          ["rules", "onRegister", "schema"],
        )
      )
    );
  },
});
export { c as _ };
