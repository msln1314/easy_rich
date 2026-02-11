import {
  e,
  r as s,
  o as a,
  j as t,
  y as r,
  x as l,
  m as n,
  M as i,
  k as d,
  N as o,
  l as p,
  F as u,
  af as f,
  dS as c,
} from "./index-6b60d190.js";
import { E as _, a as m } from "./el-table-column-0bcf5917.js";
import "./el-checkbox-4903f610.js";
import "./el-tooltip-4ed993c7.js";
import "./el-popper-09548d54.js";
/* empty css               */ import { E as y } from "./el-popconfirm-cb976538.js";
/* empty css                   */ import { E as w } from "./index-b7c1540b.js";
const g = { class: "flex justify-between" },
  k = r("span", null, "已选用户列表", -1),
  v = e({
    __name: "PasswordSendSMS",
    props: { selections: { type: Object } },
    setup(e) {
      const v = e,
        b = s(JSON.parse(JSON.stringify(v.selections))),
        h = s(!1),
        j = async () => {
          h.value = !0;
          const e = b.value
            .filter((e) => !0 !== e.reset_password_status)
            .map((e) => e.id);
          if (e.length <= 0) return f.warning("已全部重置完成，无需重复操作");
          try {
            const s = await c(e);
            s && ((b.value = s.data), f.success("重置成功"));
          } finally {
            h.value = !1;
          }
        };
      return (e, s) => {
        var f;
        return (
          a(),
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
                { default: n(() => [i("确认重置并发送短信通知")]), _: 1 },
                8,
                ["disabled", "loading"],
              ),
            ]),
            l(
              d(m),
              {
                data: b.value,
                stripe: !0,
                border: !0,
                style: { width: "100%" },
                class: "mt-10px",
                "max-height": "500px",
              },
              {
                default: n(() => [
                  l(d(_), {
                    prop: "id",
                    label: "用户编号",
                    width: "100",
                    align: "center",
                  }),
                  l(d(_), {
                    prop: "name",
                    label: "姓名",
                    width: "120",
                    align: "center",
                  }),
                  l(d(_), {
                    prop: "telephone",
                    label: "手机号",
                    width: "120",
                    align: "center",
                  }),
                  l(
                    d(_),
                    {
                      prop: "reset_password_status",
                      label: "重置状态",
                      width: "100",
                      align: "center",
                    },
                    {
                      default: n((e) => [
                        !0 === e.row.reset_password_status
                          ? (a(),
                            p(
                              d(w),
                              { key: 0, type: "success", effect: "dark" },
                              { default: n(() => [i(" 重置成功 ")]), _: 1 },
                            ))
                          : !1 === e.row.reset_password_status
                            ? (a(),
                              p(
                                d(w),
                                { key: 1, type: "danger", effect: "dark" },
                                { default: n(() => [i(" 重置失败 ")]), _: 1 },
                              ))
                            : (a(),
                              p(
                                d(w),
                                { key: 2, type: "warning", effect: "dark" },
                                { default: n(() => [i(" 待重置 ")]), _: 1 },
                              )),
                      ]),
                      _: 1,
                    },
                  ),
                  l(
                    d(_),
                    {
                      prop: "send_sms_status",
                      label: "发送状态",
                      width: "100",
                      align: "center",
                    },
                    {
                      default: n((e) => [
                        !0 === e.row.send_sms_status
                          ? (a(),
                            p(
                              d(w),
                              { key: 0, type: "success", effect: "dark" },
                              { default: n(() => [i(" 发送成功 ")]), _: 1 },
                            ))
                          : !1 === e.row.send_sms_status
                            ? (a(),
                              p(
                                d(w),
                                { key: 1, type: "danger", effect: "dark" },
                                { default: n(() => [i(" 发送失败 ")]), _: 1 },
                              ))
                            : (a(),
                              p(
                                d(w),
                                { key: 2, type: "warning", effect: "dark" },
                                { default: n(() => [i(" 待发送 ")]), _: 1 },
                              )),
                      ]),
                      _: 1,
                    },
                  ),
                  l(d(_), {
                    prop: "send_sms_msg",
                    label: "描述",
                    align: "center",
                  }),
                  l(
                    d(_),
                    {
                      fixed: "right",
                      label: "操作",
                      width: "100",
                      align: "center",
                    },
                    {
                      default: n((e) => [
                        l(
                          d(y),
                          {
                            title: "确认移除吗?",
                            onConfirm: (s) => {
                              return (
                                (a = e.$index),
                                void b.value.splice(a, 1)
                              );
                              var a;
                            },
                          },
                          {
                            reference: n(() => [
                              !0 !== e.row.send_sms_status
                                ? (a(),
                                  p(
                                    d(o),
                                    {
                                      key: 0,
                                      link: "",
                                      type: "primary",
                                      size: "small",
                                    },
                                    { default: n(() => [i("移除")]), _: 1 },
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
