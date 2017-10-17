from django import forms
from django.contrib.auth import get_user_model, authenticate, login as django_login
from django.core.exceptions import ValidationError

# from member.custom_validators import validate_username


User = get_user_model()


class SignUpForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    # clean_<필드이름> 으로 함수를 만들어주어야한다
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


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        self.user = authenticate(
            username=username,
            password=password,
        )
        if not self.user:
            raise ValidationError(
                'Invalid Login credentials'
            )
        # if를 패스하면 self에 대해 login이라는 이름으로 self._login 함수를 부를 수 있도록 설정
        else:
            setattr(self, 'login', self._login)
    
    def _login(self, request):
        django_login(request, self.user)

