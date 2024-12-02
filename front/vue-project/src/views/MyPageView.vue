<template>
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
            <span v-else class="avatar-text">
              {{ profileData.profile_user.nickname?.charAt(0) }}
            </span>
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
            </div>
          </div>
        </div>

        <!-- 자기소개 섹션 -->
        <div class="bio-section">
          <div v-if="!isEditingBio" class="bio-display">
            <p v-if="profileData.profile_user.bio" class="bio-text">
              {{ profileData.profile_user.bio }}
            </p>
            <p v-else class="bio-placeholder">자기소개를 작성해보세요! ✏️</p>
            <button @click="startEditingBio" class="edit-button">
              <i class="fas fa-edit"></i>
              {{ profileData.profile_user.bio ? "수정하기" : "작성하기" }}
            </button>
          </div>
          <div v-else class="bio-edit">
            <textarea v-model="editBio" class="bio-input" placeholder="자기소개를 입력하세요 (최대 500자)" maxlength="500"></textarea>
            <div class="bio-actions">
              <button @click="saveBio" class="save-button">
                <i class="fas fa-check"></i>
                저장하기
              </button>
              <button @click="cancelEditBio" class="cancel-button">
                <i class="fas fa-times"></i>
                취소하기
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <nav class="profile-tabs">
      <button v-for="tab in tabs" :key="tab.value" @click="currentTab = tab.value" :class="['tab-button', { active: currentTab === tab.value }]">
        {{ tab.icon }}
        {{ tab.label }}
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
              <router-link v-for="post in profileData.posts" :key="post.id" :to="{ name: 'postDetail', params: { id: post.id } }">
                <div class="post-item">
                  <h4 class="post-title">{{ post.title }}</h4>
                  <div class="post-meta">
                    <div class="meta-left">
                      <span class="post-date">🕒 {{ post.created_at }}</span>
                    </div>
                    <div class="meta-right">
                      <span class="like-count">❤️ {{ post.likes_count }}</span>
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
                      <span class="post-date">🕒 {{ comment.created_at }}</span>
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
              <router-link v-for="post in likedPosts" :key="post.id" :to="{ name: 'postDetail', params: { id: post.id } }">
                <div class="post-item">
                  <h4 class="post-title">{{ post.title }}</h4>
                  <div class="post-meta">
                    <div class="meta-left">
                      <span class="post-author">👤 {{ post.user.nickname }}</span>
                      <span class="post-date">🕒 {{ post.created_at }}</span>
                    </div>
                    <div class="meta-right">
                      <span class="like-count">❤️ {{ post.likes_count }}</span>
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
            <FavoriteMovies v-if="currentUsername" :username="currentUsername" />
          </div>

          <!-- 단어장 탭 -->
          <div v-if="currentTab === 'myword'" class="content-section">
            <h3 class="content-title">단어장</h3>
            <Myword v-if="currentUsername" :username="currentUsername" />
          </div>

          <!-- 계정 관리 탭 -->
          <div v-if="currentTab === 'account'" class="tab-content">
            <h3 class="content-title">계정 관리</h3>
            <div class="warning-section">
              <h4 class="warning-title">회원 탈퇴</h4>
              <p class="warning-text">회원 탈퇴 시 모든 데이터가 삭제되며, 이 작업은 되돌릴 수 없습니다.</p>
              <button @click="showDeleteConfirmation" class="btn-danger">회원 탈퇴</button>
            </div>
          </div>

          <!-- 모달 -->
          <section v-if="showDeleteModal" class="modal-overlay">
            <div class="modal-card">
              <h4 class="modal-title">회원 탈퇴 확인</h4>
              <p class="modal-text">정말로 탈퇴하시겠습니까? 이 작업은 되돌릴 수 없습니다.</p>
              <div class="button-group">
                <button @click="deleteAccount" class="btn-danger">탈퇴하기</button>
                <button @click="showDeleteModal = false" class="btn-secondary">취소</button>
              </div>
            </div>
          </section>
        </section>
      </transition>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import axios from "axios";
import FavoriteMovies from "./FavoriteMovies.vue";
import Myword from "./Myword.vue";
import { useToastStore } from "@/stores/toast";

const toastStore = useToastStore();

const profileData = ref(null);
const likedPosts = ref([]);
const currentTab = ref("posts");

const router = useRouter();
const authStore = useAuthStore();
const showDeleteModal = ref(false);

const isEditingBio = ref(false);
const editBio = ref("");

// username을 computed로 관리
const currentUsername = computed(() => {
  const auth = localStorage.getItem("auth");
  if (!auth) return null;
  const { username } = JSON.parse(auth);
  return username;
});

const startEditingBio = () => {
  editBio.value = profileData.value.profile_user.bio || "";
  isEditingBio.value = true;
};

const saveBio = async () => {
  try {
    const auth = localStorage.getItem("auth");
    if (!auth) return;

    const { token } = JSON.parse(auth);

    const response = await axios({
      method: "put",
      url: "http://127.0.0.1:8000/accounts/preferences/",
      headers: {
        Authorization: `Token ${token}`,
      },
      data: {
        bio: editBio.value,
      },
    });

    // 프로필 데이터 업데이트
    profileData.value.profile_user.bio = editBio.value;
    isEditingBio.value = false;
  } catch (error) {
    console.error("자기소개 업데이트 실패:", error);
    alert("자기소개 업데이트에 실패했습니다.");
  }
};

