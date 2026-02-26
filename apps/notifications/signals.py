from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from apps.post.models import Like, Comment
from apps.user.models import Follow
from .models import Notification

def send_notification_email(recipient, subject, message):
    """Utility to send emails safely"""
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [recipient.email],
            fail_silently=True,
        )
    except Exception:
        pass

@receiver(post_save, sender=Like)
def notify_like(sender, instance, created, **kwargs):
    if created and instance.user != instance.post.user:
        Notification.objects.create(
            recipient=instance.post.user,
            sender=instance.user,
            notification_type='like',
            post=instance.post,
            text_preview=f"{instance.user.username} liked your post."
        )
        send_notification_email(
            instance.post.user,
            "New Like!",
            f"Hey {instance.post.user.username}, {instance.user.username} liked your post."
        )

@receiver(post_save, sender=Comment)
def notify_comment(sender, instance, created, **kwargs):
    if created and instance.user != instance.post.user:
        Notification.objects.create(
            recipient=instance.post.user,
            sender=instance.user,
            notification_type='comment',
            post=instance.post,
            text_preview=f"{instance.user.username} commented on your post."
        )
        send_notification_email(
            instance.post.user,
            "New Comment!",
            f"{instance.user.username} said: {instance.content[:30]}..."
        )

@receiver(post_save, sender=Follow)
def notify_follow(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            recipient=instance.following,
            sender=instance.follower,
            notification_type='follow',
            text_preview=f"{instance.follower.username} started following you."
        )
