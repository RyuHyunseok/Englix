<template>
  <nav class="side-nav">
    <div class="nav-content">
      <div class="nav-header">
        <router-link to="/" class="nav-logo">|ENGLIX|</router-link>
      </div>

      <div class="nav-search">
        <div class="search-wrapper">
          <i class="fas fa-search search-icon"></i>
          <input v-model="searchQuery" @keyup.enter="handleSearch" type="text" placeholder="Search movies..." class="search-input" />
        </div>
      </div>

      <div class="nav-links">
        <router-link to="/movielist" class="nav-link">
          <i class="fas fa-film"></i>
          <span>Movies</span>
        </router-link>

        <a @click="handleCommunityClick" class="nav-link">
          <i class="fas fa-users"></i>
          <span>Community</span>
        </a>

        <router-link v-if="isLogin" to="/mypage" class="nav-link">
          <i class="fas fa-user"></i>
          <span>My Page</span>
        </router-link>

        <template v-if="!isLogin">
          <router-link to="/signup" class="nav-link">
            <i class="fas fa-user-plus"></i>
            <span>Sign Up</span>
          </router-link>

          <router-link to="/login" class="nav-link">
            <i class="fas fa-sign-in-alt"></i>
            <span>Sign In</span>
          </router-link>
        </template>

        <template v-else>
          <a @click="handleRecommendClick" class="nav-link special-link">
            <i class="fas fa-thumbs-up"></i>
            <span>For You</span>
          </a>

          <a @click="handleLogout" class="nav-link">
            <i class="fas fa-sign-out-alt"></i>
            <span>Sign Out</span>
          </a>
        </template>
      </div>
    </div>

    <div class="theme-container">
      <div class="theme-section">
        <button @click="toggleTheme" class="theme-toggle" :class="{ 'is-dark': isDarkMode }">
          <div class="toggle-track">
            <i class="fas fa-sun sun-icon"></i>
            <i class="fas fa-moon moon-icon"></i>
            <div class="toggle-thumb"></div>
          </div>
        </button>
        <span class="theme-text">{{ isDarkMode ? "Dark" : "Light" }} Mode</span>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import axios from "axios";
import { storeToRefs } from "pinia";
import { useThemeStore } from "@/stores/theme";
import { useToastStore } from "@/stores/toast";

const toastStore = useToastStore();

const themeStore = useThemeStore();

const router = useRouter();
const authStore = useAuthStore();
const { isLogin } = storeToRefs(authStore);
const searchQuery = ref("");
const { isDarkMode } = storeToRefs(themeStore);

const handleCommunityClick = () => {
  if (!isLogin.value) {
    toastStore.addToast("로그인이 필요한 서비스입니다.", "warning");
    router.push("/login");
    return;
  }
  router.push("/community");
};

const handleSearch = async () => {
  if (!searchQuery.value.trim()) return;

  try {
    const auth = localStorage.getItem("auth");
    if (!auth) return;

    const { token } = JSON.parse(auth);

    const response = await axios({
      method: "get",
      url: "http://127.0.0.1:8000/movie/search/",
      headers: {
        Authorization: `Token ${token}`,
      },
      params: {
        query: searchQuery.value,
      },
    });

    router.push({
      name: "searchResults",
      query: {
        q: searchQuery.value,
        results: JSON.stringify(response.data),
      },
    });

    searchQuery.value = "";
  } catch (error) {
    console.error("검색 실패:", error);
  }
};

const handleLogout = async () => {
  try {
    await authStore.logout();
    toastStore.addToast("로그아웃 되었습니다!", "success");
    router.push({ name: "Home" });
  } catch (error) {
    console.error("로그아웃 실패:", error);
  }
};

