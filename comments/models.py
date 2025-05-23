from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from novels.models import Novel

class Comment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("User")
    )
    novel = models.ForeignKey(
        Novel,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_("Novel")
    )
    content = models.TextField(verbose_name=_("Content"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies',
        verbose_name=_("Parent Comment")
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        
    def __str__(self):
        return f'{self.user.username} - {self.novel.title}'
