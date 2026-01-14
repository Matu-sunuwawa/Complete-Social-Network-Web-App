from django import template

register = template.Library()

@register.filter
def post_has_likes(post, user):
  """Check the post has like"""
  return post.likes.filter(user=user).exists()
