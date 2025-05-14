from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from novels import views as novel_views

urlpatterns = [
    path('admin', admin.site.urls),
    path('', novel_views.novel_list, name='home'),
    path('novels/', include('novels.urls')),
    path('users/', include(('users.urls', 'users'), namespace='users')),
    # path('comments/', include('comments.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
