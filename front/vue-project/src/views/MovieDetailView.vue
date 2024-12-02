<template>
    <div class="page-container">

  <div v-if="movieDetail" class="movie-detail-container">
    <!-- 헤더 섹션: 영화 기본 정보 -->
    <div class="movie-header">
      <div class="movie-basic-info">
        <img :src="movieDetail.poster_path" :alt="movieDetail.title" class="movie-poster" />
        <div class="movie-info">
          <h1 class="movie-title">{{ movieDetail.title }}</h1>
          <p class="release-date">개봉일: {{ movieDetail.release_date }}</p>
          <p class="overview">{{ movieDetail.overview }}</p>

          <div class="action-buttons">
            <!-- 찜하기 버튼에 팝업 메시지 추가 -->
            <!-- 찜하기 버튼 -->
            <button @click="toggleFavorite" class="favorite-btn" :class="{ 'is-favorite': isFavorite }">
              <span class="star-icon">★</span>
              {{ isFavorite ? "Remove from Favorites" : "Add to Favorites" }}
              <span class="popup-message" :class="{ show: showFavPopup }">
                {{ favPopupMessage }}
                <span class="popup-emoji">{{ isFavorite ? "💖" : "💔" }}</span>
              </span>
            </button>

   <!-- 영화 세부 정보 토글 버튼 -->
   <button @click="toggleMovieDetails" class="details-btn">
     {{ showDetails ? 'Hide Details ▲' : 'Show Details ▼' }}
   </button>

            <!-- 예고편 버튼 -->
            <button @click="toggleTrailer" class="trailer-btn">
              <span class="play-icon">{{ showTrailer ? "✕" : "▶" }}</span>
              {{ showTrailer ? "Close Trailer" : "Watch Trailer" }}
            </button>
          </div>
        </div>
      </div>

 <!-- 영화 세부 정보 섹션 -->
 <div v-if="showDetails" class="movie-details-section">
   <div class="details-grid">
     <div class="detail-item">
       <span class="detail-label">Director</span>
       <span class="detail-value">{{ movieDetail.director }}</span>
     </div>
     <div class="detail-item">
       <span class="detail-label">Runtime</span>
       <span class="detail-value">{{ movieDetail.runtime }} minutes</span>
     </div>
     <div class="detail-item">
       <span class="detail-label">Rating</span>
       <span class="detail-badge">{{ convertedRating }}</span>
     </div>
   </div>
   <div class="cast-section">
     <span class="detail-label">Cast</span>
     <div class="cast-members">
       <div v-for="actor in movieDetail.cast" :key="actor.name" class="cast-member">
         <span class="actor-name">{{ actor.name }}</span>
         <span class="actor-character">as {{ actor.character }}</span>
       </div>
     </div>
   </div>
 </div>


      <!-- 트레일러 섹션 (토글) -->
      <div v-if="showTrailer" class="trailer-section">
        <iframe
          width="100%"
          height="500"
          :src="`https://www.youtube.com/embed/${movieDetail.youtube_trailer_id}`"
          frameborder="0"
          allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
          allowfullscreen
        ></iframe>
      </div>
    </div>

    <!-- 스크립트 분석 섹션 -->
    <div class="script-analysis-section">
      <h2 class="section-title">Script Analysis</h2>
      <div class="scripts-container">
        <div v-for="(data, script) in paginatedScripts" :key="script" class="script-card">
          <div class="script-header" @click="handleScriptClick($event, script, data)">
            <div class="script-content">
              <p class="script-text">{{ script }}</p>
              <span class="timestamp">Time: {{ data.timestamp }}</span>
            </div>

            <transition name="badge-fade">
     <!-- 100 퍼센트 일 때 -->
     <span v-if="data.highest_match_rate === 100" class="achievement-badge gold">
       <i class="fas fa-trophy"></i> Perfect! (5 points)
     </span>
     <!-- 80퍼 이상 -->
     <span v-else-if="data.highest_match_rate >= 80" class="achievement-badge silver">
       <i class="fas fa-award"></i> Great! (3 points)
     </span>
     <!-- 60퍼 이상 -->
     <span v-else-if="data.highest_match_rate >= 60" class="achievement-badge bronze">
       <i class="fas fa-award"></i> Good! (1 points)
     </span>
   </transition>
          </div>

          <div class="word-list">
            <h4 class="word-list-title">Key Words</h4>
            <div class="words">
              <!-- 단어 버튼 -->
              <button v-for="word in data.words" :key="word.id" @click="addToFavoriteVoca(word.id)" class="word-chip">
                {{ word.word }}
                <span class="popup-message" :class="{ show: wordPopups[word.id] }">
                  {{ wordPopupMessages[word.id] }}
                  <span class="popup-emoji">{{ wordPopupEmojis[word.id] }}</span>
                </span>
              </button>
            </div>
          </div>

