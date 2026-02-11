import { u as e, F as o } from "./useForm-b6ceb895.js";
import { u as t } from "./useValidator-63200dcb.js";
import { g as l } from "./device-309e40d3.js";
import { u as n } from "./dict-2254259d.js";
import {
  e as a,
  r as s,
  a2 as p,
  k as c,
  L as r,
  w as i,
  o as m,
  l as d,
} from "./index-6b60d190.js";
const u = a({
  __name: "Bind",
  props: { currentRow: { type: Object, default: () => null } },
  setup(a, { expose: u }) {
    const y = a,
      { required: _, isTelephone: f, isEmail: v } = t(),
      w = s([]),
      b = s([]),
      h = s([]),
      P = s([]);
    p(async () => {
      await (async () => {
        const e = n(),
          o = await e.getDictObj([
            "connect_type",
            "connect_port",
            "connect_protocol",
          ]);
        ((w.value = o.connect_type),
          (b.value = o.connect_port),
          (h.value = o.connect_protocol));
      })();
    });
    const g = r([
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
            placeholder: "请输入设备MAC搜索",
            multiple: !1,
            clearable: !0,
            remote: !0,
            filterable: !0,
            options: P,
            remoteMethod: async (e) => {
              const o = {
                  keywords: e,
                  page: 1,
                  limit: 20,
                  device_type: "4g_io",
                },
                t = (await l(o)).data.map((e) => ({
                  label: `${e.ip} ${e.mac}`,
                  value: e.id,
                }));
              return ((P.value = t), t);
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
            options: w,
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
            options: h,
          },
          value: [],
        },
      ]),
      j = r({
        name: [_()],
        sn: [_()],
        port: [_()],
        device_id: [_()],
        connect_type: [_()],
        connect_protocol: [_()],
      }),
      { formRegister: R, formMethods: S } = e(),
      { setValues: x, getFormData: F, getElFormExpose: E } = S;
    return (
      i(
        () => y.currentRow,
        (e) => {
          e && x(e);
        },
        { deep: !0, immediate: !0 },
      ),
      u({
        submit: async () => {
          const e = await E();
          if (await (null == e ? void 0 : e.validate())) {
            return await F();
          }
        },
      }),
      (e, t) => (
        m(),
        d(c(o), { rules: j, onRegister: c(R), schema: g }, null, 8, [
          "rules",
          "onRegister",
          "schema",
        ])
      )
    );
  },
});
export { u as _ };
