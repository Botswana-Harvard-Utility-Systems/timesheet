from edc_base.model_mixins import BaseUuidModel
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_search.model_mixins import SearchSlugModelMixin
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.deletion import PROTECT
from django.db import models

from bhp_personnel.models import Employee, Supervisor

from ..choices import ENTRY_TYPE, STATUS, OFF_DAY, HALF_DAY, REGULAR_DAY, NOT_STARTED


class MonthlyEntry(SiteModelMixin, SearchSlugModelMixin, BaseUuidModel):
    employee = models.ForeignKey(Employee, on_delete=PROTECT)

    month = models.DateField()

    comment = models.TextField(
        max_length=100,
        blank=True,
        null=True)

    employee_comment = models.TextField(
        max_length=100,
        blank=True,
        null=True)

    submitted_datetime = models.DateTimeField(
        blank=True,
        null=True)

    status = models.CharField(
        max_length=10,
        choices=STATUS,
        default='draft')

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

    def __str__(self):
        return (f'{self.employee} {self.month}')

    def save(self, *args, **kwargs):
        if self.status == 'rejected':
            self._reset_approval_fields()
        if self.status == 'submitted':
            kwargs = self._reset_prev_reject_fields(**kwargs)
        super().save(*args, **kwargs)

    @property
    def total_hours(self):
        daily_entries = DailyEntry.objects.filter(monthly_entry=self)
        total_hours = sum(entry.duration for entry in daily_entries)
        total_minutes = sum(entry.duration_minutes for entry in daily_entries)
        total_hours += total_minutes // 60
        return total_hours

    @property
    def status_badge_color(self):
        if self.status == 'draft':
            return 'primary'
        elif self.status in ['approved', 'verified']:
            return 'success'
        elif self.status == 'submitted':
            return 'info'
        elif self.status == 'rejected':
            return 'danger'

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

    def _reset_approval_fields(self):
        if any([self.approved_by, self.approved_date,
                self.verified_by, self.verified_date]):
            self.approved_by = None
            self.approved_date = None
            self.verified_by = None
            self.verified_date = None

    def _reset_prev_reject_fields(self, **kwargs):
        if any([self.rejected_by, self.rejected_date, ]):
            self.rejected_by = None
            self.rejected_date = None

            overwrite = {'rejected_by', 'rejected_date'}
            update_fields = kwargs.get('update_fields')
            if update_fields is not None:
                update_fields = set(update_fields) | overwrite
                kwargs['update_fields'] = list(update_fields)
        return kwargs

    @property
    def is_final(self):
        return self.status == 'verified'

    class Meta:
        app_label = 'timesheet'
        unique_together = ('month', 'employee')


class DailyEntry(BaseUuidModel):
    monthly_entry = models.ForeignKey(
        MonthlyEntry, on_delete=PROTECT, related_name='daily_entries')

    day = models.DateField()

    duration = models.IntegerField(
        validators=[MinValueValidator(0)])

    duration_minutes = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(59)],
        default=0,
    )

    row = models.IntegerField(
        validators=[MinValueValidator(0)],
        null=True,
        blank=True)

    entry_type = models.CharField(
        max_length=10,
        choices=ENTRY_TYPE,
        default=REGULAR_DAY)

    day_indicator = models.BooleanField(
        default=False,
        null=True,
        blank=True)

    feeding_hour = models.BooleanField(
        default=False,
        null=True,
        blank=True)

    @property
    def half_day_hours(self):
        return getattr(settings, 'TIMESHEET_HALF_DAY_HOURS', 4)

    @property
    def max_day_hours(self):
        return getattr(settings, "TIMESHEET_REGULAR_DAY_HOURS", 24)

    def clean(self):
        if (self.day.year != self.monthly_entry.month.year or
                self.day.month != self.monthly_entry.month.month):
            raise ValidationError('Date must be within the monthly period.')

        employee_comment = self.monthly_entry.employee_comment
        hours = int(self.duration) if self.duration is not None else None
        if self.entry_type == OFF_DAY:
            if hours is not None and hours != 0 and not bool(employee_comment):
                raise ValidationError(
                    {'duration':
                     'Please add employee comment for hours added on Off day(s). '
                     'Otherwise Off day must have 0 hours.'})
        elif self.entry_type == HALF_DAY:
            if hours is None:
                raise ValidationError(
                    {'duration':
                     f'Half day requires {self.half_day_hours} hours.'})
            if hours != self.half_day_hours:
                raise ValidationError(
                    {'duration':
                     f'Half day must be exactly {self.half_day_hours} hours.'})
        elif self.entry_type == REGULAR_DAY:
            if hours is not None and (hours < 1 or hours > self.max_day_hours):
                raise ValidationError(
                    {'duration':
                     f'Regular hours must be between 1 and {self.max_day_hours}.'})
        elif self.entry_type == NOT_STARTED:
            if hours is not None and hours != 0:
                raise ValidationError(
                    {'duration':
                     'Not started hours must be 0.'})

    class Meta:
        app_label = 'timesheet'
        unique_together = ('monthly_entry', 'day', 'entry_type')
        ordering = ['day']
