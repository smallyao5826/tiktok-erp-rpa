<template>
  <Modal 
    :visible="visible" 
    :title="title" 
    @close="handleClose"
    @confirm="handleConfirm"
    :width="width"
  >
    <div class="p-4">
      <p class="text-sm text-slate-600">{{ message }}</p>
    </div>
  </Modal>
</template>

<script setup lang="ts">
import Modal from './Modal.vue';

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: '确认操作'
  },
  message: {
    type: String,
    default: '确定要执行此操作吗？'
  },
  width: {
    type: String,
    default: '400px'
  }
});

const emit = defineEmits(['close', 'confirm']);

const handleClose = () => {
  emit('close');
};

const handleConfirm = () => {
  emit('confirm');
};
</script>
