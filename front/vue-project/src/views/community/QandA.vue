<template>
  <div class="board-container">
    <div class="board-header">
      <h2 class="board-title">질문 게시판</h2>
      <RouterLink 
        :to="{ name: 'postCreate', query: { category: 'QandA' }}"
        class="create-button"
      >
        ✏️ 새 글 쓰기
      </RouterLink>
    </div>

    <div class="posts-list">
      <div v-for="post in posts" :key="post.id" class="post-item">
        <div class="post-main">
          <router-link 
            :to="{ name: 'postDetail', params: { id: post.id }}"
            class="post-title"
          >
            {{ post.title }}
          </router-link>          
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
              <span class="likes-count">
                ❤️ {{ post.likes_count }}
              </span>
              <span class="comments-count">
                💬 {{ post.comments_count }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { usePostStore } from '@/stores/posts';
import CommunityNavbar from "@/components/CommunityNavbar.vue";
import axios from 'axios';

const posts = ref([]);

const fetchPosts = async () => {
  try {
    const auth = localStorage.getItem('auth');
    const token = auth ? JSON.parse(auth).token : null;

    const response = await axios.get('http://127.0.0.1:8000/community/posts/', {
      headers: { Authorization: `Token ${token}` },
      params: { category: 'QandA' }
    });
    
    posts.value = response.data;
  } catch (error) {
    console.error('Error fetching posts:', error);
  }
};

onMounted(() => {
  fetchPosts();
});
</script>

<style lang="scss" scoped>
.board-container {
  padding: 1rem;
}

.board-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
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

.create-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.8rem 1.5rem;
  background-color: #ff6b6b;
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(255, 107, 107, 0.2);

  &:hover {
    transform: translateY(-2px);
    background-color: #fa5252;
  }

  i {
    font-size: 0.9rem;
  }
}
/* 아이콘 스타일 수정 */
.nav-item, .search-button {
  /* i 태그 관련 스타일 제거하고 이모지 크기 조정 */
  font-size: 1rem; /* 이모지 크기 조정 */
}

/* 이전에 있던 i 태그 관련 스타일은 제거해도 됩니다 */
.posts-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.post-item {
  background: white;
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  border: 1px solid #f1f3f5;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
    border-color: #ff6b6b;
  }
}

.post-main {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.post-title {
  font-size: 1.2rem;
  color: #495057;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s ease;

  &:hover {
    color: #ff6b6b;
  }
}

.post-content {
  color: #868e96;
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
  margin-top: 0.5rem;
  padding-top: 0.8rem;
  border-top: 1px solid #f1f3f5;
  font-size: 0.9rem;
}

.meta-left, .meta-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.post-author, .post-date, .likes-count, .comments-count {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  color: #adb5bd;

  i {
    font-size: 0.9rem;
  }
}

.post-author {
  color: #ff6b6b;
  font-weight: 500;
}

.likes-count {
  i {
    color: #ff6b6b;
  }
}

.comments-count {
  i {
    color: #74c0fc;
  }
}

// 반응형
@media (max-width: 768px) {
  .board-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
    text-align: center;
  }

  .board-title {
    padding-left: 0;
    
    &::before {
      display: none;
    }
  }

  .create-button {
    justify-content: center;
  }

  .post-meta {
    flex-direction: column;
    gap: 0.8rem;
    
    .meta-left, .meta-right {
      width: 100%;
      justify-content: center;
    }
  }
}

// 애니메이션
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

.post-item {
  animation: slideIn 0.3s ease-out forwards;
  
  @for $i from 1 through 10 {
    &:nth-child(#{$i}) {
      animation-delay: #{$i * 0.05}s;
    }
  }
}
</style>