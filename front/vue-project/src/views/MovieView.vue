<template>
    <div class="page-container">

  <div class="movie-list-container">
    <!-- 선택된 정보를 보여주는 헤더 섹션 -->
    <div class="selection-header">
      <div class="selection-info">
        <div class="info-badge">
          <span class="badge-label">Learning Level:</span>
          <span class="badge-value">{{ level }}</span>
        </div>
        <div class="info-badge">
          <span class="badge-label">Study Goal:</span>
          <span class="badge-value">{{ category }}</span>
        </div>
        <div class="info-badge">
          <span class="badge-label">Genre:</span>
          <span class="badge-value">{{ genre }}</span>
        </div>
      </div>
    </div>

    <!-- 선택된 장르의 영화 목록 -->
    <div v-if="selectedGenreMovies.length > 0" class="genre-section">
      <div class="priority-info">
        <h2 class="genre-title">These movies will suit you!</h2>
      </div>

      <div class="movie-slider">
        <button class="slider-button prev" @click="slide('left', genre)">
          <span class="arrow">&#8249;</span>
        </button>

        <div class="movie-row" :ref="el => { if (el) movieRows[genre] = el }">
          <div 
            v-for="(movie, index) in selectedGenreMovies" 
            :key="movie.tmdb_id" 
            class="movie-card"
            :class="{ 'high-priority': index < 3 }"
            @click="goToMovieDetail(movie.tmdb_id)"
          >
            <div class="priority-marker" v-if="index < 3">
              <span class="priority-number">{{ index + 1 }}</span>
            </div>
            <img 
              :src="`https://image.tmdb.org/t/p/w300${movie.poster_path}`" 
              :alt="movie.title" 
              class="movie-poster"
            />
            <h3 class="movie-title">{{ movie.title }}</h3>
          </div>
        </div>

        <button class="slider-button next" @click="slide('right', genre)">
          <span class="arrow">&#8250;</span>
        </button>
      </div>
    </div>
    
    <div v-else class="no-movies">
      <h2>No movies found for {{ genre }} genre</h2>
    </div>
  </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";

const props = defineProps({
  category: String,
  level: String,
  genre: String,
});

const route = useRoute();
const router = useRouter();
const movieRows = ref({});

const level = ref("");
const category = ref("");
const genreMovieData = ref({});

// 선택된 장르의 영화만 필터링
const selectedGenreMovies = computed(() => {
  return genreMovieData.value[props.genre] || [];
});

const slide = (direction, genreId) => {
  const container = movieRows.value[genreId];
  if (container) {
    const scrollAmount = container.clientWidth * 0.8;
    if (direction === "left") {
      container.scrollBy({ left: -scrollAmount, behavior: "smooth" });
    } else {
      container.scrollBy({ left: scrollAmount, behavior: "smooth" });
    }
  }
};

const fetchMoviesByGenre = async () => {
  try {
    level.value = route.query.level;
    category.value = route.query.category;

    const auth = JSON.parse(localStorage.getItem("auth"));
    const token = auth?.token;

    const response = await axios.get("http://localhost:8000/movie/level-movies/", {
      headers: {
        Authorization: `Token ${token}`, // 토큰 추가
      },
      params: {
        level: level.value,
        goal: category.value,
      },
    });

    genreMovieData.value = response.data;
  } catch (error) {
    console.error("Error fetching movies:", error);
  }
};

const goToMovieDetail = (tmdbId) => {
  router.push({
    name: "MovieDetail",
    params: { tmdbId: tmdbId },
    query: {
      category: route.query.category,
      level: route.query.level,
    },
  });
};

onMounted(() => {
  fetchMoviesByGenre();
});
</script>

<style scoped>
.priority-info {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 20px;
}

.priority-badge {
  padding: 8px 16px;
  border-radius: 20px;
  background-color: rgb(238, 150, 150);
  color: var(--text-color);
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  box-shadow: var(--card-shadow);
}

.priority-icon {
  font-size: 18px;
  color: rgb(180, 93, 93);
}

.movie-card.high-priority {
  border: 2px solid rgb(199, 134, 134);
  position: relative;
}

.priority-marker {
  position: absolute;
  top: -10px;
  left: -10px;
  width: 30px;
  height: 30px;
  background-color: rgb(255, 107, 107);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  z-index: 1;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.priority-number {
  font-size: 16px;
}

.no-movies {
  text-align: center;
  padding: 40px;
  border-radius: 12px;
  color: var(--text-color-light);
  background-color: var(--surface-color);
  box-shadow: var(--card-shadow);
}

.movie-list-container {
  margin: 10px;
  width: 95%;
}

.selection-header {
  padding: 20px;
  border-radius: 12px;
  margin-bottom: 30px;
  background-color: var(--surface-color);
  box-shadow: var(--card-shadow);
  width: 95%;
}

.selection-info {
  display: flex;
  gap: 20px;
  justify-content: center;
  flex-wrap: wrap;
}

.info-badge {
  background-color: rgb(255, 107, 107);
  padding: 10px 20px;
  border-radius: 50px;
  color: var(--text-color-inverse);
  display: flex;
  align-items: center;
  gap: 10px;
}

.badge-label {
  font-size: 14px;
  opacity: 0.9;
}

.badge-value {
  font-weight: 600;
  font-size: 16px;
}

.genre-section {
  margin-bottom: 40px;
  border-radius: 12px;
  padding: 20px;
  background-color: var(--surface-color);
  box-shadow: var(--card-shadow);
  width: 95%;
}

.genre-title {
  color: var(--text-color);
  margin-bottom: 16px;
  font-size: 24px;
  padding-left: 20px;
  font-weight: 600;
  border-left: 4px solid var(--primary-color);
}

.movie-slider {
  position: relative;
  display: flex;
  align-items: center;
  padding: 0 10px;
}

.movie-row {
  display: flex;
  overflow-x: hidden;
  scroll-behavior: smooth;
  gap: 20px;
  padding: 20px 0;
}

.movie-card {
  flex: 0 0 auto;
  width: 200px;
  transition: all 0.3s ease;
  border-radius: var(--border-radius-md);
  padding: 10px;
  background-color: var(--card-color);
  box-shadow: var(--card-shadow);
}

.movie-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--card-shadow-hover);
}

.movie-poster {
  width: 100%;
  height: 300px;
  object-fit: cover;
  border-radius: var(--border-radius-md);
  transition: all 0.3s ease;
}

.movie-title {
  color: var(--text-color);
  font-size: 14px;
  margin-top: 12px;
  text-align: center;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-weight: 500;
}

.slider-button {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background-color: var(--surface-color);
  border: 1px solid var(--border-color);
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 2;
  transition: all 0.3s ease;
  box-shadow: var(--card-shadow);
}

.slider-button:hover {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
  color: var(--text-color-inverse);
}

.slider-button:hover .arrow {
  color: var(--text-color-inverse);
}

.slider-button.prev {
  left: -5px;
}

.slider-button.next {
  right: -5px;
}

.arrow {
  color: var(--text-color);
  font-size: 24px;
  line-height: 1;
  transition: color 0.3s ease;
}

@media (max-width: 768px) {
  .movie-card {
    width: 150px;
  }

  .movie-poster {
    height: 225px;
  }

  .info-badge {
    padding: 8px 16px;
  }

  .badge-value {
    font-size: 14px;
  }
}
.genre-title {
  color: #2c3e50; /* 진한 청색/회색 */
  margin-bottom: 16px;
  font-size: 24px;
  padding-left: 20px;
  font-weight: 600;
  border-left: 4px solid #ff6b6b; 
}
</style>