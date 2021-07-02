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
                groups=[g.name for g in self.request.user.groups.all()],
                employee_id=self.employee_id)
        return context

    @property
    def employee_id(self):
        employee_cls = django_apps.get_model('bhp_personnel.employee')

        try:
            employee_obj = employee_cls.objects.get(email=self.request.user.email)

        except employee_cls.DoesNotExist:
            consultant_cls = django_apps.get_model('bhp_personnel.consultant')
            try:
                consultant_obj = consultant_cls.objects.get(email=self.request.user.email)
            except consultant_cls.DoesNotExist:
                return None
            else:
                return consultant_obj.identifier
        except employee_cls.MultipleObjectsReturned:
            raise
        else:
            return employee_obj.identifier
