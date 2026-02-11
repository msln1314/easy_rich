import {
  b as e,
  d as t,
  e as a,
  u as s,
  f as l,
  cs as n,
  ct as r,
  bc as o,
  b0 as i,
  az as u,
  b3 as c,
  g as d,
  o as p,
  j as f,
  s as v,
  k as m,
  y,
  n as h,
  q as g,
  z as b,
  F as k,
  l as w,
  m as $,
  p as x,
  E as F,
  _ as E,
  t as R,
  ar as S,
  an as T,
  aS as _,
  a_ as L,
  aU as C,
  r as U,
  a1 as P,
  a5 as B,
  aX as j,
  aY as D,
  x as O,
  cu as N,
  cv as q,
  cw as A,
  T as H,
  aZ as M,
  ao as W,
  ab as z,
  ap as I,
  b5 as K,
  cx as X,
  cy as J,
  w as V,
  ba as Y,
  aE as Z,
  aj as G,
  am as Q,
  a4 as ee,
  ak as te,
  a6 as ae,
} from "./index-6b60d190.js";
import { i as se } from "./isNil-1f22f7b0.js";
import { i as le } from "./isEqual-b8d86c27.js";
const ne = e({
    type: {
      type: String,
      default: "line",
      values: ["line", "circle", "dashboard"],
    },
    percentage: {
      type: Number,
      default: 0,
      validator: (e) => e >= 0 && e <= 100,
    },
    status: {
      type: String,
      default: "",
      values: ["", "success", "exception", "warning"],
    },
    indeterminate: { type: Boolean, default: !1 },
    duration: { type: Number, default: 3 },
    strokeWidth: { type: Number, default: 6 },
    strokeLinecap: { type: t(String), default: "round" },
    textInside: { type: Boolean, default: !1 },
    width: { type: Number, default: 126 },
    showText: { type: Boolean, default: !0 },
    color: { type: t([String, Array, Function]), default: "" },
    striped: Boolean,
    stripedFlow: Boolean,
    format: { type: t(Function), default: (e) => `${e}%` },
  }),
  re = ["aria-valuenow"],
  oe = { viewBox: "0 0 100 100" },
  ie = ["d", "stroke", "stroke-linecap", "stroke-width"],
  ue = ["d", "stroke", "opacity", "stroke-linecap", "stroke-width"],
  ce = { key: 0 },
  de = a({ name: "ElProgress" });
