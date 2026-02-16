from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from django.core.paginator import Paginator
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
