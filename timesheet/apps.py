from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = 'timesheet'
    verbose_name = 'Timesheets'
    admin_site_name = 'timesheet_admin'
