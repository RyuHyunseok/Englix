from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    LEVEL_CHOICES = [
        ('Beginner', '초급'),
        ('Intermediate', '중급'),
        ('Advanced', '고급'),
    ]
    GOAL_CHOICES = [
        ('SAT', '수능'),
        ('TOEIC', '토익'),
        ('BUSINESS', '비즈니스'),
    ]
    GENRE_CHOICES = [

        ('Action', '액션'),
        ('Adventure', '모험'),
        ('Animation', '애니메이션'),
        ('Comedy', '코미디'),
        ('Crime', '범죄'),
        ('Documentary', '다큐멘터리'),
        ('Drama', '드라마'),
        ('Family', '가족'),
        ('Fantasy', '판타지'),
        ('History', '역사'),
        ('Horror', '공포'),
        ('Music', '음악'),
        ('Romance', '로맨스'),
        ('Science Fiction', 'SF'),
        ('TV Movie', 'TV 영화'),
        ('Thriller', '스릴러'),
        ('War', '전쟁'),
        ('Western', '서구'),

    ]
    TIER_CHOICES = [
        ('Bronze', '브론즈'),
        ('Siver', '실버'),
        ('Gold', '골드'),
        ('Platinum', '플래티넘'),
        ('Diamond', '다이아몬드'),
        ('Ruby', '루비'),
    ]
    level = models.CharField(
        max_length=20, choices=LEVEL_CHOICES, null=True, blank=True)
    goal = models.CharField(
        max_length=50, choices=GOAL_CHOICES, null=True, blank=True)
    prefer_genre = models.CharField(
        max_length=50, choices=GENRE_CHOICES, null=True, blank=True)

    points = models.IntegerField(default=0)
    tier = models.CharField(
        max_length=10, choices=TIER_CHOICES, default='Bronze')

    nickname = models.CharField(
        max_length=50, unique=True, null=True, blank=True)  # 닉네임 필드 추가
    bio = models.TextField(max_length=500, blank=True, null=True)  # 자기소개

    # property 사용 하면 트리거를 사용하지 않아도 됌

    @property
    def tier_image_path(self):
        return {
            'Ruby': 'tier_images/ruby.png',
            'Diamond': 'tier_images/diamond.png',
            'Platinum': 'tier_images/platinum.png',
            'Gold': 'tier_images/gold.png',
            'Silver': 'tier_images/silver.png',
            'Bronze': 'tier_images/bronze.png',
        }.get(self.tier, 'tier_images/bronze.png')

    def save(self, *args, **kwargs):
        # If no nickname is set, use username as default
        if not self.nickname:
            self.nickname = self.username
        # self.tier = self.get_tier_based_on_points()
        super().save(*args, **kwargs)

    # def get_tier_based_on_points(self):
    #     """
    #     포인트 기준으로 티어를 반환.
    #     """
    #     if self.points >= 500:
    #         return 'Ruby'
    #     elif self.points >= 200:
    #         return 'Diamond'
    #     elif self.points >= 100:
    #         return 'Platinum'
    #     elif self.points >= 50:
    #         return 'Gold'
    #     elif self.points >= 10:
    #         return 'Silver'
    #     else:
    #         return 'Bronze'

    def __str__(self):
        return self.username
