from django.urls import path
from user_management import views
from django.contrib.auth import views as auth_views

app_name = 'user_management'

urlpatterns = [
    path('login', views.LoginUserView.as_view(), name='login'),
    path('registration', views.RegistrationView.as_view(), name='registration'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('ajax-check-username-exists', views.ajax_check_username_exists, name='ajax-check-username-exists'),
    path('email/verification_needed', views.EmailVerificationNeededView.as_view(), name='email-verification-needed'),
    path('email/verified', views.EmailVerifiedView.as_view(), name='email-verified'),
    path('verify/<str:user_id_b64>/<str:user_token>', views.verify_user_email, name='verify-user-email'),
]
