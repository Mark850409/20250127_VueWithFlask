import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router'
import './assets/css/main.css'
import './assets/css/RWD.css'
import '@fortawesome/fontawesome-free/css/all.min.css'
import 'remixicon/fonts/remixicon.css'
import './assets/css/dark.css'

const app = createApp(App)
const pinia = createPinia()

// 初始化主題
const initTheme = () => {
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme === 'dark') {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
}

// 在應用啟動前初始化主題
initTheme()

app.use(ElementPlus)
app.use(pinia)
app.use(router)
app.mount('#app')