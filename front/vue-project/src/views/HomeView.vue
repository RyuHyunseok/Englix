<template>
    <div class="page-container">

      <div class="home-container">
    <section class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">Learn English Through Movies</h1>
        <p class="hero-subtitle">Discover a new way to master English with personalized movie recommendations 
          and interactive learning experiences</p>
        <button @click="handleGetStarted" class="hero-button">
          <span>시작하기</span>
          <i class="fas fa-arrow-right"></i>
        </button>
      </div>
      <div class="hero-image-container">
        <img :src="imageUrl" alt="Movie Learning" class="hero-image" />
        <div class="image-overlay"></div>
      </div>
    </section>

    <section class="features-section">
      <h2 class="section-title">Why Englix?</h2>
      <div class="features-grid">
        <div class="feature-card">
          <div class="icon-container">
            <span class="emoji">🎯</span>  
          </div>
          <h3>Personalized Movies</h3>
          <p>Get movie recommendations tailored to your English level and learning goals</p>
        </div>
        <div class="feature-card">
          <div class="icon-container">
            <span class="emoji">📚</span>  
          </div>
          <h3>Vocabulary Building</h3>
          <p>Build your personal vocabulary list from movie contexts</p>
        </div>
        <div class="feature-card">
          <div class="icon-container">
            <span class="emoji">🎙️</span>  
          </div>
          <h3>Speech Practice</h3>
          <p>Practice pronunciation with real movie dialogues and get instant feedback</p>
        </div>
        <div class="feature-card">
          <div class="icon-container">
            <span class="emoji">👑</span>  
          </div>
          <h3>Ranking System</h3>
          <p>Track your progress and compete with others through our tier-based ranking system</p>
        </div>
      </div>
    </section>
  </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const router = useRouter();
const authStore = useAuthStore();

const imageUrl = ref("https://images.unsplash.com/photo-1705822898715-369170f541cf?ixid=M3w5MTMyMXwwfDF8c2VhcmNofDExOXx8bW92aWVzfGVufDB8fHx8MTczMTk1MDU4M3ww&ixlib=rb-4.0.3&w=1500");

onMounted(() => {
  authStore.initializeAuth();
});

const handleGetStarted = () => {
  if (authStore.isAuthenticated) {
    router.push("/survey");
  } else {
    router.push("/login");
  }
};
</script>
<style scoped>
.home-container {
  width: 100%;
  max-width: 1400px;
  margin: 0 20px;
  padding: 2rem;
}

.hero-section {
  display: flex;
  align-items: center;
  gap: 4rem;
  min-height: 80vh;
  padding: 2rem 0;
  position: relative;
}

.hero-content {
  flex: 1;
  max-width: 600px;
}

.hero-title {
  font-size: 4rem;
  font-weight: 800;
  line-height: 1.2;
  margin-bottom: 1.5rem;
  color: var(--text-color);
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.hero-subtitle {
  font-size: 1.2rem;
  line-height: 1.6;
  color: var(--text-color-secondary);
  margin-bottom: 2.5rem;
}

.hero-button {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 2rem;
  font-size: 1.1rem;
  font-weight: 600;
  background-color:sandybrown;
  background: linear-gradient(135deg);
  border: none;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.hero-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

.hero-button i {
  transition: transform 0.3s ease;
}

.hero-button:hover i {
  transform: translateX(5px);
}

.hero-image-container {
  flex: 1;
  position: relative;
  border-radius: 24px;
  overflow: hidden;
}

.hero-image {
  width: 80%;
  height: auto;
  border-radius: 30px;
  transform: scale(1.02);
  transition: transform 0.5s ease;
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: 24px;
}

.features-section {
  padding: 6rem 0;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  text-align: center;
  margin-bottom: 4rem;
  color: var(--text-color);
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  padding: 0 1rem;
  max-width: 1400px;
  margin: 0 auto;
}

.feature-card {
  background-color: var(--card-color);
  padding: 2rem;
  border-radius: 20px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  text-align: center;
}

.feature-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.1);
}

.emoji {
  font-size: 2rem;
  line-height: 1;
}

.icon-container {
  display: flex;
  align-items: center;
  justify-content: center;
}

