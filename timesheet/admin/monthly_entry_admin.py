from django.contrib import admin
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.widgets import DateInput
from django_revision.modeladmin_mixin import ModelAdminRevisionMixin
from edc_base.sites.admin import ModelAdminSiteMixin
from edc_model_admin import audit_fieldset_tuple, TabularInlineMixin
from edc_model_admin import (
    ModelAdminNextUrlRedirectMixin, ModelAdminFormInstructionsMixin,
    ModelAdminFormAutoNumberMixin, ModelAdminAuditFieldsMixin,
    ModelAdminReadOnlyMixin, ModelAdminInstitutionMixin,
    ModelAdminRedirectOnDeleteMixin)
from ..models import DailyEntry, MonthlyEntry
from ..forms import DailyEntryForm, MonthlyEntryForm
from ..admin_site import timesheet_admin


class DailyEntryInlineAdmin(TabularInlineMixin,
                            admin.TabularInline):
    model = DailyEntry
    form = DailyEntryForm
    extra = 0

    fieldsets = (
        (None, {
            'fields': [
                'monthly_entry',
                'day',
                'duration',
                'duration_minutes',
                'entry_type',
                'row',
                'day_indicator',
                'feeding_hour']}
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
                        ModelAdminFormInstructionsMixin,
                        ModelAdminFormAutoNumberMixin,
                        ModelAdminRevisionMixin,
                        ModelAdminAuditFieldsMixin,
                        ModelAdminReadOnlyMixin,
                        ModelAdminInstitutionMixin,
                        ModelAdminRedirectOnDeleteMixin,
                        ModelAdminSiteMixin, admin.ModelAdmin):

    form = MonthlyEntryForm

    fieldsets = (
        (None, {
            'fields': [
                'employee',
                'month',
                'supervisor',
                'comment']
            }), audit_fieldset_tuple)

    inlines = [DailyEntryInlineAdmin, ]

    list_display = ('employee', 'month', 'comment')

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

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if (request.GET.get('p_role') == 'Supervisor'):
            extra_context = {'review': True}
        if (request.GET.get('p_role') == 'HR'):
            extra_context = {'verify': True}
#         if self.get_object(request, object_id).status not in ['new', 'rejected']:
#             extra_context = {'edc_readonly' : 1}
        return super().change_view(
            request, object_id, form_url=form_url, extra_context=extra_context)
