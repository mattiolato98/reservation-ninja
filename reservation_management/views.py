from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from reservation_management.decorators import lesson_owner_only
from reservation_management.forms import LessonForm
from reservation_management.models import Lesson, Reservation, Log, Feedback
from user_management.decorators import manager_required


class LessonAddView(LoginRequiredMixin, CreateView):
    model = Lesson
    form_class = LessonForm
    template_name = "reservation_management/lesson_add.html"
    success_url = reverse_lazy("reservation_management:lesson-list")

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
    model = Reservation
    template_name = "reservation_management/reservation_list.html"

    def get_queryset(self):
        return Reservation.objects.filter(lesson__user=self.request.user)


@method_decorator(manager_required, name='dispatch')
class LogListView(ListView):
    model = Log
    template_name = "reservation_management/log_list.html"

    def get_queryset(self):
        return Log.objects.all().order_by('-date')


@method_decorator(manager_required, name='dispatch')
class FeedbackListView(ListView):
    model = Feedback
    template_name = "reservation_management/feedback_list.html"

    def get_queryset(self):
        feedbacks = Feedback.objects.all().order_by('-date', 'user')
        feedbacks_grouped_by_date = defaultdict(list)

        for feedback in feedbacks:
            feedbacks_grouped_by_date[feedback.date].append(feedback)

        # Dict cast is needed, because template see defaultdict as empty
        return dict(feedbacks_grouped_by_date)


@login_required
@require_POST
@csrf_protect
def ajax_send_feedback(request):
    user = request.user

    Feedback.objects.create(
        user=user,
        ok=bool(request.POST.get('response_ok')),
    )

    user.feedback = True
    user.save()

    return JsonResponse({'ok': True})


@login_required
@require_POST
@csrf_protect
def ajax_whats_new_confirm(request):
    user = request.user
    user.whats_new = False
    user.save()

    return JsonResponse({'ok', True})
