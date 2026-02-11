import { e as t, r as e, o as s, l as r, m as i, x as p, k as o } from './index-820a519e.js'
import { E as m, a as l } from './el-col-beabe3f6.js'
import { _ } from './DictDetail.vue_vue_type_script_setup_true_lang-a8ffa1c2.js'
import { _ as j } from './DictType.vue_vue_type_script_setup_true_lang-daf61a0a.js'
import './dict-c8c7fcf4.js'
import './Table.vue_vue_type_script_lang-a0f5d3d3.js'
import './el-message-box-faa52860.js'
import './el-input-5ae17c8f.js'
import './event-5568c9d8.js'
import './isNil-1f22f7b0.js'
import './el-overlay-34b9d092.js'
import './scroll-ac7d0423.js'
import './vnode-06a99f10.js'
import './useForm-c59a8d29.js'
import './el-form-item-2e860f96.js'
import './el-tooltip-4ed993c7.js'
import './el-popper-797844d6.js'
import './focus-trap-949626e0.js'
/* empty css               */ import './el-checkbox-77b6829c.js'
import './isEqual-cb9e370d.js'
/* empty css                          */ import './el-date-picker-6b1a21d2.js'
import './dayjs.min-e5ba30ae.js'
import './debounce-5bc596c6.js'
import './index-eb31d854.js'
import './el-radio-group-4cb40939.js'
import './el-select-38080147.js'
import './index-56bc6266.js'
import './strings-ed83d626.js'
import './validator-a9d8fe4c.js'
import './el-switch-6f4f5b6a.js'
import './el-divider-9c19755b.js'
import './el-tree-8dac9473.js'
import './index-55f4d4a6.js'
import './el-progress-97dbc0fb.js'
import './style.css_vue_type_style_index_0_src_true_lang-4a035adc.js'
import './index-2b3f7e71.js'
import './el-table-column-36e57984.js'
import './el-pagination-60eda460.js'
import './dropdown-394a0a1a.js'
import './el-image-viewer-73f400a0.js'
import './el-dropdown-item-a41cbdee.js'
import './refs-374e9e51.js'
/* empty css                   */ import './_Uint8Array-48df3306.js'
import './Search.vue_vue_type_script_setup_true_lang-9de3bdd5.js'
import './useIcon-24caadfc.js'
import './ContentWrap.vue_vue_type_script_setup_true_lang-37d6ee07.js'
import './el-card-06c161d4.js'
import './Write.vue_vue_type_script_setup_true_lang-f33a78c9.js'
import './useValidator-db15330d.js'
import './Dialog.vue_vue_type_style_index_0_lang-ce349c68.js'
import './use-dialog-2de816dc.js'
import './Write.vue_vue_type_script_setup_true_lang-ad357938.js'
const a = t({
  name: 'SystemDict',
  __name: 'Dict',
  setup(t) {
    const a = e(),
      u = (t) => {
        a.value = t
      }
    return (t, e) => (
      s(),
      r(o(l), null, {
        default: i(() => [
          p(
            o(m),
            { xs: 24, sm: 24, md: 12, lg: 12, xl: 12 },
            { default: i(() => [p(j, { onUpdateDictTypeId: u })]), _: 1 }
          ),
          p(
            o(m),
            { xs: 24, sm: 24, md: 12, lg: 12, xl: 12 },
            {
              default: i(() => [p(_, { 'dict-type-id': a.value }, null, 8, ['dict-type-id'])]),
              _: 1
            }
          )
        ]),
        _: 1
      })
    )
  }
})
export { a as default }
