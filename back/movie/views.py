import os
from .models import UserScriptProgress
from google.api_core.exceptions import GoogleAPICallError, InvalidArgument
from google.cloud import speech_v1p1beta1 as speech
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from collections import OrderedDict
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import MovieSerializer, GenreSerializer, ScriptSerializer
from accounts.models import User

from django.http import JsonResponse
from django.conf import settings
import google.generativeai as genai
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import textstat
from .models import DifficultyLevelMovie, FavoriteWord, Script, VocabularyWord, FavoriteMovie
from django.core.cache import cache
from multiprocessing import context
import requests
from django.shortcuts import render, get_object_or_404

from englix_pjt import settings
from django.http import JsonResponse, HttpResponse
import re
from pprint import pprint
from .models import Movie, Script, VocabularyWord, Genre

from django.db.models import Q


# Create your views here.
# def index(request):


#     return render(request, 'movie/index.html')

@api_view(['GET'])
def movie_list(request):
    tmdb_api_key = settings.TMDB_API_KEY
    url = "https://api.themoviedb.org/3/discover/movie"  # 인기 영화 엔드포인트
    movies = []  # 결과를 저장할 리스트
    pages_to_fetch = 3  # 총 3페이지 가져오기

    # 필터링할 국가 코드
    allowed_countries = {'US', 'GB', 'AU'}

    for page in range(1, pages_to_fetch + 1):
        params = {
            'api_key': tmdb_api_key,
            'language': 'ko-KR',
            'page': page,
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            movies_data = response.json().get('results', [])
            for movie_data in movies_data:

                tmdb_id = movie_data['id']
                genres = movie_data.get('genre_ids', [])

                # DB에 tmdb_id가 있는지 확인하고 없으면 새로 저장
                movie, created = Movie.objects.get_or_create(
                    tmdb_id=tmdb_id,
                    defaults={
                        'title': movie_data['title'],
                        'poster_path': f"https://image.tmdb.org/t/p/w300{movie_data['poster_path']}",
                        'overview': movie_data['overview'],
                        'release_date': movie_data['release_date'],
                    }
                )

                # 장르 추가
                for genre_id in genres:
                    genre = Genre.objects.filter(id=genre_id).first()
                    if genre:
                        movie.genres.add(genre)

                movies.append(movie)
        else:
            return Response(
                {"error": f"Failed to fetch page {page}: {response.status_code}"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

    # 시리얼라이저로 변환
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


def get_or_save_filtered_scripts(tmdb_id, category, user):
    # 캐시 키 생성
    cache_key = f"filtered_scripts_{tmdb_id}_{category}"

    # 캐시에서 필터링된 대사 가져오기
    filtered_scripts = cache.get(cache_key)

    if filtered_scripts is None:
        # 필터링된 대사가 캐시에 없다면 필터링 수행
        vocabulary_words = VocabularyWord.objects.filter(category=category)

        # 단어와 그 ID를 매핑한 딕셔너리 생성
        vocabulary_map = {vocabulary_word.word.lower(
        ): vocabulary_word.id for vocabulary_word in vocabulary_words}

        # tmdb_id에 해당하는 영화 대사 필터링
        scripts = Script.objects.filter(movie__tmdb_id=tmdb_id)

        filtered_scripts = {}

        # 각 대사에 대해 사용된 단어와 timestamp를 함께 저장
        for script in scripts:
            # 대사에서 단어를 추출하여 소문자 변환 후 필터링
            words_in_script = set(script.text.lower().split())
            intersecting_words = words_in_script.intersection(
                vocabulary_map.keys())
            intersecting_words.discard('to')

            if intersecting_words:

                # 사용자의 progress 정보 가져오기
                progress = UserScriptProgress.objects.filter(
                    user=user,
                    script_id=script.id
                ).first()

                # 해당 대사와 timestamp, 사용된 단어 ID를 저장
                filtered_scripts[script.text] = {
                    'script_id': script.id,
                    'timestamp': script.timestamp,
                    'words': [{'word': word, 'id': vocabulary_map[word]} for word in intersecting_words],
                    'highest_match_rate': progress.highest_match_rate if progress else 0
                }

        # 필터링된 결과를 캐시에 저장  (24시간 유효)
        cache.set(cache_key, filtered_scripts, timeout=60 * 60 * 24)
        print("캐시에 저장되었습니다.")
    else:
        # 캐시된 데이터에 사용자의 progress 정보 추가
        for script_text, script_data in filtered_scripts.items():
            progress = UserScriptProgress.objects.filter(
                user=user,
                script_id=script_data['script_id']
            ).first()
            script_data['highest_match_rate'] = progress.highest_match_rate if progress else 0

        print("캐시에서 데이터를 가져왔습니다.")

    return filtered_scripts


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def movie_detail(request, tmdb_id):
    tmdb_api_key = settings.TMDB_API_KEY
    base_url = "https://api.themoviedb.org/3"

    # 기본 영화 정보 가져오기
    params = {
        'api_key': tmdb_api_key,
        'language': 'ko-KR',
        'append_to_response': 'credits,release_dates'
    }

    # 영화 상세 정보 요청
    response = requests.get(f"{base_url}/movie/{tmdb_id}", params=params)
    movie_data = response.json()

    # 감독과 캐스트 정보 추출
    credits_data = movie_data.get('credits', {})
    director = next(
        (crew['name'] for crew in credits_data.get('crew', [])
         if crew['job'] == 'Director'),
        None
    )

    cast = [
        {'name': actor['name'], 'character': actor['character']}
        for actor in credits_data.get('cast', [])[:5]  # 상위 5명만
    ]

    # 등급 정보 추출 (미국 등급 기준)
    rating = None
    for country in movie_data.get('release_dates', {}).get('results', []):
        if country['iso_3166_1'] == 'US':
            for release in country['release_dates']:
                if release.get('certification'):
                    rating = release['certification']
                    break
            break

    # YouTube 트레일러 가져오기
    trailer_response = requests.get(
        f"{base_url}/movie/{tmdb_id}/videos",
        params={'api_key': tmdb_api_key, 'language': 'en-US'}
    )
    trailer_data = trailer_response.json()

    youtube_trailer_id = None
    for video in trailer_data.get('results', []):
        if video['site'] == 'YouTube' and video['type'] == 'Trailer':
            youtube_trailer_id = video['key']
            break

    # 선택된 카테고리의 필터링된 스크립트 가져오기
    category = request.query_params.get('category')
    filtered_scripts = get_or_save_filtered_scripts(
        tmdb_id, category, request.user)

    context = {
        'title': movie_data.get('title'),
        'poster_path': f"https://image.tmdb.org/t/p/w500{movie_data.get('poster_path')}",
        'backdrop_path': f"https://image.tmdb.org/t/p/original{movie_data.get('backdrop_path')}" if movie_data.get('backdrop_path') else None,
        'overview': movie_data.get('overview'),
        'release_date': movie_data.get('release_date'),
        'tmdb_id': movie_data.get('id'),
        'filtered_scripts': filtered_scripts,
        'youtube_trailer_id': youtube_trailer_id,
        'runtime': movie_data.get('runtime'),  # 상영 시간 (분)
        'rating': rating,  # 영화 등급
        'director': director,  # 감독
        'cast': cast,  # 출연진 배열
    }

    return Response(context)


def parse_srt(srt_content):

    pattern = r'(\d+)\n([\d:,]+ --> [\d:,]+)\n([^\n]+(?:\n[^\n]+)*)'
    subtitles = []

    matches = re.findall(pattern, srt_content)  # re.findall(패턴, 문자열)
    for match in matches:
        index = match[0]
        timestamp = match[1]
        text = match[2].replace('\n', ' ')  # 줄 바꿈을 공백으로 변경

        # 타임스탬프 분리 (start_time, end_time)
        start_time, end_time = timestamp.split(' --> ')

        subtitles.append({
            'index': index,
            'start_time': start_time,  # 시작 시간
            'end_time': end_time,      # 종료 시간
            'text': text
        })

    return subtitles


"""
 subtitles = [ {
                    ...
                },
                {'end_time': '01:35:17,710',
                'index': '1197',
                'start_time': '01:35:13,290',
                'text': 'And you will watch.'}
            ]
"""


def classify_difficulty_level(text):
    readability_score = textstat.flesch_reading_ease(text)
    word_count = len(text.split())

    # 짧은 문장 예외 처리
    if word_count <= 3:
        return 'Beginner'

    # FRE 기준 수정
    if readability_score >= 90:  # 더 쉬운 기준
        return 'Beginner'
    elif 50 <= readability_score < 90:  # 적절한 중급
        return 'Intermediate'
    else:  # 어려운 문장
        return 'Advanced'


def save_subtitle_to_db(movie, subtitles):

    for subtitle_data in subtitles:

        text = subtitle_data['text']
        difficulty_level = classify_difficulty_level(text)

        Script.objects.create(
            movie=movie,
            index=subtitle_data['index'],
            timestamp=subtitle_data['start_time'],
            text=text,
            difficulty_level=difficulty_level,
        )

        # 해당 난이도에 맞는 영화의 DifficultyLevelMovie 갱신
        update_difficulty_level_count(movie, difficulty_level)


def update_difficulty_level_count(movie, difficulty_level):
    """
    DifficultyLevelMovie 모델을 업데이트하여 각 난이도별 영화의 스크립트 개수를 갱신
    """
    # 영화의 tmdb_id에 해당하는 DifficultyLevelMovie 객체를 가져옵니다
    try:
        difficulty_level_movie = DifficultyLevelMovie.objects.get(
            tmdb_id=movie.tmdb_id)
    except DifficultyLevelMovie.DoesNotExist:
        # 만약 존재하지 않는 경우, 새로 생성합니다
        difficulty_level_movie = DifficultyLevelMovie.objects.create(
            tmdb_id=movie,
            title=movie.title,
            beginner=0,
            intermediate=0,
            advanced=0,
        )

    # 난이도에 맞는 필드값을 증가시킵니다
    if difficulty_level == 'Beginner':
        difficulty_level_movie.beginner += 1
    elif difficulty_level == 'Intermediate':
        difficulty_level_movie.intermediate += 1
    elif difficulty_level == 'Advanced':
        difficulty_level_movie.advanced += 1

    # 데이터베이스에 저장
    difficulty_level_movie.save()


def movie_subtitles(request, tmdb_id):
    opensubtitles_api_key = settings.OPENSUBTITLES_API_KEY

    # 자막 검색
    search_url = f"https://api.opensubtitles.com/api/v1/subtitles?tmdb_id={tmdb_id}&languages=en"
    headers = {
        'Api-Key': opensubtitles_api_key,
        'Content-Type': 'application/json',
        'User-Agent': 'movie v1.0'
    }

    response = requests.get(search_url, headers=headers)

    subtitles = []
    if response.status_code == 200:
        subtitles_data = response.json().get('data', [])
        if subtitles_data:
            # 첫 번째 자막의 file_id 추출
            file_id = subtitles_data[0]['attributes']['files'][0]['file_id']
            print(f"Found file_id: {file_id}")

            # 다운로드 요청
            download_url = "https://api.opensubtitles.com/api/v1/download"
            download_data = {
                "file_id": file_id
            }

            download_response = requests.post(
                download_url, headers=headers, json=download_data)
            if download_response.status_code == 200:
                # 자막 다운로드 성공 시 링크 추출
                download_info = download_response.json()
                subtitle_link = download_info.get('link', '')

                # 다운로드한 파일을 다운로드 URL을 통해 저장
                if subtitle_link:
                    subtitle_response = requests.get(subtitle_link)
                    if subtitle_response.status_code == 200:
                        subtitle_content = subtitle_response.text  # 자막 파일 내용
                        pprint(subtitle_content)
                        subtitles = parse_srt(subtitle_content)  # 자막 파일 파싱

                        # tmdb_id인 객체를 Movie 클래스에서 갖고옴. 없으면 404 오류 반환(예외처리를 안해도 되는 장점이 있다.)
                        movie = get_object_or_404(Movie, tmdb_id=tmdb_id)

                        save_subtitle_to_db(movie, subtitles)

    context = {
        'subtitles': subtitles  # 자막 목록을 템플릿에 전달
    }
    return render(request, 'movie/subtitle_view.html', context)


@csrf_exempt
@require_http_methods(["POST"])
@permission_classes([IsAuthenticated])
def analyze_script(request):
    try:

        # Gemini API 설정
        genai.configure(api_key=settings.GEMINI_API_KEY)

        # 요청 데이터 디코딩
        data = json.loads(request.body)
        script = data.get('script', '')
        words = [word['word'] for word in data.get('words', [])]

        # Gemini 모델 생성
        model = genai.GenerativeModel('gemini-pro')

        # 프롬프트 구성
        prompt = f"""
        문장을 분석하여 아래의 문제에 답변하세요:
        "답변을 출력할 때 **마크다운** 없이 출력하세요."
        (한국어가 아닌 언어로는 출력하지 마세요.)
        문장: "{script}" 
        
        사용된 단어: {', '.join(words)}

        1. 문장 해석

        2. 단어 뜻

        3. 문법 설명
        (이 문장에서 사용된 문법을 간략히 설명하세요)

        4. 유사 문법 예문 3개
        - 영어 문장 1: (해석)
        - 영어 문장 2: (해석)
        - 영어 문장 3: (해석)

        5. 단어 활용 예문 3개
        - 영어 문장 1: (해석)
        - 영어 문장 2: (해석)
        - 영어 문장 3: (해석)
        """

        # Gemini API 호출
        response = model.generate_content(prompt)

        print("Gemini API Response:")
        print(response.text)
        # 응답 처리
        answer = response.text

        return JsonResponse({
            'response': answer  # 전체 텍스트를 그대로 반환
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        print(f"Error in analyze_script: {str(e)}")
        return JsonResponse({
            'error': str(e)
        }, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def level_movies(request):
    # 'Beginner', 'Intermediate', 'Advanced'
    level = request.query_params.get('level')
    goal = request.query_params.get('goal')  # 'SAT', 'TOEIC', 'BUSINESS'

    print(f"Received request: level={level}, goal={goal}")

    # 난이도별 영화 목록 조회
    if level == 'Beginner':
        level_movies = DifficultyLevelMovie.objects.order_by('-beginner')
    elif level == 'Intermediate':
        level_movies = DifficultyLevelMovie.objects.order_by('-intermediate')
    elif level == 'Advanced':
        level_movies = DifficultyLevelMovie.objects.order_by('-advanced')
    else:
        level_movies = []

    # 장르별로 그룹화
    genre_movie_data = {}
    for level_movie in level_movies:
        movie = level_movie.tmdb_id
        genres = movie.genres.all()

        for genre in genres:
            if genre.name not in genre_movie_data:
                genre_movie_data[genre.name] = []

            genre_movie_data[genre.name].append({
                'title': movie.title,
                'poster_path': movie.poster_path,
                'overview': movie.overview,
                'release_date': movie.release_date,
                'tmdb_id': movie.tmdb_id,
            })

    print(genre_movie_data)
    return Response(genre_movie_data)


def main_page(request):

    return render(request, 'movie/main.html')


@api_view(['GET'])
def search_movies(request):
    query = request.GET.get('query', None)
    if query:
        movies = Movie.objects.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query) |
            Q(genres__name__icontains=query)
        ).distinct()
        serializer = MovieSerializer(
            movies, many=True, context={'request': request})
        return Response({
            'results': serializer.data,
            'count': len(serializer.data),
            'query': query
        })
    return Response({'message': '검색어를 입력해주세요.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_favorite_voca(request):
    print("User:", request.user)  # 로그인된 사용자 확인
    print("Data:", request.data)  # 받은 데이터 확인

    word_id = request.data.get('word_id')

    try:
        vocabulary_word = VocabularyWord.objects.get(id=word_id)
        favorite_word, created = FavoriteWord.objects.get_or_create(
            user=request.user,
            vocabularyword=vocabulary_word,
            defaults={'learning_date': timezone.now()}
        )

        if created:
            return Response(
                {"message": "단어가 추가되었습니다."},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"message": "이미 추가된 단어입니다."},
            status=status.HTTP_200_OK
        )

    except VocabularyWord.DoesNotExist:
        return Response(
            {"error": "단어를 찾을 수 없습니다."},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        print("Error:", str(e))  # 에러 로깅
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_favorite(request):
    movie_tmdb_id = request.data.get('movie_tmdb_id')
    if FavoriteMovie.objects.filter(user=request.user, movie_tmdb_id=movie_tmdb_id).exists():
        return Response({'message': '이미 찜한 영화입니다.'}, status=status.HTTP_400_BAD_REQUEST)

    FavoriteMovie.objects.create(
        user=request.user,
        movie_tmdb_id=movie_tmdb_id,
        movie_title=request.data.get('movie_title')
    )
    return Response({'message': '찜하기 완료'}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_favorite_status(request, movie_tmdb_id):
    is_favorited = FavoriteMovie.objects.filter(
        user=request.user,
        movie_tmdb_id=movie_tmdb_id
    ).exists()
    return Response({'is_favorited': is_favorited})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_favorite(request, movie_tmdb_id):
    try:
        favorite = FavoriteMovie.objects.get(
            user=request.user,
            movie_tmdb_id=movie_tmdb_id
        )
        favorite.delete()
        return Response({'message': '찜하기 취소 완료'})
    except FavoriteMovie.DoesNotExist:
        return Response({'message': '찜한 영화가 없습니다.'}, status=404)


# movie/views.py
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_favorite_movies(request, username):
    # 요청된 사용자 찾기
    user = get_object_or_404(User, username=username)

    # 해당 사용자의 찜한 영화들 가져오기
    favorites = FavoriteMovie.objects.filter(user=user).order_by('-created_at')

    # 응답할 데이터 구성
    movies_list = []
    for favorite in favorites:
        # Movie 모델에서 해당 영화 정보 가져오기
        movie = Movie.objects.filter(tmdb_id=favorite.movie_tmdb_id).first()
        if movie:
            movies_list.append({
                'movie_tmdb_id': favorite.movie_tmdb_id,
                'movie_title': favorite.movie_title,
                'poster_path': movie.poster_path,
            })

    return Response(movies_list, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def movie_general_list(request):
    movies = Movie.objects.all().prefetch_related('genres')
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def genre_list(request):
    genres = Genre.objects.all()
    serializer = GenreSerializer(genres, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def convert_speech(request):
    try:
        script_id = request.POST.get('script_id')
        original_script = request.POST.get('original_script')

        # STT 처리
        google_speech_to_text_api_key = settings.SPEECH_TO_TEXT_API_KEY
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_speech_to_text_api_key

        if 'audio' not in request.FILES:
            return JsonResponse({'error': 'No audio file provided'}, status=400)

        audio_file = request.FILES['audio']

        # Speech Client 생성 시도
        try:
            client = speech.SpeechClient()
            print("Speech Client 생성 성공")
        except Exception as e:
            print("Speech Client 생성 실패:", str(e))
            return JsonResponse({'error': f'Speech Client 생성 실패: {str(e)}'}, status=500)

        # 오디오 처리
        audio_content = audio_file.read()
        audio = speech.RecognitionAudio(content=audio_content)

        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
            sample_rate_hertz=48000,
            language_code="en-US",
            enable_automatic_punctuation=True,
        )

        response = client.recognize(config=config, audio=audio)
        transcriptions = [
            result.alternatives[0].transcript for result in response.results]
        converted_text = ' '.join(transcriptions)

        # 일치율 계산
        match_rate = calculate_match_rate(original_script, converted_text)

        # 진행상황 업데이트
        progress, created = UserScriptProgress.objects.get_or_create(
            user=request.user,
            script_id=script_id
        )

        # 결과 업데이트 및 반환
        result = progress.update_progress(match_rate)

        print('result:', result)
        print('hightest_match_rate : ', progress.highest_match_rate)

        return JsonResponse({
            'text': converted_text,
            'match_rate': result['match_rate'],
            'points': result['points'],
            'is_new_record': result['is_new_record'],
            'highest_match_rate': progress.highest_match_rate,
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def calculate_match_rate(original_script, user_speech):

    def clean_text(text):
        # 1. 모든 문장부호 및 특수문자 제거
        cleaned = re.sub(r'[^\w\s]', '', text)
        # 2. 연속된 공백을 하나로 통일
        cleaned = re.sub(r'\s+', ' ', cleaned)
        # 3. 양쪽 공백 제거 및 소문자로 통일
        cleaned = cleaned.strip().lower()
        return cleaned

    # LCS 알고리즘 구현
    def lcs(X, Y):
        m, n = len(X), len(Y)
        L = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(m + 1):
            for j in range(n + 1):
                if i == 0 or j == 0:
                    L[i][j] = 0
                elif X[i-1] == Y[j-1]:
                    L[i][j] = L[i-1][j-1] + 1
                else:
                    L[i][j] = max(L[i-1][j], L[i][j-1])

        return L[m][n]

    # 텍스트 전처리
    cleaned_original = clean_text(original_script)
    cleaned_user = clean_text(user_speech)

    # 전처리된 문장을 단어 배열로 변환
    original_words = cleaned_original.split()
    user_words = cleaned_user.split()

    # LCS 길이 계산
    match_length = lcs(original_words, user_words)

    # 일치율 계산 (더 긴 문장 기준)
    max_length = max(len(original_words), len(user_words))
    if max_length == 0:
        return 0

    match_rate = (match_length / max_length) * 100

    return match_rate


def award_points(match_rate):
    if match_rate >= 100:
        return 5
    elif match_rate >= 80:
        return 3
    elif match_rate >= 60:
        return 1
    return 0


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_favorite_words(request, username):
    user = get_object_or_404(User, username=username)
    favorite_words = FavoriteWord.objects.filter(user=user)

    words_data = []
    for favorite in favorite_words:
        word = VocabularyWord.objects.get(id=favorite.vocabularyword.id)
        words_data.append({
            'id': favorite.id,
            'word': word.word,
            'meaning': word.meaning,
            'category': word.category,
            'learning_date': favorite.learning_date
        })

    return Response(words_data)
