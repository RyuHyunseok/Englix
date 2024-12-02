<template>
  <div class="page-container">
    <div class="movie-list-container">
      <h1 class="movies-title">Movies</h1>

      <div class="genre-filters">
        <button class="genre-filter-btn all-genres" :class="{ active: !selectedGenre }" @click="selectedGenre = null">
          <span class="filter-icon">🎬</span>
          전체 장르 보기
        </button>
        <button v-for="genre in genres" :key="genre.id" @click="selectGenre(genre)" :class="['genre-filter-btn', { active: selectedGenre?.id === genre.id }]">
          <span class="filter-icon">
            {{ getGenreIcon(genre.name) }}
          </span>
          {{ genre.name }}
        </button>
      </div>

      <div
        v-for="genre in genresWithMovies"
        :key="genre.id"
        :class="[
          'genre-section',
          {
            expanded: selectedGenre?.id === genre.id,
            hidden: selectedGenre && selectedGenre.id !== genre.id,
          },
        ]"
      >
        <h2 class="genre-title" @click="selectGenre(genre)">{{ genre.name }}</h2>

        <div :class="['movie-content', { 'grid-view': selectedGenre?.id === genre.id }]">
          <template v-if="!selectedGenre || selectedGenre.id !== genre.id">
            <div class="movie-slider">
              <button class="slider-button prev" @click="slide('left', genre.id)">
                <span class="arrow">&#8249;</span>
              </button>

              <div
                class="movie-row"
                :ref="
                  (el) => {
                    if (el) movieRows[genre.id] = el;
                  }
                "
              >
                <div v-for="movie in moviesByGenre[genre.id]" :key="movie.id" class="movie-card" @click="goToMovieDetail(movie.tmdb_id)">
                  <img :src="`https://image.tmdb.org/t/p/w300${movie.poster_path}`" :alt="movie.title" class="movie-poster" />
                  <h3 class="movie-title">{{ movie.title }}</h3>
                </div>
              </div>

              <button class="slider-button next" @click="slide('right', genre.id)">
                <span class="arrow">&#8250;</span>
              </button>
            </div>
          </template>

          <template v-else>
            <div class="movie-grid">
              <div v-for="movie in moviesByGenre[genre.id]" :key="movie.id" class="movie-card" @click="goToMovieDetail(movie.tmdb_id)">
                <img :src="`https://image.tmdb.org/t/p/w300${movie.poster_path}`" :alt="movie.title" class="movie-poster" />
                <h3 class="movie-title">{{ movie.title }}</h3>
              </div>
            </div>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";

// 선택된 장르 상태 추가
const selectedGenre = ref(null);

const selectGenre = (genre) => {
  // 토글 기능 제거
  selectedGenre.value = genre;
};

const getGenreIcon = (genreName) => {
  const icons = {
    Action: "💥",
    Adventure: "🗺️",
    Animation: "🎨",
    Comedy: "😆",
    Crime: "🕵️",
    Documentary: "📹",
    Drama: "🎭",
    Family: "👨‍👩‍👧‍👦",
    Fantasy: "🐉",
    History: "📚",
    Horror: "👻",
    Music: "🎵",
    Mystery: "🔍",
    Romance: "💖",
    "Science Fiction": "🚀",
    Thriller: "😱",
    "TV Movie": "📺",
    War: "⚔️",
    Western: "🤠",
  };
  return icons[genreName] || "🎬";
};

const authStore = useAuthStore();
const router = useRouter();
const movies = ref([]);
const genres = ref([]);
const loading = ref(true);
const movieRows = ref({}); // 각 장르별 row를 저장할 객체

// 장르별로 영화 분류
const moviesByGenre = computed(() => {
  const grouped = {};
  genres.value.forEach((genre) => {
    grouped[genre.id] = movies.value.filter((movie) => movie.genres.some((g) => g.id === genre.id));
  });
  return grouped;
});

// 영화가 있는 장르만 필터링하는 computed 속성 추가
const genresWithMovies = computed(() => {
  return genres.value.filter((genre) => moviesByGenre.value[genre.id] && moviesByGenre.value[genre.id].length > 0);
});

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

// 슬라이드 기능 수정
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

import { useToastStore } from "@/stores/toast";
const toastStore = useToastStore();

