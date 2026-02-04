from django.urls import path
from .views import *

app_name = 'group'

urlpatterns = [
  path('', GroupListView.as_view(), name="group_list"),
  path('group-create', GroupCreateView.as_view(), name="group_create"),
  path('group/<int:pk>/update/', GroupUpdateView.as_view(), name='group_update'),

  path('toggle/<int:pk>/', group_membership_toggle, name="group_toggle"),
]
