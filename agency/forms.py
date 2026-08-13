from django import forms
from .models import Package, Customer


class PackageForm(forms.ModelForm):

    class Meta:
        model = Package

        fields = [
            'destination',
            'image_url',
            'days',
            'nights',
            'price',
            'description',
            'inclusions',
            'exclusions',
            'is_active',
        ]

        widgets = {
            'destination': forms.TextInput(attrs={
                'placeholder': 'Enter destination'
            }),

            'image_url': forms.URLInput(attrs={
                'placeholder': 'Enter image URL'
            }),

            'days': forms.NumberInput(attrs={
                'min': '1',
                'placeholder': 'Number of days'
            }),

            'nights': forms.NumberInput(attrs={
                'min': '0',
                'placeholder': 'Number of nights'
            }),

            'price': forms.NumberInput(attrs={
                'min': '0',
                'step': '0.01',
                'placeholder': 'Package price'
            }),

            'description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Package description'
            }),

            'inclusions': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Example: Hotel, Breakfast, Sightseeing'
            }),

            'exclusions': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Example: Flight tickets, Personal expenses'
            }),
        }

class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer

        fields = [
            'full_name',
            'mobile',
            'email',
            'package',
            'travel_date',
            'message',
        ]