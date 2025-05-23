from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Name"))

    def __str__(self):
        return self.name

class Novel(models.Model):
    STATUS_CHOICES = [
        ('ongoing', _('Đang tiến hành')),
        ('completed', _('Hoàn thành')),
    ]

    title = models.CharField(max_length=255, verbose_name=_("Title"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    author = models.CharField(max_length=255, blank=True, verbose_name=_("Author"))
    cover_image = models.ImageField(upload_to='uploads/covers/', blank=True, null=True, verbose_name=_("Cover Image"))
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ongoing', verbose_name=_("Status"))
    genres = models.ManyToManyField(Genre, related_name='novels', verbose_name=_("Genres"))
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='uploaded_novels', null=True, verbose_name=_("Uploaded By"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    def __str__(self):
        return self.title

class Chapter(models.Model):
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE, related_name='chapters', verbose_name=_("Novel"))
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    content = models.TextField(verbose_name=_("Content"))
    chapter_number = models.PositiveIntegerField(default=1, verbose_name=_("Chapter Number"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    class Meta:
        ordering = ['chapter_number']

    def __str__(self):
        return f"{self.novel.title} - {_('Chapter')} {self.chapter_number}"

class SavedNovel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_novels', verbose_name=_("User"))
    novel = models.ForeignKey('Novel', on_delete=models.CASCADE, related_name='saved_by_users', verbose_name=_("Novel"))
    saved_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Saved At"))

    class Meta:
        unique_together = ('user', 'novel')

    def __str__(self):
        return f"{self.user.username} {_('saved')} {self.novel.title}"
