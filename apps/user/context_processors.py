from django.contrib.auth.models import User


def suggested_users(request):
  if request.user.is_authenticated:
    following_ids = request.user.following.values_list('following_id', flat=True)
    suggested = User.objects.exclude(id=request.user.id).exclude(id__in=following_ids)[:5]
    return {'suggested_users':suggested}
  return {'suggested_users': []}
