from django.shortcuts import render
from django.views.generic import (
  ListView
)


class PostListView(ListView):
  pass

def postlist(request):
  return render(request, 'post/post_list.html')
