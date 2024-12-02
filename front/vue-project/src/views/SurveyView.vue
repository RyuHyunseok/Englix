<template>
  <div class="survey-container">
    <Transition name="fade" mode="out-in">
      <!-- First Section: Goal Selection -->
      <div v-if="!showSecondSection && !showThirdSection" key="goal" class="section">
        <div class="section-content">
          <h2 class="title">
            Study Goal
            <span class="subtitle">Choose your learning objective</span>
          </h2>

          <div class="goal-cards-container">
            <div class="goal-card" :class="{ active: selectedCategory === 'TOEIC' }" @click="handleFirstSelection('TOEIC')">
              <div class="card-content">
                <span class="card-icon">📚</span>
                <h3>TOEIC</h3>
              </div>
            </div>

            <div class="goal-card" :class="{ active: selectedCategory === 'SAT' }" @click="handleFirstSelection('SAT')">
              <div class="card-content">
                <span class="card-icon">🎓</span>
                <h3>SAT</h3>
              </div>
            </div>

            <div class="goal-card" :class="{ active: selectedCategory === 'BUSINESS' }" @click="handleFirstSelection('BUSINESS')">
              <div class="card-content">
                <span class="card-icon">💼</span>
                <h3>BUSINESS</h3>
              </div>
            </div>

            <div class="goal-card" :class="{ active: selectedCategory === 'DAILY' }" @click="handleFirstSelection('DAILY')">
              <div class="card-content">
                <span class="card-icon">👨‍👩‍👧‍👧</span>
                <h3>DAILY</h3>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Second Section: Level Selection -->
      <div v-else-if="showSecondSection && !showThirdSection" key="level" class="section">
        <div class="section-content">
          <h2 class="title">
            Level
            <span class="subtitle">Choose your current English level</span>
          </h2>

          <div class="level-cards-container">
            <div class="level-card" @click="handleSecondSelection('Beginner')">
              <div class="card-content">
                <span class="card-icon">🌱</span>
                <h3>Beginner</h3>
              </div>
            </div>

            <div class="level-card" @click="handleSecondSelection('Intermediate')">
              <div class="card-content">
                <span class="card-icon">🌿</span>
                <h3>Intermediate</h3>
              </div>
            </div>

            <div class="level-card" @click="handleSecondSelection('Advanced')">
              <div class="card-content">
                <span class="card-icon">🌳</span>
                <h3>Advanced</h3>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Third Section: Genre Selection -->
      <div v-else-if="showThirdSection" key="genre" class="section">
        <div class="section-content">
          <h2 class="title">
            Genre Selection
            <span class="subtitle">Choose your preferred movie genre</span>
          </h2>

          <div class="genre-cards-container">
            <div v-for="genre in genres" :key="genre.id" class="genre-card" @click="handleGenreSelection(genre.id)">
              <div class="card-content">
                <span class="card-icon">{{ genre.icon }}</span>
                <h3>{{ genre.id }}</h3>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>
<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import gridCard from "@/components/grid-card.vue";
import { useAuthStore } from "@/stores/auth";
import axios from "axios";

const router = useRouter();
const showSecondSection = ref(false);
const showThirdSection = ref(false);
const selectedCategory = ref("");
const selectedLevel = ref("");
const selectedGenre = ref("");
const authStore = useAuthStore();

// handleFirstSelection 수정
const handleFirstSelection = (category) => {
  selectedCategory.value = category;
  showSecondSection.value = true;
};

// handleSecondSelection 수정
const handleSecondSelection = (level) => {
  selectedLevel.value = level;
  showSecondSection.value = false;
  showThirdSection.value = true;
};

// handleGenreSelection 수정
const handleGenreSelection = async (genre) => {
  if (!authStore.isLogin) {
    alert("로그인이 필요한 서비스입니다.");
    router.push("/login");
    return;
  }

  try {
    const auth = localStorage.getItem("auth");
    const { token } = JSON.parse(auth);

    await axios({
      method: "put",
      url: "http://127.0.0.1:8000/accounts/preferences/",
      headers: {
        Authorization: `Token ${token}`,
        "Content-Type": "application/json",
      },
      data: {
        goal: selectedCategory.value,
        level: selectedLevel.value,
        prefer_genre: genre,
      },
    });

    router.push({
      name: "movie",
      query: {
        category: selectedCategory.value,
        level: selectedLevel.value,
        genre: genre,
      },
    });
  } catch (error) {
    console.error("Error:", error);
    if (error.response?.status === 401) {
      alert("로그인이 필요합니다.");
      router.push("/login");
    } else {
      alert("오류가 발생했습니다.");
    }
  }
};

