import datetime as dt
import pandas as pd

from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView

from reservation_management.decorators import lesson_owner_only
from reservation_management.forms import LessonForm
from reservation_management.models import Lesson, Reservation, Log, Feedback
from user_management.decorators import manager_required


class LessonAddView(LoginRequiredMixin, CreateView):
    """
    View that implements the Lesson creation.
    """
    model = Lesson
    form_class = LessonForm
    template_name = "reservation_management/lesson_add.html"
    success_url = reverse_lazy("reservation_management:lesson-list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(LessonAddView, self).form_valid(form)


class LessonListView(LoginRequiredMixin, ListView):
    """
    View to display the Lessons created by a user.
    """
    model = Lesson
    template_name = "reservation_management/lesson_list.html"

    def get_queryset(self):
        return Lesson.objects.filter(user=self.request.user)


@method_decorator((login_required, lesson_owner_only), name='dispatch')
class LessonDetailView(DetailView):
    """
    View to show detail of a Lesson.
    """
    model = Lesson
    template_name = "reservation_management/lesson_detail.html"


@method_decorator((login_required, lesson_owner_only), name='dispatch')
class LessonUpdateView(UpdateView):
    """
    View to update a Lesson.
    """
    model = Lesson
    form_class = LessonForm
    template_name = "reservation_management/lesson_update.html"

    def get_success_url(self):
        return reverse_lazy("reservation_management:lesson-detail", kwargs={'pk': self.kwargs['pk']})


@method_decorator((login_required, lesson_owner_only), name='dispatch')
class LessonDeleteView(DeleteView):
    """
    View to delete an existing dish.
    """
    model = Lesson
    template_name = 'reservation_management/lesson_delete.html'
    success_url = reverse_lazy('reservation_management:lesson-list')


class ReservationListView(LoginRequiredMixin, ListView):
    """
    View to display the reservations made for the current user.
    """
    model = Reservation
    template_name = "reservation_management/reservation_list.html"

    def get_queryset(self):
        return Reservation.objects.filter(lesson__user=self.request.user)


@method_decorator(manager_required, name='dispatch')
class LogListView(ListView):
    """
    View to display the log of the daily reservation.py execution.
    """
    model = Log
    template_name = "reservation_management/log_list.html"

    def get_queryset(self):
        return Log.objects.all().order_by('-date')


@method_decorator(manager_required, name='dispatch')
class FeedbackListView(ListView):
    """
    View to display the feedback list of the daily reservation.py execution.
    """
    model = Feedback
    template_name = "reservation_management/feedback_list.html"

    def get_queryset(self):
        feedbacks = Feedback.objects.all().order_by('-date', 'user')
        feedbacks_grouped_by_date = defaultdict(list)

        for feedback in feedbacks:
            feedbacks_grouped_by_date[feedback.date].append(feedback)

        # Dict cast is needed, because template see defaultdict as empty
        return dict(feedbacks_grouped_by_date)


class LessonTimetableView(LoginRequiredMixin, TemplateView):
    template_name = "reservation_management/lesson_timetable.html"

    def get_context_data(self, **kwargs):
        context = super(LessonTimetableView, self).get_context_data(**kwargs)

        lessons = self.request.user.lessons.all()

        min_time = min(lesson.start_time for lesson in lessons)
        max_time = max(lesson.end_time for lesson in lessons)

        if any(lesson.start_time.minute != 0 and lesson.end_time.minute != 0 for lesson in lessons):
            frequency = 60
        else:
            frequency = 30

        time_series = pd.Series()

        time_list = []
        items = 0
        time = min_time
        while time <= max_time:
            time_list.append(time)
            time = (dt.datetime.combine(dt.date(1, 1, 1), time) + dt.timedelta(minutes=frequency)).time()
            items += 1

        index = [
            f"{time.strftime('%H:%M')} - "
            f"{(dt.datetime.combine(dt.date(1, 1, 1), time) + dt.timedelta(minutes=frequency)).time().strftime('%H:%M')}"
            for time in time_list
        ]

        lessons_grouped_by_day = {
            0: [],
            1: [],
            2: [],
            3: [],
            4: [],
        }

        for lesson in lessons:
            lessons_grouped_by_day[lesson.day].append(lesson)

        data = defaultdict(list)
        for day, lessons in lessons_grouped_by_day.items():
            lesson = lessons.pop(0) if len(lessons) > 0 else None
            time = min_time
            while time <= max_time:
                next_time = (dt.datetime.combine(dt.date(1, 1, 1), time) + dt.timedelta(minutes=frequency)).time()

                if lesson is not None \
                        and lesson.start_time <= time < lesson.end_time \
                        and lesson.end_time >= next_time > lesson.start_time:
                    data[day].append(lesson.classroom.name)
                else:
                    data[day].append('')

                if lesson is not None and lesson.end_time <= next_time:
                    lesson = lessons.pop(0) if len(lessons) > 0 else None

                time = next_time

        context['df'] = pd.DataFrame(data, index=index)

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


@login_required
@require_POST
@csrf_protect
def ajax_whats_new_confirm(request):
    """
    View called by an ajax function, it confirms that a user saw the new features.
    """
    user = request.user
    user.whats_new = False
    user.save()

    return JsonResponse({'ok', True})
