<template>
  <div class="fixed top-16 right-8 z-[200] flex flex-col gap-3 w-full max-w-[360px] pointer-events-none">
    <transition-group name="noti-stack">
      <div 
        v-for="note in notifications" :key="note.id"
        class="pointer-events-auto flex items-start gap-4 p-4 bg-surface/95 backdrop-blur-md border border-slate-200/50 shadow-main rounded-lg relative overflow-hidden group"
      >
        <div 
          class="absolute bottom-0 left-0 h-[2px] opacity-20 transition-all"
          :class="typeClass[note.type].bar"
          style="animation: progress 4s linear forwards"
        ></div>

        <div class="flex-shrink-0 mt-0.5">
          <component 
            :is="typeClass[note.type].icon" 
            :size="18" 
            :stroke-width="3" 
            :class="typeClass[note.type].iconColor" 
          />
        </div>

        <div class="flex-1 min-w-0">
          <h4 class="text-sm font-bold text-heading tracking-tight mb-1 uppercase">
            {{ note.title }}
          </h4>
          <p class="text-xs text-slate-500 font-medium leading-relaxed">
            {{ note.message }}
          </p>
        </div>

        <button 
          @click="remove(note.id)" 
          class="text-slate-300 hover:text-heading transition-all p-1 -mr-1"
        >
          <X :size="14" stroke-width="4" />
        </button>
      </div>
    </transition-group>
  </div>
</template>

<script setup lang="ts">
import { CheckCircle2, AlertCircle, Info, XCircle, X } from 'lucide-vue-next';
import { useNotification } from '../../composables/useNotification';

const { notifications, remove } = useNotification();

const typeClass = {
  success: {
    icon: CheckCircle2,
    bar: 'bg-green-500',
    iconColor: 'text-green-500'
  },
  error: {
    icon: XCircle,
    bar: 'bg-primary', 
    iconColor: 'text-primary'
  },
  warning: {
    icon: AlertCircle,
    bar: 'bg-amber-500',
    iconColor: 'text-amber-500'
  },
  info: {
    icon: Info,
    bar: 'bg-secondary',
    iconColor: 'text-secondary'
  }
};
</script>

<style scoped>
/* 1. 堆叠动画：Pop & Slide 组合 */
.noti-stack-enter-active {
  transition: all 0.5s cubic-bezier(0.2, 1.2, 0.3, 1.2); /* 带有轻微弹性 */
}
.noti-stack-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: absolute; /* 确保堆叠移动顺滑 */
}

.noti-stack-enter-from {
  opacity: 0;
  transform: translateX(50px) scale(0.8);
}
.noti-stack-leave-to {
  opacity: 0;
  transform: translateX(30px) scale(0.95);
}

/* 2. 列表移动动效：当一条消失时，其他通知平滑上移 */
.noti-stack-move {
  transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

/* 3. 底部进度条动画 */
@keyframes progress {
  from { width: 100%; }
  to { width: 0%; }
}

/* 隐藏滚动条 */
.hide-scrollbar::-webkit-scrollbar { display: none; }
</style>