from django.shortcuts import render, get_object_or_404
from django.views.generic import (
  ListView, CreateView,
  UpdateView
)
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.contrib.auth.models import User

from django.db.models import Q
from apps.group.models import Group, Membership
from apps.post.models import Post
import time, json


class GroupListView(ListView):
    model = Group
    template_name = 'group/group.html'
    context_object_name = 'groups'

    def get_queryset(self):
        user = self.request.user
        tab = self.request.GET.get('tab', '')

        if tab == 'discover':
            return Group.objects.exclude(memberships__user=user)
        return Group.objects.filter(Q(created_by=user) | Q(memberships__user=user)).distinct()

    def get_context_data(self, **kwargs):
        time.sleep(1)
        context = super().get_context_data(**kwargs)
        tab = self.request.GET.get('tab', '')
        group_id = self.request.GET.get('group_id')
        context['back_tab'] = self.request.GET.get('source', '')
        context['current_tab'] = tab

        if tab == '' or tab == 'group_detail':
            if tab == 'group_detail' and group_id:
                current_group = get_object_or_404(Group, id=group_id)
                context['current_group'] = current_group
                posts = Post.objects.filter(group=current_group)
            else:
                joined_groups = self.get_queryset()
                posts = Post.objects.filter(group__in=joined_groups).exclude(group__isnull=True)

            posts = posts.select_related('user', 'group').order_by('-created_at')

            paginator = Paginator(posts, 3)
            page_num = self.request.GET.get('page', 1)
            page_obj = paginator.get_page(page_num)

            context['posts'] = page_obj.object_list
            context['page_obj'] = page_obj

        if self.request.user.is_authenticated:
            context['joined_group_ids'] = self.request.user.memberships.values_list('group_id', flat=True)
        return context

    def get_template_names(self):
        target = self.request.headers.get('HX-Target')
        tab = self.request.GET.get('tab', '')
        if self.request.headers.get('HX-Request'):
            if target == "main-content-area":
                return ['group/partials/group_content.html']
            if tab == '' or tab == 'group_detail':
                return ['post/partials/post_list.html']
            return ['group/partials/group_list.html']
        return [self.template_name]

class GroupCreateView(CreateView):
    model = Group
    fields = ['name', 'description']
    template_name = 'group/partials/group_form.html'
    success_url = reverse_lazy('group:group_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        self.object = form.save()

        Membership.objects.create(user=self.request.user, group=self.object)

        if self.request.headers.get('HX-Request'):
            response = HttpResponse()
            response['HX-Location'] = json.dumps({
                'path': self.get_success_url(),
                'target': '#main-content-area'
            })
            response['HX-Trigger'] = 'closeModal'
            return response

        return super().form_valid(form)

class GroupUpdateView(UpdateView):
    model = Group
    fields = ['name', 'description']
    template_name = 'group/partials/group_form.html'

    def test_func(self):
        group = self.get_object()
        return self.request.user == group.created_by

    def get_success_url(self):
        return f"{reverse('group:group_list')}?tab=group_detail&group_id={self.object.id}"

    def form_valid(self, form):
        self.object = form.save()
        if self.request.headers.get('HX-Request'):
            response = HttpResponse()
            response['HX-Location'] = json.dumps({
                'path': self.get_success_url(),
                'target': '#main-content-area'
            })
            response['HX-Trigger'] = 'closeModal'
            return response
        return super().form_valid(form)


def group_membership_toggle(request, pk):
    group = get_object_or_404(Group, pk=pk)
    membership = Membership.objects.filter(user=request.user, group=group)

    if membership.exists():
        membership.delete()
        action = "Join"
        btn_class = "btn-outline-success"
    else:
        Membership.objects.create(user=request.user, group=group)
        action = "Leave"
        btn_class = "btn-success"

    if request.headers.get('HX-Request'):
        toggle_url = reverse('group:group_toggle', kwargs={'pk': pk})
        return HttpResponse(f"""
            <button class="btn {btn_class} btn-sm rounded-pill px-3"
                    hx-post="{toggle_url}"
                    hx-target="this"
                    hx-swap="outerHTML">
                {action}
            </button>
        """)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
