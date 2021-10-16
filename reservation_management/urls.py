from django.urls import path
from reservation_management import views

app_name = 'reservation_management'

urlpatterns = [
    path('', views.ReservationListView.as_view(), name='reservation-list'),
    path('lesson/add', views.LessonAddView.as_view(), name='lesson-add'),
    path('lesson/list', views.LessonListView.as_view(), name='lesson-list'),
    path('lesson/<int:pk>/detail', views.LessonDetailView.as_view(), name='lesson-detail'),
]
