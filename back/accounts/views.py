# accounts/views.py
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import UserSerializer


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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    user = request.user
    print("====DEBUG INFO START====")
    print("User type:", type(user))
    print("User fields:", [field.name for field in user._meta.fields])
    print("User data:", {
        'username': user.username,
        'goal': getattr(user, 'goal', None),
        'level': getattr(user, 'level', None),
        'prefer_genre': getattr(user, 'prefer_genre', None)
    })
    print("Serializer fields:", UserSerializer().get_fields().keys())
    serializer = UserSerializer(user)
    print("Serialized data:", serializer.data)
    print("====DEBUG INFO END====")
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_account(request):
    try:
        user = request.user
        user.delete()
        return Response({'message': '계정이 성공적으로 삭제되었습니다.'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': '계정 삭제 중 오류가 발생했습니다.'}, status=status.HTTP_400_BAD_REQUEST)
    
from .models import User


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_users(request):
    try:
        users = User.objects.all().order_by('-points')
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    except Exception as e:
        print(f"Error in get_all_users: {str(e)}")
        return Response({"error": str(e)}, status=500)