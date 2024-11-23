import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

import App from './App.vue'
import './assets/styles/global.css'
import router from './router'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { library } from '@fortawesome/fontawesome-svg-core'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { far } from '@fortawesome/free-regular-svg-icons'
import { faXTwitter } from '@fortawesome/free-brands-svg-icons'
import { faInstagram } from '@fortawesome/free-brands-svg-icons'
import { faGoogle } from '@fortawesome/free-brands-svg-icons'

library.add(fas, far, faInstagram, faXTwitter, faGoogle)

const app = createApp(App)

app.use(router)

const pinia = createPinia()
app.use(pinia)
pinia.use(piniaPluginPersistedstate)

app.component('font-awesome-icon', FontAwesomeIcon)
app.mount('#app')
