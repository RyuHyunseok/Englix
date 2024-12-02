from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['pk', 'username', 'email','bio','nickname',
                  'first_name', 'last_name', 'goal', 'level', 'prefer_genre', 'points', 'tier', 'tier_image_path']


from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(required=True)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['nickname'] = self.validated_data.get('nickname', '')
        return data
    
    def save(self, request):
        user = super().save(request)
        user.nickname = self.validated_data.get('nickname', '')
        user.save()
        return user
    
class UserSerializer(serializers.ModelSerializer):
    tier_image_path = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'nickname', 'points', 'tier', 'tier_image_path',]

    def get_tier_image_path(self, obj):
        return obj.tier_image_path