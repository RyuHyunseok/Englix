from django.db import models
from django.conf import settings
from django.utils import timezone
from accounts.models import User


class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Movie(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255, default='untitled')
    release_date = models.DateField()
    poster_path = models.TextField()
    backdrop_path = models.TextField(null=True, blank=True)  # 두 번째 이미지
    overview = models.TextField()
    genres = models.ManyToManyField(Genre, related_name='movies')

    runtime = models.IntegerField(null=True, blank=True)  # 상영 시간
    rating = models.CharField(max_length=10, null=True, blank=True)  # 등급
    director = models.CharField(max_length=255, null=True, blank=True)  # 감독
    cast = models.JSONField(default=list)  # 출연진 정보를 JSON으로 저장

    def __str__(self):
        return self.title


class Script(models.Model):
    movie = models.ForeignKey(
        Movie, to_field='tmdb_id', on_delete=models.CASCADE)
    index = models.IntegerField()
    timestamp = models.CharField(max_length=50, null=True, blank=True)
    text = models.TextField()
    DIFFICULTY_CHOICES = [
        ('Beginner', '초급'),
        ('Intermediate', '중급'),
        ('Advanced', '고급'),
    ]
    difficulty_level = models.CharField(
        max_length=20, choices=DIFFICULTY_CHOICES)

    def __str__(self):
        return f"Script {self.index} - {self.movie.title}"


class DifficultyLevelMovie(models.Model):
    beginner = models.IntegerField()
    intermediate = models.IntegerField()
    advanced = models.IntegerField()
    tmdb_id = models.ForeignKey(
        Movie, to_field='tmdb_id', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.tmdb_id.title


class FavoriteMovie(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='favorites')
    movie_tmdb_id = models.CharField(max_length=50)
    movie_title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.movie_title}"


class VocabularyWord(models.Model):
    word = models.CharField(max_length=100)
    meaning = models.CharField(max_length=300)
    category = models.CharField(max_length=20)

    class Meta:
        unique_together = ('word', 'category')

    def __str__(self):
        return self.word


class FavoriteWord(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorite_words')
    vocabularyword = models.ForeignKey(
        VocabularyWord, on_delete=models.CASCADE, related_name='favorited_by')
    learning_date = models.DateField(default=timezone.now())

    class Meta:
        # 한 사용자가 동일한 단어를 여러 번 저장하지 않도록 설정
        unique_together = ('user', 'vocabularyword')

    def __str__(self):
        return f"{self.user.username} - {self.vocabularyword.word}"


class UserScriptProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    script = models.ForeignKey(Script, on_delete=models.CASCADE)
    highest_match_rate = models.IntegerField(default=0)  # 최고 일치율
    highest_points = models.IntegerField(default=0)      # 해당 스크립트에서 받은 최고 점수
    last_attempt = models.DateTimeField(auto_now=True)   # 마지막 시도 시간

    class Meta:
        unique_together = ('user', 'script')
        indexes = [
            models.Index(fields=['user', 'highest_match_rate']),
            models.Index(fields=['script', 'highest_match_rate']),
        ]

    def update_progress(self, match_rate):
        """
        일치율에 따라 점수를 계산하고 필요한 경우 업데이트
        """
        # 점수 계산 (예: 100% = 5점, 80% = 3점, 60% = 1점)
        new_points = 0
        if match_rate >= 100:
            new_points = 5
        elif match_rate >= 80:
            new_points = 3
        elif match_rate >= 60:
            new_points = 1

        # 최고 점수/일치율 업데이트가 필요한 경우
        points_changed = False
        if match_rate > self.highest_match_rate:
            old_points = self.highest_points
            self.highest_match_rate = match_rate
            self.highest_points = new_points
            points_changed = True

            # 사용자 총점 업데이트
            point_diff = new_points - old_points
            if point_diff > 0:
                self.user.points += point_diff
                self.user.save()

        self.save()
        return {
            'match_rate': match_rate,
            'points': new_points if points_changed else 0,
            'is_new_record': points_changed
        }
