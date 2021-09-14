from django import forms
from django.forms import ModelForm
from .models import Contact
import time

# todo automate the date for the form based on time, so fall 2021 etc so I don't need to manually update it. the date to pick is right before

class IndexForm(forms.Form):
    class_name = forms.CharField(label='class name', max_length=100)
    CHOICES = [('202109', 'Fall 2021'),
               ('202201', 'Winter 2022')]
    term = forms.CharField(label='term', widget=forms.RadioSelect(choices=CHOICES))

class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
        field_order = [ "email", "subject", "message"]
