from django.urls import path
from reservation_management import views

app_name = 'reservation_management'

urlpatterns = [
    path('lesson/add', views.LessonAddView.as_view(), name='lesson-add'),
]