<!-- 녹음 영역 -->
<div class="recording-section">
  <div class="record-area">
    <h4>Speech Practice</h4>
    <div class="controls">
      <button 
        @click="toggleRecording(script, data.script_id)" 
        :class="{ 'recording': isRecording[script] }"
        class="record-button"
      >
        <span class="record-icon">🎤</span>
        {{ isRecording[script] ? 'Stop Recording' : 'Start Recording' }}
      </button>
      
      <div v-if="recordedAudio[script]" class="audio-controls">
        <audio :src="recordedAudio[script]?.url" controls></audio>
        <button 
          @click="convertToText(script, data.script_id)" 
          :disabled="isConverting[script]"
          class="submit-button"
        >
          Check Pronunciation
        </button>
      </div>
    </div>

    <!-- 결과 표시 -->
    <div v-if="practiceResults[script]" class="result-section">
      <div class="result-header">
        <h4>Your Result:</h4>
        <div class="badges">
          <span 
            class="match-badge"
            :class="getMatchRateClass(practiceResults[script].match_rate)"
          >
            {{ practiceResults[script].match_rate.toFixed(2) }}% Match
          </span>
          <span v-if="practiceResults[script].is_new_record" class="new-record-badge">
            You've gained {{ practiceResults[script].points }} points!
          </span>
        </div>
      </div>
      <div class="speech-comparison">
        <div class="original-text">
          <p class="label">Original:</p>
          <p class="text">{{ script }}</p>
        </div>
        <div class="your-speech">
          <p class="label">Your Speech:</p>
          <p class="text">{{ practiceResults[script].text }}</p>
        </div>
      </div>
    </div>
  </div>
</div>

          <!-- gpt 결과 -->
          <div class="gpt-output" :class="{ active: gptOutputDisplay[script] }" v-show="gptOutputDisplay[script]">
            <div class="loading" v-if="loadingDisplay[script]">
              <div class="loading-spinner"></div>
              Analyzing...
            </div>
            <div class="content" :data-content="`content-${script.replace(/\s+/g, '-')}`"></div>
          </div>
        </div>

        <!-- 페이지네이션 -->
        <div class="pagination">
          <button @click="handlePrevGroup" :disabled="currentPageGroup === 1" class="pagination-btn">Previous</button>
          <div class="page-numbers">
            <button v-for="pageNum in displayedPages" :key="pageNum" @click="currentPage = pageNum" class="page-number" :class="{ active: currentPage === pageNum }">
              {{ pageNum }}
            </button>
          </div>
          <button @click="handleNextGroup" :disabled="currentPageGroup >= maxPageGroup" class="pagination-btn">Next</button>
        </div>
      </div>
    </div>
  </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";
import { useAuthStore } from "@/stores/auth";
import { storeToRefs } from "pinia";
// 페이지네이션 상태
const currentPage = ref(1);
const itemsPerPage = 5;
const pagesPerGroup = 5;

// 찜하기 관련 상태
const showFavPopup = ref(false);
const favPopupMessage = ref("");

// 단어장 관련 상태
const wordPopups = ref({});
const wordPopupMessages = ref({});
const wordPopupEmojis = ref({});

