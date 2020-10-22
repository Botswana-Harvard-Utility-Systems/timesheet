from edc_base.model_mixins import BaseUuidModel
from django.db.models.deletion import PROTECT
from django.db import models
from django.core.validators import MinValueValidator
from bhp_personnel.models import Employee


from ..choices import entry_type

class MonthlyEntry(BaseUuidModel):
    
    employee = models.ForeignKey(Employee, on_delete=PROTECT)
    
    month = models.DateField()

class DailyEntry(BaseUuidModel):
    
    monthly_entry = models.ForeignKey(MonthlyEntry, on_delete=PROTECT)
    
    day = models.DateField(
        unique=True)
    
    duration = models.IntegerField(
        validators=[MinValueValidator(0)])
    
    entry_type = models.CharField(
        max_length=10,
        choices=entry_type)
    
    