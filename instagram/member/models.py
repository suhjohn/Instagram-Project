from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.db import models



class UserManager(DjangoUserManager):
    def create_superuser(self, *args, **kwargs):
        return super().create_superuser(age=30, *args, **kwargs)

# Create your models here.
class User(AbstractUser):
    img_profile = models.ImageField(
        upload_to='user',
        blank=True,
    )
    age = models.IntegerField('나이')
    # like_posts = models.ManyToManyField(
    #     'post.Post',
    #     verbose_name='좋아요 누른 포스트 목록',
    #
    # )
    objects= UserManager()

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural= f'{verbose_name} 목록'

    # def like_post(self, post):
    #     """
    #     자신의 like_posts에 해당내용 추가
    #     :param post:
    #     :return:
    #     """
    #     self.like_posts.add(post=post)

    #Createsuperuser를 할 때 물어보는 항목 추가
    # REQUIRED_FIELDS = AbstractUser.REQUIRED_FIELDS + ['age']
