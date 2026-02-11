import {
  e,
  r as t,
  o as a,
  l as s,
  m as i,
  x as r,
  k as l,
  j as o,
  a1 as _,
  a5 as p,
  F as m,
  dH as u,
} from "./index-6b60d190.js";
import { E as n, a as d } from "./el-tab-pane-1bfe2fef.js";
import { _ as j } from "./Basic.vue_vue_type_style_index_0_lang-17805e59.js";
import { _ as b } from "./Privacy.vue_vue_type_script_setup_true_lang-3aaa7a8a.js";
import { _ as c } from "./Agreement.vue_vue_type_script_setup_true_lang-3c099a82.js";
import { _ as v } from "./WechatServer.vue_vue_type_script_setup_true_lang-d11dfe5e.js";
import { _ as y } from "./Email.vue_vue_type_script_setup_true_lang-1f72cfb9.js";
import { _ as g } from "./SMS.vue_vue_type_script_setup_true_lang-b0f159f8.js";
import { _ as f } from "./ContentWrap.vue_vue_type_script_setup_true_lang-067de0d9.js";
import "./strings-00317668.js";
import "./event-5568c9d8.js";
import "./vnode-34f6d346.js";
import "./useForm-b6ceb895.js";
import "./el-form-item-ce18addb.js";
import "./el-col-b8aa0d1a.js";
import "./el-tooltip-4ed993c7.js";
import "./el-popper-09548d54.js";
import "./isNil-1f22f7b0.js";
import "./focus-trap-275966d8.js";
import "./el-input-38d674e5.js";
/* empty css               */ import "./el-checkbox-4903f610.js";
import "./isEqual-b8d86c27.js";
/* empty css                          */ import "./el-date-picker-91f17f23.js";
import "./debounce-5c500a3d.js";
import "./index-fdfa028a.js";
import "./el-radio-group-0c46635e.js";
import "./el-select-8805ff65.js";
import "./index-b7c1540b.js";
import "./scroll-6dba6951.js";
import "./validator-f032316f.js";
import "./el-switch-5507f2ea.js";
import "./el-divider-2dd0a1ee.js";
import "./el-tree-84af12f2.js";
import "./index-55fef7b1.js";
import "./el-progress-31e0b945.js";
import "./style.css_vue_type_style_index_0_src_true_lang-d8fdefc2.js";
import "./useValidator-63200dcb.js";
import "./el-card-37d6f3c4.js";
const k = e({
  name: "SystemSettings",
  __name: "Settings",
  setup(e) {
    const k = t("web_basic"),
      x = t([]);
    return (
      (async () => {
        const e = await u(["web", "aliyun"]);
        e && (x.value = e.data);
      })(),
      (e, t) => (
        a(),
        s(l(f), null, {
          default: i(() => [
            r(
              l(n),
              {
                modelValue: k.value,
                "onUpdate:modelValue": t[0] || (t[0] = (e) => (k.value = e)),
              },
              {
                default: i(() => [
                  (a(!0),
                  o(
                    _,
                    null,
                    p(
                      x.value,
                      (e) => (
                        a(),
                        o(
                          _,
                          { key: e.id },
                          [
                            e.hidden
                              ? m("", !0)
                              : (a(),
                                s(
                                  l(d),
                                  {
                                    key: 0,
                                    name: e.tab_name,
                                    label: e.tab_label,
                                  },
                                  {
                                    default: i(() => [
                                      "web_basic" === e.tab_name
                                        ? (a(),
                                          s(
                                            j,
                                            { key: 0, "tab-id": e.id },
                                            null,
                                            8,
                                            ["tab-id"],
                                          ))
                                        : "web_privacy" === e.tab_name
                                          ? (a(),
                                            s(
                                              b,
                                              { key: 1, "tab-id": e.id },
                                              null,
                                              8,
                                              ["tab-id"],
                                            ))
                                          : "web_agreement" === e.tab_name
                                            ? (a(),
                                              s(
                                                c,
                                                { key: 2, "tab-id": e.id },
                                                null,
                                                8,
                                                ["tab-id"],
                                              ))
                                            : "wx_server" === e.tab_name
                                              ? (a(),
                                                s(
                                                  v,
                                                  { key: 3, "tab-id": e.id },
                                                  null,
                                                  8,
                                                  ["tab-id"],
                                                ))
                                              : "web_email" === e.tab_name
                                                ? (a(),
                                                  s(
                                                    y,
                                                    { key: 4, "tab-id": e.id },
                                                    null,
                                                    8,
                                                    ["tab-id"],
                                                  ))
                                                : "aliyun_sms" === e.tab_name
                                                  ? (a(),
                                                    s(
                                                      g,
                                                      {
                                                        key: 5,
                                                        "tab-id": e.id,
                                                      },
                                                      null,
                                                      8,
                                                      ["tab-id"],
                                                    ))
                                                  : m("", !0),
                                    ]),
                                    _: 2,
                                  },
                                  1032,
                                  ["name", "label"],
                                )),
                          ],
                          64,
                        )
                      ),
                    ),
                    128,
                  )),
                ]),
                _: 1,
              },
              8,
              ["modelValue"],
            ),
          ]),
          _: 1,
        })
      )
    );
  },
});
export { k as default };
