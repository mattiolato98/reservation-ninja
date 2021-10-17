from django.http import HttpResponseForbidden


def manager_required(func):
    def check_and_call(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_manager:
            return func(request, *args, **kwargs)
        return HttpResponseForbidden()
    return check_and_call
