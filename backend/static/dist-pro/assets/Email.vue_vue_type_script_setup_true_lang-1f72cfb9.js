import { u as a, F as e } from "./useForm-b6ceb895.js";
import {
  e as s,
  ad as t,
  L as o,
  x as l,
  N as r,
  M as n,
  a1 as i,
  r as p,
  af as m,
  dI as c,
  o as u,
  l as d,
  k as f,
  ac as w,
} from "./index-6b60d190.js";
import { u as _ } from "./useValidator-63200dcb.js";
const v = s({
  __name: "Email",
  props: { tabId: t.number },
  setup(s) {
    const t = s,
      { required: v } = _(),
      y = o([
        {
          field: "email_access",
          label: "邮箱账号",
          colProps: { span: 24 },
          component: "Input",
          componentProps: { style: { width: "500px" } },
        },
        {
          field: "email_password",
          label: "邮箱密码",
          colProps: { span: 24 },
          component: "Input",
          componentProps: { style: { width: "500px" } },
        },
        {
          field: "email_server",
          label: "邮箱服务器",
          colProps: { span: 24 },
          component: "Input",
          componentProps: { style: { width: "500px" } },
        },
        {
          field: "email_port",
          label: "服务器端口",
          colProps: { span: 24 },
          component: "Input",
          componentProps: { style: { width: "500px" } },
        },
        {
          field: "active",
          label: "",
          colProps: { span: 24 },
          formItemProps: {
            slots: {
              default: () =>
                l(i, null, [
                  l(
                    r,
                    { loading: E.value, type: "primary", onClick: R },
                    { default: () => [n("立即提交")] },
                  ),
                ]),
            },
          },
        },
      ]),
      P = o({
        email_access: [v()],
        email_password: [v()],
        email_port: [v()],
        email_server: [v()],
      }),
      { formRegister: b, formMethods: x } = a(),
      { setValues: I, getFormData: h, getElFormExpose: g } = x;
    let F = p({});
    const j = async () => {
        const a = await w({ tab_id: t.tabId });
        if (a) {
          (await I(a.data), (F.value = a.data));
          const e = await g();
          null == e || e.clearValidate();
        }
      },
      E = p(!1),
      R = async () => {
        const a = await g();
        if (await (null == a ? void 0 : a.validate())) {
          const a = await h();
          if (((E.value = !0), !a))
            return ((E.value = !1), m.error("未获取到数据"));
          try {
            if (await c(a)) return (j(), m.success("更新成功"));
          } finally {
            E.value = !1;
          }
        }
      };
    return (
      j(),
      (a, s) => (
        u(),
        d(f(e), { rules: P, onRegister: f(b), schema: y }, null, 8, [
          "rules",
          "onRegister",
          "schema",
        ])
      )
    );
  },
});
export { v as _ };
