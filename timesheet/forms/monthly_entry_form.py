from django import forms
from ..models import MonthlyEntry, DailyEntry

BIRTH_YEAR_CHOICES = ['1980', '1981', '1982']
FAVORITE_COLORS_CHOICES = [
    ('blue', 'Blue'),
    ('green', 'Green'),
    ('black', 'Black'),
]

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
