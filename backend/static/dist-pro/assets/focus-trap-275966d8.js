import {
  a2 as e,
  aJ as t,
  aj as n,
  aA as o,
  r as s,
  _ as a,
  e as r,
  am as u,
  w as c,
  k as d,
  q as i,
  as as l,
  g as f,
} from "./index-6b60d190.js";
import { i as p } from "./isNil-1f22f7b0.js";
let v = [];
const m = (e) => {
    const t = e;
    t.key === o.esc && v.forEach((e) => e(t));
  },
  E = "focus-trap.focus-after-trapped",
  w = "focus-trap.focus-after-released",
  y = { cancelable: !0, bubbles: !1 },
  L = { cancelable: !0, bubbles: !1 },
  h = "focusAfterTrapped",
  T = "focusAfterReleased",
  b = Symbol("elFocusTrap"),
  k = s(),
  g = s(0),
  F = s(0);
let R = 0;
const N = (e) => {
    const t = [],
      n = document.createTreeWalker(e, NodeFilter.SHOW_ELEMENT, {
        acceptNode: (e) => {
          const t = "INPUT" === e.tagName && "hidden" === e.type;
          return e.disabled || e.hidden || t
            ? NodeFilter.FILTER_SKIP
            : e.tabIndex >= 0 || e === document.activeElement
              ? NodeFilter.FILTER_ACCEPT
              : NodeFilter.FILTER_SKIP;
        },
      });
    for (; n.nextNode(); ) t.push(n.currentNode);
    return t;
  },
  K = (e, t) => {
    for (const n of e) if (!P(n, t)) return n;
  },
  P = (e, t) => {
    if ("hidden" === getComputedStyle(e).visibility) return !0;
    for (; e; ) {
      if (t && e === t) return !1;
      if ("none" === getComputedStyle(e).display) return !0;
      e = e.parentElement;
    }
    return !1;
  },
  S = (e, t) => {
    if (e && e.focus) {
      const n = document.activeElement;
      (e.focus({ preventScroll: !0 }),
        (F.value = window.performance.now()),
        e !== n &&
          ((e) => e instanceof HTMLInputElement && "select" in e)(e) &&
          t &&
          e.select());
    }
  };
function I(e, t) {
  const n = [...e],
    o = e.indexOf(t);
  return (-1 !== o && n.splice(o, 1), n);
}
const _ = (() => {
    let e = [];
    return {
      push: (t) => {
        const n = e[0];
        (n && t !== n && n.pause(), (e = I(e, t)), e.unshift(t));
      },
      remove: (t) => {
        var n, o;
        ((e = I(e, t)),
          null == (o = null == (n = e[0]) ? void 0 : n.resume) || o.call(n));
      },
    };
  })(),
  x = () => {
    ((k.value = "pointer"), (g.value = window.performance.now()));
  },
  A = () => {
    ((k.value = "keyboard"), (g.value = window.performance.now()));
  },
  C = (e) =>
    new CustomEvent("focus-trap.focusout-prevented", { ...L, detail: e });
