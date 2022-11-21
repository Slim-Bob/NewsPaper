from __future__ import annotations
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Author(models.Model):
    # rating = models.IntegerField()
    _rating = models.IntegerField(default=0, db_column='rating')

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def rating(self):
        return self._rating

    def update_rating(self):
        self._rating = 0

        comments = Comment.objects.filter(user=self.user)
        for comment in comments:
            self._rating += comment.rating

        posts = Post.objects.filter(author=self)
        for post in posts:
            comments_post = Comment.objects.filter(post=post)
            self._rating += post.rating * 3

            for comment in comments_post:
                self._rating += comment.rating

        self.save()

    def __str__(self):
        return f'{self.user.username}'


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


POST_ARTICLE = 'AE'
POST_NEWS = 'NS'

POST_TYPE = [
    (POST_ARTICLE, 'статья'),
    (POST_NEWS, 'новость'),
]

class Post(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    type = models.CharField(max_length=2, choices=POST_TYPE, default=POST_NEWS)
    create_date_time = models.DateTimeField(auto_now_add=True)

    _rating = models.IntegerField(default=0, db_column='rating')

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory')

    @property
    def rating(self):
        return self._rating  # Заменить на расчет

    def like(self):
        self._rating += 1
        self.save()

    def dislike(self):
        self._rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[:120]}...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    text = models.TextField()
    create_date_time = models.DateTimeField(auto_now_add=True)

    _rating = models.IntegerField(default=0, db_column='rating')

    @property
    def rating(self):
        return self._rating

    def like(self):
        self._rating += 1
        self.save()

    def dislike(self):
        self._rating -= 1
        self.save()


class Censorship(models.Model):
    pattern = models.TextField()