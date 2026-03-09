from django.conf import settings
from django.db import models


class Group(models.Model):
  name = models.CharField(max_length=100)
  description = models.TextField(blank=True)
  created_by = models.ForeignKey(
    settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="created_groups"
  )
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    ordering = ["-updated_at"]

  def __str__(self):
    return self.name[:15]

  @property
  def num_member(self):
    return self.memberships.count()


class Membership(models.Model):
  user = models.ForeignKey(
    settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="memberships"
  )
  group = models.ForeignKey(
    Group, on_delete=models.CASCADE, related_name="memberships"
  )
  joined_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    unique_together = ('user', 'group')

  def __str__(self):
    return f"{self.user} in {self.group}"
