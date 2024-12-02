<template>
  <nav
    class="sidebar"
    :class="{
      'sidebar-hidden': isHidden && !isAtTop,
      'sidebar-visible': isVisible || isAtTop,
      'sidebar-peek': isHidden && !isAtTop && !isVisible
    }"
    @mouseenter="handleMouseEnter"
  >
    <div class="nav-content">
      <!-- Logo -->
      <router-link to="/" class="nav-logo">
        ENGLIX|
      </router-link>

      <!-- Main Navigation -->
      <div class="nav-links">
        <!-- Search Box -->
        <div class="search-container">
          <div class="search-box">
            <input 
              v-model="searchQuery" 
              @keyup.enter="handleSearch" 
              type="text" 
              placeholder="Search movies..." 
              class="search-input" 
            />
            <button @click="handleSearch" class="search-button">
              <span class="search-icon">🔍</span>
            </button>
          </div>
        </div>

        <router-link to="/movielist" class="nav-link">
          <span class="nav-icon">🎬</span>
          <span class="nav-text">Movies</span>
        </router-link>
        
        <router-link to="/community" class="nav-link">
          <span class="nav-icon">💭</span>
          <span class="nav-text">Community</span>
        </router-link>
        
        <router-link v-if="isLogin" to="/mypage" class="nav-link">
          <span class="nav-icon">👤</span>
          <span class="nav-text">My Page</span>
        </router-link>

        <a v-if="isLogin" @click="handleRecommendClick" class="nav-link">
          <span class="nav-icon">🎯</span>
          <span class="nav-text">For You</span>
        </a>
      </div>

      <!-- Bottom Section -->
      <div class="nav-bottom">
        <template v-if="!isLogin">
          <router-link to="/signup" class="nav-link">
            <span class="nav-icon">✨</span>
            <span class="nav-text">Sign Up</span>
          </router-link>
          <router-link to="/login" class="nav-link">
            <span class="nav-icon">🔑</span>
            <span class="nav-text">Sign In</span>
          </router-link>
        </template>
        <template v-else>
          <a @click="handleLogout" class="nav-link logout-btn">
            <span class="nav-icon">🚪</span>
            <span class="nav-text">Sign Out</span>
          </a>
        </template>
        <!-- Dark mode toggle could be added here -->
      </div>
    </div>
  </nav>

  <!-- Trigger area for mouse detection -->
  <div 
    class="sidebar-trigger"
    :class="{ 'trigger-hidden': isVisible || isAtTop }"
    @mouseenter="handleMouseEnter"
  ></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { storeToRefs } from "pinia";
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";
import axios from "axios";

const router = useRouter();
const authStore = useAuthStore();
const { isLogin } = storeToRefs(authStore);

// Navbar 숨김/표시 관련 상태
const isAtTop = ref(true);
const isHidden = ref(false);
const isVisible = ref(true);
const lastScrollY = ref(0);
let timeout = null;
const searchQuery = ref("");
const isFixed = ref(false);

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

// 스크롤 이벤트 핸들러
const handleScroll = () => {
  const currentScrollY = window.scrollY;
  isAtTop.value = currentScrollY === 0;

  // 최상단일 때
  if (isAtTop.value) {
    isHidden.value = false;
    isVisible.value = true;
    if (timeout) {
      clearTimeout(timeout);
      timeout = null;
    }
    return;
  }

  // 스크롤 방향 확인
  if (currentScrollY > lastScrollY.value) {
    if (!isHidden.value && currentScrollY > 70) {
      // navbar 높이보다 더 스크롤했을 때
      isVisible.value = false;
      setTimeout(() => {
        isHidden.value = true;
      }, 300);
    }
  } else {
    isHidden.value = false;
    isVisible.value = true;
  }

  lastScrollY.value = currentScrollY;

  // 스크롤 멈춤 감지 (최상단이 아닐 때만)
  if (timeout) clearTimeout(timeout);
  if (!isAtTop.value) {
    timeout = setTimeout(() => {
      if (!isHidden.value) {
        isVisible.value = false;
        setTimeout(() => {
          isHidden.value = true;
        }, 300);
      }
    }, 2000);
  }
};

