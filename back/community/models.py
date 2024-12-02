from django.db import models
from django.conf import settings


class Post(models.Model):
    CATEGORY_CHOICES = [
        ('QandA', '질문 게시판'),
        ('LearningResource', '자료 공유 게시판'), 
        ('free', '자유 게시판'),
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(
        max_length=20, 
        choices=CATEGORY_CHOICES,
        default='free' 
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    file = models.FileField(upload_to='post_files/', null=True, blank=True)
    
    def __str__(self):
        return self.title

    @property
    def is_image(self):
        if not self.file:
            return False
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
        file_extension = self.file.name.lower().endswith(tuple(image_extensions))
        return file_extension

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"


class Follow(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='followers', on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('follower', 'followed')  # 중복 팔로우 방지


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post_likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  # 한 사용자가 같은 게시글에 중복 좋아요 방지

    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"