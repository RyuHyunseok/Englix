<template>
  <div class="movies-page">
    <movie-genre-list :genre-title="'수능 영화'" :movies="movies" />
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import { useAuthStore } from "@/stores/auth";
import MovieGenreList from "@/components/movies/MovieGenreList.vue";

export default {
  name: "CSATMovies",
  components: {
    MovieGenreList,
  },
  setup() {
    const movieStore = useAuthStore();
    const movies = ref([]);

    onMounted(async () => {
      try {
        const response = await movieStore.fetchMoviesByCategory("csat");
        movies.value = response;
      } catch (error) {
        console.error("Error fetching movies:", error);
      }
    });

    return {
      movies,
    };
  },
};
</script>
