from django import forms
from ..models import MonthlyEntry, DailyEntry


class MonthlyEntryForm(forms.ModelForm):


    class Meta:
        model = MonthlyEntry
        fields = '__all__'
        

class DailyEntryForm(forms.ModelForm):


    class Meta:
        model = DailyEntry
        fields = '__all__'