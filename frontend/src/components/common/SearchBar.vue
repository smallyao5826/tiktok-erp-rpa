<template>
  <div class="relative group w-full h-[50px] transition-all">
    <div class="absolute left-5 top-1/2 -translate-y-1/2 z-10 pointer-events-none text-slate-300 group-focus-within:text-primary transition-colors">
      <Search v-if="!loading" :size="18" />
      <Loader2 v-else :size="18" class="animate-spin" />
    </div>

    <input 
      :value="modelValue"
      @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
      @keyup.enter="handleTrigger"
      :placeholder="placeholder"
      class="w-full h-full bg-slate-50 border border-transparent rounded-xl pl-12 pr-12 text-sm font-bold text-heading focus:bg-white focus:ring-4 focus:ring-primary/5 focus:border-primary/20 transition-all shadow-subtle hover:shadow-main outline-none placeholder:text-slate-300"
    >

    <div class="absolute right-2 top-1/2 -translate-y-1/2">
      <button 
        @click="handleTrigger"
        :disabled="loading || !modelValue.trim()"
        class="p-2 bg-primary text-white rounded-md shadow-md shadow-primary/20 hover:bg-primary/90 active:scale-90 disabled:opacity-0 transition-all flex items-center justify-center"
      >
        <ArrowRight :size="14" stroke-width="4" />
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Search, Loader2, ArrowRight } from 'lucide-vue-next';

const props = defineProps<{ 
  modelValue: string, 
  loading?: boolean, 
  placeholder?: string 
}>();

const emit = defineEmits(['update:modelValue', 'search']);

const handleTrigger = () => {
  if (props.loading || !props.modelValue.trim()) return;
  emit('search', props.modelValue.trim());
};
</script>