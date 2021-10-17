from crispy_forms.helper import FormHelper
from django.utils.translation import gettext_lazy as _
from crispy_forms.layout import Layout, Row, Column, Submit
from django import forms

from reservation_management.models import Lesson

"""
per i giorni della settimana fornire in input una lista, lato server tradurre i giorni in numero.
ottenere questo con un dizionario, ad ogni giorno della settimana (chiave), è associato il corrispettivo indice 
numerico (valore) 
"""


class LessonForm(forms.ModelForm):
    helper = FormHelper()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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

