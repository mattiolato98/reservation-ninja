from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, HTML
from django.utils.translation import gettext_lazy as _
from django import forms

from reservation_management.models import Lesson

"""
per i giorni della settimana fornire in input una lista, lato server tradurre i giorni in numero.
ottenere questo con un dizionario, ad ogni giorno della settimana (chiave), è associato il corrispettivo indice 
numerico (valore) 
"""


class LessonForm(forms.ModelForm):
    helper = FormHelper()

    weekday = forms.ChoiceField(choices=[
        (0, _("Monday")),
        (1, _("Tuesday")),
        (2, _("Wednesday")),
        (3, _("Thursday")),
        (4, _("Friday")),
    ],
        widget=forms.Select(
            attrs={
                'class': 'selectpicker',
                'data-live-search': 'true',
                'data-dropdown-align-right': 'true'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper.layout = Layout(
            Row(
                Column('weekday', css_class='form-group mb-0'),
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
            'classroom': forms.Select(attrs={'class': 'selectpicker', 'data-live-search': 'true'}),
        }

