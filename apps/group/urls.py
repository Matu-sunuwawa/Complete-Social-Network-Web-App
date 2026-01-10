from django.urls import path
from . import views

app_name = 'group'

urlpatterns = [
  path('', views.grouplist, name="group_list"),
]
