# from django.contrib import admin
# from django.urls import include, path
# from .views import blog_list, blog_detail

# urlpatterns = [
#     path('', blog_list, name='blog_list'),
#     path('<int:pk>/', blog_detail, name='blog_detail'),
# ]

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (blog_list, blog_detail, create_post, update_post, dashboard_view, delete_post, login_view, logout_view, register_view, comment_view)
from . import views
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import CategoryViewSet, PostViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('api/', include(router.urls)),  # Prefix API routes with /api/
    path('', dashboard_view, name='dashboard'),
    path('mypost/', blog_list, name='blog_list'),
    path('<int:pk>/', blog_detail, name='blog_detail'),
    path('new/', create_post, name='create_post'),
    path('<int:pk>/edit/', update_post, name='update_post'),
    path('<int:pk>/delete/', delete_post, name='delete_post'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('comments/', views.comment_view, name='comment_view'),

    


]

# Serving static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Add this line for media files
