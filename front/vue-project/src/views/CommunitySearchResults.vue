<template>
    <div class="page-container">

      <div class="search-container">
    <h2 class="search-title">"{{ searchQuery }}" 검색 결과 ✨</h2>
   
    <div v-if="searchResults && searchResults.length > 0" class="posts-list">
      <div v-for="post in searchResults" :key="post.id" class="post-item">
        <div class="post-main">
          <router-link 
            :to="{ name: 'postDetail', params: { id: post.id }}"
            class="post-title"
          >
            {{ post.title }}
          </router-link>
          <p class="post-content">{{ post.content }}</p>
          <div class="post-meta">
            <div class="meta-left">
              <span class="post-author">
                👤 {{ post.user.nickname }}
              </span>
              <span class="post-date">
                🕒 {{ post.created_at }}
              </span>
            </div>
            <div class="meta-right">
              <span class="like-badge">
                ❤️ {{ post.likes_count }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
   
    <div v-else class="no-results">
      <div class="no-results-icon">😔</div>
      <h3>검색 결과가 없습니다</h3>
      <p>다른 검색어로 다시 시도해보세요</p>
    </div>
  </div>
    </div>
   </template>
   
   <script setup>
   import { ref, onMounted, watch } from 'vue';
   import { useRoute } from 'vue-router';
   
   const route = useRoute();
   const searchQuery = ref('');
   const searchResults = ref([]);
   
   const updateSearchResults = () => {
    searchQuery.value = route.query.q;
    try {
      if (route.query.results) {
        const data = JSON.parse(route.query.results);
        searchResults.value = data.results || [];
      }
    } catch (error) {
      console.error('Search results parsing error:', error);
      searchResults.value = [];
    }
   };
   
   onMounted(updateSearchResults);
   watch(() => route.query, updateSearchResults, { deep: true });
   </script>
   
   <style scoped>
   .search-container {
  max-width: 1200px;
  padding: 0 50px;
}

.search-title {
  font-size: 1.8rem;
  color: #2c3e50;
  margin-bottom: 30px;
  padding-bottom: 15px;
  border-bottom: 2px solid #eee;
  text-align: center;
}

.posts-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.post-item {
  background: white;
  border: 1px solid #eee;
  border-radius: 16px;
  padding: 20px;
  transition: transform 0.2s, box-shadow 0.2s;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.post-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
  border-color: #ff6b6b;
}

.post-main {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.post-title {
  font-size: 1.2rem;
  color: #2c3e50;
  text-decoration: none;
  font-weight: 600;
  display: block;
  margin-bottom: 8px;
  transition: color 0.3s ease;
}

.post-title:hover {
  color: #ff6b6b;
}

.post-content {
  color: #666;
  font-size: 0.95rem;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.post-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
  border-top: 1px solid #eee;
  font-size: 0.9rem;
  color: #888;
}

.meta-left {
  display: flex;
  gap: 15px;
}

.post-author {
  color: #ff6b6b;
  font-weight: 500;
}

.like-badge {
  display: flex;
  align-items: center;
  gap: 5px;
}

.no-results {
  text-align: center;
  padding: 50px;
  background: white;
  border-radius: 16px;
  margin-top: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.no-results-icon {
  font-size: 3rem;
  margin-bottom: 20px;
}

.no-results h3 {
  color: #ff6b6b;
  margin-bottom: 10px;
  font-size: 1.5rem;
}

.no-results p {
  color: #666;
}

@media (max-width: 768px) {
  .search-container {
    padding: 0 20px;
  }

  .search-title {
    font-size: 1.5rem;
  }

  .post-item {
    padding: 15px;
  }
}

/* 애니메이션 */
.post-item {
  animation: slideIn 0.3s ease-out forwards;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

   </style>