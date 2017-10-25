
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager, PermissionsMixin
from django.utils.translation import ugettext as _
from django.core.mail import send_mail
from django.utils import six, timezone
from django.contrib.auth.validators import UnicodeUsernameValidator, ASCIIUsernameValidator
from django.db import models

class UserManager(DjangoUserManager):
    def create_superuser(self, *args, **kwargs):
        return super().create_superuser(age=30, *args, **kwargs)


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """
    username_validator = UnicodeUsernameValidator() if six.PY3 else ASCIIUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    # Facebook
    USER_TYPE_FACEBOOK = 'f'
    USER_TYPE_DJANGO = 'd'
    CHOICES_USER_TYPE = (
        (USER_TYPE_FACEBOOK, 'Facebook'),
        (USER_TYPE_DJANGO, 'Django'),
    )
    user_type = models.CharField(
        max_length=1,
        choices=CHOICES_USER_TYPE,
    )

    # Additional personal info
    img_profile = models.ImageField(
        upload_to='user',
        blank=True,
    )
    age = models.IntegerField(
        '나이',
        blank=True,
    )
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

    def follow_toggle(self, user):
        """

        :param user:
        :return:
        """
        if not isinstance(user, User):
            raise ValueError("'user' must be a User instance.")

        relation, relation_created = self.following_user_relations.get_or_create(to_user=user)
        if relation_created:
            return True

        relation.delete()
        return False

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
