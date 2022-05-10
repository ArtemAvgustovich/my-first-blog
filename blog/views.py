from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post
from .forms import PostForm

class IndexView(ListView):
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_queryset(self):
        """
        Excludes any posts that aren't published yet.
        """
        return Post.objects.filter(published_date__lte=timezone.now())


class PostNew(LoginRequiredMixin, CreateView):
    model = Post
    fields =  ('title', 'text')
    template_name = 'blog/post_edit.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.published_date = timezone.now()
        return super().form_valid(form)


class PostEdit(LoginRequiredMixin, UpdateView):
    model = Post
    fields =  ('title', 'text')
    template_name_suffix = '_edit'
    
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if request.user == post.author:
            return super().get(request, pk)
        return HttpResponseForbidden("Access denied! You can't edit other user's posts.")

    def form_valid(self, form):
        if self.request.user == form.instance.author:
            form.instance.published_date = timezone.now()
            return super().form_valid(form)
        return HttpResponseForbidden("Access denied! You can't edit other user's posts.")

