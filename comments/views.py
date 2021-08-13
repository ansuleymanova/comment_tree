from rest_framework import filters, permissions, viewsets
from rest_framework.generics import get_object_or_404

from articles.models import Article

from .models import Comment
from .serializers import CommentSerializer


class QueryViewSet(viewsets.ModelViewSet):
    """base class for Comment viewsets"""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['id']
    http_method_names = ['get', 'post', 'delete']


class CommentViewSet(viewsets.ModelViewSet):
    """
    general comment viewset:
    perform_create method is redefined to save uneditable fields
    and is used to POST comments of depth 0
    get_queryset method hits database once
    and returns only comments with depth up to 3
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        try:
            parent_comment = Comment.objects.get(
                id=self.kwargs.get('comment_id'))
            depth = parent_comment.depth + 1
        except Comment.DoesNotExist:
            parent_comment = None
            depth = 0
        article = get_object_or_404(Article,
                                    id=self.kwargs.get('article_id'))
        serializer.save(article=article,
                        author=self.request.user,
                        depth=depth,
                        parent_comment=parent_comment)

    def get_queryset(self):
        article = get_object_or_404(Article,
                                    id=self.kwargs.get('article_id'))
        return article.comments.filter(depth__lte=3)


class ChildCommentsViewSet(CommentViewSet):
    """
    viewset to POST child comments (depth 1 and up)
    get_queryset method returns all comment branches of a comment
    while hitting database only once
    """
    queryset = Comment.objects.all()
    pagination_class = None

    def perform_create(self, serializer):
        parent = Comment.objects.get(id=self.kwargs.get('comment_id'))
        depth = parent.depth + 1
        article = get_object_or_404(Article,
                                    id=self.kwargs.get('article_id'))
        serializer.save(article=article,
                        author=self.request.user,
                        depth=depth,
                        parent_comment=parent)

    def get_queryset(self):
        article = get_object_or_404(Article,
                                    id=self.kwargs.get('article_id'))
        child_comments = article.comments.filter(
            parent_comment=self.kwargs.get('comment_id'))
        comments = set()

        def get_children(child_comments):
            for comment in child_comments:
                if comment.id is None:
                    return []
                comments.add(comment)
                children = article.comments.filter(parent_comment=comment.id)
                get_children(children)
            return comments

        return get_children(child_comments)
