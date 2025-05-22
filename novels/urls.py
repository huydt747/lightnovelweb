from django.urls import path
from . import views

app_name = 'novels'

urlpatterns = [
    path('', views.novel_list, name='novel_list'),
    path('<int:novel_id>/', views.novel_detail, name='novel_detail'),
    path('<int:novel_id>/chapter/<int:chapter_id>/', views.chapter_detail, name='chapter_detail'),
    path('genre/<int:genre_id>/', views.genre_filter, name='genre_filter'),
    path('original/', views.original_novels, name='original'),
    path('search/', views.search_novels, name='search'),
]
