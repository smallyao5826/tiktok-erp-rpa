<template>
  <button
    :class="[
      'px-4 py-2 rounded-lg font-bold text-sm transition-all active:scale-95 flex items-center justify-center gap-2',
      variantClasses[variant],
      sizeClasses[size],
      { 'opacity-30 cursor-not-allowed': disabled || loading }
    ]"
    :disabled="disabled || loading"
    @click="$emit('click')"
  >
    <div v-if="loading" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
    <div v-if="loading" class="text-xs">查询中</div>
    <slot v-else></slot>
  </button>
</template>

<script setup lang="ts">
defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: (value: string) => ['primary', 'secondary', 'success', 'danger', 'ghost'].includes(value)
  },
  size: {
    type: String,
    default: 'medium',
    validator: (value: string) => ['small', 'medium', 'large'].includes(value)
  },
  disabled: {
    type: Boolean,
    default: false
  },
  loading: {
    type: Boolean,
    default: false
  }
});

defineEmits(['click']);

const variantClasses = {
  primary: 'bg-primary text-white hover:bg-primary/90',
  secondary: 'bg-secondary text-white hover:bg-secondary/90',
  success: 'bg-emerald-500 text-white hover:bg-emerald-600',
  danger: 'bg-red-500 text-white hover:bg-red-600',
  ghost: 'bg-transparent hover:bg-slate-100 text-slate-700'
};

const sizeClasses = {
  small: 'h-8 px-3 text-xs',
  medium: 'h-10 px-4 text-sm',
  large: 'h-12 px-6 text-base'
};
</script>

<style scoped>
@reference "../../style.css";
</style>
