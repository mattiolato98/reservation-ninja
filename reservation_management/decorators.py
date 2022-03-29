from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse_lazy

from reservation_management.models import Lesson


def lesson_owner_only(func):
    """
    Decorator that returns a function which protect a resource from users
    that are not the owner of that resource.

    Args:
        func (function): the decorated function.
    """

    def check_and_call(request, *args, **kwargs):
        lesson = Lesson.objects.get(pk=kwargs["pk"])
        if not lesson.user == request.user:
            return HttpResponseForbidden()
        return func(request, *args, **kwargs)

    return check_and_call


def check_correctness(func):
    def check_and_call(request, *args, **kwargs):
        lessons = request.user.lessons.all()
        # if the user has no lessons, just return an error page
        if not lessons:
            return HttpResponseRedirect(
                reverse_lazy("reservation_management:no-lessons-error")
            )
        for lesson in lessons:
            if not request.user.check_lesson_time_overlap(lesson, update=True):
                return HttpResponseRedirect(
                    reverse_lazy("reservation_management:lesson-overlap-error")
                )
        return func(request, *args, **kwargs)

    return check_and_call
