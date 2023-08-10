// import './assets/main.css'-

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"

import 'bootstrap/dist/js/bootstrap.js';
// import "@popperjs/core"
import $ from 'jquery';
window.$ = window.jQuery = $;


const app = createApp(App)

import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import { useAuthStore } from './stores/authStore'
const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)
app.use(pinia)
app.use(useAuthStore())

app.use(router)

app.mount('#app')
