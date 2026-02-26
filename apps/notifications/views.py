from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from .models import Notification

class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'notifications/notification_list.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        qs = Notification.objects.filter(recipient=self.request.user)
        qs.filter(is_read=False).update(is_read=True)
        return qs

    def get_template_names(self):
        if self.request.headers.get('HX-Request'):
            return ['notifications/partials/notification_content.html']
        return [self.template_name]

def unread_notification_count(request):
    if not request.user.is_authenticated:
        return HttpResponse("")
    count = request.user.notifications.filter(is_read=False).count()
    return render(request, 'notifications/partials/unread_badge.html', {'unread_count': count})
