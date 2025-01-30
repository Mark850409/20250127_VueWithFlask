import { createRouter, createWebHistory } from 'vue-router'
import FrontLayout from './layouts/FrontLayout.vue'
import AdminLayout from './components/admin/AdminLayout.vue'
import Dashboard from './components/admin/Dashboard.vue'
import AccountManagement from './components/admin/system/AccountManagement.vue'
import LogManagement from './components/admin/system/LogManagement.vue'
import MenuManagement from './components/admin/system/MenuManagement.vue'
import ShopManagement from './components/admin/order/ShopManagement.vue'
import RatingManagement from './components/admin/order/RatingManagement.vue'
import CommentManagement from './components/admin/order/CommentManagement.vue'
import UserManagement from './components/admin/personal/UserManagement.vue'
import FavoriteManagement from './components/admin/personal/FavoriteManagement.vue'
import GitManagement from '@/views/admin/GitManagement.vue'

const routes = [
  {
    path: '/',
    component: FrontLayout,
    children: [
      {
        path: '',
        name: 'Home',
        component: () => import('./components/food/FoodRecommendation.vue')
      },
      {
        path: 'features',
        name: 'Features',
        component: () => import('./components/food/pages/Features.vue')
      },
      {
        path: 'learning',
        name: 'Learning',
        component: () => import('./components/food/pages/Learning.vue')
      },
      {
        path: 'pricing',
        name: 'Pricing',
        component: () => import('./components/food/pages/Pricing.vue')
      }
    ]
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('./views/auth/Login.vue')
  },
  {
    path: '/admin',
    component: AdminLayout,
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: () => import('./components/admin/Dashboard.vue')
      },
      {
        path: 'accounts',
        name: 'AccountManagement',
        component: () => import('./components/admin/system/AccountManagement.vue')
      },
      {
        path: 'logs',
        name: 'LogManagement', 
        component: () => import('./components/admin/system/LogManagement.vue')
      },
      {
        path: 'menus',
        name: 'MenuManagement',
        component: () => import('./components/admin/system/MenuManagement.vue')
      },
      {
        path: 'shops',
        name: 'ShopManagement',
        component: () => import('./components/admin/order/ShopManagement.vue')
      },
      {
        path: 'ratings',
        name: 'RatingManagement',
        component: () => import('./components/admin/order/RatingManagement.vue')
      },
      {
        path: 'comments',
        name: 'CommentManagement',
        component: () => import('./components/admin/order/CommentManagement.vue')
      },
      {
        path: 'users',
        name: 'UserManagement',
        component: () => import('./components/admin/personal/UserManagement.vue')
      },
      {
        path: 'favorites',
        name: 'FavoriteManagement',
        component: () => import('./components/admin/personal/FavoriteManagement.vue')
      },
      {
        path: 'git',
        name: 'GitManagement',
        component: GitManagement,
        meta: {
          requiresAuth: true,
          title: '版控管理'
        }
      }
    ]
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