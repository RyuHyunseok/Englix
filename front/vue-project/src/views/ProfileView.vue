<template>
    <div class="page-container">

  <div class="mypage-container" v-if="profileData">
    <!-- 프로필 카드 섹션 -->
    <section class="profile-card">
      <div class="profile-header">
        <div class="profile-main">
          <div class="profile-avatar">
            <img
              v-if="profileData.profile_user.tier_image_path"
              :src="`http://127.0.0.1:8000/static/${profileData.profile_user.tier_image_path}`"
              :alt="profileData.profile_user.tier"
              class="tier-avatar"
            />
            <span v-else class="avatar-text">{{ profileData.profile_user.nickname?.charAt(0) }} 여기</span>
          </div>
          <div class="profile-info">
            <h2 class="profile-name">{{ profileData.profile_user.nickname }}</h2>
            <div class="profile-stats">
              <div class="stat-item">
                <span class="stat-value">{{ profileData.followers_count }}</span>
                <span class="stat-label">팔로워</span>
              </div>
              <div class="stat-divider"></div>
              <div class="stat-item">
                <span class="stat-value">{{ profileData.following_count }}</span>
                <span class="stat-label">팔로잉</span>
              </div>
              <!-- 팔로우 버튼 -->
              <button 
                v-if="!profileData.is_self" 
                @click="handleFollow" 
                class="follow-button"
                :class="{ 'following': profileData.is_following }"
              >
                {{ profileData.is_following ? "언팔로우" : "팔로우" }}
              </button>
            </div>
          </div>
        </div>

        <!-- 자기소개 섹션 -->
        <div class="bio-section">
          <p v-if="profileData.profile_user.bio" class="bio-text">
            {{ profileData.profile_user.bio }}
          </p>
          <p v-else class="bio-text empty">아직 작성된 자기소개가 없습니다.</p>
        </div>

        
      </div>
    </section>

    <!-- 탭 네비게이션 -->
    <nav class="profile-tabs">
      <button 
        v-for="tab in tabs" 
        :key="tab.value" 
        @click="currentTab = tab.value"
        class="tab-button"
        :class="{ active: currentTab === tab.value }"
      >
        {{ tab.icon }} {{ tab.label }}
      </button>
    </nav>

    <!-- 컨텐츠 섹션 -->
    <div class="tab-content-container">
      <transition name="fade" mode="out-in">
        <section :key="currentTab">
          <!-- 내가 쓴 글 탭 -->
          <div v-if="currentTab === 'posts'" class="content-section">
    <h3 class="content-title">작성한 글 ({{ profileData.posts.length }})</h3>
    <div v-if="profileData.posts.length > 0" class="content-list">
      <router-link 
        v-for="post in profileData.posts" 
        :key="post.id" 
        :to="{ name: 'postDetail', params: { id: post.id }}" 
      >
        <div class="post-item">
          <h4 class="post-title">{{ post.title }}</h4>
          <div class="post-meta">
            <div class="meta-left">
              <span class="post-date">
                🕒 {{ post.created_at }}
              </span>
            </div>
            <div class="meta-right">
              <span class="like-count">
                ❤️ {{ post.likes_count }}
              </span>
              <span class="comments-count">💬 {{ post.comments_count }}</span>
            </div>
          </div>
        </div>
      </router-link>
    </div>
    <p v-else class="empty-message">작성한 게시글이 없습니다.</p>
  </div>

          <!-- 내가 쓴 댓글 탭 -->
          <div v-if="currentTab === 'comments'" class="content-section">
            <h3 class="content-title">작성한 댓글 ({{ profileData.comments.length }})</h3>
    <div v-if="profileData.comments.length > 0" class="content-list">
      <div v-for="comment in profileData.comments" :key="comment.id" class="post-item">
        <div class="post-main">
          <p class="post-content">{{ comment.content }}</p>
          <div class="post-meta">
            <div class="meta-left">
              <span class="post-date">
                🕒 {{ comment.created_at }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
    <p v-else class="empty-message">작성한 댓글이 없습니다.</p>
          </div>

          <!-- 좋아요한 글 -->
          <div v-if="currentTab === 'likes'" class="content-section">
  <h3 class="content-title">좋아요한 글 ({{ likedPosts.length }})</h3>
  <div v-if="likedPosts.length > 0" class="content-list">
    <router-link 
      v-for="post in likedPosts" 
      :key="post.id" 
      :to="{ name: 'postDetail', params: { id: post.id }}" 
    >
      <div class="post-item">
        <h4 class="post-title">{{ post.title }}</h4>
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
            <span class="like-count">
              ❤️ {{ post.likes_count }}
            </span>
            <span class="comments-count">💬 {{ post.comments_count }}</span>
          </div>
        </div>
      </div>
    </router-link>
  </div>
  <p v-else class="empty-message">좋아요한 글이 없습니다.</p>
</div>

          <!-- 찜한 영화 탭 -->
          <div v-if="currentTab === 'favorites'" class="content-section">
            <h3 class="content-title">찜한 영화</h3>
            <FavoriteMovies :username="username" />
          </div>

          <!-- 단어장 탭 -->
          <div v-if="currentTab === 'myword'" class="content-section">
            <h3 class="content-title">단어장</h3>
            <Myword :username="username" />
          </div>
        </section>
      </transition>
    </div>
  </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";
import FavoriteMovies from "./FavoriteMovies.vue";
import Myword from "./Myword.vue";

const route = useRoute();
const profileData = ref(null);
const currentTab = ref("posts"); // 기본 탭을 'posts'로 설정
const likedPosts = ref([]);

// URL 파라미터에서 username을 가져오는 computed 속성 추가
const username = computed(() => route.params.username);

const tabs = [
  { label: "작성한 글", value: "posts", icon: "🖊️" },
  { label: "작성한 댓글", value: "comments", icon: "💬" },
  { label: "좋아요한 글", value: "likes", icon: "❤️" },
  { label: "찜한 영화", value: "favorites", icon: "⭐" },
  { label: "단어장", value: "myword", icon: "📖" },
];

const fetchLikedPosts = async () => {
  try {
    const auth = localStorage.getItem("auth");
    if (!auth) return;

    const { token } = JSON.parse(auth);

    const response = await axios({
      method: "get",
      url: "http://127.0.0.1:8000/community/liked-posts/",
      headers: {
        Authorization: `Token ${token}`,
      },
    });

    likedPosts.value = response.data;
  } catch (error) {
    console.error("좋아요한 글 로딩 실패:", error);
  }
};

const fetchProfileData = async () => {
  try {
    if (!username.value) return;

    const token = JSON.parse(localStorage.getItem("auth")).token;

    const response = await axios({
      method: "get",
      url: `http://127.0.0.1:8000/community/profile/${username.value}/`,
      headers: {
        Authorization: `Token ${token}`,
      },
    });

    profileData.value = response.data;
  } catch (error) {
    console.error("프로필 데이터 로딩 실패:", error);
    alert("프로필 정보를 불러오는데 실패했습니다.");
  }
};

const handleFollow = async () => {
  try {
    if (!username.value) return;

    const token = JSON.parse(localStorage.getItem("auth")).token;

    await axios({
      method: "post",
      url: `http://127.0.0.1:8000/community/profile/${username.value}/follow/`,
      headers: {
        Authorization: `Token ${token}`,
      },
    });

    await fetchProfileData();
  } catch (error) {
    console.error("팔로우 처리 실패:", error);
    alert("팔로우 처리에 실패했습니다.");
  }
};

onMounted(() => {
  if (username.value) {
    fetchProfileData();
    fetchLikedPosts();
  }
});
</script>

<style lang="scss" scoped>
.mypage-container {
  min-height: 100vh;
  padding: 2rem;
}

.profile-card {
  background: white;
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
  margin-bottom: 2rem;
}

.profile-main {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.profile-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: var(--primary-color);
  display: flex;
  align-items: center;
  justify-content: center;
}

.tier-avatar {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-text {
  font-size: 2rem;
  color: white;
  text-transform: uppercase;
}

.profile-info {
  flex: 1;

  .profile-name {
    font-size: 2rem;
    color: #495057;
    margin-bottom: 1rem;
  }
}

.profile-stats {
  display: flex;
  gap: 2rem;
  align-items: center;

  .stat-item {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .stat-value {
    font-size: 1.5rem;
    font-weight: bold;
    color: #ff6b6b;
  }

  .stat-label {
    color: #868e96;
  }

  .stat-divider {
    height: 30px;
    width: 1px;
    background: #e9ecef;
  }
}

.bio-section {
  margin-top: 2rem;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 15px;
}

.bio-text,
.bio-placeholder {
  font-size: 1.1rem;
  line-height: 1.6;
  color: #495057;
  margin-bottom: 1rem;
}

.bio-placeholder {
  color: #adb5bd;
  font-style: italic;
}

.edit-button,
.save-button,
.cancel-button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;

  i {
    margin-right: 0.5rem;
  }
}

.edit-button {
  background: #e9ecef;
  color: #495057;

  &:hover {
    background: #dee2e6;
  }
}

.save-button {
  background: #ff6b6b;
  color: white;

  &:hover {
    background: #ff6b6b;
  }
}

.cancel-button {
  background: #868e96;
  color: white;
  margin-left: 0.5rem;

  &:hover {
    background: #495057;
  }
}

.bio-input {
  width: 100%;
  padding: 1rem;
  border: 2px solid #e9ecef;
  border-radius: 10px;
  font-size: 1rem;
  resize: vertical;
  min-height: 100px;
  margin-bottom: 1rem;

  &:focus {
    outline: none;
    border-color: #ff6b6b;
  }
}

.profile-tabs {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  align-content: center;
  justify-content: center;
}

.tab-button {
  padding: 1rem 1.5rem;
  border: none;
  border-radius: 15px;
  background: white;
  color: #495057;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);

  i {
    margin-right: 0.5rem;
  }

  &:hover {
    transform: translateY(-2px);
  }

  &.active {
    background: sandybrown;
    color: white;
  }
}

.tab-button.active {
  background: #ff6b6b;
  color: white;
}

/* 리스트 아이템 */
.list-item {
  background: var(--surface-color);
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 15px;
  transition: transform 0.2s ease;
  text-decoration: none;
  color: var(--text-color);
  text-decoration: none; /* 링크 밑줄 제거 */
  color: inherit;
}

.list-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
a {
  text-decoration: none;
  color: inherit;
}
router-link {
  text-decoration: none;
  color: inherit;
}
.item-content {
  margin-bottom: 12px;
}

.item-title {
  font-size: 1.2rem;
  margin-bottom: 8px;
}

.item-meta {
  display: flex;
  gap: var(--spacing-md);
  font-size: 0.9rem;
  color: var(--text-color-light);
}

.like-badge {
  display: flex;
  align-items: center;
  gap: 4px;
}

.empty-message {
  text-align: center;
  padding: var(--spacing-xl);
  color: var(--text-color-light);
  font-style: italic;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .mypage-container {
    padding: 1rem;
  }

  .profile-main {
    flex-direction: column;
    text-align: center;
  }

  .profile-stats {
    justify-content: center;
  }

  .profile-tabs {
    justify-content: center;
  }

  .tab-button {
    width: 100%;
  }
}


/* 반응형 디자인 */
@media (max-width: 768px) {
  .mypage-container {
    padding: 10px;
  }

  .profile-header {
    padding: 20px;
  }

  .profile-tabs {
    padding: 0 10px;
  }

  .profile-content {
    padding: 15px;
  }
}

/* 기존 스타일 유지하되 max-width 제한 추가 */
.items-list,
.content-section,
.account-management-section {
  max-width: 100%;
  overflow-x: hidden;
}

/* 스크롤바가 필요한 경우에만 표시 */
.items-list {
  overflow-y: auto;
  max-height: 600px; /* 필요한 경우 조정 */
}

/* MovieView와 일관된 카드 스타일 */
.post-item,
.comment-item {
  background: white;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s ease;
}

.post-item:hover,
.comment-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.list-item {
  background: var(--surface-color);
  border-radius: var(--border-radius-md);
  padding: var(--spacing-md);
  margin-bottom: var(--spacing-sm);
  transition: transform 0.3s ease;
  text-decoration: none;
  color: var(--text-color);
  display: block;
}

.list-item:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.follow-button {
  margin-top: 20px;
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 20px;
  background-color: #c96969;
  color: white;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.follow-button.following {
  background-color: #e0e0e0;
  color: #666;
}

.follow-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.list-item {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  transition: all 0.3s ease;
  cursor: pointer;
  text-decoration: none;
  color: inherit;
}

.list-item:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.empty-message {
  text-align: center;
  padding: 3rem;
  color: #666;
  background: #f8f9fa;
  border-radius: 12px;
  margin-top: 1rem;
}
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* MyPageView.vue와 ProfileView.vue 둘 다 적용 */
.mypage-container {
  animation: fadeInUp 0.6s ease-out;
}

/* 각 섹션별로도 적용 가능 */
.profile-card,
.profile-content,
.content-section {
  animation: fadeInUp 0.6s ease-out;
}

/* 딜레이를 주고 싶다면 */
.profile-card {
  animation: fadeInUp 0.6s ease-out 0.2s;
  animation-fill-mode: both;
}

.profile-content {
  animation: fadeInUp 0.6s ease-out 0.4s;
  animation-fill-mode: both;
}
.content-section {
  background: white;
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  margin-bottom: 2rem;
}

.content-title {
  font-size: 1.8rem;
  color: #495057;
  padding-left: 1rem;
  border-left: 4px solid #ff6b6b;
}

.post-item {
  background: white;
  border-radius: 16px;
  padding: 1.5rem;
  margin-bottom: 1rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  border: 1px solid #f1f3f5;
  text-decoration: none;
  color: inherit;

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
  font-weight: 600;
  margin: 0;
}

.post-content {
  color: #868e96;
  font-size: 0.95rem;
  line-height: 1.5;
  margin: 0;
}

.post-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1.2rem;
  border-top: 1px solid #f1f3f5;
  font-size: 0.9rem;
}

.meta-left, .meta-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.post-author, .post-date, .like-count {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  color: #adb5bd;
}

.post-author {
  color: #ff6b6b;
  font-weight: 500;
}

.empty-message {
  text-align: center;
  padding: 2rem;
  color: #868e96;
  background: #f8f9fa;
  border-radius: 12px;
}

@media (max-width: 768px) {
  .content-section {
    padding: 1rem;
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
</style>