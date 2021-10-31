from django.urls import path
from app.reservation_management import views

app_name = 'reservation_management'

urlpatterns = [
    path('', views.ReservationListView.as_view(), name='reservation-list'),
    path('lesson/add', views.LessonAddView.as_view(), name='lesson-add'),
    path('lesson/list', views.LessonListView.as_view(), name='lesson-list'),
    path('lesson/<int:pk>/detail', views.LessonDetailView.as_view(), name='lesson-detail'),
    path('lesson/<int:pk>/update', views.LessonUpdateView.as_view(), name='lesson-update'),
    path('lesson/<int:pk>/delete', views.LessonDeleteView.as_view(), name='lesson-delete'),
    path('log-list', views.LogListView.as_view(), name='log-list'),
    path('feedback-list', views.FeedbackListView.as_view(), name='feedback-list'),
    path('send-feedback', views.ajax_send_feedback, name='send-feedback'),
    path('whats-new-confirm', views.ajax_whats_new_confirm, name='whats-new-confirm'),
]