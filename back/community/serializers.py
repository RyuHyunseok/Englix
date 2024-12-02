# serializers.py
from accounts.serializers import UserSerializer
from rest_framework import serializers
from .models import Post, Comment, Follow


class PostSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_image = serializers.BooleanField(read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post  
        fields = ['id', 'user', 'title', 'content', 'category', 'created_at', 'likes_count', 'is_liked','file', 'is_image', 'comments_count']
        read_only_fields = ['id', 'user', 'created_at', 'likes_count', 'is_liked', 'comments_count']

    def get_user(self, obj):
        return {
            'id': obj.user.id, 
            'username': obj.user.username,
            'nickname': obj.user.nickname
        }
    
    def get_likes_count(self, obj):
        return obj.post_likes.count()
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.post_likes.filter(user=request.user).exists()
        return False
    
    def create(self, validated_data):
        user = self.context.get('request').user 
        if user:
            return Post.objects.create(user=user, **validated_data)
        raise serializers.ValidationError("User is required")
            
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance

    def get_comments_count(self, obj): 
        return obj.comments.count()

class CommentSerializer(serializers.ModelSerializer):
   user = serializers.SerializerMethodField()
   created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
   

   class Meta: 
       model = Comment
       fields = ['id', 'content', 'user', 'created_at']
       read_only_fields = ['id', 'user', 'created_at']

   def get_user(self, obj):
       return {
           'id': obj.user.id,
           'username': obj.user.username,
           'nickname': obj.user.nickname
       }

class FollowSerializer(serializers.ModelSerializer):
   follower = UserSerializer() 
   followed = UserSerializer()

   class Meta:
       model = Follow
       fields = ['id', 'follower', 'followed', 'created_at']