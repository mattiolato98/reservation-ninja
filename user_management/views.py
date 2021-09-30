from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import CreateView, TemplateView
from django.utils.translation import gettext_lazy as _

from user_management.forms import LoginForm, PlatformUserCreationForm

account_activation_token = PasswordResetTokenGenerator()


class LoginUserView(LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'


class RegistrationView(CreateView):
    form_class = PlatformUserCreationForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('user_management:email-verification-needed')

    def form_valid(self, form):
        response = super(RegistrationView, self).form_valid(form)

        mail_subject = _('Conferma la tua mail')
        relative_confirm_url = reverse(
            'user_management:verify-user-email',
            args=[
                urlsafe_base64_encode(force_bytes(self.object.pk)),
                account_activation_token.make_token(self.object)
            ]
        )

        self.object.email_user(
            subject=mail_subject,
            message=_(f'''Ciao {self.object.username}, '''
                      + '''ti diamo il benvenuto in Wallet.\n'''
                      + '''\nClicca il seguente link per confermare la tua email:'''
                      + f'''\n{self.request.build_absolute_uri(relative_confirm_url)}\n'''
                      + '''\nA presto, \nil Team di Wallet.''')
        )

        self.object.token_sent = True
        self.object.is_active = False
        self.object.save()

        return response


def user_login_by_token(request, user_id_b64=None, user_token=None):
    """
    Check the token is equal to one of user trying to verify its email.
    """
    try:
        uid = force_text(urlsafe_base64_decode(user_id_b64))
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, user_token):
        user.is_active = True
        user.save()
        login(request, user)
        return True

    return False


def verify_user_email(request, user_id_b64=None, user_token=None):
    """
    Check for the token and redirect to email verification succeeded page.
    """
    if not user_login_by_token(request, user_id_b64, user_token):
        message = _('Errore. Tentativo di validazione email per l\'utente {user} con token {token}')

    return redirect('user_management:email-verified')


class EmailVerificationNeededView(TemplateView):
    template_name = 'user_management/email_verification_needed.html'


class EmailVerifiedView(LoginRequiredMixin, TemplateView):
    template_name = 'user_management/email_verified.html'


def ajax_check_username_exists(request):
    return JsonResponse({'exists': True}) \
        if get_user_model().objects.filter(username=request.GET.get('username')).exists() \
        else JsonResponse({'exists': False})


def ajax_check_email(request):
    email = request.GET.get('email')

    if '@' in email and email.split('@')[1] == 'studenti.unimore.it':
        return JsonResponse({'is_unimore_email': True})
    return JsonResponse({'is_unimore_email': False})
