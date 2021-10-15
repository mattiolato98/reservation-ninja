from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
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
                css_class='form-row'
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
        widgets = {
            'day': forms.Select(attrs={'class': 'selectpicker', 'data-live-search': 'true'}),
            'classroom': forms.Select(attrs={'class': 'selectpicker', 'data-live-search': 'true'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

