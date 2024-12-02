
from django.urls import path
from . import views
# from .views import MovieListAPIView, GenreListAPIView, ScriptListAPIView

app_name = "movie"
urlpatterns = [
    path('', views.movie_list, name='index'),
    path('movie_detail/<int:tmdb_id>/', views.movie_detail, name='movie_detail'),
    path('analyze_script/', views.analyze_script, name='analyze_script'),
    path('subtitles/<int:tmdb_id>/', views.movie_subtitles, name='movie_subtitles'),
    path('level-movies/', views.level_movies, name='level_movies'),
    path('main/', views.main_page, name='main_page'),
    path('search/', views.search_movies, name='movie_search'),
    path('add_to_favorite_voca/', views.add_to_favorite_voca,
         name='add_to_favorite_voca'),
    path('favorites/status/<str:movie_tmdb_id>/',
         views.check_favorite_status, name='check_favorite_status'),
    path('favorites/', views.add_favorite, name='add_favorite'),
    path('favorites/<str:movie_tmdb_id>/',
         views.remove_favorite, name='remove_favorite'),
    path('favorite-movies/<str:username>/',
         views.get_favorite_movies, name='get_favorite_movies'),
    path('list/', views.movie_general_list, name='movie_general_list'),
    path('genres/', views.genre_list, name='genre_list'),
    path('convert-speech/', views.convert_speech, name='convert_speech'),
     path('favorite-words/<str:username>/', views.get_favorite_words, name='get_favorite_words'),

]
