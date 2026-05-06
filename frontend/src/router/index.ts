import { createRouter, createWebHistory } from 'vue-router';
import MainLayout from '../layouts/MainLayout.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: () => import('../views/Login.vue'),
    },
    {
      path: '/',
      component: MainLayout,
      redirect: '/dashboard',
      children: [
        { path: 'dashboard', name: 'Dashboard', component: () => import('../views/Home.vue') },
        { path: 'shops', name: 'Shops', component: () => import('../views/Shops.vue') },
        // 闪购自动化模块
        { path: 'flash/add', name: 'FlashAdd', component: () => import('../views/flash/Add.vue') },
        { path: 'flash/manage', name: 'FlashManage', component: () => import('../views/flash/Manage.vue') },
        { path: 'flash/strategy', name: 'FlashStrategy', component: () => import('../views/flash/Strategy.vue') },
        // 发货管理模块
        { path: 'shipping/pre-launch', name: 'ShippingPreLaunch', component: () => import('../views/shipping/PreLaunch.vue') },
        // 设置页面
        { path: 'settings', name: 'Settings', component: () => import('../views/Settings.vue') },
        // 关于页面
        { path: 'about', name: 'About', component: () => import('../views/About.vue') },
      ]
    }
  ],
});

export default router;