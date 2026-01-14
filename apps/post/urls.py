from django.urls import path
from .views import *

app_name = 'post'

urlpatterns = [
  path('', PostListView.as_view(), name="post_list"),
  path('create/', PostCreateView.as_view(), name="post_create"),
  path('<int:pk>/', PostDetailView.as_view(), name="post_detail"),
  path('<int:pk>/update/', PostUpdateView.as_view(), name="post_update"),

  path('<int:pk>/like/', like_post, name="like_post"),
]
