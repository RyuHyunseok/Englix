<template>
  <div class="page-container">
  <div class="community-container">
    <h1 class="community-title">Community</h1>

    <nav class="community-nav">
      <router-link to="/community" class="nav-item" :class="{ active: $route.path === '/community' }">💭 자유 게시판</router-link>
      <router-link to="/resource" class="nav-item" :class="{ active: $route.path === '/resource' }">📚 자료 공유 게시판</router-link>
      <router-link to="/Q&A" class="nav-item" :class="{ active: $route.path === '/Q&A' }">❓ 질문 게시판</router-link>
      <router-link to="/ranking" class="nav-item" :class="{ active: $route.path === '/ranking' }">🏆 명예의 전당</router-link>
    </nav>

    <!-- 검색창도 수정 -->
    <div class="search-section">
      <div class="search-container">
        <input v-model="searchQuery" @keyup.enter="handleSearch" placeholder="검색어를 입력하세요..." class="search-input" />
        <button @click="handleSearch" class="search-button">🔍</button>
      </div>
    </div>

    <!-- 게시판 컨텐츠 -->
    <div class="content-section">
      <LearningResources />
    </div>
  </div>
  </div>
</template>

<script setup>
import LearningResources from "./community/LearningResources.vue";
import { ref } from 'vue';
 import { RouterLink, useRouter } from "vue-router";
 import axios from 'axios';
 
 const router = useRouter();
 const searchQuery = ref('');
 
 const handleSearch = async () => {
  if (!searchQuery.value.trim()) return;
 
  try {
    const auth = localStorage.getItem('auth');
    if (!auth) return;
    
    const { token } = JSON.parse(auth);
    
    const response = await axios({
      method: 'get',
      url: 'http://127.0.0.1:8000/community/posts/search/',
      headers: { 'Authorization': `Token ${token}` },
      params: { query: searchQuery.value }
    });
 
    router.push({
      name: 'communitySearchResults',
      query: { 
        q: searchQuery.value,
        results: JSON.stringify(response.data)
      }
    });
 
    searchQuery.value = '';
  } catch (error) {
    console.error('검색 실패:', error);
  }
 };
</script>

<style lang="scss" scoped>
.community-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  min-height: 100vh;
}

.community-title {
  font-size: 2.5rem;
  font-weight: 700;
  text-align: center;
  color: #ff6b6b;
  margin-bottom: 2rem;
  position: relative;

  &::after {
    content: "";
    position: absolute;
    bottom: -10px;
    left: 50%;
    transform: translateX(-50%);
    width: 100px;
    height: 3px;
    background: linear-gradient(to right, #ff6b6b, #ffa8a8);
    border-radius: 2px;
  }
}

.community-nav {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  justify-content: center;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 1.5rem;
  background: white;
  border-radius: 15px;
  color: #495057;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);

  i {
    font-size: 1.1rem;
    color: #ff6b6b;
  }

  &:hover {
    transform: translateY(-2px);
    background: #fff5f5;
  }

  &.active {
    background: #ff6b6b;
    color: white;

    i {
      color: white;
    }
  }
}
/* 아이콘 스타일 수정 */
.nav-item,
.search-button {
  /* i 태그 관련 스타일 제거하고 이모지 크기 조정 */
  font-size: 1rem; /* 이모지 크기 조정 */
}

/* 이전에 있던 i 태그 관련 스타일은 제거해도 됩니다 */
.search-section {
  margin-bottom: 2rem;
  display: flex;
  justify-content: center;
}

.search-container {
  display: flex;
  align-items: center;
  max-width: 600px;
  width: 100%;
  background: white;
  border-radius: 20px;
  padding: 0.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.search-input {
  flex: 1;
  padding: 0.8rem 1.2rem;
  border: none;
  border-radius: 15px;
  font-size: 1rem;
  background: transparent;

  &:focus {
    outline: none;
  }

  &::placeholder {
    color: #adb5bd;
  }
}

.search-button {
  background: #ff6b6b;
  border: none;
  border-radius: 15px;
  padding: 0.8rem 1.2rem;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;

  &:hover {
    background: #fa5252;
    transform: translateY(-2px);
  }
}

.content-section {
  background: white;
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

@media (max-width: 768px) {
  .community-container {
    padding: 1rem;
  }

  .community-nav {
    flex-direction: column;
  }

  .nav-item {
    width: 100%;
    justify-content: center;
  }

  .search-container {
    margin: 0 1rem;
  }
}

// 애니메이션 효과
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.content-section {
  animation: fadeIn 0.5s ease-out;
}
</style>
