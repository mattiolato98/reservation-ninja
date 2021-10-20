from django.urls import path
from reservation_management import views

app_name = 'reservation_management'

urlpatterns = [
    path('', views.ReservationListView.as_view(), name='reservation-list'),
    path('lesson/add', views.LessonAddView.as_view(), name='lesson-add'),
    path('lesson/list', views.LessonListView.as_view(), name='lesson-list'),
    path('lesson/<int:pk>/detail', views.LessonDetailView.as_view(), name='lesson-detail'),
    path('lesson/<int:pk>/update', views.LessonUpdateView.as_view(), name='lesson-update'),
    path('lesson/<int:pk>/delete', views.LessonDeleteView.as_view(), name='lesson-delete'),
    path('log-list', views.LogListView.as_view(), name='log-list'),
]
