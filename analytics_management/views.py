import datetime as dt

from collections import defaultdict

import pytz
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.views.generic import ListView, TemplateView

from analytics_management.models import Log, Feedback, Stats
from reservation_management.models import Lesson, Reservation
from user_management.decorators import manager_required


@method_decorator([login_required, manager_required], name='dispatch')
class LogListView(ListView):
    """
    View to display the log of the daily reservation.py execution.
    """
    model = Log
    template_name = "analytics_management/log_list.html"

    def get_queryset(self):
        return Log.objects.all().order_by('-date')


@method_decorator([login_required, manager_required], name='dispatch')
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


@method_decorator([login_required, manager_required], name='dispatch')
class UserListView(ListView):
    model = get_user_model()
    template_name = "analytics_management/user_list.html"

    def get_queryset(self):
        return get_user_model().objects.all().order_by('-date_joined')


@method_decorator([login_required, manager_required], name='dispatch')
class StatsView(TemplateView):
    template_name = "analytics_management/stats.html"

    def get_context_data(self, **kwargs):
        context = super(StatsView, self).get_context_data(**kwargs)

        context['users'] = get_user_model().objects.count()
        context['unsubscribed_users'] = Stats.objects.first().unsubscribed_users
        context['subscribers_last_7_days'] = len(get_user_model().objects.filter(
            date_joined__gte=dt.datetime.now(pytz.timezone('Europe/Rome')) - dt.timedelta(days=7)
        ))
        context['percent_increment_subscribers_last_7_days'] = ((
            context['subscribers_last_7_days']
        ) / (context['users'] - context['subscribers_last_7_days'])) * 100
        context['logged_in_last_7_days'] = get_user_model().objects.filter(
            last_login__gte=dt.datetime.now(pytz.timezone('Europe/Rome')) - dt.timedelta(days=7)
        ).count()
        context['percent_logged_in_last_7_days'] = (
            context['logged_in_last_7_days'] / context['users']
        ) * 100
        context['inactive_users'] = get_user_model().objects.filter(is_active=False).count()

        users = get_user_model().objects.annotate(num_lessons=Count('lessons'))

        context['more_than_five_lessons'] = users.filter(num_lessons__gt=5).count()
        context['percent_more_than_five_lessons'] = (context['more_than_five_lessons'] / context['users']) * 100
        context['from_one_to_five_lessons'] = users.filter(num_lessons__lte=5, num_lessons__gt=0).count()
        context['percent_from_one_to_five_lessons'] = (context['from_one_to_five_lessons'] / context['users']) * 100
        context['zero_lessons'] = users.filter(num_lessons=0).count()
        context['percent_zero_lessons'] = (context['zero_lessons'] / context['users']) * 100

        context['green_pass_added'] = get_user_model().objects.filter(green_pass_link__isnull=False).count()
        context['percent_green_pass_added'] = (context['green_pass_added'] / context['users']) * 100
        context['seen_whats_new'] = get_user_model().objects.filter(whats_new=False).count()
        context['percent_seen_whats_new'] = (context['seen_whats_new'] / context['users']) * 100
        context['feedback_disabled'] = get_user_model().objects.filter(ask_for_feedback=False).count()
        context['percent_feedback_disabled'] = (context['feedback_disabled'] / context['users']) * 100
        context['wrong_credentials'] = get_user_model().objects.filter(credentials_ok=False).count()
        context['percent_wrong_credentials'] = (context['wrong_credentials'] / context['users']) * 100

        context['lessons'] = Lesson.objects.count()

        context['average_lessons_per_user'] = context['lessons'] / context['users']
        context['today_lessons'] = Lesson.objects.filter(
            day=dt.datetime.now(pytz.timezone('Europe/Rome')).weekday()
        ).count()
        context['lessons_per_day'] = {
            'Monday': Lesson.objects.filter(day=0).count(),
            'Tuesday': Lesson.objects.filter(day=1).count(),
            'Wednesday': Lesson.objects.filter(day=2).count(),
            'Thursday': Lesson.objects.filter(day=3).count(),
            'Friday': Lesson.objects.filter(day=4).count(),
        }

        context['reservations'] = Reservation.objects.count()
        context['average_reservations_per_user'] = context['reservations'] / context['users']

        if Log.objects.filter(date=dt.datetime.now(pytz.timezone('Europe/Rome'))).exists():
            log = Log.objects.filter(date=dt.datetime.now(pytz.timezone('Europe/Rome'))).first()
            context['average_reservations_per_today_user'] = context['reservations'] / log.users

        return context


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
