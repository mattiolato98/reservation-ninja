from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from app.reservation_tool_base_folder.decorators import not_authenticated_only


@method_decorator(not_authenticated_only, name='dispatch')
class HomepageView(TemplateView):
    template_name = '../templates/home.html'


class HelpView(TemplateView):
    template_name = '../templates/help.html'
