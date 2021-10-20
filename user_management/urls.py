from django.urls import path
from user_management import views
from django.contrib.auth import views as auth_views

app_name = 'user_management'

urlpatterns = [
    path('login', views.LoginUserView.as_view(), name='login'),
    path('registration', views.RegistrationView.as_view(), name='registration'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('list', views.UserListView.as_view(), name='list'),
    path('ajax-check-username-exists', views.ajax_check_username_exists, name='ajax-check-username-exists'),
    path('ajax-check-email', views.ajax_check_email, name='ajax-check-email'),
    path('email/verification_needed', views.EmailVerificationNeededView.as_view(), name='email-verification-needed'),
    path('email/verified', views.EmailVerifiedView.as_view(), name='email-verified'),
    path('verify/<str:user_id_b64>/<str:user_token>', views.verify_user_email, name='verify-user-email'),
    path('ajax-check-username-is-correct', views.ajax_check_username_is_correct, name='ajax-check-username-is-correct'),
    path('settings', views.SettingsView.as_view(), name='settings'),
    path('delete', views.UserDeleteView.as_view(), name='delete'),
    path('privacy-policy', views.PrivacyPolicyView.as_view(), name='privacy-policy'),
    path('cookie-policy', views.CookiePolicyView.as_view(), name='cookie-policy'),
    # path(
    #     'update-unimore-credentials',
    #     views.UserUpdateUnimoreCredentialsView.as_view(),
    #     name='update-unimore-credentials'
    # ),
]