// mounted 시점에 ref 초기화
onMounted(async () => {
  await authStore.getUserProfile();

  try {
    const auth = localStorage.getItem("auth");
    if (!auth) {
      toastStore.addToast("로그인이 필요한 서비스입니다!", "warning");
      // alert("로그인이 필요한 서비스입니다.");
      router.push("/login");
      return;
    }

    const { token } = JSON.parse(auth);

    const [moviesResponse, genresResponse] = await Promise.all([
      axios({
        method: "get",
        url: "http://127.0.0.1:8000/movie/list/",
        headers: {
          Authorization: `Token ${token}`,
        },
      }),
      axios({
        method: "get",
        url: "http://127.0.0.1:8000/movie/genres/",
        headers: {
          Authorization: `Token ${token}`,
        },
      }),
    ]);

    movies.value = moviesResponse.data;
    genres.value = genresResponse.data;

    // ref 객체 초기화
    genres.value.forEach((genre) => {
      movieRows.value[genre.id] = null;
    });
  } catch (error) {
    console.error("Error fetching data:", error);
    if (error.response?.status === 401) {
      alert("로그인이 필요합니다.");
      router.push("/login");
    } else {
      alert("데이터를 불러오는데 실패했습니다.");
    }
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.genre-filters {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 20px;
  padding: 15px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.genre-filter-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  border: none;
  border-radius: 12px;
  background: #f8f9fa;
  color: #2c3e50;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-size: 14px;
  font-weight: 500;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.genre-filter-btn:hover {
  background: #e9ecef;
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.genre-filter-btn.active {
  background: #ff6b6b;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(52, 152, 219, 0.3);
}

.genre-filter-btn.all-genres {
  background: linear-gradient(135deg, #ff6b6b, #2ecc71);
  color: white;
}

.genre-filter-btn.all-genres:hover {
  background: linear-gradient(135deg, #ff6b6b, #27ae60);
}

.filter-icon {
  font-size: 16px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.genre-title {
  cursor: pointer;
  transition: all 0.3s ease;
}

.genre-title:hover {
  color: rgb(255, 107, 107);
  transform: translateX(5px);
}

.genre-section {
  transition: all 0.5s ease;
  max-height: 500px;
  opacity: 1;
  margin-bottom: 40px;
  overflow: hidden;
}

.genre-section.expanded {
  max-height: 2000px; /* 충분히 큰 값 */
}

.genre-section.hidden {
  max-height: 0;
  opacity: 0;
  margin: 0;
  padding: 0;
}

.movie-content {
  transition: all 0.5s ease;
}

.movie-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
  padding: 20px;
}

.grid-view .movie-card {
  animation: fadeIn 0.5s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ----------------------------------------------------------------- */

.movie-list-container {
  padding: 20px;
  width: 100%;
  padding: 0 50px;
  margin: 50px 0px;
}

.genre-section {
  margin-bottom: 40px;
  background-color: #ffffff; /* 흰색 섹션 배경 */
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05); /* 부드러운 그림자 */
}

.genre-title {
  color: #2c3e50; /* 진한 청색/회색 */
  margin-bottom: 16px;
  font-size: 24px;
  padding-left: 20px;
  font-weight: 600;
  border-left: 4px solid #ff6b6b; /* 파란색 강조선 */
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
  background-color: #ffffff;
  border-radius: 8px;
  padding: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.movie-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.movie-poster {
  width: 100%;
  height: 300px;
  object-fit: cover;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.movie-title {
  color: #2c3e50; /* 진한 청색/회색 */
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
  background-color: #ffffff; /* 흰색 배경 */
  border: 1px solid #e0e0e0;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 2;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.slider-button:hover {
  background-color: #ff6b6b; /* 호버 시 파란색 */
  border-color: #ff6b6b;
}

.slider-button:hover .arrow {
  color: white;
}

.slider-button.prev {
  left: -5px;
}

.slider-button.next {
  right: -5px;
}

.arrow {
  color: #2c3e50; /* 진한 청색/회색 */
  font-size: 24px;
  line-height: 1;
  transition: color 0.3s ease;
}

/* 학습 관련 추가 스타일 */
.movie-card:hover::before {
  opacity: 1;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .movie-card {
    width: 150px;
  }

  .movie-poster {
    height: 225px;
  }

  .genre-title {
    font-size: 20px;
  }

  .slider-button {
    width: 32px;
    height: 32px;
  }

  .arrow {
    font-size: 20px;
  }
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
.movie-list-container {
  animation: fadeInUp 0.6s ease-out;
}

/* 각 영화 카드에 순차적 애니메이션 적용 */
.movie-card {
  animation: fadeInUp 0.6s ease-out;
}

.genre-section {
  animation: fadeInUp 0.6s ease-out;
}

.movies-title {
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
</style>
