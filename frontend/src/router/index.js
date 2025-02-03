import { createRouter, createWebHistory } from 'vue-router'
import Admin from '@/views/admin/Admin.vue'

const routes = [
  {
    path: '/admin',
    name: 'Admin',
    component: Admin,
    meta: { requiresAuth: true }
  }
  // ... 其他路由
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 添加路由守衛
router.beforeEach((to, from, next) => {
  console.log('路由變化:', to.path) // 新增
  if (to.matched.some(record => record.meta.requiresAuth)) {
    const token = localStorage.getItem('token')
    if (!token) {
      next('/login')
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router 