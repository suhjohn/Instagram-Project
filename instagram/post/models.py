from django.db import models

# Create your models here.
from config import settings


class PostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(author__isnull=False)


class Post(models.Model):
    objects = PostManager()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    photo = models.ImageField(
        upload_to='post',
        blank=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = [
            "-created_at",
        ]
    def __str__(self):
        return self.pk


class PostComment(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    content = models.TextField(
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.content

    class Meta:
        ordering = [
            "created_at",
        ]
