from django.contrib import admin
from .models import Category, Author, Post, PostCategory, Comment, Censorship


admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(Comment)
admin.site.register(Censorship)
