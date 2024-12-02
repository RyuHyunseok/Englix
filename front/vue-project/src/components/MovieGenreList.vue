<template>
    <div class="moviesgenre-portofolio section-container">
      <div class="moviesgenre-max-width max-content-container">
        <h1 class="moviesgenre-text10 thq-heading-1">
          <span class="movie-text24">{{ genreTitle }}</span>
        </h1>
        <div class="moviesgenre-tab-selector-cards-container">
          <movie-card
            v-for="movie in movies"
            :key="movie.id"
            :movie="movie"
          />
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import MovieCard from './MovieCard.vue'
  
  export default {
    name: 'MovieGenreList',
    components: {
      MovieCard
    },
    props: {
      genreTitle: {
        type: String,
        required: true
      },
      movies: {
        type: Array,
        required: true
      }
    }
  }
  </script>