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
            'no_of_persons',
            'no_of_days',
            'budget',
            'travel_date',
            'message',
        ]

        widgets = {

            'full_name': forms.TextInput(attrs={
                'placeholder': 'Your Name'
            }),

            'mobile': forms.TextInput(attrs={
                'placeholder': 'Phone Number'
            }),

            'email': forms.EmailInput(attrs={
                'placeholder': 'Email Address'
            }),

            'package': forms.Select(attrs={
                'id': 'destination'
            }),

            'no_of_persons': forms.NumberInput(attrs={
                'min': '1',
                'placeholder': 'Number of Persons'
            }),

            'no_of_days': forms.NumberInput(attrs={
                'min': '1',
                'placeholder': 'Number of Days'
            }),

            'budget': forms.NumberInput(attrs={
                'min': '0',
                'step': '0.01',
                'placeholder': 'Budget'
            }),

            'travel_date': forms.DateInput(attrs={
                'type': 'date'
            }),

            'message': forms.Textarea(attrs={
                'placeholder': 'Tell us about your travel plans...'
            }),
        }