import {
  cC as e,
  b as a,
  d as s,
  an as n,
  i as t,
  e as l,
  bp as o,
  dj as i,
  dk as c,
  a_ as u,
  u as r,
  bY as d,
  r as f,
  dl as v,
  ab as m,
  f as p,
  w as b,
  as as g,
  a2 as k,
  o as w,
  l as x,
  x as _,
  m as I,
  y,
  s as z,
  k as C,
  n as h,
  aY as O,
  F as N,
  E as T,
  az as A,
  j as Y,
  a1 as E,
  ax as L,
  ay as R,
  dm as X,
  cv as F,
  p as j,
  dn as $,
  dp as B,
  a5 as D,
  a0 as M,
  aH as S,
  q as W,
  D as q,
  bZ as H,
  _ as P,
  by as V,
  aA as Z,
  dq as G,
  t as J,
} from "./index-6b60d190.js";
import { d as K } from "./debounce-5c500a3d.js";
function Q(a, s, n) {
  var t = !0,
    l = !0;
  if ("function" != typeof a) throw new TypeError("Expected a function");
  return (
    e(n) &&
      ((t = "leading" in n ? !!n.leading : t),
      (l = "trailing" in n ? !!n.trailing : l)),
    K(a, s, { leading: t, maxWait: s, trailing: l })
  );
}
const U = a({
    urlList: { type: s(Array), default: () => n([]) },
    zIndex: { type: Number },
    initialIndex: { type: Number, default: 0 },
    infinite: { type: Boolean, default: !0 },
    hideOnClickModal: Boolean,
    teleported: Boolean,
    closeOnPressEscape: { type: Boolean, default: !0 },
    zoomRate: { type: Number, default: 1.2 },
  }),
  ee = { close: () => !0, switch: (e) => t(e) },
  ae = ["src"],
  se = l({ name: "ElImageViewer" });
