from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('saved/', views.saved_novels, name='saved_novels'),
    path('toggle-save/<int:novel_id>/', views.toggle_save_novel, name='toggle_save_novel'),
]
