import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './index.css'
import '@fortawesome/fontawesome-free/css/all.min.css'
const app = createApp(App)
app.use(router)
app.mount('#app') 