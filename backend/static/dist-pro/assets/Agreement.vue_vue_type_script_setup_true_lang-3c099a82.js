import {
  e as a,
  ad as e,
  r as s,
  o as r,
  j as t,
  x as l,
  k as o,
  y as n,
  m as u,
  M as c,
  N as i,
  a1 as d,
  ac as m,
  dI as _,
  af as f,
} from "./index-6b60d190.js";
import { _ as y } from "./style.css_vue_type_style_index_0_src_true_lang-d8fdefc2.js";
const g = { class: "mt-10px", style: { float: "right" } },
  p = a({
    __name: "Agreement",
    props: { tabId: e.number },
    setup(a) {
      const e = a,
        p = s(),
        v = s(""),
        b = async () => {
          const a = await m({ tab_id: e.tabId });
          a && (v.value = a.data.web_agreement || "");
        },
        w = s(!1),
        k = async () => {
          w.value = !0;
          try {
            const a = s({});
            if (((a.value = await _({ web_agreement: v.value })), a.value))
              return (b(), f.success("更新成功"));
          } finally {
            w.value = !1;
          }
        },
        x = {
          customAlert: (a, e) => {
            switch (e) {
              case "success":
                f.success(a);
                break;
              case "info":
              default:
                f.info(a);
                break;
              case "warning":
                f.warning(a);
                break;
              case "error":
                f.error(a);
            }
          },
          autoFocus: !0,
          scroll: !0,
          readOnly: !1,
          uploadImgShowBase64: !0,
        };
      return (
        b(),
        (a, e) => (
          r(),
          t(
            d,
            null,
            [
              l(
                o(y),
                {
                  modelValue: v.value,
                  "onUpdate:modelValue": e[0] || (e[0] = (a) => (v.value = a)),
                  ref_key: "editorRef",
                  ref: p,
                  editorId: "web_agreement",
                  editorConfig: x,
                },
                null,
                8,
                ["modelValue"],
              ),
              n("div", g, [
                l(
                  o(i),
                  { loading: w.value, type: "primary", onClick: k },
                  { default: u(() => [c("立即保存")]), _: 1 },
                  8,
                  ["loading"],
                ),
              ]),
            ],
            64,
          )
        )
      );
    },
  });
export { p as _ };
