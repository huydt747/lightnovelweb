from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


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
    genres = models.ManyToManyField(Genre, related_name='novels')  # ManyToMany trực tiếp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Dùng auto_now để cập nhật khi edit

    def __str__(self):
        return self.title


class Chapter(models.Model):
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=255)
    content = models.TextField()
    chapter_number = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['chapter_number']

    def __str__(self):
        return f"{self.novel.title} - Chapter {self.chapter_number}"
