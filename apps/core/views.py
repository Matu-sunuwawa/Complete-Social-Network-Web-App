from django.shortcuts import render
from django.views.generic import TemplateView, FormView

class HomeView(TemplateView):
    template_name = 'core/home.html'

class AboutView(TemplateView):
    pass

def custom_404(request, exception=None):
    """Custom 404 error handler."""
    return render(request, 'core/errors/404.html', status=404)

def custom_500(request):
    """Custom 500 error handler."""
    return render(request, 'core/errors/500.html', status=500)
