import {
  a as e,
  b as t,
  d as a,
  p as l,
  c as i,
  e as o,
} from "./device-309e40d3.js";
import {
  _ as s,
  g as r,
} from "./Write.vue_vue_type_script_setup_true_lang-fa153819.js";
import { u as p, _ as n } from "./Table.vue_vue_type_script_lang-230d9abb.js";
import {
  e as u,
  I as d,
  r as c,
  a2 as m,
  aj as v,
  L as _,
  x as f,
  k as w,
  a1 as j,
  a0 as h,
  Z as g,
  N as y,
  M as b,
  o as x,
  j as k,
  m as P,
  ai as I,
  l as D,
  ak as C,
  z as S,
  F as z,
  af as A,
} from "./index-6b60d190.js";
import { a as L, E as R } from "./el-col-b8aa0d1a.js";
import { E as T } from "./el-divider-2dd0a1ee.js";
import { _ as W } from "./Search.vue_vue_type_script_setup_true_lang-9c85421f.js";
import { _ as O } from "./ContentWrap.vue_vue_type_script_setup_true_lang-067de0d9.js";
import { _ as E } from "./Dialog.vue_vue_type_style_index_0_lang-d732453c.js";
import { s as M } from "./dict-4a6e55e6.js";
import { u as U } from "./dict-2254259d.js";
import { _ as V } from "./Import.vue_vue_type_script_setup_true_lang-f068988c.js";
import { _ as q } from "./DictTag.vue_vue_type_script_lang-5f3c338f.js";
import "./useForm-b6ceb895.js";
import "./el-form-item-ce18addb.js";
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
import "./el-tree-84af12f2.js";
import "./index-55fef7b1.js";
import "./el-progress-31e0b945.js";
import "./style.css_vue_type_style_index_0_src_true_lang-d8fdefc2.js";
import "./useValidator-63200dcb.js";
import "./el-message-box-2d28828b.js";
import "./el-overlay-2c5c0104.js";
import "./vnode-34f6d346.js";
import "./index-62254dd8.js";
import "./el-table-column-0bcf5917.js";
import "./el-pagination-491dd0e9.js";
import "./dropdown-84a04b2c.js";
import "./el-image-viewer-5060851c.js";
import "./el-dropdown-item-943c2eb7.js";
import "./refs-64421a9c.js";
/* empty css                   */ import "./_Uint8Array-f98e6540.js";
import "./useIcon-7641a992.js";
import "./el-card-37d6f3c4.js";
import "./use-dialog-0e1ee265.js";
import "./dict-593a5a5e.js";
import "./el-link-28d2ea34.js";
import "./el-popconfirm-cb976538.js";
import "./client-84434f04.js";
const F = u({
  name: "IotDevice",
  __name: "Device",
  setup(u) {
    const { t: F } = d(),
      {
        tableRegister: G,
        tableState: N,
        tableMethods: K,
      } = p({
        fetchDataApi: async () => {
          const { pageSize: e, currentPage: a } = N,
            l = await t({ page: w(a), limit: w(e), ...w(re) });
          return { list: l.data || [], total: l.count || 0 };
        },
        fetchDelApi: async (e) => 200 === (await a(e)).code,
        fetchExportApi: async (e) => {
          const { pageSize: t, currentPage: a } = N;
          return await l({ page: w(a), limit: w(t), ...w(re) }, e);
        },
      }),
      { dataList: Q, loading: Z, total: B, pageSize: H, currentPage: J } = N,
      { getList: X, delList: Y, getSelections: $, exportQueryList: ee } = K,
      te = c([]),
      ae = c([]),
      le = c([]),
      ie = c(null);
    (m(() => {
      ie.value = setInterval(X, 5e4);
    }),
      v(() => {
        clearInterval(ie.value);
      }),
      m(async () => {
        await (async () => {
          const e = U(),
            t = await e.getDictObj([
              "Device_type",
              "device_tag",
              "port_status",
            ]);
          ((te.value = t.Device_type), (ae.value = t.connect_type));
          const a = await r();
          le.value = a.data;
        })();
      }));
    const oe = _([
        { field: "selection", type: "selection", show: !0, disabled: !0 },
        {
          field: "ip",
          label: "IP地址",
          width: "100px",
          show: !1,
          disabled: !1,
        },
        {
          field: "mac",
          label: "MAC地址",
          show: !0,
          align: "center",
          showOverflowTooltip: !1,
          minWidth: "220px",
        },
        {
          field: "Device_type",
          label: "客户端类型",
          show: !1,
          slots: {
            default: (e) => {
              const t = e.row;
              return f(j, null, [f("div", null, [M(w(te), t.device_type)])]);
            },
          },
        },
        {
          field: "device_tag",
          label: "设备标记",
          show: !1,
          slots: {
            default: (e) => {
              const t = e.row;
              return f(j, null, [
                f(q, { type: "device_tag", value: t.device_tag }, null),
              ]);
            },
          },
        },
        {
          field: "online_status",
          label: "在线状态",
          show: !0,
          showOverflowTooltip: !1,
          minWidth: "120px",
          slots: {
            default: (e) => {
              const t = e.row;
              return f(j, null, [
                f(q, { type: "online_status", value: t.online_status }, null),
                f(T, { direction: "vertical" }, null),
                t.last_time,
              ]);
            },
          },
        },
        {
          field: "address",
          label: "位置",
          show: !0,
          showOverflowTooltip: !1,
          disabled: !0,
        },
        { field: "area", label: "单位", show: !0, disabled: !0 },
        {
          field: "is_active",
          label: "是否可用",
          show: !1,
          slots: {
            default: (e) => {
              const t = e.row;
              return f(j, null, [
                f(q, { type: "active_status", value: t.is_active }, null),
              ]);
            },
          },
        },
        { field: "ccid", label: "ccid", width: "220px", show: !1 },
        { field: "phone", label: "phone", width: "100px", show: !0 },
        { field: "created_at", label: "创建时间", width: "190px", show: !1 },
        {
          field: "remark",
          label: "备注",
          width: "100px",
          show: !0,
          showOverflowTooltip: !1,
          resizable: !0,
        },
        {
          field: "action",
          width: "180px",
          label: "操作",
          showOverflowTooltip: !1,
          show: !0,
          slots: {
            default: (e) => {
              const t = e.row;
              return f(j, null, [
                h(
                  f(
                    y,
                    {
                      type: "primary",
                      link: !0,
                      size: "small",
                      onClick: () => je(t),
                    },
                    { default: () => [b("编辑")] },
                  ),
                  [[g("hasPermi"), ["iot.device.update"]]],
                ),
                h(
                  f(
                    y,
                    {
                      type: "danger",
                      loading: ue.value,
                      link: !0,
                      size: "small",
                      onClick: () => de(t),
                    },
                    { default: () => [b("删除")] },
                  ),
                  [[g("hasPermi"), ["iot.Device.delete"]]],
                ),
              ]);
            },
          },
        },
      ]),
      se = _([
        {
          field: "ip",
          label: "IP",
          component: "Input",
          componentProps: { clearable: !1, style: { width: "214px" } },
          formItemProps: { labelWidth: "80px" },
        },
        {
          field: "mac",
          label: "MAC",
          component: "Input",
          componentProps: { clearable: !1, style: { width: "214px" } },
          formItemProps: { labelWidth: "80px" },
        },
        {
          field: "ccid",
          label: "CCID",
          component: "Input",
          componentProps: { clearable: !1, style: { width: "214px" } },
          formItemProps: { labelWidth: "80px" },
        },
        {
          field: "is_active",
          label: "状态",
          component: "Select",
          componentProps: {
            style: { width: "180px" },
            options: [
              { label: "正常", value: !0 },
              { label: "停用", value: !1 },
            ],
          },
        },
        {
          field: "product_id",
          label: "产品",
          colProps: { span: 12 },
          component: "Select",
          componentProps: {
            style: { width: "100%" },
            nodeKey: "value",
            checkStrictly: !0,
            defaultExpandAll: !0,
            options: le,
          },
        },
        {
          field: "online_status",
          label: "在线状态",
          component: "Select",
          componentProps: {
            style: { width: "180px" },
            options: [
              { label: "在线", value: "1" },
              { label: "离线", value: "0" },
              { label: "空", value: "-1" },
            ],
          },
        },
      ]),
      re = c({}),
      pe = (e) => {
        ((J.value = 1), (re.value = e), X());
      },
      ne = () => {
        ((J.value = 1), (re.value = {}), X());
      },
      ue = c(!1),
      de = async (e) => {
        ((ue.value = !0),
          e
            ? await Y(!0, [e.id]).finally(() => {
                ue.value = !1;
              })
            : await Y(!0).finally(() => {
                ue.value = !1;
              }));
      },
      ce = c(!1),
      me = c(""),
      ve = c(),
      _e = c(""),
      fe = c();
    c();
    const we = c(!1),
      je = async (t) => {
        const a = await e(t.id);
        a &&
          ((me.value = "编辑设备"),
          (_e.value = "edit"),
          (ve.value = a.data),
          (ce.value = !0));
      },
      he = () => {
        ((me.value = "新增设备"),
          (_e.value = "add"),
          (ve.value = void 0),
          (ce.value = !0));
      },
      ge = () => {
        ((me.value = "批量导入设备"),
          (_e.value = "import"),
          (ve.value = void 0),
          (ce.value = !0));
      };
    c([]);
    const ye = async () => {
      const e = w(fe),
        t = await (null == e ? void 0 : e.submit());
      if (t) {
        we.value = !0;
        try {
          const e = c({});
          "add" === _e.value
            ? ((e.value = await i(t)),
              e.value && ((ce.value = !1), await X(), A.success("添加成功!")))
            : "edit" === _e.value &&
              ((e.value = await o(t)),
              e.value && ((ce.value = !1), await X(), A.success("编辑成功!")));
        } finally {
          we.value = !1;
        }
      }
    };
    return (e, t) => {
      const a = g("hasPermi");
      return (
        x(),
        k(
          j,
          null,
          [
            f(w(O), null, {
              default: P(() => [
                f(w(W), { schema: se, onReset: ne, onSearch: pe }, null, 8, [
                  "schema",
                ]),
                f(
                  w(n),
                  {
                    "current-page": w(J),
                    "onUpdate:currentPage":
                      t[2] || (t[2] = (e) => (I(J) ? (J.value = e) : null)),
                    "page-size": w(H),
                    "onUpdate:pageSize":
                      t[3] || (t[3] = (e) => (I(H) ? (H.value = e) : null)),
                    showAction: "",
                    columns: oe,
                    "default-expand-all": "",
                    "node-key": "id",
                    data: w(Q),
                    loading: w(Z),
                    pagination: { total: w(B) },
                    onRegister: w(G),
                    onRefresh: w(X),
                  },
                  {
                    toolbar: P(() => [
                      f(
                        w(L),
                        { gutter: 10 },
                        {
                          default: P(() => [
                            h(
                              (x(),
                              D(
                                w(R),
                                { span: 1.5 },
                                {
                                  default: P(() => [
                                    f(
                                      w(y),
                                      { type: "primary", onClick: he },
                                      {
                                        default: P(() => [b("新增设备")]),
                                        _: 1,
                                      },
                                    ),
                                  ]),
                                  _: 1,
                                },
                              )),
                              [[a, ["iot.device.create"]]],
                            ),
                            h(
                              (x(),
                              D(
                                w(R),
                                { span: 1.5 },
                                {
                                  default: P(() => [
                                    f(
                                      w(y),
                                      { onClick: ge },
                                      {
                                        default: P(() => [b("批量导入设备")]),
                                        _: 1,
                                      },
                                    ),
                                  ]),
                                  _: 1,
                                },
                              )),
                              [[a, ["iot.device.import"]]],
                            ),
                            h(
                              (x(),
                              D(
                                w(R),
                                { span: 1.5 },
                                {
                                  default: P(() => [
                                    f(
                                      w(y),
                                      {
                                        onClick:
                                          t[0] || (t[0] = (e) => w(ee)()),
                                      },
                                      {
                                        default: P(() => [b("导出筛选设备")]),
                                        _: 1,
                                      },
                                    ),
                                  ]),
                                  _: 1,
                                },
                              )),
                              [[a, ["iot.device.export"]]],
                            ),
                            h(
                              (x(),
                              D(
                                w(R),
                                { span: 1.5 },
                                {
                                  default: P(() => [
                                    f(
                                      w(y),
                                      {
                                        type: "danger",
                                        onClick:
                                          t[1] || (t[1] = (e) => de(null)),
                                      },
                                      {
                                        default: P(() => [b("批量删除")]),
                                        _: 1,
                                      },
                                    ),
                                  ]),
                                  _: 1,
                                },
                              )),
                              [[a, ["iot.device.delete"]]],
                            ),
                          ]),
                          _: 1,
                        },
                      ),
                    ]),
                    _: 1,
                  },
                  8,
                  [
                    "current-page",
                    "page-size",
                    "columns",
                    "data",
                    "loading",
                    "pagination",
                    "onRegister",
                    "onRefresh",
                  ],
                ),
              ]),
              _: 1,
            }),
            f(
              w(E),
              {
                modelValue: ce.value,
                "onUpdate:modelValue": t[5] || (t[5] = (e) => (ce.value = e)),
                title: me.value,
                height: 600,
                width: 700,
              },
              C(
                {
                  default: P(() => [
                    "add" === _e.value || "edit" === _e.value
                      ? (x(),
                        D(
                          s,
                          {
                            key: 0,
                            ref_key: "writeRef",
                            ref: fe,
                            "current-row": ve.value,
                          },
                          null,
                          8,
                          ["current-row"],
                        ))
                      : "import" === _e.value
                        ? (x(),
                          D(V, { key: 1, onGetList: w(X) }, null, 8, [
                            "onGetList",
                          ]))
                        : z("", !0),
                  ]),
                  _: 2,
                },
                [
                  "add" === _e.value ||
                  "edit" === _e.value ||
                  "bind" === _e.value
                    ? {
                        name: "footer",
                        fn: P(() => [
                          f(
                            w(y),
                            { type: "primary", loading: we.value, onClick: ye },
                            {
                              default: P(() => [
                                b(S(w(F)("exampleDemo.save")), 1),
                              ]),
                              _: 1,
                            },
                            8,
                            ["loading"],
                          ),
                          f(
                            w(y),
                            {
                              onClick: t[4] || (t[4] = (e) => (ce.value = !1)),
                            },
                            {
                              default: P(() => [
                                b(S(w(F)("dialogDemo.close")), 1),
                              ]),
                              _: 1,
                            },
                          ),
                        ]),
                        key: "0",
                      }
                    : void 0,
                ],
              ),
              1032,
              ["modelValue", "title"],
            ),
          ],
          64,
        )
      );
    };
  },
});
export { F as default };
