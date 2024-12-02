<template>
    <div class="board-container">
      <div class="board-header">
        <h2 class="board-title">Ranking</h2>
      </div>
  

    <!-- 컬럼 헤더 -->
    <div class="ranking-header">
      <div class="rank-column">등수</div>
      <div class="nickname-column">닉네임</div>
      <div class="points-column">포인트</div>
      <div class="tier-column">티어</div>
    </div>

    <div class="ranking-list" v-if="!loading">
      <div v-for="(user, index) in paginatedUsers" 
           :key="user.id" 
           class="ranking-item"
           :class="{'top-rank': calculateRank(index) <= 3}">
        <div class="rank-column">
          <span class="rank-number" :class="'rank-' + calculateRank(index)">
            {{ calculateRank(index) }}
          </span>
        </div>
        <div class="nickname-column">{{ user.nickname }}</div>
        <div class="points-column">{{ user.points.toLocaleString() }} pts</div>
        <div class="tier-column">
          <div v-if="user.tier" class="tier-badge" :class="user.tier.toLowerCase()">
            {{ user.tier }}
          </div>
        </div>
      </div>
    </div>
  
      <div v-if="!loading && users.length > 0" class="pagination">
        <button 
          :disabled="currentPage === 1"
          @click="currentPage--"
          class="page-button"
        >
          Previous
        </button>
        <span class="page-info">Page {{ currentPage }} of {{ totalPages }}</span>
        <button 
          :disabled="currentPage === totalPages"
          @click="currentPage++"
          class="page-button"
        >
          Next
        </button>
      </div>
    </div>
  </template>
  
  <script setup>
  import CommunityNavbar from '@/components/CommunityNavbar.vue';
  import { ref, computed, onMounted } from 'vue';
  import axios from 'axios';
import { useAuthStore } from '@/stores/auth';
  
  const authStore = useAuthStore();
  const users = ref([]);
  const currentPage = ref(1);
  const itemsPerPage = 20;
  const loading = ref(true);
  
  onMounted(async () => {
    try {
      const response = await axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/accounts/users/all/',
        headers: {
          Authorization: `Token ${authStore.token}`
        }
      });
  
      if (Array.isArray(response.data)) {
        users.value = response.data
          .filter(user => user.points !== undefined)
          .sort((a, b) => b.points - a.points);
      }
    } catch (error) {
      console.error('Error details:', error.response || error);
      users.value = [];
    } finally {
      loading.value = false;
    }
  });
  
  const paginatedUsers = computed(() => {
    const start = (currentPage.value - 1) * itemsPerPage;
    const end = start + itemsPerPage;
    return users.value.slice(start, end);
  });
  
  const totalPages = computed(() => {
    return Math.ceil(users.value.length / itemsPerPage);
  });
  
  const calculateRank = (index) => {
    return (currentPage.value - 1) * itemsPerPage + index + 1;
  };
  </script>
  
  <style scoped>
  /* 기본 컨테이너 스타일 */
  .board-container {
    padding: 20px;
    max-width: 1200px;
    margin: 0 auto;
  }
  
  .board-header {
    margin-bottom: 30px;
  }
  
  .board-title {
  font-size: 1.8rem;
  color: #495057;
  font-weight: 600;
  position: relative;
  padding-left: 1rem;

  &::before {
    content: '';
    position: absolute;
    left: 0;
    top: 50%;
    transform: translateY(-50%);
    width: 4px;
    height: 24px;
    background: #ff6b6b;
    border-radius: 2px;
  }
}
  
  /* 컬럼 공통 스타일 */
  .rank-column,
  .nickname-column,
  .points-column,
  .tier-column {
    padding: 0 15px;
    display: flex;
    align-items: center;
  }
  
  .rank-column {
  width: 100px;  /* 80px에서 100px로 증가 */
  justify-content: center;  /* 가운데 정렬 추가 */
}
  
  .nickname-column {
    flex: 1;
    min-width: 150px;
  }
  
  .points-column {
    width: 150px;
    justify-content: center;
  }
  
  .tier-column {
    width: 120px;
    justify-content: center;
  }
  
  /* 헤더 스타일 */
  .ranking-header {
    display: flex;
    background: #f8f9fa;
    padding: 15px 0;
    border-radius: 12px 12px 0 0;
    font-weight: 600;
    color: #666;
    border: 1px solid #eee;
    border-bottom: none;
  }
  
  /* 랭킹 아이템 스타일 */
  .ranking-list {
    display: flex;
    flex-direction: column;
  }
  
  .ranking-item {
    display: flex;
    background: white;
    border: 1px solid #eee;
    border-top: none;
    padding: 15px 0;
    transition: all 0.2s ease;
  }
  
  .ranking-item:last-child {
    border-radius: 0 0 12px 12px;
  }
  
  .ranking-item:hover {
    background-color: #f8f9fa;
  }
  
  /* 상위 랭커 스타일 */
  .top-rank {
    background-color: #fff9e6;
  }
  
  .rank-1 { color: #FFD700; font-size: 1.3rem; }
  .rank-2 { color: #C0C0C0; font-size: 1.2rem; }
  .rank-3 { color: #CD7F32; font-size: 1.1rem; }
  
  .crown {
    position: absolute;
    top: -15px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 1.2rem;
    animation: float 2s ease-in-out infinite;
  }
  
  @keyframes float {
    0%, 100% { transform: translateY(0) translateX(-50%); }
    50% { transform: translateY(-5px) translateX(-50%); }
  }
  
  /* 티어 배지 스타일 */
  .tier-badge {
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 0.9rem;
    font-weight: 500;
    text-align: center;
  }
  
  .bronze { background-color: #cd7f32; color: white; }
  .silver { background-color: #c0c0c0; color: white; }
  .gold { background-color: #ffd700; color: black; }
  .platinum { background-color: #e5e4e2; color: black; }
  .diamond { background-color: #b9f2ff; color: black; }
  .ruby { background-color: #e0115f; color: white; }
  
  /* 페이지네이션 스타일 유지 */
  .pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-top: 30px;
}

.page-button {
  background-color: #4CAF50;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.3s;
}

.page-button:hover:not(:disabled) {
  background-color: #45a049;
}

.page-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.page-info {
  color: #666;
  font-size: 0.9rem;
}
  </style>