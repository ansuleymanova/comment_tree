from django.db import models

from articles.models import Article
from users.models import User


class Comment(models.Model):
    id = models.IntegerField(primary_key=True)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comments')
    article = models.ForeignKey(Article,
                                on_delete=models.CASCADE,
                                related_name='comments')
    nesting_level = models.IntegerField(auto_created=True,
                                        default=0,
                                        editable=False)
    parent_comment = models.ForeignKey('self',
                                       null=True,
                                       blank=True,
                                       on_delete=models.CASCADE,
                                       related_name='children_comments')
    pub_date = models.DateField(auto_now_add=True)
    text = models.TextField()

    def __str__(self):
        return(self.text)

    class Meta:
        ordering = ['nesting_level']
