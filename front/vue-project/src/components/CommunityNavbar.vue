<template>
  <div class="community-navbar">
    <div class="nav-links">
      <router-link to="/community" class="nav-logo">자유 게시판</router-link>
      <router-link to="/resource" class="nav-logo">자료 공유 게시판</router-link>
      <router-link to="/Q&A" class="nav-logo">질문 게시판</router-link>
      <router-link to="/ranking" class="nav-logo">명예의 전당</router-link>
    </div>
    <div class="search-container">
      <input 
        v-model="searchQuery" 
        @keyup.enter="handleSearch"
        placeholder="검색어를 입력하세요..."
        class="search-input"
      >
      <button @click="handleSearch" class="search-button">
        🔍
      </button>
    </div>
  </div>
 </template>
 
 <script setup>
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
.community-navbar {
 display: flex;
 justify-content: space-between;
 align-items: center;
 padding: 1rem;
 width: 100%;
}

.nav-links {
 display: flex;
 gap: 1rem;
 height: 40px; // 고정 높이 설정
}

.nav-logo {
 padding: 0.5rem 1rem;
 color: var(--text-color);
 text-decoration: none;
 font-size: 0.95rem;
 font-weight: 600;
 border-radius: 8px;
 background-color: var(--surface-color);
 box-shadow: var(--card-shadow);
 transition: all 0.3s ease;
 display: flex;
 align-items: center; // 수직 중앙 정렬
 justify-content: center; // 수평 중앙 정렬
 height: 80%; // 부모 높이를 상속
 white-space: nowrap; // 텍스트 줄바꿈 방지

 &:hover {
   background-color: var(--primary-color);
   color: white;
   transform: translateY(-2px);
   box-shadow: var(--card-shadow-hover);
 }

 &.router-link-active {
   background-color: var(--primary-color);
   color: white;
 }
}

.search-container {
 display: flex;
 align-items: center;
 gap: 0.5rem;
 height: 40px; // nav-links와 동일한 높이
}

.search-input {
 padding: 0.5rem 1rem;
 border: 1px solid var(--border-color);
 border-radius: 8px;
 width: 200px;
 font-size: 0.9rem;
 transition: all 0.3s ease;
 height: 100%; // 컨테이너 높이와 동일하게

 &:focus {
   outline: none;
   border-color: var(--primary-color);
   box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.1);
 }
}

.search-button {
 background: none;
 border: none;
 font-size: 1.2rem;
 cursor: pointer;
 padding: 0.5rem;
 transition: transform 0.2s ease;
 height: 100%; // 컨테이너 높이와 동일하게
 display: flex;
 align-items: center;

 &:hover {
   transform: scale(1.1);
   color: var(--primary-color);
 }
}

// 다크모드 대응
:root[class~="dark"] {
 .nav-logo {
   background-color: var(--dark-surface);
   color: var(--dark-text);

   &:hover, &.router-link-active {
     background-color: var(--primary-color);
     color: white;
   }
 }

 .search-input {
   background-color: var(--dark-surface);
   color: var(--dark-text);
   border-color: var(--dark-border);

   &::placeholder {
     color: var(--dark-text-secondary);
   }
 }
}

// 반응형 디자인
@media (max-width: 768px) {
 .community-navbar {
   flex-direction: column;
   gap: 1rem;
   padding: 1rem;
 }

 .nav-links {
   width: 100%;
   justify-content: space-between;
   gap: 0.5rem;
 }

 .nav-logo {
   font-size: 0.85rem;
   padding: 0.5rem 0.75rem;
   flex: 1;
 }

 .search-container {
   width: 100%;
 }

 .search-input {
   flex: 1;
   width: auto;
 }
}
</style>