const showTrailer = ref(false);
const route = useRoute();
const movieDetail = ref(null);
const analyzedScripts = ref({});
const gptOutputDisplay = ref({});
const loadingDisplay = ref({});
const words = ref([]);
const showDetails = ref(false)

const authStore = useAuthStore();
const isFavorite = ref(false);
const { token, isLogin } = storeToRefs(authStore);

// 녹음관련 상태
const isRecording = ref({});
const recordedAudio = ref({});
const practiceResults = ref({});
const mediaRecorder = ref(null);
const isConverting = ref({});

// 상세 정보 토글 함수
const toggleMovieDetails = () => {
  showDetails.value = !showDetails.value;
};

// 영화 등급
const convertedRating = computed(() => {
  const usRating = movieDetail.value?.rating?.toUpperCase();
  
  switch (usRating) {
    case 'G':
      return '전체 관람가'
    case 'PG':
    case 'PG-13':
      return '12세 이상 관람가'
    case 'R':
      return '15세 이상 관람가'
    case 'NC-17':
      return '청소년 관람불가'
    case 'NR':
    case 'UNRATED':
      return '미분류'
    default:
      return '등급 정보 없음'
  }
})


// 녹음 토글 함수
const toggleRecording = async (script, scriptId) => {
  if (isRecording.value[script]) {
    stopRecording(script);
  } else {
    startRecording(script);
  }
};

// 녹음 시작 함수
const startRecording = async (script) => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ 
      audio: {
        sampleRate: 48000,
        channelCount: 1,
        echoCancellation: true,
        noiseSuppression: true,
      }
    });
    
    mediaRecorder.value = new MediaRecorder(stream, {
      mimeType: 'audio/webm;codecs=opus'
    });
    
    const chunks = [];

    mediaRecorder.value.ondataavailable = (e) => {
      if (e.data.size > 0) chunks.push(e.data);
    };

    mediaRecorder.value.onstop = () => {
      const blob = new Blob(chunks, { type: 'audio/webm' });
      recordedAudio.value[script] = {
        url: URL.createObjectURL(blob),
        blob: blob
      };
      stream.getTracks().forEach(track => track.stop());
    };

    mediaRecorder.value.start();
    isRecording.value[script] = true;
  } catch (err) {
    console.error('Error accessing microphone:', err);
    alert('마이크 접근 권한이 필요합니다.');
  }
};

// 녹음 중지 함수
const stopRecording = (script) => {
  if (mediaRecorder.value?.state === 'recording') {
    mediaRecorder.value.stop();
    isRecording.value[script] = false;
  }
};

// 텍스트 변환 함수
const convertToText = async (script, scriptId) => {
  try {
    isConverting.value[script] = true;
    const audioData = recordedAudio.value[script];

    if (!audioData?.blob) {
      throw new Error('녹음된 오디오가 없습니다.');
    }

    const formData = new FormData();
    formData.append('audio', audioData.blob, 'recording.webm');
    formData.append('original_script', script);
    formData.append('script_id', scriptId);

    const auth = JSON.parse(localStorage.getItem("auth"));
    const response = await axios.post(
      'http://localhost:8000/movie/convert-speech/',
      formData,
      {
        headers: {
          Authorization: `Token ${auth.token}`,
          'Content-Type': 'multipart/form-data',
        }
      }
    );

    practiceResults.value[script] = {
      text: response.data.text,
      match_rate: response.data.match_rate,
      is_new_record: response.data.is_new_record,
      points: response.data.points
    };
        // 새로운 최고 기록일 경우 highest_match_rate 업데이트
    if (paginatedScripts.value[script] && response.data.is_new_record) {
      paginatedScripts.value[script].highest_match_rate = response.data.match_rate;
    }

  } catch (error) {
    console.error('STT conversion error:', error);
    alert(error.message || '음성 변환 중 오류가 발생했습니다.');
  } finally {
    isConverting.value[script] = false;
  }
};

// 일치율에 따른 클래스 반환
const getMatchRateClass = (rate) => {
  if (rate >= 90) return 'excellent';
  if (rate >= 70) return 'good';
  return 'needs-improvement';
};


