from django.apps import apps as django_apps
from django.views.generic import TemplateView
from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin


class HomeView(EdcBaseViewMixin, NavbarViewMixin, TemplateView):

    template_name = 'timesheet/home.html'
    navbar_name = 'timesheet'
    navbar_selected_item = 'home'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
                groups=[g.name for g in self.request.user.groups.all()],)
        return context