const pe = R(
    E(
      a({
        ...de,
        props: ne,
        setup(e) {
          const t = e,
            a = {
              success: "#13ce66",
              exception: "#ff4949",
              warning: "#e6a23c",
              default: "#20a0ff",
            },
            E = s("progress"),
            R = l(() => ({
              width: `${t.percentage}%`,
              animationDuration: `${t.duration}s`,
              backgroundColor: q(t.percentage),
            })),
            S = l(() => ((t.strokeWidth / t.width) * 100).toFixed(1)),
            T = l(() =>
              ["circle", "dashboard"].includes(t.type)
                ? Number.parseInt(
                    "" + (50 - Number.parseFloat(S.value) / 2),
                    10,
                  )
                : 0,
            ),
            _ = l(() => {
              const e = T.value,
                a = "dashboard" === t.type;
              return `\n          M 50 50\n          m 0 ${a ? "" : "-"}${e}\n          a ${e} ${e} 0 1 1 0 ${a ? "-" : ""}${2 * e}\n          a ${e} ${e} 0 1 1 0 ${a ? "" : "-"}${2 * e}\n          `;
            }),
            L = l(() => 2 * Math.PI * T.value),
            C = l(() => ("dashboard" === t.type ? 0.75 : 1)),
            U = l(() => `${(-1 * L.value * (1 - C.value)) / 2}px`),
            P = l(() => ({
              strokeDasharray: `${L.value * C.value}px, ${L.value}px`,
              strokeDashoffset: U.value,
            })),
            B = l(() => ({
              strokeDasharray: `${L.value * C.value * (t.percentage / 100)}px, ${L.value}px`,
              strokeDashoffset: U.value,
              transition:
                "stroke-dasharray 0.6s ease 0s, stroke 0.6s ease, opacity ease 0.6s",
            })),
            j = l(() => {
              let e;
              return (
                (e = t.color ? q(t.percentage) : a[t.status] || a.default),
                e
              );
            }),
            D = l(() =>
              "warning" === t.status
                ? n
                : "line" === t.type
                  ? "success" === t.status
                    ? r
                    : o
                  : "success" === t.status
                    ? i
                    : u,
            ),
            O = l(() =>
              "line" === t.type
                ? 12 + 0.4 * t.strokeWidth
                : 0.111111 * t.width + 2,
            ),
            N = l(() => t.format(t.percentage));
          const q = (e) => {
            var a;
            const { color: s } = t;
            if (c(s)) return s(e);
            if (d(s)) return s;
            {
              const t = (function (e) {
                const t = 100 / e.length;
                return e
                  .map((e, a) =>
                    d(e) ? { color: e, percentage: (a + 1) * t } : e,
                  )
                  .sort((e, t) => e.percentage - t.percentage);
              })(s);
              for (const a of t) if (a.percentage > e) return a.color;
              return null == (a = t[t.length - 1]) ? void 0 : a.color;
            }
          };
          return (e, t) => (
            p(),
            f(
              "div",
              {
                class: v([
                  m(E).b(),
                  m(E).m(e.type),
                  m(E).is(e.status),
                  {
                    [m(E).m("without-text")]: !e.showText,
                    [m(E).m("text-inside")]: e.textInside,
                  },
                ]),
                role: "progressbar",
                "aria-valuenow": e.percentage,
                "aria-valuemin": "0",
                "aria-valuemax": "100",
              },
              [
                "line" === e.type
                  ? (p(),
                    f(
                      "div",
                      { key: 0, class: v(m(E).b("bar")) },
                      [
                        y(
                          "div",
                          {
                            class: v(m(E).be("bar", "outer")),
                            style: h({ height: `${e.strokeWidth}px` }),
                          },
                          [
                            y(
                              "div",
                              {
                                class: v([
                                  m(E).be("bar", "inner"),
                                  {
                                    [m(E).bem("bar", "inner", "indeterminate")]:
                                      e.indeterminate,
                                  },
                                  {
                                    [m(E).bem("bar", "inner", "striped")]:
                                      e.striped,
                                  },
                                  {
                                    [m(E).bem("bar", "inner", "striped-flow")]:
                                      e.stripedFlow,
                                  },
                                ]),
                                style: h(m(R)),
                              },
                              [
                                (e.showText || e.$slots.default) && e.textInside
                                  ? (p(),
                                    f(
                                      "div",
                                      {
                                        key: 0,
                                        class: v(m(E).be("bar", "innerText")),
                                      },
                                      [
                                        g(
                                          e.$slots,
                                          "default",
                                          { percentage: e.percentage },
                                          () => [y("span", null, b(m(N)), 1)],
                                        ),
                                      ],
                                      2,
                                    ))
                                  : k("v-if", !0),
                              ],
                              6,
                            ),
                          ],
                          6,
                        ),
                      ],
                      2,
                    ))
                  : (p(),
                    f(
                      "div",
                      {
                        key: 1,
                        class: v(m(E).b("circle")),
                        style: h({
                          height: `${e.width}px`,
                          width: `${e.width}px`,
                        }),
                      },
                      [
                        (p(),
                        f("svg", oe, [
                          y(
                            "path",
                            {
                              class: v(m(E).be("circle", "track")),
                              d: m(_),
                              stroke: `var(${m(E).cssVarName("fill-color-light")}, #e5e9f2)`,
                              "stroke-linecap": e.strokeLinecap,
                              "stroke-width": m(S),
                              fill: "none",
                              style: h(m(P)),
                            },
                            null,
                            14,
                            ie,
                          ),
                          y(
                            "path",
                            {
                              class: v(m(E).be("circle", "path")),
                              d: m(_),
                              stroke: m(j),
                              fill: "none",
                              opacity: e.percentage ? 1 : 0,
                              "stroke-linecap": e.strokeLinecap,
                              "stroke-width": m(S),
                              style: h(m(B)),
                            },
                            null,
                            14,
                            ue,
                          ),
                        ])),
                      ],
                      6,
                    )),
                (!e.showText && !e.$slots.default) || e.textInside
                  ? k("v-if", !0)
                  : (p(),
                    f(
                      "div",
                      {
                        key: 2,
                        class: v(m(E).e("text")),
                        style: h({ fontSize: `${m(O)}px` }),
                      },
                      [
                        g(
                          e.$slots,
                          "default",
                          { percentage: e.percentage },
                          () => [
                            e.status
                              ? (p(),
                                w(
                                  m(F),
                                  { key: 1 },
                                  {
                                    default: $(() => [(p(), w(x(m(D))))]),
                                    _: 1,
                                  },
                                ))
                              : (p(), f("span", ce, b(m(N)), 1)),
                          ],
                        ),
                      ],
                      6,
                    )),
              ],
              10,
              re,
            )
          );
        },
      }),
      [
        [
          "__file",
          "/home/runner/work/element-plus/element-plus/packages/components/progress/src/progress.vue",
        ],
      ],
    ),
  ),
  fe = Symbol("uploadContextKey");
