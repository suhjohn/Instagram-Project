# from django.core.exceptions import ValidationError, FieldError
# from django.utils.translation import ugettext_lazy as _
# from django.contrib.auth import get_user_model
#
# User = get_user_model()
#
#
# def validate_username(value):
#     if " " in value:
#         raise ValidationError(
#             ('Space in username'),
#         )
#
#     if User.objects.filter(username=value).exists():
#         raise ValidationError(
#             ('Username Already Exists!'),
#         )
#     # pass