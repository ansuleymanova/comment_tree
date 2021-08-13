from django.db import models

from users.models import User


class Article(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=400)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='articles')
    text = models.TextField()
    pub_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name
