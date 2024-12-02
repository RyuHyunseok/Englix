from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    # ... 기존 URL 패턴들 ...
    path('preferences/', views.update_user_preferences, name='update_preferences'),
    path('user/', views.get_user_info, name='user_info'),
    path('delete/', views.delete_account, name='delete_account'),
    path('users/all/', views.get_all_users, name='all_users'),
]
