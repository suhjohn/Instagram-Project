from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

# from member.custom_validators import validate_username


User = get_user_model()


class SignUpForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control',
            }
        )
    )
    #clean_<필드이름> 으로 함수를 만들어주어야한다
    def clean_username(self):
        username = self.cleaned_data["username"]
        if " " in username:
            raise ValidationError(
                ('Space in username'),
            )

        if User.objects.filter(username=username).exists():
            raise ValidationError(
                ('Username Already Exists!'),
            )
        return username



