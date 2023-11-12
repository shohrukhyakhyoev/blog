from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

from rest_framework import routers

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from api.views import (
    UserViewSet,

    PostViewSet,
    ProjectViewSet,
    CourseViewSet,

    PostUpdateView,
    ThumbnailUpdateView,

    CategoryViewSet,
    TagViewSet,
)

router = routers.DefaultRouter()  
router.register(r'api/users', UserViewSet, basename='users')
router.register(r'api/posts', PostViewSet, basename='posts')
router.register(r'api/projects', ProjectViewSet, basename='projects')
router.register(r'api/academy', CourseViewSet, basename='projects')
router.register(r'api/category', CategoryViewSet, basename='categories')
router.register(r'api/tags', TagViewSet, basename='tags')




urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),
    path('', include(router.urls)), 

    path('api/update/post/<int:pk>/', PostUpdateView.as_view(), name='post_update'),
    path('api/update/file/<int:pk>/', ThumbnailUpdateView.as_view(), name='file_submit'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)