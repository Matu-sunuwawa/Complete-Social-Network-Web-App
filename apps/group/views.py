from django.shortcuts import render, get_object_or_404
from django.views.generic import (
  ListView, CreateView
)
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.contrib.auth.models import User

from django.db.models import Q
from apps.group.models import Group, Membership
from apps.post.models import Post
import time


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
        context = super().get_context_data(**kwargs)
        tab = self.request.GET.get('tab', '')
        context['current_tab'] = tab

        if tab == '':
            joined_groups = self.get_queryset()

            context['posts'] = Post.objects.filter(group__in=joined_groups).exclude(group__isnull=True).select_related('user', 'group').order_by('-created_at')

        if self.request.user.is_authenticated:
            context['joined_group_ids'] = self.request.user.memberships.values_list('group_id', flat=True)
        return context

    def get_template_names(self):
        target = self.request.headers.get('HX-Target')
        if self.request.headers.get('HX-Request'):
            if target == "main-content-area":
                return ['group/partials/group_content.html']
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
            response['HX-Redirect'] = self.success_url
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
