import {
  g as e,
  p as t,
  a as l,
  b as a,
  d as o,
  c as i,
  e as s,
  f as n,
  h as r,
} from "./client-84434f04.js";
import { g as u } from "./client_group-caf4c37c.js";
import { u as p, _ as c } from "./Table.vue_vue_type_script_lang-230d9abb.js";
import {
  e as d,
  I as m,
  r as v,
  a2 as _,
  aj as f,
  L as w,
  x as y,
  k as b,
  a1 as h,
  M as j,
  a0 as g,
  Z as x,
  N as k,
  af as C,
  o as P,
  j as z,
  m as S,
  ai as T,
  l as I,
  ak as O,
  z as W,
  F as R,
} from "./index-6b60d190.js";
import { E as A } from "./el-switch-5507f2ea.js";
import { a as D, E } from "./el-col-b8aa0d1a.js";
import { E as L } from "./el-message-box-2d28828b.js";
import "./el-input-38d674e5.js";
import "./el-overlay-2c5c0104.js";
import { E as V } from "./el-divider-2dd0a1ee.js";
import { _ as U } from "./Search.vue_vue_type_script_setup_true_lang-9c85421f.js";
import { _ as M } from "./ContentWrap.vue_vue_type_script_setup_true_lang-067de0d9.js";
import { _ as F } from "./Write.vue_vue_type_script_setup_true_lang-4914ba58.js";
import { _ as G } from "./Dialog.vue_vue_type_style_index_0_lang-d732453c.js";
import { s as N } from "./dict-4a6e55e6.js";
import { u as q } from "./dict-2254259d.js";
import { _ as B } from "./Import.vue_vue_type_script_setup_true_lang-9d73a4f8.js";
import { _ as K } from "./Bind.vue_vue_type_script_setup_true_lang-14f1c160.js";
import { _ as Q } from "./DictTag.vue_vue_type_script_lang-5f3c338f.js";
import "./el-table-column-0bcf5917.js";
import "./el-popper-09548d54.js";
import "./isNil-1f22f7b0.js";
import "./focus-trap-275966d8.js";
import "./isEqual-b8d86c27.js";
import "./el-checkbox-4903f610.js";
import "./event-5568c9d8.js";
import "./debounce-5c500a3d.js";
import "./index-fdfa028a.js";
import "./el-tooltip-4ed993c7.js";
/* empty css               */ import "./el-pagination-491dd0e9.js";
import "./el-select-8805ff65.js";
import "./index-b7c1540b.js";
import "./strings-00317668.js";
import "./scroll-6dba6951.js";
import "./validator-f032316f.js";
import "./dropdown-84a04b2c.js";
import "./el-image-viewer-5060851c.js";
import "./useForm-b6ceb895.js";
import "./el-form-item-ce18addb.js";
/* empty css                          */ import "./el-date-picker-91f17f23.js";
import "./el-radio-group-0c46635e.js";
import "./el-tree-84af12f2.js";
import "./index-55fef7b1.js";
import "./el-progress-31e0b945.js";
import "./style.css_vue_type_style_index_0_src_true_lang-d8fdefc2.js";
import "./el-dropdown-item-943c2eb7.js";
import "./refs-64421a9c.js";
/* empty css                   */ import "./_Uint8Array-f98e6540.js";
import "./index-62254dd8.js";
import "./vnode-34f6d346.js";
import "./useIcon-7641a992.js";
import "./el-card-37d6f3c4.js";
import "./useValidator-63200dcb.js";
import "./use-dialog-0e1ee265.js";
import "./dict-593a5a5e.js";
import "./el-link-28d2ea34.js";
import "./el-popconfirm-cb976538.js";
import "./device-309e40d3.js";
const Z = d({
  name: "IotClient",
  __name: "Client",
  setup(d) {
    const { t: Z } = m(),
      {
        tableRegister: H,
        tableState: J,
        tableMethods: X,
      } = p({
        fetchDataApi: async () => {
          const { pageSize: e, currentPage: t } = J,
            l = await a({ page: b(t), limit: b(e), ...b(ve) });
          return { list: l.data || [], total: l.count || 0 };
        },
        fetchDelApi: async (e) => 200 === (await o(e)).code,
        fetchExportApi: async (e) => {
          const { pageSize: t, currentPage: l } = J;
          return await i({ page: b(l), limit: b(t), ...b(ve) }, e);
        },
      }),
      { dataList: Y, loading: $, total: ee, pageSize: te, currentPage: le } = J,
      { getList: ae, delList: oe, getSelections: ie, exportQueryList: se } = X,
      ne = v([]),
      re = v([]),
      ue = v([]),
      pe = v([]),
      ce = v(null);
    (_(() => {
      ce.value = setInterval(ae, 5e4);
    }),
      f(() => {
        clearInterval(ce.value);
      }),
      _(async () => {
        await (async () => {
          const e = q(),
            t = await e.getDictObj([
              "client_type",
              "connect_type",
              "port_status",
            ]);
          ((ne.value = t.client_type),
            (re.value = t.connect_type),
            (ue.value = t.port_status));
          const l = await u();
          pe.value = l.data;
        })();
      }));
    const de = w([
        { field: "selection", type: "selection", show: !0, disabled: !0 },
        { field: "id", label: "编号", width: "100px", show: !1, disabled: !1 },
        {
          field: "sn",
          label: "桩编号",
          show: !0,
          align: "center",
          showOverflowTooltip: !1,
          minWidth: "220px",
          cellStyle: {
            "background-color": "#f5f7fa",
            color: "#f5f7fa",
            "font-size": "15px",
          },
        },
        {
          field: "name",
          label: "站名称",
          show: !0,
          resizable: !0,
          minWidth: "220px",
          showOverflowTooltip: !1,
        },
        {
          field: "client_type",
          label: "充电桩类型",
          show: !1,
          slots: {
            default: (e) => {
              const t = e.row;
              return y(h, null, [y("div", null, [N(b(ne), t.client_type)])]);
            },
          },
        },
        {
          field: "connect_type",
          label: "连接类型",
          show: !1,
          slots: {
            default: (e) => {
              const t = e.row;
              return y(h, null, [
                y(Q, { type: "connect_type", value: t.connect_type }, null),
              ]);
            },
          },
        },
        {
          field: "port_status",
          label: "端口状态",
          show: !0,
          showOverflowTooltip: !1,
          minWidth: "120px",
          slots: {
            default: (e) => {
              const t = e.row;
              return y(h, null, [
                y(Q, { type: "online_status", value: t.online_status }, null),
                y(V, { direction: "vertical" }, null),
                y(Q, { type: "port_status", value: t.port_status }, null),
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
        { field: "client_tag", label: "标签", show: !0 },
        {
          field: "port",
          label: "连接信息",
          resizable: !0,
          minWidth: "180px",
          showOverflowTooltip: !1,
          slots: {
            default: (e) => {
              var t, l;
              const a = e.row;
              return y(h, null, [
                y("div", { class: "text-truncate" }, [
                  a.connect_type,
                  a.connect_protocol,
                  (null == (t = a.device) ? void 0 : t.connect_time)
                    ? a.device.connect_time
                    : "",
                  y("br", null, null),
                  j(" 最近:"),
                  null == (l = a.device) ? void 0 : l.last_time,
                ]),
              ]);
            },
          },
          show: !0,
        },
        {
          field: "device",
          label: "设备",
          show: !0,
          resizable: !0,
          minWidth: "140px",
          showOverflowTooltip: !1,
          slots: {
            default: (e) => {
              var t, l;
              const a = e.row;
              return y(h, null, [
                y("div", null, [
                  a.port,
                  y("br", null, null),
                  j(" "),
                  null == (t = a.device) ? void 0 : t.ip,
                  y("br", null, null),
                  j(" "),
                  null == (l = a.device) ? void 0 : l.mac,
                ]),
              ]);
            },
          },
        },
        {
          field: "is_active",
          label: "是否可用",
          show: !1,
          slots: {
            default: (e) => {
              const t = e.row;
              return y(h, null, [
                y(Q, { type: "active_status", value: t.is_active }, null),
              ]);
            },
          },
        },
        {
          field: "bind_status",
          label: "绑定状态",
          show: !0,
          showOverflowTooltip: !1,
          resizable: !0,
          minWidth: "120px",
          slots: {
            default: (e) => {
              const t = e.row;
              return y(h, null, [
                y(Q, { type: "bind_status", value: t.bind_status }, null),
              ]);
            },
          },
        },
        { field: "bind_time", label: "绑定时间", show: !1, width: "190px" },
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
              const t = e.row,
                l = ["iot.Client.bind"];
              return y(h, null, [
                (1 == t.port_status || 0 == t.port_status) &&
                  g(
                    y(
                      A,
                      {
                        size: "default",
                        "active-value": 1,
                        "inactive-value": 0,
                        "active-text": "闭合",
                        "inactive-text": "断开",
                        "inline-prompt": !0,
                        onClick: async () => await Te(t),
                        modelValue: t.port_status,
                        "onUpdate:modelValue": (e) => (t.port_status = e),
                      },
                      null,
                    ),
                    [[x("hasPermi"), ["iot.Client.on_of"]]],
                  ),
                g(
                  y(
                    k,
                    {
                      type: "primary",
                      link: !0,
                      size: "small",
                      onClick: () => Pe(t),
                    },
                    { default: () => [j("编辑")] },
                  ),
                  [[x("hasPermi"), ["iot.Client.update"]]],
                ),
                0 == t.bind_status &&
                  g(
                    y(
                      k,
                      {
                        type: "success",
                        link: !0,
                        size: "small",
                        onClick: () => ze(t),
                      },
                      { default: () => [j("绑定")] },
                    ),
                    [[x("hasPermi"), l]],
                  ),
                1 == t.bind_status &&
                  g(
                    y(
                      k,
                      {
                        type: "danger",
                        link: !0,
                        size: "small",
                        onClick: () => Se(t),
                      },
                      { default: () => [j("解绑"), 1 == t.bind_status] },
                    ),
                    [[x("hasPermi"), l]],
                  ),
                g(
                  y(
                    k,
                    {
                      type: "danger",
                      loading: we.value,
                      link: !0,
                      size: "small",
                      onClick: () => ye(t),
                    },
                    { default: () => [j("删除")] },
                  ),
                  [[x("hasPermi"), ["iot.Client.delete"]]],
                ),
              ]);
            },
          },
        },
      ]),
      me = w([
        {
          field: "name",
          label: "桩编号|站名称",
          component: "Input",
          componentProps: { clearable: !1, style: { width: "214px" } },
        },
        {
          field: "keywords",
          label: "IP|MAC",
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
          field: "port_status",
          label: "端口状态",
          component: "Select",
          componentProps: {
            style: { width: "180px" },
            options: [
              { label: "闭合", value: 1 },
              { label: "断开", value: 0 },
              { label: "未使用", value: -1 },
            ],
          },
        },
        {
          field: "group_id",
          label: "分组",
          colProps: { span: 12 },
          component: "Select",
          componentProps: {
            style: { width: "100%" },
            nodeKey: "value",
            checkStrictly: !0,
            defaultExpandAll: !0,
            options: pe,
          },
        },
        {
          field: "bind_status",
          label: "绑定状态",
          component: "Select",
          componentProps: {
            style: { width: "180px" },
            options: [
              { label: "是", value: 1 },
              { label: "否", value: 0 },
            ],
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
      ve = v({}),
      _e = (e) => {
        ((le.value = 1), (ve.value = e), ae());
      },
      fe = () => {
        ((le.value = 1), (ve.value = {}), ae());
      },
      we = v(!1),
      ye = async (e) => {
        ((we.value = !0),
          e
            ? await oe(!0, [e.id]).finally(() => {
                we.value = !1;
              })
            : await oe(!0).finally(() => {
                we.value = !1;
              }));
      },
      be = v(!1),
      he = v(""),
      je = v(),
      ge = v(""),
      xe = v(),
      ke = v(),
      Ce = v(!1),
      Pe = async (t) => {
        const l = await e(t.id);
        l &&
          ((he.value = "编辑充电桩"),
          (ge.value = "edit"),
          (je.value = l.data),
          (be.value = !0));
      },
      ze = async (t) => {
        const l = await e(t.id);
        l &&
          ((he.value = "绑定充电桩"),
          (ge.value = "bind"),
          (je.value = l.data),
          (be.value = !0));
      },
      Se = async (e) => {
        try {
          (await L.confirm("确认要解绑" + e.sn + '"设备吗?'),
            C.success("执行中，请等待...."),
            await t({ id: e.id }),
            await ae(),
            C.success("解绑成功"));
        } catch {
          C.error("执行失败");
        }
      },
      Te = async (e) => {
        try {
          const t = 1 == e.port_status ? "闭合" : "断开";
          (await L.confirm('确认要"' + t + '""' + e.sn + '"设备吗?'),
            C.success("执行中，请等待...."),
            await l({ id: e.id, port_status: e.port_status }),
            await ae(),
            C.success(t + "执行成功"));
        } catch {
          (C.error("执行失败"), (e.port_status = 1 == e.port_status ? 0 : 1));
        }
      },
      Ie = () => {
        ((he.value = "新增充电桩"),
          (ge.value = "add"),
          (je.value = void 0),
          (be.value = !0));
      },
      Oe = () => {
        ((he.value = "批量导入充电桩"),
          (ge.value = "import"),
          (je.value = void 0),
          (be.value = !0));
      };
    v([]);
    const We = async () => {
      const e = "bind" === ge.value ? b(ke) : b(xe),
        t = await (null == e ? void 0 : e.submit());
      if (t) {
        Ce.value = !0;
        try {
          const e = v({});
          "add" === ge.value
            ? ((e.value = await s(t)),
              e.value && ((be.value = !1), await ae(), C.success("添加成功!")))
            : "edit" === ge.value
              ? ((e.value = await n(t)),
                e.value &&
                  ((be.value = !1), await ae(), C.success("编辑成功!")))
              : "bind" === ge.value &&
                ((e.value = await r(t)),
                e.value &&
                  ((be.value = !1), await ae(), C.success("绑定成功!")));
        } finally {
          Ce.value = !1;
        }
      }
    };
    return (e, t) => {
      const l = x("hasPermi");
      return (
        P(),
        z(
          h,
          null,
          [
            y(b(M), null, {
              default: S(() => [
                y(b(U), { schema: me, onReset: fe, onSearch: _e }, null, 8, [
                  "schema",
                ]),
                y(
                  b(c),
                  {
                    "current-page": b(le),
                    "onUpdate:currentPage":
                      t[2] || (t[2] = (e) => (T(le) ? (le.value = e) : null)),
                    "page-size": b(te),
                    "onUpdate:pageSize":
                      t[3] || (t[3] = (e) => (T(te) ? (te.value = e) : null)),
                    showAction: "",
                    columns: de,
                    "default-expand-all": "",
                    "node-key": "id",
                    data: b(Y),
                    loading: b($),
                    pagination: { total: b(ee) },
                    onRegister: b(H),
                    onRefresh: b(ae),
                  },
                  {
                    toolbar: S(() => [
                      y(
                        b(D),
                        { gutter: 10 },
                        {
                          default: S(() => [
                            g(
                              (P(),
                              I(
                                b(E),
                                { span: 1.5 },
                                {
                                  default: S(() => [
                                    y(
                                      b(k),
                                      { type: "primary", onClick: Ie },
                                      {
                                        default: S(() => [j("新增充电桩")]),
                                        _: 1,
                                      },
                                    ),
                                  ]),
                                  _: 1,
                                },
                              )),
                              [[l, ["iot.Client.create"]]],
                            ),
                            g(
                              (P(),
                              I(
                                b(E),
                                { span: 1.5 },
                                {
                                  default: S(() => [
                                    y(
                                      b(k),
                                      { onClick: Oe },
                                      {
                                        default: S(() => [j("批量导入充电桩")]),
                                        _: 1,
                                      },
                                    ),
                                  ]),
                                  _: 1,
                                },
                              )),
                              [[l, ["iot.Client.import"]]],
                            ),
                            g(
                              (P(),
                              I(
                                b(E),
                                { span: 1.5 },
                                {
                                  default: S(() => [
                                    y(
                                      b(k),
                                      {
                                        onClick:
                                          t[0] || (t[0] = (e) => b(se)()),
                                      },
                                      {
                                        default: S(() => [j("导出筛选充电桩")]),
                                        _: 1,
                                      },
                                    ),
                                  ]),
                                  _: 1,
                                },
                              )),
                              [[l, ["iot.Client.export"]]],
                            ),
                            g(
                              (P(),
                              I(
                                b(E),
                                { span: 1.5 },
                                {
                                  default: S(() => [
                                    y(
                                      b(k),
                                      {
                                        type: "danger",
                                        onClick:
                                          t[1] || (t[1] = (e) => ye(null)),
                                      },
                                      {
                                        default: S(() => [j("批量删除")]),
                                        _: 1,
                                      },
                                    ),
                                  ]),
                                  _: 1,
                                },
                              )),
                              [[l, ["iot.Client.delete"]]],
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
            y(
              b(G),
              {
                modelValue: be.value,
                "onUpdate:modelValue": t[5] || (t[5] = (e) => (be.value = e)),
                title: he.value,
                height: 600,
                width: 700,
              },
              O(
                {
                  default: S(() => [
                    "add" === ge.value || "edit" === ge.value
                      ? (P(),
                        I(
                          F,
                          {
                            key: 0,
                            ref_key: "writeRef",
                            ref: xe,
                            actionType: ge.value,
                            "current-row": je.value,
                          },
                          null,
                          8,
                          ["actionType", "current-row"],
                        ))
                      : "bind" === ge.value
                        ? (P(),
                          I(
                            K,
                            {
                              key: 1,
                              ref_key: "bindRef",
                              ref: ke,
                              "current-row": je.value,
                            },
                            null,
                            8,
                            ["current-row"],
                          ))
                        : "import" === ge.value
                          ? (P(),
                            I(B, { key: 2, onGetList: b(ae) }, null, 8, [
                              "onGetList",
                            ]))
                          : R("", !0),
                  ]),
                  _: 2,
                },
                [
                  "add" === ge.value ||
                  "edit" === ge.value ||
                  "bind" === ge.value
                    ? {
                        name: "footer",
                        fn: S(() => [
                          y(
                            b(k),
                            { type: "primary", loading: Ce.value, onClick: We },
                            {
                              default: S(() => [
                                j(W(b(Z)("exampleDemo.save")), 1),
                              ]),
                              _: 1,
                            },
                            8,
                            ["loading"],
                          ),
                          y(
                            b(k),
                            {
                              onClick: t[4] || (t[4] = (e) => (be.value = !1)),
                            },
                            {
                              default: S(() => [
                                j(W(b(Z)("dialogDemo.close")), 1),
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
export { Z as default };
