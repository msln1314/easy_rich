import { u as e, F as a } from "./useForm-b6ceb895.js";
import { u as l } from "./useValidator-63200dcb.js";
import {
  e as s,
  L as t,
  x as i,
  M as r,
  al as o,
  a1 as u,
  r as n,
  af as p,
  w as m,
  o as c,
  j as d,
  k as v,
  l as g,
  F as f,
} from "./index-6b60d190.js";
import { E as x } from "./el-progress-31e0b945.js";
import { E as w } from "./el-image-viewer-5060851c.js";
const h = s({
  __name: "Write",
  props: { currentRow: { type: Object, default: () => null } },
  setup(s, { expose: h }) {
    const b = s,
      { required: j } = l(),
      P = t([
        {
          field: "upload_method",
          label: "上传方式",
          colProps: { span: 24 },
          component: "RadioGroup",
          componentProps: {
            options: [
              { label: "同时上传", value: "1" },
              { label: "按顺序上传", value: "2" },
            ],
          },
          value: "1",
          formItemProps: { rules: [j()] },
        },
        {
          field: "images",
          label: "",
          colProps: { span: 24 },
          formItemProps: {
            rules: [j()],
            slots: {
              default: () =>
                i(u, null, [
                  i("div", { class: "flex justify-between w-[100%]" }, [
                    i("span", null, [r("图片资源")]),
                    i("span", null, [
                      r("最大数量限制："),
                      M.value.length,
                      r("/"),
                      I.value,
                    ]),
                  ]),
                  i(
                    x,
                    {
                      class: "resource-image-uploader",
                      action: "#",
                      "http-request": B,
                      "file-list": M.value,
                      "onUpdate:file-list": (e) => (M.value = e),
                      "show-file-list": !0,
                      multiple: !0,
                      "before-upload": V,
                      "on-success": q,
                      "on-preview": C,
                      "on-exceed": J,
                      accept: "image/jpeg,image/png",
                      name: "file",
                      "list-type": "picture-card",
                      limit: I.value,
                      drag: !0,
                      disabled: I.value <= M.value.length,
                    },
                    {
                      default: () => [
                        M.value.length < I.value
                          ? i(
                              "div",
                              { class: "resource-image-uploader-icon" },
                              [
                                i(
                                  o,
                                  { icon: "akar-icons:plus", size: 23 },
                                  null,
                                ),
                                i("span", { class: "text-[12px]" }, [
                                  r("点击或拖拽到这里"),
                                ]),
                                i("span", { class: "text-[12px]" }, [
                                  M.value.length,
                                  r("/"),
                                  I.value,
                                ]),
                              ],
                            )
                          : i(
                              "div",
                              { class: "resource-image-uploader-icon" },
                              [
                                i("span", { class: "text-[12px]" }, [
                                  r("已到最大限制"),
                                ]),
                                i("span", { class: "text-[12px]" }, [
                                  M.value.length,
                                  r("/"),
                                  I.value,
                                ]),
                              ],
                            ),
                      ],
                    },
                  ),
                ]),
            },
          },
        },
      ]),
      { formRegister: y, formMethods: R } = e(),
      { setValues: F, getFormData: E, getElFormExpose: _, setValue: k } = R,
      z = n(!1),
      G = n(0),
      I = n(50),
      M = n([]),
      V = (e) => {
        const a = ["image/jpeg", "image/gif", "image/png"].includes(e.type),
          l = e.size / 1024 / 1024 < 3;
        return (
          a || p.error("上传图片素材必须是 JPG/PNG/ 格式!"),
          l || p.error("上传图片素材大小不能超过 3MB!"),
          a && l
        );
      },
      q = (e, a, l) => {
        ((M.value = l), k("images", l));
      },
      B = (e) =>
        new Promise((a) => {
          a(e);
        }),
      C = (e) => {
        ((G.value = M.value.findIndex((a) => a.uid === e.uid)), (z.value = !0));
      },
      D = () => {
        z.value = !1;
      },
      J = () => {
        p.error("上传失败，超出图片最大数量限制!");
      };
    return (
      m(
        () => b.currentRow,
        (e) => {
          e && F(e);
        },
        { deep: !0, immediate: !0 },
      ),
      h({
        submit: async () => {
          const e = await _();
          if (await (null == e ? void 0 : e.validate())) {
            return await E();
          }
        },
      }),
      (e, l) => (
        c(),
        d(
          u,
          null,
          [
            i(v(a), { onRegister: v(y), schema: P }, null, 8, [
              "onRegister",
              "schema",
            ]),
            z.value
              ? (c(),
                g(
                  v(w),
                  {
                    key: 0,
                    "z-index": 9999,
                    onClose: D,
                    "url-list": M.value.map((e) => e.url),
                    "initial-index": G.value,
                  },
                  null,
                  8,
                  ["url-list", "initial-index"],
                ))
              : f("", !0),
          ],
          64,
        )
      )
    );
  },
});
export { h as _ };
