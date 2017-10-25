from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from member.forms import SignUpForm
from member.models import User


class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional info', {'fields': (
            'img_profile',
            'age',
            'user_type',
            'like_posts',
        )}),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional info', {'fields': (
            'email',
            'first_name',
            'last_name',
        )}),
    )


admin.site.register(User, UserAdmin)
