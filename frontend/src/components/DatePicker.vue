<template>
  <div class="relative w-full text-left" v-click-outside="() => (isOpen = false)">
    <div 
      @click="isOpen = !isOpen"
      class="w-full bg-slate-50 border border-transparent hover:border-primary/20 hover:bg-white rounded-lg px-6 h-[48px] flex items-center justify-between cursor-pointer transition-all group active:scale-[0.99] shadow-subtle hover:shadow-main"
    >
      <div class="flex items-center gap-4 overflow-hidden">
        <Calendar :size="18" class="text-slate-300 group-hover:text-primary transition-colors" />
        <div class="flex flex-col min-w-0">
          <span v-if="modelValue" class="text-[9px] font-black uppercase text-primary tracking-tighter mb-0.5 text-left">Selected Date</span>
          <span :class="modelValue ? 'text-heading' : 'text-slate-400'" class="font-bold text-sm font-mono tracking-tight">
            {{ modelValue || '选择时间' }}
          </span>
        </div>
      </div>
      <ChevronDown :size="16" :class="{'rotate-180': isOpen}" class="text-slate-300 group-hover:text-primary transition-transform duration-300" />
    </div>

    <transition name="fade-up">
      <div v-if="isOpen" class="absolute z-[110] left-0 mt-3 w-full max-w-[340px] bg-surface/95 backdrop-blur-xl border border-slate-100 rounded-lg shadow-active p-6 animate-fade-up origin-top">
        <div class="flex items-center justify-between mb-6 px-1">
          <button @click.stop="prevMonth" class="p-2 hover:bg-slate-50 rounded-md transition-colors text-slate-400 hover:text-primary"><ChevronLeft :size="18" /></button>
          <div class="flex flex-col items-center">
            <span class="text-sm font-black text-heading">{{ monthNames[viewDate.getMonth()] }}</span>
            <span class="text-[10px] font-mono font-bold text-slate-400 uppercase tracking-tighter">{{ viewDate.getFullYear() }}</span>
          </div>
          <button @click.stop="nextMonth" class="p-2 hover:bg-slate-50 rounded-md transition-colors text-slate-400 hover:text-primary"><ChevronRight :size="18" /></button>
        </div>

        <div class="grid grid-cols-7 gap-1 mb-2">
          <div v-for="day in ['日', '一', '二', '三', '四', '五', '六']" :key="day" class="text-center text-[9px] font-black text-slate-300 uppercase py-2">{{ day }}</div>
        </div>

        <div class="grid grid-cols-7 gap-1">
          <div 
            v-for="{ date, isCurrentMonth, dateString } in calendarDays" 
            :key="dateString"
            @click.stop="selectDate(dateString)"
            class="aspect-square flex items-center justify-center text-xs font-bold rounded-md cursor-pointer transition-all relative group/day"
            :class="[!isCurrentMonth ? 'text-slate-200' : 'text-heading hover:bg-slate-50', modelValue === dateString ? 'bg-primary! text-white! shadow-lg shadow-primary/20' : '']"
          >
            {{ date.getDate() }}
            <div v-if="isToday(date) && modelValue !== dateString" class="absolute bottom-1.5 w-1 h-1 bg-primary rounded-full opacity-40"></div>
          </div>
        </div>

        <div class="mt-6 pt-4 border-t border-slate-50 flex justify-between px-1">
          <button @click.stop="setToday" class="text-[10px] font-black uppercase text-primary hover:bg-primary/5 px-3 py-1 rounded-md transition-all">Today</button>
          <button @click.stop="isOpen = false" class="text-[10px] font-black uppercase text-slate-400 hover:text-heading px-3 py-1 rounded-md transition-all">Close</button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { Calendar, ChevronDown, ChevronLeft, ChevronRight } from 'lucide-vue-next';

const props = defineProps<{ modelValue: string }>();
const emit = defineEmits(['update:modelValue']);
const isOpen = ref(false);

// 初始化 viewDate，如果传入的值为空，默认显示今天
const viewDate = ref(props.modelValue ? new Date(props.modelValue.replace(/-/g, '/')) : new Date());
const monthNames = ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"];

const vClickOutside = {
  mounted(el: any, binding: any) {
    el.clickOutsideEvent = (event: any) => { if (!(el === event.target || el.contains(event.target))) binding.value(); };
    document.addEventListener("click", el.clickOutsideEvent);
  },
  unmounted(el: any) { document.removeEventListener("click", el.clickOutsideEvent); },
};

// 格式化函数：改用本地时间获取，避免时差导致的日期偏差
const formatDate = (date: Date) => {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, '0');
  const d = String(date.getDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
};

const calendarDays = computed(() => {
  const year = viewDate.value.getFullYear();
  const month = viewDate.value.getMonth();
  const firstDay = new Date(year, month, 1).getDay();
  const lastDate = new Date(year, month + 1, 0).getDate();
  const days = [];
  
  const prevMonthLastDate = new Date(year, month, 0).getDate();
  for (let i = firstDay - 1; i >= 0; i--) { 
    const d = new Date(year, month - 1, prevMonthLastDate - i);
    days.push({ date: d, isCurrentMonth: false, dateString: formatDate(d) }); 
  }
  for (let i = 1; i <= lastDate; i++) { 
    const d = new Date(year, month, i);
    days.push({ date: d, isCurrentMonth: true, dateString: formatDate(d) }); 
  }
  const remain = 42 - days.length;
  for (let i = 1; i <= remain; i++) { 
    const d = new Date(year, month + 1, i);
    days.push({ date: d, isCurrentMonth: false, dateString: formatDate(d) }); 
  }
  return days;
});

const isToday = (date: Date) => {
  const now = new Date();
  return date.getFullYear() === now.getFullYear() && 
         date.getMonth() === now.getMonth() && 
         date.getDate() === now.getDate();
};

const selectDate = (dateStr: string) => { 
  emit('update:modelValue', dateStr); 
  isOpen.value = false; 
};

const prevMonth = () => { viewDate.value = new Date(viewDate.value.getFullYear(), viewDate.value.getMonth() - 1, 1); };
const nextMonth = () => { viewDate.value = new Date(viewDate.value.getFullYear(), viewDate.value.getMonth() + 1, 1); };
const setToday = () => { selectDate(formatDate(new Date())); };
</script>

<style scoped>
.fade-up-enter-active, .fade-up-leave-active { transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1); }
.fade-up-enter-from { opacity: 0; transform: translateY(12px) scale(0.98); }
.fade-up-leave-to { opacity: 0; transform: translateY(8px) scale(0.99); }
</style>