// 마우스 이벤트 핸들러
const handleMouseMove = (e) => {
  if (e.clientY < 100) {
    // 상단 100px 영역에 마우스가 있을 때
    isHidden.value = false;
    isVisible.value = true;
  }
};

// 컴포넌트 마운트/언마운트 시 이벤트 리스너 관리
onMounted(() => {
  window.addEventListener("scroll", handleScroll);
  document.addEventListener("mousemove", handleMouseMove);
});

onUnmounted(() => {
  window.removeEventListener("scroll", handleScroll);
  document.removeEventListener("mousemove", handleMouseMove);
});

const handleLogout = async () => {
  try {
    await authStore.logout();
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
</script>

<style scoped>
.navbar {
  height: var(--navbar-height);
  display: flex;
  align-items: center;
  padding: 1rem 3rem;
  background-color: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(5px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  will-change: transform, position;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  justify-content: flex-start; /* 추가 */
  flex-wrap: nowrap; /* 추가: 줄바꿈 방지 */
}

.navbar-floating {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  background-color: rgba(255, 255, 255, 0.95);
}

.navbar-fixed {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background-color: rgba(255, 255, 255, 0.98);
  & + .main-content {
    /* navbar가 fixed일 때 main-content에 마진 추가 */
    margin-top: var(--navbar-height);
  }
}

.navbar-hidden {
  transform: translateY(-100%);
}

.navbar-visible {
  transform: translateY(0);
}
.nav-logo {
  font-size: 1.5rem;
  font-weight: 600;
  color: #3498db;
  text-decoration: none;
  margin-right: 2rem;
}

.nav-link {
  color: #2c3e50;
  text-decoration: none;
  padding: 0.5rem 1rem;
  font-weight: 500;
  transition: all 0.3s ease;
  cursor: pointer;
  white-space: nowrap; /* 추가: 텍스트 줄바꿈 방지 */
}

.nav-link:hover {
  color: #3498db;
}

.logout-btn {
  color: #e74c3c;
}

.logout-btn:hover {
  color: #c0392b;
}
.search-container {
  display: flex;
  align-items: center;
  margin-left: auto; /* 변경: 오른쪽 정렬을 위해 */
  min-width: 200px; /* 최소 너비 설정 */
}

.search-input {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 20px;
  margin-right: 0.5rem;
  width: 100%; /* 변경 */
  max-width: 200px; /* 추가: 최대 너비 제한 */
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.search-input:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 5px rgba(52, 152, 219, 0.3);
}

.search-button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
  padding: 0.5rem;
  transition: transform 0.2s ease;
}

.search-button:hover {
  transform: scale(1.1);
}

/* 반응형 수정 */
@media (max-width: 768px) {
  .navbar {
    padding: 1rem;
  }

  .search-container {
    min-width: 150px; /* 모바일에서 최소 너비 축소 */
    order: 0; /* 기존 order 제거 */
  }

  .search-input {
    max-width: 150px; /* 모바일에서 최대 너비 축소 */
  }

  .nav-link {
    padding: 0.5rem 0.5rem; /* 패딩 축소 */
    font-size: 0.85rem; /* 폰트 크기 축소 */
  }
  .nav-logo {
    font-size: 1.2rem; /* 로고 크기 축소 */
    margin-right: 1rem; /* 여백 축소 */
  }
}

@media (max-width: 640px) {
  .navbar {
    padding: 1rem 0.5rem; /* 패딩 더 축소 */
  }

  .nav-link {
    padding: 0.5rem 0.3rem; /* 패딩 더 축소 */
    font-size: 0.8rem; /* 폰트 크기 더 축소 */
  }
}
</style>
