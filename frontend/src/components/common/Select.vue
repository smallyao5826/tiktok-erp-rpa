<template>
  <div class="relative">
    <select 
      :value="modelValue" 
      @input="$emit('update:modelValue', ($event.target as HTMLSelectElement).value)"
      class="w-full text-sm border border-slate-200 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-primary/30 transition-all hover:border-primary/50 cursor-pointer"
      @change="handleChange"
    >
      <option v-if="placeholder" value="">{{ placeholder }}</option>
      <option 
        v-for="option in options" 
        :key="option.value" 
        :value="option.value"
      >
        {{ option.label }}
      </option>
    </select>
  </div>
</template>

<script setup lang="ts">
const props = defineProps({
  modelValue: {
    type: [String, Number, Boolean],
    default: ''
  },
  options: {
    type: Array,
    default: () => []
  },
  placeholder: {
    type: String,
    default: ''
  }
});

const emit = defineEmits(['update:modelValue', 'change']);

const handleChange = (event: Event) => {
  const target = event.target as HTMLSelectElement;
  const value = target.value;
  emit('change', value);
};
</script>

<style scoped>
select {
  border-radius: 0.5rem !important;
  border: 1px solid #e2e8f0 !important;
  padding: 0.75rem !important;
  transition: all 0.2s ease !important;
}

select:hover {
  border-color: rgba(254, 44, 85, 0.5) !important;
  cursor: pointer !important;
}

select:focus {
  outline: none !important;
  box-shadow: 0 0 0 2px rgba(254, 44, 85, 0.3) !important;
  border-color: #FE2C55 !important;
}
</style>
