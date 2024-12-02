<template>
    <div class="moviespic-speaker-card">
      <div class="moviespic-image-container">
        <img :alt="movie.title" :src="movie.poster_path" class="moviespic-image">
        <div class="moviespic-see-project-container">
          <button class="button-md button-secondary-white button" @click="goToDetail">
            <span>See movie</span>
          </button>
        </div>
      </div>
      <span class="moviespic-first-name">
        <span>{{ movie.title }}</span>
      </span>
    </div>
  </template>
  
  <script>
  export default {
    name: 'MovieCard',
    props: {
      movie: {
        type: Object,
        required: true
      }
    },
    methods: {
      goToDetail() {
        this.$router.push(`/movies/${this.movie.id}`)
      }
    }
  }
  </script>