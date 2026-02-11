import { u as e, F as a } from "./useForm-b6ceb895.js";
import {
  e as s,
  ad as t,
  L as o,
  x as r,
  N as p,
  M as l,
  a1 as n,
  r as i,
  af as c,
  dI as d,
  o as u,
  l as m,
  k as _,
  ac as f,
} from "./index-6b60d190.js";
import { u as w } from "./useValidator-63200dcb.js";
const v = s({
  __name: "WechatServer",
  props: { tabId: t.number },
  setup(s) {
    const t = s,
      { required: v } = w(),
      x = o([
        {
          field: "wx_server_app_id",
          label: "AppID",
          colProps: { span: 24 },
          component: "Input",
          componentProps: { style: { width: "500px" } },
        },
        {
          field: "wx_server_app_secret",
          label: "AppSecret",
          colProps: { span: 24 },
          component: "Input",
          componentProps: { style: { width: "500px" } },
        },
        {
          field: "wx_server_email",
          label: "官方邮件",
          colProps: { span: 24 },
          component: "Input",
          componentProps: { style: { width: "500px" } },
        },
        {
          field: "wx_server_phone",
          label: "服务热线",
          colProps: { span: 24 },
          component: "Input",
          componentProps: { style: { width: "500px" } },
        },
        {
          field: "wx_server_site",
          label: "官方邮箱",
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
                r(n, null, [
                  r(
                    p,
                    { loading: R.value, type: "primary", onClick: S },
                    { default: () => [l("立即提交")] },
                  ),
                ]),
            },
          },
        },
      ]),
      P = o({ wx_server_app_id: [v()], wx_server_app_secret: [v()] }),
      { formRegister: y, formMethods: b } = e(),
      { setValues: h, getFormData: I, getElFormExpose: g } = b;
    let F = i({});
    const j = async () => {
        const e = await f({ tab_id: t.tabId });
        if (e) {
          (await h(e.data), (F.value = e.data));
          const a = await g();
          null == a || a.clearValidate();
        }
      },
      R = i(!1),
      S = async () => {
        const e = await g();
        if (await (null == e ? void 0 : e.validate())) {
          const e = await I();
          if (((R.value = !0), !e))
            return ((R.value = !1), c.error("未获取到数据"));
          try {
            if (await d(e)) return (j(), c.success("更新成功"));
          } finally {
            R.value = !1;
          }
        }
      };
    return (
      j(),
      (e, s) => (
        u(),
        m(_(a), { rules: P, onRegister: _(y), schema: x }, null, 8, [
          "rules",
          "onRegister",
          "schema",
        ])
      )
    );
  },
});
export { v as _ };
