from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView

from reservation_management.forms import LessonForm
from reservation_management.models import Lesson


class LessonAddView(CreateView):
    model = Lesson
    form_class = LessonForm
    template_name = "reservation_management/lesson_add.html"
    success_url = reverse_lazy("home")

    def post(self, request, *args, **kwargs):
        """
        In order to manage the cancel button from the lesson form. If 'cancel'
        is in the request.POST, the lesson must not be created.
        :return: HTTP response.
        """
        if 'cancel' in request.POST:
            return HttpResponseRedirect(reverse_lazy("home"))
        else:
            return super(LessonAddView, self).post(request, *args, **kwargs)
