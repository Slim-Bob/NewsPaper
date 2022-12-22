from django.urls import path
from .views import PostsList, PostDetail, PostsSearch, NewsCreate, NewsUpdate, NewsDelete, ArticlesCreate, ArticlesUpdate, ArticlesDelete, CategoryListView, subscribe, unsubscribe


urlpatterns = [
   path('', PostsList.as_view()),
   path('search/', PostsSearch.as_view()),
   path('post/<int:pk>', PostDetail.as_view(), name='post'),
   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_update'),
   path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
   path('articles/create/', ArticlesCreate.as_view(), name='articles_create'),
   path('articles/<int:pk>/edit/', ArticlesUpdate.as_view(), name='articles_update'),
   path('articles/<int:pk>/delete/', ArticlesDelete.as_view(), name='articles_delete'),
   path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
   path('categories/<int:pk>/unsubscribe', unsubscribe, name='unsubscribe'),
]






