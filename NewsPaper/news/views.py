from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView

from .forms import PostForm
from .models import Post, POST_NEWS, POST_ARTICLE, Category
from .filters import PostsSearchFilter

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required

from django.core.cache import cache
import logging


logger = logging.getLogger(__name__)


class PostsList(ListView):
    model = Post
    ordering = 'create_date_time'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def setup(self, request, *args, **kwargs):
        logger.info('INFO')
        super(PostsList, self).setup(request, *args, **kwargs)


    def get_queryset(self):
        logger.info('INFO')
        return super().get_queryset()


class PostsSearch(ListView):
    model = Post
    ordering = 'create_date_time'
    template_name = 'search.html'
    context_object_name = 'posts'
    paginate_by = 5

    # def setup(self, request, *args, **kwargs):
    #     super(PostsList, self).setup(request, *args, **kwargs)
    #     logger.info('INFO')

    def get_queryset(self):
        logger.info('INFO')
        queryset = super().get_queryset()
        self.filterset = PostsSearchFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        logger.info('INFO')
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
            return obj


class NewsCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    raise_exception = True
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = POST_NEWS
        post._rating = 0
        return super().form_valid(form)

    success_url = '/news'


class NewsUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    raise_exception = True
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

    success_url = '/news'


class NewsDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    raise_exception = True
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'news_delete.html'
    success_url = '/news'


class ArticlesCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    raise_exception = True
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'articles_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = POST_ARTICLE
        post._rating = 0
        return super().form_valid(form)

    success_url = '/news'


class ArticlesUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    raise_exception = True
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'articles_edit.html'

    success_url = '/news'


class ArticlesDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    raise_exception = True
    model = Post
    template_name = 'articles_delete.html'
    success_url = '/news'


class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-create_date_time')
        return queryset

    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        contex['is_not_subscriber'] = self.request.user not in self.category.subcribers.all()
        contex['category'] = self.category
        return contex


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subcribers.add(user)

    message = f'Подписались на категорию {category}'
    return redirect(request.META['HTTP_REFERER'])
        # render(request, 'subscribe.html', {'category':category, 'message': message})


@login_required
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subcribers.remove(user)

    message = f'Отписались от категории {category}'
    return redirect(request.META['HTTP_REFERER'])
        # render(request, 'unsubscribe.html', {'category':category, 'message': message})
