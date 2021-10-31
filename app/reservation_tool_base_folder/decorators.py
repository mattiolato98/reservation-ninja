from django.shortcuts import redirect


def not_authenticated_only(func):
    def check_and_call(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('reservation_management:reservation-list')
        return func(request, *args, **kwargs)
    return check_and_call
