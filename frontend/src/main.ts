import { createApp } from 'vue'
import App from './App.vue'
import './style.css'
import '@assets/animations.css'
import '@assets/lib/bootstrap-utilities.min.css'
import {router} from "./router/router.ts";
import YmapPlugin from 'vue-yandex-maps'
import {createPinia} from "pinia";

export const mapSettings = {
  apiKey: 'd9fafac2-a391-4a17-be16-f1e225e9b1ec',
  lang: 'ru_RU',
  coordorder: 'latlong',
  debug: true,
  version: '2.1'
}

createApp(App)
  .use(router)
  .use(createPinia())
  .use(YmapPlugin, mapSettings)
  .mount('#app')