const handleRecommendClick = async () => {
  try {
    const auth = localStorage.getItem("auth");
    if (!auth) {
      alert("로그인이 필요합니다.");
      router.push("/login");
      return;
    }

    const { token } = JSON.parse(auth);

    // 사용자 정보 가져오기
    const response = await axios({
      method: "get",
      url: "http://127.0.0.1:8000/accounts/user/",
      headers: {
        Authorization: `Token ${token}`,
      },
    });

    const userData = response.data;
    console.log("전체 User Data:", userData); // 전체 데이터 확인
    console.log("goal:", userData.goal); // goal 값 확인
    console.log("level:", userData.level); // level 값 확인
    console.log("Condition check:", Boolean(userData.goal && userData.level)); // 조건문 결과 확인

    if (userData.goal && userData.level) {
      console.log("Movie 페이지로 이동 시도");
      // 선호도 정보가 있으면 movie 페이지로 이동
      router.push({
        name: "movie", // name으로 변경
        query: {
          category: userData.goal,
          level: userData.level,
          genre: userData.prefer_genre,
        },
      });
    } else {
      console.log("Survey 페이지로 이동");
      // 선호도 정보가 없으면 survey 페이지로 이동
      router.push("/survey");
    }
  } catch (error) {
    console.error("사용자 정보 조회 실패:", error);
    if (error.response?.status === 401) {
      alert("로그인이 필요합니다.");
      router.push("/login");
    } else {
      alert("오류가 발생했습니다.");
      console.error("상세 에러:", error);
    }
  }
};

const toggleTheme = () => {
  themeStore.toggleTheme();
};
</script>

<style scoped>
.side-nav {
  width: 220px;
  height: 100vh;
  position: fixed;
  background-color: var(--surface-color);
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  justify-content: space-between; /* 상단 콘텐츠와 하단 테마 토글 사이 공간 분배 */
  transition: all 0.3s ease;
  overflow-y: auto;
}

/* 상단 네비게이션 콘텐츠 */
.nav-content {
  padding: 1.25rem 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 1.75rem;
}

.nav-header {
  text-align: center;
  padding: 0.5rem 0;
  color: #ff6b6b;
}

.nav-logo {
  font-size: 2rem;
  font-weight: bold;
  color: var(--primary-color);
  text-decoration: none;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
  display: inline-block;
}

.nav-search {
  padding: 0 0.5rem;
}

.search-wrapper {
  position: relative;
  width: 100%;
}

.search-icon {
  position: absolute;
  left: 0.8rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.search-input {
  width: 100%;
  box-sizing: border-box;
  padding: 0.7rem 1rem 0.7rem 2.3rem;
  border: 1.5px solid var(--border-color);
  border-radius: 8px;
  background-color: var(--surface-secondary);
  color: var(--text-color);
  font-size: 0.9rem;
  transition: all 0.2s ease;
}

.search-input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(var(--primary-color-rgb), 0.1);
}

.nav-links {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  padding: 0 0.5rem;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  padding: 0.8rem 1rem;
  color: var(--text-color);
  text-decoration: none;
  border-radius: 8px;
  font-weight: 500;
  font-size: 0.95rem;
  transition: all 0.2s ease;
  cursor: pointer;
}

.nav-link i {
  width: 18px;
  text-align: center;
  font-size: 1rem;
}

.nav-link:hover {
  background-color: var(--surface-hover);
  color: var(--primary-color);
  transform: translateX(3px);
}

.special-link {
  color: var(--primary-color);
  background-color: rgba(var(--primary-color-rgb), 0.1);
}

.special-link:hover {
  background-color: rgba(var(--primary-color-rgb), 0.15);
  color: var(--primary-color);
}

/* 테마 토글 컨테이너 */
.theme-container {
  padding: 1rem 0.75rem 1.5rem; /* 상하 여백 조정 */
  border-top: 1px solid var(--border-color); /* 구분선 추가 */
}

.theme-section {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  padding: 0.8rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  background-color: var(--surface-secondary);
}

.theme-section:hover {
  background-color: var(--surface-hover);
}

.theme-toggle {
  background: none;
  border: none;
  padding: 0;
  cursor: pointer;
  width: 46px;
  height: 24px;
}

.theme-text {
  font-size: 0.95rem;
  color: var(--text-color);
  font-weight: 500;
}

.toggle-track {
  width: 100%;
  height: 100%;
  background-color: #e2e8f0;
  border-radius: 12px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 4px;
  transition: background-color 0.3s ease;
}

.is-dark .toggle-track {
  background-color: #4a5568;
}

.sun-icon,
.moon-icon {
  font-size: 0.8rem;
  color: #718096;
  position: relative;
  z-index: 1;
}

.is-dark .sun-icon {
  color: #ffd700;
}

.is-dark .moon-icon {
  color: #ffffff;
}

.toggle-thumb {
  position: absolute;
  left: 2px;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background-color: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.is-dark .toggle-thumb {
  transform: translateX(22px);
}
</style>
