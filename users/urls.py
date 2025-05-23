from django.urls import path
from . import views
from .views import update_avatar

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    # path('profile/<str:username>/', views.profile_detail_view, name='uploader_profile'),
    path('saved/', views.saved_novels, name='saved_novels'),
    path('toggle-save/<int:novel_id>/', views.toggle_save_novel, name='toggle_save_novel'),
    path('avatar/update/', update_avatar, name='update_avatar'),
]
