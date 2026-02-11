import {
  e,
  r as a,
  o as s,
  j as t,
  y as r,
  x as l,
  m as i,
  M as n,
  k as d,
  N as o,
  l as p,
  F as u,
  af as f,
  dT as c,
} from "./index-6b60d190.js";
import { E as m, a as _ } from "./el-table-column-0bcf5917.js";
import "./el-checkbox-4903f610.js";
import "./el-tooltip-4ed993c7.js";
import "./el-popper-09548d54.js";
/* empty css               */ import { E as y } from "./el-popconfirm-cb976538.js";
/* empty css                   */ import { E as w } from "./index-b7c1540b.js";
const g = { class: "flex justify-between" },
  k = r("span", null, "已选用户列表", -1),
  v = e({
    __name: "PasswordSendEmail",
    props: { selections: { type: Object } },
    setup(e) {
      const v = e,
        b = a(JSON.parse(JSON.stringify(v.selections))),
        h = a(!1),
        j = async () => {
          h.value = !0;
          const e = b.value
            .filter((e) => !0 !== e.reset_password_status)
            .map((e) => e.id);
          if (e.length <= 0) return f.warning("已全部重置完成，无需重复操作");
          try {
            const a = await c(e);
            a && ((b.value = a.data), f.success("重置成功"));
          } finally {
            h.value = !1;
          }
        };
      return (e, a) => {
        var f;
        return (
          s(),
          t("div", null, [
            r("div", g, [
              k,
              l(
                d(o),
                {
                  type: "primary",
                  disabled: 0 === (null == (f = b.value) ? void 0 : f.length),
                  loading: h.value,
                  onClick: j,
                },
                { default: i(() => [n("确认重置并发送邮件通知")]), _: 1 },
                8,
                ["disabled", "loading"],
              ),
            ]),
            l(
              d(_),
              {
                data: b.value,
                stripe: !0,
                border: !0,
                style: { width: "100%" },
                class: "mt-10px",
                "max-height": "500px",
              },
              {
                default: i(() => [
                  l(d(m), {
                    prop: "id",
                    label: "用户编号",
                    width: "100",
                    align: "center",
                  }),
                  l(d(m), {
                    prop: "name",
                    label: "姓名",
                    width: "120",
                    align: "center",
                  }),
                  l(d(m), {
                    prop: "email",
                    label: "邮箱",
                    width: "200",
                    align: "center",
                  }),
                  l(
                    d(m),
                    {
                      prop: "reset_password_status",
                      label: "重置状态",
                      width: "100",
                      align: "center",
                    },
                    {
                      default: i((e) => [
                        !0 === e.row.reset_password_status
                          ? (s(),
                            p(
                              d(w),
                              { key: 0, type: "success", effect: "dark" },
                              { default: i(() => [n(" 重置成功 ")]), _: 1 },
                            ))
                          : !1 === e.row.reset_password_status
                            ? (s(),
                              p(
                                d(w),
                                { key: 1, type: "danger", effect: "dark" },
                                { default: i(() => [n(" 重置失败 ")]), _: 1 },
                              ))
                            : (s(),
                              p(
                                d(w),
                                { key: 2, type: "warning", effect: "dark" },
                                { default: i(() => [n(" 待重置 ")]), _: 1 },
                              )),
                      ]),
                      _: 1,
                    },
                  ),
                  l(
                    d(m),
                    {
                      prop: "send_sms_status",
                      label: "发送状态",
                      width: "100",
                      align: "center",
                    },
                    {
                      default: i((e) => [
                        !0 === e.row.send_sms_status
                          ? (s(),
                            p(
                              d(w),
                              { key: 0, type: "success", effect: "dark" },
                              { default: i(() => [n(" 发送成功 ")]), _: 1 },
                            ))
                          : !1 === e.row.send_sms_status
                            ? (s(),
                              p(
                                d(w),
                                { key: 1, type: "danger", effect: "dark" },
                                { default: i(() => [n(" 发送失败 ")]), _: 1 },
                              ))
                            : (s(),
                              p(
                                d(w),
                                { key: 2, type: "warning", effect: "dark" },
                                { default: i(() => [n(" 待发送 ")]), _: 1 },
                              )),
                      ]),
                      _: 1,
                    },
                  ),
                  l(d(m), {
                    prop: "send_sms_msg",
                    label: "描述",
                    align: "center",
                  }),
                  l(
                    d(m),
                    {
                      fixed: "right",
                      label: "操作",
                      width: "100",
                      align: "center",
                    },
                    {
                      default: i((e) => [
                        l(
                          d(y),
                          {
                            title: "确认移除吗?",
                            onConfirm: (a) => {
                              return (
                                (s = e.$index),
                                void b.value.splice(s, 1)
                              );
                              var s;
                            },
                          },
                          {
                            reference: i(() => [
                              !0 !== e.row.send_sms_status
                                ? (s(),
                                  p(
                                    d(o),
                                    {
                                      key: 0,
                                      link: "",
                                      type: "primary",
                                      size: "small",
                                    },
                                    { default: i(() => [n("移除")]), _: 1 },
                                  ))
                                : u("", !0),
                            ]),
                            _: 2,
                          },
                          1032,
                          ["onConfirm"],
                        ),
                      ]),
                      _: 1,
                    },
                  ),
                ]),
                _: 1,
              },
              8,
              ["data"],
            ),
          ])
        );
      };
    },
  });
export { v as _ };
