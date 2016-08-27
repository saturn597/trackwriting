from django import forms

from .models import UserInfo, Writing


class PreferencesForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['num_words', 'timezone']
        help_texts = {
            'num_words': 'How many words do you want to write per day?',
        }
        labels = {
            'num_words': 'Words per day:',
        }
        error_messages = {
            'num_words': {
                'required': 'Please give a number of words per day.',
            },
        }


class WritingForm(forms.ModelForm):
    class Meta:
        fields = ['title', 'text']
        model = Writing
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title'}),
            'text': forms.Textarea(attrs={'placeholder': 'Write here!'}),
        }
        error_messages = {
            'title': {
                'max_length': 'Whoops! That title\'s a bit too long!',
                'required': 'Please give your work a title and try saving '
                            'again.',
            },
            'text': {
                'required': 'You didn\'t write anything - please write '
                            'something. :)',
            },
        }
