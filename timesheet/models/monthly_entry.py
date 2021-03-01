from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import date_not_future
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_search.model_mixins import SearchSlugModelMixin
from django.db.models.deletion import PROTECT
from django.db import models
from django.core.validators import MinValueValidator
from bhp_personnel.models import Employee, Supervisor


from ..choices import ENTRY_TYPE, STATUS

class MonthlyEntry(SiteModelMixin, SearchSlugModelMixin, BaseUuidModel):

    employee = models.ForeignKey(Employee, on_delete=PROTECT)

    supervisor = models.ForeignKey(Supervisor, on_delete=PROTECT)

    month = models.DateField()

    comment = models.TextField(
         max_length=100,
         blank=True,
         null=True)

    status = models.CharField(
        max_length=10,
        choices=STATUS,
        default='new')

    @property
    def total_hours(self):
        daily_entries = DailyEntry.objects.filter(monthly_entry=self)

        total_hours = 0

        for h in daily_entries:
            total_hours += h.duration
        return total_hours

    def get_search_slug_fields(self):
        fields = super().get_search_slug_fields()
        fields.append('employee')
        fields.append('supervisor')
        return fields

    class Meta:
        app_label = 'timesheet'
        unique_together = ('month', 'employee')

class DailyEntry(BaseUuidModel):

    monthly_entry = models.ForeignKey(MonthlyEntry, on_delete=PROTECT)

    day = models.DateField()

    duration = models.IntegerField(
        validators=[MinValueValidator(0)])

    row = models.IntegerField(
        validators=[MinValueValidator(0)])

    entry_type = models.CharField(
        max_length=10,
        choices=ENTRY_TYPE,
        default='reg_hours')

    class Meta:
        app_label = 'timesheet'
        unique_together = ('monthly_entry', 'day', 'entry_type')


