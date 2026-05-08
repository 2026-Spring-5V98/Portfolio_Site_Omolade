from django import forms
from .models import Appointment, ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Your full name',
                'class': 'form-control',
                'autocomplete': 'name',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'your@email.com',
                'class': 'form-control',
                'autocomplete': 'email',
            }),
            'subject': forms.TextInput(attrs={
                'placeholder': 'What is this about?',
                'class': 'form-control',
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Write your message here...',
                'class': 'form-control',
                'rows': 5,
            }),
        }


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['name', 'email', 'phone', 'date', 'time', 'purpose', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Your full name',
                'class': 'form-control',
                'autocomplete': 'name',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'your@email.com',
                'class': 'form-control',
                'autocomplete': 'email',
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'Phone (optional)',
                'class': 'form-control',
                'autocomplete': 'tel',
            }),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
            }),
            'time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control',
            }),
            'purpose': forms.TextInput(attrs={
                'placeholder': 'e.g. Job opportunity, Collaboration, Consultation',
                'class': 'form-control',
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Any additional context or notes...',
                'class': 'form-control',
                'rows': 4,
            }),
        }
