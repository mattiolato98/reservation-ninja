from crispy_forms.layout import Layout, Row, Column
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from crispy_forms.helper import FormHelper
from django import forms


class LoginForm(AuthenticationForm):
    helper = FormHelper()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Password'})


class PlatformUserCreationForm(UserCreationForm):
    helper = FormHelper()
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].help_text = None

        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm password'})
        self.fields['unimore_username'].widget.attrs.update({'placeholder': 'Unimore username'})
        self.fields['unimore_password'].widget.attrs.update({'placeholder': 'Unimore password'})

        self.helper.layout = Layout(
            Row(
                Column('username', css_class='form-group mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('email', css_class='form-group'),
                css_class='form-row'
            ),
            Row(
                Column('unimore_username', css_class='form-group'),
                Column('unimore_password', css_class='form-group'),
                css_class='form-row'
            ),
            Row(
                Column('password1', css_class='form-group'),
                Column('password2', css_class='form-group'),
                css_class='form-row',
            ),
        )

    class Meta:
        model = get_user_model()
        fields = [
            'username',
            'email',
            'password1',
            'password2',
            'unimore_username',
            'unimore_password',
        ]
        widgets = {
            'unimore_password': forms.PasswordInput(),
        }
