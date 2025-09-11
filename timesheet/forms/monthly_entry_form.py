from django import forms
from django.forms.models import inlineformset_factory

from ..models import MonthlyEntry, DailyEntry
from ..choices import REGULAR_DAY


class MonthlyEntryForm(forms.ModelForm):

    class Meta:
        model = MonthlyEntry
        fields = []


class DailyEntryForm(forms.ModelForm):
    # Flipped to True in the view when user clicks "Submit" (strict validation)
    strict = False

    class Meta:
        model = DailyEntry
        fields = ['day', 'duration', 'entry_type']
        widgets = {
            'day': forms.DateInput(
                attrs={'type': 'date', 'readonly': True}),
        }

    def clean(self):
        cleaned = super().clean()
        entry_type = cleaned.get('entry_type')
        hours = cleaned.get('duration')

        # If user is submitting, enforce presence of hours for REGULAR
        if self.strict and entry_type == REGULAR_DAY:
            if hours is None:
                raise forms.ValidationError(
                    {'entry_type':
                     'Please provide hours for regular days (or mark it as Off/Half).'})

        return cleaned


DailyEntryFormSet = inlineformset_factory(
    MonthlyEntry,
    DailyEntry,
    form=DailyEntryForm,
    extra=0,
    can_delete=False)
