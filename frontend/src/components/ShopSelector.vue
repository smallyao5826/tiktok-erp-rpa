<template>
  <div class="w-full">
    <div class="relative inline-block text-left transition-all w-full h-[50px]" v-click-outside="() => (isOpen = false)">
      <div 
          @click="isOpen = !isOpen" 
          class="w-full h-full bg-slate-50 border border-transparent hover:border-primary/20 hover:bg-white rounded-lg px-5 flex items-center justify-between cursor-pointer transition-all group active:scale-[0.99] shadow-subtle hover:shadow-main"
        >
      <div class="flex items-center gap-3 overflow-hidden">
        <div v-if="selectedShop" class="w-2 h-2 rounded-full flex-shrink-0 animate-pulse" :style="{ backgroundColor: getSiteColor(selectedShop.site) }"></div>
        <Store v-else :size="16" class="text-slate-300 group-hover:text-primary transition-colors" />
        
        <div class="flex flex-col min-w-0">
          <span v-if="selectedShop" class="text-[9px] font-black uppercase text-primary tracking-tighter">{{ getSiteName(selectedShop.site) }}</span>
          <span class="text-sm font-bold text-heading truncate tracking-tight">{{ displayText }}</span>
        </div>
      </div>
      <ChevronDown :size="16" :class="{'rotate-180': isOpen}" class="text-slate-300 group-hover:text-primary transition-transform duration-300" />
    </div>

    <transition name="fade-up">
      <div v-if="isOpen" class="absolute z-[100] w-full mt-2 bg-surface/95 backdrop-blur-xl border border-slate-100 rounded-lg shadow-active overflow-hidden origin-top">
        <div class="max-h-[300px] overflow-y-auto custom-scrollbar p-2">
          <div 
            v-for="shop in shops" :key="shop.shop_id"
            @click="toggleSelect(shop)"
            class="flex items-center justify-between p-3 rounded-md cursor-pointer transition-all mb-1 last:mb-0 group/item"
            :class="isSelected(shop.shop_id) ? 'bg-primary/5 shadow-sm' : 'hover:bg-slate-50'"
          >
            <div class="flex items-center gap-3 flex-1 overflow-hidden">
              <div class="w-1 h-8 rounded-full flex-shrink-0" :style="{ backgroundColor: getSiteColor(shop.site) }"></div>
              <div class="flex flex-col min-w-0">
                <span class="text-sm font-black text-heading group-hover/item:text-primary truncate">{{ shop.shop_nick }}</span>
                <span class="text-[10px] font-black uppercase opacity-60">{{ getSiteName(shop.site) }} 站点</span>
              </div>
            </div>
            <Check v-if="isSelected(shop.shop_id)" :size="14" stroke-width="4" class="text-primary" />
          </div>
        </div>
      </div>
    </transition>
      <div v-if="isOpen" @click="isOpen = false" class="fixed inset-0 z-[90]"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { Store, ChevronDown, Check } from 'lucide-vue-next';
import { shopApi } from '../api/shop';
import { getSiteName, getSiteColor } from '../utils/mapping';

const props = defineProps<{ modelValue: any; mode: 'single' | 'multiple'; }>();
const emit = defineEmits(['update:modelValue', 'change']);
const isOpen = ref(false);
const shops = ref<any[]>([]);

const vClickOutside = {
  mounted(el: any, binding: any) {
    el.clickOutsideEvent = (event: any) => { if (!(el === event.target || el.contains(event.target))) binding.value(); };
    document.addEventListener("click", el.clickOutsideEvent);
  },
  unmounted(el: any) { document.removeEventListener("click", el.clickOutsideEvent); },
};

const selectedShop = computed(() => (props.mode === 'single' && props.modelValue) ? shops.value.find(s => s.shop_id === props.modelValue) : null);
const isSelected = (id: string) => props.mode === 'multiple' ? props.modelValue.includes(id) : props.modelValue === id;
const displayText = computed(() => {
  if (!props.modelValue || (Array.isArray(props.modelValue) && props.modelValue.length === 0)) return '选择目标店铺';
  return props.mode === 'multiple' ? `已选择 ${props.modelValue.length} 个店铺` : (selectedShop.value?.shop_nick || '选择目标店铺');
});

const toggleSelect = (shop: any) => {
  if (props.mode === 'multiple') {
    const newVal = [...props.modelValue];
    const idx = newVal.indexOf(shop.shop_id);
    idx > -1 ? newVal.splice(idx, 1) : newVal.push(shop.shop_id);
    emit('update:modelValue', newVal);
  } else {
    emit('update:modelValue', shop.shop_id);
    isOpen.value = false;
  }
  emit('change', shop.shop_id);
};

onMounted(async () => {
  const res = await shopApi.getShops();
  if (res.data.code === 200) shops.value = res.data.data;
});
</script>

<style scoped>
.fade-up-enter-active, .fade-up-leave-active { transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1); }
.fade-up-enter-from { opacity: 0; transform: translateY(12px) scale(0.98); }
.fade-up-leave-to { opacity: 0; transform: translateY(8px) scale(0.99); }
</style>