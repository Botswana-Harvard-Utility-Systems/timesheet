from django.contrib import admin
from edc_model_admin import TabularInlineMixin

from ..models import DailyEntry, MonthlyEntry
from ..forms import DailyEntryForm, MonthlyEntryForm
from ..admin_site import timesheet_admin


class DailyEntryInlineAdmin(TabularInlineMixin, admin.TabularInline):
    model = DailyEntry
    form = DailyEntryForm
    
    fieldsets = (
        (None, {
            'fields': [
                'monthly_entry',
                'day',
                'regular_hours',
                'entry_type']}
         ),)

@admin.register(MonthlyEntry, site=timesheet_admin)
class MonthlyEntryAdmin(admin.ModelAdmin):
    
    form = MonthlyEntryForm
    
    fieldsets = (
        (None, {
            'fields': [
                'employee',
                'department',
                'title',
                'month']
            }),)
    
    inlines = [DailyEntryInlineAdmin, ]
    