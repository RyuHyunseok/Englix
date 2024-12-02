from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import VocabularyWord, FavoriteWord, Movie, Script, Genre, DifficultyLevelMovie


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)  # ManyToMany 관계를 처리

    class Meta:
        model = Movie
        fields = ['tmdb_id', 'title', 'release_date',
                  'poster_path', 'overview', 'genres']


class ScriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Script
        fields = ['id', 'movie', 'index',
                  'timestamp', 'text', 'difficulty_level']


class DifficultyLevelMovieSerializer(serializers.ModelSerializer):
    tmdb_id = MovieSerializer()  # ForeignKey로 연결된 Movie 모델 포함

    class Meta:
        model = DifficultyLevelMovie
        fields = ['id', 'beginner', 'intermediate',
                  'advanced', 'tmdb_id', 'title']


class VocabularyWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = VocabularyWord
        fields = ['id', 'word', 'category']


class FavoriteWordSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    vocabularyword = VocabularyWordSerializer()

    class Meta:
        model = FavoriteWord
        fields = ['id', 'user', 'vocabularyword', 'learning_date']
