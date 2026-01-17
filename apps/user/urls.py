from django.urls import path
from .views import *

app_name = 'user'

urlpatterns = [
    path('profile/<str:username>/', ProfileDetailView.as_view(), name="profile_detail"),
    path('edit-profile/', ProfileUpdateView.as_view(), name="profile_update"),
    path('delete-profile/', ProfileDeleteView.as_view(), name="profile_delete"),
]
