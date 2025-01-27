import { createRouter, createWebHistory } from 'vue-router'
import FoodRecommendation from './components/food/FoodRecommendation.vue'
import Features from './components/food/pages/Features.vue'
import Learning from './components/food/pages/Learning.vue'
import Pricing from './components/food/pages/Pricing.vue'
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

const routes = [
  {
    path: '/',
    name: 'Home',
    component: FoodRecommendation
  },
  {
    path: '/features',
    name: 'Features',
    component: Features
  },
  {
    path: '/learning',
    name: 'Learning',
    component: Learning
  },
  {
    path: '/pricing',
    name: 'Pricing',
    component: Pricing
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