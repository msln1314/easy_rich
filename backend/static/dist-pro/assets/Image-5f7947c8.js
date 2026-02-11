import {
  U as e,
  e as a,
  I as t,
  L as l,
  x as i,
  a1 as s,
  N as o,
  M as r,
  r as n,
  dx as p,
  af as u,
  o as d,
  j as m,
  m as c,
  k as g,
  ai as _,
  z as f,
} from "./index-6b60d190.js";
import {
  u as v,
  E as j,
  _ as h,
} from "./Table.vue_vue_type_script_lang-230d9abb.js";
import { a as w, E as y } from "./el-col-b8aa0d1a.js";
import "./el-image-viewer-5060851c.js";
import { _ as x } from "./Search.vue_vue_type_script_setup_true_lang-9c85421f.js";
import { _ as b } from "./ContentWrap.vue_vue_type_script_setup_true_lang-067de0d9.js";
import { _ as k } from "./Write.vue_vue_type_style_index_0_lang-ab33ceeb.js";
import { _ as z } from "./Dialog.vue_vue_type_style_index_0_lang-d732453c.js";
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
import "./el-switch-5507f2ea.js";
import "./el-divider-2dd0a1ee.js";
import "./el-tree-84af12f2.js";
import "./index-55fef7b1.js";
import "./el-progress-31e0b945.js";
import "./style.css_vue_type_style_index_0_src_true_lang-d8fdefc2.js";
import "./index-62254dd8.js";
import "./el-table-column-0bcf5917.js";
import "./el-pagination-491dd0e9.js";
import "./dropdown-84a04b2c.js";
import "./el-dropdown-item-943c2eb7.js";
import "./refs-64421a9c.js";
/* empty css                   */ import "./_Uint8Array-f98e6540.js";
import "./useIcon-7641a992.js";
import "./el-card-37d6f3c4.js";
import "./useValidator-63200dcb.js";
import "./use-dialog-0e1ee265.js";
const C = (a) =>
    e.post({
      url: "/resource/images",
      headersType: "multipart/form-data",
      data: a,
    }),
  R = a({
    name: "ResourceImage",
    __name: "Image",
    setup(a) {
      const { t: R } = t(),
        {
          tableRegister: D,
          tableState: A,
          tableMethods: S,
        } = v({
          fetchDataApi: async () => {
            const { pageSize: a, currentPage: t } = A,
              l = await ((i = { page: g(t), limit: g(a), ...g(N) }),
              e.get({ url: "/resource/images", params: i }));
            var i;
            return { list: l.data || [], total: l.count || 0 };
          },
          fetchDelApi: async (a) => {
            var t;
            return (
              200 ===
              (await ((t = a), e.delete({ url: "/resource/images", data: t })))
                .code
            );
          },
        }),
        { dataList: I, loading: P, total: E, pageSize: L, currentPage: U } = A,
        { getList: F, delList: V } = S,
        W = l([
          { field: "selection", type: "selection", show: !0, disabled: !0 },
          {
            field: "id",
            label: "编号",
            show: !0,
            disabled: !1,
            align: "center",
            headerAlign: "center",
            width: "80px",
          },
          {
            field: "image_url",
            label: "图片",
            show: !0,
            disabled: !0,
            minWidth: "90px",
            slots: {
              default: (e) => {
                const a = e.row;
                return i(s, null, [
                  i("div", { class: "resource-image-name flex items-center" }, [
                    i("div", null, [
                      i(
                        j,
                        {
                          src: `${a.image_url}?x-oss-process=image/resize,m_fixed,h_100`,
                          "zoom-rate": 1.2,
                          "preview-src-list": I.value.map((e) => e.image_url),
                          "preview-teleported": !0,
                          "initial-index": e.$index,
                          style: "height: 60px; display: block",
                          fit: "cover",
                        },
                        null,
                      ),
                    ]),
                    i("div", { class: "leading-[35px] ml-2 truncate" }, [
                      i("span", null, [a.filename]),
                    ]),
                  ]),
                ]);
              },
            },
          },
          { field: "remark", label: "备注", show: !1, disabled: !1 },
          {
            field: "update_datetime",
            label: "更新时间",
            show: !1,
            width: "180px",
          },
          { field: "created_at", label: "创建时间", width: "180px", show: !0 },
          { field: "create_user.name", label: "创建人", show: !1 },
          {
            field: "action",
            width: "200px",
            label: "操作",
            fixed: "right",
            disabled: !1,
            show: !0,
            slots: {
              default: (e) => {
                const a = e.row;
                return i(s, null, [
                  i(
                    o,
                    {
                      type: "primary",
                      link: !0,
                      size: "small",
                      onClick: () => Q(a.id),
                    },
                    { default: () => [r("复制编号")] },
                  ),
                  i(
                    o,
                    {
                      type: "primary",
                      link: !0,
                      size: "small",
                      onClick: () => Q(a.image_url),
                    },
                    { default: () => [r("复制链接")] },
                  ),
                  i(
                    o,
                    {
                      type: "danger",
                      loading: T.value,
                      link: !0,
                      size: "small",
                      onClick: () => $(a),
                    },
                    { default: () => [r("删除")] },
                  ),
                ]);
              },
            },
          },
        ]),
        M = l([
          {
            field: "filename",
            label: "文件名称",
            component: "Input",
            componentProps: { clearable: !1, style: { width: "214px" } },
          },
        ]),
        N = n({}),
        q = (e) => {
          ((U.value = 1), (N.value = e), F());
        },
        T = n(!1),
        $ = async (e) => {
          ((T.value = !0),
            e
              ? await V(!0, [e.id]).finally(() => {
                  T.value = !1;
                })
              : await V(!0).finally(() => {
                  T.value = !1;
                }));
        },
        B = n(!1),
        G = n(""),
        H = n(),
        J = n(""),
        K = n(),
        O = n(!1),
        Q = async (e) => {
          const { copy: a } = p();
          return (await a(e), u.success("复制成功"));
        },
        X = () => {
          ((G.value = "新增图片素材"),
            (J.value = "add"),
            (H.value = void 0),
            (B.value = !0));
        },
        Y = async () => {
          const e = g(K),
            a = await (null == e ? void 0 : e.submit());
          if (a) {
            if (
              ((O.value = !0),
              null == a || a.images.forEach((e) => (e.status = "uploading")),
              "2" === (null == a ? void 0 : a.upload_method))
            )
              for (const e of null == a ? void 0 : a.images) {
                const a = new FormData();
                (a.append("file", e.raw), await C(a), (e.status = "success"));
              }
            else if ("1" === (null == a ? void 0 : a.upload_method)) {
              const e =
                null == a
                  ? void 0
                  : a.images.map(async (e) => {
                      const a = new FormData();
                      (a.append("file", e.raw),
                        await C(a),
                        (e.status = "success"));
                    });
              await Promise.all(e);
            }
            (F(), (B.value = !1), (O.value = !1));
          }
        };
      return (e, a) => (
        d(),
        m(
          s,
          null,
          [
            i(g(b), null, {
              default: c(() => [
                i(g(x), { schema: M, onReset: q, onSearch: q }, null, 8, [
                  "schema",
                ]),
                i(
                  g(h),
                  {
                    "current-page": g(U),
                    "onUpdate:currentPage":
                      a[1] || (a[1] = (e) => (_(U) ? (U.value = e) : null)),
                    "page-size": g(L),
                    "onUpdate:pageSize":
                      a[2] || (a[2] = (e) => (_(L) ? (L.value = e) : null)),
                    showAction: "",
                    columns: W,
                    "default-expand-all": "",
                    "node-key": "id",
                    data: g(I),
                    loading: g(P),
                    pagination: { total: g(E) },
                    onRegister: g(D),
                    onRefresh: g(F),
                  },
                  {
                    toolbar: c(() => [
                      i(
                        g(w),
                        { gutter: 10 },
                        {
                          default: c(() => [
                            i(
                              g(y),
                              { span: 1.5 },
                              {
                                default: c(() => [
                                  i(
                                    g(o),
                                    { type: "primary", onClick: X },
                                    {
                                      default: c(() => [r("新增图片素材")]),
                                      _: 1,
                                    },
                                  ),
                                  i(
                                    g(o),
                                    {
                                      type: "danger",
                                      onClick: a[0] || (a[0] = (e) => $(null)),
                                    },
                                    { default: c(() => [r("批量删除")]), _: 1 },
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
            i(
              g(z),
              {
                modelValue: B.value,
                "onUpdate:modelValue": a[4] || (a[4] = (e) => (B.value = e)),
                title: G.value,
                width: "996px",
                height: "600px",
                top: "3vh",
              },
              {
                footer: c(() => [
                  i(
                    g(o),
                    { type: "primary", loading: O.value, onClick: Y },
                    {
                      default: c(() => [r(f(g(R)("exampleDemo.save")), 1)]),
                      _: 1,
                    },
                    8,
                    ["loading"],
                  ),
                  i(
                    g(o),
                    { onClick: a[3] || (a[3] = (e) => (B.value = !1)) },
                    {
                      default: c(() => [r(f(g(R)("dialogDemo.close")), 1)]),
                      _: 1,
                    },
                  ),
                ]),
                default: c(() => [
                  i(
                    k,
                    { ref_key: "writeRef", ref: K, "current-row": H.value },
                    null,
                    8,
                    ["current-row"],
                  ),
                ]),
                _: 1,
              },
              8,
              ["modelValue", "title"],
            ),
          ],
          64,
        )
      );
    },
  });
export { R as default };
