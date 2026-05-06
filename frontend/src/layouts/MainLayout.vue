<template>
  <div class="h-full w-full flex overflow-hidden bg-canvas">
    
    <aside class="w-64 relative h-full bg-surface border-r border-slate-100 flex flex-col overflow-hidden z-20">
      <div class="flex-1 flex flex-col p-4 overflow-hidden">
        
        <div class="flex items-center mb-10 h-9 px-2">
          <div class="flex items-center gap-2.5 overflow-hidden">
            <div class="w-9 h-9 bg-primary rounded-md flex-shrink-0 flex items-center justify-center text-white shadow-active">
              <Zap :size="18" stroke-width="3" />
            </div>
            <span class="text-lg font-black uppercase tracking-tighter text-heading whitespace-nowrap">
              Automator
            </span>
          </div>
        </div>
        
        <nav class="flex-1 space-y-1 overflow-y-auto hide-scrollbar">
          <router-link to="/dashboard" class="nav-item group" active-class="nav-active">
            <LayoutDashboard :size="20" class="flex-shrink-0" />
            <div class="flex items-center gap-2">
              <span class="text-base">首页</span>
              <span class="text-xs text-slate-400 font-normal">Dashboard</span>
            </div>
          </router-link>

          <router-link to="/shops" class="nav-item group" active-class="nav-active">
            <Store :size="20" class="flex-shrink-0" />
            <div class="flex items-center gap-2">
              <span class="text-base">店铺</span>
              <span class="text-xs text-slate-400 font-normal">Shops</span>
            </div>
          </router-link>

          <div class="space-y-1">
            <div 
              @click="groups.shipping = !groups.shipping" 
              class="nav-item justify-between group cursor-pointer"
              :class="[ $route.path.startsWith('/shipping') ? 'nav-active' : '' ]"
            >
              <div class="flex items-center gap-3">
                <Package :size="20" class="flex-shrink-0" />
                <div class="flex items-center gap-2">
                  <span class="text-base">发货</span>
                  <span class="text-xs text-slate-400 font-normal">Shipping</span>
                </div>
              </div>
              <ChevronDown :size="14" :class="{'rotate-180': groups.shipping}" class="transition-transform opacity-40" />
            </div>
            
            <transition name="expand">
              <div v-show="groups.shipping" class="pl-10 space-y-1 overflow-hidden mt-1">
                <router-link to="/shipping/pre-launch" class="nav-sub-item text-sm" active-class="nav-sub-active">预上线</router-link>
              </div>
            </transition>
          </div>

          <div class="space-y-1">
            <div 
              @click="groups.flash = !groups.flash" 
              class="nav-item justify-between group cursor-pointer"
              :class="[ $route.path.startsWith('/flash') ? 'nav-active' : '' ]"
            >
              <div class="flex items-center gap-3">
                <Zap :size="20" class="flex-shrink-0" />
                <div class="flex items-center gap-2">
                  <span class="text-base">闪购</span>
                  <span class="text-xs text-slate-400 font-normal">Flash Sale</span>
                </div>
              </div>
              <ChevronDown :size="14" :class="{'rotate-180': groups.flash}" class="transition-transform opacity-40" />
            </div>
            
            <transition name="expand">
              <div v-show="groups.flash" class="pl-10 space-y-1 overflow-hidden mt-1">
                <router-link to="/flash/add" class="nav-sub-item text-sm" active-class="nav-sub-active">添加闪购</router-link>
                <router-link to="/flash/manage" class="nav-sub-item text-sm" active-class="nav-sub-active">管理闪购</router-link>
                <router-link to="/flash/strategy" class="nav-sub-item text-sm" active-class="nav-sub-active">价格策略</router-link>
              </div>
            </transition>
          </div>
        </nav>

        <div class="mt-auto pt-6 border-t border-slate-50">
          <router-link to="/settings" class="nav-item group" active-class="nav-active">
            <Settings :size="20" class="flex-shrink-0" />
            <div class="flex items-center gap-2">
              <span class="text-base">设置</span>
              <span class="text-xs text-slate-400 font-normal">Settings</span>
            </div>
          </router-link>
          <router-link to="/about" class="nav-item group" active-class="nav-active">
            <Info :size="20" class="flex-shrink-0" />
            <div class="flex items-center gap-2">
              <span class="text-base">关于</span>
              <span class="text-xs text-slate-400 font-normal">About</span>
            </div>
          </router-link>
        </div>
      </div>
    </aside>

    <main class="flex-1 h-full flex flex-col min-w-0 bg-canvas overflow-hidden">
      <div class="flex-1 overflow-y-auto custom-scrollbar">
        <div class="mx-auto max-w-[1440px] min-h-full p-10 space-y-8">
          <router-view v-slot="{ Component }">
            <transition name="page-slide" mode="out-in">
              <component :is="Component" />
            </transition>
          </router-view>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue';
import { useRoute } from 'vue-router';
import { 
  LayoutDashboard, Zap, Store, UserRoundPlus, ChevronDown ,Settings, Package, Info
} from 'lucide-vue-next';

const route = useRoute();

// 只保留菜单分组的展开/收起状态
const groups = reactive({
  flash: route.path.startsWith('/flash'),
  shipping: route.path.startsWith('/shipping')
});
</script>

<style scoped>
/* 子菜单展开动画 */
.expand-enter-active, .expand-leave-active {
  transition: all 0.3s ease-in-out;
  max-height: 200px;
}
.expand-enter-from, .expand-leave-to {
  max-height: 0;
  opacity: 0;
}

/* 隐藏滚动条 */
.hide-scrollbar {
  scrollbar-width: none;
  -ms-overflow-style: none;
}
.hide-scrollbar::-webkit-scrollbar {
  display: none;
}

/* 导航项 Active 状态 */
.nav-active {
  font-weight: 900 !important;
}
</style>