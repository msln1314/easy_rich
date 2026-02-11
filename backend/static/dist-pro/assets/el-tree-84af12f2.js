import {
  bg as e,
  L as t,
  ap as n,
  _ as d,
  e as o,
  u as a,
  ao as r,
  a$ as s,
  am as i,
  r as l,
  cp as c,
  cq as h,
  E as u,
  aW as p,
  aq as f,
  w as g,
  as as y,
  cr as k,
  b1 as N,
  a0 as v,
  aH as C,
  o as x,
  j as m,
  y as b,
  l as E,
  m as D,
  p as K,
  s as w,
  aY as S,
  F as A,
  x as B,
  n as L,
  a1 as T,
  a5 as $,
  b3 as _,
  g as O,
  ab as q,
  a2 as z,
  aw as M,
  by as I,
  aA as F,
  a as j,
  a_ as R,
  f as H,
  bo as P,
  q as U,
  z as W,
} from "./index-6b60d190.js";
import { _ as Y } from "./index-55fef7b1.js";
import { E as G } from "./el-checkbox-4903f610.js";
const J = "$treeNodeId",
  Q = function (e, t) {
    t &&
      !t[J] &&
      Object.defineProperty(t, J, {
        value: e.id,
        enumerable: !1,
        configurable: !1,
        writable: !1,
      });
  },
  V = function (e, t) {
    return e ? t[e] : t[J];
  },
  X = (e, t, n) => {
    const d = e.value.currentNode;
    n();
    const o = e.value.currentNode;
    d !== o && t("current-change", o ? o.data : null, o);
  },
  Z = (e) => {
    let t = !0,
      n = !0,
      d = !0;
    for (let o = 0, a = e.length; o < a; o++) {
      const a = e[o];
      ((!0 !== a.checked || a.indeterminate) &&
        ((t = !1), a.disabled || (d = !1)),
        (!1 !== a.checked || a.indeterminate) && (n = !1));
    }
    return { all: t, none: n, allWithoutDisable: d, half: !t && !n };
  },
  ee = function (e) {
    if (0 === e.childNodes.length || e.loading) return;
    const { all: t, none: n, half: d } = Z(e.childNodes);
    t
      ? ((e.checked = !0), (e.indeterminate = !1))
      : d
        ? ((e.checked = !1), (e.indeterminate = !0))
        : n && ((e.checked = !1), (e.indeterminate = !1));
    const o = e.parent;
    o && 0 !== o.level && (e.store.checkStrictly || ee(o));
  },
  te = function (e, t) {
    const n = e.store.props,
      d = e.data || {},
      o = n[t];
    if ("function" == typeof o) return o(d, e);
    if ("string" == typeof o) return d[o];
    if (void 0 === o) {
      const e = d[t];
      return void 0 === e ? "" : e;
    }
  };