class ve extends Error {
  constructor(e, t, a, s) {
    (super(e),
      (this.name = "UploadAjaxError"),
      (this.status = t),
      (this.method = a),
      (this.url = s));
  }
}
function me(e, t, a) {
  let s;
  return (
    (s = a.response
      ? `${a.response.error || a.response}`
      : a.responseText
        ? `${a.responseText}`
        : `fail to ${t.method} ${e} ${a.status}`),
    new ve(s, a.status, t.method, e)
  );
}
const ye = ["text", "picture", "picture-card"];
let he = 1;
const ge = () => Date.now() + he++,
  be = e({
    action: { type: String, default: "#" },
    headers: { type: t(Object) },
    method: { type: String, default: "post" },
    data: { type: Object, default: () => T({}) },
    multiple: { type: Boolean, default: !1 },
    name: { type: String, default: "file" },
    drag: { type: Boolean, default: !1 },
    withCredentials: Boolean,
    showFileList: { type: Boolean, default: !0 },
    accept: { type: String, default: "" },
    type: { type: String, default: "select" },
    fileList: { type: t(Array), default: () => T([]) },
    autoUpload: { type: Boolean, default: !0 },
    listType: { type: String, values: ye, default: "text" },
    httpRequest: {
      type: t(Function),
      default: (e) => {
        "undefined" == typeof XMLHttpRequest &&
          S("ElUpload", "XMLHttpRequest is undefined");
        const t = new XMLHttpRequest(),
          a = e.action;
        t.upload &&
          t.upload.addEventListener("progress", (t) => {
            const a = t;
            ((a.percent = t.total > 0 ? (t.loaded / t.total) * 100 : 0),
              e.onProgress(a));
          });
        const s = new FormData();
        if (e.data)
          for (const [n, r] of Object.entries(e.data))
            Array.isArray(r) ? s.append(n, ...r) : s.append(n, r);
        (s.append(e.filename, e.file, e.file.name),
          t.addEventListener("error", () => {
            e.onError(me(a, e, t));
          }),
          t.addEventListener("load", () => {
            if (t.status < 200 || t.status >= 300)
              return e.onError(me(a, e, t));
            e.onSuccess(
              (function (e) {
                const t = e.responseText || e.response;
                if (!t) return t;
                try {
                  return JSON.parse(t);
                } catch (a) {
                  return t;
                }
              })(t),
            );
          }),
          t.open(e.method, a, !0),
          e.withCredentials &&
            "withCredentials" in t &&
            (t.withCredentials = !0));
        const l = e.headers || {};
        if (l instanceof Headers) l.forEach((e, a) => t.setRequestHeader(a, e));
        else
          for (const [n, r] of Object.entries(l))
            se(r) || t.setRequestHeader(n, String(r));
        return (t.send(s), t);
      },
    },
    disabled: Boolean,
    limit: Number,
  }),
  ke = e({
    ...be,
    beforeUpload: { type: t(Function), default: _ },
    beforeRemove: { type: t(Function) },
    onRemove: { type: t(Function), default: _ },
    onChange: { type: t(Function), default: _ },
    onPreview: { type: t(Function), default: _ },
    onSuccess: { type: t(Function), default: _ },
    onProgress: { type: t(Function), default: _ },
    onError: { type: t(Function), default: _ },
    onExceed: { type: t(Function), default: _ },
  }),
  we = e({
    files: { type: t(Array), default: () => T([]) },
    disabled: { type: Boolean, default: !1 },
    handlePreview: { type: t(Function), default: _ },
    listType: { type: String, values: ye, default: "text" },
  }),
  $e = ["onKeydown"],
  xe = ["src"],
  Fe = ["onClick"],
  Ee = ["title"],
  Re = ["onClick"],
  Se = ["onClick"],
  Te = a({ name: "ElUploadList" });
