const e = { id: "id", children: "children", pid: "pid" },
  n = {
    children: "children",
    label: "label",
    value: "value",
    isLeaf: "leaf",
    disable: "",
  },
  l = (n) => Object.assign({}, e, n),
  r = (e, n = {}) => {
    n = l(n);
    const { children: r } = n,
      i = [...e];
    for (let l = 0; l < i.length; l++)
      i[l][r] && i.splice(l + 1, 0, ...i[l][r]);
    return i;
  },
  i = (e, n, r = {}) => {
    r = l(r);
    const i = [],
      t = [...e],
      s = new Set(),
      { children: c } = r;
    for (; t.length; ) {
      const e = t[0];
      if (s.has(e)) (i.pop(), t.shift());
      else if ((s.add(e), e[c] && t.unshift(...e[c]), i.push(e), n(e)))
        return i;
    }
    return null;
  },
  t = (e, n, r = {}) => {
    const i = (r = l(r)).children;
    return (function e(l) {
      return l
        .map((e) => ({ ...e }))
        .filter(
          (l) => ((l[i] = l[i] && e(l[i])), n(l) || (l[i] && l[i].length)),
        );
    })(e);
  },
  s = (e, n, l = {}) => {
    e.forEach((e) => {
      const r = n(e, l) || e;
      e.children && s(e.children, n, r);
    });
  };
export { t as a, n as d, s as e, i as f, r as t };
