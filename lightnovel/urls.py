from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _

from novels import views as novel_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),  
    path('', novel_views.novel_list, name='home'),
    path('novels/', include('novels.urls')),
    path('users/', include(('users.urls', 'users'), namespace='users')),
    path('uploads/', include('uploads.urls')),
    path('original/', novel_views.original_novels, name='original'),
    path('published/', novel_views.published_novels, name='published'),
    path('guidelines/', novel_views.guidelines, name='guidelines'),
    # path('comments/', include('comments.urls')),

      
]

urlpatterns += i18n_patterns(
    path('', include('novels.urls')),
    path('users/', include('users.urls')),
    prefix_default_language=True  # Hiển thị /vi/ cho tiếng Việt
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
