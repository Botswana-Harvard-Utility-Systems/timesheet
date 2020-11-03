from django.conf import settings
from edc_navbar import NavbarItem, site_navbars, Navbar


timesheet = Navbar(name='timesheet')

timesheet.append_item(
    NavbarItem(
        name='employee_timesheet',
        label='My Timesheets',
        fa_icon='fa-clock-o',
        url_name=settings.DASHBOARD_URL_NAMES.get('timesheet_listboard_url')))

site_navbars.register(timesheet)
