# README

## 1. 팀원 정보 및 업무 분담 내역

---

### 김윤지

- 로그인, 로그아웃 기능
- 회원가입, 회원탈퇴 기능
- 커뮤니티 게시글, 댓글 기능
- 좋아요, 팔로우 기능
- 프로필 조회 기능
- 검색 서비스 기능

### 류현석

- 영화 데이터 저장
- 영화 목록, 상세 목록 조회
- 영화 추천 알고리즘
- AI 활용 문장 분석
- AI 활용 스피치 분석

## 2. 목표 서비스 구현 및 실제 구현 정도

---

- 목표 서비스
    - 영화 스크립트를 통한 영어공부

1. 커뮤니티
    1. 로그인
        
        ![image.png](./images/image.png)
        
    2. 게시판
        
        ![image.png](./images/image%201.png)
        
        - 글작성, 수정, 삭제

![image.png](./images/image%202.png)

![image.png](./images/image%203.png)

c. 마이페이지

![image.png](./images/image%204.png)

d. 영화 찜목록, 단어장

![image.png](./images/image%205.png)

![image.png](./images/image%206.png)

e. 회원 탈퇴

![image.png](./images/image%207.png)

1. **학습 목표 및 레벨별 맞춤 영화 추천** 
    1. 공부하고 싶은 카테고리 선택
        
        : vocabularyword 테이블에 저장된 category 를 이용해서 내가 선택한 영화의 script 중에서 내가 고른 category의 단어들이 포함된 스크립트를 추출함.
        
        ![image.png](./images/image%208.png)
        
    2. 난이도 선택
        
        : Beginner, Intermediate, Advanced
        
        ![image.png](./images/image%209.png)
        
    3. 장르 선택
        
        ![image.png](./images/image%2010.png)
        
    
    d. 설문을 바탕으로 영화 추천 목록 제공
    
    ![image.png](./images/image%2011.png)
    
2. **전체 및 장르별 영화 목록**
    
    ![image.png](./images/image%2012.png)
    

1. **영화 상세 정보 페이지**
    
    ![image.png](./images/image%2013.png)
    

1. **대사 학습 및 복습 기능**
    - 영화 대사별 학습 기능 제공 (문장 분석)
    
    ![image.png](./images/image%2014.png)
    
    - 중요 단어를 저장하고 복습할 수 있는 '단어장' 기능
        
        ![image.png](./images/image%2015.png)
        
    
    → 단어추가 기능
    
    ![image.png](./images/image%2016.png)
    
    → My Page의 단어장 탭에서 내가 저장한 단어 확인 가능
    
2. **발음 분석 기능**
    - 사용자의 발음을 녹음하고 AI로 정확도 제공
        
        ![image.png](./images/image%2017.png)
        
    - 발음 정확도별 점수 제공
        
        ![image.png](./images/image%2018.png)
        
        ![image.png](./images/image%2019.png)
        
        `일치율이 100% 이면 +5점, 100 미만 80 이상이면 +3점, 80미만 60% 이상이면 +1점 얻음.`
        

1. **학습 점수 랭킹 제공**
    - 개인별 학습 성취도 기록

![image.png](./images/image%2020.png)

## 3. ERD

---

![image.png](./images/image%2021.png)

## 4. 영화 추천 알고리즘에 대한 기술적 설명

---

**영화 추천 알고리즘**

1. 공부 목적별 ( 토익, 수능, 비지니스, 일상)
    
    : vocabularyword 테이블에 저장된 category 를 이용. 내가 선택한 영화의 전체 script 중에서 내가 고른 category의 단어들이 포함된 스크립트를 추출함.
    
    ![image.png](./images/image%2022.png)
    
