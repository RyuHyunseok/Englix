from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('movie/', include('movie.urls')),
    path('community/', include('community.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('dj_rest_auth.urls')),
    path('accounts/signup/', include('dj_rest_auth.registration.urls')),
]

# 개발 환경에서 미디어/스태틱 파일 서빙
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# urlpatterns += [
#     path('api/schema/', SpectacularAPIView.as_view(),
#          name='schema'),  # OpenAPI JSON
#     path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'),
#          name='swagger-ui'),  # Swagger UI
#     path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'),
#          name='redoc'),  # Redoc
#     path('api/', include('movie.urls')),
# ]