var _e = E(
  a({
    ...Te,
    props: we,
    emits: { remove: (e) => !!e },
    setup(e, { emit: t }) {
      const { t: a } = L(),
        l = s("upload"),
        n = s("icon"),
        o = s("list"),
        c = C(),
        d = U(!1),
        x = (e) => {
          t("remove", e);
        };
      return (e, t) => (
        p(),
        w(
          H,
          {
            tag: "ul",
            class: v([
              m(l).b("list"),
              m(l).bm("list", e.listType),
              m(l).is("disabled", m(c)),
            ]),
            name: m(o).b(),
          },
          {
            default: $(() => [
              (p(!0),
              f(
                P,
                null,
                B(
                  e.files,
                  (s) => (
                    p(),
                    f(
                      "li",
                      {
                        key: s.uid || s.name,
                        class: v([
                          m(l).be("list", "item"),
                          m(l).is(s.status),
                          { focusing: d.value },
                        ]),
                        tabindex: "0",
                        onKeydown: j((e) => !m(c) && x(s), ["delete"]),
                        onFocus: t[0] || (t[0] = (e) => (d.value = !0)),
                        onBlur: t[1] || (t[1] = (e) => (d.value = !1)),
                        onClick: t[2] || (t[2] = (e) => (d.value = !1)),
                      },
                      [
                        g(e.$slots, "default", { file: s }, () => [
                          "picture" === e.listType ||
                          ("uploading" !== s.status &&
                            "picture-card" === e.listType)
                            ? (p(),
                              f(
                                "img",
                                {
                                  key: 0,
                                  class: v(m(l).be("list", "item-thumbnail")),
                                  src: s.url,
                                  alt: "",
                                },
                                null,
                                10,
                                xe,
                              ))
                            : k("v-if", !0),
                          "uploading" === s.status ||
                          "picture-card" !== e.listType
                            ? (p(),
                              f(
                                "div",
                                {
                                  key: 1,
                                  class: v(m(l).be("list", "item-info")),
                                },
                                [
                                  y(
                                    "a",
                                    {
                                      class: v(m(l).be("list", "item-name")),
                                      onClick: D(
                                        (t) => e.handlePreview(s),
                                        ["prevent"],
                                      ),
                                    },
                                    [
                                      O(
                                        m(F),
                                        { class: v(m(n).m("document")) },
                                        { default: $(() => [O(m(N))]), _: 1 },
                                        8,
                                        ["class"],
                                      ),
                                      y(
                                        "span",
                                        {
                                          class: v(
                                            m(l).be("list", "item-file-name"),
                                          ),
                                          title: s.name,
                                        },
                                        b(s.name),
                                        11,
                                        Ee,
                                      ),
                                    ],
                                    10,
                                    Fe,
                                  ),
                                  "uploading" === s.status
                                    ? (p(),
                                      w(
                                        m(pe),
                                        {
                                          key: 0,
                                          type:
                                            "picture-card" === e.listType
                                              ? "circle"
                                              : "line",
                                          "stroke-width":
                                            "picture-card" === e.listType
                                              ? 6
                                              : 2,
                                          percentage: Number(s.percentage),
                                          style: h(
                                            "picture-card" === e.listType
                                              ? ""
                                              : "margin-top: 0.5rem",
                                          ),
                                        },
                                        null,
                                        8,
                                        [
                                          "type",
                                          "stroke-width",
                                          "percentage",
                                          "style",
                                        ],
                                      ))
                                    : k("v-if", !0),
                                ],
                                2,
                              ))
                            : k("v-if", !0),
                          y(
                            "label",
                            { class: v(m(l).be("list", "item-status-label")) },
                            [
                              "text" === e.listType
                                ? (p(),
                                  w(
                                    m(F),
                                    {
                                      key: 0,
                                      class: v([
                                        m(n).m("upload-success"),
                                        m(n).m("circle-check"),
                                      ]),
                                    },
                                    { default: $(() => [O(m(r))]), _: 1 },
                                    8,
                                    ["class"],
                                  ))
                                : ["picture-card", "picture"].includes(
                                      e.listType,
                                    )
                                  ? (p(),
                                    w(
                                      m(F),
                                      {
                                        key: 1,
                                        class: v([
                                          m(n).m("upload-success"),
                                          m(n).m("check"),
                                        ]),
                                      },
                                      { default: $(() => [O(m(i))]), _: 1 },
                                      8,
                                      ["class"],
                                    ))
                                  : k("v-if", !0),
                            ],
                            2,
                          ),
                          m(c)
                            ? k("v-if", !0)
                            : (p(),
                              w(
                                m(F),
                                {
                                  key: 2,
                                  class: v(m(n).m("close")),
                                  onClick: (e) => x(s),
                                },
                                { default: $(() => [O(m(u))]), _: 2 },
                                1032,
                                ["class", "onClick"],
                              )),
                          k(
                            " Due to close btn only appears when li gets focused disappears after li gets blurred, thus keyboard navigation can never reach close btn",
                          ),
                          k(" This is a bug which needs to be fixed "),
                          k(" TODO: Fix the incorrect navigation interaction "),
                          m(c)
                            ? k("v-if", !0)
                            : (p(),
                              f(
                                "i",
                                { key: 3, class: v(m(n).m("close-tip")) },
                                b(m(a)("el.upload.deleteTip")),
                                3,
                              )),
                          "picture-card" === e.listType
                            ? (p(),
                              f(
                                "span",
                                {
                                  key: 4,
                                  class: v(m(l).be("list", "item-actions")),
                                },
                                [
                                  y(
                                    "span",
                                    {
                                      class: v(m(l).be("list", "item-preview")),
                                      onClick: (t) => e.handlePreview(s),
                                    },
                                    [
                                      O(
                                        m(F),
                                        { class: v(m(n).m("zoom-in")) },
                                        { default: $(() => [O(m(q))]), _: 1 },
                                        8,
                                        ["class"],
                                      ),
                                    ],
                                    10,
                                    Re,
                                  ),
                                  m(c)
                                    ? k("v-if", !0)
                                    : (p(),
                                      f(
                                        "span",
                                        {
                                          key: 0,
                                          class: v(
                                            m(l).be("list", "item-delete"),
                                          ),
                                          onClick: (e) => x(s),
                                        },
                                        [
                                          O(
                                            m(F),
                                            { class: v(m(n).m("delete")) },
                                            {
                                              default: $(() => [O(m(A))]),
                                              _: 1,
                                            },
                                            8,
                                            ["class"],
                                          ),
                                        ],
                                        10,
                                        Se,
                                      )),
                                ],
                                2,
                              ))
                            : k("v-if", !0),
                        ]),
                      ],
                      42,
                      $e,
                    )
                  ),
                ),
                128,
              )),
              g(e.$slots, "append"),
            ]),
            _: 3,
          },
          8,
          ["class", "name"],
        )
      );
    },
  }),
  [
    [
      "__file",
      "/home/runner/work/element-plus/element-plus/packages/components/upload/src/upload-list.vue",
    ],
  ],
);
const Le = e({ disabled: { type: Boolean, default: !1 } }),
  Ce = { file: (e) => M(e) },
  Ue = ["onDrop", "onDragover"],
  Pe = "ElUploadDrag",
  Be = a({ name: Pe });
