<template>
  <Transition name="fade">
    <div v-if="toasts.length" class="toast-container">
      <TransitionGroup name="toast">
        <div v-for="toast in toasts" :key="toast.id" class="toast" :class="toast.type">
          <div class="toast-content">
            <span class="toast-icon">
              <i class="fas" :class="toastIcon(toast.type)"></i>
            </span>
            <span class="toast-message">{{ toast.message }}</span>
          </div>
          <button @click="() => toastStore.removeToast(toast.id)" class="toast-close">
            <i class="fas fa-times"></i>
          </button>
        </div>
      </TransitionGroup>
    </div>
  </Transition>
</template>

<script setup>
import { useToastStore } from "@/stores/toast";
import { storeToRefs } from "pinia";

const toastStore = useToastStore();
const { toasts } = storeToRefs(toastStore);

const toastIcon = (type) => {
  switch (type) {
    case "success":
      return "fa-check-circle";
    case "error":
      return "fa-exclamation-circle";
    case "warning":
      return "fa-exclamation-triangle";
    default:
      return "fa-info-circle";
  }
};
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.toast {
  padding: 10px 14px;
  border-radius: 12px;
  min-width: 200px;
  max-width: 300px;
  background-color: white;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  display: flex;
  align-items: center;
  justify-content: space-between;
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.toast-content {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
}

.toast-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 13px;
  height: 13px;
  border-radius: 50%;
  font-size: 10px;
}

.toast-message {
  font-size: 13px;
  font-weight: 500;
  padding: 2px 0;
}

.toast-close {
  background: none;
  border: none;
  padding: 2px;
  cursor: pointer;
  opacity: 0.6;
  transition: opacity 0.2s;
  font-size: 12px;
  color: inherit;
  display: flex;
  align-items: center;
  justify-content: center;
}

.toast-close:hover {
  opacity: 1;
}

/* 토스트 타입별 스타일 */
.toast.success {
  background-color: #ebfbf2;
  border: 1px solid #d1f3e0;
  color: #0d6832;
}

.toast.success .toast-icon {
  background-color: #d1f3e0;
  color: #0d6832;
}

.toast.error {
  background-color: #fee7e7;
  border: 1px solid #fcd3d3;
  color: #b91c1c;
}

.toast.error .toast-icon {
  background-color: #fcd3d3;
  color: #b91c1c;
}

.toast.warning {
  background-color: #fff7ed;
  border: 1px solid #ffedd5;
  color: #c2410c;
}

.toast.warning .toast-icon {
  background-color: #ffedd5;
  color: #c2410c;
}

/* 토스트 애니메이션 */
.toast-enter-active,
.toast-leave-active {
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(30px) scale(0.9);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(30px) scale(0.95);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 모바일 대응 */
@media (max-width: 768px) {
  .toast-container {
    top: 10px;
    right: 10px;
    left: 10px;
  }

  .toast {
    min-width: unset;
    width: 100%;
  }
}
</style>
