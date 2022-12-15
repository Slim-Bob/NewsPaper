from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView

from .forms import PostForm
from .models import Post, POST_NEWS, POST_ARTICLE
from .filters import PostsSearchFilter

from django.http import HttpResponse, HttpResponseRedirect


class PostsList(ListView):
    model = Post
    ordering = 'create_date_time'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostsSearch(ListView):
    model = Post
    ordering = 'create_date_time'
    template_name = 'search.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostsSearchFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


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