from django.http import HttpResponseForbidden

from reservation_management.models import Lesson


def lesson_owner_only(func):
    """
    Decorator that returns a function which protect a resource from users 
    that are not the owner of that resource.

    Args:
        func (function): the decorated function.
    """
    def check_and_call(request, *args, **kwargs):
        lesson = Lesson.objects.get(pk=kwargs['pk'])
        if not lesson.user == request.user:
            return HttpResponseForbidden()
        return func(request, *args, **kwargs)
    return check_and_call
