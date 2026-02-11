import {
  r as l,
  o as a,
  l as e,
  m as u,
  j as s,
  a1 as b,
  a5 as v,
  k as o,
  M as t,
  z as r
} from './index-820a519e.js'
import { a as m, E as i } from './el-descriptions-item-6ddb822e.js'
import './vnode-06a99f10.js'
import './isNil-1f22f7b0.js'
const n = {
  __name: 'CronExample',
  setup(n) {
    const p = l([
      { value: '0 0 10,15,16 * * ?', label: '每天上午10点，下午3点，4点' },
      { value: '0 0/30 9-17 * * ?', label: '朝九晚五工作时间内每半小时' },
      { value: '0 0 12 ? * WED\t', label: '表示每个星期三中午12点' },
      { value: '0 0 12 * * ?', label: '每天中午12点触发' },
      { value: '0 15 10 ? * *', label: '每天上午10:15触发' },
      { value: '0 15 10 * * ?', label: '每天上午10:15触发 （跟上面的一样）' },
      { value: '0 15 10 * * ? 2005', label: '2005年的每天上午10:15触发' },
      { value: '0 * 14 * * ?', label: '在每天下午2点到下午2:59期间的每1分钟触发' },
      { value: '0 0/5 14 * * ?', label: '在每天下午2点到下午2:55期间的每5分钟触发' },
      {
        value: '0 0/5 14,18 * * ?',
        label: '在每天下午2点到2:55期间和下午6点到6:55期间的每5分钟触发'
      },
      { value: '0 0-5 14 * * ?', label: '在每天下午2点到下午2:05期间的每1分钟触发' },
      { value: '0 10,44 14 ? 3 WED', label: '每年三月的星期三的下午2:10和2:44触发' },
      { value: '0 15 10 ? * MON-FRI', label: '周一至周五的上午10:15触发' },
      { value: '0 15 10 15 * ?', label: '每月15日上午10:15触发' },
      { value: '0 15 10 L * ?', label: '每月最后一日的上午10:15触发' }
    ])
    return (l, n) => (
      a(),
      e(
        o(i),
        { column: 1, border: !0 },
        {
          default: u(() => [
            (a(!0),
            s(
              b,
              null,
              v(
                p.value,
                (l, s) => (
                  a(),
                  e(
                    o(m),
                    { key: s, label: l.value },
                    { default: u(() => [t(r(l.label), 1)]), _: 2 },
                    1032,
                    ['label']
                  )
                )
              ),
              128
            ))
          ]),
          _: 1
        }
      )
    )
  }
}
export { n as default }
