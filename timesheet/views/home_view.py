from django.apps import apps as django_apps
from django.views.generic import TemplateView
from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin


class HomeView(EdcBaseViewMixin, NavbarViewMixin, TemplateView):

    template_name = 'timesheet/home.html'
    navbar_name = 'timesheet'
    navbar_selected_item = 'employee_timesheet'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            is_hr=self.request.user.groups.filter(name='HR').exists(),
            is_supervisor=self._is_supervisor,
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

    @property
    def _is_supervisor(self):
        user = self.request.user
        supervisor_cls = django_apps.get_model('bhp_personnel.supervisor')
        supervisor_group = user.groups.filter(name='Supervisor').exists()
        supervisor_instance = supervisor_cls.objects.filter(email=user.email).exists()
        return supervisor_group and supervisor_instance