const ne = J(
  P(
    l({
      ...se,
      props: U,
      emits: ee,
      setup(e, { expose: a, emit: s }) {
        const n = e,
          l = {
            CONTAIN: { name: "contain", icon: o(i) },
            ORIGINAL: { name: "original", icon: o(c) },
          },
          { t: P } = u(),
          J = r("image-viewer"),
          { nextZIndex: K } = d(),
          U = f(),
          ee = f([]),
          se = v(),
          ne = f(!0),
          te = f(n.initialIndex),
          le = m(l.CONTAIN),
          oe = f({
            scale: 1,
            deg: 0,
            offsetX: 0,
            offsetY: 0,
            enableTransition: !1,
          }),
          ie = p(() => {
            const { urlList: e } = n;
            return e.length <= 1;
          }),
          ce = p(() => 0 === te.value),
          ue = p(() => te.value === n.urlList.length - 1),
          re = p(() => n.urlList[te.value]),
          de = p(() => [
            J.e("btn"),
            J.e("prev"),
            J.is("disabled", !n.infinite && ce.value),
          ]),
          fe = p(() => [
            J.e("btn"),
            J.e("next"),
            J.is("disabled", !n.infinite && ue.value),
          ]),
          ve = p(() => {
            const {
              scale: e,
              deg: a,
              offsetX: s,
              offsetY: n,
              enableTransition: t,
            } = oe.value;
            let o = s / e,
              i = n / e;
            switch (a % 360) {
              case 90:
              case -270:
                [o, i] = [i, -o];
                break;
              case 180:
              case -180:
                [o, i] = [-o, -i];
                break;
              case 270:
              case -90:
                [o, i] = [-i, o];
            }
            const c = {
              transform: `scale(${e}) rotate(${a}deg) translate(${o}px, ${i}px)`,
              transition: t ? "transform .3s" : "",
            };
            return (
              le.value.name === l.CONTAIN.name &&
                (c.maxWidth = c.maxHeight = "100%"),
              c
            );
          }),
          me = p(() => (t(n.zIndex) ? n.zIndex : K()));
        function pe() {
          (se.stop(), s("close"));
        }
        function be() {
          ne.value = !1;
        }
        function ge(e) {
          ((ne.value = !1), (e.target.alt = P("el.image.error")));
        }
        function ke(e) {
          if (ne.value || 0 !== e.button || !U.value) return;
          oe.value.enableTransition = !1;
          const { offsetX: a, offsetY: s } = oe.value,
            n = e.pageX,
            t = e.pageY,
            l = Q((e) => {
              oe.value = {
                ...oe.value,
                offsetX: a + e.pageX - n,
                offsetY: s + e.pageY - t,
              };
            }),
            o = V(document, "mousemove", l);
          (V(document, "mouseup", () => {
            o();
          }),
            e.preventDefault());
        }
        function we() {
          oe.value = {
            scale: 1,
            deg: 0,
            offsetX: 0,
            offsetY: 0,
            enableTransition: !1,
          };
        }
        function xe() {
          if (ne.value) return;
          const e = G(l),
            a = Object.values(l),
            s = le.value.name,
            n = (a.findIndex((e) => e.name === s) + 1) % e.length;
          ((le.value = l[e[n]]), we());
        }
        function _e(e) {
          const a = n.urlList.length;
          te.value = (e + a) % a;
        }
        function Ie() {
          (ce.value && !n.infinite) || _e(te.value - 1);
        }
        function ye() {
          (ue.value && !n.infinite) || _e(te.value + 1);
        }
        function ze(e, a = {}) {
          if (ne.value) return;
          const {
            zoomRate: s,
            rotateDeg: t,
            enableTransition: l,
          } = {
            zoomRate: n.zoomRate,
            rotateDeg: 90,
            enableTransition: !0,
            ...a,
          };
          switch (e) {
            case "zoomOut":
              oe.value.scale > 0.2 &&
                (oe.value.scale = Number.parseFloat(
                  (oe.value.scale / s).toFixed(3),
                ));
              break;
            case "zoomIn":
              oe.value.scale < 7 &&
                (oe.value.scale = Number.parseFloat(
                  (oe.value.scale * s).toFixed(3),
                ));
              break;
            case "clockwise":
              oe.value.deg += t;
              break;
            case "anticlockwise":
              oe.value.deg -= t;
          }
          oe.value.enableTransition = l;
        }
        return (
          b(re, () => {
            g(() => {
              const e = ee.value[0];
              (null == e ? void 0 : e.complete) || (ne.value = !0);
            });
          }),
          b(te, (e) => {
            (we(), s("switch", e));
          }),
          k(() => {
            var e, a;
            (!(function () {
              const e = Q((e) => {
                  switch (e.code) {
                    case Z.esc:
                      n.closeOnPressEscape && pe();
                      break;
                    case Z.space:
                      xe();
                      break;
                    case Z.left:
                      Ie();
                      break;
                    case Z.up:
                      ze("zoomIn");
                      break;
                    case Z.right:
                      ye();
                      break;
                    case Z.down:
                      ze("zoomOut");
                  }
                }),
                a = Q((e) => {
                  ze((e.deltaY || e.deltaX) < 0 ? "zoomIn" : "zoomOut", {
                    zoomRate: n.zoomRate,
                    enableTransition: !1,
                  });
                });
              se.run(() => {
                (V(document, "keydown", e), V(document, "wheel", a));
              });
            })(),
              null == (a = null == (e = U.value) ? void 0 : e.focus) ||
                a.call(e));
          }),
          a({ setActiveItem: _e }),
          (e, a) => (
            w(),
            x(
              H,
              { to: "body", disabled: !e.teleported },
              [
                _(
                  q,
                  { name: "viewer-fade", appear: "" },
                  {
                    default: I(() => [
                      y(
                        "div",
                        {
                          ref_key: "wrapper",
                          ref: U,
                          tabindex: -1,
                          class: z(C(J).e("wrapper")),
                          style: h({ zIndex: C(me) }),
                        },
                        [
                          y(
                            "div",
                            {
                              class: z(C(J).e("mask")),
                              onClick:
                                a[0] ||
                                (a[0] = O(
                                  (a) => e.hideOnClickModal && pe(),
                                  ["self"],
                                )),
                            },
                            null,
                            2,
                          ),
                          N(" CLOSE "),
                          y(
                            "span",
                            {
                              class: z([C(J).e("btn"), C(J).e("close")]),
                              onClick: pe,
                            },
                            [
                              _(C(T), null, {
                                default: I(() => [_(C(A))]),
                                _: 1,
                              }),
                            ],
                            2,
                          ),
                          N(" ARROW "),
                          C(ie)
                            ? N("v-if", !0)
                            : (w(),
                              Y(
                                E,
                                { key: 0 },
                                [
                                  y(
                                    "span",
                                    { class: z(C(de)), onClick: Ie },
                                    [
                                      _(C(T), null, {
                                        default: I(() => [_(C(L))]),
                                        _: 1,
                                      }),
                                    ],
                                    2,
                                  ),
                                  y(
                                    "span",
                                    { class: z(C(fe)), onClick: ye },
                                    [
                                      _(C(T), null, {
                                        default: I(() => [_(C(R))]),
                                        _: 1,
                                      }),
                                    ],
                                    2,
                                  ),
                                ],
                                64,
                              )),
                          N(" ACTIONS "),
                          y(
                            "div",
                            { class: z([C(J).e("btn"), C(J).e("actions")]) },
                            [
                              y(
                                "div",
                                { class: z(C(J).e("actions__inner")) },
                                [
                                  _(
                                    C(T),
                                    {
                                      onClick:
                                        a[1] || (a[1] = (e) => ze("zoomOut")),
                                    },
                                    { default: I(() => [_(C(X))]), _: 1 },
                                  ),
                                  _(
                                    C(T),
                                    {
                                      onClick:
                                        a[2] || (a[2] = (e) => ze("zoomIn")),
                                    },
                                    { default: I(() => [_(C(F))]), _: 1 },
                                  ),
                                  y(
                                    "i",
                                    { class: z(C(J).e("actions__divider")) },
                                    null,
                                    2,
                                  ),
                                  _(
                                    C(T),
                                    { onClick: xe },
                                    {
                                      default: I(() => [
                                        (w(), x(j(C(le).icon))),
                                      ]),
                                      _: 1,
                                    },
                                  ),
                                  y(
                                    "i",
                                    { class: z(C(J).e("actions__divider")) },
                                    null,
                                    2,
                                  ),
                                  _(
                                    C(T),
                                    {
                                      onClick:
                                        a[3] ||
                                        (a[3] = (e) => ze("anticlockwise")),
                                    },
                                    { default: I(() => [_(C($))]), _: 1 },
                                  ),
                                  _(
                                    C(T),
                                    {
                                      onClick:
                                        a[4] || (a[4] = (e) => ze("clockwise")),
                                    },
                                    { default: I(() => [_(C(B))]), _: 1 },
                                  ),
                                ],
                                2,
                              ),
                            ],
                            2,
                          ),
                          N(" CANVAS "),
                          y(
                            "div",
                            { class: z(C(J).e("canvas")) },
                            [
                              (w(!0),
                              Y(
                                E,
                                null,
                                D(e.urlList, (e, a) =>
                                  M(
                                    (w(),
                                    Y(
                                      "img",
                                      {
                                        ref_for: !0,
                                        ref: (e) => (ee.value[a] = e),
                                        key: e,
                                        src: e,
                                        style: h(C(ve)),
                                        class: z(C(J).e("img")),
                                        onLoad: be,
                                        onError: ge,
                                        onMousedown: ke,
                                      },
                                      null,
                                      46,
                                      ae,
                                    )),
                                    [[S, a === te.value]],
                                  ),
                                ),
                                128,
                              )),
                            ],
                            2,
                          ),
                          W(e.$slots, "default"),
                        ],
                        6,
                      ),
                    ]),
                    _: 3,
                  },
                ),
              ],
              8,
              ["disabled"],
            )
          )
        );
      },
    }),
    [
      [
        "__file",
        "/home/runner/work/element-plus/element-plus/packages/components/image-viewer/src/image-viewer.vue",
      ],
    ],
  ),
);
export { ne as E };
