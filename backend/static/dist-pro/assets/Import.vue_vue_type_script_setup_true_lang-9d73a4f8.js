import {
  e,
  r as a,
  o as l,
  j as t,
  y as s,
  x as r,
  m as n,
  M as i,
  k as o,
  N as p,
  z as u,
  l as d,
  a1 as m,
  af as c,
} from "./index-6b60d190.js";
import { E as f } from "./el-link-28d2ea34.js";
import { E as _, a as b } from "./el-col-b8aa0d1a.js";
import { E as y, a as v } from "./el-table-column-0bcf5917.js";
import "./el-checkbox-4903f610.js";
import "./el-tooltip-4ed993c7.js";
import { E as g } from "./el-popper-09548d54.js";
/* empty css               */ import { E as h } from "./el-progress-31e0b945.js";
import { E as w } from "./el-popconfirm-cb976538.js";
/* empty css                   */ import {
  i as x,
  j as k,
} from "./client-84434f04.js";
const j = s("span", null, "导入步骤：", -1),
  E = { style: { "margin-top": "7px" } },
  z = s(
    "li",
    { style: { "margin-top": "7px" } },
    "编辑模板文件，（将需要导入的数据按格式填写进去）",
    -1,
  ),
  C = s(
    "li",
    { style: { "margin-top": "7px" } },
    "上传模板文件，点击确认导入",
    -1,
  ),
  L = s(
    "li",
    { style: { "margin-top": "7px" } },
    "查看导入结果，是否全部导入",
    -1,
  ),
  M = { class: "mt-10px" },
  X = { class: "flex justify-between mr-10px" },
  B = s("span", null, "导入结果", -1),
  F = { style: { color: "red" } },
  S = e({
    __name: "Import",
    emits: ["getList"],
    setup(e, { emit: S }) {
      const q = (e) => {
          const a = [
              "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            ].includes(e.type),
            l = e.size / 1024 / 1024 < 10;
          return (
            a || c.error("上传文件必须是 XLSX 格式!"),
            l || c.error("上传文件大小不能超过 10MB!"),
            a && l
          );
        },
        A = a(),
        D = a([]),
        I = a([]),
        K = async (e) => {
          ((D.value = []),
            D.value.push({
              filename: e.file.name,
              filesize: (e.file.size / 1024).toFixed(1) + "KB",
              status: "上传成功",
            }),
            (A.value = e.file));
        },
        N = () => {
          ((D.value = []), (A.value = null));
        },
        Q = a(!1),
        G = a(0),
        H = async () => {
          Q.value = !0;
          const e = new FormData();
          e.append("file", A.value);
          try {
            const a = await x(e);
            a &&
              (I.value.push({
                filename: A.value.name,
                success_number: a.data.success_number,
                error_number: a.data.error_number,
                error_url: a.data.error_url,
              }),
              (G.value += a.data.success_number),
              N(),
              S("getList"));
          } finally {
            Q.value = !1;
          }
        },
        J = async () => {
          c.info("正在下载请稍等！");
          const e = await k();
          if (e) {
            const a = document.createElement("a");
            ((a.style.display = "none"),
              (a.href = e.data.url),
              (a.target = "_blank"),
              (a.download = e.data.filename));
            const l = new MouseEvent("click");
            a.dispatchEvent(l);
          }
        };
      return (e, a) => (
        l(),
        t(
          m,
          null,
          [
            s("div", null, [
              j,
              s("ol", null, [
                s("li", E, [
                  r(
                    o(f),
                    { onClick: J, target: "_blank", type: "primary" },
                    { default: n(() => [i(" 下载最新批量导入模板 ")]), _: 1 },
                  ),
                ]),
                z,
                C,
                L,
              ]),
            ]),
            s("div", null, [
              r(
                o(b),
                { gutter: 10, class: "!mt-0 !mr-0" },
                {
                  default: n(() => [
                    r(
                      o(_),
                      { span: 1.5 },
                      {
                        default: n(() => [
                          s("div", null, [
                            r(
                              o(h),
                              {
                                action: "",
                                "http-request": K,
                                data: { path: "Clients" },
                                "show-file-list": !1,
                                "before-upload": q,
                                accept: ".xlsx",
                                disabled: D.value.length > 0,
                              },
                              {
                                default: n(() => [
                                  r(
                                    o(g),
                                    {
                                      effect: "dark",
                                      content: "只支持上传XLSX文件",
                                      placement: "top",
                                    },
                                    {
                                      default: n(() => [
                                        r(
                                          o(p),
                                          {
                                            type: "primary",
                                            size: "small",
                                            disabled: D.value.length > 0,
                                          },
                                          {
                                            default: n(() => [i("上传文件")]),
                                            _: 1,
                                          },
                                          8,
                                          ["disabled"],
                                        ),
                                      ]),
                                      _: 1,
                                    },
                                  ),
                                ]),
                                _: 1,
                              },
                              8,
                              ["disabled"],
                            ),
                          ]),
                        ]),
                        _: 1,
                      },
                    ),
                    r(
                      o(_),
                      { span: 1.5 },
                      {
                        default: n(() => [
                          r(
                            o(p),
                            {
                              type: "primary",
                              size: "small",
                              disabled: 0 === D.value.length,
                              loading: Q.value,
                              onClick: H,
                            },
                            { default: n(() => [i("确认导入")]), _: 1 },
                            8,
                            ["disabled", "loading"],
                          ),
                        ]),
                        _: 1,
                      },
                    ),
                  ]),
                  _: 1,
                },
              ),
              r(
                o(v),
                {
                  data: D.value,
                  border: !0,
                  style: { width: "100%" },
                  class: "mt-10px",
                },
                {
                  default: n(() => [
                    r(o(y), {
                      prop: "filename",
                      label: "文件名称",
                      align: "left",
                    }),
                    r(o(y), {
                      prop: "filesize",
                      label: "文件大小",
                      width: "100",
                      align: "center",
                    }),
                    r(o(y), {
                      prop: "status",
                      label: "上传状态",
                      width: "100",
                      align: "center",
                    }),
                    r(
                      o(y),
                      {
                        fixed: "right",
                        label: "操作",
                        width: "130",
                        align: "center",
                      },
                      {
                        default: n(() => [
                          r(
                            o(w),
                            { title: "确认删除吗?", onConfirm: N },
                            {
                              reference: n(() => [
                                r(
                                  o(p),
                                  { link: "", type: "primary", size: "small" },
                                  { default: n(() => [i("删除")]), _: 1 },
                                ),
                              ]),
                              _: 1,
                            },
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
            ]),
            s("div", M, [
              s("div", X, [
                B,
                s("span", null, "成功导入总数：" + u(G.value), 1),
              ]),
              r(
                o(v),
                {
                  data: I.value,
                  border: !0,
                  style: { width: "100%" },
                  class: "mt-10px",
                },
                {
                  default: n(() => [
                    r(o(y), {
                      prop: "filename",
                      label: "文件名称",
                      align: "left",
                    }),
                    r(o(y), {
                      prop: "success_number",
                      label: "成功数量",
                      width: "100",
                      align: "center",
                    }),
                    r(
                      o(y),
                      {
                        prop: "error_number",
                        label: "失败数量",
                        width: "100",
                        align: "center",
                      },
                      {
                        default: n((e) => [
                          s("span", F, u(e.row.error_number), 1),
                        ]),
                        _: 1,
                      },
                    ),
                    r(
                      o(y),
                      {
                        fixed: "right",
                        label: "操作",
                        width: "130",
                        align: "center",
                      },
                      {
                        default: n((e) => [
                          e.row.error_number > 0
                            ? (l(),
                              d(
                                o(f),
                                {
                                  key: 0,
                                  onClick: (a) =>
                                    (async (e) => {
                                      c.info("正在下载请稍等！");
                                      const a = document.createElement("a");
                                      ((a.style.display = "none"),
                                        (a.href = e.error_url),
                                        (a.target = "_blank"),
                                        (a.download = e.filename));
                                      const l = new MouseEvent("click");
                                      a.dispatchEvent(l);
                                    })(e.row),
                                  target: "_blank",
                                  type: "primary",
                                },
                                { default: n(() => [i("下载失败数据")]), _: 2 },
                                1032,
                                ["onClick"],
                              ))
                            : (l(),
                              d(
                                o(f),
                                { key: 1, type: "success", underline: !1 },
                                { default: n(() => [i("成功全部导入")]), _: 1 },
                              )),
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
            ]),
          ],
          64,
        )
      );
    },
  });
export { S as _ };
