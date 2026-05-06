import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

// 2. 后引入包含 Tailwind 的样式文件
import './style.css' 

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.mount('#app')