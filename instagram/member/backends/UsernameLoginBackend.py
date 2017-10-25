
from django.db.models import Q

from member.models import User


class UsernameLoginBackend(object):
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            # Try to fetch the user by searching the username or email field
            user = User.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user

        except User.DoesNotExist:  # Run the default password hasher once to reduce the timing
        # difference between an existing and a non-existing user (#20760).
            User().set_password(password)