const toggleTrailer = () => {
  showTrailer.value = !showTrailer.value;
};

const props = defineProps({
  movieId: String,
  movieTitle: String,
});

// 디버깅을 위해 props 값 확인
console.log("Props:", props.movieId, props.movieTitle);


// 전체 페이지 수 계산
const totalPages = computed(() => {
  if (!movieDetail.value?.filtered_scripts) return 1;
  return Math.ceil(Object.keys(movieDetail.value.filtered_scripts).length / itemsPerPage);
});

// 현재 페이지 그룹
const currentPageGroup = computed(() => {
  return Math.ceil(currentPage.value / pagesPerGroup);
});

// 최대 페이지 그룹
const maxPageGroup = computed(() => {
  return Math.ceil(totalPages.value / pagesPerGroup);
});

// 화면에 표시할 페이지 번호들
const displayedPages = computed(() => {
  const start = (currentPageGroup.value - 1) * pagesPerGroup + 1;
  const end = Math.min(start + pagesPerGroup - 1, totalPages.value);
  return Array.from({ length: end - start + 1 }, (_, i) => start + i);
});

// 현재 페이지에 표시할 스크립트들
const paginatedScripts = computed(() => {
  if (!movieDetail.value?.filtered_scripts) return {};

  const scripts = Object.entries(movieDetail.value.filtered_scripts);
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;

  return Object.fromEntries(scripts.slice(start, end));
});

// 이전 그룹으로 이동
const handlePrevGroup = () => {
  const newPage = Math.max(1, (currentPageGroup.value - 1) * pagesPerGroup);
  currentPage.value = newPage;
};

// 다음 그룹으로 이동
const handleNextGroup = () => {
  const newPage = Math.min(totalPages.value, currentPageGroup.value * pagesPerGroup + 1);
  currentPage.value = newPage;
};
const typeText = (element, text, speed = 25) => {
  let index = 0;
  element.innerHTML = "";

  const addChar = () => {
    if (index < text.length) {
      if (text.slice(index).startsWith("\n")) {
        element.innerHTML += "<br>";
        index++;
      } else {
        // HTML 태그 처리
        if (text.slice(index).startsWith("<")) {
          const closingIndex = text.indexOf(">", index) + 1;
          if (closingIndex > index) {
            element.innerHTML += text.slice(index, closingIndex);
            index = closingIndex;
            setTimeout(addChar, 0); // 태그는 즉시 추가
            return;
          }
        }
        element.innerHTML += text[index];
        index++;
      }
      setTimeout(addChar, speed);
    }
  };

  addChar();
};

// 단어 추가 함수
const addToFavoriteVoca = async (wordId) => {
  const auth = JSON.parse(localStorage.getItem("auth"));
  const token = auth?.token;

  if (!token) {
    alert("로그인이 필요합니다.");
    return;
  }

  try {
    const response = await axios({
      method: "post",
      url: "http://localhost:8000/movie/add_to_favorite_voca/",
      data: { word_id: wordId },
      headers: {
        Authorization: `Token ${token}`,
        "Content-Type": "application/json",
      },
    });

    // 응답에 따라 다른 메시지와 이모지 설정
    wordPopupMessages.value[wordId] = response.data.message === "이미 추가된 단어입니다." ? "Already in vocabulary!" : "Added to vocabulary!";
    wordPopupEmojis.value[wordId] = response.data.message === "이미 추가된 단어입니다." ? "📝" : "✨";

    // 팝업 표시 및 자동 숨김
    wordPopups.value[wordId] = true;
    setTimeout(() => {
      wordPopups.value[wordId] = false;
    }, 2000);
  } catch (error) {
    console.error("Error:", error);
  }
};
const handleScriptClick = async (event, script, data) => {
  if (analyzedScripts.value[script]) {
    gptOutputDisplay.value[script] = !gptOutputDisplay.value[script];
    return;
  }

  gptOutputDisplay.value[script] = true;
  loadingDisplay.value[script] = true;

  try {
    const auth = JSON.parse(localStorage.getItem("auth"));
    const token = auth?.token;

    const response = await axios.post(
      "http://localhost:8000/movie/analyze_script/",
      {
        script: script,
        words: data.words,
      },
      {
        headers: {
          Authorization: `Token ${token}`,
        },
      }
    );

    // ref를 사용하여 DOM 요소 접근 방식 수정
    const contentKey = `content-${script.replace(/\s+/g, "-")}`;
    const contentElement = document.querySelector(`[data-content="${contentKey}"]`);

    if (contentElement) {
      // 타이핑 효과 적용
      typeText(contentElement, response.data.response);
      analyzedScripts.value[script] = true;
    }
  } catch (error) {
    console.error("Analysis error:", error);
    const contentKey = `content-${script.replace(/\s+/g, "-")}`;
    const contentElement = document.querySelector(`[data-content="${contentKey}"]`);
    if (contentElement) {
      contentElement.innerHTML = '<p class="error">분석 중 오류가 발생했습니다.</p>';
    }
  } finally {
    loadingDisplay.value[script] = false;
  }
};

