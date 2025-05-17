from django.contrib import admin
from .models import NovelUpload, ChapterUpload, GenreSelection

class ChapterUploadInline(admin.TabularInline):
    model = ChapterUpload
    extra = 0

class GenreSelectionInline(admin.TabularInline):
    model = GenreSelection
    extra = 0

@admin.register(NovelUpload)
class NovelUploadAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'uploaded_at')
    list_filter = ('status', 'uploaded_at')
    search_fields = ('title', 'user__username')
    inlines = [GenreSelectionInline, ChapterUploadInline]

@admin.register(ChapterUpload)
class ChapterUploadAdmin(admin.ModelAdmin):
    list_display = ('title', 'novel_upload', 'chapter_number', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('title', 'novel_upload__title')