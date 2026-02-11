import { u as e, F as s } from "./useForm-b6ceb895.js";
import { u as t } from "./useValidator-63200dcb.js";
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
  k as f,
} from "./index-6b60d190.js";
import { _ as v } from "./ContentWrap.vue_vue_type_script_setup_true_lang-067de0d9.js";
import { a as _, b as g, p as y, c as w } from "./issue-18263b13.js";
import "./el-form-item-ce18addb.js";
import "./el-col-b8aa0d1a.js";
import "./el-tooltip-4ed993c7.js";
import "./el-popper-09548d54.js";
import "./isNil-1f22f7b0.js";
import "./focus-trap-275966d8.js";
import "./el-input-38d674e5.js";
import "./event-5568c9d8.js";
/* empty css               */ import "./el-checkbox-4903f610.js";
import "./isEqual-b8d86c27.js";
/* empty css                          */ import "./el-date-picker-91f17f23.js";
import "./debounce-5c500a3d.js";
import "./index-fdfa028a.js";
import "./el-radio-group-0c46635e.js";
import "./el-select-8805ff65.js";
import "./index-b7c1540b.js";
import "./strings-00317668.js";
import "./scroll-6dba6951.js";
import "./validator-f032316f.js";
import "./el-switch-5507f2ea.js";
import "./el-divider-2dd0a1ee.js";
import "./el-tree-84af12f2.js";
import "./index-55fef7b1.js";
import "./el-progress-31e0b945.js";
import "./style.css_vue_type_style_index_0_src_true_lang-d8fdefc2.js";
import "./el-card-37d6f3c4.js";
const b = o({
  name: "HelpIssueForm",
  __name: "Write",
  setup(o, { expose: b }) {
    const { required: h } = t(),
      { push: P, currentRoute: x } = r(),
      I = {
        customAlert: (e, s) => {
          switch (s) {
            case "success":
              u.success(e);
              break;
            case "info":
            default:
              u.info(e);
              break;
            case "warning":
              u.warning(e);
              break;
            case "error":
              u.error(e);
          }
        },
        autoFocus: !1,
        scroll: !0,
        readOnly: !1,
        uploadImgShowBase64: !0,
        placeholder: "请输入内容...",
      },
      k = a([
        {
          field: "title",
          label: "标题名称",
          component: "Input",
          colProps: { span: 24 },
          componentProps: { style: { width: "100%" } },
          formItemProps: { rules: [h()] },
        },
        {
          field: "content",
          label: "内容",
          colProps: { span: 24 },
          component: "Editor",
          componentProps: {
            style: { width: "100%" },
            editorConfig: I,
            editorId: "issueContent",
          },
          formItemProps: { rules: [h()] },
        },
        {
          field: "category_id",
          label: "问题类别",
          colProps: { span: 24 },
          component: "Select",
          componentProps: { style: { width: "100%" } },
          formItemProps: { rules: [h()] },
          optionApi: async () => (await _()).data,
        },
        {
          field: "",
          label: "",
          colProps: { span: 24 },
          formItemProps: {
            slots: {
              default: () =>
                i(m, null, [
                  i(
                    l,
                    { loading: N.value, type: "primary", onClick: M },
                    { default: () => [p("立即保存")] },
                  ),
                ]),
            },
          },
        },
      ]),
      { formRegister: F, formMethods: C } = e(),
      { getFormData: E, getElFormExpose: R, setValues: q } = C,
      A = n(""),
      N = n(!1);
    (async () => {
      const e = x.value.query.id;
      if (e) {
        A.value = "edit";
        const s = await w(Number(e));
        s ? q(s.data) : P("/404");
      } else A.value = "add";
    })();
    const M = async () => {
      const e = await R();
      if (await (null == e ? void 0 : e.validate())) {
        N.value = !0;
        const s = await E();
        if (!s) return ((N.value = !1), u.error("未获取到数据"));
        const t = n();
        try {
          "add" === A.value
            ? ((t.value = await g(s)),
              t.value && (null == e || e.resetFields(), u.success("新增成功")))
            : "edit" === A.value &&
              ((t.value = await y(s)),
              t.value && (q(t.value.data), u.success("更新成功")));
        } finally {
          N.value = !1;
        }
      }
    };
    return (
      b({ submit: M }),
      (e, t) => (
        c(),
        d(f(v), null, {
          default: j(() => [
            i(
              f(s),
              { onRegister: f(F), schema: k, labelPosition: "top" },
              null,
              8,
              ["onRegister", "schema"],
            ),
          ]),
          _: 1,
        })
      )
    );
  },
});
export { b as default };
