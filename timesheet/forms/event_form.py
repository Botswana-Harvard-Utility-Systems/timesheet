from django import forms
from ..models import Event

class EventForm(forms.ModelForm):
    
    month = forms.DateField(
        widget=forms.SelectDateWidget()
        )
    
    class Meta:
        model = Event
        fields = '__all__'
