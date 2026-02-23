from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.models import User
from apps.group.models import Group
from apps.post.models import Post
import random
import time


class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_template_names(self):
        time.sleep(2)
        trigger_target = self.request.headers.get('HX-Target')
        if self.request.headers.get('HX-Request'):
            if trigger_target == "feed-container":
                return ['core/partials/feed_with_tabs.html']
            if trigger_target == "post-list":
                return ['post/partials/post_list.html']
            if trigger_target == "main-content-area":
                return ['core/partials/home_content.html']
        return [self.template_name]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tab = self.request.GET.get('tab', 'recent')
        posts = Post.objects.all()
        if tab == 'friends':
            following_ids = self.request.user.following.values_list('following_id', flat=True)
            posts = posts.filter(user_id__in=following_ids)
        posts = posts.order_by('-created_at')
        paginator = Paginator(posts, 3)
        page_num = self.request.GET.get('page', 1)
        page_obj = paginator.get_page(page_num)

        context['posts'] = page_obj.object_list
        context['page_obj'] = page_obj
        context['current_tab'] = tab
        return context

class AboutView(TemplateView):
    pass

def custom_404(request, exception=None):
    """Custom 404 error handler."""
    return render(request, 'core/errors/404.html', status=404)

def custom_500(request):
    """Custom 500 error handler."""
    return render(request, 'core/errors/500.html', status=500)


class SearchView(TemplateView):
    template_name = 'core/search.html'

    def get_template_names(self):
        if self.request.headers.get('HX-Request'):
            return ['core/partials/search_content.html']
        return [self.template_name]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', 'all')

        context['query'] = query
        context['search_type'] = search_type

        if query:
            if search_type in ['all', 'users']:
                context['users'] = User.objects.filter(
                    Q(username__icontains=query) |
                    Q(first_name__icontains=query) |
                    Q(last_name__icontains=query)
                ).distinct()[:10]

            if search_type in ['all', 'groups']:
                context['groups'] = Group.objects.filter(
                    Q(name__icontains=query) |
                    Q(description__icontains=query)
                ).distinct()[:10]

            if search_type in ['all', 'posts']:
                context['posts'] = Post.objects.filter(
                    content__icontains=query
                ).order_by('-created_at')[:15]

        return context