let ne = 0;
class de {
  constructor(t) {
    ((this.id = ne++),
      (this.text = null),
      (this.checked = !1),
      (this.indeterminate = !1),
      (this.data = null),
      (this.expanded = !1),
      (this.parent = null),
      (this.visible = !0),
      (this.isCurrent = !1),
      (this.canFocus = !1));
    for (const n in t) e(t, n) && (this[n] = t[n]);
    ((this.level = 0),
      (this.loaded = !1),
      (this.childNodes = []),
      (this.loading = !1),
      this.parent && (this.level = this.parent.level + 1));
  }
  initialize() {
    const e = this.store;
    if (!e) throw new Error("[Node]store is required!");
    e.registerNode(this);
    const t = e.props;
    if (t && void 0 !== t.isLeaf) {
      const e = te(this, "isLeaf");
      "boolean" == typeof e && (this.isLeafByUser = e);
    }
    if (
      (!0 !== e.lazy && this.data
        ? (this.setData(this.data),
          e.defaultExpandAll && ((this.expanded = !0), (this.canFocus = !0)))
        : this.level > 0 && e.lazy && e.defaultExpandAll && this.expand(),
      Array.isArray(this.data) || Q(this, this.data),
      !this.data)
    )
      return;
    const n = e.defaultExpandedKeys,
      d = e.key;
    (d && n && n.includes(this.key) && this.expand(null, e.autoExpandParent),
      d &&
        void 0 !== e.currentNodeKey &&
        this.key === e.currentNodeKey &&
        ((e.currentNode = this), (e.currentNode.isCurrent = !0)),
      e.lazy && e._initDefaultCheckedNode(this),
      this.updateLeafState(),
      !this.parent ||
        (1 !== this.level && !0 !== this.parent.expanded) ||
        (this.canFocus = !0));
  }
  setData(e) {
    let t;
    (Array.isArray(e) || Q(this, e),
      (this.data = e),
      (this.childNodes = []),
      (t =
        0 === this.level && Array.isArray(this.data)
          ? this.data
          : te(this, "children") || []));
    for (let n = 0, d = t.length; n < d; n++) this.insertChild({ data: t[n] });
  }
  get label() {
    return te(this, "label");
  }
  get key() {
    const e = this.store.key;
    return this.data ? this.data[e] : null;
  }
  get disabled() {
    return te(this, "disabled");
  }
  get nextSibling() {
    const e = this.parent;
    if (e) {
      const t = e.childNodes.indexOf(this);
      if (t > -1) return e.childNodes[t + 1];
    }
    return null;
  }
  get previousSibling() {
    const e = this.parent;
    if (e) {
      const t = e.childNodes.indexOf(this);
      if (t > -1) return t > 0 ? e.childNodes[t - 1] : null;
    }
    return null;
  }
  contains(e, t = !0) {
    return (this.childNodes || []).some((n) => n === e || (t && n.contains(e)));
  }
  remove() {
    const e = this.parent;
    e && e.removeChild(this);
  }
  insertChild(e, n, d) {
    if (!e) throw new Error("InsertChild error: child is required.");
    if (!(e instanceof de)) {
      if (!d) {
        const t = this.getChildren(!0);
        t.includes(e.data) ||
          (void 0 === n || n < 0 ? t.push(e.data) : t.splice(n, 0, e.data));
      }
      (Object.assign(e, { parent: this, store: this.store }),
        (e = t(new de(e))) instanceof de && e.initialize());
    }
    ((e.level = this.level + 1),
      void 0 === n || n < 0
        ? this.childNodes.push(e)
        : this.childNodes.splice(n, 0, e),
      this.updateLeafState());
  }
  insertBefore(e, t) {
    let n;
    (t && (n = this.childNodes.indexOf(t)), this.insertChild(e, n));
  }
  insertAfter(e, t) {
    let n;
    (t && ((n = this.childNodes.indexOf(t)), -1 !== n && (n += 1)),
      this.insertChild(e, n));
  }
  removeChild(e) {
    const t = this.getChildren() || [],
      n = t.indexOf(e.data);
    n > -1 && t.splice(n, 1);
    const d = this.childNodes.indexOf(e);
    (d > -1 &&
      (this.store && this.store.deregisterNode(e),
      (e.parent = null),
      this.childNodes.splice(d, 1)),
      this.updateLeafState());
  }
  removeChildByData(e) {
    let t = null;
    for (let n = 0; n < this.childNodes.length; n++)
      if (this.childNodes[n].data === e) {
        t = this.childNodes[n];
        break;
      }
    t && this.removeChild(t);
  }
  expand(e, t) {
    const n = () => {
      if (t) {
        let e = this.parent;
        for (; e.level > 0; ) ((e.expanded = !0), (e = e.parent));
      }
      ((this.expanded = !0),
        e && e(),
        this.childNodes.forEach((e) => {
          e.canFocus = !0;
        }));
    };
    this.shouldLoadData()
      ? this.loadData((e) => {
          Array.isArray(e) &&
            (this.checked
              ? this.setChecked(!0, !0)
              : this.store.checkStrictly || ee(this),
            n());
        })
      : n();
  }
  doCreateChildren(e, t = {}) {
    e.forEach((e) => {
      this.insertChild(Object.assign({ data: e }, t), void 0, !0);
    });
  }
  collapse() {
    ((this.expanded = !1),
      this.childNodes.forEach((e) => {
        e.canFocus = !1;
      }));
  }
  shouldLoadData() {
    return !0 === this.store.lazy && this.store.load && !this.loaded;
  }
  updateLeafState() {
    if (
      !0 === this.store.lazy &&
      !0 !== this.loaded &&
      void 0 !== this.isLeafByUser
    )
      return void (this.isLeaf = this.isLeafByUser);
    const e = this.childNodes;
    !this.store.lazy || (!0 === this.store.lazy && !0 === this.loaded)
      ? (this.isLeaf = !e || 0 === e.length)
      : (this.isLeaf = !1);
  }
  setChecked(e, t, n, d) {
    if (
      ((this.indeterminate = "half" === e),
      (this.checked = !0 === e),
      this.store.checkStrictly)
    )
      return;
    if (!this.shouldLoadData() || this.store.checkDescendants) {
      const { all: n, allWithoutDisable: o } = Z(this.childNodes);
      this.isLeaf || n || !o || ((this.checked = !1), (e = !1));
      const a = () => {
        if (t) {
          const n = this.childNodes;
          for (let r = 0, s = n.length; r < s; r++) {
            const o = n[r];
            d = d || !1 !== e;
            const a = o.disabled ? o.checked : d;
            o.setChecked(a, t, !0, d);
          }
          const { half: o, all: a } = Z(n);
          a || ((this.checked = a), (this.indeterminate = o));
        }
      };
      if (this.shouldLoadData())
        return void this.loadData(
          () => {
            (a(), ee(this));
          },
          { checked: !1 !== e },
        );
      a();
    }
    const o = this.parent;
    o && 0 !== o.level && (n || ee(o));
  }
  getChildren(e = !1) {
    if (0 === this.level) return this.data;
    const t = this.data;
    if (!t) return null;
    const n = this.store.props;
    let d = "children";
    return (
      n && (d = n.children || "children"),
      void 0 === t[d] && (t[d] = null),
      e && !t[d] && (t[d] = []),
      t[d]
    );
  }
  updateChildren() {
    const e = this.getChildren() || [],
      t = this.childNodes.map((e) => e.data),
      n = {},
      d = [];
    (e.forEach((e, o) => {
      const a = e[J];
      !!a && t.findIndex((e) => e[J] === a) >= 0
        ? (n[a] = { index: o, data: e })
        : d.push({ index: o, data: e });
    }),
      this.store.lazy ||
        t.forEach((e) => {
          n[e[J]] || this.removeChildByData(e);
        }),
      d.forEach(({ index: e, data: t }) => {
        this.insertChild({ data: t }, e);
      }),
      this.updateLeafState());
  }
  loadData(e, t = {}) {
    if (
      !0 !== this.store.lazy ||
      !this.store.load ||
      this.loaded ||
      (this.loading && !Object.keys(t).length)
    )
      e && e.call(this);
    else {
      this.loading = !0;
      const n = (n) => {
        ((this.childNodes = []),
          this.doCreateChildren(n, t),
          (this.loaded = !0),
          (this.loading = !1),
          this.updateLeafState(),
          e && e.call(this, n));
      };
      this.store.load(this, n);
    }
  }
}
class oe {
  constructor(t) {
    ((this.currentNode = null), (this.currentNodeKey = null));
    for (const n in t) e(t, n) && (this[n] = t[n]);
    this.nodesMap = {};
  }
  initialize() {
    if (
      ((this.root = new de({ data: this.data, store: this })),
      this.root.initialize(),
      this.lazy && this.load)
    ) {
      (0, this.load)(this.root, (e) => {
        (this.root.doCreateChildren(e), this._initDefaultCheckedNodes());
      });
    } else this._initDefaultCheckedNodes();
  }
  filter(e) {
    const t = this.filterNodeMethod,
      n = this.lazy,
      d = function (o) {
        const a = o.root ? o.root.childNodes : o.childNodes;
        if (
          (a.forEach((n) => {
            ((n.visible = t.call(n, e, n.data, n)), d(n));
          }),
          !o.visible && a.length)
        ) {
          let e = !0;
          ((e = !a.some((e) => e.visible)),
            o.root ? (o.root.visible = !1 === e) : (o.visible = !1 === e));
        }
        e && (!o.visible || o.isLeaf || n || o.expand());
      };
    d(this);
  }
  setData(e) {
    e !== this.root.data
      ? (this.root.setData(e), this._initDefaultCheckedNodes())
      : this.root.updateChildren();
  }
  getNode(e) {
    if (e instanceof de) return e;
    const t = n(e) ? V(this.key, e) : e;
    return this.nodesMap[t] || null;
  }
  insertBefore(e, t) {
    const n = this.getNode(t);
    n.parent.insertBefore({ data: e }, n);
  }
  insertAfter(e, t) {
    const n = this.getNode(t);
    n.parent.insertAfter({ data: e }, n);
  }
  remove(e) {
    const t = this.getNode(e);
    t &&
      t.parent &&
      (t === this.currentNode && (this.currentNode = null),
      t.parent.removeChild(t));
  }
  append(e, t) {
    const n = t ? this.getNode(t) : this.root;
    n && n.insertChild({ data: e });
  }
  _initDefaultCheckedNodes() {
    const e = this.defaultCheckedKeys || [],
      t = this.nodesMap;
    e.forEach((e) => {
      const n = t[e];
      n && n.setChecked(!0, !this.checkStrictly);
    });
  }
  _initDefaultCheckedNode(e) {
    (this.defaultCheckedKeys || []).includes(e.key) &&
      e.setChecked(!0, !this.checkStrictly);
  }
  setDefaultCheckedKey(e) {
    e !== this.defaultCheckedKeys &&
      ((this.defaultCheckedKeys = e), this._initDefaultCheckedNodes());
  }
  registerNode(e) {
    const t = this.key;
    if (e && e.data)
      if (t) {
        void 0 !== e.key && (this.nodesMap[e.key] = e);
      } else this.nodesMap[e.id] = e;
  }
  deregisterNode(e) {
    this.key &&
      e &&
      e.data &&
      (e.childNodes.forEach((e) => {
        this.deregisterNode(e);
      }),
      delete this.nodesMap[e.key]);
  }
  getCheckedNodes(e = !1, t = !1) {
    const n = [],
      d = function (o) {
        (o.root ? o.root.childNodes : o.childNodes).forEach((o) => {
          ((o.checked || (t && o.indeterminate)) &&
            (!e || (e && o.isLeaf)) &&
            n.push(o.data),
            d(o));
        });
      };
    return (d(this), n);
  }
  getCheckedKeys(e = !1) {
    return this.getCheckedNodes(e).map((e) => (e || {})[this.key]);
  }
  getHalfCheckedNodes() {
    const e = [],
      t = function (n) {
        (n.root ? n.root.childNodes : n.childNodes).forEach((n) => {
          (n.indeterminate && e.push(n.data), t(n));
        });
      };
    return (t(this), e);
  }
  getHalfCheckedKeys() {
    return this.getHalfCheckedNodes().map((e) => (e || {})[this.key]);
  }
  _getAllNodes() {
    const t = [],
      n = this.nodesMap;
    for (const d in n) e(n, d) && t.push(n[d]);
    return t;
  }
  updateChildren(e, t) {
    const n = this.nodesMap[e];
    if (!n) return;
    const d = n.childNodes;
    for (let o = d.length - 1; o >= 0; o--) {
      const e = d[o];
      this.remove(e.data);
    }
    for (let o = 0, a = t.length; o < a; o++) {
      const e = t[o];
      this.append(e, n.data);
    }
  }
  _setCheckedKeys(e, t = !1, n) {
    const d = this._getAllNodes().sort((e, t) => t.level - e.level),
      o = Object.create(null),
      a = Object.keys(n);
    d.forEach((e) => e.setChecked(!1, !1));
    for (let r = 0, s = d.length; r < s; r++) {
      const n = d[r],
        s = n.data[e].toString();
      if (!a.includes(s)) {
        n.checked && !o[s] && n.setChecked(!1, !1);
        continue;
      }
      let i = n.parent;
      for (; i && i.level > 0; ) ((o[i.data[e]] = !0), (i = i.parent));
      if (n.isLeaf || this.checkStrictly) n.setChecked(!0, !1);
      else if ((n.setChecked(!0, !0), t)) {
        n.setChecked(!1, !1);
        const e = function (t) {
          t.childNodes.forEach((t) => {
            (t.isLeaf || t.setChecked(!1, !1), e(t));
          });
        };
        e(n);
      }
    }
  }
  setCheckedNodes(e, t = !1) {
    const n = this.key,
      d = {};
    (e.forEach((e) => {
      d[(e || {})[n]] = !0;
    }),
      this._setCheckedKeys(n, t, d));
  }
  setCheckedKeys(e, t = !1) {
    this.defaultCheckedKeys = e;
    const n = this.key,
      d = {};
    (e.forEach((e) => {
      d[e] = !0;
    }),
      this._setCheckedKeys(n, t, d));
  }
  setDefaultExpandedKeys(e) {
    ((e = e || []),
      (this.defaultExpandedKeys = e),
      e.forEach((e) => {
        const t = this.getNode(e);
        t && t.expand(null, this.autoExpandParent);
      }));
  }
  setChecked(e, t, n) {
    const d = this.getNode(e);
    d && d.setChecked(!!t, n);
  }
  getCurrentNode() {
    return this.currentNode;
  }
  setCurrentNode(e) {
    const t = this.currentNode;
    (t && (t.isCurrent = !1),
      (this.currentNode = e),
      (this.currentNode.isCurrent = !0));
  }
  setUserCurrentNode(e, t = !0) {
    const n = e[this.key],
      d = this.nodesMap[n];
    (this.setCurrentNode(d),
      t &&
        this.currentNode.level > 1 &&
        this.currentNode.parent.expand(null, !0));
  }
  setCurrentNodeKey(e, t = !0) {
    if (null == e)
      return (
        this.currentNode && (this.currentNode.isCurrent = !1),
        void (this.currentNode = null)
      );
    const n = this.getNode(e);
    n &&
      (this.setCurrentNode(n),
      t &&
        this.currentNode.level > 1 &&
        this.currentNode.parent.expand(null, !0));
  }
}
var ae = d(
  o({
    name: "ElTreeNodeContent",
    props: { node: { type: Object, required: !0 }, renderContent: Function },
    setup(e) {
      const t = a("tree"),
        n = r("NodeInstance"),
        d = r("RootTree");
      return () => {
        const o = e.node,
          { data: a, store: r } = o;
        return e.renderContent
          ? e.renderContent(s, { _self: n, node: o, data: a, store: r })
          : d.ctx.slots.default
            ? d.ctx.slots.default({ node: o, data: a })
            : s("span", { class: t.be("node", "label") }, [o.label]);
      };
    },
  }),
  [
    [
      "__file",
      "/home/runner/work/element-plus/element-plus/packages/components/tree/src/tree-node-content.vue",
    ],
  ],
);
function re(e) {
  const t = r("TreeNodeMap", null),
    n = {
      treeNodeExpand: (t) => {
        e.node !== t && e.node.collapse();
      },
      children: [],
    };
  return (
    t && t.children.push(n),
    i("TreeNodeMap", n),
    {
      broadcastExpanded: (t) => {
        if (e.accordion) for (const e of n.children) e.treeNodeExpand(t);
      },
    }
  );
}
const se = Symbol("dragEvents");
const ie = o({
    name: "ElTreeNode",
    components: {
      ElCollapseTransition: Y,
      ElCheckbox: G,
      NodeContent: ae,
      ElIcon: u,
      Loading: p,
    },
    props: {
      node: { type: de, default: () => ({}) },
      props: { type: Object, default: () => ({}) },
      accordion: Boolean,
      renderContent: Function,
      renderAfterExpand: Boolean,
      showCheckbox: { type: Boolean, default: !1 },
    },
    emits: ["node-expand"],
    setup(e, t) {
      const n = a("tree"),
        { broadcastExpanded: d } = re(e),
        o = r("RootTree"),
        s = l(!1),
        c = l(!1),
        h = l(null),
        u = l(null),
        p = l(null),
        N = r(se),
        v = f();
      (i("NodeInstance", v),
        e.node.expanded && ((s.value = !0), (c.value = !0)));
      const C = o.props.children || "children";
      (g(
        () => {
          const t = e.node.data[C];
          return t && [...t];
        },
        () => {
          e.node.updateChildren();
        },
      ),
        g(
          () => e.node.indeterminate,
          (t) => {
            x(e.node.checked, t);
          },
        ),
        g(
          () => e.node.checked,
          (t) => {
            x(t, e.node.indeterminate);
          },
        ),
        g(
          () => e.node.expanded,
          (e) => {
            (y(() => (s.value = e)), e && (c.value = !0));
          },
        ));
      const x = (t, n) => {
          ((h.value === t && u.value === n) ||
            o.ctx.emit("check-change", e.node.data, t, n),
            (h.value = t),
            (u.value = n));
        },
        m = () => {
          e.node.isLeaf ||
            (s.value
              ? (o.ctx.emit("node-collapse", e.node.data, e.node, v),
                e.node.collapse())
              : (e.node.expand(),
                t.emit("node-expand", e.node.data, e.node, v)));
        },
        b = (t, n) => {
          (e.node.setChecked(n.target.checked, !o.props.checkStrictly),
            y(() => {
              const t = o.store.value;
              o.ctx.emit("check", e.node.data, {
                checkedNodes: t.getCheckedNodes(),
                checkedKeys: t.getCheckedKeys(),
                halfCheckedNodes: t.getHalfCheckedNodes(),
                halfCheckedKeys: t.getHalfCheckedKeys(),
              });
            }));
        };
      return {
        ns: n,
        node$: p,
        tree: o,
        expanded: s,
        childNodeRendered: c,
        oldChecked: h,
        oldIndeterminate: u,
        getNodeKey: (e) => V(o.props.nodeKey, e.data),
        getNodeClass: (t) => {
          const n = e.props.class;
          if (!n) return {};
          let d;
          if (_(n)) {
            const { data: e } = t;
            d = n(e, t);
          } else d = n;
          return O(d) ? { [d]: !0 } : d;
        },
        handleSelectChange: x,
        handleClick: (t) => {
          (X(o.store, o.ctx.emit, () => o.store.value.setCurrentNode(e.node)),
            (o.currentNode.value = e.node),
            o.props.expandOnClickNode && m(),
            o.props.checkOnClickNode &&
              !e.node.disabled &&
              b(null, { target: { checked: !e.node.checked } }),
            o.ctx.emit("node-click", e.node.data, e.node, v, t));
        },
        handleContextMenu: (t) => {
          (o.instance.vnode.props.onNodeContextmenu &&
            (t.stopPropagation(), t.preventDefault()),
            o.ctx.emit("node-contextmenu", t, e.node.data, e.node, v));
        },
        handleExpandIconClick: m,
        handleCheckChange: b,
        handleChildNodeExpand: (e, t, n) => {
          (d(t), o.ctx.emit("node-expand", e, t, n));
        },
        handleDragStart: (t) => {
          o.props.draggable && N.treeNodeDragStart({ event: t, treeNode: e });
        },
        handleDragOver: (t) => {
          (t.preventDefault(),
            o.props.draggable &&
              N.treeNodeDragOver({
                event: t,
                treeNode: { $el: p.value, node: e.node },
              }));
        },
        handleDrop: (e) => {
          e.preventDefault();
        },
        handleDragEnd: (e) => {
          o.props.draggable && N.treeNodeDragEnd(e);
        },
        CaretRight: k,
      };
    },
  }),
  le = [
    "aria-expanded",
    "aria-disabled",
    "aria-checked",
    "draggable",
    "data-key",
  ],
  ce = ["aria-expanded"];
