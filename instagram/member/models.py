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
    age = models.IntegerField()

    objects= UserManager()

    #Createsuperuser를 할 때 물어보는 항목 추가
    # REQUIRED_FIELDS = AbstractUser.REQUIRED_FIELDS + ['age']
