from django.contrib import admin
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch
from edc_model_admin import audit_fieldset_tuple, TabularInlineMixin
from edc_model_admin import ModelAdminNextUrlRedirectMixin, ModelAdminAuditFieldsMixin
from ..models import DailyEntry, MonthlyEntry
from ..forms import DailyEntryForm, MonthlyEntryForm
from ..admin_site import timesheet_admin


class DailyEntryInlineAdmin(TabularInlineMixin, admin.TabularInline):
    model = DailyEntry
    form = DailyEntryForm
    extra = 1
    
    fieldsets = (
        (None, {
            'fields': [
                'monthly_entry',
                'day',
                'duration',
                'entry_type']}
         ),)

@admin.register(MonthlyEntry, site=timesheet_admin)
class MonthlyEntryAdmin(ModelAdminNextUrlRedirectMixin,
                        ModelAdminAuditFieldsMixin,
                        admin.ModelAdmin):
    
    form = MonthlyEntryForm
    
    fieldsets = (
        (None, {
            'fields': [
                'employee',
                'month']
            }),audit_fieldset_tuple)
    
    inlines = [DailyEntryInlineAdmin, ]
    
    def redirect_url(self, request, obj, post_url_continue=None):
        redirect_url = super().redirect_url(
            request, obj, post_url_continue=post_url_continue)
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
