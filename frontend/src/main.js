import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router'
import './index.css'
import '@fortawesome/fontawesome-free/css/all.min.css'

const app = createApp(App)

app.use(ElementPlus)
app.use(router)
app.mount('#app')

console.log('Environment Variables in main.js:', import.meta.env) 