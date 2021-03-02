from django.apps import AppConfig as DjangoAppConfig
from edc_base.apps import AppConfig as BaseEdcBaseAppConfig


class AppConfig(DjangoAppConfig):
    name = 'timesheet'
    verbose_name = 'Timesheets'
    admin_site_name = 'timesheet_admin'
