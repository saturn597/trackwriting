from django.contrib.auth.models import User
from django import forms

from .models import UserInfo, Writing

import pytz

class PreferencesForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['num_words', 'timezone']
        labels = {
                'num_words': 'How many words do you want to write per day?',
                }

class WritingForm(forms.ModelForm):
    class Meta:
        model = Writing
        fields = ['title', 'text']
        widgets = {
                    'title': forms.TextInput(attrs={'placeholder': 'Title'}),
                    'text': forms.Textarea(attrs={'placeholder': 'Write here!'}),
                }
