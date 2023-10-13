import HomeView from "../views/HomeView.vue";
import {createRouter, createWebHashHistory, RouteRecordRaw} from "vue-router";

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  }
]

export const router = createRouter({
  history: createWebHashHistory(),
  routes
})