const getCookie = (name) => {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
};

const fetchMovieDetail = async () => {
  try {
    const tmdbId = route.params.tmdbId;
    const category = route.query.category;

    const auth = JSON.parse(localStorage.getItem("auth"));
    const token = auth?.token;

    const response = await axios.get(`http://localhost:8000/movie/movie_detail/${tmdbId}/`, {
      headers: {
        Authorization: `Token ${token}`,
      },
      params: {
        category: category,
      },
    });
    movieDetail.value = response.data;
  } catch (error) {
    console.error("Error fetching movie details:", error);
  }
};

// 찜하기 토글 함수 수정
const toggleFavorite = async () => {
  try {
    const auth = JSON.parse(localStorage.getItem("auth"));
    if (!auth?.token) {
      alert("로그인이 필요합니다.");
      return;
    }

    const response = await axios.get(`http://localhost:8000/movie/favorites/status/${movieDetail.value.tmdb_id}/`, { headers: { Authorization: `Token ${auth.token}` } });

    if (response.data.is_favorited) {
      await axios.delete(`http://localhost:8000/movie/favorites/${movieDetail.value.tmdb_id}/`, { headers: { Authorization: `Token ${auth.token}` } });
      isFavorite.value = false;
      favPopupMessage.value = "Removed from favorites!";
    } else {
      await axios.post(
        "http://localhost:8000/movie/favorites/",
        {
          movie_tmdb_id: movieDetail.value.tmdb_id,
          movie_title: movieDetail.value.title,
        },
        { headers: { Authorization: `Token ${auth.token}` } }
      );
      isFavorite.value = true;
      favPopupMessage.value = "Added to favorites!";
    }

    // 팝업 표시 및 자동 숨김
    showFavPopup.value = true;
    setTimeout(() => {
      showFavPopup.value = false;
    }, 2000);
  } catch (error) {
    console.error("Error:", error);
  }
};

const checkFavoriteStatus = async () => {
  try {
    const auth = JSON.parse(localStorage.getItem("auth"));
    if (!movieDetail.value?.tmdb_id || !auth?.token) return;

    const response = await axios.get(`http://localhost:8000/movie/favorites/status/${movieDetail.value.tmdb_id}/`, { headers: { Authorization: `Token ${auth.token}` } });
    isFavorite.value = response.data.is_favorited;
  } catch (error) {
    console.error("Error checking favorite status:", error);
  }
};
onMounted(async () => {
  await fetchMovieDetail();
  if (movieDetail.value) {
    checkFavoriteStatus();
  }

});
</script>

<style scoped>

.details-btn {
  padding: 10px 20px;
  border-radius: 8px;
  border: 2px solid #ff6b6b;
  background: white;
  color: #ff6b6b;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.details-btn:hover {
  background: #ff6b6b;
  color: white;
}

