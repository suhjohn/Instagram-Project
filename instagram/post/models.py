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