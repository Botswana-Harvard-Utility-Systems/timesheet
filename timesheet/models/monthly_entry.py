from edc_base.model_mixins import BaseUuidModel
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_search.model_mixins import SearchSlugModelMixin
from django.db.models.deletion import PROTECT
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from bhp_personnel.models import Employee, Supervisor

from ..choices import ENTRY_TYPE, STATUS


class MonthlyEntry(SiteModelMixin, SearchSlugModelMixin, BaseUuidModel):
    employee = models.ForeignKey(Employee, on_delete=PROTECT)

    month = models.DateField()

    comment = models.TextField(
        max_length=100,
        blank=True,
        null=True)

    submitted_datetime = models.DateTimeField(
        blank=True,
        null=True)

    status = models.CharField(
        max_length=10,
        choices=STATUS,
        default='new')

    monthly_overtime = models.IntegerField(
        default=0)

    annual_leave_taken = models.IntegerField(
        default=0)

    sick_leave_taken = models.IntegerField(
        default=0)

    study_leave_taken = models.IntegerField(
        default=0)

    compassionate_leave_taken = models.IntegerField(
        default=0)

    maternity_leave_taken = models.IntegerField(
        default=0)

    paternity_leave_taken = models.IntegerField(
        default=0)

    approved_by = models.CharField(
        max_length=50,
        blank=True,
        null=True)

    approved_date = models.DateField(
        blank=True,
        null=True)

    verified_by = models.CharField(
        max_length=50,
        blank=True,
        null=True)

    verified_date = models.DateField(
        blank=True,
        null=True)

    rejected_by = models.CharField(
        max_length=50,
        blank=True,
        null=True)

    rejected_date = models.DateField(
        blank=True,
        null=True)

    @property
    def total_hours(self):
        daily_entries = DailyEntry.objects.filter(monthly_entry=self)
        total_hours = sum(entry.duration for entry in daily_entries)
        total_minutes = sum(entry.duration_minutes for entry in daily_entries)
        total_hours += total_minutes / 60
        return total_hours

    def readable_total_hours(self):
        hours = int(self.total_hours)
        minutes = int((self.total_hours - hours) * 60)
        time_string = f"{hours:02d} hours and {minutes:02d} minutes"
        return time_string

    def get_search_slug_fields(self):
        fields = super().get_search_slug_fields()
        fields.append('employee')
        # fields.append('employee__supervisor')
        return fields

    def __str__(self):
        return (f'{self.employee} {self.month}')

    class Meta:
        app_label = 'timesheet'
        unique_together = ('month', 'employee')


class DailyEntry(BaseUuidModel):
    monthly_entry = models.ForeignKey(MonthlyEntry, on_delete=PROTECT)

    day = models.DateField()

    duration = models.IntegerField(
        validators=[MinValueValidator(0)])

    duration_minutes = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(59)],
        default=0,
    )

    row = models.IntegerField(
        validators=[MinValueValidator(0)])

    entry_type = models.CharField(
        max_length=10,
        choices=ENTRY_TYPE,
        default='reg_hours')

    day_indicator = models.BooleanField(
        default=False,
        null=True,
        blank=True)

    feeding_hour = models.BooleanField(
        default=False,
        null=True,
        blank=True)

    class Meta:
        app_label = 'timesheet'
        unique_together = ('monthly_entry', 'day', 'entry_type')
