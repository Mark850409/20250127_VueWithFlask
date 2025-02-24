import { createRouter, createWebHistory } from 'vue-router'
import FrontLayout from '@/layouts/FrontLayout.vue'
import AdminLayout from '@/components/admin/AdminLayout.vue'
import Dashboard from '@/components/admin/Dashboard.vue'
import AccountManagement from '@/components/admin/system/AccountManagement.vue'
import LogManagement from '@/components/admin/system/LogManagement.vue'
import MenuManagement from '@/components/admin/system/MenuManagement.vue'
import ShopManagement from '@/components/admin/order/ShopManagement.vue'
import RatingManagement from '@/components/admin/order/RatingManagement.vue'
import CommentManagement from '@/components/admin/order/CommentManagement.vue'
import UserManagement from '@/components/admin/personal/UserManagement.vue'
import FavoriteManagement from '@/components/admin/personal/FavoriteManagement.vue'
import GitManagement from '@/components/admin/system/GitManagement.vue'
import NotFound from '@/views/error/NotFound.vue'
import Home from '@/components/food/FoodRecommendation.vue'
import Features from '@/components/food/pages/Features.vue'
import Learning from '@/components/food/pages/Learning.vue'
import Pricing from '@/components/food/pages/Pricing.vue'
import Login from '@/views/auth/Login.vue'
import ResetPassword from '@/views/auth/ResetPassword.vue'
import BotManagement from '@/components/admin/Bot/BotManagement.vue'
import KnowledgeManagement from '@/components/admin/knowledge/KnowledgeManagement.vue'
import MonitorManagement from '@/components/admin/monitor/MonitorManagement.vue'
import ProjectManagement from '@/components/admin/projects/ProjectManagement.vue'
import BannerManagement from '@/components/admin/banner/BannerManagement.vue'
import LearningManagement from '@/components/admin/learning/LearningManagement.vue'

const routes = [
  {
    path: '/',
    component: FrontLayout,
    children: [
      {
        path: '',
        name: 'Home',
        component: Home
      },
      {
        path: 'features',
        name: 'Features',
        component: Features
      },
      {
        path: 'learning',
        name: 'Learning',
        component: Learning
      },
      {
        path: 'pricing',
        name: 'Pricing',
        component: Pricing
      }
    ]
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/admin',
    component: AdminLayout,
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: Dashboard
      },
      {
        path: 'accounts',
        name: 'accounts',
        component: AccountManagement
      },
      {
        path: 'logs',
        name: 'logs',
        component: LogManagement
      },
      {
        path: 'menus',
        name: 'menus',
        component: MenuManagement
      },
      {
        path: 'shops',
        name: 'shops',
        component: ShopManagement
      },
      {
        path: 'ratings',
        name: 'ratings',
        component: RatingManagement
      },
      {
        path: 'comments',
        name: 'comments',
        component: CommentManagement
      },
      {
        path: 'users',
        name: 'users',
        component: UserManagement
      },
      {
        path: 'favorites',
        name: 'favorites',
        component: FavoriteManagement
      },
      {
        path: 'git',
        name: 'git',
        component: GitManagement,
        meta: {
          requiresAuth: true,
          title: '版控管理'
        }
      },
      {
        path: 'bots',
        name: 'bots',
        component: BotManagement,
        meta: {
          requiresAuth: true,
          title: '快速提問&預設訊息管理'
        }
      },
      {
        path: 'knowledge',
        name: 'knowledge',
        component: KnowledgeManagement,
        meta: {
          title: '知識庫管理',
          requiresAuth: true
        }
      },
      {
        path: 'monitor',
        name: 'monitor',
        component: MonitorManagement,
        meta: {
          title: '監控管理',
          requiresAuth: true
        }
      },
      {
        path: 'projects',
        name: 'projects',
        component: ProjectManagement,
        meta: {
          requiresAuth: true,
          title: '專案管理'
        }
      },
      {
        path: 'learning',
        name: 'learning',
        component: LearningManagement,
        meta: {
          requiresAuth: true,
          title: '學習中心管理'
        }
      },
      {
        path: 'banner',
        name: 'banner',
        component: BannerManagement,
        meta: {
          title: '輪播圖管理',
          requiresAuth: true
        }
      }
    ]
  },
  {
    path: '/404',
    name: 'NotFound',
    component: NotFound,
    props: true
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/404'
  },
  {
    path: '/reset-password/:token',
    name: 'ResetPassword',
    component: ResetPassword
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

router.beforeEach((to, from, next) => {
  const isAdmin = localStorage.getItem('isAdmin') === 'true'
  
  // 檢查是否需要管理員權限的路由
  if (to.path.startsWith('/admin')) {
    if (!isAdmin) {
      // 如果不是管理員，重定向到首頁
      next('/')
      return
    }
  }
  
  next()
})

export default router 