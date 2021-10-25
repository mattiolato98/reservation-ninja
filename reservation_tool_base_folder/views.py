from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from reservation_tool_base_folder.decorators import not_authenticated_only


@method_decorator(not_authenticated_only, name='dispatch')
class HomepageView(TemplateView):
    template_name = 'home.html'


class HelpView(TemplateView):
    template_name = 'help.html'
