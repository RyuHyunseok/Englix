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
      <!-- 게시글 내용 -->
      <h2 class="board-title">{{ getBoardTitle }}</h2>

    <form @submit.prevent="handleSubmit" class="create-form">
      <div class="form-group">
        <label for="title">제목</label>
        <input 
          type="text" 
          id="title" 
          v-model.trim="title" 
          placeholder="제목을 입력하세요" 
          required 
        />
      </div>

      <div class="form-group">
        <label for="content">내용</label>
        <textarea 
          id="content" 
          v-model.trim="content" 
          placeholder="내용을 입력하세요" 
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

      <button type="submit" class="submit-button">
        ✨ 작성하기
      </button>
    </form>
  </div>
  </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { RouterLink, useRouter, useRoute } from "vue-router";
import { usePostStore } from "@/stores/posts";
import axios from "axios";

const title = ref("");
const content = ref("");
const router = useRouter();
const route = useRoute();
const store = usePostStore();
const selectedFile = ref(null);

const previewUrl = ref(null);

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
  const category = route.query.category;
  switch (category) {
    case "QandA":
      return "질문 게시판";
    case "LearningResource":
      return "자료 공유 게시판";
    default:
      return "자유 게시판";
  }
});

const handleFileChange = (event) => {
  const file = event.target.files[0];
  selectedFile.value = file;

  // 이미지 파일인 경우 미리보기 생성
  if (file && file.type.startsWith("image/")) {
    const reader = new FileReader();
    reader.onload = (e) => {
      previewUrl.value = e.target.result;
    };
    reader.readAsDataURL(file);
  } else {
    previewUrl.value = null;
  }
};

const handleSubmit = async () => {
  try {
    const auth = localStorage.getItem("auth");
    if (!auth) {
      alert("로그인이 필요합니다.");
      router.push({ name: "login" });
      return;
    }

    const formData = new FormData();
    formData.append("title", title.value);
    formData.append("content", content.value);
    formData.append("category", route.query.category || "free");
    if (selectedFile.value) {
      formData.append("file", selectedFile.value);
    }

    const { token } = JSON.parse(auth);

    const response = await axios({
      method: "POST",
      url: "http://127.0.0.1:8000/community/posts/",
      headers: {
        Authorization: `Token ${token}`,
        "Content-Type": "multipart/form-data",
      },
      data: formData,
    });

    router.push({
      name: "postDetail",
      params: { id: response.data.id },
    });
  } catch (error) {
    alert("게시글 작성에 실패했습니다.");
    console.error(error);
  }
};
</script>

<style scoped>
.form-container {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h1 {
  text-align: center;
  color: #333;
  margin-bottom: 20px;
}

form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

label {
  font-weight: bold;
  color: #666;
  margin-bottom: 5px;
}

input[type="text"],
textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1em;
}

textarea {
  min-height: 200px;
  resize: vertical;
}

input[type="submit"] {
  width: 100%;
  padding: 12px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1em;
  transition: background-color 0.3s;
}

input[type="submit"]:hover {
  background-color: #45a049;
}

.error-message {
  color: #f44336;
  font-size: 0.9em;
  margin-top: 5px;
}

@media (max-width: 768px) {
  .form-container {
    margin: 10px;
    padding: 15px;
  }

  input[type="submit"] {
    padding: 10px;
  }
}
.file-input {
  margin: 10px 0;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  width: 100%;
}

.file-name {
  font-size: 0.9em;
  color: #666;
  margin-top: 5px;
}
.image-preview {
  margin: 15px 0;
  text-align: center;
}

.preview-image {
  max-width: 100%;
  max-height: 300px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.file-input {
  margin: 10px 0;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  width: 100%;
}

.file-name {
  font-size: 0.9em;
  color: #666;
  margin-top: 5px;
}
.community-title {
  font-size: 32px;
  font-weight: bold;
  margin: 30px 0;
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
}

.nav-item:hover {
  transform: translateY(-2px);
  background: #fff5f5;
}

.nav-item.active {
  background: #ff6b6b;
  color: white;
}

.create-form {
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

input[type="text"],
textarea {
  width: 100%;
  padding: 12px 15px;
  border: 2px solid #e9ecef;
  border-radius: 12px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background-color: #f8f9fa;
}

input[type="text"]:focus,
textarea:focus {
  outline: none;
  border-color: #ff6b6b;
  background-color: white;
}

textarea {
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

.submit-button {
  width: 100%;
  padding: 15px 25px;
  background-color: #ff6b6b;
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(255, 107, 107, 0.2);
}

.submit-button:hover {
  background-color: #fa5252;
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(255, 107, 107, 0.3);
}

.board-title {
  font-size: 1.8rem;
  color: #495057;
  font-weight: 600;
  text-align: center;
  margin-bottom: 30px;
  position: relative;
}

.board-title::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  width: 100px;
  height: 3px;
  background: linear-gradient(to right, #ff6b6b, #ffa8a8);
  border-radius: 2px;
}

@media (max-width: 768px) {
  .create-form {
    padding: 20px;
    margin: 0 15px;
  }

  .submit-button {
    padding: 12px 20px;
  }
}

/* 애니메이션 */
.create-form {
  animation: slideUp 0.5s ease-out;
}

@keyframes slideUp {
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
