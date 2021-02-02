from django.contrib import admin
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.widgets import DateInput
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch
from edc_model_admin import audit_fieldset_tuple, TabularInlineMixin, ModelAdminReadOnlyMixin
from edc_model_admin import ModelAdminNextUrlRedirectMixin, ModelAdminAuditFieldsMixin
from edc_model_admin import ModelAdminNextUrlRedirectError
from ..models import DailyEntry, MonthlyEntry
from ..forms import DailyEntryForm, MonthlyEntryForm
from ..admin_site import timesheet_admin
import calendar
from calendar import HTMLCalendar
import datetime
from .event_calender import EventCalendar
from django.utils.safestring import mark_safe


class DailyEntryInlineAdmin(TabularInlineMixin,
                            admin.TabularInline):
    model = DailyEntry
    form = DailyEntryForm
    extra = 0
    template = 'timesheet/timesheet_templates/timesheet.html'
    
    fieldsets = (
        (None, {
            'fields': [
                'monthly_entry',
                'day',
                'duration',
                'entry_type']}
         ),)
    
    def has_change_permission(self, request, obj):
        if obj:
            return request.user.username == obj.user_created
        else:
            return True
    
    def has_add_permission(self, request, obj):
        if obj:
            return request.user.username == obj.user_created
        else:
            return True
        
    

@admin.register(MonthlyEntry, site=timesheet_admin)
class MonthlyEntryAdmin(ModelAdminNextUrlRedirectMixin,
                        ModelAdminAuditFieldsMixin,
                        ModelAdminReadOnlyMixin,
                        admin.ModelAdmin):
    
    form = MonthlyEntryForm
    
    fieldsets = (
        (None, {
            'fields': [
                'employee',
                'month',
                'supervisor',
                'comment']
            }),audit_fieldset_tuple)
    
    inlines = [DailyEntryInlineAdmin, ]
    
    def redirect_url(self, request, obj, post_url_continue=None):
        redirect_url = super().redirect_url(
            request, obj, post_url_continue=post_url_continue)
        if request.POST.get('_approve'):
            obj.status = 'approved'
            obj.save()
        elif request.POST.get('_reject'):
            obj.status = 'rejected'
            obj.save()
        elif request.POST.get('_verify'):
            obj.status = 'verified'
            obj.save()
            
        if request.GET.dict().get('next'):
            url_name = request.GET.dict().get('next').split(',')[0]
            attrs = request.GET.dict().get('next').split(',')[1:]
            options = {k: request.GET.dict().get(k)
                       for k in attrs if request.GET.dict().get(k)}
            try:
                redirect_url = reverse(url_name, kwargs=options)
            except NoReverseMatch as e:
                raise ModelAdminNextUrlRedirectError(
                    f'{e}. Got url_name={url_name}, kwargs={options}.')
        return redirect_url
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj and obj.status not in ['new', 'rejected']:
            for form_field in form.base_fields.values():
                form_field.disabled = True
                try:
                    form_field.widget.can_add_related = False
                    form_field.widget.can_change_related = False
                    form_field.widget.can_delete_related = False
                except AttributeError:
                    pass
                if isinstance(form_field.widget, AdminDateWidget):
                    form_field.widget = DateInput()
        return form
#             request.GET['edc_readonly'] = '1'
#         return super().get_form(request, obj, **kwargs)

#     def add_view(self, request, extra_context=None):
#         after_day = request.GET.get('day__gte', None)
#         extra_context = extra_context or {}
#         if not after_day:
#             d = datetime.date.today()
#         else:
#             try:
#                 split_after_day = after_day.split('-')
#                 d = datetime.date(year=int(split_after_day[0]), month=int(split_after_day[1]), day=1)
#             except:
#                 d = datetime.date.today()
# 
#         previous_month = datetime.date(year=d.year, month=d.month, day=1)  # find first day of current month
#         previous_month = previous_month - datetime.timedelta(days=1)  # backs up a single day
#         previous_month = datetime.date(year=previous_month.year, month=previous_month.month,
#                                        day=1)  # find first day of previous month
# 
#         last_day = calendar.monthrange(d.year, d.month)
#         next_month = datetime.date(year=d.year, month=d.month, day=last_day[1])  # find last day of current month
#         next_month = next_month + datetime.timedelta(days=1)  # forward a single day
#         next_month = datetime.date(year=next_month.year, month=next_month.month,
#                                    day=1)  # find first day of next month
# 
#         extra_context['previous_month'] = reverse('timesheet_admin:timesheet_event_changelist') + '?day__gte=' + str(
#             previous_month)
#         request.resolver_match.url_name + '?day__gte=' + str(previous_month)
#         reverse('timesheet_admin:timesheet_event_changelist') + '?day__gte=' + str(
#                                                                                    previous_month)
#         extra_context['next_month'] = reverse('timesheet_admin:timesheet_event_changelist') + '?day__gte=' + str(next_month)
#         request.resolver_match.url_name + '?day__gte=' + str(next_month)
#         reverse('timesheet_admin:timesheet_event_changelist') + '?day__gte=' + str(next_month)
# 
#         cal = EventCalendar()
#         html_calendar = cal.formatmonth(d.year, d.month, withyear=True)
#         html_calendar = html_calendar.replace('<td ', '<td  width="150" height="150"')
#         extra_context['calendar'] = mark_safe(html_calendar)
#         return super().changelist_view(request, extra_context)

    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        if (request.GET.get('p_role') == 'Supervisor'):
            extra_context = {'review': True}
        if (request.GET.get('p_role')=='HR'):
            extra_context = {'verify': True}
#         if self.get_object(request, object_id).status not in ['new', 'rejected']:
#             extra_context = {'edc_readonly' : 1}
        return super().change_view(
            request, object_id, form_url=form_url, extra_context=extra_context)