var je = E(
  a({
    ...Be,
    props: Le,
    emits: Ce,
    setup(e, { emit: t }) {
      const a = W(fe);
      a || S(Pe, "usage: <el-upload><el-upload-dragger /></el-upload>");
      const l = s("upload"),
        n = U(!1),
        r = C(),
        o = (e) => {
          if (r.value) return;
          ((n.value = !1), e.stopPropagation());
          const s = Array.from(e.dataTransfer.files),
            l = a.accept.value;
          if (!l) return void t("file", s);
          const o = s.filter((e) => {
            const { type: t, name: a } = e,
              s = a.includes(".") ? `.${a.split(".").pop()}` : "",
              n = t.replace(/\/.*$/, "");
            return l
              .split(",")
              .map((e) => e.trim())
              .filter((e) => e)
              .some((e) =>
                e.startsWith(".")
                  ? s === e
                  : /\/\*$/.test(e)
                    ? n === e.replace(/\/\*$/, "")
                    : !!/^[^/]+\/[^/]+$/.test(e) && t === e,
              );
          });
          t("file", o);
        },
        i = () => {
          r.value || (n.value = !0);
        };
      return (e, t) => (
        p(),
        f(
          "div",
          {
            class: v([m(l).b("dragger"), m(l).is("dragover", n.value)]),
            onDrop: D(o, ["prevent"]),
            onDragover: D(i, ["prevent"]),
            onDragleave: t[0] || (t[0] = D((e) => (n.value = !1), ["prevent"])),
          },
          [g(e.$slots, "default")],
          42,
          Ue,
        )
      );
    },
  }),
  [
    [
      "__file",
      "/home/runner/work/element-plus/element-plus/packages/components/upload/src/upload-dragger.vue",
    ],
  ],
);
const De = e({
    ...be,
    beforeUpload: { type: t(Function), default: _ },
    onRemove: { type: t(Function), default: _ },
    onStart: { type: t(Function), default: _ },
    onSuccess: { type: t(Function), default: _ },
    onProgress: { type: t(Function), default: _ },
    onError: { type: t(Function), default: _ },
    onExceed: { type: t(Function), default: _ },
  }),
  Oe = ["onKeydown"],
  Ne = ["name", "multiple", "accept"],
  qe = a({ name: "ElUploadContent", inheritAttrs: !1 });
