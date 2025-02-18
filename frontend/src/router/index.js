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
        name: 'AccountManagement',
        component: AccountManagement
      },
      {
        path: 'logs',
        name: 'LogManagement',
        component: LogManagement
      },
      {
        path: 'menus',
        name: 'MenuManagement',
        component: MenuManagement
      },
      {
        path: 'shops',
        name: 'ShopManagement',
        component: ShopManagement
      },
      {
        path: 'ratings',
        name: 'RatingManagement',
        component: RatingManagement
      },
      {
        path: 'comments',
        name: 'CommentManagement',
        component: CommentManagement
      },
      {
        path: 'users',
        name: 'UserManagement',
        component: UserManagement
      },
      {
        path: 'favorites',
        name: 'FavoriteManagement',
        component: FavoriteManagement
      },
      {
        path: 'git',
        name: 'GitManagement',
        component: GitManagement,
        meta: {
          requiresAuth: true,
          title: '版控管理'
        }
      },
      {
        path: 'bots',
        name: 'BotManagement',
        component: BotManagement,
        meta: {
          requiresAuth: true,
          title: '快速提問&預設訊息管理'
        }
      },
      {
        path: 'knowledge',
        name: 'KnowledgeManagement',
        component: KnowledgeManagement,
        meta: {
          title: '知識庫管理',
          requiresAuth: true
        }
      },
      {
        path: 'monitor',
        name: 'MonitorManagement',
        component: MonitorManagement,
        meta: {
          title: '監控管理',
          requiresAuth: true
        }
      },
      {
        path: 'projects',
        name: 'ProjectManagement',
        component: ProjectManagement,
        meta: {
          requiresAuth: true,
          title: '專案管理'
        }
      },
      {
        path: 'learning',
        name: 'LearningManagement',
        component: LearningManagement,
        meta: {
          requiresAuth: true,
          title: '學習中心管理'
        }
      },
      {
        path: 'banner',
        name: 'BannerManagement',
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

export default router 