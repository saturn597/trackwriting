from django import forms

from .models import Writing

class WritingForm(forms.ModelForm):
    class Meta:
        model = Writing
        fields = ['title', 'text']
        widgets = {
                    'title': forms.TextInput(attrs={'placeholder': 'Title'}),
                    'text': forms.Textarea(attrs={'placeholder': 'Write here!'}),
                }
