from django import forms
from ..models import MonthlyEntry, DailyEntry


class MonthlyEntryForm(forms.ModelForm):

    month = forms.DateField(
        widget=forms.SelectDateWidget()
        )

    class Meta:
        model = MonthlyEntry
        fields = '__all__'


class DailyEntryForm(forms.ModelForm):

#     def clean(self):
#         cleaned_data = super().clean()

    class Meta:
        model = DailyEntry
        fields = '__all__'
