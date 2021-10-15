from crispy_forms.layout import Layout, Row, Column, HTML
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from crispy_forms.helper import FormHelper
from django.utils.translation import gettext_lazy as _
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

        self.fields['email'].label = "Unimore Email"

        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update({'placeholder': _('Your Unimore Email')})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder': _('Confirm password')})
        self.fields['unimore_username'].widget.attrs.update({'placeholder': _('Unimore username')})
        self.fields['unimore_password'].widget.attrs.update({'placeholder': _('Unimore password')})

        self.helper.layout = Layout(
            Row(
                Column('username', css_class='form-group mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('password1', css_class='form-group'),
                Column('password2', css_class='form-group'),
                css_class='form-row',
            ),
            Row(HTML("<hr>")),
            Row(
                HTML(_("""
                    <h3 class='mt-3 mb-0 logo-font site-color'>Unimore Credentials</h3>
                """)),
            ),
            Row(
                HTML(_("""
                    <span class='form-text small mt-0 mb-2'>
                    Your credentials will be encrypted and securely stored and you can delete them at any time.
                    </span>      
                """))
            ),
            Row(
                Column('unimore_username', css_class='form-group'),
                Column('unimore_password', css_class='form-group'),
                css_class='form-row mt-3'
            ),
            Row(
                Column('email', css_class='form-group'),
                css_class='form-row'
            ),
        )

    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'email',
            'password1',
            'password2',
            'unimore_username',
            'unimore_password',
        )
        labels = {
            'unimore_username': _('Unimore username'),
            'unimore_password': _('Unimore password'),
            'email': _('Unimore Email'),
        }
        widgets = {
            'unimore_password': forms.PasswordInput(),
        }
