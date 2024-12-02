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
    <div class="content-section" v-if="post">
      <!-- 게시글 내용 -->
      <h2 class="board-title">{{ getBoardTitle }}</h2>

      <div v-if="!isEditing" class="post-content">
        <!-- 기존 게시글 보기 내용 -->
        <h2>{{ post.title }}</h2>
        <div class="post-info">
          <p>
            작성자:
            <router-link :to="{ name: 'profile', params: { username: post.user.username } }" class="author-link">
              {{ post.user.nickname }}
            </router-link>
          </p>
          <p>작성일: {{ post.created_at }}</p>
          <div class="like-section">
            <button @click="handleLike" :class="{ liked: isLiked }" class="like-button">❤️ {{ likesCount }}</button>
          </div>
        </div>
        <div class="content">{{ post.content }}</div>

        <div v-if="post.file" class="file-section">
          <!-- 이미지인 경우 미리보기 표시 -->
          <div v-if="post.is_image" class="image-preview">
            <img :src="post.file" :alt="post.title" class="attached-image" @click="openImageModal" />
          </div>

          <!-- 파일 다운로드 버튼 -->
          <div class="file-download">
            <button @click="downloadFile" class="download-button">
              <span class="download-icon">📎</span>
              첨부파일 다운로드
            </button>
            <span class="file-name">{{ getFileName(post.file) }}</span>
          </div>
        </div>

        <!-- 이미지 모달 - Teleport 사용 -->
        <Teleport to="body">
          <div v-if="showImageModal" class="image-modal" @click.self="closeImageModal">
            <div class="modal-content">
              <button class="close-button" @click.stop="closeImageModal">×</button>
              <img :src="post.file" :alt="post.title" class="modal-image" />
            </div>
          </div>
        </Teleport>

        <div v-if="isAuthor" class="button-group">
          <button @click="startEditing" class="edit-btn">수정</button>
          <button @click="confirmDelete" class="delete-btn">삭제</button>
        </div>

        <!-- 댓글 섹션 - 수정 모드가 아닐 때만 표시 -->
        <div class="comments-section">
          <h3>댓글</h3>

          <div class="comment-form">
            <textarea v-model="newComment" placeholder="댓글을 입력하세요" class="comment-input"></textarea>
            <button @click="addComment" class="comment-submit-btn">댓글 작성</button>
          </div>

          <div class="comments-list">
            <div v-for="comment in comments" :key="comment.id" class="comment-item">
              <div class="comment-header">
                <router-link :to="{ name: 'profile', params: { username: comment.user.username } }" class="comment-author">
                  {{ comment.user.nickname }}
                </router-link>
                <span class="comment-date">{{ comment.created_at }}</span>
              </div>
              <p class="comment-content">{{ comment.content }}</p>
              <button v-if="comment.user.username === currentUser" @click="deleteComment(comment.id)" class="comment-delete-btn">삭제</button>
            </div>
          </div>
        </div>
      </div>

      <!-- 게시글 수정 폼 -->
<div v-else class="edit-form">
  <div class="form-group">
    <label for="title">제목</label>
    <input 
      type="text" 
      id="title" 
      v-model="editTitle" 
      placeholder="제목을 입력하세요" 
      class="edit-input"
      required 
    />
  </div>
  <div class="form-group">
    <label for="content">내용</label>
    <textarea 
      id="content" 
      v-model="editContent" 
      placeholder="내용을 입력하세요" 
      class="edit-textarea"
      required
    ></textarea>
  </div>

  <div class="form-group">
    <label for="file">
      📎 파일 첨부
    </label>
    <input 
      type="file" 
      id="file" 
      @change="handleFileChange" 
      class="file-input"
      accept="image/*,.pdf,.doc,.docx,.txt"
    />

    <!-- 이미지 미리보기 -->
    <div v-if="previewUrl" class="image-preview">
      <img :src="previewUrl" alt="Preview" class="preview-image" />
    </div>

    <p class="file-name" v-if="selectedFile">
      선택된 파일: {{ selectedFile.name }}
    </p>
  </div>

  <div class="button-group">
    <button @click="updatePost" class="save-btn">
      ✨ 저장하기
    </button>
    <button @click="cancelEdit" class="cancel-btn">취소</button>
  </div>
</div>

