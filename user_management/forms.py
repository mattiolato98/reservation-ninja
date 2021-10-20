from crispy_forms.layout import Layout, Row, Column, HTML, Submit
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from crispy_forms.helper import FormHelper
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
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

        self.fields['email'].label = _("Unimore Email")

        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update({'placeholder': _('Your Unimore Email')})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder': _('Confirm password')})
        self.fields['unimore_username'].widget.attrs.update({'placeholder': _('Unimore username')})
        self.fields['unimore_password'].widget.attrs.update({'placeholder': _('Unimore password')})

        privacy_policy_url = reverse_lazy('user_management:privacy-policy')
        cookie_policy_url = reverse_lazy('user_management:cookie-policy')

        self.fields['privacy_and_cookie_policy_acceptance'].label = mark_safe(_(
            "I agree with the <a href='{}' target='_blank' class='site-link'>privacy policy</a> "
            "and the use of essential cookies, according with our <a href='{}' "
            "target='_blank' class='site-link'>cookie policy</a>, in order to allow the proper operation of the app"
        ).format(privacy_policy_url, cookie_policy_url))

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
            Row(
                Column('privacy_and_cookie_policy_acceptance', css_class='form-group'),
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
            'privacy_and_cookie_policy_acceptance',
        )
        labels = {
            'unimore_username': _('Unimore username'),
            'unimore_password': _('Unimore password'),
            'email': _('Unimore Email'),
        }
        widgets = {
            'unimore_password': forms.PasswordInput(),
        }

    def clean(self):
        if self.cleaned_data['email'].split('@')[1] != 'studenti.unimore.it':
            raise ValidationError(_("Seems that you are not a Unimore student."))
        if not self.cleaned_data['privacy_and_cookie_policy_acceptance']:
            raise ValidationError(_("You must accept the privacy policies."))

        return super(PlatformUserCreationForm, self).clean()


class UserUpdateUnimoreCredentialsForm(forms.ModelForm):
    helper = FormHelper()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['unimore_username'].widget.attrs.update({'placeholder': _('Unimore username')})
        self.fields['unimore_password'].widget.attrs.update({'placeholder': _('Unimore password')})

        self.helper.layout = Layout(
            Row(
                Column('unimore_username', css_class='form-group'),
                css_class='form-row'
            ),
            Row(
                Column('unimore_password', css_class='form-group'),
                css_class='form-row'
            ),
            Row(
                Column(
                    Submit('submit', _('Update'), css_class="btn site-btn w-100 font-5"),
                    css_class='form-group d-flex justify-content-center align-items-end'
                ),
                css_class='form-row'
            )
        )

    class Meta:
        model = get_user_model()
        fields = ('unimore_username', 'unimore_password')
        labels = {
            'unimore_username': _('Unimore username'),
            'unimore_password': _('Unimore password'),
        }
        widgets = {
            'unimore_password': forms.PasswordInput(),
        }
