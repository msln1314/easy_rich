import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import type { App } from 'vue'
import { Layout } from '@/utils/routerHelper'
import { useI18n } from '@/hooks/web/useI18n'

const { t } = useI18n()

export const constantRouterMap: AppRouteRecordRaw[] = [
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard/analysis',
    name: 'Root',
    meta: {
      hidden: true
    },
    children: [
      {
        path: 'home',
        name: 'Home',
        component: () => import('@/views/Home/Home.vue'),
        meta: {
          affix: false,
          alwaysShow: true,
          breadcrumb: true,
          canTo: true,
          hidden: true,
          noCache: true,
          noTagsView: false,
          title: '个人主页'
        }
      }
    ]
  },
  {
    path: '/redirect',
    component: Layout,
    name: 'Redirect',
    children: [
      {
        path: '/redirect/:path(.*)',
        name: 'Redirect',
        component: () => import('@/views/Redirect/Redirect.vue'),
        meta: {}
      }
    ],
    meta: {
      hidden: true,
      noTagsView: true
    }
  },
  {
    path: '/login',
    component: () => import('@/views/Login/Login.vue'),
    name: 'Login',
    meta: {
      hidden: true,
      title: t('router.login'),
      noTagsView: true
    }
  },
  {
    path: '/reset/password',
    component: () => import('@/views/Reset/Reset.vue'),
    name: 'ResetPassword',
    meta: {
      hidden: true,
      title: '重置密码',
      noTagsView: true
    }
  },
  {
    path: '/404',
    component: () => import('@/views/Error/404.vue'),
    name: 'NoFind',
    meta: {
      hidden: true,
      title: '404',
      noTagsView: true
    }
  }
]

export const asyncRouterMap: AppRouteRecordRaw[] = [
  {
    path: '/dashboard',
    component: Layout,
    redirect: '/dashboard/workplace',
    name: 'Dashboard',
    meta: {
      title: t('router.dashboard'),
      icon: 'ant-design:dashboard-filled',
      alwaysShow: true
    },
    children: [
      {
        path: 'workplace',
        component: () => import('@/views/Dashboard/Workplace.vue'),
        name: 'Workplace',
        meta: {
          title: t('router.workplace'),
          noCache: true
        }
      }
    ]
  },
  {
    path: '/stock',
    component: Layout,
    redirect: '/stock/sector-rotation',
    name: 'Stock',
    meta: {
      title: '股票分析',
      icon: 'mdi:chart-line',
      alwaysShow: true
    },
    children: [
      {
        path: 'sector-rotation',
        component: () => import('@/views/Vadmin/Stock/SectorRotation/SectorRotation.vue'),
        name: 'SectorRotation',
        meta: {
          title: '板块轮动',
          noCache: true
        }
      },
      {
        path: 'market-dashboard',
        component: () => import('@/views/Vadmin/Stock/MarketDashboard/MarketDashboard.vue'),
        name: 'MarketDashboard',
        meta: {
          title: '大盘座舱',
          noCache: true
        }
      },
      {
        path: 'daily-ranking',
        component: () => import('@/views/Vadmin/Stock/DailyRanking/DailyRanking.vue'),
        name: 'DailyRanking',
        meta: {
          title: '每日排行',
          noCache: true
        }
      },
      {
        path: 'base-info',
        component: () => import('@/views/Vadmin/Stock/BaseInfo/BaseInfo.vue'),
        name: 'StockBaseInfo',
        meta: {
          title: '股票基础信息',
          noCache: true
        }
      },
      {
        path: 'hot-news',
        component: () => import('@/views/Vadmin/Stock/HotNews/HotNews.vue'),
        name: 'HotNews',
        meta: {
          title: '热门头条',
          noCache: true
        }
      },
      {
        path: 'review',
        component: () => import('@/views/Vadmin/Stock/Review/Review.vue'),
        name: 'ReviewWorkbench',
        meta: {
          title: '复盘工作台',
          noCache: true
        }
      },
      {
        path: 'experience',
        component: () => import('@/views/Vadmin/Stock/Review/Experience.vue'),
        name: 'ExperienceLibrary',
        meta: {
          title: '心得经验库',
          noCache: true
        }
      },
      {
        path: 'rules',
        component: () => import('@/views/Vadmin/Stock/Review/Rules.vue'),
        name: 'RiskRules',
        meta: {
          title: '雷区基线',
          noCache: true
        }
      },
      {
        path: 'calendar',
        component: () => import('@/views/Vadmin/Stock/InvestCalendar/InvestCalendar.vue'),
        name: 'InvestCalendar',
        meta: {
          title: '财经日历',
          noCache: true
        }
      },
      {
        path: 'cloud-map',
        component: () => import('@/views/Vadmin/Stock/MarketCloudMap/MarketCloudMap.vue'),
        name: 'MarketCloudMap',
        meta: {
          title: '大盘云图',
          noCache: true
        }
      },
      {
        path: 'mainforce',
        component: () => import('@/views/Vadmin/Stock/Fund/MainForce.vue'),
        name: 'MainForceAnalysis',
        meta: {
          title: '主力分析',
          noCache: true
        }
      },
      {
        path: 'screener',
        component: () => import('@/views/Vadmin/Stock/Screener/Screener.vue'),
        name: 'StockScreener',
        meta: {
          title: '智能选股',
          noCache: true
        }
      },
      {
        path: 'selection-signal',
        component: () => import('@/views/Vadmin/Stock/SelectionSignal/SelectionSignal.vue'),
        name: 'SelectionSignal',
        meta: {
          title: '选股信号',
          noCache: true
        }
      },
      {
        path: 'pattern',
        component: () => import('@/views/Vadmin/Stock/Pattern/Pattern.vue'),
        name: 'PatternRecognition',
        meta: {
          title: '形态识别',
          noCache: true
        }
      },
      {
        path: 'aggregate',
        component: () => import('@/views/Vadmin/Stock/Aggregate/Aggregate.vue'),
        name: 'StockAggregate',
        meta: {
          title: '股票全景',
          noCache: true
        }
      },
      // AI 分析模块
      {
        path: 'ai-chat',
        component: () => import('@/views/Vadmin/Stock/AI/Chat/Chat.vue'),
        name: 'AIChat',
        meta: {
          title: 'AI对话助手',
          noCache: true
        }
      },
      {
        path: 'ai-workbench',
        component: () => import('@/views/Vadmin/Stock/AI/Workbench/Workbench.vue'),
        name: 'AIWorkbench',
        meta: {
          title: 'AI分析师工作台',
          noCache: true
        }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  strict: true,
  routes: constantRouterMap as RouteRecordRaw[],
  scrollBehavior: () => ({ left: 0, top: 0 })
})

export const resetRouter = (): void => {
  const resetWhiteNameList = ['Login', 'NoFind', 'Root']
  router.getRoutes().forEach((route) => {
    const { name } = route
    if (name && !resetWhiteNameList.includes(name as string)) {
      router.hasRoute(name) && router.removeRoute(name)
    }
  })
}

export const setupRouter = (app: App<Element>) => {
  app.use(router)
}

export default router