var j = a(
  r({
    name: "ElFocusTrap",
    inheritAttrs: !1,
    props: {
      loop: Boolean,
      trapped: Boolean,
      focusTrapEl: Object,
      focusStartEl: { type: [Object, String], default: "first" },
    },
    emits: [
      h,
      T,
      "focusin",
      "focusout",
      "focusout-prevented",
      "release-requested",
    ],
    setup(a, { emit: r }) {
      const i = s();
      let L, P;
      const { focusReason: I } =
        (e(() => {
          (0 === R &&
            (document.addEventListener("mousedown", x),
            document.addEventListener("touchstart", x),
            document.addEventListener("keydown", A)),
            R++);
        }),
        n(() => {
          (R--,
            R <= 0 &&
              (document.removeEventListener("mousedown", x),
              document.removeEventListener("touchstart", x),
              document.removeEventListener("keydown", A)));
        }),
        {
          focusReason: k,
          lastUserFocusTimestamp: g,
          lastAutomatedFocusTimestamp: F,
        });
      var j;
      ((j = (e) => {
        a.trapped && !O.paused && r("release-requested", e);
      }),
        e(() => {
          (0 === v.length && document.addEventListener("keydown", m),
            t && v.push(j));
        }),
        n(() => {
          ((v = v.filter((e) => e !== j)),
            0 === v.length && t && document.removeEventListener("keydown", m));
        }));
      const O = {
          paused: !1,
          pause() {
            this.paused = !0;
          },
          resume() {
            this.paused = !1;
          },
        },
        q = (e) => {
          if (!a.loop && !a.trapped) return;
          if (O.paused) return;
          const {
              key: t,
              altKey: n,
              ctrlKey: s,
              metaKey: u,
              currentTarget: c,
              shiftKey: d,
            } = e,
            { loop: i } = a,
            l = t === o.tab && !n && !s && !u,
            f = document.activeElement;
          if (l && f) {
            const t = c,
              [n, o] = ((e) => {
                const t = N(e);
                return [K(t, e), K(t.reverse(), e)];
              })(t);
            if (n && o)
              if (d || f !== o) {
                if (d && [n, t].includes(f)) {
                  const t = C({ focusReason: I.value });
                  (r("focusout-prevented", t),
                    t.defaultPrevented || (e.preventDefault(), i && S(o, !0)));
                }
              } else {
                const t = C({ focusReason: I.value });
                (r("focusout-prevented", t),
                  t.defaultPrevented || (e.preventDefault(), i && S(n, !0)));
              }
            else if (f === t) {
              const t = C({ focusReason: I.value });
              (r("focusout-prevented", t),
                t.defaultPrevented || e.preventDefault());
            }
          }
        };
      (u(b, { focusTrapRef: i, onKeydown: q }),
        c(
          () => a.focusTrapEl,
          (e) => {
            e && (i.value = e);
          },
          { immediate: !0 },
        ),
        c([i], ([e], [t]) => {
          (e &&
            (e.addEventListener("keydown", q),
            e.addEventListener("focusin", H),
            e.addEventListener("focusout", M)),
            t &&
              (t.removeEventListener("keydown", q),
              t.removeEventListener("focusin", H),
              t.removeEventListener("focusout", M)));
        }));
      const D = (e) => {
          r(h, e);
        },
        B = (e) => r(T, e),
        H = (e) => {
          const t = d(i);
          if (!t) return;
          const n = e.target,
            o = e.relatedTarget,
            s = n && t.contains(n);
          if (!a.trapped) {
            (o && t.contains(o)) || (L = o);
          }
          (s && r("focusin", e),
            O.paused || (a.trapped && (s ? (P = n) : S(P, !0))));
        },
        M = (e) => {
          const t = d(i);
          if (!O.paused && t)
            if (a.trapped) {
              const n = e.relatedTarget;
              p(n) ||
                t.contains(n) ||
                setTimeout(() => {
                  if (!O.paused && a.trapped) {
                    const e = C({ focusReason: I.value });
                    (r("focusout-prevented", e),
                      e.defaultPrevented || S(P, !0));
                  }
                }, 0);
            } else {
              const n = e.target;
              (n && t.contains(n)) || r("focusout", e);
            }
        };
      async function U() {
        await l();
        const e = d(i);
        if (e) {
          _.push(O);
          const t = e.contains(document.activeElement)
            ? L
            : document.activeElement;
          L = t;
          if (!e.contains(t)) {
            const n = new Event(E, y);
            (e.addEventListener(E, D),
              e.dispatchEvent(n),
              n.defaultPrevented ||
                l(() => {
                  let n = a.focusStartEl;
                  (f(n) ||
                    (S(n), document.activeElement !== n && (n = "first")),
                    "first" === n &&
                      ((e, t = !1) => {
                        const n = document.activeElement;
                        for (const o of e)
                          if ((S(o, t), document.activeElement !== n)) return;
                      })(N(e), !0),
                    (document.activeElement !== t && "container" !== n) ||
                      S(e));
                }));
          }
        }
      }
      function W() {
        const e = d(i);
        if (e) {
          e.removeEventListener(E, D);
          const t = new CustomEvent(w, {
            ...y,
            detail: { focusReason: I.value },
          });
          (e.addEventListener(w, B),
            e.dispatchEvent(t),
            t.defaultPrevented ||
              ("keyboard" != I.value &&
                g.value > F.value &&
                !e.contains(document.activeElement)) ||
              S(null != L ? L : document.body),
            e.removeEventListener(w, B),
            _.remove(O));
        }
      }
      return (
        e(() => {
          (a.trapped && U(),
            c(
              () => a.trapped,
              (e) => {
                e ? U() : W();
              },
            ));
        }),
        n(() => {
          a.trapped && W();
        }),
        { onKeydown: q }
      );
    },
  }),
  [
    [
      "render",
      function (e, t, n, o, s, a) {
        return i(e.$slots, "default", { handleKeydown: e.onKeydown });
      },
    ],
    [
      "__file",
      "/home/runner/work/element-plus/element-plus/packages/components/focus-trap/src/focus-trap.vue",
    ],
  ],
);
export { j as E, b as F };
