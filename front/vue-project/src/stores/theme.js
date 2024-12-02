// stores/theme.js
import { defineStore } from 'pinia';

export const useThemeStore = defineStore('theme', {
  state: () => ({
    isDarkMode: localStorage.getItem('theme') === 'dark'
  }),
  
  actions: {
    toggleTheme() {
      this.isDarkMode = !this.isDarkMode;
      // localStorage에 테마 설정 저장
      localStorage.setItem('theme', this.isDarkMode ? 'dark' : 'light');
      // HTML root element에 dark-mode 클래스 토글
      document.documentElement.classList.toggle('dark-mode');
    },
    
    initTheme() {
      // 페이지 로드 시 저장된 테마 설정 적용
      if (this.isDarkMode) {
        document.documentElement.classList.add('dark-mode');
      }
    }
  }
});