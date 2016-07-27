from django.contrib.auth.models import User
from django import forms

from .models import Preferences, Writing

class PreferencesForm(forms.ModelForm):
    class Meta:
        model = Preferences
        fields = ['num_words']
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
