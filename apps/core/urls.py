from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('search/', views.SearchView.as_view(), name='search'),

    path('error/404/', views.custom_404, name='error_404'),
    path('error/500/', views.custom_500, name='error_500'),
]
