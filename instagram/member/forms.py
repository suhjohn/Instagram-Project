from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model, authenticate, login as django_login
from django.core.exceptions import ValidationError

# from member.custom_validators import validate_username


User = get_user_model()


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        class_update_fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email')
        for field in class_update_fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password1', 'password2',)
        widgets = {
            'password1': forms.PasswordInput(
                attrs={
                    'class': 'form-control',
                }
            ),
        }
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
        }
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                }
            )
        }
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            )
        }
        widgets = {
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            )
        }


class LoginForm(forms.Form):
    """
    is_valid()에서 주어진 username/password를 사용한 authentication 실행
    성공 시 login(request) 메소드를 사용할 수 있음
    """
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder':"사용자 이름 또는 이메일",
                'class': 'form-control',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': "비밀번호",
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
