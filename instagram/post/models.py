from django.db import models

# Create your models here.

class Post(models.Model):
    photo = models.ImageField(
        upload_to='post',
        blank=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

class PostComment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
    )
    content = models.TextField()
    created_at = models.DateTimeField(
        auto_now_add=True
    )
