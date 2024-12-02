import { defineStore } from "pinia";
import { ref } from "vue";

export const useToastStore = defineStore("toast", () => {
  const toasts = ref([]);

  const addToast = (message, type = "success", duration = 3000) => {
    const id = Date.now();

    toasts.value.push({
      id,
      message,
      type,
      duration,
    });

    setTimeout(() => {
      removeToast(id);
    }, duration);
  };

  const removeToast = (id) => {
    toasts.value = toasts.value.filter((toast) => toast.id !== id);
  };

  return {
    toasts,
    addToast,
    removeToast,
  };
});