const genres = [
  { id: "Adventure", icon: "🌎", description: "Exciting journey films" },
  { id: "Fantasy", icon: "🔮", description: "Magical and imaginative stories" },
  { id: "Animation", icon: "🎨", description: "Animated masterpieces" },
  { id: "Drama", icon: "🎭", description: "Emotional storytelling" },
  { id: "Horror", icon: "👻", description: "Thrilling scary movies" },
  { id: "Action", icon: "💥", description: "High-energy action films" },
  { id: "Comedy", icon: "😄", description: "Fun and humor" },
  { id: "History", icon: "📚", description: "Historical events" },
  { id: "Western", icon: "🤠", description: "Wild west stories" },
  { id: "Thriller", icon: "🔍", description: "Suspenseful movies" },
  { id: "Crime", icon: "🚔", description: "Crime and detective stories" },
  { id: "Science Fiction", icon: "🚀", description: "Futuristic sci-fi" },
  { id: "Mystery", icon: "🔎", description: "Mystery solving" },
  { id: "Music", icon: "🎵", description: "Musical stories" },
  { id: "Romance", icon: "💝", description: "Love stories" },
  { id: "Family", icon: "👨‍👩‍👧‍👦", description: "Family-friendly content" },
  { id: "War", icon: "⚔️", description: "War-themed movies" },
];
</script>

<style scoped>
.genre-cards-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
  padding: 20px 0;
}

.genre-card {
  background: white;
  border-radius: 12px;
  padding: 16px;
  transition: all 0.3s ease;
  border: 2px solid #e0e0e0;
  min-height: 150px;
  justify-content: center;
}

.genre-card:hover {
  transform: translateY(-5px);
  border-color: #3498db;
  box-shadow: 0 8px 24px rgba(52, 152, 219, 0.15);
}

.survey-container {
  min-height: 100vh;
  padding: 40px 20px;
  justify-content: center;
  align-items: center;
}

.section {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
}

.section-content {
  background: white;
  border-radius: 16px;
  padding: 40px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  width: 100%;
  max-width: 800px;
  opacity: 0;
  transform: translateY(20px);
  animation: fadeInUp 0.6s ease forwards;
}

.title {
  text-align: center;
  color: #ff6b6b;
  font-size: 32px;
  margin-bottom: 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.subtitle {
  font-size: 18px;
  color: #666;
  font-weight: normal;
}

.cards-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 24px;
  padding: 20px 0;
}

.goal-card,
.level-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid #e0e0e0;
  min-height: 180px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  text-align: center;
}

.goal-card:hover,
.level-card:hover {
  transform: translateY(-5px);
  border-color: #ff6b6b;
  box-shadow: 0 8px 24px rgba(52, 152, 219, 0.15);
}

.goal-card.active {
  border-color: #ff6b6b;
  background-color: #f8f9ff;
}

.card-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.card-icon {
  font-size: 40px;
  margin-bottom: 8px;
}

h3 {
  color: #2c3e50;
  font-size: 24px;
  margin: 0;
}

p {
  color: #666;
  margin: 0;
}

/* Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
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

@media (max-width: 768px) {
  .section-content {
    padding: 20px;
  }

  .title {
    font-size: 24px;
  }

  .subtitle {
    font-size: 16px;
  }

  .cards-container {
    grid-template-columns: 1fr;
  }
}

/* Goal 섹션용 그리드 (2x2) */
.goal-cards-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
}

/* Level 섹션용 그리드 (3x1) */
.level-cards-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
}

.goal-card, .level-card {
  border-radius: 12px;
  padding: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid #e0e0e0;
  min-height: 150px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .goal-cards-container, .level-cards-container {
    grid-template-columns: 1fr;
    padding: 0 20px;
  }
}
</style>
