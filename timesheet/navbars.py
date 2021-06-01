from django.conf import settings
from edc_navbar import NavbarItem, site_navbars, Navbar


timesheet = Navbar(name='timesheet')

timesheet.append_item(
    NavbarItem(
        name='employee_timesheet',
        label='Timesheets',
        icon='fas fa-stopwatch',
        url_name=settings.DASHBOARD_URL_NAMES.get('timesheet_home_url')))

site_navbars.register(timesheet)
