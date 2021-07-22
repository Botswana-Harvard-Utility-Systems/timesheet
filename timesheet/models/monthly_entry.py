from edc_base.model_mixins import BaseUuidModel
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_search.model_mixins import SearchSlugModelMixin
from django.db.models.deletion import PROTECT
from django.db import models
from django.core.validators import MinValueValidator
from bhp_personnel.models import Employee, Supervisor
from datetime import datetime, timedelta, time
import datetime

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

    monthly_overtime = models.CharField(
        max_length=100,
        blank=True,
        default='0')

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
        totalHours = timedelta(hours=0, minutes=0)
        for daily_entry in daily_entries:
            totalHours += timedelta(hours=daily_entry.duration.hour,
                                    minutes=daily_entry.duration.minute)

        if totalHours and totalHours.days > 0:
            minutes, seconds = divmod(
                totalHours.seconds + totalHours.days * 86400, 60)
            hours, minutes = divmod(minutes, 60)
            totalHours = f'{hours:d}:{minutes:02d}'

        return str(totalHours)

    def get_search_slug_fields(self):
        fields = super().get_search_slug_fields()
        fields.append('employee')
        # fields.append('employee__supervisor')
        return fields

    def __str__(self):
        return(f'{self.employee} {self.month}')

    class Meta:
        app_label = 'timesheet'
        unique_together = ('month', 'employee')


class DailyEntry(BaseUuidModel):

    monthly_entry = models.ForeignKey(MonthlyEntry, on_delete=PROTECT)

    day = models.DateField()

    duration = models.TimeField(auto_now=False, auto_now_add=False)

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
