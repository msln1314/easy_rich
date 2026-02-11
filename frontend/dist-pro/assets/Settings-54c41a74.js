import {
  e,
  r as t,
  o as a,
  l as s,
  m as i,
  x as r,
  k as l,
  j as o,
  a1 as _,
  a5 as p,
  F as m,
  dH as u
} from './index-820a519e.js'
import { E as n, a as d } from './el-tab-pane-bc33a695.js'
import { _ as j } from './Basic.vue_vue_type_style_index_0_lang-8b3503e1.js'
import { _ as b } from './Privacy.vue_vue_type_script_setup_true_lang-192f646c.js'
import { _ as c } from './Agreement.vue_vue_type_script_setup_true_lang-fc31a28f.js'
import { _ as v } from './WechatServer.vue_vue_type_script_setup_true_lang-50509bc2.js'
import { _ as y } from './Email.vue_vue_type_script_setup_true_lang-75ab175d.js'
import { _ as g } from './SMS.vue_vue_type_script_setup_true_lang-232d23f8.js'
import { _ as f } from './ContentWrap.vue_vue_type_script_setup_true_lang-37d6ee07.js'
import './strings-ed83d626.js'
import './event-5568c9d8.js'
import './vnode-06a99f10.js'
import './useForm-c59a8d29.js'
import './el-form-item-2e860f96.js'
import './el-col-beabe3f6.js'
import './el-tooltip-4ed993c7.js'
import './el-popper-797844d6.js'
import './isNil-1f22f7b0.js'
import './focus-trap-949626e0.js'
import './el-input-5ae17c8f.js'
/* empty css               */ import './el-checkbox-77b6829c.js'
import './isEqual-cb9e370d.js'
/* empty css                          */ import './el-date-picker-6b1a21d2.js'
import './dayjs.min-e5ba30ae.js'
import './debounce-5bc596c6.js'
import './index-eb31d854.js'
import './el-radio-group-4cb40939.js'
import './el-select-38080147.js'
import './index-56bc6266.js'
import './scroll-ac7d0423.js'
import './validator-a9d8fe4c.js'
import './el-switch-6f4f5b6a.js'
import './el-divider-9c19755b.js'
import './el-tree-8dac9473.js'
import './index-55f4d4a6.js'
import './el-progress-97dbc0fb.js'
import './style.css_vue_type_style_index_0_src_true_lang-4a035adc.js'
import './useValidator-db15330d.js'
import './el-card-06c161d4.js'
const k = e({
  name: 'SystemSettings',
  __name: 'Settings',
  setup(e) {
    const k = t('web_basic'),
      x = t([])
    return (
      (async () => {
        const e = await u(['web', 'aliyun'])
        e && (x.value = e.data)
      })(),
      (e, t) => (
        a(),
        s(l(f), null, {
          default: i(() => [
            r(
              l(n),
              { modelValue: k.value, 'onUpdate:modelValue': t[0] || (t[0] = (e) => (k.value = e)) },
              {
                default: i(() => [
                  (a(!0),
                  o(
                    _,
                    null,
                    p(
                      x.value,
                      (e) => (
                        a(),
                        o(
                          _,
                          { key: e.id },
                          [
                            e.hidden
                              ? m('', !0)
                              : (a(),
                                s(
                                  l(d),
                                  { key: 0, name: e.tab_name, label: e.tab_label },
                                  {
                                    default: i(() => [
                                      'web_basic' === e.tab_name
                                        ? (a(),
                                          s(j, { key: 0, 'tab-id': e.id }, null, 8, ['tab-id']))
                                        : 'web_privacy' === e.tab_name
                                          ? (a(),
                                            s(b, { key: 1, 'tab-id': e.id }, null, 8, ['tab-id']))
                                          : 'web_agreement' === e.tab_name
                                            ? (a(),
                                              s(c, { key: 2, 'tab-id': e.id }, null, 8, ['tab-id']))
                                            : 'wx_server' === e.tab_name
                                              ? (a(),
                                                s(v, { key: 3, 'tab-id': e.id }, null, 8, [
                                                  'tab-id'
                                                ]))
                                              : 'web_email' === e.tab_name
                                                ? (a(),
                                                  s(y, { key: 4, 'tab-id': e.id }, null, 8, [
                                                    'tab-id'
                                                  ]))
                                                : 'aliyun_sms' === e.tab_name
                                                  ? (a(),
                                                    s(g, { key: 5, 'tab-id': e.id }, null, 8, [
                                                      'tab-id'
                                                    ]))
                                                  : m('', !0)
                                    ]),
                                    _: 2
                                  },
                                  1032,
                                  ['name', 'label']
                                ))
                          ],
                          64
                        )
                      )
                    ),
                    128
                  ))
                ]),
                _: 1
              },
              8,
              ['modelValue']
            )
          ]),
          _: 1
        })
      )
    )
  }
})
export { k as default }
