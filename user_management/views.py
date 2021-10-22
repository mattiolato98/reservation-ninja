from cryptography.fernet import Fernet
from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.views import LoginView
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_GET, require_POST
from django.views.generic import CreateView, TemplateView, DeleteView, ListView, UpdateView, FormView
from django.utils.translation import gettext_lazy as _

from reservation_tool_base_folder.decorators import not_authenticated_only
from user_management.check_unimore_credentials import check_unimore_credentials
from user_management.decorators import manager_required
from user_management.forms import LoginForm, PlatformUserCreationForm, UserUpdateUnimoreCredentialsForm, \
    UserAddGreenPass
from user_management.models import PlatformUser

account_activation_token = PasswordResetTokenGenerator()


@method_decorator(not_authenticated_only, name='dispatch')
class LoginUserView(LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'


@method_decorator(not_authenticated_only, name='dispatch')
class RegistrationView(CreateView):
    form_class = PlatformUserCreationForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('user_management:email-verification-needed')

    def form_valid(self, form):
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


class UserUpdateUnimoreCredentialsView(LoginRequiredMixin, FormView):
    model = get_user_model()
    form_class = UserUpdateUnimoreCredentialsForm
    template_name = "user_management/user_update_unimore_credentials.html"
    success_url = reverse_lazy('user_management:settings')

    def get_context_data(self, **kwargs):
        context = super(UserUpdateUnimoreCredentialsView, self).get_context_data(**kwargs)
        context['form'].fields['unimore_username'].widget.attrs.update({'value': self.request.user.plain_unimore_username})
        context['form'].fields['unimore_password'].widget.attrs.update({'value': ''})
        return context

    def form_valid(self, form):
        self.object = self.request.user

        username = form.cleaned_data['unimore_username']
        password = form.cleaned_data['unimore_password']

        encryptor = Fernet(settings.CRYPTOGRAPHY_KEY.encode())
        self.object.unimore_username = encryptor.encrypt(username.encode()).decode()
        self.object.unimore_password = encryptor.encrypt(password.encode()).decode()

        self.object.save()

        return super(UserUpdateUnimoreCredentialsView, self).form_valid(form)

    def get_object(self, queryset=None):
        return self.request.user


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


class UserGreenPassAddView(LoginRequiredMixin, FormView):
    model = get_user_model()
    form_class = UserAddGreenPass
    template_name = "user_management/greenpass_add.html"
    success_url = reverse_lazy("reservation_management:reservation-list")

    def post(self, request, *args, **kwargs):
        """
        In order to manage the cancel button from the lesson form. If 'cancel'
        is in the request.POST, the lesson must not be created.
        :return: HTTP response.
        """
        if 'cancel' in request.POST:
            return HttpResponseRedirect(reverse_lazy("home"))
        else:
            return super(UserGreenPassAddView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = self.request.user

        self.object.green_pass_link = form.cleaned_data['green_pass_link']
        self.object.save()

        return super(UserGreenPassAddView, self).form_valid(form)


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


@login_required
@require_POST
@csrf_protect
def ajax_check_unimore_credentials(request):
    if not check_unimore_credentials(
            request.POST.get('username'), request.POST.get('password')
    ):
        return JsonResponse({'is_valid': False})
    return JsonResponse({'is_valid': True})
