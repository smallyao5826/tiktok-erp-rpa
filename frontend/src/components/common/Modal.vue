<template>
  <div v-if="visible" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
    <div class="bg-white rounded-xl shadow-xl max-w-md w-full mx-4">
      <div class="p-6 border-b border-slate-100">
        <h3 class="text-xl font-black text-heading tracking-tight">{{ title }}</h3>
      </div>
      <div class="p-6">
        <slot></slot>
      </div>
      <div class="p-4 border-t border-slate-100 flex justify-end gap-3">
        <button 
          @click="$emit('close')"
          class="px-4 py-2 text-sm font-black text-slate-600 hover:bg-slate-50 rounded-md transition-colors"
        >
          取消
        </button>
        <button 
          @click="$emit('confirm')"
          class="px-4 py-2 text-sm font-black text-white bg-primary hover:bg-primary/90 rounded-md transition-colors"
        >
          确认
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  visible: boolean;
  title: string;
}>();

defineEmits<{
  (e: 'close'): void;
  (e: 'confirm'): void;
}>();
</script>