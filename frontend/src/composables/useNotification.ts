import { ref } from 'vue';

export type NotificationType = 'success' | 'error' | 'info' | 'warning';

interface Notification {
  id: number;
  type: NotificationType;
  title: string;
  message: string;
}

const notifications = ref<Notification[]>([]);
let counter = 0;

export function useNotification() {
  const add = (type: NotificationType, title: string, message: string, duration = 4000) => {
    const id = counter++;
    notifications.value.unshift({ id, type, title, message });

    if (duration > 0) {
      setTimeout(() => remove(id), duration);
    }
  };

  const remove = (id: number) => {
    const index = notifications.value.findIndex(n => n.id === id);
    if (index !== -1) notifications.value.splice(index, 1);
  };

  return {
    notifications,
    remove,
    success: (title: string, message: string) => add('success', title, message),
    error: (title: string, message: string) => add('error', title, message),
    info: (title: string, message: string) => add('info', title, message),
    warning: (title: string, message: string) => add('warning', title, message),
  };
}