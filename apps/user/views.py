from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import (
  DetailView, UpdateView, DeleteView
)
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .models import UserProfile


class ProfileDetailView(DetailView):
  model = User
  template_name = 'user/profile.html'
  context_object_name = 'profile_user'
  slug_field = 'username'
  slug_url_kwarg = 'username'

  def get_template_names(self):
    if self.request.headers.get('HX-Request'):
      return ['user/partials/profile_content.html']
    return [self.template_name]

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['posts'] = self.object.posts.all().order_by('-created_at')
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
        return render(self.request, 'user/partials/profile_info.html', {
            'profile_user': self.request.user
        })
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
