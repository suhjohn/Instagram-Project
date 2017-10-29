from django.core.exceptions import ValidationError


def validate_fb_username(value):
    if len(value) > 3 and value[:2] == "fb_":
        raise ValidationError(
            ('cannot use this username'),
        )
