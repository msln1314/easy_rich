import { u as e, F as o } from "./useForm-b6ceb895.js";
import { u as t } from "./useValidator-63200dcb.js";
import { g as s } from "./device-309e40d3.js";
import { u as l } from "./dict-2254259d.js";
import {
  e as p,
  r as i,
  a2 as r,
  k as a,
  L as n,
  w as c,
  o as m,
  l as d,
} from "./index-6b60d190.js";
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
import "./dict-593a5a5e.js";
const u = p({
  __name: "Bind",
  props: { currentRow: { type: Object, default: () => null } },
  setup(p, { expose: u }) {
    const j = p,
      { required: y, isTelephone: _, isEmail: v } = t(),
      f = i([]),
      b = i([]),
      w = i([]),
      g = i([]);
    r(async () => {
      await (async () => {
        const e = l(),
          o = await e.getDictObj([
            "connect_type",
            "connect_port",
            "connect_protocol",
          ]);
        ((f.value = o.connect_type),
          (b.value = o.connect_port),
          (w.value = o.connect_protocol));
      })();
    });
    const h = n([
        {
          field: "name",
          label: "名称",
          colProps: { span: 24 },
          component: "Input",
          componentProps: {
            style: { width: "100%" },
            placeholder: "请输入名称",
            readonly: !0,
            disabled: !0,
          },
        },
        {
          field: "sn",
          label: "桩号",
          colProps: { span: 24 },
          component: "Input",
          componentProps: {
            style: { width: "100%" },
            readonly: !0,
            disabled: !0,
          },
        },
        {
          field: "device_id",
          label: "设备",
          colProps: { span: 16 },
          component: "SelectV2",
          componentProps: {
            style: { width: "100%" },
            multiple: !1,
            clearable: !0,
            remote: !0,
            filterable: !0,
            options: g,
            remoteMethod: async (e) => {
              const o = {
                  keywords: e,
                  page: 1,
                  limit: 20,
                  device_type: "4g_io",
                },
                t = (await s(o)).data.map((e) => ({
                  label: `${e.ip} ${e.mac}`,
                  value: e.id,
                }));
              return ((g.value = t), t);
            },
            props: { label: "ip", value: "id" },
          },
          value: [],
        },
        {
          field: "port",
          label: "连接端口",
          colProps: { span: 8 },
          component: "Select",
          componentProps: {
            style: { width: "100%" },
            multiple: !1,
            options: b,
          },
          value: [],
        },
        {
          field: "connect_type",
          label: "连接类型",
          colProps: { span: 12 },
          component: "Select",
          componentProps: {
            style: { width: "100%" },
            multiple: !1,
            options: f,
          },
          value: [],
        },
        {
          field: "connect_protocol",
          label: "连接协议",
          colProps: { span: 12 },
          component: "Select",
          componentProps: {
            style: { width: "100%" },
            multiple: !1,
            options: w,
          },
          value: [],
        },
      ]),
      P = n({ name: [y()], sn: [y()] }),
      { formRegister: x, formMethods: R } = e(),
      { setValues: k, getFormData: E, getElFormExpose: F } = R;
    return (
      c(
        () => j.currentRow,
        (e) => {
          e && k(e);
        },
        { deep: !0, immediate: !0 },
      ),
      u({
        submit: async () => {
          const e = await F();
          if (await (null == e ? void 0 : e.validate())) {
            return await E();
          }
        },
      }),
      (e, t) => (
        m(),
        d(a(o), { rules: P, onRegister: a(x), schema: h }, null, 8, [
          "rules",
          "onRegister",
          "schema",
        ])
      )
    );
  },
});
export { u as default };
