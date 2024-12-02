<!-- Myword.vue -->
<template>
    <div class="word-container">
      <div v-if="loading" class="loading">
        로딩 중...
      </div>
      <div v-else-if="error" class="error">
        {{ error }}
      </div>
      <div v-else>
        <div v-if="favoriteWords.length === 0" class="empty-state">
          저장된 단어가 없습니다.
        </div>
        <div v-else class="word-list">
          <div v-for="word in favoriteWords" :key="word.id" class="word-item">
            <div class="word-content">
              <h4>{{ word.word }}</h4>
              <p>{{ word.meaning }}</p>
            </div>
            <div class="word-category">{{ word.category }}</div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, watch } from 'vue';
  import axios from 'axios';
  
  const props = defineProps({
    username: {
      type: String,
      required: true
    }
  });
  
  const favoriteWords = ref([]);
  const loading = ref(false);
  const error = ref(null);
  
  const fetchFavoriteWords = async () => {
    if (!props.username) return;
    
    loading.value = true;
    error.value = null;
  
    try {
      const auth = localStorage.getItem('auth');
      if (!auth) throw new Error('인증 정보가 없습니다.');
      
      const { token } = JSON.parse(auth);
      
      const response = await axios({
        method: 'get',
        url: `http://127.0.0.1:8000/movie/favorite-words/${props.username}/`,
        headers: {
          'Authorization': `Token ${token}`
        }
      });
      
      favoriteWords.value = response.data;
    } catch (err) {
      console.error('단어장 로딩 실패:', err);
      error.value = '단어장을 불러오는데 실패했습니다.';
    } finally {
      loading.value = false;
    }
  };
  
  // username이 변경될 때마다 데이터 다시 불러오기
  watch(() => props.username, (newUsername) => {
    if (newUsername) {
      fetchFavoriteWords();
    }
  });
  
  onMounted(() => {
    if (props.username) {
      fetchFavoriteWords();
    }
  });
  </script>
  
  <style scoped>
  .word-container {
    padding: 20px;
  }
  
  .loading {
    text-align: center;
    padding: 20px;
    color: #666;
  }
  
  .error {
    color: #dc3545;
    padding: 20px;
    text-align: center;
  }
  
  .empty-state {
    text-align: center;
    padding: 2rem;
    color: #868e96;
    background: #f8f9fa;
    border-radius: 12px;
  }
    
  .word-list {
    display: grid;
    gap: 20px;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  }
  
  .word-item {
    background: white;
    border: 1px solid #eee;
    border-radius: 8px;
    padding: 15px;
    transition: transform 0.2s;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  
  .word-item:hover {
    transform: translateY(-2px);
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  }
  
  .word-content h4 {
    margin: 0 0 8px 0;
    color: #2c3e50;
  }
  
  .word-content p {
    margin: 0;
    color: #666;
    font-size: 0.9em;
  }
  
  .word-category {
    margin-top: 10px;
    font-size: 0.8em;
    color: #2196F3;
    text-align: right;
  }
  </style>