const cancelEditBio = () => {
  isEditingBio.value = false;
  editBio.value = "";
};
const showDeleteConfirmation = () => {
  showDeleteModal.value = true;
};

const deleteAccount = async () => {
  try {
    const auth = localStorage.getItem("auth");
    if (!auth) return;

    const { token } = JSON.parse(auth);

    await axios({
      method: "delete",
      url: "http://127.0.0.1:8000/accounts/delete/",
      headers: {
        Authorization: `Token ${token}`,
      },
    });

    // 로그아웃 처리
    await authStore.logout();

    // 홈페이지로 리다이렉트
    router.push("/");
    toastStore.addToast("회원 탈퇴가 완료되었습니다.", "success");
    // alert("회원 탈퇴가 완료되었습니다.");
  } catch (error) {
    console.error("회원 탈퇴 실패:", error);
    toastStore.addToast("회원 탈퇴 처리 중 오류가 발생했습니다.", "success");
    // alert("회원 탈퇴 처리 중 오류가 발생했습니다.");
  }
};

const tabs = [
  { label: "내가 쓴 글", value: "posts", icon: "🖊️" },
  { label: "내가 쓴 댓글", value: "comments", icon: "💬" },
  { label: "좋아요한 글", value: "likes", icon: "❤️" },
  { label: "찜한 영화", value: "favorites", icon: "⭐" },
  { label: "단어장", value: "myword", icon: "📖" },
  { label: "계정 관리", value: "account", icon: "⚙️" },
];

const fetchProfileData = async () => {
  try {
    if (!currentUsername.value) {
      router.push("/login");
      return;
    }

    const auth = localStorage.getItem("auth");
    const { token } = JSON.parse(auth);

    const response = await axios({
      method: "get",
      url: `http://127.0.0.1:8000/community/profile/${currentUsername.value}/`,
      headers: {
        Authorization: `Token ${token}`,
      },
    });

    console.log("Profile response:", response.data);

    // tier에 따라 이미지 경로 설정
    if (response.data.profile_user.tier) {
      response.data.profile_user.tier_image_path = `tier_images/${response.data.profile_user.tier.toLowerCase()}.png`;
    }

    profileData.value = response.data;
  } catch (error) {
    console.error("프로필 데이터 로딩 실패:", error);
    if (error.response?.status === 401) {
      router.push("/login");
    }
  }
};

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

onMounted(async () => {
  if (currentUsername.value) {
    await fetchProfileData(); // 기존 프로필 데이터 가져오기
    await fetchLikedPosts(); // 좋아요 데이터 가져오기
  } else {
    router.push("/login");
  }
});
const getTabIcon = (tabValue) => {
  const iconMap = {
    posts: "fas fa-pen",
    comments: "fas fa-comments",
    likes: "fas fa-heart",
    favorites: "fas fa-star",
    myword: "fas fa-book",
    account: "fas fa-user-cog",
  };
  return iconMap[tabValue];
};
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
    color: sandybrown;
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
  background: sandybrown;
  color: white;

  &:hover {
    background: sandybrown;
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
    border-color: sandybrown;
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

.profile-content {
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 96%;
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

.mypage-container {
  animation: fadeInUp 0.6s ease-out;
}

/* 각 섹션별로도 적용 가능 */
.profile-card,
.profile-content,
.content-section {
  animation: fadeInUp 0.3s ease-out;
}

/* 딜레이를 주고 싶다면 */
.profile-card {
  animation: fadeInUp 0.4s ease-out 0.2s;
  animation-fill-mode: both;
}

.profile-content {
  animation: fadeInUp 0.4s ease-out 0.4s;
  animation-fill-mode: both;
}
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
  background-color: sandybrown;
  color: white;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.follow-button.following {
  background-color: #e0e0e0;
  color: #666;
}

.follow-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
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
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  cursor: pointer;
  text-decoration: none;
  color: inherit;
}

.list-item:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
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
  margin-bottom: 2rem;
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

.meta-left,
.meta-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.post-author,
.post-date,
.like-count {
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

    .meta-left,
    .meta-right {
      width: 100%;
      justify-content: center;
    }
  }
}
.tab-content {
  padding: 2rem;
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.content-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 1.5rem;
  color: #2c3e50;
}

.warning-section {
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 2rem;
}

.warning-title {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
  color: #721c24;
}

.warning-text {
  margin-bottom: 1rem;
  color: #721c24;
}

.btn-danger {
  background-color: #dc3545;
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-danger:hover {
  background-color: #c82333;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-card {
  background-color: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-width: 500px;
  width: 100%;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 1rem;
  color: #2c3e50;
}

.modal-text {
  margin-bottom: 1.5rem;
  color: #2c3e50;
}

.button-group {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-secondary:hover {
  background-color: #5a6268;
}
</style>