var he = d(
  o({
    name: "ElTree",
    components: {
      ElTreeNode: d(ie, [
        [
          "render",
          function (e, t, n, d, o, a) {
            const r = N("el-icon"),
              s = N("el-checkbox"),
              i = N("loading"),
              l = N("node-content"),
              c = N("el-tree-node"),
              h = N("el-collapse-transition");
            return v(
              (x(),
              m(
                "div",
                {
                  ref: "node$",
                  class: w([
                    e.ns.b("node"),
                    e.ns.is("expanded", e.expanded),
                    e.ns.is("current", e.node.isCurrent),
                    e.ns.is("hidden", !e.node.visible),
                    e.ns.is("focusable", !e.node.disabled),
                    e.ns.is("checked", !e.node.disabled && e.node.checked),
                    e.getNodeClass(e.node),
                  ]),
                  role: "treeitem",
                  tabindex: "-1",
                  "aria-expanded": e.expanded,
                  "aria-disabled": e.node.disabled,
                  "aria-checked": e.node.checked,
                  draggable: e.tree.props.draggable,
                  "data-key": e.getNodeKey(e.node),
                  onClick:
                    t[1] ||
                    (t[1] = S(
                      (...t) => e.handleClick && e.handleClick(...t),
                      ["stop"],
                    )),
                  onContextmenu:
                    t[2] ||
                    (t[2] = (...t) =>
                      e.handleContextMenu && e.handleContextMenu(...t)),
                  onDragstart:
                    t[3] ||
                    (t[3] = S(
                      (...t) => e.handleDragStart && e.handleDragStart(...t),
                      ["stop"],
                    )),
                  onDragover:
                    t[4] ||
                    (t[4] = S(
                      (...t) => e.handleDragOver && e.handleDragOver(...t),
                      ["stop"],
                    )),
                  onDragend:
                    t[5] ||
                    (t[5] = S(
                      (...t) => e.handleDragEnd && e.handleDragEnd(...t),
                      ["stop"],
                    )),
                  onDrop:
                    t[6] ||
                    (t[6] = S(
                      (...t) => e.handleDrop && e.handleDrop(...t),
                      ["stop"],
                    )),
                },
                [
                  b(
                    "div",
                    {
                      class: w(e.ns.be("node", "content")),
                      style: L({
                        paddingLeft:
                          (e.node.level - 1) * e.tree.props.indent + "px",
                      }),
                    },
                    [
                      e.tree.props.icon || e.CaretRight
                        ? (x(),
                          E(
                            r,
                            {
                              key: 0,
                              class: w([
                                e.ns.be("node", "expand-icon"),
                                e.ns.is("leaf", e.node.isLeaf),
                                { expanded: !e.node.isLeaf && e.expanded },
                              ]),
                              onClick: S(e.handleExpandIconClick, ["stop"]),
                            },
                            {
                              default: D(() => [
                                (x(), E(K(e.tree.props.icon || e.CaretRight))),
                              ]),
                              _: 1,
                            },
                            8,
                            ["class", "onClick"],
                          ))
                        : A("v-if", !0),
                      e.showCheckbox
                        ? (x(),
                          E(
                            s,
                            {
                              key: 1,
                              "model-value": e.node.checked,
                              indeterminate: e.node.indeterminate,
                              disabled: !!e.node.disabled,
                              onClick: t[0] || (t[0] = S(() => {}, ["stop"])),
                              onChange: e.handleCheckChange,
                            },
                            null,
                            8,
                            [
                              "model-value",
                              "indeterminate",
                              "disabled",
                              "onChange",
                            ],
                          ))
                        : A("v-if", !0),
                      e.node.loading
                        ? (x(),
                          E(
                            r,
                            {
                              key: 2,
                              class: w([
                                e.ns.be("node", "loading-icon"),
                                e.ns.is("loading"),
                              ]),
                            },
                            { default: D(() => [B(i)]), _: 1 },
                            8,
                            ["class"],
                          ))
                        : A("v-if", !0),
                      B(
                        l,
                        { node: e.node, "render-content": e.renderContent },
                        null,
                        8,
                        ["node", "render-content"],
                      ),
                    ],
                    6,
                  ),
                  B(h, null, {
                    default: D(() => [
                      !e.renderAfterExpand || e.childNodeRendered
                        ? v(
                            (x(),
                            m(
                              "div",
                              {
                                key: 0,
                                class: w(e.ns.be("node", "children")),
                                role: "group",
                                "aria-expanded": e.expanded,
                              },
                              [
                                (x(!0),
                                m(
                                  T,
                                  null,
                                  $(
                                    e.node.childNodes,
                                    (t) => (
                                      x(),
                                      E(
                                        c,
                                        {
                                          key: e.getNodeKey(t),
                                          "render-content": e.renderContent,
                                          "render-after-expand":
                                            e.renderAfterExpand,
                                          "show-checkbox": e.showCheckbox,
                                          node: t,
                                          accordion: e.accordion,
                                          props: e.props,
                                          onNodeExpand: e.handleChildNodeExpand,
                                        },
                                        null,
                                        8,
                                        [
                                          "render-content",
                                          "render-after-expand",
                                          "show-checkbox",
                                          "node",
                                          "accordion",
                                          "props",
                                          "onNodeExpand",
                                        ],
                                      )
                                    ),
                                  ),
                                  128,
                                )),
                              ],
                              10,
                              ce,
                            )),
                            [[C, e.expanded]],
                          )
                        : A("v-if", !0),
                    ]),
                    _: 1,
                  }),
                ],
                42,
                le,
              )),
              [[C, e.node.visible]],
            );
          },
        ],
        [
          "__file",
          "/home/runner/work/element-plus/element-plus/packages/components/tree/src/tree-node.vue",
        ],
      ]),
    },
    props: {
      data: { type: Array, default: () => [] },
      emptyText: { type: String },
      renderAfterExpand: { type: Boolean, default: !0 },
      nodeKey: String,
      checkStrictly: Boolean,
      defaultExpandAll: Boolean,
      expandOnClickNode: { type: Boolean, default: !0 },
      checkOnClickNode: Boolean,
      checkDescendants: { type: Boolean, default: !1 },
      autoExpandParent: { type: Boolean, default: !0 },
      defaultCheckedKeys: Array,
      defaultExpandedKeys: Array,
      currentNodeKey: [String, Number],
      renderContent: Function,
      showCheckbox: { type: Boolean, default: !1 },
      draggable: { type: Boolean, default: !1 },
      allowDrag: Function,
      allowDrop: Function,
      props: {
        type: Object,
        default: () => ({
          children: "children",
          label: "label",
          disabled: "disabled",
        }),
      },
      lazy: { type: Boolean, default: !1 },
      highlightCurrent: Boolean,
      load: Function,
      filterNodeMethod: Function,
      accordion: Boolean,
      indent: { type: Number, default: 18 },
      icon: { type: j },
    },
    emits: [
      "check-change",
      "current-change",
      "node-click",
      "node-contextmenu",
      "node-collapse",
      "node-expand",
      "check",
      "node-drag-start",
      "node-drag-end",
      "node-drop",
      "node-drag-leave",
      "node-drag-enter",
      "node-drag-over",
    ],
    setup(e, t) {
      const { t: n } = R(),
        d = a("tree"),
        o = l(
          new oe({
            key: e.nodeKey,
            data: e.data,
            lazy: e.lazy,
            props: e.props,
            load: e.load,
            currentNodeKey: e.currentNodeKey,
            checkStrictly: e.checkStrictly,
            checkDescendants: e.checkDescendants,
            defaultCheckedKeys: e.defaultCheckedKeys,
            defaultExpandedKeys: e.defaultExpandedKeys,
            autoExpandParent: e.autoExpandParent,
            defaultExpandAll: e.defaultExpandAll,
            filterNodeMethod: e.filterNodeMethod,
          }),
        );
      o.value.initialize();
      const r = l(o.value.root),
        s = l(null),
        u = l(null),
        p = l(null),
        { broadcastExpanded: y } = re(e),
        { dragState: k } = (function ({
          props: e,
          ctx: t,
          el$: n,
          dropIndicator$: d,
          store: o,
        }) {
          const r = a("tree"),
            s = l({
              showDropIndicator: !1,
              draggingNode: null,
              dropNode: null,
              allowDrop: !0,
              dropType: null,
            });
          return (
            i(se, {
              treeNodeDragStart: ({ event: n, treeNode: d }) => {
                if ("function" == typeof e.allowDrag && !e.allowDrag(d.node))
                  return (n.preventDefault(), !1);
                n.dataTransfer.effectAllowed = "move";
                try {
                  n.dataTransfer.setData("text/plain", "");
                } catch (o) {}
                ((s.value.draggingNode = d),
                  t.emit("node-drag-start", d.node, n));
              },
              treeNodeDragOver: ({ event: o, treeNode: a }) => {
                const i = a,
                  l = s.value.dropNode;
                l && l.node.id !== i.node.id && c(l.$el, r.is("drop-inner"));
                const u = s.value.draggingNode;
                if (!u || !i) return;
                let p = !0,
                  f = !0,
                  g = !0,
                  y = !0;
                ("function" == typeof e.allowDrop &&
                  ((p = e.allowDrop(u.node, i.node, "prev")),
                  (y = f = e.allowDrop(u.node, i.node, "inner")),
                  (g = e.allowDrop(u.node, i.node, "next"))),
                  (o.dataTransfer.dropEffect = f || p || g ? "move" : "none"),
                  (p || f || g) &&
                    (null == l ? void 0 : l.node.id) !== i.node.id &&
                    (l && t.emit("node-drag-leave", u.node, l.node, o),
                    t.emit("node-drag-enter", u.node, i.node, o)),
                  (p || f || g) && (s.value.dropNode = i),
                  i.node.nextSibling === u.node && (g = !1),
                  i.node.previousSibling === u.node && (p = !1),
                  i.node.contains(u.node, !1) && (f = !1),
                  (u.node === i.node || u.node.contains(i.node)) &&
                    ((p = !1), (f = !1), (g = !1)));
                const k = i.$el
                    .querySelector(`.${r.be("node", "content")}`)
                    .getBoundingClientRect(),
                  N = n.value.getBoundingClientRect();
                let v;
                const C = p ? (f ? 0.25 : g ? 0.45 : 1) : -1,
                  x = g ? (f ? 0.75 : p ? 0.55 : 0) : 1;
                let m = -9999;
                const b = o.clientY - k.top;
                v =
                  b < k.height * C
                    ? "before"
                    : b > k.height * x
                      ? "after"
                      : f
                        ? "inner"
                        : "none";
                const E = i.$el
                    .querySelector(`.${r.be("node", "expand-icon")}`)
                    .getBoundingClientRect(),
                  D = d.value;
                ("before" === v
                  ? (m = E.top - N.top)
                  : "after" === v && (m = E.bottom - N.top),
                  (D.style.top = `${m}px`),
                  (D.style.left = E.right - N.left + "px"),
                  "inner" === v
                    ? h(i.$el, r.is("drop-inner"))
                    : c(i.$el, r.is("drop-inner")),
                  (s.value.showDropIndicator = "before" === v || "after" === v),
                  (s.value.allowDrop = s.value.showDropIndicator || y),
                  (s.value.dropType = v),
                  t.emit("node-drag-over", u.node, i.node, o));
              },
              treeNodeDragEnd: (e) => {
                const { draggingNode: n, dropType: d, dropNode: a } = s.value;
                if (
                  (e.preventDefault(),
                  (e.dataTransfer.dropEffect = "move"),
                  n && a)
                ) {
                  const s = { data: n.node.data };
                  ("none" !== d && n.node.remove(),
                    "before" === d
                      ? a.node.parent.insertBefore(s, a.node)
                      : "after" === d
                        ? a.node.parent.insertAfter(s, a.node)
                        : "inner" === d && a.node.insertChild(s),
                    "none" !== d && o.value.registerNode(s),
                    c(a.$el, r.is("drop-inner")),
                    t.emit("node-drag-end", n.node, a.node, d, e),
                    "none" !== d && t.emit("node-drop", n.node, a.node, d, e));
                }
                (n && !a && t.emit("node-drag-end", n.node, null, d, e),
                  (s.value.showDropIndicator = !1),
                  (s.value.draggingNode = null),
                  (s.value.dropNode = null),
                  (s.value.allowDrop = !0));
              },
            }),
            { dragState: s }
          );
        })({ props: e, ctx: t, el$: u, dropIndicator$: p, store: o });
      !(function ({ el$: e }, t) {
        const n = a("tree"),
          d = q([]),
          o = q([]);
        (z(() => {
          r();
        }),
          M(() => {
            ((d.value = Array.from(
              e.value.querySelectorAll("[role=treeitem]"),
            )),
              (o.value = Array.from(
                e.value.querySelectorAll("input[type=checkbox]"),
              )));
          }),
          g(o, (e) => {
            e.forEach((e) => {
              e.setAttribute("tabindex", "-1");
            });
          }),
          I(e, "keydown", (o) => {
            const a = o.target;
            if (!a.className.includes(n.b("node"))) return;
            const r = o.code;
            d.value = Array.from(
              e.value.querySelectorAll(`.${n.is("focusable")}[role=treeitem]`),
            );
            const s = d.value.indexOf(a);
            let i;
            if ([F.up, F.down].includes(r)) {
              if ((o.preventDefault(), r === F.up)) {
                i = -1 === s ? 0 : 0 !== s ? s - 1 : d.value.length - 1;
                const e = i;
                for (; !t.value.getNode(d.value[i].dataset.key).canFocus; ) {
                  if ((i--, i === e)) {
                    i = -1;
                    break;
                  }
                  i < 0 && (i = d.value.length - 1);
                }
              } else {
                i = -1 === s ? 0 : s < d.value.length - 1 ? s + 1 : 0;
                const e = i;
                for (; !t.value.getNode(d.value[i].dataset.key).canFocus; ) {
                  if ((i++, i === e)) {
                    i = -1;
                    break;
                  }
                  i >= d.value.length && (i = 0);
                }
              }
              -1 !== i && d.value[i].focus();
            }
            [F.left, F.right].includes(r) && (o.preventDefault(), a.click());
            const l = a.querySelector('[type="checkbox"]');
            [F.enter, F.space].includes(r) &&
              l &&
              (o.preventDefault(), l.click());
          }));
        const r = () => {
          var t;
          ((d.value = Array.from(
            e.value.querySelectorAll(`.${n.is("focusable")}[role=treeitem]`),
          )),
            (o.value = Array.from(
              e.value.querySelectorAll("input[type=checkbox]"),
            )));
          const a = e.value.querySelectorAll(
            `.${n.is("checked")}[role=treeitem]`,
          );
          a.length
            ? a[0].setAttribute("tabindex", "0")
            : null == (t = d.value[0]) || t.setAttribute("tabindex", "0");
        };
      })({ el$: u }, o);
      const N = H(() => {
        const { childNodes: e } = r.value;
        return !e || 0 === e.length || e.every(({ visible: e }) => !e);
      });
      (g(
        () => e.currentNodeKey,
        (e) => {
          o.value.setCurrentNodeKey(e);
        },
      ),
        g(
          () => e.defaultCheckedKeys,
          (e) => {
            o.value.setDefaultCheckedKey(e);
          },
        ),
        g(
          () => e.defaultExpandedKeys,
          (e) => {
            o.value.setDefaultExpandedKeys(e);
          },
        ),
        g(
          () => e.data,
          (e) => {
            o.value.setData(e);
          },
          { deep: !0 },
        ),
        g(
          () => e.checkStrictly,
          (e) => {
            o.value.checkStrictly = e;
          },
        ));
      const v = () => {
        const e = o.value.getCurrentNode();
        return e ? e.data : null;
      };
      return (
        i("RootTree", {
          ctx: t,
          props: e,
          store: o,
          root: r,
          currentNode: s,
          instance: f(),
        }),
        i(P, void 0),
        {
          ns: d,
          store: o,
          root: r,
          currentNode: s,
          dragState: k,
          el$: u,
          dropIndicator$: p,
          isEmpty: N,
          filter: (t) => {
            if (!e.filterNodeMethod)
              throw new Error(
                "[Tree] filterNodeMethod is required when filter",
              );
            o.value.filter(t);
          },
          getNodeKey: (t) => V(e.nodeKey, t.data),
          getNodePath: (t) => {
            if (!e.nodeKey)
              throw new Error("[Tree] nodeKey is required in getNodePath");
            const n = o.value.getNode(t);
            if (!n) return [];
            const d = [n.data];
            let a = n.parent;
            for (; a && a !== r.value; ) (d.push(a.data), (a = a.parent));
            return d.reverse();
          },
          getCheckedNodes: (e, t) => o.value.getCheckedNodes(e, t),
          getCheckedKeys: (e) => o.value.getCheckedKeys(e),
          getCurrentNode: v,
          getCurrentKey: () => {
            if (!e.nodeKey)
              throw new Error("[Tree] nodeKey is required in getCurrentKey");
            const t = v();
            return t ? t[e.nodeKey] : null;
          },
          setCheckedNodes: (t, n) => {
            if (!e.nodeKey)
              throw new Error("[Tree] nodeKey is required in setCheckedNodes");
            o.value.setCheckedNodes(t, n);
          },
          setCheckedKeys: (t, n) => {
            if (!e.nodeKey)
              throw new Error("[Tree] nodeKey is required in setCheckedKeys");
            o.value.setCheckedKeys(t, n);
          },
          setChecked: (e, t, n) => {
            o.value.setChecked(e, t, n);
          },
          getHalfCheckedNodes: () => o.value.getHalfCheckedNodes(),
          getHalfCheckedKeys: () => o.value.getHalfCheckedKeys(),
          setCurrentNode: (n, d = !0) => {
            if (!e.nodeKey)
              throw new Error("[Tree] nodeKey is required in setCurrentNode");
            X(o, t.emit, () => o.value.setUserCurrentNode(n, d));
          },
          setCurrentKey: (n, d = !0) => {
            if (!e.nodeKey)
              throw new Error("[Tree] nodeKey is required in setCurrentKey");
            X(o, t.emit, () => o.value.setCurrentNodeKey(n, d));
          },
          t: n,
          getNode: (e) => o.value.getNode(e),
          remove: (e) => {
            o.value.remove(e);
          },
          append: (e, t) => {
            o.value.append(e, t);
          },
          insertBefore: (e, t) => {
            o.value.insertBefore(e, t);
          },
          insertAfter: (e, t) => {
            o.value.insertAfter(e, t);
          },
          handleNodeExpand: (e, n, d) => {
            (y(n), t.emit("node-expand", e, n, d));
          },
          updateKeyChildren: (t, n) => {
            if (!e.nodeKey)
              throw new Error("[Tree] nodeKey is required in updateKeyChild");
            o.value.updateChildren(t, n);
          },
        }
      );
    },
  }),
  [
    [
      "render",
      function (e, t, n, d, o, a) {
        const r = N("el-tree-node");
        return (
          x(),
          m(
            "div",
            {
              ref: "el$",
              class: w([
                e.ns.b(),
                e.ns.is("dragging", !!e.dragState.draggingNode),
                e.ns.is("drop-not-allow", !e.dragState.allowDrop),
                e.ns.is("drop-inner", "inner" === e.dragState.dropType),
                { [e.ns.m("highlight-current")]: e.highlightCurrent },
              ]),
              role: "tree",
            },
            [
              (x(!0),
              m(
                T,
                null,
                $(
                  e.root.childNodes,
                  (t) => (
                    x(),
                    E(
                      r,
                      {
                        key: e.getNodeKey(t),
                        node: t,
                        props: e.props,
                        accordion: e.accordion,
                        "render-after-expand": e.renderAfterExpand,
                        "show-checkbox": e.showCheckbox,
                        "render-content": e.renderContent,
                        onNodeExpand: e.handleNodeExpand,
                      },
                      null,
                      8,
                      [
                        "node",
                        "props",
                        "accordion",
                        "render-after-expand",
                        "show-checkbox",
                        "render-content",
                        "onNodeExpand",
                      ],
                    )
                  ),
                ),
                128,
              )),
              e.isEmpty
                ? (x(),
                  m(
                    "div",
                    { key: 0, class: w(e.ns.e("empty-block")) },
                    [
                      U(e.$slots, "empty", {}, () => {
                        var t;
                        return [
                          b(
                            "span",
                            { class: w(e.ns.e("empty-text")) },
                            W(
                              null != (t = e.emptyText)
                                ? t
                                : e.t("el.tree.emptyText"),
                            ),
                            3,
                          ),
                        ];
                      }),
                    ],
                    2,
                  ))
                : A("v-if", !0),
              v(
                b(
                  "div",
                  { ref: "dropIndicator$", class: w(e.ns.e("drop-indicator")) },
                  null,
                  2,
                ),
                [[C, e.dragState.showDropIndicator]],
              ),
            ],
            2,
          )
        );
      },
    ],
    [
      "__file",
      "/home/runner/work/element-plus/element-plus/packages/components/tree/src/tree.vue",
    ],
  ],
);
he.install = (e) => {
  e.component(he.name, he);
};
const ue = he,
  pe = ue;
export { pe as E, ue as _ };
