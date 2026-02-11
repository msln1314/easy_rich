import {
  e as t,
  r as e,
  o as s,
  l as r,
  m as i,
  x as p,
  k as o,
} from "./index-6b60d190.js";
import { E as m, a as l } from "./el-col-b8aa0d1a.js";
import { _ } from "./DictDetail.vue_vue_type_script_setup_true_lang-185d4056.js";
import { _ as a } from "./DictType.vue_vue_type_script_setup_true_lang-3be098f7.js";
import "./dict-593a5a5e.js";
import "./Table.vue_vue_type_script_lang-230d9abb.js";
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
import "./el-image-viewer-5060851c.js";
import "./el-dropdown-item-943c2eb7.js";
import "./refs-64421a9c.js";
/* empty css                   */ import "./_Uint8Array-f98e6540.js";
import "./Search.vue_vue_type_script_setup_true_lang-9c85421f.js";
import "./useIcon-7641a992.js";
import "./ContentWrap.vue_vue_type_script_setup_true_lang-067de0d9.js";
import "./el-card-37d6f3c4.js";
import "./Write.vue_vue_type_script_setup_true_lang-07f2bbbb.js";
import "./useValidator-63200dcb.js";
import "./Dialog.vue_vue_type_style_index_0_lang-d732453c.js";
import "./use-dialog-0e1ee265.js";
import "./Write.vue_vue_type_script_setup_true_lang-f3243979.js";
const j = t({
  name: "SystemDict",
  __name: "Dict",
  setup(t) {
    const j = e(),
      u = (t) => {
        j.value = t;
      };
    return (t, e) => (
      s(),
      r(o(l), null, {
        default: i(() => [
          p(
            o(m),
            { xs: 24, sm: 24, md: 12, lg: 12, xl: 12 },
            { default: i(() => [p(a, { onUpdateDictTypeId: u })]), _: 1 },
          ),
          p(
            o(m),
            { xs: 24, sm: 24, md: 12, lg: 12, xl: 12 },
            {
              default: i(() => [
                p(_, { "dict-type-id": j.value }, null, 8, ["dict-type-id"]),
              ]),
              _: 1,
            },
          ),
        ]),
        _: 1,
      })
    );
  },
});
export { j as default };
