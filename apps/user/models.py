from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
  bio = models.TextField(blank=True)
  profile_pic = models.ImageField(upload_to="profile_pics/", blank=True, null=True)

  def __str__(self):
    return self.user.username

  @property
  def followers_count(self):
    return self.user.followers.count()

  @property
  def following_count(self):
    return self.user.following.count()

class Follow(models.Model):
  follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
  following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    unique_together = ('follower', 'following')

  def __str__(self):
    return f"{self.follower} follows {self.following}"