.movie-details-section {
  margin-top: 20px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 12px;
  animation: slideDown 0.3s ease;
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.detail-label {
  font-weight: 600;
  color: #64748b;
}

.detail-value {
  font-size: 16px;
  color: #334155;
}

.detail-badge {
  align-self: flex-start;
  background: #e3f2fd;
  color: #ff6b6b;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
}

.cast-section {
  margin-top: 20px;
}

.cast-members {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 12px;
  margin-top: 10px;
}

.cast-member {
  background: white;
  padding: 12px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.actor-name {
  font-weight: 600;
  color: #334155;
}

.actor-character {
  font-size: 14px;
  color: #64748b;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 768px) {
  .action-buttons {
    flex-wrap: wrap;
  }
  
  .details-grid {
    grid-template-columns: 1fr;
  }
}

/* ======================== */

.recording-section {
  margin-top: 20px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 12px;
}

.record-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  background: #ff6b6b;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.record-button.recording {
  background: #e74c3c;
  animation: pulse 2s infinite;
}

.audio-controls {
  margin-top: 15px;
  display: flex;
  gap: 10px;
  align-items: center;
}

.submit-button {
  padding: 8px 16px;
  border: none;
  border-radius: 8px;
  background: #2ecc71;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.submit-button:disabled {
  background: #95a5a6;
  cursor: not-allowed;
}

.result-section {
  margin-top: 20px;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.badges {
  display: flex;
  gap: 10px;
}

.match-badge {
  padding: 6px 12px;
  border-radius: 20px;
  font-weight: 600;
}

.match-badge.excellent {
  background: #e3fcef;
  color: #0f766e;
}

.match-badge.good {
  background: #e3f2fd;
  color: #ff6b6b;
}

.match-badge.needs-improvement {
  background: #fff3cd;
  color: #997404;
}

.new-record-badge {
  padding: 6px 12px;
  border-radius: 20px;
  background: #fdf2f8;
  color: #be185d;
  font-weight: 600;
}

.speech-comparison {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.label {
  font-weight: 600;
  color: #64748b;
  margin-bottom: 5px;
}

.text {
  padding: 10px;
  background: #f8fafc;
  border-radius: 6px;
  color: #334155;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.6; }
  100% { opacity: 1; }
}
/* =============================== */

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-top: 30px;
  padding: 20px 0;
}

.page-numbers {
  display: flex;
  gap: 10px;
}

.page-number {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
  background: white;
  color: #2c3e50;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.page-number.active {
  background: #ff6b6b;
  color: white;
  border-color: #ff6b6b;
}

.page-number:hover:not(.active) {
  background: #f8f9fa;
  transform: translateY(-2px);
}

.pagination-btn {
  padding: 8px 16px;
  border-radius: 8px;
  background: #ff6b6b;
  color: white;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
}

.pagination-btn:disabled {
  background: #95a5a6;
  cursor: not-allowed;
}

.pagination-btn:not(:disabled):hover {
  background: #ff6b6b;
  transform: translateY(-2px);
}

/* ================================== */

.popup-message {
  position: absolute;
  top: -40px;
  left: 50%;
  transform: translateX(-50%) translateY(10px);
  background: white;
  padding: 8px 16px;
  border-radius: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  font-size: 14px;
  color: #2c3e50;
  pointer-events: none;
  opacity: 0;
  transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  white-space: nowrap;
  display: flex;
  align-items: center;
  gap: 6px;
  border: 2px solid #e8f5fe;
}

/* 팝업 화살표 */
.popup-message::after {
  content: "";
  position: absolute;
  bottom: -8px;
  left: 50%;
  transform: translateX(-50%);
  border-width: 8px 8px 0 8px;
  border-style: solid;
  border-color: white transparent transparent transparent;
}

/* 팝업 표시 애니메이션 */
.popup-message.show {
  opacity: 1;
  transform: translateX(-50%) translateY(0);
}

/* 팝업 이모지 스타일 */
.popup-emoji {
  font-size: 16px;
  line-height: 1;
}

/* 버튼 관련 스타일 수정 */
.favorite-btn,
.word-chip {
  position: relative;
}

/* 호버 효과 개선 */
.favorite-btn:hover,
.word-chip:hover {
  transform: translateY(-2px);
}

/* 버튼 클릭 효과 */
.favorite-btn:active,
.word-chip:active {
  transform: translateY(0);
}

/* 반응형 조정 */
@media (max-width: 768px) {
  .popup-message {
    font-size: 12px;
    padding: 6px 12px;
  }
}

.movie-detail-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 80%;
  padding: 0 50px;
}

.movie-header {
  background: white;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 30px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  max-width: 2000px;
  width: 100%;
}

.movie-basic-info {
  display: flex;
  gap: 30px;
}

.movie-poster {
  width: 200px;
  height: 300px;
  object-fit: cover;
  border-radius: 8px;
}

.movie-info {
  flex: 1;
}

.movie-title {
  font-size: 28px;
  color: #2c3e50;
  margin-bottom: 10px;
}

.release-date {
  color: #666;
  margin-bottom: 10px;
}

.overview {
  color: #2c3e50;
  line-height: 1.6;
  margin-bottom: 20px;
}

.action-buttons {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.favorite-btn,
.trailer-btn {
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.favorite-btn {
  border: 2px solid #ffd700;
  background: white;
}

.favorite-btn.is-favorite {
  background: #ffd700;
  color: white;
}

.trailer-btn {
  background: #ff6b6b;
  color: white;
  border: none;
}

.trailer-btn:hover {
  background: #ff6b6b;
}

.trailer-section {
  margin-top: 20px;
}

.script-analysis-section {
  background: white;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  max-width: 2000px;
  width: 100%;
}

.section-title {
  font-size: 24px;
  color: #2c3e50;
  margin-bottom: 20px;
  padding-left: 20px;
  border-left: 4px solid #ff6b6b;
}

.script-card {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  transition: all 0.3s ease;
  position: relative;
}

.script-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.script-text {
 flex: 1;
 margin: 0;
}

.achievement-badge {
  position: absolute;
  top: 0;
  right: 10px;
  display: inline-flex;
  align-items: center;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.9em;
  font-weight: bold;
  white-space: nowrap;
  z-index: 2;
}

.achievement-badge.gold {
 background-color: #FFD700;
 color: #2C3E50;
 box-shadow: 0 2px 4px rgba(255, 215, 0, 0.3);
}

.achievement-badge.silver {
 background-color: #C0C0C0;
 color: #2C3E50;
 box-shadow: 0 2px 4px rgba(192, 192, 192, 0.3);
}

.achievement-badge.bronze {
 background-color: #CD7F32;
 color: #FFFFFF;
 box-shadow: 0 2px 4px rgba(205, 127, 50, 0.3);
}

.achievement-badge i {
 margin-right: 6px;
}

/* 동적 생성을 위한 트랜지션 효과 */
.badge-fade-enter-active {
 transition: all 0.3s ease-out;
}

.badge-fade-leave-active {
 transition: all 0.3s ease-in;
}

.badge-fade-enter-from,
.badge-fade-leave-to {
 opacity: 0;
 transform: translateX(20px);
}

/* 스크립트 카드 호버 효과에서도 뱃지가 잘 보이도록 */
.script-card:hover .achievement-badge {
 z-index: 2;
}

.script-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.script-header {
  position: relative;
  margin-bottom: 15px;
}

/* script 부분 */
.script-text {
 font-size: 18px;
 color: #2c3e50;
 line-height: 1.8;
 margin-right: 120px;
 position: relative;
 cursor: pointer;
 transition: all 0.3s ease;
 padding: 4px 8px;
 display: inline-block;  /* 텍스트 크기만큼만 차지하도록 변경 */
}

/* 심플한 hover 효과 */
.script-text:hover {
 color: #ff6b6b;  /* 메인 컬러로 변경 */
 transform: translateX(4px);  /* 살짝 오른쪽으로 이동 */
}

/* 클릭 효과 */
.script-text:active {
 transform: translateX(2px);  /* 클릭시 살짝 덜 이동 */
}


/* ============== */

.timestamp {
  color: #666;
  font-size: 14px;
}

.word-list {
  margin: 15px 0;
}

.words {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 10px;
}

.word-chip {
  background: #e3f2fd;
  color: #ff6b6b;
  padding: 5px 12px;
  border-radius: 15px;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
}

.word-chip:hover {
  background: #ff6b6b;
  color: white;
}

.gpt-output {
  background: white;
  border-radius: 8px;
  padding: 20px;
  margin-top: 15px;
  border: 1px solid #e0e0e0;
}

.loading {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #666;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid #f3f3f3;
  border-top: 2px solid #ff6b6b;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

@media (max-width: 768px) {
  .movie-basic-info {
    flex-direction: column;
  }

  .movie-poster {
    width: 100%;
    height: auto;
    max-width: 300px;
    margin: 0 auto;
  }
}
.movie-detail-container {
  max-width: 1200px;
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
  margin: 0 auto;
}

/* 헤더 섹션 */
.movie-header {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
}

.movie-basic-info {
  display: flex;
  gap: 2rem;
}

.movie-poster {
  width: 200px;
  height: auto;
  object-fit: cover;
  border-radius: 8px;
}

.movie-info {
  flex: 1;
}

.movie-title {
  font-size: 2rem;
  color: #2c3e50;
  margin-bottom: 1rem;
}

.release-date {
  color: #666;
  margin-bottom: 1rem;
}

.overview {
  color: #2c3e50;
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.favorite-btn,
.trailer-btn,
.details-btn {
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 500;
}

.favorite-btn {
  border: 2px solid #ffd700;
  background: white;
  color: #ffd700;
}

.favorite-btn.is-favorite {
  background: #ffd700;
  color: white;
}

.trailer-btn {
  background: #ff6b6b;
  color: white;
  border: none;
}

.details-btn {
  border: 2px solid #ff6b6b;
  background: white;
  color: #ff6b6b;
}

.trailer-btn:hover,
.details-btn:hover {
  background: #ff8585;
  color: white;
  border-color: #ff8585;
}

/* 영화 세부 정보 섹션 */
.movie-details-section {
  margin-top: 1.5rem;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 12px;
  width: 96%;
  animation: fadeIn 0.5s ease-out;
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.detail-label {
  font-weight: 600;
  color: #64748b;
}

.detail-value {
  font-size: 1rem;
  color: #334155;
}

.detail-badge {
  align-self: flex-start;
  background: #e3f2fd;
  color: #ff6b6b;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 600;
}

.cast-section {
  margin-top: 1.5rem;
}

.cast-members {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.cast-member {
  background: white;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.actor-name {
  font-weight: 600;
  color: #334155;
}

.actor-character {
  font-size: 0.875rem;
  color: #64748b;
}

/* 스크립트 분석 섹션 */
.script-analysis-section {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  margin-top: 2rem;
}

.section-title {
  font-size: 1.5rem;
  color: #2c3e50;
  margin-bottom: 1.5rem;
  padding-left: 1rem;
  border-left: 4px solid #ff6b6b;
}

/* ... 나머지 스타일 ... */

/* 반응형 디자인 */
@media (max-width: 768px) {
  .movie-detail-container {
    padding: 1rem;
  }

  .movie-header,
  .script-analysis-section {
    padding: 1.5rem;
  }

  .movie-basic-info {
    flex-direction: column;
    gap: 1.5rem;
  }

  .movie-poster {
    width: 100%;
    max-width: 300px;
    margin: 0 auto;
  }

  .action-buttons {
    justify-content: center;
  }
}

/* 애니메이션 */
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

.movie-detail-container {
  animation: fadeIn 0.6s ease-out;
}

.movie-header {
  animation: fadeIn 0.6s ease-out 0.2s;
  animation-fill-mode: both;
}

.script-analysis-section {
  animation: fadeIn 0.6s ease-out 0.4s;
  animation-fill-mode: both;
}


</style>
