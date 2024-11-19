from django import forms
from .models import ContactMessage
from django_recaptcha.fields import ReCaptchaField
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class ContactForm(forms.ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message', 'captcha']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError('Invalid email format')
        return email

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message) < 10:
            raise forms.ValidationError('Message must be at least 10 characters long')
        return message
