from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.views.generic import (
  DetailView, UpdateView, DeleteView
)
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from .models import UserProfile, Follow
from apps.post.models import Post
import time


class ProfileDetailView(DetailView):
  model = User
  template_name = 'user/profile.html'
  context_object_name = 'profile_user'
  slug_field = 'username'
  slug_url_kwarg = 'username'

  def get_template_names(self):
      trigger_target = self.request.headers.get('HX-Target')
      if self.request.headers.get('HX-Request'):
          if trigger_target == "main-content-area":
              return ['user/partials/profile_content.html']
          return ['post/partials/post_list.html']
      return [self.template_name]

  def get_context_data(self, **kwargs):
      time.sleep(1)
      context = super().get_context_data(**kwargs)
      profile_user = self.get_object()
      posts = Post.objects.filter(user=profile_user).order_by('-created_at')
      paginator = Paginator(posts, 3)
      page_num = self.request.GET.get('page',1)
      page_obj = paginator.get_page(page_num)

      context['posts'] = page_obj.object_list
      context['page_obj'] = page_obj
      return context

class ProfileUpdateView(UpdateView):
  model = UserProfile
  template_name = 'user/partials/edit_profile_info.html'
  fields = ['bio', 'profile_pic']

  def get_object(self):
    return self.request.user.profile

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    if self.request.POST:
      context['username_val']=self.request.POST.get('username')
    else:
      context['username_val']=self.request.user.username
    return context

  def form_valid(self, form):
    new_username = self.request.POST.get('username')
    if new_username:
        self.request.user.username = new_username
        self.request.user.save()

    self.object = form.save()

    if self.request.headers.get('HX-Request'):
        profile_info_html = render_to_string('user/partials/profile_info.html', {
            'profile_user': self.request.user,
            'request': self.request
        })
        sidebar_info_html = render_to_string('core/includes/_sidebar_user_info.html', {
            'request': self.request
        })
        return HttpResponse(profile_info_html + sidebar_info_html)

    return super().form_valid(form)

class ProfileDeleteView(DeleteView):
  model = UserProfile
  success_url = reverse_lazy('core:home')

  def get_object(self):
    return self.request.user.profile

  def delete(self, request, *args, **kwargs):
    user = request.user
    user.is_active = False
    user.save()

    if self.request.headers.get('HX-Request'):
        response = HttpResponse("")
        response['HX-Redirect'] = self.success_url
        return response
    return super().delete(request, *args, **kwargs)


def follow_toggle(request, username):
  user_to_follow = get_object_or_404(User, username=username)
  follow_rel = Follow.objects.filter(follower=request.user, following=user_to_follow)

  if follow_rel:
    follow_rel.delete()
    action = "Follow"
    btn_class = "btn-outline-primary"
  else:
     Follow.objects.create(follower=request.user, following=user_to_follow)
     action = "Unfollow"
     btn_class = "btn-primary"

  if request.headers.get('HX-Request'):
    post_url = reverse('user:follow_user', kwargs={'username':username})
    return HttpResponse(f"""
        <button class="btn {btn_class} btn-sm"
                hx-post="{post_url}"
                hx-target="this"
                hx-swap="outerHTML">
            {action}
        </button>
    """)

  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# def user_following_list(request, username):
#   profile_user = get_object_or_404(User, username=username)
#   following_list = User.objects.filter(followers__follower=profile_user)

#   context = {
#       'profile_user': profile_user,
#       'following_list': following_list,
#   }

#   if request.headers.get('HX-Request'):
#       return render(request, 'user/partials/following_tab.html', context)
#   return HttpResponseRedirect(reverse('user:profile_detail', args=[username]))

def user_following_list(request, username):
    profile_user = get_object_or_404(User, username=username)
    following_list = User.objects.filter(followers__follower=profile_user)

    current_user_following_ids = []
    if request.user.is_authenticated:
        current_user_following_ids = request.user.following.values_list('following_id', flat=True)

    context = {
        'profile_user': profile_user,
        'following_list': following_list,
        'current_user_following_ids': current_user_following_ids,
    }

    if request.headers.get('HX-Request'):
        return render(request, 'user/partials/following_tab.html', context)
    return HttpResponseRedirect(reverse('user:profile_detail', args=[username]))

def user_followers_list(request, username):
    profile_user = get_object_or_404(User, username=username)
    followers_list = User.objects.filter(following__following=profile_user)

    current_user_following_ids = []
    if request.user.is_authenticated:
        current_user_following_ids = request.user.following.values_list('following_id', flat=True)

    context = {
        'profile_user': profile_user,
        'followers_list': followers_list,
        'current_user_following_ids': current_user_following_ids,
    }

    if request.headers.get('HX-Request'):
        return render(request, 'user/partials/followers_tab.html', context)
    return HttpResponseRedirect(reverse('user:profile_detail', args=[username]))
