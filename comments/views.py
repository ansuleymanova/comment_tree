from rest_framework import filters, permissions, viewsets
from rest_framework.generics import get_object_or_404

from articles.models import Article

from .models import Comment
from .serializers import CommentSerializer


class QueryViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['id']
    http_method_names = ['get', 'post', 'delete']


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        try:
            parent_comment = Comment.objects.get(
                id=self.kwargs.get('comment_id'))
            nesting_level = parent_comment.nesting_level + 1
        except Comment.DoesNotExist:
            parent_comment = None
            nesting_level = 0
        article = get_object_or_404(Article,
                                    id=self.kwargs.get('article_id'))
        serializer.save(article=article,
                        # author=self.request.user,
                        nesting_level=nesting_level,
                        parent_comment=parent_comment)

    def get_queryset(self):
        article = get_object_or_404(Article,
                                    id=self.kwargs.get('article_id'))
        return article.comments.filter(nesting_level__lt=3)


class ChildCommentsViewSet(CommentViewSet):
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        parent_comment = Comment.objects.get(id=self.kwargs.get('comment_id'))
        nesting_level = parent_comment.nesting_level + 1
        article = get_object_or_404(Article,
                                    id=self.kwargs.get('article_id'))
        serializer.save(article=article,
                        # author=self.request.user,
                        nesting_level=nesting_level,
                        parent_comment=parent_comment)

    def get_queryset(self):
        return Comment.objects.filter(
            parent_comment__id=self.kwargs.get('comment_id'))
