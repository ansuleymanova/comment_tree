from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ArticleViewSet

v1_router = DefaultRouter()
v1_router.register(r'articles', ArticleViewSet, basename='articles')

urlpatterns = [
    path('', include(v1_router.urls)),
]
