from django.urls import path
from . import views

app_name = 'novels'

urlpatterns = [
    path('', views.novel_list, name='novel_list'),
    path('<int:novel_id>/', views.novel_detail, name='novel_detail'),
    path('novel/<int:novel_id>/chapter/<int:chapter_id>/', views.chapter_detail, name='chapter_detail'),
]
