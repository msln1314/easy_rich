import { d as e } from './tree-ae7cba8b.js'
import { g as a, p as l } from './role-0252bcb8.js'
import {
  e as t,
  r as s,
  Z as o,
  o as u,
  l as i,
  m as r,
  x as d,
  k as m,
  N as n,
  M as v,
  a0 as p,
  z as c,
  dG as f,
  as as _,
  af as j,
  J as x
} from './index-820a519e.js'
import { E as y } from './el-switch-6f4f5b6a.js'
/* empty css               */ import { E as h, a as g } from './el-form-item-2e860f96.js'
import { E as k } from './el-tree-8dac9473.js'
import './el-checkbox-77b6829c.js'
import { E as V } from './el-card-06c161d4.js'
import { _ as b } from './Dialog.vue_vue_type_style_index_0_lang-ce349c68.js'
import { E as C } from './index-56bc6266.js'
import './validator-a9d8fe4c.js'
import './event-5568c9d8.js'
import './index-55f4d4a6.js'
import './isEqual-cb9e370d.js'
import './el-overlay-34b9d092.js'
import './scroll-ac7d0423.js'
import './vnode-06a99f10.js'
import './use-dialog-2de816dc.js'
import './focus-trap-949626e0.js'
import './isNil-1f22f7b0.js'
import './refs-374e9e51.js'
import './index-2b3f7e71.js'
const w = x(
  t({
    name: 'SystemRoleAssignMenuForm',
    __name: 'RoleAssignMenuForm',
    emits: ['success'],
    setup(t, { expose: x, emit: w }) {
      const E = s(!1),
        M = s(!1),
        N = s({}),
        R = s(),
        F = s([]),
        U = s(!1),
        A = s(),
        D = s(!1)
      x({
        open: async (e) => {
          const { data: l } = await a(e.id)
          E.value = !0
          const t = await f()
          if (t) {
            ;((F.value = t.data), (N.value = l), (M.value = !0), await _())
            try {
              const e = l.menus.map((e) => e.id)
              ;((N.value.menu_ids = e),
                N.value.menu_ids.forEach((e) => {
                  A.value.setChecked(e, !0, !1)
                }))
            } finally {
              M.value = !1
            }
          }
        }
      })
      const H = async () => {
          if (!R.value) return
          if (await R.value.validate()) {
            M.value = !0
            try {
              const e = [...A.value.getCheckedKeys(!1), ...A.value.getHalfCheckedKeys()]
              ;((N.value.menu_ids = e),
                await l(N.value),
                j.success('保存成功!'),
                (E.value = !1),
                w('success'))
            } finally {
              M.value = !1
            }
          }
        },
        I = () => {
          A.value.setCheckedNodes(D.value ? F.value : [])
        },
        J = () => {
          var e
          const a = null == (e = A.value) ? void 0 : e.store.nodesMap
          for (let l in a) a[l].expanded !== U.value && (a[l].expanded = U.value)
        }
      return (a, l) => {
        const t = o('loading')
        return (
          u(),
          i(
            m(b),
            {
              modelValue: E.value,
              'onUpdate:modelValue': l[3] || (l[3] = (e) => (E.value = e)),
              title: '菜单权限'
            },
            {
              footer: r(() => [
                d(
                  m(n),
                  { disabled: M.value, type: 'primary', onClick: H },
                  { default: r(() => [v('确 定')]), _: 1 },
                  8,
                  ['disabled']
                ),
                d(
                  m(n),
                  { onClick: l[2] || (l[2] = (e) => (E.value = !1)) },
                  { default: r(() => [v('取 消')]), _: 1 }
                )
              ]),
              default: r(() => [
                p(
                  (u(),
                  i(
                    m(h),
                    { ref_key: 'formRef', ref: R, model: N.value, 'label-width': '80px' },
                    {
                      default: r(() => [
                        d(
                          m(g),
                          { label: '角色名称' },
                          {
                            default: r(() => [
                              d(m(C), null, { default: r(() => [v(c(N.value.name), 1)]), _: 1 })
                            ]),
                            _: 1
                          }
                        ),
                        d(
                          m(g),
                          { label: '角色标识' },
                          {
                            default: r(() => [
                              d(m(C), null, { default: r(() => [v(c(N.value.code), 1)]), _: 1 })
                            ]),
                            _: 1
                          }
                        ),
                        d(
                          m(g),
                          { label: '菜单权限' },
                          {
                            default: r(() => [
                              d(
                                m(V),
                                { class: 'cardHeight' },
                                {
                                  header: r(() => [
                                    v(' 全选/全不选: '),
                                    d(
                                      m(y),
                                      {
                                        modelValue: D.value,
                                        'onUpdate:modelValue':
                                          l[0] || (l[0] = (e) => (D.value = e)),
                                        'active-text': '是',
                                        'inactive-text': '否',
                                        'inline-prompt': '',
                                        onChange: I
                                      },
                                      null,
                                      8,
                                      ['modelValue']
                                    ),
                                    v(' 全部展开/折叠: '),
                                    d(
                                      m(y),
                                      {
                                        modelValue: U.value,
                                        'onUpdate:modelValue':
                                          l[1] || (l[1] = (e) => (U.value = e)),
                                        'active-text': '展开',
                                        'inactive-text': '折叠',
                                        'inline-prompt': '',
                                        onChange: J
                                      },
                                      null,
                                      8,
                                      ['modelValue']
                                    )
                                  ]),
                                  default: r(() => [
                                    d(
                                      m(k),
                                      {
                                        ref_key: 'treeRef',
                                        ref: A,
                                        data: F.value,
                                        props: m(e),
                                        'empty-text': '加载中，请稍候',
                                        'node-key': 'value',
                                        'show-checkbox': ''
                                      },
                                      null,
                                      8,
                                      ['data', 'props']
                                    )
                                  ]),
                                  _: 1
                                }
                              )
                            ]),
                            _: 1
                          }
                        )
                      ]),
                      _: 1
                    },
                    8,
                    ['model']
                  )),
                  [[t, M.value]]
                )
              ]),
              _: 1
            },
            8,
            ['modelValue']
          )
        )
      }
    }
  }),
  [['__scopeId', 'data-v-ee17db22']]
)
export { w as default }
