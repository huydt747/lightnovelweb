from django.db import models
from django.conf import settings
from novels.models import Novel, Chapter, Genre

class NovelUpload(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'), 
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='uploads')
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.CharField(max_length=255)
    cover_image = models.ImageField(upload_to='uploads/covers/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='approved')
    novel = models.ForeignKey(Novel, on_delete=models.SET_NULL, null=True, blank=True, related_name='uploads')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} by {self.user.username}"
    
    def get_genres(self):
        return ChapterUpload.objects.filter(novel_upload=self)

class ChapterUpload(models.Model):
    novel_upload = models.ForeignKey(NovelUpload, on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=255)
    content = models.TextField()
    chapter_number = models.PositiveIntegerField(default=1)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['chapter_number']
    
    def __str__(self):
        return f"{self.novel_upload.title} - Chapter {self.chapter_number}"

class GenreSelection(models.Model):
    novel_upload = models.ForeignKey(NovelUpload, on_delete=models.CASCADE, related_name='genre_selections')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('novel_upload', 'genre')
        
    def __str__(self):
        return f"{self.novel_upload.title} - {self.genre.name}"