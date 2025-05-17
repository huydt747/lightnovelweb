from django.urls import path
from . import views

urlpatterns = [
    path('novel/create/', views.upload_novel, name='upload_novel'),
    path('novel/<int:novel_upload_id>/chapter/', views.upload_chapter, name='upload_chapter'),
    path('my-uploads/', views.my_uploads, name='my_uploads'),
    path('novel/<int:novel_upload_id>/edit/', views.edit_novel_upload, name='edit_novel_upload'),
    path('chapter/<int:chapter_id>/edit/', views.edit_chapter, name='edit_chapter'),
]