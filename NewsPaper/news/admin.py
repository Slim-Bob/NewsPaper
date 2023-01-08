from django.contrib import admin
from .models import Category, Author, Post, PostCategory, Comment, Censorship

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating')
    list_filter = ('user', '_rating')
    search_fields = ('user', 'rating')


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'type', 'create_date_time', 'rating', 'author')
    list_filter = ('title', 'text', 'type', 'create_date_time', '_rating', 'author')
    search_fields = ('title', 'text', 'type', 'create_date_time', 'rating', 'author')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment)
admin.site.register(Censorship)
