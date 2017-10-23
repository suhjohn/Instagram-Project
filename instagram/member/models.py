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
    like_posts = models.ManyToManyField(
        'post.Post',
        verbose_name='좋아요 누른 포스트 목록',
        related_name='liked_user'
    )
    # 내가 팔로우 하고 있는 유저 목록

    # 나를 follow하고 있는 사람 목록
    #   followers
    # 내가 follow하고 있는 사람 목록은
    #   followed_users
    following_users = models.ManyToManyField(
        'self',
        through='Relation',
        symmetrical=False,
        related_name='followers',
    )


    objects = UserManager()

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = f'{verbose_name} 목록'

    def like_post(self, post):
        """자신의 like_posts에 해당내용 추가
        :param post:
        :return:
        """
        self.like_posts.add(post=post)

        # Createsuperuser를 할 때 물어보는 항목 추가
        # REQUIRED_FIELDS = AbstractUser.REQUIRED_FIELDS + ['age']

class Relation(models.Model):
    """
    User의 follow 목록을 가질 수 있도록 MTM의 중개모델 구성
    from_user, to_user
    """
    from_user = models.ForeignKey(
        User,
        related_name='following_users_relations',
        on_delete=models.CASCADE,
    )
    to_user = models.ForeignKey(
        User,
        related_name='follower_relations',
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
