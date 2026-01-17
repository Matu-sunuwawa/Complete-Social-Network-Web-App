from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
  ListView, DetailView, CreateView,
  UpdateView, DeleteView
)
from django.http import HttpResponse
from .models import Post, Comment
import time


class PostListView(ListView):
  model = Post
  template_name = 'post/partials/post_list.html'
  context_object_name = 'posts'
  paginate_by = 10

  def get_queryset(self):
    time.sleep(1)
    return super().get_queryset()

  def get_template_names(self):
    if self.request.headers.get('HX-Request'):
      return ['post/partials/post_list.html']

class PostCreateView(CreateView):
  model = Post
  fields = ['content', 'image']

  def get_template_names(self):
    if self.request.headers.get('HX-Request'):
      return ['post/partials/post_create.html']

  def form_valid(self, form):
    form.instance.user = self.request.user
    self.object = form.save()

    if self.request.headers.get('HX-Request'):
        posts = Post.objects.all()
        return render(self.request, 'core/partials/home.html', {'posts': posts})

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

class PostDeleteView(DeleteView):
  model = Post

  def get_template_names(self):
    if self.request.headers.get('HX-Request'):
      return ['post/partials/post_delete.html']

  def delete(self, request, *args, **kwargs):
    self.object = self.get_object()
    self.object.delete()

    if self.request.headers.get('HX-Request'):
        return HttpResponse("")

    return super().delete(request, *args, **kwargs)

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

def comment_create(request,pk):
  post = get_object_or_404(Post, pk=pk)

  if request.method == "POST":
    content = request.POST["content"]
    comment = Comment.objects.create(
      user = request.user,
      post = post,
      content = content
    )
    if request.headers.get('HX-Request'):
      return render(request, 'post/partials/comment.html', {"comment":comment})
