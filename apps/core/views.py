from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from django.core.paginator import Paginator
from apps.post.models import Post
import random
import time


class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_template_names(self):
        if self.request.headers.get('HX-Request'):
            return ['core/partials/home.html']
        return [self.template_name]

    def get_context_data(self, **kwargs):
        time.sleep(2)
        context = super().get_context_data(**kwargs)
        posts = list(Post.objects.all())
        random.shuffle(posts)
        paginator = Paginator(posts, 3)
        page_num = self.request.GET.get('page',1)
        page_obj = paginator.get_page(page_num)

        context['posts'] = page_obj.object_list
        context['page_obj'] = page_obj
        return context

class AboutView(TemplateView):
    pass

def custom_404(request, exception=None):
    """Custom 404 error handler."""
    return render(request, 'core/errors/404.html', status=404)

def custom_500(request):
    """Custom 500 error handler."""
    return render(request, 'core/errors/500.html', status=500)
