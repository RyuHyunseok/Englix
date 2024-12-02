from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import MovieSerializer, GenreSerializer, ScriptSerializer

from django.http import JsonResponse
from django.conf import settings
import google.generativeai as genai
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import textstat
from .models import DifficultyLevelMovie, Script, VocabularyWord
from django.core.cache import cache
from multiprocessing import context
import requests
from django.shortcuts import render, get_object_or_404

from englix_pjt import settings
from django.http import JsonResponse, HttpResponse
import re
from pprint import pprint
from .models import Movie, Script, VocabularyWord, Genre


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
    if readability_score >= 80:  # 더 쉬운 기준
        return 'Beginner'
    elif 60 <= readability_score < 80:  # 적절한 중급
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