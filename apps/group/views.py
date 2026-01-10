from django.shortcuts import render
from django.views.generic import (
  ListView
)


class GroupListView(ListView):
  pass

def grouplist(request):
  return render(request, 'group/group_list.html')
