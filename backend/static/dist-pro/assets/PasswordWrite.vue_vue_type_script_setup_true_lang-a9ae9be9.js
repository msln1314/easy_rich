import { u as s, F as a } from "./useForm-b6ceb895.js";
import { u as e } from "./useValidator-63200dcb.js";
import {
  e as r,
  v as o,
  L as l,
  r as t,
  o as i,
  l as d,
  k as n,
  x as p,
  N as m,
  M as c,
  a1 as u,
  O as w,
  af as f,
} from "./index-6b60d190.js";
const g = r({
  __name: "PasswordWrite",
  setup(r) {
    const { required: g } = e(),
      P = o(),
      v = l([
        { field: "title", colProps: { span: 24 } },
        {
          field: "password",
          label: "新密码",
          component: "InputPassword",
          colProps: { span: 24 },
          componentProps: {
            style: { width: "50%" },
            placeholder: "请输入新密码",
          },
        },
        {
          field: "password_two",
          label: "确认密码",
          component: "InputPassword",
          colProps: { span: 24 },
          componentProps: {
            style: { width: "50%" },
            placeholder: "请再次输入新密码",
          },
        },
        {
          field: "save",
          colProps: { span: 24 },
          formItemProps: {
            slots: {
              default: () =>
                p(u, null, [
                  p("div", { class: "w-[50%]" }, [
                    p(
                      m,
                      {
                        loading: _.value,
                        type: "primary",
                        class: "w-[100%]",
                        onClick: j,
                      },
                      { default: () => [c("保存")] },
                    ),
                  ]),
                ]),
            },
          },
        },
      ]),
      b = {
        password: [
          g(),
          {
            min: 8,
            max: 16,
            message: "长度需为8-16个字符,请重新输入。",
            trigger: "blur",
          },
        ],
        password_two: [
          g(),
          {
            min: 8,
            max: 16,
            message: "长度需为8-16个字符,请重新输入。",
            trigger: "blur",
          },
        ],
      },
      { formRegister: h, formMethods: y } = s(),
      { setValues: k, getFormData: x, getElFormExpose: F } = y;
    k(P.getUser);
    const _ = t(!1),
      j = async () => {
        const s = await F();
        if (await (null == s ? void 0 : s.validate())) {
          _.value = !0;
          const a = await x();
          try {
            (await w(a)) &&
              (null == s || s.resetFields(), f.success("保存成功"));
          } finally {
            _.value = !1;
          }
        }
      };
    return (s, e) => (
      i(),
      d(
        n(a),
        {
          onRegister: n(h),
          schema: v,
          rules: b,
          "hide-required-asterisk": "",
          class:
            "dark:border-1 dark:border-[var(--el-border-color)] dark:border-solid",
        },
        null,
        8,
        ["onRegister", "schema"],
      )
    );
  },
});
export { g as _ };
