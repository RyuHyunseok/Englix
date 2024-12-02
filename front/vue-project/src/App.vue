<template>
  <div class="app-layout">
    <side-nav class="app-sidebar" :class="{ 'mobile-hidden': !isSidebarVisible }" />
    <div class="app-content">
      <div class="mobile-menu-button" @click="toggleSidebar">
        <i class="fas fa-bars"></i>
      </div>
      <div class="content-container">
        <router-view />
      </div>
    </div>
    <ToastNotification />
  </div>
</template>

<script setup>
import { ref } from "vue";
import SideNav from "@/components/SideNav.vue";
import ToastNotification from "./components/ToastNotification.vue";

const isSidebarVisible = ref(false);

const toggleSidebar = () => {
  isSidebarVisible.value = !isSidebarVisible.value;
};
</script>

<style>
/* 전역 스타일 */
:root {
  --max-width: 1200px;
  --content-padding: 2rem;
}

.app-layout {
  display: flex;
  min-height: 100vh;
  position: relative;
}

.app-sidebar {
  position: fixed;
  width: var(--sidebar-width);
  height: 100vh;
  z-index: 1000;
}

.app-content {
  flex: 1;
  margin-left: var(--sidebar-width);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.content-container {
  max-width: var(--max-width);
  width: 100%;
  margin: 0 auto;
  padding: var(--content-padding);
  box-sizing: border-box;
  flex: 1;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .app-content {
    margin-left: 0;
  }

  .content-container {
    padding: 1rem;
  }
}

/* 공통 스타일 클래스 */
.section-container {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.page-title {
  font-size: 2rem;
  font-weight: 600;
  margin-bottom: 2rem;
  text-align: center;
}
.content-container {
  max-width: var(--max-width);
  width: 100%;
  margin: 0 auto;
  padding: 1rem 2rem; /* 상하 패딩 줄임 */
  box-sizing: border-box;
  flex: 1;
}
</style>
