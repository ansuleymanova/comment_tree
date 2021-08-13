from django.db import models

from articles.models import Article
from users.models import User


class Comment(models.Model):
    id = models.IntegerField(primary_key=True,
                             editable=False,
                             auto_created=True)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comments')
    article = models.ForeignKey(Article,
                                on_delete=models.CASCADE,
                                related_name='comments')
    depth = models.IntegerField(auto_created=True,
                                default=0,
                                editable=False)
    parent_comment = models.ForeignKey('self',
                                       on_delete=models.CASCADE,
                                       null=True,
                                       blank=True,
                                       editable=False,
                                       related_name='children')
    pub_date = models.DateField(auto_now_add=True)
    text = models.TextField()

    class Meta:
        ordering = ['depth']

    def __str__(self):
        return(self.text)
