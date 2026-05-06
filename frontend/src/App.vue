<template>
  <div class="app-shell flex flex-col h-screen w-screen overflow-hidden bg-canvas">
    
    <header 
      class="window-header h-10 flex-shrink-0 flex items-center justify-between px-4 bg-surface border-b border-slate-100 select-none z-[9999] relative"
      data-tauri-drag-region
    >
      <div class="flex items-center gap-2 pointer-events-none">
        <Zap :size="14" class="text-primary fill-primary/10" />
        <span class="text-xs font-black uppercase tracking-[0.2em] text-slate-400">
          MiaoShou · TikTok RPA
        </span>
      </div>

      <div class="flex items-center gap-1 relative z-20">
        <button @click.stop="minimizeWindow" class="control-btn hover:bg-slate-100 pointer-events-auto">
          <Minus :size="14" stroke-width="3" />
        </button>
        <button @click.stop="toggleMaximizeWindow" class="control-btn hover:bg-slate-100 pointer-events-auto">
          <Square :size="12" stroke-width="3" />
        </button>
        <button @click.stop="closeWindow" class="control-btn close-btn pointer-events-auto">
          <X :size="14" stroke-width="3" />
        </button>
      </div>
    </header>

    <main class="flex-1 relative overflow-hidden bg-canvas">
      <router-view v-slot="{ Component }">
        <transition name="page-slide" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <Notification />
  </div>
</template>

<script setup lang="ts">
import { Minus, Square, X, Zap } from 'lucide-vue-next';
import Notification from './components/common/Notification.vue';
import { getCurrentWindow } from '@tauri-apps/api/window';

const appWindow = getCurrentWindow();
const minimizeWindow = () => appWindow.minimize();
const toggleMaximizeWindow = () => appWindow.toggleMaximize();
const closeWindow = () => appWindow.close();
</script>

<style>
@import "./style.css";

.control-btn {
  @apply w-8 h-8 flex items-center justify-center rounded-md transition-all text-slate-400 active:scale-90;
  cursor: default;
}
.close-btn:hover {
  @apply bg-primary text-white shadow-active;
}

/* 路由动画 */
.page-slide-enter-active, .page-slide-leave-active {
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}
.page-slide-enter-from { opacity: 0; transform: translateY(10px); }
.page-slide-leave-to { opacity: 0; transform: translateY(-8px); }

::-webkit-scrollbar { display: none; }
</style>