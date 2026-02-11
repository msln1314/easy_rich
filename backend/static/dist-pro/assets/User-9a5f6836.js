import {
  e,
  I as a,
  r as t,
  L as l,
  x as s,
  k as i,
  a1 as o,
  a0 as r,
  Z as u,
  N as n,
  M as p,
  dK as d,
  o as m,
  j as c,
  m as v,
  ai as _,
  l as f,
  ak as g,
  z as j,
  F as w,
  dL as y,
  dM as h,
  dN as b,
  af as x,
  dO as k,
  dP as P,
} from "./index-6b60d190.js";
import { u as L, _ as S } from "./Table.vue_vue_type_script_lang-230d9abb.js";
import { E as C } from "./el-switch-5507f2ea.js";
import { E as z, a as G } from "./el-col-b8aa0d1a.js";
import { _ as R } from "./Search.vue_vue_type_script_setup_true_lang-9c85421f.js";
import { _ as D } from "./ContentWrap.vue_vue_type_script_setup_true_lang-067de0d9.js";
import { _ as A } from "./Write.vue_vue_type_script_setup_true_lang-6cd2601b.js";
import { _ as I } from "./Dialog.vue_vue_type_style_index_0_lang-d732453c.js";
import { s as E } from "./dict-4a6e55e6.js";
import { u as N } from "./dict-2254259d.js";
import { _ as U } from "./Import.vue_vue_type_script_setup_true_lang-6fb0f8c0.js";
import { _ as M } from "./PasswordSendSMS.vue_vue_type_script_setup_true_lang-fc49e348.js";
import { _ as V } from "./PasswordSendEmail.vue_vue_type_script_setup_true_lang-bb0f067e.js";
import { _ as W } from "./PasswordReset.vue_vue_type_script_setup_true_lang-34a026a8.js";
import { _ as F } from "./DeptTree.vue_vue_type_script_setup_true_lang-e0c336cc.js";
import "./el-message-box-2d28828b.js";
import "./el-input-38d674e5.js";
import "./event-5568c9d8.js";
import "./isNil-1f22f7b0.js";
import "./el-overlay-2c5c0104.js";
import "./scroll-6dba6951.js";
import "./vnode-34f6d346.js";
import "./useForm-b6ceb895.js";
import "./el-form-item-ce18addb.js";
import "./el-tooltip-4ed993c7.js";
import "./el-popper-09548d54.js";
import "./focus-trap-275966d8.js";
/* empty css               */ import "./el-checkbox-4903f610.js";
import "./isEqual-b8d86c27.js";
/* empty css                          */ import "./el-date-picker-91f17f23.js";
import "./debounce-5c500a3d.js";
import "./index-fdfa028a.js";
import "./el-radio-group-0c46635e.js";
import "./el-select-8805ff65.js";
import "./index-b7c1540b.js";
import "./strings-00317668.js";
import "./validator-f032316f.js";
import "./el-divider-2dd0a1ee.js";
import "./el-tree-84af12f2.js";
import "./index-55fef7b1.js";
import "./el-progress-31e0b945.js";
import "./style.css_vue_type_style_index_0_src_true_lang-d8fdefc2.js";
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
import "./useValidator-63200dcb.js";
import "./role-af5fad9c.js";
import "./dept-7c279e0e.js";
import "./use-dialog-0e1ee265.js";
import "./dict-593a5a5e.js";
import "./el-link-28d2ea34.js";
import "./el-popconfirm-cb976538.js";
const O = e({
  name: "AuthUser",
  __name: "User",
  setup(e) {
    const { t: O } = a(),
      {
        tableRegister: T,
        tableState: Z,
        tableMethods: q,
      } = L({
        fetchDataApi: async () => {
          const { pageSize: e, currentPage: a } = Z,
            t = await y({ page: i(a), limit: i(e), ...i(se) });
          return { list: t.data || [], total: t.count || 0 };
        },
        fetchDelApi: async (e) => 200 === (await h(e)).code,
        fetchExportApi: async (e) => {
          const { pageSize: a, currentPage: t } = Z;
          return await b({ page: i(t), limit: i(a), ...i(se) }, e);
        },
      }),
      { dataList: K, loading: Q, total: B, pageSize: H, currentPage: J } = Z,
      { getList: X, delList: Y, getSelections: $, exportQueryList: ee } = q,
      ae = t([]);
    (async () => {
      const e = N(),
        a = await e.getDictObj(["sys_gender"]);
      ae.value = a.sys_vadmin_gender;
    })();
    const te = l([
        { field: "selection", type: "selection", show: !0, disabled: !0 },
        {
          field: "id",
          label: "用户编号",
          width: "100px",
          show: !1,
          disabled: !1,
        },
        { field: "name", label: "姓名", show: !0, disabled: !0 },
        { field: "nickname", label: "昵称", show: !0 },
        { field: "phone", label: "手机号", show: !0, disabled: !0 },
        { field: "email", label: "邮箱", show: !0, disabled: !0 },
        {
          field: "gender",
          label: "性别",
          show: !1,
          slots: {
            default: (e) => {
              const a = e.row;
              return s(o, null, [s("div", null, [E(i(ae), a.gender)])]);
            },
          },
        },
        {
          field: "roles",
          label: "角色",
          show: !0,
          slots: {
            default: (e) => {
              const a = e.row;
              return s(o, null, [
                s("div", { class: "text-truncate" }, [
                  a.roles.map((e) => e.name).join(),
                ]),
              ]);
            },
          },
        },
        {
          field: "dept",
          label: "部门",
          show: !0,
          slots: {
            default: (e) => {
              var a;
              const t = e.row;
              return s(o, null, [
                s("div", { class: "text-truncate" }, [
                  null == (a = t.dept) ? void 0 : a.name,
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
              const a = e.row;
              return s(o, null, [
                s(C, { value: a.is_active, disabled: !0 }, null),
              ]);
            },
          },
        },
        {
          field: "is_staff",
          label: "工作人员",
          show: !0,
          slots: {
            default: (e) => {
              const a = e.row;
              return s(o, null, [
                s(C, { value: a.is_staff, disabled: !0 }, null),
              ]);
            },
          },
        },
        {
          field: "is_admin",
          label: "管理人员",
          show: !0,
          slots: {
            default: (e) => {
              const a = e.row;
              return s(o, null, [
                s(C, { value: a.is_admin, disabled: !0 }, null),
              ]);
            },
          },
        },
        {
          field: "last_login",
          label: "最近登录时间",
          show: !0,
          width: "190px",
        },
        { field: "created_at", label: "创建时间", width: "190px", show: !1 },
        {
          field: "action",
          width: "150px",
          label: "操作",
          show: !0,
          slots: {
            default: (e) => {
              const a = e.row;
              return s(o, null, [
                r(
                  s(
                    n,
                    {
                      type: "primary",
                      link: !0,
                      size: "small",
                      onClick: () => _e(a),
                    },
                    { default: () => [p("编辑")] },
                  ),
                  [[u("hasPermi"), ["sys.user.update"]]],
                ),
                r(
                  s(
                    n,
                    {
                      type: "danger",
                      loading: re.value,
                      link: !0,
                      size: "small",
                      onClick: () => ue(a),
                    },
                    { default: () => [p("删除")] },
                  ),
                  [[u("hasPermi"), ["sys.user.delete"]]],
                ),
              ]);
            },
          },
        },
      ]),
      le = l([
        {
          field: "name",
          label: "姓名",
          component: "Input",
          componentProps: { clearable: !1, style: { width: "214px" } },
          formItemProps: { labelWidth: "47px" },
        },
        {
          field: "phone",
          label: "手机号",
          component: "Input",
          componentProps: { clearable: !1, style: { width: "214px" } },
        },
        {
          field: "is_active",
          label: "状态",
          component: "Select",
          componentProps: {
            style: { width: "214px" },
            options: [
              { label: "正常", value: !0 },
              { label: "停用", value: !1 },
            ],
          },
        },
        {
          field: "is_staff",
          label: "工作人员",
          component: "Select",
          componentProps: {
            style: { width: "214px" },
            options: [
              { label: "是", value: !0 },
              { label: "否", value: !1 },
            ],
          },
        },
      ]),
      se = t({}),
      ie = (e) => {
        ((J.value = 1), (se.value = e), X());
      },
      oe = () => {
        ((J.value = 1), (se.value = {}), X());
      },
      re = t(!1),
      ue = async (e) => {
        ((re.value = !0),
          e
            ? await Y(!0, [e.id]).finally(() => {
                re.value = !1;
              })
            : await Y(!0).finally(() => {
                re.value = !1;
              }));
      },
      ne = t(!1),
      pe = t(""),
      de = t(),
      me = t(""),
      ce = t(),
      ve = t(!1),
      _e = async (e) => {
        const a = await d(e.id);
        a &&
          ((pe.value = "编辑用户"),
          (a.data.role_ids = a.data.roles.map((e) => e.id)),
          (me.value = "edit"),
          (de.value = a.data),
          (ne.value = !0));
      },
      fe = () => {
        ((pe.value = "新增用户"),
          (me.value = "add"),
          (de.value = void 0),
          (ne.value = !0));
      },
      ge = () => {
        ((pe.value = "批量导入用户"),
          (me.value = "import"),
          (de.value = void 0),
          (ne.value = !0));
      },
      je = t([]),
      we = async () => {
        if (((je.value = await $()), !(je.value.length > 0)))
          return x.warning("请先选择数据");
        ((pe.value = "重置密码并发送短信"),
          (me.value = "sms"),
          (de.value = void 0),
          (ne.value = !0));
      },
      ye = async () => {
        if (((je.value = await $()), !(je.value.length > 0)))
          return x.warning("请先选择数据");
        ((pe.value = "重置密码并发送邮件"),
          (me.value = "email"),
          (de.value = void 0),
          (ne.value = !0));
      },
      he = async () => {
        if (((je.value = await $()), !(je.value.length > 0)))
          return x.warning("请先选择数据");
        ((pe.value = "重置密码"),
          (me.value = "reset_password"),
          (de.value = void 0),
          (ne.value = !0));
      },
      be = async (e) => {
        ((se.value.dept_id = e.value), await X());
      },
      xe = async () => {
        const e = i(ce),
          a = await (null == e ? void 0 : e.submit());
        if (a) {
          ve.value = !0;
          try {
            const e = t({});
            "add" === me.value
              ? ((e.value = await k(a)),
                e.value && ((ne.value = !1), await X(), x.success("添加成功!")))
              : "edit" === me.value &&
                ((e.value = await P(a)),
                e.value &&
                  ((ne.value = !1), await X(), x.success("编辑成功!")));
          } finally {
            ve.value = !1;
          }
        }
      };
    return (e, a) => {
      const t = u("hasPermi");
      return (
        m(),
        c(
          o,
          null,
          [
            s(
              i(G),
              { gutter: 20 },
              {
                default: v(() => [
                  s(
                    i(z),
                    { span: 4, xs: 24 },
                    {
                      default: v(() => [
                        s(
                          i(D),
                          { class: "h-1/1 -mr-15px" },
                          {
                            default: v(() => [s(F, { onNodeClick: be })]),
                            _: 1,
                          },
                        ),
                      ]),
                      _: 1,
                    },
                  ),
                  s(
                    i(z),
                    { span: 20, xs: 24 },
                    {
                      default: v(() => [
                        s(i(D), null, {
                          default: v(() => [
                            s(
                              i(R),
                              { schema: le, onReset: oe, onSearch: ie },
                              null,
                              8,
                              ["schema"],
                            ),
                            s(
                              i(S),
                              {
                                "current-page": i(J),
                                "onUpdate:currentPage":
                                  a[2] ||
                                  (a[2] = (e) => (_(J) ? (J.value = e) : null)),
                                "page-size": i(H),
                                "onUpdate:pageSize":
                                  a[3] ||
                                  (a[3] = (e) => (_(H) ? (H.value = e) : null)),
                                showAction: "",
                                columns: te,
                                "default-expand-all": "",
                                "node-key": "id",
                                data: i(K),
                                loading: i(Q),
                                pagination: { total: i(B) },
                                onRegister: i(T),
                                onRefresh: i(X),
                              },
                              {
                                toolbar: v(() => [
                                  s(
                                    i(G),
                                    { gutter: 10 },
                                    {
                                      default: v(() => [
                                        r(
                                          (m(),
                                          f(
                                            i(z),
                                            { span: 1.5 },
                                            {
                                              default: v(() => [
                                                s(
                                                  i(n),
                                                  {
                                                    type: "primary",
                                                    onClick: fe,
                                                  },
                                                  {
                                                    default: v(() => [
                                                      p("新增用户"),
                                                    ]),
                                                    _: 1,
                                                  },
                                                ),
                                              ]),
                                              _: 1,
                                            },
                                          )),
                                          [[t, ["sys.user.create"]]],
                                        ),
                                        r(
                                          (m(),
                                          f(
                                            i(z),
                                            { span: 1.5 },
                                            {
                                              default: v(() => [
                                                s(
                                                  i(n),
                                                  { onClick: ge },
                                                  {
                                                    default: v(() => [
                                                      p("批量导入用户"),
                                                    ]),
                                                    _: 1,
                                                  },
                                                ),
                                              ]),
                                              _: 1,
                                            },
                                          )),
                                          [[t, ["sys.user.import"]]],
                                        ),
                                        r(
                                          (m(),
                                          f(
                                            i(z),
                                            { span: 1.5 },
                                            {
                                              default: v(() => [
                                                s(
                                                  i(n),
                                                  {
                                                    onClick:
                                                      a[0] ||
                                                      (a[0] = (e) => i(ee)()),
                                                  },
                                                  {
                                                    default: v(() => [
                                                      p("导出筛选用户"),
                                                    ]),
                                                    _: 1,
                                                  },
                                                ),
                                              ]),
                                              _: 1,
                                            },
                                          )),
                                          [[t, ["sys.user.export"]]],
                                        ),
                                        r(
                                          (m(),
                                          f(
                                            i(z),
                                            { span: 1.5 },
                                            {
                                              default: v(() => [
                                                s(
                                                  i(n),
                                                  { onClick: we },
                                                  {
                                                    default: v(() => [
                                                      p("重置密码通知短信"),
                                                    ]),
                                                    _: 1,
                                                  },
                                                ),
                                              ]),
                                              _: 1,
                                            },
                                          )),
                                          [[t, ["sys.user.reset"]]],
                                        ),
                                        r(
                                          (m(),
                                          f(
                                            i(z),
                                            { span: 1.5 },
                                            {
                                              default: v(() => [
                                                s(
                                                  i(n),
                                                  { onClick: ye },
                                                  {
                                                    default: v(() => [
                                                      p("重置密码通知邮件"),
                                                    ]),
                                                    _: 1,
                                                  },
                                                ),
                                              ]),
                                              _: 1,
                                            },
                                          )),
                                          [[t, ["sys.user.reset"]]],
                                        ),
                                        r(
                                          (m(),
                                          f(
                                            i(z),
                                            { span: 1.5 },
                                            {
                                              default: v(() => [
                                                s(
                                                  i(n),
                                                  { onClick: he },
                                                  {
                                                    default: v(() => [
                                                      p("重置密码"),
                                                    ]),
                                                    _: 1,
                                                  },
                                                ),
                                              ]),
                                              _: 1,
                                            },
                                          )),
                                          [[t, ["sys.user.reset"]]],
                                        ),
                                        r(
                                          (m(),
                                          f(
                                            i(z),
                                            { span: 1.5 },
                                            {
                                              default: v(() => [
                                                s(
                                                  i(n),
                                                  {
                                                    type: "danger",
                                                    onClick:
                                                      a[1] ||
                                                      (a[1] = (e) => ue(null)),
                                                  },
                                                  {
                                                    default: v(() => [
                                                      p("批量删除"),
                                                    ]),
                                                    _: 1,
                                                  },
                                                ),
                                              ]),
                                              _: 1,
                                            },
                                          )),
                                          [[t, ["sys.user.delete"]]],
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
                      ]),
                      _: 1,
                    },
                  ),
                ]),
                _: 1,
              },
            ),
            s(
              i(I),
              {
                modelValue: ne.value,
                "onUpdate:modelValue": a[5] || (a[5] = (e) => (ne.value = e)),
                title: pe.value,
                height: 600,
                width:
                  "sms" === me.value || "email" === me.value
                    ? "1000px"
                    : "700px",
              },
              g(
                {
                  default: v(() => [
                    "add" === me.value || "edit" === me.value
                      ? (m(),
                        f(
                          A,
                          {
                            key: 0,
                            ref_key: "writeRef",
                            ref: ce,
                            "current-row": de.value,
                          },
                          null,
                          8,
                          ["current-row"],
                        ))
                      : "import" === me.value
                        ? (m(),
                          f(U, { key: 1, onGetList: i(X) }, null, 8, [
                            "onGetList",
                          ]))
                        : "sms" === me.value
                          ? (m(),
                            f(
                              M,
                              { key: 2, selections: je.value, onGetList: i(X) },
                              null,
                              8,
                              ["selections", "onGetList"],
                            ))
                          : "email" === me.value
                            ? (m(),
                              f(
                                V,
                                {
                                  key: 3,
                                  selections: je.value,
                                  onGetList: i(X),
                                },
                                null,
                                8,
                                ["selections", "onGetList"],
                              ))
                            : "reset_password" === me.value
                              ? (m(),
                                f(
                                  W,
                                  {
                                    key: 4,
                                    selections: je.value,
                                    onGetList: i(X),
                                  },
                                  null,
                                  8,
                                  ["selections", "onGetList"],
                                ))
                              : w("", !0),
                  ]),
                  _: 2,
                },
                [
                  "add" === me.value || "edit" === me.value
                    ? {
                        name: "footer",
                        fn: v(() => [
                          s(
                            i(n),
                            { type: "primary", loading: ve.value, onClick: xe },
                            {
                              default: v(() => [
                                p(j(i(O)("exampleDemo.save")), 1),
                              ]),
                              _: 1,
                            },
                            8,
                            ["loading"],
                          ),
                          s(
                            i(n),
                            {
                              onClick: a[4] || (a[4] = (e) => (ne.value = !1)),
                            },
                            {
                              default: v(() => [
                                p(j(i(O)("dialogDemo.close")), 1),
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
              ["modelValue", "title", "width"],
            ),
          ],
          64,
        )
      );
    };
  },
});
export { O as default };
