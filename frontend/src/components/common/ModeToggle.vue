<template>
  <div 
    class="flex bg-slate-50 p-1.5 rounded-xl relative w-full h-[50px] border border-transparent hover:border-primary/10 transition-all shadow-subtle group overflow-hidden"
  >
    <div 
      v-if="activeIndex !== -1"
      class="absolute top-1.5 bottom-1.5 bg-white shadow-sm rounded-lg transition-all duration-400 ease-[cubic-bezier(0.2,1,0.2,1)]"
      :style="{ 
        width: `calc(${100 / options.length}% - 3px)`, 
        left: `calc(${(100 / options.length) * activeIndex}% + 1.5px)`,
      }"
    ></div>

    <button 
      v-for="(opt, index) in options" :key="opt.value"
      @click="$emit('update:modelValue', opt.value)"
      class="flex-1 rounded-lg text-xs font-black transition-colors duration-300 relative z-10 flex items-center justify-center active:scale-[0.97]"
      :class="modelValue === opt.value ? 'text-primary' : 'text-slate-400 hover:text-heading'"
    >
      {{ opt.label }}
    </button>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{ 
  modelValue: string, 
  options: { label: string, value: string }[] 
}>();

const emit = defineEmits(['update:modelValue']);

// 计算当前激活项的索引，用于滑块定位
const activeIndex = computed(() => {
  return props.options.findIndex(opt => opt.value === props.modelValue);
});
</script>