from django.utils.translation import gettext_lazy as _
from django.template.defaulttags import register


@register.filter
def get_day_from_int(day_idx):
    weekdays = {
        0: _("Monday"),
        1: _("Tuesday"),
        2: _("Wednesday"),
        3: _("Thursday"),
        4: _("Friday"),
    }
    return weekdays.get(day_idx, None)
