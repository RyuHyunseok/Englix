<template>
  <div class="favorite-movies">
    <div v-if="favorites.length > 0" class="movies-grid">
      <div v-for="movie in favorites" :key="movie.movie_tmdb_id" class="movie-card">
        <div @click="goToMovieDetail(movie.movie_tmdb_id)" class="movie-link" style="cursor: pointer">
          <img :src="movie.poster_path" :alt="movie.movie_title" class="movie-poster" />
          <h3>{{ movie.movie_title }}</h3>
        </div>
      </div>
    </div>
    <div v-else class="empty-message">찜한 영화가 없습니다.</div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import axios from "axios";
import { useRoute, useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const favorites = ref([]);

// props 정의
const props = defineProps({
  username: {
    type: String,
    required: true
  }
});

const fetchFavoriteMovies = async () => {
  try {
    const auth = localStorage.getItem("auth");
    if (!auth) {
      router.push("/login");
      return;
    }

    const { token } = JSON.parse(auth);

    const response = await axios({
      method: "get",
      url: `http://localhost:8000/movie/favorite-movies/${props.username}/`,
      headers: {
        Authorization: `Token ${token}`,
      },
    });

    favorites.value = response.data;
  } catch (error) {
    console.error("찜한 영화 목록을 가져오는데 실패했습니다:", error);
  }
};

// 영화 상세 페이지로 이동하는 함수
const goToMovieDetail = async (tmdbId) => {
  try {
    const userProfile = await authStore.getUserProfile();
    const userLevel = userProfile?.level || "Beginner";
    const userGoal = userProfile?.goal || "SAT";
    const user_prefer_genre = userProfile?.prefer_genre || "Action";

    router.push({
      name: "MovieDetail",
      params: { tmdbId: tmdbId.toString() },
      query: {
        category: userGoal,
        level: userLevel,
        prefer_genre: user_prefer_genre,
      },
    });
  } catch (error) {
    console.error("영화 상세 페이지로 이동 중 오류 발생:", error);
    router.push({
      name: "MovieDetail",
      params: { tmdbId: tmdbId.toString() },
      query: {
        category: "SAT",
        level: "Beginner",
        prefer_genre: "Action",
      },
    });
  }
};

watch(() => props.username, (newUsername) => {
  if (newUsername) {
    fetchFavoriteMovies();
  }
});

onMounted(() => {
  if (props.username) {
    fetchFavoriteMovies();
  }
});
</script>

<style scoped>
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
.empty-message {
  text-align: center;
  padding: 2rem;
  color: #868e96;
  background: #f8f9fa;
  border-radius: 12px;
}
</style>
