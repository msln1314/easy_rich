import { o as e } from './datav-vue3.es-ea900063.js'
import { e as t, r as a, L as o, w as r, o as s, j as n, x as i, k as m } from './index-820a519e.js'
const c = { class: 'center-bottom-view' },
  d = t({
    __name: 'CenterBottom',
    props: { centerBottomData: { type: Array, required: !0 } },
    setup(t) {
      const d = t,
        l = a(null),
        u = a(d.centerBottomData),
        p = o({
          header: ['部门名称', '甲醛', 'PM2.5', 'PM10', '温度', '湿度', '更新时间'],
          data: u.value,
          index: !0,
          columnWidth: [50],
          align: ['center'],
          rowNum: 6,
          waitTime: 2e3,
          headerHeight: 40
        })
      return (
        r(
          () => d.centerBottomData,
          (e) => {
            l.value.updateRows(e)
          },
          { deep: !0 }
        ),
        (t, a) => (
          s(),
          n('div', c, [
            i(m(e), { ref_key: 'scrollBoardRef', ref: l, config: p }, null, 8, ['config'])
          ])
        )
      )
    }
  })
export { d as _ }
