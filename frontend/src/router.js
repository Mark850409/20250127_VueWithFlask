import { createRouter, createWebHistory } from 'vue-router'
import FoodRecommendation from './components/food/FoodRecommendation.vue'
import Features from './components/food/pages/Features.vue'
import Learning from './components/food/pages/Learning.vue'
import Pricing from './components/food/pages/Pricing.vue'

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