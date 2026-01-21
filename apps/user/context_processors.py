from django.contrib.auth.models import User
from apps.group.models import Group


def suggested_users(request):
  if request.user.is_authenticated:
    following_ids = request.user.following.values_list('following_id', flat=True)
    suggested = User.objects.exclude(id=request.user.id).exclude(id__in=following_ids)[:5]
    return {'suggested_users':suggested}
  return {'suggested_users': []}

def sidebar_data(request):
    if request.user.is_authenticated:
        following_ids = request.user.following.values_list('following_id', flat=True)
        suggested_people = User.objects.exclude(id=request.user.id).exclude(id__in=following_ids).order_by('?')[:5]
        following = User.objects.filter(followers__follower=request.user)

        joined_group_ids = request.user.memberships.values_list('group_id', flat=True)
        suggested_groups = Group.objects.exclude(id__in=joined_group_ids).order_by('?')[:3]

        return {
            'suggested_users': suggested_people,
            'following_users': following,
            'suggested_groups': suggested_groups,
        }
    return {}
