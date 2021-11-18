from crispy_forms.helper import FormHelper
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from crispy_forms.layout import Layout, Row, Column, Submit
from django import forms

from reservation_management.models import Lesson


class LessonForm(forms.ModelForm):
    """
    Form used to create or update a lesson.
    """
    helper = FormHelper()

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(LessonForm, self).__init__(*args, **kwargs)

        self.helper.layout = Layout(
            Row(
                Column('day', css_class='form-group mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('start_time', css_class='form-group'),
                Column('end_time', css_class='form-group'),
                css_class='form-row',
            ),
            Row(
                Column('classroom', css_class='form-group mb-0'),
                Column(
                    Submit('submit', _('Insert'), css_class="btn site-btn mb-3 w-75 font-5"),
                    css_class='d-flex align-items-end justify-content-end'
                ),
                css_class='form-row '
            ),
        )

    def check_time_overlap(self):
        idx = 0

        # TODO: come formattare bene questa riga? Assegnare nomi a variabili?
        while idx < len(self.request.user.get_day_lessons(self.cleaned_data["day"])) \
                and self.cleaned_data["start_time"] >= self.request.user.get_day_lessons(
                self.cleaned_data["day"])[idx].end_time:
            idx += 1

        if idx < len(self.request.user.get_day_lessons(self.cleaned_data["day"])) \
                and self.cleaned_data["end_time"] > self.request.user.get_day_lessons(
                self.cleaned_data["day"])[idx].start_time:
            return False

        return True

        # the new lesson is after all the other lessons
        # if idx == len(self.request.user.get_day_lessons(self.cleaned_data["day"])):
        #     return True
        # if self.cleaned_data["end_time"] <= self.request.user.get_day_lessons(self.cleaned_data["day"])[idx].start_time:
        #     return True
        # else:
        #     return False

    def clean(self):
        if not self.check_time_overlap():
            raise ValidationError(_('You have already a lesson in this time interval'))

        return super(LessonForm, self).clean()

    class Meta:
        model = Lesson
        fields = (
            "day",
            "start_time",
            "end_time",
            "classroom",
        )
        labels = {
            'day': _('Day'),
            'start_time': _('Start time'),
            'end_time': _('End time'),
            'classroom': _('Classroom'),

        }
        widgets = {
            'day': forms.Select(attrs={'class': 'selectpicker', 'data-live-search': 'true'}),
            'classroom': forms.Select(attrs={'class': 'selectpicker', 'data-live-search': 'true'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}, format='%H:%M'),
            'end_time': forms.TimeInput(attrs={'type': 'time'}, format='%H:%M'),
        }
