from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import (
  ListView, DetailView, CreateView,
  UpdateView, DeleteView
)
from django.http import HttpResponse
from .models import Post, Comment
import time, json


class PostCreateView(CreateView):
    model = Post
    fields = ['content', 'image']

    def get_template_names(self):
        if self.request.headers.get('HX-Request'):
            return ['post/partials/post_create.html']
        return ['post/post_form.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tab = self.request.GET.get('tab', '')
        context['group_id'] = self.request.GET.get('group_id')
        context['current_tab'] = tab
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        group_id = self.request.GET.get('group_id')
        if group_id:
            form.instance.group_id = group_id
        self.object = form.save()

        if self.request.headers.get('HX-Request'):
            response = HttpResponse()
            if self.object.group:
                success_url = f"{reverse('group:group_list')}?tab=group_detail&group_id={self.object.group.id}"
            else:
                success_url = reverse('core:home')
            response['HX-Location'] = json.dumps({
                'path': success_url,
                'target': '#main-content-area'
            })
            response['HX-Trigger'] = 'closeModal'
            return response

        return super().form_valid(form)

class PostDetailView(DetailView):
  context_object_name = 'post'
  model = Post
  template_name = 'post/post_detail.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['back_url'] = self.request.GET.get('next', reverse_lazy('core:home'))
    return context

  def get_template_names(self):
    time.sleep(1)
    if self.request.headers.get('HX-Request'):
      return ['post/partials/post_detail.html']
    return [self.template_name]

class PostUpdateView(UpdateView):
  model = Post
  fields = ['content', 'image']
  template_name = 'post/post_update.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['back_url'] = self.request.GET.get('next', reverse('core:home'))
    return context

  def get_template_names(self):
    if self.request.headers.get('HX-Request'):
      return ['post/partials/post_update.html']
    return [self.template_name]

  def form_valid(self, form):
    self.object = form.save()

    if self.request.headers.get('HX-Request'):
        next_url = self.request.GET.get('next', reverse('core:home'))
        response = HttpResponse()
        response['HX-Location'] = next_url
        return response

    return super().form_valid(form)

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


class FeedListView(ListView):
  model = Post
  template_name = "post/feed.html"
  context_object_name = 'posts'
  paginate_by = 4

  def get_queryset(self):
    time.sleep(2)
    return Post.objects.filter(likes__user=self.request.user).order_by('-likes__created_at')

  def get_template_names(self):
    trigger_target = self.request.headers.get('HX-Target')
    if self.request.headers.get('HX-Request'):
      if trigger_target == "main-content-area":
        return ['post/partials/feed_content.html']
      return ['post/partials/post_list.html']
    return [self.template_name]


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
