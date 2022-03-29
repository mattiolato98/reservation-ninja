import datetime as dt
from collections import defaultdict
import math

import pandas as pd

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
    TemplateView,
)

from reservation_management.decorators import lesson_owner_only, check_correctness
from reservation_management.forms import LessonForm
from reservation_management.models import Lesson, Reservation


class LessonAddView(LoginRequiredMixin, CreateView):
    """
    View that implements the Lesson creation.
    """

    model = Lesson
    form_class = LessonForm
    template_name = "reservation_management/lesson_add.html"
    success_url = reverse_lazy("reservation_management:lesson-list")

    def get_form_kwargs(self):
        kwargs = super(LessonAddView, self).get_form_kwargs()
        kwargs.update({"request": self.request})
        return kwargs

    # TODO: keeping this function here and not in the FormClass is probably conceptually wrong now.
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


@method_decorator((login_required, lesson_owner_only), name="dispatch")
class LessonDetailView(DetailView):
    """
    View to show detail of a Lesson.
    """

    model = Lesson
    template_name = "reservation_management/lesson_detail.html"


@method_decorator((login_required, lesson_owner_only), name="dispatch")
class LessonUpdateView(UpdateView):
    """
    View to update a Lesson.
    """

    model = Lesson
    form_class = LessonForm
    template_name = "reservation_management/lesson_update.html"

    def get_form_kwargs(self):
        kwargs = super(LessonUpdateView, self).get_form_kwargs()
        kwargs.update({"request": self.request})
        return kwargs

    def get_success_url(self):
        return reverse_lazy(
            "reservation_management:lesson-detail", kwargs={"pk": self.kwargs["pk"]}
        )


@method_decorator((login_required, lesson_owner_only), name="dispatch")
class LessonDeleteView(DeleteView):
    """
    View to delete an existing dish.
    """

    model = Lesson
    template_name = "reservation_management/lesson_delete.html"
    success_url = reverse_lazy("reservation_management:lesson-list")


class ReservationListView(LoginRequiredMixin, ListView):
    """
    View to display the reservations made for the current user.
    """

    model = Reservation
    template_name = "reservation_management/reservation_list.html"

    def get_queryset(self):
        return Reservation.objects.filter(lesson__user=self.request.user)


@method_decorator((login_required, check_correctness), name="dispatch")
class LessonTimetableView(TemplateView):
    """
    View to display the timetable of the current user.
    """

    template_name = "reservation_management/lesson_timetable.html"

    def get_context_data(self, **kwargs):
        context = super(LessonTimetableView, self).get_context_data(**kwargs)

        lessons = self.request.user.lessons.all()
        min_time = min(lesson.get_approximated_start_time for lesson in lessons)
        max_time = max(lesson.get_approximated_end_time for lesson in lessons)
        sorted_times = set()

        for lesson in lessons:
            sorted_times.add(lesson.get_approximated_start_time)
            sorted_times.add(lesson.get_approximated_end_time)
        sorted_times = list(
            sorted(sorted_times)
        )  # in order to access elements by index

        # retrieving all possible deltas between each lesson
        time_deltas = {
            dt.datetime.combine(dt.date.min, sorted_times[idx + 1])
            - dt.datetime.combine(dt.datetime.min, sorted_times[idx])
            for idx in range(len(sorted_times))
            if idx < len(sorted_times) - 1
        }
        time_deltas = {
            int(
                (delta.seconds % 3600) / 60
            )  # distribute the durations in an hour and convert seconds in minutes
            for delta in time_deltas
            if delta.seconds % 3600 != 0
        }
        time_interval = math.gcd(
            *time_deltas, 60
        )  # this is the time interval of the timetable

        time_list = []
        current_time_slot = min_time
        while current_time_slot < max_time:
            time_list.append(current_time_slot)
            current_time_slot = (
                dt.datetime.combine(dt.date.min, current_time_slot)
                + dt.timedelta(minutes=time_interval)
            ).time()
        # this index will be used in a pandas DataFrame
        index = [
            f"{time.strftime('%H:%M')} - "
            f"""{(dt.datetime.combine(dt.date.min, time) 
                 + dt.timedelta(minutes=time_interval)).time().strftime('%H:%M')}"""
            for time in time_list
        ]
        # this empty dictionary has to be instantiated early because a user
        # could not have lessons every day
        lessons_by_day = {
            0: [],
            1: [],
            2: [],
            3: [],
            4: [],
        }
        for lesson in lessons:  # the lessons are already ordered
            lessons_by_day[lesson.day].append(lesson)

        data = defaultdict(list)  # the content of the pandas DataFrame
        for day, lessons in lessons_by_day.items():  # creating the actual timetable
            lesson = lessons.pop(0) if len(lessons) > 0 else None
            current_time_slot = min_time
            while current_time_slot < max_time:
                next_time_slot = (
                    dt.datetime.combine(dt.date.min, current_time_slot)
                    + dt.timedelta(minutes=time_interval)
                ).time()

                if (
                    lesson is not None
                    and lesson.get_approximated_start_time <= current_time_slot
                    and lesson.get_approximated_end_time >= next_time_slot
                ):
                    data[day].append(lesson)
                else:
                    data[day].append(
                        ""
                    )  # if there is no lesson, we have to fill the time slot anyway

                if lesson is not None and lesson.end_time <= next_time_slot:
                    lesson = lessons.pop(0) if len(lessons) > 0 else None

                current_time_slot = next_time_slot

        context["df"] = pd.DataFrame(data, index=index)

        return context


class LessonOverlapErrorView(LoginRequiredMixin, TemplateView):
    template_name = "reservation_management/lesson_overlap_error.html"


class NoLessonsErrorView(LoginRequiredMixin, TemplateView):
    template_name = "reservation_management/no_lessons_error.html"


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

    return JsonResponse({"ok", True})


@login_required
@require_POST
@csrf_protect
def ajax_instagram_confirm(request):
    """
    View called by an ajax function, it confirms that a user saw the Instagram modal.
    """
    user = request.user
    user.instagram = False
    user.save()

    return JsonResponse({"ok", True})
