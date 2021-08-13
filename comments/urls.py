from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ChildCommentsViewSet, CommentViewSet

v1_router = DefaultRouter()

v1_router.register(
    r'articles/(?P<article_id>[\d]+)/comments',
    CommentViewSet,
    basename='main-comments')

v1_router.register(
    r'articles/(?P<article_id>[\d]+)/comments/(?P<comment_id>[\d]+)/child-comments',
    ChildCommentsViewSet,
    basename='child-comments')

urlpatterns = [
    path('', include(v1_router.urls)),
]
