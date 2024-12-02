from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from accounts.models import User
from .models import Post, Comment, Like, Follow
from .serializers import PostSerializer, CommentSerializer
from django.db.models import Q


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'GET':
        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        if post.user != request.user:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        # 기존 파일 정보 저장
        old_file = post.file if post.file else None

        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            # 파일이 비어있는 문자열로 전송된 경우 (파일 삭제 요청)
            if request.data.get('file') == '':
                # 기존 파일 삭제
                if old_file:
                    old_file.delete(save=False)
                post.file = None

            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if post.user != request.user:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        post.delete()
        return Response({'message': 'Post deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


# views.py
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def post_list(request):
    if request.method == 'GET':
        category = request.query_params.get('category', 'free')
        posts = Post.objects.filter(category=category).order_by('-created_at')
        serializer = PostSerializer(
            posts, many=True, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data, context={
                                    'request': request})  # context 추가
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def comment_list(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)

    if request.method == 'GET':
        comments = Comment.objects.filter(post=post).order_by('-created_at')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        comment = Comment.objects.create(
            post=post,
            user=request.user,
            content=request.data.get('content')
        )
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def comment_detail(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if comment.user != request.user:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)

    try:
        like = Like.objects.get(user=request.user, post=post)
        like.delete()
        return Response({
            'message': 'Like removed',
            'likes_count': post.post_likes.count()
        }, status=status.HTTP_200_OK)
    except Like.DoesNotExist:
        Like.objects.create(user=request.user, post=post)
        return Response({
            'message': 'Like added',
            'likes_count': post.post_likes.count()
        }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user).order_by('-created_at')
    comments = Comment.objects.filter(user=user).order_by('-created_at')

    # 팔로워/팔로잉 수 계산
    followers_count = user.followers.count()
    following_count = user.following.count()

    # 현재 로그인한 사용자가 이 프로필의 사용자를 팔로우하고 있는지 확인
    is_following = request.user.following.filter(followed=user).exists()

    return Response({
        'profile_user': {
            'username': user.username,
            'nickname': user.nickname,
            'bio': user.bio,
            'id': user.id,
            'tier': user.tier,
            'tier_image_path': user.tier_image_path,
        },
        'posts': PostSerializer(posts, context={'request': request}, many=True).data,
        'comments': CommentSerializer(comments, many=True).data,
        'followers_count': followers_count,
        'following_count': following_count,
        'is_following': is_following,
        'is_self': request.user == user,  # 자기 자신의 프로필인지 확인
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_toggle(request, username):
    target_user = get_object_or_404(User, username=username)

    if target_user == request.user:
        return Response({'error': 'You cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)

    follow, created = Follow.objects.get_or_create(
        follower=request.user,
        followed=target_user
    )

    if not created:
        follow.delete()
        return Response({'message': 'Unfollowed'}, status=status.HTTP_200_OK)

    return Response({'message': 'Followed'}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def search_posts(request):
    query = request.GET.get('query', None)
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__username__icontains=query) |
            Q(user__nickname__icontains=query)
        ).distinct()

        serializer = PostSerializer(posts, many=True)
        return Response({
            'results': serializer.data,
            'count': len(serializer.data),
            'query': query
        })
    return Response({'message': '검색어를 입력해주세요.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_liked_posts(request):
    # 사용자가 좋아요한 게시글들 가져오기
    liked_posts = Post.objects.filter(
        post_likes__user=request.user).order_by('-created_at')
    serializer = PostSerializer(
        liked_posts, many=True, context={'request': request})
    return Response(serializer.data)
