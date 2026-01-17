
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls

handler404 = 'apps.core.views.custom_404'
handler500 = 'apps.core.views.custom_500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls', namespace='core')),
    path('posts/', include('apps.post.urls', namespace='post')),
    path('groups/', include('apps.group.urls', namespace='group')),
    path('user/', include('apps.user.urls', namespace='user')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += debug_toolbar_urls()