var Ae = E(
  a({
    ...qe,
    props: De,
    setup(e, { expose: t }) {
      const a = e,
        l = s("upload"),
        n = C(),
        r = z({}),
        o = z(),
        i = (e) => {
          if (0 === e.length) return;
          const {
            autoUpload: t,
            limit: s,
            fileList: l,
            multiple: n,
            onStart: r,
            onExceed: o,
          } = a;
          if (s && l.length + e.length > s) o(e, l);
          else {
            n || (e = e.slice(0, 1));
            for (const a of e) {
              const e = a;
              ((e.uid = ge()), r(e), t && u(e));
            }
          }
        },
        u = async (e) => {
          if (((o.value.value = ""), !a.beforeUpload)) return c(e);
          let t,
            s = {};
          try {
            const l = a.data,
              n = a.beforeUpload(e);
            ((s = I(a.data) ? K(a.data) : a.data),
              (t = await n),
              I(a.data) && le(l, s) && (s = K(a.data)));
          } catch (n) {
            t = !1;
          }
          if (!1 === t) return void a.onRemove(e);
          let l = e;
          (t instanceof Blob &&
            (l =
              t instanceof File ? t : new File([t], e.name, { type: e.type })),
            c(Object.assign(l, { uid: e.uid }), s));
        },
        c = (e, t) => {
          const {
              headers: s,
              data: l,
              method: n,
              withCredentials: o,
              name: i,
              action: u,
              onProgress: c,
              onSuccess: d,
              onError: p,
              httpRequest: f,
            } = a,
            { uid: v } = e,
            m = {
              headers: s || {},
              withCredentials: o,
              file: e,
              data: null != t ? t : l,
              method: n,
              filename: i,
              action: u,
              onProgress: (t) => {
                c(t, e);
              },
              onSuccess: (t) => {
                (d(t, e), delete r.value[v]);
              },
              onError: (t) => {
                (p(t, e), delete r.value[v]);
              },
            },
            y = f(m);
          ((r.value[v] = y),
            y instanceof Promise && y.then(m.onSuccess, m.onError));
        },
        d = (e) => {
          const t = e.target.files;
          t && i(Array.from(t));
        },
        h = () => {
          n.value || ((o.value.value = ""), o.value.click());
        },
        b = () => {
          h();
        };
      return (
        t({
          abort: (e) => {
            X(r.value)
              .filter(e ? ([t]) => String(e.uid) === t : () => !0)
              .forEach(([e, t]) => {
                (t instanceof XMLHttpRequest && t.abort(), delete r.value[e]);
              });
          },
          upload: u,
        }),
        (e, t) => (
          p(),
          f(
            "div",
            {
              class: v([m(l).b(), m(l).m(e.listType), m(l).is("drag", e.drag)]),
              tabindex: "0",
              onClick: h,
              onKeydown: j(D(b, ["self"]), ["enter", "space"]),
            },
            [
              e.drag
                ? (p(),
                  w(
                    je,
                    { key: 0, disabled: m(n), onFile: i },
                    { default: $(() => [g(e.$slots, "default")]), _: 3 },
                    8,
                    ["disabled"],
                  ))
                : g(e.$slots, "default", { key: 1 }),
              y(
                "input",
                {
                  ref_key: "inputRef",
                  ref: o,
                  class: v(m(l).e("input")),
                  name: e.name,
                  multiple: e.multiple,
                  accept: e.accept,
                  type: "file",
                  onChange: d,
                  onClick: t[0] || (t[0] = D(() => {}, ["stop"])),
                },
                null,
                42,
                Ne,
              ),
            ],
            42,
            Oe,
          )
        )
      );
    },
  }),
  [
    [
      "__file",
      "/home/runner/work/element-plus/element-plus/packages/components/upload/src/upload-content.vue",
    ],
  ],
);
const He = "ElUpload",
  Me = (e, t) => {
    const a = J(e, "fileList", void 0, { passive: !0 }),
      s = (e) => a.value.find((t) => t.uid === e.uid);
    function l(e) {
      var a;
      null == (a = t.value) || a.abort(e);
    }
    return (
      V(
        () => e.listType,
        (t) => {
          ("picture-card" !== t && "picture" !== t) ||
            (a.value = a.value.map((t) => {
              const { raw: s, url: l } = t;
              if (!l && s)
                try {
                  t.url = URL.createObjectURL(s);
                } catch (n) {
                  e.onError(n, t, a.value);
                }
              return t;
            }));
        },
      ),
      V(
        a,
        (e) => {
          for (const t of e)
            (t.uid || (t.uid = ge()), t.status || (t.status = "success"));
        },
        { immediate: !0, deep: !0 },
      ),
      {
        uploadFiles: a,
        abort: l,
        clearFiles: function (e = ["ready", "uploading", "success", "fail"]) {
          a.value = a.value.filter((t) => !e.includes(t.status));
        },
        handleError: (t, l) => {
          const n = s(l);
          n &&
            ((n.status = "fail"),
            a.value.splice(a.value.indexOf(n), 1),
            e.onError(t, n, a.value),
            e.onChange(n, a.value));
        },
        handleProgress: (t, l) => {
          const n = s(l);
          n &&
            (e.onProgress(t, n, a.value),
            (n.status = "uploading"),
            (n.percentage = Math.round(t.percent)));
        },
        handleStart: (t) => {
          se(t.uid) && (t.uid = ge());
          const s = {
            name: t.name,
            percentage: 0,
            status: "ready",
            size: t.size,
            raw: t,
            uid: t.uid,
          };
          if ("picture-card" === e.listType || "picture" === e.listType)
            try {
              s.url = URL.createObjectURL(t);
            } catch (l) {
              (Y(He, l.message), e.onError(l, s, a.value));
            }
          ((a.value = [...a.value, s]), e.onChange(s, a.value));
        },
        handleSuccess: (t, l) => {
          const n = s(l);
          n &&
            ((n.status = "success"),
            (n.response = t),
            e.onSuccess(t, n, a.value),
            e.onChange(n, a.value));
        },
        handleRemove: async (t) => {
          const n = t instanceof File ? s(t) : t;
          n || S(He, "file to be removed not found");
          const r = (t) => {
            l(t);
            const s = a.value;
            (s.splice(s.indexOf(t), 1),
              e.onRemove(t, s),
              ((e) => {
                var t;
                (null == (t = e.url) ? void 0 : t.startsWith("blob:")) &&
                  URL.revokeObjectURL(e.url);
              })(t));
          };
          if (e.beforeRemove) {
            !1 !== (await e.beforeRemove(n, a.value)) && r(n);
          } else r(n);
        },
        submit: function () {
          a.value
            .filter(({ status: e }) => "ready" === e)
            .forEach(({ raw: e }) => {
              var a;
              return e && (null == (a = t.value) ? void 0 : a.upload(e));
            });
        },
      }
    );
  },
  We = a({ name: "ElUpload" });
