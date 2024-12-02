from django.urls import path
from . import views

app_name = "community"

urlpatterns = [
    path('posts/', views.post_list, name='post_list'),  
    path('posts/<int:pk>/', views.post_detail, name='post_detail'), 
    path('posts/<int:post_pk>/comments/', views.comment_list, name='comment_list'),
    path('comments/<int:pk>/update/', views.comment_detail, name='comment_detail'),
    path('posts/<int:post_pk>/like/', views.like_post, name='like_post'),
    path('profile/<str:username>/', views.profile_view, name='profile_view'),
    path('profile/<str:username>/follow/', views.follow_toggle, name='follow_toggle'),
    path('posts/search/', views.search_posts, name='search_posts'),
    path('liked-posts/', views.get_liked_posts, name='liked-posts'),

]