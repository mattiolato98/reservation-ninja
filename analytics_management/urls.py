from django.urls import path
from analytics_management import views

app_name = 'analytics_management'

urlpatterns = [
    path('log-list', views.LogListView.as_view(), name='log-list'),
    path('feedback-list', views.FeedbackListView.as_view(), name='feedback-list'),
    path('user-list', views.UserListView.as_view(), name='user-list'),
    path('stats', views.StatsView.as_view(), name='stats'),
    path('send-feedback', views.ajax_send_feedback, name='send-feedback'),
]
