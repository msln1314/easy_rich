import {
  I as a,
  e,
  r as t,
  L as s,
  Z as l,
  o,
  j as i,
  x as r,
  m as n,
  k as u,
  M as d,
  y as m,
  z as p,
  $ as y,
  a0 as b,
  l as c,
  a1 as _,
} from "./index-6b60d190.js";
import { E as g, a as x } from "./el-col-b8aa0d1a.js";
import { E as f } from "./el-divider-2dd0a1ee.js";
import { E as v } from "./el-skeleton-item-298f4c82.js";
import { E as h, a as j } from "./el-table-column-0bcf5917.js";
import "./el-checkbox-4903f610.js";
import "./el-tooltip-4ed993c7.js";
import "./el-popper-09548d54.js";
/* empty css               */ import {
  E as w,
  a as q,
} from "./el-radio-group-0c46635e.js";
import { E } from "./el-date-picker-91f17f23.js";
import "./el-input-38d674e5.js";
import { _ as k } from "./Echart.vue_vue_type_script_setup_true_lang-5c4679ac.js";
import "./isEqual-b8d86c27.js";
import "./debounce-5c500a3d.js";
import "./index-fdfa028a.js";
import "./event-5568c9d8.js";
import "./isNil-1f22f7b0.js";
import "./focus-trap-275966d8.js";
const { t: S } = a(),
  T = {
    xAxis: {
      data: [
        S("analysis.january"),
        S("analysis.february"),
        S("analysis.march"),
        S("analysis.april"),
        S("analysis.may"),
        S("analysis.june"),
        S("analysis.july"),
        S("analysis.august"),
        S("analysis.september"),
        S("analysis.october"),
        S("analysis.november"),
        S("analysis.december"),
      ],
      boundaryGap: !1,
      axisTick: { show: !1 },
    },
    grid: { left: 20, right: 20, bottom: 35, top: 30, containLabel: !0 },
    tooltip: {
      trigger: "axis",
      axisPointer: { type: "cross" },
      padding: [5, 10],
    },
    yAxis: { type: "value", axisTick: { show: !1 } },
    legend: { data: ["销售额", "充值金额"], bottom: -5 },
    series: [
      {
        name: "销售额",
        smooth: !1,
        symbol: "circle",
        symbolSize: 8,
        type: "line",
        data: [
          86423, 74129, 57231, 62547, 87345, 92856, 64123, 51237, 95874, 73019,
          58642, 69428,
        ],
        animationDuration: 2800,
        animationEasing: "quadraticOut",
        itemStyle: { color: "rgba(110,199,30)" },
        lineStyle: { width: 1, opacity: 1 },
        areaStyle: { color: "rgba(110,199,30, 0.2)" },
      },
      {
        name: "充值金额",
        smooth: !1,
        symbol: "circle",
        symbolSize: 8,
        type: "line",
        data: [
          95874, 86423, 87345, 74129, 73019, 62547, 69428, 57231, 64123, 58642,
          92856, 51237,
        ],
        animationDuration: 2800,
        animationEasing: "quadraticOut",
        itemStyle: { color: "rgba(79,168,249)" },
        lineStyle: { width: 1, opacity: 1 },
        areaStyle: { color: "rgba(79,168,249, 0.2)" },
      },
    ],
  },
  z = {
    xAxis: {
      data: [
        S("analysis.january"),
        S("analysis.february"),
        S("analysis.march"),
        S("analysis.april"),
        S("analysis.may"),
        S("analysis.june"),
        S("analysis.july"),
        S("analysis.august"),
        S("analysis.september"),
        S("analysis.october"),
        S("analysis.november"),
        S("analysis.december"),
      ],
      boundaryGap: !1,
      axisTick: { show: !1 },
    },
    grid: { left: 20, right: 20, bottom: 35, top: 30, containLabel: !0 },
    tooltip: {
      trigger: "axis",
      axisPointer: { type: "cross" },
      padding: [5, 10],
    },
    yAxis: { type: "value", axisTick: { show: !1 } },
    legend: {
      data: ["服饰", "电器", "茶叶", "珠宝", "家纺", "玩具"],
      bottom: -5,
    },
    series: [
      {
        name: "服饰",
        smooth: !1,
        type: "line",
        data: [
          60384, 74218, 57149, 83297, 21675, 96743, 38547, 72436, 93742, 59073,
          81394, 66912,
        ],
        animationDuration: 2800,
        animationEasing: "quadraticOut",
      },
      {
        name: "电器",
        smooth: !1,
        type: "line",
        data: [
          29541, 64783, 79942, 50472, 91374, 26819, 69247, 78354, 48672, 81124,
          92038, 36847,
        ],
      },
      {
        name: "茶叶",
        smooth: !1,
        type: "line",
        data: [
          84273, 73842, 21675, 97342, 65938, 82473, 59172, 40672, 92438, 76592,
          83947, 50283,
        ],
      },
      {
        name: "珠宝",
        smooth: !1,
        type: "line",
        data: [
          21675, 84273, 50283, 76924, 68574, 92438, 39572, 93742, 50472, 78354,
          59247, 92038,
        ],
      },
      {
        name: "家纺",
        smooth: !1,
        type: "line",
        data: [
          78354, 76924, 82473, 50472, 48672, 65938, 64783, 50283, 73842, 40672,
          84273, 76592,
        ],
      },
      {
        name: "玩具",
        smooth: !1,
        type: "line",
        data: [
          40672, 50472, 59247, 81394, 36847, 59273, 26819, 66912, 59172, 84273,
          50283, 76924,
        ],
      },
    ],
  },
  V = {
    tooltip: { trigger: "item", formatter: "{a} <br/>{b} : {c} ({d}%)" },
    series: [
      {
        name: "各品类销售额情况统计",
        type: "pie",
        radius: "55%",
        center: ["50%", "40%"],
        data: [
          { value: 599999, name: "服饰" },
          { value: 89999, name: "电器" },
          { value: 219879, name: "茶叶" },
          { value: 897999, name: "珠宝" },
          { value: 102999, name: "家纺" },
          { value: 499090, name: "玩具" },
        ],
      },
    ],
  },
  A = m("div", { class: "text-[#787a7d] text-[12px]" }, "销售额", -1),
  D = { class: "text-[#121315] text-[20px] mt-[10px]" },
  P = m("div", { class: "text-[#787a7d] text-[12px]" }, "充值金额", -1),
  C = { class: "text-[#121315] text-[20px] mt-[10px]" },
  G = m(
    "div",
    null,
    [
      m("div", { class: "text-[#787a7d] text-[12px]" }, "销量"),
      m("div", { class: "text-[#121315] text-[20px] mt-[10px]" }, "3999"),
    ],
    -1,
  ),
  L = m(
    "div",
    null,
    [
      m("div", { class: "text-[#787a7d] text-[12px]" }, "订单数"),
      m("div", { class: "text-[#121315] text-[20px] mt-[10px]" }, "1899"),
    ],
    -1,
  ),
  O = { class: "mt-8" },
  F = e({
    __name: "Finance",
    setup(a) {
      const e = t(!1),
        S = s(z),
        F = s(V),
        M = t([
          {
            name: "美的家用落地扇",
            category: "电风扇",
            order_quantity: "131",
            buy_user_number: "72",
            sales: "36981",
            sales_volume: "90",
          },
          {
            name: "天斧88d 3u",
            category: "羽毛球拍",
            order_quantity: "131",
            buy_user_number: "72",
            sales: "36981",
            sales_volume: "90",
          },
          {
            name: "格力空调",
            category: "空调",
            order_quantity: "131",
            buy_user_number: "72",
            sales: "36981",
            sales_volume: "90",
          },
          {
            name: "海尔冰箱",
            category: "冰箱",
            order_quantity: "131",
            buy_user_number: "72",
            sales: "36981",
            sales_volume: "90",
          },
          {
            name: "小米电视",
            category: "电视",
            order_quantity: "131",
            buy_user_number: "72",
            sales: "36981",
            sales_volume: "90",
          },
          {
            name: "荣耀笔记本",
            category: "笔记本",
            order_quantity: "131",
            buy_user_number: "72",
            sales: "36981",
            sales_volume: "90",
          },
          {
            name: "iPhone12",
            category: "手机",
            order_quantity: "131",
            buy_user_number: "72",
            sales: "36981",
            sales_volume: "90",
          },
          {
            name: "Macbook Pro",
            category: "笔记本",
            order_quantity: "131",
            buy_user_number: "72",
            sales: "36981",
            sales_volume: "90",
          },
        ]),
        N = t(0),
        U = t(),
        B = () => {},
        H = (a) =>
          new Date("2023/01/01").getTime() > a.getTime() ||
          a.getTime() > Date.now();
      return (a, t) => {
        const s = l("loading");
        return (
          o(),
          i(
            _,
            null,
            [
              r(
                u(q),
                {
                  modelValue: N.value,
                  "onUpdate:modelValue": t[1] || (t[1] = (a) => (N.value = a)),
                  onChange: B,
                },
                {
                  default: n(() => [
                    r(
                      u(w),
                      { label: "0" },
                      { default: n(() => [d("全部")]), _: 1 },
                    ),
                    r(
                      u(w),
                      { label: "1" },
                      { default: n(() => [d("今天")]), _: 1 },
                    ),
                    r(
                      u(w),
                      { label: "2" },
                      { default: n(() => [d("昨天")]), _: 1 },
                    ),
                    r(
                      u(w),
                      { label: "3" },
                      { default: n(() => [d("最近7天")]), _: 1 },
                    ),
                    r(
                      u(w),
                      { label: "4" },
                      { default: n(() => [d("最近30天")]), _: 1 },
                    ),
                    r(
                      u(E),
                      {
                        class: "ml-2",
                        modelValue: U.value,
                        "onUpdate:modelValue":
                          t[0] || (t[0] = (a) => (U.value = a)),
                        type: "daterange",
                        "range-separator": "-",
                        "start-placeholder": "开始时间",
                        "end-placeholder": "结束时间",
                        "disabled-date": H,
                        "unlink-panels": !0,
                        size: "default",
                      },
                      null,
                      8,
                      ["modelValue"],
                    ),
                  ]),
                  _: 1,
                },
                8,
                ["modelValue"],
              ),
              r(u(f)),
              r(
                u(x),
                { gutter: 20, class: "pt-4" },
                {
                  default: n(() => [
                    r(
                      u(g),
                      {
                        xs: 12,
                        sm: 6,
                        class: "border-r-1 border-r-[#f0f0f0] b-r-solid mb-2",
                      },
                      {
                        default: n(() => [
                          r(
                            u(v),
                            { loading: e.value, animated: "", rows: 4 },
                            {
                              default: n(() => [
                                m("div", null, [
                                  A,
                                  m("div", D, p(u(y)(899999)), 1),
                                ]),
                              ]),
                              _: 1,
                            },
                            8,
                            ["loading"],
                          ),
                        ]),
                        _: 1,
                      },
                    ),
                    r(
                      u(g),
                      {
                        xs: 12,
                        sm: 6,
                        class: "border-r-1 border-r-[#f0f0f0] b-r-solid mb-2",
                      },
                      {
                        default: n(() => [
                          r(
                            u(v),
                            { loading: e.value, animated: "", rows: 4 },
                            {
                              default: n(() => [
                                m("div", null, [
                                  P,
                                  m("div", C, p(u(y)(899999)), 1),
                                ]),
                              ]),
                              _: 1,
                            },
                            8,
                            ["loading"],
                          ),
                        ]),
                        _: 1,
                      },
                    ),
                    r(
                      u(g),
                      {
                        xs: 12,
                        sm: 6,
                        class: "border-r-1 border-r-[#f0f0f0] b-r-solid mb-2",
                      },
                      {
                        default: n(() => [
                          r(
                            u(v),
                            { loading: e.value, animated: "", rows: 4 },
                            { default: n(() => [G]), _: 1 },
                            8,
                            ["loading"],
                          ),
                        ]),
                        _: 1,
                      },
                    ),
                    r(
                      u(g),
                      {
                        xs: 12,
                        sm: 6,
                        class: "border-r-1 border-r-[#f0f0f0] b-r-solid",
                      },
                      {
                        default: n(() => [
                          r(
                            u(v),
                            { loading: e.value, animated: "", rows: 4 },
                            { default: n(() => [L]), _: 1 },
                            8,
                            ["loading"],
                          ),
                        ]),
                        _: 1,
                      },
                    ),
                    r(u(g), { xs: 12, sm: 6 }),
                  ]),
                  _: 1,
                },
              ),
              r(u(f)),
              r(
                u(v),
                { loading: e.value, animated: "", rows: 4 },
                {
                  default: n(() => [
                    r(u(k), { options: u(T), height: 350 }, null, 8, [
                      "options",
                    ]),
                  ]),
                  _: 1,
                },
                8,
                ["loading"],
              ),
              r(u(f)),
              r(
                u(x),
                { gutter: 20, class: "pt-4" },
                {
                  default: n(() => [
                    r(
                      u(g),
                      { xs: 24, sm: 6 },
                      {
                        default: n(() => [
                          r(
                            u(v),
                            { loading: e.value, animated: "", rows: 4 },
                            {
                              default: n(() => [
                                r(u(k), { options: F, height: 350 }, null, 8, [
                                  "options",
                                ]),
                              ]),
                              _: 1,
                            },
                            8,
                            ["loading"],
                          ),
                        ]),
                        _: 1,
                      },
                    ),
                    r(
                      u(g),
                      { xs: 24, sm: 18 },
                      {
                        default: n(() => [
                          r(
                            u(v),
                            { loading: e.value, animated: "", rows: 4 },
                            {
                              default: n(() => [
                                r(u(k), { options: S, height: 350 }, null, 8, [
                                  "options",
                                ]),
                              ]),
                              _: 1,
                            },
                            8,
                            ["loading"],
                          ),
                        ]),
                        _: 1,
                      },
                    ),
                  ]),
                  _: 1,
                },
              ),
              r(u(f)),
              m("div", O, [
                b(
                  (o(),
                  c(
                    u(j),
                    {
                      data: M.value,
                      style: { width: "100%" },
                      headerCellStyle: {
                        "background-color": "#f5f7fa",
                        color: "#787a7d",
                        "font-size": "12px",
                      },
                    },
                    {
                      default: n(() => [
                        r(u(h), { type: "index", width: "50" }),
                        r(u(h), { prop: "name", label: "商品名称" }),
                        r(u(h), { prop: "category", label: "商品品类" }),
                        r(u(h), {
                          prop: "order_quantity",
                          label: "商品购买次数",
                        }),
                        r(u(h), {
                          prop: "buy_user_number",
                          label: "商品购买人数",
                        }),
                        r(
                          u(h),
                          {
                            prop: "sales",
                            label: "商品销售额",
                            align: "center",
                          },
                          {
                            default: n(({ row: a }) => [
                              m("span", null, p(u(y)(a.sales)), 1),
                            ]),
                            _: 1,
                          },
                        ),
                        r(u(h), {
                          prop: "sales_volume",
                          label: "商品销量",
                          align: "center",
                        }),
                      ]),
                      _: 1,
                    },
                    8,
                    ["data"],
                  )),
                  [[s, e.value]],
                ),
              ]),
            ],
            64,
          )
        );
      };
    },
  });
export { F as default };
