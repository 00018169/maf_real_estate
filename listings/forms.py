from django import forms
from .models import Property, Appointment

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'title', 'description', 'property_type', 'price', 
            'bedrooms', 'bathrooms', 'area', 'floors_total',
            'city', 'address', 'year_built', 'last_major_renovation_at',
            'has_gas', 'has_electricity', 'has_internet',
            'image'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'price': forms.NumberInput(attrs={'step': '1', 'min': '0'}),
            'last_major_renovation_at': forms.DateInput(attrs={'type': 'date'}),
        }

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['start_time', 'message']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'message': forms.Textarea(attrs={'rows': 3}),
        }
