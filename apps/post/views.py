from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
  ListView, DetailView, CreateView,
  UpdateView
)
from .models import Post
import time


class PostListView(ListView):
  pass

class PostCreateView(CreateView):
  model = Post
  fields = ['content', 'image']

  def form_valid(self, form):
    form.instance.user = self.request.user
    self.object = form.save()
    return super().form_valid(form)

  def get_success_url(self):
    return reverse_lazy('core:home')

class PostDetailView(DetailView):
  context_object_name = 'post'
  model = Post

  def get_template_names(self):
    time.sleep(1)
    if self.request.headers.get('HX-Request'):
      return ['post/partials/post_detail.html']

class PostUpdateView(UpdateView):
  model = Post
  fields = ['content', 'image']

  def get_template_names(self):
    if self.request.headers.get('HX-Request'):
      return ['post/partials/post_update.html']

  def get_success_url(self):
    return reverse_lazy('core:home')

def like_post(request, pk):
  post = get_object_or_404(Post, pk=pk)
  like, created = post.likes.get_or_create(user=request.user, post=post)
  if not created:
    like.delete()

  if request.headers.get('HX-Request'):
    return render(request, 'post/partials/like_button.html', {
      'post': post,
      'user': request.user
    })