2. 레벨 (초급, 중급, 고급)
    - 수준별 영화를 어떻게 분류 할 수 있을까 고민 → 영화의 각 스크립트를 Textstat 이라는 라이브러리를 이용해서 수준을 나눌 수 있겠다고 판단
        - Textstat 라이브러리(텍스트의 난이도와 가독성을 측정할 수 있는 자연어 처리 python 라이브러리)
        
        ```python
        import textstat
        
        def classify_difficulty_level(text):
            readability_score = textstat.flesch_reading_ease(text)
            word_count = len(text.split())
        
            # 짧은 문장 예외 처리
            if word_count <= 3:
                return 'Beginner'
        
            # FRE 기준 수정
            if readability_score >= 80:  # 더 쉬운 기준
                return 'Beginner'
            elif 60 <= readability_score < 80:  # 적절한 중급
                return 'Intermediate'
            else:  # 어려운 문장
                return 'Advanced'
        ```
        
        - textstat.flesch_reading_ease(text) → 점수 반환
            
            → 점수가 높을 수록 읽기 쉬움(100~90 : 초등수준, 90~70: 중등수준, 70~50:고등,대학수준, 50~0 : 대학 수준 이상)
            
        - 점수에 따라 세 단계로 난이도를 선정함
    - 모든 영화의 모든 subtitles를 대사 하나하나 textstat의 flesch_reading_ease() 함수를 수행해서 difficultylevelmovie 테이블에 각 영화의 beginner, intermediate,  advanced 대사의 개수를 저장함.(이 과정은 apps.py에서 초기 데이터를 저장할 때 수행됨)
    - <MovieDifficultyLevel 테이블>
    
    ![image.png](./images/image%2023.png)
    
    - 난이도가 Beginner 면 difficultylevelmovie 테이블 의 Beginner 를 내림차순으로 정렬해서 위에서 부터 추천
    - Intermediate면 difficultylevelmovie 테이블의 Intermediate를 내림차순으로 정렬해서 위에서 부터 추천
    - Advanced도 위와 같은 방식
    - 한계점
        - 영화 대사는 문장이 단순한 경우가 많아 대개 점수가 높아서 정확성이 높지는 않음.
        
3. 장르
    - survey.vue 페이지에서 장르까지 선택하면 accounts/preference/ url로 axios 요청을 함
    
    ```python
    # SurveyView.vue
    
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
        
        # router/index.js
            {
          path: "/movie",
          name: "movie",
          component: MovieView,
          props: (route) => ({
            category: route.query.category,
            level: route.query.level,
            genre: route.query.genre,
            prefer_genre: route.query.prefer_genre,
          }),
        }, 
    ```
    
    ⇒ MovieView.vue 페이지에 추천 알고리즘에 의해 정렬된 영화들을 보여줌
    
    ```python
    # accounts/views.py
    
    @api_view(['PUT'])
    @permission_classes([IsAuthenticated])
    def update_user_preferences(request):
        user = request.user
    
        # request.data에 있는 필드만 업데이트
        if 'goal' in request.data:
            user.goal = request.data['goal']
        if 'level' in request.data:
            user.level = request.data['level']
        if 'prefer_genre' in request.data:
            user.prefer_genre = request.data['prefer_genre']
        if 'bio' in request.data:
            user.bio = request.data['bio']
    
        user.save()
    
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    ```
    
    ⇒ SurveyVue.vue 페이지에서 사용자가 고른 3가지 정보(level, goal, prefer_genre)가 User 테이블에 업데이트됨
    

![image.png](./images/image%2024.png)

⇒ MovieView.vue 페이지에 현재 로그인한 사용자의 정보(업데이트된 level, prefer_genre)를 바탕으로 추천 영화를 보여줌

고른 장르 영화들 중에서, moviedifficultylevelmovie 테이블에서 내가 고른 난이도를 내림차순으로 보여줌(그중에 상위 3개는 1, 2, 3으로 표시됨)

![image.png](./images/image%2025.png)

![image.png](./images/image%2026.png)

## 5. 생성형 AI를 활용한 부분

---

1. 내가 공부하고자 하는 스크립트를 분석하기 위해 google의 Gemini 생성형 AI를 활용함.

![image.png](./images/image%2027.png)

![image.png](./images/image%2028.png)

1. 스크립트를 따라 녹음하면서 영어 말하기 공부를 위해 google의  speech-to-text AI를 활용함.

![image.png](./images/image%2029.png)

![image.png](./images/image%2030.png)

## 7. 기타 (느낀점, 후기 등)

---

### 류현석

- 싸피에서의 첫 프로젝트였는데 잠도 제대로 못자고 피곤했지만, 재미있는 아이디어를 하나씩 구현하면서 즐거웠습니다.
그리고 수업시간에 놓쳤던 내용들을 스스로 복습할 수 있었던 좋은 기회였습니다.

### 김윤지

- 첫 프로젝트라서 걱정이 앞섰지만 생각보다 성공적으로 마무리한 거 같아서 잠 안 자고 열심히 한 보람이 있는 거 같습니다.
    
    기획부터 설계, 구현까지 팀원과 계속해서 의논하고 의견을 맞춰나가고 하나씩 해내 가면서 열정과 의욕이 점점 커졌습니다.
    
    더 많은 기능을 구현하고 싶어 아쉬움이 남아 추후에 발전시켜보고 싶습니다.
    
    또한 구현하면서 어려웠던 점을 제대로 정리해서 다음 프로젝트에서는 아주 쉽게 해결해 나갈 수 있도록 하고 싶습니다.