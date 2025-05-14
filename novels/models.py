from django.db import models
from django.utils.text import slugify
from django.utils import timezone

class Novel(models.Model):
    STATUS_CHOICES = [
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    author = models.CharField(max_length=255, blank=True)
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ongoing')
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Removed default
    updated_at = models.DateTimeField(auto_now_add=True)  # Removed default

    def generate_unique_slug(self):
        base_slug = slugify(self.title)
        slug = base_slug
        num = 1
        while Novel.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{num}"
            num += 1
        return slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Chapter(models.Model):
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=255)
    content = models.TextField()
    chapter_number = models.PositiveIntegerField(default=1)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Removed default

    class Meta:
        ordering = ['chapter_number']

    def generate_unique_slug(self):
        base_slug = slugify(f"{self.novel.title}-chapter-{self.chapter_number}")
        slug = base_slug
        num = 1
        while Chapter.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{num}"
            num += 1
        return slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.novel.title} - Chapter {self.chapter_number}"


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class NovelGenre(models.Model):
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('novel', 'genre')