
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum



# Create your models here.

class Author(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, verbose_name='Имя')
    rating = models.IntegerField(default=0.0)

    def update_rating(self):
        rating_post = Post.objects.filter(author=self).aggregate(Sum('rating'))['rating__sum'] * 3
        rating_comment = Comment.objects.filter(user=self.user).aggregate(Sum('rating'))['rating__sum']
        rating_comment_post = Comment.objects.filter(post__author__user=self.user).aggregate(Sum('rating'))['rating__sum']
        self.rating = rating_post + rating_comment + rating_comment_post
        self.save()

class Category(models.Model):
    name = models.CharField(unique = True, max_length=255, verbose_name='Категории' )


class Post(models.Model):
    news = 'NE'
    article = 'AR'

    POST_TYPES = [
        (news, 'Новость'),
        (article, 'Статья')
    ]
    author = models.ForeignKey(Author, on_delete = models.CASCADE, verbose_name='Автор')
    post_type = models.CharField(max_length=2, choices=POST_TYPES, default=article, verbose_name='Вид поста')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='дата и время создания')
    date_update = models.DateTimeField(auto_now=True, verbose_name='дата и время изменения')
    categories = models.ManyToManyField(Category, through="PostCategory", through_fields=("post", "category"),)
    title = models.CharField(max_length=255, default = 'Default title', verbose_name='заголовок')
    content = models.TextField(default = 'Default content', verbose_name='текст')
    rating = models.IntegerField(default=0.0)

    def like(self):
        self.rating+=1
        self.save()

    def dislike(self):
        self.rating-=1
        self.save()

    def preview(self):
        return self.content[:124] + '...' if len(self.content) > 124 else self.content


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE,  null=True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE, null=True)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, verbose_name='Пост')
    user = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name='Пользователь')
    text_comment = models.TextField(default = 'Default comment', verbose_name='текст комментария' )
    datetime_create = models.DateTimeField(auto_now_add=True, verbose_name='дата и время создания комментария')
    rating = models.IntegerField(default=0.0)

    def like(self):
        self.rating+=1
        self.save()
    def dislike(self):
        self.rating-=1
        self.save()