from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db.models import Sum


# Create your models here.

class Post(models.Model):
    news = 'NE'
    article = 'AR'

    POST_TYPES = [
        (news, 'Новость'),
        (article, 'Статья')
    ]
    author = models.CharField(max_length=255, default='Default author', verbose_name='author')
    post_type = models.CharField(max_length=2, choices=POST_TYPES, default=article, verbose_name='Вид поста')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='дата и время создания')
    date_update = models.DateTimeField(auto_now=True, verbose_name='дата и время изменения')
    #categories = models.ManyToManyField(Category, through="PostCategory", through_fields=("post", "category"), )
    title = models.CharField(max_length=255, default='Default title', verbose_name='заголовок')
    content = models.TextField(default='Default content', verbose_name='текст')
    #rating = models.IntegerField(default=0.0)

    def __str__(self):
        return f'{self.title}: {self.date_create.strftime("%d-%m-%Y, %H:%M:%S")}: {self.content[:20]}'