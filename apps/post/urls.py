from django.urls import path
from .views import *

app_name = 'post'

urlpatterns = [
  path('create/', PostCreateView.as_view(), name="post_create"),
  path('feed/', FeedListView.as_view(), name="feed_list"),
  path('<int:pk>/', PostDetailView.as_view(), name="post_detail"),
  path('<int:pk>/update/', PostUpdateView.as_view(), name="post_update"),
  path('<int:pk>/delete/', PostDeleteView.as_view(), name="post_delete"),

  path('<int:pk>/like/', like_post, name="like_post"),
  path('<int:pk>/comment/', comment_create, name="comment_create")
]
