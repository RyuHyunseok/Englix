<template>
    <div class="page-container">
      <div class="search-results">
    <h2 class="search-title">"{{ searchQuery }}" 검색 결과 🎬</h2>
    <div v-if="searchResults && searchResults.length > 0" class="movies-grid">
      <div v-for="movie in searchResults" :key="movie.tmdb_id" class="movie-card">
        <div class="movie-link" @click="goToMovieDetail(movie.tmdb_id)">
          <div class="movie-poster-container">
            <img :src="movie.poster_path" :alt="movie.title" class="movie-poster" />
            <div class="movie-hover-info">
              <h3 class="movie-title">{{ movie.title }}</h3>
              <p class="movie-release">{{ movie.release_date }}</p>
              <p class="movie-overview">{{ movie.overview }}</p>
              <button class="view-details-btn">상세보기 ✨</button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="no-results">
      <div class="no-results-icon">🤔</div>
      <h3 class="no-results-title">검색 결과가 없습니다</h3>
      <p class="no-results-text">다른 검색어로 다시 시도해보세요</p>
    </div>
  </div>
    </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const router = useRouter();
const authStore = useAuthStore();
const route = useRoute();
const searchQuery = ref("");
const searchResults = ref([]);

// 영화 상세 페이지로 이동하는 함수
const goToMovieDetail = (tmdbId) => {
  const userLevel = authStore.userProfile?.level || "Beginner";
  const userGoal = authStore.userProfile?.goal || "SAT";
  const user_prefer_genre = authStore.userProfile?.prefer_genre || "Action";

  router.push({
    name: "MovieDetail",
    params: { tmdbId: tmdbId.toString() },
    query: {
      category: userGoal,
      level: userLevel,
      prefer_genre: user_prefer_genre,
    },
  });
};

const updateSearchResults = () => {
  searchQuery.value = route.query.q;
  try {
    if (route.query.results) {
      const data = JSON.parse(route.query.results);
      searchResults.value = data.results || [];
    }
  } catch (error) {
    console.error("Search results parsing error:", error);
    searchResults.value = [];
  }
};

onMounted(updateSearchResults);
watch(() => route.query, updateSearchResults, { deep: true });
</script>

<style scoped>
.search-results {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 50px;
}

.search-title {
  font-size: 2rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 30px;
}

.movies-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 15px;
}

.movie-card {
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.3s ease;
  width: 80%;
  height: 80%;
}

.movie-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.15);
}

.movie-link {
  display: block;
  text-decoration: none;
  color: inherit;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.movie-poster-container {
  position: relative;
  overflow: hidden;
  padding-top: 150%;
}

.movie-poster {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.movie-card:hover .movie-poster {
  transform: scale(1.05);
}

.movie-info {
  padding: 15px;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.movie-title {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 10px;
}

.movie-release {
  font-size: 0.9rem;
  color: #888;
  margin-bottom: 15px;
}

.movie-overview {
  font-size: 0.9rem;
  line-height: 1.5;
  color: #555;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  flex-grow: 1;
}

.no-results {
  text-align: center;
  padding: 50px;
  background-color: #f8f9fa;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.no-results-icon {
  font-size: 4rem;
  margin-bottom: 20px;
}

.no-results-title {
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

.no-results-text {
  font-size: 1rem;
  color: #666;
}
.search-results {
  max-width: 1200px;
  margin-bottom: 10px;
  background-color: #ffffff; /* 흰색 섹션 배경 */
  border-radius: 12px;
  padding: 20px 40px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05); /* 부드러운 그림자 */
}

.search-title {
  font-size: 2rem;
  font-weight: bold;
  color: #2c3e50;
  margin: 30px 0;
  text-align: center;
  padding-bottom: 15px;
  border-bottom: 2px solid #eee;
}

.movies-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 2px;
  padding: 10px 10px;
}

.movie-card {
  background-color: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s ease;
  cursor: pointer;
}

.movie-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

.movie-poster-container {
  position: relative;
  overflow: hidden;
  aspect-ratio: 16/6;
}

.movie-poster {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.movie-hover-info {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  padding: 20px;
  color: white;
  opacity: 0;
  transition: opacity 0.3s ease;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.movie-card:hover .movie-hover-info {
  opacity: 1;
}

.movie-title {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 10px;
}

.movie-release {
  font-size: 0.9rem;
  color: #ff6b6b;
  margin-bottom: 15px;
}

.movie-overview {
  font-size: 0.9rem;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin-bottom: 20px;
}

.view-details-btn {
  padding: 8px 16px;
  background-color: #ff6b6b;
  color: white;
  border: none;
  border-radius: 20px;
  font-weight: bold;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.view-details-btn:hover {
  transform: scale(1.05);
}

.no-results {
  text-align: center;
  padding: 50px;
  background: white;
  border-radius: 16px;
  margin: 40px auto;
  max-width: 500px;
}

.no-results-icon {
  font-size: 4rem;
  margin-bottom: 20px;
}

.no-results-title {
  font-size: 1.5rem;
  font-weight: bold;
  color: #ff6b6b;
  margin-bottom: 10px;
}

.no-results-text {
  color: #666;
  font-size: 1.1rem;
}

@media (max-width: 768px) {
  .search-results {
    padding: 0 20px;
  }

  .search-title {
    font-size: 1.5rem;
  }

  .movies-grid {
    gap: 20px;
  }
}

/* 애니메이션 */
.movie-card,.search-results {
  animation: fadeInUp 0.5s ease-out forwards;
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
.favorite-movies {
  padding: 20px;
}

.movies-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.movie-card {
  border: 1px solid #ddd;
  padding: 10px;
  border-radius: 8px;
  background-color: white;
  transition: transform 0.2s;
}

.movie-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.movie-link {
  text-decoration: none;
  color: inherit;
}

.movie-poster {
  width: 100%;
  height: auto;
  border-radius: 4px;
  margin-bottom: 10px;
}

.movie-card h3 {
  margin: 10px 0;
  font-size: 1.1em;
  text-align: center;
}

.movie-card p {
  margin: 5px 0;
  font-size: 0.9em;
  color: #666;
}

</style>