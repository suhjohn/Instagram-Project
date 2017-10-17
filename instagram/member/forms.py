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

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data["username"]
        if " " in username:
            raise ValidationError(
                ('Space in username'),
            )

        elif User.objects.filter(username=username).exists():
            raise ValidationError(
                ('Username Already Exists!'),
            )
        return username

    def clean_password2(self):
        if self.cleaned_data["password"] != self.cleaned_data["password2"]:
            raise ValidationError(
                ("Password Check Failed. Please check the password."),
            )

    def clean(self):
        super().clean()
        if self.is_valid():
            setattr(self, 'signup', self._signup)

        return self.cleaned_data

    def _signup(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        return User.objects.create_user(username=username, password=password)


class LoginForm(forms.Form):
    """
    is_valid()에서 주어진 username/password를 사용한 authentication 실행
    성공 시 login(request) 메소드를 사용할 수 있음
    """
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
        """
        :param request: django.contrib.auth.login()에 주어질 로그인 세션 정보가 있는 HttpResponse 객체
        :return:
        """
        django_login(request, self.user)