.feature-card i {
  font-size: 2rem;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.feature-card h3 {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: var(--text-color);
}

.feature-card p {
  color: var(--text-color-secondary);
  line-height: 1.6;
}

@media (max-width: 1024px) {
  .hero-section {
    gap: 3rem;
  }

  .hero-title {
    font-size: 3.5rem;
  }
}

@media (max-width: 768px) {
  .hero-section {
    flex-direction: column;
    text-align: center;
    gap: 3rem;
  }

  .hero-content {
    max-width: 100%;
  }

  .hero-title {
    font-size: 3rem;
  }

  .hero-button {
    margin: 0 auto;
  }

  .features-grid {
    grid-template-columns: 1fr;
    max-width: 500px;
    margin: 0 auto;
  }
}

@media (max-width: 480px) {
  .hero-title {
    font-size: 2.5rem;
  }

  .hero-subtitle {
    font-size: 1rem;
  }
}

/* 다크 모드 대응 */
:root[class~="dark"] .feature-card {
  background-color: var(--dark-card);
}

:root[class~="dark"] .hero-title {
  color: rgb(255, 107, 107);
}

:root[class~="dark"] .hero-subtitle {
  color: var(--dark-text-secondary);
}

:root[class~="dark"] .section-title {
  color: var(--dark-text);
}

:root[class~="dark"] .feature-card h3 {
  color: var(--dark-text);
}

:root[class~="dark"] .feature-card p {
  color: var(--dark-text-secondary);
}

.home-container {
  width: 100%;
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 2rem;
}

.features-section {
  padding: 4rem 0;
}

.section-title {
  text-align: center;
  font-size: 2.5rem;
  color: rgb(255, 107, 107);
  margin-bottom: 3rem;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 2rem;
  padding: 0 2rem;
}

.feature-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  text-align: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.icon-container {
  width: 64px;
  height: 64px;
  background: #f8f9fa;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem;
}

.emoji {
  font-size: 2rem;
}

.feature-card h3 {
  color: #2c3e50;
  font-size: 2rem;
  margin-bottom: 1rem;
}

.feature-card p {
  color: #666;
  font-size: 1rem;
  line-height: 1.6;
}

/* 반응형 디자인 */
@media (max-width: 1200px) {
  .features-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .features-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .section-title {
    font-size: 2rem;
  }
}
/* 카드에 그라데이션 테두리 효과 추가 */
.feature-card {
  position: relative;
  background: linear-gradient(white, white) padding-box,
              linear-gradient(45deg, #ff6b6b, #ffd93d) border-box;
  border: 2px solid transparent;
}

/* 아이콘 컨테이너에 그라데이션 배경 추가 */
.icon-container {
  background: linear-gradient(135deg, #ff6b6b);
  color: white;
}

/* 부드러운 등장 애니메이션 */
.feature-card {
  animation: fadeInUp 0.6s ease-out;
  animation-fill-mode: both;
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

/* 각 카드마다 딜레이를 주어 순차적으로 등장 */
.feature-card:nth-child(1) { animation-delay: 0.1s; }
.feature-card:nth-child(2) { animation-delay: 0.2s; }
.feature-card:nth-child(3) { animation-delay: 0.3s; }
.feature-card:nth-child(4) { animation-delay: 0.4s; }

.home-container {
  width: 100%;
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 0 2rem; /* 상하 패딩 제거 */
}

.hero-section {
  min-height: 70vh; /* 100vh에서 70vh로 줄임 */
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 2rem;
  padding: 2rem 0; /* 상하 패딩 줄임 */
}

.hero-content {
  flex: 1;
  max-width: 600px;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 800;
  margin-bottom: 1rem;
  color:rgb(255, 107, 107);
}

.hero-subtitle {
  font-size: 1.2rem;
  color: #666;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.hero-button {
  padding: 1rem 2rem;
  font-size: 1.1rem;
  font-weight: 600;
  color: white;
  background: #a16363;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
}

.hero-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4);
}

.features-section {
  padding: 10rem; /* 패딩 줄임 */
  background-color: rgb(247, 238, 226);
  border-radius: 12px;
  padding: 1.5rem; /* 패딩 줄임 */
  text-align: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.section-title {
  font-size: 2.5rem;
  text-align: center;
  color: rgb(255, 107, 107);
  margin-bottom: 2rem; /* 마진 줄임 */
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem; /* 갭 줄임 */
}

.feature-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem; /* 패딩 줄임 */
  text-align: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.icon-container {
  width: 56px; /* 크기 줄임 */
  height: 56px;
  margin: 0 auto 1rem; /* 마진 줄임 */
}

/* 반응형 디자인 */
@media (max-width: 1200px) {
  .features-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .hero-section {
    flex-direction: column;
    text-align: center;
    min-height: auto;
    padding-top: 1rem;
  }

  .hero-title {
    font-size: 2.5rem;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }

  .hero-content {
    margin: 0 auto;
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
.home-container {
  animation: fadeInUp 0.6s ease-out;
}

.hero-section {
  position: relative;
  height: 80vh;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  margin-bottom: 2rem;
}

.hero-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.hero-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5); /* 배경 이미지 위에 어두운 오버레이 */
}

.hero-content {
  position: relative;
  z-index: 2;
  text-align: center;
  padding: 0 2rem;
  max-width: 800px;
}

.hero-title {
  font-size: 4rem;
  font-weight: 800;
  color: ff6b6b;
  margin-bottom: 1.5rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.hero-subtitle {
  font-size: 1.5rem;
  margin-bottom: 2.5rem;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
}

.hero-button {
  display: inline-flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 2rem;
  font-size: 1.1rem;
  font-weight: 600;
  background-color: #ff6b6b;
  color: white;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.hero-button:hover {
  transform: translateY(-2px);
  background-color: #ff5252;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }

  .hero-subtitle {
    font-size: 1.2rem;
  }
}
.features-section {
  padding: 5rem 0; /* 상하 패딩 증가 */
  margin-bottom: 5rem; /* 하단 여백 추가 */
}

.section-title {
  font-size: 3rem;
  font-weight: 700;
  text-align: center;
  color: rgb(255, 107, 107);
  margin-bottom: 5rem; /* 제목과 카드 사이 간격 증가 */
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 3rem; /* 카드 사이 간격 증가 */
  padding: 0 4rem; /* 좌우 패딩 추가 */
  max-width: 1400px;
  margin: 0 auto;
}

.feature-card {
  padding: 2rem 1rem; /* 카드 내부 패딩 증가 */
  margin-bottom: 2rem; /* 카드 아래 여백 추가 */
}

/* 모바일 반응형 조정 */
@media (max-width: 768px) {
  .features-section {
    padding: 6rem 2rem; /* 모바일에서는 패딩 줄임 */
  }

  .features-grid {
    padding: 0 1rem;
    gap: 2rem;
  }
}
.features-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr); /* 2열 그리드로 변경 */
  gap: 3rem;
  padding: 0 4rem;
  max-width: 1200px; /* 최대 너비 조정 */
  margin: 0 auto;
}



/* 모바일 반응형 */
@media (max-width: 768px) {
  .features-grid {
    grid-template-columns: 1fr; /* 모바일에서는 1열로 */
    padding: 0 2rem;
    gap: 2rem;
  }
}
</style>
