import { U as t } from "./index-6b60d190.js";
const a = (a) => t.get({ url: "/iot/clients", params: a }),
  i = (a) => t.post({ url: "/iot/clients", data: a }),
  s = (a) => t.delete({ url: "/iot/clients", data: a }),
  e = (a) => t.put({ url: `/iot/clients/${a.id}`, data: a }),
  l = (a) => t.put({ url: `/iot/clients/bind/${a.id}`, data: a }),
  o = (a) => t.put({ url: `/iot/clients/unbind/${a.id}` }),
  r = (a) => t.put({ url: `/iot/clients/status/${a.id}`, data: a }),
  d = (a) => t.get({ url: `/iot/clients/${a}` }),
  p = (a, i) =>
    t.post({ url: "/iot/clients/export/excel", params: a, data: i }),
  u = () => t.get({ url: "/iot/clients/download/import/template" }),
  n = (a) =>
    t.post({
      url: "/iot/clients/import",
      headersType: "multipart/form-data",
      data: a,
    });
export {
  r as a,
  a as b,
  p as c,
  s as d,
  i as e,
  e as f,
  d as g,
  l as h,
  n as i,
  u as j,
  o as p,
};
