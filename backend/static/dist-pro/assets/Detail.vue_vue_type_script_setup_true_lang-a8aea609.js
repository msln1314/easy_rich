import { D as e } from "./Descriptions-889cd6fb.js";
import { e as a, L as l, o as s, l as t, k as i } from "./index-6b60d190.js";
const p = a({
  __name: "Detail",
  props: { currentRow: { type: Object, default: () => null } },
  setup(a) {
    const p = l([
      { field: "user_id", label: "操作人编号", width: "100px", span: 24 },
      { field: "user.name", label: "操作人", width: "100px", span: 24 },
      { field: "phone", label: "手机号", width: "130px", span: 24 },
      { field: "client_ip", label: "客户端地址", width: "130px", span: 24 },
      { field: "device.mac", label: "设备SN", span: 24 },
      { field: "message", label: "操作内容", span: 24 },
      { field: "status", label: "操作状态", width: "100px", span: 24 },
      { field: "browser", label: "浏览器", width: "150px", span: 24 },
      { field: "system", label: "系统", width: "150px", span: 24 },
      { field: "process_time", label: "总耗时", span: 24 },
      { field: "created_at", label: "操作时间", span: 24 },
    ]);
    return (l, d) => (
      s(),
      t(i(e), { schema: p, data: a.currentRow || {} }, null, 8, [
        "schema",
        "data",
      ])
    );
  },
});
export { p as _ };
