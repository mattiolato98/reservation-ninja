from collections import defaultdict

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from analytics_management.models import Log, Feedback
from user_management.decorators import manager_required


@method_decorator(manager_required, name='dispatch')
class LogListView(ListView):
    """
    View to display the log of the daily reservation.py execution.
    """
    model = Log
    template_name = "analytics_management/log_list.html"

    def get_queryset(self):
        return Log.objects.all().order_by('-date')


@method_decorator(manager_required, name='dispatch')
class FeedbackListView(ListView):
    """
    View to display the feedback list of the daily reservation.py execution.
    """
    model = Feedback
    template_name = "analytics_management/feedback_list.html"

    def get_queryset(self):
        feedbacks = Feedback.objects.all().order_by('-date', 'user')
        feedbacks_grouped_by_date = defaultdict(list)

        for feedback in feedbacks:
            feedbacks_grouped_by_date[feedback.date].append(feedback)

        # Dict cast is needed, because template see defaultdict as empty
        return dict(feedbacks_grouped_by_date)


@method_decorator(manager_required, name='dispatch')
class UserListView(ListView):
    model = get_user_model()
    template_name = "analytics_management/user_list.html"

    def get_queryset(self):
        return get_user_model().objects.all().order_by('-date_joined')


@login_required
@require_POST
@csrf_protect
def ajax_send_feedback(request):
    """
    View called by an ajax function, it creates a feedback object.
    """
    user = request.user

    Feedback.objects.create(
        user=user,
        ok=int(request.POST.get('response_ok')) == 1,
    )

    user.feedback = True
    user.save()

    return JsonResponse({'ok': True})
