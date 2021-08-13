from rest_framework import filters, permissions, viewsets

from .models import Article
from .serializers import ArticleSerializer


class QueryViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['id']
    http_method_names = ['get', 'post', 'delete']


class ArticleViewSet(QueryViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
