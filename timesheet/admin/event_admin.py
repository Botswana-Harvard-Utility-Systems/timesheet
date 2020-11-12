from django.contrib import admin
import datetime
import calendar
from django.urls import reverse
from calendar import HTMLCalendar
from django.utils.safestring import mark_safe

from ..admin_site import timesheet_admin
from ..models import Event
from ..forms import EventForm
 
    
@admin.register(Event, site=timesheet_admin)
class EventAdmin(admin.ModelAdmin):
    
    form = EventForm
    
    fieldsets = (
        (None, {
            'fields': [
                'day',
                'start_time',
                'end_time',
                'notes']
            }),)
    
    list_display = ['day', 'start_time', 'end_time', 'notes']
    
    change_list_template = 'admin/timesheet/change_list.html'
 
    def changelist_view(self, request, extra_context=None):
        after_day = request.GET.get('day__gte', None)
        extra_context = extra_context or {}
        if not after_day:
            d = datetime.date.today()
        else:
            try:
                split_after_day = after_day.split('-')
                d = datetime.date(year=int(split_after_day[0]), month=int(split_after_day[1]), day=1)
            except:
                d = datetime.date.today()
 
        previous_month = datetime.date(year=d.year, month=d.month, day=1)  # find first day of current month
        previous_month = previous_month - datetime.timedelta(days=1)  # backs up a single day
        previous_month = datetime.date(year=previous_month.year, month=previous_month.month,
                                       day=1)  # find first day of previous month
 
        last_day = calendar.monthrange(d.year, d.month)
        next_month = datetime.date(year=d.year, month=d.month, day=last_day[1])  # find last day of current month
        next_month = next_month + datetime.timedelta(days=1)  # forward a single day
        next_month = datetime.date(year=next_month.year, month=next_month.month,
                                   day=1)  # find first day of next month
 
        extra_context['previous_month'] = reverse('admin:timesheet_scheduling_changelist') + '?day__gte=' + str(
            previous_month)
#         request.resolver_match.url_name + '?day__gte=' + str(
#             previous_month)
#         reverse('admin:timesheet_event_changelist') + '?day__gte=' + str(
#             previous_month)
        extra_context['next_month'] = reverse('admin:timesheet_scheduling_changelist') + '?day__gte=' + str(next_month)
#         request.resolver_match.url_name + '?day__gte=' + str(next_month)
#         reverse('admin:timesheet_event_changelist') + '?day__gte=' + str(next_month)
 
        cal = HTMLCalendar()
        html_calendar = cal.formatmonth(d.year, d.month, withyear=True)
        html_calendar = html_calendar.replace('<td ', '<td  width="150" height="150"')
        extra_context['calendar'] = mark_safe(html_calendar)
        return super().changelist_view(request, extra_context)
    