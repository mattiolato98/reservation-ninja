from cryptography.fernet import Fernet
from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_GET
from django.views.generic import CreateView, TemplateView, DeleteView, ListView
from django.utils.translation import gettext_lazy as _

from user_management.decorators import manager_required
from user_management.forms import LoginForm, PlatformUserCreationForm
from user_management.models import PlatformUser

account_activation_token = PasswordResetTokenGenerator()


class LoginUserView(LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'


class RegistrationView(CreateView):
    form_class = PlatformUserCreationForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('user_management:email-verification-needed')

    def form_valid(self, form):
        if form.cleaned_data['email'].split('@')[1] != 'studenti.unimore.it' or \
                not form.cleaned_data['privacy_and_cookie_policy_acceptance']:
            return redirect('user_management:registration')

        self.object = form.save(commit=False)

        encryptor = Fernet(settings.CRYPTOGRAPHY_KEY.encode())
        self.object.unimore_username = encryptor.encrypt(self.object.unimore_username.encode()).decode()
        self.object.unimore_password = encryptor.encrypt(self.object.unimore_password.encode()).decode()

        response = super(RegistrationView, self).form_valid(form)

        mail_subject = _('Reservation Ninja - Confirm your email')
        relative_confirm_url = reverse(
            'user_management:verify-user-email',
            args=[
                urlsafe_base64_encode(force_bytes(self.object.pk)),
                account_activation_token.make_token(self.object)
            ]
        )

        self.object.email_user(
            subject=mail_subject,
            message=_(f'''Hi {self.object.username}, '''
                      + '''welcome to Reservation Ninja.\n'''
                      + '''\nClick this link to confirm your email:'''
                      + f'''\n{self.request.build_absolute_uri(relative_confirm_url)}\n'''
                      + '''\nSee you soon, \nReservation Ninja.''')
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
        message = _(f'Error. Attempt to validate email for the user {user_id_b64} with token {user_token}')
        subject = _('Authentication error')
        # in this case manager and admin are the same entity
        manager = PlatformUser.objects.get(is_manager=True)
        manager.email_user(subject=subject, message=message)
        # TODO: maybe provide an error message?
        return redirect('user_management:registration')

    return redirect('user_management:email-verified')


class PrivacyPolicyView(TemplateView):
    template_name = "user_management/privacy_policy.html"


class CookiePolicyView(TemplateView):
    template_name = "user_management/cookie-policy.html"


class EmailVerificationNeededView(TemplateView):
    template_name = 'user_management/email_verification_needed.html'


class EmailVerifiedView(TemplateView):
    template_name = 'user_management/email_verified.html'


class SettingsView(LoginRequiredMixin, TemplateView):
    template_name = "user_management/settings.html"


class UserDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "user_management/user_delete.html"
    success_url = reverse_lazy("home")
    model = get_user_model()

    def get_object(self, queryset=None):
        return self.request.user


@method_decorator(manager_required, name='dispatch')
class UserListView(ListView):
    model = get_user_model()
    template_name = "user_management/user_list.html"

    def get_queryset(self):
        return get_user_model().objects.all().order_by('-date_joined')


def ajax_check_username_exists(request):
    return JsonResponse({'exists': True}) \
        if get_user_model().objects.filter(username=request.GET.get('username')).exists() \
        else JsonResponse({'exists': False})


def ajax_check_email(request):
    email = request.GET.get('email')

    if '@' in email and email.split('@')[1] == 'studenti.unimore.it':
        return JsonResponse({'is_unimore_email': True})
    return JsonResponse({'is_unimore_email': False})


@login_required
@require_GET
@csrf_protect
def ajax_check_username_is_correct(request):
    if request.GET.get('username') == request.user.username:
        return JsonResponse({'is_correct': True})
    return JsonResponse({'is_correct': False})
