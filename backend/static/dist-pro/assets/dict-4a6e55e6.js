const l = (l, n) => {
  var r;
  if (null == n) return "";
  {
    const e = null == (r = l.find((l) => l.value == n)) ? void 0 : r.label;
    return void 0 === e ? n : e;
  }
};
export { l as s };