<div v-if="!isEditing" class="nav-buttons">
  <button @click="goBack" class="back-btn">목록으로</button>
</div>
</div>
  </div>
  </div>
  
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, Teleport } from "vue";
import { useRoute, useRouter, RouterLink } from "vue-router";
import { usePostStore } from "@/stores/posts";
import axios from "axios";
import CommunityNavbar from "@/components/CommunityNavbar.vue";

const route = useRoute();
const store = usePostStore();

const post = ref(null);
const isEditing = ref(false);
const editTitle = ref("");
const editContent = ref("");
const currentUser = ref("");
const comments = ref([]);
const newComment = ref("");
const isLiked = ref(false);
const likesCount = ref(0);
const showImageModal = ref(false);

const router = useRouter();
const searchQuery = ref("");

const handleSearch = async () => {
  if (!searchQuery.value.trim()) return;

  try {
    const auth = localStorage.getItem("auth");
    if (!auth) return;

    const { token } = JSON.parse(auth);

    const response = await axios({
      method: "get",
      url: "http://127.0.0.1:8000/community/posts/search/",
      headers: { Authorization: `Token ${token}` },
      params: { query: searchQuery.value },
    });

    router.push({
      name: "communitySearchResults",
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

const getBoardTitle = computed(() => {
  if (!post.value) return "";

  switch (post.value.category) {
    case "QandA":
      return "질문 게시판";
    case "LearningResource":
      return "자료 공유 게시판";
    default:
      return "자유 게시판";
  }
});
const openImageModal = () => {
  showImageModal.value = true;
  document.body.style.overflow = "hidden";
};

const closeImageModal = () => {
  showImageModal.value = false;
  document.body.style.overflow = "auto";
};

// ESC 키 이벤트 핸들러를 별도 함수로 분리
const handleEscKey = (e) => {
  if (e.key === "Escape" && showImageModal.value) {
    closeImageModal();
  }
};

onMounted(() => {
  window.addEventListener("keydown", handleEscKey);
});

onUnmounted(() => {
  window.removeEventListener("keydown", handleEscKey); // 동일한 함수 참조 사용
  document.body.style.overflow = "auto";
});
// 좋아요 처리 함수
const handleLike = async () => {
  try {
    const token = JSON.parse(localStorage.getItem("auth")).token;
    const response = await axios({
      method: "post",
      url: `http://127.0.0.1:8000/community/posts/${post.value.id}/like/`,
      headers: {
        Authorization: `Token ${token}`,
      },
    });

    isLiked.value = !isLiked.value;
    likesCount.value = response.data.likes_count;

    // 게시글 데이터 업데이트
    post.value = {
      ...post.value,
      is_liked: isLiked.value,
      likes_count: likesCount.value,
    };
  } catch (error) {
    console.error("좋아요 처리 실패:", error);
    alert("좋아요 처리에 실패했습니다.");
  }
};

const isAuthor = computed(() => {
  if (!post.value || !currentUser.value) return false;
  return currentUser.value === post.value.user.username;
});

// 댓글 목록 불러오기
const fetchComments = async () => {
  try {
    const token = JSON.parse(localStorage.getItem("auth")).token;
    const response = await axios({
      method: "get",
      url: `http://127.0.0.1:8000/community/posts/${route.params.id}/comments/`,
      headers: {
        Authorization: `Token ${token}`,
      },
    });
    comments.value = response.data;
  } catch (error) {
    alert("댓글을 불러오는데 실패했습니다.");
  }
};

// 댓글 작성
const addComment = async () => {
  if (!newComment.value.trim()) {
    alert("댓글 내용을 입력해주세요.");
    return;
  }

  try {
    const token = JSON.parse(localStorage.getItem("auth")).token;
    const response = await axios({
      method: "post",
      url: `http://127.0.0.1:8000/community/posts/${route.params.id}/comments/`,
      headers: {
        Authorization: `Token ${token}`,
        "Content-Type": "application/json",
      },
      data: {
        content: newComment.value,
      },
    });

    comments.value = [response.data, ...comments.value];
    newComment.value = "";
  } catch (error) {
    alert("댓글 작성에 실패했습니다.");
  }
};

// 댓글 삭제
const deleteComment = async (commentId) => {
  if (!confirm("댓글을 삭제하시겠습니까?")) return;

  try {
    await axios({
      method: "delete",
      url: `http://127.0.0.1:8000/community/comments/${commentId}/update/`,
      headers: {
        Authorization: `Token ${JSON.parse(localStorage.getItem("auth")).token}`,
      },
    });
    comments.value = comments.value.filter((c) => c.id !== commentId);
  } catch (error) {
    alert("댓글 삭제에 실패했습니다.");
  }
};

onMounted(async () => {
  const auth = localStorage.getItem("auth");
  if (auth) {
    const parsedAuth = JSON.parse(auth);
    currentUser.value = parsedAuth.username;
  }
  const response = await store.getPostDetail(route.params.id);
  post.value = response;
  isLiked.value = response.is_liked; // 서버에서 받은 좋아요 상태
  likesCount.value = response.likes_count; // 서버에서 받은 좋아요 수
  await fetchComments();
});

const cancelEdit = () => {
  isEditing.value = false;
  editTitle.value = "";
  editContent.value = "";
};
const startEditing = () => {
  editTitle.value = post.value.title;
  editContent.value = post.value.content;
  isEditing.value = true;
};
const updatePost = async () => {
  if (!editTitle.value.trim() || !editContent.value.trim()) {
    alert("제목과 내용을 모두 입력해주세요.");
    return;
  }

  try {
    const auth = localStorage.getItem("auth");
    if (!auth) {
      alert("로그인이 필요합니다.");
      router.push({ name: "login" });
      return;
    }

    const token = JSON.parse(auth).token;
    const response = await axios({
      method: "put",
      url: `http://127.0.0.1:8000/community/posts/${post.value.id}/`,
      headers: {
        Authorization: `Token ${token}`,
        "Content-Type": "application/json",
      },
      data: {
        title: editTitle.value,
        content: editContent.value,
      },
    });

    post.value = response.data;
    isEditing.value = false;
    alert("게시글이 수정되었습니다.");
  } catch (error) {
    alert("게시글 수정에 실패했습니다.");
  }
};

const confirmDelete = async () => {
  if (confirm("정말로 이 게시글을 삭제하시겠습니까?")) {
    try {
      await store.deletePost(post.value.id);
      router.push({ name: "community" });
    } catch (error) {
      alert("게시글 삭제에 실패했습니다.");
    }
  }
};

const goBack = () => {
  let routeName;
  switch (post.value.category) {
    case "QandA":
      routeName = "Q&A";
      break;
    case "LearningResource":
      routeName = "resource";
      break;
    default:
      routeName = "community";
  }
  router.push({ name: routeName });
};

const getFileName = (fileUrl) => {
  if (!fileUrl) return "";
  return fileUrl.split("/").pop();
};

const downloadFile = async () => {
  try {
    const response = await axios({
      url: post.value.file,
      method: "GET",
      responseType: "blob",
    });

    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", getFileName(post.value.file));
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error("파일 다운로드 실패:", error);
    alert("파일 다운로드에 실패했습니다.");
  }
};
</script>

<style scoped>
.post-detail {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.post-content {
  margin-bottom: 20px;
}

h2 {
  color: #333;
  margin-bottom: 15px;
}

.post-info {
  color: #666;
  font-size: 0.9em;
  margin-bottom: 20px;
}

.content {
  line-height: 1.6;
  margin: 20px 0;
  white-space: pre-wrap;
}

.button-group {
  margin: 20px 0;
  display: flex;
  gap: 10px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  color: #666;
}

.edit-input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1em;
}

.edit-textarea {
  width: 100%;
  min-height: 200px;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1em;
  resize: vertical;
}

button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
}

.edit-btn {
  background-color: #4caf50;
  color: white;
}

.delete-btn {
  background-color: #f44336;
  color: white;
}

.save-btn {
  background-color: #2196f3;
  color: white;
}

.cancel-btn {
  background-color: #808080;
  color: white;
}

.back-btn {
  background-color: #666;
  color: white;
}

button:hover {
  opacity: 0.9;
}

.nav-buttons {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.comments-section {
  margin-top: 40px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.comment-form {
  margin-bottom: 20px;
}

.comment-input {
  width: 100%;
  min-height: 80px;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  resize: vertical;
}

.comment-submit-btn {
  background-color: #4caf50;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.comments-list {
  margin-top: 20px;
}

.comment-item {
  padding: 15px;
  border: 1px solid #eee;
  border-radius: 4px;
  margin-bottom: 10px;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 0.9em;
  color: #666;
}

.comment-content {
  margin-bottom: 10px;
}

.comment-delete-btn {
  background-color: #f44336;
  color: white;
  border: none;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8em;
  cursor: pointer;
}

.comment-delete-btn:hover {
  opacity: 0.9;
}

.comment-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}

.comment-author {
  color: #2196f3;
  text-decoration: none;
  font-weight: bold;
}

.comment-author:hover {
  text-decoration: underline;
}

.comment-date {
  font-size: 0.85em;
  color: #666;
}

@media (max-width: 768px) {
  .post-detail {
    margin: 10px;
    padding: 15px;
  }

  .button-group {
    flex-direction: column;
  }

  button {
    width: 100%;
    margin: 5px 0;
  }

  .like-section {
    margin: 10px 0;
  }

  .like-button {
    padding: 8px 16px;
    border: none;
    border-radius: 20px;
    cursor: pointer;
    background-color: #f8f9fa;
    transition: all 0.3s ease;
  }

  .like-button.liked {
    background-color: #ffebee;
    color: #e91e63;
  }

  .like-button:hover {
    transform: scale(1.05);
  }
}
.file-attachment {
  margin: 20px 0;
  padding: 15px;
  background-color: #f5f5f5;
  border-radius: 8px;
}

.download-link {
  display: inline-block;
  padding: 8px 16px;
  background-color: #4caf50;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.download-link:hover {
  background-color: #45a049;
}

.file-section {
  margin: 20px 0;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.image-preview {
  margin-bottom: 20px;
  text-align: center;
}

.attached-image {
  max-width: 100%;
  max-height: 500px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.file-download {
  display: flex;
  align-items: center;
  gap: 10px;
}

.download-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.3s ease;
}

.download-button:hover {
  background-color: #45a049;
}

.download-icon {
  font-size: 1.2em;
}

.file-name {
  color: #666;
  font-size: 0.9em;
  word-break: break-all;
}
.attached-image {
  max-width: 100%;
  max-height: 500px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.2s ease;
}

.attached-image:hover {
  transform: scale(1.02);
}

/* 모달 스타일 */
.image-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.9);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  position: relative;
  max-width: 90vw;
  max-height: 90vh;
}

.modal-image {
  max-width: 100%;
  max-height: 90vh;
  object-fit: contain;
}

.close-button {
  position: absolute;
  top: -40px;
  right: 0;
  background: none;
  border: none;
  color: white;
  font-size: 30px;
  cursor: pointer;
  padding: 10px;
  z-index: 1001;
}

.close-button:hover {
  color: #ddd;
}

/* 모달 줌 기능 */
@media (min-width: 768px) {
  .modal-content {
    transition: transform 0.3s ease;
  }

  .modal-image {
    cursor: zoom-in;
  }
}

/* 모바일 대응 */
@media (max-width: 767px) {
  .modal-content {
    width: 100%;
  }

  .close-button {
    top: -30px;
    right: 0;
  }
}
.community-title {
  font-size: 32px;
  font-weight: bold;
  margin: 30px 0;
  text-align: center;
}

.board-title {
  font-size: 24px;
  color: #333;
  margin: 20px 0;
  text-align: center;
}
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
.community-title {
  font-size: 32px;
  font-weight: bold;
  margin: 30px 0;
  text-align: center;
}

.board-title {
  font-size: 24px;
  color: #333;
  margin: 20px 0;
  text-align: center;
}

.post-content {
  background-color: white;
  border-radius: 15px;
  padding: 30px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  margin-bottom: 20px;
}

.post-info {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 15px 0;
  border-bottom: 1px solid #eee;
  margin-bottom: 20px;
}

.author-link {
  color: #ff6b6b;
  text-decoration: none;
  font-weight: 600;
}

.author-link:hover {
  text-decoration: underline;
}

.like-button {
  padding: 8px 16px;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  background-color: #f8f9fa;
  transition: all 0.3s ease;
}

.like-button.liked {
  background-color: #ffebee;
  color: #e91e63;
}

.like-button:hover {
  transform: scale(1.05);
}

.comment-section {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.comment-form {
  margin-bottom: 20px;
}

.comment-input {
  width: 100%;
  padding: 15px;
  border: 2px solid #eee;
  border-radius: 12px;
  margin-bottom: 10px;
  resize: vertical;
  min-height: 100px;
  transition: all 0.3s ease;
}

.comment-input:focus {
  border-color: #ff6b6b;
  outline: none;
}

.comment-submit-btn {
  background-color: #ff6b6b;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.comment-submit-btn:hover {
  background-color: #fa5252;
  transform: translateY(-2px);
}

.comment-item {
  background-color: #f8f9fa;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 15px;
  transition: all 0.3s ease;
}

.comment-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.comment-author {
  color: #ff6b6b;
  font-weight: 600;
  text-decoration: none;
}

.comment-date {
  color: #868e96;
  font-size: 0.9em;
}

.comment-content {
  color: #495057;
  line-height: 1.6;
}

.comment-delete-btn {
  background-color: #ff6b6b;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.9em;
  margin-top: 10px;
  transition: all 0.3s ease;
}

.comment-delete-btn:hover {
  background-color: #fa5252;
}

.button-group {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.edit-btn, .delete-btn, .save-btn, .cancel-btn, .back-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.edit-btn {
  background-color: #4CAF50;
  color: white;
}

.delete-btn {
  background-color: #ff6b6b;
  color: white;
}

.save-btn {
  background-color: #4CAF50;
  color: white;
}

.cancel-btn {
  background-color: #868e96;
  color: white;
}

.back-btn {
  background-color: #495057;
  color: white;
}

.edit-form {
  background-color: white;
  border-radius: 15px;
  padding: 30px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.edit-input, .edit-textarea {
  width: 100%;
  padding: 12px;
  border: 2px solid #eee;
  border-radius: 12px;
  margin-bottom: 20px;
  transition: all 0.3s ease;
}

.edit-input:focus, .edit-textarea:focus {
  border-color: #ff6b6b;
  outline: none;
}

.edit-textarea {
  min-height: 200px;
  resize: vertical;
}

@media (max-width: 768px) {
  .post-info {
    flex-direction: column;
    gap: 10px;
    align-items: flex-start;
  }

  .button-group {
    flex-direction: column;
  }

  .edit-btn, .delete-btn, .save-btn, .cancel-btn, .back-btn {
    width: 100%;
  }
}
.edit-form {
  max-width: 800px;
  margin: 0 auto;
  background: white;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.form-group {
  margin-bottom: 25px;
}

label {
  display: block;
  font-size: 1.1rem;
  color: #495057;
  margin-bottom: 10px;
  font-weight: 500;
}

.edit-input,
.edit-textarea {
  width: 100%;
  padding: 12px 15px;
  border: 2px solid #e9ecef;
  border-radius: 12px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background-color: #f8f9fa;
}

.edit-input:focus,
.edit-textarea:focus {
  outline: none;
  border-color: #ff6b6b;
  background-color: white;
}

.edit-textarea {
  min-height: 300px;
  resize: vertical;
  line-height: 1.6;
}

.file-input {
  display: block;
  width: 100%;
  padding: 10px;
  background: #f8f9fa;
  border: 2px dashed #e9ecef;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.file-input:hover {
  border-color: #ff6b6b;
  background: #fff5f5;
}

.image-preview {
  margin: 20px 0;
  text-align: center;
  background: #f8f9fa;
  padding: 20px;
  border-radius: 12px;
}

.preview-image {
  max-width: 100%;
  max-height: 300px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.file-name {
  margin-top: 10px;
  color: #868e96;
  font-size: 0.9rem;
  padding: 8px 12px;
  background: #f8f9fa;
  border-radius: 8px;
  display: inline-block;
}

.button-group {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.save-btn,
.cancel-btn {
  padding: 15px 25px;
  border: none;
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.save-btn {
  background-color: #ff6b6b;
  color: white;
  flex: 1;
  box-shadow: 0 4px 12px rgba(255, 107, 107, 0.2);
}

.save-btn:hover {
  background-color: #fa5252;
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(255, 107, 107, 0.3);
}

.cancel-btn {
  background-color: #e9ecef;
  color: #495057;
  padding: 15px 30px;
}

.cancel-btn:hover {
  background-color: #dee2e6;
  transform: translateY(-2px);
}
</style>
