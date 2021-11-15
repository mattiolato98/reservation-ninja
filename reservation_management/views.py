from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from reservation_management.decorators import lesson_owner_only
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