const ze = R(
  E(
    a({
      ...We,
      props: ke,
      setup(e, { expose: t }) {
        const a = e,
          s = Z(),
          n = C(),
          r = z(),
          {
            abort: o,
            submit: i,
            clearFiles: u,
            uploadFiles: c,
            handleStart: d,
            handleError: v,
            handleRemove: y,
            handleSuccess: h,
            handleProgress: b,
          } = Me(a, r),
          x = l(() => "picture-card" === a.listType),
          F = l(() => ({
            ...a,
            fileList: c.value,
            onStart: d,
            onProgress: b,
            onSuccess: h,
            onError: v,
            onRemove: y,
          }));
        return (
          G(() => {
            c.value.forEach(({ url: e }) => {
              (null == e ? void 0 : e.startsWith("blob:")) &&
                URL.revokeObjectURL(e);
            });
          }),
          Q(fe, { accept: ee(a, "accept") }),
          t({
            abort: o,
            submit: i,
            clearFiles: u,
            handleStart: d,
            handleRemove: y,
          }),
          (e, t) => (
            p(),
            f("div", null, [
              m(x) && e.showFileList
                ? (p(),
                  w(
                    _e,
                    {
                      key: 0,
                      disabled: m(n),
                      "list-type": e.listType,
                      files: m(c),
                      "handle-preview": e.onPreview,
                      onRemove: m(y),
                    },
                    te(
                      {
                        append: $(() => [
                          O(
                            Ae,
                            ae({ ref_key: "uploadRef", ref: r }, m(F)),
                            {
                              default: $(() => [
                                m(s).trigger
                                  ? g(e.$slots, "trigger", { key: 0 })
                                  : k("v-if", !0),
                                !m(s).trigger && m(s).default
                                  ? g(e.$slots, "default", { key: 1 })
                                  : k("v-if", !0),
                              ]),
                              _: 3,
                            },
                            16,
                          ),
                        ]),
                        _: 2,
                      },
                      [
                        e.$slots.file
                          ? {
                              name: "default",
                              fn: $(({ file: t }) => [
                                g(e.$slots, "file", { file: t }),
                              ]),
                            }
                          : void 0,
                      ],
                    ),
                    1032,
                    [
                      "disabled",
                      "list-type",
                      "files",
                      "handle-preview",
                      "onRemove",
                    ],
                  ))
                : k("v-if", !0),
              !m(x) || (m(x) && !e.showFileList)
                ? (p(),
                  w(
                    Ae,
                    ae({ key: 1, ref_key: "uploadRef", ref: r }, m(F)),
                    {
                      default: $(() => [
                        m(s).trigger
                          ? g(e.$slots, "trigger", { key: 0 })
                          : k("v-if", !0),
                        !m(s).trigger && m(s).default
                          ? g(e.$slots, "default", { key: 1 })
                          : k("v-if", !0),
                      ]),
                      _: 3,
                    },
                    16,
                  ))
                : k("v-if", !0),
              e.$slots.trigger
                ? g(e.$slots, "default", { key: 2 })
                : k("v-if", !0),
              g(e.$slots, "tip"),
              !m(x) && e.showFileList
                ? (p(),
                  w(
                    _e,
                    {
                      key: 3,
                      disabled: m(n),
                      "list-type": e.listType,
                      files: m(c),
                      "handle-preview": e.onPreview,
                      onRemove: m(y),
                    },
                    te({ _: 2 }, [
                      e.$slots.file
                        ? {
                            name: "default",
                            fn: $(({ file: t }) => [
                              g(e.$slots, "file", { file: t }),
                            ]),
                          }
                        : void 0,
                    ]),
                    1032,
                    [
                      "disabled",
                      "list-type",
                      "files",
                      "handle-preview",
                      "onRemove",
                    ],
                  ))
                : k("v-if", !0),
            ])
          )
        );
      },
    }),
    [
      [
        "__file",
        "/home/runner/work/element-plus/element-plus/packages/components/upload/src/upload.vue",
      ],
    ],
  ),
);
export { ze as E };
