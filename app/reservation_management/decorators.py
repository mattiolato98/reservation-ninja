from django.http import HttpResponseForbidden

from app.reservation_management.models import Lesson


def lesson_owner_only(func):
    def check_and_call(request, *args, **kwargs):
        lesson = Lesson.objects.get(pk=kwargs['pk'])
        if not lesson.user == request.user:
            return HttpResponseForbidden()
        return func(request, *args, **kwargs)
    return check_and_call
